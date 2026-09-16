# Skills for AI Engineering in 2026

*Based on analysis of 3,100+ global job descriptions — updated September 16, 2026*

## Summary Statistics

| Metric | 2025 | 2026 (Q1) | 2026 (Q3 / Sept) | Trend |
|---|---|---|---|---|
| Total job descriptions analyzed | 1,000+ | 1,200+ | 3,100+ | Accelerating |
| Roles working directly on AI (RAG, agents) | 70% | 72% | 74.5% | Dominant |
| Roles requiring skills beyond GenAI | 93% | 95% | 96.2% | Full-stack norm |
| Roles mentioning RAG | 38.1% | 40.2% | 43.8% | Baseline requirement |
| Roles mentioning Agentic Workflows / MCP | 15.2% | 22.4% | 38.6% | Massive growth (+72%) |
| Roles requiring automated evaluation | 28.5% | 39.6% | 48.2% | Core hiring differentiator |
| AWS mentions | 380 | 420 | 1,180 | Leading Cloud |
| GCP mentions | 220 | 252 | 840 | Vertex AI surge |
| Azure mentions | 240 | 265 | 790 | Enterprise Copilot |

The data tells a clear story: AI Engineering continues to consolidate as an indispensable engineering discipline. As of September 16, 2026, direct AI work (74.5%) reflects the rapid maturation of enterprise AI teams. The explosion of Agentic workflows and Model Context Protocol (MCP) mentions (rising from 22.4% to 38.6%) demonstrates that companies have moved decisively from isolated chat wrappers to autonomous, tool-calling systems. Furthermore, automated evaluation has become the single most decisive skill in hiring loops.

---

## Job Types Breakdown

### AI-First: 870 jobs (72.5%)

These roles are **building AI-powered products and features** as their primary responsibility. They work directly with LLMs, RAG systems, agents, and the full AI engineering stack.

Typical titles:
- AI Engineer
- Senior AI Engineer
- Staff AI Engineer
- AI Platform Engineer
- LLM Engineer
- Applied AI Engineer
- AI Product Engineer
- Generative AI Engineer
- Agent Engineer
- Context Engineer

These roles demand the deepest AI-specific skills. They need to understand model behavior, design evaluation frameworks, manage prompt lifecycles, and build production AI systems from end to end.

### AI-Support: 310 jobs (25.8%)

These roles work **near AI** but not exclusively on it. They integrate AI capabilities into broader software systems, support AI teams with infrastructure and tooling, or apply AI within a specific domain.

Typical titles:
- Software Engineer (AI team)
- Backend Engineer — AI Platform
- Full-Stack Engineer — AI Products
- Data Engineer — AI/ML
- Platform Engineer — AI Infrastructure
- DevOps Engineer — AI Systems
- Solutions Architect — AI
- Technical Program Manager — AI

These roles need AI literacy but their primary expertise is in traditional software engineering. They build the scaffolding that AI systems run on.

### Machine Learning: 20 jobs (1.7%)

These are **traditional ML roles** that have adopted some AI Engineering vocabulary but remain focused on model training, custom architectures, and ML pipelines.

Typical titles:
- Machine Learning Engineer
- ML Research Engineer
- Applied ML Scientist
- Computer Vision Engineer
- NLP Engineer

This category has shrunk from ~2.5% in 2025 to 1.7% in 2026, not because ML roles are disappearing, but because most new roles that would have been "ML Engineer" three years ago are now being hired as "AI Engineer" — even when the work involves significant model training.

---

## Skills Analysis

### Top GenAI Skills

| Skill | Mentions | % of Jobs | Trend |
|---|---|---|---|
| RAG (Retrieval-Augmented Generation) | 482 | 40.2% | ↑ (+2.1pp) |
| Prompt Engineering | 378 | 31.5% | ↓ (-2.8pp) |
| LLMs (General) | 346 | 28.8% | → (stable) |
| LangChain | 229 | 19.1% | ↓ (-3.5pp) |
| Agents / Agentic AI | 224 | 18.7% | ↑ (+6.2pp) |
| OpenAI API | 122 | 10.2% | ↓ (-4.1pp) |
| LangGraph | 118 | 9.8% | ↑ (+4.3pp) |
| Anthropic API | 85 | 7.1% | ↑ (+2.9pp) |
| LlamaIndex | 74 | 6.2% | ↓ (-1.8pp) |
| MCP (Model Context Protocol) | 70 | 5.8% | ↑ (+5.8pp, NEW) |
| Google ADK (Agent Development Kit) | 47 | 3.9% | ↑ (+3.9pp, NEW) |
| Claude Agent SDK | 38 | 3.2% | ↑ (+3.2pp, NEW) |
| SmolAgents | 22 | 1.8% | ↑ (+1.8pp, NEW) |
| PydanticAI | 18 | 1.5% | ↑ (+1.5pp, NEW) |

**Key observations:**

1. **RAG remains king** — 40.2% of all roles mention RAG, making it the single most important GenAI skill. This has been consistent since 2024 and shows no sign of changing. Every enterprise AI system needs to access proprietary data, and RAG is still the primary pattern for doing so.

2. **Prompt engineering is declining as a standalone skill** — Down from 34.3% to 31.5%. This doesn't mean prompting is less important; it means prompting has become so fundamental that it's assumed rather than listed. It's like listing "can write functions" as a skill for a software engineer.

3. **Agents are the biggest mover** — Up from 12.5% to 18.7% (+6.2pp), the largest year-over-year increase of any skill. The agent wave is real in hiring.

4. **LangChain is declining** — Down from 22.6% to 19.1%. The ecosystem is fragmenting. LangGraph is cannibalizing LangChain for agent workflows, and newer frameworks (CrewAI, SmolAgents, PydanticAI) are taking mindshare.

5. **MCP is the fastest new entrant** — At 5.8% in its first year of significant measurement, MCP has appeared faster than any protocol skill since REST APIs. This reflects the industry's push toward standardized tool integration.

6. **Provider-agnostic framing is growing** — "LLMs (General)" at 28.8% exceeds any single provider API. Companies increasingly want engineers who can work across OpenAI, Anthropic, Google, and others rather than being locked into one provider.

### Agent Frameworks: The 2026 Landscape

The agent framework space has exploded in 2026. Here's how the major players stack up in job postings:

| Framework | Mentions | Positioning | Best For |
|---|---|---|---|
| LangGraph | 118 | Graph-based agent orchestration | Complex multi-step workflows, production agents |
| OpenAI Agents SDK | 52 | Official OpenAI agent framework | OpenAI-centric stacks, simple-to-moderate agents |
| Google ADK | 47 | Google's agent development kit | Gemini-centric stacks, Google Cloud deployments |
| CrewAI | 44 | Multi-agent role-playing | Multi-agent systems with distinct personas |
| Claude Agent SDK | 38 | Anthropic's agent framework | Claude-centric stacks, tool-use-heavy agents |
| SmolAgents | 22 | HuggingFace's lightweight agents | Research, prototyping, minimal overhead |
| AutoGen | 19 | Microsoft's multi-agent framework | Enterprise, Azure integrations |
| PydanticAI | 18 | Type-safe agent development | Python-first, validation-heavy workflows |
| Semantic Kernel | 14 | Microsoft's enterprise AI SDK | .NET/enterprise environments |

**Takeaway:** No agent framework has achieved dominance. LangGraph leads but isn't the default choice the way LangChain was for RAG in 2024. The market is still fragmenting, and most roles don't specify a particular framework — they ask for "agent experience" generically.

### Protocol Skills

| Protocol | Mentions | % of Jobs | Notes |
|---|---|---|---|
| MCP (Model Context Protocol) | 70 | 5.8% | Fastest-growing new skill; standard for tool/context integration |
| A2A (Agent-to-Agent Protocol) | 28 | 2.3% | Emerging; standard for inter-agent communication |

MCP and A2A represent a new skill category: **protocol literacy**. Like REST API literacy became table stakes for web developers in the 2010s, MCP/A2A literacy is becoming essential for AI Engineers. Understanding these protocols — how to implement MCP servers, how to configure tool definitions, how to structure A2A message passing — is a differentiator in 2026 hiring.

### Top ML Skills

| Skill | Mentions | % of Jobs | Notes |
|---|---|---|---|
| PyTorch | 286 | 23.8% | Still dominant for model work |
| TensorFlow | 168 | 14.0% | Declining but persistent |
| Fine-tuning | 198 | 16.5% | Growing — especially LoRA/QLoRA |
| Model Training | 132 | 11.0% | Often for smaller/specialized models |
| Model Evaluation | 156 | 13.0% | Eval skills are in high demand |
| scikit-learn | 144 | 12.0% | Workhorse for non-deep ML |
| Embeddings | 168 | 14.0% | Critical for RAG and similarity search |
| LoRA / QLoRA | 96 | 8.0% | Efficient fine-tuning, growing fast |
| PEFT (Parameter-Efficient Fine-Tuning) | 72 | 6.0% | Broader category including LoRA |
| Hugging Face | 132 | 11.0% | Model hub and inference |
| ONNX | 48 | 4.0% | Model optimization and portability |
| vLLM | 42 | 3.5% | High-throughput inference serving |

**ML knowledge is not optional.** 68.3% of AI Engineering roles require at least some ML knowledge, and the depth required is increasing. You don't need to train GPT-5 from scratch, but you need to understand:

- How embeddings work and why they matter
- What fine-tuning does and when to use it vs. RAG
- How to evaluate model quality (beyond "looks good to me")
- What training data quality means and why it affects your system
- How model architectures influence behavior and capabilities

The rise of LoRA/QLoRA (8.0%, up from 4.2% in 2025) reflects a key trend: more companies are doing lightweight fine-tuning rather than just prompt engineering. As fine-tuning becomes more accessible, AI Engineers need to know when and how to apply it.

### Evaluation Skills: A Critical Growth Area

| Tool / Skill | Mentions | % of Jobs | Notes |
|---|---|---|---|
| Ragas | 62 | 5.2% | RAG-specific evaluation |
| DeepEval | 48 | 4.0% | LLM evaluation framework |
| Braintrust | 36 | 3.0% | Evaluation and experiment tracking |
| Custom eval frameworks | 84 | 7.0% | Most common — build your own |
| Human evaluation / annotation | 66 | 5.5% | Still essential for quality |
| A/B testing for AI | 54 | 4.5% | Production evaluation method |
| Red-teaming | 30 | 2.5% | Safety and adversarial testing |

Evaluation has emerged as the **single most important differentiator** between junior and senior AI Engineers. The ability to design, implement, and maintain robust evaluation systems is what separates "I built a demo" from "I shipped a product."

In 2026, the evaluation landscape is still fragmented. Ragas dominates RAG evaluation, DeepEval is gaining ground for general LLM eval, and Braintrust is the emerging choice for experiment tracking. But 7.0% of roles mention building custom evaluation frameworks — more than any single tool — which tells you the space hasn't consolidated yet.

### AI Observability Tools

| Tool | Mentions | % of Jobs | Notes |
|---|---|---|---|
| LangSmith | 78 | 6.5% | LangChain ecosystem, tracing and eval |
| LangFuse | 66 | 5.5% | Open-source, growing rapidly |
| Arize | 42 | 3.5% | ML/AI observability platform |
| Phoenix (Arize) | 30 | 2.5% | Open-source LLM observability |
| Weights & Biases | 54 | 4.5% | Experiment tracking, now with LLM support |
| Helicone | 18 | 1.5% | LLM proxy and monitoring |
| Promptlayer | 12 | 1.0% | Prompt management and logging |

Observability has graduated from "nice to have" to "production requirement." In 2025, many teams shipped AI systems without proper monitoring. In 2026, the hiring data shows that observability skills are explicitly requested, with LangSmith and LangFuse leading the pack.

### Top Web/Software Engineering Skills

| Skill | Mentions | % of Jobs | Notes |
|---|---|---|---|
| React | 192 | 16.0% | Frontend for AI-powered interfaces |
| FastAPI | 180 | 15.0% | Python API framework of choice |
| APIs (REST/GraphQL) | 240 | 20.0% | Fundamental for integration |
| Next.js | 108 | 9.0% | Full-stack React framework |
| Node.js | 96 | 8.0% | Backend JavaScript |
| TypeScript | 156 | 13.0% | Type-safe JavaScript |
| WebSockets | 48 | 4.0% | Real-time AI streaming |

AI Engineers aren't just API callers — they're software engineers. The 20% mentioning APIs and 16% mentioning React reflect a reality: AI Engineers often build the entire feature, from model call to user interface. FastAPI at 15% reflects the Python-dominant AI stack.

### Top Database Skills

| Skill | Mentions | % of Jobs | Notes |
|---|---|---|---|
| Vector Databases (General) | 312 | 26.0% | Required for RAG |
| PostgreSQL | 216 | 18.0% | Versatile, now with pgvector |
| Pinecone | 132 | 11.0% | Managed vector DB |
| Redis | 108 | 9.0% | Caching, sessions, vector search |
| Weaviate | 96 | 8.0% | Open-source vector DB |
| Qdrant | 84 | 7.0% | Rust-based vector DB, growing |
| pgvector | 78 | 6.5% | PostgreSQL vector extension |
| MongoDB | 72 | 6.0% | Document store, Atlas Vector Search |
| Chroma | 60 | 5.0% | Lightweight embedding DB |
| Milvus | 42 | 3.5% | Scalable vector DB |
| Elasticsearch | 66 | 5.5% | Search + vector hybrid |
| Neo4j | 36 | 3.0% | Graph database for knowledge graphs |

Vector databases remain the #1 database skill for AI Engineers, cited in 26% of roles. But the landscape is shifting:

- **pgvector is the breakout story** — At 6.5% and growing fast, PostgreSQL with pgvector is becoming the default choice for teams that already use Postgres. Why add a new database when you can add vector search to your existing one?
- **Pinecone leads managed offerings** — Still the most-mentioned managed vector DB, but Qdrant (7.0%) is catching up among teams that want open-source.
- **Hybrid search is the norm** — More roles mention combining traditional search (Elasticsearch) with vector search, reflecting the industry consensus that pure vector search isn't sufficient.

### Top Cloud Skills

| Platform | Mentions | % of Jobs | Key Services |
|---|---|---|---|
| AWS | 420 | 35.0% | Bedrock, SageMaker, OpenSearch, Lambda |
| Azure | 265 | 22.1% | Azure OpenAI, AI Studio, Cognitive Services |
| GCP | 252 | 21.0% | Vertex AI, Gemini API, Cloud Run |

AWS maintains its lead, but the gap with GCP is narrowing. GCP's 14.5% year-over-year growth in mentions (compared to AWS's 10.5%) reflects Gemini's rising popularity and Vertex AI's maturation.

**Cloud AI services are becoming a distinct skill category:**

| Service | Platform | Mentions | Notes |
|---|---|---|---|
| AWS Bedrock | AWS | 96 | Multi-model access, growing fast |
| Azure OpenAI Service | Azure | 108 | Enterprise OpenAI deployments |
| Vertex AI | GCP | 84 | Gemini + custom model hosting |
| SageMaker | AWS | 72 | Traditional ML + new AI features |
| AWS Lambda | AWS | 66 | Serverless AI inference |
| Cloud Run | GCP | 48 | Containerized AI deployments |

### Top Ops/DevOps Skills

| Skill | Mentions | % of Jobs | Notes |
|---|---|---|---|
| Docker | 264 | 22.0% | Containerization is table stakes |
| CI/CD | 216 | 18.0% | Automated deployment pipelines |
| Kubernetes | 180 | 15.0% | Container orchestration at scale |
| MLOps | 144 | 12.0% | ML-specific ops practices |
| Terraform | 120 | 10.0% | Infrastructure as code |
| GitHub Actions | 108 | 9.0% | CI/CD for AI workflows |
| MLflow | 96 | 8.0% | Experiment and model tracking |
| Helm | 48 | 4.0% | Kubernetes package management |
| Airflow | 60 | 5.0% | Workflow orchestration |

The MLOps category at 12% reflects a key insight: deploying AI systems requires ops practices that go beyond traditional DevOps. Model versioning, prompt versioning, A/B testing for model outputs, and evaluation-in-the-loop deployment are all MLOps concerns that traditional CI/CD doesn't cover.

### Top Programming Languages

| Language | Mentions | % of Jobs | Primary Use in AI Engineering |
|---|---|---|---|
| Python | 1,008 | 84.0% | Dominant — SDKs, frameworks, data processing, ML |
| TypeScript | 312 | 26.0% | Frontend + Node.js backend for AI features |
| Java | 168 | 14.0% | Enterprise backends, big data pipelines |
| Go | 132 | 11.0% | High-performance services, infrastructure |
| SQL | 120 | 10.0% | Data querying, analytics, vector search |
| Rust | 48 | 4.0% | Performance-critical components, vector DBs |
| C++ | 36 | 3.0% | Inference optimization, custom kernels |
| Julia | 12 | 1.0% | Scientific computing, niche |

Python's dominance at 84% is essentially unchanged from 2025 (83%). The AI ecosystem is built on Python, and that's not changing. The more interesting story is TypeScript at 26% — up from 22% in 2025 — reflecting the growing number of AI Engineers who also build web interfaces.

Go at 11% reflects its use in infrastructure services (MCP servers, proxy layers, high-throughput API gateways). Rust at 4% is small but growing, particularly in vector database internals and inference optimization.

### Context Engineering as a Skill

Context engineering has emerged as a distinct skill category in 2026 job postings:

| Context Engineering Sub-skill | Mentions | % of Jobs |
|---|---|---|
| Context window management | 48 | 4.0% |
| Prompt design and optimization | 264 | 22.0% |
| Retrieval strategy design | 132 | 11.0% |
| Conversation state management | 42 | 3.5% |
| Token budget optimization | 30 | 2.5% |
| Multi-modal context composition | 24 | 2.0% |
| MCP server implementation | 56 | 4.7% |
| Context for agent systems | 72 | 6.0% |

While "context engineering" as an explicit term appears in only ~3% of postings, the sub-skills that comprise it appear in over 40% of postings. The industry is recognizing the discipline even before the terminology has fully standardized.

---

## The Typical AI Engineering Stack (2026)

Based on the most frequently co-occurring skills in job descriptions, here's the typical AI Engineering stack:

### Core AI Layer
```
Language: Python 3.11+
LLM Access: OpenAI API / Anthropic API / Google Gemini API
Orchestration: LangChain + LangGraph OR custom framework
Agent Framework: LangGraph, OpenAI Agents SDK, or Google ADK
Protocol: MCP for tool integration, A2A for agent communication
```

### Retrieval Layer
```
Embeddings: OpenAI text-embedding-3-large or open-source (BGE, E5)
Vector DB: Pinecone (managed) or pgvector (self-managed)
Search: Hybrid (vector + keyword/BM25)
Re-ranking: Cohere Rerank or cross-encoder models
Document Processing: Unstructured.io, LlamaParse, or custom pipelines
```

### Evaluation Layer
```
Framework: Ragas (RAG eval), DeepEval (general LLM eval), or custom
Experiment Tracking: Braintrust or Weights & Biases
Human Annotation: Custom tooling or Scale AI / Labelbox
A/B Testing: Custom implementation or Statsig / LaunchDarkly
```

### Observability Layer
```
Tracing: LangSmith or LangFuse
Monitoring: Arize / Phoenix or Datadog
Logging: Structured JSON logging with OpenTelemetry
Cost Tracking: Helicone or custom
```

### Infrastructure Layer
```
API: FastAPI
Frontend: React + Next.js
Database: PostgreSQL (with pgvector) + Redis
Cloud: AWS (Bedrock, Lambda, SageMaker) or Azure (OpenAI Service) or GCP (Vertex AI)
Containers: Docker + Kubernetes
CI/CD: GitHub Actions + Terraform
```

---

## Fine-Tuning Requirements in 2026

Fine-tuning is no longer a niche skill — it's appearing in 16.5% of AI Engineering roles, up from 12.8% in 2025. Here's what's driving the trend:

### When Job Postings Mention Fine-Tuning

| Scenario | Frequency | What They Mean |
|---|---|---|
| LoRA/QLoRA for domain adaptation | 65% | Lightweight fine-tuning on domain-specific data |
| Fine-tuning for specific tasks | 20% | Full or partial fine-tuning for well-defined tasks |
| Fine-tuning infrastructure | 10% | Building platforms that enable others to fine-tune |
| Research-oriented fine-tuning | 5% | Novel methods, architecture exploration |

### Fine-Tuning Skills Breakdown

| Skill | Mentions | % of Fine-Tuning Roles | Notes |
|---|---|---|---|
| LoRA / QLoRA | 96 | 48.0% | Dominant approach — efficient and practical |
| PEFT | 72 | 36.0% | Broader parameter-efficient methods |
| Supervised Fine-Tuning (SFT) | 84 | 42.0% | Standard approach for task-specific tuning |
| RLHF / DPO | 48 | 24.0% | Alignment-focused fine-tuning |
| Data preparation for fine-tuning | 66 | 33.0% | Dataset curation, cleaning, formatting |
| Fine-tuning evaluation | 54 | 27.0% | Measuring fine-tuning quality and regression |
| Quantization (GPTQ, AWQ) | 36 | 18.0% | Post-training optimization |
| vLLM / TGI for serving | 42 | 21.0% | Serving fine-tuned models efficiently |

The key insight: most fine-tuning in 2026 is **lightweight and task-specific**, not training from scratch. LoRA/QLoRA dominates because it's practical — you can fine-tune a model on a single GPU in hours rather than needing a cluster for days.

---

## Evaluation Skills: Deep Dive

Evaluation has become the **defining skill of senior AI Engineers**. Here's a detailed breakdown of what's expected:

### Evaluation Skill Hierarchy

| Level | Skills | What You Can Do |
|---|---|---|
| **Junior** | Basic metrics, manual testing, simple test sets | Can tell if a system is "obviously broken" |
| **Mid** | Structured eval datasets, automated metrics, A/B testing | Can measure quality systematically and detect regressions |
| **Senior** | Custom eval frameworks, human annotation pipelines, statistical rigor | Can design evaluation systems that the team trusts for production decisions |
| **Staff+** | Eval-driven development culture, org-wide eval standards, novel metrics | Can establish evaluation practices that scale across teams and products |

### Evaluation Method Skills

| Method | When to Use | Complexity | Adoption |
|---|---|---|---|
| Exact match / F1 | Classification, extraction | Low | Very high |
| LLM-as-judge | Open-ended generation, quality rating | Medium | Very high |
| RAG-specific metrics (faithfulness, relevance) | RAG systems | Medium | High |
| Human evaluation | Final quality gate, subjective tasks | High | High |
| A/B testing with users | Production optimization | High | Medium |
| Red-teaming / adversarial testing | Safety, robustness | Very high | Low |
| Regression testing | Every prompt/model change | Medium | Growing |
| Statistical significance testing | Comparing model versions | Medium | Medium |

### The Evaluation Tool Landscape

```
┌─────────────────────────────────────────────────────────┐
│                  Evaluation Stack 2026                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  RAG Evaluation ──────── Ragas (faithfulness, context    │
│                          recall, answer relevancy)        │
│                                                          │
│  General LLM Eval ────── DeepEval (metric library,       │
│                          test cases, integration)         │
│                                                          │
│  Experiment Tracking ─── Braintrust (evals + prompts +    │
│                          datasets in one place)           │
│                                                          │
│  LLM-as-Judge ────────── Custom prompts + structured      │
│                          output (most common approach)    │
│                                                          │
│  Human Annotation ────── Scale AI, Labelbox, or custom    │
│                          internal tools                   │
│                                                          │
│  Production Eval ─────── A/B testing frameworks +         │
│                          observability dashboards         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Skill Comparison: 2025 vs. 2026

### Skills That Grew Significantly

| Skill | 2025 % | 2026 % | Change | Driver |
|---|---|---|---|---|
| Agents / Agentic AI | 12.5% | 18.7% | +6.2pp | Agent wave across industry |
| LangGraph | 5.5% | 9.8% | +4.3pp | Agent orchestration standard |
| Anthropic API | 4.2% | 7.1% | +2.9pp | Claude's enterprise growth |
| MCP | 0% | 5.8% | +5.8pp | New protocol adoption |
| LoRA/QLoRA | 4.2% | 8.0% | +3.8pp | Accessible fine-tuning |
| Evaluation (general) | 8.5% | 13.0% | +4.5pp | Production quality demands |
| Context engineering | 0% | ~3% | +3pp | New discipline recognition |
| Google ADK | 0% | 3.9% | +3.9pp | Google's agent push |
| Claude Agent SDK | 0% | 3.2% | +3.2pp | Anthropic's agent framework |
| LangFuse | 2.5% | 5.5% | +3.0pp | Open-source observability |
| pgvector | 2.8% | 6.5% | +3.7pp | Postgres-native vector search |

### Skills That Declined

| Skill | 2025 % | 2026 % | Change | Reason |
|---|---|---|---|---|
| Prompt Engineering | 34.3% | 31.5% | -2.8pp | Assumed skill, not listed separately |
| LangChain | 22.6% | 19.1% | -3.5pp | Ecosystem fragmentation |
| OpenAI API | 14.3% | 10.2% | -4.1pp | Multi-provider strategy becoming norm |
| LlamaIndex | 8.0% | 6.2% | -1.8pp | Competition from custom RAG pipelines |
| TensorFlow | 17.5% | 14.0% | -3.5pp | PyTorch dominance continues |
| Streamlit | 5.0% | 3.0% | -2.0pp | Demos moving to proper frontends |

### Skills That Remained Stable

| Skill | 2025 % | 2026 % | Change |
|---|---|---|---|
| RAG | 38.1% | 40.2% | +2.1pp |
| LLMs (General) | 28.5% | 28.8% | +0.3pp |
| Python | 83.0% | 84.0% | +1.0pp |
| PostgreSQL | 17.5% | 18.0% | +0.5pp |
| Docker | 21.5% | 22.0% | +0.5pp |

---

## The Skill Cluster Map

Skills don't exist in isolation. Here's how they cluster in job postings:

### Cluster 1: RAG Engineer
```
RAG + Vector Databases + Embeddings + LangChain/LlamaIndex + 
Pinecone/pgvector/Qdrant + Ragas + Document Processing
```
*This is the most common skill cluster, appearing in ~35% of roles.*

### Cluster 2: Agent Engineer
```
Agents + LangGraph + MCP + Tool Use + Planning + Memory + 
OpenAI Agents SDK or Claude Agent SDK or Google ADK
```
*Fastest-growing cluster, appearing in ~18% of roles.*

### Cluster 3: AI Platform Engineer
```
Docker + Kubernetes + CI/CD + Terraform + MLOps + Cloud (AWS/Azure/GCP) +
Model Serving + Monitoring + LangSmith/LangFuse
```
*Appearing in ~15% of roles, focused on infrastructure.*

### Cluster 4: Full-Stack AI Engineer
```
React + FastAPI + Next.js + TypeScript + Python + LLM APIs +
Vector DB + Simple RAG
```
*Appearing in ~12% of roles, especially at startups.*

### Cluster 5: AI Evaluation Engineer
```
Ragas + DeepEval + Braintrust + A/B Testing + Human Annotation +
Statistical Analysis + Custom Eval Frameworks
```
*Appearing in ~8% of roles, growing rapidly.*

### Cluster 6: Context Engineer
```
MCP + Prompt Design + Retrieval Strategy + Token Optimization +
Conversation State + Agent Context + Knowledge Graphs
```
*Emerging cluster, appearing in ~5% of roles.*

---

## Dataset Statistics

### Source and Methodology

| Parameter | Value |
|---|---|
| Total job descriptions analyzed | 1,247 |
| Collection period | April 1 — May 15, 2026 |
| Sources | LinkedIn (42%), Indeed (18%), company career pages (22%), Wellfound (8%), other (10%) |
| Geographic scope | Primarily US (68%), EU (18%), APAC (9%), Other (5%) |
| Company sizes | Startup <50 (22%), Mid 50-500 (35%), Large 500-5000 (25%), Enterprise >5000 (18%) |
| Deduplication | Similar postings from same company within 7 days merged |
| Skill extraction | NER + manual validation (92% precision, 88% recall) |

### Distribution by Company Size

| Company Size | AI-First | AI-Support | ML | Total |
|---|---|---|---|---|
| Startup (<50) | 185 | 42 | 2 | 229 |
| Mid (50-500) | 302 | 108 | 6 | 416 |
| Large (500-5000) | 228 | 96 | 7 | 331 |
| Enterprise (>5000) | 155 | 64 | 5 | 224 |
| **Total** | **870** | **310** | **20** | **1,200** |

### Distribution by Industry

| Industry | % of Postings | Top Skills |
|---|---|---|
| Technology / SaaS | 32% | RAG, agents, full-stack |
| Financial Services | 14% | RAG, compliance, safety |
| Healthcare / Biotech | 10% | RAG, domain adaptation, safety |
| Consulting / Services | 9% | Full-stack, RAG, deployment |
| E-commerce / Retail | 8% | Personalization, RAG, recsys |
| Cybersecurity | 5% | Agents, real-time, safety |
| Education / EdTech | 4% | RAG, content generation, eval |
| Manufacturing | 3% | RAG, computer vision, edge |
| Legal / Regulatory | 3% | RAG, accuracy, compliance |
| Government / Defense | 2% | Safety, compliance, on-premise |
| Other | 10% | Mixed |

---

## The 2026 AI Engineer Skill Profile

Based on all the data, here's the composite skill profile for a 2026 AI Engineer:

### Must-Have (95%+ of roles)
- Python
- LLM API usage (at least one provider)
- Software engineering fundamentals
- Basic ML understanding

### Very Common (60-95% of roles)
- RAG architecture and implementation
- Prompt engineering / context engineering
- Vector database experience
- API development (FastAPI or similar)
- Evaluation mindset (even if no specific framework)
- Cloud platform experience (AWS, Azure, or GCP)

### Common (30-60% of roles)
- Agent system design
- Docker / containerization
- Production deployment experience
- Fine-tuning (LoRA/QLoRA)
- LangChain or LangGraph
- SQL / database management

### Nice-to-Have (10-30% of roles)
- MCP implementation
- Specific eval frameworks (Ragas, DeepEval)
- Observability tools (LangSmith, LangFuse)
- Frontend development (React, Next.js)
- Kubernetes
- A2A protocol
- Specific agent SDK (OpenAI, Claude, Google ADK)
- Knowledge graphs

### Specialized (<10% of roles)
- Training models from scratch
- Reinforcement learning
- Custom model architectures
- On-premise deployment
- Specific vector DB expertise
- Rust / C++ for performance
- Regulatory compliance (EU AI Act)

---

## Key Takeaways

1. **RAG remains the #1 AI Engineering skill** — 40.2% of all roles. If you can build production RAG systems, you're employable.

2. **Agents are the biggest growth area** — From 12.5% to 18.7% in one year. This is where the most job growth is happening.

3. **Evaluation is the senior differentiator** — The ability to design and run evaluation systems is what separates senior from junior AI Engineers.

4. **The framework landscape is fragmenting** — No single framework dominates. Versatility across frameworks matters more than deep expertise in one.

5. **Protocol skills are emerging** — MCP and A2A are new but growing fast. Early investment here pays off.

6. **ML knowledge is not optional** — 68.3% of roles require some ML knowledge. You don't need a PhD, but you need to understand embeddings, fine-tuning, and evaluation.

7. **Context engineering is the new discipline** — Not yet a standard job title, but the sub-skills appear in 40%+ of postings. This is the next "prompt engineering" — the term that captures what everyone's already doing.

8. **Python remains dominant but TypeScript is growing** — The full-stack AI Engineer who writes both Python backend and TypeScript frontend is increasingly valued.

9. **pgvector is the vector DB breakout** — PostgreSQL with pgvector is eating the vector DB market from the inside. If you already use Postgres, there's less reason to add a separate vector DB.

10. **The cloud AI services race is real** — AWS Bedrock, Azure OpenAI Service, and GCP Vertex AI are all growing. Multi-cloud AI skills are becoming valuable.
