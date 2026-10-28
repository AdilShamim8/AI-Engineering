# Level 6 · Context Engineering

> **Phase 3 · Agentic** · 9 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/6/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Manage the model’s limited context window deliberately — decide what enters, what stays, what gets compressed, and what gets moved outside — and build the agent harness that applies these decisions across long-running work.

## Why this level matters

**Interview weight: 6/10**

**Rarely asked as a topic by name**. It mostly helps you give better answers in RAG and agent questions, which can set you apart in **senior-level discussions**.

**On-the-job weight: 8/10**

Once systems grow, quality depends heavily on **what goes into the model’s input**. It’s often the **hidden cause** of a system getting worse over time or becoming expensive.

---

## Modules

### 01 · The context window as a resource (M6.1 · 1 session)

- **Context as a budget** — Treat context as a limited budget rather than “more is always better.”
- **Context rot & lost-in-the-middle** — Understand context rot, distraction, conflicting context, lost-in-the-middle, and token/cost growth.
- **Inspecting what actually enters** — Inspect what actually enters the model’s window and identify which parts are useful versus noise.
- **Allocating the budget** — Allocate rough budgets across instructions, conversation history, retrieval, memory, tools, and working state.

**Outcome** · Diagnose when model degradation is really a context-management problem.

### 02 · Context selection & assembly (M6.2 · 2 sessions)

- **Assembling the window deliberately** — Assemble instructions + conversation history + retrieved knowledge + memory + tool definitions/results + application state deliberately.
- **Always present, retrieved, or excluded** — Decide what should be always present, dynamically retrieved, summarized, or excluded.
- **Prioritising what matters** — Prioritize information based on relevance, importance, recency, and reliability.
- **Ordering so sources stay distinguishable** — Order and structure context so instructions, evidence, memory, and user data remain clearly distinguishable.
- **Cutting redundant & stale context** — Avoid redundant, stale, contradictory, or irrelevant context.

**Outcome** · Construct the smallest useful context for the current model decision.

### 03 · Compression & compaction (M6.3 · 2 sessions)

- **Summarizing history without losing goals** — Summarize growing conversation history while preserving goals, constraints, decisions, and unresolved work.
- **Compacting large tool outputs** — Compact large tool outputs before feeding them back into the model.
- **Rolling & hierarchical summaries** — Apply rolling summaries and hierarchical summarization for long-running tasks.
- **Preserving exact structured data** — Preserve exact structured information separately when summarization could lose important details.
- **Reduction vs information loss** — Understand the trade-off between context reduction and information loss.

**Outcome** · Reduce context size without losing task-critical information.

### 04 · Memory & state offloading (M6.4 · 2 sessions)

- **Scratchpads, files & external stores** — Move information outside the active window using scratchpads, files, databases, memory stores, task state, and working notes.
- **Active context vs stored context** — Distinguish active context from information that can be stored externally and retrieved later.
- **Persisting plans & progress** — Persist plans, completed steps, decisions, intermediate results, and important facts across long-running tasks.
- **Note-taking agents** — Build note-taking agents that write useful information externally and recall it when required.
- **Remembering vs freeing space** — Understand the distinction between memory for remembering and offloading for freeing context space.

**Outcome** · Build systems that do not require the entire task history to remain inside the model’s context.

### 05 · Long-context strategies (M6.5 · 1 session)

- **Why big windows do not solve it** — Understand why large context windows do not eliminate context-engineering problems.
- **Managing lost-in-the-middle** — Manage lost-in-the-middle using better positioning, selective retrieval, and context restructuring.
- **Stuffing vs retrieval vs summarization** — Compare full-context stuffing, retrieval-over-history, summarization, hierarchical context, and selective loading.
- **More context or better context** — Decide when to give the model more context versus retrieve only the relevant parts.

**Outcome** · Choose an appropriate strategy for very long documents, conversations, and agent runs.

### 06 · Tool context management (M6.6 · 1 session)

- **Tool definitions compete for space** — Understand that tool definitions and tool results also compete for context-window space.
- **Exposing only relevant tools** — Dynamically expose only the tools relevant to the current task where possible.
- **Filtering large tool outputs** — Summarize or filter large API/search/database outputs before returning them to the model.
- **Keeping full results externally** — Keep full tool results externally and retrieve details again when required.
- **Stopping observation build-up** — Prevent long agent loops from accumulating unnecessary observations and tool output.

**Outcome** · Keep tool-heavy agents coherent without letting their action history overwhelm the context.

### 07 · Context caching & efficiency (M6.7 · 1 session)

- **The cost of resending static context** — Understand how repeatedly sending large static contexts affects cost and latency.
- **Structuring for cache hits** — Structure stable instructions and reusable context to benefit from prompt/context caching where supported.
- **Stable context vs changing state** — Separate stable context from rapidly changing task state.
- **Cutting redundant tokens** — Reduce redundant tokens while preserving useful information.
- **Measuring cache utilization** — Measure token usage, cache utilization, latency, and cost rather than optimizing blindly.

**Outcome** · Make large-context applications more efficient without sacrificing quality.

### 08 · Harness engineering (M6.8 · 2 sessions)

The agent harness

- **What an agent harness is** — Understand the harness as everything around the model that turns it into a working agent: the loop, system prompt, tool set, context management, state, permissions, and the environment it acts in.
- **Harness problems vs model problems** — Recognize that the same model can succeed or fail on the same task depending on its harness, and that many agent failures are harness problems rather than model problems.
- **Designing the agent loop** — Design the agent loop: how model calls and tool calls alternate, how results and errors are fed back, and when to stop using step, time, and token limits.
- **What the harness enforces** — Decide what the harness enforces versus what the model decides: fixed workflow steps, permission checks, human approval for risky actions, and safe defaults.

Harnesses for long-running work

- **Work across many context windows** — Structure work that spans many context windows: an initial run that sets up the environment, plan, and task list, and later runs that read progress notes, complete one task at a time, and record what changed.
- **Durable artifacts as the source of truth** — Use durable artifacts as the source of truth between runs, such as progress files, task lists, git commits, and tests, rather than conversation history.
- **Self-run feedback loops** — Give the agent feedback loops it can run itself, such as tests, linters, type checks, and end-to-end checks, so it verifies work before marking it done.
- **An environment agents can read** — Make the environment legible to the agent: short instruction files (such as AGENTS.md), a clear project structure, and documentation written to be read by agents.
- **Sub-agents for isolated context** — Use sub-agents to give focused subtasks a fresh, isolated context and return only condensed results.

**Outcome** · Design a harness that keeps an agent productive and on track across long tasks that no single context window can hold.

#### Capstone: Context-Managed Long-Horizon Agent (M6.9 · 1 session)

- A long task that degrades naively Take a tool-using agent from Level 5 and run it through a long task where naive context accumulation causes degradation.
- An explicit context budget Define an explicit context budget and dynamically decide what to keep, retrieve, compress, offload, or discard.
- Compaction, offloading & retrieval Add history compaction, external state, selective memory retrieval, and tool-output compression.
- Wrapping the agent in a harness Wrap the agent in a harness: a progress file and task list it updates, a verification step before any task is marked done, and step and token limits.
- Holding the goal across a long run Preserve the original goal, constraints, completed work, and pending tasks across a long execution.
- Managed vs keep-everything comparison Compare the context-managed version against a naive “keep everything” implementation on coherence, token usage, latency, and cost.

an agent that stays useful across a long, tool-heavy session because its context is actively managed.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — the definitive engineering article on context as a budget, compaction and just-in-time retrieval.
- [Prompt Engineering Guide — Context Engineering](https://www.promptingguide.ai/guides/context-engineering-guide) — structured guide to context selection and assembly techniques.
- [Sourcegraph — Context Engineering: A Practical Guide for AI Agents](https://sourcegraph.com/blog/context-engineering) — practitioner guide tied to real codebase agents.
- [Lost in the Middle: How Language Models Use Long Contexts (paper)](https://arxiv.org/abs/2307.03172) — the research behind position bias in long contexts; free on arXiv.
- [LangChain — Context Engineering blog series](https://blog.langchain.com/) — practical write-ups on writing context for LLM agents.
- [MemGPT / Letta (GitHub)](https://github.com/letta-ai/letta) — reference architecture for memory offloading and context management.

## In this repository

- [Context Engineering curriculum](../../101_LLM-Literacy/03-Context%20Engineering/1.%20Introduction%20to%20Context%20Engineering.md)
- [Memory compression & pruning note](../../102_AI-Application-Development/04-Memory/5.%20Memory%20Compression%20%26%20Pruning.md)

---

[← Level 5 · AI Agents](level-05-ai-agents.md) | [Roadmap map](README.md) | [Level 7 · LLM Evaluations →](level-07-llm-evaluations.md)

<!-- nav-footer -->
---

**Navigate:** [← Level 05 AI Agents](level-05-ai-agents.md) · [Section hub](README.md) · [Level 07 LLM Evaluations →](level-07-llm-evaluations.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
