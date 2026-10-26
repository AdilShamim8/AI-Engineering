# LLM Evaluations — Course Cheat Sheet

> One page holding every formula, number, and decision rule from the 19-lecture [LLM Evaluations course](README.md). Use it after the course, in interviews, and while building your own eval suite. Every entry links to the lecture note that teaches it in depth.

---

## The one distinction that organizes everything

**Model evals** — how good is the model itself? (benchmarks, leaderboards — frontier-lab work, you need *literacy*)
**Application evals** — how good is *your* system? (golden datasets, judges, pipelines — **your day job**)
→ [Lecture 2](02-model-vs-application-evals.md)

## The evaluation workflow (build → test → build)

Component → pipeline → application. Build a component, test it, then build the next. Never build everything and test at the end. → [Lecture 3](03-evaluation-workflow.md)

## Why one pipeline is never enough

Different evals answer different questions; each needs its own pipeline (retriever evals, generator evals, pipeline evals, application evals, operational evals, safety evals). → [Lecture 4](04-multiple-eval-pipelines.md)

---

## Count-based metrics (lectures 5, 13, 14)

| Metric | Formula | Direction |
|---|---|---|
| **Recall@k** | relevant retrieved ÷ total relevant | higher = better |
| **Precision@k** | relevant retrieved ÷ total retrieved | higher = better |
| **Faithfulness** | supported claims ÷ total claims in answer | higher = better |
| **Answer relevance** | claims relevant to question ÷ total claims | higher = better |
| **Contextual relevancy** | relevant claims across contexts ÷ total claims in contexts | higher = better |
| **Toxicity** (DeepEval) | toxic opinions ÷ total opinions | **lower = better** |
| **PII** (DeepEval) | non-PII ÷ total extracted | higher = better |

**Reference-based** = you have the ideal answer/context → count against it. **Reference-free** = no reference, judge or model scores directly (toxicity, style, answer relevance as implemented by RAGAS). → [Lecture 5](05-eval-methods-reference-based-vs-free.md)

## Offline vs online

**Offline** (golden datasets, judges, before deploy): regression suites, release gates. **Online** (production traffic): monitoring, drift, sampled judging, alerting. Offline filters, online confirms; production failures promote back into offline goldens. → [Lecture 6](06-offline-vs-online-evals.md)

## Model evaluation literacy (lectures 7–11)

- **8 capability areas** to read benchmarks by: knowledge, reasoning, math, coding, instruction following, long context, multilingual, safety. → [Lecture 7](07-model-evals-capabilities.md)
- **Saturation** = benchmark too easy, top scores compress → tells you nothing. **Contamination** = test data leaked into training → scores lie. → [Lecture 8](08-benchmarking-saturation-contamination.md)
- **Benchmark evolution**: MMLU → MMLU-Pro → GPQA/MMLU-Redux era; always check what a benchmark *actually measures* and its label-noise history. → [Lecture 9](09-llm-benchmarks-evolution.md)
- **Leaderboards**: read the methodology (LM Arena = human preference; LMArena-style vs static benchmarks); distrust single-number rankings; check your *use case's* slice. → [Lecture 10](10-llm-leaderboards.md)
- **Model selection**: build a small custom eval on *your* task (the Text-to-SQL demo), 5 runs, judge with a pinned model; pick by task-fit + cost + latency, not leaderboard rank. → [Lecture 11](11-model-selection-custom-evals.md)

---

## RAG evaluation, hands-on (lectures 12–15)

- **The interview answer** — 3 levels × the build-test story: component (recall/precision; faithfulness/relevance), pipeline (RAG Triad), application (quality: correctness/completeness/style; safety; operations) + regression + monitoring. → [Lecture 12](12-rag-eval-interview-answer.md)
- **Retriever testing**: chunk-ID goldens or ideal-answer goldens; DeepEval three-part pattern (`LLMTestCase` + metric + `evaluate`); improvement loop 80/80 → 97/83 → 92/85 (reranker) → 99/85 (larger embeddings); k trade-offs. → [Lecture 13](13-testing-rag-retrievers.md)
- **Generator + pipeline**: faithfulness/answer relevance on the generator; then the **RAG Triad** (context relevance + faithfulness + answer relevance) on the full pipeline; the curious case — recall 99 / precision 89 / contextual relevancy 42 → noise per chunk → fix = smaller chunks. → [Lecture 14](14-rag-triad-generator-pipeline.md)
- **G-Eval** (deterministic judging): CoT criteria → evaluation steps → rubric → probability-weighted score over score tokens (8×0.7368 + 7×0.2105 + 9×0.0526 ≈ 7.84, ÷10 → 0.784) — kills judge variance. → [Lecture 15](15-geval-deterministic-judge.md)

## Safety evals (lecture 16)

1. Learn the failure modes (leakage, scope, toxicity, hallucination, bias, agency) and attacks (injection, jailbreak, poisoning, inference, tool hijack, DoS).
2. Pick **your** attack surface (the Doubt Solver: leakage + scope + toxicity; bias no — homogeneous audience; agency no — no tools).
3. Write the **safety policy** (the constitution).
4. Dataset = **adversarial + benign + mixed** (benign catches over-refusal; mixed tests partial compliance).
5. Toxicity: DeepEval built-in, threshold 0.3, lower-is-better. Leakage: 3 evaluators (prompt + content G-Evals, PII built-in). Scope: custom G-Eval (built-in `misuse` domain too coarse).
6. Fix with system prompts → guardrails → (last resort) fine-tuning. → [Lecture 16](16-rag-security-toxicity-leakage-scope-drift.md)

## Operational evals (lecture 17)

**Latency**: P50/P95/P99 (tail = worst UX), component breakdown, TTFT, cold starts (skip first 2 runs), repeats (5×), budgets, workload mix. **Cost**: per query, input/output split, P95-cost, segmentation, budget; output ≈ 4× input price; model choice = the biggest lever. **Reliability**: success/error/timeout/retry rates, categorized failures, under load. No judges, no goldens — just measurement. → [Lecture 17](17-rag-operational-evals.md)

## Regression testing (lecture 18)

- **Baseline** run (`baseline.json`) → change → **candidate** run → `compare.py` per-metric deltas → **metric registry** (which direction is good, per metric) → **noise threshold** (2σ from repeated runs) → verdict: promote / block.
- Any change (prompt, model, vector DB, chunk size) re-runs the whole suite. Wire into CI/CD. → [Lecture 18](18-rag-regression-testing.md)

## Online monitoring (lecture 19)

Tracing (`@traceable`) → dashboards (P95 latency, cost) → alerts → built-in toxicity evaluator on traces → same-evaluator golden rule (identical judge/thresholds online and offline) → `Add to dataset` closes the loop back to goldens. → [Lecture 19](19-online-eval-langsmith-monitoring.md)

---

## Numbers worth memorizing

- G-Eval worked example: ≈ **7.84 / 10 → 0.784** vs threshold 0.7
- Retriever loop: **80/80 → 97/83 → 92/85 → 99/85**; k=5→10 hurts precision; k=3 recall 84
- Generator: **91/73 → 96/92** after prompt fixes; overfitting warning after 3–4 rounds
- RAG Triad result: **92–93 / 86–87 / 42–43**; the 42 → noise per chunk (2 useful lines in a 5-line chunk = 2/5)
- Latency SLOs (failed): P95 **5.3 s vs 3.0 s** budget; TTFT **2,081 ms vs 1,200 ms**
- Cost: GPT-4o-mini ≈ **2 paise/query**; ₹57/day → **₹1,700/month** at 2k queries/day
- Regression demo: **45 → 38** (the metric you improved regressed) → **block**
- Thresholds used in the course: 0.7 (quality metrics), 0.3 (toxicity), 0.6 (style, after iteration)
- Dataset sizes: **15** goldens per course eval; at n=15 one flipped case = **6.7 points**

## The five interview one-liners

1. "I evaluate at three levels — component, pipeline, application — with both quality and safety metrics at each level."
2. "Count-based metrics for grounding; G-Eval-style probability-weighted judging for judgment calls."
3. "Every change re-runs the full suite against a noise threshold — 2 standard deviations — before it ships."
4. "Safety datasets mix adversarial, benign, and mixed cases, because over-refusal is also a failure."
5. "Online, I sample traces for judge-based metrics and alert on drift; failures promote back into the offline goldens."

---

## Cross-references

- [Course hub](README.md) · [Glossary](glossary.md) · [Self-assessment quiz](flashcards.md)
- [Section 105 — AI Evaluation](../README.md) — the reference layer beneath this course
