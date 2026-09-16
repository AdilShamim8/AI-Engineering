# Real-World Production AI System Design Case Studies (2026)

> **Architectural blueprints, latency/cost budgets, failure mitigations, and evaluation frameworks for the 4 most commonly tested AI system design interview questions.**

---

# 🏢 CASE STUDY 1: Enterprise Agentic RAG for Financial & SEC Filings

### 1. Problem Statement & Requirements
- **Scale:** 10,000,000+ 10-K, 10-Q, and 8-K annual/quarterly financial filings spanning 15 years.
- **Traffic:** 2,500 queries/minute from institutional equity research analysts.
- **SLA:** P95 response latency < 1.2s; 0% tolerance for ungrounded financial hallucinations; mandatory source citations with exact page numbers and table coordinates.

```
+-----------------------------------------------------------------------------------+
|                     FINANCIAL AGENTIC RAG SYSTEM ARCHITECTURE                     |
|                                                                                   |
|  [Ingestion Pipeline]                                                             |
|  PDF SEC Filings ──► [MinerU / Marker OCR] ──► Tables to Markdown + Summaries     |
|                              │                                                    |
|                              ▼                                                    |
|  Parent Chunks (1000 tokens) + Child Chunks (200 tokens) ──► Qdrant (HNSW + BM25) |
|                                                                                   |
|  [Runtime Query Pipeline]                                                         |
|  User Query ──► [Query Decomposition Agent] (Splits multi-company comparisons)    |
|                          │                                                        |
|                          ▼                                                        |
|  [Hybrid Search + Metadata Filter (ticker, fiscal_year, report_type)]              |
|                          │                                                        |
|                          ▼ (Top 30 Chunks)                                        |
|  [Cohere Rerank v3] ──► Top 4 Chunks ──► [Self-RAG Grounding Grader]              |
|                                                     │                             |
|                                                     ▼                             |
|  [Reasoning LLM (Claude 3.5 Sonnet)] ──► Grounded Report with Exact Citations     |
+-----------------------------------------------------------------------------------+
```

### 2. Key Architectural Decisions
- **Table Handling:** Financial data lives in tables. Raw text chunking breaks tabular columns. We convert all tables into structured Markdown and compute an LLM-generated table summary, which is prepended to each table slice before embedding.
- **Parent-Child Ingestion:** Child chunks (200 tokens) are embedded for pinpoint search precision; upon match, the 1000-token Parent Chunk is injected into context so financial context (units, currency, footnote asterisks) is never dropped.
- **Strict Grounding Guardrail:** If retrieved chunk confidence is below 0.85, system replies: *"Document does not state Q3 EBITDA for the cloud subsidiary."*

---

# 💻 CASE STUDY 2: Autonomous Code Review & Refactoring Agent with MCP

### 1. Problem Statement & Requirements
- Automatically inspect incoming pull requests, identify bugs, optimize performance, verify test coverage, and submit refactoring suggestions.
