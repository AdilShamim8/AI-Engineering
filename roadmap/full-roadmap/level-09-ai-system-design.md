# Level 9 · AI System Design

> **Phase 5 · Production** · 10 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/9/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Design a complete production AI application and defend every architectural choice across quality, latency, cost, reliability, and user experience.

## Why this level matters

**Interview weight: 9/10**

Mid-level and senior hiring usually includes a **dedicated round**, such as “design a chatbot over company documents.” It’s where **scope, trade-offs, and seniority** get judged.

**On-the-job weight: 8/10**

Matters for **every architecture decision**: which model, how much retrieval, cost vs quality. It grows in importance **as you become more senior**.

---

## Modules

### 01 · The AI system design framework (M9.1 · 2 sessions)

- **Starting from requirements & constraints** — Start from the use case, success criteria, constraints, traffic, latency requirements, quality requirements, privacy, and cost budget.
- **Prompting, RAG, agents or fine-tuning** — Decide deliberately between prompting, **RAG**, agents, fine-tuning, or combinations of them.
- **Quality ↔ latency ↔ cost** — Reason about the central trade-offs: quality ↔ latency ↔ cost, plus complexity and reliability.
- **Baseline before sophistication** — Establish a simple baseline before introducing sophisticated architecture.

**Outcome** · Turn a product requirement into a defensible AI architecture rather than starting with a favorite technology.

### 02 · Context & knowledge architecture (M9.2 · 2 sessions)

- **Where knowledge should come from** — Decide what knowledge should come from model knowledge, prompt/context, **RAG**, memory, or external tools.
- **The full context pipeline** — Design the full context pipeline: ingestion → retrieval → reranking → context assembly → generation.
- **Combining retrieval approaches** — Combine vector, keyword, graph, and other retrieval approaches where justified.
- **Freshness, access control & provenance** — Handle freshness, updates, access control, scale, and source provenance.
- **Retrieved dynamically or held in context** — Decide what information should be retrieved dynamically versus kept permanently in the model's context or external state.

**Outcome** · Design the knowledge layer that supplies the model with the right information at the right time.

### 03 · Model routing & gateways (M9.3 · 2 sessions)

- **What a model gateway does** — Understand the role of a model gateway as the abstraction between application code and model providers.
- **Routing on task, cost & risk** — Route requests based on task type, capability, latency, context length, cost, modality, or risk.
- **Model cascades** — Build model cascades where cheaper/faster models handle easy requests and stronger models handle difficult ones.
- **Provider fallbacks & quality risk** — Add model/provider fallbacks and understand the quality risks introduced by switching models.
- **Centralising auth, limits & tracking** — Centralize authentication, usage tracking, retries, rate limits, and provider abstraction where appropriate.

**Outcome** · Avoid designing applications around a single hard-coded model.

### 04 · Latency & inference optimization (M9.4 · 2 sessions)

- **Breaking latency into components** — Break latency into components such as retrieval, **TTFT**, model generation, tool calls, and network overhead.
- **Streaming for perceived latency** — Use streaming to improve perceived latency.
- **Parallelising independent work** — Parallelize independent operations and avoid unnecessary sequential LLM calls.
- **When a smaller model will do** — Understand when smaller/faster models can replace larger models.
- **Context reduction & batching** — Apply prompt/context reduction, batching, and inference-service optimizations where appropriate.
- **Throughput & utilization at scale** — Reason about throughput, latency, and utilization at scale.

**Outcome** · Identify where an AI application is slow and choose the appropriate optimization instead of simply upgrading infrastructure.

### 05 · Caching architecture (M9.5 · 1 session)

- **The four caches in an AI system** — Understand the different caches available in an AI system: exact-response caching, prompt/context caching, retrieval caching, and semantic caching.
- **What is safe to cache** — Decide what is safe to cache and define appropriate expiration/invalidation strategies.
- **Semantic caching** — Use semantic caching when different queries can reasonably share an answer.
- **Freshness vs latency & cost** — Understand the trade-off between freshness, quality, latency, and cost.
- **Measuring the hit rate** — Measure actual cache hit rate and savings rather than assuming caching helps.

**Outcome** · Use caching as an architectural optimization rather than an afterthought.

### 06 · Reliability, guardrails & graceful degradation (M9.6 · 2 sessions)

- **Designing for every failure** — Design for model failures, provider outages, tool failures, rate limits, malformed outputs, and retrieval failures.
- **Timeouts, circuit breakers & queues** — Add timeouts, retries, fallbacks, circuit breakers, queues, and rate limits where appropriate.
- **Guardrails at system boundaries** — Place guardrails at important system boundaries rather than relying entirely on the model.
- **Graceful degradation** — Design graceful degradation: simpler model, reduced functionality, cached answer, human escalation, or explicit inability to complete the request.
- **Human approval for high-risk actions** — Use human approval for high-risk or irreversible actions.
- **Service-level expectations** — Define service-level expectations for availability, latency, and quality.

**Outcome** · Design a system that remains useful when individual AI components fail.

### 07 · AI pipeline orchestration (M9.7 · 1 session)

- **The end-to-end flow** — Design the end-to-end flow between retrieval, models, tools, agents, guardrails, caches, and external systems.
- **Deterministic vs model-delegated decisions** — Decide which decisions should be deterministic and which should be delegated to the model.
- **Sync, async, queued or long-running** — Choose between synchronous execution, asynchronous jobs, queues, and long-running agent workflows.
- **Avoiding unnecessary agentic complexity** — Avoid unnecessary agentic complexity when a deterministic pipeline is sufficient.
- **Component boundaries** — Define clear component boundaries so individual parts can be changed, evaluated, and scaled independently.

**Outcome** · Turn individual AI components into a coherent production system.

### 08 · Monitoring, feedback & continuous improvement (M9.8 · 1 session)

- **Wiring evals & feedback into production** — Connect evals, traces, operational metrics, and user feedback into the production architecture.
- **What to monitor** — Monitor quality, latency, cost, errors, retrieval behavior, tool usage, and model/provider performance.
- **Explicit & implicit feedback** — Capture explicit feedback such as ratings as well as useful implicit behavioral signals.
- **Failures become evaluation cases** — Turn production failures and user feedback into new evaluation cases.
- **Versioning for traceable regressions** — Version models, prompts, retrieval configurations, and application changes so regressions can be traced.
- **Deploy → observe → improve → redeploy** — Understand the loop: deploy → observe → collect feedback → evaluate → improve → redeploy.

**Outcome** · Design AI products that improve from real-world usage rather than remaining static after launch.

### 09 · AI system design case studies (M9.9 · 2 sessions)

- **Whiteboard and defend the choices** — Whiteboard several systems end-to-end and defend the choices.

Customer-support copilot

- **Design around** — Design around:
- **RAG & fresh knowledge** — RAG and fresh knowledge
- **Citations** — citations
- **Model routing** — model routing
- **Caching** — caching
- **Escalation to humans** — escalation to humans
- **Latency & cost constraints** — latency and cost constraints.

Coding assistant

- **Design around** — Design around:
- **Large codebase context** — large codebase context
- **Retrieval** — retrieval
- **Tool & code execution** — tool/code execution
- **Model selection** — model selection
- **Sandboxing** — sandboxing
- **Long-running tasks** — long-running tasks.

Deep research agent

- **Design around** — Design around:
- **Search & retrieval** — search and retrieval
- **Planning** — planning
- **Parallel tool calls** — parallel tool calls
- **Context management** — context management
- **Long-running execution** — long-running execution
- **Citations** — citations
- **Cost budgets & failure recovery** — cost budgets and failure recovery.
- **Requirements → architecture → trade-offs** — For each case, reason about requirements → baseline → architecture → bottlenecks → failure modes → scaling → trade-offs.

**Outcome** · Defend architectural decisions rather than merely draw boxes and arrows.

#### Capstone: AI System Design Document (M9.10 · 1 session)

- A complete design document Choose a substantial AI product and produce a complete design covering:
- Requirements & success criteria requirements and success criteria
- Expected traffic & constraints expected traffic and constraints
- High-level architecture high-level architecture
- Model choice & routing model choice and routing
- Context / RAG architecture context/**RAG** architecture
- Tools & agents where required tools/agents where required
- Caching strategy caching strategy
- Latency & cost budget latency and cost budget
- Reliability & fallback strategy reliability and fallback strategy
- Security & guardrails security/guardrails
- Evaluation & monitoring evaluation and monitoring
- User-feedback loop user-feedback loop
- Scaling strategy scaling strategy.
- A diagram and the rejected alternatives Include an architecture diagram and explicitly justify the major trade-offs and alternatives rejected.

a design you could defend in an AI system-design interview or an engineering architecture review.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [AI System Design Guide (GitHub)](https://github.com/ombharatiya/ai-system-design-guide) — free community guide to designing AI systems end to end.
- [Chip Huyen's blog](https://huyenchip.com/blog/) — free essays on AI architecture, latency/cost trade-offs and production systems.
- [Designing Machine Learning Systems — free resources (GitHub)](https://github.com/chiphuyen/dmls-book) — chapter summaries and references for the systems-design mindset.
- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — free cloud architecture guidance covering reliability, cost and performance trade-offs.
- [ByteByteGo System Design Newsletter](https://bytebytego.com/) — free weekly articles on caching, queues, load balancing and scaling patterns.
- [This repository's production case studies](../../interview/09-real-world-case-studies.md) — design exercises with validation requirements.
- [Google Cloud Architecture Center — AI and ML resources](https://cloud.google.com/architecture/ai-ml) — free reference architectures for retrieval, agents and serving.

## In this repository

- [Production system design case studies](../../interview/09-real-world-case-studies.md)
- [AI system design interview questions](../../interview/questions/04-ai-system-design.md)
- [Deployment architectures note](../../104_LLMOps/2.%20Deployment/1.%20Deployment%20Architectures.md)

---

[← Level 8 · AI Security](level-08-ai-security.md) | [Roadmap map](README.md) | [Level 10 · LLMOps: From Development to Production →](level-10-llmops.md)
