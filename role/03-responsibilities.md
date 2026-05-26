# AI Engineering Responsibilities in 2026

*Based on analysis of 6,200+ responsibilities extracted from 1,200+ job descriptions, April-May 2026*

## Overview

When companies write job postings for AI Engineers, what do they actually ask them to do? We extracted and categorized 6,200+ individual responsibility statements to find out. The results reveal a role that's far more diverse than "call the API and ship it" — and far more demanding than most people outside the field realize.

Responsibilities fall into a clear frequency distribution: a handful of core activities that appear in most postings, a larger set of common but not universal duties, and a long tail of specialized responsibilities that reflect the diversity of AI applications across industries.

---

## Very Common (Appears in 50%+ of Job Postings)

These are the responsibilities that define AI Engineering as a discipline. If you're an AI Engineer, you're doing most of these regularly.

### Building AI Systems

**Frequency: ~78% of postings**

This is the bread and butter. AI Engineers build AI-powered systems — RAG pipelines, chatbots, agent workflows, evaluation systems, and generative applications (text, image, vision). The specific system varies, but the core activity is the same: take a user need, design an AI-powered solution, and implement it end to end.

Common variations:
- **RAG systems** — The most common AI system type. Document ingestion, embedding, retrieval, generation, citation tracking. Most AI Engineers will build at least one RAG system in their career.
- **Conversational AI** — Chatbots, virtual assistants, and dialogue systems. These range from simple FAQ bots to complex multi-turn reasoning assistants.
- **Agent systems** — Autonomous or semi-autonomous AI agents that use tools, plan multi-step actions, and interact with external systems. Growing rapidly in 2026.
- **Generative vision** — Image generation, image understanding, multimodal systems. Less common than text-only systems but growing with the availability of vision-capable models.
- **Evaluation systems** — Building the infrastructure to measure AI output quality. This is a meta-responsibility: AI Engineers build systems to evaluate AI systems.

What this looks like day-to-day:
- Designing system architecture for a new AI feature
- Writing prompt chains and retrieval logic
- Implementing tool integrations for agent systems
- Building MCP servers to connect AI systems to company data
- Creating evaluation datasets and running quality tests
- Debugging why the model produced an unexpected output

### Productionizing AI

**Frequency: ~65% of postings**

Getting an AI system working in a notebook is one thing. Making it work reliably in production is another thing entirely. Productionizing AI covers deployment, monitoring, on-call, scaling, and all the operational concerns that turn a prototype into a product.

Common responsibilities:
- **Deployment** — Containerizing AI systems, setting up CI/CD pipelines, managing model versioning, deploying to cloud infrastructure (AWS, Azure, GCP)
- **Monitoring** — Setting up dashboards for latency, error rates, token usage, cost, and output quality. Using tools like LangSmith, LangFuse, Arize, or Phoenix.
- **On-call** — Being the person who gets paged when the AI system goes down or starts producing garbage. AI on-call is harder than traditional on-call because the failure modes are more subtle — the system doesn't crash, it just gets worse.
- **Scaling** — Handling increased traffic, optimizing inference costs, managing rate limits across LLM providers, implementing caching strategies
- **Incident response** — When an AI system produces harmful output, hallucinates critical information, or goes off the rails, AI Engineers need to diagnose and fix the issue quickly

The production challenge in 2026:
- LLM APIs have gotten more reliable, but they still have outages, latency spikes, and silent behavior changes
- Model updates from providers can silently change output quality
- Cost management is an ongoing concern as usage scales
- Regulatory requirements (EU AI Act, etc.) add compliance overhead to deployment

### Evaluation and Quality

**Frequency: ~58% of postings**

Evaluation has become a first-class responsibility, not an afterthought. AI Engineers are expected to design evaluation frameworks, implement quality metrics, and ensure their systems meet quality standards.

Common responsibilities:
- **Building evaluation frameworks** — Creating structured approaches to measure AI output quality across dimensions like accuracy, relevance, completeness, safety, and coherence
- **Implementing safety guardrails** — Input validation, output filtering, content policy enforcement, PII detection and redaction
- **Hallucination detection** — Identifying when the model generates factually incorrect or unsupported information. This is particularly critical for RAG systems where citation fidelity matters
- **Bias assessment** — Testing for and mitigating biases in AI outputs across demographic groups, geographies, and use cases
- **Human-in-the-loop systems** — Designing workflows where human reviewers validate, correct, or override AI outputs before they reach end users
- **Regression testing** — Running evaluation suites after every prompt change, model update, or system modification to catch quality degradation
- **A/B testing** — Comparing different prompts, models, or retrieval strategies with real users to make data-driven quality decisions

The evaluation stack in 2026:
```
Automated Metrics (Ragas, DeepEval)
        ↓
LLM-as-Judge (structured evaluation prompts)
        ↓
Human Annotation (domain experts, Scale AI, internal)
        ↓
User Feedback (thumbs up/down, corrections, escalation)
        ↓
Production Monitoring (drift detection, quality alerts)
```

### Using Provider APIs

**Frequency: ~55% of postings**

AI Engineers work extensively with LLM provider APIs — OpenAI, Anthropic, Google, Mistral, and others. This isn't just "calling the API"; it's about understanding model capabilities, managing provider relationships, and building systems that work reliably across providers.

Common responsibilities:
- **Model selection** — Choosing the right model for each task (GPT-4o for complex reasoning, GPT-4o-mini for simple tasks, Claude for nuanced analysis, Gemini for multimodal)
- **API integration** — Implementing robust API clients with retry logic, rate limiting, fallback strategies, and error handling
- **Model routing** — Directing requests to different models based on task complexity, cost constraints, and performance requirements
- **Provider management** — Staying on top of model updates, deprecations, new features, and pricing changes across multiple providers
- **Multi-provider architectures** — Building systems that aren't locked into a single provider, enabling flexibility and risk mitigation

Provider landscape in 2026:
| Provider | Key Models | Differentiator |
|---|---|---|
| OpenAI | GPT-4o, GPT-4o-mini, o3, o4-mini | Broadest adoption, most tooling |
| Anthropic | Claude Sonnet 4, Claude Opus 4, Claude Haiku | Safety focus, long context, nuance |
| Google | Gemini 2.5 Pro, Gemini 2.5 Flash | Multimodal, Vertex AI integration |
| Mistral | Mistral Large, Mistral Medium | European, open-weight options |
| Meta | Llama 4 (via hosted APIs) | Open-weight, self-hostable |

---

## Common (Appears in 25-50% of Job Postings)

These responsibilities appear frequently but aren't universal. They tend to cluster by company type, industry, and team structure.

### RAG and Retrieval

**Frequency: ~48% of postings**

RAG is so important that it deserves its own responsibility category beyond "Building AI Systems." The retrieval layer is often the most complex and failure-prone part of an AI system, and many AI Engineers spend the majority of their time on retrieval-related work.

Common responsibilities:
- **Document processing** — Ingesting documents in various formats (PDF, HTML, Markdown, DOCX, images), extracting text, handling tables and figures, maintaining document structure
- **Chunking strategy** — Deciding how to split documents into retrievable chunks (fixed-size, semantic, recursive, document-structure-aware) and tuning chunk sizes for optimal retrieval
- **Embedding selection and optimization** — Choosing embedding models, benchmarking embedding quality, fine-tuning embeddings for domain-specific vocabulary
- **Vector search implementation** — Setting up and tuning vector databases (Pinecone, Weaviate, Qdrant, pgvector), configuring index types and parameters
- **Hybrid search** — Combining vector search with keyword search (BM25), implementing reciprocal rank fusion or other combination strategies
- **Query rewriting** — Transforming user queries to improve retrieval: query expansion, decomposition, hypothetical document embeddings (HyDE)
- **Re-ranking** — Using cross-encoder models or LLM-based re-ranking to improve retrieval precision after initial vector search
- **Knowledge graphs** — Building and querying graph-structured knowledge bases for relationship-aware retrieval, especially useful for complex domains
- **Citation tracking** — Ensuring generated responses accurately reference their source documents, building citation verification systems

The RAG quality challenge:
```
Raw Query → Query Rewriting → Retrieval → Re-ranking → 
Context Assembly → Generation → Citation Verification → Response

Each step introduces potential failure:
- Query rewriting can misinterpret intent
- Retrieval can miss relevant documents
- Re-ranking can demote important results
- Context assembly can lose critical information
- Generation can hallucinate or misrepresent sources
- Citation verification can fail to catch errors
```

### Data Processing

**Frequency: ~38% of postings**

AI systems are data-hungry, and someone needs to feed them. Data processing responsibilities cover the pipelines that transform raw data into the formats AI systems need.

Common responsibilities:
- **Building data pipelines** — ETL workflows that ingest, clean, transform, and deliver data to AI systems. Airflow, Prefect, or custom orchestration.
- **Data transformation** — Converting data between formats, normalizing text, handling encoding issues, deduplicating records
- **Dataset management** — Curating and versioning evaluation datasets, training datasets (for fine-tuning), and knowledge bases (for RAG)
- **Data quality** — Monitoring data quality over time, detecting drift in input distributions, flagging data issues that could affect AI performance
- **Annotation pipeline management** — Managing workflows for human annotators, ensuring annotation quality, resolving disagreements

Data processing in 2026 increasingly involves:
- **Unstructured data processing** — PDFs, images, audio, video. Tools like Unstructured.io and LlamaParse have matured significantly.
- **Multi-modal data pipelines** — Processing text, images, and structured data together for multimodal AI systems
- **Real-time data pipelines** — Streaming data to AI systems that need up-to-the-minute information (stock prices, news, sensor data)

### Collaboration and Communication

**Frequency: ~35% of postings**

AI Engineers don't work in isolation. The cross-functional nature of AI — spanning product, engineering, data, design, legal, and domain experts — means collaboration skills are essential.

Common responsibilities:
- **Cross-functional collaboration** — Working with product managers to define AI features, designers to craft AI-powered UX, domain experts to validate AI outputs, and legal/compliance to ensure regulatory adherence
- **Stakeholder management** — Communicating AI capabilities and limitations to non-technical stakeholders, managing expectations about what AI can and cannot do
- **Technical leadership** — Leading architectural decisions for AI systems, mentoring junior engineers, establishing best practices for the team
- **Documentation** — Writing technical specs, architecture docs, runbooks, and post-mortems. AI systems need especially thorough documentation because their behavior is harder to understand from code alone.
- **Knowledge sharing** — Teaching the broader engineering org about AI patterns, evaluation practices, and emerging capabilities

The collaboration challenge for AI Engineers:
- Non-technical stakeholders often have unrealistic expectations about AI capabilities
- The probabilistic nature of AI outputs makes communication about quality and reliability especially important
- AI features often cut across traditional team boundaries, requiring coordination across multiple teams

### Infrastructure and Platforms

**Frequency: ~30% of postings**

Some AI Engineers are responsible for the infrastructure that AI systems run on. This is especially common at larger companies with dedicated AI platforms.

Common responsibilities:
- **AI platform engineering** — Building internal platforms that make it easy for other engineers to build, deploy, and monitor AI features. Model registries, prompt management systems, evaluation infrastructure.
- **GPU and compute management** — Managing GPU clusters for inference and (occasionally) fine-tuning. Optimizing compute utilization, managing spot/preemptible instances.
- **Vector database infrastructure** — Deploying, scaling, and maintaining vector databases. This includes pgvector on PostgreSQL, managed services (Pinecone), or self-hosted (Qdrant, Weaviate).
- **Model registries** — Managing model versions, metadata, and deployment configurations. Tracking which model version is serving which traffic.
- **MCP server infrastructure** — Deploying and managing MCP servers that connect AI systems to internal tools and data sources. In 2026, this is a growing infrastructure concern.
- **AI gateway / proxy layer** — Building the layer that routes requests to different models, manages API keys, enforces rate limits, and provides unified observability

The platform engineering spectrum:
```
Small team:  Engineer builds everything (AI system + infra)
Medium team: Dedicated platform engineer supports AI team
Large team:  Platform team provides self-service AI platform
Enterprise:  Multiple platform teams (inference, data, eval, safety)
```

### Agents and Agentic Workflows

**Frequency: ~28% of postings**

Agent systems are the fastest-growing responsibility area, up from ~15% in 2025. Building agents requires a different mindset than building RAG systems — you're designing autonomous (or semi-autonomous) systems that make decisions, use tools, and plan multi-step actions.

Common responsibilities:
- **Multi-step planning** — Designing agent systems that can break complex tasks into steps, execute them sequentially or in parallel, and adapt when steps fail
- **Tool use and integration** — Connecting agents to external tools via function calling, MCP, or custom integrations. Defining tool schemas, handling tool errors, managing tool permissions.
- **Agent memory** — Implementing short-term (conversation) and long-term (knowledge) memory for agents. Deciding what to remember, what to forget, and how to retrieve relevant memories.
- **Agent orchestration** — Managing multiple agents working together on a task. Using LangGraph, CrewAI, or A2A for inter-agent communication and coordination.
- **Safety boundaries** — Defining what agents can and cannot do. Permission systems, action validation, human approval workflows for high-stakes actions.
- **Debugging agent behavior** — Tracing agent decision-making, understanding why an agent took a particular action, diagnosing planning failures

The agent maturity model:
```
Level 1: Single-turn tool use (function calling)
Level 2: Multi-step planning with error recovery
Level 3: Autonomous agents with safety boundaries
Level 4: Multi-agent orchestration (A2A)
Level 5: Self-improving agent systems
```

Most production agent systems in 2026 are at Level 2-3. Level 4 is emerging but rare. Level 5 remains aspirational.

---

## Uncommon (Appears in 10-25% of Job Postings)

These responsibilities appear in a minority of postings but are important for specific roles, industries, or company stages.

### Working with Customers

**Frequency: ~18% of postings**

Some AI Engineers, especially at startups and consultancies, work directly with customers to understand their needs, demonstrate AI capabilities, and gather feedback.

Common responsibilities:
- Customer discovery for AI features
- Demo preparation and delivery
- Gathering user feedback on AI outputs
- Understanding domain-specific requirements
- Translating customer needs into technical specifications

This is more common at:
- AI-native startups (small teams, everyone talks to customers)
- AI consultancies (client-facing delivery)
- Enterprise AI teams building internal tools (internal customers)

### Frontend and User Interfaces

**Frequency: ~16% of postings**

Some AI Engineers build the user interfaces for AI-powered features, not just the backend systems. This is especially common at startups and small teams where roles are broader.

Common responsibilities:
- Building chat interfaces (React, Next.js)
- Implementing streaming responses (Server-Sent Events, WebSockets)
- Designing AI-specific UX patterns (loading states, confidence indicators, feedback mechanisms)
- Building annotation and review interfaces for human-in-the-loop workflows
- Creating dashboards for AI system monitoring

The frontend skills needed for AI Engineering are specific:
- Streaming text rendering (tokens arriving incrementally)
- Optimistic UI updates for agent actions
- Handling long-running operations gracefully
- Visualizing AI confidence and uncertainty
- Feedback capture mechanisms (thumbs up/down, corrections)

### Performance Optimization

**Frequency: ~14% of postings**

Optimizing AI system performance — latency, throughput, cost — is a specialized responsibility that becomes more important as systems scale.

Common responsibilities:
- **Latency optimization** — Reducing time-to-first-token, implementing streaming, optimizing retrieval speed, caching frequent queries
- **Cost optimization** — Token usage optimization, model routing (cheaper models for simple queries), prompt compression, batch processing
- **Throughput optimization** — Handling concurrent requests, managing LLM API rate limits, implementing request queuing and prioritization
- **Prompt optimization** — Reducing prompt token count while maintaining output quality, using system prompts efficiently
- **Caching strategies** — Semantic caching (caching similar queries), exact caching, cache invalidation strategies

Performance targets in 2026:
| Metric | Good | Great | Notes |
|---|---|---|---|
| Time to first token | <2s | <1s | Depends on model and provider |
| Total response time (chat) | <5s | <3s | For typical responses |
| RAG retrieval time | <500ms | <200ms | Vector search + re-ranking |
| Agent step time | <10s | <5s | Including tool execution |
| Cost per conversation | <$0.10 | <$0.03 | Varies widely by use case |

### Self-Hosting Models

**Frequency: ~12% of postings**

Some AI Engineers deploy and manage their own model instances rather than using provider APIs. This is driven by data privacy requirements, cost considerations at scale, or the need for customization that API providers don't support.

Common responsibilities:
- Selecting and deploying open-weight models (Llama 4, Mistral, Qwen)
- Setting up inference servers (vLLM, TGI, TensorRT-LLM)
- Managing GPU infrastructure (provisioning, scaling, monitoring)
- Implementing model serving APIs compatible with OpenAI/Anthropic formats
- Quantizing models for efficient deployment (GPTQ, AWQ, GGUF)
- Managing model updates and versioning

Self-hosting is most common in:
- Financial services (data cannot leave the organization)
- Healthcare (HIPAA compliance, patient data)
- Government / defense (classified data, sovereignty)
- Companies with very high API call volumes (cost savings)

### Fine-tuning Models

**Frequency: ~11% of postings**

Fine-tuning is uncommon as a primary responsibility but appears in roles that need domain-specific model behavior. The rise of LoRA/QLoRA has made fine-tuning more accessible, but it's still not a core responsibility for most AI Engineers.

Common responsibilities:
- Preparing fine-tuning datasets (curation, cleaning, formatting)
- Running LoRA/QLoRA fine-tuning on domain-specific data
- Evaluating fine-tuned models against base models
- Managing fine-tuning infrastructure (GPU instances, training scripts)
- Implementing fine-tuning pipelines for continuous improvement

When fine-tuning makes sense:
- Domain-specific vocabulary or knowledge (medical, legal, financial)
- Consistent output format requirements
- Cost reduction (smaller fine-tuned model vs. large general model)
- Latency reduction (smaller model = faster inference)
- Data privacy (fine-tune on-premise, serve on-premise)

### Experimentation and Research

**Frequency: ~10% of postings**

A small but important subset of AI Engineers have explicit research or experimentation responsibilities. This is more common at AI labs, research-oriented companies, and teams pushing the frontier of what's possible.

Common responsibilities:
- Evaluating new model releases and capabilities
- Prototyping novel AI architectures and approaches
- Running experiments to compare approaches
- Publishing internal technical reports
- Contributing to open-source AI tools and frameworks
- Staying current with the latest research and translating it into practice

---

## Rare (Appears in <10% of Job Postings)

These responsibilities appear infrequently but are critical when they do. They tend to be concentrated in specific industries (finance, healthcare, government) or at larger companies with dedicated compliance functions.

### Security and Compliance

**Frequency: ~7% of postings**

AI security and compliance is a growing concern but still handled by dedicated security/compliance teams at most organizations. AI Engineers are rarely the primary owners, but they need to understand the requirements.

Common responsibilities:
- Implementing data privacy controls (PII detection, data masking, access controls)
- Ensuring AI systems comply with regulations (EU AI Act, HIPAA, SOX, etc.)
- Conducting security assessments of AI systems (prompt injection, data exfiltration, model manipulation)
- Implementing audit trails for AI decisions
- Managing model access controls and API key security

The regulatory landscape in 2026:
- **EU AI Act** — In full enforcement. High-risk AI systems require compliance documentation, human oversight, and transparency measures.
- **US State Laws** — A patchwork of state-level AI regulations (Colorado AI Act, California proposals) requiring attention
- **Industry-Specific** — HIPAA for healthcare, FINRA for finance, FedRAMP for government
- **Corporate Policies** — Many companies have internal AI governance frameworks that exceed regulatory requirements

### AI Governance and Responsible AI

**Frequency: ~4% of postings**

Dedicated AI governance roles are rare but growing, especially at larger organizations. These responsibilities focus on the ethical and societal implications of AI systems.

Common responsibilities:
- Developing AI governance frameworks and policies
- Conducting algorithmic impact assessments
- Implementing fairness and bias testing protocols
- Managing AI risk registers
- Ensuring transparency and explainability of AI decisions
- Coordinating with legal, ethics, and compliance teams
- Publishing responsible AI reports

This is most common at:
- Large technology companies (Microsoft, Google, Meta)
- Financial institutions (algorithmic lending, trading)
- Healthcare companies (diagnostic AI, patient-facing systems)
- Government agencies (public-facing AI services)

---

## Responsibility Distribution by Role Level

| Responsibility Area | Junior (0-2yr) | Mid (2-5yr) | Senior (5-8yr) | Staff+ (8yr+) |
|---|---|---|---|---|
| Building AI Systems | Implement | Design + Implement | Architect + Lead | Define direction |
| Productionizing AI | Deploy with guidance | Deploy independently | Own production systems | Define production standards |
| Evaluation and Quality | Run existing evals | Build new evals | Design eval frameworks | Establish org-wide eval practices |
| Using Provider APIs | Call APIs | Optimize API usage | Design multi-provider strategy | Negotiate provider relationships |
| RAG and Retrieval | Implement retrieval | Design retrieval systems | Architect RAG pipelines | Define retrieval strategy |
| Data Processing | Build pipelines | Design data architecture | Own data platform | Define data strategy |
| Collaboration | Participate | Lead workstream | Lead cross-team efforts | Influence org direction |
| Infrastructure | Use platform | Configure infrastructure | Design infrastructure | Own platform strategy |
| Agents | Implement agent steps | Design agent workflows | Architect agent systems | Define agent strategy |
| Security/Compliance | Follow requirements | Implement controls | Design security architecture | Own compliance strategy |

---

## Key Insights from the Data

### 1. AI Engineering Is Broad, Not Deep

The median AI Engineer has responsibilities spanning 5-6 of the categories above. Only at senior levels or in specialized roles do engineers focus deeply on one area. This breadth is both a strength (AI Engineers can work across the stack) and a challenge (it's hard to be expert at everything).

### 2. Evaluation Has Become a Core Responsibility

In 2025, evaluation was mentioned in ~40% of postings. In 2026, it's 58%. The industry has learned the hard way that you can't ship AI systems without robust evaluation. This is no longer a "nice to have" — it's expected.

### 3. Production Experience Is Non-Negotiable

65% of postings mention productionizing AI. The era of "I built a demo" is over. Companies want engineers who can take AI from prototype to production, and that requires a fundamentally different skill set.

### 4. Agent Responsibilities Are Growing Fastest

Agent-related responsibilities grew from ~15% to ~28% of postings year-over-year. This is the biggest mover in the responsibility landscape. If you're building your career in AI Engineering, agent systems are where the growth is.

### 5. Security and Compliance Will Grow

At 7% today, security/compliance seems niche. But with the EU AI Act in full enforcement and increasing regulatory scrutiny worldwide, this will be a growing responsibility area. AI Engineers who understand compliance will have a significant advantage.

### 6. Infrastructure Is Specializing

AI infrastructure has diverged from general infrastructure. Vector database management, MCP server deployment, model serving, and AI-specific monitoring require specialized knowledge that general platform engineers often don't have.

### 7. The "Full-Stack AI Engineer" Is Real

A significant minority of postings (~16%) expect AI Engineers to build both the AI backend and the user-facing frontend. This "full-stack AI Engineer" role is especially common at startups and in teams building customer-facing AI products.

---

## Most Common Words in Responsibilities

Analysis of the 6,200+ responsibility statements reveals the most frequent terms (after removing stop words):

| Rank | Word | Frequency | Context |
|---|---|---|---|
| 1 | **build** | 3,420 | "Build AI systems," "build RAG pipelines," "build evaluation frameworks" |
| 2 | **design** | 2,880 | "Design architectures," "design evaluation systems," "design agent workflows" |
| 3 | **develop** | 2,640 | "Develop AI features," "develop prompts," "develop data pipelines" |
| 4 | **implement** | 2,400 | "Implement retrieval," "implement safety guardrails," "implement monitoring" |
| 5 | **evaluate** | 2,160 | "Evaluate model performance," "evaluate AI outputs," "evaluate quality" |
| 6 | **deploy** | 1,920 | "Deploy to production," "deploy models," "deploy AI systems" |
| 7 | **optimize** | 1,680 | "Optimize performance," "optimize costs," "optimize retrieval quality" |
| 8 | **integrate** | 1,560 | "Integrate LLM APIs," "integrate tools," "integrate with data sources" |
| 9 | **monitor** | 1,440 | "Monitor performance," "monitor quality," "monitor costs" |
| 10 | **collaborate** | 1,320 | "Collaborate with product," "collaborate cross-functionally" |

**Observation:** The top words — build, design, develop, implement — are all **creation verbs**. AI Engineers are builders. The presence of evaluate, deploy, and monitor in the top 10 reflects the maturation of the discipline: it's not just about building, but about building systems that work reliably.

---

## The Responsibility Stack Model

AI Engineering responsibilities can be visualized as a stack, where each layer builds on the ones below:

```
┌──────────────────────────────────────────────┐
│         AI Governance & Responsible AI        │  ← Rare
├──────────────────────────────────────────────┤
│        Security & Compliance                  │  ← Rare
├──────────────────────────────────────────────┤
│   Experimentation   │   Fine-tuning           │  ← Uncommon
│   Frontend/UI       │   Performance Opt.      │
│   Customer-Facing   │   Self-Hosting          │
├──────────────────────────────────────────────┤
│   RAG & Retrieval   │   Data Processing       │  ← Common
│   Collaboration     │   Infrastructure        │
│   Agent Workflows   │                         │
├──────────────────────────────────────────────┤
│   Building AI Systems                         │  ← Very Common
│   Productionizing AI                          │
│   Evaluation & Quality                        │
│   Using Provider APIs                         │
└──────────────────────────────────────────────┘
```

Most AI Engineers spend 70-80% of their time in the bottom layer (Very Common), 15-20% in the middle layer (Common), and 5-10% in the upper layers (Uncommon/Rare). As they advance in their career, the distribution shifts upward — senior engineers spend more time on architecture, strategy, and governance.

---

## Responsibilities by Company Size

| Responsibility | Startup (<50) | Mid (50-500) | Large (500-5000) | Enterprise (>5000) |
|---|---|---|---|---|
| Building AI Systems | 90% | 80% | 72% | 65% |
| Productionizing AI | 55% | 65% | 70% | 72% |
| Evaluation & Quality | 42% | 55% | 62% | 68% |
| Using Provider APIs | 60% | 55% | 50% | 45% |
| RAG and Retrieval | 52% | 50% | 45% | 40% |
| Data Processing | 30% | 38% | 42% | 45% |
| Collaboration | 28% | 35% | 38% | 40% |
| Infrastructure | 15% | 25% | 35% | 45% |
| Agent Workflows | 22% | 28% | 30% | 28% |
| Frontend/UI | 25% | 18% | 12% | 8% |
| Security/Compliance | 3% | 5% | 8% | 15% |
| AI Governance | 1% | 2% | 5% | 10% |

**Key observations:**
- Startups: Broader responsibilities, more building, more customer-facing work
- Enterprise: More production, compliance, and infrastructure specialization
- Mid-size companies: The sweet spot for AI Engineers — enough scale to be interesting, enough breadth to grow skills
- Large companies: Most specialization, most infrastructure work, most compliance concerns

---

## The Evolution of Responsibilities (2024-2026)

| Responsibility | 2024 | 2025 | 2026 | Trend |
|---|---|---|---|---|
| Building AI Systems | 75% | 77% | 78% | Stable |
| Productionizing AI | 50% | 58% | 65% | ↑↑ Growing |
| Evaluation & Quality | 32% | 40% | 58% | ↑↑↑ Fastest growing |
| Using Provider APIs | 60% | 57% | 55% | ↓ Slight decline (multi-provider) |
| RAG and Retrieval | 40% | 44% | 48% | ↑ Growing |
| Data Processing | 35% | 37% | 38% | → Stable |
| Collaboration | 30% | 33% | 35% | ↑ Growing |
| Infrastructure | 22% | 26% | 30% | ↑ Growing |
| Agent Workflows | 5% | 15% | 28% | ↑↑↑ Explosive growth |
| Security/Compliance | 4% | 5% | 7% | ↑ Growing (regulation) |
| AI Governance | 1% | 2% | 4% | ↑ Growing (regulation) |

The three biggest trends:
1. **Evaluation has become a core responsibility** — From 32% to 58% in two years
2. **Agent responsibilities have exploded** — From 5% to 28% in two years
3. **Production concerns have grown** — From 50% to 65% in two years

These trends reflect the maturation of AI Engineering as a discipline: from "build cool demos" to "ship reliable, evaluated, production AI systems."
