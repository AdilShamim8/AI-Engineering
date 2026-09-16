# Project Deep Dive

> The project deep-dive is one of the most important and most underrated rounds in AI engineering interviews (Updated: September 16, 2026). It's your opportunity to demonstrate real production experience, technical depth, and the ability to reason about trade-offs — things that are hard to assess in a coding exercise or system design prompt.

---

## Format

| Aspect | Details |
|--------|---------|
| Duration | 45–60 minutes |
| Format | You present a past project, then answer deep follow-up questions |
| Typical split | 15–20 min presentation + 25–40 min Q&A |
| Interviewers | 1–3 (usually senior engineers + hiring manager) |
| Common names | "Project walkthrough", "Past experience deep-dive", "Technical retrospective" |

---

## What Interviewers Evaluate

### Technical Depth
- Do you understand the system at a level deeper than "I used LangChain"?
- Can you explain the architecture, data flow, and component interactions?
- Do you understand the ML/AI components well enough to debug them?

### Trade-off Reasoning
- Can you articulate *why* you chose this approach over alternatives?
- Do you acknowledge the downsides of your chosen approach?
- When you say "it depends," do you specify what it depends on?

### Production Awareness
- Have you dealt with production issues (latency, cost, reliability)?
- Do you think about monitoring, alerting, and observability?
- Can you discuss deployment, rollback, and incident response?

### Failure Handling
- What broke in production and how did you respond?
- What would you do differently with hindsight?
- Do you have a blame-aware but accountability-oriented mindset?

### AI-Specific Dimensions
- How did you handle model non-determinism?
- How did you evaluate the AI component of your system?
- How did you manage prompt drift, model updates, or cost surprises?
- What was your approach to hallucination and safety?

---

## Common Follow-Up Probes

Be ready for these — they come up in almost every project deep-dive:

### Architecture Probes
- "Why did you choose this architecture over [alternative]?"
- "What would change if you needed to handle 10x the traffic?"
- "How would you extend this to support [new requirement]?"
- "Draw the architecture on the whiteboard and walk me through it."

### Technical Depth Probes
- "How does the retrieval component actually work?"
- "What embedding model did you use and why?"
- "How did you handle the context window limit?"
- "Walk me through what happens when a user submits this query."

### Failure and Edge Cases
- "What broke in production?"
- "What's the biggest failure you've had with this system?"
- "How did you handle [specific edge case]?"
- "What happens when the LLM returns garbage?"

### Scaling Probes
- "How would you scale this to millions of users?"
- "What's the cost per query? How would you reduce it?"
- "How would you handle real-time updates to the document corpus?"
- "What's the bottleneck in this system?"
- "How did you monitor prompt caching hit rate and TTFT (time-to-first-token) degradations?"

### Agentic & Tool-Execution Probes (2026)
- "How did you isolate and sandbox untrusted code executed by agents or tools (e.g. gVisor, Firecracker microVMs, Docker)?"
- "What was your state-recovery mechanism when an agent got stuck in an infinite retry loop or hit a 429 rate limit mid-plan?"
- "How did you handle human-in-the-loop approvals for sensitive actions without introducing unbounded async latency?"
- "If your tools were exposed via Model Context Protocol (MCP), how did you handle authentication, permissions, and tool discovery?"

### Reflection Probes
- "What would you change if you rebuilt this today?"
- "What did you learn from this project?"
- "What's the biggest technical debt in this system?"
- "If you had 2 more weeks, what would you improve?"

---

## Project Presentation Tips

### Choosing the Right Project

**Ideal project characteristics:**
- You built it (or led the technical direction)
- It has AI/LLM as a core component (not a bolt-on)
- It ran in production (or close to it)
- It had interesting trade-offs and decisions
- Something went wrong that you can talk about

**Avoid:**
- Pure tutorial or course projects with no customization
- Projects where you only used an API without understanding the system
- Projects you can't discuss in depth (NDA, too old, too superficial)

### Structuring Your Walkthrough

Use this **6-part structure** for maximum impact:

#### 1. Context (2–3 minutes)
- What problem were you solving?
- Who were the users?
- What were the constraints (time, budget, team size)?

#### 2. Requirements and Constraints (2–3 minutes)
- What were the functional requirements?
- What were the non-functional requirements? (latency, cost, accuracy)
- What were the initial assumptions?

#### 3. Architecture and Design Decisions (5–7 minutes)
- Walk through the architecture (have a diagram ready)
- Explain the key design decisions and *why* you made them
- Mention alternatives you considered and rejected (with reasons)

#### 4. Implementation Details (3–5 minutes)
- Highlight 1–2 technically interesting implementation challenges
- Show specific code or configuration if relevant (not the whole codebase)
- Discuss the AI/ML components in depth

#### 5. Production and Evaluation (2–3 minutes)
- How did you evaluate the system? What metrics?
- What was the production deployment like?
- What monitoring and alerting did you set up?

#### 6. Retrospective (2–3 minutes)
- What went well?
- What went wrong?
- What would you change with hindsight?
- What did you learn?

---

## Red Flags and Green Flags

### 🚩 Red Flags

1. **"I just used LangChain"** — without understanding what LangChain does under the hood
2. **No trade-offs discussed** — every design decision has downsides; not acknowledging them signals naivety
3. **No failures mentioned** — if nothing went wrong, the project wasn't complex enough or you're not being honest
4. **Hand-waving on evaluation** — "it worked well" without metrics or methodology
5. **No production awareness** — discussing only the development experience, not deployment and operations
6. **Blaming others for everything** — ownership means acknowledging your own mistakes
7. **Can't explain "why"** — if you can't explain why you chose approach X over Y, it suggests you didn't evaluate alternatives
8. **Surprised by follow-up questions** — if you built it, you should be able to go deep on any component
9. **No mention of cost or latency** — in 2026, ignoring these signals you haven't built production AI systems
10. **Ignoring safety** — no discussion of guardrails, PII handling, or prompt injection risks

### ✅ Green Flags

1. **Immediate articulation of trade-offs** — "We chose RAG over fine-tuning because X, but the trade-off was Y"
2. **Specific metrics and numbers** — "We reduced hallucination rate from 12% to 3%" not "we improved accuracy"
3. **Honest about failures** — "The biggest issue was X. We debugged it by Y. In hindsight, we should have Z."
4. **Production stories** — "On launch day, we hit a rate limit and had to implement exponential backoff"
5. **Evaluation methodology** — "We built a golden dataset of 200 examples and ran automated evaluation on every prompt change"
6. **Cost awareness** — "Our cost per query was $0.03, which was too high, so we implemented semantic caching and got it to $0.008"
7. **Architecture evolution** — "We started with a simple pipeline, then evolved to [more complex architecture] because of [specific problem]"
8. **Ownership language** — "I decided to X because Y" vs. "We just did X"
9. **Safety consciousness** — "We added guardrails because we noticed PII leakage in testing"
10. **Clear communication** — Can explain complex systems to interviewers who may not know the specific tools

---

## Handling Questions About AI-Generated Code in Your Projects

This is a new and increasingly common line of questioning in 2026. Interviewers want to understand your relationship with AI coding tools.

### Common Questions

- "How much of this code was AI-generated?"
- "Did you use Copilot/Cursor/ChatGPT to build this?"
- "What's your process for verifying AI-generated code?"
- "How do you debug AI-generated code that doesn't work?"

### How to Answer

**Be honest but frame it well:**

> "I use AI coding tools extensively — probably 40–50% of my code is AI-assisted in some way. But I treat AI output as a first draft that always needs review. For this project, I used Cursor for boilerplate and test generation, but the architecture decisions, the RAG pipeline design, and the evaluation framework were all hand-crafted because they required domain-specific reasoning that AI tools don't handle well yet."

**Key principles:**
1. **Don't hide AI tool usage** — it's expected in 2026; hiding it is a red flag
2. **Emphasize verification** — show that you review, test, and validate AI output
3. **Distinguish between types of code** — AI is great for boilerplate, but architecture and domain logic require human judgment
4. **Show ownership** — you're responsible for all code in your project, whether you typed it or an AI suggested it
5. **Demonstrate AI fluency** — knowing *when* to use AI tools and *when not to* is a valuable skill

---

## Preparation Checklist

- [ ] Choose 2–3 projects you can present in depth
- [ ] Prepare architecture diagrams for each (simple, clear, not overloaded)
- [ ] For each project, write down: the problem, the architecture, 3 key decisions with trade-offs, 1 failure story, and what you'd change
- [ ] Practice presenting in 15–20 minutes (time yourself)
- [ ] Practice answering the common follow-up probes listed above
- [ ] Prepare specific metrics and numbers for each project
- [ ] Have an honest answer ready about AI tool usage in your projects
- [ ] Prepare 1–2 "deep technical details" you can go into if asked
- [ ] Know the cost and latency characteristics of your systems
- [ ] Practice explaining your projects to a non-expert (communication clarity)

---

> **Next**: [AI System Design →](04-ai-system-design.md)
