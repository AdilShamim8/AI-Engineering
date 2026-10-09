# Get Hired

> Preparation advice reviewed October 9, 2026. Interview accounts are anecdotes, not a representative hiring survey. Use the employer's current process and demonstrate your own measured work.

---

## What Interviewers Test

### Demonstrate competencies rather than quoting prevalence

Prepare to explain implementation, model limitations, retrieval, data quality, evaluation, authorization, operations and tradeoffs. Job requirements and interview formats vary by employer. The previous percentage tables had no traceable sampling records and have been removed.

Bring a reproducible experiment, a baseline, failed cases, dataset provenance and an architecture decision record. See [the advanced path](../learning-paths/advanced-engineering.md) and [reproduced job-posting tags](../role/02-skills.md).

---

## What Interviewers Focus On by Seniority

### Junior (0–2 years)
- **Can you build it?** Working prototypes, correct implementation, clean code
- **Do you understand the basics?** How LLMs work, RAG fundamentals, basic evaluation
- **Can you learn?** Curiosity, growth mindset, awareness of the landscape
- **Less expected**: Production architecture, cost optimization, safety design

### Mid-Level (2–5 years)
- **Can you build it well?** Production-quality code, error handling, monitoring
- **Do you understand trade-offs?** Cost vs. quality, latency vs. accuracy, build vs. buy
- **Can you evaluate it?** Metrics, datasets, LLM-as-judge, regression testing
- **Can you communicate?** Explaining AI to non-experts, writing technical docs

### Senior (5–8 years)
- **Can you design the system?** Architecture, component selection, failure mode analysis
- **Can you lead?** Technical direction, mentoring, code review standards
- **Can you own it in production?** Incident response, cost management, SLA ownership
- **Can you make hard trade-offs?** Model selection, safety vs. capability, timeline vs. quality

### Staff+ (8+ years)
- **Can you define the strategy?** Technical roadmap, build vs. buy, platform vs. product
- **Can you influence the organization?** Standards, best practices, hiring bar
- **Can you navigate ambiguity?** Undefined problems, conflicting requirements, evolving landscape
- **Can you think multi-system?** How does this AI feature fit into the broader architecture?

---

## What Separates Candidates

> Based on 60+ interviews at top AI startups (Series A–D), conducted by hiring managers and senior engineers.

### Top Candidates (Offers Extended)

1. **Have production AI stories with specific metrics.** "Our RAG pipeline served 50K queries/day with 3% hallucination rate and $0.008 cost per query."

2. **Reason from first principles.** When asked about a new system, they don't jump to tools. They start with requirements, then constraints, then architecture, then tools.

3. **Acknowledge what they don't know.** "I haven't used that specific tool, but based on the architecture you described, here's how I'd approach it."

4. **Have opinions formed through experience.** "In my experience, semantic caching works well for FAQ-style queries but poorly for exploratory queries because..."

5. **Think about safety by default.** They don't need to be prompted to discuss guardrails, PII handling, or prompt injection.

6. **Communicate clearly at multiple levels.** They can explain the same concept to a junior engineer, a PM, and a VP in appropriate language.

7. **Show evaluation thinking.** Every design decision includes "and here's how I'd measure whether this actually works."

### Average Candidates (No Offer)

1. **Tool-focused rather than concept-focused.** "I used LangChain for RAG" vs. "I built a RAG pipeline — here's the retrieval strategy and why."

2. **Can't explain why.** They built something but can't articulate the reasoning behind design decisions.

3. **No production awareness.** The system works on a laptop but they haven't considered latency, cost, or failure modes at scale.

4. **Ignore evaluation.** "It worked well" without metrics or methodology.

5. **Over-rely on one framework.** "I'd use LangChain for everything" without understanding the trade-offs.

6. **Don't ask clarifying questions.** They jump into answers without understanding the problem.

7. **No safety consciousness.** They don't mention guardrails, PII, or prompt injection unless explicitly asked.

---

## Portfolio Strategy

> See the [Portfolio section](../portfolio/) for detailed guidance on building an AI engineering portfolio.

**Key points for 2026**:

- **A GitHub with 2–3 substantial AI projects is more valuable than 20 toy projects**
- **Projects should demonstrate production thinking**: evaluation, monitoring, cost awareness
- **Include a blog or writing**: Even 3–4 posts about AI engineering decisions show depth
- **Contribute to open-source AI tools**: Even small contributions to LangChain, LlamaIndex, or vLLM signal engagement
- **Your portfolio is your best preparation**: The projects you build for your portfolio become the stories you tell in interviews

---

## Before You Apply

### GitHub Portfolio Checklist
- [ ] 2–3 AI projects with clean READMEs and documentation
- [ ] At least one RAG pipeline project
- [ ] At least one agent or tool-use project
- [ ] At least one evaluation framework or benchmarking project
- [ ] Clean git history showing your thought process
- [ ] No hardcoded API keys or secrets
- [ ] Working code with setup instructions

### Project Stories to Prepare
For each project, prepare a 2-minute pitch covering:
- What problem does it solve?
- What's the architecture?
- What were the key design decisions and trade-offs?
- What would you change with more time?
- What did you learn?

### Opinions on AI (Expected in 2026)
Interviewers expect you to have informed opinions on current AI topics:

- **When is RAG better than fine-tuning?** (And vice versa)
- **What's your take on agent frameworks?** (LangGraph vs. CrewAI vs. custom)
- **How do you evaluate AI systems?** (Your evaluation philosophy)
- **What's overhyped in AI right now?** (Shows independent thinking)
- **What's underhyped?** (Shows depth of understanding)
- **How do you think about AI safety?** (Not just "safety is important" — specific practices)
- **What's your mental model for LLM costs?** (Shows production experience)

### Essay Requirements
Some companies (especially Anthropic, OpenAI, and mission-driven startups) require written essays or responses as part of the application:

- Anthropic: "Why do you want to work on AI safety?"
- OpenAI: "Describe a technical challenge you've overcome"
- Startups: "What excites you about AI engineering?"

**Tips**: Be specific, be genuine, and connect your answer to the company's mission. Generic essays are obvious and forgettable.

---

## Resume Tips for 2026

### AI Engineering-Specific Resume Tips

1. **Lead with impact, not tools.** "Reduced hallucination rate by 60%" not "Used LangChain and Pinecone"

2. **Quantify everything.** "Built a RAG pipeline serving 10K queries/day at $0.02/query" is 10x more compelling than "Built a RAG pipeline"

3. **Show production experience.** "Deployed to production with monitoring and alerting" vs. "Built a prototype"

4. **Include evaluation.** "Evaluated with custom golden dataset of 200 examples" shows maturity

5. **Mention cost awareness.** "Optimized token usage to reduce cost by 40%" is a strong differentiator

6. **Don't list every AI framework.** "LangChain, LlamaIndex, CrewAI, AutoGen, Haystack,..." looks like keyword stuffing. List what you've used in production.

7. **Include a projects section.** If you don't have professional AI experience, personal projects can demonstrate capability.

8. **Tailor to the company.** Emphasize RAG experience for RAG-heavy roles, agent experience for agent-heavy roles.

### What Not to Include
- "ChatGPT expert" or "Prompt engineer" as a standalone skill (too generic)
- Course certificates without demonstrated application
- AI-generated cover letters (they can tell)
- Every AI tool you've ever touched (focus on depth, not breadth)

---

## Common Mistakes

### In Interviews
1. **Not asking clarifying questions** — this signals poor communication and bad engineering judgment
2. **Jumping to implementation before understanding the problem** — design first, code second
3. **Ignoring production concerns** — cost, latency, monitoring, error handling
4. **Being too tool-specific** — "I'd use LangChain" instead of "I'd build a retrieval and generation pipeline"
5. **Not showing your work** — silent coding or designing without verbalizing your thought process
6. **Dismissing safety concerns** — "We can add guardrails later" is a red flag
7. **Not having specific metrics** — vague claims of improvement without numbers
8. **Failing the "why" test** — if you can't explain why you made a decision, it suggests you didn't evaluate alternatives

### In Job Search
1. **Only applying to big tech** — the best AI engineering roles are often at mid-size companies and startups
2. **Not leveraging your network** — 40%+ of AI engineering hires come through referrals
3. **Applying without tailoring** — generic applications get generic results
4. **Not preparing for AI-specific interviews** — treating them like traditional SWE interviews
5. **Ignoring company mission and values** — especially at companies like Anthropic where mission alignment is evaluated
6. **Not following up** — a thoughtful follow-up email after interviews shows professionalism
7. **Negotiating poorly** — accepting the first offer without understanding your market value

---

## How to Prepare (From People Who Succeeded)

### Mimansa Jaiswal — AI Engineer at a Top AI Lab
> "I spent 8 weeks preparing. The first 4 weeks were building — I created 3 AI projects that I could present in depth. The last 4 weeks were practicing — I did mock interviews every week and refined my stories. The projects were the foundation; the practice was the polish."

**Key advice**: Build first, practice second. Your projects give you the stories; practice helps you tell them well.

### Yuan Meng — Staff AI Engineer at a Series C Startup
> "The biggest surprise was how much interviewers cared about evaluation. Every system design question eventually came back to 'how would you measure this?' I wish I'd spent more time on evaluation methodology and less on learning new frameworks."

**Key advice**: Evaluation is the most underrated preparation topic. Spend at least 20% of your prep time on evaluation.

### Janvi Kalra — Senior AI Engineer at a FAANG Company
> "The behavioral round at [big tech] was harder than I expected. They wanted specific stories about handling AI failures in production, and they probed deep. I had good technical stories but hadn't practiced the behavioral format. Prepare behavioral stories with the same rigor as technical topics."

**Key advice**: Don't treat behavioral as an afterthought. Prepare 6–8 AI-specific stories using the SAIL framework.

---

## Suggested Timeline (8–12 Weeks)

### Weeks 1–2: Foundation
- [ ] Build or polish 2–3 portfolio projects
- [ ] Review LLM fundamentals (architecture, inference, sampling)
- [ ] Practice explaining concepts out loud (attention mechanism, RAG pipeline, agent design)

### Weeks 3–4: Technical Depth
- [ ] Deep-dive on RAG, agents, and evaluation
- [ ] Learn context engineering (new for 2026)
- [ ] Practice from-scratch ML implementations (attention, LoRA, KV cache)
- [ ] Build an evaluation framework for one of your projects

### Weeks 5–6: Interview Practice
- [ ] 2–3 mock system design interviews
- [ ] 2–3 mock coding interviews (mix of DSA and AI coding)
- [ ] Prepare 6–8 behavioral stories using SAIL framework
- [ ] Practice project deep-dive presentation (15 minutes)

### Weeks 7–8: Company-Specific Prep
- [ ] Research target companies (products, tech stack, interview format)
- [ ] Tailor resume and portfolio for each company
- [ ] Practice company-specific question types
- [ ] Write and refine essays/cover letters

### Weeks 9–10: Active Interviewing
- [ ] Apply to 5–8 companies (mix of reach, target, safety)
- [ ] Schedule interviews strategically (safety companies first, reach companies last)
- [ ] Debrief after each interview and adjust preparation

### Weeks 11–12: Close and Negotiate
- [ ] Collect offers and compare
- [ ] Negotiate (see [After the Interview](04-after-the-interview.md))
- [ ] Make decision and accept

---

## Resources

### Books
- **"Designing Machine Learning Systems"** — Chip Huyen (ML system design foundation)
- **"Building LLM Apps"** — Valentina Alto (LLM application patterns)
- **"AI Engineering"** — Chip Huyen (AI engineering practices, 2025)
- **"Machine Learning System Design Interview"** — Ali Aminian & Alex Xu (interview prep)
- **"Deep Learning"** — Goodfellow, Bengio, Courville (theory reference)

### Courses
- **DeepLearning.AI short courses** — Practical LLM, RAG, and agent courses
- **Stanford CS229 / CS224N** — ML and NLP fundamentals (free lecture videos)
- **Andrej Karpathy's "Neural Networks: Zero to Hero"** — From-scratch implementations
- **Fast.ai** — Practical deep learning
- **Full Stack LLM Bootcamp** — Comprehensive AI engineering course

### Coding Practice
- **LeetCode** — For companies that still ask DSA (Medium difficulty, focus on arrays/strings/graphs)
- **HuggingFace tutorials** — Hands-on ML implementation practice
- **Build your own projects** — The best coding practice is building real AI systems

### ML/LLM Coding Prep
- Implement self-attention from scratch (30 min)
- Implement LoRA from scratch (20 min)
- Implement a simple KV cache (20 min)
- Build a RAG pipeline from scratch (60 min)
- Build a tool-calling agent (45 min)
- Implement an evaluation pipeline (30 min)

### System Design
- **"Designing Data-Intensive Applications"** — Martin Kleppmann (foundation)
- **Alex Xu's System Design Interview books** — Practice problems
- **Eugene Yan's blog** — Applied ML systems design
- **Company engineering blogs** — Read how real systems are built

### Evaluation
- **RAGAS documentation** — RAG evaluation framework
- **DeepEval documentation** — LLM evaluation framework
- **LangSmith tutorials** — Observability and evaluation
- **"Evaluating LLMs"** — Various survey papers and blog posts

### Behavioral
- **Amazon Leadership Principles** — Framework for structured behavioral answers
- **STAR/SAIL frameworks** — Structure for behavioral stories
- **"Cracking the Coding Interview" behavioral chapter** — General behavioral prep

### Organization
- **Notion or Obsidian** — Track preparation progress, notes, and stories
- **Spaced repetition** — Use Anki for theory concepts
- **Interview journal** — Record every interview experience for debrief

---

## Career Transitions

### From Software Engineering to AI Engineering
- **Easiest transition**: You already have production engineering skills. Focus on AI-specific knowledge (LLMs, RAG, agents, evaluation).
- **Biggest gap**: ML/AI theory and evaluation methodology.
- **Recommended path**: Build 2–3 AI projects → Take DeepLearning.AI courses → Apply to AI-forward companies.
- **Timeline**: 3–6 months of focused preparation.

### From Data Science / ML to AI Engineering
- **Easiest transition**: You already understand ML theory and evaluation.
- **Biggest gap**: Production engineering (API design, deployment, monitoring, cost optimization).
- **Recommended path**: Build production AI applications → Focus on engineering practices → Apply to AI engineering roles (not ML research roles).
- **Timeline**: 2–4 months of focused preparation.

### From Research to AI Engineering
- **Easiest transition**: Deep understanding of models and theory.
- **Biggest gap**: Production engineering, cost awareness, and "good enough" mentality (researchers tend to over-optimize models; engineers optimize the whole system).
- **Recommended path**: Build a production AI application end-to-end → Practice system design → Apply to applied AI roles.
- **Timeline**: 3–6 months of focused preparation.

### From Other Fields (Product, Design, etc.)
- **Easiest transition**: Domain expertise + AI is incredibly valuable.
- **Biggest gap**: Technical depth (coding, system design, ML fundamentals).
- **Recommended path**: Learn Python → Build AI projects → Take comprehensive courses → Apply to domain-specific AI roles (e.g., AI for healthcare if you have healthcare background).
- **Timeline**: 6–12 months of focused preparation.

---

## Job Search and Networking

### Where to Find AI Engineering Jobs (2026)

| Source | Quality | Notes |
|--------|---------|-------|
| Company career pages | High | Best for specific companies you're targeting |
| LinkedIn | Medium–High | Good for volume, set alerts for "AI Engineer" |
| Wellfound (AngelList) | Medium | Good for startups |
| Y Combinator jobs | Medium | Good for early-stage startups |
| AI-specific job boards | Medium | aisjobs.net, ai-jobs.net |
| Referrals | Highest | 40%+ of hires come through referrals |
| Conferences and meetups | High | NeurIPS, ICML, AI Engineer Summit, local meetups |
| Twitter/X | Medium | Many AI companies post roles on X |
| Direct outreach | Medium | DM founders/hiring managers at startups |

### Networking Strategy

1. **Build in public.** Share your AI projects and learnings on Twitter/X and LinkedIn.
2. **Contribute to open source.** Even small PRs to AI tools get you noticed.
3. **Attend events.** AI Engineer Summit, local AI meetups, company-hosted events.
4. **Write.** Blog posts about AI engineering decisions demonstrate depth and reach hiring managers.
5. **Informational interviews.** Reach out to AI engineers at target companies for 15-minute chats.
6. **Be specific in outreach.** "I loved your blog post about [X] and I'm building something similar" gets more responses than "I'd love to connect."

---

## Negotiation and Offers

### Compare actual offer terms

The previous salary ranges were not supported by traceable records. Use [the compensation comparison guide](07-global-compensation-and-job-market.md) to separate recurring cash, one-time cash and equity, and retain dates and location-specific evidence.

### Key Negotiation Points

1. **Know your market value.** Use Levels.fyi, Blind, and Glassdoor to understand compensation ranges for your target role and level.

2. **Total compensation matters more than base salary.** Separate cash from equity and compare the actual grant and vesting terms; no universal equity share is established here.

3. **Negotiate the equity, not just the base.** At startups, equity has the most upside. At big tech, equity refreshers are standard.

4. **Get competing offers.** The single strongest negotiation lever is a competing offer. Even if you prefer Company A, having an offer from Company B gives you leverage.

5. **Understand the equity.** At startups: What's the valuation? What's your strike price? What's the vesting schedule? What happens if the company raises at a down round? See [After the Interview](04-after-the-interview.md) for detailed equity evaluation guidance.

6. **Don't negotiate against yourself.** Let them make the first offer. Then counter with data, not feelings.

7. **Consider the full package.** Signing bonus, relocation, remote work policy, learning budget, and 401(k) match all have real value.

8. **Be professional but firm.** "I'm excited about the role and I'd like to discuss compensation. Based on my research and competing offers, I was expecting [range]."

### Big Tech vs. Startup Compensation

| Factor | Big Tech | AI Startup |
|--------|----------|------------|
| Base salary | Higher | Lower |
| Equity value | Known (public stock) | Speculative (options) |
| Equity upside | Moderate (already large) | Potentially huge (or zero) |
| Liquidity | RSUs vest and are sellable | Options may never liquidate |
| Risk | Low (stable employment) | High (startup may fail) |
| Growth | Slower (more process) | Faster (more ownership) |
| Impact | Incremental | Potentially company-defining |

---

## Sources

[^1]: Legacy aggregate compensation attribution was not reproducible. See the compensation comparison guide for evidence requirements.
[^2]: Interview reports aggregated from Blind, Glassdoor, and LeetCode Discuss, 2025–2026.
[^3]: Mimansa Jaiswal, Yuan Meng, Janvi Kalra — interview preparation advice from social media posts and blog articles, 2025–2026. Names used with context from public posts.
[^4]: Unverified legacy survey attribution; no identifiable survey release was established in this review.
[^5]: Unverified legacy report attribution; no identifiable report was established in this review.
[^6]: Company engineering blogs and career pages, 2024–2026.
[^7]: "How to Negotiate Your AI Engineering Offer", various guides and practitioner advice, 2025.

---

> **Next**: [After the Interview →](04-after-the-interview.md)
