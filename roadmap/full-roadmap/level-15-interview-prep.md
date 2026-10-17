# Level 15 · GenAI / AI Engineer Interview Prep

> **Phase 7 · Interview** · 10 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/15/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Convert everything learned across the roadmap into interview performance. This level does not re-teach concepts; it focuses on scenario-based questions, system-design discussions, debugging cases, trade-offs, and defending real engineering decisions under interview conditions.

## Why this level matters

**Interview weight: 9/10**

It directly **turns what you know into answers**. Being able to explain trade-offs and project decisions under pressure is a separate skill, and **strong candidates fail without practising it**.

**On-the-job weight: 1/10**

**No direct use on the job**, apart from occasionally interviewing other candidates.

---

## Modules

### 01 · Interview strategy & role positioning (M15.1 · 1 session)

- **How GenAI interviews have shifted** — Understand how GenAI interviews have shifted from theory-heavy questioning toward system design, debugging, architecture, and production scenarios.
- **Reading a job description** — Learn to read a job description and identify which roadmap areas are actually being tested instead of trying to prepare every listed tool.
- **AI Engineer vs GenAI DS vs DS** — Distinguish AI Engineer, GenAI Data Scientist, and traditional Data Scientist roles by emphasis rather than treating them as completely separate disciplines.
- **Why the engineering layer dominates** — Understand why modern AI-engineering interviews increasingly emphasize the engineering layer: APIs, inference, LLMOps, observability, networking, cloud, reliability, and deployment.
- **API-hosted vs self-hosted models** — Practice explaining API-hosted models vs self-hosted open-weight models across capability, cost, latency, control, privacy, and operational burden.
- **A personalized preparation plan** — Build a personalized interview-preparation plan based on target role and current weaknesses.

**Outcome** · Prioritize interview preparation intelligently and position your existing skillset for the role being targeted.

### 02 · Production RAG interview scenarios (M15.2 · 2 sessions)

- **Ingestion for messy enterprise data** — Design ingestion pipelines for messy enterprise data containing complex **PDFs**, nested tables, diagrams, varying layouts, and continuously changing documents.
- **RAG at concurrent-user scale** — Whiteboard a **RAG** system serving large numbers of concurrent users across very large document collections.
- **Splitting the architecture into services** — Separate the architecture into services such as embedding, retrieval, LLM inference, ingestion, orchestration, and storage.
- **Stateless services, stateful stores** — Explain why application/orchestration services should often remain stateless while persistent state belongs in databases, object stores, vector databases, graph databases, caches, or search indexes.
- **Production infrastructure around RAG** — Reason about production infrastructure around **RAG**:
- **Asynchronous messaging & queues** — asynchronous messaging and queues
- **Service fallbacks** — service fallbacks
- **Object, vector, graph & search storage** — object/vector/graph/search storage
- **Observability & SLAs** — observability and SLAs
- **Networking & IAM** — networking and IAM
- **Secrets & encryption** — secrets and encryption
- **CI/CD & deployment** — CI/CD and deployment.
- **"Quality dropped after a week"** — Practice debugging scenarios such as: “The RAG system worked well for a week and then quality dropped. How would you investigate?”
- **Isolating the failing stage** — Isolate failures across ingestion, retrieval, generation, data changes, model changes, and infrastructure.

**Outcome** · Whiteboard and defend a production-scale RAG architecture rather than describing a demo-level retriever → LLM pipeline.

### 03 · Agentic AI interview scenarios (M15.3 · 2 sessions)

- **Designing an agent for a business task** — Design an agentic system for a concrete business task involving planning, tools, memory, and multi-step execution.
- **Workflow or autonomous agent** — Defend the choice between a deterministic workflow and an autonomous agent.
- **Tools, MCP, memory & multi-agent** — Reason about tools, **MCP** integrations, memory, and multi-agent architectures under realistic constraints.
- **Common failure scenarios** — Handle common interview failure scenarios:
- **Runaway loops** — runaway loops
- **Poor tool selection** — poor tool selection
- **Tool failures** — tool failures
- **Nondeterministic trajectories** — nondeterministic trajectories
- **Excessive token & cost usage** — excessive token/cost usage
- **Context degradation** — context degradation
- **Overly powerful tool permissions** — overly powerful tool permissions.
- **Human-in-the-loop checkpoints** — Design human-in-the-loop checkpoints and guardrails for consequential actions.
- **Debugging an agent from its trajectory** — Debug an agent from its trajectory when it succeeds in testing but fails under production conditions.
- **When not to go autonomous** — Explain when not to introduce multi-agent or autonomous behavior.

**Outcome** · Design and defend an agent architecture while reasoning explicitly about autonomy, cost, reliability, recovery, and blast radius.

### 04 · Fine-tuning & model adaptation interviews (M15.4 · 1 session)

- **Prompt vs RAG vs fine-tuning** — Make the prompt vs **RAG** vs fine-tuning decision from a concrete product brief.
- **When fine-tuning earns its complexity** — Explain when fine-tuning creates meaningful value and when it adds unnecessary training and deployment complexity.
- **LoRA, QLoRA, PEFT & quantization** — Discuss **LoRA**, **QLoRA**, **PEFT**, and quantization in terms of engineering trade-offs rather than only definitions.
- **Deploying a fine-tuned open-weight model** — Reason about deploying a fine-tuned open-weight model: serving architecture, GPU requirements, inference optimization, latency, and cost.
- **"Accuracy dropped after deployment"** — Practice the debugging case: “The fine-tuned model performed well before deployment, but production accuracy dropped. What do you investigate?”
- **What to investigate** — Consider training data, formatting, distribution shift, evaluation regressions, inference configuration, serving changes, and quantization artifacts.

**Outcome** · Defend a model-adaptation strategy and systematically debug performance degradation after deployment.

### 05 · LLMOps & production debugging interviews (M15.5 · 2 sessions)

- **Diagnosing production incidents** — Diagnose production incidents involving model APIs, self-hosted inference, retrieval services, queues, caches, rate limits, and downstream tools.
- **Latency spikes, outages & cost explosions** — Reason through latency spikes, provider outages, cost explosions, capacity limits, and degraded model quality.
- **Fallbacks, retries & autoscaling** — Discuss fallback strategies, graceful degradation, retries, load balancing, and autoscaling.
- **Reading monitoring signals** — Interpret monitoring signals such as latency, throughput, error rates, token usage, cost, retrieval quality, and eval scores.
- **Alert, rollback or investigate** — Explain what should trigger an alert and what requires rollback versus investigation.
- **Proprietary API vs self-hosted inference** — Practice comparing proprietary API deployment with self-hosted inference under realistic traffic and privacy constraints.

**Outcome** · Demonstrate that you can operate and troubleshoot an AI system after it leaves the notebook.

### 06 · AI system-design interviews (M15.6 · 2 sessions)

- **Turning ambiguity into assumptions** — Practice turning an ambiguous product requirement into explicit assumptions around users, traffic, latency, quality, cost, freshness, privacy, and reliability.
- **Simplest viable architecture first** — Start with the simplest viable architecture before introducing **RAG**, agents, fine-tuning, routing, caching, or complex infrastructure.
- **Whiteboarding the full AI stack** — Whiteboard systems using the full AI stack:
- **Model selection & routing** — model selection/routing
- **RAG & context** — RAG and context
- **Tools & agents** — tools/agents
- **Caches** — caches
- **Databases** — databases
- **Inference services** — inference services
- **Observability** — observability
- **Evals** — evals
- **Security** — security
- **Deployment** — deployment.
- **Designing under enterprise constraints** — Design under enterprise constraints where a public API is not allowed, and defend a managed platform or self-hosted deployment on identity, residency, capacity, and cost.
- **Explaining trade-offs, not naming tools** — Explain every major trade-off rather than merely naming technologies.
- **Systems to practise** — Practice system designs such as:
- **Enterprise support assistant** — enterprise support assistant
- **Coding assistant** — coding assistant
- **Research agent** — research agent
- **Large-scale document intelligence** — large-scale document intelligence system.

**Outcome** · Run a structured AI-system-design interview from requirements through architecture, bottlenecks, failure modes, and scaling.

### 07 · Staying current without chasing hype (M15.7 · 1 session)

- **A process for evaluating what is new** — Build a defensible process for evaluating new models, frameworks, papers, benchmarks, and tooling.
- **Capability change vs hype** — Separate meaningful capability/infrastructure changes from short-lived hype.
- **Evaluating a newly released model** — Explain how you would evaluate a newly released model before replacing an existing production model.
- **Benchmarks → evals → controlled rollout** — Use benchmarks → shortlist → custom evals → cost/latency comparison → controlled rollout rather than social-media consensus.
- **"How do you stay current?"** — Develop a strong answer to common interview questions such as “How do you stay current in GenAI?”

**Outcome** · Demonstrate informed judgment rather than simply listing the latest tools.

### 08 · Project & portfolio defense (M15.8 · 2 sessions)

- **Choosing two or three projects to defend** — Prepare 2–3 major projects from the roadmap for deep technical questioning.
- **A structure for explaining each** — Explain each project using:
- **Problem → architecture → results** — problem → requirements → baseline → architecture → decisions → trade-offs → failures → evals → production results.
- **Justifying every technology choice** — Be prepared to explain why you selected a particular model, retriever, agent architecture, framework, database, or deployment strategy.
- **Quantifying the outcome** — Quantify where possible: quality scores, latency, cost/query, throughput, dataset size, traffic, or improvement over baseline.
- **Discussing failures openly** — Discuss failures and design mistakes openly and explain what you changed as a result.
- **Expected follow-ups** — Prepare for interviewer follow-ups such as:
- **"Why didn't you use RAG?"** — “Why didn't you use **RAG**?”
- **"Why not fine-tune?"** — “Why not fine-tune?”
- **"Why do you need an agent?"** — “Why do you need an agent?”
- **"What happens at 100× traffic?"** — “What happens at 100× traffic?”
- **"How would you halve the cost?"** — “How would you reduce the cost by 50%?”
- **"What breaks first?"** — “What breaks first?”

**Outcome** · Defend projects as engineering decisions rather than merely demonstrate that they work.

### 09 · Behavioral communication for AI engineers (M15.9 · 1 session)

- **Clarity without implementation detail** — Communicate technical reasoning clearly without drowning the interviewer in implementation details.
- **Stating assumptions first** — State assumptions before solving ambiguous design questions.
- **Thinking in trade-offs** — Think in structured trade-offs rather than jumping directly to a tool or architecture.
- **Revealing a design progressively** — Use diagrams and whiteboards to progressively reveal a design.
- **Measuring instead of bluffing** — When unsure, explain how you would measure, experiment, or debug rather than bluffing.
- **Structuring experience-based answers** — Structure experience-based answers around the situation, decision, implementation, result, and lessons learned.

**Outcome** · Make strong technical thinking visible to the interviewer.

#### Capstone: Full Mock GenAI Interview Loop

- Simulate a complete interview Simulate a complete AI-engineering interview.
- Round 1 · Scenario & debugging
- Rapid production scenarios Solve rapid production scenarios such as:
- RAG accuracy suddenly drops **RAG** accuracy suddenly drops.
- Agent enters an expensive loop Agent enters an expensive loop.
- Provider latency doubles Model provider latency doubles.
- Fine-tuned model regresses Fine-tuned model regresses after deployment.
- Prompt change doubles cost Prompt change improves quality but doubles cost.
- Retriever fails on real queries Retriever works offline but fails on real production queries.
- Round 2 · System design
- From ambiguous brief to architecture Receive an ambiguous product brief and:
- The full design sequence Clarify requirements → define constraints → establish baseline → design architecture → choose models → design data/context layer → handle scale → add reliability/security → define evals/monitoring → defend trade-offs.
- Round 3 · Project defense
- Deep follow-ups on one project Present one major portfolio project and handle increasingly deep follow-up questions on architecture, alternatives, costs, failures, evals, and scaling.

demonstrate that you can reason like an AI engineer under interview conditions, not merely recall AI concepts.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [The 100 interview questions in this roadmap](../accelerated-roadmap/interview-questions.md) — practice bank with strong-answer outlines for every question.
- [This repository's interview section](../../interview/README.md) — process, question banks by round, salary negotiation and resume playbook.
- [Introduction to Machine Learning Interviews (free book repo)](https://github.com/chiphuyen/ml-interviews-book) — Chip Huyen's open interview-preparation book.
- [AI System Design Guide (GitHub)](https://github.com/ombharatiya/ai-system-design-guide) — system-design practice for AI applications.
- [RAG Interview Questions and Answers Hub (GitHub)](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub) — community question bank for RAG rounds.
- [igotanoffer — Generative AI system design interview guide](https://igotanoffer.com/en/advice/generative-ai-system-design-interview) — free articles on GenAI system-design rounds.
- [TechIE — AI engineer interview experiences](https://www.techinterviewhandbook.org/) — free behavioral and technical interview preparation frameworks.

## In this repository

- [Interview preparation section](../../interview/README.md)
- [Interview question bank (theory, coding, system design, behavioral)](../../interview/02-questions.md)
- [Resume & portfolio playbook](../../interview/08-ai-engineer-resume-and-portfolio-playbook.md)

---

[← Level 14 · Projects](level-14-projects.md) | [Roadmap map](README.md)
