# LLM Evaluations — The Complete Course Notes

> A video-by-video, step-by-step English study companion for the **"LLM Evaluations: The Step-by-Step Playlist for 2026"** course by CampusX (taught in Hindi by Nitish Singh).
> Every lecture has been transcribed, translated to English, and expanded into structured expert notes — with **nothing skipped**.

**Source playlist:** [Master LLM Evaluations: The Step-by-Step Playlist for 2026 (CampusX, 2026)](https://www.youtube.com/playlist?list=PLEneLIDJFpcA) — 19 videos, ~20 hours of instruction.

---

## What this course teaches

Evaluation is the single most underrated skill in AI engineering. This course builds it from zero to production:

- **What LLM evaluations actually are** — the *complete testing setup*, not just metrics
- **The one distinction that organizes everything** — model evals vs application evals
- **How to run evaluations** — the end-to-end workflow, multiple pipelines, offline vs online
- **Evaluation methods** — exact-match, semantic similarity, LLM-as-a-Judge, reference-based vs reference-free
- **Model evaluation literacy** — the 8 capability areas, benchmarks (MMLU, GSM8K, SWE-bench…), saturation, contamination, leaderboards, and how to select a model with custom evals
- **RAG evaluation in practice** — retriever testing, the RAG Triad, G-Eval, security testing (toxicity, leakage, scope drift)
- **Production evaluation** — operational evals, regression testing, and online monitoring with LangSmith

The instructor's framing is unapologetically practical: as an AI engineer you build **applications**, so **application evaluation is the main topic of this course** — model evaluation is covered for *literacy* (so you can pick models and read benchmark claims critically), not because you will run frontier-lab evals yourself.

## Course structure

| Unit | Videos | Focus |
|---|---|---|
| **0. Orientation** | 1 | What the playlist covers and how to study it |
| **1. Foundations** | 2–6 | What evals are, the evaluation workflow, why one pipeline is never enough, eval methods, offline vs online |
| **2. Model evaluation & benchmarks** | 7–11 | Capabilities, benchmarking, benchmark evolution, leaderboards, model selection with custom evals |
| **3. RAG evaluation** | 12–15 | The interview answer, retriever testing hands-on, the RAG Triad, G-Eval |
| **4. Production evaluation** | 16–19 | Security testing, operational evals, regression testing, online monitoring with LangSmith |

## Lecture notes & transcripts

| # | Lecture | Duration | Notes | Transcript |
|---|---|---|---|---|
| 1 | Master LLM Evaluations — playlist overview | 23:24 | [01-course-overview.md](01-course-overview.md) | [transcript](transcripts/01-course-overview.md) |
| 2 | Introduction — Model Evals vs Application Evals | 24:32 | [02-model-vs-application-evals.md](02-model-vs-application-evals.md) | [transcript](transcripts/02-model-vs-application-evals.md) |
| 3 | How to Evaluate LLM Applications — the Complete Workflow | ~17:00 | [03-evaluation-workflow.md](03-evaluation-workflow.md) | [transcript](transcripts/03-evaluation-workflow.md) |
| 4 | Why Your AI Application Needs Multiple Eval Pipelines | 28:03 | [04-multiple-eval-pipelines.md](04-multiple-eval-pipelines.md) | [transcript](transcripts/04-multiple-eval-pipelines.md) |
| 5 | LLM Eval Methods — LLM-as-a-Judge, Reference-Based vs Reference-Free | 53:10 | [05-eval-methods-reference-based-vs-free.md](05-eval-methods-reference-based-vs-free.md) | [transcript](transcripts/05-eval-methods-reference-based-vs-free.md) |
| 6 | Offline Evals vs Online Evals | 1:21:09 | [06-offline-vs-online-evals.md](06-offline-vs-online-evals.md) | [transcript](transcripts/06-offline-vs-online-evals.md) |
| 7 | LLM Model Evals & Capabilities | 37:52 | [07-model-evals-capabilities.md](07-model-evals-capabilities.md) | [transcript](transcripts/07-model-evals-capabilities.md) |
| 8 | What is LLM Benchmarking — Saturation vs Contamination | 51:20 | [08-benchmarking-saturation-contamination.md](08-benchmarking-saturation-contamination.md) | [transcript](transcripts/08-benchmarking-saturation-contamination.md) |
| 9 | What are LLM Benchmarks — Evolution of AI Knowledge Benchmarks | 1:50:47 | [09-llm-benchmarks-evolution.md](09-llm-benchmarks-evolution.md) | [transcript](transcripts/09-llm-benchmarks-evolution.md) |
| 10 | How to Use LLM Leaderboards | 30:07 | [10-llm-leaderboards.md](10-llm-leaderboards.md) | [transcript](transcripts/10-llm-leaderboards.md) |
| 11 | Selecting the Right LLM — Running Custom Model Evals | 1:56:53 | [11-model-selection-custom-evals.md](11-model-selection-custom-evals.md) | [transcript](transcripts/11-model-selection-custom-evals.md) |
| 12 | How to Answer "How Do You Evaluate Your RAG App?" in Interviews | 46:20 | [12-rag-eval-interview-answer.md](12-rag-eval-interview-answer.md) | [transcript](transcripts/12-rag-eval-interview-answer.md) |
| 13 | How to Test RAG Retrievers (Hands-On) | 1:47:02 | [13-testing-rag-retrievers.md](13-testing-rag-retrievers.md) | [transcript](transcripts/13-testing-rag-retrievers.md) |
| 14 | Evaluating RAG — Generator & Full Pipeline with the RAG Triad | 1:21:29 | [14-rag-triad-generator-pipeline.md](14-rag-triad-generator-pipeline.md) | [transcript](transcripts/14-rag-triad-generator-pipeline.md) |
| 15 | Mastering G-Eval — the Deterministic LLM-as-a-Judge Framework | 1:26:52 | [15-geval-deterministic-judge.md](15-geval-deterministic-judge.md) | [transcript](transcripts/15-geval-deterministic-judge.md) |
| 16 | Securing Your RAG Application — Toxicity, Leakage & Scope Drift | 1:35:19 | [16-rag-security-toxicity-leakage-scope-drift.md](16-rag-security-toxicity-leakage-scope-drift.md) | [transcript](transcripts/16-rag-security-toxicity-leakage-scope-drift.md) |
| 17 | RAG Operational Evals — Building Faster & Cheaper RAG Systems | 1:19:32 | [17-rag-operational-evals.md](17-rag-operational-evals.md) | [transcript](transcripts/17-rag-operational-evals.md) |
| 18 | RAG Regression Testing — Preventing Silent AI Failures | 54:16 | [18-rag-regression-testing.md](18-rag-regression-testing.md) | [transcript](transcripts/18-rag-regression-testing.md) |
| 19 | Online RAG Evaluation — Monitoring Production LLMs with LangSmith | 1:14:24 | [19-online-eval-langsmith-monitoring.md](19-online-eval-langsmith-monitoring.md) | [transcript](transcripts/19-online-eval-langsmith-monitoring.md) |

## How to study this course

1. **Watch/read in order the first time.** The course is deliberately cumulative: the model-vs-application distinction from lecture 2 is used in every later lecture; the eval methods from lecture 5 power the RAG metrics in lectures 13–15.
2. **Read the notes before or instead of the video.** The notes are written to stand alone — every concept, example, analogy, and side remark from the lecture is here, restructured for reading.
3. **Do the hands-on parts.** Lectures 13, 14, 17 and 19 are code-alongs (retriever metrics, RAG Triad, operational evals, LangSmith). Reproduce them on your own RAG project.
4. **Use the transcripts for detail work.** When notes mention something you want verbatim (a prompt, a metric name, a slide's wording), search the transcript.
5. **Test yourself after each unit.** The [self-assessment quiz](flashcards.md) has 60 questions with verified answers across the four units — if you miss more than 2 per unit, re-read that unit's notes.
6. **Look up terms in the glossary.** The [course glossary](glossary.md) defines all 120 terms the course uses, each linked back to the lecture that teaches it.
7. **Connect to the knowledge base.** Each note cross-links the corresponding [Section 105 reference notes](../README.md) (LLM-as-a-Judge, agent benchmarks, RAG evaluation, eval engineering) for the research-grade depth: papers, surveys, and failure cases beyond the course.

## Conventions used in these notes

- **Timestamps** like `(12:18)` mark where in the lecture a concept is discussed.
- **> 💡 Expert commentary** blocks add context the lecture didn't cover — clarifications, corrections, industry practice, and pointers to primary sources. They are clearly separated so the instructor's voice stays intact.
- Code, prompts, and tool names are formatted as the lecture presents them.
- The transcripts are machine-translated from Hindi auto-captions and lightly cleaned; they preserve everything the instructor said, in his own (translated) words.

## Relationship to the rest of this repository

- [**105 — AI Evaluation (parent section)**](../README.md): the concept-level knowledge base (fundamentals, LLM-as-a-Judge, agent benchmarks, RAG evaluation, eval engineering). Start there for the map; use this course for the step-by-step build-up.
- [**Full roadmap Level 7 — LLM Evaluations**](../../roadmap/full-roadmap/level-07-llm-evaluations.md): the session-by-session learning path that includes this topic.
- [**102 — AI Application Development**](../../102_AI-Application-Development/README.md): the RAG curriculum whose evaluation layer this course deepens.
- [**104 — LLMOps**](../../104_LLMOps/README.md): observability and monitoring — where online evaluation (lecture 19) hands off.
- [**106 — AI Security & Safety**](../../106_AI-Security-Safety/README.md): red teaming and guardrails — the security testing of lecture 16 is its evaluation-side mirror.
