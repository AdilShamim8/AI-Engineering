# Level 8 · AI Security

> **Phase 4 · Evaluation & Trust** · 9 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/8/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Secure LLM, RAG, and agent systems against model-specific attacks, unsafe actions, data leakage, and regulatory risk.

## Why this level matters

**Interview weight: 5/10**

**Expect one question**, usually about prompt injection, and it’s rarely a deciding factor. **Knowing the basics is enough** unless you’re applying for security roles.

**On-the-job weight: 7/10**

**Prompt injection and data leaks** are real risks in any system that uses tools or private data. **One incident can be very costly**, but daily effort is moderate unless you’re in a regulated industry.

---

## Modules

### 01 · AI threat model (M8.1 · 1 session)

- **How the attack surface changes** — Understand how the attack surface changes when models can process untrusted content, access private data, call tools, and take actions.
- **Trust boundaries** — Identify trust boundaries across prompts, retrieved data, tools, memory, model outputs, and external systems.
- **Model output is untrusted** — Treat model-generated outputs and actions as untrusted until validated.

**Outcome** · Threat-model an LLM application before adding defenses.

### 02 · Prompt injection & data exfiltration (M8.2 · 3 sessions)

- **Direct vs indirect injection** — Distinguish direct prompt injection from indirect injection hidden inside documents, web pages, emails, retrieved chunks, or tool outputs.
- **What injection attacks attempt** — Understand attacks that attempt to override instructions, manipulate tools, expose private context, or redirect an agent's objective.
- **Untrusted input + tools + an exit path** — Understand the dangerous combination of untrusted input + powerful tools/private data + an exfiltration path.
- **Layered defences** — Defend using instruction/data separation, least privilege, authorization checks, restricted tools, confirmation gates, and output validation.
- **Why "ignore malicious instructions" fails** — Understand why prompting the model to “ignore malicious instructions” is not a sufficient security boundary.

**Outcome** · Build applications that remain safe even when malicious instructions reach the model.

### 03 · Jailbreaks, guardrails & moderation (M8.3 · 2 sessions)

- **Jailbreaks vs injection** — Distinguish jailbreaks from prompt injection and recognize common jailbreak patterns.
- **Input & output guardrails** — Add input and output guardrails, moderation, validation, and policy checks.
- **Why one layer is not enough** — Understand the limitations of model-based guardrails and why multiple layers of defense are required.
- **Testing against obfuscated input** — Test guardrails against adversarial and obfuscated inputs instead of only normal requests.

**Outcome** · Reduce unsafe model behavior without relying on a single defensive prompt.

### 04 · Agent & tool security (M8.4 · 2 sessions)

- **Least privilege for agents** — Apply least privilege so agents only receive the tools and permissions required for the task.
- **Read-only vs consequential actions** — Separate read-only actions from consequential actions such as sending messages, modifying records, deleting data, purchasing, or executing code.
- **Validating tool use outside the LLM** — Validate tool selection, arguments, permissions, and outputs independently of the LLM.
- **Human approval for irreversible actions** — Add human approval for sensitive or irreversible operations.
- **Step, runtime & cost limits** — Limit agent steps, runtime, cost, and tool usage to prevent runaway execution.
- **Sandboxing generated code** — Sandbox model-generated code and treat generated **SQL**, commands, URLs, or API calls as untrusted.

**Outcome** · Give agents useful autonomy without giving them unrestricted control over real systems.

### 05 · RAG & knowledge security (M8.5 · 1 session)

- **Retrieved documents are data, not instructions** — Treat retrieved documents as untrusted data, not trusted instructions.
- **Retrieval poisoning** — Understand retrieval poisoning and malicious instructions hidden inside indexed documents.
- **Document-level permissions** — Enforce document-level permissions so users retrieve only information they are authorized to access.
- **Preventing cross-tenant leakage** — Prevent cross-user or cross-tenant data leakage from vector stores and memory systems.
- **Preserving provenance** — Preserve source/provenance information for retrieved content.

**Outcome** · Secure the knowledge layer underneath a RAG application.

### 06 · Data privacy, PII & secrets (M8.6 · 2 sessions)

- **Identifying sensitive data** — Identify sensitive data including **PII**, credentials, financial information, private conversations, and confidential business data.
- **Redaction & minimization** — Detect, redact, mask, or minimize sensitive information before sending it to models when appropriate.
- **Keeping PII out of logs & traces** — Avoid unnecessarily storing sensitive data in prompts, logs, traces, memories, vector stores, or evaluation datasets.
- **Retention, deletion & residency** — Understand data retention, deletion, residency, access control, and third-party model-provider considerations.
- **Private connectivity & zero retention** — Use the controls that make regulated deployments possible: private connectivity to the model endpoint, no public egress, and contractual zero-retention or no-training terms.
- **Protecting secrets from the model** — Protect secrets so they are never unnecessarily exposed to the model.

**Outcome** · Minimize the amount of sensitive information exposed throughout an AI system.

### 07 · Red teaming AI systems (M8.7 · 2 sessions)

- **Building adversarial test suites** — Build adversarial tests for prompt injection, jailbreaks, malicious documents, tool misuse, data extraction, and unsafe agent actions.
- **Attacking RAG through the corpus** — Test **RAG** systems by injecting malicious content into retrievable documents.
- **Attacking agents through their tools** — Test agents by attempting to make them exceed permissions, misuse tools, reveal secrets, or enter loops.
- **Vulnerabilities become regression tests** — Turn discovered vulnerabilities into permanent security regression tests.
- **Attack-success & leakage rates** — Track measures such as attack-success rate, sensitive-data leakage, and unsafe-action rate where useful.

**Outcome** · Test defenses adversarially instead of assuming they work.

### 08 · Responsible AI & governance (M8.8 · 1 session)

- **Bias, transparency & human oversight** — Understand core concerns around hallucination, bias/fairness, transparency, accountability, and human oversight.
- **Documenting use, limits & risks** — Document intended use, known limitations, important risks, evaluations, and human-control mechanisms.
- **The EU AI Act & India's DPDP** — Understand the practical implications of relevant regulations such as the **EU AI Act** and India's **DPDP** framework.
- **Auditability** — Maintain auditability through model/prompt versions, logs, approvals, and evaluation records.

**Outcome** · Recognize when an AI application creates governance or compliance obligations.

#### Capstone: Red-Team & Secure an Agentic RAG App (M8.9 · 1 session)

- Attack an app you already built Take an application built in earlier levels and attack it using:
- Direct & indirect prompt injection direct and indirect prompt injection
- Malicious retrieved documents malicious retrieved documents
- Jailbreak attempts jailbreak attempts
- Private-data extraction private-data extraction
- Tool misuse tool misuse
- Unauthorized actions unauthorized actions.
- Then add
- Least-privilege tools least-privilege tools
- Permission checks permission checks
- Guardrails guardrails
- PII & secrets protection **PII**/secrets protection
- Approval gates approval gates
- Sandboxing sandboxing
- Security regression tests security regression tests.

an AI system designed to remain safe even when the model makes a bad decision or receives malicious input.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10) — the canonical, freely available list of LLM application risks (updated 2026 edition).
- [OWASP Gen AI Security Project](https://genai.owasp.org/) — free guides, checklists and agentic security resources.
- [Simon Willison's blog — prompt injection tag](https://simonwillison.net/tags/prompt-injection/) — the most consistently current practitioner writing on injection attacks and defenses.
- [Anthropic — Mitigating prompt injections in browser use](https://www.anthropic.com/research/prompt-injection-defenses) — provider-side research on layered injection defenses.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — free framework for governance, risk and trustworthy AI.
- [EU AI Act — official portal](https://artificialintelligenceact.eu/) — free access to the regulation text and timelines.
- [Microsoft AI Red Team guidance](https://learn.microsoft.com/en-us/security/ai-red-team) — provider guidance on AI red teaming and securing generative AI deployments.
- [PyRIT (Python Risk Identification Toolkit, Microsoft)](https://github.com/Azure/PyRIT) — open-source red-teaming automation for LLM systems.

## In this repository

- **[106 — AI Security & Safety](../../106_AI-Security-Safety/README.md)** — the dedicated knowledge base for this level: [threat modeling](../../106_AI-Security-Safety/01-threat-modeling.md), [prompt injection defense](../../106_AI-Security-Safety/02-prompt-injection-defense.md), [red teaming](../../106_AI-Security-Safety/03-red-teaming.md), [agent & MCP security](../../106_AI-Security-Safety/04-agent-mcp-security.md), [AI alignment](../../106_AI-Security-Safety/05-ai-alignment.md), [responsible AI](../../106_AI-Security-Safety/06-responsible-ai.md)
- [Safety & guardrails curriculum](../../104_LLMOps/4.%20Safety%20%26%20Guardrails/1.%20Input%20Safety.md)
- [Prompt injection & jailbreak defense note](../../104_LLMOps/4.%20Safety%20%26%20Guardrails/4.%20Prompt%20Injection%20%26%20Jailbreak%20Defense.md)
- [Governance curriculum](../../104_LLMOps/5.%20Governance/1.%20Data%20Governance.md)

---

[← Level 7 · LLM Evaluations](level-07-llm-evaluations.md) | [Roadmap map](README.md) | [Level 9 · AI System Design →](level-09-ai-system-design.md)
