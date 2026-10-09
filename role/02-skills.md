# AI engineering skills: evidence and practice

Reviewed October 9, 2026. Latest source observation: September 23, 2026. This page replaces incompatible legacy denominators with a reproducible snapshot and separates measured annotations from recommendations.

## What the dataset measures

The [pinned upstream dataset](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c/job-market) contains raw job advertisements and LLM-enriched records. Our [executed analysis](../research/job-market-summary.json) counts 8,051 observations across nine scrape folders. The latest folder contains 1,086 records and 651 distinct company names as stored.

This is a single job-board convenience sample. It is not a representative sample of worldwide vacancies. Scrape dates are not posting dates; advertisements are not hires. Role types and skill tags below are the upstream model's annotations, not independently verified labels. [Reproduction instructions and limitations](../research/README.md) describe the measurement.

### Latest extracted role labels

| Stored label | Records | Interpretation of the annotation |
|---|---:|---|
| `ai-first` | 777 | Work shaping AI-powered application behavior |
| `ai-support` | 256 | Platforms, integration, and infrastructure supporting AI |
| `ml-first` | 43 | Model-oriented ML work under the upstream taxonomy |
| `unknown` | 10 | Keep uncertainty visible; do not force a label |
| **Total** | **1,086** | All latest-scrape records are retained |

Titles overlap. Use actual responsibilities and a written classification rule rather than claiming that all AI engineers integrate models while all ML engineers train them.

### Selected exact skill tags

These are tag occurrences counted once per record across categories. The denominator is **1,086 latest-scrape records**, including unknown role labels. Tags overlap, so percentages do not sum to 100%. Synonyms are not merged; a percentage is not the share of the worldwide market requiring that skill.

| Exact extracted tag | Records | Share of latest records |
|---|---:|---:|
| Python | 769 | 70.81% |
| RAG | 492 | 45.30% |
| Agentic Workflows | 450 | 41.44% |
| AWS | 440 | 40.52% |
| CI/CD | 415 | 38.21% |
| Prompt Engineering | 393 | 36.19% |
| Azure | 363 | 33.43% |
| GCP | 302 | 27.81% |
| LLM Evaluation | 282 | 25.97% |
| Docker | 269 | 24.77% |
| SQL | 241 | 22.19% |
| TypeScript | 212 | 19.52% |
| Observability | 202 | 18.60% |

Broad labels such as `LLMs` are present in the full output but omitted from this selected table because they are less specific learning objectives. Different wording in an advertisement, annotation mistakes, and omission of familiar skills can all change a tag count. Do not interpret absence as proof a skill is unnecessary.

The latest raw records all contain URLs and descriptions. Normalizing whitespace and case finds 22 identical-description groups covering 50 records. These are retained and disclosed, not silently deduplicated. The latest annotations report model `glm-5.2` and prompt hash `ef6fdeb19af2` for all 1,086 records. These identifiers describe provenance; they do not establish extraction accuracy.

The upstream [extraction evaluation](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) documents unsupported skills, ambiguous classifications, and unreliable company-stage/management fields. It does not validate every responsibility or use-case annotation. We therefore omit company-stage prevalence, global geography estimates, and causal hiring-growth claims.

## Competencies beyond framework names

The following is a recommended engineering rubric, not a measured frequency table.

| Competency | Foundation | Advanced evidence |
|---|---|---|
| Software engineering | APIs, data modeling, version control, input validation | Reproducible builds, concurrency control, integration tests, cancellation and idempotency |
| Model literacy | Tokens, representations, training/inference, limitations | Task-specific model selection, context budgeting, calibration, model/version migration experiments |
| Retrieval | Corpus ingestion, lexical and vector retrieval | Baselines, relevance judgments, held-out evaluation, retrieval ablations, deletion and authorization tests |
| Evaluation | Define expected behavior and inspect errors | Frozen splits, paired comparisons, uncertainty, human/judge calibration, slice analysis, contamination review |
| Agents | Explicit tools and bounded workflows | End-state verification, durable recovery, least privilege, ambiguous-write reconciliation, repeated-trial reliability |
| Operations | Deployment, monitoring, cost accounting | Load-tested SLOs, error budgets, canaries, rollback, provider failure drills, measured cost per successful task |
| Data governance | Data provenance, privacy and access controls | Retention/deletion evidence, trace access policy, lineage, dataset rights and approved-use review |
| Communication | Explain the implementation | Defend alternatives with evidence, write architecture decisions, report unresolved risks and failed experiments |

## Choose tools through experiments

Begin with the simplest implementation that meets the workflow: a deterministic program, a direct model call, or a bounded sequence may be enough. Add retrieval, reranking, agents, model routing, fine-tuning, or self-hosting to address a diagnosed problem. Record the baseline, the expected benefit, the result, and the operational cost.

Choose one implementation stack to learn deeply. Tool selection depends on team skills, integration needs, data residency, licensing, latency and cost. No framework ranking in this page establishes a universally correct stack.

Use the [advanced learning path](../learning-paths/advanced-engineering.md) to turn these competencies into inspectable artifacts. Follow the [evidence policy](../research/evidence-policy.md) before quoting market percentages or benchmark improvements.
