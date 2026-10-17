# Evaluation fundamentals

> Part of [105 — AI Evaluation](README.md) · Reviewed October 17, 2026

This note covers the concepts that every other evaluation topic builds on: what you are measuring, where you measure it, what you measure it *against*, and how a measurement becomes a release decision. If you have built eval suites before, skim to the sections on golden datasets and release decisions, which are where most teams go wrong.

## Model evals vs application evals

The single most common beginner mistake is conflating two different questions:

- **Model evaluation** asks: *how capable is this foundation model, in general?* It is answered by public benchmarks (MMLU-Pro, GPQA, SWE-bench) and leaderboards. Its unit of analysis is the model.
- **Application evaluation** asks: *does this specific system do the job its users need?* It is answered by your own test suite over your own data and prompts. Its unit of analysis is the end-to-end system — including your prompt, retrieval corpus, guardrails, and tools.

A model that tops every leaderboard can fail your application, and a mid-ranked model can be the right choice once cost, latency, and your actual task distribution are considered. The [LLM literacy note on benchmarks](../101_LLM-Literacy/01-LLM%20101/7.%20Evaluation%20%26%20Benchmarks.md) covers model-side evaluation and its pitfalls (contamination, saturation, Goodhart's law); the rest of this section is about the application side, which is where AI engineers spend most of their time.

Model evals still matter to you at two moments: **shortlisting** (using leaderboards to pick 2–3 candidates to test seriously) and **requalification** (when a provider deprecates a model version and you must re-run your suite against the replacement).

## Offline vs online evaluation

| | Offline evaluation | Online evaluation |
|---|---|---|
| **When** | Before release, in CI | After release, continuously |
| **Data** | Curated eval sets (golden datasets) | Production traffic, sampled |
| **Question** | "Is this change at least as good as the baseline?" | "Is quality drifting in the real world?" |
| **Failure it catches** | Regressions you can enumerate | Emergent failures, distribution shift, adversarial users |
| **Cost of being wrong** | You ship a bad change | Users already experienced it |

You need both, and you need the loop between them: production failures that matter get **promoted into the offline suite** so the same regression can never ship again. This "self-improving golden dataset" pattern is the core of [eval engineering](05-eval-engineering.md), and the observability side of the loop (logging, sampling, dashboards, alerts) is covered in [104 — LLMOps / Observability](../104_LLMOps/README.md).

Online evaluation has a measurement subtlety worth internalizing early: proxy signals (thumbs-up rates, retry rates, escalation to human) measure *user-perceived* quality, while sampled LLM-judged or human-reviewed audits measure *actual* quality. They disagree in systematic ways — users thumb up confident wrong answers — so track them as separate metrics rather than blending them.

## What are you measuring? A taxonomy of eval targets

Every eval answers a question about a *target*. Naming the target precisely determines the metric:

| Target | Example question | Example metric |
|---|---|---|
| **Exact output** | "Is the JSON schema-valid?" | Pass/fail assertion |
| **Output property** | "Is the answer grounded in the cited sources?" | Faithfulness score (LLM-judged) |
| **Retrieval quality** | "Did the retriever surface the evidence needed?" | Recall@k, nDCG@k |
| **Trajectory quality** | "Did the agent take a sensible path?" | Tool-selection accuracy, step efficiency |
| **Task outcome** | "Did the user actually get their problem solved?" | Task success rate, human review |
| **Safety** | "Does it refuse harmful requests without over-refusing?" | Attack success rate, over-refusal rate |
| **Operations** | "Can we afford it? Is it fast enough?" | Latency percentiles, cost per query |

The taxonomy matters because **each row needs different machinery**: assertions and programmatic checks for the top rows, judge calibration for the middle, red-team suites for safety (see [106 — AI Security & Safety](../106_AI-Security-Safety/README.md)), and load testing for the bottom. Teams that try to score everything with one "quality" number end up with a metric nobody can act on.

## Golden datasets

A **golden dataset** is your curated, versioned set of test cases with known-good references or expected behaviors. It is the anchor that makes comparisons meaningful across time. Practical rules that hold up in real projects:

1. **Size for coverage, not statistics.** 50–200 well-chosen cases representing your real query distribution — including the awkward slices (ambiguous queries, unanswerable questions, adversarial inputs, non-English, edge-case formatting) — beat 10,000 auto-generated clones. The [retrieval evaluation protocol note](../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md) covers the split discipline in depth: development vs held-out test, and why random splits leak.
2. **Hand-write the core; augment deliberately.** LLM-generated test cases are *candidates*, not ground truth — they inherit the generating model's blind spots and must be reviewed before promotion. Use synthetic generation for bulk/coverage, human review for anything that gates a release.
3. **Version everything the result depends on.** Cases, prompts, model versions, judge prompts, retrieval corpus snapshot. An eval result that cannot name its inputs is not a measurement; it is an anecdote.
4. **Feed failures in.** Every production incident and every red-team discovery becomes a new case (with the fix's PR linked). The dataset should grow monotonically toward the specific ways your system has actually failed.

## Metric design: from question to number

Once the target is named, design the metric in four steps:

1. **Define construct.** "Faithfulness = every claim in the answer is entailed by the retrieved context." Write it down; the definition is the spec for whoever implements the scorer.
2. **Choose mechanism.** Programmatic (exact match, schema validation, unit-test pass) where possible — deterministic, cheap, debuggable. Human review for gold standards and calibration. LLM-as-judge for scale on semantic properties, accepting its calibration burden (see [note 2](02-llm-as-a-judge.md)).
3. **Pilot on failures, not on easy cases.** Run the metric on cases where you already know the system fails. A metric that scores known-bad outputs as fine is broken, no matter how elegant its definition.
4. **Report uncertainty honestly.** For paired comparisons over the same eval set, report the distribution of per-case differences, not just means. A +2% average that is +30% on one query slice and −10% on another is a different engineering story.

## Release decisions: where evaluation meets engineering

The end product of an eval suite is a **release decision**, and treating that decision explicitly is what separates mature teams:

- **Set thresholds before you look at results.** Acceptance criteria decided after seeing the numbers are rationalization, not criteria. Absolute thresholds are task-specific; there is no universal "0.9 faithfulness is good."
- **Separate must-haves from diagnostics.** Some metrics gate the release (regression on faithfulness blocks ship); others only inform (cost per query is up 8% — acceptable or not is a product call).
- **Distinguish regressions from noise.** Re-run variance on stochastic metrics is real; a change within run-to-run variance is not a regression. Know your noise floor before declaring wins.
- **Keep a decision log.** What shipped, what the evals said, who decided, what happened next. This is the audit trail that [governance](../104_LLMOps/README.md) and incident retrospectives will ask for.

The Air Canada case is the canonical cautionary tale for skipping this discipline: in *Moffatt v. Air Canada* (British Columbia Civil Resolution Tribunal, February 2024), the airline was held liable for its chatbot inventing a bereavement-fare policy, in part because there was no evaluation or verification layer between the model and the customer. The tribunal rejected the argument that the chatbot was "a separate legal entity." An eval suite that measured factual grounding against the airline's actual policies was exactly the missing control. ([BBC coverage](https://www.bbc.com/travel/article/20240222-air-canada-chatbot-misinformation-what-travellers-should-know))

## References

- Hamel Husain, [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) — the practitioner essay on building failure-driven eval suites (accessed October 2026).
- Anthropic Engineering, [*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (January 2026) — how a frontier lab structures agent evals.
- [Roadmap Level 7 — LLM Evaluations](../roadmap/full-roadmap/level-07-llm-evaluations.md) — the session-by-session learning path for this whole topic.
- [Evidence policy](../research/evidence-policy.md) — this repository's rules for what a measurement can and cannot claim.

Next: [LLM-as-a-Judge →](02-llm-as-a-judge.md)
