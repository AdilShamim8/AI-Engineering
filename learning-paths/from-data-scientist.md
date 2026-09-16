# From Data Scientist to AI Engineer

> Evaluation is your superpower (Updated: September 16, 2026). Now add engineering rigor to ship AI systems that work in production.

---

## Your Superpower: Evaluation

Data scientists are uniquely positioned for AI engineering because you already think in terms of metrics, experiments, and measurement. In a field where most people "vibe check" their AI systems, your instinct to quantify quality is invaluable. The gap is engineering: turning notebooks into services, writing tests, and deploying reliably.

---

## What You Already Have

| Skill | How It Transfers |
|-------|-----------------|
| **ML knowledge** | Understanding model capabilities, limitations, and failure modes |
| **Statistical thinking** | Designing rigorous evals, measuring significance, A/B testing |
| **Model evaluation** | The hardest AI engineering skill — you already do this intuitively |
| **Python** | Fluent in the primary AI engineering language |
| **Experimentation** | Tracking experiments, comparing results, iteration methodology |
| **Data analysis** | Understanding data distributions, quality, and preprocessing |
| **Jupyter workflows** | Rapid prototyping (now graduate to production) |
| **Feature engineering** | Analogous to context engineering — selecting the right inputs |

---

## What You Need to Add

### Priority 1: Software Engineering Fundamentals (Weeks 1–3)
- **Clean Python**: Type hints, dependency management (uv/poetry), virtual environments, linting (ruff)
- **Testing with pytest**: Unit tests, fixtures, parametrized tests — test your LLM calls, not just your models
- **Git workflows**: Branching, PRs, code review — collaborative development beyond notebooks
- **API development with FastAPI**: Building REST endpoints that serve your models/prompts
- **CI/CD basics**: Automated testing and deployment pipelines (GitHub Actions)

### Priority 2: LLM and RAG Systems (Weeks 4–5)
- LLM APIs: OpenAI, Anthropic, Google — structured output, function calling, streaming
- Prompt engineering and context engineering as systematic disciplines
- RAG architecture: embeddings, vector search, chunking, retrieval-augmented generation
- Building RAG pipelines: document processing → embedding → retrieval → generation

### Priority 3: Agent Frameworks (Weeks 6–7)
- Function calling: defining tools, handling results, composing multi-step workflows
- The agentic loop: LLM decides → tool executes → result feeds back → repeat
- Frameworks: PydanticAI (type-safe), OpenAI Agents SDK, LangGraph (stateful agents)
- MCP for tool integration, building MCP servers

### Priority 4: Production Deployment (Weeks 8–9)
- From notebooks to services: refactoring prototypes into maintainable code
- Docker containerization, deployment to cloud (AWS/GCP/Azure)
- Observability: LangFuse/LangSmith for tracing, cost monitoring
- Guardrails: input validation, output filtering, safety checks

---

## Step-by-Step Learning Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Python engineering: types, testing, Git | Refactored notebook → tested module |
| 2 | FastAPI, dependency management, CI/CD | API serving an ML model with tests |
| 3 | Production Python patterns, Docker | Containerized API deployed to cloud |
| 4 | LLM APIs, prompt engineering, structured output | Service calling LLMs with eval metrics |
| 5 | RAG: embeddings, vector DBs, retrieval | RAG system with retrieval quality metrics |
| 6 | Function calling, agent frameworks | Agent that uses tools to accomplish tasks |
| 7 | MCP, multi-step agents, evaluation | Evaluated agent with LLM-as-judge |
| 8 | Deployment, monitoring, guardrails | Production AI service with observability |
| 9–12 | Portfolio project + specialization | End-to-end AI application |

---

## Practice Projects

### 1. Eval-Driven Prompt Optimization Tool (Weeks 1–5)
Build a tool that systematically tests prompt variations against an eval dataset, measures quality with multiple metrics (accuracy, faithfulness, coherence), and identifies the best-performing prompt. This leverages your experimentation skills while building engineering discipline.

### 2. RAG System for Research Papers (Weeks 4–7)
Ingest arXiv papers, build a vector index, implement hybrid search with re-ranking, and create an agent that can answer complex research questions with citations. Evaluate retrieval quality with MRR/NDCG and generation quality with LLM-as-judge. You'll appreciate the evaluation layer more than most.

### 3. Automated ML Pipeline Analyzer (Portfolio)
An agent that reads ML experiment logs, analyzes model performance across runs, generates insights and recommendations, and creates automated reports. Combines your ML expertise with agentic AI. Deploy with full evaluation and monitoring.

---

## Common Pitfalls for Data Scientists

1. **Notebook-forever syndrome**: Jupyter is for exploration, not production. If your "system" is a notebook, it's not a system. Graduate to modules, APIs, and services early.

2. **Over-focusing on model quality, under-focusing on system quality**: In production AI, the retrieval, the UX, the error handling, and the monitoring matter as much as the model output. Build the system, not just the model call.

3. **Ignoring deterministic components**: Not everything needs an LLM. If a rule, a lookup, or a simple algorithm works — use it. Reserve LLMs for tasks that genuinely need language understanding.

4. **Skipping software engineering basics**: "It works on my machine" doesn't cut it. Learn Docker, learn testing, learn CI/CD before you ship. These aren't optional — they're what separate engineers from researchers.

5. **Rebuilding everything from scratch**: Your instinct to implement custom solutions (common in DS) will slow you down. Use frameworks (PydanticAI, LangGraph), use managed services (Qdrant Cloud, Pinecone), use existing patterns.

6. **Measuring the wrong things**: You know how to evaluate models, but AI systems need end-to-end evaluation. Don't just measure LLM accuracy — measure retrieval quality, latency, cost, and user satisfaction.

7. **Neglecting the data pipeline**: RAG systems are 70% data engineering. Don't treat the ingestion pipeline as an afterthought — it determines your system's quality ceiling.

---

## Key Resources

- **[FastAPI Documentation](https://fastapi.tiangolo.com/)** — The framework you'll use daily
- **[PydanticAI](https://ai.pydantic.dev/)** — Type-safe agent framework, feels natural for DS → engineering transition
- **[Test-Driven Development with Python](https://www.obeythetestinggoat.com/)** — Build engineering discipline
- **[Anthropic's Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)** — Agentic patterns from first principles
- **[DSPy Documentation](https://dspy.ai/)** — Programmatic prompt optimization — appeals to your scientific mindset
- **[LangFuse](https://langfuse.com/docs)** — Open-source observability that supports eval workflows
- **[Full Stack LLM Bootcamp](https://fullstackdeeplearning.com/)** — Bridging ML and engineering

---

*You already know how to measure quality. Now build the systems that deliver it reliably.*
