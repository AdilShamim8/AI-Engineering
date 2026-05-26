# Getting Hired

Based on 100+ sources: candidate stories, hiring manager observations, career blogs, and interview guides. These are patterns from what candidates and hiring managers actually report.


## What Interviewers Test

What job postings list (baseline everyone claims):

- Python, TensorFlow/PyTorch, SQL
- "Experience with LLMs" or "familiarity with machine learning"
- Cloud platforms (AWS/GCP/Azure)
- Generic "strong communication skills"

What interviewers actually test and value:

- Evaluation frameworks over model building. "Unsuccessful LLM products almost always share a common root cause: a failure to create robust evaluation systems." [^hamel-husain] Every RAG system should have an eval harness [^reddit-ycombinator-assignments]
- Cost and latency reasoning. Token budgets, per-query costs, model routing. "100K daily users x 10 interactions x ~2K tokens = 2B tokens/day = $13K/day on GPT-4 Turbo" - this kind of estimation separates production thinkers from prototype thinkers [^interviewquery-2025] [^sdh-genai]
- Trade-off fluency. Not "what is RAG?" but "when would you NOT use RAG?" Retrieval speed vs. context length, fine-tuning vs. prompting, GPU cost vs. latency [^interviewnode] [^designgurus]
- Systems thinking. Think in loops: retrieval, generation, feedback. "Generative AI system design is no longer about pipelines, it's about lifecycles" [^interviewnode]
- Observability. Logging, tracing, drift detection, hallucination tracking. TTFT, TBT, tokens/second, per-user costs. From day one, not as an afterthought [^chip-huyen-platform]
- Safety and guardrails. Prompt injection, data leakage, unsafe tool execution. Skipping this signals weak production awareness [^sdh-anthropic] [^igotanoffer]
- AI fluency with coding tools. How you prompt, verify, and direct AI tools (Cursor, Claude Code) - not just whether you can code [^interviewquery-2025]
- Python depth. Race conditions, GIL, async patterns, concurrency vs. parallelism. "I look for strong Python programmers because we can't expect people to have GenAI experience yet" [^fahd-mirza]
- DSA fundamentals. Algorithm rounds at Eightfold, OpenAI, Anthropic, xAI. Anthropic: 90-minute CodeSignal requiring perfect correctness. xAI: LeetCode Hard over volume [^eightfold-internship] [^sundeep-teki]
- ML implementation from scratch. Multi-Head Attention, Transformer layers, LoRA, KV cache from memory at frontier labs. Use "shape suffixes" (Noam Shazeer method) to track tensor dimensions [^mimansa-jaiswal-resources] [^sundeep-teki]
- Full-stack capability. Many AI engineer roles are "low-key full stack roles." Expect questions on the JS event loop, database choices, message queues alongside GenAI [^fahd-mirza]

What interviewers focus on by seniority:

- Junior/Intern - coding fundamentals, basic ML concepts, willingness to learn, project enthusiasm
- Mid-level - end-to-end system knowledge, RAG pipelines, embeddings, production awareness
- Senior - trade-off fluency, system design at scale, failure mode reasoning, cost optimization
- Staff+ - technical leadership, cross-team influence, project presentations, organizational impact


## What Separates Candidates

From 50+ AI engineer interviews at top startups: [^fonzi-ai-50-interviews]

- The first 5 minutes decide everything. Lead with impact, not model names
- Talk like a builder, not a researcher. "We tried fine-tuning but it hallucinated too often, so we switched to hybrid RAG"
- Cost awareness is a superpower. One engineer showed a before-and-after cost breakdown proving 70% reduction in OpenAI spend - got an offer the next day
- Honesty beats bluffing. "I haven't worked with LangSmith yet, but if you're using it for evals, I'd love to understand how you've set up your metrics" - turned into a job offer
- You don't need to be a unicorn. Companies will hire strong generalists with depth in 1-2 areas
- One brilliant answer on a fundamental can carry a mediocre interview - and failing one fundamental can tank a strong one [^proptech-founder]
- Tinkerer mindset. Strong opinions on tools, staying current. "Tinkerers who thrive in uncertainty" over rigid academic approaches [^promptlayer]
- Honest uncertainty is a feature. Knowing what you don't know signals real production experience [^techeon]

The 90/10 rule: 90% of interview success comes from prior career decisions - university, internships, companies, relationships. Only 10% is application strategy, networking, and negotiation [^sundeep-teki]


## Portfolio Strategy

See [portfolio project ideas and strategy](../portfolio/README.md) for detailed guidance on project selection, README writing, and what hiring managers look at.


## Before You Apply

Some companies require more than a resume upfront:

- A GitHub portfolio with AI projects - Dentsu Creative asks candidates to submit "portfolio or GitHub showcasing AI/automation projects you've built"
- A "best project" story with metrics - Wolters Kluwer asks for a "Statement of Exceptional Work" covering your role, technical challenges, and measurable impact
- Opinions on AI, not just skills - Dentsu Creative asks "your thoughts on where most companies go wrong with AI implementation"
- Be ready to write, not just code - Strange Loop Labs requires a 1-2 page essay. Apollo.io requires 5 short screening questions answered in the application

Resume tips:

- Lead with impact, not model names. "Reduced customer support response time by 40%" beats "Experience with LangChain and GPT-4" [^fonzi-ai-50-interviews]
- Avoid multi-column LaTeX formats - ATS parsing issues. Consider Typst instead [^mimansa-jaiswal]
- Prepare a self-presentation blurb on 2-3 areas of expertise. ~10 iterations over 12 weeks [^mimansa-jaiswal]
- Create a website or blog. Direct LinkedIn outreach to founders proved effective for startups [^mimansa-jaiswal]


## Common Mistakes

In the interview:

- Jumping to fine-tuning too early. Default to prompt engineering with RAG; fine-tune only if extreme specialization or latency demands it [^igotanoffer]
- Treating the LLM as a source of truth. Ground with retrieval, tools, or citations [^igotanoffer]
- Skipping evaluation and monitoring. Explain how output quality and regressions will be measured [^igotanoffer]
- Name-dropping tools without trade-offs. Instead of "I'd use LangChain," explain why. If you mention Redis, know when it's wrong [^interviewnode] [^hellointerview-openai]
- Ignoring failure modes. Discuss what breaks, how failures are detected, graceful degradation [^igotanoffer]
- Over-engineering from the start. Get a working implementation first, optimize on follow-ups [^hellointerview-openai]
- Bluffing on gaps. "I need a hint" outperforms bluffing [^fonzi-ai-50-interviews] [^mimansa-jaiswal]
- Failing on fundamentals. Know how LLMs work (tokenization, transformers, next-token prediction), race conditions, the GIL [^fahd-mirza]

In the job search:

- Pursuing only compensation. "What problem do you want to solve?" - candidates who can't answer get passed on [^fonzi-ai-failed-hires]
- Overselling outdated skills. "Most AI & ML candidates fail interviews not because they lack skills, but because they describe the wrong ones" [^fonzi-ai-failed-hires]
- Misunderstanding role fragmentation. "ML Engineer" has split into Applied ML, MLOps, LLM Systems, Research Engineering [^amplework]
- Not having projects ready. Some companies require portfolio upfront. Have 2-3 polished projects before applying
- Too little effort on take-homes. Best candidates document decisions, test edge cases, submit with a Loom video [^fonzi-ai-50-interviews]
- Not asking clarifying questions. "Asking questions is never a bad thing - it demonstrates communication skills" [^aidi-rivera]


## How to Prepare

### From people who succeeded

Mimansa Jaiswal - 20+ companies (Anthropic, OpenAI, Meta, Amazon, Apple, Google), multiple offers: [^mimansa-jaiswal]

- 12 weeks of preparation, ~6 hours daily of interview-specific practice
- 150+ NeetCode problems completed
- ~10 iterations on self-presentation blurb
- Organized preparation in Notion with 7 major sections and categorized questions ("Aced it," "Took time," "Didn't get it," "Just saw it somewhere")
- Transparency about limitations performed better than bluffing: openly disclosed experience with 0.5-1B parameter models only, LoRA focus, no pretraining experience

Yuan Meng - 5-10 onsite companies at senior+ level, offers from nearly all: [^yuan-meng]

- Deep domain expertise was the competitive advantage: "every aspect of RecSys since 2022"
- "Why you? Why not anyone else?" is the central hiring question. Interview success correlates more with domain expertise and passion alignment than perfect execution across all rounds
- NeetCode 250 with focus on problem-solving intuition, not memorization
- Read "Understanding Deep Learning" by Simon Prince thoroughly
- Used SAIL structure (Situation, Action, Impact, Learning) for behavioral interviews

Janvi Kalra - 46 companies, SWE to AI engineer, now at OpenAI: [^janvi-kalra]

- 6 months of interviewing across product, infrastructure, and model companies
- Used Cracking the Coding Interview and NeetCode Blind 75 with spaced repetition
- Hackathons (weekend and multi-week online) were more effective than courses
- Self-taught when denied internal AI team role: built LLM apps, attended hackathons, wrote about it publicly
- Alex Xu System Design Interview books: "just reading those, really understanding them, doing them again and again"

General advice:

1. Build 2-3 end-to-end projects: RAG app, autonomous agent, something deployed
2. Practice explaining trade-offs aloud - verbal reasoning matters more than perfect code. "Practice verbally explaining concepts without hesitation - fluency signals experience" [^reddit-generativeai]
3. Learn evaluation early: Ragas, DeepEval, LLM-as-judge frameworks
4. Show production readiness: Docker, CI/CD, monitoring - not just notebooks
5. Understand cost/latency: caching, batching, model routing decisions
6. Practice storytelling, not memorized answers - record yourself explaining your last project in 60 seconds [^fonzi-ai-50-interviews]
7. For agentic AI roles: at senior/staff levels, interviewers pick 3-5 questions and drill deep into failure modes and trade-offs rather than covering many topics superficially. Prepare to explain the orchestrator vs LLM responsibility split, how you enforce autonomy boundaries structurally, and how you handle agent termination conditions [^techeon]
8. Treat take-homes like a mini job. Document decisions, test edge cases, submit with a Loom video. One engineer built a CLI tool for summarizing PDFs with configurable models and chunking strategies - had two competing offers within 72 hours [^fonzi-ai-50-interviews]

### Suggested timeline (8-12 weeks)

- Weeks 1-2: coding fundamentals. NeetCode 150/250, focus on patterns not memorization
- Weeks 3-4: ML/LLM implementation. Transformers, attention mechanisms, LoRA from scratch using NumPy/PyTorch. Practice on Deep-ML
- Weeks 5-6: system design. Study RAG architecture, agentic design patterns, model serving. Read Chip Huyen's AI Engineering and engineering blogs from target companies
- Weeks 7-8: build or polish 1-2 portfolio projects with evaluation, deployment, and documentation
- Weeks 9-10: mock interviews. Practice verbal trade-off explanations, behavioral stories (SAIL/STAR), system design walkthroughs aloud
- Weeks 11-12: company-specific prep. Study target company blog posts, products, values. Refine self-presentation blurb. Practice with recording yourself

### Resources

Books and courses:

- Chip Huyen: AI Engineering (2025) [^chip-huyen-book] - the definitive book on building with foundation models
- "Understanding Deep Learning" by Simon Prince [^udl-book] - recommended for ML fundamentals; develop deep conceptual understanding rather than checkbox memorization [^yuan-meng]
- "Designing Data-Intensive Applications" [^ddia] - skim chapters 1-11 for system design prep [^yuan-meng]
- Andrej Karpathy: Neural Networks - Zero to Hero [^karpathy-zero-to-hero]

Articles and patterns:

- Eugene Yan: Patterns for Building LLM-based Systems [^eugene-yan-patterns] - 7 core patterns (evals, RAG, fine-tuning, caching, guardrails, defensive UX, data flywheel)
- What We Learned from a Year of Building with LLMs [^applied-llms]

Coding practice:

- NeetCode 250 [^neetcode] - recommended by multiple successful candidates. Focus on problem-solving intuition; connect problems to real web-scale data processing challenges [^yuan-meng]. Use spaced repetition [^janvi-kalra]
- Deep-ML [^deep-ml] - ML-specific coding practice for implementing architectures from scratch [^yuan-meng] [^mimansa-jaiswal-resources]
- Great Frontend [^great-frontend] - front-end interview questions for full-stack AI engineer roles [^janvi-kalra]

ML/LLM coding prep:

- Mimansa Jaiswal's breakdown of what to implement from scratch for ML coding rounds (25-35 min, no debugging): neural networks, LSTMs, RNNs in NumPy/PyTorch; attention mechanisms (cached, grouped query, multi-head); Transformer components; RAG/inference decoding strategies (top-p, top-k, beam search) [^mimansa-jaiswal-resources]

System design:

- Alex Xu: System Design Interview books [^alex-xu-system-design] - "just reading those, really understanding them, doing them again and again" [^janvi-kalra]
- Company engineering blogs from Netflix, Uber, Pinterest, and other target companies for ML infra design prep [^yuan-meng]

Evaluation:

- Maven: AI Evals for Engineers & PMs [^maven-evals] - Hamel Husain and Shreya Shankar

Behavioral:

- SAIL structure (Situation, Action, Impact, Learning) for behavioral interviews - map stories explicitly to company values [^yuan-meng]
- Prepare distinct examples per interview - "repeatedly telling the same stories can make responses sound mechanical." Vary personal introductions. Use water breaks between STAR paragraphs [^mimansa-jaiswal-resources]

Organization:

- Notion for tracking preparation across 7+ sections [^mimansa-jaiswal]
- Zotero and Raindrop for paper and research tracking
- Record yourself explaining projects in 60 seconds to refine storytelling

See [Awesome AI Engineering](../awesome.md) for the full collection.


## Career Transitions

If you are transitioning from another engineering role, see the [learning paths](../learning-paths/README.md#role-specific-guides) - they cover the transition from backend, frontend, data engineering, data science, and ML engineering backgrounds.

Key principle for all transitions: "Start the job before you have it. Start writing code to do the things you'd like it to do. Building something yourself is what gets you specific knowledge, the type of knowledge you can't get from courses." [^zero-to-mastery]


## Job Search and Networking

- Categorize the AI market to focus your search. Three categories: product companies (Cursor, Codium), infrastructure companies (Modal, Fireworks, Pinecone, Braintrust), and model companies (OpenAI, Anthropic, Google, Meta). Decide which segment excites you most [^janvi-kalra]
- Direct outreach works. LinkedIn messages to founders and hiring managers proved effective for startups. "Reach out to connections despite unpublished work - most people were immensely supportive" [^mimansa-jaiswal]
- Hackathons as networking and learning. Weekend and multi-week online hackathons serve as both skill development and networking. Building in public (blog posts, Twitter threads) was more effective than courses when the field moves this fast [^janvi-kalra]
- In-person interviews are back. In-person rounds increased from 24% (2022) to 38% (2025) to counter cheating concerns. More frontier labs require in-person onsites. Be prepared to travel [^interviewquery-2025]
- Referrals matter more than cold applications. Network-based hiring is increasing as AI-generated applications flood pipelines. Recruiters can detect when candidates feed resumes directly into ChatGPT. Authentic application materials outperform AI-polished generic submissions [^hn-referrals]
- Top candidates accept offers within 2-3 weeks. Companies with slow processes lose strong applicants. Be prepared to move quickly, and manage your interview timeline so onsites cluster together [^juicebox-ai]
- References matter more than before. Most top companies now require 2-3 references from recent managers and colleagues. Team matching has become competitive; strong candidates may wait weeks for ideal teams [^yuan-meng]


## Negotiation and Offers

- Your strongest negotiation move is a competing offer. Direct all leverage toward the equity grant size, not base salary, since base bands at each level are relatively narrow [^teamrora]
- Always benchmark by total compensation, not just base pay. Equity, bonuses, and cloud credits for AI experimentation can add 20-40% to your real annual package. At Meta, total compensation for an E4 MLE is ~$332K, E5 ~$492K, E6 ~$648K annually [^interviewquery-salary]
- AI engineers earn 10-20% more than general software engineers due to specialized expertise. Professionals with AI expertise earn 56% more on average than peers without it [^ziprecruiter]
- Startup due diligence like an investor. "All engineers that take a pay cut to go to a startup should have an informed thesis on why they think that company is going to grow during their tenure." Evaluate: (1) revenue and revenue growth rate, (2) large market with room to expand, (3) loyal/obsessed customers, (4) competitive positioning. If a startup will not share financials after you have an offer, that is a red flag [^janvi-kalra]
- Watch for offer expiration pressure. "Seven-day expiration windows - too short in my view - forcing me to request extensions." Ask for extensions when needed; companies that refuse may signal cultural issues [^mimansa-jaiswal]

Compensation ranges (2025-2026 US market):

| Level | Big Tech Total Comp | AI Startup Range |
|---|---|---|
| Junior/New Grad | $150K-$250K | $120K-$200K + equity |
| Mid-level | $250K-$400K | $180K-$300K + equity |
| Senior | $350K-$500K | $250K-$400K + equity |
| Staff+ | $500K-$800K+ | $350K-$600K + equity |

Ranges approximate; varies significantly by company, location, and specific role. [^interviewquery-salary] [^mimansa-jaiswal]


## Sources

[^hamel-husain]: [Hamel Husain: Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/)
[^interviewquery-2025]: [InterviewQuery: AI Interview Trends 2025](https://www.interviewquery.com/p/ai-interview-trends-tech-hiring-2025)
[^promptlayer]: [PromptLayer: The Agentic System Design Interview](https://blog.promptlayer.com/the-agentic-system-design-interview-how-to-evaluate-ai-engineers/)
[^techeon]: [TechEon: Agentic AI System Design Interview Guide](https://atul4u.medium.com/the-complete-agentic-ai-system-design-interview-guide-2026-f95d0cfeb7cf)
[^reddit-ycombinator-assignments]: [Reddit r/ycombinator - AI Engineer Interview Assignments](https://www.reddit.com/r/ycombinator/comments/1jnfijm/what_is_your_interview_assignment_for_ai_engineers/)
[^sundeep-teki]: [Dr. Sundeep Teki: AI Research Engineer Interview Guide](https://www.sundeepteki.org/advice/the-ultimate-ai-research-engineer-interview-guide-cracking-openai-anthropic-google-deepmind-top-ai-labs)
[^fonzi-ai-50-interviews]: [Fonzi AI: 50+ AI Engineer Interviews](https://medium.com/fonzi-ai/what-ive-learned-from-sitting-in-on-50-ai-engineer-interviews-c493696453c4)
[^proptech-founder]: [PropTech Founder: AI Engineer Interview](https://www.youtube.com/watch?v=leXRiJ5TuQo)
[^mimansa-jaiswal]: [Mimansa Jaiswal: LLM/ML Job Interviews](https://mimansajaiswal.github.io/posts/llm-ml-job-interviews-fall-2024-process/)
[^mimansa-jaiswal-resources]: [Mimansa Jaiswal: Interview Resources](https://mimansajaiswal.github.io/posts/llm-ml-job-interviews-resources/)
[^yuan-meng]: [Yuan Meng: MLE Interviews 2.0](https://www.yuan-meng.com/posts/mle_interviews_2.0/)
[^janvi-kalra]: [Janvi Kalra / Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/from-software-engineer-to-ai-engineer)
[^reddit-generativeai]: [Reddit r/generativeAI - How to Clear AI Interviews](https://www.reddit.com/r/generativeAI/comments/1p4yrjk/how_to_clear_interviews_in_ai_gen_rag_llm/)
[^chip-huyen-book]: [Chip Huyen: AI Engineering](https://huyenchip.com/books/)
[^udl-book]: [Understanding Deep Learning](https://udlbook.github.io/udlbook/)
[^ddia]: [Designing Data-Intensive Applications](https://dataintensive.net/)
[^karpathy-zero-to-hero]: [Andrej Karpathy: Neural Networks - Zero to Hero](https://karpathy.ai/zero-to-hero.html)
[^eugene-yan-patterns]: [Eugene Yan: Patterns for Building LLM-based Systems](https://eugeneyan.com/writing/llm-patterns/)
[^applied-llms]: [What We Learned from a Year of Building with LLMs](https://applied-llms.org/)
[^neetcode]: [NeetCode](https://neetcode.io/)
[^deep-ml]: [Deep-ML](https://www.deep-ml.com/)
[^great-frontend]: [Great Frontend](https://www.greatfrontend.com/)
[^alex-xu-system-design]: [Alex Xu: System Design Interview](https://www.amazon.com/System-Design-Interview-insiders-Second/dp/B08CMF2CQF)
[^maven-evals]: [Maven: AI Evals for Engineers and PMs](https://maven.com/parlance-labs/evals)
[^interviewnode]: [InterviewNode: GenAI System Design Patterns](https://www.interviewnode.com/post/generative-ai-system-design-interview-patterns-you-should-know)
[^designgurus]: [DesignGurus: OpenAI System Design Questions](https://www.designgurus.io/blog/openai-system-design-interview-questions)
[^chip-huyen-platform]: [Chip Huyen: Building a GenAI Platform](https://huyenchip.com/2024/07/25/genai-platform.html)
[^sdh-anthropic]: [System Design Handbook: Anthropic Interview](https://www.systemdesignhandbook.com/guides/anthropic-system-design-interview/)
[^igotanoffer]: [IGotAnOffer: GenAI System Design Interview](https://igotanoffer.com/en/advice/generative-ai-system-design-interview)
[^sdh-genai]: [System Design Handbook: GenAI Interview](https://www.systemdesignhandbook.com/guides/generative-ai-system-design-interview/)
[^hellointerview-openai]: [HelloInterview: OpenAI L5 Guide](https://www.hellointerview.com/guides/openai/l5)
[^eightfold-internship]: [Inside Eightfold AI's Internship Process](https://medium.com/@bhardwajtushar2004/inside-eightfold-ais-agentic-ai-internship-hiring-process-2026-f86dcb625aa8)
[^fonzi-ai-failed-hires]: [Fonzi AI: 50 Failed AI Hires from 2025](https://medium.com/fonzi-ai/i-reviewed-50-failed-ai-hires-from-2025-00770218130d)
[^amplework]: [Amplework: Why Hiring ML Engineers Is Hard](https://www.amplework.com/blog/why-hiring-a-machine-learning-engineer-is-so-hard/)
[^aidi-rivera]: [Aidi Rivera: My First Take-Home Code Challenge](https://dev.to/aidiri/learn-from-my-mistakes-my-first-take-home-code-challenge-778)
[^teamrora]: [TeamRora: AI/ML Salary Negotiation Guide](https://www.teamrora.com/post/aiml-salary-negotiation)
[^interviewquery-salary]: [InterviewQuery: AI Engineer Salary Guide](https://www.interviewquery.com/p/ai-engineer-salary-2025-guide)
[^ziprecruiter]: [ZipRecruiter: AI/ML Engineer Salary](https://www.ziprecruiter.com/Salaries/Ai-Ml-Engineer-Salary)
[^juicebox-ai]: [Juicebox AI: Recruitment Mistakes](https://juicebox.ai/blog/ai-recruitment-mistakes)
[^hn-referrals]: [Hacker News: AI-Generated Applications](https://news.ycombinator.com/item?id=45932838)
[^fahd-mirza]: [Fahd Mirza: How to Become an AI Engineer](https://www.youtube.com/watch?v=Zt-h5BiBWH0)
[^zero-to-mastery]: [Zero to Mastery: How to Become an AI Engineer](https://zerotomastery.io/blog/how-to-become-an-ai-engineer-from-scratch/)
