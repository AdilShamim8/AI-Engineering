# Responsible AI & governance

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 27, 2026
>
> The [governance curriculum in 104](../104_LLMOps/README.md) covers the operational controls — data governance, access management, model & prompt governance, auditability. This note covers the frameworks those controls answer to: the risk-management standards and the regulation timeline, plus the documentation artifacts (model cards, incident records) that make a deployment reviewable.

## The three-layer stack

1. **Voluntary frameworks** — NIST AI RMF, ISO/IEC 42001: how organizations structure AI risk management regardless of jurisdiction.
2. **Binding regulation** — the EU AI Act (the world's first comprehensive AI law, in phased application since 2024) plus sectoral and national laws (GDPR for data, India's DPDP, US state laws).
3. **Engineering artifacts** — model cards, system cards, eval reports, incident logs: the evidence layer that both of the above ultimately demand.

An AI engineer mostly lives in layer 3, but must read layer 1 fluently (it is how "responsible AI" becomes requirements) and know layer 2's timeline (it sets hard deadlines).

## NIST AI Risk Management Framework

The [AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) (NIST AI 100-1, January 2023) is the dominant voluntary framework — free, sector-agnostic, and structured around four functions you can map directly onto this repository's curriculum:

| Function | What it asks | Where this repo covers it |
|---|---|---|
| **Govern** | Policies, accountability, roles, risk tolerance | [Governance curriculum (104/5)](../104_LLMOps/README.md) |
| **Map** | Context, intended use, affected parties, risks | [Threat modeling](01-threat-modeling.md) · [use cases](../role/04-use-cases.md) |
| **Measure** | Quantified characteristics, evaluation, monitoring | [105 — AI Evaluation](../105_AI-Evaluation/README.md) |
| **Manage** | Prioritized response, mitigation, residual-risk acceptance | [Red teaming → fixes](03-red-teaming.md) · [safety controls](02-prompt-injection-defense.md) |

For generative AI specifically, the [Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) (NIST AI 600-1, July 2024) enumerates 12 risk categories (including hallucination, information integrity, harmful bias, data privacy) and maps actions to them — it is the most direct "checklist" a builder can adopt. NIST is revising AI RMF 1.0 under the White House AI Action Plan and released a [Critical Infrastructure Profile concept note](https://www.nist.gov/itl/ai-risk-management-framework) in April 2026 — track, but don't wait for, the revision.

ISO/IEC 42001 (AI management systems, 2023) plays the same role for organizations that CERT/ISO 27001 plays for security management: the certifiable structure around policies and controls. If your company sells AI into enterprises, you will meet it in procurement.

## The EU AI Act: the timeline that matters

Regulation (EU) 2024/1689, in phased application — with a major amendment ("AI Omnibus", Regulation (EU) 2026/1744, in force July 27, 2026) that **delayed and restructured the high-risk schedule**. Current state, per the [official implementation timeline](https://artificialintelligenceact.eu/implementation-timeline/):

| Date | What applies |
|---|---|
| Feb 2, 2025 | **Prohibited practices** (8 banned uses: manipulative deception, social scoring, emotion recognition in workplaces/education, untargeted facial-recognition scraping, …) + AI-literacy duties |
| Aug 2, 2025 | **GPAI obligations** — training-data summaries, copyright policy, systemic-risk models' evaluation & incident reporting (the GPT-class layer) |
| Aug 2, 2026 | **General application** — Article 50 transparency (disclose AI interaction, mark synthetic content), governance & enforcement machinery |
| Dec 2, 2026 | Two further prohibitions (non-consensual intimate imagery, CSAM generation) + synthetic-marking deadline for **existing** generative systems |
| Dec 2, 2027 | **Annex III high-risk obligations** (employment, education, essential services, biometrics — the CV-screening, credit-scoring, exam-grading categories) |
| Aug 2, 2028 | High-risk requirements for AI **embedded in regulated products** (machinery, toys, medical devices) |

Practical readings for engineers (not legal advice):

- **"High-risk" is about use, not model size.** An LLM in a hiring workflow is high-risk; the same model in a code editor is not. The Act's risk tiers (unacceptable / high / limited-transparency / minimal) map to *what you deploy it for*.
- **GPAI obligations sit with model providers**, but they flow down to deployers via documentation: expect model cards, training-data summaries, and system-risk evaluations from your providers, and expect to *pass them through* in enterprise procurement.
- **Transparency duties are already live**: disclosing AI interaction and machine-readable synthetic-content marking (Aug 2026) apply to systems in market now.
- The [AI Act portal](https://artificialintelligenceact.eu/) maintains the regulation text, timeline, and guidance in one place; the [European Commission's AI Act page](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) is the primary source.

## Documentation artifacts: what "reviewable" means

The artifacts that frameworks and regulation converge on, all of which this repository's practices already produce:

- **Model card / system card** — intended use, training/eval data provenance, benchmark results with conditions, known limitations, safety evaluations. The discipline is the [evidence policy](../research/evidence-policy.md)'s: state what a result does *not* establish. (Provider cards: OpenAI's model docs, Google's model cards, Anthropic's system cards; the format originates with Mitchell et al., *Model Cards for Model Reporting*, 2019 — [arXiv:1810.03993](https://arxiv.org/abs/1810.03993).)
- **Eval reports** — from your [CI suite](../105_AI-Evaluation/05-eval-engineering.md): datasets, metrics, thresholds, per-slice results, decision log.
- **Red-team reports** — attack families tested, success rates, mitigations, residual risk ([method](03-red-teaming.md)).
- **Incident records** — what happened, detection time, blast radius, remediation, and the regression tests added. For external accountability: the [AI Incident Database](https://incidentdatabase.ai/) aggregates publicly reported AI harms; contribution is voluntary but the record format is instructive.
- **Human-oversight design** — who can override, pause, or roll back; where approval gates sit ([HITL curriculum](../103_Agentic%20AI/04-Multi-Agent%20Orchestration/2.%20Human-in-the-Loop%20%26%20Production%20Safety.md)).

## Deploying responsibly: the minimum viable set

For a team shipping an LLM application without a compliance department, this is the honest minimum:

1. **Write down intended use and out-of-scope uses** (one page; it anchors everything else).
2. **Run the NIST GenAI Profile's 12 risks as a design review** — for each: does it apply, what's the control, where's the evidence?
3. **Maintain the eval + red-team evidence loop** ([105](../105_AI-Evaluation/README.md) + [note 3](03-red-teaming.md)) — governance without measurement is paperwork.
4. **Classify your deployment against the EU tiers** if you have any EU exposure; high-risk uses trigger obligations *before* the 2027 dates in procurement practice, not after.
5. **Keep the audit trail**: versions, prompts, evals, incidents, decisions. [Auditability](../104_LLMOps/README.md) is the control that makes every other control verifiable after the fact.
6. **Have an incident plan**: detection (canaries, monitoring), containment (kill switch, rollback), disclosure path (who decides, in what timeframe). The [Air Canada case](../105_AI-Evaluation/01-evaluation-fundamentals.md) is what the absence of this looks like in a tribunal record.
7. **Watch the world's incident record** — the [incident databases](08-incident-databases.md) are the governance instrument most teams ignore: the [AI Incident Database](https://incidentdatabase.ai/) for curated precedent, MIT's classified tracker (1,776 real-world incidents) for pattern queries, and the [OECD AIM](https://oecd.ai/en/incidents) monitor (~18,579 incidents & hazards) for worldwide horizon scanning — all free, all citable in a risk register. A governance record that says "we reviewed the external failure record as of this date" is materially stronger than one that only cites internal testing, and EU-style serious-incident reporting duties are easiest to satisfy when the external monitoring loop already exists.

## References

- [NIST AI RMF 1.0](https://www.nist.gov/itl/ai-risk-management-framework) (NIST AI 100-1) · [Generative AI Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) (NIST AI 600-1) — both free
- [EU AI Act portal — implementation timeline](https://artificialintelligenceact.eu/implementation-timeline/) · [European Commission — AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)
- Mitchell et al., *Model Cards for Model Reporting* — [arXiv:1810.03993](https://arxiv.org/abs/1810.03993)
- [AI Incident Database](https://incidentdatabase.ai/)
- [Governance curriculum (104/5)](../104_LLMOps/README.md) — operational controls: data governance, access, compliance, auditability
- [Roadmap Level 8, module M8.8](../roadmap/full-roadmap/level-08-ai-security.md) — the syllabus entry for this topic

Previous: [AI alignment](05-ai-alignment.md) · Next: [Security & safety datasets](07-security-safety-datasets.md)

<!-- nav-footer -->
---

**Navigate:** [← 05. AI Alignment](05-ai-alignment.md) · [Section hub](README.md) · [07. Security Safety Datasets →](07-security-safety-datasets.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
