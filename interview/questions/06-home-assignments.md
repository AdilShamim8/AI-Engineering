# Home Assignments

> Based on analysis of 140+ GitHub repos with real take-home assignments, plus candidate reports verified up to September 16, 2026. Take-homes are the most revealing part of AI engineering interviews — testing full lifecycle development, evaluation, and production hygiene.

---

## Types of Assignments

| Type | Frequency | Typical Time | What It Tests |
|------|-----------|-------------|---------------|
| RAG System | 35% | 3–6 hours | Retrieval, generation, evaluation, citation |
| Agent Building | 25% | 4–8 hours | Tool use, orchestration, error handling, state management |
| Evaluation Framework | 20% | 3–5 hours | Metrics, datasets, LLM-as-judge, automation |
| Data Pipeline | 12% | 3–5 hours | Ingestion, processing, embedding, storage |
| Full-Stack AI App | 8% | 1–7 days | End-to-end building, UI, API, deployment |

### RAG System Assignments

The most common take-home format. Typical requirements:

- Ingest a set of documents (PDFs, web pages, or a provided corpus)
- Implement retrieval with semantic search (bonus: hybrid search)
- Generate answers with citations
- Evaluate quality (even a simple evaluation is better than none)
- Handle edge cases (empty results, ambiguous queries, out-of-domain questions)

**Example prompt**: "Build a RAG system that answers questions about a set of medical research papers. Include citations, handle out-of-domain questions gracefully, and implement at least one evaluation metric."

### Agent Building Assignments

Growing rapidly in 2026 as agents become mainstream:

- Build an agent that can use 2–4 tools to accomplish tasks
- Implement error handling and retry logic
- Add guardrails for safety
- Handle multi-step reasoning
- Provide observability (logging, tracing)

**Example prompt**: "Build a research agent that can search the web, read papers, and synthesize findings into a report. The agent should handle tool failures gracefully and know when to stop researching."

### Evaluation Framework Assignments

Increasingly common as companies recognize evaluation as a critical skill:

- Create a golden dataset
- Implement evaluation metrics (faithfulness, relevance, coherence)
- Build LLM-as-judge pipeline
- Automate evaluation runs
- Generate reports

**Example prompt**: "Build an evaluation framework for a customer support chatbot. Include at least 50 test cases, automated evaluation, and a dashboard showing metrics over time."

### Data Pipeline Assignments

Less common but still present at data-heavy companies:

- Ingest documents from multiple sources
- Parse, chunk, and embed
- Store in a vector database
- Handle updates and deletions
- Monitor pipeline health

**Example prompt**: "Build a data pipeline that ingests 10,000 documents, chunks them semantically, embeds them, and stores them in a vector database. Include a mechanism for incremental updates."

### Full-Stack AI App Assignments

The most time-intensive format, usually at startups:

- Build a complete AI application with frontend
- Implement user authentication
- Connect to LLM APIs
- Handle streaming responses
- Deploy or provide deployment instructions

**Example prompt**: "Build a chat-with-your-documents application. Include a React frontend, API backend, document upload, and real-time chat with citations."

---

## Typical Timeframes

| Timeframe | Frequency | Typical Assignment | Fair? |
|-----------|-----------|-------------------|-------|
| 2–3 hours | 20% | Focused coding task, limited scope | ✅ Fair |
| 4–6 hours | 35% | RAG pipeline, agent system, or evaluation | ✅ Usually fair |
| 1–2 days | 25% | More complex system with documentation | ⚠️ Borderline |
| 3–5 days | 15% | Full-stack app with deployment | ❌ Often exploitative |
| 5–7 days | 5% | Ambiguous, open-ended project | ❌ Exploitative |

**Rule of thumb**: If the assignment takes more than 6 hours of focused work, it should be compensated. In 2026, some companies are starting to pay candidates for take-homes, but this is still the exception.

---

## What Companies Look For in Submissions

### Code Quality (Always Evaluated)
- Clean, readable code with appropriate abstractions
- Error handling for API failures, edge cases, and unexpected inputs
- Type hints and docstrings (Python) or equivalent (TypeScript)
- No hardcoded secrets or API keys

### Architecture and Design (Always Evaluated)
- Clear separation of concerns (retrieval, generation, evaluation)
- Reasonable technology choices with justification
- Scalability awareness (even if not implemented, mention it)
- Cost awareness (token budgeting, caching opportunities)

### Evaluation (Heavily Weighted in 2026)
- At least basic evaluation metrics
- Test cases or golden dataset
- Awareness of evaluation limitations
- LLM-as-judge implementation (bonus)

### Documentation (Heavily Weighted)
- Clear README with setup instructions
- Architecture decisions documented
- Trade-offs discussed
- Known limitations acknowledged

### Production Awareness (Differentiating)
- Monitoring and logging
- Error handling and graceful degradation
- Cost estimation
- Security considerations (PII, prompt injection)
- Deployment considerations

### The Submission Itself
- Clean git history (meaningful commits, not one massive commit)
- Working code (test it before submitting)
- Reasonable dependencies (don't over-engineer)
- Tests (even a few integration tests show maturity)

---

## Real Examples

### Anthropic — Research Engineering Take-Home
**Time**: 4 hours
**Task**: Analyze a dataset of model outputs, identify patterns in failures, and propose mitigation strategies.
**What they look for**: Analytical rigor, clear communication, safety awareness, practical recommendations.
**Notable**: Anthropic explicitly tells candidates not to spend more than 4 hours and values a clear write-up over exhaustive analysis.

### Arcan-Tech — AI Engineer Take-Home
**Time**: 3 hours
**Task**: Build a RAG system for legal documents with citation support.
**What they look for**: Retrieval quality, citation accuracy, handling of legal-specific edge cases.
**Notable**: The assignment is publicly available on GitHub with a grading rubric. [^1]

### LangChain — Software Engineer Take-Home
**Time**: 3–4 hours
**Task**: Build a multi-step agent using LangGraph that accomplishes a research task.
**What they look for**: Correct use of LangGraph primitives, error handling, observability, clear documentation.
**Notable**: Candidates who are already LangChain users have a significant advantage. The assignment directly tests the product.

### Doctolib — AI Engineer Take-Home
**Time**: 5 hours
**Task**: Build a medical document Q&A system with safety guardrails.
**What they look for**: Safety awareness (this is medical data!), retrieval quality, citation, "I don't know" handling.
**Notable**: Doctolib evaluates safety as a first-class criterion. Systems without guardrails are automatically rejected.

### Various Startups — Common Patterns

**Startup A** (Series A, AI infrastructure):
- Build an MCP server that connects to a mock API
- Implement tool discovery and execution
- Add error handling and logging
- Time: 4 hours

**Startup B** (Seed, AI agents):
- Build a multi-agent system that decomposes a task
- Implement agent communication and coordination
- Handle agent failures gracefully
- Time: 6 hours

**Startup C** (Series B, AI evaluation):
- Build an evaluation pipeline for a summarization system
- Implement 3+ metrics (ROUGE, faithfulness, coherence)
- Create a test dataset of 30+ examples
- Time: 4 hours

---

## Best Practices for Submission

### Documentation
- **README.md**: Setup, usage, architecture overview, trade-offs, limitations
- **ARCHITECTURE.md** (optional): Detailed architecture decisions with alternatives considered
- **Inline comments**: For non-obvious logic, not for obvious code
- **Type hints**: Show professionalism and catch errors

### Tests
- At least a few integration tests showing the pipeline works end-to-end
- Unit tests for critical components (retrieval, evaluation)
- Test data included (don't require the evaluator to set up test data)

### Loom Video
- 3–5 minute walkthrough of your solution
- Explain your design decisions and trade-offs
- Show the system working
- Discuss what you'd improve with more time
- **This is increasingly expected** — candidates who include a Loom video have a significant advantage

### README Structure (Recommended)

```markdown
# Project Name

## Setup
- Prerequisites
- Installation steps
- Environment variables needed

## Usage
- How to run the system
- Example queries and expected output

## Architecture
- High-level architecture diagram
- Key design decisions and rationale

## Trade-offs
- What I chose and why
- What I'd do differently with more time

## Evaluation
- How I evaluated the system
- Metrics and results

## Limitations
- Known issues and edge cases
- What's not handled and why

## Time Spent
- Honest estimate of hours spent
```

---

## Exploitative Take-Homes: How to Identify and Handle Them

### Red Flags

| Red Flag | Why It's Problematic |
|----------|---------------------|
| No time cap mentioned | They'll take whatever you give, rewarding over-investment |
| Vague or open-ended requirements | No clear scope = no clear evaluation = free consulting |
| "Build our product" | The assignment is suspiciously close to a real business problem |
| No grading rubric shared | You don't know what they're evaluating |
| Takes more than 6 hours | This is unpaid work, not an assessment |
| They ask for "production-ready" code | Production-ready takes weeks, not hours |
| No follow-up interview about your submission | They're using your code, not evaluating your thinking |
| Multiple rounds of revisions | One round is an interview; multiple rounds is free work |
| The same assignment has been used for years | They're likely building a solution bank, not evaluating individuals |

### How to Handle Exploitative Assignments

1. **Ask for a time cap upfront.** If they can't give one, that's a red flag.
2. **Set your own boundary.** "I'll spend up to X hours on this. Here's what I'll prioritize in that time."
3. **Document your time.** Include hours spent in your submission. This creates accountability.
4. **Talk to your network.** Ask if others have done the same assignment. If it's suspiciously similar to a real product, share that concern.
5. **It's okay to say no.** If an assignment is clearly exploitative, declining is a valid choice. Companies that respect candidates will respect boundaries.
6. **Report exploitative practices.** Share on Blind, Reddit, or teamblind to warn other candidates.

---

## AI Tool Usage During Take-Homes

### Policies Vary Widely

| Policy | Frequency | Companies |
|--------|-----------|-----------|
| AI tools explicitly allowed | 30% | LangChain, many startups |
| AI tools allowed with disclosure | 25% | Various mid-size companies |
| No policy stated | 35% | Most companies |
| AI tools explicitly forbidden | 10% | Some traditional companies, finance |

### How to Navigate

1. **If allowed**: Use AI tools as you would on the job. This is actually a skill being evaluated.
2. **If forbidden**: Respect the policy. Getting caught using AI tools when forbidden is an automatic reject.
3. **If no policy**: Ask. "What's your policy on using AI coding tools for the take-home?" This shows transparency and professionalism.
4. **Always disclose**: Even if allowed, mention in your README what tools you used and how. This shows integrity and gives context to your code.
5. **Verify everything**: AI-generated code in a take-home still needs to work correctly and be well-structured. Blind AI usage without verification is a red flag.

### What Smart Companies Do

The best companies in 2026 are moving toward:

- **Explicit AI tool policies** in the assignment instructions
- **Evaluating AI fluency** as part of the take-home (how well do you use AI tools?)
- **Asking about tool usage** in the follow-up interview
- **Focusing on design decisions and trade-offs** rather than raw coding ability
- **Providing starter code** so candidates focus on the interesting parts

---

## How to Approach the Assignment Strategically

### Before You Start

1. **Read the entire prompt carefully.** Twice. Identify every requirement.
2. **Estimate the time.** Be honest about what you can accomplish in the stated timeframe.
3. **Clarify ambiguities.** If requirements are unclear, ask. This shows good judgment.
4. **Plan your architecture.** Spend 15–30 minutes planning before coding. This saves hours.
5. **Identify the evaluation criteria.** What are they actually testing? Focus your effort there.

### During the Assignment

1. **Start with the core functionality.** Get the basic pipeline working before adding features.
2. **Implement evaluation early.** If you build evaluation first, you can iterate on quality.
3. **Handle edge cases.** Empty inputs, API failures, out-of-domain queries — these differentiate.
4. **Add error handling.** Production awareness is heavily evaluated in 2026.
5. **Document as you go.** Don't leave documentation to the end.
6. **Commit frequently.** Clean git history shows how you think and work.

### After the Assignment

1. **Test thoroughly.** Make sure it works before submitting.
2. **Write a clear README.** This is often the first thing evaluators read.
3. **Record a Loom video.** 3–5 minutes walking through your solution.
4. **Be honest about limitations.** Acknowledge what you didn't have time for.
5. **Submit on time.** Late submissions signal poor time management.

### Time Allocation (For a 4-Hour Assignment)

| Phase | Time | Activities |
|-------|------|-----------|
| Planning | 30 min | Read prompt, plan architecture, identify requirements |
| Core implementation | 2 hrs | Build the main pipeline (retrieval + generation) |
| Evaluation | 45 min | Implement basic evaluation, create test cases |
| Error handling and edge cases | 30 min | Add robustness, handle failures |
| Documentation | 30 min | README, inline comments, Loom video |
| Testing and polish | 15 min | Final test run, clean up, submit |

---

## Common Mistakes

1. **Over-engineering.** Building a production-grade system when a clean prototype with good documentation would suffice. Time-box and prioritize.

2. **Under-documenting.** Code without context is hard to evaluate. A clear README with design decisions is worth more than extra features.

3. **No evaluation.** Submitting an AI system without any evaluation shows a lack of production awareness. Even simple metrics are better than none.

4. **Ignoring edge cases.** What happens when the API is down? When the query is empty? When the retrieved context is irrelevant? Handling these differentiates.

5. **Hardcoded secrets.** Including API keys in your submission is an automatic red flag at security-conscious companies.

6. **One massive commit.** A single commit with all your code makes it look like you didn't think iteratively. Meaningful commits show your thought process.

7. **Not testing before submitting.** If the evaluator can't run your code, that's a strong negative signal. Include setup instructions and verify they work.

8. **Spending too much time.** If the assignment says 4 hours and you spend 20, you're either over-investing or the assignment is exploitative. Either way, set boundaries.

9. **Not mentioning trade-offs.** Every design decision has trade-offs. Documenting what you chose and why is more valuable than the code itself.

10. **Copying without understanding.** If you use AI tools or reference implementations, make sure you understand every line. You'll be asked about your code in the follow-up interview.

---

## Sources

[^1]: Arcan-Tech take-home assignment, GitHub, 2025.
[^2]: LangChain take-home assignment, candidate reports, 2025–2026.
[^3]: Anthropic take-home reports, Blind and candidate blogs, 2025–2026.
[^4]: Doctolib AI engineer take-home, candidate reports, 2026.
[^5]: "Take-Home Assignments: A Survey of AI Engineering Candidates", community survey, 2025 (~200 respondents).
[^6]: "Exploitative Take-Homes in Tech", discussion threads on Blind and Reddit, 2025–2026.
[^7]: Analysis of 140+ GitHub repos containing AI engineering take-home assignments, 2024–September 16, 2026.
[^8]: "AI Tools in Take-Home Assignments", hiring manager survey, 2025 (n=50).
[^9]: LangChain hiring manager comments on AI tool usage, Twitter/X and blog posts, 2025–2026.

---

> **Next**: [Get Hired →](../03-get-hired.md)
