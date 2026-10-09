# AI engineering responsibilities

Reviewed October 9, 2026. This is an engineering ownership guide, not a ranking by job-posting frequency. Earlier responsibility totals and frequency tables had no reproducible local source and have been removed. The [job dataset](../research/README.md) includes derived responsibility annotations, but those fields have not been independently validated here.

## From prototypes to owned systems

| Responsibility | What the engineer does | Reviewable deliverable |
|---|---|---|
| Problem definition | Identify users, decisions, failure consequences, and whether a deterministic solution is sufficient | Requirements, baseline, acceptance criteria and non-goals |
| Data preparation | Obtain authorized data, track provenance, validate schema and freshness, handle duplicates | Data card, lineage, validation report, deletion/refresh procedure |
| Model integration | Select models through workflow evaluations; validate outputs and handle refusals and failures | Versioned configuration, regression results, fallback behavior |
| Retrieval | Build ingestion and indexing; compare lexical/dense approaches and measure relevance | Frozen corpus, relevance labels, per-query retrieval results |
| Evaluation | Define correctness, review labels, isolate test data and measure uncertainty | Reproducible evaluation protocol, error slices, release criteria |
| Tool workflows | Authenticate callers, authorize actions, constrain arguments and enforce budgets | Tool contracts, permission tests, durable execution records |
| Reliability | Manage timeouts, retries, partial failures, provider outages and overload | Load-test results, idempotency policy, recovery and rollback drill |
| Observability | Capture useful traces with controlled sensitive-data exposure | Trace schema, retention/access controls, actionable alerts |
| Performance and cost | Measure first-token/completion latency and cost per successful task | Workload definition, latency distributions, cost-quality experiments |
| Security and governance | Review threats, data access, retention, secrets and applicable obligations | Threat model, access/deletion tests and documented escalation owners |
| Collaboration | Explain uncertainty and tradeoffs to product, domain, security and operations teams | Architecture decision records and release review |

## Own boundaries, not only model prompts

For retrieval systems, identity and document access rules must come from trusted application state. Authorization belongs at retrieval and cache boundaries. Similarity is not permission; filtering prompts cannot enforce access control.

For write-capable agents, a timeout can mean the tool failed or that the tool completed and the response was lost. Use idempotency keys, durable state and reconciliation before retrying. Test unauthorized calls, duplicate requests, interruption and rollback. A fluent explanation of a plan is not evidence that its side effects were correct.

For evaluation, distinguish answer correctness, citation support, task completion, policy compliance and user impact. A response can be well grounded in stale or incorrect source material. A successful task can still have caused an unauthorized side effect. Evaluate these dimensions separately.

## Seniority through scope and evidence

| Scope | Expected evidence |
|---|---|
| A component | Correct behavior under documented inputs, useful tests, readable implementation and diagnosed failures |
| A workflow | Integration behavior, dataset quality, measurable acceptance criteria, cost and latency accounting |
| A production service | Authorization, reliable writes, monitoring, load behavior, release gates and recovery ownership |
| A shared platform or cross-team system | Architecture alternatives, stable contracts, migration plans, governance, incident learning and operational accountability |

This is a learning rubric, not a universal leveling policy or an estimate of years of experience. Employers define scope differently.

## When deeper specialization is justified

Fine-tuning needs a measured limitation of prompting/retrieval, a licensed training corpus, held-out evaluation, and a lifecycle plan. Self-hosting needs hardware and capacity measurements, an operational owner and a complete cost model. Multi-agent coordination needs a demonstrated advantage over a single bounded workflow, plus explicit shared-state and failure semantics.

Before adding complexity, record what would falsify the expected benefit. After the experiment, report improvements and regressions under the same evaluation protocol. Preserve useful baselines and failed runs.

Use the [advanced path](../learning-paths/advanced-engineering.md) for projects, and the [evidence policy](../research/evidence-policy.md) for results and claims.
