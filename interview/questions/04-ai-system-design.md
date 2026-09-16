# AI System Design

> AI system design has emerged as a distinct interview category — updated September 16, 2026. It tests your ability to design systems where the core component is an LLM or AI model, and where non-determinism, cost, latency, and safety are first-class design constraints.

---

## AI System Design as a Distinct Category

Traditional system design asks: "How do you design a URL shortener?"
ML system design asks: "How do you design a recommendation system?"
**AI system design asks**: "How do you design a conversational AI that helps doctors diagnose patients — safely, reliably, and at scale?"

The key differences:

| Aspect | Traditional | ML System | AI System |
|--------|------------|-----------|-----------|
| Core component | Database/cache | Model training pipeline | LLM + retrieval + agents |
| Determinism | Deterministic | Probabilistic predictions | Non-deterministic generation |
| Failure mode | Timeout, error | Wrong prediction | Hallucination, injection, cost spike |
| Key constraint | Throughput, consistency | Feature freshness, model accuracy | Safety, cost, latency, quality |
| Evaluation | Uptime, latency | Accuracy, precision/recall | Faithfulness, relevance, safety |
| Scaling challenge | Database sharding | Feature store, model serving | Token throughput, context management |
| Cost model | Infrastructure | Compute for training | Per-token inference cost |

---

## Format

| Aspect | Details |
|--------|---------|
| Duration | 45–60 minutes |
| Typical question | "Design an AI-powered [X]" |
| Time allocation | 5 min clarify → 10 min high-level → 20 min deep-dive → 10 min trade-offs → 5 min wrap-up |
| Interviewers | 1–2 (usually senior/staff engineers) |
| Tools | Whiteboard or shared doc — diagrams expected |

### Time Allocation (Recommended)

| Phase | Duration | What to Cover |
|-------|----------|---------------|
| Requirements clarification | 5 min | Scope, constraints, users, scale, safety requirements |
| High-level architecture | 10 min | Major components, data flow, AI/non-AI boundary |
| Deep-dive on AI components | 20 min | LLM selection, retrieval strategy, agent design, prompt architecture |
| Trade-offs and alternatives | 10 min | Cost vs. quality, latency vs. accuracy, build vs. buy |
| Monitoring and safety | 5 min | Evaluation, guardrails, incident response, cost control |

---

## Typical Questions

### Core AI System Design Questions

| Question | Key Challenges | Companies |
|----------|---------------|-----------|
| AI Chatbot for customer support | Hallucination, escalation, cost | Intercom, Zendesk |
| Document Q&A / RAG system | Retrieval quality, citations, scale | Doctolib, Casetext |
| Enterprise GraphRAG Knowledge Graph | Entity extraction, graph community clustering, hybrid search | Microsoft, Palantir |
| AI co-pilot for coding | Latency, context, safety of generated code | GitHub, Cursor |
| MCP-Based Multi-Agent Developer Swarm | Tool discovery, RPC authentication, human-in-the-loop sandbox | Anthropic, Cognition |
| Local SLM with Speculative Decoding | Memory footprint, KV cache quant, p99 token throughput | Apple, Meta, Mistral |
| Voice assistant with LLM | Latency, STT/TTS, interruption handling | OpenAI, Amazon |
| Contract generation system | Legal accuracy, clause consistency, review workflow | Harvey, LegalOn |
| AI-powered candidate sourcing | Bias, relevance, personalization | Eightfold, LinkedIn |
| Fraud detection with LLM | False positives, real-time requirements, explainability | Stripe, Goldman Sachs |
| Multi-agent workflow | Orchestration, failure recovery, observability | LangChain, CrewAI |
| Content detection / moderation | Scale, nuance, policy, multilingual | Meta, OpenAI |
| Unified query engine (text + SQL + code) | Query routing, schema understanding, ambiguity | Doctolib, Notion |
| Perplexity-like search engine | Real-time retrieval, citation, speed | Perplexity, You.com |

### Near-AI Systems

These questions test infrastructure around AI rather than the AI pipeline itself:

| Question | Key Challenges |
|----------|---------------|
| Real-time vs. batch inference pipeline | Latency SLAs, queue management, GPU utilization |
| Data ingestion for AI (ETL) | Document parsing, chunking, embedding, updates |
| Image generation pipeline | Rate limiting, content policy, GPU management, cost |
| GPU job queue for model training | Priority scheduling, preemption, multi-tenant fairness |
| Model deployment and versioning | A/B testing, rollback, shadow deployment, canary |
| Feature store for AI | Real-time features, point-in-time correctness, freshness |

---

## Expectations by Seniority

| Seniority | What's Expected | What's Not Expected |
|-----------|----------------|-------------------|
| Junior (0–2 years) | Clear architecture, identify key components, basic trade-offs | Deep cost analysis, multi-region deployment, advanced safety |
| Mid (2–5 years) | Detailed architecture, specific technology choices, cost estimation, evaluation strategy | Multi-system orchestration, advanced agent design |
| Senior (5–8 years) | Production-grade design, failure modes, monitoring, cost optimization, safety guardrails, team impact | — |
| Staff+ (8+ years) | Multi-system architecture, organizational impact, build vs. buy decisions, technical strategy | — |

---

## AI System Design vs Traditional vs ML System Design

| Dimension | Traditional System Design | ML System Design | AI System Design |
|-----------|--------------------------|------------------|------------------|
| **Core question** | How to serve data reliably? | How to train and serve a model? | How to build a system with LLMs at the center? |
| **Primary constraint** | Availability, consistency | Model accuracy, data quality | Non-determinism, cost, safety |
| **Data flow** | Request → DB → Response | Features → Model → Prediction | Query → Retrieval + Context → LLM → Response |
| **Scaling** | Horizontal scaling, caching | Model serving, feature store | Token throughput, context management, caching |
| **Evaluation** | SLA, latency p99 | Precision, recall, F1 | Faithfulness, relevance, safety scores |
| **Failure mode** | Server down, data corruption | Model drift, feature staleness | Hallucination, prompt injection, cost overrun |
| **Cost model** | $/request (infrastructure) | $/training run + $/prediction | $/token (inference) + $/embedding + $/storage |
| **Monitoring** | Uptime, error rate | Model metrics, feature drift | Hallucination rate, cost per query, user satisfaction |
| **Safety** | Auth, encryption | Fairness, bias | PII leakage, prompt injection, harmful output |
| **Iteration speed** | Deploy new code | Retrain model (days–weeks) | Update prompt (minutes), swap model (hours) |

---

## How to Prepare: 5-Step Structure

When you get an AI system design question, follow this structure:

### Step 1: Clarify Requirements (5 min)

- What are the functional requirements? (What should the system do?)
- What are the non-functional requirements? (Latency, cost, accuracy, safety)
- Who are the users? What's the scale?
- What are the safety/compliance constraints?
- **AI-specific**: What's the acceptable hallucination rate? What's the cost per query budget?

### Step 2: Define the AI/Non-AI Boundary (5 min)

- Which parts of the system need LLM/AI? Which can be traditional software?
- Where are the AI "hot spots" (where non-determinism enters the system)?
- What's the fallback when the AI component fails or degrades?

### Step 3: Design the AI Pipeline (15 min)

- **Retrieval**: How do you get context? (RAG, tools, knowledge graph, hybrid)
- **Generation**: Which model? What prompt architecture? What's the context window strategy?
- **Evaluation**: How do you evaluate outputs in real-time? What's the fallback?
- **Guardrails**: Input validation, output filtering, content policy, PII handling
- **Caching**: What can you cache? Semantic cache? Prompt cache?

### Step 4: Design the Infrastructure (10 min)

- API layer, load balancing, rate limiting
- Database choices (vector DB, relational, cache)
- Monitoring and observability (LangSmith, Arize, custom)
- Cost management (token budgets, model tiering, caching)
- Deployment (model versioning, A/B testing, rollback)

### Step 5: Discuss Trade-offs and Alternatives (10 min)

- Cost vs. quality (cheaper model + more context vs. expensive model + less context)
- Latency vs. accuracy (streaming, speculative decoding, model tiering)
- Build vs. buy (open-source model vs. API, custom vs. managed vector DB)
- Safety vs. capability (guardrail strictness vs. model flexibility)
- What would change at different scales?

---

## 4 Repeatable Patterns

Most AI system design questions map to one of these patterns:

### Pattern 1: RAG
**Applies to**: Document Q&A, knowledge assistants, search engines, customer support bots

Key design decisions:
- Chunking strategy (fixed, semantic, recursive)
- Embedding model selection
- Vector DB choice (Pinecone, Weaviate, Qdrant, pgvector)
- Retrieval strategy (dense, sparse, hybrid, re-ranking)
- Context window management
- Citation/attribution implementation
- Evaluation methodology

### Pattern 2: Feedback and Reinforcement
**Applies to**: Recommendation systems, personalization, content ranking, ad targeting

Key design decisions:
- Feedback signal collection (implicit vs. explicit)
- How to incorporate feedback (prompt adjustment, fine-tuning, DPO)
- Cold start handling
- Evaluation (offline vs. online, A/B testing)
- Bias and fairness considerations

### Pattern 3: Hallucination Mitigation
**Applies to**: Medical AI, legal AI, financial AI, any high-stakes domain

Key design decisions:
- Grounding strategy (retrieval, knowledge graph, constrained generation)
- Verification pipeline (self-consistency, entailment, retrieval verification)
- "I don't know" threshold calibration
- Citation and attribution
- Human-in-the-loop design
- Monitoring and alerting for hallucination spikes

### Pattern 4: Scalability and Cost
**Applies to**: Consumer-facing AI, high-volume API services, enterprise deployments

Key design decisions:
- Model tiering (route to cheapest adequate model)
- Caching strategy (semantic cache, prompt cache, response cache)
- Token budget management
- Batch vs. real-time processing
- GPU utilization optimization
- Multi-region deployment for latency

---

## What Companies Build

Understanding what companies actually build helps you anticipate their system design questions:

| Company | AI Systems They Build | Likely Design Questions |
|---------|----------------------|------------------------|
| **Doctolib** | Medical document Q&A, appointment assistant | Design a medical RAG system with safety constraints |
| **Uber** | ETA prediction, fraud detection, customer support AI | Design a real-time fraud detection system with LLM reasoning |
| **Airbnb** | Listing description generation, search ranking, host assistant | Design an AI co-pilot for Airbnb hosts |
| **Perplexity** | AI search engine with citations | Design a Perplexity-like search engine |
| **Slack** | AI message summarization, search, workflow automation | Design an AI summarization feature for team channels |
| **LinkedIn** | Job matching, content recommendation, profile optimization | Design an AI-powered candidate sourcing system |
| **Anthropic** | Safety-focused AI assistants, API platform | Design an AI system with safety guarantees |
| **DoorDash** | Order prediction, menu optimization, support chatbot | Design a real-time AI order prediction system |
| **Spotify** | Playlist generation, music discovery, podcast summarization | Design an AI-powered music discovery system |
| **Notion** | AI writing assistant, database Q&A, search | Design a unified query engine for structured and unstructured data |

---

## Common Mistakes

1. **Treating the LLM as a black box.** Interviewers want to see you understand what happens inside — context management, token costs, latency characteristics.

2. **Ignoring cost entirely.** In 2026, cost is a first-class design constraint. Not discussing cost signals you haven't built production AI systems.

3. **Over-engineering the retrieval.** Starting with a complex hybrid retrieval + re-ranking + knowledge graph pipeline when simple semantic search would suffice. Start simple, then add complexity with justification.

4. **No evaluation strategy.** If you can't evaluate the AI component, you can't improve it. Always include evaluation in your design.

5. **Forgetting the non-AI parts.** The database, the API layer, the authentication, the monitoring — these still matter and interviewers will notice if you skip them.

6. **No fallback plan.** What happens when the LLM is down? When latency spikes? When cost exceeds budget? Production systems need graceful degradation.

7. **Ignoring safety.** Even if the interviewer doesn't mention safety, bring it up. PII handling, prompt injection defense, and content policy are now table stakes.

8. **Not asking clarifying questions.** Jumping into design without clarifying requirements wastes time and signals poor communication.

9. **Designing for the wrong scale.** Ask about scale early. Designing for 10M users when the system will serve 10K users (or vice versa) shows poor judgment.

10. **No diagram.** System design requires visual communication. If you're not drawing, you're not communicating effectively.

---

## Sources

[^1]: "Designing LLM Applications", Eugene Yan, 2024–2025.
[^2]: "Machine Learning System Design Interview", Ali Aminian and Alex Xu, 2024.
[^3]: "Building LLM Apps", Valentina Alto, 2024.
[^4]: Interview reports from Blind, Glassdoor, and LeetCode Discuss, 2025–2026.
[^5]: Company engineering blogs: Doctolib, Uber, Airbnb, Perplexity, Slack, LinkedIn, Anthropic, DoorDash, Spotify, Notion — 2024–2026.
[^6]: "RAG Systems in Production", LangChain State of AI Engineering Survey, 2025.
[^7]: "AI System Design Patterns", emerging community resources, 2025–2026.
[^8]: "Cost Optimization for LLM Applications", OpenAI and Anthropic best practices, 2025.
[^9]: "Hallucination Mitigation in Production AI Systems", various industry reports, 2025.

---

> **Next**: [Behavioral Questions →](05-behavioral.md)
