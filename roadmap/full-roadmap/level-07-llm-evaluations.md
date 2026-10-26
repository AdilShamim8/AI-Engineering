# Level 7 · LLM Evaluations

> **Phase 4 · Evaluation & Trust** · 9 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/7/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Design, execute, and automate comprehensive evaluations for Large Language Models and AI applications to ensure quality, safety, and reliability in production environments.

## Why this level matters

**Interview weight: 8/10**

Increasingly a decisive question: “**How would you know your system works?**” Most candidates answer weakly, so a concrete answer (test sets, LLM-as-judge, metrics) **sets you apart sharply**.

**On-the-job weight: 10/10**

Without evals, **every change is a guess**. Teams that measure ship faster and with more confidence, and this is where much of the **senior-level work** happens.

---

## Modules

### 01 · Introduction to LLM evaluations (M7.1 · 1 session)

- **Pitfalls of vibe testing** — Understand the pitfalls of “vibe testing” by examining real-world failure case studies like Air Canada.
- **Deterministic vs probabilistic testing** — Navigate the differences between deterministic software testing and probabilistic LLM systems.
- **Model evals vs application evals** — Distinguish between evaluating core foundation model capabilities and testing complete application workflows.
- **The end-to-end evaluation workflow** — Implement an end-to-end evaluation process covering task definition, criteria, datasets, execution, analysis, and iteration.

**Outcome** · Understand the foundational need for and workflow of LLM evaluations compared to traditional software testing.

### 02 · Evaluation methods & paradigms (M7.2 · 1 session)

- **Programmatic, human & LLM-as-a-Judge** — Categorize evaluation execution mechanisms into Programmatic, Human, and **LLM-as-a-Judge** approaches.
- **Reference-based vs reference-free** — Understand reference-based vs reference-free evaluation.
- **When a Golden Dataset is required** — Determine when a Golden Dataset answer key is required versus when evaluation can rely entirely on LLM judgment.
- **Matching method to behaviour** — Choose the appropriate evaluation method based on whether the target behavior is deterministic, semantic, subjective, or operational.

**Outcome** · Select the appropriate evaluation execution method and paradigm for a given LLM testing scenario.

### 03 · Offline vs online evaluations (M7.3 · 2 sessions)

- **Offline suites for pre-release testing** — Use offline evaluation suites for pre-release testing, version comparison, experimentation, and preventing performance regression.
- **Post-deployment production risks** — Identify post-deployment production risks including unexpected inputs, emergent systematic failures, changing user behavior, and data drift.
- **System metrics vs quality metrics** — Differentiate automatically captured system metrics such as latency, token usage, and errors from LLM-computed quality metrics such as hallucination or relevance.
- **Continuous online evaluation pipeline** — Implement a continuous online evaluation pipeline through production logging, sampling, dashboarding, and alerting.
- **Feeding failures back offline** — Feed important production failures back into the offline evaluation dataset.

**Outcome** · Design a dual-layer evaluation strategy that catches regressions before release and monitors quality after deployment.

### 04 · Model evaluations & benchmarking (M7.4 · 1 session)

- **Core LLM capabilities** — Explore core LLM capabilities such as knowledge, reasoning, mathematics, coding, instruction following, long-context understanding, multimodal capability, safety, and tool use.
- **Anatomy of a benchmark** — Analyze the anatomy of a benchmark through its dataset, prompts, run configuration, scoring method, and result aggregation.
- **Public leaderboards** — Understand how public leaderboards compare foundation models.
- **Benchmark pitfalls** — Identify benchmark pitfalls including data contamination, score saturation, benchmark overfitting, and configuration gaming.

**Outcome** · Critically assess public LLM benchmarks and understand how core model capabilities are formally measured.

### 05 · The evolution of knowledge benchmarks (M7.5 · 1 session)

- **From MMLU to harder knowledge tests** — Trace the progression from benchmarks such as **MMLU** and **TruthfulQA** toward harder tests of knowledge and factual reliability.
- **Human exams as benchmarks** — Understand the use of human exams in benchmarks such as **AGIEval** to compare human and model capabilities.
- **GPQA, MMLU-Pro, SimpleQA, HLE** — Explore harder benchmarks such as **GPQA**, **MMLU-Pro**, **SimpleQA**, and Humanity's Last Exam.
- **Why benchmarks keep getting harder** — Understand why benchmarks continually become harder as frontier models saturate older datasets.

**Outcome** · Understand the progression of knowledge benchmarks and select appropriate tests for increasingly capable models.

### 06 · Custom model evaluations (M7.6 · 1 session)

- **Evaluating on your actual task** — Move beyond public benchmarks and evaluate models on the actual task your application needs to solve.
- **Shortlisting candidate models** — Use leaderboards and aggregation platforms to shortlist candidate models based on capability, latency, context, and cost.
- **Building a custom eval dataset** — Build a custom evaluation dataset for a real task such as **Text-to-SQL**.
- **Like-for-like model comparison** — Compare shortlisted models using the same inputs, prompts, parameters, and scoring criteria.
- **Estimating usage & token cost** — Estimate API usage and token costs and use techniques such as prompt caching where appropriate.
- **Quality / latency / cost trade-off** — Select the model that offers the best task-specific quality / latency / cost trade-off, rather than simply choosing the highest-ranked general model.

**Outcome** · Evaluate and select the most capable and cost-effective foundation model for a specific application.

### 07 · Building an eval suite & regression testing (M7.7 · 2 sessions)

- **Component, pipeline & application levels** — Structure evaluations across component level, pipeline level, and application level depending on what is being tested.
- **Versioning tests, configs & results** — Maintain versioned test cases, evaluation configurations, prompts, models, and results.
- **Experiment tracking & baselines** — Track experiments and compare new versions against established baselines.
- **CI/CD quality gates** — Build automated **CI/CD** quality gates so changes cannot ship when important metrics regress.
- **Self-improving golden dataset** — Create a self-improving loop by adding edge cases and failures discovered in production back into the offline golden dataset.
- **Quality alongside latency & cost** — Track quality together with latency and cost so improvements in one area do not silently damage another.

**Outcome** · Build an automated evaluation suite that prevents regressions and improves continuously from real-world usage.

### 08 · RAG Evals (M7.8 · 5 sessions)

- **Four levels of RAG evaluation** — Evaluate a **RAG** system at component, pipeline, application, and safety levels, rather than treating it as one black-box system.

Component-level evaluation

- **Evaluating the retriever alone** — Evaluate the retriever independently to determine whether it finds the information required to answer the question.
- **Diagnosing missed & noisy retrieval** — Diagnose cases where the retriever completely misses the relevant context or retrieves excessive irrelevant/noisy chunks.
- **Retrieval metrics** — Measure retrieval effectiveness using metrics such as Contextual Recall, Contextual Precision, **Recall@k**, and other ranking-aware metrics where appropriate.
- **Building the Golden Dataset** — Generate or curate relevant chunks and ideal answers for a Golden Dataset through hand-authoring, LLM-assisted generation, or tools such as **DeepEval**'s synthetic-data generators.
- **Evaluating the generator alone** — Evaluate the generator independently by providing known-good context and checking whether it produces faithful and relevant answers.
- **Detecting unfaithful answers** — Detect unfaithful claims, irrelevant answers, missing information, and misuse of provided context.
- **Component tests with DeepEval & RAGAS** — Implement component tests using frameworks such as **DeepEval** or **RAGAS** while understanding what each metric actually measures.

Pipeline-level evaluation

- **The full retrieve → generate pipeline** — Evaluate the complete retrieval → context → generation pipeline.
- **The RAG Triad** — Measure the **RAG** Triad:
- **Contextual Relevancy** — Contextual Relevancy
- **Faithfulness** — Faithfulness
- **Answer Relevance** — Answer Relevance
- **When good components interact badly** — Understand how individually strong components can still interact poorly when connected.
- **Diagnosing pipeline-level failures** — Diagnose cases such as high retrieval precision but low overall contextual relevance or poor downstream answers.
- **Locating the root failure** — Determine whether the root failure lies in retrieval, assembled context, or generation.

Application-level evaluation

- **Evaluating from the user's perspective** — Evaluate the **RAG** system from the actual user's perspective rather than only testing internal components.
- **Factual correctness** — Measure whether the final answer is factually correct given the available evidence.
- **Answer completeness** — Evaluate completeness: does the answer address all important parts of the user's request?
- **Tone, format & citation behaviour** — Evaluate application-specific requirements such as tone, style, persona, format, citation behavior, and instruction following.
- **Operational metrics per query** — Track operational metrics including latency, token usage, cost per query, and error rates alongside quality.

Safety evaluation for RAG

- **Harmful & disallowed responses** — Evaluate whether the system produces harmful, illegal, dangerous, biased, or otherwise disallowed responses.
- **PII protection & redaction** — Test whether sensitive **PII** such as contact details, credentials, or payment information is appropriately protected or redacted.
- **Direct & indirect prompt injection** — Test direct and indirect prompt injection, including malicious instructions hidden inside retrieved documents.
- **Jailbreak attempts** — Test jailbreak attempts intended to bypass application guardrails.
- **Poisoned retrieval content** — Evaluate whether retrieved malicious or misleading content can manipulate the model into leaking data or ignoring application instructions.

**Outcome** · Evaluate a RAG application comprehensively across retrieval quality, generator behavior, pipeline interaction, user-facing quality, operational performance, and safety.

### 09 · Agent Evals (M7.9 · 3 sessions)

- **Six dimensions of agent evaluation** — Evaluate agentic systems at the level of decision-making, trajectories, tool usage, task completion, recovery, and safety.

Agent behavior & trajectory evaluation

- **Why the final answer is not enough** — Understand why evaluating only the final answer is insufficient when an agent autonomously decides how to complete a task.
- **Tool selection** — Evaluate whether the agent chooses the correct tool for a given situation.
- **Tool argument correctness** — Test whether the agent generates accurate and properly formatted tool arguments.
- **Trajectory quality** — Evaluate the sequence of actions taken by the agent and whether the trajectory is appropriate for the task.
- **Loops, redundancy & early exit** — Detect unnecessary tool calls, redundant actions, loops, incorrect ordering, and premature termination.
- **Task-completion success rate** — Measure overall task-completion success rate for complex multi-step user requests.

Failure recovery

- **Injecting realistic failures** — Introduce tool failures, malformed results, unavailable services, missing information, and unexpected intermediate states.
- **Noticing failure & choosing recovery** — Evaluate whether the agent notices failure and chooses an appropriate recovery strategy.
- **Retry, fall back, replan, escalate** — Test whether it can retry, select an alternative tool, revise its plan, or escalate appropriately.
- **Measuring recovery, not just success** — Measure successful recovery rather than only measuring success in ideal conditions.

Agent safety evaluation

- **Unauthorized & destructive actions** — Test whether agents attempt unauthorized or destructive actions.
- **Approval gates & permission boundaries** — Evaluate human-approval gates and permission boundaries around consequential actions.
- **Resistance to prompt injection** — Test agent resistance to direct and indirect prompt injections designed to hijack its tool usage.
- **Secret extraction & scope escape** — Attempt to manipulate an agent into revealing secrets, exceeding permissions, or using tools outside the intended scope.
- **Cybersecurity capability benchmarks** — Use relevant cybersecurity benchmarks where appropriate to assess dangerous capabilities such as exploitation, reverse engineering, or other high-risk computer-use behavior.
- **Outcome quality vs execution efficiency** — Track both outcome quality and execution efficiency through steps, latency, tool calls, token usage, and cost.

**Outcome** · Systematically evaluate whether an agent makes good decisions, uses tools correctly, completes tasks efficiently, recovers from failures, and remains within its security boundaries.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [DeepEval documentation](https://deepeval.com/docs/getting-started) — open-source LLM evaluation framework with RAG and agent metrics.
- [Ragas documentation](https://docs.ragas.io/) — RAG evaluation metrics: faithfulness, answer relevance, contextual precision/recall.
- [promptfoo](https://www.promptfoo.dev/docs/intro/) — open-source prompt and application testing with CI integration.
- [Hamel Husain — Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) — the practitioner essay on building eval suites that catch real failures.
- [OpenAI Evals (GitHub)](https://github.com/openai/evals) — framework for benchmarking language models.
- [Arize Phoenix (GitHub)](https://github.com/Arize-ai/phoenix) — open-source tracing and evaluation of LLM applications.
- [Langfuse documentation](https://langfuse.com/docs) — open-source observability with online evaluation and dataset testing.
- [TruLens documentation](https://www.trulens.org/) — RAG triad evaluation and tracking.
- [BEIR benchmark (GitHub)](https://github.com/beir-cellar/beir) — retrieval evaluation datasets for measuring retriever quality.

## In this repository

- **[105 — AI Evaluation](../../105_AI-Evaluation/README.md)** — the dedicated knowledge base for this level: [evaluation fundamentals](../../105_AI-Evaluation/01-evaluation-fundamentals.md), [LLM-as-a-Judge](../../105_AI-Evaluation/02-llm-as-a-judge.md), [agent benchmarks](../../105_AI-Evaluation/03-agent-benchmarks.md), [RAG evaluation](../../105_AI-Evaluation/04-rag-evaluation.md), [eval engineering](../../105_AI-Evaluation/05-eval-engineering.md)
- **[The LLM Evaluations course](../../105_AI-Evaluation/course/README.md)** — a complete step-by-step curriculum layer for this level: 19 lectures of video-by-video English notes and transcripts (foundations → eval methods → offline/online → benchmarks → leaderboards → model selection → RAG evaluation → production monitoring), built from a full Hindi-language course and cross-linked to the knowledge-base notes above
- [RAG evaluation & benchmarking note (RAGAS, TruLens, DeepEval)](../../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md)
- [Evidence policy for measurable claims](../../research/evidence-policy.md)

---

[← Level 6 · Context Engineering](level-06-context-engineering.md) | [Roadmap map](README.md) | [Level 8 · AI Security →](level-08-ai-security.md)
