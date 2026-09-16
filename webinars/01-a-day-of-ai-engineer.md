# A Day in the Life of an AI Engineer

**Webinar Recording** | Duration: 62 min | Speakers: Jenny Shen (Ramp), Marcus Okafor (Cursor), Priya Natarajan (Stripe)

---

## Overview

What does an AI Engineer actually do all day? This webinar strips away the hype and walks through a real — not idealized — workday from three practitioners working at very different scales. The answer, it turns out, is less "building AGI" and more "staring at evaluation dashboards wondering why the model hallucinated a citation to a paper that doesn't exist."

---

## Morning: Monitoring & Model Performance

### The First 30 Minutes

Every panelist agreed: the day starts with monitoring. Not with writing code, not with architecture decisions — with checking whether last night's deployments are still healthy.

**Jenny Shen (Ramp):**
> "I open Grafana before I open Slack. If the latency p99 on our embedding endpoint spiked overnight, I need to know that before I start responding to any design doc comments."

The morning checklist typically includes:

1. **Model serving dashboards** — latency percentiles (p50, p95, p99), error rates, token throughput
2. **Cost tracking** — API spend over the last 24 hours, any unexpected spikes from retry storms
3. **Quality monitors** — complaint rates from downstream consumers, thumbs-down signals, fallback rates
4. **Data freshness** — are vector store indexes current? Did the nightly re-index job complete?
5. **Incident queue** — any P1/P2 tickets assigned overnight, any ongoing incidents

### The Model Performance Ritual

Marcus described a pattern common at tooling companies:

> "We ship a prompt change, and within hours we can see if it helped or hurt. The feedback loop is tight. But that means the morning is often about interpreting whether the signal is real or just variance."

Key metrics that AI Engineers track differently from traditional SWEs:

| Metric | Traditional SWE | AI Engineer |
|--------|----------------|-------------|
| Error rate | Binary (success/fail) | Spectrum (hallucination severity, relevance score) |
| Latency | Deterministic | Variable (token length dependent, model-dependent) |
| Cost | Mostly fixed | Usage-proportional, can spike unpredictably |
| Regression | Functional | Behavioral (model behavior drifts) |

### The Morning Standup

AI Engineering standups often include a unique question: "Did the model change?" This covers:

- Provider-side model updates (OpenAI silently updating gpt-4o, Anthropic adjusting Claude)
- Self-hosted model redeployments
- Prompt version changes merged overnight
- Embedding model swaps that affect retrieval quality

Priya noted:
> "At Stripe, we track model versions alongside code versions in our deploy annotations. A model update is treated with the same gravity as a database migration."

---

## Mid-Day: Building Features

### The Core Work Block

The middle of the day is where the building happens. But "building" in AI Engineering looks different from what most people imagine.

#### RAG Pipeline Development

The most common feature pattern across all three companies:

1. **Chunking strategy iteration** — Testing overlap ratios, semantic chunking vs. fixed-size, recursive splitting
2. **Embedding model selection** — Balancing cost, latency, and retrieval quality (often settling on a tiered approach: fast cheap model for initial retrieval, re-rank with a better model)
3. **Retrieval parameter tuning** — Top-k, similarity thresholds, hybrid search weighting (keyword vs. semantic)
4. **Context window management** — Deciding what fits, how to prioritize, when to summarize

Marcus on the RAG iteration loop:
> "I've spent three days on a chunking strategy change that ultimately moved recall from 0.72 to 0.74. That sounds tiny, but at Cursor's scale, it means thousands of users get the right code suggestion instead of the wrong one every day."

#### Agent Workflow Construction

Building agentic systems involves a different kind of complexity:

- **Tool definition and boundary-setting** — What can the agent do? What must it ask about?
- **Planning prompt design** — How does the agent decompose a task? How do you evaluate plan quality?
- **Error recovery paths** — What happens when a tool call fails? When the model goes off-track?
- **Guardrail implementation** — Rate limits, cost caps, safety checks, human-in-the-loop triggers

Jenny described Ramp's approach:
> "Our expense categorization agent has a confidence threshold. Below 0.85 confidence, it routes to a human. Above, it auto-categorizes. Tuning that threshold is a weekly activity — it's always a tradeoff between automation rate and accuracy."

#### Prompt Engineering — The Real Version

Prompt engineering in production is not about clever one-shot tricks. It's about:

- **System prompt version control** — Treating prompts as code with commit history, rollback capability
- **A/B testing frameworks** — Running prompt variants against evaluation suites before deployment
- **Prompt decomposition** — Breaking monolithic prompts into composable modules
- **Token budget management** — Ensuring prompts stay within cost and latency budgets as context grows

### The Iteration Speed Problem

All three panelists highlighted the same frustration: AI feature development has a slower iteration loop than traditional software.

> "With regular code, you write it, run it, and know in seconds. With AI features, you write it, run it, get a result, and then you have to evaluate: is this result *actually good*? That evaluation step is the bottleneck." — Marcus Okafor

This is why the afternoon is dominated by evaluation work.

---

## Afternoon: Code Reviews, Evaluation & Collaboration

### The Evaluation Loop

This is the activity that dominates the AI Engineer's day more than any other. The panelists estimated:

- **Jenny:** "60% of my time is evaluation or evaluation-adjacent."
- **Marcus:** "I'd say 50-70% depending on the week."
- **Priya:** "At Stripe, we have a dedicated eval infra team. But I still spend at least 40% of my time on eval-related work."

The evaluation loop consists of:

1. **Writing evaluation cases** — Gold-standard examples that represent real user queries
2. **Running model comparisons** — Testing prompt/model changes against the eval suite
3. **Analyzing failures** — Categorizing errors, identifying patterns
4. **Iterating on fixes** — Adjusting prompts, retrieval, post-processing
5. **Regression testing** — Ensuring fixes don't break previously-working cases

### Code Reviews with an AI Twist

AI code reviews include unique concerns:

- **Prompt changes reviewed for safety** — Could this prompt change enable injection attacks?
- **Model call efficiency** — Are we making unnecessary API calls? Can we cache?
- **Evaluation coverage** — Does this change have corresponding eval cases?
- **Cost impact assessment** — Will this change increase per-request cost significantly?

### Collaboration with PMs

Product managers and AI Engineers have a particularly interesting dynamic. PMs often want "the model to just be smarter," while AI Engineers need to translate that into specific, measurable improvements.

Priya's framework:
> "I make PMs write success criteria before I write any code. 'Better responses' is not a success criterion. 'Reduce miscategorization rate from 8% to 4% on merchant type classification' is."

Common collaboration patterns:
- **Weekly model behavior reviews** — Looking at aggregate quality metrics with the product team
- **User feedback triage** — Categorizing complaints into model issues vs. UX issues vs. edge cases
- **Feature scoping with AI uncertainty** — Accepting that AI features have wider confidence intervals than deterministic features
- **Setting realistic timelines** — AI features are harder to estimate because model behavior is less predictable

---

## Production Incidents & On-Call Realities

### The Unique Pain of AI Incidents

AI incidents are fundamentally different from traditional software incidents:

- **Non-deterministic reproduction** — "It works on my machine" becomes "it works on this prompt but not that one"
- **Provider-side changes** — The model you deployed last week isn't the same model running today
- **Degraded, not broken** — The system works, just worse than before, and detecting "worse" requires eval infrastructure
- **Cost incidents** — A prompt change that increases output tokens by 20% can create a significant cost incident

Marcus on Cursor's worst incident:
> "We had a model provider change their response format slightly — still valid JSON, but the keys were in a different order than before. Our parsing code assumed key ordering. It silently degraded quality for two days before anyone noticed, because our evals checked values but not the full response shape."

### On-Call for AI Systems

Key patterns for AI-specific on-call:

1. **Model health dashboards separate from service health** — Your service can be up while your model is producing garbage
2. **Automated quality canaries** — Periodic test prompts that verify model behavior hasn't drifted
3. **Provider status monitoring** — Tracking status pages and community reports for model provider issues
4. **Cost anomaly alerting** — Alerting on spend rate, not just absolute spend
5. **Rollback procedures for prompts** — One-click prompt rollback, separate from code rollback

---

## Startup vs. Big Tech: How the Day Differs

| Dimension | Startup (20-100 eng) | Big Tech (1000+ eng) |
|-----------|----------------------|----------------------|
| Monitoring | DIY Grafana + alerts | Mature observability platform |
| Model access | API-first, limited fine-tuning | Fine-tuning, self-hosting possible |
| Evaluation | Manual + ad-hoc scripts | Dedicated eval infrastructure |
| On-call | Everyone is on-call | Dedicated SRE + rotation |
| Feature scope | Full-stack AI work | Specialized (retrieval OR generation OR eval) |
| Prompt iteration | Deploy immediately, monitor | Staged rollout, canary deployments |
| Cost sensitivity | Hyper-aware, every dollar counts | Less constrained, more experimentation |
| Collaboration | Direct with founders | Through PMs and tech leads |
| Stack choice | Pragmatic, ship fast | Standardized, often internal tools |

Jenny, who has worked at both:
> "At a startup, you're the AI team. You do the RAG, the eval, the deployment, the monitoring, the on-call. At a big company, you might own just the retrieval ranking model and never touch a prompt. Both have value. But know which you're signing up for."

---

## Key Takeaways

1. **Monitoring is the real morning routine.** AI Engineers start their day checking model health, not writing code.
2. **The evaluation loop dominates.** Expect to spend 40-70% of your time on evaluation-related work.
3. **AI incidents are sneakier than traditional incidents.** Degraded quality is harder to detect than outright failures.
4. **Prompt engineering is systems engineering.** It's about version control, testing, and composability — not clever one-shots.
5. **The iteration loop is slower.** Evaluating whether a change "works" is fundamentally harder than checking if code compiles.
6. **PM collaboration requires metrics.** Force specificity. "Better" is not a success criterion.
7. **Your day depends enormously on company size.** Startup AI Engineers are generalists; big-tech AI Engineers are specialists.
8. **Provider dependency is a fact of life.** Model updates you don't control will affect your system. Plan for it.
9. **Cost awareness is a core skill.** Token-efficient design is as important as time-efficient design.
10. **The role is still defining itself.** What you do today may look different in six months — and that's okay.

---

## Recommended Resources

- [Building LLM Apps: A Step-by-Step Guide](https://huyenchip.com/2023/04/11/llm-engineering.html) — Chip Huyen
- [Prompt Engineering Guide](https://www.promptingguide.ai/) — DAIR.AI
- [The AI Engineering Stack](https://www.latent.space/p/ai-engineering-stack) — Latent Space Podcast

---

*This note is part of the AI Engineering Field Guide — Webinars section (Updated: September 16, 2026).*
