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
