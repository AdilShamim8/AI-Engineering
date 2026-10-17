# Level 5 · AI Agents

> **Phase 3 · Agentic** · 11 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/5/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Build systems where models can decide what to do next, use tools, maintain state, recover from failures, and collaborate with other agents. Planning · tools · MCP · memory · multi-agent · LangGraph.

*Short on time? Do the 27-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 9/10**

One of the **hottest topics** in current job descriptions. Tool calling, MCP, LangGraph, and multi-agent setups are keywords that **pass resume filters** and come up often in interviews.

**On-the-job weight: 7/10**

More and more common, but many production tasks are better handled by **simple fixed workflows**. Knowing **when not to build an agent** is part of the skill.

---

## Modules

### 01 · What is an agent? (M5.1 · 1 session)

- **The agent loop** — Understand the basic loop: goal → decide → act → observe → repeat → finish.
- **Call vs chain vs workflow vs agent** — Distinguish LLM call vs chain vs workflow vs agent, especially based on who decides what happens next.
- **Where agents are useful** — Understand where agents are useful: open-ended, multi-step tasks where the execution path cannot be fully predetermined.
- **When a workflow is better** — Know when a deterministic workflow is simpler, cheaper, and more reliable.
- **The components of an agent** — Understand the basic components of an agent: model, instructions, tools, state/memory, control loop, stopping conditions.

**Outcome** · Decide whether a problem genuinely requires an agent.

### 02 · ReAct, planning & reflection (M5.2 · 2 sessions)

- **The ReAct pattern** — Understand the ReAct pattern: the agent alternates between deciding what to do and acting on the environment.
- **Writing the loop by hand first** — Implement a simple agent loop manually before using a framework.
- **Step-by-step vs plan-first** — Understand step-by-step execution vs plan-first execution.
- **Decomposing and revising plans** — Break complex goals into subtasks and dynamically revise plans as new information appears.
- **Reflection & self-correction** — Use reflection/self-correction when actions fail or results are insufficient.
- **Stopping conditions & loop protection** — Implement stopping conditions, maximum steps, and protection against repetitive loops.
- **What planning costs** — Understand that more planning/reflection can increase quality but also latency and cost.

**Outcome** · Build an agent capable of solving a multi-step task without hard-coding its exact execution path.

### 03 · Tools for agents (M5.3 · 2 sessions)

- **From tool calling to agentic tool use** — Extend Level 2 tool calling into agentic tool use where the model repeatedly selects among available capabilities.
- **Designing tools for agents** — Design tools with clear names, descriptions, schemas, typed arguments, useful outputs, and useful error messages.
- **Improving selection & arguments** — Improve tool selection and argument correctness.
- **Sequential, parallel & repeated calls** — Handle sequential, dependent, parallel, and repeated tool calls.
- **Recovering from tool failures** — Handle tool failures and allow the agent to recover or choose an alternative.
- **Limiting tool-result size** — Limit the size of tool results returned to the model so context does not become overwhelmed.
- **Read-only vs consequential tools** — Separate read-only tools from consequential tools and add confirmation/permission checks where necessary.

**Outcome** · Give an agent useful capabilities without giving it uncontrolled access to the underlying application.

### 04 · MCP (Model Context Protocol) (M5.4 · 3 sessions)

- **Why MCP exists** — Understand why MCP exists: provide a standardized way for AI applications to connect to external tools, resources, and prompts.
- **Host → client → server** — Understand the host → client → server architecture and the responsibility of each component.
- **Tool calling vs MCP** — Distinguish ordinary function calling from MCP: tool calling describes how a model requests an action, while MCP standardizes how external capabilities are exposed to AI applications.
- **Building an MCP server** — Build an **MCP** server that exposes tools/resources from a real system such as a database, filesystem, SaaS application, or internal API.
- **Schemas, transports & auth** — Work with schemas, capabilities, errors, local/remote transports, and authentication.
- **Building and connecting a client** — Build/use an **MCP** client and connect it to one or more servers.
- **Permissions & untrusted servers** — Understand permissions, trust boundaries, and the risk of connecting to untrusted **MCP** servers.

**Outcome** · Build a reusable MCP integration that can expose a real system to compatible AI applications.

### 05 · Memory basics (M5.5 · 2 sessions)

- **History, state, short- & long-term memory** — Distinguish conversation history, state, short-term memory, and long-term memory.
- **Short-term memory** — Implement short-term memory so an agent can retain information during a conversation or task.
- **Long-term memory** — Implement basic long-term memory using persistent stores or retrieval-backed memory.
- **Storing what is worth keeping** — Store useful facts, preferences, summaries, or previous outcomes instead of blindly preserving every message.
- **Retrieving only relevant memories** — Retrieve relevant memories when needed rather than injecting the entire history into every request.
- **Write → retrieve → update → forget** — Understand basic memory operations: write → retrieve → update → forget.
- **Trimming & summarizing growth** — Handle growing conversations through trimming or summarization.
- **Offloading comes later** — Keep deeper context offloading/compression strategies for the later Context Engineering level.

**Outcome** · Build an agent that remembers relevant information during and across interactions.

### 06 · Multi-agent architectures (M5.6 · 3 sessions)

- **Why more than one agent** — Understand why multiple agents may help when tasks require different tools, instructions, models, permissions, or areas of expertise.
- **Common patterns** — Learn common patterns:
- **Orchestrator → workers** — orchestrator → workers
- **Sequential handoffs** — sequential handoffs
- **Parallel specialists** — parallel specialists
- **Hierarchical supervisor/worker** — hierarchical supervisor/worker architectures.
- **Building an orchestrator** — Build an orchestrator that decomposes work and delegates tasks to specialist agents.
- **Passing state & aggregating output** — Pass useful state/context between agents and aggregate their outputs.
- **Worker failure & escalation** — Handle worker failures, retries, reassignment, and escalation.
- **What goes wrong with many agents** — Understand common multi-agent problems: duplicated work, coordination overhead, context growth, conflicting results, latency, and cost.
- **A2A vs MCP** — Understand **A2A** as an interoperability approach for independently built agents and contrast it conceptually with **MCP**: **MCP** connects agents to tools/resources; **A2A** connects agents to agents.
- **When one strong agent is better** — Learn when multiple agents genuinely improve specialization and when one strong agent with several tools is preferable.

**Outcome** · Design multi-agent systems only when decomposition or specialization actually justifies the additional complexity.

### 07 · Building agents with LangGraph (M5.7 · 3 sessions)

- **What LangGraph is for** — LangGraph is positioned as a low-level orchestration framework/runtime for long-running, stateful agents.
- **State, nodes & edges** — Model agent execution using state, nodes, and edges.
- **Building nodes** — Build nodes for model calls, tools, processing logic, and decisions.
- **Conditional edges** — Use conditional edges to dynamically determine the next action.
- **Loops for retries & iteration** — Implement loops for repeated tool use, retries, and iterative execution.
- **Checkpointing & persistence** — Add checkpointing/persistence so execution can survive interruptions.
- **Resuming long runs** — Resume long-running agent runs rather than restarting them from scratch.
- **Human-in-the-loop interrupts** — Add human-in-the-loop interrupts for actions requiring approval or intervention.
- **Inspecting state to debug** — Inspect agent state to debug why a particular execution path was taken.
- **When a graph beats a loop** — Understand when graph-based orchestration offers more control than a simple agent loop.

**Outcome** · Build a controllable, stateful, resumable agent with explicit execution logic.

### 08 · Sandboxed execution (M5.8 · 1 session)

- **Why generated code must not run in-process** — Understand why model-generated **Python**, shell commands, or arbitrary programs should not execute directly inside the production application.
- **Sandboxes: E2B, Modal & containers** — Run generated code inside isolated environments such as **E2B**, **Modal**, containers, or equivalent sandboxes.
- **Restricting filesystem, network & time** — Restrict filesystem, network, credentials, execution time, and compute resources.
- **Capturing output safely** — Capture stdout, stderr, files, and errors and return only necessary results to the agent.
- **Reducing the blast radius** — Understand the principle of reducing the blast radius when an agent can take executable actions.

**Outcome** · Give an agent code-execution capabilities without exposing the host system unnecessarily.

### 09 · Agent reliability, UX & failure recovery (M5.9 · 2 sessions)

- **Common agent failures** — Handle common failures: wrong tool selection, bad arguments, unavailable tools, repeated actions, incomplete plans, infinite loops, and context growth.
- **Step, time, retry & cost budgets** — Define maximum steps, timeouts, retry budgets, cost/token budgets, and stopping conditions.
- **Idempotent operations** — Make operations idempotent where possible so retries do not accidentally repeat real-world side effects.
- **Persisting state to resume** — Persist enough execution state to resume after interruption.
- **Fallbacks & human escalation** — Add fallback actions and human escalation when the agent cannot continue safely.
- **Surfacing progress to users** — Surface useful progress to users: current task, tool/action being performed, results, sources, and requests for approval.
- **Cancel, pause, resume, redirect** — Allow users to cancel, pause, resume, or redirect long-running work.
- **Understandable without exposing reasoning** — Avoid exposing unnecessary private reasoning while still making execution understandable.

**Outcome** · Build agents that fail predictably, recover gracefully, and keep the user informed and in control.

### 10 · Agent frameworks & libraries (M5.10 · 2 sessions)

- **One agent, several frameworks** — After learning the primitives, implement the same small agent in several frameworks and understand what each one abstracts.

LangGraph

- **Graph-based, stateful orchestration** — Low-level graph/state-based orchestration for long-running, stateful agents.
- **Where explicit control flow wins** — Strong fit when explicit control flow, persistence, loops, and human-in-the-loop behavior matter.

Google Agent Development Kit (ADK)

- **Google's ADK** — Build agents using Google's open-source **ADK** and explore its agent, session/state, tools, multi-agent, deployment, and **A2A**-related abstractions.
- **Building, debugging & deploying agents** — Understand its emphasis on building, debugging, evaluating, and deploying agent systems rather than merely wrapping an LLM call.

CrewAI

- **Crews and Flows** — Build agents and collaborative Crews, and understand Flows for more controlled workflow-style orchestration.
- **Role-based vs graph orchestration** — Explore role-based multi-agent patterns and compare them with explicit graph orchestration.

Agno

- **Agents, Teams & Workflows** — Build Agents, Teams, and Workflows and understand the distinction between agent autonomy, team coordination, and deterministic workflows.
- **The production runtime layer** — Explore its production/runtime layer and how agent systems can be exposed as services.

OpenAI Agents SDK

- **Code-first agents with handoffs** — Build code-first agents using tools, handoffs, sessions, guardrails, tracing, and specialist agents.
- **Lightweight SDK vs graph frameworks** — Compare a lightweight SDK-style agent loop with graph-oriented or multi-agent-first frameworks.

Compare them on

- **Abstraction level** — abstraction level
- **Control over execution** — control over execution
- **State & persistence** — state/persistence
- **Multi-agent support** — multi-agent support
- **Tool integrations** — tool integrations
- **MCP & A2A support** — MCP/A2A support
- **Debugging & observability** — debugging/observability
- **Deployment** — deployment
- **Vendor & model flexibility** — vendor/model flexibility.

**Outcome** · Understand the agent-framework landscape and choose a framework based on architecture rather than popularity.

#### Capstone: Build a Production-Style Agent (M5.11 · 1 session)

- Choosing a substantial project Choose one substantial project.
- Option A · Research agent
- Build
- Planner → Researcher → Analyst → Writer Planner → Researcher → Analyst → Writer
- Dynamic planning, state & retries with dynamic planning, tools, state, source tracking, retries, and optional specialist agents.
- Option B · MCP-powered agent
- A server plus an agent that uses it Build an **MCP** server for a real service and an agent capable of using its tools/resources to complete multi-step tasks.
- Option C · Coding/data agent
- Build an agent that
- Plan → write → run → inspect → fix understands task → plans → writes code → executes in sandbox → inspects result/error → fixes code → returns output
- Capstone requirements Capstone requirements
- At least three useful tools at least 3 useful tools
- Multi-step autonomous execution multi-step autonomous execution
- Explicit state explicit state
- Stopping conditions stopping conditions
- Failure recovery failure recovery
- Logs & progress visibility logs/progress visibility
- A human approval point at least one human approval point for consequential actions where appropriate
- One framework, explained from first principles implementation in one agent framework while being able to explain the underlying agent loop.

a real agent that demonstrates planning + tools + state + recovery + controlled autonomy, not merely an LLM wrapped in a while loop.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course) — free certified course covering agent fundamentals, frameworks and MCP.
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — state, nodes, edges, checkpointing, human-in-the-loop interrupts.
- [LangChain Academy — Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) — free hands-on course building agents with LangGraph.
- [Model Context Protocol — official docs](https://modelcontextprotocol.io/) — the MCP specification, SDKs and guides (current spec version 2026-07-28).
- [Anthropic — Introduction to MCP (free course)](https://anthropic.skilljar.com/introduction-to-model-context-protocol) — official free course on building and connecting MCP servers.
- [MCP server reference implementations (GitHub)](https://github.com/modelcontextprotocol/servers) — read production-grade server code.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — handoffs, guardrails, sessions and tracing.
- [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) — Google's open-source agent framework with multi-agent and A2A support.
- [smolagents documentation](https://huggingface.co/docs/smolagents) — lightweight code-first agents from Hugging Face.
- [Agent2Agent (A2A) protocol (GitHub)](https://github.com/a2aproject/A2A) — the emerging agent-to-agent interoperability standard.
- [E2B documentation](https://e2b.dev/docs) and [Modal documentation](https://modal.com/docs) — sandboxed code execution for agents.

## In this repository

- [Agentic AI curriculum](../../103_Agentic%20AI/README.md)
- [MCP curriculum](../../103_Agentic%20AI/02-Agent%20Protocols/1.%20Introduction%20to%20Model%20Context%20Protocol%20%28MCP%29.md)
- [Multi-agent orchestration curriculum](../../103_Agentic%20AI/04-Multi-Agent%20Orchestration/1.%20Multi-Agent%20Collaboration%20Patterns.md)
- [Memory systems curriculum](../../102_AI-Application-Development/04-Memory/1.%20Introduction%20to%20Memory%20in%20AI%20Systems.md)

---

[← Level 4 · RAG](level-04-rag.md) | [Roadmap map](README.md) | [Level 6 · Context Engineering →](level-06-context-engineering.md)
