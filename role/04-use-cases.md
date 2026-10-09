# AI engineering use cases and measurable outcomes

Reviewed October 9, 2026. This catalog describes application patterns; it is not a frequency ranking. Earlier use-case totals and percentages lacked reproducible supporting records and have been removed. The real-job dataset's use-case fields are LLM-derived and were not independently validated in this review.

## Connect the application to evidence

| Use case | Data required | Useful measures | Failure cases to inspect |
|---|---|---|---|
| Enterprise knowledge retrieval | Authorized documents, versions, access rules, reviewed relevance queries | Retrieval recall/ranking, supported citations, answer correctness, abstention | Missing evidence, stale policies, cross-tenant retrieval or cache leaks |
| Customer support | Approved policies and de-identified, consented interaction records | Correct resolution, policy adherence, escalation quality, user effort | Incorrect refunds, invented policy, duplicate writes, unresolved requests marked complete |
| Document extraction | Licensed documents and reviewed field/span annotations | Per-field correctness, invalid outputs, review burden and coverage | OCR errors, units/currency mismatch, missing fields, unsupported inferred values |
| Workflow automation | Explicit tool contracts, authorized workflow history and reviewed outcomes | End-state correctness, side-effect correctness, retries and recovery | Ambiguous timeouts, repeated transactions, unsupported tool arguments |
| Software assistance | Real repository issues, tests, expected behavior and isolated execution | Required tests passed, regressions, task resolution, review burden | Plausible patches that fail tests, credential exposure, unsafe code execution |
| Summarization and reporting | Versioned source documents and expert-reviewed key claims | Factual support, omission of material facts, citation correctness | Fabricated claims, lost qualifiers, outdated or contradictory evidence |
| Search and recommendations | Authorized interaction records, item metadata and appropriate relevance labels | Task-specific relevance and measured user outcomes | Feedback loops, cold-start errors, privacy issues, popularity bias |
| Voice and multimodal interaction | Licensed audio/images, consented recordings and reviewed task labels | Task outcome, recognition errors, interruption recovery, time to audible response | Bad endpointing, accent/language slices, stale tool state, delayed cancellation |
| Evaluation and monitoring | Frozen test sets, reviewed failures and access-controlled traces | Regressions, calibration, drift by slice, incident detection | Judge disagreement, contaminated tests, noisy alerts, sensitive data in logs |

These metrics are recommendations. Set thresholds from workflow requirements and empirical calibration; do not reuse example percentages as universal release standards.

## Use real datasets for the right question

- [The pinned job-posting corpus](../research/README.md) provides real advertisements for a data-quality and annotation-audit project. It does not supply product outcome labels.
- [BEIR](https://github.com/beir-cellar/beir) provides retrieval tasks. Its SciFact conversion supports retrieval experiments, while original SciFact supports scientific claim verification under its own split definitions.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) provides real GitHub issues and a software evaluation harness. Tests must run in an isolated environment.
- [MTEB / MMTEB](https://github.com/embeddings-benchmark/mteb) organizes embedding tasks. Inspect each task's dataset origin, split and license rather than treating the collection as a single uniform dataset.
- [τ³-bench](https://github.com/sierra-research/tau2-bench) uses simulated customer-service environments. It is useful supplemental testing, not a corpus of real customer transactions.

Public benchmarks help establish baselines. Product claims require measurements on the product's actual authorized workflow. Keep raw observations, derived labels and synthetic examples separate.

## Expert-level project review

Define the user's decision and the cost of a wrong answer or action before choosing a model. Record a deterministic or simpler baseline, dataset rights, sampling/labeling process, development/test separation, uncertainty and failure slices. Explain the permissions boundary, deletion behavior, operational budget and recovery plan.

The final artifact should include data provenance, an executable experiment, per-item results, failures and an architecture decision record. An attractive interface or a list of frameworks is insufficient evidence that the use case works.

See [responsibilities](03-responsibilities.md), [the advanced path](../learning-paths/advanced-engineering.md), and [the source manifest](../research/sources.json).
