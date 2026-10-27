# 106 — AI Security & Safety

*Securing AI systems against adversarial inputs, unsafe actions, and misuse — and aligning them with human intent in the first place.*

> Reviewed October 27, 2026. Every reference in this section was checked on that date (incident-database figures — ATLAS, MIT tracker, OECD AIM — verified against the live sites; dataset facts checked against the [AI-Safety repository's](https://github.com/AdilShamim8/AI-Safety) verified catalog of 43 dataset cards). Like [105 — AI Evaluation](../105_AI-Evaluation/README.md), this is a **knowledge base**: concepts, research, tooling, and documented incidents, cross-linked to the deeper curriculum notes in 101–104.

---

## Why this section exists

The [full roadmap](../roadmap/full-roadmap/level-08-ai-security.md) rates AI security at 7/10 for on-the-job importance with a blunt justification: *"Prompt injection and data leaks are real risks in any system that uses tools or private data. One incident can be very costly."* Between when that roadmap was written and this review, the field accumulated evidence for exactly how costly:

- **November 2025** — Anthropic disclosed and disrupted [the first reported AI-orchestrated cyber-espionage campaign](https://www.anthropic.com/news/disrupting-AI-espionage): a state-sponsored group jailbroke Claude Code into an attack framework targeting ~30 organizations, executing reconnaissance and intrusion at machine speed. The first documented large-scale cyberattack run largely without human intervention.
- **April–May 2026** — OX Security disclosed a command-execution flaw embedded in the *default STDIO transport of the official MCP SDKs*, exposing an estimated 200,000 instances across a supply chain of 150M+ package downloads ([Cloud Security Alliance analysis](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled)). Not a bug in one product — a design default propagated by the reference implementation.
- **December 2025** — OWASP published the first [Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026), a peer-reviewed catalog of risk categories (goal hijack, tool misuse, memory poisoning, cascading failures) that did not exist when most security checklists were written.

Meanwhile the safety side of the field — alignment techniques, responsible deployment, and governance — moved from research topic to compliance obligation, with the EU AI Act's general application date passing in August 2026 and NIST's Generative AI Profile in active industrial use.

This section gives both halves — **security** (defending against adversaries) and **safety** (making the system itself behave as intended) — a dedicated home, because they share machinery: evaluation under adversarial conditions, red teaming, and measurement instead of assurances.

## What is in this section

| # | Note | What it covers | Start here if… |
|---|---|---|---|
| 1 | [Threat modeling](01-threat-modeling.md) | The AI attack surface, trust boundaries, OWASP LLM Top 10 + Agentic ASI Top 10, MITRE ATLAS coverage mapping | you are designing a new AI system |
| 2 | [Prompt injection defense](02-prompt-injection-defense.md) | The unsolved problem, layered defenses, research frontier (CaMeL, spotlighting) | you build anything that touches untrusted content |
| 3 | [Red teaming](03-red-teaming.md) | Methodology, tools (PyRIT, garak, promptfoo), the attack-corpora layers, converting findings to regression tests | you need to test before an adversary does |
| 4 | [Agent & MCP security](04-agent-mcp-security.md) | Tool poisoning, rug pulls, the STDIO flaw, the Claude Code espionage case, least privilege + benchmark validation | you build agents or connect tools |
| 5 | [AI alignment](05-ai-alignment.md) | RLHF, DPO, Constitutional AI, RLAIF, the preference datasets behind them — and reward hacking in the wild | you want to understand why models misbehave and how labs shape them |
| 6 | [Responsible AI & governance](06-responsible-ai.md) | NIST AI RMF, EU AI Act (post-2026 Omnibus), model cards, incident response + external monitoring | you ship to regulated users or the EU |
| 7 | [Security & safety datasets](07-security-safety-datasets.md) | The public testing corpus: jailbreak benchmarks, agent-security suites, preference data, real-world distributions, bias instruments — sizes, licenses, provenance | you need to know what to test on |
| 8 | [Incident databases](08-incident-databases.md) | The real-world failure record: AIID, MIT's classified tracker, MITRE ATLAS, OECD AIM, NIST ARIA — and the intelligence loop | you want empirical grounding for threat models and governance |

## How this connects to the rest of the repository

- **[Full roadmap Level 8 — AI Security](../roadmap/full-roadmap/level-08-ai-security.md)** is the session-by-session learning path; this section is the reference material beneath it.
- **[104 — LLMOps / Safety & Guardrails](../104_LLMOps/README.md)** owns the *implementation* curriculum: input safety, output filtering, tool safety, [prompt injection & jailbreak defense](../104_LLMOps/4.%20Safety%20%26%20Guardrails/4.%20Prompt%20Injection%20%26%20Jailbreak%20Defense.md), and human-in-the-loop safeguards. This section adds the research context, the incident record, and the adversarial-testing methodology around those notes.
- **[101 — LLM Literacy](../101_LLM-Literacy/README.md)** covers [security in prompting](../101_LLM-Literacy/02-Prompt%20Engineering/7.%20Security%20%26%20Safety%20in%20Prompting.md) at the practitioner level and [model limitations](../101_LLM-Literacy/01-LLM%20101/8.%20Limitations%20%26%20Failure%20Modes.md) including reward hacking.
- **[103 — Agentic AI](../103_Agentic%20AI/README.md)** covers agent architectures and [human-in-the-loop production safety](../103_Agentic%20AI/04-Multi-Agent%20Orchestration/2.%20Human-in-the-Loop%20%26%20Production%20Safety.md); note 4 here covers securing what those architectures connect to.
- **[105 — AI Evaluation](../105_AI-Evaluation/README.md)** — red teaming *is* evaluation with an adversary; the [benchmark integrity crisis](../105_AI-Evaluation/03-agent-benchmarks.md) is the alignment story (note 5) told through measurements. For the hands-on version, the [LLM Evaluations course lecture 16](../105_AI-Evaluation/course/16-rag-security-toxicity-leakage-scope-drift.md) builds the safety eval suite end-to-end: attack-surface analysis → safety policy → toxicity/leakage/scope-drift evals with DeepEval.
- **[Governance curriculum](../104_LLMOps/README.md)** in 104/5 pairs with note 6 here: 104 covers the operational controls, note 6 covers the regulatory frameworks they satisfy.
- **[The AI-Safety repository](https://github.com/AdilShamim8/AI-Safety)** (sister repository) is the deep curriculum behind notes 7–8: 24 chapters, 10 runnable projects, 43 verified dataset cards with a machine-readable catalog, 251 registered sources, and worked incident reviews — the evidence ladder this section's claims are checked against.

## The three ideas that organize everything here

1. **The model is not a security boundary.** Anything the model reads — retrieved documents, web pages, tool outputs, file contents — is untrusted input; anything it emits is untrusted output until validated. Defenses that rely on the model *itself* resisting manipulation (instructions like "ignore malicious instructions") are prompt-shaped hopes, not controls. Real controls live outside the model: authorization, sandboxing, validation, human approval.
2. **Capability cuts both ways.** The same autonomy that makes agents useful (plan → act → observe → adapt) is what made the November 2025 espionage campaign possible. Every capability you add to an agent is attack surface you must defend; least privilege is the discipline that keeps the two in balance.
3. **Safety is measured, not declared.** Alignment techniques (note 5) reduce misbehavior probabilistically; red teaming (note 3) quantifies what remains; governance (note 6) makes the residual risk explicit and owned. The [evidence policy](../research/evidence-policy.md) applies to safety claims the same way it applies to benchmark claims: a vendor's assurance is not a measurement.
