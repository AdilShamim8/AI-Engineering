# Level 3 · Prompt Engineering

> **Phase 1 · Foundations** · 9 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/3/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Design instructions that make LLM behavior more reliable and predictable. Context engineering comes later.

*Short on time? Do the 7-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 5/10**

Interviewers **rarely ask about it in depth**; they assume you can do it. It doesn’t set you apart, and listing it on a resume as a headline skill **can look junior**.

**On-the-job weight: 8/10**

You **write and revise prompts constantly**. Small changes to instructions often fix problems faster than code changes, so it **matters more on the job than in interviews**.

---

## Modules

### 01 · Anatomy of a prompt (M3.1 · 1 session)

- **The parts of a prompt** — Structure prompts using instructions, context, input, constraints, examples, and output requirements.
- **Roles & instruction priority** — Use system/user/assistant roles correctly and understand instruction priority.
- **Separating instructions from data** — Separate instructions clearly from user-provided or external data.

### 02 · Zero-shot & few-shot prompting (M3.2 · 2 sessions)

- **When examples are needed** — Know when a clear zero-shot instruction is sufficient and when examples are needed.
- **Designing few-shot examples** — Design useful few-shot examples that demonstrate desired behavior and output format.
- **Example quality, diversity & order** — Understand how example quality, diversity, and ordering can affect results.
- **Few-shot vs fine-tuning** — Distinguish few-shot prompting from fine-tuning.

### 03 · Reasoning & decomposition (M3.3 · 1 session)

- **When to prompt for reasoning** — Use reasoning-oriented prompting for complex logic, planning, mathematics, coding, and constraint-heavy tasks.
- **When reasoning is unnecessary** — Know when extra reasoning is unnecessary for tasks such as extraction, classification, and rewriting.
- **Decomposing complex tasks** — Break complex tasks into clearer subproblems or intermediate steps.
- **Prompting reasoning models** — Adapt prompting for reasoning models rather than relying blindly on “think step by step.”

### 04 · System prompt design (M3.4 · 2 sessions)

- **What belongs in a system prompt** — Define application purpose, behavior, constraints, boundaries, and output expectations in the system prompt.
- **Stable rules vs task instructions** — Separate stable application rules from task-specific user instructions.
- **Handling missing or out-of-scope input** — Specify what the model should do when information is missing, ambiguous, or outside scope.
- **Lightweight behavioural guardrails** — Add lightweight behavioral guardrails without turning the system prompt into an enormous rulebook.

### 05 · Controlling output (M3.5 · 1 session)

- **Controlling style, length & format** — Control response style, length, format, headings, labels, tables, and **JSON** through clear instructions and examples.
- **When prompting is not enough** — Know when prompting is enough and when structured-output/schema enforcement from Level 2 is more reliable.
- **Semantic instruction vs format enforcement** — Separate semantic instructions from programmatic format enforcement.

### 06 · Prompt reliability & debugging (M3.6 · 2 sessions)

- **Diagnosing prompt failures** — Diagnose failures caused by ambiguous instructions, conflicting constraints, poor examples, missing context, or unclear output requirements.
- **Building a small test set** — Build a small test set containing normal cases, edge cases, and known failures.
- **Comparing versions on the same examples** — Compare prompt versions on the same examples instead of judging them from individual responses.
- **Reducing variance & regressions** — Reduce unnecessary output variance and regressions through systematic iteration.

### 07 · Prompt versioning, cost & caching (M3.7 · 1 session)

- **Versioning prompts like code** — Version prompts like code and track which prompt/model combination produced each result.
- **Comparing on quality, latency & cost** — Compare prompt variants using quality, latency, token usage, and cost.
- **Trimming unnecessary context** — Remove unnecessary context and repeated instructions.
- **Prompt caching & reusable prefixes** — Understand prompt caching and structure reusable prompt prefixes to benefit from caching where supported.

### 08 · Prompt injection basics (M3.8 · 1 session)

- **What prompt injection is** — Understand prompt injection and why external/user-controlled text should be treated as untrusted data.
- **Recognising override attempts** — Recognize attempts to override system instructions or extract hidden information.
- **Wording is not a security boundary** — Understand that prompt wording alone is not a security boundary; permissions and sensitive actions must be controlled by application code.
- **Deeper defences come later** — Leave deeper adversarial security and defenses for the later security level.

#### Capstone: Optimize a Real Prompt (module 09 · capstone)

- Choosing a realistic task Choose one realistic task such as classification, extraction, support answering, or a domain-specific assistant.
- A test set and competing prompt versions Create a small test set and develop multiple prompt versions. Compare them on:
- Correctness correctness
- Instruction following instruction following
- Output-format adherence output-format adherence
- Consistency consistency
- Token usage token usage
- Latency & cost latency/cost.
- Choosing on measurement, not intuition Select the final prompt based on measured performance rather than intuition.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [Anthropic Prompt Engineering guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — the most current provider guidance on structure, clarity and system prompts.
- [Anthropic Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — free hands-on exercises.
- [Prompt Engineering Guide (promptingguide.ai)](https://www.promptingguide.ai/) — open, community-maintained compendium of techniques from zero-shot to decomposition.
- [OpenAI Prompt engineering guide](https://platform.openai.com/docs/guides/prompt-engineering) — provider-side tactics and examples.
- [Google Gemini prompting strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) — prompt design for multimodal models.
- [Learn Prompting (learnprompting.org)](https://learnprompting.org/) — free structured curriculum for prompt fundamentals.
- [DSPy documentation](https://dspy.ai/) — declarative prompt programming and automatic prompt optimization.

## In this repository

- [Prompt Engineering curriculum (7 notes)](../../101_LLM-Literacy/02-Prompt%20Engineering/1.%20Mental%20Model%20of%20Prompting%20%28Foundation%20Layer%29.md)
- [Prompt robustness & reliability note](../../101_LLM-Literacy/02-Prompt%20Engineering/5.%20Prompt%20Robustness%20%26%20Reliability.md)

---

[← Level 2 · Working with LLM APIs (Orchestration)](level-02-working-with-llm-apis.md) | [Roadmap map](README.md) | [Level 4 · RAG →](level-04-rag.md)
