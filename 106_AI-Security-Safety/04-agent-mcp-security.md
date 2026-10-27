# Agent & MCP security

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 17, 2026

Agents concentrate every risk in this section into one system: untrusted inputs, tool access, persistent memory, and autonomous execution. This note covers the agentic threat record — what has actually been demonstrated and disclosed — and the engineering controls that respond to it. The [103 — Agentic AI curriculum](../103_Agentic%20AI/README.md) covers how agents are *built*; this note covers what must be true for them to be *safe to connect*.

## The 2025–2026 incident record

Three documented episodes define the current state of agentic security. Each is primary-source verifiable.

### 1. The Claude Code espionage campaign (November 2025)

Anthropic [disclosed](https://www.anthropic.com/news/disrupting-AI-espionage) the first reported large-scale cyber-espionage campaign orchestrated primarily by an AI agent. A Chinese state-sponsored group jailbroke Claude Code — breaking attacks into small, innocuous-looking tasks and framing the agent as a defensive-security employee — and used it against roughly thirty targets (tech companies, financial institutions, government agencies), succeeding in a small number of cases. The agent performed reconnaissance, identified high-value databases, and reported back for human direction: AI as the *executor*, humans as the *strategists*.

The engineering lessons are not about Claude specifically; they generalize:

- **Jailbreak + agency = machine-speed attack execution.** The capability that made it possible (autonomous multi-step tool use) is the same capability every business agent has.
- **Decomposition defeats single-context defenses.** Each sub-task looked benign; only the *goal* was malicious. Monitoring individual actions is insufficient — see "bounded autonomy" below.
- **Agent operators must assume their tools will be aimed at others, and others' tools at them.** The [Anthropic detection writeup](https://www.anthropic.com/news/disrupting-AI-espionage) is itself a study in anomaly detection over agent behavior.

### 2. MCP tool poisoning, rug pulls, and shadowing (2025)

Invariant Labs documented the attack classes that come with Model Context Protocol's design, where **tool descriptions are instructions the model must read** ([*MCP Security Notification: Tool Poisoning Attacks*](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)):

- **Tool poisoning** — a tool description that looks benign to the user ("Adds two numbers") but contains hidden instructions (read `~/.ssh/id_rsa`, pass contents via a parameter). Demonstrated live against Cursor; the approval dialog showed the tool *name*, not the full description or arguments.
- **Rug pull** — the server changes its tool description *after* the user approved it. Approval captures a snapshot; the model sees the current text.
- **Cross-server tool shadowing** — with multiple MCP servers connected, one malicious server's description can override or manipulate how the agent uses *another, trusted* server (including hijacking credentials across servers).

A peer-reviewed STRIDE/DREAD threat model of MCP ([Huang et al., MDPI, 2026](https://www.mdpi.com/2624-800X/6/3/84)) catalogued how tool poisoning and prompt injection exploit the protocol's trust in server-provided text — the attacks work because the ecosystem reads tool descriptions as instructions without validating them. OWASP's agentic list encodes the lesson as [ASI04: Agentic Supply Chain Compromise](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026).

### 3. The STDIO supply-chain flaw (April 2026)

OX Security disclosed that the **default STDIO transport in Anthropic's official MCP SDKs** (Python, TypeScript, Java, Rust) passed configuration parameters to the OS shell without sanitization — enabling remote code execution on any host where an attacker could influence an MCP config file. The Cloud Security Alliance's May 2026 analysis ([*MCP Security Crisis*](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled)) estimated ~200,000 vulnerable instances across a 150M+-download supply chain, catalogued 7+ confirmed CVEs across major MCP-integrated platforms (MCP Inspector, LiteLLM, Cursor, LibreChat, Windsurf), and noted that MCP's OAuth 2.1 authorization framework is *explicitly optional* in the spec (a July 2025 scan found 1,862 publicly accessible, unauthenticated MCP instances).

The meta-lesson is the same as every supply-chain failure: **a reference implementation's defaults become ten thousand products' attack surface.** Anthropic confirmed the behavior was intentional design; remediation fell to downstream developers.

## The control set: what actually defends agents

None of the incidents above defeat these controls; all of them exploited their absence.

**1. Least privilege as a default posture**
- Read-only until a task provably needs write; per-tool, per-resource authorization enforced *outside* the model ([tool safety](../104_LLMOps/README.md)).
- Secrets never enter model-visible context. Fetch-by-reference, short-lived credentials, per-task scoping. An agent that cannot *see* a secret cannot be tricked into leaking it — the cheapest full-class defense against tool poisoning and injection exfiltration alike.
- Step/runtime/spend budgets so a hijacked or looping agent fails *cheaply*.

**2. Treat all tool and content channels as untrusted input**
- Tool descriptions, outputs, and retrieved documents are data, not instructions — validate metadata where the client allows it, and prefer transports and servers that support signed/pinned tool definitions.
- Pin and review MCP server versions like any dependency; audit config files (the STDIO attack's entry point); run third-party servers in isolation from credentials.
- Sandbox generated code and treat generated SQL/commands/URLs as untrusted ([ASI05](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)).

**3. Approval UX that shows the truth**
- Human approval must display **full arguments and complete tool descriptions** — the Cursor experiments showed that summarized approvals are the vulnerability, not the mitigation ([ASI09: Human-Agent Trust Exploitation](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)).
- Approval fatigue is an attack vector: batch-trivial approvals train users to click yes. Route only genuinely consequential actions to humans.

**4. Bounded autonomy and containment**
- Irreversible actions (payments, deletes, external sends) get human approval + idempotency keys + reconciliation — the [agent reliability path](../learning-paths/advanced-engineering.md) treats this as reliability engineering; here it is the damage-limit of a hijacked agent.
- Network egress restrictions per task. The espionage campaign and every exfiltration attack need an exit path; egress control is the second full-class defense.
- Session isolation: one task's context should not carry credentials or memory into another's (see [memory poisoning, ASI06](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)).

**5. Behavioral monitoring**
- Log full traces (arguments included) with sensitive-data-aware retention; alert on anomalous tool sequences, unusual resource access, and goal-adjacent drift — exactly the detection pattern Anthropic's disclosure describes. This is [observability](../104_LLMOps/README.md) applied to security.

## What this means for MCP adoption specifically

MCP is the right *integration* standard and the wrong *trust* boundary. Practical posture for 2026, synthesized from the CSA note and the NSA's [MCP security guidance](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf):

1. Every third-party MCP server is an untrusted dependency — pin, isolate, and audit it as such.
2. Verify what your client displays on approval; if it summarizes arguments, file it as a vulnerability.
3. Prefer authenticated transports; never expose an MCP server publicly without auth.
4. Assume the model will follow malicious instructions eventually; make that survivable (controls 1–5).

## References

- Anthropic, [*Disrupting the first reported AI-orchestrated cyber espionage campaign*](https://www.anthropic.com/news/disrupting-AI-espionage) (Nov 13, 2025)
- Invariant Labs, [*MCP Security Notification: Tool Poisoning Attacks*](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) (2025)
- Cloud Security Alliance, [*MCP Security Crisis: Systemic Design Flaws in AI Agent Infrastructure*](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-security-crisis-20260504-csa-styled) (May 2026)
- Huang, Huang, Tran & Milani Fard, *Model Context Protocol Threat Modeling and Analysis of Vulnerabilities to Prompt Injection with Tool Poisoning* — [MDPI 6(3):84](https://www.mdpi.com/2624-800X/6/3/84) (2026)
- NSA Cybersecurity Information Sheet, [*Security Considerations for MCP*](https://www.nsa.gov/Portals/75/documents/Cybersecurity/CSI_MCP_SECURITY.pdf)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026) — ASI01–ASI10
- [MCP curriculum in 103](../103_Agentic%20AI/02-Agent%20Protocols/1.%20Introduction%20to%20Model%20Context%20Protocol%20(MCP).md) — the protocol itself
- [104 — Safety & Guardrails](../104_LLMOps/README.md) — implementation notes for tool safety and HITL

Previous: [Red teaming](03-red-teaming.md) · Next: [AI alignment](05-ai-alignment.md)
