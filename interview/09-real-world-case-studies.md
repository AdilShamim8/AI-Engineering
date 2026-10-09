# Production AI system-design exercises

> Reviewed October 9, 2026. These four architectures are hypothetical exercises, not verified production case studies or a ranking of interview frequency. Workload sizes, timings, thresholds and availability figures below are proposed assumptions/targets, not measured results. Historical model/tool names are illustrative; check current provider documentation before implementation.

---

# 🏢 CASE STUDY 1: Enterprise Agentic RAG for Financial & SEC Filings

### 1. Problem Statement & Requirements
- **Scale:** 10,000,000+ 10-K, 10-Q, and 8-K annual/quarterly financial filings spanning 15 years.
- **Traffic:** 2,500 queries/minute from institutional equity research analysts.
- **Illustrative requirements:** P95 completion latency target < 1.2s under a specified workload; unsupported financial answers require review/abstention rather than a promised zero error rate; mandatory source citations with exact page numbers and table coordinates.

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
- **Strict Grounding Guardrail:** Calibrate an answerability/abstention rule on reviewed evidence; a similarity value is not a universal confidence threshold. For an unsupported answer, the system may reply: *"Document does not state Q3 EBITDA for the cloud subsidiary."*

---

# 💻 CASE STUDY 2: Autonomous Code Review & Refactoring Agent with MCP

### 1. Problem Statement & Requirements
- Automatically inspect incoming pull requests, identify bugs, optimize performance, verify test coverage, and submit refactoring suggestions.
- **Safety:** Must never execute malicious code on host machines; zero permission to merge to `main` without human approval.

```
+-----------------------------------------------------------------------------------+
|                        AUTONOMOUS CODING AGENT ARCHITECTURE                       |
|                                                                                   |
|  GitHub Webhook (PR Opened) ──► [LangGraph Supervisor Agent]                      |
|                                          │                                        |
|                                          ▼                                        |
|              [Tree-sitter AST Parser] (Extract modified classes/functions)        |
|                                          │                                        |
|                                          ▼                                        |
|  [Model Context Protocol (MCP) Client]                                            |
|       │                                                                           |
|       ├─► MCP Tool 1: Code Search Server (Ripgrep / Embedding index)              |
|       ├─► MCP Tool 2: Ephemeral Sandbox Runner (E2B MicroVM)                      |
|       │    * Executes `pytest` in isolated Linux container                        |
|       └─► MCP Tool 3: Linter & Static Security Analyzer (Semgrep / Ruff)          |
|                                          │                                        |
|                                          ▼                                        |
|              [Critic / Refactor Agent] (Drafts code patch & verification)         |
|                                          │                                        |
|                                          ▼                                        |
|              [HUMAN APPROVAL GATE: GitHub Review Comment Created]                 |
+-----------------------------------------------------------------------------------+
```

---

# 🎙️ CASE STUDY 3: Low-Latency Multimodal Voice Support Agent (<600ms TTFT)

### 1. Problem Statement & Requirements
- Real-time conversational customer support over VoIP / WebRTC.
- **Target Latency:** Voice-to-voice turn-around under 600ms as an illustrative design target; measure end-of-user-speech to first audible response separately from text TTFT.

```
+-----------------------------------------------------------------------------------+
|                       STREAMING MULTIMODAL VOICE PIPELINE                         |
|                                                                                   |
|  [User Microphone]                                                                |
|         │ (WebRTC Audio Stream)                                                   |
|         ▼                                                                         |
|  [Deepgram Nova-2 Streaming ASR] (Sub-120ms chunked transcription)                |
|         │ (Partial transcript stream)                                             |
|         ▼                                                                         |
|  [VAD (Voice Activity Detection)] ──► Interruption detected? Kill current TTS!    |
|         │                                                                         |
|         ▼                                                                         |
|  [Fast Intent Classifier & Router] ──► (Simple query? GPT-4o-mini; Complex? Sonnet)
|         │                                                                         |
|         ▼ (First token streamed in 220ms)                                         |
|  [Cartesia / ElevenLabs Streaming TTS] (Converts token buffer to raw PCM audio)   |
|         │ (WebSocket audio packets)                                               |
|         ▼                                                                         |
|  [User Speaker] ──► User hears speech start within ~520ms Total Turnaround!       |
+-----------------------------------------------------------------------------------+
```

### 2. Interruption Handling (Barge-In)
When the user speaks while the bot is talking, the WebRTC client sends a high-priority `INTERRUPT` frame. The backend immediately cancels the downstream LLM generation worker, empties the audio output playback buffer, and shifts context to listen.

---

# 🛡️ CASE STUDY 4: High-Throughput Enterprise LLM Gateway & Caching Router

### 1. Problem Statement & Requirements
- Centralized enterprise AI gateway handling 150M tokens/day across 80 internal engineering teams.
- Targets 99.99% availability, requiring a defined measurement window and an error-budget/recovery plan, prevent single-provider outages, enforce token quotas, and minimize redundant compute costs.

```
+-----------------------------------------------------------------------------------+
|                          ENTERPRISE AI GATEWAY BLUEPRINT                          |
|                                                                                   |
|  [Internal Team Microservices] (Send requests to https://ai-gateway.company.internal)|
|                           │                                                       |
|                           ▼                                                       |
|  [Kong / Envoy API Gateway] (API Key Auth + Team Token Quota Enforcement)         |
|                           │                                                       |
|                           ▼                                                       |
|  [Redis Semantic Cache] (HNSW index on query embeddings)                         |
|         │                                                                         |
|         ├─► [Similarity >= 0.96?] ──► Revalidate scope/version, then return cached response |
|         │                                                                         |
|         ▼ (Cache Miss)                                                            |
|  [LiteLLM Smart Router & Cascading Fallback Pool]                                 |
|         │                                                                         |
|         ├─► Primary: Claude 3.5 Sonnet (Direct API)                              |
|         │    └─► (HTTP 429/500 or timeout > 4s?)                                  |
|         ├─► Secondary Fallback: GPT-4o (Azure OpenAI)                             |
|         │    └─► (Provider Outage?)                                               |
|         └─► Tertiary Fallback: vLLM Self-Hosted Llama-3.3-70B on Private AWS GPUs |
|                           │                                                       |
|                           ▼                                                       |
|  [Async OpenTelemetry + Langfuse Telemetry] (Token usage, latency, spend per team)|
+-----------------------------------------------------------------------------------+
```

### 2. Cost Attribution & Chargebacks
Every request is tagged with an `x-team-id` and `x-project-id` header. The gateway logs exact prompt and completion token counts to ClickHouse, allowing automated monthly department chargebacks and budget limit enforcement.


## Required validation before calling an exercise a case study

Use a real licensed corpus/workflow, record provenance and task IDs, implement a simpler baseline, and execute a frozen evaluation. Publish failure slices, first-token versus completion/voice latency, workload/concurrency, total cost and uncertainty. Financial claims require source/units verification; code agents require isolated test execution; voice flows require interruption and consent checks; gateways require permission-scoped caching and validated fallback contracts.

For any architecture with cache reuse, derive identity and effective permissions before cache lookup. Include source and policy revisions and test revocation/deletion. For writes, test idempotency and ambiguous timeouts. An availability target requires measured service behavior and recovery exercises, not a diagram.

See [the advanced path](../learning-paths/advanced-engineering.md), [production RAG controls](../102_AI-Application-Development/03-RAG/7.%20Production%20RAG%20Architecture%2C%20Caching%20%26%20Failure%20Modes.md), and [the evidence policy](../research/evidence-policy.md).
