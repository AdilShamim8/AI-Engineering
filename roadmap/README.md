# AI Engineer Roadmaps (2026)

Two complete roadmaps for becoming an AI engineer — a **full in-depth roadmap** that covers 100% of the craft, and an **accelerated 100-day roadmap** that covers the ~80% you need to land your first job — plus a **complete interview preparation track** with the 100 most-asked GenAI/AI-engineer interview questions, every one answered in full.

> **Source attribution:** the roadmap structure, levels, modules, session counts, interview/on-the-job weights, and the 100 interview questions in this section are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/) (© 2026 CampusX, retrieved October 17, 2026). This repository is not affiliated with CampusX. Every *Free learning resources* section is independently curated from free worldwide alternatives — no CampusX courses or paid referrals are included anywhere in this section.

---

## Which roadmap should you follow?

| | [Full Roadmap](full-roadmap/README.md) | [Accelerated Roadmap (100 Days)](accelerated-roadmap/README.md) |
|---|---|---|
| **Goal** | Master AI engineering end to end, at depth | Get job-ready with the core ~80% as fast as possible |
| **Structure** | 16 levels · 7 phases · 286 sessions · 165 modules | 6 modules · 100 days · 86 units |
| **Coverage** | 100% — including multimodal, fine-tuning, managed platforms, context engineering | ~80% — LLMs, APIs, prompting, RAG, agents, shipping to production |
| **Best for** | Career switchers with time, engineers targeting senior scope | Working professionals, bootcamp-style timelines, first-job seekers |
| **Projects** | 14 capstone projects across levels | Course project + [12 portfolio projects](accelerated-roadmap/projects.md) |
| **Interview prep** | [Level 15](full-roadmap/level-15-interview-prep.md) | [The 100 interview questions](accelerated-roadmap/interview-questions.md) + [full answers](accelerated-roadmap/interview-answers.md) |
| **Time estimate** | Multi-month, at your own pace | 100 days of focused work |

**Recommended path:** finish the [100-day accelerated roadmap](accelerated-roadmap/README.md) first to become employable, then return to the [full roadmap](full-roadmap/README.md) for the specialist levels — managed platforms (L11), multimodal (L12), fine-tuning (L13) — as your career demands them. Every accelerated module names exactly what it skips and where to find it in the full roadmap.

---

## How important is each topic? (interview vs real-world job)

Every level in the full roadmap carries two weights from the original source: how heavily it appears in **interviews**, and how much it matters in the **day-to-day job**. They are not the same thing — and knowing the difference is how you prioritize.

| Level | Topic | Interview weight | On-the-job weight |
|---|---|---|---|
| [L0](full-roadmap/level-00-software-engineering-fundamentals.md) | Software Engineering Fundamentals | 9/10 | 10/10 |
| [L1](full-roadmap/level-01-llm-101.md) | LLM 101 | 8/10 | 7/10 |
| [L2](full-roadmap/level-02-working-with-llm-apis.md) | Working with LLM APIs (Orchestration) | 8/10 | 10/10 |
| [L3](full-roadmap/level-03-prompt-engineering.md) | Prompt Engineering | 5/10 | 8/10 |
| [L4](full-roadmap/level-04-rag.md) | RAG | 10/10 | 9/10 |
| [L5](full-roadmap/level-05-ai-agents.md) | AI Agents | 9/10 | 7/10 |
| [L6](full-roadmap/level-06-context-engineering.md) | Context Engineering | 6/10 | 8/10 |
| [L7](full-roadmap/level-07-llm-evaluations.md) | LLM Evaluations | 8/10 | 10/10 |
| [L8](full-roadmap/level-08-ai-security.md) | AI Security | 5/10 | 7/10 |
| [L9](full-roadmap/level-09-ai-system-design.md) | AI System Design | 9/10 | 8/10 |
| [L10](full-roadmap/level-10-llmops.md) | LLMOps: From Development to Production | 7/10 | 9/10 |
| [L11](full-roadmap/level-11-managed-ai-platforms.md) | Managed AI Platforms | 6/10 | 7/10 |
| [L12](full-roadmap/level-12-multimodal-101.md) | Multimodal 101: Beyond Text | 4/10 | 5/10 |
| [L13](full-roadmap/level-13-fine-tuning.md) | Fine-Tuning | 7/10 | 3/10 |
| [L14](full-roadmap/level-14-projects.md) | Projects | 10/10 | 6/10 |
| [L15](full-roadmap/level-15-interview-prep.md) | GenAI / AI Engineer Interview Prep | 9/10 | 1/10 |

Reading the table honestly:

- **RAG (L4) and Projects (L14) are the two 10/10 interview topics.** RAG is the most frequently asked technical topic and the most common job-description requirement; deployed portfolio projects are the biggest factor in getting shortlisted at all.
- **The daily job is still software engineering (L0, L2, L7 at 10/10 on-the-job).** APIs, databases, testing, debugging, deployments and evaluation are where most working hours go — most production incidents are ordinary software bugs, not model problems.
- **Some topics interview better than they work (L13 Fine-Tuning: 7/10 interview, 3/10 job).** Interviewers love asking "fine-tuning vs RAG" even though you will rarely fine-tune on the job.
- **Some topics work better than they interview (L3 Prompt Engineering: 5/10 interview, 8/10 job).** Interviewers assume you can prompt; on the job you revise prompts constantly.

Each level page explains, in the source's own words, *why* it carries its weights.

---

## What is in this section

```
roadmap/
├── README.md                    ← you are here
├── full-roadmap/                ← Roadmap 1: the complete, in-depth path (100% coverage)
│   ├── README.md                ← 16 levels · 7 phases · 286 sessions · 14 projects
│   └── level-00 … level-15      ← one page per level: modules, outcomes, weights, resources
└── accelerated-roadmap/         ← Roadmap 2: the job-focused path (~80% coverage)
    ├── README.md                ← 100 days · 6 modules · 86 units
    ├── module-1 … module-6      ← one page per module: units, day-by-day
    ├── projects.md              ← 12 portfolio projects with "done when" criteria
    ├── interview-questions.md   ← the 100 interview questions, copied exactly
    └── interview-answers.md     ← all 100 questions answered in full
```

Both roadmaps are cross-linked with the rest of this repository: every level lists the matching curriculum notes in [101 LLM Literacy](../101_LLM-Literacy/README.md), [102 AI Application Development](../102_AI-Application-Development/README.md), [103 Agentic AI](../103_Agentic%20AI/README.md) and [104 LLMOps](../104_LLMOps/README.md), the reference knowledge bases [105 AI Evaluation](../105_AI-Evaluation/README.md) and [106 AI Security & Safety](../106_AI-Security-Safety/README.md), plus this guide's own [interview section](../interview/README.md).

---

## How to use either roadmap

Three simple rules, from the original source:

1. **Start where you are.** Each level lists what you need to know first. If you already know it, skip ahead.
2. **Do one level at a time.** Each level has a few modules, and most end with a project. Go in order, because each level builds on the last.
3. **Finish by building.** A level is done when you've built its project and can do everything on its outcome list. Watching videos is not enough.
