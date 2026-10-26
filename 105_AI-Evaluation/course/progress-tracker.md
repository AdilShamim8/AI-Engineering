# LLM Evaluations — Progress Tracker

> A checklist for working through the [19-lecture course](README.md). Copy this file, check off as you go, and date each milestone. The time estimates assume you read the notes (~1 hour per lecture) and do the four code-along lectures hands-on (~3 hours each).

---

## Unit 0 — Orientation

- [ ] **Lecture 1** — Playlist overview · 23:24 · [notes](01-course-overview.md) · read: _what the course covers and how to study it_
  - Completed on: ______

## Unit 1 — Foundations (lectures 2–6)

- [ ] **Lecture 2** — Model vs application evals · 24:32 · [notes](02-model-vs-application-evals.md) · _the one distinction that organizes everything_
- [ ] **Lecture 3** — The evaluation workflow · 17:00 · [notes](03-evaluation-workflow.md) · _build → test → build_
- [ ] **Lecture 4** — Multiple eval pipelines · 28:03 · [notes](04-multiple-eval-pipelines.md) · _why one pipeline is never enough_
- [ ] **Lecture 5** — Eval methods · 53:10 · [notes](05-eval-methods-reference-based-vs-free.md) · _LLM-as-a-Judge, reference-based vs free_
- [ ] **Lecture 6** — Offline vs online evals · 1:21:09 · [notes](06-offline-vs-online-evals.md) · _the two halves of the discipline_
- [ ] **Checkpoint**: [Unit 1 quiz](flashcards.md) — 15 questions, miss ≤ 2 before moving on
  - Completed on: ______

## Unit 2 — Model evaluation & benchmarks (lectures 7–11)

- [ ] **Lecture 7** — Model evals & capabilities · 37:52 · [notes](07-model-evals-capabilities.md) · _the 8 capability areas_
- [ ] **Lecture 8** — Benchmarking: saturation & contamination · 51:20 · [notes](08-benchmarking-saturation-contamination.md) · _why benchmark scores lie_
- [ ] **Lecture 9** — Benchmark evolution · 1:50:47 · [notes](09-llm-benchmarks-evolution.md) · _MMLU and its descendants_
- [ ] **Lecture 10** — Leaderboards · 30:07 · [notes](10-llm-leaderboards.md) · _reading rankings critically_
- [ ] **Lecture 11** — Model selection with custom evals · 1:56:53 · [notes](11-model-selection-custom-evals.md) · _picking a model on YOUR task_
- [ ] **Checkpoint**: [Unit 2 quiz](flashcards.md) — 14 questions
  - Completed on: ______

## Unit 3 — RAG evaluation (lectures 12–15) · *the hands-on core*

- [ ] **Lecture 12** — The RAG eval interview answer · 46:20 · [notes](12-rag-eval-interview-answer.md) · _the 3-level map_
- [ ] **Lecture 13** — Testing RAG retrievers · 1:47:02 · [notes](13-testing-rag-retrievers.md) · 💻 **code-along**
- [ ] **Lecture 14** — Generator & pipeline: the RAG Triad · 1:21:29 · [notes](14-rag-triad-generator-pipeline.md) · 💻 **code-along**
- [ ] **Lecture 15** — G-Eval · 1:26:52 · [notes](15-geval-deterministic-judge.md) · _deterministic LLM-as-a-Judge_
- [ ] **Checkpoint**: [Unit 3 quiz](flashcards.md) — 15 questions
  - Completed on: ______

## Unit 4 — Production evaluation (lectures 16–19)

- [ ] **Lecture 16** — Security: toxicity, leakage, scope drift · 1:35:19 · [notes](16-rag-security-toxicity-leakage-scope-drift.md) · _the safety eval suite_
- [ ] **Lecture 17** — Operational evals · 1:19:32 · [notes](17-rag-operational-evals.md) · 💻 **code-along** · _latency, cost, reliability_
- [ ] **Lecture 18** — Regression testing · 54:16 · [notes](18-rag-regression-testing.md) · _the release gate_
- [ ] **Lecture 19** — Online monitoring with LangSmith · 1:14:24 · [notes](19-online-eval-langsmith-monitoring.md) · 💻 **code-along** · _closing the loop_
- [ ] **Checkpoint**: [Unit 4 quiz](flashcards.md) — 16 questions
  - Completed on: ______

## After the course

- [ ] Re-read the [cheat sheet](cheatsheet.md) the day before any interview
- [ ] Answer the five interview one-liners from the [cheat sheet](cheatsheet.md) out loud, unprompted
- [ ] Build your own eval suite for a RAG project you own (the four code-alongs are the template)
- [ ] Read the reference layer for depth: [LLM-as-a-Judge](../02-llm-as-a-judge.md) → [Eval engineering](../05-eval-engineering.md) → [Dataset engineering](../06-evaluation-datasets.md) → [Online experimentation](../07-online-experimentation.md)
- [ ] Practice the [project deep-dive answers](../../interview/questions/03-project-deep-dive.md) using your eval-suite project as the story

---

## Time budget

| Path | Reading | Hands-on | Total |
|---|---|---|---|
| Notes only (no code) | ~22 h | — | ~22 h |
| Full path (with 4 code-alongs) | ~22 h | ~12 h | ~34 h |
| Crash revision (cheat sheet + quiz + glossary) | — | — | ~3 h |

## Cross-references

- [Course hub](README.md) · [Glossary](glossary.md) · [Self-assessment quiz](flashcards.md) · [Cheat sheet](cheatsheet.md)
- [Section 105 — AI Evaluation](../README.md)
