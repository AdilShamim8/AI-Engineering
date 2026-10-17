# Prompt injection defense

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 17, 2026
>
> The [deep curriculum note in 104](../104_LLMOps/4.%20Safety%20%26%20Guardrails/4.%20Prompt%20Injection%20%26%20Jailbreak%20Defense.md) teaches the mechanics of injection and jailbreak attacks from first principles — attack types, defense pillars, worked examples. Read it for the full treatment. This note covers what it can't: the honest state of the problem (unsolved), the current defense consensus, and the research frontier as of late 2026.

## The problem, stated precisely

**Prompt injection** is the injection of instructions through a channel the system treats as data. Direct injection comes from the user; **indirect injection** — the dangerous variant — comes from content the system *reads*: web pages, PDFs, retrieved documents, tool outputs, emails. **Jailbreaking** is the related practice of eliciting policy-violating behavior from the model itself, independent of external content.

The reason this is an *architecture* problem and not a *prompting* problem: the model has no mechanism that reliably distinguishes "developer instruction" from "text that looks like an instruction." Everything arrives as tokens. No prompt, however carefully worded, creates a hard boundary — which is why *"just tell the model to ignore malicious instructions"* is not a security control, a point every serious source agrees on.

Simon Willison, who named the class in 2022, tracks the ongoing incident record on his [prompt injection tag](https://simonwillison.net/tags/prompt-injection/); the pattern that recurs is always the same three legs: **untrusted input + privileged capability + an exit path** (see [threat modeling](01-threat-modeling.md)).

## Why it matters now: agents raised the stakes

A chatbot that can be injected produces bad text. An agent that can be injected *acts on your behalf*: it reads files, sends messages, calls APIs, spends money. Injection became an escalation-of-privilege primitive the moment models got tools. Two documented consequences anchor this:

- The November 2025 [Claude Code espionage campaign](04-agent-mcp-security.md) began with jailbreaking an agent into an attack framework — injection as the entry point to machine-speed intrusion.
- [MCP tool poisoning](04-agent-mcp-security.md) hides injection payloads in *tool descriptions* — instructions the model must read to use the tool at all, invisible in most approval UIs.

## The defense consensus: layers, with the model outside the trust boundary

No layer is sufficient; the working consensus stacks them, and every layer assumes the model *will* be manipulated eventually:

1. **Instruction/data separation (best effort).** Structured prompts that demarcate untrusted content (XML tags, delimiters) plus instructions to treat it as data. Raises the bar, defeats casual payloads; not a boundary against a determined attacker who can write "ignore the above."
2. **Spotlighting.** Encode or transform untrusted content (escaping, marking, chunk-prefixing) so it is less likely to be interpreted as instructions. Same tier: friction, not prevention.
3. **Least privilege & capability removal.** The strongest layer: an injected agent that has no destructive tools, no access to secrets, and no exfiltration path cannot do damage *even when hijacked*. Give read-only defaults; grant write/send/execute per task; keep secrets out of model-visible context (fetch-by-reference instead of paste).
4. **Action validation outside the LLM.** Allowlists for tool arguments, schema validation, URL/domain policy checks, SQL read-only enforcement, path sandboxing. The model proposes; deterministic code disposes. (See [tool safety in 104](../104_LLMOps/README.md).)
5. **Human approval for irreversible actions.** Approval UIs must show *full* arguments — summarized approvals are an attack surface of their own (ASI09).
6. **Output filtering & exfiltration blocking.** Scan model output for secrets/PII before display or transmission; restrict egress destinations. Cheap and effective against the final leg of most attacks.
7. **Anomaly & rate limits.** Unusual tool-call patterns, step budgets, spend caps — containment rather than prevention.

Anthropic's own engineering writeups are a good primary source for how a frontier provider thinks about this in products: [*Beyond permission prompts: making Claude Code more secure and autonomous*](https://www.anthropic.com/engineering/claude-code-sandboxing) (October 2025) and [*Mitigating prompt injections in browser use*](https://www.anthropic.com/research/prompt-injection-defenses) (November 2025) — the latter documents their browser-agent defense combination (spotlighting + tool-call ACLs + anomaly detection) with honest limits.

## The research frontier: defeat by design

Three directions worth knowing beyond the consensus:

- **[CaMeL](https://arxiv.org/abs/2503.18813)** (Debenedetti et al., Google DeepMind, 2025) — *Defeating Prompt Injections by Design.* The key idea: stop trying to make the model resist, and instead **wrap it in a capability-security control plane**. A trusted "privileged" LLM and an untrusted "quarantined" LLM; all control flow and dataflow between them pass through a security manager that enforces information-flow rules (what untrusted content is allowed to influence). Provably defeats the exfiltration class at the cost of a heavier architecture — the strongest published answer to date to "can this be solved at all?"
- **System-level isolation** — running each task in a sandbox with only its required capabilities; injected code that cannot reach the network cannot exfiltrate. Increasingly the default in agent execution products.
- **Detection as a signal, not a gate** — classifiers that flag likely-injected content (used by Anthropic's browser mitigations). Raises attacker cost; judged insufficient alone.

The realistic engineering posture for 2026: **you cannot prevent injection into the model; you can prevent injection from becoming an incident.** Design so that a fully-hijacked model still cannot read what it shouldn't, act beyond its task, or exfiltrate — that is the CaMeL insight in one sentence, and it is achievable with today's layer-3/4/6 controls even without the full architecture.

## Testing your defenses

Defenses that have never faced an attacker are decorative. Minimum bar before release (the [red teaming note](03-red-teaming.md) covers the methodology and tooling):

- A corpus of **indirect injection payloads in retrieved documents** (hidden instructions, Unicode tricks, images with text) run against the live pipeline.
- **Exfiltration canaries** — fake secrets seeded in context; any appearance in outbound traffic or tool calls is a confirmed breach.
- **Tool-abuse scenarios** — injected instructions attempting privilege escalation, budget exhaustion, chain-of-attacks across tools.
- Every confirmed vulnerability becomes a **permanent regression test** in the CI suite (see [eval engineering](../105_AI-Evaluation/05-eval-engineering.md)) — security regressions ship exactly like quality regressions, through the same gate.

## References

- [Prompt injection & jailbreak defense — the 104 deep note](../104_LLMOps/4.%20Safety%20%26%20Guardrails/4.%20Prompt%20Injection%20%26%20Jailbreak%20Defense.md) — first-principles curriculum
- Simon Willison, [prompt injection tag](https://simonwillison.net/tags/prompt-injection/) — incident record & analysis
- OWASP [LLM01: Prompt Injection](https://genai.owasp.org/llm-top-10/) and [ASI01: Agent Goal Hijack](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026)
- Debenedetti et al., *Defeating Prompt Injections by Design* (CaMeL) — [arXiv:2503.18813](https://arxiv.org/abs/2503.18813)
- Anthropic, [*Mitigating prompt injections in browser use*](https://www.anthropic.com/research/prompt-injection-defenses) (Nov 2025) and [*Beyond permission prompts*](https://www.anthropic.com/engineering/claude-code-sandboxing) (Oct 2025)
- Willison & Perez, *Prompt injection attacks against GPT-3* (2022, [simonwillison.net](https://simonwillison.net/2022/Sep/12/prompt-injection/)) — the original writeup that named the class

Previous: [Threat modeling](01-threat-modeling.md) · Next: [Red teaming](03-red-teaming.md)
