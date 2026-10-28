# 105 — AI Evaluation

*How to know — with evidence, not vibes — that an AI system works.*

> Reviewed October 27, 2026 (notes 1–5 reviewed October 17; notes 6–7 and the course study materials added October 27). Every reference has been checked. This section is a **knowledge base**, not a course: it explains the concepts, the research, and the tooling, and cross-links the deeper curriculum notes elsewhere in this repository.

---

## Why this section exists

Evaluation is the discipline that separates AI *demos* from AI *systems*. The [full roadmap](../roadmap/full-roadmap/level-07-llm-evaluations.md) rates LLM evaluations at **10/10 for on-the-job importance** — "without evals, every change is a guess" — and at 8/10 for interviews, where *"How would you know your system works?"* is increasingly the decisive question. Yet most learning material treats evaluation as an afterthought: a metric name here, a tool logo there. This section gives the topic a dedicated home.

Two things make LLM evaluation genuinely different from ordinary software testing, and both shape everything that follows:

1. **Outputs are open-ended and probabilistic.** The same input can yield many valid answers, so exact-match assertions almost never work. You end up measuring *properties* of outputs — groundedness, relevance, correctness — which are themselves judgment calls.
2. **The measurement instruments are themselves fallible.** LLM-as-a-judge, the industry's workhorse metric, has documented biases and failure modes. Evaluating the evaluator becomes part of the job.

A third theme runs through this section because it dominated the 2025–2026 research literature: **benchmarks and evals can be gamed** — by models (reward hacking), by harnesses (infrastructure noise), and by the people reporting scores. Any engineer who can reason about *measurement validity*, not just metric values, is operating at the senior level the [accelerated roadmap](../roadmap/accelerated-roadmap/README.md) aims for.

## What is in this section

| # | Note | What it covers | Start here if… |
|---|---|---|---|
| 1 | [Evaluation fundamentals](01-evaluation-fundamentals.md) | Model vs application evals, offline vs online, golden datasets, metric design, release decisions | you have never built an eval suite |
| 2 | [LLM-as-a-Judge](02-llm-as-a-judge.md) | MT-Bench lineage, judge biases, calibration, rubric design, Agent-as-a-Judge | you use (or plan to use) model-graded metrics |
| 3 | [Agent benchmarks](03-agent-benchmarks.md) | SWE-bench family, GAIA, WebArena/OSWorld, τ-bench, pass^k — and the benchmark-integrity crisis | you evaluate agents or quote benchmark numbers |
| 4 | [RAG evaluation](04-rag-evaluation.md) | Component/pipeline/application/safety levels, RAGAS & DeepEval in practice | you build retrieval systems |
| 5 | [Eval engineering](05-eval-engineering.md) | Turning evals into CI/CD gates, regression suites, observability handoff, tooling | you want evals to block bad releases |
| 6 | [Evaluation dataset engineering](06-evaluation-datasets.md) | Golden-set taxonomies, synthesis methods and their circularity traps, size statistics, versioning and governance | your eval numbers depend on what you evaluate on |
| 7 | [Online experimentation](07-online-experimentation.md) | A/B, interleaving, shadow and canary designs; captured vs computed metrics; judge-in-the-loop; statistical hygiene | you need answers offline evals can't give |
| 🎓 | **[The LLM Evaluations course](course/README.md)** | Video-by-video English notes + transcripts for the full 19-lecture CampusX playlist (~20 h): foundations → benchmarks → RAG evaluation → production monitoring | you want a guided, step-by-step build-up rather than reference lookups |

## The course layer

The five notes above are the **reference layer** — concept maps for people who know what they're looking for. The [`course/`](course/README.md) subfolder is the **curriculum layer**: a complete, ordered walk through the CampusX *LLM Evaluations: The Step-by-Step Playlist for 2026* — every lecture transcribed from Hindi to English, expanded into structured notes, and cross-linked back into these reference notes. If you're new to evaluation, start with the [course](course/README.md); use these seven notes as the depth layer when a specific topic matters.

## How this connects to the rest of the repository

- **[Full roadmap Level 7 — LLM Evaluations](../roadmap/full-roadmap/level-07-llm-evaluations.md)** gives the session-by-session *learning path* through this topic; this section is the corresponding *reference material*. The roadmap also carries the interview vs on-the-job weights.
- **[101 — LLM Literacy](../101_LLM-Literacy/README.md)** covers [model benchmarks from the model-understanding angle](../101_LLM-Literacy/01-LLM%20101/7.%20Evaluation%20%26%20Benchmarks.md) (MMLU, GSM8K, contamination) — read it for literacy, read this section for engineering practice.
- **[102 — AI Application Development](../102_AI-Application-Development/README.md)** contains the RAG curriculum; [note 4](04-rag-evaluation.md) here extends its [evaluation protocol note](../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md) with concrete tooling.
- **[103 — Agentic AI](../103_Agentic%20AI/README.md)** covers agent architectures; [note 3](03-agent-benchmarks.md) covers how those systems are measured.
- **[104 — LLMOps](../104_LLMOps/README.md)** owns [observability](../104_LLMOps/README.md) — what you monitor *after* release. Note 5 defines the handoff point where offline eval ends and production monitoring begins.
- **[106 — AI Security & Safety](../106_AI-Security-Safety/README.md)** extends evaluation into adversarial territory: red teaming is evaluation with an adversary, and safety evals share machinery with quality evals.
- **[The evidence policy](../research/evidence-policy.md)** applies to every number quoted here: benchmark results are *measurements under specific conditions*, not universal properties of a model.

## The questions this section teaches you to answer

1. **"How would you know your system works?"** — with a task-defined eval set, explicit metrics, and a baseline, not a vibe. *(notes 1, 4, 5)*
2. **"Why should I trust your LLM-as-a-judge score?"** — because you measured its agreement with humans, checked its biases, and calibrated it. *(note 2)*
3. **"Model X tops benchmark Y — so what?"** — you know what the benchmark measures, what it doesn't, whether it's contaminated or saturated, and whether the harness itself moved the score. *(note 3)*
4. **"Did last week's prompt change make things better or worse?"** — your regression suite can answer, per metric, with uncertainty. *(note 5)*
5. **"What happens in production when reality drifts from the eval set?"** — you have online evaluation feeding failures back into the offline suite. *(notes 1, 5, 7)*
6. **"How many golden cases do you need — and how do you know they're not lying to you?"** — with size statistics, circularity controls, and drift audits on the dataset itself. *(note 6)*

<!-- nav-footer -->
---

*Open the [interactive site index](https://adilshamim8.github.io/AI-Engineering/) — every note, course, and guide in this repository on one page.*
