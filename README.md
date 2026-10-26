# AI Engineering Field Guide (2026 Edition)

A curriculum and field guide for building, evaluating and operating AI systems.

> **Evidence review: October 9, 2026.** The latest job-data snapshot inspected is September 23, 2026. Review dates and source publication/collection dates are separate. Some long-form legacy claims still need source-level verification; see the [audit](research/audit-2026-10-09.md).
>
> **Section review: October 17, 2026.** The [AI Evaluation](105_AI-Evaluation/README.md) and [AI Security & Safety](106_AI-Security-Safety/README.md) sections were added with all references verified on that date.

## Start here

- [From foundations to advanced engineering](learning-paths/advanced-engineering.md) — competency stages, real-data projects, measurable exit criteria and expert review questions.
- [Evidence and real datasets](research/README.md) — a reproduced job-posting analysis, dataset limitations, dated benchmark references and reproduction commands.
- [Evidence policy](research/evidence-policy.md) — distinguish measurements, source-reported claims, design targets and teaching illustrations.
- [Repository audit](research/audit-2026-10-09.md) — what was checked, corrected and left unresolved.

The reproduced source contains **8,051 stored job observations across nine scrape folders**, including **1,086 records in the September 23, 2026 folder**. These are counts from a selected job-board dataset, not worldwide demand estimates. Structured skills and role labels are LLM-derived annotations; the [analysis and input fingerprint](research/job-market-summary.json) make the counting reproducible without certifying every annotation.

Advanced practice requires a baseline, versioned data, held-out evaluation, failure analysis, authorization checks, measured operating costs and a recovery plan. The curriculum retains its introductory explanations; the advanced path connects them to reviewable engineering artifacts.

## Roadmaps (Full + Accelerated 100-Day)

Two complete roadmaps for becoming an AI engineer, plus a full interview-preparation track — structure adapted verbatim from the CampusX AI Engineering Roadmap 2026, with every learning resource replaced by free worldwide alternatives:

- [Roadmap hub — which one to follow](roadmap/README.md) — comparison, and how important each topic is for interviews vs the real-world job
- [Full Roadmap](roadmap/full-roadmap/README.md) — 16 levels · 7 phases · 286 sessions · 14 projects; 100% coverage from software fundamentals to interview prep
- [Accelerated Roadmap — 100 Days of AI Engineering](roadmap/accelerated-roadmap/README.md) — 6 modules · 100 days; the core ~80% you need to land your first AI engineering job
- [The 100 GenAI / AI Engineer Interview Questions](roadmap/accelerated-roadmap/interview-questions.md) — copied exactly, with strong-answer outlines and a practice loop
- [12 portfolio projects](roadmap/accelerated-roadmap/projects.md) — full specifications with "done when" criteria and a target-role selection table

## Technical Curriculum (101–106)

- [101 — LLM Literacy](101_LLM-Literacy/README.md) — first-principles guide to transformer mechanics, inference sampling, prompt & context engineering
- [102 — AI Application Development](102_AI-Application-Development/README.md) — orchestration, vector databases, complete RAG curriculum, memory systems, and fine-tuning
- [103 — Agentic AI](103_Agentic%20AI/README.md) — autonomous planning loops, Model Context Protocol (MCP), agentic frameworks, and multi-agent orchestration
- [104 — LLMOps](104_LLMOps/README.md) — deployment architectures, observability, safety guardrails, governance, and enterprise scaling
- [105 — AI Evaluation](105_AI-Evaluation/README.md) — evaluation fundamentals, LLM-as-a-Judge, agent benchmarks and the integrity crisis, RAG evaluation practice, eval engineering in CI/CD, [dataset engineering](105_AI-Evaluation/06-evaluation-datasets.md), and [online experimentation](105_AI-Evaluation/07-online-experimentation.md) — plus a complete [19-lecture LLM Evaluations course](105_AI-Evaluation/course/README.md) with full English notes and transcripts, a [glossary](105_AI-Evaluation/course/glossary.md), a [self-assessment quiz](105_AI-Evaluation/course/flashcards.md), and a [cheat sheet](105_AI-Evaluation/course/cheatsheet.md)
- [106 — AI Security & Safety](106_AI-Security-Safety/README.md) — threat modeling (OWASP LLM + Agentic Top 10), prompt injection defense, red teaming, agent & MCP security, AI alignment, and responsible AI governance


## The AI Engineer Role

- [My vision of the role](role/01-my-vision.md) — how I see AI engineering, comparison with DS/ML/DE roles, CRISP-DM for AI
- [Skills analysis](role/02-skills.md) — reproduced annotation counts, limitations and a competency rubric
- [Responsibilities](role/03-responsibilities.md) — engineering ownership and reviewable deliverables
- [Use cases](role/04-use-cases.md) — application patterns, data requirements and measurable outcomes
- [Reality vs. job postings](role/05-reality-vs-postings.md) — what candidates experience vs. what's advertised
- [Worldwide job market analysis](role/06-worldwide-job-market-analysis.md) — global geographical demand, compensation profiles, and company archetypes


## Interview Preparation

- [Interview process](interview/01-interview-process.md) — common patterns, step counts, time estimates, AI use in hiring, key takeaways
- [Interview questions](interview/02-questions.md) — practice topics and individually attributed legacy reports — **every question now carries an expert answer (`**A:**`)**
  - [Theory](interview/questions/01-theory.md) — LLMs, RAG, agents, context engineering, evaluation, safety, fine-tuning, MCP — answered
  - [Coding](interview/questions/02-coding.md) — coding round formats, DSA problems, from-scratch ML implementations — answered
  - [Project deep dive](interview/questions/03-project-deep-dive.md) — presentation rounds, follow-up probes, what interviewers evaluate — answered
  - [AI system design](interview/questions/04-ai-system-design.md) — system design for AI applications — answered
  - [Behavioral](interview/questions/05-behavioral.md) — values, leadership, problem-solving — answered
  - [Home assignments](interview/questions/06-home-assignments.md) — assignment preparation and public examples — answered
- [Skills that get you hired](interview/03-get-hired.md) — baseline expectations, differentiators, and portfolio strategy
- [After the interview](interview/04-after-the-interview.md) — handling offers, rejections, and salary negotiation
- [Interview trends](interview/05-trends.md) — AI cheating, AI-proctored rounds, context engineering interviews
- [Global compensation & negotiation guide](interview/07-global-compensation-and-job-market.md) — compare dated local evidence and written offer terms
- [Resume & portfolio playbook](interview/08-ai-engineer-resume-and-portfolio-playbook.md) — ATS optimization, high-impact bullet formulas, and 60-second GitHub repo audit checklist
- [Production system design case studies](interview/09-real-world-case-studies.md) — illustrative design exercises and validation requirements


## Learning Paths

- [General learning path](learning-paths/README.md) — what to learn and in what order
- [From Data Engineer](learning-paths/from-data-engineer.md) — smoothest transition, 3-4 months
- [From Data Scientist](learning-paths/from-data-scientist.md) — evaluation is your superpower, add engineering
- [From ML Engineer](learning-paths/from-ml-engineer.md) — easiest transition, replace model call with API call
- [From Backend Engineer](learning-paths/from-backend-engineer.md) — 2-3 months, add AI on top of engineering
- [From Frontend Engineer](learning-paths/from-frontend-engineer.md) — backend first, then AI, unique full-stack advantage


## Portfolio

- [Project ideas and built projects](portfolio/README.md) — project specifications with evaluation guidance, plus the five built project repositories (101–105)


## [Awesome AI Engineering](awesome.md)

Curated collection of resources compiled while researching content for this field guide:

- Practitioner interview stories
- AI system design guides
- Company engineering blogs
- Books and courses
- Case study collections

See [awesome.md](awesome.md) for the list.


## Webinars

Supplemental notes on AI engineering careers. Recording, speaker and survey claims in these notes have not been independently verified; see [their evidence status](webinars/README.md).

1. [A Day of an AI Engineer](webinars/01-a-day-of-ai-engineer.md) — the practical reality of the role
2. [Defining the AI Engineer Role](webinars/02-defining-the-role.md) — role scope and engineering responsibilities
3. [The Interview Process](webinars/03-the-interview-process.md) — real hiring trends, technical questions, and live coding challenges
4. [Take-Home Assignments](webinars/04-take-home-assignments.md) — analyzing real assignments and building production-ready solutions

## Acknowledgments

This guide builds on the foundational work by [Alexey Grigorev](https://github.com/alexeygrigorev) in the original [AI Engineering Field Guide](https://github.com/alexeygrigorev/ai-engineering-field-guide). The October 9 review links to a pinned upstream dataset and adds a reproducible counting method. Upstream annotations and third-party data retain their own limitations and rights; this repository does not claim a newly collected worldwide dataset.

<div align="center">

### ✦ Connect With Me

<p>
  <a href="https://www.adilshamim.me">
    <img src="https://img.shields.io/badge/Portfolio-111111?style=for-the-badge&logo=About.me&logoColor=white" />
  </a>
  <a href="https://linkedin.com/in/adilshamim8">
    <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://adilshamim8.medium.com">
    <img src="https://img.shields.io/badge/Medium-000000?style=for-the-badge&logo=medium&logoColor=white" />
  </a>
  <a href="https://adilshamim.substack.com">
    <img src="https://img.shields.io/badge/Substack-FF6719?style=for-the-badge&logo=substack&logoColor=white" />
  </a>
</p>

<p>
  <a href="https://github.com/AdilShamim8">
    <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  <a href="https://www.kaggle.com/adilshamim8">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" />
  </a>
  <a href="https://leetcode.com/u/AdilShamim8">
    <img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=111111" />
  </a>
  <a href="https://twitter.com/adil_shamim8">
    <img src="https://img.shields.io/badge/X-111111?style=for-the-badge&logo=x&logoColor=white" />
  </a>
</p>

<sub>Building • Learning • Researching • Sharing</sub>

<br/>

⭐ <strong>If this repository helped you, consider giving it a star!</strong> ⭐

</div>

---

> **Engineering principle:**
> Robust AI engineering requires deterministic software engineering surrounding probabilistic model outputs. Focus on evaluation suites, reproducible benchmarking, and production monitoring to ensure reliable business outcomes.
