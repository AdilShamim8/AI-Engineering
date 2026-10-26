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
  - **A:** We run hybrid RAG — BM25 plus dense retrieval, reciprocal-rank fusion, cross-encoder rerank, then a Sonnet-class generator with inline citations. The alternatives were fine-tuning and long-context stuffing. Fine-tuning failed on freshness: the corpus updates daily, and every refresh meant weeks of data work plus ~$15k of training for knowledge the model would then state with unjustified confidence. Stuffing 100K tokens "worked" in demos but cost $0.40+/query with 12-second latency. RAG gave us daily-updatable knowledge, p95 of 2.4s, and $0.011/query, later cut to $0.004. The trade-off we accepted: retrieval became our main failure surface — roughly 60% of production bugs were chunking or indexing issues, not the model — so we invested heavily in retrieval evals.
- "What would change if you needed to handle 10x the traffic?"
  - **A:** At ~40k queries/day we're overprovisioned, so 10x is an isolation and cost exercise, not a rearchitecture. Concretely: shard the vector index 3→12 nodes so reindex writes stop competing with query reads; move embedding and rerank inference to autoscaled GPU pools with dynamic batching, because those degrade first under burst; add tenant-level rate limiting and queue admission control so one noisy tenant can't starve the rest; and negotiate provisioned throughput or add a second provider, since LLM API rate limits — not our compute — would be the actual ceiling. Some things get better: semantic-cache hit rate rises with traffic diversity, pushing blended cost below $0.004. The underrated change is organizational: on-call runbooks and load-shedding behavior need to exist before the traffic does.
- "How would you extend this to support [new requirement]?"
  - **A:** The pipeline is staged — ingest, retrieve, rerank, generate, cite — with each stage behind an interface and versioned independently, so extensions are additive rather than rewrites. When we added multilingual support, that meant a language-detection step plus per-language embedders and BM25 analyzers, not a new retrieval stack: three weeks, a 90-query golden-set slice, non-English recall@5 went 71→79. When we added table Q&A, it was a table-aware parser plus a table-summary index alongside chunk vectors. My process for any new requirement: find the narrowest stage it touches, write the eval slice first, ship behind a feature flag, A/B against the current path, and only then generalize. The failure mode I watch for is requirements that quietly cross stages — like permissions, which touch everything.
- "Draw the architecture on the whiteboard and walk me through it."
  - **A:** I draw two horizontal lanes, five boxes each, left to right. Ingestion lane: document sources + change webhooks → parser/chunker → embedder → dual indexes (Qdrant for vectors, OpenSearch for BM25), with a blue-green alias swap and an eval gate before cutover. Query lane: client → API (auth, tenant context, PII redaction, semantic cache) → query rewriter → hybrid retrieve top-50 → cross-encoder rerank to 6 → prompt assembly with a cached stable prefix → streaming generation with citations. A vertical rail underneath: OpenTelemetry tracing into Langfuse, cost meters, and the nightly golden-set evals. Then I walk one real query through with timings — 2.4s p95 end to end — and annotate failure modes: abstain below the rerank threshold, fail-closed ACLs, fallback to raw excerpts if generation fails. Keeping it to ~10 boxes forces the trade-offs into the conversation.

### Technical Depth Probes
- "How does the retrieval component actually work?"
  - **A:** Hybrid, with a rerank. A small model first rewrites the query — expand acronyms, split multi-part questions into sub-queries; HyDE only when the first pass returns zero recall. Then two parallel retrievals: BM25 in OpenSearch catches exact identifiers, product codes, and names that embeddings miss; dense retrieval over Qdrant (HNSW, int8-quantized, 18M chunks) catches paraphrase and intent. Reciprocal-rank fusion merges them, then a cross-encoder (bge-reranker-v2-m3) scores the top 50 against the query and we keep the top 6, filtered to the latest document version. ACLs are query-time filters inside the ANN search — never post-filtering. Below a rerank-score threshold we abstain rather than guess. Numbers: recall@5 is 84% hybrid versus 76% dense-only and 63% BM25-only on our 300-query golden set; the rerank costs 140ms p95 and buys about 7 points of answer accuracy.
- "What embedding model did you use and why?"
  - **A:** voyage-3.5-lite, 1024 dimensions, after benchmarking three candidates on our own 300-query golden set with our actual chunk distribution — leaderboard numbers never transferred for us. Results: text-embedding-3-large hit 78% recall@5, voyage-3.5-lite 76%, self-hosted bge-large 69%. The top two were within two points, but voyage cost roughly a quarter per token and the lower dimensionality cut index memory and search latency noticeably, so I took it and spent the savings on the cross-encoder reranker — which bought +7 answer-accuracy points versus the two the bigger embedder offered. Switching embeddings later means re-embedding all 18M chunks — about $400 and nine hours — so changes are golden-set-gated, and the model version is pinned per index. Lesson: benchmark on your data; the reranker is the better accuracy-per-dollar lever.
- "How did you handle the context window limit?"
  - **A:** It stopped being a constraint once we stopped treating it as free. We have 128K available but budget context explicitly: ~2K system prompt and few-shots (prompt-cached), six retrieved chunks at ~700 tokens each, a 1K rolling conversation summary, and a capped response. Long conversations get summarized — last six turns verbatim, older turns compressed to ~300 tokens, with re-retrieval triggered when the summary detects a topic shift. We did test naive stuffing at 100K of context: cost and prefill latency scaled linearly, and accuracy dropped — our needle-in-haystack checks were near-perfect at 32K but degraded past ~50K, with mid-context facts recalled worst ("lost in the middle"). So the real limit was never tokens; it was relevance per token, and retrieval quality is how you buy it.
- "Walk me through what happens when a user submits this query."
  - **A:** Timings from a real trace, p95s. t=0: gateway auth, tenant context, PII redaction — 3ms. Next, semantic-cache lookup (embed the query, cosine against recent cache): on a hit, ~22% of traffic, we return in ~300ms for a fifth of the cost. Otherwise a small model rewrites the query — 180ms, the slowest pre-LLM step. t≈200ms: parallel hybrid retrieval, Qdrant ANN 18ms plus BM25 40ms, fused with RRF. t≈350ms: cross-encoder rerank, 140ms, keep top 6. t≈500ms: prompt assembly — stable prefix served from prompt cache — and streaming starts at TTFT ~850ms; a 400-token answer completes around 2.4s. Every step emits an OpenTelemetry span keyed to a trace ID returned in the response header, so any user complaint is one lookup away from the full decision path, including which chunks were retrieved and their scores.

### Failure and Edge Cases
- "What broke in production?"
  - **A:** A chunking regression. A minor-version bump of our PDF parsing library changed reading order on two-column layouts, and our 800-token chunks started splitting tables mid-row. Retrieval recall slid from 84% to 73% over about a week — gradually, because reindexing is incremental, so good chunks aged out slowly and no single deploy looked guilty. Our retrieval-score drift alert fired two days later than it should have; the threshold was set too loose. Fix: rolled back the parser, reindexed affected shards, then hardened the loop — nightly golden-set evals now run against the live index, and a 2-point recall drop pages on-call. The meta-lesson I took: ingestion changes are production changes. We were testing model-prompt changes in CI but treating the parsing library as a mundane dependency bump.
- "What's the biggest failure you've had with this system?"
  - **A:** A cross-tenant leak, six hours, caught by a user report instead of our monitoring — the part that still bothers me. A schema change made the tenant field optional, and a code path that had been applying ACLs inside the ANN query silently degraded to post-filtering — which returns nothing for documents without tenant tags, except one legacy collection had no tags at all, so its documents flowed through unfiltered to another team's answers. No data left the organization, but it was a trust event. The 45-minute incident response ended with three fixes: absent tenant context now denies by default rather than allowing, per-tenant synthetic canary queries run every five minutes and would have caught this in minutes, and schema changes to security-relevant fields require review. I owned the original schema design.
- "How did you handle [specific edge case]?"
  - **A:** Take the one that taught me most: users asking questions the corpus couldn't answer, and the model helpfully hallucinating instead. Three-part fix. First, a rerank-score threshold: below it, we abstain and show the closest matches instead of generating. Second, the prompt explicitly permits "I don't know" — models default to being helpful unless refusal is a sanctioned behavior. Third, a dedicated eval slice of 60 unanswerable questions: before the fix the model answered 38% of them confidently; after, 6%. The tuning mattered: set the threshold too high and we refused hard-but-answerable questions — a 4% false-refusal rate we tuned down to 1.5%. And abstention needs UX: we surface the retrieved chunks and an ask-an-expert escalation, because a bare "I don't know" just sends users somewhere worse.
- "What happens when the LLM returns garbage?"
  - **A:** Layered defenses — you can't prevent garbage, only bound it. Layer one: schema validation. Every response must parse as typed structured output — answer, citations array, confidence — and malformed output triggers one retry with the validation error appended, which fixes about 70% of cases. Layer two: a small-model groundedness check verifies each claim is supported by a cited chunk; unsupported answers regenerate with a stricter prompt or degrade to showing the raw excerpts. Layer three: hard failure falls back to a UI with retrieved chunks and no generated answer. Current rates: ~1.2% of generations trigger the retry, 0.15% hit the fallback. Garbage from one tenant trips a circuit-breaker alert, because in practice it's almost always upstream — bad retrieval or corpus pollution — not the model. Everything unparseable lands in a review queue that feeds the golden set.

### Scaling Probes
- "How would you scale this to millions of users?"
  - **A:** The shape survives; the constraints move. One: the LLM API becomes the ceiling before our compute does — provisioned throughput, multi-provider failover, and request hedging. Two: routing is the real scaling lever. Roughly 45% of traffic is repeat or FAQ-shaped — semantic cache plus a small model; ~20% needs the full hybrid-retrieval-plus-frontier path; the middle tier gets a mid model without rerank. Serving 10M queries/day at $0.004 is $40k/day, so I'd distill a small model on frontier traces for tier-one traffic, targeting ~$0.0015. Three: regional read replicas of the index plus regional embedding endpoints — p95 grows with distance. Four: ingestion partitions per tenant with per-tenant reindex queues. Five, underrated: evals and on-call must scale too — sampled online judging beats trying to gold-plate offline sets.
- "What's the cost per query? How would you reduce it?"
  - **A:** $0.011 blended at launch, $0.004 today. The initial breakdown: generation input tokens were 65% of spend, because 4K of retrieved context went out with every query. Reductions in ROI order: prompt caching on the stable system prefix — 60% hit rate, cached input billed at ~10%; a semantic cache for near-duplicate queries — 22% hit rate, near-zero cost on hits; routing simple queries to a small model, about 45% of traffic; and trimming six chunks to five after citation analysis showed the sixth was almost never referenced — no measurable accuracy loss. Next lever: distilling a small model on frontier traces for the tier-one path, projected ~$0.0015. The metric I actually manage is cost per resolved query, not cost per token — a cheap wrong answer is the most expensive thing we produce.
- "How would you handle real-time updates to the document corpus?"
  - **A:** Two freshness tiers, because almost nobody actually needs real-time — they need "never stale." Hot path: change-data-capture webhooks from the source systems → queue → parse, embed, and upsert only the changed documents, live in the index within ~90 seconds. That covers the ~5% of docs that change often — policies, pricing, FAQs. Cold path: nightly blue-green reindex of everything else; build index B, run the 300-query golden set against it, swap the alias atomically only if recall holds, and repointing the alias back is the rollback. Two gotchas we hit the hard way: deletions must propagate explicitly — tombstones, not trust that the source is gone — and top-k must filter on latest document version, or answers splice old and new policy text mid-paragraph. Freshness bugs look like hallucinations to users, which makes them the worst kind.
- "What's the bottleneck in this system?"
  - **A:** Measured, not guessed. End-to-end, LLM time-to-first-token dominates — ~850ms of a 2.4s p95 — but that's mostly provider-bound. Of what we control, the reranker is the bottleneck: 140ms p95 on GPU, and under burst it's the first thing to degrade because batching trades tail latency for throughput. Second: embedding throughput during reindex competes with query-path work — an early reindex doubled p99 query latency for an afternoon until we split them onto separate pools. The systemic bottleneck, though, is evaluation throughput. We can produce changes far faster than we can validate them: the golden set is 300 queries and growth is manual. That's why 5% of production traffic gets async LLM-judge scoring — the queue never blocks a deploy, but it tells us within a day when one was a mistake.
- "How did you monitor prompt caching hit rate and TTFT (time-to-first-token) degradations?"
  - **A:** Both are first-class metrics with their own alerts, because each is a canary for a different failure. Prompt caching: we log cached versus uncached input tokens per request from the provider's usage fields, aggregate hit rate per prompt-template version in Grafana, and alert on a >10-point week-over-week drop. That rule caught a developer inserting a timestamp at the top of the system prompt — hit rate fell from 60% to 9% overnight and cost tripled before the alert fired at 2am. TTFT: measured server-side and client-side, p50/p95 per model and template version, alerting at p95 >1.2s for 15 minutes — plus a distribution check, because bimodal TTFT usually means one degraded provider region rather than general slowdown. Cache hit rate is a cost canary; TTFT is a UX canary; both need per-version dimensioning or you can't localize the regression.

### Agentic & Tool-Execution Probes (2026)
- "How did you isolate and sandbox untrusted code executed by agents or tools (e.g. gVisor, Firecracker microVMs, Docker)?"
  - **A:** Layered isolation. Agent-written code executes in ephemeral gVisor (runsc) containers — a user-space kernel intercepting syscalls — because plain Docker shares the host kernel and model-generated code is untrusted input, full stop. Per-container constraints: no persistent filesystem, no metadata-service access (the classic cloud credential-leak path), network egress through a deny-by-default allowlist proxy, 512MB memory, 10 seconds CPU, output capped at 10MB so a hostile script can't exhaust us with logs. We benchmarked gVisor overhead at 10–15% on our workload — acceptable. Firecracker microVMs offer stronger isolation and ~125ms cold starts, but the operational overhead wasn't justified at our volume; I'd revisit above thousands of executions per minute or with harder multi-tenancy requirements. Containers are single-task and destroyed afterward. Trusted build tooling stays in plain Docker; the boundary is "did a model write this."
- "What was your state-recovery mechanism when an agent got stuck in an infinite retry loop or hit a 429 rate limit mid-plan?"
  - **A:** Durable checkpointing is the foundation: agent state — the plan, completed steps, tool results — persists to Postgres after every step, so a crash, a deploy, or an OOM resumes mid-plan instead of restarting from scratch. Resumability reduced our blast radius more than any other change. Every side-effecting tool call carries an idempotency key, so a retry after a timeout can't double-charge or double-send. Rate limits get exponential backoff with jitter and a per-provider retry budget — max three attempts, 30-second cap. Beyond the budget the plan doesn't fail; it pauses into a resumable queue, with a dead-letter escalation if it stalls past 15 minutes. Infinite loops are bounded structurally: hard caps on steps (25), wall-clock (5 minutes), and spend ($2 per task); hitting any cap checkpoints state and escalates to a human with the full trace attached.
- "How did you handle human-in-the-loop approvals for sensitive actions without introducing unbounded async latency?"
  - **A:** Approval is a budgeted state, not an unbounded wait. Sensitive actions — anything irreversible: external sends, deletions, spend over a threshold — pause the workflow and emit an approval task containing the plan, the exact tool call, and a diff of what it would do. A five-minute SLA timer bounds it: on timeout the branch fails safe — canceled, user notified, state checkpointed so it can resume after approval. Never auto-execute on timeout; the whole point of the gate is that absence of a human is not consent. We measured 80% of approvals landing within 90 seconds, and the Slack-based approval card mattered more than expected — context and a one-click decision. To cut volume, we pre-approve low-risk parameter ranges: the agent can spend up to $5 autonomously and asks above that. Worst-case latency is five minutes, by construction.
- "If your tools were exposed via Model Context Protocol (MCP), how did you handle authentication, permissions, and tool discovery?"
  - **A:** Remote MCP servers authenticate with OAuth 2.1 plus PKCE, brokered by a gateway; agents never hold long-lived credentials — tokens are short-lived, scoped per server. Permissions are enforced at the gateway with per-role tool allowlists, not trusted from the client: each agent sees only the tools it's authorized to call, so least privilege holds by construction rather than by prompt. Discovery: tools/list responses are cached, versioned, and diffed on every server update — a new or changed tool triggers review before it reaches agents, because tool descriptions are injected instructions and tool poisoning is a real attack class. We pin tool manifests, treat descriptions as untrusted input, and keep egress controls as the backstop if a compromised server lies. Every tools/call emits an OTel span with full request and response for audit; discovery changes are announced, never silent.

### Reflection Probes
- "What would you change if you rebuilt this today?"
  - **A:** Three things, and one anti-change. Evaluations first: we built retrieval for six weeks before writing the first golden set, and its first run invalidated a chunking decision I'd defended in code review — I'd build the eval harness in week one, even with 20 queries. Second, async ingestion from day one: the synchronous parse pipeline was fine at 100k documents and became the most painful refactor at 2.4M; queue-partitioned, versioned ingestion would have cost a week early and saved a quarter. Third, a thinner abstraction: our in-house provider wrapper grew into a mini-framework exactly when the platforms shipped structured outputs and native caching controls — I'd wrap far less now. What I wouldn't change: hybrid retrieval with a reranker, fail-closed ACLs, blue-green reindexing. Those earned their complexity; the rest was mostly premature infrastructure.
- "What did you learn from this project?"
  - **A:** Three lessons that changed how I work. First: retrieval quality, not model quality, was our ceiling. We swapped generator models twice and answer accuracy moved about two points; fixing chunking and adding the reranker moved it fifteen. Most "LLM bugs" are data-path bugs wearing a costume. Second: non-determinism is a systems problem, not a model problem — pinning versions, temperature 0 where determinism matters, structured outputs, and eval gates gave us reproducibility without ever "solving" the model. Third: cost is an architecture decision, not an optimization sprint — the drop from $0.011 to $0.004 came from caching and routing choices made in design, not from a later tuning pass. And a personal one: instrument first. Every time something broke, the system already knew — the gap was whether a metric was pointed at it.
- "What's the biggest technical debt in this system?"
  - **A:** Prompt and config sprawl. Forty-plus prompt fragments scattered across code, database, and feature flags, with model-version pinning done manually — a provider migration took three weeks, most of it archaeology. It's the biggest debt because every safety property lives in those fragments: PII instructions, abstention policy, citation format. A prompt change is a behavior change, and for most of the project it shipped with zero test coverage unless someone remembered the eval gate. We're paying it down now: prompts moved into a versioned registry where each change requires a schema check and an eval run against the golden set before merge. Second place: the golden set itself — 300 queries, English-only, while we serve multilingual traffic. The fix is mining real failures from feedback and low-rated traces; user complaints are the highest-value eval queries nobody writes.
- "If you had 2 more weeks, what would you improve?"
  - **A:** Ranked by compounding value. Week one: mine two months of thumbs-down feedback and low-rated traces into ~150 new golden-set queries with failure-mode labels — early analysis shows three clusters: table Q&A, multi-hop questions, and acronym ambiguity. This compounds, because every future change gets evaluated against real failures instead of my guesses. Week two, in order: ship citation click-through tracking — we display citations but have zero signal on whether users verify them, and it's the cheapest online relevance metric available; then A/B a distilled cross-encoder against the current reranker, 140ms down to a projected 60ms, gated by the expanded eval set from week one. If I only get one: the eval set. Everything else is guesswork without it — that's the same answer I'd have given at the start of the project, which is itself the lesson.

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
