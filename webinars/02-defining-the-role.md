# Defining the AI Engineer Role

**Webinar Recording** | Duration: 78 min | Speakers: Dr. Aisha Patel (Hiring Lab), Ryan McDowell (Vercel), Li Wei Chen (Databricks), Tomasz Tunguz (Sutter Hill Ventures)

---

## Overview

What is an AI Engineer? The title has proliferated across job boards, LinkedIn profiles, and company career pages — but the actual role varies wildly. This webinar presents findings from an analysis of 3,100+ job descriptions posted between January 2025 and January 2026, cross-referenced with hiring manager interviews at 40+ companies. The result is a taxonomy that cuts through the noise.

---

## The Three Types of AI Engineer

After clustering job descriptions by required skills, responsibilities, and compensation bands, three distinct role types emerged:

### Type 1: AI-First Engineer

**Prevalence:** ~35% of postings
**Alias titles:** AI Engineer, LLM Engineer, Applied AI Engineer, AI Product Engineer

This is the role most people picture when they hear "AI Engineer." These engineers build products where AI is the core value proposition, not a feature add-on.

**Typical responsibilities:**
- Designing and implementing RAG pipelines from scratch
- Building agentic workflows with tool use and planning
- Developing prompt management systems and versioning
- Creating evaluation frameworks for model outputs
- Optimizing token usage and inference costs
- Integrating foundation models into product surfaces

**Stack signature:**
- Python (mandatory), TypeScript (common)
- LangChain / LlamaIndex (appears in 68% of postings)
- Vector databases (Pinecone, Weaviate, Qdrant, pgvector)
- OpenAI / Anthropic / open-weight model APIs
- Evaluation tools (LangSmith, Braintrust, custom frameworks)

**Compensation range (US, 2025-2026):**
- Junior (0-2 years): $145K–$185K base
- Mid (2-5 years): $185K–$260K base
- Senior (5+ years): $260K–$380K base
- Staff/Principal: $350K–$500K+ base (rare, mostly big tech)

**Company examples:** Cursor, Harvey, Perplexity, character.ai, Ramp's AI team, Vercel AI group

### Type 2: AI-Support Engineer

**Prevalence:** ~45% of postings
**Alias titles:** Software Engineer (AI), Backend Engineer — AI Systems, ML Platform Engineer, Data Engineer — AI

This is the silent majority. These engineers work at companies where AI is a feature, not the product. They're adding AI capabilities to existing software — search, recommendations, content generation, summarization.

**Typical responsibilities:**
- Integrating LLM APIs into existing product surfaces
- Building infrastructure for model serving and routing
- Implementing guardrails and content filtering
- Maintaining data pipelines that feed AI features
- Supporting ML engineers who build custom models
- Handling AI-related observability and alerting

**Stack signature:**
- Python or primary company language (Go, Java, Ruby + Python for AI)
- REST/gRPC API integration patterns
- Redis/caching layers for model responses
- Existing CI/CD with AI testing bolted on
- Often uses internal AI platforms rather than direct model access

**Compensation range (US, 2025-2026):**
- Junior (0-2 years): $130K–$165K base
- Mid (2-5 years): $165K–$230K base
- Senior (5+ years): $230K–$320K base

**Company examples:** Stripe, Notion, Canva, Spotify, most traditional tech companies adding AI features

### Type 3: ML Engineer (AI-Labeled)

**Prevalence:** ~20% of postings
**Alias titles:** ML Engineer, AI/ML Engineer, Applied Scientist, Research Engineer

These are traditional ML roles rebranded with "AI" in the title to attract candidates. The work is primarily about training, fine-tuning, and deploying custom models — not building on top of foundation models.

**Typical responsibilities:**
- Fine-tuning foundation models for domain-specific tasks
- Training custom models (classification, ranking, recommendation)
- Building and maintaining training infrastructure
- Developing data labeling pipelines
- Optimizing model inference for latency and cost
- Conducting experiments and publishing results internally

**Stack signature:**
- Python (mandatory), C++ (common for optimization)
- PyTorch (dominant), JAX (Google-adjacent roles)
- Kubernetes + GPU clusters
- MLflow / Weights & Biages / internal experiment tracking
- ONNX / TensorRT / vLLM for serving

**Compensation range (US, 2025-2026):**
- Junior (0-2 years): $150K–$190K base
- Mid (2-5 years): $190K–$270K base
- Senior (5+ years): $270K–$400K base

**Company examples:** Databricks, Hugging Face, Cohere, Google DeepMind, Meta FAIR, any company training custom models

---

## Skills Demand Breakdown

The analysis of 3,100+ job descriptions revealed the following skill demand frequencies:

### Technical Skills (Ranked by Appearance Frequency)

| Skill / Technology | % of Postings | Trend vs. 2024 |
|-------------------|---------------|----------------|
| Python | 94% | Stable |
| LLM API integration (OpenAI/Anthropic) | 78% | ↑ +22% |
| RAG / vector databases | 67% | ↑ +31% |
| Prompt engineering / management | 61% | ↑ +18% |
| LangChain or LlamaIndex | 54% | ↓ -8% (fragmentation) |
| Evaluation / testing frameworks | 52% | ↑ +40% |
| Agent design patterns | 44% | ↑ +35% |
| PyTorch | 38% | ↓ -12% |
| TypeScript / JavaScript | 37% | ↑ +15% |
| Fine-tuning / training | 34% | ↓ -6% |
| MLOps / model serving | 33% | Stable |
| Kubernetes / containerization | 31% | Stable |
| SQL / data engineering | 28% | Stable |
| Safety / guardrails / alignment | 26% | ↑ +45% |
| Streaming / real-time inference | 22% | ↑ +19% |

### The Rising Skills

Three skill categories showed dramatic year-over-year increases:

1. **Evaluation frameworks (+40%)** — Companies have realized that deploying AI features without rigorous evaluation is a liability. Engineers who can build and maintain eval suites are in high demand.

2. **Safety and guardrails (+45%)** — The biggest percentage increase. Regulatory pressure (EU AI Act enforcement beginning 2025) and high-profile incidents have made this a mandatory concern.

3. **Agent design patterns (+35%)** — The shift from single-turn chatbots to multi-step agents has created demand for engineers who understand planning, tool use, and error recovery patterns.

### The Declining Skills

1. **PyTorch usage in AI Engineer roles (-12%)** — As foundation models become more capable, fewer companies need engineers to train models from scratch. PyTorch demand is shifting to dedicated ML Engineer roles.

2. **LangChain/LlamaIndex dominance (-8%)** — Not declining in usage, but the ecosystem is fragmenting. Companies now list alternatives (Haystack, DSPy, custom frameworks) more frequently, and many postings say "LangChain or equivalent."

### Soft Skills (Ranked by Mention Frequency)

| Skill | % of Postings | Notes |
|-------|---------------|-------|
| Cross-functional collaboration | 72% | Working with PMs, designers, domain experts |
| Communication (technical to non-technical) | 64% | Explaining model behavior and limitations |
| Problem decomposition | 58% | Breaking ambiguous AI problems into tractable pieces |
| Rapid prototyping | 51% | Building quick proofs of concept |
| User empathy | 43% | Understanding when AI helps vs. frustrates users |
| Ethical reasoning | 31% | Making responsible design decisions |

---

## What Hiring Managers Actually Look For

The hiring manager interviews (n=40+) revealed a significant gap between what job descriptions list and what actually drives hiring decisions.

### The Unspoken Requirements

**1. Comfort with ambiguity (mentioned by 87% of hiring managers)**

> "The biggest failure mode I see in candidates is expecting clear specs. In AI Engineering, the spec is often 'make it work better,' and you have to define what 'better' means yourself." — Ryan McDowell, Vercel

**2. Evaluation mindset (mentioned by 79%)**

> "I don't care if you can build a RAG pipeline — that's table stakes. I care if you can tell me whether your RAG pipeline is actually working well, and what you'd do to make it work better." — Li Wei Chen, Databricks

**3. Systems thinking (mentioned by 73%)**

> "Prompt engineering in isolation is useless. I want engineers who think about the full system: how the prompt connects to retrieval, how retrieval connects to the data pipeline, how the output connects to the user experience." — Dr. Aisha Patel

**4. Pragmatism over purism (mentioned by 68%)**

> "I'd take an engineer who ships a working solution with GPT-4o and a simple RAG pipeline over one who spends three months building the 'perfect' architecture with fine-tuned models that never launches." — Tomasz Tunguz

**5. Cost consciousness (mentioned by 62%)**

> "At our scale, a 10% reduction in token usage is worth more than a 10% improvement in model accuracy. Engineers who think about cost from the start are rare and valuable." — Ryan McDowell

### The Portfolio That Actually Gets Attention

Hiring managers were asked what portfolio elements make them stop scrolling:

| Portfolio Element | % Who Value It | Why |
|------------------|----------------|-----|
| Working demo with eval metrics | 91% | Shows end-to-end thinking |
| Production-grade code (error handling, logging, tests) | 85% | Proves you can ship, not just prototype |
| Post-mortem / failure analysis | 78% | Demonstrates evaluation mindset |
| Cost-optimized solution | 71% | Shows practical awareness |
| Creative use of constraints | 68% | Reveals problem-solving ability |
| Blog post explaining trade-offs | 65% | Demonstrates communication skills |
| Open-source contributions | 52% | Nice to have, not decisive |
| Tutorial follow-alongs | 23% | Negative signal if it's the only content |

---

## The Full-Stack Expectation

### The Uncomfortable Truth

One of the most discussed topics in the webinar was the full-stack expectation placed on AI Engineers. The data is clear:

- **72% of AI-First Engineer postings** require backend development skills
- **48% require frontend or API design skills**
- **41% require infrastructure / DevOps skills**
- **31% require data engineering skills**

This means the "AI Engineer" title often implies: "Build the entire AI feature, from data pipeline to user interface."

### The Full-Stack AI Engineer Skill Tree

```
AI Engineer (Core)
├── Model Interaction Layer
│   ├── Prompt engineering & management
│   ├── Model selection & routing
│   ├── Token optimization
│   └── Fallback & error handling
├── Data & Retrieval Layer
│   ├── Vector database design & ops
│   ├── Embedding pipeline management
│   ├── Chunking strategy & iteration
│   └── Data freshness & indexing
├── Evaluation Layer
│   ├── Eval suite design & maintenance
│   ├── Regression testing
│   ├── A/B testing for model changes
│   └── Quality monitoring & alerting
├── Infrastructure Layer
│   ├── Model serving & routing
│   ├── Caching strategies
│   ├── Cost management
│   └── Observability & logging
└── Product Layer
    ├── API design for AI features
    ├── Streaming response handling
    ├── UX considerations for AI uncertainty
    └── Guardrail implementation
```

Li Wei Chen's perspective:
> "At Databricks, we hire specialists. But most companies can't afford to. If you're the third engineer at a startup, you need to own the entire stack from the vector database to the streaming response endpoint. The title says 'AI Engineer' but the job description says 'everything between the model and the user.'"

### Bridging the Gap

For engineers transitioning from traditional SWE or pure ML roles:

| If you're coming from... | Your likely gaps | Recommended focus |
|--------------------------|-----------------|-------------------|
| Backend SWE | Model behavior intuition, eval mindset | Build 2-3 AI side projects with rigorous evals |
| Frontend SWE | Infrastructure, data pipelines, model APIs | Take a RAG pipeline from zero to production |
| Data Science | Production engineering, systems design | Ship a feature end-to-end, including on-call |
| ML Research | Product thinking, cost awareness, speed | Build something users actually interact with |
| MLOps | Product-facing AI work, prompt design | Work on a user-facing feature, not just infra |

---

## Q&A Highlights

### Q: Is the AI Engineer role just a temporary trend that will disappear as models get better?

**A:** The panelists unanimously disagreed, but with nuance.

> "The *specific skills* will change. Five years from now, nobody will list 'LangChain' on a job posting. But the *need for people who can integrate AI capabilities into products reliably* will only grow. That's the durable part of this role." — Tomasz Tunguz

> "Models are getting better, but that doesn't eliminate the need for engineers who understand how to deploy, evaluate, monitor, and iterate on AI features. If anything, better models mean more AI features, which means more integration work, not less." — Dr. Aisha Patel

### Q: Do I need a graduate degree?

**A:** Based on the data:
- **AI-First Engineer:** 22% of postings require graduate degrees (down from 34% in 2024)
- **AI-Support Engineer:** 15% require graduate degrees
- **ML Engineer:** 61% require graduate degrees (stable)

Ryan McDowell: "I've never checked a degree requirement when hiring. I check if you can build and evaluate AI systems. That's it."

### Q: How important is it to understand model internals (transformer architecture, attention mechanisms, etc.)?

**A:** The answer depends on the role type:

- **AI-First Engineer:** Helpful but not required. Understanding tokenization limits and context windows matters more than understanding attention heads.
- **AI-Support Engineer:** Rarely necessary. API-level understanding is sufficient.
- **ML Engineer:** Mandatory. You can't fine-tune effectively without understanding what you're fine-tuning.

> "I ask candidates: 'What happens when a model's context window fills up?' If they can explain the practical implications — truncation, lost information, retrieval degradation — that's worth more than being able to derive the attention formula." — Li Wei Chen

### Q: What's the single most valuable thing I can learn right now?

**A:** The panelists converged on one answer: **evaluation engineering**.

> "Everyone can build a demo. Very few people can tell you whether their demo is actually working well in a principled, measurable way. Learn to build eval suites. Learn to define metrics. Learn to run regression tests. That skill will be valuable regardless of which framework or model is popular." — Dr. Aisha Patel

---

## Key Takeaways

1. **There are three distinct AI Engineer role types.** Know which one you're targeting — the skills, compensation, and career paths differ significantly.
2. **AI-Support Engineer is the most common role.** Most AI Engineers are adding AI to existing products, not building AI-native products.
3. **Evaluation is the #1 rising skill.** Companies have moved past "can we build it?" to "is it actually working well?"
4. **Safety and guardrails demand is surging.** Regulatory pressure and incident awareness have made this a non-negotiable skill.
5. **The full-stack expectation is real.** Most AI Engineer roles require competency across the entire AI feature stack.
6. **Hiring managers care about different things than job descriptions suggest.** Ambiguity tolerance, evaluation mindset, and systems thinking matter more than specific framework experience.
7. **Your portfolio should show working demos with eval metrics.** A deployed side project with quality measurements beats a polished tutorial every time.
8. **Graduate degree requirements are declining.** Except for ML Engineer roles, demonstrated ability outweighs formal credentials.
9. **LangChain dominance is fragmenting.** Being framework-agnostic and understanding underlying patterns is more durable than knowing any single framework.
10. **Cost consciousness is an underrated differentiator.** Engineers who think about token efficiency from the start stand out in interviews and on the job.

---

## Data Appendix

### Methodology

- **Job posting sources:** LinkedIn, Indeed, Wellfound, company career pages
- **Date range:** January 2025 — January 2026
- **Filter criteria:** Job titles containing "AI Engineer," "LLM Engineer," "Applied AI," "AI Product Engineer," or "ML Engineer" where the description referenced LLM/AI product work
- **Hiring manager interviews:** 42 interviews across seed-stage startups to FAANG companies
- **Clustering method:** K-means on skill embeddings, validated with manual review

### Limitations

- Job postings overstate requirements (the "kitchen sink" problem)
- Compensation data is self-reported and subject to selection bias
- The field is evolving rapidly; data from 2025 may not reflect 2027 realities
- Geographic concentration: 71% of postings were US-based

---

*This note is part of the AI Engineering Field Guide 2026 — Webinars section.*
