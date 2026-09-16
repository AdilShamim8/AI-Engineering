# 🧠 03 — RAG (Retrieval-Augmented Generation)

### *From Naive Prototypes to Production-Grade Enterprise Retrieval Systems*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Modules](https://img.shields.io/badge/Modules-7_Comprehensive_Guides-blue.svg)](#-curriculum-overview)
[![Level](https://img.shields.io/badge/Level-Intermediate_%E2%86%92_Advanced-orange.svg)](#-overview)

Here's the GitHub repository link: https://github.com/AdilShamim8/RAG-Roadmap-with-Notes-and-Projects

> *Verified & Updated: September 16, 2026.*

---

## 📌 Overview

Retrieval-Augmented Generation (RAG) is the dominant architectural pattern in applied AI engineering. It connects frozen parametric language models with dynamic, private, non-parametric enterprise knowledge bases.

This module provides a **first-principles, production-ready curriculum** covering the entire RAG lifecycle: from raw document ingestion and semantic chunking to advanced multi-query transformations, graph-based retrieval (GraphRAG), evaluation frameworks (RAGAS), and enterprise production serving with sub-second latency and multi-tenant security.

---

## 📚 Curriculum Overview

| # | Topic Document | Core Concepts Covered |
|---|---|---|
| **01** | [1. RAG Architecture & Foundations](./1.%20RAG%20Architecture%20%26%20Foundations.md) | First-principles RAG equation, the amnesiac librarian analogy, Parametric vs. Non-Parametric memory, Naive vs. Advanced vs. Modular RAG, Reciprocal Rank Fusion math. |
| **02** | [2. Document Ingestion & Chunking Strategies](./2.%20Document%20Ingestion%20%26%20Chunking%20Strategies.md) | The chunk size spectrum, Recursive Character Splitting, Document-Structure-Aware (Markdown/AST), Semantic Chunking, Parent-Child / Hierarchical Chunking, Sentence-Window retrieval, complex tables & PDF ingestion. |
| **03** | [3. Dense, Sparse & Hybrid Retrieval](./3.%20Dense,%20Sparse%20%26%20Hybrid%20Retrieval.md) | Dense bi-encoders vs. Sparse BM25 lexical search, Learned Sparse (SPLADE), Hybrid Search, Vector Indexing algorithms (HNSW, IVF, PQ), Reciprocal Rank Fusion (RRF) production code. |
| **04** | [4. Re-Ranking, Context Compression & Fusion](./4.%20Re-Ranking,%20Context%20Compression%20%26%20Fusion.md) | Bi-Encoder vs. Cross-Encoder architecture, Cohere Rerank v3, BGE-Reranker, solving the "Lost in the Middle" attention cliff, prompt token compression with LongLLMLingua, two-stage retrieval pipeline. |
| **05** | [5. Advanced RAG Patterns (GraphRAG, Self-RAG, Corrective RAG)](./5.%20Advanced%20RAG%20Patterns%20%28GraphRAG,%20Self-RAG,%20Corrective%20RAG%29.md) | Query Rewriting, Multi-Query expansion, Sub-Question decomposition, HyDE (Hypothetical Document Embeddings), Self-RAG reflection tokens, Corrective RAG (CRAG) web fallbacks, Microsoft GraphRAG & Leiden community detection. |
| **06** | [6. RAG Evaluation & Benchmarking (RAGAS, TruLens, DeepEval)](./6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS,%20TruLens,%20DeepEval%29.md) | The RAG Triad (Context Relevance, Faithfulness, Answer Relevance), RAGAS metrics & formulas, LLM-as-a-Judge biases, synthetic test dataset generation, CI/CD automated quality gates. |
| **07** | [7. Production RAG Architecture, Caching & Failure Modes](./7.%20Production%20RAG%20Architecture,%20Caching%20%26%20Failure%20Modes.md) | Enterprise RAG blueprint, Pre-filtering multi-tenant RBAC / ACLs, Redis Semantic Caching (<15ms latency), Server-Sent Events (SSE) streaming, soft tombstoning document invalidation, production failure taxonomy. |

---

## 🔑 Core Mental Model

```
+-----------------------------------------------------------------------------------+
|                        PRODUCTION TWO-STAGE HYBRID RAG                            |
|                                                                                   |
|  [User Query] ──► [Query Transformation (Multi-Query / HyDE)]                     |
|                            │                                                      |
|                            ▼                                                      |
|  [Hybrid Retrieval: Dense (HNSW) + Sparse (BM25)] ──► Top 25 Candidates          |
|                            │                                                      |
|                            ▼                                                      |
|  [Cross-Encoder Reranker (Cohere / BGE)] ──► Top 3-5 Filtered Chunks              |
|                            │                                                      |
|                            ▼                                                      |
|  [Grounded LLM Generation + Strict Source Citations] ──► Final User Response      |
+-----------------------------------------------------------------------------------+
```

---

<div align="center">
  <sub>Part of the <b>AI Engineering Field Guide</b> by Adil Shamim.</sub>
</div>

---

> 💡 **2026 Production Engineering Takeaway (RAG Architecture):**
> Naive vector search fails at enterprise scale without hybrid keyword fusion (BM25 + Dense) and cross-encoder re-ranking. Always isolate chunk retrieval from generation, implement reciprocal rank fusion, and track context precision metrics in production.
