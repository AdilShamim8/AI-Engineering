# Take-Home Assignments for AI Engineers

**Webinar Recording** | Duration: 92 min | Speakers: Emily Rodriguez (Hiring science researcher), Jamal Watkins (ex-Stripe, now advisory), Sophia Liu (open-source AI eval contributor), Carlos Mendez (AI Engineer at scale)

---

## Overview

The take-home assignment is the most polarizing part of the AI Engineer hiring process. Done well, it's the strongest signal a company can get. Done poorly, it's exploitative free labor with a 4% callback rate. This webinar analyzes 120+ real take-home assignments from public GitHub repos and company documentation, identifies what makes submissions stand out, and walks through building a production-ready solution.

---

## Common Assignment Types

### Type 1: RAG System (42% of assignments)

**The prompt:** "Build a question-answering system over [document set]. Users should be able to ask natural language questions and get accurate, sourced answers."

**Variations:**
- Over internal company docs (simulated)
- Over a specific domain (legal, medical, financial)
- Over code repositories
- Over multi-modal content (text + tables + images)

**Typical constraints:**
- Time limit: 4-8 hours
- Must use a specific model API (or choose your own)
- Must include source citations
- Must handle edge cases (out-of-domain questions, conflicting information)

**What it's actually testing:**
- Can you build a complete RAG pipeline? (Many candidates can't.)
- Do you understand chunking, embedding, and retrieval beyond the tutorial level?
- Can you evaluate retrieval quality?
- Do you handle errors and edge cases?
- Is the code production-quality or prototype-quality?

### Type 2: Agent System (28% of assignments)

**The prompt:** "Build an agent that can [task requiring multiple steps and tool use]. The agent should plan, execute, and verify its work."

**Variations:**
- Research agent (gather and synthesize information)
- Coding agent (write, test, and fix code)
- Data analysis agent (query databases, generate insights)
- Workflow automation agent (execute multi-step business processes)

**Typical constraints:**
- Time limit: 6-10 hours
- Must implement at least 3 tools
- Must handle tool failures gracefully
- Must have a planning mechanism
- Must prevent infinite loops

**What it's actually testing:**
- Can you design a coherent agent architecture?
- Do you understand the ReAct pattern or similar approaches?
- Can you handle the messy reality of LLM outputs (malformed tool calls, hallucinated tools)?
- Do you implement proper guardrails?
- Can you debug and iterate on agent behavior?

### Type 3: Evaluation Framework (18% of assignments)

**The prompt:** "Design and implement an evaluation framework for [AI system]. The framework should measure quality, detect regressions, and provide actionable insights."

**Variations:**
- Evaluate a RAG system (retrieval + generation quality)
- Evaluate a chatbot (relevance, safety, coherence)
- Evaluate a code generation system (correctness, efficiency, style)
- Evaluate an agent (task completion, efficiency, safety)

**Typical constraints:**
- Time limit: 4-6 hours
- Must include both automated and LLM-as-judge metrics
- Must define a scoring methodology
- Must handle ambiguous or subjective outputs
- Must produce interpretable results

**What it's actually testing:**
- Can you define meaningful quality metrics?
- Do you understand different evaluation approaches and their tradeoffs?
- Can you design a framework that's practical (runs in reasonable time/cost)?
- Do you think about regression detection?
- Can you communicate results clearly?

### Type 4: Prompt Engineering Challenge (8% of assignments)

**The prompt:** "Design prompts for [task]. Your solution should be robust, cost-efficient, and handle edge cases."

**Variations:**
- Structured output extraction from unstructured text
- Multi-turn conversation design
- Content moderation / safety filtering
- Domain-specific generation (medical, legal, technical)

**What it's actually testing:**
- Systematic prompt design methodology
- Understanding of prompt components (system, user, few-shot, chain-of-thought)
- Token efficiency
- Robustness testing
- Version control and iteration documentation

### Type 5: Full-Stack AI Feature (4% of assignments)

**The prompt:** "Build a complete user-facing AI feature including backend API, model integration, and simple frontend."

**What it's actually testing:**
- End-to-end delivery capability
- API design for AI features (streaming, error handling)
- Basic frontend skills
- Production considerations (caching, rate limiting, monitoring)

---

## Analysis of Real Assignments from 120+ GitHub Repos

### Methodology

We analyzed 120+ public GitHub repositories that were explicitly labeled as AI Engineer take-home submissions. Repos were identified through:
- GitHub search for "take-home," "assignment," "challenge" in AI-related repos
- Reddit and Blind posts where candidates shared their submissions
- Open-source contributions from hiring process discussions

### What the Data Shows

#### Completion Rates by Assignment Type

| Assignment Type | Average Completion Rate | Avg. Stars | Avg. Code Quality Score* |
|----------------|------------------------|------------|--------------------------|
| RAG System | 89% | 12 | 3.2/5 |
| Agent System | 71% | 18 | 2.8/5 |
| Evaluation Framework | 82% | 8 | 3.6/5 |
| Prompt Engineering | 94% | 5 | 3.0/5 |
| Full-Stack AI Feature | 63% | 22 | 2.5/5 |

*Code quality scored on: error handling, testing, documentation, modularity, configuration management

#### The Quality Distribution

The overwhelming finding: most submissions are mediocre.

- **Top 10%:** Production-quality code with thorough evaluation, clear documentation, and thoughtful design decisions
- **Middle 60%:** Working implementations with some evaluation, decent documentation, and a few rough edges
- **Bottom 30%:** Barely working prototypes, copy-pasted tutorials, no evaluation, no error handling

### Common Patterns in Submissions

#### Pattern 1: The Tutorial Clone (35% of submissions)

These submissions look like they followed a LangChain or LlamaIndex tutorial and swapped in the assignment's document set.

**Red flags:**
- Default chunking parameters with no justification
- No evaluation beyond "it looks right to me"
- Hardcoded API keys (yes, this still happens)
- No error handling for API failures
- Identical architecture to the quickstart guide

#### Pattern 2: The Over-Engineered Solution (15% of submissions)

These submissions implement custom vector databases, multi-stage retrieval pipelines, and complex agent architectures — for what should be a straightforward task.

**Red flags:**
- Complexity that doesn't serve the use case
- More time spent on architecture than on quality
- Doesn't actually work well because complexity introduced bugs
- No comparison to simpler approaches

#### Pattern 3: The Thoughtful Minimalist (12% of submissions)

These submissions implement a clean, focused solution with clear rationale for every design decision.

**Green flags:**
- Simple architecture with justified complexity additions
- Evaluation suite that measures actual quality
- Clear documentation of tradeoffs considered
- Error handling and edge case coverage
- Cost and latency awareness

**This is the pattern that gets offers.**

### The Evaluation Gap

The single most striking finding: **only 23% of submissions included any form of systematic evaluation.** This despite evaluation being the most commonly tested skill in AI Engineer interviews.

Of those that did include evaluation:
- 61% used only "vibe check" (manual inspection of a few examples)
- 24% used automated metrics (BLEU, ROUGE, semantic similarity)
- 11% used LLM-as-judge
- 4% used human evaluation or comprehensive frameworks

Emily Rodriguez's take:
> "The evaluation gap is staggering. Companies are explicitly testing for evaluation skills, and 77% of candidates submit assignments with no systematic evaluation. That's not a skills gap — that's a strategic failure. Adding a solid eval section to your submission is the easiest way to differentiate yourself."

---

## What Makes a Submission Stand Out

### The Standout Scorecard

Based on analysis of the top 10% of submissions and hiring manager feedback:

| Dimension | Weight | What Stands Out |
|-----------|--------|-----------------|
| Working Solution | 20% | It actually works, reliably, on edge cases |
| Evaluation | 25% | Systematic, with clear metrics and regression detection |
| Code Quality | 15% | Production-grade: error handling, logging, configuration |
| Design Rationale | 15% | Documented tradeoffs and justified decisions |
| Cost Awareness | 10% | Token usage analysis, optimization strategies |
| Documentation | 10% | Clear README, inline comments, architecture diagram |
| Creativity | 5% | Novel but appropriate solutions to the problem |

### The Seven Things That Make Reviewers Stop and Say "Wow"

**1. An evaluation section that goes beyond accuracy.**

Most submissions that include evaluation measure retrieval accuracy or answer correctness. Standout submissions measure:
- Robustness (performance on adversarial or out-of-distribution inputs)
- Consistency (same question asked different ways gets same answer)
- Cost efficiency (quality per dollar, not just quality)
- Latency (quality per second)
- Failure modes (when does it break and how badly?)

**2. A comparison of approaches.**

Instead of just implementing one approach, standout submissions implement 2-3 variants and compare them:

```
Approach 1: Naive chunking + GPT-4o
  - Recall@5: 0.71, Latency: 2.3s, Cost/req: $0.012

Approach 2: Semantic chunking + hybrid search + GPT-4o
  - Recall@5: 0.83, Latency: 2.8s, Cost/req: $0.014

Approach 3: Semantic chunking + hybrid search + re-rank + GPT-4o-mini
  - Recall@5: 0.81, Latency: 2.1s, Cost/req: $0.004
```

This shows decision-making ability, not just implementation ability.

**3. Production error handling.**

Most submissions assume the API always returns valid responses. Standout submissions handle:
- API rate limits and retries with exponential backoff
- Malformed model outputs (the model returned invalid JSON)
- Timeout handling for long-running requests
- Graceful degradation when the model is unavailable
- Input validation and sanitization

**4. A cost analysis section.**

Even a brief cost analysis shows practical awareness:

```
Estimated costs at scale:
- Embedding: ~$0.0001/doc × 10,000 docs = $1.00 (one-time)
- Query: ~$0.008/query × 1,000 queries/day = $8/day
- Monthly estimate: ~$250/month at 1K queries/day
- Cost per correct answer: ~$0.010 (assuming 80% accuracy)
```

**5. Configuration over hardcoding.**

Standout submissions use environment variables, configuration files, and sensible defaults:

```python
# Instead of:
MODEL = "gpt-4o"

# Use:
MODEL = os.getenv("RAG_MODEL", "gpt-4o")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "512"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "64"))
```

**6. A "What I'd Do With More Time" section.**

This demonstrates awareness of the solution's limitations and the ability to prioritize:

```markdown
## What I'd Do With More Time

1. **Implement semantic caching** — Currently, every query hits the model.
   Estimated cost reduction: 30-40% for repeated queries.

2. **Add hybrid search** — Current retrieval is purely semantic.
   BM25 + semantic would improve recall on keyword-heavy queries.

3. **Build a re-ranking step** — Current top-k is used directly.
   A cross-encoder re-ranker would improve precision by ~5-8%.

4. **Add user feedback loop** — Currently no mechanism to learn from
   user corrections. Thumbs up/down would enable continuous improvement.

5. **Implement A/B testing framework** — Currently no way to compare
   prompt or retrieval variants in production.
```

**7. Clean, communicative commit history.**

The Git history tells a story. Standout submissions have commits like:
- "Initial RAG pipeline with naive chunking"
- "Add hybrid search — recall improved from 0.71 to 0.78"
- "Add evaluation suite with 50 test cases"
- "Fix: handle malformed JSON from model API"
- "Optimize: reduce token usage by 35% with context compression"

---

## Building a Production-Ready Solution: Walkthrough

### The Scenario

You've received a take-home assignment: "Build a RAG system that answers questions about a set of 200 technical documents. Include evaluation."

### Step 1: Scope and Plan (30 min)

Before writing any code:

```
Scope:
- 200 documents, average 5 pages each
- Question types: factual, comparative, procedural
- Expected: 100-500 queries/day
- Quality bar: 85%+ correct with citations

Architecture:
- Document processing: PDF → text → chunks → embeddings
- Storage: pgvector (simple, reliable, SQL-compatible)
- Retrieval: Hybrid (semantic + BM25) with re-ranking
- Generation: GPT-4o-mini (cost-efficient, good enough)
- Evaluation: Automated + LLM-as-judge

Key decisions to document:
1. Why pgvector over Pinecone? → Simpler setup, no vendor lock-in, sufficient for 200 docs
2. Why GPT-4o-mini over GPT-4o? → 10x cheaper, sufficient quality with good retrieval
3. Why hybrid search? → Semantic alone fails on exact term matches
```

### Step 2: Core Implementation (2 hours)

Build the minimum viable pipeline:

1. **Document processing script** — PDF extraction, text cleaning, chunking
2. **Embedding and indexing** — Generate embeddings, store in pgvector
3. **Retrieval function** — Hybrid search with configurable weights
4. **Generation function** — Prompt template + context injection + response
5. **API endpoint** — Simple FastAPI server with the query endpoint

### Step 3: Evaluation Suite (1.5 hours)

This is where you differentiate:

```python
# eval_suite.py

class RAGEvaluator:
    """Evaluation suite for RAG system quality."""

    def __init__(self, test_cases: list[dict]):
        self.test_cases = test_cases  # {question, expected_answer, source_docs}

    def evaluate_retrieval(self, k: int = 5) -> dict:
        """Measure retrieval quality independently."""
        metrics = {"recall@k": [], "mrr": [], "precision@k": []}
        for case in self.test_cases:
            retrieved = self.rag.retrieve(case["question"], top_k=k)
            relevant = set(case["source_docs"])
            retrieved_ids = set(r.id for r in retrieved)
            # ... compute metrics
        return {k: np.mean(v) for k, v in metrics.items()}

    def evaluate_generation(self) -> dict:
        """Measure answer quality using LLM-as-judge."""
        metrics = {"faithfulness": [], "relevance": [], "completeness": []}
        for case in self.test_cases:
            answer = self.rag.query(case["question"])
            scores = self.llm_judge.evaluate(
                question=case["question"],
                answer=answer,
                reference=case["expected_answer"],
                context=self.rag.retrieve(case["question"])
            )
            # ... compute metrics
        return {k: np.mean(v) for k, v in metrics.items()}

    def evaluate_robustness(self) -> dict:
        """Test on adversarial and edge-case inputs."""
        # Paraphrased questions should get same answer
        # Out-of-domain questions should be handled gracefully
        # Conflicting information should be acknowledged
        ...
```

### Step 4: Error Handling and Production Concerns (1 hour)

- Add retry logic with exponential backoff for API calls
- Add input validation (query length, content filtering)
- Add structured logging with request IDs
- Add health check endpoint
- Add configuration management
- Add a Dockerfile and docker-compose.yml

### Step 5: Documentation and Polish (30 min)

- Write a clear README with setup instructions
- Document architecture decisions and tradeoffs
- Include evaluation results in the README
- Add the "What I'd Do With More Time" section
- Clean up commit history

### Total Time: ~5.5 hours

This is achievable within a typical 6-8 hour assignment window while leaving buffer time for unexpected issues.

---

## Handling Exploitative Assignments

### The Red Flags

Not all take-home assignments are created equal. Watch for these warning signs:

| Red Flag | Severity | Example |
|----------|----------|---------|
| Unreasonable time expectation | High | "Build a production RAG system in 2 hours" |
| Uses company's real data | High | "Here's our actual customer support dataset" |
| Solves a current business problem | High | "Build exactly what our team has been planning" |
| No time limit specified | Medium | "Take as long as you need" (means: unlimited free labor) |
| Vague success criteria | Medium | "Make it good" with no quality bar |
| Requires proprietary tools | Medium | "Must use our internal AI platform" |
| No compensation for extensive work | Low | 10+ hour assignments with no stipend |
| No feedback guaranteed | Low | "We'll be in touch" with no timeline |

### The Spectrum of Exploitation

**Legitimate:** 4-6 hour assignment, clear requirements, company-provided resources, guaranteed feedback within one week, assignment is generic enough to not be free consulting.

**Gray Area:** 8-10 hour assignment, somewhat vague requirements, uses realistic but not company-specific data, feedback timeline unspecified.

**Exploitative:** 15+ hour assignment, uses company's real data or solves their actual problem, no feedback guarantee, assignment is suspiciously similar to a current job posting for the role.

### How to Respond

**For gray-area assignments:**

1. **Clarify the scope upfront.** Email the recruiter: "I want to make sure I allocate the right amount of time. What's the expected time investment for this assignment?"
2. **Set your own boundaries.** Decide in advance how many hours you're willing to spend. Stop at that boundary even if the solution isn't perfect.
3. **Document your time allocation.** In your submission, include a time breakdown. This signals professionalism and prevents scope creep.

**For exploitative assignments:**

1. **Politely decline.** "I appreciate the opportunity, but I'm not able to commit 15+ hours to a pre-interview assignment. Is there a shorter alternative that would demonstrate my skills?"
2. **Propose an alternative.** "Would a 1-hour live coding session or a portfolio review of my existing work serve the same purpose?"
3. **Walk away if necessary.** A company that exploits candidates before hiring will exploit employees after hiring.

Jamal Watkins shared:
> "At Stripe, we deliberately designed our take-home to be completable in 3-4 hours, and we pay candidates $200 for their time. It's not about the money — it's about signaling that we respect your time and expertise. Companies that don't do this are telling you something important about their culture."

### Legal Considerations

- **You own your code** unless you sign an agreement stating otherwise. Companies cannot use your submission without your permission.
- **If a company uses your assignment as production code**, you may have legal recourse depending on your jurisdiction.
- **If an assignment uses company proprietary data**, be cautious about confidentiality obligations that may be buried in the instructions.

---

## Key Takeaways

1. **RAG systems are the most common take-home (42%).** Master building, evaluating, and documenting RAG pipelines.
2. **77% of submissions include no systematic evaluation.** Adding evaluation is the single easiest way to stand out.
3. **The "Thoughtful Minimalist" pattern gets offers.** Simple, clean, well-evaluated beats complex and impressive-but-broken.
4. **Comparison of approaches is a major differentiator.** Show 2-3 variants with metrics, not just one implementation.
5. **Production error handling is rare and valued.** Handle API failures, malformed outputs, and edge cases.
6. **Cost analysis shows practical maturity.** Even a brief cost breakdown signals that you think about real-world constraints.
7. **"What I'd Do With More Time" demonstrates prioritization.** It shows you can see the bigger picture even when time-boxed.
8. **Clean commit history tells a story.** Your Git log should show a narrative of incremental improvement.
9. **Watch for exploitative assignments.** Know the red flags and be prepared to set boundaries or walk away.
10. **The best submissions read like engineering blogs.** Clear narrative, justified decisions, honest limitations, actionable next steps.

---

## Appendix: Assignment Quality Rubric

Use this rubric to self-evaluate your take-home before submitting:

| Criterion | 1 (Weak) | 3 (Acceptable) | 5 (Strong) |
|-----------|----------|-----------------|------------|
| **Functionality** | Barely works, crashes on edge cases | Works on happy path, some edge cases | Works reliably, handles edge cases gracefully |
| **Evaluation** | None or vibe check only | Basic metrics on a few examples | Systematic suite with regression detection |
| **Code Quality** | No error handling, hardcoded values | Some error handling, basic config | Production-grade: logging, config, error handling, tests |
| **Documentation** | Minimal or missing | README with setup instructions | Full docs: rationale, tradeoffs, limitations, next steps |
| **Design Rationale** | No justification for choices | Some explanation of decisions | Documented tradeoffs, comparison of alternatives |
| **Cost Awareness** | No consideration | Mentions cost as a concern | Quantitative analysis with optimization strategies |
| **Creativity** | Tutorial clone | Minor modifications to standard approach | Novel but appropriate solutions to the problem |
| **Time Respect** | Over-engineered or under-done | Appropriate scope for time given | Strategic scoping with "what I'd do with more time" |

**Target score:** 30+ out of 40 for competitive submissions at top companies.

---

## Methodology

- **120+ GitHub repositories** analyzed for code quality, evaluation practices, and design patterns
- **30 hiring managers** interviewed about what makes submissions stand out
- **15 interview coaches** consulted on common submission mistakes
- **8 companies** shared anonymized rubrics and scoring criteria
- **Assignment data** collected from public job postings, candidate reports, and recruiter disclosures
- **Date range:** Q2 2025 — Q1 2026

---

*This note is part of the AI Engineering Field Guide 2026 — Webinars section.*
