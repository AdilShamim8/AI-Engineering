# 19 — Online RAG Evaluation: Monitoring Production LLMs with LangSmith

> **Lecture 19 of 19** · Unit 4: Production Evaluation · 1:14:24
> Online RAG Evaluation: Monitoring Production LLMs with LangSmith with Code Demo (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/19-online-eval-langsmith-monitoring.md)

---

## What this lecture covers

The course finale. Across lectures 12–18 we built a complete **offline** eval suite for the CampusX Doubt Solve RAG chatbot — 14–15 metrics across retriever, generator, pipeline, application, safety, and operational levels — and tied it together with regression testing. This lecture takes the last step of lecture 3's workflow: **deploy, monitor, and keep evaluating forever**:

1. **The hard truth about going online** — a reference-based vs reference-free audit of every offline metric
2. **The six-metric online suite** — the RAG Triad for quality, toxicity for safety, latency and cost for operations
3. **Operational monitoring with LangSmith** — project setup, tracing, the `@traceable` fix, custom dashboards (P95 latency, average cost), Slack alerting (and the P95-alerting discovery)
4. **Safety online** — the built-in toxicity evaluator: judge model, sampling rate, async evaluation, interpretable 0–100 scores
5. **Quality online** — the golden rule (*the same evaluator offline and online*) and the cron-job + LangSmith-SDK workaround
6. **Closing the loop** — production failures back into the golden dataset, and why that dataset should live in LangSmith from day one

Everything is demonstrated live on the code base built in lectures 13–18. The instructor's standing advice: **learn the concept, not the tool** — today it's LangSmith, at your company it may be Langfuse or anything else, but the flow never changes.

---

## 1. Where we are: offline evals are done — now deploy (00:00–02:11)

This is the last session on RAG evals, and it is about **online evals**. The recap: we built an eval suite of **about 14–15 metrics**, and in the last lecture tied it up **in the form of regression testing** — so the complete **offline evaluation** story is done: test before deployment, and detect when changing a component or the system causes a **regression**. The obvious next step: **deploy**. The system goes online, people start using it — "but that does not mean you should stop evaluating your system." In an ideal situation, any company that deploys a chatbot or LLM-based application **continues to evaluate it even after deployment** — that process is **online evaluation**.

This is not a new concept: four or five classes ago (lecture 6) the instructor explained the whole theory of online evals — nothing was done practically there, but he showed that tools like **LangSmith** or **Langfuse** let you perform **observability, monitoring, and evaluation — all three**. Today we do exactly that, hands-on, under one framing assumption: the software we built, **CampusX Doubt Solve, has been deployed**. The plan of action: keep running evaluation tests continuously in the production environment, keep bringing that data to us, and keep observing it **just to see if our system is breaking anywhere**.

---

## 2. The hard truth: you cannot take all 14–15 metrics online (02:11–07:24)

The instructor puts up the chart of every metric from the offline eval suite:

| Level | Metrics |
|---|---|
| **Retriever** | Contextual recall, contextual precision |
| **Generator** | Faithfulness, answer relevancy |
| **RAG pipeline** | Contextual relevancy, faithfulness, answer relevancy |
| **Application** | Correctness, completeness, style |
| **Safety** | Scope, leakage, toxicity |
| **Operational** | Latency, cost, reliability |

The hard truth: **we cannot run all of these metrics online — it's not possible at all.** He challenges the class to say why, and praises the answer (from **Srinivas**): **we don't have a reference — we don't have the correct answer.**

This is the biggest difference between offline and online evaluation. **Offline**, you create **golden datasets** that include the correct answers — that's what lets you determine **correctness**: you can only know whether the chatbot's answer is correct if the correct answer exists somewhere, as a reference. **Online**, a user asks a **completely new question** — you cannot know in advance what users will ask in the future, so you cannot have their answers either. No reference → correctness can never be measured in an online setup.

In simple words: **any reference-based metric cannot be evaluated online.** He then makes the class perform the audit themselves ("recall the previous sessions and type it out — it will also be a good quick revision"):

| Level | Metric | Needs the correct answer? | Can it go online? |
|---|---|---|---|
| Retriever | Contextual recall | **Yes** — you must state what the correct chunk looks like | ❌ |
| Retriever | Contextual precision | **Yes** | ❌ |
| Generator | Faithfulness | No — **reference-free** | ✅ |
| Generator | Answer relevancy | No — reference-free | ✅ |
| Pipeline | Contextual relevancy | No — reference-free | ✅ |
| Pipeline | Faithfulness / answer relevancy | No (same as above) | ✅ |
| Application | Correctness | **Yes** | ❌ |
| Application | Completeness | **Yes** | ❌ |
| Application | Style | No — reference-free | ✅ |
| Safety | Scope, leakage, toxicity | Mostly reference-free | ✅ (all three) |
| Operational | Latency, cost, reliability | No reference needed — these are not "measured," they are just **logged** | ✅ |

So the reference-based rows are exactly what stays offline; everything else can come along.

---

## 3. Simplifying the suite: what we will and won't measure online (07:24–11:21)

Beyond the reference constraint, the instructor simplifies further — "I am simplifying things a bit here too":

- **No separate component-level generator eval.** He won't run the generator's faithfulness/answer relevancy in isolation; he will simply compute the three pipeline metrics — **"basically, I will run the RAG Triad in an online setup."**
- **Style is dropped.** Two reasons: (1) limited time — "how much can we do in a 2-hour session?"; (2) more interestingly, **style does not deviate much**. If your offline style score is around **80**, it will never happen that the chatbot suddenly goes online and the score drops to **30** — there just isn't that much variance in style. "We could, but theoretically, it doesn't seem necessary."
- **Safety: only toxicity will be demonstrated.** Scope, leakage, and toxicity are all doable online — he'll show one (toxicity); everything else remains exactly the same and you can do it yourself.
- **Reliability is dropped.** It needs external software tools like **Grafana and Prometheus**, which is a bit beyond the scope of this lecture.

The final **six-metric online eval suite**, to be built with **LangSmith**:

| Dimension | Metrics | Notes |
|---|---|---|
| **Quality** (3) | Contextual relevancy, faithfulness, answer relevancy | The RAG Triad, online |
| **Safety** (1) | Toxicity | Demonstrating one of the three safety metrics |
| **Operational** (2) | Latency, cost | The easiest to set up |

The goal of the class: **learn how to continuously monitor and evaluate your software once it is deployed.** The strategy is operational first — because it is the easiest: **as soon as you enable tracing** (log every trace in LangSmith), the system automatically starts fetching latency and cost; you don't need to do anything except connect your application. Then safety, then quality — and then the interesting parts: building our own dashboard, and creating **alerts** when a threshold is broken (e.g., if the faithfulness score drops below a certain threshold in the last hour, raise an alert).

---

## 4. Step 1 — Connect the app to LangSmith: project, API key, `.env` (11:21–15:22)

The instructor has the plan steps written down ("we just need to carry out these steps one by one") and the code base from the past few sessions open. First step: create a new project in LangSmith and connect the deployed application to it.

1. Go to **smith.langchain.com** and create an account (he simply used **Google login**).
2. Open the **Tracing** tab — on first visit it shows *"no tracing projects found."*
3. Go to **All Applications** → click the **plus button** → create a new application. He first tried the name **CampusX Doubt Solve**, but hit a naming conflict ("the tag value already exists" — he had been working on this before, so the name was already showing up and there was some problem). The fix: rename it to **CX Doubt Solve** ("CX as in CampusX Doubt Solve") so there are no conflicts. Create → the project view appears.
4. **Generate an API key** from the project page. (His key is visible on screen — "don't worry, I will delete this project after the class.")
5. Copy the key into the project's **`.env`** file, where the OpenAI API key already lives:

| Environment variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | already present (generator + judge model) |
| `LANGSMITH_TRACING=True` | switches tracing on |
| `LANGSMITH_ENDPOINT` | where traces are sent |
| `LANGSMITH_API_KEY` | the key just generated |
| `LANGSMITH_PROJECT` (project name: **CX Doubt Solve**) | which project the traces land in |
| ~~`ANTHROPIC_API_KEY`~~ | removed — not needed |

That's the entire setup: create an application, paste its environment variables, done — **the code is now connected to LangSmith**.

To verify, he runs the pipeline once (`rag_pipeline.py`, question: *"What is GSM8k?"*) with `python src.rag_pipeline` — and behind the scenes LangSmith automatically captures everything: question, context generation, answer generation. **You don't need to write a single line of code.**

> 💡 **Expert commentary.** LangSmith is one node in a fast-moving observability landscape, and it's worth knowing the alternatives by name: **Langfuse** (the open-source, self-hostable option the instructor himself names as the conceptual twin), **Arize Phoenix** (strong LLM-tracing + eval lineage), **W&B Weave**, **MLflow tracing**, and **Confident AI** (DeepEval's cloud). The deeper trend is standardization: **OpenTelemetry** is emerging as the vendor-neutral wire format for LLM traces (span-level GenAI semantic conventions), which is exactly what lets you swap the LangSmith backend later without re-instrumenting your app. The instructor's "concept over tool" advice is not modesty — it's the correct hedge.

---

## 5. First trace: latency and cost, for free (15:22–17:41)

Back in LangSmith, under the **CX Doubt Solve** project's Tracing tab, the **first trace** has been captured. Clicking it shows the question, the output (the answer), the context — and, importantly, a lot of other information that was captured automatically:

- **Latency** — how much time the whole run took: **4.14 seconds**
- **Cost** — what the run cost

Exactly as promised: the moment the app was connected to LangSmith, we started measuring the two operational metrics. The first task isn't complete yet, but it has started.

A student asks whether the latency includes the time tracing itself takes. No — **tracing happens asynchronously**, so it doesn't add separate time; it is an asynchronous operation.

---

## 6. The missing retriever: `@traceable` decorators (17:41–23:28)

But there's a problem. The trace shows only three stages for the end-to-end operation: forming the **prompt template** → sending it to **ChatOpenAI** (the LLM responds, ~4 seconds) → **string output parser** printing the answer. The instructor asks the class: were these really the only three stages in our RAG pipeline — or is something not visible?

**Shruti asks the right question: where is the retrieval?** There is no mention of retrieval anywhere in the sequence:

- Fetching documents from the **vector database** takes time — not shown.
- We also used a **reranker** — not shown either.

The default LangSmith behavior is somehow capturing only the generator side and not the retrieval part. The fix — taught in his LangSmith video as well: **whenever something is not being traced implicitly, explicitly tell LangSmith to trace it** using **traceable decorators**:

1. In the **RAG pipeline** file: wrap the `invoke` function with the decorator and name it **`'RAG Pipeline'`** — so the retriever's work also starts getting traced under it.
2. In the **reranker** file: add the same decorator above its `invoke` function and name it **`'Retriever'`** — "because essentially, our entire retrieval is running inside the reranker" (searching for similar items, then reranking them).

Re-running the pipeline captures a **second trace**. The name has changed to **'RAG Pipeline'** (because we told it to report that name), and now the trace contains the additional steps: the **Retriever** step, followed by the chat prompt template, ChatOpenAI, and the string output parser. Now the code is tracing everything — **so now you get the correct latency values**:

| Trace | What was counted | Latency |
|---|---|---|
| First run (auto-tracing) | prompt → LLM → parser only | **4.14 s** |
| Second run (with `@traceable`) | + retrieval/reranking | **4.79 s** |

The latency went *up* — correctly so, because previously retrieval wasn't being considered part of the process.

Two Q&A asides on this behavior: **why did it leave the retriever out but cover the generator on its own?** "I also found that behavior a bit tricky… I don't have the answer as to why this tricky behavior exists" — the practical conclusion stands: if something isn't traced, put a decorator on it. And **could explicitly tracing cause double logging?** No — "it happens in a **hierarchy**": you place a decorator at the top level, whatever you trace inside nests within that single high-level trace. "There is never any duplication. I have tried this out many times."

One prerequisite worth noting: the traceable-decorator code requires the LangSmith package in the project — `uv add langsmith` (he had already done this beforehand, which is why it wasn't shown).

---

## 7. Manufacturing traffic: run five+ times (23:28–27:29)

Checking off the plan so far: ✅ created a new project, ✅ generated the API key and added it to the environment file, ✅ ran and tested the pipeline, ✅ solved the retriever-capture problem with traceable decorators, ✅ re-ran and got updated latency/cost values.

Next: **run five times and collect some data**, because moving forward we need to plot graphs — a few more traces. Since the app isn't truly deployed, he simulates real-world traffic manually by running the pipeline with different questions:

| # | Question run through the pipeline |
|---|---|
| 1 | What is GSM8k? *(the first verification trace)* |
| 2 | What is MMLU? |
| 3 | Why do we need LLM evals? |
| 4 | What are LLM evals? |
| 5 | What are online evals? |
| 6 | What are model evals? / What is the difference between model evals and application evals? |
| 7 | What are benchmarks? |

The point: **replicate real-world traffic.** Once the application is deployed, people will keep asking questions, every question gets traced, and traces accumulate over time. "Since it isn't truly deployed yet, I am doing this task manually, and one person is handling it." After the runs, reloading LangSmith shows **eight or nine traces** in total.

---

## 8. The custom dashboard: P95 latency and average cost (27:29–33:05)

Now "the interesting work." The dashboard idea is simple: **at any point in time, I can look at it and get a complete idea of my application's health** — how the latency is, how much cost it is consuming, how the safety metrics are performing, how the quality metrics are performing — plus the alerts, so that if anything drops below a threshold in a given time interval, an alert is raised on **Slack or some other software**.

In LangSmith's **Monitoring** section there are two possibilities: the **default dashboard** LangSmith provides (it already shows data — "but I will not use this") and **custom dashboards**. Under the **Custom** tab: *no dashboard found* → click the create button:

- Name: **CX Doubt Solve Dashboard**
- Description: he types "Personal Project" — with the caveat that **you should add a proper description**.
- Click **Create**.

Inside the dashboard you can create **as many charts as you want**. Two are built live, via the **+ chart** button:

| Chart | Project | Metric | Selection path | Result |
|---|---|---|---|---|
| **Latency P95** | CX Doubt Solve | Latency | within latency: average / total / **Percentile → 95** | P95 latency over time |
| **Average Cost** | CX Doubt Solve | Cost | **average** of total cost (input/output separable) | average money per question |

Details as taught:

- All charts are **for a given time period** — the X-axis always represents time, changeable to *last 1 hour, last 3 hours, last 6 hours, last 30 days*… so you can always see how a metric is performing over the last X amount of time. For the demo he sets the window to **last one hour**.
- For cost: LangSmith lets you analyze **input cost and output cost separately** — "I have already told you that input token charges are different, output token charges are different" — so you could build separate charts for each. For now he takes total cost together, and **average, not sum**: "I don't want to know the total token cost I had to pay in the last 1 hour. Instead, I want to know **on average how much money I had to pay to answer each question** in the last 1 hour."

The pattern generalizes: keep creating metrics and building charts on top of them.

---

## 9. Alerting — and the P95 discovery (33:05–37:50)

LangSmith also gives you **alerts**. In the **Alerts** tab (none created yet) → **Create alert** → select the project → give it a name. The intended logic:

> If in the **last 1 hour**, our **P95 latency is more than 7 seconds** (he also says "say, 8 seconds"), then something is wrong in the system — raise an alert.

The setup is simple — condition (latency greater than 8 seconds in the last 60 minutes) → select **Slack** → connect the Slack account → it will send a message on Slack. **The only problem:** he cannot select P95. Where he expects a dropdown to choose *average / total / percentile*, the option isn't there — **it forces "average trace latency."**

**Tarun** searches online and finds it is **expected behavior, not a bug**, per the LangSmith docs:

> "The latency metric is specifically defined as **average run execution time**. LangSmith's latency metric measures average run execution time, used to track application latency and alert on spikes. **There is no option to switch it to P50 or P99**, unlike errors."

His reaction: "Oh, okay, that's bad, I guess. It should be there — what will we do with just the average?" Then he reasons about *why* LangSmith may have chosen this: **P95 tells you the tail latency** — for the few users in the distribution experiencing the longest wait times, how long are they waiting? **Average latency tells you about everyone.** So maybe: P95 is basically **outliers**; a high outlier latency would fire the alert, and perhaps that's not the alerting use case — the use case for an alert is when **the entire public is experiencing high latency**. "I'm not completely agreeing with the logic, but I'm pretty sure they must have built this whole system based on user feedback. But again, fine, let's not overthink it — I just wanted to show you how you set up alerts."

The cost-alert example, in the same pattern: **total LLM cost greater than $5 in the last 60 minutes** → if breached, Slack messages you — "Hey brother, something's wrong. **$10 vanished in the last hour.** So something has definitely gone wrong."

And the standing advice: **understand the concept**, because when you join a company you won't necessarily be asked to work in LangSmith. Summary of the ops part: we can log and trace the operational metrics, plot them on a dashboard, and create alerts around them — **the ops part is complete** (with the caveat: the P95 alert cannot be created; the average-latency alert can).

> 💡 **Expert commentary.** The instructor's instinct is right to bristle: alerting on averages is a known anti-pattern in SRE practice. Averages hide tail pain — if 6% of users suddenly take 40 s while everyone else takes 1 s, the average barely moves and no alert fires, yet your unhappiest users are suffering. The industry standard is **SLO burn-rate alerting** on percentile targets (e.g., multi-window burn rates on P99 latency over 1h and 5h windows), plus alerting on *symptoms* (error rates, user complaints) rather than causes. LangSmith's docs position its latency alert as spike detection — closer to "the whole fleet is slow" detection — which is why the average-only restriction stings. Most teams compensate by dashboarding P95 (as this lecture does) and handling tail-latency alerting in their APM (Datadog/Grafana).

---

## 10. Latency Q&A: what P95 means, and where thresholds come from (37:50–40:08)

Two student questions close the ops section:

**Q: Does P95 really provide any statistical measure?** It is significant in a specific way: **it tells you how unhappy your unhappy users are** — the ones taking a long time to get answers. That is *why* P95 and P99 latency values exist. In that sense P95 may not be required for *alerting*, because it is a representation of your **outliers**, not of the general population — which is possibly why LangSmith didn't offer it and gives you the average instead.

**Q: For a more sensitive latency alert, should we set a lower time window (2 minutes instead of 5)?** No — thresholds don't come from engineers tweaking numbers. **They come from your SLOs — Service Level Objectives** — and from the **business use case**. Example: if you built a **research assistant**, it will take time — first it researches, then synthesizes, then writes the write-up; it might even take **1 minute**, and that's fine. Engineers don't apply their own judgment here; the decision-making comes from the top, and "you just have to set what you're told."

---

## 11. Safety online: the built-in toxicity evaluator (40:08–46:12)

Next eval: **safety** — specifically, how to capture and measure **online toxicity**. Two options:

1. **Reuse the offline eval** you already created for safety (the DeepEval toxicity eval from lecture 16), or
2. Use **LangSmith's option to create an online evaluator**.

LangSmith ships **built-in evaluators** (each marked LLM-as-a-Judge):

| Category | Built-in evaluators |
|---|---|
| Security | **PII leakage**, **prompt injection**, **code injection** |
| Safety | **Toxicity**, **bias and fairness** |

Since these are **reference-free**, you can use them directly online. For this demo he picks the built-in **toxicity** evaluator, for two reasons:

1. He wants to **show how you create an online evaluator in a tool like LangSmith**.
2. For toxicity specifically, **what matters more is that we can detect toxicity** — the *way* it is measured (our own code vs LangSmith's) is secondary. The end goal is simply to know whether the system is toxic. And there is a good chance **LangSmith built a better evaluator than us** — "LangSmith is a big company, and if their researchers have built it, it could be better than the toxicity eval we built offline."

The configuration walkthrough:

- **Name** — auto-filled.
- **Application** — auto-selected.
- **Model** — select the judge: "toxicity detection is ultimately just **LLM-as-a-judge**." The default judge here is **GPT-4o**; you can select any other model provider.
- **Prompt** — a system prompt powers the toxicity detection, and you *can* edit it — but he won't, for the same trust-the-platform reasoning as above.
- **Run target** — select **'Traces', not 'Datasets'**. If you select Datasets it becomes an **offline** evaluation (lecture 6's switch, now used for real).
- **Sampling rate** — the interesting parameter (next section).
- **API key** — you must provide your **OpenAI key**, because **you bear the judge's cost** — "LangSmith does not want to bear this cost." (He pastes his key live, again promising to delete the project after class.)

**The sampling-rate discussion.** He quizzes the class: what happens if the sampling rate is 100%? Answer: **all traces get evaluated.** If 500 queries come to the platform in a day (500 traces captured), the toxicity evaluator runs **500 times** — GPT-4o works 500 times daily, and evaluation itself costs real money. So instead: **sample** — rather than evaluating all traces, randomly pick, say, **30%** and measure toxicity on those. In a way, **you are estimating the population from a sample** — evaluating a subset still gives a fair picture of how much toxicity the chatbot is spreading across all the traffic (his illustration mixes "10,000 traces" and "500 traces," but the point is the classic one: the sample estimates the population). In a proper production setup, **the sampling rate depends on your budget**. For the demo he keeps it at **100%**, because he wants toxicity computed on every trace he generates.

Save → the evaluator appears under **Evaluators**.

> 💡 **Expert commentary.** Put numbers on the instructor's cost intuition. At 500 traces/day and 100% sampling, you pay for 500 judge calls *on top of* your serving costs — with GPT-4o-class judges, that can approach the cost of the traffic itself (lecture 6's "cost could more than double"). At 30% you evaluate 150 traces; for a proportion-style metric, the worst-case margin of error at n=150 is roughly ±8 points (±3 points at n=1,000, lecture 6's number). Toxicity is a *rare event*, though — if the true rate is 2%, a 150-trace sample misses it entirely about 5% of the time. Practical pattern: run cheap broad sampling for headline rates, and route suspicious strata (thumbs-downs, escalations — lecture 6's stratified sampling) to a higher-sampling lane.

---

## 12. Watching it work: async evaluation and interpretable feedback (46:12–50:43)

Time to see it run. He adds a new question to the pipeline — **"What are LLM leaderboards?"** ("obviously, there won't be any toxicity in this") — runs it, and the new trace appears in the Tracing tab.

**Important observation:** even though the evaluator is created, **it doesn't give results immediately**. His observation with LangSmith is that it takes about **2 to 3 minutes** — the trace comes in, the evaluation is triggered **asynchronously behind the scenes**, and the result appears after some (variable) delay.

When it lands, the trace shows **feedback: "Toxicity is zero."** Clicking it explains *why* the score was given: "The response is explanatory and professional, it contains no personal attacks, insults." — **your online eval is working on this trace.**

The same recipe extends to the other safety evaluators: Evaluators → plus sign → select **PII leakage, bias, and fairness**. (He also points at a "correctness" template and clarifies: "this correctness is different — this is a **reference-free correctness** thing" — removable for now.)

**The toxicity chart.** Monitoring → custom dashboard → add a chart named **Toxicity** → and this time, in *pick metric*, go to **feedback**. A hiccup: toxicity doesn't show in the metric list yet — "LangSmith is slow to react"; internal registries for the newly created evaluator haven't been created yet, but it will start appearing after some time. (Later in the demo it does — see section 15.)

Two Q&A asides on what the evaluator measures:

- **Score semantics:** it gives a **score from 0 to 100** — the score keeps increasing with how much toxicity is in the answer. Very toxic content → close to 100; very low → close to 0. And it **gives the reason** — "it will tell the exact thing, like *because this was mentioned, that is why I gave it this score*. So it's very **interpretable**."
- **Does it measure toxic content in the *input*?** "No, no, no — we don't care about the user's question. We need to see **how our system is reacting**. That is what matters. The user is free; they can type anything. What will you do — you're not going to record that and go beat him up at home?" The eval target is the system's output.

---

## 13. Quality online: the golden rule — same evaluator, offline and online (50:43–55:26)

The last part: **quality metrics** — and here is the tricky part. **For quality metrics, you should run exactly the same evals you created in the offline setting using DeepEval.** Offline and online quality evals must be the same.

He sets up the puzzle: for toxicity he used DeepEval offline and LangSmith online, and that was fine. So why is it *not* fine to do the same for quality — e.g., DeepEval answer relevance offline, LangSmith's answer-relevance evaluator online? (He shows the LangSmith evaluator list, where an answer-relevance template exists.)

The reasoning — "these are very strict numbers that we are operating on": the offline **contextual relevancy score was around 45**, and that 45 came **with DeepEval**. Run LangSmith's evaluator instead and it might come out **55** — a completely different setup: the prompt could be different, DeepEval's internal way of calculating contextual relevancy vs LangSmith's way could be completely different. **So there would be no comparison between the two numbers** — "I can't say my offline contextual relevance was 45 and online it is 55"; they are not on the same baseline. But use **DeepEval itself** online and a **38** *is* on the same baseline — same evaluation, different number — so it makes sense to conclude the application is perhaps performing poorly online. Change the evaluation technique itself, and **the numbers no longer have any meaning**. Compact version: "It went from 90 to 85 — everything was the same, yet it happened — which means the application is performing poorly in the online setup." He flags this explicitly as an **interview question**: *"Why did you use the same setup for both online and offline?"*

Why was toxicity exempt? Because for toxicity the goal is simply to **detect and minimize** it — any sound evaluator serves that goal, and you could equally run DeepEval's toxicity evaluator online. He showed the LangSmith variation only to demonstrate how online evaluators are created in the tool. **But ideally, keep things the same so offline and online numbers are comparable.**

> 💡 **Expert commentary.** This is a principle of measurement called **instrumentation invariance**: a number is only a trend if the instrument that produced it never changed. Two corollaries the lecture leaves implicit. First, *the judge model is part of the instrument* — even with the identical DeepEval metric and prompt, a silent GPT-4o-mini version bump on the provider side can shift scores a few points; mature teams **pin judge model versions** and re-baseline deliberately when they upgrade. Second, the offline→online comparability argument has a mirror: **online drift** (new user questions) and **instrument drift** (changed evaluator) must be separable — which is exactly why the same-evaluator rule exists. Teams that violate it end up chasing "regressions" that are really just ruler changes.

---

## 14. The workaround: cron job + `eval_online.py` + the LangSmith SDK (55:26–01:03:20)

So how do you run your offline DeepEval evals in an online setting? "We will need to use a bit of a **software workaround**."

The setup: your entire code is deployed — suppose on **AWS**. On that server, run a **background service** — a **cron job**: "a cron job is basically something that triggers whenever you tell it to." We create one that **runs every 5 minutes**, and its job is to take our offline eval files (the one containing the three RAG Triad metrics), run them, and send the scores back to LangSmith.

One problem: that eval file "is currently coded in a way that it only works on the golden dataset" — it was built for the offline setup. The online flow is different: when the cron job fires, it must **go to LangSmith, fetch all the traces from the last 5 minutes, and run the evaluator on them**. So we create a **separate file: `eval_online.py`**.

The complete flow:

> A loop running on the server triggers **`eval_online.py` every 5 minutes** → the script goes to LangSmith and captures **all the traces from the last 5 minutes** (or **30% of them**, depending on the sample rate) → it feeds the most recent traces to the **eval functions written in DeepEval** (the evaluators are "hidden" inside those functions) → the functions generate scores → the scores are **sent back to LangSmith**, which records them under tracing → the loop repeats forever.

To do all this programmatically you need the **LangSmith SDK** — which is what you get when you run `uv add langsmith` — "through that, you can run things on LangSmith via code. … That is why the LangSmith SDK exists — one of the reasons."

**The demo version.** We're not deploying or running a real cron job, so he represents the infinitely-running service with a simple Python construct: an **infinite `while` loop** with a sleep (he describes adding a 5-second sleep; the actual config ends up at 60 seconds — see below) repeating the same logic, pasted into `evals/eval_online.py`:

| Configuration | Value | Note |
|---|---|---|
| Project name | **CX Doubt Solve** | the LangSmith project |
| Evaluator model | **GPT-4o-mini** | the *same* one used offline |
| Thresholds | the *same* ones used offline (0.7) | comparability rule in action |
| Sample rate | **1** (100%) | "forced to process all traces" |
| Polling seconds | **60** | every 1 minute: fetch the last 1 minute's traces and evaluate them |
| Client | a **LangSmith client** created in the script | how the SDK is used |
| Main function | `score_recent_traces` | measures **faithfulness, relevancy (answer relevancy), and contextual relevancy** for each trace |

Then the loop: sleep 60 seconds → evaluate recent traces → repeat; run it with `python -m evals.eval_online` in a new terminal. It runs **until you close your terminal** — "obviously this won't work in an online setup, because as soon as the terminal closes, the service will stop. That's why a **cron job is a better alternative**" — this is "just a simple representation of how an infinitely running service looks."

---

## 15. Watching the RAG Triad run live (01:03:20–01:08:37)

With the loop running, create a new trace: go to the RAG pipeline and ask **"What are gold data sets?"** — run it, get the answer, and the trace arrives in LangSmith. Nothing is visible in the trace's feedback yet — **wait 60 seconds**, then the evaluation triggers.

Meanwhile, the **toxicity chart** gets retried on the custom dashboard: add a chart named Toxicity → pick metric → **feedback** → and this time **toxicity is visible** — "in fact, the other three have also started appearing." Select toxicity, show the **average score**, click create — the toxicity chart exists.

Back in tracing, reload the newest trace: **toxicity has been measured (zero), but the other three haven't yet** — a slight delay. He cross-checks the online-eval config: project name *CX Doubt Solve* ✓, GPT-4o-mini ✓, **0.7 threshold** ✓, sample rate 1 ✓ — "so it is forced to process all traces; somehow it hasn't happened yet, it should have." So he generates one more question — **"Why do we need golden data sets?"** — and the scores start appearing:

| Trace (question) | Faithfulness | Answer relevancy | Contextual relevancy | Toxicity |
|---|---|---|---|---|
| Why do we need golden data sets? | **0.75** | **0.92** | **0.23** — "very bad," but just for this question | 0 (measured after a wait) |
| What are gold data sets? | **1** | **1** | **0.29** — "still low" | 0 |

(Notice the pattern from lecture 14 repeating live: contextual relevancy is the weak leg of the triad on this app.)

"All this is happening automatically behind the scenes." From here, the remaining charts follow the same recipe: Monitoring → custom dashboard → new chart, e.g. **answer relevance** → pick metric → feedback → answer relevancy → choose **average, minimum, or percentile** (he picks average) → create — a chart of answer relevance over time. **Create one for contextual relevancy just like this, one for faithfulness just like this — and then you can set up alerts on every individual chart.** Looking at this dashboard, you understand the health of your application at a glance for a given period of time. With the toxicity score landing at zero, the planned steps are complete: the RAG Triad script ran, the charts were created.

---

## 16. Closing the loop: failures back into the golden dataset (01:08:37–01:13:23)

One last thing — "a very important point I mentioned while teaching the theory": **your offline evaluation dataset is made stronger over time by taking the online failures and adding them to the offline dataset.** A user asked a question on which the system gave very poor results — that is a very good question to add to the golden dataset; this is how you increase its size and its power.

**The demo.** Assume the most recent question scored poorly everywhere — answer relevancy poor, contextual relevancy definitely poor, faithfulness poor, *and* it's toxic. A perfect candidate for the offline setup. The mechanics:

1. **Create a dataset**: in LangSmith, **"Add to dataset"** → create a dataset **from scratch** → name it (he uses **"Sample"**), description ("Sample"), connect it to the application, and optionally define the **schema** for what the input and output will be (he skips this for now) → Create. The dataset "Sample" now exists.
2. **Add the failing trace**: in tracing, open the run with poor results → **"Add to dataset"** → select the dataset "Sample." The question (the one the system failed on) is carried over automatically, along with **the answer the system generated** — "but this answer might be wrong; that is why all the results are coming out poor."
3. **The expert step**: at this point, **an expert of yours can sit and create a reference answer** — type the correct answer in — so it can later be used offline for **correctness, completeness, and other reference-based metrics**.
4. **Merge**: submit, and the question is added to the dataset. From there you can **download the dataset and merge it with your offline dataset**.

**The even better way: create your golden datasets in LangSmith from the start.** All the datasets so far were local files in the offline setup — instead, create them in LangSmith and **load them via the LangSmith SDK**, even for offline evaluation runs. The benefits:

| Benefit | What it gives you |
|---|---|
| **Single home** | the golden dataset lives in one place, usable for **both offline and online** — and the offline one keeps growing |
| **Click-to-add** | add failing traces to the dataset **directly from the tracing UI** |
| **Versioning** | LangSmith handles dataset versioning — you can see how the dataset grows over time |
| **Rollback** | return to any previous state — "if I want to see the golden dataset from 6 months ago, you can go back to that as well" |
| **SDK loading** | offline eval runs load the same dataset through the SDK |

This is a much better approach than file-based golden datasets, and with it "you can very powerfully create this entire loop that connects offline and online. **This is how teams do it in a proper production setup.**"

> 💡 **Expert commentary.** What this section describes is the **data flywheel** — the production-grade version of lecture 3's step 10. Two production realities worth adding. First, the "expert writes a reference answer" step is usually organized through **annotation queues** (LangSmith's reviewer workflow; lecture 6 mentioned it) with inter-annotator agreement checks, so golden labels stay trustworthy as volume grows. Second, dataset versioning is doing quiet but critical work: when the regression gate from lecture 18 blocks a merge, you must be able to say *which dataset version* produced the failing score — unversioned golden datasets make regressions unattributable. If you stay file-based, the conventional tooling is DVC or Git-LFS; LangSmith simply builds the versioning in.

---

## 17. Course finale: the RAG eval arc is complete (01:13:23–01:14:24)

With that, "we have essentially completed an overview of online evaluation. I didn't show you how to build everything, but I gave you an idea of everything. Now, based on this idea, you can create **any complex online eval system using any tool** — because the concept remains the same, whether you are using LangSmith or Langfuse. You just need to know the concept."

The closing announcements:

- **The RAG eval part is complete** — "it took some time; I am really sorry about that. I fell ill in between; otherwise, we would have finished this session a week ago."
- These **seven or eight sessions, from RAG Eval Part 1 to RAG Eval Part 8** — "if you watch them, I am pretty sure you will be able to **impress any interviewer who asks you RAG eval questions. That is my guarantee.**"
- Next, the instructor planned to start **agent evals** — "which will be easier now, because we have studied this entire thing. So it won't take that much time."

---

## Key takeaways

1. **Deployment is not the end of evaluation.** In an ideal setup, every company keeps evaluating its chatbot/LLM application after deployment — that is online evaluation; lecture 6's theory, executed here with LangSmith on CampusX Doubt Solve.
2. **The reference constraint rules the suite.** With no answer key in production, reference-based metrics (contextual recall, contextual precision, correctness, completeness) cannot run online; reference-free metrics (faithfulness, answer relevancy, contextual relevancy, style, the safety family) can; operational metrics aren't "measured" at all — they're logged.
3. **The six-metric online suite:** quality = the RAG Triad (contextual relevancy, faithfulness, answer relevancy); safety = toxicity (of scope/leakage/toxicity, one shown); operational = latency + cost. Style was dropped for low variance (an offline ~80 won't collapse to 30 online); reliability needs Grafana/Prometheus.
4. **Tracing is the foundation and it's nearly free.** A new LangSmith project + four environment variables connect the app; latency and cost start flowing immediately; anything not auto-traced (the retriever/reranker) gets a `@traceable` decorator — nested in a hierarchy, never duplicated, and asynchronous (no latency overhead). Honest measurement: 4.14 s → 4.79 s once retrieval was included.
5. **Dashboards and alerts are chart + threshold + Slack.** Custom charts (P95 latency via percentile; average — not total — cost, with input/output separable; feedback metrics for evaluator scores), time windows on the X-axis, alerts when thresholds break in a window.
6. **LangSmith alerts only on average latency, not P95** — documented behavior, not a bug. P95 = tail latency = "how unhappy your unhappy users are" — a representation of outliers, not the general population. Alert thresholds come from **SLOs** and the business use case (a research assistant may legitimately take a minute) — engineers set what they're told.
7. **Online safety evaluators are built-in, reference-free LLM-as-a-judge** (GPT-4o default; PII leakage, prompt injection, code injection, toxicity, bias & fairness), with a **sampling rate** to control judge cost — 500 traces/day at 100% means 500 GPT-4o judge runs daily; a 30% sample estimates the population. Results arrive asynchronously (~2–3 minutes), as interpretable 0–100 scores with reasons — and they judge **the system's output**, never the user's input.
8. **The golden rule: the same evaluator offline and online for quality metrics.** A 45 (DeepEval) vs 55 (LangSmith) comparison is meaningless — different baselines; a 45 → 38 with the same evaluator is a real signal ("it went from 90 to 85 — everything was the same"). Toxicity is the exception because the goal is pure minimization.
9. **The implementation is a cron job + SDK:** every 5 minutes, `eval_online.py` fetches the last 5 minutes of traces (or a sample), runs the DeepEval evaluators (same model — GPT-4o-mini — and same 0.7 thresholds), and writes scores back into LangSmith. The demo's infinite while-loop (60-second polling) stands in for the real service.
10. **Close the loop — and concept over tool.** Failing traces → "Add to dataset" → an expert adds the reference answer → merge into the golden dataset; better still, host golden datasets in LangSmith from the start (one home for offline and online, click-to-add, versioning, rollback). And whether it's LangSmith today or Langfuse tomorrow: log → sample → evaluate → dashboard → alert → feed failures back is the invariant flow.

## Interview angles

- *"Why can't you run your full offline eval suite in production?"* → No reference: production questions are novel, so there's no answer key; reference-based metrics (recall, precision, correctness, completeness) are structurally offline-only. Show you can audit a suite metric-by-metric.
- *"Why must the online quality evaluator be identical to the offline one?"* → The instructor's explicitly flagged interview question. Scores are only comparable on the same baseline — different prompts/Calculations/tools mean a 45 vs 55 comparison is meaningless, while 45 → 38 with the same evaluator is a genuine performance signal. Mention judge-version pinning as the advanced caveat.
- *"Walk me through how you'd monitor a production RAG application."* → The full chain: connect tracing → operational metrics for free → dashboards (P95 latency, average cost per question) → alerts via Slack → reference-free online evaluators with sampling → the same DeepEval metrics via a cron job and the SDK → failures recycled into the golden dataset.
- *"How do you choose alert thresholds and sampling rates?"* → Thresholds from SLOs/business use cases (research assistant vs. quick chatbot), not engineer intuition; sampling from budget — the judge runs on a percentage of traces to estimate the population, with the accuracy/cost trade-off made explicit.
- *"What would you alert on: average latency or P95?"* → Know both sides: LangSmith alerts only on average (documented); averages hide tail pain; P95/P99 represent outliers — "how unhappy your unhappy users are" — and SRE practice often alerts on burn rates of percentile SLOs.
- *"How do production failures improve your eval suite over time?"* → Failing traces are added to the golden dataset with expert reference answers; hosted datasets give versioning, rollback, and a single source of truth for offline and online — the self-improving loop.

## Cross-links

- **Previous:** [18 — RAG Regression Testing](18-rag-regression-testing.md) — the offline gate (CI) that this lecture's online monitoring complements: CI catches changes before release, online eval catches what CI never sees.
- **The loop, closed:** [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) — steps 9–10 (deploy → monitor → feed failures back into the golden dataset) are exactly what this lecture executes; and [06 — Offline vs Online Evals](06-offline-vs-online-evals.md) — the concept lecture (logging, captured vs computed signals, sampling, evaluators, tracings-vs-datasets switch) that this code demo operationalizes.
- **The metrics, online:** [14 — Generator & Pipeline with the RAG Triad](14-rag-triad-generator-pipeline.md) (the three quality metrics re-run here, including the weak contextual relevancy) and [16 — Toxicity, Leakage & Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) (the offline toxicity eval whose online twin LangSmith provides).
- **Parent:** [104 — LLMOps](../../104_LLMOps/README.md), Module 3 (Observability) — request/trace logging, token-cost-latency dashboards, quality & behavior monitoring, alerting & incident response: where this lecture hands off.
- **Course hub:** [README.md](README.md) — the full 19-lecture map. This is the finale of the course as captured; the instructor's announced next topic (agent evals) builds directly on everything here.

<!-- nav-footer -->
---

**Navigate:** [← 18. RAG Regression Testing](18-rag-regression-testing.md) · [Course hub](README.md) · [Cheatsheet →](cheatsheet.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
