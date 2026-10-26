# How This Course Is Organized — and Why

> The playlist this course transcribes ([CampusX, LLM Evaluations, 2026](README.md)) is unusually well-organized for a free Hindi-language series: ~20 hours across 19 videos, cumulative, hands-on, and interview-aware. This note documents the organizational principles we extracted from how the instructor structures his teaching — the same principles this repository's course folder applies — so you can reuse them for any long-form technical course you need to internalize or teach.

---

## The seven principles

### 1. One spine, drawn every lecture

The instructor opens nearly every lecture by re-drawing the same flowchart: **component → pipeline → application**, with quality/safety/operations at the application level. Each lecture fills in one box and re-shows the map. The repetition is deliberate — by lecture 14, every student can reproduce the whole architecture from memory, which is exactly what makes the knowledge interview-ready.

*Applied here:* every note's "What this lecture covers" section restates where the lecture sits in the course structure, and the [course hub](README.md) table is the map.

### 2. The distinction-first teaching order

Lecture 2 (model vs application evals) is pure taxonomy — no code, no metrics — and the whole course depends on it. The instructor teaches the *one distinction that organizes the domain* before any detail, then every later concept is filed against it. Detail without a filing system is forgotten; a filing system without detail is empty.

*Applied here:* the notes preserve this order exactly; the [glossary](glossary.md) carries the taxonomy as definitions you can look up later.

### 3. Build → test → build (never build-then-test)

The hands-on track (lectures 12–19) never assembles the whole system and tests at the end. It builds the retriever, tests the retriever, builds the generator, tests the generator, wires the pipeline, tests the pipeline. Each component is verified *before* the next depends on it — the software-engineering discipline of incremental integration, applied to an AI system.

*Applied here:* the four code-along lectures ([13](13-testing-rag-retrievers.md), [14](14-rag-triad-generator-pipeline.md), [17](17-rag-operational-evals.md), [19](19-online-eval-langsmith-monitoring.md)) are marked in the [progress tracker](progress-tracker.md) as the sequence to reproduce on your own project.

### 4. Theory in service of a running example

There is exactly one example system for the entire hands-on half: the CampusX Doubt Solver (a RAG chatbot over course transcripts). Every metric, judge, threshold, and failure is demonstrated on *that* system. No toy datasets, no switching contexts. The running example means every concept lands with the question "how would this number look on my system?" already activated.

*Applied here:* the notes preserve every number from the running example (recall 80→97, faithfulness 91→96, the 42% contextual-relevancy curious case) — the [cheat sheet](cheatsheet.md) collects them as worked examples.

### 5. Datasets before metrics

The instructor builds golden datasets *before* introducing each metric that consumes them — retriever goldens before recall/precision, judgment goldens before G-Eval, adversarial/benign/mixed sets before safety metrics. The implicit lesson (made explicit in [Section 105 note 6](../06-evaluation-datasets.md)): the dataset is the moat, the metric is just the reader.

### 6. The interview layer on top of the engineering layer

Periodically the instructor pauses the engineering to deliver "how to answer this in an interview" — the model answer for "how do you evaluate your RAG app?" is a whole lecture ([12](12-rag-eval-interview-answer.md)). Teaching the same knowledge twice — once as engineering, once as interview narrative — is what makes it retrievable under pressure.

*Applied here:* every note carries an **Interview angles** section separating the interview framing from the engineering content; the [quiz](flashcards.md) tests both.

### 7. Honest teaching of variance and failure

The instructor shows eval runs failing, judges wobbling, overfitting warnings, and a scope-adherence failure live on camera — then fixes them. Curriculum that only shows the happy path produces engineers who panic at the first red metric. Every "it failed, here's why, here's the fix" moment is preserved in the notes rather than smoothed away.

*Applied here:* the notes keep every failure-and-fix loop verbatim-faithfully, and the expert-commentary blocks (`💡`) extend them with the research context the lecture didn't cover.

## How we applied it to the repository structure

| Course-folder artifact | Principle it serves |
|---|---|
| `README.md` hub with the 19-lecture table | The spine (1) |
| `01`–`19` notes, one per lecture | Distinction-first order, running example (2, 4) |
| `transcripts/` — full English transcripts | Nothing-skipped fidelity; searchable verbatim detail |
| `glossary.md` — 120 terms, lecture-linked | The taxonomy as a lookup (2) |
| `flashcards.md` — 60-question quiz | Retention checkpoints per unit |
| `cheatsheet.md` — formulas and numbers | The running example's worked results (4) |
| `progress-tracker.md` — per-lecture checklist | The build→test→build study sequence (3) |
| Cross-links into Section 105's reference notes | Depth beyond the course (5, 7) |

The same structure generalizes to any course you want to internalize: **map → ordered notes → transcripts → glossary → quiz → cheat sheet → tracker → reference layer**. If you're transcribing and translating a course yourself (as this folder did from Hindi), build those artifacts in that order — the map first, always.

## Cross-references

- [Course hub](README.md) · [Progress tracker](progress-tracker.md) · [Glossary](glossary.md) · [Cheat sheet](cheatsheet.md)
- [Section 105 — AI Evaluation](../README.md) — the reference layer
- [Eval engineering](../05-eval-engineering.md) — where the course's hands-on track hands off to production practice
