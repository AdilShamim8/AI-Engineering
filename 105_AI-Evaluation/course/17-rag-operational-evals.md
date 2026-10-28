# 17 — RAG Operational Evals: Faster & Cheaper RAG Systems

> **Lecture 17 of 19** · Unit 4: Production Evaluation · 1:19:32
> RAG Operational Evals: Building Faster & Cheaper RAG Systems (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/17-rag-operational-evals.md)

---

## What this lecture covers

The last five sessions built one thing: the **RAG eval suite** for the CampusX Doubt Solver. Component level ✅, pipeline level ✅, application *quality* ✅, application *safety* ✅. Exactly one box in the flowchart is still empty — **operations**. This lecture fills it, hands-on:

1. **What operational evals are** — the eval family that asks "can this system run *reliably, quickly, and cheaply*?" instead of "are the answers good?" — and why, unlike every eval so far, they need **no LLM judge and no golden dataset**
2. **Why they belong in the *offline* suite** even though they sound post-deployment — the before/after scenario (quality ↑, latency 2.3→4.1 s, cost 72 paise→₹1.08) that proves the point
3. **Latency in depth** — ten measurement considerations (P50/P95/P99, component breakdown, TTFT, cold starts, token counts, throughput, repeated runs, timeout tracking, budgets, segmented workloads), a working `eval_latency.py`, its failing report, and the reduction playbook (model router, k, compression, caching, infrastructure co-location)
4. **Cost** — where the money goes (LLM tokens above all), five considerations, `eval_cost.py` with its ~2-paise-per-query result and ₹1,700/month projection, and the shorter reduction playbook
5. **Reliability** — error/success/timeout/retry rates, failure categorization, reliability under load, and `eval_reliability.py`'s honest 100% result — closing with the **complete eval suite** that regression testing (next lecture) turns into a deploy/no-deploy decision

---

## 1. Recap: the eval-suite flowchart — and a plan change (00:00–01:59)

The instructor opens with the flow diagram he made for this session ("I used to draw the same diagram repeatedly. That's why in this session, I made this flow diagram"). It summarizes the last five sessions: building and evaluating a RAG application — the **doubt-solving chatbot** that helps students with the LLM course. The eval suite plan had **three levels**:

1. **Component-level evals** — done (lectures 13–14)
2. **Pipeline-level evals** — done (lecture 14, the RAG Triad)
3. **Application-level evals** — quality done (lecture 15), safety done (lecture 16), **operations not yet**

So in the entire flowchart, only one part is left: **operations** — today's entire focus.

A plan change is announced honestly: regression testing was originally going to be squeezed into this lecture too, but the instructor is not feeling well, so it moves to the next session. Today's goal: **finish building the complete eval suite**, then use it for regression testing next time.

---

## 2. What are operational evals? (01:59–04:36)

**Operational evals for a RAG application answer a different question from quality evals** such as correctness, faithfulness, and relevance. Every eval studied so far — component, pipeline, or application level — judged the *quality* of the application: how good the output is. Operational evals do not answer that question; they tell you whether you are able to run your application **reliably, quickly, and cheaply**. The slide's phrasing:

> Even if the RAG system gives good answers, can it run reliably, quickly, and economically in production?

The second key difference: **almost every metric so far used an LLM as a judge internally** ("most of them, I guess all of them"), and several needed golden datasets. Operational evals need **neither**. You simply measure a software system on different qualities. As the slide says:

> Operational evals are primarily **software and telemetry-driven**; unlike quality evals, they usually do not require golden datasets or LLM judges.

So: operational evals are the set of measurements that tell you whether your RAG application, once deployed, will work **reliably at scale, quickly, and economically** — with no judge, no golden dataset, just direct measurement of the running system.

---

## 3. The three main operational evals — plus the one deferred (04:36–05:52)

| # | Operational eval | The question it answers |
|---|---|---|
| 1 | **Latency** | How long do your users have to wait to see the answers? |
| 2 | **Cost** | How much money are you spending to answer per query? |
| 3 | **Reliability** | How many times did the entire pipeline run correctly vs. hit an error? |
| 4 | **Throughput** | How many requests can be served in a given time? — **deferred**: requires load testing, which is out of scope for this course |

These three — latency, cost, reliability — are the lecture's agenda.

---

## 4. Why operational evals belong in the *offline* suite (05:52–14:04)

The instructor poses a genuinely sharp question to the class. By definition, operational evals tell you whether the application is working correctly **after deployment** — so it *sounds* like they only come into the picture post-deployment. Does that mean they **shouldn't be part of the offline eval suite** we just spent five sessions building — are we wasting our time? He polls the class: "First, say yes or no." Most people say yes; a couple aren't sure. The answer is **obviously yes** — and the reason is a worked scenario.

You built a RAG application: top-5 chunks from the retriever, fed into an LLM, answers generated. You measured quality — **correctness 91%, faithfulness 94%, answer relevance 93%** — and then, wisely, also measured the operational metrics:

| Metric | Before | Change made | After |
|---|---|---|---|
| Correctness | 91% | — | 95% |
| Faithfulness | 94% | — | 96% |
| Answer relevance | 93% | — | 95% |
| **Average latency** | 2.3 s | + re-ranker | 4.1 s |
| **P95 latency** | 4.8 s | + top-10 chunks (was 5) | 6.2 s |
| **Average cost per query** | 72 paise | + larger LLM | ₹1.08 |
| **Timeout rate** | 2% | — | 1% (improved) |
| **Success rate** | 99.8% | — | 99.9% (improved) |

(P95 latency is a type of latency — explained in the next section.) The three changes — **re-ranker, k=5→10, larger LLM** — were big, and quality went up on every axis. But because operational evals existed, you *also* saw the price: latency nearly doubled, cost per query went up 50%.

**What if you hadn't measured?**

> "Your latency suddenly went from 2.3 seconds to 4.1 seconds. And you wouldn't even know it, and you would have deployed it, and suddenly your users would say, 'Hey, your application has suddenly become slow.' You would start paying more money. You wouldn't even know how much more you were paying."

Measuring only quality is not enough. As a team building a RAG application for scale, you should have everything clear beforehand — **operational evals give you the complete picture**, including whether the system has **regressed**.

**The honest caveat — absolutes vs. differentials.** The instructor is careful: an offline value like "2.3 seconds on your laptop" does **not** mean production will also be 2.3 seconds — absolute offline values are *not potent*. But the **differential** — 2.3 vs 4.1 — is true: latency increased because of the new model and the other changes, and that direction is reliable. That differential is exactly what tells you **what broke** when you make changes.

A student (Tarun) asks the right follow-up: this assumes the setup stays identical between the two experiments. Yes — that's the assumption. If you change the experimental setup itself, the direction you get is not reliable. Offline experiments are always run on the same setup.

Operational evals' natural home is post-deployment — observability tools like **LangSmith** or **Confident AI** log these values **by default**, and that's where they have the highest relevance (the online-evals session). But that doesn't make them unnecessary offline. The slide line that summarizes the whole discussion:

> **Do not wait until production to discover that your RAG pipeline is too slow or too expensive.**

---

## 5. Latency: definition and the naive timer (14:04–16:47)

"Come on, latency is very important, guys." In interviews and in real company chatbot work, latency considerations dominate — the next stretch of the lecture deserves full focus.

**Definition:** latency is the amount of time a system takes to respond to a request. The user typed *"What is MMLU?"* and hit enter — how long until they see the full reply? That duration is the latency.

The naive measurement is a timer around the pipeline: take the question → pass it to the RAG pipeline (which internally calls the retriever for context, then sends context + question to the generator, which calls the LLM and returns the answer) → start a counter before the call, close it after, compute `close − start`. That's genuinely all a latency measurement *is* — but it is **not that straightforward**: there are considerations — ten of them — that a real latency eval script must respect.

---

## 6. Consideration 1 — prefer latency distributions over averages: P50, P95, P99 (16:47–21:50)

In production, latency lives on a dashboard card, always within a **time window** — last 1 hour, last 24 hours, last week, last month. Say the window is one hour and **2,000 students** each asked one question: every question has a latency value → **2,000 latency values**. Plot them as a distribution (a PDF): most students got answers around **2 seconds**, very few around **1 second**, very few around **4 seconds**. The rule: **don't simply report the mean** of those 2,000 values — report the percentiles:

| Statistic | Meaning |
|---|---|
| **P50** | 50% of all requests completed within this time — the **median** |
| **P95** | 95% of all requests completed within this time — the 95th percentile |
| **P99** | 99% of all requests completed within this time — the 99th percentile |

Why the tail matters: the average case being fine at 2 seconds is okay — but you need to see the users who waited a *long* time, because **their experience is very poor**. P95 and P99 are the worst-case scenario; they tell you how bad the bad experience is. Observability tools like LangSmith compute all of these for you directly from the distribution of latency values.

> 💡 **Expert commentary.** Latency distributions are almost always **right-skewed** — a handful of slow requests drag the mean far above the median, so the mean systematically overstates the typical experience while hiding nothing about the tail. Percentiles are *order statistics*: robust to those outliers, which is why SLO practice (Google SRE et al.) writes targets as "P95 < X" rather than "mean < X." Two additions worth knowing: (1) at small sample counts, high percentiles are basically the max — your P99 from 50 runs is one noisy number, which is exactly why the instructor later recommends 500–1000 runs; (2) in systems that fan out (one answer touching retriever + reranker + LLM), the *slowest* component dominates the user's wait — the classic "tail at scale" finding (Dean & Barroso, CACM 2013) — so P99 gets *more* important as your pipeline gets more components.

---

## 7. Considerations 2 & 3 — component-level breakdown, and TTFT (21:50–24:30)

**Consideration 2 — report component-level latency, not just end-to-end.** End-to-end latency (question in → answer out) is needed, but always break it down: if overall end-to-end is **4.5 seconds**, report that the **retriever took 1.5 s** and the **generator took 3 s**. Go finer: how much time in **embedding**, in **retrieval** from the vector database, in **re-ranking**, in the **generator**. There is no benefit in just the end-to-end value — the breakdown shows where the time goes, and therefore **where there is scope for improvement**.

**Consideration 3 — measure TTFT separately.** (The instructor first expands it loosely as "Total Time to First Token," then settles on the standard expansion: **Time To First Token**.) All LLM apps **stream**: as soon as the first token arrives from the LLM, it's shown on the screen — that's why answers look like they're being *printed* in front of you rather than appearing all at once. Streaming exists because it improves user experience, for two reasons:

1. **Readability** — if the entire text suddenly appears at once, it's difficult to read; if words appear one by one, the user reads along as it generates.
2. **Perceived speed** — if an answer takes a long time to generate and you wait for the whole thing, nothing is visible on the screen for a while and the user gets frustrated ("Man, I can't see anything"). With streaming, there's immediate movement, so the user sits patiently. So don't just measure end-to-end latency — also state the **TTFT**: your question went to the LLM; how long until the LLM produced the *first* token?

> 💡 **Expert commentary.** TTFT and end-to-end latency are governed by *different physics*, which is why they need separate SLOs — exactly the two budgets this lecture's script defines. TTFT is dominated by **prefill** (processing the prompt + retrieved context) plus queueing, so context-size levers (smaller k, compression) move TTFT. The remaining time is **decode-bound** — roughly output tokens ÷ tokens-per-second — so output-length caps move time-to-completion but barely touch TTFT. Streaming converts the second quantity into *perceived* latency: users tolerate long streamed answers if the first token lands quickly. A production dashboard should carry both numbers, with different budgets and different owners.

---

## 8. Considerations 4 & 5 — cold starts; token counts and context size (24:30–27:57)

**Consideration 4 — watch for cold starts.** The analogy: when you start your machine, it takes 5–10 seconds to boot — that's a cold start. The same happens at the server level: your server restarted, the vector database just came up, or the server hosting your LLM API just started. Per the slide, a cold start occurs whenever **a connection is being initialized** — a model loading, a vector-DB connection being set up, a network handshake, a cache initializing, a container or serverless function starting up. All of these add extra time to the *first* question.

Practical rule: **skip the first one or two questions when measuring latency; start measuring from the third.** The instructor's own example from this course: the first run shows the reranking model downloading from Hugging Face — a cold start. It doesn't happen on subsequent questions because the model is already loaded.

**Consideration 5 — always specify the token count and context size of the answer.** Latency depends on both: a very long answer takes more time to generate; a large context sent to the LLM takes more time to process. Report the token count alongside the latency value, or the latency number is uninterpretable.

---

## 9. Considerations 6 & 7 — latency vs. throughput; repeating runs (27:57–31:47)

**Consideration 6 — distinguish latency from throughput.**

| Concept | Definition |
|---|---|
| **Latency** | Time taken to process a *single* request |
| **Throughput** | How many requests the system can handle in a given amount of time (concurrently) |

The analogy: **latency** is how long a customer waits in a restaurant for their food to arrive at the table; **throughput** is how many customers the kitchen can serve in an hour. Below a certain threshold of concurrent load, latency stays fine — cross it, and latency rises too. Example: a server that handles **10,000 concurrent users** suddenly gets **20,000** — the first 10,000 are served, the next 10,000 queue, and the queued 10,000 experience high latency. So always measure (or at least state) the concurrency context: on your laptop, one user, single request — say so. On a server, state the concurrent-user count at which the latency was measured.

**Consideration 7 — repeat runs, because external APIs are noisy.** A script with 10 sample questions sent once gives 10 latency values — **not reliable**, because the LLM is an external API and its server may be having issues. Recommendation: send **every question five times** → 50 latency values → average per question to reduce the noise.

---

## 10. Considerations 8–10 — timeouts, budgets, representative workloads (31:47–36:16)

**Consideration 8 — track failures separately from latency.** Suppose you ran the 50-request trial and P95 came out at 3 seconds — but **1% of requests timed out** (the instructor's arithmetic aside: 2% of 50 is one request; 1% would be 0.5 — "let's assume it's two… well, one doesn't matter"). Now a second experiment: timeout rate jumps to **8%** (four questions unanswered), but P95 *drops* to 2 seconds. It looks like latency improved — a **false sense of improvement**. In reality, many questions aren't being answered at all, and only the answered ones have lower latency. Always measure the **timeout rate alongside latency**, or latency-in-isolation lies to you.

**Consideration 9 — define latency budgets, at system level *and* component level.** Decide, per your application and business: "our **P95 latency should never exceed 3 seconds**" — a constitution for yourself. Component-level too: "the retriever should never take more than 1 second." Where does the number come from? A mixture of your application, your users, and industry standards — but you must have *one* number, and it lives in your script as the threshold you don't cross.

**Consideration 10 — use representative and segmented workloads.** Of your 10 test questions: **3 simple, 4 medium, 3 complex.** Every question type a real user might ask should be represented — otherwise you send only easy questions, get a flattering latency, deploy, and discover a completely different latency on the server when people ask all sorts of questions.

> "It's not as simple as… you started a counter or timer, you called the RAG application, as soon as you got the answer you stopped the timer… No — you create a script considering all these things."

---

## 11. The latency eval script: `eval_latency.py` (36:16–41:13)

The instructor created the script **with the help of Claude**, giving it exact instructions to honor all the considerations above. It's ~100 lines — he explicitly won't walk through it line by line ("looking at it, you won't understand. But the idea is the same") — and urges reading the docstring. The design parameters:

| Parameter | Value |
|---|---|
| Test questions | **5 questions** |
| Repeats | Each question sent **5 times** → **25 LLM calls** (5×5) |
| Warm-up runs | **2** (the first two runs are discarded) |
| Budget (system) | **P95 end-to-end latency ≤ 3 s** |
| Budget (TTFT) | **TTFT ≤ 1.2 s** |

Workflow: create `evals/eval_latency.py`, paste the script, run `python -m evals.eval_latency` → a detailed report (it takes time — you're running the whole RAG application 25 times).

Two live-class moments worth keeping:

- **The streaming fix.** Mid-run he realizes the `src/generator.py` change hadn't been pushed to the project folder: a **streaming feature was added** to the generator (it didn't exist before) specifically so **TTFT can be measured**. He copies the updated `generator.py` into `src/` and re-runs — an authentic fix-on-camera moment.
- **A self-correction on warm-up.** The report shows the reranker "warming up, two runs discarded" — and he corrects his earlier phrasing: the script does **not** discard the first two runs *of every question*; it discards **only the first two runs overall** (out of the 25).
- **Honesty about sample size.** 25 runs is *low* — "you would probably do this 500 or 1000 times to get a good reliable number. But again, this is all we can do for now."

---

## 12. Reading the latency report — and failing both SLOs (41:13–45:26)

The output is a table where **each row is a metric**:

| Metric | Mean | P50 | P95 | P99 | Min | Max |
|---|---|---|---|---|---|---|
| **End-to-end latency** | 3.6 s | 3.8 s | 5.3 s | 5.3 s | 1.3 s | 5.3 s |
| **TTFT** | 1.6 s | ~1.6 s | 2.0 s | 2.1 s | 1.3 s | ~2.1 s |
| **Retrieval** | ~700 ms (756) | 762 ms | 983 ms | >1 s | — | ~1 s |
| **Generation** | 2.9 s | — | — | — | — | — |
| **Answer length** | ~1,158 characters (average across the five questions) | | | | | |

- **End-to-end**: mean 3.6 s ("when we sent all our 20 questions" — his reading of the measured runs; the design was 5×5 calls with 2 warm-ups discarded), median 3.8 s, P95 5.3 s, P99 5.3 s, min 1.3 s (one question answered in just 1.3 s), max 5.3 s.
- **The breakdown**: retrieval ≈ 700 ms + generation 2.9 s ≈ the end-to-end number. The generator takes **almost 4× longer** — expected: the generator calls the LLM, while the retriever ran locally. Retrieval's own spread is tight (756 / 762 / P95 983 ms, P99 just crossing 1 second) — the main time sink is clearly **generation**.
- **TTFT**: mean 1.6 s — the user starts seeing the first token after 1.6 seconds on average, "which is good, not bad." P50 similar, P95 2 s ("again kind of fine"), P99 2.1 s, min 1.3 s. And **answer length**: ~1,158 characters average — reported because **latency scales with output length**: longer answers → higher latency; shorter → lower.
- **The SLO check** — the script's own budget verdict against the **SLO (Service Level Objective)** thresholds defined earlier:

| SLO | Budget | Actual | Verdict |
|---|---|---|---|
| End-to-end P95 latency | 3,000 ms | 5,300 ms | ❌ FAIL |
| TTFT P95 | 1,200 ms | 2,081 ms | ❌ FAIL |

Failing both means one thing: **go back and improve the RAG pipeline** so it meets its SLOs — which triggers the next discussion: how?

---

## 13. The latency-reduction playbook (45:26–51:52)

"Now your entire team will sit down and discuss how we can reduce latency." The playbook, as listed:

**Generator-side levers**

| Lever | How it works | Notes |
|---|---|---|
| **Faster model** | e.g. currently on **Gemini 3.1** → switch to its **flash variant** | Slight quality hit possible; decide by whether your app needs quality or speed more |
| **Model router** | Classify each incoming question: simple → small model, complex → heavy large model | Latency drops for simple questions, so the overall average P95 can come down |
| **Concise answers + length limit** | Prompt the generator to be concise; even set a hard cap — literally write in the system prompt "make sure your answer does not exceed 500 words" | Bounds the decode time directly |

**Context-side levers** — reduce the context size sent to the generator: reduce **k** (k=10 → k=5), or use **contextual compression** — send a compressed version of the context instead of the whole thing. Trade-off warning: compression itself takes time, so evaluate the net win.

**Retriever-side levers** — break the retriever down further: time the query embedding separately, the vector-database retrieval separately, the reranker separately — then improve the slow one. Currently ~700 ms; maybe you can bring it to 500 ms.

**Caching.** Caching increases speed: if something repeats, store it instead of reprocessing. Cacheable at many levels:

| Cache level | What you store |
|---|---|
| **Embeddings** | The same question keeps coming → store its embedding; don't re-vectorize |
| **Retrieval** | Same question → same retrieved context every time → store it |
| **Reranking** | Same question + same context → same reranking → store it |
| **System prompt** | Only two things vary per request — the question and the context. All your big rules are being sent repeatedly; cache them |

**Infrastructure distance.** An "actually interesting" lever: **optimize the distance of your infrastructure**. Suppose your vector database is hosted in **Mumbai**, your reranker is an API (e.g. **Cohere**, which takes question + context and returns the reranked context) hosted in the **US**, and your LLM API is in **Europe**. Three systems communicating across the globe add half-seconds and fractions of seconds. Instead: if you serve the **India region**, put the reranker, vector DB, and LLM **all in the India region**; likewise for the US. "You can save fractions of a second with this too." Latency matters a lot — it is *critical* for certain applications, and something you need to understand well and then solve.

---

## 14. Cost: where the money goes (51:52–56:36)

**Cost** is how much money your system spends to answer one query. Before the slide, the instructor asks the class to think and write: *where in the RAG pipeline is there scope for spending money?*

| Cost source | Detail |
|---|---|
| **The LLM** (biggest expense) | Someone's API — OpenAI, Anthropic — paid **per request**, priced on **tokens**: input tokens in + output tokens out → a rate is applied |
| **Commercial vector database** | e.g. **Pinecone** — you pay for better service and better performance |
| **Paid reranker** | e.g. the **Cohere** reranking API |
| **Embedding model** | Repeatedly converts questions into vectors; "this cost isn't that high, it is still a cost nonetheless" |
| **Infrastructure** | Wherever your application is hosted |

The instructor's framing: "Go to any company or application developer and ask them where they have spent money like water. They will always tell you that **the token burn from our LLMs is the biggest cost factor**." So cost analysis focuses on the LLM. (When you build real operational evals you'll measure the whole system's cost — but this project's assumptions are: free vector database, free reranker, small/local embedding model, nothing deployed yet. So the entire discussion is **LLM cost**.)

The slide definition:

> Cost is the **monetary expense incurred to process a user query, driven primarily by the LLM tokens consumed during generation**.

The computation is conceptually simple: **measure the tokens, multiply by the rate**. Rates live on the provider's pricing pages — check **OpenRouter** for any model, or the OpenAI models page — and are quoted **per 1 million tokens**, with **input and output prices different: assume output is ~4× more costly than input**. Then:

- Input tokens (your system prompt etc.) × input rate = **input cost**
- Output tokens (what the LLM generated) × output rate = **output cost**
- Input + output = **total LLM cost**

---

## 15. Computing cost — and its five considerations (56:36–59:02)

| # | Consideration | What to do |
|---|---|---|
| 1 | **Cost per query** | The most relevant number — not just "what we spent in the last hour / day / month" (those are calculated too, but per-query is the headline) |
| 2 | **Input vs. output split** | Break the total into input cost and output cost — shows where the improvement scope is |
| 3 | **Cost as a distribution** | Don't take a single number: 2,000 queries → 2,000 cost values → plot them, look at **P95 cost** and the long tail. Maybe a typical question costs 2 paise, but some cost **₹1.5** and a few **₹3** — analyze *why* those tails are expensive |
| 4 | **Segment by query type** | Cost of simple vs. medium vs. difficult questions, separately |
| 5 | **Set a cost budget** | The business team gives a monthly ceiling ("we cannot spend more than this many rupees"); translate it per query — e.g. "not more than 50 paise per complex query" — so a budget always exists |

---

## 16. The cost eval script: `eval_cost.py` and its output (59:02–01:03:58)

Again **generated with Claude** from the full list of considerations (one gap acknowledged: the distribution part isn't implemented — "you can do it, though"). Design: **4 questions × 3 sends each**; pricing set from the known model name; budgets defined; and a USD→INR conversion factor that was wrong in the script — **88, where reality is ~95–96** — fixed live to ~95 ("I don't know the exact value right now. But I'm expecting something around 95"). Workflow: `evals/eval_cost.py`, then run it. One important property of cost as a metric, stated before running: **unlike latency, cost works fine offline** — rates are fixed, so costs don't fluctuate much between laptop and server; "latency has a lot of variance, but cost will work just fine even offline. So this is a slightly more reliable metric."

The output:

| Item | Value |
|---|---|
| Model | **GPT-4o-mini** — same model runs the chatbot *and* the evals ("Don't get confused") |
| Pricing | **$0.15 / 1M input tokens**, **$0.60 / 1M output tokens** (exactly the 4× ratio) |
| Samples | 12 (4 questions × 3) |
| Average input tokens | ~1,753 ("1700 something") — of which **1,109 cached automatically** |
| Average output tokens | 209 |
| **Average cost per query** | **≈ 2 paise** |
| Spread | Very tight min–max range → **cost is stable**, unlike latency |
| Input vs. output spend | **More on input than output** — the *opposite* of typical applications |
| Projection @ 2,000 queries/day | **₹57/day**, **₹1,700/month** — and "just keep increasing this number": at 5,000 requests the figures scale up |
| Budget verdict | Within budget → **passing the SLO** ✅ |

The input>output inversion gets its own explanation: generally applications spend less on input and more on output — the counter-example is a **coding agent**, where you send one instruction ("generate this file for me") and the entire work lands in the output, which costs a lot more. Our RAG app is the opposite: a large, repeated system prompt + context on the input side, a modest 209-token answer out.

> 💡 **Expert commentary.** This little report is **cost observability** in miniature — and its production version is a discipline of its own (LLM FinOps). Every provider response carries a `usage` object (prompt tokens, completion tokens, cached tokens); real dashboards join those fields with a **versioned pricing table** and attribute cost per feature, per tenant, per user. Two practical rules: (1) the **per-query number** (here, ~2 paise) is the unit-economics figure a business actually prices on — monthly totals are just it multiplied by volume; (2) never hardcode rates in code — providers change prices, cached-token discounts change, and your ₹-projection silently rots. Treat the pricing table like the thresholds file in [eval engineering](../05-eval-engineering.md): configuration, reviewed by diff. Note also that the 1,109 cached tokens weren't free — cached input is billed at a discount (OpenAI ~50%, Anthropic down to 0.1×), which is exactly why the effective input rate came out "slightly lower."

---

## 17. The cost-reduction playbook (01:03:58–01:06:16)

If you ever fail the cost SLO, the levers — noticeably fewer than for latency:

| Lever | How it helps |
|---|---|
| **Reduce context size** | Input tokens drop — and output tokens may drop too (less information to process → shorter answers). Use **smaller chunks** or **contextual compression** |
| **Efficient system prompt** | Carefully tweak it — "if it's currently 1000 tokens, how can I reduce it to 800 without losing the essence" |
| **Concise / word-limited answers** | Directly instruct the model to answer within a certain number of words |
| **Cheaper model** | "This option is always there" |
| **Caching** | At every level discussed for latency — especially **prompt caching**, which saves money on both input and output |

The structural insight: **there aren't too many ways to save costs, unlike latency** — where you can improve at the entire system level. Since most cost comes from the LLM, you can only optimize around it. **The biggest lever is which model you use.** If costs rise too much at scale, you can switch to **open-source models hosted on your own infrastructure** — that's where the biggest cost change comes from. Everything else is a minor optimization worth roughly a **±5% differential**.

---

## 18. No judges, no golden datasets — and the aggressive-caching Q&A (01:06:16–01:07:56)

A recap of what just made these three scripts special: **no golden dataset was created anywhere, and no LLM is used in these scripts** — no judging is involved. Which means **these scripts are free to run** (yes, questions go to the LLM internally — but nobody judges anything, so the eval itself costs nothing beyond the inference).

A student (Kritika) notices the aggressive caching in the cost report — **1,109 of 1,753 tokens cached** — and the instructor explains: that's because the script sends the *same question* three-four times in a row; the API recognizes the repetition and caches aggressively. **In a real production setup the caching factor will be lower, because the model receives different questions.** And the key clarification: **the provider (OpenAI) is doing this caching on their end — no caching code was written.** That automatic provider caching is why the input rates came out slightly lower.

> 💡 **Expert commentary.** What happened here is **automatic prefix caching** — providers detect repeated prompt prefixes (your system prompt, mostly) and bill the cached portion at a discount. The lecture's own cache list (embeddings, retrieval, reranking, system prompt) is all *exact-match* caching. One step beyond sits **semantic caching** (GPTCache-style): embed the incoming query, find the nearest *previously answered* query above a similarity threshold, and serve the stored answer — skipping the entire pipeline. It can be a massive cost/latency win for FAQ-shaped traffic, but it carries real risk: a "similar" question is not the *same* question, so a false-positive hit damages correctness, and caches go stale when the corpus or prompt changes. If you adopt it, do it behind the eval suite this course just built — the quality evals become the cache's regression gate.

---

## 19. Reliability: definition and metrics (01:07:56–01:10:13)

The third operational eval. The slide definition:

> Reliability is the ability of a RAG system to **successfully serve requests without errors, timeouts, crashes, or broken pipeline stages**.

The picture: 10 users arrive and each gives your chatbot a question. Only **8** get an answer; the other **2** see *"try again after some time."* The reason could be anything — the LLM API failed, the re-ranking API failed, the vector database couldn't produce context, your server was down. Serving only 8 of 10 means your system is currently **80% reliable**.

What you measure inside reliability:

| Metric | Definition |
|---|---|
| **Error rate** | Percentage of requests that failed |
| **Success rate** | Percentage served successfully — `1 − error rate` (the two are complementary) |
| **Timeout rate** | Percentage of requests that exceed the allowed time — **different from an error** |
| **Retry rate** | Percentage of requests that required **at least one retry** |

---

## 20. Reliability considerations (01:10:13–01:13:33)

| # | Consideration | What it means |
|---|---|---|
| 1 | **Overall success/failure rates** | Measure them, obviously |
| 2 | **Categorize failures** — no single generic error rate | A 20% failure rate must be broken down by *why* |
| 3 | **Reliability under load, separately** | A pipeline can be highly reliable in single-user offline tests and start failing when concurrency rises — failure rate always increases with concurrent users |
| 4 | **Enough samples** | 25–50 questions is too little — likely 100% answered; send ~1,000 and you'll finally see that one error |
| 5 | **Representative requests** | Simple queries, long-context queries, complex questions, queries producing long answers, and edge cases — complex queries may carry a higher error rate than simple ones |

The failure taxonomy for consideration #2 — the reasons to break a generic error rate into:

| Failure category | Example |
|---|---|
| LLM API failure | The model API itself failed |
| Retriever failure | Retrieval stage broke |
| Reranker failure | Reranking stage broke |
| Timeout error | Exceeded the allowed serving time |
| Rate-limit error | You can't make more than N API requests in the time period |
| Parser / formatting error | Output parsing broke |
| Internal exception | An exception triggered in your own code |

This categorization needs **extra code** — which this lecture hasn't written, but a proper company evaluation does: you wrap every API call in a **try-except block**, wrap the reranking step in one, and thereby learn *where* it broke.

> 💡 **Expert commentary.** Why does failure rate climb with concurrency? Three compounding mechanisms: provider **rate limits** start returning 429s; local resources (connection pools, memory) saturate; and queueing delays convert into **timeouts** — which then trigger **retries**, and naive retries amplify the very load that caused them (the retry-storm pattern; production systems add exponential backoff + jitter). The load and stress testing the instructor defers is exactly this field: tools like **Locust** or **k6** emulate thousands of virtual users, and a **soak test** (sustained moderate load for hours) catches slow leaks that quick runs miss. A useful mental model is Little's law (concurrency ≈ arrival rate × wait time): once wait time saturates, piling on requests can't increase throughput — it only inflates latency until things start timing out. Treat the 100% single-user laptop result as an *upper bound*, not an estimate.

---

## 21. The reliability eval script — 100% success, and the dev-vs-prod Q&A (01:13:33–01:17:13)

`eval_reliability.py` — with the instructor's own disclaimer: "This code is not quite production-grade. I am saying this myself. But it will do the work." It measures the three things: **error rate, success rate, retry rate**. Setup: **4 questions × 5 sends = 20 API hits**, with **max retries = 2** (even if a retry comes into play, at most two are allowed).

The result, as predicted: **success rate 100%, error rate 0%, zero retries** — every request answered on the very first try. Why so clean? Because the setup is too ideal to produce bad numbers: 20 requests from a laptop against a very reliable API. Two remarks sharpen this:

- **Ollama**: if you were using Ollama models (it has cloud models too) instead of OpenAI, you'd see the reliability score come down.
- **Himanshu's point** ("DeepEval has five metrics per 100 golden…") — "yes, yes right" — and the related observation: use a more expensive model and you start getting **rate-limiting errors** too. It all depends on the setup. Increase requests, increase users, use a slightly less reliable API — "there, you will see all these numbers spike."

Post-deployment, with thousands of users arriving in a time period, these numbers become **very meaningful**: how many requests served successfully, the error rate, how many needed retries, how many faced timeouts. On a laptop setup, they honestly don't matter much — but the evaluation suite you're building must include them.

**Tushar's question — separate budgets for dev vs. prod testing?** (If you test by passing 1,000 questions in dev mode, that costs money.) Answer: **no — at least not for cost.** You *can* do it for **latency**, because production latency is generally higher than what you see on your machine (the system is online, one server here and another there, latency might increase, tokens could spike, the budget might go up). But **cost remains the same** — rates don't change between dev and prod.

---

## 22. Wrap-up: the eval suite is complete (01:17:13–01:18:55)

Three things were covered under operational evals: **latency** in detail, **cost/tokens** in detail, and **reliiability**. The fourth — **throughput** — needs **load testing** and **stress testing**, with dedicated software that emulates many requests hitting your application; out of scope here, but in a proper company production setup it is also an important aspect.

With that, **the entire RAG eval suite is built** — "it took five sessions, but this entire thing is done":

| Suite level | Evals | Built in |
|---|---|---|
| Component | Retriever (recall/precision), generator (faithfulness, answer relevance) | Lectures 13–14 |
| Pipeline | RAG Triad (faithfulness, answer relevance, contextual relevancy) | Lecture 14 |
| Application — quality | Correctness, completeness, style (G-Eval) | Lecture 15 |
| Application — safety | Toxicity, leakage, scope drift | Lecture 16 |
| **Application — operations** | **Latency, cost, reliability** | **This lecture** |

What remains is to **create the regression testing flow**: using that flow and this suite, you will always be able to tell whether — after any given change — the system **improved, stayed the same, or got worse**, and based on that, answer whether or not to deploy the new version. After regression testing, one session remains (**online evals**), and then the course moves to **agent evaluation**, which can go faster now that the fundamentals are clear.

The instructor's closing defense of the pace: "I know we took a lot of time on this whole thing. But you might agree that we didn't waste time anywhere. This entire RAG evaluation we studied, we consciously decided to study it very well… There is no time wastage anywhere. I hope you agree."

---

## Key takeaways

1. **Operational evals ask a different question.** Quality evals (correctness, faithfulness, relevance) judge the output; operational evals ask whether the system runs **reliably, quickly, and cheaply** in production.
2. **No judges, no goldens, no eval cost.** Operational evals are software- and telemetry-driven measurements — no LLM-as-a-judge, no golden dataset, so the eval scripts themselves are free to run.
3. **Three evals (plus one deferred): latency, cost, reliability** — throughput requires load testing and was declared out of scope.
4. **Keep them in the offline suite for the differential.** Absolute offline values (laptop latency) aren't dependable, but the *before/after delta* is true — the 91→95 correctness upgrade that silently cost 2.3→4.1 s latency and 72 paise→₹1.08 per query. "Do not wait until production to discover that your RAG pipeline is too slow or too expensive."
5. **Latency has ten measurement considerations**: P50/P95/P99 distributions (tail = worst-case UX), component-level breakdown, TTFT, cold starts (skip the first two runs), token/context reporting, latency-vs-throughput (restaurant analogy), repeated runs (noisy external APIs), timeout tracking (else a false sense of improvement), system+component budgets, and simple/medium/complex workload mixes.
6. **The worked latency run failed both SLOs**: end-to-end P95 5.3 s vs. 3.0 s budget; TTFT P95 2,081 ms vs. 1,200 ms — generation (~2.9 s) dominated retrieval (~0.7 s), triggering the improvement loop.
7. **The latency playbook**: faster/flash models, a model router (simple→small model), concise/length-capped answers, smaller k, contextual compression, retriever sub-breakdown, caching at four levels (embeddings, retrieval, reranking, system prompt), and co-locating infrastructure per region.
8. **Cost = tokens × rate; output ≈ 4× input.** Cost per query is the headline; cost is *stable offline* (unlike latency) because rates are fixed. The GPT-4o-mini run: ~1,753 input tokens (1,109 auto-cached), 209 output, **≈2 paise per query**, ₹57/day and ₹1,700/month at 2,000 queries/day — passing the budget, with input spending exceeding output (unlike the coding-agent pattern).
9. **The cost playbook is shorter**: context size, prompt efficiency (1,000→800 tokens), word-limited answers, caching, cheaper model — the **biggest lever by far is the model itself** (open-source self-hosted at scale); everything else is ±5%.
10. **Reliability = success / error / timeout / retry rates, with failures categorized** (API, retriever, reranker, timeout, rate limit, parser, internal exceptions) and measured **under load with enough samples** — the laptop's 100% success is an artifact of an ideal setup, not a production estimate.

## Interview angles

- *"Why would you measure latency and cost *before* deployment if they're production metrics?"* → The differential argument: offline absolutes aren't dependable, but the before/after delta from a controlled same-setup experiment reliably tells you what a change broke — quality metrics alone would have hidden the 2.3→4.1 s and 72-paise→₹1.08 regression.
- *"Why report P95/P99 instead of average latency?"* → Right-skewed distributions; the mean hides the tail where the worst user experience lives; percentiles are robust order statistics and are how SLOs are written. Bonus: name the other nine measurement considerations (component breakdown, TTFT, cold starts, token counts, throughput context, repeats, timeouts, budgets, workload mix).
- *"What's the difference between latency and throughput — and how do they interact?"* → Single-request wait vs. requests served per unit time; the restaurant/kitchen analogy; above the concurrency threshold, queues form and latency rises (10,000-user server meeting 20,000 users).
- *"Your latency improved but the timeout rate went from 2% to 8% — good news?"* → No: failures are excluded from latency, so survivors look faster; always report timeout/reliability metrics alongside latency.
- *"Your cost per query doubled after a quality upgrade — what are your levers?"* → Reduce context (k, chunk size, contextual compression), tighten the system prompt, cap answer length, prompt caching — but the dominant lever is the model choice itself (±5% for everything else).
- *"How would you evaluate the reliability of a RAG system?"* → Success/error/timeout/retry rates; categorize failures with try-except instrumentation; measure under load with enough samples and representative queries; single-user offline reliability is an upper bound.

## Cross-links

- **Previous:** [16 — Securing Your RAG Application: Toxicity, Leakage & Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) (the safety half of the application level — this lecture completes the suite)
- **Next:** [18 — RAG Regression Testing](18-rag-regression-testing.md) (the whole suite becomes the improved/same/worse gate for deploy decisions)
- **Parent notes:** [Section 105 note 5 — Eval Engineering](../05-eval-engineering.md) (budgets and thresholds as reviewable configuration; the CI release gate this suite feeds) · [104 — LLMOps](../../104_LLMOps/README.md) (observability, latency & responsiveness, scaling — where these metrics live in production)
- **The suite's earlier floors:** [12 — The RAG Eval Interview Answer](12-rag-eval-interview-answer.md) (the three-level plan), [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md), [14 — RAG Triad](14-rag-triad-generator-pipeline.md) (the chunk-size/noise homework behind this lecture's context levers), [15 — G-Eval](15-geval-deterministic-judge.md)
- **Prompt-caching economics in a procurement decision:** [11 — Selecting the Right LLM](11-model-selection-custom-evals.md)
- **Where these numbers get logged by default:** [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md)
- **Course hub:** [README.md](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 16. RAG Security Toxicity Leakage Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) · [Course hub](README.md) · [18. RAG Regression Testing →](18-rag-regression-testing.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
