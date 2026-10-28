# 06 — Offline Evals vs Online Evals

> **Lecture 6 of 19** · Unit 1: Foundations · 1:21:09
> Offline Evals Vs Online Evals (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/06-offline-vs-online-evals.md)

---

## What this lecture covers

This lecture closes Unit 1 by adding the last axis to the evaluation mental model: **when** you evaluate. Everything built so far — the workflow, the multiple pipelines, the three methods — has quietly been one kind of evaluation. Now it gets its proper name, and its missing twin:

1. **Offline evals, defined** — the realization that *everything studied so far is offline eval*, plus the three purposes that make it indispensable: pre-release testing (the release gate), version comparison, and regression testing.
2. **Why offline evals are never enough** — the three risks that only exist in production: unintended inputs, emergent/systematic failures, and drift.
3. **Online evals, defined** — evaluation on live production traffic that works **without an answer key**, and the crucial distinction it forces: **correctness vs normality**.
4. **The online evaluation pipeline, end to end** — logging (and its four engineering properties), captured vs computed signals, sampling, LLM-as-a-Judge evaluators, dashboards, and alerting — with **LangSmith** as the running platform.
5. **The self-improving loop** — how production failures flow back into the golden dataset, closing the circle between online and offline.

The instructor is explicit that this is an **overview class**: nothing is demonstrated hands-on ("I haven't shown anything practically… it was a very beginner level class"), but by the end you know *why* online eval exists, *how* the flow runs, and *where* each piece lives.

---

## 1. Recap and agenda (00:00–03:06)

The instructor opens by calling this the course's **third and fourth session combined** — a longer sitting — and recaps everything covered so far:

| # | Topic covered so far | Where |
|---|---|---|
| 1 | **Why** we need evals | Lecture 1–2 |
| 2 | **What** evals exactly are | Lecture 2 |
| 3 | **Model-based vs application-based** types | Lecture 2 |
| 4 | **How an LLM evaluation looks** — the eval pipeline (the 10-step workflow) | Lecture 3 |
| 5 | **Why one application needs multiple eval pipelines** — two reasons: multiple **failure points** (component / workflow / application level) and different **risk categories** (application quality, security, operations) | Lecture 4 |
| 6 | **The eval methods** — programmatic, LLM-as-a-Judge, and evaluation with humans | Lecture 5 |

Today's agenda: **offline eval vs online eval** — what offline eval is, what online eval is, and the differences between the two ("you'll learn a lot in the process").

---

## 2. Offline evals, defined — you already know them (03:06–05:12)

The good news: **there is nothing new to learn here.** Every example from the last two or three sessions — every eval pipeline built in the course so far — was already an example of offline eval.

> **Offline evals** are any eval pipeline you apply to your LLM application **before deploying it**.

The instructor's reference point is the **UPSC application** from the last session: an LLM application that evaluates Mains mock papers and mock tests just like a human examiner would. There, step by step, a **golden dataset** was created, the **LLM-as-a-Judge** method was chosen, and the evaluation was performed. That evaluation happened **after the software was built but before deployment** — which makes it an offline eval.

So the general rule: any time you have an LLM-based application and want to **thoroughly test it before deploying** — to see whether it is deployable — the evals you run there are called offline evals. "As simple as that. We didn't learn anything new; we just gave a new name to what we learned in the past." He even polls the chat: *if someone asks you tomorrow "what are offline evals?", would you be able to answer?*

---

## 3. The three purposes of offline evals (05:12–14:00)

Why run offline evals at all? Why not build the LLM-based software and deploy it directly? The instructor poses this to the audience, then answers: **if you deploy without testing, you won't know how the software will behave in production, and any risk could arise** — the failure case studies from the course opening (the Air Canada chatbot among them) exist precisely because systems were deployed without adequate testing.

| Purpose | The question it answers | Lecture's example |
|---|---|---|
| **1. Pre-release testing** | Is this system deployable at all? | The CI/CD release gate at a 95% threshold |
| **2. Version comparison** | I have more than one possibility — which do I choose? | Claude vs OpenAI on the same golden dataset |
| **3. Regression testing** | Did my change break something else? | The CampusX refund-tone fix that softened everything |

### Purpose 1 — Pre-release testing and the release gate (05:54–08:01)

Offline eval lets you properly test **before releasing**. And here the instructor previews something you'll learn properly in an **LLMOps course**: the entire build-test-deploy process can be so automated that you create a **gate** —

> If the result of running the eval is **above 95%, deploy the software; if it's below 95%, don't deploy it.**

The mechanics: you make a change to the software; the code is pushed; at the gate, **CI is triggered through GitHub Actions** and your **eval script runs there**, producing a score. If the score is above the threshold, the **deployment pipeline is automatically triggered**; if below, you get a **notification that the eval test failed**. Used correctly, offline eval works as a **release gate**: the change ships if the eval passes, and **rolls back to the previous version** if it doesn't.

> 💡 **Expert commentary.** What the instructor describes is exactly the **eval-as-release-gate** pattern from CI/CD engineering. Three properties decide whether a gate survives contact with a real team: it must be *trustworthy* (low flakiness — a stochastic metric needs enough samples or a measured noise floor, otherwise a 1% "regression" inside ±3% run variance blocks releases randomly), *fast enough to respect* (a 40-minute gate gets skipped; a 6-minute core suite gets obeyed), and *explainable when it fails* (which slice regressed, with example outputs — not a red X on "faithfulness: 0.78 < 0.80"). Thresholds should live in reviewable configuration, not hard-coded. This is developed in depth in [Section 105 note 5 — Eval Engineering](../05-eval-engineering.md), and lecture 18 of this course makes regression gating the main topic.

### Purpose 2 — Version comparison (08:01–09:51)

With a RAG application (say, the UPSC one) you face choices: build it with a **Claude model or an OpenAI model**? Everything else is identical — the rest of the code is the same, only the model differs. How do you decide which gives better results *for your purposes*?

> Create **two versions of your software and run the same eval on both.** Because the eval is the same, the **golden dataset is the same** — the field is level — so the results let you easily see that (in his example) **Claude is scoring higher than OpenAI**, and you use Claude.

The same trick works for anything swappable: comparing different **prompts**, different **models**, different **rerankers**, different **vector databases**, even different **architectures** of your application. Whenever you think "I have more than one possibility — which one should I choose?", the answer comes from running the evaluation on multiple versions of the software.

### Purpose 3 — Regression testing (09:51–13:26)

A very famous term in software — the instructor quizzes the chat, and credits Amar's answer: regression testing is **"the test of change."**

His worked example: **version one of the CampusX chatbot is already live**, students interacting with it. In production you observe a pattern: whenever students ask for a **refund**, the chatbot responds in a **cold manner**. Since you always want the chatbot to speak to students in a nice tone, you go in and change the system prompt: *"You have to be very kind and very polite. You have to answer nicely."*

Now a new behavior emerges — the chatbot's personality becomes **very soft**. Ask "What's the cost of the Insider plan?" and suppose it costs **19,500**; the chatbot will softly say **"around 19,000"** — rounding down *to impress the other person, just to make sure it sounds good*. (The instructor laughs at himself: "I know, I'm not giving a very good example.") The point it carries is serious:

> When you're building a very complex system, **you try to improve one thing, and everything else goes wrong.** Performance improves on the thing you targeted and deteriorates everywhere else. **That is regression.**

Offline eval protects you. How? Your golden dataset deliberately contains **different types of cases** — refund questions, pricing questions, course-curriculum questions — covering every type of student question. You run the eval per question type and check the success rates: if **refunds were at 90% before** the change, they should stay around 90% after. **If it drops to 80%, there's a regression — and you shouldn't ship the change you just made.** The rule generalizes: whenever you change the model, the vector database, *anything*, nothing else should break — and offline eval is how you verify it.

Summing up the section (13:26): the three biggest advantages of offline evals are pre-release testing, version comparison, and change/regression testing — **"work is impossible without them."** (And a pacing aside: "We're moving very slowly, but we're covering the whole thing.")

---

## 4. Why offline evals are never enough: three risks of production (14:00–22:17)

Suppose you built your LLM-based software, ran offline eval, all results passed, and you deployed. **Now what? What problems can arise in production?** Three major ones — and the punchline is that offline eval **cannot cover any of them**.

### Risk 1 — A variety of unintended inputs (14:54–16:38)

In the offline setup you created a golden dataset of **200–500 questions you thought a user might ask** — and tested the chatbot *only on those*. Deploying opens it to the real world, where **students can ask any type of question**, including ones you never tested. The instructor's list of what suddenly shows up:

- **Hindi–English mixing** — people start talking in a blend ("Hinglish"). You trained/fine-tuned mostly on English because you anticipated English-only conversation.
- **Ambiguous half-questions** — where it's not even clear what the user is trying to ask.
- **Angry rants** — where a real question is *hidden behind the anger*.
- **Adversarial prompt injections** — users deliberately trying to trick the chatbot into giving answers it shouldn't.

In production you are exposed to **a much larger superset** of inputs than anything you showed or tested the system on.

### Risk 2 — Emergent and systematic failures (16:38–18:26)

Small failures that **only come into the picture when you deploy** — problems that arise **at scale**:

- **Load-driven latency.** You launch a new course on CampusX; suddenly thousands of people arrive and the chatbot has **thousands of concurrent users**; latency suddenly spikes. *You could never test this offline, because you can't bring thousands of users into an offline setup.*
- **Subtle bias.** Your chatbot might be slightly **biased against people from non-technical backgrounds** — but you only notice once it has chatted with thousands of people. With enough data a pattern emerges: it speaks well with technical people, and a little bias creeps in with non-technical ones.
- Plus, generally, **systematic failures you never anticipated beforehand**.

### Risk 3 — Drift (18:26–20:58)

The instructor flags this as **the most technical point of the three**. **Drift** means your offline development setup — the basis on which you tested and deployed — *gradually becomes obsolete*. His scenario: you just built the CampusX chatbot and loaded today's documents — **the pricing structure, course pages, curriculum pages, transcripts of lectures**. But over the years the business keeps changing: the price of a course changes, the curriculum shifts slightly, policies are updated. **As a business operates, its documents gradually change.** A year from now, the documents feeding your RAG look very different from a year ago — but **the golden dataset was designed for *today***.

Because the underlying data distribution has changed, the golden dataset — the whole eval pipeline — becomes **kind of obsolete**. The trap this sets: your offline eval **still returns good results** when you test the application, while **online, users flood you with negative feedback** because they don't like the chatbot's behavior. It's happening because *you kept changing the product but never changed the eval setup*. Drift creeps in; the eval setup goes stale; its results stop mattering.

> 💡 **Expert commentary.** The lecture's drift story is **data/document drift** — the retrieval corpus and the query distribution moving out from under a frozen test set. Practitioners split the phenomenon further: *document drift* (the knowledge base changes), *user-population drift* (new user segments, like the non-technical users in Risk 2), and *concept drift* (what counts as a "good answer" changes — e.g., a new policy makes yesterday's correct answer wrong). The standard defenses are re-baselining the golden dataset on a schedule, refreshing a fraction of test cases from recent production traffic (which is exactly the promote-failures loop in section 16), and monitoring input distributions — the observability side covered by [104 — LLMOps](../../104_LLMOps/README.md).

### The conclusion — no golden dataset exists in production (20:58–22:17)

So: offline eval is *necessary* (testing before launch is essential), but **after launch there are many risks that offline eval cannot cover**. The structural reason is simple — **how do offline evals work? They need a golden dataset with correct answers.** Once you're in production, **there is no golden dataset**: users can ask anything, you don't have the correct answers, and you cannot know in advance which student will ask what question, or what the correct answer to that future question is. That is precisely the gap **online eval** steps into.

---

## 5. Online evals, defined (22:17–23:42)

The name gives the idea:

> **Online eval** is evaluating your system on **live production traffic, after deployment, as real users interact with it**.

The simplest definition: a *different type* of evaluation that we run **in production, after the software is deployed**. And its **biggest characteristic**: it works **without an answer key** — without a golden dataset. That is why it is so critical, and why it is hard: it helps you ensure the deployed software **continues to run properly**, and tells you when there are **glitches online**.

---

## 6. Offline vs online — the full comparison (23:42–26:22)

Based on everything discussed so far, the instructor outlines the difference in four-plus key points (he enumerates four, then walks more):

| Dimension | Offline eval | Online eval |
|---|---|---|
| **Timing** | Before deployment | After deployment — and continues **consistently** forever |
| **Data** | A fixed dataset you create — the **golden dataset** | **Live production traffic** — all the queries being asked |
| **Answer key** | Mostly available (the golden dataset) | **None** — you have to *guess on the fly* what the correct answer might be |
| **Inputs** | Only what you **anticipate** (you put it in the golden dataset) | **Can't anticipate** — anything can happen |
| **What it catches** | **Regressions** | **Drift**, surprises, emerging bugs |
| **Best used for** | Getting started, **gating** (threshold + CI + deploy), **version comparison** | Detecting drift; telling how the chatbot is performing **in the real world** |
| **Cost & speed** | **Fast, cheap, repeatable** — simple code + an LLM on a small dataset | Evaluation at **much larger scale** — can be costly |

The cost row deserves its own note: your chatbot might be talking to **500 people a day** (or, at the upper end of his examples, **50,000 conversations a day**) — you would have to monitor every one of those conversations. So online eval uses a **sampling technique**: rather than monitoring each of the (tens of) thousands of conversations, you **sample around 1,000 of them randomly**, which brings the cost down.

---

## 7. Complementary, not rivals: correctness vs normality (26:22–34:05)

The most important thing to understand: **these two are not rivals.** Online eval is **not a replacement** for offline eval — the two **always happen together**; they are **complementary**. It's never "one will be there and the other won't."

The instructor then shares "a very good line I read somewhere" — the sentence to carry out of this lecture:

> **Offline eval's job is to check whether your application is *working correctly*. Online eval's job is to tell whether your application is *running normally* in production.**

### The UPSC grader: correctness offline, unmeasurable online (27:41–30:29)

Recall the UPSC paper-grader. In the last class, when applying **offline** evaluation to it, what were we trying to achieve? That it evaluates papers **exactly the way a human would**. So the measure of **correctness** was: *the marks my grader gives to a particular answer should be close to what a human would have given.*

Now imagine the system passed offline eval and was deployed. **Can you measure its correctness online?** The instructor puts it to the chat; many say no. Why not? **Because at this moment you don't know how many marks the answer being graded deserves from a human.** There is **no golden dataset for this particular answer** — no human perception exists in production; this answer has never been evaluated by a human; your system is evaluating it for the first time. Correctness is simply **unmeasurable** online.

### What you *can* check online: normality, via the score distribution (30:29–33:33)

So we checked correctness offline, deployed — and online we check that the system is **running normally**. How? By watching the **distribution of scores**:

- Say the system evaluates **1,000 papers a week**. Student one scored 300, student two 456, student three 700 — plot them all and you get a distribution (scores ranging 0–1000: most students around 500, many around 700, very few around 200).
- That first week becomes your **baseline**. You keep plotting week after week — and as long as the distributions match the baseline, you can say the system is working the same way as last week; and *if it was correct last week, it's correct today*.
- Then in a particular week, **very high scores suddenly start appearing** — around 900, 800, 700 — the distribution shifts. That tells you something **abnormal** is happening; it triggers you to go and see what went wrong.

A student (Shoaib) pushes back: the distribution change might be due to **some other trend** — maybe suddenly *very intelligent students* started taking the exam. Absolutely possible, says the instructor — but now you're *aware of it*; you'll go and investigate why the system is suddenly giving such high scores. That investigation trigger **is** the online eval doing its job.

Two honesty notes from the instructor: online eval **can't guarantee correctness** — "in some cases it can, in others it can't" — it mostly tells you whether the application is working *normally*. And: **"Don't just stick to the example** — I constructed it only to explain the difference between correctness and normality; it's not applicable everywhere."

He closes the stretch with a comprehension check worth internalizing: *if you feel online eval is unnecessary in your life, then there's a problem — either with your understanding or with my teaching method.*

> 💡 **Expert commentary.** "Correctness offline, normality online" is the practitioner's summary of a deeper statistical reality: online you trade **ground truth** for **proxy signals and distributional monitoring**. The industry's gold-standard online techniques all live on this axis — **A/B testing** (split live traffic between variants and compare behavioral outcomes), **interleaving** (mix responses from two systems inside one conversation and infer preference from engagement — more sensitive than A/B at equal traffic), **human feedback** (thumbs, ratings, escalations — directly measures user-perceived quality, but users thumb up confident wrong answers), and increasingly **bandits** (allocate traffic to the better variant dynamically instead of a fixed 50/50 split). The lecture's score-distribution watch is the cheapest member of this family — an SRE-style control chart over a judge-able metric. Note the same taxonomy the parent note draws: proxy signals measure *user-perceived* quality; sampled LLM-judged audits measure *actual* quality — track them separately, because they disagree in systematic ways ([Section 105 note 1](../01-evaluation-fundamentals.md)).

| Method | How it works | Strength | Watch out |
|---|---|---|---|
| **A/B testing** | Randomly split users between version A and B; compare outcome metrics | Real behavior, real users | Needs lots of traffic; slow; one dimension at a time |
| **Interleaving** | Blend outputs from both versions in one session; infer preference from user choices | Much more sample-efficient | Needs a presenting layer that can mix; mostly ranking/retrieval |
| **Human feedback** | Thumbs up/down, ratings, escalations captured in-product | Cheapest continuous signal; measures perception | Biased, sparse, gameable; ≠ correctness |
| **Distribution monitoring** | Watch a computed metric's distribution vs baseline (this lecture's method) | No extra users needed; catches drift | Confounds (the "intelligent students" effect); needs a judge for the metric |

---

## 8. Estimating quality without an answer key (34:49–37:39)

A student (Shiva) asks the obvious question: *online eval has no answer — how do we actually estimate quality?* The instructor's answer: there are many ways — you'll see them right away. Two families emerge:

**Family 1 — metrics that don't need the correct answer.** Take a **RAG chatbot**: you can check its **faithfulness**. What does faithfulness mean? **Is the answer generated from the retrieved context?** You *have* the context, you *have* the generated answer — you can ask an LLM, "given this context and this answer, tell me the faithfulness." It can be determined **without ever knowing the correct answer**. Many metrics can be evaluated this way.

**Family 2 — workarounds when the metric does need the answer.** Like the UPSC example, where no correct answer exists in production: there you **compared against the baseline distribution** to check the system was working *normally*. If your metric needs ground truth you don't have, you're restricted — and you have to think your way to a conclusion.

A second worked example of Family 2: **can you measure the *correctness* of a chatbot in a live setup?** A new question comes in; you don't have its correct answer; you can't evaluate it directly. Is there *another signal* that can stand in for the answer key? Yes — **what if you provided thumbs-up and thumbs-down buttons in your chatbot?** If you suddenly notice that **many conversations in the past hour are receiving thumbs-down**, something is wrong — the chatbot is giving answers users judge to be wrong. It's "a tricky way" to determine correctness is holding up — and the general name for it: **the alternative to correctness online is user feedback.**

(Transition note: which signals should you *actually* track online, and where things can go wrong — that's the next major section, "I just have this written on the screen in front of you.")

---

## 9. The score-distribution method, re-explained (38:08–40:48)

A student (Shruti) didn't get the distribution part, so the instructor walks it again, slowly:

1. **The problem.** In production I have no way to know whether the paper my system is grading *at this moment* is being graded correctly. I have the question paper's answer key, but **not the user's answer key — no human's marks** to compare my score against. So correctness is unmeasurable per-paper.
2. **The move.** Store **every total score** the system awards, and plot the scores over a **one-week window**. A distribution emerges — scores ranging **0 to 1000**: most students around **500**, many around **700**, very few around **200**. That was last week.
3. **The comparison.** Week two, plot the same graph: now **most students scored around 800**, and very few around 200, 300, or 500. Weeks one through four all had similar distributions; **the fifth week suddenly looks like this**. Comparing distributions week by week, you conclude: *something's different this week — something's definitely wrong. Why did my software suddenly start giving higher marks?*
4. **The conclusion.** You couldn't measure correctness — so you **compared against the last baseline**, and that told you whether the software was working *normally*. That is the point.

This re-explanation is the bridge into the lecture's centerpiece: what an online evaluation pipeline actually looks like.

---

## 10. The online evaluation pipeline — step 1: logging (40:48–48:48)

> "Now, the most important section of this class. In this one, you're going to learn the most important things."

**Step 1 of any online eval pipeline is logging.** The idea is simple: your chatbot is live, people are talking to it — before you can evaluate *anything*, you must **record everything that happens, every conversation, somewhere**. If you don't record it, it's lost; and if it's lost, *what will you evaluate it on?*

> Logging means you **capture a structured, replicable record of every conversation turn**.

If you're having 50,000 conversations a day, you store them properly. What does "storing a conversation" actually mean? The instructor's inventory:

| Layer | Fields logged |
|---|---|
| **Identity** | **Conversation ID**; a **turn ID** for every turn (user speaks, chatbot speaks, user speaks, chatbot speaks…); **user ID**; **session ID**; a **timestamp** |
| **Content** | The **question** the user asked; the **context** the chatbot generated while answering (the RAG retrieval); the **output** the chatbot gave based on that question and context |
| **Operational** | **Latency in milliseconds**; **tokens spent** (including completion tokens); **total cost**; whether any **errors** occurred; the **status code** |
| **Behavioral signals** | **Thumbs-up / thumbs-down** pressed during the conversation; **escalation** ("I don't want to talk to you — connect me to a human, or give me your email address, I want to email"); the user **repeatedly asking the same question** because the chatbot isn't helping, or **rephrasing** it |

**The tool:** a student (Aman) answers correctly — **LangSmith**. The instructor has taught LangSmith on YouTube before: you build a chatbot and store every conversation on it. In the live peek: LangSmith has **projects**; inside a project you see all the stored **conversations** — what the user sent, what your output was, plus **lots of metadata** — everything is stored there.

Logging has **four engineering properties** you must design for:

| Property | What it demands |
|---|---|
| **1. Non-blocking** | Logging is itself an operation running alongside `chat.completion` — the two must not overlap in a way that **adds latency**. The conversation proceeds normally on one side; logging happens automatically on the other. |
| **2. Durable & queryable** | Store via a **data-warehouse-type tool or an observability tool like LangSmith**, in a very structured way — and be able to **retrieve it anytime in the future**. "This is very important." |
| **3. Late-signal attachment** | Some user signals **don't arrive during the conversation — they arrive later**. Example: the user escalates by sending an email to support *the day after* the conversation. You must still record that the escalation happened, by joining it back via the **conversation ID**. |
| **4. PII handling** | If a user shares **sensitive personal information** — phone number, address, card number, date of birth, **Aadhaar number** (PII = personally identifiable information) — you **delete, blur, or corrupt** it before storing it in LangSmith, so that no teammate or employee can ever extract it later. For text, this is **masking**. Privacy must be maintained. |

So step one: before evaluating anything, first store everything — generally in a data warehouse and/or an observability tool like LangSmith.

> 💡 **Expert commentary.** The tooling landscape beyond LangSmith: **Langfuse** and **Arize Phoenix** are the popular open-source alternatives with the same trace-store + dataset + online-eval loop, and everything converges on **OpenTelemetry**-style tracing (spans for each LLM call, with token/cost/error attributes) — which is what makes logs *queryable* later. Two additions worth knowing: the log schema is a **contract** (dashboards, evaluators and the promotion pipeline in section 16 all read from it — changing it carelessly breaks the whole downstream stack), and PII handling is increasingly a **redaction-at-ingestion** pipeline (detectors + masking before the write), not a cleanup job afterward. The observability curriculum that owns this layer is [104 — LLMOps](../../104_LLMOps/README.md).

---

## 11. Step 2 — two kinds of signals: captured vs computed (48:48–52:53)

Before the pipeline's next step, you need to know **what matters in online evaluation — what signals to pay attention to**. There are exactly two types:

| | **Captured signals** | **Computed signals** |
|---|---|---|
| **Definition** | Already present — you just **store them as-is** | You must **extract, calculate, or figure them out** |
| **Examples** | Thumbs-up / thumbs-down; **latency** (however long the answer took — store it directly); **token usage** (simply counting); **cost** (your LLM provider tells you, or it's pre-calculated) | **Faithfulness, answer relevance, correctness, hallucinations, toxicity, bias, fairness** |
| **Machinery needed** | None beyond logging | An **evaluator** — e.g., an *online evaluator* you send the stored chat to, which computes and returns the score |

The instructor's illustration of *computed*: you want your chatbot's **faithfulness** in production — you won't get that by just storing the chat. You must create an evaluator, send the chat to it, and it calculates the faithfulness score.

A subtle taxonomy note he makes: the captured quantities — latency, tokens, cost, errors — are **general quantities you'd find in any software, even "normal" (non-LLM) software**. They aren't LLM-specific. The computed quality quantities are what make online evaluation specifically *LLM* evaluation.

---

## 12. The captured-signal flow: dashboarding and alerting (52:53–58:53)

For a **captured** quantity (say, latency), nothing needs computing — so the flow is short:

> **Logging → Dashboarding → Alerting**

**Dashboarding (52:53).** In every production setup you create a dashboard and display these quantities **on a time basis**: latency in the last hour, last 24 hours, last week, last 6 months. The dashboard's graph tells you whether the system is functioning normally. His worked example: you launch a course, **500 people hit the website simultaneously**, they start chatting — and the chatbot's **response time suddenly climbs**; the graph that was flat "suddenly looks like this." You read it instantly: something's wrong. The response: **allocate more resources — if you're on AWS, start more EC2 instances, spin up your load balancer**, manage the traffic somehow — and after a while latency comes back down on its own.

**Alerting (54:36).** You won't have an engineer staring at the graph all day — "they could be on vacation, sleeping, or whatever." So you set up **alerts**: if the quantity crosses a **threshold**, an alert fires to the concerned engineer via **Slack, or email, or WhatsApp** ("WhatsApp doesn't typically happen, but let's use WhatsApp") — e.g., *"latency has exceeded 4 seconds"* — and they quickly go and normalize things.

**The LangSmith tour (55:50–58:21).** In LangSmith: open **Monitoring**, select your project, and a dashboard is **already created** with graphs for — **trace latency, error rate, LLM call count, LLM latency, and cost**. "This is how I understand the health of my system." You can slice by time window — **last one hour, three hours, six hours** — because a single conversation's latency in isolation doesn't matter; latency fluctuates within individual conversations. What's meaningful is the **aggregated** latency across many conversations in the last hour: if the average is climbing across conversations, that's a **system-level glitch**. On the alerting side, LangSmith has an **Alerts** section: create a new alert, select the project, name it, pick the metric it watches, set the trigger condition (a threshold such as "more than X in the last 5 minutes"), and connect a destination — **Slack, PagerDuty, a platform like Dynatrace, or your own API** — "so you can set up alerting as you see fit." Under the hood this reads the logged values (in the **Trending** view you can see, e.g., **latency 2.03 seconds** being tracked) and surfaces them in Monitoring, with the alert watching for sudden increases.

| LangSmith Monitoring graph | What it tells you |
|---|---|
| Trace latency | End-to-end responsiveness of a full request chain |
| Error rate | Failures / status-code problems per window |
| LLM call count | Volume — how hard the model is being hit |
| LLM latency | Model-side slowness, isolated from the rest of the trace |
| Cost | Spend per window — budget health |

---

## 13. The computed-signal flow: evaluators and sampling (58:53–01:05:09)

Now the main, "most interesting" part: tracking a **computed** quantity in production. The running example: **hallucinations** — we need to see, in real time, whether the chatbot is hallucinating. The pipeline:

**Step 1 — Log.** Same as before: if the chatbot is having its daily conversations (his running number: 500 a day), you log every one of them with a tool like LangSmith.

**Step 2 — Set up an evaluator — and it must be reference-free.** He quizzes the class on the last lecture's distinction: an evaluation where you *have* the answer key in your golden dataset is **reference-based** (the UPSC grader was the example); an evaluation with *no* golden dataset and no correct answer key is **reference-free**. Now think: the user asked a question; the chatbot produced an answer. **Do I have an answer key saying whether that answer was a hallucination? No.** So hallucination checking in production is **reference-free evaluation** — but it still must be performed. The implementation: use **LLM-as-a-Judge**. Bring in a slightly **more powerful LLM**, show it **the retrieved context, the question the user asked, and the output your LLM generated**, and ask: *"Is the LLM hallucinating or not?"* Behind that question you write a **detailed rubric** that guides the judge on how to decide.

**Step 3 — Sampling.** Here's the big problem, and he makes the class think about it: *can you apply this evaluator to all 500 conversations?* Should the judge-LLM grade every single one? **Obviously not — it would be very, very costly.** You're already paying to *run* the chatbot (those 500 conversations aren't free); if you also pay to *evaluate* every one, **the cost could more than double**. So a step sits in between: **sampling** — randomly select roughly **1,000 conversations** (from the day's traffic) and run the evaluator, the LLM-as-a-Judge, on those.

**Step 4 — Dashboard, then alert.** The evaluator produces a quantity — the **hallucination rate** — which goes to the **dashboard**, exactly like the captured quantities above, and **alerts** are created from it.

> The flow is *exactly the same* as for captured signals, with only two additions: **sampling** (to save cost) and the **evaluation step** that computes the metric in between.

| Step | Captured quantity (e.g., latency) | Computed quantity (e.g., hallucination rate) |
|---|---|---|
| 1 | **Log** it | **Log** the conversation |
| 2 | — | **Sample** the day's conversations |
| 3 | — | **Evaluate**: reference-free LLM-as-a-Judge with a rubric |
| 4 | **Dashboard** it over time windows | **Dashboard** the computed rate over time windows |
| 5 | **Alert** on threshold breach | **Alert** on threshold breach |

---

## 14. Random vs stratified sampling (01:05:09–01:08:31)

A design question the instructor poses: *you randomly selected the sample — **is random sampling actually a good strategy, or could there be a better one?***

A student (Amar) suggests: **ignore the conversations that got a thumbs-up**. Valid, says the instructor — the student was most likely happy with the chatbot's performance, so most likely no hallucination there. "Not exactly a fact, but it's a good signal" — keeping those conversations in the eval sample won't help. The complementary move: **focus more on the questions that got a thumbs-down**. Or on conversations that:

- **ended abruptly**,
- involved **escalations**,
- had the user **repeatedly rephrasing the same question**,
- or were **about money — refunds, admissions, fees** being discussed.

The principle: **not all conversations are the same.** So instead of plain random sampling, you do **stratified sampling**: first **divide all conversations into categories** (strata), then **select more samples from the problematic categories** (heavy money talk, thumbs-downs) and fewer from the normal ones. The result: your sampled conversations have a **higher chance of accurately detecting hallucinations**. (Implementation aside: you can think of it as **clustering** — you'd set up a small model that detects who has a thumbs-down, who's talking this way or that way. "This is a technicality — I just wanted you to know your sampling isn't just random; you're doing stratified sampling.")

He then restates the **entire online-eval flow** as built up across the lecture: **log everything → sample → set up the evaluator → the evaluator evaluates the sampled conversations and gives metrics → aggregate the metrics over a period of time and display them on a dashboard → if a threshold is crossed, trigger the alerting system.** And remember lecture 4's lesson still applies online: you set up **multiple evaluators** — multiple eval pipelines — not just one.

> 💡 **Expert commentary.** One caveat the lecture leaves implicit: **stratified sampling optimizes detection, not estimation.** If you oversample the problematic strata, your *hallucination-rate estimate* becomes biased upward — it's no longer the rate of the traffic, it's the rate of the scary slices. Mature setups square this circle by keeping **two samples**: a small *unbiased random* sample (for the honest headline number, with confidence intervals — at 1,000 draws your margin of error is roughly ±3 points) and a *stratified/oversampled* one (for detection power on the slices that matter). The same discipline powers alerting thresholds: with small nightly samples per stratum, set thresholds on smoothed multi-day windows or you'll page engineers over noise.

---

## 15. LangSmith: the evaluator templates and the tracings-vs-datasets switch (01:08:31–01:14:31)

The instructor now shows how this whole flow is productized in **LangSmith**. There's an **Evaluators** section ("Get Started with Evaluators" → **Show All Templates**) with ready-made evaluator templates — and next to each one it says **"LLM as a Judge,"** because that's what runs behind the scenes:

| Category | Evaluator templates shown | What it does |
|---|---|---|
| **Security** | **PII leakage** | Computes whether the chatbot is leaking personal information |
| | **Prompt injection** | Detects adversarial prompt-injection attempts |
| | **Code injection** | Detects code-injection attempts |
| **Safety** | **Toxicity** | Flags toxic outputs |
| | **Bias & fairness** | Flags biased/unfair behavior |
| **Quality** | **Hallucinations** | The reference-free judge we just built by hand |
| | **Correctness** | Judges answer correctness |
| | **Assertions, Concision, Factual checker** | Format compliance, brevity, factuality of the conversation |
| **Agents** | **Trajectory** | "This is actually for agents — this is not for chatbots" |
| **Modalities** | separate evaluators | Different ones for **image-based chatbots** and **voice-based chatbots** |

**Setting one up** (using the hallucination evaluator as the example): click the evaluator type → give it a **name** → select the **application** it runs on (an organization can have more than one) → select the **model** for the LLM-as-a-Judge — **OpenAI or Claude or whatever** — provide your **API key**, and set **temperature and other settings** → then the **prompt** you'll give the judge: define your **rubric** telling it how to detect hallucinations, write your instructions, provide some reminders and context ("we'll learn all this later") → finally, the **output format** the judge must return.

**The key switch — tracings vs datasets.** The setup screen offers two run targets: run this evaluator **on tracings** or **on a dataset**. The instructor challenges the class with what this means, and praises the correct answer:

| Run the evaluator on… | It becomes… |
|---|---|
| **Tracings** (the logged production conversations) | An **online evaluator** |
| **A dataset** (an offline golden dataset) | An **offline evaluator** |

> **LangSmith is an overall evaluation platform** — you can do both online and offline evaluation in it. Select "tracing" and you've triggered online evaluation; select a dataset and you've triggered offline evaluation.

He walks both sides: under **Datasets and Experiments** you can **create a new dataset** and keep adding examples to it (this is what you'd point an offline evaluator at), and **New Experiment** gives you **code to run offline experiments** ("we'll explore this in future sessions"). LangSmith gives you the complete setup: create datasets, run offline experiments, do the logging, monitor, alert, and run your evaluators — "a complete evaluation platform." And a scoping note: **"We're not demonstrating because this is an overview class"** — the point today is knowing *what happens where and how*.

---

## 16. Closing the loop: the self-improving cycle (01:14:31–01:16:49)

Recall from the workflow lecture (lecture 3): in production, when problems appear in certain conversations, **you make them part of your dataset**. That was written into the offline flow's deploy-and-monitor step — *if a failure occurs in production, pick it up and put it in the offline dataset.* LangSmith operationalizes exactly this:

- **Add to Data Set.** Something goes wrong with a particular conversation in production and your team identifies it — there's an option at the top of the trace: **"Add to Data Set."** One click makes that conversation part of your offline dataset, and **the next offline evaluation runs on the updated dataset**. "This is how you close the loop — working offline and online in sync all the time."
- **Annotation queue.** You can also send a conversation to an **annotation queue** and record **what went right and what went wrong** in it. You keep annotating the data arriving online, and it keeps becoming part of your offline data.

Which "basically forms a circle" — the **self-improving loop**:

> **Offline evals → deploy → failures occur in production → picked up and added back to the offline dataset → offline evals run again (on the richer dataset) → deploy → new failures appear → …** — the work continues in a circle for as long as the system lives.

---

## 17. Wrap-up: baselines, the mindset shift, and the road ahead (01:16:49–01:21:09)

**Q&A — how do you judge a dashboard number?** A student asks: suppose the dashboard shows **faithfulness 87** (with toxicity and latency numbers next to it, e.g., latency 3) — how do you actually judge whether that's good? The instructor's answer:

> **Everything has a baseline defined — and that baseline generally comes from your offline evaluation.** If your faithfulness baseline is **85** and the dashboard shows **87**, you're better than baseline — you'll be happy. But if in the last 24 hours faithfulness **drops to 75**, then against the 85% baseline this is concerning: **alerting will occur**, or you'll step in and make improvements to the system.

**The mindset shift.** Before this course, the goal was "I want to build a chatbot — a RAG chatbot": grab an API, build the software, go to sleep. Now your level has risen: you start thinking about **how your chatbot will work properly for thousands, millions, and billions of people**. *"I didn't just build it — I'm also learning to operate it properly."* That is the idea of this playlist, and why it will set you apart from your competition — **not many people are studying this yet**, so if you learn it, you have value in interviews and beyond. And a calibration aside: "Honestly, the playlist has just begun — this is technically the second lecture — but you seem to understand the potential in this whole thing."

**What's next.** In the coming sessions the course moves from concepts to application: learning to **create golden datasets**, to **run offline evaluations**, and to **run online evaluations** — with tools and libraries: **LangChain** (already seen), **DeepEval**, and **RAGAS**. After that, the course pivots to **benchmarks**: recall there are two types of LLM evaluations — **model-level and application-level** — and *everything discussed so far has been application-level*; a dedicated session will cover **model-level evaluations** (benchmarks and the rest) before returning to application evaluations. Scheduling note: "Today is the 8th — my goal is to complete this playlist for you this month, plus or minus one week."

**Final Q&A — the 92→99 question.** A student asks: *if offline evaluation improves from 92 to 99, is that good for online production?* The instructor's answer: **"Depends — the question isn't complete."** Which quantity are you talking about? And isn't it possible that in going from 92 to 99, **the other quantities went down**? If *everything* is improving, obviously it's good — but **the improvement of one thing shouldn't come at the detriment of something else.** Because that is exactly what happens in LLM-based systems: you try to improve one thing, you encounter **regression**, and everything else falls apart. "That shouldn't be happening. Okay, guys? See you in the next class."

---

## Key takeaways

1. **Offline evals** are any eval pipeline applied to the LLM application **before deployment** — everything the course built so far (Zomato router, UPSC grader) was already offline eval. Nothing new; just a name.
2. **Three purposes of offline evals:** (1) **pre-release testing** — automatable into a CI/CD **release gate** (eval score above a threshold like 95% → auto-deploy; below → block/rollback); (2) **version comparison** — same eval, same golden dataset, two system variants (Claude vs OpenAI, different prompts, rerankers, vector DBs, architectures) makes the choice empirical; (3) **regression testing** — the test of change: fix the refund tone, and verify pricing/refund/curriculum success rates didn't move (90% → 80% means don't ship).
3. **Three risks that only exist in production:** unintended inputs (Hinglish, half-questions, angry rants, prompt injections — the real world is a superset of your 200–500 test questions); emergent/systematic failures (thousands of concurrent users spiking latency, subtle bias visible only across thousands of conversations); and **drift** (the business's documents change while your golden dataset stays frozen — offline scores stay green while users complain).
4. **The structural gap:** offline evals need a golden dataset with correct answers; **in production there is no answer key**. Online eval is the evaluation you run on **live production traffic**, and its defining feature is that it **works without one**.
5. **Offline and online are complementary, never rivals:** offline checks whether the application **works correctly**; online checks whether it's **running normally** in production. Correctness is often unmeasurable online (no human marks for this answer) — so you watch **normality**: compare score distributions against a baseline, and treat a shift as an investigation trigger (while remembering the shift might have a benign cause — "maybe very intelligent students started taking the exam").
6. **Quality without an answer key, two ways:** use **reference-free metrics** (faithfulness = is the answer generated from the retrieved context — computable from context + answer alone) or **user feedback** (a spike in thumbs-down in the past hour is your correctness proxy).
7. **The online pipeline:** **log everything** (IDs, turns, question/context/output, latency, tokens, cost, errors, thumbs, escalations — in a tool like **LangSmith**, with logging that is non-blocking, durable & queryable, late-signal-attaching, and PII-masked) → split signals into **captured** (thumbs, latency, tokens, cost — straight to dashboards and alerts) and **computed** (faithfulness, hallucination rate, toxicity… — needing a **reference-free LLM-as-a-Judge evaluator** and **sampling**, ideally **stratified** toward risky conversations: money, thumbs-down, escalations, rephrasing) → **dashboard over time windows** → **alert on thresholds** against an **offline-derived baseline**.
8. **The self-improving loop:** production failures get **added back to the offline dataset** (LangSmith's "Add to Data Set", annotation queues), so offline evals re-run on reality — offline → production → failures → richer dataset → re-deploy, forever.
9. **One metric improving is not progress:** 92→99 on one quantity counts only if nothing else regressed — LLM systems improve one thing and break others by default.

## Interview angles

- *"What's the difference between offline and online evaluation?"* → Timing, data (fixed golden dataset vs live traffic), answer key (present vs absent), inputs (anticipated vs anything), what they catch (regression vs drift/emergence), cost profile (cheap/repeatable vs sampled-at-scale) — and the closer: "they're complementary; offline tells me the app works *correctly*, online tells me it's running *normally*."
- *"Your offline evals all pass, but users complain in production. What's happening?"* → Walk the three production risks — input superset (Hinglish, adversarial), emergent failures at scale (latency, subtle bias), and drift (corpus moved, golden dataset froze) — then explain the fix: online eval plus the promote-failures-back-to-the-dataset loop.
- *"How can you measure quality in production when you don't have the correct answer?"* → Reference-free metrics (faithfulness from context+answer via a judge), user feedback (thumbs spikes), and baseline distribution monitoring — name the correctness-vs-normality distinction explicitly.
- *"Design an online evaluation pipeline for a RAG chatbot with 50,000 conversations a day."* → Non-blocking durable PII-masked logging (LangSmith) → captured signals to dashboards/alerts → computed signals via sampled reference-free LLM-as-a-Judge (hallucination, toxicity) → stratified sampling over random (money/thumbs-down/escalation strata, plus a small unbiased sample) → thresholds baselined from offline evals → failures promoted into the golden dataset.
- *"Your faithfulness dashboard shows 75 today. Is that bad?"* → Only relative to the baseline from your offline eval: 87 vs 85 is fine, 75 vs 85 in 24 hours is a drift signal — alert, investigate, improve.

## Cross-links

- **Previous:** [05 — Eval Methods: LLM-as-a-Judge, Reference-Based vs Reference-Free](05-eval-methods-reference-based-vs-free.md) — the reference-free judging this lecture deploys online.
- **Next:** [07 — LLM Model Evals & Capabilities](07-model-evals-capabilities.md) — the model-level track the course pivots to ("everything so far has been application-level").
- **Hands-on continuations:** [19 — Online RAG Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md) (this lecture's overview, made practical), [18 — RAG Regression Testing](18-rag-regression-testing.md) (purpose 3 in depth), [16 — Security Testing](16-rag-security-toxicity-leakage-scope-drift.md) (the security evaluator templates).
- **Reference depth:** [Section 105 note 1 — Evaluation Fundamentals](../01-evaluation-fundamentals.md) (the offline/online table and the proxy-vs-audited quality distinction) and [note 5 — Eval Engineering](../05-eval-engineering.md) (release gates, thresholds-as-config, the self-improving suite).
- **The monitoring handoff:** [104 — LLMOps](../../104_LLMOps/README.md) — observability, dashboards, and alerting infrastructure.
- **Course hub:** [README.md](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 05. Eval Methods Reference Based vs Free](05-eval-methods-reference-based-vs-free.md) · [Course hub](README.md) · [07. Model Evals Capabilities →](07-model-evals-capabilities.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
