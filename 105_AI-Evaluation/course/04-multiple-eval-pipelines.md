# 04 — Multiple Eval Pipelines

> **Lecture 4 of 19** · Unit 1: Foundations · 28:03
> Why Your AI Application Needs Multiple Eval Pipelines? (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/04-multiple-eval-pipelines.md)

---

## What this lecture covers

Lecture 3 closed on a single sentence — *one LLM application may have several LLM evals*. This lecture is the proof of that sentence, delivered "very intuitively" through one running example and a series of live audience polls.

The thesis: **whenever you build an LLM application, 99.99% of the time it needs more than one evaluation pipeline** — for two independent reasons:

1. **Multiple failure points** — an LLM application can break at the **component level**, the **workflow level**, and the **application level**. The centerpiece is a thought experiment where the retriever and the generator *both pass* their own evals while the application still returns a wrong answer.
2. **Multiple risk categories** — attached to every failure point are independent aspects of risk — **quality**, **safety**, and **operations** — and each aspect becomes its own pipeline.

The mental model to keep: **a pipeline per failure point, and a pipeline per risk. Never one pipeline for everything.**

---

## 1. Where we are — and the one line that starts this lecture (00:00–03:26)

The instructor opens with a joke about how early we still are — "technically, we haven't had a single class in this course yet" — and then recaps the three things covered so far:

1. **Why we need LLM evaluations** — argued through case studies, answering the question: how can you deploy an LLM application into production without evaluating it?
2. **What LLM evaluations are** — a **systematic and reliable way of evaluating LLMs and LLM-based applications against clear criteria**, and the two types: **Model Evaluation** (evaluating the LLMs themselves, using benchmarks) and **Application Evaluation** (evaluating the LLM applications you've built). The course revolves mostly around application evaluation — as an AI engineer, that is where your time goes. Model evaluations are generally done in frontier labs; you still learn them so you can understand and decide *which LLM your application needs*.
3. **How evaluation is done** — the step-by-step eval pipeline walked through in the previous session.

Today's lecture begins from the **last line** of that session, which the instructor repeats for emphasis:

> When you build any LLM application, it doesn't have just *one* eval pipeline — it has **multiple eval pipelines**.

The plan for today: discuss *why* this is so — why one eval pipeline can never be enough — intuitively, with examples.

---

## 2. The running example: a RAG chatbot (03:26–04:07)

The vehicle for the whole lecture: a **RAG chatbot** built "for our company, our school, or college — whatever." By now you should have the components memorized:

- a **retriever** connected to a **vector database**,
- which retrieves documents and hands them to a **generator**,
- which generates the answer.

The flow:

> **user query → retriever → fetches relevant documents from the vector database → query + retrieved documents → generator (an LLM) → answer based on the relevant context.**

"That is the setup of RAG." Now the question: why does this application need multiple eval pipelines?

---

## 3. Reason 1 — your application has multiple failure points (04:07–05:54)

One of the biggest reasons for multiple eval pipelines: **your LLM-based application can break at many places** — it has multiple failure points.

The lecture is interactive here: the instructor asks the live chat to look at the basic RAG architecture and type out — *where are the failure points? Where can errors occur? Where can the code break? Where are the chances of incorrect responses?*

Even looking at it directly, **two failure points are easily visible**:

| Failure point | How it fails | Consequence |
|---|---|---|
| **Retriever** | Fetches the wrong documents | The generator answers *from wrong documents* → wrong answer |
| **Generator** | Retriever works, but the generator ignores the context and hallucinates | Wrong answer despite correct retrieval |

Both failure points must be working properly — only then will the application run properly. So what do you do?

> "You need to install an evaluation pipeline on the retriever, and another on the generator. That's simple logic."

---

## 4. The two component-level eval pipelines (05:54–08:51)

Now study the two pipelines independently. (The instructor is careful about scope: "we're not discussing the *nature* of the pipeline right now — just the overall idea.")

| Pipeline | Installed on | What it checks |
|---|---|---|
| **Retriever eval** | The retriever | Given a query, are you getting the **right relevant documents** from the vector database? |
| **Generator eval** | The generator | Given a context, was the **answer generated correctly** based on that context? |

### What the generator eval checks: faithfulness (07:16)

The quality check on the generator is **faithfulness** — sometimes also called **groundedness**: the answer must be generated based on what was found in the relevant documents provided in the context, and **no other facts may be created on their own**.

The instructor's example:

- **Question:** "What is the duration of a machine learning course?"
- **Extracted document:** the duration is *three weeks*.
- **Correct generated answer:** "The duration of the machine learning course is three weeks." Full stop.
- **What must NOT happen:** additional information automatically appended — "It's a great course," or "You can also purchase the Python course; the duration of the Python course is four weeks."

The answer should be **grounded in context** — the pipeline checks that the context and the generated answer are *faithful to each other*.

---

## 5. The thought experiment — green components, broken pipeline (08:51–14:52)

This is the lecture's centerpiece. Assume both evaluation pipelines are in place, and both report success: the retriever is working correctly, the generator is working correctly.

**The poll:** does this guarantee the RAG application works correctly? "All you have to do is answer yes or no." Many people say yes; some say no. For the no-sayers — where could the failure possibly come from?

### The scenario (09:30)

A user asks: *"What is the duration of a machine learning course?"* The question goes to the retriever, where **K was set to 5**.

(Quick audience check — what is K in a RAG retriever? It means we fetch the **five most relevant documents** from the vector database.)

The five retrieved documents:

| Position | Document |
|---|---|
| D1 | "Some Random Thing" |
| D2 | "Some Random Thing" |
| D3 | "Some Random Thing" |
| D4 | "Some Random Thing" |
| D5 | **"The Duration of the ML Course is Eight Weeks"** |

**Did the retriever do its job?** Yes. Forget about reranking for now — assume the system doesn't have one. K = 5 means the retriever must provide the correct answer *within* five documents, and it did. The instructor's analogy:

> "I'll give you five attempts — you have to crack the exam one out of five. If you do it even once out of five, my job is done."

### Where it breaks (11:45)

All five documents, along with the question, go to the generator. The system prompt says: you'll receive a question and multiple contexts — merge them and generate an answer. But the generator **focuses more on the initial documents**. Generally, the generator answers based on the context of the first retrieved document — or the system explicitly guides it to give **higher priority to the earlier documents (D1, D2, D3, D4)**.

So the generator picks up a fact from the top — *"the duration of the Python course is six weeks"* — and answers:

> **"The duration of the ML course is six weeks."**

Obviously wrong. But now the harder question: **did the generator do its job properly?** Yes — and the instructor's defense of it is the most memorable passage of the lecture:

> "What happened to that poor guy? It was given the wrong documents, so it tried to do its job correctly even with the wrong documents. **It wasn't hallucinating.** It got the six-weeks data from above — it didn't generate it out of thin air. It just mixed the wrong things. But it was diligently following the instructions I gave it."

### The verdict (13:37)

- The retriever worked fine **independently**.
- The generator worked fine **independently**.
- Yet **the pipeline broke**, and the application gave wrong results.

The lesson: you also need to evaluate **the workflow created by their interaction** — a **workflow-level evaluation** that checks how your combination of retriever and generator works together. Component-level evals alone cannot see this failure.

---

## 6. What the workflow eval buys you — the reranker (14:52–15:59)

Suppose you build that third eval — the one that evaluates the retriever + generator combination. It flags the error, and it can even tell you what's wrong:

> "Yes, brother — here's the mistake. Your **most accurate document is at the bottom of the priority order**."

That diagnosis points directly at the fix: place a **reranker** in the pipeline. What does a reranker do? After the results are returned, it **reranks them** — judging that, based on this query, D5 should have the highest priority. It picks up D5 and places it at the top, moves D1–D4 down — "and suddenly, your entire ranking pipeline starts working properly."

The instructor's summary of the whole example:

> "Simply placing evals at the component level doesn't necessarily guarantee that your pipeline will work properly. Individual components will work fine, but **the pipeline can fail**."

> 💡 **Expert commentary.** This scenario encodes two well-documented phenomena. First, **position sensitivity**: LLMs attend unevenly to where evidence sits in the context — the "lost in the middle" literature (Liu et al., *Lost in the Middle: How Language Models Use Long Contexts*) shows accuracy dropping when relevant information is buried away from the context edges; a system prompt that explicitly prioritizes early documents produces the same class of bug. Second, whether the retriever "passed" depends on *which retrieval metric you chose*: **recall@5** counts D5 as a hit (the right document appeared within the top 5), while ranking-aware metrics like **MRR** or **nDCG@k** would have flagged the poor ordering immediately — even before the workflow eval did. This is precisely why two-stage retrieval exists: cheap first-stage retrieval for recall, then a cross-encoder **reranker** (e.g., Cohere Rerank, bge-reranker) to fix the ordering. Lecture 13 makes retrieval metrics hands-on.

---

## 7. Still not enough — the application level (15:59–17:44)

One more poll. You now have three evals, all green: the retriever's own eval, the generator's own eval, and the pipeline-level eval of their combination. **Does this guarantee the RAG application your users touch works correctly?**

"Many people are saying, 'Yes, there could still be problems.'" And they're right. The instructor's example:

> Everything is working fine — but my entire pipeline is taking **10 seconds** to answer a question. The user types the question, waits 10 seconds, and only then the answer returns. **Is our application fit for production deployment? The answer is no.**

So you also need an eval **at the application level** — one that ensures the **latency remains below a certain threshold**.

---

## 8. The three levels of failure points (17:44–19:14)

The instructor now formalizes the whole discussion — failure points in an LLM-based application exist at **three levels**:

| Level | What can fail | The eval you install |
|---|---|---|
| **Component level** | Any individual component: the **system prompt**, the **retriever**, the **reranker**, the **query writer**, the **embedding model**, the **vector database**; in structured-output applications, the **output parser**; in agents, the **tools**, **memory**, and **guardrails** | One evaluation pipeline per component |
| **Workflow level** | The interaction between components — the retriever↔generator hand-off; an **agent's workflow**; a **multi-turn chatbot's** conversation flow | A workflow-level eval of the combination |
| **Application level** | Whole-system properties: **latency**, **token cost per query**, **time to first token** (how long until the first token prints) | Application-level evals with thresholds |

The chain of "even if": even if everything works at the component level, there can be a problem at the workflow level; and even if everything works at the workflow level, you still need evaluations at the entire application level.

The instructor's meta-comment on his own method: "I spent about 15–20 minutes trying to prove this point with an example. That's it — we didn't discuss anything more than that."

> 💡 **Expert commentary.** This is the LLM-flavored version of the software **testing pyramid**: component evals ≈ unit tests, workflow evals ≈ integration tests, application evals ≈ end-to-end tests — with the operational layer playing the role of performance and load testing. The industry tooling encodes the same layering: **RAGAS** separates retrieval metrics from generation metrics; **DeepEval** attaches metrics per test case inside a pytest harness; **LangSmith** traces per-component spans so evaluators can be attached at any level of the trace. Lecture 18 turns the layered suite into regression gates that run in CI.

---

## 9. Reason 2 — every failure point carries multiple risk categories (19:14–23:35)

So far: one reason for multiple eval pipelines (multiple failure points). Now the second reason: **risk categories**.

You have three things you can apply evaluations to — individual components, workflows, and the entire application. But there are **variations within each of these three things**: each target has multiple *aspects* worth evaluating.

- **Application level:** say you built a dashboard. When a user uses it, the answer must obviously be **correct** and **helpful** — but it must also be **safe**. "It shouldn't happen that I'm chatting with a chatbot and the chatbot tells me another user's phone number and email."
- **Workflow level:** in the retriever→generator workflow, one aspect is whether the resulting answer is **faithful / grounded**; another is that the answer **shouldn't cost too much to retrieve** — retrieval cost above a threshold is its own risk.
- **Component level:** the retriever's sole function is fetching relevant documents — but the component's **latency** also matters. Fetching the correct document while taking 5 or 10 seconds to do so is still a problem.

The framing:

> Not only do you have multiple failure points — associated with each failure point, you have **multiple aspects**. These are what we call **risk categories**.

### The three broad risk categories (21:48)

| Category | The lecture's definition |
|---|---|
| **Application quality** | Does the app do its actual job well — does it give **correct, relevant, complete** answers to the user's question? |
| **Safety** | The answer coming out must **not be harmful**: no toxic content, no dangerous content, no biased content, no leaks of private data — and you shouldn't be able to **jailbreak** it into doing something it shouldn't |
| **Operations** | Once deployed: can it run **fast, cheap, and reliably**? |

> 💡 **Expert commentary.** The quality/safety/operations triad maps closely onto how production teams actually split eval ownership: quality metrics gate product releases; safety evals usually run as **separate pipelines on adversarial datasets** (red-team suites, jailbreak corpora — lecture 16); and operational metrics become **SLOs** — latency percentiles and cost budgets with alerting (lecture 17). A useful design heuristic: if two risks have different failure conditions, different datasets, and different owners, they belong in **different pipelines** — even when they target the same component. This is also why a single "quality score" for an application is a red flag in itself.

---

## 10. The risk-category catalog (23:35–26:54)

The instructor closes the argument with a reference table: the risk categories you will see (and use) when building your own applications. It is deliberately not exhaustive — "I've listed the important ones that you'll see frequently" — and application quality is organized by **application family**.

### Application-quality risks, by family

| Family | Risk category | The question it asks |
|---|---|---|
| **General LLM application** (e.g., a text summarizer: long input in → summarized / bullet-point answer out) | **Correctness & accuracy** | Is the generated summary accurate — correct or not? |
| | **Relevance** | Did I get answers related to what I asked? |
| | **Completeness** | Did I get answers to *all* the questions I asked? |
| | **Instruction following** | If I specified a format or length, did the answer come in that format and length? |
| **RAG** | **Context relevance** | Are the retrieved documents relevant? (the retriever's job) |
| | **Retriever recall** | Did retrieval surface the needed documents? (closely related to the above) |
| | **Groundedness & faithfulness** | Was the answer generated from my context, with no extra information added? |
| | **Citation accuracy** | Can each generated line be cited to the specific document it was extracted from? (as you've seen in ChatGPT) |
| **Agent** | **Tool selection** | Is the agent able to select the right tool for the right task? |
| | **Parameter correctness** | When calling a tool, are the correct parameters passed? |
| | **Task completion** | Does the agent complete the task correctly, or is its failure rate high? |
| | **Error recovery** | If the agent makes a mistake mid-task, can it recover from it? |
| **Multi-turn chatbot** | **Context retention** | How much of our past conversations can the chatbot remember? |
| | **Clarification behavior** | When the chatbot is confused, or receives ambiguous messages from the user, does it ask for clarification? (also monitored) |

### The safety dimensions (26:21)

The lecture counts "four or five" safety dimensions:

| Dimension | What it checks |
|---|---|
| **Toxicity** | Are the answers it gives toxic? |
| **Harmful content** | Is it giving out things it shouldn't — self-harm-related content, weapons-related content, illegal acts, app-related content? |
| **Bias** | Does it answer everyone the same way, or give different answers based on the user's profile? |
| **Privacy / data leakage** | Is the chatbot or RAG chatbot giving out someone's personal information — credit card information, contact details? |
| **Prompt injection & jailbreak resistance** | Can someone make your LLM application do something it shouldn't, just by giving prompts? |

### The operations metrics (26:54)

| Metric | What it tracks |
|---|---|
| **Latency** | End-to-end response time |
| **Cost per request** | How much one query costs to answer |
| **Token efficiency** | Tokens consumed per answer |
| **Error / failure rate** | How often the system fails |
| **Latency under load** | Response time when traffic spikes — "things like that are considered" |

> 💡 **Expert commentary.** Treat this catalog as a metrics shopping list, because nearly every row has a standard implementation you can adopt rather than invent: **RAGAS** ships context relevance/recall and faithfulness as built-in metrics (lectures 13–14); **G-Eval** (lecture 15) is the judgment layer for the fuzzier quality rows; citation accuracy is the *attribution* problem; the agent rows (tool selection, parameter correctness, task completion, error recovery) are exactly what agent benchmarks grade; **instruction following** even has a dedicated model-side benchmark (IFEval, lectures 7–8); and the safety rows have purpose-built classifiers and guardrail tooling (lecture 16). The design move the course is teaching: translate each row you care about into *dataset + metric + threshold* — that triple **is** an eval pipeline.

---

## 11. The 99.99% rule (26:54–28:03)

The nutshell summary of the entire discussion:

> Based on these risk categories, you create different evaluation pipelines. It's the **same application** — but it has an eval pipeline for **latency**, an eval pipeline for **safety**, and an eval pipeline for **correctness**.

Which reinforces the statement the lecture set out to prove:

> Whenever you build an LLM application, most of the time — **99.99% of the time** — you'll have more than one evaluation pipeline.

And the two major reasons, restated one final time:

1. **Multiple failure points** — component level, workflow level, application level.
2. **Multiple risk categories** — quality, safety, operations — attached to each of those failure points.

---

## Key takeaways

1. **The 99.99% rule:** a real LLM application almost never has a single eval pipeline. Two independent reasons: **multiple failure points** and **multiple risk categories**.
2. **Failure points exist at three levels.** Component level (system prompt, retriever, reranker, query writer, embedding model, vector database, output parser, tools, memory, guardrails — one pipeline each), workflow level (component *interactions*: agent workflows, multi-turn chatbot flows, the retriever↔generator hand-off), and application level (whole-system latency, token cost per query, time to first token).
3. **Green components ≠ green pipeline.** In the K = 5 thought experiment, the retriever surfaced the right document at rank 5 of 5 (its job, by the exam-attempt analogy, was done) and the generator dutifully prioritized the earlier documents — mixing in a wrong fact without hallucinating. Both components passed; the application answered wrongly. Only a **workflow-level eval** catches this, and it points to the fix: a **reranker**.
4. **Even three green evals don't make a production system.** A pipeline that answers correctly but takes 10 seconds per question is unfit for deployment — application-level evals enforce operational thresholds.
5. **Risk categories** are the multiple aspects attached to every failure point: **application quality** (correct, relevant, complete answers), **safety** (no toxicity, dangerous content, bias, or private-data leakage; jailbreak-resistant), and **operations** (fast, cheap, reliable).
6. **The risk catalog**, organized by family — general apps: correctness & accuracy, relevance, completeness, instruction following; RAG: context relevance, retriever recall, groundedness/faithfulness, citation accuracy; agents: tool selection, parameter correctness, task completion, error recovery; multi-turn chatbots: context retention, clarification behavior; safety: toxicity, harmful content, bias, privacy, prompt injection & jailbreak resistance; operations: latency, cost per request, token efficiency, error rate, latency under load.
7. **The design formula:** enumerate your failure points, cross them with the risk categories that matter for your product — the result is your list of eval pipelines. Same application; separate pipelines for latency, safety, and correctness.

## Interview angles

- *"Why can't a single eval pipeline cover an entire LLM application?"* → Two reasons, in order: failure points live at three levels (component / workflow / application — walk the retriever → generator → reranker → latency chain), and every failure point carries independent risk categories (quality / safety / operations). One pipeline tests one target against one criterion family; it cannot do all of it.
- *"All your component tests pass. Are you ready to ship?"* → No — reproduce the K = 5 example: the right document retrieved at rank 5, the generator anchoring on the top-priority documents, a wrong answer with *no component at fault* — then the 10-second latency case. Show the fix chain: workflow-level eval → reranker; application-level eval → latency threshold.
- *"What evals would you build for a RAG chatbot?"* → Enumerate, don't average: retriever (context relevance, recall), generator (faithfulness/groundedness), workflow (end-to-end answer correctness, citation accuracy), application (latency, cost per query, time to first token), safety (toxicity, data leakage, jailbreak resistance). The enumeration itself is the answer interviewers want.
- *"What's the difference between quality, safety, and operational evals — and why separate pipelines?"* → Give the three definitions; then note that their datasets, failure conditions, and owners differ (a golden Q&A set vs an adversarial jailbreak corpus vs a load test), so they need separate pipelines with separate thresholds.

## Cross-links

- **Previous:** [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) — whose closing "one application, several evals" line this lecture proves in detail.
- **Next:** [05 — Eval Methods: LLM-as-a-Judge, Reference-Based vs Reference-Free](05-eval-methods-reference-based-vs-free.md) — how each of these pipelines actually judges an output.
- **Where the course implements the catalog:** [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) (context relevance, recall), [14 — The RAG Triad](14-rag-triad-generator-pipeline.md) (faithfulness, end-to-end RAG), [16 — RAG Security: Toxicity, Leakage & Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) (the safety rows), [17 — RAG Operational Evals](17-rag-operational-evals.md) (the operations rows), [18 — Regression Testing](18-rag-regression-testing.md) (the multi-pipeline suite as a release gate).
- **Reference depth:** [Evaluation Fundamentals](../01-evaluation-fundamentals.md) — the eval-target taxonomy is the formal version of the three levels; [Eval Engineering](../05-eval-engineering.md) — versioned suites, thresholds-as-config, and CI gates for many pipelines.
- **Course hub:** [README.md](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 03. Evaluation Workflow](03-evaluation-workflow.md) · [Course hub](README.md) · [05. Eval Methods Reference Based vs Free →](05-eval-methods-reference-based-vs-free.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
