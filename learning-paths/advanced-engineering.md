# From foundations to advanced AI engineering

Reviewed October 9, 2026. This is a competency progression, not a promise of expertise after a fixed number of months. The existing 101–104 curriculum supplies background; advancing requires artifacts that another engineer can inspect and reproduce.

## Progression and exit criteria

| Stage | Study | Build | Evidence required to advance |
|---|---|---|---|
| Foundation | [LLM literacy](../101_LLM-Literacy/README.md): tokens, representations, training versus inference, uncertainty | A small application with validated inputs and explicit failure responses | Explain tokenization/model assumptions; reproduce an error; distinguish illustrative examples from measured results |
| Application | [Application development](../102_AI-Application-Development/README.md): retrieval, structured output, memory | A retrieval system over a real, licensed corpus | Frozen corpus/splits, lexical baseline, per-query retrieval scores, citation review, empty/ambiguous-query behavior |
| Advanced evaluation | Retrieval and [evaluation protocol](../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md) | A controlled experiment comparing retrieval or model choices | Paired comparison, confidence intervals, contamination checks, error slices, judge calibration, cost-quality tradeoff |
| Advanced systems | [Agentic AI](../103_Agentic%20AI/README.md) and [LLMOps](../104_LLMOps/README.md) | A bounded workflow with persistent state and authenticated tools | End-state correctness, idempotency, cancellation, authorization tests, replayable traces, measured load behavior |
| Expert practice | Cross-team constraints, security, operations, governance | A release candidate plus an architecture decision record and incident exercise | Defend a simpler baseline, document residual risks, demonstrate rollback and data deletion, explain where evidence is insufficient |

Passing one project does not establish ten years of experience. Expert work is visible in the quality of decisions, measurement, debugging, and operational responsibility.

## Track A: Real-world dataset audit

Start with the [reproduced job-posting analysis](../research/README.md). The raw advertisements are real records; the structured skills and role types are LLM-derived annotations.

1. Reproduce the pinned September snapshot and the input fingerprint.
2. Inspect a stratified set of raw/structured pairs, recording supported, unsupported, and omitted claims. Sample different locations, role types, sparse descriptions, and duplicated text.
3. Keep a development sample separate from a final annotation audit. Record annotator disagreements and do not call an annotation pipeline accurate from examples used to tune it.
4. Compare exact-tag counting with a documented synonym taxonomy. Report every change in denominator and interpretation.
5. Write a data card explaining why this sample cannot estimate worldwide demand or salary premiums.

**Deliverables:** reproducible counts, claim-to-record references, annotation rubric, disagreement log, data-quality report, and limitations. Do not invent missing job advertisements or infer unstated salaries.

## Track B: Retrieval and grounded generation

Use [BEIR](https://github.com/beir-cellar/beir) to establish retrieval baselines; SciFact is a useful research task with evidence-linked claims. Original SciFact test labels are not public; do not confuse its claim-verification split with the BEIR retrieval conversion. Preserve each dataset's task definition and license.

1. Freeze the exact corpus, queries, relevance labels, and splits. Prevent document-family overlap from leaking evidence into a held-out experiment.
2. Evaluate lexical, dense, and hybrid retrieval separately. Tune on development queries. Choose reranking or fusion only when its measured benefit justifies latency and complexity.
3. Report Recall@k and nDCG@k with the official evaluator, per-query outputs and paired uncertainty. Distinguish unjudged documents from confirmed irrelevant documents.
4. Add answer generation after retrieval is understood. Evaluate citation support, answer correctness, abstention, and invalid citations separately.
5. Run authorization and cache-isolation tests on your implementation. Scientific retrieval benchmark scores say nothing about tenant security.

**Deliverables:** run files, dataset/model revisions, baseline comparison, ablations, failure taxonomy, calibration report, and a cost/latency breakdown. No universal score threshold qualifies a system for production.

## Track C: Software agents on real issues

Use [SWE-bench](https://github.com/SWE-bench/SWE-bench) for real repository issues. Follow its pinned harness and task definition; existing repository tests and benchmark tests determine success, not whether a model says the patch is correct.

Run untrusted code in an isolated worker without host credentials. Record image/task revisions, proposed patch, test logs, failed runs, timeouts, and token/compute budgets. Examine contamination risk and whether issue descriptions or patches were exposed during development. A resolved task must also preserve existing behavior under the required test suite.

**Deliverables:** task-level outcomes and logs, reproducible environment, sandbox policy, resource accounting, and analyses of unsuccessful patches. A benchmark success rate is not permission to merge automatically.

## Track D: Agent reliability and production operations

[τ³-bench](https://github.com/sierra-research/tau2-bench) can supplement testing with simulated customer-service tasks. Label simulated users and transactions explicitly. Its July 2026 grading change makes version pinning essential; do not compare incompatible banking results. For a real-world-only portfolio, use real consented workflow records and reviewed outcomes instead of claiming simulation is production evidence.

Evaluate workflow completion, incorrect or unauthorized side effects, repeated-run consistency, recovery after interrupted writes, and user-visible timeouts. Distinguish success in at least one attempt from reliable success across attempts. Read the selected benchmark's exact metric definition.

For an implementation, require:

- Server-derived identity and per-resource authorization at every read/write boundary.
- Idempotency keys and reconciliation for writes with ambiguous timeout outcomes.
- Step, token, time, and monetary limits enforced outside model text.
- Durable checkpoints, replay-safe recovery, and human approval where the application's policy requires it.
- Sensitive-data-aware traces with retention/deletion rules; prompts and tool outputs are not safe to log by default.
- Load tests with measured first-token and completion latency, concurrency, errors, and spending.
- Release gates calibrated to the actual workflow; canary criteria, rollback triggers, and an incident runbook.

## Expert review questions

Can you explain why a deterministic workflow was insufficient? Which failure does each component address? What measurement would make you remove it? What can your evaluation miss? Who can see a cached answer after permissions change? How do you prevent duplicate writes after a timeout? What evidence would disprove your launch decision?

Write an architecture decision record with context, alternatives, evidence, selected design, consequences, owner, and revisit trigger. Expert-level documentation makes uncertainty and tradeoffs inspectable; naming more frameworks does not replace that work.

The [evidence policy](../research/evidence-policy.md) and [dated source manifest](../research/sources.json) apply to every deliverable.
