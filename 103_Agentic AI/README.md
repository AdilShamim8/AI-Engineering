# 🧠 103: Agentic AI — Planning, Protocols & Frameworks

[![AI Engineering](https://img.shields.io/badge/Domain-AI%20Engineering-blue.svg?style=for-the-badge&logo=python)](https://github.com)
[![Edition](https://img.shields.io/badge/Edition-September_16,_2026-blue.svg?style=for-the-badge)](https://github.com)
[![Topic](https://img.shields.io/badge/Focus-Agentic%20AI%20%26%20MCP-8A2BE2.svg?style=for-the-badge)](https://github.com)
[![Level](https://img.shields.io/badge/Level-Beginner%20%E2%86%92%20Expert-emerald.svg?style=for-the-badge)](https://github.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> **The Definitive, First-Principles Guide to Engineering Autonomous AI Agents, Universal Agent Protocols (MCP), and Modern Framework Architectures.**

> *Verified & Updated: September 16, 2026.*

---

## 📌 Executive Overview

Welcome to **103: Agentic AI** — an exhaustive, production-grade curriculum designed to take software engineers, AI developers, and system architects from **ground zero to interview & enterprise-ready expertise** in Agentic AI systems.

Unlike traditional LLM applications that rely on single-prompt completion (`Input ➔ Output`), **Agentic AI** systems possess autonomy: they break goals down into sub-tasks, reason through complex paths, utilize external tools, maintain state across environment shifts, adapt to failure, and communicate across standardized protocol interfaces.

This repository covers **four core pillars**:
1. **Planning & Reasoning Loops**: Algorithms, patterns (ReAct, CoT, ToT, GoT, Reflexion), state management, guardrails, and evaluation benchmarks.
2. **Agent Protocols (MCP)**: Deep dive into Anthropic's Model Context Protocol, tool standardization schemas, client-server architectures, and capability discovery.
3. **Agentic Frameworks**: Comparative analysis and architectural patterns of LangGraph, CrewAI, AutoGen, LlamaIndex, DSPy, and Claude Computer Use.
4. **Multi-Agent Orchestration & Production Safety**: Collaboration topologies (supervisors, swarms, consensus), Human-in-the-Loop (HITL) approval gates, ephemeral sandboxing, and circuit breakers.

---

## 🗺️ Repository Structure

```
103_Agentic AI/
│
├── 📁 01-Planning & Reasoning/
│   ├── 📄 1. Foundations of Agentic Planning.md
│   ├── 📄 2. Reasoning Patterns in LLM Systems.md
│   ├── 📄 3. Single-Agent Planning.md
│   ├── 📄 4. Task Decomposition Strategies.md
│   ├── 📄 5. Iterative Reasoning Loops.md
│   ├── 📄 6. Tool-Aware Reasoning.md
│   ├── 📄 7. State-Aware Planning.md
│   ├── 📄 8. Planning Constraints & Control.md
│   ├── 📄 9. Failure Modes in Planning Systems.md
│   └── 📄 10. Evaluation of Reasoning Systems.md
│
├── 📁 02-Agent Protocols/
│   ├── 📄 1. Introduction to Model Context Protocol (MCP).md
│   ├── 📄 2. Tool Interface Standardization.md
│   ├── 📄 3. Client–Server Architecture for Agents.md
│   └── 📄 4. Capability Discovery.md
│
├── 📁 03-Agentic AI Frameworks/
│   └── 📄 Frameworks & Libraries.md
│
├── 📁 04-Multi-Agent Orchestration/
│   ├── 📄 1. Multi-Agent Collaboration Patterns.md
│   └── 📄 2. Human-in-the-Loop & Production Safety.md
│
└── 📄 README.md
```

---

## 📚 Detailed Curriculum & Module Breakdown

### 🧩 Module 1: Planning & Reasoning

Master how autonomous models think, break down problems, select actions, handle state, enforce constraints, and evaluate their execution trajectories.

| # | Topic Document | Core Concepts Covered |
|---|---|---|
| **01** | [1. Foundations of Agentic Planning](./01-Planning%20%26%20Reasoning/1.%20Foundations%20of%20Agentic%20Planning.md) | Passive LLMs vs. Active Agents, Plan-Act-Observe-Replan loops, Perception, Memory & Action primitives. |
| **02** | [2. Reasoning Patterns in LLM Systems](./01-Planning%20%26%20Reasoning/2.%20Reasoning%20Patterns%20in%20LLM%20Systems.md) | Chain-of-Thought (CoT), ReAct, Tree-of-Thoughts (ToT), Graph-of-Thoughts (GoT), Reflexion, and Self-Consistency. |
| **03** | [3. Single-Agent Planning](./01-Planning%20%26%20Reasoning/3.%20Single-Agent%20Planning.md) | Architecture of solo agents, execution loop design, short-term/long-term/episodic memory integration, error recovery. |
| **04** | [4. Task Decomposition Strategies](./01-Planning%20%26%20Reasoning/4.%20Task%20Decomposition%20Strategies.md) | Hierarchical goal structures, Directed Acyclic Graphs (DAGs), dynamic re-planning, sub-goal generation. |
| **05** | [5. Iterative Reasoning Loops](./01-Planning%20%26%20Reasoning/5.%20Iterative%20Reasoning%20Loops.md) | Self-Correction, Critique & Refine loops, Human-in-the-Loop (HITL), termination & convergence criteria. |
| **06** | [6. Tool-Aware Reasoning](./01-Planning%20%26%20Reasoning/6.%20Tool-Aware%20Reasoning.md) | Function calling paradigms, dynamic API tool selection, parameter validation, schema alignment & fallback strategies. |
| **07** | [7. State-Aware Planning](./01-Planning%20%26%20Reasoning/7.%20State-Aware%20Planning.md) | World state representation, state mutation tracking, context window management, persistent memory mechanisms. |
| **08** | [8. Planning Constraints & Control](./01-Planning%20%26%20Reasoning/8.%20Planning%20Constraints%20%26%20Control.md) | Guardrails, token budget limits, infinite loop detection, safety policy enforcement, structural output constraints. |
| **09** | [9. Failure Modes in Planning Systems](./01-Planning%20%26%20Reasoning/9.%20Failure%20Modes%20in%20Planning%20Systems.md) | Planning hallucinations, error propagation, context drifting, over-planning loops, tool misuse mitigation. |
| **10** | [10. Evaluation of Reasoning Systems](./01-Planning%20%26%20Reasoning/10.%20Evaluation%20of%20Reasoning%20Systems.md) | Benchmarks (ALFWorld, WebArena, HumanEval, GAIA, AgentBench), path success rate, trajectory cost metrics. |

---

### 🔌 Module 2: Agent Protocols & Model Context Protocol (MCP)

Learn how to decouple model intelligence from tools and data sources through standardized open protocols.

| # | Topic Document | Core Concepts Covered |
|---|---|---|
| **01** | [1. Introduction to MCP](./02-Agent%20Protocols/1.%20Introduction%20to%20Model%20Context%20Protocol%20%28MCP%29.md) | The $M \times N$ integration bottleneck, MCP architecture, Core Primitives (Resources, Prompts, Tools). |
| **02** | [2. Tool Interface Standardization](./02-Agent%20Protocols/2.%20Tool%20Interface%20Standardization.md) | JSON Schema validation, input/output contract enforcement, protocol security boundaries, sandboxing. |
| **03** | [3. Client–Server Architecture for Agents](./02-Agent%20Protocols/3.%20Client%E2%80%93Server%20Architecture%20for%20Agents.md) | MCP Host vs. Server roles, Transport mechanisms (`stdio`, `SSE`, `HTTP`), payload request/response cycles. |
| **04** | [4. Capability Discovery](./02-Agent%20Protocols/4.%20Capability%20Discovery.md) | Dynamic registration, runtime capability negotiation, multi-server routing, schema inspection. |

---

### 🛠️ Module 3: Agentic AI Frameworks & Ecosystems

An in-depth comparative guide for selecting, designing, and scaling agent applications using industry frameworks.

| Topic Document | Key Frameworks & Technologies Analyzed |
|---|---|
| 📄 [Frameworks & Libraries](./03-Agentic%20AI%20Frameworks/Frameworks%20%26%20Libraries.md) | **LangGraph**, **CrewAI**, **Microsoft AutoGen**, **LlamaIndex Workflows**, **Semantic Kernel**, **DSPy**, **Haystack**, **Anthropic Computer Use**. Includes comparative decision matrices and trade-off guides. |

---

### 🤖 Module 4: Multi-Agent Orchestration & Production Safety

Architecting multi-agent collaboration networks, asynchronous human approval checkpoints, secure code sandboxes, and circuit breakers.

| # | Topic Document | Core Concepts Covered |
|---|---|---|
| **01** | [1. Multi-Agent Collaboration Patterns](./04-Multi-Agent%20Orchestration/1.%20Multi-Agent%20Collaboration%20Patterns.md) | Hierarchical supervisor-worker, Sequential chat, Consensus & Debate, LangGraph cyclic state graphs, Shared blackboard memory. |
| **02** | [2. Human-in-the-Loop & Production Safety](./04-Multi-Agent%20Orchestration/2.%20Human-in-the-Loop%20%26%20Production%20Safety.md) | Action risk tiers, Asynchronous interrupts with checkpoint rewind, Ephemeral microVM sandboxing (E2B / gVisor), Token budget & step circuit breakers. |

---

## ⚡ Key Mental Models & Paradigms

```
+-----------------------------------------------------------------------------------+
|                                 AGENTIC REASONING LOOP                            |
|                                                                                   |
|    +-------------+       +-------------------+       +-----------------------+    |
|    |  User Goal  | ----> | Task Decomposition| ----> |  Reasoning & Planning |    |
|    +-------------+       +-------------------+       +-----------------------+    |
|                                                                  |                |
|                                                                  v                |
|    +-------------+       +-------------------+       +-----------------------+    |
|    | Final Goal  | <---- | Observe State &   | <---- | Action Execution      |    |
|    |  Achieved   |       | Re-Plan / Correct |       | (Tools / MCP Server)  |    |
|    +-------------+       +-------------------+       +-----------------------+    |
+-----------------------------------------------------------------------------------+
```

### 🧠 Reasoning Taxonomy Quick Reference

| Pattern | Description | Best Used For |
|---|---|---|
| **ReAct** | Interleaves Reasoning (`Thought`) with Action (`Act`) and Observation (`Obs`). | Tool-using agents performing step-by-step tasks. |
| **CoT (Chain of Thought)** | Linear step-by-step reasoning prior to output generation. | Arithmetic, multi-step math, and logical problems. |
| **ToT (Tree of Thoughts)** | Explores multiple branch paths with evaluation/backtracking. | Complex search spaces, chess, strategic planning. |
| **GoT (Graph of Thoughts)** | Non-linear network combining thoughts from multiple branches. | Synthesizing diverse ideas, complex data aggregation. |
| **Reflexion** | Evaluates past execution feedback to self-correct in subsequent attempts. | Code generation, iterative optimization, self-healing. |

---

## 🎯 Who Is This For?

- **AI Engineers & Developers**: Engineers building autonomous agents, multi-agent orchestrations, or custom tool integrations.
- **System Architects**: Tech leads evaluating agentic frameworks (LangGraph vs CrewAI vs AutoGen) or designing enterprise MCP infrastructures.
- **Researchers & Students**: Anyone seeking a clean, intuitive, and mathematical understanding of agentic planning algorithms.

---

## 🚀 How to Study This Curriculum

1. **Start with Module 01 (Planning & Reasoning)**: Build intuition on how agents break down goals, handle state, and prevent loops.
2. **Move to Module 02 (Agent Protocols)**: Understand how modern agents standardize communication with tools and databases via Model Context Protocol (MCP).
3. **Finish with Module 03 (Frameworks & Libraries)**: Learn when to use production frameworks (LangGraph, CrewAI, AutoGen) versus building custom lightweight agentic loops.

---

## 🤝 Contributing

Contributions, fixes, and improvements are welcome! If you find a typo, want to expand on a topic, or introduce new code examples:

1. Fork the Repository
2. Create your Feature Branch (`git checkout -b feature/agentic-expansion`)
3. Commit your Changes (`git commit -m 'Add deep dive on multi-agent consensus'`)
4. Push to the Branch (`git push origin feature/agentic-expansion`)
5. Open a Pull Request

---

## 📜 License

This repository is available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ for the AI Engineering Community. Master the future of Autonomous Intelligence.</sub>
</div>
