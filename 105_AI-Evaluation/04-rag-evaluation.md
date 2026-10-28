# RAG evaluation in practice

> Part of [105 — AI Evaluation](README.md) · Reviewed October 17, 2026
>
> This note extends the repository's [reproducible RAG evaluation protocol](../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md) (which defines the protocol discipline: splits, baselines, paired comparisons, judge calibration) with the **tooling and metric mechanics** for day-to-day work. Read that note first if you haven't — it explains *why* the discipline matters; this note explains *how* the frameworks implement pieces of it.

## The four-level model

Evaluate a RAG system at the level where the failure lives. The levels, and the question each answers:

| Level | Question | Primary metrics |
|---|---|---|
| **Retrieval (component)** | Did we find the right evidence? | Recall@k, nDCG@k, context precision/recall |
| **Generation (component)** | Given good context, is the answer faithful and relevant? | Faithfulness, answer relevancy, claim support |
| **Pipeline (end-to-end)** | Does retrieve→generate produce correct, complete answers? | Factual correctness, completeness, citation validity |
| **Safety** | Can the corpus or query make it leak, inject, or misbehave? | Injection success, PII leakage, permission violations |

The diagnostic value comes from the combination: low context recall with high faithfulness means your generator is honest but starved (fix retrieval); high context recall with low faithfulness means the generator ignores good evidence (fix prompting or model); everything good at component level but poor at pipeline level means interaction effects (context assembly, ordering, truncation).

## Retrieval metrics: definitions that actually matter

- **Recall@k** — of the documents/chunks labeled relevant for a query, what fraction appears in the top-k? This is the metric that most directly predicts "did the system have a chance to answer."
- **nDCG@k** — like recall but position-aware, using graded relevance. Use it when ranking quality matters (the answer depends more on the top-2 chunks than the top-10).
- **Context precision / context recall** (as implemented in [Ragas](https://docs.ragas.io/)) — LLM-judged versions of "were the retrieved chunks relevant" and "was all needed information retrieved." Convenient when you lack human relevance labels; remember they are *judge-derived* quantities and inherit judge calibration concerns (see [LLM-as-a-Judge](02-llm-as-a-judge.md)).
- **Unjudged ≠ irrelevant.** In classic IR datasets (BEIR-style), documents without relevance labels are unknowns, not negatives. Report the judged fraction; an nDCG computed over 30% judged coverage is a weak instrument.

A grounded habit from the protocol note, worth repeating: **always run the lexical (BM25) baseline.** If your dense retrieval doesn't beat BM25 on your corpus, the embedding model isn't earning its complexity. [BEIR](https://github.com/beir-cellar/beir) remains the standard public resource for cross-task retrieval baselines; [MTEB](https://github.com/embeddings-benchmark/mteb) for embedding-model shortlisting (check per-task, not aggregate, scores — and note its license caveats per task).

## Generation metrics: the RAG triad and beyond

The [RAG triad](https://www.trulens.org/getting_started/core_concepts/rag_triad/) — **context relevance, groundedness (faithfulness), answer relevance** — decomposes quality into three judgeable properties:

1. **Context relevance** — is the retrieved context pertinent to the query? (retrieval quality, judged)
2. **Groundedness / faithfulness** — are the claims in the answer supported by the retrieved context?
3. **Answer relevance** — does the answer address what was actually asked?

The triad is a *diagnostic triangle*: each pair of failures localizes the problem. Its key conceptual limit, stated plainly in the protocol note: **groundedness is not factual truth.** An answer can faithfully repeat a stale or wrong document. Factual correctness against reference answers (or fresh sources) is a separate, fourth metric — and for high-stakes domains it is the one that matters most.

Completeness, citation validity (does the cited chunk exist and contain the cited claim?), abstention on unanswerable questions, and format compliance round out the application-level set.

## Tooling: what the frameworks actually do

| Tool | Sweet spot | Evaluation model |
|---|---|---|
| [Ragas](https://docs.ragas.io/) | RAG metric suite + synthetic test-set generation | Reference-free judge metrics (faithfulness, relevancy, precision/recall) + testset generation with human-in-the-loop review |
| [DeepEval](https://github.com/confident-ai/deepeval) | Pytest-native evals, includes agent metrics & red teaming | Metrics as pytest assertions; G-Eval-style rubric metrics; integrates with CI |
| [TruLens](https://www.trulens.org/) | RAG triad + tracing in notebooks/apps | Feedback functions (judged) wired to traces |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Matrix evals across prompts/models + CI + red teaming | Assertions (deterministic, semantic, model-graded) over YAML-declared matrices |

A minimal, honest DeepEval-style test (illustrative of the shape, not a certified result — configure your own provider and dataset):

```python
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric

def test_rag_answer():
    case = LLMTestCase(
        input="What is the notice period for cancelling a Pro plan?",
        actual_output=rag_pipeline.answer("What is the notice period for cancelling a Pro plan?"),
        expected_output="14 days before the next renewal date.",
        retrieval_context=rag_pipeline.last_retrieved_chunks,  # what the generator actually saw
    )
    # Judge metrics: pin the judge model + prompt, and calibrate against
    # human labels before letting these gate anything (see note 02).
    assert_test(case, [FaithfulnessMetric(threshold=0.8), AnswerRelevancyMetric(threshold=0.7)])
```

Three implementation rules that make such tests trustworthy:

1. **Feed the judge the actual retrieval context** (`retrieval_context`), not a re-fetch — you are measuring what the generator saw, not what a fresh retrieval would find.
2. **Pin judge model and prompts** in the test configuration; a drifting judge silently redefines your metrics.
3. **Treat thresholds as task-specific calibrations**, not universal standards — 0.8 faithfulness on policy Q&A is a different bar than 0.8 on creative summarization. Set them from your calibration set, and revisit when the task distribution shifts.

## The safety level

RAG's unique attack surface is that **the corpus is an input channel**. The safety level of evaluation must cover:

- **Indirect prompt injection** — instructions hidden in retrieved documents that attempt to hijack the generator (test with a poisoned corpus deliberately; see [prompt injection defense](../106_AI-Security-Safety/02-prompt-injection-defense.md)).
- **Permission boundaries** — can user A's query retrieve user B's documents? Test cross-tenant queries explicitly; retrieval benchmarks say nothing about authorization (a point the [advanced learning path](../learning-paths/advanced-engineering.md) also insists on).
- **PII leakage** — does the answer echo sensitive fields from context that should be redacted at retrieval or generation time?
- **Corpus poisoning persistence** — if a malicious document enters the index, do your guardrails catch it at query time, and can you trace and purge it? (Provenance metadata makes this tractable — see [governance](../106_AI-Security-Safety/06-responsible-ai.md).)

## Common failure patterns (and what they teach)

- **Retrieval finds it, answer ignores it** — check context ordering (lost-in-the-middle), instruction strength, and whether the generator's context exceeds its effective attention.
- **Answer is faithful to the wrong document** — stale corpus versioning; add document-freshness checks to the eval set.
- **Great on your eval set, poor in production** — eval set drift; mine production failures back into the set (the [self-improving loop](05-eval-engineering.md)).
- **Ragas scores move, nothing else does** — judge prompt or judge model drifted; pin and version them, and calibrate against human labels periodically.

## References

- [Reproducible RAG evaluation protocol](../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md) — this repository's discipline-first companion note
- [RAG curriculum, module 5–7](../102_AI-Application-Development/03-RAG/README.md) — advanced RAG patterns and production architecture
- Ragas — [docs.ragas.io](https://docs.ragas.io/) · [repository](https://github.com/vibrantlabsai/ragas)
- DeepEval — [repository](https://github.com/confident-ai/deepeval) · [documentation](https://deepeval.com/docs/getting-started)
- TruLens RAG triad — [trulens.org](https://www.trulens.org/getting_started/core_concepts/rag_triad/)
- BEIR (retrieval baselines) — [repository](https://github.com/beir-cellar/beir) · MTEB (embedding evaluation) — [repository](https://github.com/embeddings-benchmark/mteb)
- [Roadmap Level 7, module 8 — RAG evals](../roadmap/full-roadmap/level-07-llm-evaluations.md) — the session-level syllabus for this topic

Previous: [Agent benchmarks](03-agent-benchmarks.md) · Next: [Eval engineering](05-eval-engineering.md)

<!-- nav-footer -->
---

**Navigate:** [← 03. Agent Benchmarks](03-agent-benchmarks.md) · [Section hub](README.md) · [05. Eval Engineering →](05-eval-engineering.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
