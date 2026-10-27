# Incident databases — the real-world failure record

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 27, 2026

Datasets tell you what attacks look like in the lab. Incident databases tell you what failures look like **in the world** — what actually happened, to whom, through which failure path. They are the closest thing AI security has to the NTSB accident record or the CVE feed, and they are the empirical grounding that turns [threat modeling](01-threat-modeling.md) from an imagination exercise into a literature review. All figures below were verified against the live sites on October 27, 2026.

## 1. The AI Incident Database (AIID)

The [AI Incident Database](https://incidentdatabase.ai/) — run by the Responsible AI Collaborative, an organization chartered specifically to advance it — is dedicated to indexing "the collective history of harms or near harms realized in the real world by the deployment of artificial intelligence systems." The design ancestry is explicit: like aviation and computer-security incident databases before it, it exists so the field can learn from experience rather than repeat it.

What makes AIID the reference record:

- **Incident, near-miss, and issue are separate classifications** — a realized harm, a harm that almost happened, and a systemic risk factor are different objects with different response semantics. This taxonomy alone is worth copying in any internal incident process.
- **Submissions are curated, not scraped.** Entries carry identifiers (recent IDs run into the 1780s), citations to primary reporting, and taxonomy tags. The database does not publish a single headline count on its homepage — the number that circulates most reliably is the one derived by the classifier project below.
- **It is the upstream source for downstream analyses** — most visibly the MIT tracker (next) and a large fraction of the incident case studies used in governance and research work.

The honest limitation: coverage is bounded by English-language media and submission volume, so geographic and sector skews are real. Treat AIID as the curated core of the record, not its full extent.

## 2. The MIT AI Risk Incident Tracker

The [AI Incident Tracker](https://airisk.mit.edu/ai-incident-tracker) at MIT (part of the AI Risk Initiative) is the machine-classified layer on top of AIID: it processes the raw AIID reports through an LLM pipeline (built with Arcola AI) and classifies **1,776 real-world incidents** — verified on the project page, October 27, 2026 — into structured, filterable form. It builds explicitly on the Responsible AI Collaborative's work as the underlying data source.

Why a classified layer matters:

- **Two taxonomies, joined.** Each incident is classified by the MIT Risk Repository taxonomy (risk causes) *and* CSET's AI Harm Taxonomy for severity — distinguishing harm types like physical harm, property damage, financial loss, and human-rights impacts. Cause and consequence on one record is what makes patterns queryable.
- **Seven domains**, covering discrimination & toxicity, privacy & security, misinformation, malicious actors, human-computer interaction, socioeconomic & environmental effects, and AI system safety, failures & limitations — the full failure surface, not just the security slice.
- **Coverage since 2016**, so trend questions ("is this failure class growing?") are answerable with a query instead of a literature search.

For a threat modeler, the practical move is: before writing your own attack tree, query this tracker for your domain and read the last two years of incidents. That is your empirical risk register.

## 3. MITRE ATLAS — the adversary playbook

[MITRE ATLAS](https://atlas.mitre.org/) (Adversarial Threat Landscape for Artificial-Intelligence Systems) is "a globally accessible, living knowledge base of adversary tactics and techniques involving AI, including attacks against AI-enabled systems, abuse or manipulation of AI capabilities, and harmful autonomous behavior materially enabled by AI" — based on empirical evidence from real-world attacks and realistic demonstrations from AI red teams and security groups. Current scale, verified on the live site October 27, 2026: **16 tactics, 208 techniques, 40 mitigations, and 73 case studies**, with © 2021–2026 dating its establishment.

ATLAS is the AI-specific sibling of MITRE ATT&CK, and some of its tactics and techniques are explicitly adapted from ATT&CK (marked as such on the site). The division of labor between the two is the important operational fact: ATT&CK covers the traditional infrastructure layer (hosts, networks, identity), while ATLAS covers the layers ATT&CK never modeled — training pipelines, model artifacts, inference APIs, the ML supply chain, and the model's own behavior. A real intrusion into an AI system typically crosses both, which is why an AI threat model that only maps ATT&CK controls and one that only maps ATLAS controls are both incomplete.

How to actually use it (this is where most teams stop too early):

1. **Coverage gap analysis.** ATLAS techniques are enumerated (AML.T-prefixed identifiers). List the techniques relevant to your stack, then map each to a control you actually have — a detection, a mitigation, an accepted-risk note. The unmapped remainder is your gap list, in priority order of consequence × reachability.
2. **Case studies as threat-model input.** The 73 documented cases (research demonstrations + real incidents) are pre-worked attack narratives: initial access → staging → execution. Reading the ones adjacent to your architecture is faster than inventing equivalents.
3. **Red-team scoping.** Each ATLAS technique is a testable objective; hand your red team the technique list for your stack and require the report to reference technique IDs, so findings roll up into the same coverage ledger.
4. **Detection engineering.** Several ATLAS techniques describe observable adversary behavior (reconnaissance via inference APIs, model-access probing). Where the technique is observable, the control is a detection; where it isn't, the control is architectural.

## 4. The OECD AI Incidents Monitor (AIM)

The [OECD's AIM](https://oecd.ai/en/incidents) is the worldwide media-monitoring layer: it documents negative outcomes of AI as reported in reputable international media, with data processing powered by Microsoft Azure using Event Registry data. Current scale, verified on the live site October 27, 2026: **about 18,579 incidents and hazards** — an order of magnitude beyond the curated databases, because the filter is different: breadth of coverage over depth of verification.

Two design choices distinguish it:

- **Incidents vs. hazards, separated.** AIM distinguishes *AI incidents* (realized harms) from *AI hazards* (potential risks) — the same incident/near-miss discipline as AIID, applied at media scale. When you quote an AIM number, say which of the two you mean; the mixture is not a comparable quantity.
- **Structured filtering across policy dimensions** — date, geography, industry, OECD AI principles (accountability, fairness, human wellbeing…), harm type, affected stakeholders, business function, AI task, and the AI system's autonomy level. The autonomy-level filter is the quietly radical one: it lets a policy analyst or a security team slice the record by *how much agency the system had* when the harm occurred — exactly the variable that [agent security](04-agent-mcp-security.md) worries about.

AIM's role in your process is horizon scanning: it will surface non-English-coverage incidents, sector patterns, and regulatory-relevant events that the curated databases miss; its per-entry depth is correspondingly thinner. Curated depth (AIID/MIT) for analysis, worldwide breadth (AIM) for detection.

## 5. NIST's ARIA program — evaluation infrastructure, not a database

Rounding out the institutional layer: [ARIA](https://ai-challenges.nist.gov/) (Assessing Risks and Impacts of AI), launched by NIST in May 2024, is best understood not as another incident list but as the research program building **how to evaluate AI risks sociotechnically at scale** — experimental evaluation of real systems in realistic contexts, feeding the [NIST AI RMF](06-responsible-ai.md) ecosystem with methods rather than anecdotes. Its companion Constructing an Open Risk Index (CORIX) work aims at structured risk indexes. For a practitioner, ARIA matters as the place where the assessment *methodology* your regulator will eventually reference is being worked out — worth a periodic check, not a daily one.

## 6. Operationalizing the record — the intelligence loop

These databases earn their keep when they close a loop with your own system. The minimum viable loop, in order:

1. **Subscribe.** AIM for breadth (filter to your industry and autonomy levels), AIID/MIT tracker for depth (filter to your domains), ATLAS for the technique feed. A monthly 30-minute review is enough cadence for most teams; security-critical deployments want it weekly.
2. **Triage against your architecture.** For each relevant incident, ask the one question that matters: *could our stack produce this failure?* If yes or unsure, it becomes a row in your risk register with the source citation attached.
3. **Map to ATLAS techniques.** Translate the incident narrative into technique identifiers, and check your coverage ledger from [threat modeling](01-threat-modeling.md). Incidents reveal which techniques are *actually being used* — that is your prioritization signal for closing gaps.
4. **Feed the red team.** New incident patterns become new attack objectives — each one either a confirmed-vulnerable case (fix + [regression test](03-red-teaming.md)) or a documented control pass. The [Claude Code espionage campaign](04-agent-mcp-security.md) is the worked example: a novel incident class that every agent team should have converted into tests within a release cycle.
5. **Write it into the governance record.** The [responsible-AI documentation set](06-responsible-ai.md) should reference the incident record you reviewed and when — "we checked the world's failure record as of this date" is a strong sentence in any audit, and a defensible one.

One discipline note: incident counts are *reporting rates*, not harm rates. Coverage skews toward English-language media, high-visibility sectors, and harms that photograph well. The numbers are for direction and trend, not denominators — the same epistemic honesty the [evidence policy](../research/evidence-policy.md) demands elsewhere in this repository.

## References

- [AI Incident Database](https://incidentdatabase.ai/) — Responsible AI Collaborative; the curated core record
- [MIT AI Risk Incident Tracker](https://airisk.mit.edu/ai-incident-tracker) — 1,776 classified AIID incidents; MIT Risk Repository + CSET harm taxonomies; verified October 27, 2026
- [MITRE ATLAS](https://atlas.mitre.org/) — 16 tactics / 208 techniques / 40 mitigations / 73 case studies; verified October 27, 2026
- [OECD AI Incidents Monitor (AIM)](https://oecd.ai/en/incidents) — ~18,579 incidents & hazards; Azure + Event Registry; verified October 27, 2026
- [NIST ARIA](https://ai-challenges.nist.gov/) — Assessing Risks and Impacts of AI program (launched May 2024)
- Cross-cutting: [threat modeling](01-threat-modeling.md) (where the record feeds in) · [red teaming](03-red-teaming.md) (where incidents become tests) · [security & safety datasets](07-security-safety-datasets.md) (the lab-side counterpart) · [AI-Safety repository's incident reviews](https://github.com/AdilShamim8/AI-Safety) (14 worked incident analyses in its research notes)

Previous: [Security & safety datasets](07-security-safety-datasets.md) · [Back to section home](README.md)
