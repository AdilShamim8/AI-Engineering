# Threat modeling for AI systems

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 17, 2026

Threat modeling is the exercise of enumerating *what can attack what* before adding defenses. For AI systems it starts from one structural observation: **the LLM sits between untrusted inputs and privileged actions**, which is a position no conventional component occupies.

## How the attack surface changes

A classical web application validates untrusted input against typed schemas before it touches anything privileged. An LLM application inverts this: the model *reads natural language from everywhere* — user prompts, retrieved documents, web pages fetched by tools, emails summarized, file contents, tool outputs and error messages — and then *decides* what to do next. Three properties follow:

1. **Every text channel is an instruction channel.** The model does not syntactically distinguish "data to summarize" from "instructions to follow." This is the root cause of [indirect prompt injection](02-prompt-injection-defense.md).
2. **The model's output can drive privileged actions.** If outputs are connected to tools (write files, send email, execute SQL, call APIs), then whoever can influence the output influences the action.
3. **Probabilistic components fail probabilistically.** The same attack fails and succeeds across retries; defenses need to hold across distributions, not single instances — which is why [red teaming](03-red-teaming.md) reports rates, not binary verdicts.

## Trust boundaries: the checklist

Walk your architecture and mark every place data crosses a boundary. The canonical set for an LLM application:

| Boundary | What crosses | Question to ask |
|---|---|---|
| User → system | Free-text prompts | Is the user authenticated and authorized for *this* action, or just *a* action? |
| Corpus → retriever → model | Documents (possibly attacker-writable) | Who can write to the index? Is retrieved content treated as data, never instructions? |
| Web/tool → model | Fetched pages, tool outputs, error strings | Could a third party control any byte of this content? |
| Model → tools | Generated tool calls, arguments | Are calls validated, permission-checked, rate-limited *outside* the model? |
| Model → user | Generated content | Is it scanned for sensitive-data leakage before display? |
| System → logs/traces | Prompts, outputs, retrieved context | What sensitive data is being persisted, and who can read the logs? |
| Provider ↔ system | Everything, over the wire | What are the retention, training-use, and tenancy terms of the model API? |

The two most-forgotten boundaries in practice are **retrieved documents** (teams sanitize user input but index third-party content unread) and **logs** (prompts containing PII are stored forever with weak access control). The [governance note](06-responsible-ai.md) and the [data-governance curriculum](../104_LLMOps/README.md) cover the compliance side of both.

## The OWASP Top 10 for LLM Applications

The community-standard risk catalog, maintained by the [OWASP GenAI Security Project](https://owasp.org/www-project-top-10-for-large-language-model-applications/). The current edition (the 2025 list, still the operative version as of this review; see [the project's Top 10 page](https://genai.owasp.org/llm-top-10/)) leads with:

1. **LLM01: Prompt Injection** — instructions in input (direct) or in content the model reads (indirect) that override intended behavior. The #1 risk, and the one [note 2](02-prompt-injection-defense.md) is entirely about.
2. **LLM02: Sensitive Information Disclosure** — the model revealing PII, credentials, or proprietary data via outputs or logs.
3. **LLM03: Supply Chain Vulnerabilities** — poisoned models, plugins, and dependencies; includes the MCP supply-chain issues of [note 4](04-agent-mcp-security.md).
4. **LLM04: Data and Model Poisoning** — training- or index-time tampering that changes behavior at inference.
5. **LLM05: Improper Output Handling** — passing model output to downstream systems without validation (XSS, command injection, SSRF via generated URLs).
6. **LLM06: Excessive Agency** — more permissions, tools, or autonomy than the task requires.
7. **LLM07: System Prompt Leakage** — exposure of instructions (which themselves may contain secrets or logic worth attacking).
8. **LLM08: Vector and Embedding Weaknesses** — retrieval-layer issues: cross-tenant leakage, poisoned embeddings, authorization gaps at query time.
9. **LLM09: Misinformation** — hallucinated but confidently delivered content causing real-world harm (the [Air Canada case](../105_AI-Evaluation/01-evaluation-fundamentals.md) is the canonical incident).
10. **LLM10: Unbounded Consumption** — cost and DoS exposure from uncontrolled inference spend.

The list is a *checklist for design reviews*, not a difficulty ranking: LLM01 is unsolved (see note 2) while LLM05 and LLM06 are fully within your control today.

## The OWASP Top 10 for Agentic Applications (2026)

Agents add a second catalog because they add failure classes that have no chatbot analogue. Published December 2025 ([announcement](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/), [resource page](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)), with risk IDs ASI01–ASI10:

| ID | Risk | One-line summary |
|---|---|---|
| ASI01 | Agent Goal Hijack | Injection (often indirect) redirects the agent's objective |
| ASI02 | Tool Misuse & Exploitation | Unsafe tool composition, recursion, budget exhaustion |
| ASI03 | Agent Identity & Privilege Abuse | Weak or borrowed identity; no per-action authorization |
| ASI04 | Agentic Supply Chain Compromise | Malicious MCP servers, poisoned tools/models — note 4's core topic |
| ASI05 | Unexpected Code Execution | Generated or fetched code running without sandboxing |
| ASI06 | Memory & Context Poisoning | Persistent memory as a long-lived injection channel |
| ASI07 | Insecure Inter-Agent Communication | Multi-agent traffic without authentication/integrity |
| ASI08 | Cascading Agent Failures | One agent's error propagating through the topology |
| ASI09 | Human-Agent Trust Exploitation | Approval fatigue, UI that hides what was actually approved |
| ASI10 | Rogue Agents | Agents pursuing unintended emergent goals, incl. shutdown resistance |

Read ASI09 next to the [MCP client research](04-agent-mcp-security.md): several 2025–26 attacks worked *because* approval UIs summarized away the malicious parameters the user was approving.

## Threat-modeling procedure that works for AI systems

1. **Draw the data flow diagram** including the model, retrieval store, tools, external content sources, and humans. Mark the boundaries from the table above.
2. **For each boundary, ask STRIDE-flavored questions** — the [MCP threat-modeling paper](https://www.mdpi.com/2624-800X/6/3/84) (Huang et al., 2026) applies STRIDE/DREAD to MCP architectures and is a useful template for agent stacks: who can *spoof* this tool's response, *tamper* with this corpus entry, *repudiate* this action, *disclose* this context, *deny* this service, *escalate* through this permission?
3. **Enumerate the "untrusted input + privileged capability + exfiltration path" triples.** Injection attacks need all three legs; breaking any leg breaks the attack class (this is the design principle behind [CaMeL](02-prompt-injection-defense.md)).
4. **Classify actions by consequence.** Read-only vs consequential vs irreversible. Irreversible actions (payments, deletes, sends) get human approval and idempotency keys regardless of model confidence — see [tool safety](../104_LLMOps/README.md) and [agent security](04-agent-mcp-security.md).
5. **Write the attacks you will test for** — this becomes the initial [red-team suite](03-red-teaming.md). A threat model that never converts into tests is documentation, not defense.
6. **Re-run when the architecture changes.** Every new tool, corpus source, or model version moves the boundaries.

## References

- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — project page; current list at [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/)
- [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) — ASI01–ASI10
- Huang, Huang, Tran & Milani Fard, *Model Context Protocol Threat Modeling and Analysis of Vulnerabilities to Prompt Injection with Tool Poisoning* (STRIDE/DREAD over MCP), 2026 — [MDPI](https://www.mdpi.com/2624-800X/6/3/84)
- [Roadmap Level 8 — AI Security](../roadmap/full-roadmap/level-08-ai-security.md) — module M8.1 is the syllabus version of this note
- [104 — Safety & Guardrails curriculum](../104_LLMOps/README.md) — implementation-level notes on each control
- Simon Willison's [prompt injection archive](https://simonwillison.net/tags/prompt-injection/) — the most consistently current incident record

Next: [Prompt injection defense →](02-prompt-injection-defense.md)
