# 02 — Model Evals vs Application Evals

> **Lecture 2 of 19** · Unit 1: Foundations · 24:32
> Introduction to LLM Evaluations — Model Evals vs Application Evals (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/02-model-vs-application-evals.md)

---

## What this lecture covers

This is the conceptual foundation of the entire course. Three questions are answered:

1. **What are LLM evaluations?** — a precise definition and the three characteristics that make a test a *real* eval
2. **The biggest misconception** — evals are *not* just metrics; they are the complete testing setup
3. **The one distinction that organizes everything** — **model evaluations vs application evaluations**, why the industry's "LLM evals" almost always means the second one, and why this course focuses there

If you keep one mental model from this lecture, make it this: **frontier labs benchmark the model; you evaluate the system you built around it.**

---

## 1. What are LLM evaluations? (00:00–04:24)

### The definition

> LLM evaluations are **systematic, repeatable tests used to judge an LLM and LLM-powered systems against clear criteria**.

Every word of that definition is load-bearing. The tests can target:
- an **LLM itself** (the raw model), or
- an **LLM-based application** (the system you build around the model).

And the definition has **three defining characteristics** — the instructor calls them the three most important pointers of LLM evaluation.

### Characteristic 1 — Systematic (01:27)

Systematic is the opposite of ad-hoc. The anti-pattern the instructor describes:

> "Five questions came to your mind. You asked, got an answer. You thought, yes, everything is correct. That doesn't happen here."

That is **vibe testing** — and it is exactly what evaluations exist to replace. Being systematic means:

- You create **proper datasets** for testing.
- Those datasets deliberately cover **all kinds of edge cases**.
- You test your chatbot / LLM-based system against that dataset, so you observe **real-world behavior**, not lucky samples.

**The instructor's example:** if you are building a chatbot for CampusX, don't invent test questions from your own head. Instead, take **100 real user chats** with the system, build a dataset from them, and test on that. Now your evaluation measures the behavior actual users experience.

### Characteristic 2 — Repeatable (02:03)

Repeatable means the evaluation survives change. Tomorrow you may:

- change the **model**,
- change the **retriever**,
- change the **chunking strategy**,

… and you must still be able to evaluate the system **exactly the way you did before**. Why this matters:

- The same dataset can be applied to **any version** of the software, the same way, extracting comparable results.
- This is the *only* way to answer "is version 1 better or version 2 better?" — version 1's performance on the dataset vs version 2's performance on the same dataset is what tells you whether the system is improving.

Without repeatability you have anecdotes; with it, you have an **improvement signal**.

### Characteristic 3 — Clear criteria (03:12)

The most important dependency of LLM evaluation: **what criteria are you evaluating against?**

**The instructor's example** — a CampusX chatbot might be evaluated on:

1. **Correctness** — the answer coming out should be correct
2. **Simple explanations** — answers should be easy to understand
3. **Grounding** — explanations should come *only from our own course content*
4. **Safety** — no unsafe content, no insults, no threatening tone

The instructor's one-liner is the takeaway:

> "Without criteria, you're just doing vibe testing. **With criteria, you're doing proper evaluation.**"

> 💡 **Expert commentary.** Notice that criteria 1–3 are *quality* criteria and 4 is a *safety* criterion. In production settings this split becomes formal: quality evals (faithfulness, relevance, correctness) and safety evals (toxicity, leakage, scope drift) usually live in **separate pipelines with separate thresholds** — a design this course returns to in lecture 16 when it tests a RAG app for toxicity, data leakage, and scope drift.

---

## 2. Evals are not just metrics — they are the complete testing setup (04:24–07:28)

The instructor flags this as the confusion *he himself* had coming from machine learning, and the one he most wants to pre-empt for you.

### The ML/DL mental model (and why it misleads)

In classic ML, "evaluation" meant **metric**: accuracy, precision, recall, F1-score, the confusion matrix. So the natural assumption is that "LLM evals" will likewise be *a set of metrics*.

**That assumption is wrong.**

### The correct mental model

> LLM evals = **the complete testing setup** — everything you build in order to test.

The instructor decomposes "the complete setup" into four questions, using a **RAG chatbot** as the running example:

| Question | Example answer | Part of your evals? |
|---|---|---|
| **What are we evaluating?** | The **retriever** inside the RAG chatbot (a component) | ✅ |
| **On what basis?** | The retriever's accuracy — the metric | ✅ |
| **When are we running the tests?** | Offline, or after deployment in production | ✅ |
| **With which tools?** | RAGAS (because it's a RAG application) | ✅ |

All four — component, metric, timing, tooling — together constitute "LLM evals."

**The interview-ready formulation:** *whenever someone asks you "what are LLM evals?", the answer is: the entire testing setup — what we test, on what basis, when, and with which tools — not just metrics.*

### The questions LLM evaluations answer (07:28)

The instructor lists the operational questions that only evals can answer:

- Is this system **good enough to ship** / put into production?
- Did **prompt v2 actually improve** over prompt v1? (prompt evaluation)
- Is the **RAG answer grounded** in the retrieved context?
- Is the **agent completing the task** correctly?
- Is the **chatbot safe** for real users?
- Is the **latency under control**?

Every one of these is a question an AI engineer gets asked by a manager, a reviewer, or an interviewer — and each maps to a specific kind of evaluation (release gate, regression test, groundedness metric, task eval, safety eval, performance eval).

---

## 3. The core distinction: Model Evals vs Application Evals (08:37–10:33)

This is the lecture's centerpiece — "a very important distinction" that will organize the rest of the course.

> **Model evaluations** evaluate the *LLM itself*.
> **Application evaluations** evaluate the *LLM-based application* — the whole system built around the model.

The definition from section 1 already contained the seed: evals judge "an LLM **and** LLM-powered systems" — two targets, two kinds of evaluation.

### An honest disclaimer from the instructor (09:58)

The terms *model eval* and *application eval* are **his own teaching terms, not official industry terminology**. In industry, both are collectively just called "LLM evaluations," and context tells you which one is meant. He explicitly asks you not to quote these as standard terms — they exist to make the topic learnable.

> 💡 **Expert commentary.** The closest industry-standard vocabulary for this same split: **model-level ("capability") benchmarks** vs **application-level ("product") evals**. You'll also see "offline evals" used loosely for both — which is exactly why lecture 6 of this course spends a full session disentangling *offline vs online* from *model vs application*. Keep the two axes separate in your head: *what you evaluate* (model vs application) and *when you evaluate* (offline vs online) are independent choices.

---

## 4. Model evaluations in detail (10:33–16:27)

### What model evals do (10:33)

> Model evals evaluate the model itself. The main idea is to **test and evaluate the capabilities of a model**.

The goal: when a new LLM is released, its capabilities are tested, benchmarked, and **documented** — that documentation is what you see quoted in model launches: "this LLM topped benchmark X, scored N% on leaderboard Y." Those claims come from model evaluations that somebody ran.

### The 8 capability areas (11:44–14:06)

Modern LLMs are evaluated (the instructor says "majory") on **eight capability categories**:

| # | Capability | The question it asks |
|---|---|---|
| 1 | **Reasoning** | Can the LLM reason — solve a problem step by step? |
| 2 | **Knowledge** | Does it have basic world/general knowledge (everything up to its **cutoff date**)? |
| 3 | **Basic maths** | Can it solve maths problems? |
| 4 | **Coding** | Can it write code? |
| 5 | **Instruction following** | Given 10 instructions, does it follow them one after another? |
| 6 | **Long context handling** | Can it pull the right answers out of a very large context? |
| 7 | **Multimodal understanding** | Can it understand/produce images, text, sound? |
| 8 | **Tool use** | Can it properly utilize tools? |

### The benchmark examples (14:06–14:39)

For each capability area there are standard benchmarks. The ones named in the lecture:

| Capability | Benchmark | What it does |
|---|---|---|
| General knowledge + reasoning | **MMLU** | Asks questions across many subjects — science, history, law, medicine — and records/evaluates the answers |
| Maths | **GSM8K** | Grade-school maths questions |
| Coding | **SWE-bench**, **HumanEval** | Famous coding benchmarks |
| Instruction following | **IFEval** | (named in the lecture) |
| Long context | **Needle in a Haystack** | (named in the lecture) |
| Multimodal | **MMMU** ("Triple M") | (named in the lecture) |

The full benchmark landscape — how these benchmarks evolved, how they're applied, how results are extracted — is deferred to a dedicated later lecture (lectures 8–9 of this course).

> 💡 **Expert commentary.** MMLU (Massive Multitask Language Understanding, Hendrycks et al.) covers 57 subjects and has become the canonical "knowledge" benchmark; GSM8K is grade-school math word problems; SWE-bench tasks a model with resolving real GitHub issues; HumanEval is function-level code generation (pass@k); IFEval checks verifiable instruction compliance ("answer in exactly 3 bullet points"); Needle-in-a-Haystack probes retrieval from long contexts; MMMU tests multimodal understanding. Lecture 9 of this course walks through how the knowledge-benchmark family evolved — including why newer models saturate the older ones.

### Why an AI engineer needs model-eval literacy (15:14–16:27)

The instructor is blunt about how much of this you'll *do*:

> "If you are going to become an AI engineer, you won't do as much work on model evaluations… **there is a good chance that you never do model evaluations.**"

But you still need to *know* it, for two reasons:

1. **Literacy** — benchmark claims are the language of model launches; you should be able to read them critically.
2. **Model selection decisions** — choosing OpenAI vs Anthropic vs an open-source LLM for your application "comes out from model evaluation itself." Lecture 11 makes this practical by running custom model evals to pick a model.

---

## 5. Application evaluations in detail (16:27–22:52)

### Why application evals are *the* topic of this course (16:27–17:46)

> "As an AI engineer, your job is to build LLM-based applications. **So evaluating them is also your job.**"

Application evaluation is the main topic of the whole playlist — the course will focus here. Model evaluation gets "just one dedicated lecture," and that only for literacy.

### The LLM is just one component (18:22–19:31)

Beginners think "LLM application = the LLM is the brain, so everything is about the LLM." With experience — especially on bigger applications — you realize the brain matters, but a working application needs much more around it. The instructor's component inventory:

- **Interface** — the user-facing layer
- **System prompt** — the prompt you write
- **Tools & APIs** — added to the system
- **Orchestration code** — e.g. written in LangGraph: control flows here, branching happens there, then control goes in parallel
- **Guardrails** — applied at application level ("a very important thing")
- **Output parsers** — if you use them
- **Memory & context** — "what can I even say — superb" (the instructor's emphasis)
- **The retrieval system** (for RAG) — a separate system: its own embedding model, vector databases
- **Monitoring setup** — after deployment, the whole monitoring stack
- **Feedback loop** — the whole feedback pipeline

> That's why application evals is such an important topic — model evaluation alone won't cut it.

### The smartphone analogy (20:02–21:15)

The lecture's most memorable analogy:

- Smartphone chip makers (Snapdragon, MediaTek) release benchmark scores — AnTuTu/"N2" scores — proving how strong the processor is.
- **Does a strong processor guarantee a good smartphone?** Obviously not: you also need the camera system, the operating system, the sound system, the graphics, the battery…
- A good smartphone is all of those working together — "just having a good processor doesn't achieve anything."

The mapping:

| Smartphone world | LLM world |
|---|---|
| Chip maker | Frontier lab |
| Chip benchmark scores (AnTuTu etc.) | Model evaluations / benchmarks |
| The finished phone (camera, OS, battery…) | Your LLM application |
| Testing the *phone* end-to-end | **Application evaluation — your responsibility** |

> "Frontier labs are doing the LLM evaluation for us. But the evaluation of the whole system we built on top — that responsibility is **ours**, as AI engineers."

### What application evals ask (21:45–22:52)

The formal framing from the lecture:

> Application evals **assess the behavior and performance of an LLM-powered application — both at the level of the entire system and at specific components within it.**

Two levels, both yours:

1. **System level** — the whole RAG chatbot: final response quality, latency, cost per token
2. **Component level** — is my **retriever** working correctly? my **embedding model**? my **reranker**?

And the key reframing:

> In application evals we **don't ask "can the model do this?"** — that's model evaluation's job. Instead we ask: **"will our product work correctly?"**

For the CampusX chatbot, application evals answer:

- Was the **student's question answered** correctly?
- Was **course material used properly**?
- Was the answer **faithful**?
- Was it **easy for a beginner**?
- Did **hallucination** happen or not?
- Did the answer come **quickly** (latency)?
- Is our chatbot **safe**?

> 💡 **Expert commentary.** "Faithful / used course material properly / hallucination" are three phrasings of the groundedness family — the single most-evaluated property in RAG systems. The course returns to it with dedicated machinery: the RAG Triad (lecture 14) and G-Eval (lecture 15). Notice also that latency and cost appear alongside quality — in production, an eval suite that ignores latency and cost is answering only half of "will our product work."

---

## 6. How to read the term "LLM evaluation" from now on (23:30–24:32)

A practical tip from the instructor:

> When you see a video or article titled "LLM evaluation," **you can assume it's teaching application evaluation** — not model evaluation. 99% of the time, that's what you need to learn.

### Lecture summary (the instructor's own recap)

The lecture followed a Why → What → Types arc:

1. **Why** — why this topic matters (previous lecture)
2. **What** — LLM evals are systematic, repeatable tests against clear criteria; evals = the *complete testing setup*, not just metrics
3. **Types** — model evals vs application evals

Next lecture moves to **How**: how LLM evaluations are actually done — taught, with an explicit disclaimer, **from the application-eval perspective**.

---

## Key takeaways

1. **LLM evals** = systematic (proper datasets, edge cases), repeatable (same dataset, any version), criteria-driven tests that judge LLMs and LLM-powered systems.
2. **Evals ≠ metrics.** Evals are the complete testing setup: the component under test, the metric, the timing (offline/online), and the tooling.
3. **Model evals** test the model's capabilities (reasoning, knowledge, maths, coding, instruction following, long context, multimodality, tool use) via benchmarks like MMLU, GSM8K, SWE-bench, IFEval, Needle-in-a-Haystack, MMMU. Frontier labs run them; engineers *read* them — for model selection literacy.
4. **Application evals** test the system you built — at component level *and* system level. They ask "will our product work?", not "can the model do this?"
5. **The smartphone rule:** a great chip doesn't make a great phone; a great LLM doesn't make a great application. Evaluating the phone is your job.
6. **99% rule:** "LLM evaluation" content almost always means application evaluation.

## Interview angles

- *"What are LLM evaluations?"* → Give the definition, then immediately add: "and importantly, evals are the complete testing setup — the dataset, the criteria, the pipeline, the tooling — not just a metric." That one addition signals real experience.
- *"What's the difference between evaluating a model and evaluating an LLM application?"* → The 8 capabilities + benchmarks vs component/system-level product evals; use the smartphone analogy to make it land.
- *"Why can't we just use the model's benchmark scores to decide if our app will work?"* → Because your application adds prompt, orchestration, retrieval, guardrails, memory — each introduces failure modes the benchmark never measured; only application evals on your data can answer "will *our* product work."

## Cross-links

- **Next:** [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) applies the "how" to a real pipeline.
- **Deeper on benchmarks:** [09 — LLM Benchmarks Evolution](09-llm-benchmarks-evolution.md) and [Section 105 note 3 — Agent Benchmarks](../03-agent-benchmarks.md).
- **Deeper on judging methods:** [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) and [Section 105 note 2 — LLM-as-a-Judge](../02-llm-as-a-judge.md).
- **RAG application of these ideas:** [Section 105 note 4 — RAG Evaluation](../04-rag-evaluation.md).
