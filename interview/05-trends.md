# Interview Trends

> The AI engineering interview landscape is changing fast. This document tracks the major trends, controversies, and shifts observed in 2025–2026, based on 130+ interview rounds, hiring manager reports, and industry analysis.

---

## Market Data (2025–2026)

### Layoffs and Contractions

The AI hiring market in 2025–2026 is paradoxical: **demand for AI engineers is at an all-time high, even as tech layoffs continue.**

| Event | Impact |
|-------|--------|
| Big tech layoffs (2024–2025) | ~60,000+ tech workers laid off; many pivoted to AI roles |
| AI startup funding surge (2025) | $45B+ in AI startup funding; created thousands of new AI engineering positions |
| Traditional SWE demand softening | Companies shifting headcount from general SWE to AI-specialized roles |
| AI-native company growth | OpenAI, Anthropic, Databricks, and others doubled engineering headcount in 2025 |
| Government AI mandates | EU AI Act and US executive orders created compliance-focused AI roles |

**Net effect**: The market for AI engineers is strong, but competition for top positions is fierce. Average candidates face a tough market; strong candidates with AI-specific experience are in high demand.

### AI-Native Role Surge

| Metric | 2024 | 2025 | 2026 (proj.) |
|--------|------|------|-------------|
| "AI Engineer" job postings | ~8,000 | ~18,000 | ~32,000 |
| "ML Engineer" job postings | ~25,000 | ~28,000 | ~30,000 |
| "Prompt Engineer" job postings | ~3,000 | ~1,500 | ~800 |
| AI-specific interview guides | 5 | 15 | 30+ |
| Companies with AI engineering teams | 500+ | 1,200+ | 2,000+ |

**Key observation**: The "Prompt Engineer" role is dying — subsumed into broader AI engineering. Companies want engineers who can build systems, not just write prompts.

---

## Patterns from Practitioners

> Based on 130+ interview rounds reported by AI engineering candidates in 2025–2026.

### Most Common Interview Flow (2026)

1. Recruiter screen (15–30 min)
2. Technical: AI system design or coding (45–60 min)
3. Technical: Project deep-dive or ML implementation (45–60 min)
4. Take-home or live AI coding (variable)
5. Behavioral + culture (30–45 min)
6. Hiring manager / founder (15–30 min)

### Biggest Surprises Reported by Candidates

| Surprise | Frequency | Details |
|----------|-----------|---------|
| No LeetCode at all | 45% | Many AI-native companies skip DSA entirely |
| Deep evaluation questions | 60% | Candidates didn't expect evaluation to be so central |
| Safety questions everywhere | 40% | Even at companies not known for safety focus |
| Context engineering questions | 25% | New topic that caught many off guard |
| AI-assisted coding round | 20% | Didn't know they could (or should) use AI tools |
| Length of process | 35% | AI-native companies have longer processes (4–7 rounds) |
| Take-home with no time cap | 30% | Ambiguous scope led to over-investment |

---

## "No Whiteboard" — Realistic Assessments

The trend toward practical, realistic assessments continues to accelerate:

### Companies Moving Away from Whiteboard Interviews

| Company | Alternative | Rationale |
|---------|------------|-----------|
| LangChain | Take-home + code review session | Tests real skills, not performance anxiety |
| PostHog | Take-home + discussion | Better signal for AI engineering specifically |
| Anthropic | System design with safety constraints | More relevant than algorithmic puzzles |
| Stripe | Pair programming on real problems | Tests collaboration and practical coding |
| Various startups | "Day in the life" simulations | Most realistic assessment possible |

### Why This Is Happening

1. **Whiteboard coding tests the wrong skills for AI engineering.** Writing a linked list from memory doesn't predict your ability to design a RAG pipeline.
2. **AI tools exist.** On the job, you'd use Copilot, Cursor, or ChatGPT. Testing without them tests memorization, not productivity.
3. **Performance anxiety is a poor signal.** Whiteboard interviews systematically disadvantage candidates who are strong engineers but struggle with public coding.
4. **The field moves too fast.** Testing specific API knowledge is futile when the APIs change monthly. Testing understanding and judgment is more durable.

---

## Framework Bias in Hiring

### The Problem

Some interviewers at AI companies have strong biases toward specific frameworks:

- **LangChain enthusiasts** who expect candidates to know LangChain idioms
- **"Build it from scratch" advocates** who penalize anyone using a framework
- **Cloud provider loyalists** who favor AWS/GCP/Azure-native solutions

### How to Navigate

1. **Ask about tech stack early.** "What does your AI stack look like?" — this tells you what the interviewer values.
2. **Present alternatives.** "I'd use LangChain here for [reasons], but an alternative would be [custom implementation] because [trade-offs]."
3. **Don't be religious about frameworks.** Show you understand both the value and the limitations of any tool.
4. **Focus on concepts, not tools.** "I'd build a retrieval and generation pipeline" is better than "I'd use LangChain" because it shows understanding over memorization.

---

## Real-Time AI Cheating During Interviews

### The Emerging Problem

Candidates are increasingly using AI tools during interviews without disclosure:

- **Screen-sharing interviews**: AI tools running on a second monitor
- **Phone interviews**: ChatGPT running on a separate device
- **Take-homes**: Extensive AI-generated code without disclosure
- **Live coding**: AI assistance via earpiece or second screen

### How Companies Are Responding

| Detection Method | Companies Using | Effectiveness |
|------------------|----------------|---------------|
| AI-generated code detection | 30% | Low — detectors have high false positive rates |
| Proctored assessments | 20% | Medium — but invasive and poor candidate experience |
| Follow-up questioning | 70% | High — candidates who didn't write the code can't explain it |
| In-person interviews | 15% (growing) | High — eliminates remote cheating entirely |
| "Explain your code" requirement | 60% | High — the most effective countermeasure |

### The Reality

The cat-and-mouse game between candidates and companies is escalating. But the most effective countermeasure is also the simplest: **if you can explain your code and reasoning in depth, it doesn't matter how you wrote it.** Companies that focus on understanding over execution are less vulnerable to cheating.

---

## AI Surveillance During Remote Interviews

### Growing Concerns

Some companies are using AI-powered surveillance during remote interviews:

- **Eye tracking** to detect looking at other screens
- **Keystroke analysis** to detect AI-pasted code
- **Screen recording** with AI analysis of browsing behavior
- **Background audio analysis** to detect whispered prompts or earpieces

### Candidate Sentiment

A 2025 survey of 500+ AI engineering candidates found:

| Sentiment | Percentage |
|-----------|-----------|
| Comfortable with basic recording | 65% |
| Uncomfortable with AI surveillance | 78% |
| Would withdraw from process if surveillance disclosed | 34% |
| Believe surveillance signals toxic culture | 62% |

**Key insight**: AI surveillance in interviews creates a perverse dynamic — companies that build AI are using AI to surveil candidates who build AI. Many candidates see this as hypocritical and a cultural red flag.

---

## AI-Proctored Early Rounds

### The Trend

Companies are using AI to screen candidates in early rounds:

- **Eightfold.ai**: Uses its own AI hiring platform to evaluate candidates
- **Coinbase**: AI-assisted initial assessments
- **Deepthi Sudharsan**: AI-proctored coding assessments for early screening
- **Various enterprise companies**: Automated ML/LLM knowledge quizzes with AI grading

### How It Works

1. Candidate completes an online assessment (coding + ML knowledge)
2. AI grades the assessment and ranks candidates
3. Top-ranked candidates advance to human interviews
4. AI provides initial screening data to human interviewers

### Concerns

- **Bias in AI grading**: AI systems may have biases that affect evaluation
- **False negatives**: Strong candidates who don't perform well in AI-graded assessments may be filtered out
- **Gaming the AI**: Candidates who understand the AI's evaluation criteria may optimize for the AI, not for actual skill
- **Lack of feedback**: AI-graded assessments rarely provide meaningful feedback to rejected candidates

---

## The "No AI Tools" Irony

### The Situation

Some companies explicitly forbid AI tool usage during interviews, creating a bizarre contradiction:

- **The company's product** is an AI tool that helps people work more efficiently
- **The interview** forbids candidates from using AI tools to work more efficiently
- **The result**: Candidates are tested on skills they'll never use on the job (manual coding without AI assistance)

### Why This Happens

1. **Interview inertia.** Companies haven't updated their interview processes for the AI era.
2. **Cheating concerns.** Companies can't distinguish between AI-assisted work and AI-cheating.
3. **Evaluation difficulty.** It's harder to evaluate AI-assisted work than manual work.
4. **Fairness arguments.** Companies want all candidates on a level playing field.

### The Shift

In 2026, more companies are moving to **"AI tools allowed"** policies because:

- It better reflects how engineers actually work
- It tests a more relevant skill (AI-assisted problem-solving)
- It's nearly impossible to enforce "no AI tools" anyway
- It differentiates candidates who can use AI effectively from those who can't

---

## Employers Using AI in Hiring

### How Companies Use AI to Evaluate Candidates

| Use Case | Companies | Controversy Level |
|----------|-----------|------------------|
| Resume screening | Most large companies | Medium |
| AI-graded coding assessments | Eightfold, HackerRank | Medium |
| AI-analyzed video interviews | HireVue, some enterprise | High |
| AI-generated interview questions | Growing trend | Low |
| AI scoring of behavioral responses | Emerging | High |
| AI-matched candidates to roles | Eightfold, LinkedIn | Medium |

### The Meta-Problem

When AI engineers are evaluated by AI systems, we've created a recursive loop. The quality of the hiring AI becomes as important as the quality of the candidate — but the hiring AI is rarely evaluated with the rigor that the candidate is.

---

## Encouraging or Evaluating AI Fluency

### The Positive Trend

Some companies are actively testing AI fluency as a competency:

- **Microsoft**: "Show us how you'd use Copilot to solve this problem"
- **OpenAI**: "Use ChatGPT to help you implement this feature"
- **Exponent**: AI-assisted coding as part of their interview
- **Various startups**: "Use whatever tools you'd use on the job"

### What This Tests

| Skill | How It's Evaluated |
|-------|-------------------|
| Prompt engineering | Can you write effective prompts for coding tasks? |
| Verification | Do you check AI-generated code for correctness and security? |
| Iteration | Can you refine prompts when the first output isn't right? |
| Integration | Can you incorporate AI suggestions into a larger codebase? |
| Judgment | Do you know when AI output is wrong or suboptimal? |
| Speed | Can you accomplish more with AI assistance than without? |

---

## Published AI Guidelines for Candidates

### Companies with Public AI Tool Policies

| Company | Policy | Source |
|---------|--------|--------|
| OpenAI | AI tools allowed during coding rounds | Interview instructions, 2026 |
| Microsoft | Copilot encouraged during coding rounds | Interview instructions, 2026 |
| Anthropic | No AI tools during live interviews; allowed for take-homes with disclosure | Candidate reports, 2026 |
| LangChain | AI tools allowed and encouraged for take-homes | Job posting, 2026 |
| Google | No AI tools during on-site; take-home policy varies | Candidate reports, 2026 |
| Various startups | "Use whatever tools you'd use on the job" | Growing trend, 2026 |

### What This Means for Candidates

1. **Always ask about the AI tool policy** before the interview.
2. **If AI tools are allowed**, use them as you would on the job — but verify everything.
3. **If AI tools are forbidden**, respect the policy. Getting caught is worse than the skill gap.
4. **If no policy is stated**, ask. This shows professionalism and awareness.
5. **Document your AI usage** in take-homes. Transparency builds trust.

---

## In-Person Interviews Are Coming Back

### The Trend

After years of fully remote interviews, some companies are bringing back in-person rounds:

- **Google**: On-site loops for final rounds
- **Meta**: In-person for senior roles
- **Amazon**: On-site for L6+ roles
- **Anthropic**: In-person final rounds at SF office
- **Various startups**: "Team day" in-person interviews

### Why

1. **Anti-cheating**: In-person interviews eliminate remote AI cheating
2. **Culture assessment**: Harder to evaluate culture fit over video
3. **Collaboration testing**: Whiteboard design and pair programming work better in person
4. **Commitment signal**: Candidates who show up in person demonstrate interest
5. **Serendipity**: In-person interactions reveal things video doesn't

### Impact on Candidates

- Budget for travel if interviewing at companies with on-site requirements
- Practice whiteboard system design (draw architecture diagrams by hand)
- Prepare for more social, conversational interviews (lunch interviews, team interactions)
- Dress codes are returning — but the standard is still "smart casual" at most AI companies

---

## AI Tools Allowed During Live Coding

### The Growing List

| Company | Tools Allowed | How It's Evaluated |
|---------|--------------|-------------------|
| OpenAI | ChatGPT | How effectively you use it; do you verify output? |
| Microsoft | Copilot | Speed and accuracy of AI-assisted coding |
| Exponent | Any AI tool | AI fluency as a core competency |
| Various startups | Cursor, Copilot, ChatGPT | Realistic assessment of day-to-day work |

### How to Prepare

1. **Practice with AI tools under time pressure.** Set a 45-minute timer and solve problems with Cursor/Copilot.
2. **Develop a verification habit.** Always read and test AI-generated code before accepting it.
3. **Learn to prompt for code.** "Write a function that [specific requirement] with [error handling] and [type hints]" produces better output than "help me code."
4. **Practice debugging AI output.** Intentionally generate buggy code with AI and practice fixing it.
5. **Show your work.** Narrate your AI interactions: "I'm going to use Copilot for the boilerplate, then I'll verify and modify for our specific requirements."

---

## Context Engineering as Interview Topic

> **NEW for 2026**

### What's Happening

Context engineering — the discipline of assembling the right information into an LLM's context window — is emerging as a distinct interview topic. Companies building production AI systems have realized that context management is often the difference between a working system and a broken one.

### Companies Testing Context Engineering

| Company | How They Test | Seniority |
|---------|--------------|-----------|
| Anthropic | "How would you manage context for a multi-turn medical conversation?" | Mid–Senior |
| OpenAI | "Design a context assembly pipeline that adapts to user queries" | Senior+ |
| Google DeepMind | "How do you handle context window constraints at scale?" | Mid–Senior |
| Databricks | "Design a context caching strategy for a high-volume API" | Senior+ |
| Various startups | "How do you decide what goes into the context window?" | All levels |

### What to Know

- Context window budgeting (how to allocate tokens across system prompt, context, history, output)
- Dynamic context assembly (adapting context based on the query)
- Context pruning (removing low-value context without losing critical information)
- Multi-source context fusion (combining RAG, tools, conversation, knowledge graph)
- Context caching strategies (prefix caching, semantic caching, prompt caching)
- The "attention dilution" problem (more context ≠ better output)

---

## MCP/A2A Knowledge Testing

> **NEW for 2026**

### What's Happening

The Model Context Protocol (MCP) and Agent-to-Agent (A2A) protocol have become important infrastructure for AI systems. Companies building agent platforms are beginning to test knowledge of these protocols.

### What Interviewers Ask

- "What is MCP and what problem does it solve?"
- "How would you build an MCP server for [specific use case]?"
- "How does tool discovery work in MCP?"
- "What is the A2A protocol and how does it differ from MCP?"
- "Design a multi-agent system using MCP and A2A."

### Companies Testing This

- **LangChain**: MCP and LangGraph knowledge expected
- **Anthropic**: MCP is their protocol — deep knowledge expected
- **Various agent infrastructure startups**: Protocol knowledge is core to the role

### How to Prepare

- Read the MCP specification (it's relatively short)
- Build a simple MCP server
- Understand the difference between MCP (tool/context connection) and A2A (agent communication)
- Know the security considerations (authentication, authorization, data exposure)

---

## AI Engineering Interviews Lack Standardization

### The Problem

Unlike software engineering (where the "LeetCode + system design" format is well-established) or data science (where the "SQL + statistics + case study" format is common), AI engineering interviews have **no standard format**.

### What This Means

| Company Type | Typical Format | Variance |
|-------------|---------------|----------|
| Big tech (FAANG) | DSA + ML theory + system design | Low |
| AI-native companies | System design + AI coding + safety | Medium |
| Traditional tech adding AI | Mix of SWE + ML interviews | High |
| Startups | Take-home + discussion | Very high |
| Quant/finance | DSA + probability + ML implementation | Low |

### Impact on Candidates

1. **You must research each company's format.** A "one-size-fits-all" preparation strategy will fail.
2. **Ask the recruiter about the format.** "What does the interview process look like? What rounds should I prepare for?"
3. **Prepare for multiple formats.** DSA, system design, AI coding, take-homes, behavioral — you need all of them.
4. **The bar is inconsistent.** Some companies have rigorous, well-calibrated processes. Others are making it up as they go.

---

## Junior vs. Senior Expectations Are Diverging

### The Gap

| Dimension | Junior Expectations | Senior Expectations |
|-----------|-------------------|-------------------|
| ML theory | Basic understanding of LLMs, RAG, agents | Deep understanding of architecture, training, optimization |
| Coding | Working prototypes | Production-grade with error handling, monitoring, testing |
| System design | Can identify components | Can design end-to-end systems with trade-offs |
| Evaluation | Knows basic metrics | Can build evaluation frameworks from scratch |
| Safety | Awareness of issues | Can design guardrails and safety systems |
| Cost | Awareness that cost matters | Can optimize and predict costs |
| Communication | Can explain to teammates | Can explain to executives and non-technical stakeholders |
| Ownership | Can execute on defined tasks | Can define what needs to be built |

### Why This Matters

The junior AI engineering market is **oversaturated** with bootcamp graduates and career transitioners. The senior AI engineering market has **severe talent shortages**. This divergence means:

- Juniors face intense competition and need to differentiate through projects and depth
- Seniors can be more selective but need to demonstrate genuine production experience
- Companies are increasingly using seniority-specific interview tracks

---

## Read the Room: LLM Hype Can Backfire

### The Problem

Some candidates over-index on LLM knowledge at the expense of engineering fundamentals. Every problem becomes "let's use an LLM" — even when a simpler solution exists.

### What Interviewers See

- **Red flag**: "I'd use an LLM to solve this" when a rule-based system would be simpler, cheaper, and more reliable
- **Green flag**: "I'd start with a simple heuristic and only add LLM-based reasoning where the heuristic fails"

### The Right Approach

1. **Consider non-LLM solutions first.** Not every problem needs an LLM.
2. **Quantify the LLM advantage.** "An LLM-based approach would improve accuracy by X% at a cost of $Y/query."
3. **Know when to use simple models.** Classification, extraction, and ranking tasks often work better with fine-tuned smaller models.
4. **Show restraint.** The best AI engineers know when NOT to use AI.

---

## The Bar Feels Higher

### Candidate Reports

A consistent theme in 2025–2026 interview reports: **the bar feels higher than a year ago.**

| Factor | Why the Bar Is Higher |
|--------|----------------------|
| More candidates | Layoffs + career transitions increased the applicant pool |
| More AI-savvy interviewers | Interviewers themselves are more knowledgeable about AI |
| Production expectations | Companies want production-ready AI engineers, not learners |
| Broader scope | AI engineering now includes evaluation, safety, cost — not just building |
| Competitive market | Companies can afford to be more selective |

### What This Means for Preparation

- **Surface-level knowledge is no longer sufficient.** "I know what RAG is" won't cut it when the next candidate can design and evaluate a RAG pipeline end-to-end.
- **Production experience is the differentiator.** If you don't have it, build it through portfolio projects.
- **Breadth + depth is required.** You need breadth across AI engineering topics AND depth in at least 2–3 areas.

---

## Exploitative Take-Homes at AI Startups

### The Problem

AI startups are increasingly using take-home assignments that are effectively unpaid consulting:

- **Vague requirements** that require 20+ hours of work
- **"Production-ready" expectations** for a take-home
- **Assignments suspiciously similar to real business problems**
- **No compensation for time invested**
- **No feedback provided** after submission

### Data from 2025–2026

| Metric | Value |
|--------|-------|
| Candidates who feel take-homes were exploitative | 38% |
| Average time spent on "4-hour" take-homes | 8.2 hours |
| Candidates who declined to complete take-homes due to scope | 22% |
| Companies that provide grading rubrics | 15% |
| Companies that compensate for take-home time | 5% |

### What Candidates Are Doing

- **Setting boundaries**: "I'll spend up to X hours on this"
- **Asking for rubrics**: "What specifically are you evaluating?"
- **Sharing experiences**: Posting on Blind and Reddit to warn other candidates
- **Declining exploitative assignments**: Walking away from processes that feel like free consulting

---

## Emerging Interview Formats

### Code Review of AI-Generated Code

You're given AI-generated code and asked to review it for correctness, security, and quality. This tests:

- Can you identify subtle bugs in AI output?
- Do you notice security vulnerabilities?
- Can you improve the prompts that generated the code?

### AI-Generated Code Review (Reverse)

You submit code (possibly AI-assisted) and the interviewer uses AI to review it, then discusses the AI's findings with you. This tests:

- Do you agree with the AI's assessment?
- Can you identify where the AI reviewer is wrong?
- Can you defend your design decisions?

### "AI Delta" Assessment

You solve a problem twice — once without AI tools, once with. The interviewer evaluates the "AI delta": how much more you accomplish with AI assistance. This tests:

- Can you use AI tools effectively?
- Does AI assistance actually improve your output quality?
- Can you verify and correct AI-generated code?

### Pair Programming with AI

You and the interviewer (possibly with AI assistance) build a feature together. This tests:

- Can you collaborate effectively?
- Can you integrate AI suggestions into a team workflow?
- Can you communicate about AI-generated code?

---

## New Interview Round Types

### Safety and Ethics Round

Companies like Anthropic and Google DeepMind are adding dedicated rounds that evaluate:

- How you think about AI safety in concrete scenarios
- Your approach to PII handling and data privacy
- How you'd respond to a prompt injection attack
- Your ethical reasoning about AI deployment

### Context Engineering Round

New for 2026, this round tests:

- How you manage context windows in production systems
- Your approach to dynamic context assembly
- Context pruning and prioritization strategies
- Caching and cost optimization through context management

### MCP/Agent Protocol Round

For companies building agent infrastructure, this round tests:

- Knowledge of MCP and A2A protocols
- Ability to design tool interfaces for LLMs
- Understanding of agent communication patterns
- Security considerations for agent systems

### AI Fluency Round

Testing how effectively you use AI tools:

- Can you write effective prompts for coding tasks?
- Do you verify AI-generated output?
- Can you identify when AI output is wrong?
- Do you use AI tools to accelerate without sacrificing quality?

---

## Sources

[^1]: Layoff data from Layoffs.fyi and TrueUp, 2024–2025.
[^2]: AI startup funding data from PitchBook and Crunchbase, 2025.
[^3]: Job posting analysis from LinkedIn, Wellfound, and Y Combinator, 2024–2026.
[^4]: Candidate survey on AI surveillance in interviews, n=500+, 2025.
[^5]: Take-home assignment survey, AI engineering community, n=200+, 2025.
[^6]: Interview reports from Blind, Glassdoor, and LeetCode Discuss, 2025–2026.
[^7]: Company AI tool policies from interview instructions and candidate reports, 2026.
[^8]: MCP specification, Anthropic, 2024. A2A protocol specification, Google DeepMind, 2025.
[^9]: "Context Engineering" as interview topic: emerging from practitioner reports and company interview formats, 2025–2026.
[^10]: Eightfold.ai hiring platform documentation and candidate reports, 2025–2026.
[^11]: Coinbase AI-proctored assessment reports, Blind, 2025.
[^12]: In-person interview return: company announcements and candidate reports, 2025–2026.
[^13]: "AI Fluency as a Competency", Microsoft and OpenAI hiring blog posts, 2025.
[^14]: Exploitative take-home data from community surveys and discussion threads, 2025–2026.
[^15]: Emerging interview formats from hiring manager discussions at AI Engineer Summit, 2025.
