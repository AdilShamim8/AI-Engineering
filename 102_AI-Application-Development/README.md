<div align="center">

# 🧠 102 — AI Application Development

### *From Fundamentals to Production-Ready AI Systems*

> *Verified & Updated: September 16, 2026.*


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Edition](https://img.shields.io/badge/Edition-September_16,_2026-blue.svg)](#-learning-modules)
[![Modules](https://img.shields.io/badge/Modules-6-blue.svg)](#-learning-modules)
[![Topics](https://img.shields.io/badge/Topics-35%2B-green.svg)](#-learning-modules)
[![Level](https://img.shields.io/badge/Level-Intermediate_%E2%86%92_Advanced-orange.svg)](#-who-is-this-for)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/AdilShamim8/102_AI-Application-Development/pulls)

<br/>

> **A comprehensive, first-principles curriculum for building production-grade AI applications.**
> Every concept is taught from zero — with real analogies, deep explanations, and interview-ready mastery.

<br/>

[🚀 Get Started](#-getting-started) • [📚 Modules](#-learning-modules) • [🗺️ Learning Path](#️-learning-path) • [🤝 Contributing](#-contributing)

</div>

---

## 📌 Overview

This repository is a **structured, depth-first learning system** for engineers who want to go beyond prompt engineering and build real AI-powered applications. It covers the full stack of modern AI application development — from orchestrating multi-step LLM pipelines to fine-tuning your own models.

Each module is designed with a **"Prediction Before Explanation"** methodology — challenging you to reason before you read, so that every concept sticks deeply.

---

## 🎯 What You Will Learn

By completing this curriculum, you will be able to:

- ✅ **Design and implement** multi-step LLM orchestration pipelines
- ✅ **Build** semantic search systems using vector databases and embeddings
- ✅ **Implement RAG** (Retrieval-Augmented Generation) architectures from scratch
- ✅ **Architect memory systems** for stateful, context-aware AI applications
- ✅ **Fine-tune LLMs** using LoRA, QLoRA, and PEFT techniques
- ✅ **Automate complex workflows** with n8n, Zapier, Make, and custom pipelines
- ✅ **Evaluate, debug, and deploy** production AI systems with confidence

---

## 📚 Learning Modules

### 🟦 Module 01 — Orchestration

> *"Why one AI call is never enough for real applications"*

The orchestration module covers the **core architectural blueprints** for coordinating multiple AI models, tools, APIs, and decision points into coherent, production-grade systems.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | Introduction to Orchestration | What orchestration is, why single LLM calls fail, the conductor analogy |
| 2 | Core Orchestration Patterns | Sequential chains, branching, parallel execution, routing patterns |
| 3 | Structured Output | JSON schemas, output parsers, Pydantic models, validation |
| 4 | Tool Integration & Function Calling | Tool use, function calling APIs, agent-tool communication |

**Core Insight:** Just as an orchestra conductor coordinates many musicians into one symphony, an orchestration layer coordinates AI models, tools, and data sources into a working application.

---

### 🟩 Module 02 — Vector Databases

> *"Semantic search: teaching machines to understand meaning, not just keywords"*

This module builds intuition for why traditional keyword search fails and how vector databases enable semantic, meaning-aware retrieval at scale.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | Introduction to Vector Databases | Why keyword search fails, semantic meaning, real-world failures |
| 2 | Embeddings & Vector Space Fundamentals | Embedding models, cosine similarity, vector arithmetic, dimensionality |
| 3 | Ecosystem & Tools | Pinecone, Weaviate, Qdrant, Chroma, pgvector — when to use each |

**Core Insight:** Traditional databases check if words match. Vector databases check if *meanings* match — enabling applications that truly understand user intent.

**Tools Covered:** `Pinecone` · `Weaviate` · `Qdrant` · `Chroma` · `Milvus` · `pgvector` · `FAISS`

---

### 🟨 Module 03 — RAG (Retrieval-Augmented Generation)

> *"Giving LLMs access to knowledge they were never trained on"*

RAG is the most widely deployed pattern in production AI systems. This module covers architecture, chunking strategies, dense/sparse/hybrid retrieval, cross-encoder re-ranking, advanced GraphRAG/Self-RAG, and automated evaluation.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | [RAG Architecture & Foundations](03-RAG/1.%20RAG%20Architecture%20&%20Foundations.md) | Triad of RAG, naive vs advanced RAG, failure taxonomy |
| 2 | [Document Ingestion & Chunking Strategies](03-RAG/2.%20Document%20Ingestion%20&%20Chunking%20Strategies.md) | Semantic, sliding window, hierarchical & parent-document chunking |
| 3 | [Dense, Sparse & Hybrid Retrieval](03-RAG/3.%20Dense,%20Sparse%20&%20Hybrid%20Retrieval.md) | Bi-encoders, BM25, Reciprocal Rank Fusion (RRF), ColBERT late interaction |
| 4 | [Re-Ranking, Context Compression & Fusion](03-RAG/4.%20Re-Ranking,%20Context%20Compression%20&%20Fusion.md) | Cross-encoders, Cohere/BGE rerankers, Long-Context reordering, LLMLingua |
| 5 | [Advanced RAG Patterns (GraphRAG, Self-RAG, Corrective RAG)](03-RAG/5.%20Advanced%20RAG%20Patterns%20(GraphRAG,%20Self-RAG,%20Corrective%20RAG).md) | Knowledge graphs, self-reflection tokens, web fallback loops |
| 6 | [RAG Evaluation & Benchmarking (RAGAS, TruLens, DeepEval)](03-RAG/6.%20RAG%20Evaluation%20&%20Benchmarking%20(RAGAS,%20TruLens,%20DeepEval).md) | Faithfulness, answer relevance, context precision/recall, golden test sets |
| 7 | [Production RAG Architecture, Caching & Failure Modes](03-RAG/7.%20Production%20RAG%20Architecture,%20Caching%20&%20Failure%20Modes.md) | Exact/semantic caching, streaming SSE, RBAC security, incident runbooks |

📎 **External Curriculum Companion** → [RAG Roadmap with Notes and Projects](https://github.com/AdilShamim8/RAG-Roadmap-with-Notes-and-Projects)

---

### 🟥 Module 04 — Memory in AI Systems

> *"Turning stateless LLMs into context-aware, remembering applications"*

One of the most overlooked but critical topics in AI engineering — how to give your applications persistent, structured memory that scales.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | Introduction to Memory | Stateless LLMs, the goldfish waiter analogy, hard truths |
| 2 | Types of Memory | Short-term, long-term, episodic, semantic, procedural memory |
| 3 | Memory Storage Mechanisms | In-context, external DB, vector store, key-value, graph storage |
| 4 | Memory Retrieval Strategies | Recency, relevance, importance scoring, hybrid retrieval |
| 5 | Memory Compression & Pruning | Summarization, forgetting strategies, context window management |
| 6 | Memory in Agentic Systems | Multi-agent memory sharing, agent memory architectures |
| 7 | Memory Failure Modes | Hallucination from bad retrieval, context poisoning, staleness |
| 8 | Tools & Frameworks | Mem0, Zep, LangChain Memory, MemGPT, custom implementations |

**Core Insight:** An LLM is stateless by nature — like a waiter who forgets everything after walking to the kitchen. Memory systems are the engineering layer that gives your app a persistent, intelligent mind.

---

### 🟪 Module 05 — Fine-Tuning

> *"Transforming a generalist model into a domain expert"*

The most technically deep module in the curriculum — covers the full fine-tuning lifecycle from theory to production deployment.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | Fine-Tuning Fundamentals | What fine-tuning is and isn't, parametric adaptation |
| 2 | Pretraining vs Fine-Tuning | When each applies, knowledge vs. behavior modification |
| 3 | Supervised Fine-Tuning (SFT) | Dataset formats, training loops, loss functions |
| 4 | Preference-Based Tuning | RLHF overview, DPO (Direct Preference Optimization) |
| 5 | PEFT | Adapter layers, prompt tuning, prefix tuning |
| 6 | LoRA (Low-Rank Adaptation) | Rank decomposition, trainable parameters, merge strategies |
| 7 | QLoRA (Quantized LoRA) | 4-bit quantization, bitsandbytes, memory-efficient training |
| 8 | Data Preparation | Dataset curation, formatting, quality filters, deduplication |
| 9 | Fine-Tuning vs RAG vs Prompting | Decision framework: when to use which approach |
| 10 | Evaluation of Fine-Tuned Models | Benchmarks, human eval, task-specific metrics |
| 11 | Overfitting & Catastrophic Forgetting | Detection, prevention, continual learning strategies |
| 12 | Adapter Management & Versioning | Model registry, adapter versioning, experiment tracking |
| 13 | Deployment of Fine-Tuned Models | vLLM, GGUF, ONNX, serving infrastructure |

**Core Insight:** Fine-tuning is not retraining from scratch. It's like a smart university graduate joining a company and learning specific rules and workflows — not going back to school.

**Frameworks Covered:** `Hugging Face Transformers` · `PEFT` · `TRL` · `bitsandbytes` · `Axolotl` · `Unsloth`

---

### 🟫 Module 06 — AI Automation

> *"Building intelligent systems that run themselves"*

This module bridges the gap between AI knowledge and operational AI — covering automation patterns, design principles, and the major workflow orchestration tools used in production.

| # | Topic | Key Concepts |
|---|-------|-------------|
| 1 | Introduction to AI Automation | Automation vs intelligence, what AI automation enables |
| 2 | Automation Design Patterns | Event-driven, polling, webhook, pub-sub patterns |
| 3 | Tool Integration for Automation | API chaining, authentication, error handling, retry logic |
| 4 | Workflow Orchestration Tools | n8n vs Zapier vs Make — deep comparison & decision framework |

**Tools Deep-Dived:**

| Tool | Type | Best For |
|------|------|----------|
| **n8n** | Self-hosted / Open-source | Full control, complex logic, dev-friendly |
| **Zapier** | SaaS | Rapid prototyping, 5000+ integrations |
| **Make** | SaaS | Visual workflows, data transformation |

---

## 🗺️ Learning Path

```
┌─────────────────────────────────────────────────────────┐
│                   RECOMMENDED ORDER                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  01 Orchestration  ──►  02 Vector DBs  ──►  03 RAG      │
│                                               │          │
│                                               ▼          │
│  06 Automation  ◄──  05 Fine-Tuning  ◄──  04 Memory     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

> **Note:** Each module builds on the previous. Orchestration is foundational — start there before jumping to fine-tuning or RAG.

---

## 👤 Who Is This For?

This curriculum is designed for:

- 🎓 **CS students** who want to go beyond university AI courses
- 💼 **Software engineers** transitioning into AI/ML roles
- 🔬 **Data scientists** who want to build production AI systems
- 🚀 **Developers** who want to build AI products, not just call APIs
- 📚 **Self-learners** who want a rigorous, structured path into AI engineering

**Prerequisites:**
- Basic Python programming
- Familiarity with APIs and HTTP
- Basic understanding of what an LLM is

---

## 📁 Repository Structure

```
102_AI-Application-Development/
│
├── 📂 01-Orchestration/
│   ├── 1. Introduction to Orchestration.md
│   ├── 2. Core Orchestration Patterns.md
│   ├── 3. Structured Output.md
│   └── 4. Tool Integration & Function Calling.md
│
├── 📂 02-Vector Databases/
│   ├── 1. Introduction to Vector Databases.md
│   ├── 2. Embeddings & Vector Space Fundamentals.md
│   └── 3. Ecosystem & Tools.md
│
├── 📂 03-RAG/
│   └── README.md  →  Full curriculum at linked repo
│
├── 📂 04-Memory/
│   ├── 1. Introduction to Memory in AI Systems.md
│   ├── 2. Types of Memory.md
│   ├── 3. Memory Storage Mechanisms.md
│   ├── 4. Memory Retrieval Strategies.md
│   ├── 5. Memory Compression & Pruning.md
│   ├── 6. Memory in Agentic Systems.md
│   ├── 7. Memory Failure Modes.md
│   └── 8. Tools & Frameworks for Memory Management.md
│
├── 📂 05-Fine-Tuning/
│   ├── 1. Fine-Tuning Fundamentals.md
│   ├── 2. Pretraining vs Fine-Tuning.md
│   ├── 3. Supervised Fine-Tuning (SFT).md
│   ├── 4. Preference-Based Tuning (RLHF, DPO – Overview).md
│   ├── 5. Parameter-Efficient Fine-Tuning (PEFT).md
│   ├── 6. LoRA (Low-Rank Adaptation).md
│   ├── 7. QLoRA (Quantized LoRA).md
│   ├── 8. Data Preparation for Fine-Tuning.md
│   ├── 9. Fine-Tuning vs RAG vs Prompt Engineering.md
│   ├── 10. Evaluation of Fine-Tuned Models.md
│   ├── 11. Overfitting & Catastrophic Forgetting.md
│   ├── 12. Adapter Management & Versioning.md
│   └── 13. Deployment of Fine-Tuned Models.md
│
└── 📂 06-AI-Automation/
    ├── 1. Introduction to AI Automation.md
    ├── 2. Automation Design Patterns.md
    ├── 3. Tool Integration for Automation.md
    └── 4. Workflow Orchestration Tools.md
```

---

## 🔑 Teaching Philosophy

This curriculum uses a **4-step mastery loop** in every module:

```
1. PREDICT  →  "What do YOU think this means?"
2. REVEAL   →  First-principles explanation with analogies
3. BUILD    →  Technical depth, code, diagrams, comparisons
4. APPLY    →  Real-world scenarios, interview questions, edge cases
```

This approach is based on the **retrieval practice effect** — forcing prediction before explanation dramatically improves long-term retention and deep understanding.

---

## 🛠️ Technologies & Tools Referenced

| Category | Tools |
|----------|-------|
| **LLM Frameworks** | LangChain · LlamaIndex · OpenAI SDK · Hugging Face |
| **Vector Databases** | Pinecone · Weaviate · Qdrant · Chroma · Milvus · FAISS · pgvector |
| **Fine-Tuning** | PEFT · TRL · bitsandbytes · Axolotl · Unsloth · vLLM |
| **Memory Systems** | Mem0 · Zep · MemGPT · LangChain Memory · Redis · PostgreSQL |
| **Automation** | n8n · Zapier · Make · Prefect · Airflow · LangGraph |
| **Evaluation** | RAGAs · TruLens · LangSmith · Weights & Biases |

---

## 🚀 Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/AdilShamim8/102_AI-Application-Development.git
cd 102_AI-Application-Development
```

**2. Follow the recommended learning path**
```
Start → 01-Orchestration → 02-Vector Databases → 03-RAG → 04-Memory → 05-Fine-Tuning → 06-AI-Automation
```

**3. For each module:**
- Read the introduction file first
- Attempt the **prediction challenges** before reading the explanation
- Take notes on concepts that are new to you
- Apply the knowledge to a small side project before moving on

---

## 🤝 Contributing

Contributions, corrections, and improvements are warmly welcome!

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/improve-module-04`
3. **Commit** your changes: `git commit -m "Add: memory retrieval examples"`
4. **Push** to the branch: `git push origin feature/improve-module-04`
5. **Open** a Pull Request

Please make sure your contributions follow the existing teaching style — first-principles, analogy-first, and depth-over-breadth.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🔗 Related Resources

| Resource | Link |
|----------|------|
| RAG Roadmap (Full Curriculum) | [AdilShamim8/RAG-Roadmap-with-Notes-and-Projects](https://github.com/AdilShamim8/RAG-Roadmap-with-Notes-and-Projects) |

---

<div align="center">

**Built with ❤️ for the AI engineering community**

*If this repository helped you, consider giving it a ⭐ — it helps others find it too.*

</div>
