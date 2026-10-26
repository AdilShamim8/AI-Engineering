# AI System Design

> AI system design has emerged as a distinct interview category — updated September 16, 2026. It tests your ability to design systems where the core component is an LLM or AI model, and where non-determinism, cost, latency, and safety are first-class design constraints.

---

## AI System Design as a Distinct Category

Traditional system design asks: "How do you design a URL shortener?"
ML system design asks: "How do you design a recommendation system?"
**AI system design asks**: "How do you design a conversational AI that helps doctors diagnose patients — safely, reliably, and at scale?"

The key differences:

| Aspect | Traditional | ML System | AI System |
|--------|------------|-----------|-----------|
| Core component | Database/cache | Model training pipeline | LLM + retrieval + agents |
| Determinism | Deterministic | Probabilistic predictions | Non-deterministic generation |
| Failure mode | Timeout, error | Wrong prediction | Hallucination, injection, cost spike |
| Key constraint | Throughput, consistency | Feature freshness, model accuracy | Safety, cost, latency, quality |
| Evaluation | Uptime, latency | Accuracy, precision/recall | Faithfulness, relevance, safety |
| Scaling challenge | Database sharding | Feature store, model serving | Token throughput, context management |
| Cost model | Infrastructure | Compute for training | Per-token inference cost |

---

## Format

| Aspect | Details |
|--------|---------|
| Duration | 45–60 minutes |
| Typical question | "Design an AI-powered [X]" |
| Time allocation | 5 min clarify → 10 min high-level → 20 min deep-dive → 10 min trade-offs → 5 min wrap-up |
| Interviewers | 1–2 (usually senior/staff engineers) |
| Tools | Whiteboard or shared doc — diagrams expected |

### Time Allocation (Recommended)

| Phase | Duration | What to Cover |
|-------|----------|---------------|
| Requirements clarification | 5 min | Scope, constraints, users, scale, safety requirements |
| High-level architecture | 10 min | Major components, data flow, AI/non-AI boundary |
| Deep-dive on AI components | 20 min | LLM selection, retrieval strategy, agent design, prompt architecture |
| Trade-offs and alternatives | 10 min | Cost vs. quality, latency vs. accuracy, build vs. buy |
| Monitoring and safety | 5 min | Evaluation, guardrails, incident response, cost control |

---

## Typical Questions

### Core AI System Design Questions

| Question | Key Challenges | Companies |
|----------|---------------|-----------|
| AI Chatbot for customer support | Hallucination, escalation, cost | Intercom, Zendesk |
| Document Q&A / RAG system | Retrieval quality, citations, scale | Doctolib, Casetext |
| Enterprise GraphRAG Knowledge Graph | Entity extraction, graph community clustering, hybrid search | Microsoft, Palantir |
| AI co-pilot for coding | Latency, context, safety of generated code | GitHub, Cursor |
| MCP-Based Multi-Agent Developer Swarm | Tool discovery, RPC authentication, human-in-the-loop sandbox | Anthropic, Cognition |
| Local SLM with Speculative Decoding | Memory footprint, KV cache quant, p99 token throughput | Apple, Meta, Mistral |
| Voice assistant with LLM | Latency, STT/TTS, interruption handling | OpenAI, Amazon |
| Contract generation system | Legal accuracy, clause consistency, review workflow | Harvey, LegalOn |
| AI-powered candidate sourcing | Bias, relevance, personalization | Eightfold, LinkedIn |
| Fraud detection with LLM | False positives, real-time requirements, explainability | Stripe, Goldman Sachs |
| Multi-agent workflow | Orchestration, failure recovery, observability | LangChain, CrewAI |
| Content detection / moderation | Scale, nuance, policy, multilingual | Meta, OpenAI |
| Unified query engine (text + SQL + code) | Query routing, schema understanding, ambiguity | Doctolib, Notion |
| Perplexity-like search engine | Real-time retrieval, citation, speed | Perplexity, You.com |

#### Answers

- AI Chatbot for customer support
  - **A:** Put a router at the front door: a fast classifier (~20ms) splits traffic into deterministic flows (order status, refund policy — pure tool/API calls, no LLM), RAG-able help-center questions, and out-of-scope — the LLM handles only 30–50% of volume, which caps cost and hallucination surface. RAG branch: query rewrite → hybrid BM25 + dense over help center plus account context fetched via tools → cross-encoder rerank top-50→5 → grounded streaming answer with citations; a retrieval-score threshold abstains and escalates rather than guessing. Escalation hands the human agent a transcript summary, account context, and what was already tried. Guardrails: refunds/cancellations execute only through tools with rule checks — never free-text promises; PII redaction inbound and outbound; ticket text treated as untrusted data (injection defense). Numbers: p95 first token <1s; $0.005–0.02 per AI answer vs $5–15 per human ticket; 50–70% resolution is a credible target; semantic cache on FAQ traffic (20–40% hit rate). Failure modes: hallucinated policy (cite-or-abstain), wrong account context from tool errors, model outage (canned fallback + queue). Track deflection, CSAT vs human baseline, escalation precision, cost per resolution.

- Document Q&A / RAG system
  - **A:** Hybrid retrieval (BM25 + dense) → rerank top-50 to top-5 → generate with inline citations; HNSW index sharded by tenant. Sizing: 10M docs ≈ 20–50M chunks; at 768d fp32 that's ~30GB per 10M vectors plus roughly 1.5× HNSW graph overhead — int8 quantization cuts vector memory to a quarter (~7.7GB per 10M), binary + full-precision rescoring to ~1GB; 10M vectors fit comfortably on one 64GB node, so shard 4–8× for tenant isolation and write throughput, not raw capacity. Nightly blue/green reindex with alias swap; CDC webhooks for minute-level freshness on hot collections; doc-version filters prevent top-k from mixing old and new revisions. Latency budget: embed 30ms + ANN 10–20ms + rerank 100–200ms + streaming TTFT 300–600ms → p95 <2s. Enforce ACLs as query-time filters — post-hoc filtering of results is the classic enterprise leak. Evals: a golden set of 200–500 real queries gated in CI on RAGAS faithfulness/context recall, plus 1–5% online sampling with an LLM judge. Failure modes: permission leaks, version mixing, index drift from source-of-truth, stale semantic cache after reindex.

- Enterprise GraphRAG Knowledge Graph
  - **A:** Two layers: a property graph (Neo4j or Postgres+AGE) plus a vector index over entity and community summaries — GraphRAG complements vector RAG, it doesn't replace it. Ingestion: LLM entity/relationship extraction against a typed schema (Haiku/GPT-4o-mini class — extraction calls per document make indexing 10–100× a vector index's cost, so constrain the schema, cache aggressively, and budget per document), entity resolution via blocking + embedding similarity, Leiden community detection, and hierarchical community summaries written by a stronger model. Query routing: local, entity-centric questions → vector search finds entities → expand the k-hop subgraph → grounded answer; global "what are the themes across…" questions → map-reduce over community summaries — GraphRAG's unique capability, since top-k chunk retrieval can't see corpus-level structure. Trade-offs: indexing cost and staleness — re-extract incrementally, only changed documents. Entity-resolution errors compound: one wrong merge poisons every downstream subgraph, so measure resolution precision on sampled pairs. Failure modes: resolution errors, stale graph, community summaries drifting from the underlying text, cost blowup on large corpora. Microsoft's GraphRAG is the reference implementation.

- AI co-pilot for coding
  - **A:** Two surfaces with different latency budgets. Autocomplete: keystroke-to-token <200ms → a small coder SLM (Qwen-Coder/Codestral class, 7–14B) with fill-in-the-middle training, speculative decoding, KV-prefix reuse, and speculative multiline lookahead; served on GPU, increasingly on-device NPU. Chat/agent surface: 128K–1M context assembled from a repo map (tree-sitter AST skeleton, Aider-style — compresses a repo to its symbol graph), an embedding index over AST-aware chunks, BM25 for exact identifiers, and open buffers plus recent diffs. Reindex dirty files incrementally in <100ms; full reindex async. Guardrails: no training on customer code (contractual), secret and license scanning of generated code, sandboxed test execution, approval gates on agent-mode shell commands. Numbers: 25–40% completion acceptance rate is solid; prompt caching on the stable repo-map prefix bills at a fraction (10–50%) of normal input rates, cutting long-context cost dramatically. Failure modes: stale index grounding on renamed/deleted symbols; hallucinated APIs (constrain decoding to retrieved signatures where possible); latency spikes on huge files; command injection in agent mode. GitHub Copilot and Cursor are the reference builds.

- MCP-Based Multi-Agent Developer Swarm
  - **A:** MCP servers expose tools/resources/prompts via JSON-RPC (stdio locally, Streamable HTTP remotely) with capability discovery through tools/list; agents invoke tools/call without knowing server internals. Architecture: an agent gateway holds per-server authenticated sessions (OAuth 2.1 for remote servers, short-lived tokens, per-role tool allowlists) → an orchestrator (typed state machine, LangGraph-style) fans tasks to specialized agents — planner, implementer, tester, reviewer → each runs in an ephemeral sandboxed container (scoped filesystem, network policy, no shared credentials) → a shared artifact store (branches, logs, results) → merge gates require human approval. Human-in-the-loop is a budget, not an afterthought: irreversible actions (push, deploy, external messages) pause for approval; everything else auto-approves within sandbox limits. Observability: one OTel span per MCP call with full request/response — traces make the swarm replayable and debuggable. Numbers: cap depth (5–10 agents), steps (20–50), and spend ($0.50–5 per task); p95 task 2–10 minutes. Failure modes: tool poisoning (malicious descriptions are injected instructions — signed manifests, distrust descriptions), confused-deputy attacks, cascading loops (step/cost caps), sandbox escape. References: Claude Code, Cognition's Devin.

- Local SLM with Speculative Decoding
  - **A:** Speculative decoding: a draft model 5–10× smaller proposes 4–8 tokens; the target model verifies them in one parallel forward pass and accepts the longest valid prefix — mathematically lossless, typically 2–3× throughput; gains vanish if draft acceptance drops below ~60%, so draft and target must share a tokenizer and stay distributionally close. Memory is the binding constraint: a 4B model is 8GB fp16, ~2.5GB at 4-bit; the KV cache then dominates — roughly 130KB/token for an 8B-class GQA model in fp16 (~0.5MB/token pre-GQA), so a 32K context costs 4–17GB → quantize KV to int8/int4 (2–4×) and prefer GQA/sliding-window architectures. Throughput targets: 20–50 tok/s solo on an 8GB-class GPU/NPU for a 4B fp16 model, pushed to 40–100 effective tok/s by speculation. Failure modes: draft misalignment (garbage proposals — verification cost, no speedup), reasoning-style content small drafts can't predict, memory pressure → swap (a ~100× slowdown — cap context), thermal throttling on fanless devices, battery drain. This is Apple's on-device stack; Mistral and Meta ship the compact open models.

- Voice assistant with LLM
  - **A:** The cascade: WebRTC capture → VAD on 20ms frames → streaming STT (conformer-transducer class; partial hypotheses every 100–200ms; endpointing after 600–900ms silence) → turn-taking check → LLM streaming → sentence-chunked neural TTS (first audio ~150ms) → playback. Budget: VAD 20ms + STT finalize 200–300ms + LLM TTFT 200–500ms + TTS 150–300ms ≈ 600ms–1.2s voice-to-voice; <1s feels conversational, >2s kills usage. Interruption handling is the hard part: on barge-in, cancel TTS playback, abort the LLM stream, and truncate conversation state to the tokens actually spoken — unspoken tail tokens must never enter history, or the model "remembers" responses the user never heard. 2026 options: speech-native end-to-end models (GPT-4o-realtime class) collapse the stack to sub-500ms with native turn-taking, at roughly an order of magnitude higher per-minute cost; cascades stay cheaper and let you swap STT/LLM/TTS independently. Failure modes: echo-triggered false barge-ins, STT errors compounding into generation, per-hop latency stack-up, cross-talk, and voice-PII retention policy (buffering limits, redaction).

- Contract generation system
  - **A:** Don't free-generate legal prose. Core asset: a versioned clause library — every clause carries risk level, jurisdiction, negotiation notes, and approval status. Pipeline: intake questionnaire + uploaded documents → RAG over the clause library, precedent corpus, and the firm's playbook → constrained generation that selects and instantiates clause IDs (structured output, not open text) → automated verification: clause-level entailment against source obligations, conflict detection across the draft (governing law vs arbitration venue, indemnity vs liability caps), defined-term consistency linting → redline/diff UI → attorney approval workflow with a full audit trail: every clause tagged with model, prompt, and library versions. Latency is forgiving (30–120s async is fine); cost $0.10–1 per contract — noise against attorney hours. Use a frontier model for drafting, a small one for classification/extraction. Compliance: client contracts are privileged — no training without explicit consent, encryption, tenant isolation, regional residency. Failure modes: hallucinated clause language (restrict generation to retrieved clause text, always show diffs), cross-clause conflicts, jurisdiction errors, silent prompt/model drift (pin versions, golden-contract evals in CI).

- AI-powered candidate sourcing
  - **A:** A classic learning-to-rank core with LLMs at the edges — never in the retrieval hot path. Ingestion: profile parsing → structured attributes + profile embeddings at hundreds-of-millions scale → sharded ANN, p99 lookup <100ms. Query side: JD → LLM extracts structured criteria (skills, seniority, location, must/nice-to-have) → embedding → ANN candidates → LTR rerank trained on engagement signals (view/reply/accept). LLMs shine at query understanding, fit explanations, and drafting personalized outreach — with human review before send. Bias is the defining constraint, in three forms: proxy discrimination (ZIP code, university, name-adjacent features encode protected attributes), feedback-loop amplification (training on historical hires reproduces past bias — inject exploration, use counterfactual evaluation), and legal exposure (EEOC scrutiny; NYC Local Law 144 mandates annual independent bias audits for automated hiring tools). Mitigations: audit features for protected proxies, monitor selection and outreach rates for disparate impact (four-fifths rule) where data collection is lawful, fairness-aware ranking, adversarial testing pre-launch. Failure modes: bias amplification, stale profiles, self-fulfilling predictions, GDPR data-minimization friction, homogeneous outreach tripping spam filters.

- Fraud detection with LLM
  - **A:** Keep the LLM out of the real-time decision path. Hot path (p99 <100ms, billions of transactions/day): deterministic rules → gradient-boosted trees (XGBoost) over engineered features → graph features (shared devices, velocity, account networks — a new card hitting five merchants in ten minutes). LLM value sits where latency and determinism don't matter: async alert triage (pull linked accounts, draft the analyst case summary), unstructured signals (embed email/merchant-descriptor text as features), synthetic rare-pattern generation for training, and human-readable explanations of flags — phrased strictly from SHAP/feature attributions, never invented. Explainability is regulatory: every decline needs a defensible reason code. Numbers: fraud base rate ~0.1% → extreme class imbalance (cost-sensitive losses, negative downsampling); alert-to-true-fraud ratios of 10:1–100:1 mean false positives are the dominant cost — a 0.1% FP jump at 1B transactions is a million wrongly blocked customers. Retrain weekly with drift monitors, because adversaries adapt in weeks. Failure modes: adversarial drift, LLM-hallucinated explanations (ground them in attribution data), label bias (you only train on fraud you caught), latency creep from feature bloat.

- Multi-agent workflow
  - **A:** Start from a deterministic state machine (LangGraph-style typed state, explicit nodes and edges) and insert LLM agents only where a step is genuinely open-ended; a "fully autonomous swarm" is an anti-pattern — coordination cost grows superlinearly and failures become unreproducible. Canonical topology: orchestrator decomposes → workers execute with tools → a separate critic verifies outputs → bounded repair loop (3–5 iterations) → human escalation on repeated failure. Reliability machinery: idempotency keys on every side-effecting tool call (retries must be safe), durable checkpointing so a crash resumes mid-workflow instead of restarting, per-node timeouts, circuit breakers on flaky tools, and hard caps on steps (10–30) and spend. Observability: end-to-end traces (LangSmith/Langfuse) with per-agent inputs/outputs, per-node token cost, and tool latency — plus replay for debugging. Numbers: keep it to ≤5–10 agents; p95 of a five-hop LLM workflow is 10–30s, so this belongs in async or interactive products, not request/response APIs. Failure modes: error propagation between agents (verify at every handoff), infinite loops, cost blowups, and non-reproducibility — temperature 0–0.2, seeds, log everything.

- Content detection / moderation
  - **A:** Tiered classifiers, not LLM-for-everything. Tier 0: hash matching against known-bad databases (PhotoDNA-style for CSAM) — exact/near-exact, negligible cost. Tier 1: small multilingual transformers (XLM-R-derived, distilled, int8-quantized) scoring every item — platform scale means tens of thousands of items per second, so batched GPU inference at <5ms/item; this tier covers 95%+ of volume. Tier 2: LLM-as-judge for the ambiguous 1–5% — harassment-in-context, coded language, cross-cultural nuance — where 1–2s latency is acceptable. Tier 3: humans for appeals and edge cases. Policy velocity is the differentiator: write policy as prompts, generate synthetic labeled examples, distill into tier-1 classifiers — new rules live in days, not months. Multilingual: calibrate thresholds per language and monitor per-language false-positive rates; low-resource languages perform worst, and over-blocking there is both a harm and a regulator magnet. Report precision/recall per policy class, never blended. Failure modes: adversarial obfuscation (homoglyphs, leetspeak, paraphrase — normalize inputs, train on adversarial examples), overblocking legitimate speech (precision floors + appeal flows), inputs engineered against open LLM judges, cold-start on new content types (memes, voice → multimodal classifiers).

- Unified query engine (text + SQL + code)
  - **A:** Router first (small classifier + LLM fallback, p99 ~100ms): text → RAG; SQL → text-to-SQL; code → sandbox. The SQL path is where these systems die, so invest there: a semantic layer (dbt metrics/curated views with business definitions) over raw tables; schema retrieval — embed table/column descriptions and fetch only the relevant subset per query (a 5,000-table schema doesn't fit in context, and shouldn't); constrained generation against the schema; validation via EXPLAIN dry-run before execution; execution as a read-only role with injected LIMITs, 30s timeout, and cost cap; render the SQL and its assumptions to the user. Ambiguity (two definitions of "revenue") → a clarifying question, never a silent guess. Code path: container sandbox — no network, CPU/memory/time limits, output scanning. Cross-engine queries: an orchestrator runs both engines and synthesizes one answer citing documents and SQL results. Numbers: SQL end-to-end p95 3–5s; 85–90% execution accuracy on curated golden sets is achievable with a semantic layer — far lower on raw schemas. Failure modes: hallucinated columns (validate against information_schema), plausible-but-wrong joins (golden query set in CI + always show the SQL), prompt injection in indexed docs, expensive full-table scans.

- Perplexity-like search engine
  - **A:** Query understanding (intent, entity extraction, freshness classification) → parallel retrieval: web index via partner search APIs or a proprietary crawler+index at scale, a news vertical with minute-level freshness, and structured/knowledge data → dedupe → rerank with a cross-encoder or small LLM ranker weighted by authority and recency — explicitly downranking SEO-optimized and AI-generated content farms, a first-order 2026 quality problem → LLM synthesis with sentence-level inline citations, streamed → related questions for follow-on. Numbers: end-to-end p95 1–4s; time-to-first-token <800ms — start synthesizing from the first reranked results while the rest stream in; cost $0.005–0.02 per query (search API + LLM over 5–15 pages); cache aggressively with per-query-class TTLs (news queries never cached). Citation integrity is the product: asynchronously verify each claim entails from its cited page and demote or flag failures — unverified citations destroy trust faster than wrong answers. Failure modes: claim–citation mismatch, stale caches on fast-moving events, index coverage gaps, adversarial SEO engineered to hijack answers, and hallucination beyond the retrieved sources (grounded-generation prompting + abstention when evidence is thin).

### Near-AI Systems

These questions test infrastructure around AI rather than the AI pipeline itself:

| Question | Key Challenges |
|----------|---------------|
| Real-time vs. batch inference pipeline | Latency SLAs, queue management, GPU utilization |
| Data ingestion for AI (ETL) | Document parsing, chunking, embedding, updates |
| Image generation pipeline | Rate limiting, content policy, GPU management, cost |
| GPU job queue for model training | Priority scheduling, preemption, multi-tenant fairness |
| Model deployment and versioning | A/B testing, rollback, shadow deployment, canary |
| Feature store for AI | Real-time features, point-in-time correctness, freshness |

#### Answers

- Real-time vs. batch inference pipeline
  - **A:** One model, two paths, selected by SLA. Real-time (<500ms–2s p95): an autoscaled GPU pool behind a gateway with admission control — token-bucket limits, load shedding to protect p99, continuous batching (vLLM-style: a ~100ms window coalesces concurrent requests for several-fold throughput), and KV/prompt caching for shared prefixes. Utilization is structurally poor (20–40%) because you provision for peak. Batch (embeddings, evals, backfills, doc summarization — nobody is waiting): a queue (Kafka/SQS) feeding workers that pull full batches → 80–95% GPU utilization, spot/preemptible capacity, checkpointed and idempotent so any failure resumes — effectively 5–20× cheaper per token. Design rules: never let batch contend with interactive traffic (separate pools, or priority preemption with checkpoint-restart); make every job idempotent (key = content hash); treat queue lag as a monitored SLO with backpressure. Escape hatch for peaks: shed to the batch tier with async delivery ("we'll email you") rather than erroring. Failure modes: noisy-neighbor GPU contention, retry storms, cold-start latency when autoscaling lags (keep warm capacity ≥ p50 load), silent cost drift as prompts grow.

- Data ingestion for AI (ETL)
  - **A:** Connectors (S3, Drive, Confluence, GitHub) → change detection (webhooks/CDC where offered, hourly scans as fallback — never full rescans) → parsing with a fallback chain per format (layout-aware parsers → OCR for scans → quarantine with metrics; silent parse failures are invisible RAG gaps) → cleaning: dedupe (content hash + fuzzy near-dupes), boilerplate stripping, PII/language detection → structure-aware chunking (headers, ASTs; 256–1K tokens, 10–15% overlap) → batched embedding (thousands of chunks per minute per GPU; batch APIs for non-urgent work) → versioned upsert keyed (doc_id, chunk_hash) so unchanged chunks skip re-embedding — at 10M docs, full re-embeds are a real cost line. Carry metadata end-to-end: version, ACLs, source URI, timestamps. The #1 enterprise failure mode is ACL drift: permissions change upstream and the index keeps serving the old audience — sync ACLs on every change and enforce them as query-time filters. Others: partial ingestion (per-connector completeness dashboards), duplicate chunks crowding out top-k, version mixing on doc updates. Observability: per-stage counters, dead-letter queues, and a freshness SLO per source class.

- Image generation pipeline
  - **A:** Gateway first: auth, per-user token-bucket rate limits and daily quotas, payment/device fingerprints against free-tier farming. Safety wraps both ends: pre-generation prompt classifiers (CSAM, gore, likeness of real people, political figures, brand IP) with hard blocks never reaching GPUs, plus post-generation output classifiers — prompts can be adversarial (benign prompt, harmful output), so you check pixels, not just text. Generation: async job pattern — enqueue, return a job ID, deliver via signed short-TTL CDN URLs; GPU pool autoscaling on queue depth; self-hosted Flux/SDXL-class models with per-style LoRAs, or hosted APIs at $0.002–0.08 per image. Provenance: invisible watermarking + C2PA metadata on every output; perceptual-hash matching against known-bad outputs to catch repeat abuse. Numbers: p95 5–15s for high-res; queue depth is the scaling signal; enforce per-user daily cost caps. Failure modes: adversarial prompt bypass (defense in depth — classifier + output check + flagged-queue human review), GPU hotspots under viral load, deepfake/likeness abuse (identity checks, KYC for API tiers), cost runaway, and safety behavior drifting when models/LoRAs are bumped (re-run the safety eval suite on every change).

- GPU job queue for model training
  - **A:** Kubernetes + Kueue/Volcano (or Slurm on bare metal). Four coupled problems. Gang scheduling: distributed jobs need all N GPUs atomically or they deadlock holding partial allocations. Fairness + priority: weighted fair-share per team (dominant-resource fairness across GPU/CPU/memory), priority tiers (production > experiment > exploration), aging so low priority never starves. Preemption: checkpoint every 15–30 minutes — tuned to the lost-work-vs-checkpoint-cost tradeoff — so preempting a training run costs minutes, not hours; preempt lowest priority first, youngest first within a tier (least lost work). Topology: schedule ranks within NVLink/NVSwitch domains and respect fabric rails, or multi-node NCCL throughput craters. Organizational guardrail: hard quotas and budgets per team, because one unattended hyperparameter sweep will otherwise eat the cluster. Numbers: a 256–4K GPU cluster; utilization target >70–75% (lower burns money, higher starves queues); track queue wait time by priority as the user-facing SLO. Failure modes: fragmentation (bin-packing + packing small jobs onto big-job leftovers), checkpoint I/O storms on mass preemption (rate-limit, tier to warm object storage), spot-reclaim cascades, gang deadlocks, noisy neighbors on shared nodes.

- Model deployment and versioning
  - **A:** Version three artifacts together as one deployable bundle: model weights, prompts, and retrieval/index config — most production regressions are prompt edits, not weight changes, and every trace must pin the bundle ID for reproducibility. Progression: shadow deployment first (mirror 100% of live traffic to the new version with zero user exposure; compare outputs, latency, and eval scores on the real distribution — this catches eval-set/prod drift that offline evals miss) → canary 1% → 5% → 25% → 100%, 30–60 minutes per step, with automated rollback gates: p99 latency, error/refusal rate, cost per query, and a faithfulness/quality score from 1–5% online LLM-judge sampling dropping beyond ~2–3 standard deviations → rollback is a traffic flip back to the warm previous bundle. A/B tests answer preference questions (does the new answer style convert better?) with fixed horizons or proper sequential testing — LLM non-determinism inflates false positives if you peek early. Failure modes: silent prompt drift (diff prompts in CI like code), eval–prod distribution gap, unlogged versions making incidents unreproducible, and canary routing bugs (route by stable user hash, not round-robin).

- Feature store for AI
  - **A:** Two serving planes over one feature definition (Feast/Tecton pattern). Offline: a lakehouse (Parquet/Iceberg) where every feature row carries its computation timestamp; training-set builds use as-of joins so a label at time T sees only features that existed before T — point-in-time correctness is the sole real defense against label leakage, the silent killer that yields great offline metrics and a dead model online. Online: Redis/DynamoDB serving precomputed features at p99 <10ms. Freshness per feature by information decay: batch features hourly/daily, streaming features via Flink/Kafka in seconds. Skew prevention: one transformation library shared by training and serving; compute-on-demand for complex derivations, precompute-and-lookup for hot features; monitor online-vs-offline distribution divergence (PSI) per feature and alert before it moves business metrics. Numbers: millions of entities, thousands of features, backfills over years of history in hours. Failure modes: leakage (as-of join bugs — audit training sets for future-dated features), dual implementations drifting apart, freshness lag degrading models silently (feature-age monitors), NaN-default semantics encoding fake signal, and entity-key mismatches (user_id vs device_id joins) between planes.

---

## Expectations by Seniority

| Seniority | What's Expected | What's Not Expected |
|-----------|----------------|-------------------|
| Junior (0–2 years) | Clear architecture, identify key components, basic trade-offs | Deep cost analysis, multi-region deployment, advanced safety |
| Mid (2–5 years) | Detailed architecture, specific technology choices, cost estimation, evaluation strategy | Multi-system orchestration, advanced agent design |
| Senior (5–8 years) | Production-grade design, failure modes, monitoring, cost optimization, safety guardrails, team impact | — |
| Staff+ (8+ years) | Multi-system architecture, organizational impact, build vs. buy decisions, technical strategy | — |

---

## AI System Design vs Traditional vs ML System Design

| Dimension | Traditional System Design | ML System Design | AI System Design |
|-----------|--------------------------|------------------|------------------|
| **Core question** | How to serve data reliably? | How to train and serve a model? | How to build a system with LLMs at the center? |
| **Primary constraint** | Availability, consistency | Model accuracy, data quality | Non-determinism, cost, safety |
| **Data flow** | Request → DB → Response | Features → Model → Prediction | Query → Retrieval + Context → LLM → Response |
| **Scaling** | Horizontal scaling, caching | Model serving, feature store | Token throughput, context management, caching |
| **Evaluation** | SLA, latency p99 | Precision, recall, F1 | Faithfulness, relevance, safety scores |
| **Failure mode** | Server down, data corruption | Model drift, feature staleness | Hallucination, prompt injection, cost overrun |
| **Cost model** | $/request (infrastructure) | $/training run + $/prediction | $/token (inference) + $/embedding + $/storage |
| **Monitoring** | Uptime, error rate | Model metrics, feature drift | Hallucination rate, cost per query, user satisfaction |
| **Safety** | Auth, encryption | Fairness, bias | PII leakage, prompt injection, harmful output |
| **Iteration speed** | Deploy new code | Retrain model (days–weeks) | Update prompt (minutes), swap model (hours) |

---

## How to Prepare: 5-Step Structure

When you get an AI system design question, follow this structure:

### Step 1: Clarify Requirements (5 min)

- What are the functional requirements? (What should the system do?)
- What are the non-functional requirements? (Latency, cost, accuracy, safety)
- Who are the users? What's the scale?
- What are the safety/compliance constraints?
- **AI-specific**: What's the acceptable hallucination rate? What's the cost per query budget?

### Step 2: Define the AI/Non-AI Boundary (5 min)

- Which parts of the system need LLM/AI? Which can be traditional software?
- Where are the AI "hot spots" (where non-determinism enters the system)?
- What's the fallback when the AI component fails or degrades?

### Step 3: Design the AI Pipeline (15 min)

- **Retrieval**: How do you get context? (RAG, tools, knowledge graph, hybrid)
- **Generation**: Which model? What prompt architecture? What's the context window strategy?
- **Evaluation**: How do you evaluate outputs in real-time? What's the fallback?
- **Guardrails**: Input validation, output filtering, content policy, PII handling
- **Caching**: What can you cache? Semantic cache? Prompt cache?

### Step 4: Design the Infrastructure (10 min)

- API layer, load balancing, rate limiting
- Database choices (vector DB, relational, cache)
- Monitoring and observability (LangSmith, Arize, custom)
- Cost management (token budgets, model tiering, caching)
- Deployment (model versioning, A/B testing, rollback)

### Step 5: Discuss Trade-offs and Alternatives (10 min)

- Cost vs. quality (cheaper model + more context vs. expensive model + less context)
- Latency vs. accuracy (streaming, speculative decoding, model tiering)
- Build vs. buy (open-source model vs. API, custom vs. managed vector DB)
- Safety vs. capability (guardrail strictness vs. model flexibility)
- What would change at different scales?

---

## 4 Repeatable Patterns

Most AI system design questions map to one of these patterns:

### Pattern 1: RAG
**Applies to**: Document Q&A, knowledge assistants, search engines, customer support bots

Key design decisions:
- Chunking strategy (fixed, semantic, recursive)
- Embedding model selection
- Vector DB choice (Pinecone, Weaviate, Qdrant, pgvector)
- Retrieval strategy (dense, sparse, hybrid, re-ranking)
- Context window management
- Citation/attribution implementation
- Evaluation methodology

### Pattern 2: Feedback and Reinforcement
**Applies to**: Recommendation systems, personalization, content ranking, ad targeting

Key design decisions:
- Feedback signal collection (implicit vs. explicit)
- How to incorporate feedback (prompt adjustment, fine-tuning, DPO)
- Cold start handling
- Evaluation (offline vs. online, A/B testing)
- Bias and fairness considerations

### Pattern 3: Hallucination Mitigation
**Applies to**: Medical AI, legal AI, financial AI, any high-stakes domain

Key design decisions:
- Grounding strategy (retrieval, knowledge graph, constrained generation)
- Verification pipeline (self-consistency, entailment, retrieval verification)
- "I don't know" threshold calibration
- Citation and attribution
- Human-in-the-loop design
- Monitoring and alerting for hallucination spikes

### Pattern 4: Scalability and Cost
**Applies to**: Consumer-facing AI, high-volume API services, enterprise deployments

Key design decisions:
- Model tiering (route to cheapest adequate model)
- Caching strategy (semantic cache, prompt cache, response cache)
- Token budget management
- Batch vs. real-time processing
- GPU utilization optimization
- Multi-region deployment for latency

---

## What Companies Build

Understanding what companies actually build helps you anticipate their system design questions:

| Company | AI Systems They Build | Likely Design Questions |
|---------|----------------------|------------------------|
| **Doctolib** | Medical document Q&A, appointment assistant | Design a medical RAG system with safety constraints |
| **Uber** | ETA prediction, fraud detection, customer support AI | Design a real-time fraud detection system with LLM reasoning |
| **Airbnb** | Listing description generation, search ranking, host assistant | Design an AI co-pilot for Airbnb hosts |
| **Perplexity** | AI search engine with citations | Design a Perplexity-like search engine |
| **Slack** | AI message summarization, search, workflow automation | Design an AI summarization feature for team channels |
| **LinkedIn** | Job matching, content recommendation, profile optimization | Design an AI-powered candidate sourcing system |
| **Anthropic** | Safety-focused AI assistants, API platform | Design an AI system with safety guarantees |
| **DoorDash** | Order prediction, menu optimization, support chatbot | Design a real-time AI order prediction system |
| **Spotify** | Playlist generation, music discovery, podcast summarization | Design an AI-powered music discovery system |
| **Notion** | AI writing assistant, database Q&A, search | Design a unified query engine for structured and unstructured data |

---

## Common Mistakes

1. **Treating the LLM as a black box.** Interviewers want to see you understand what happens inside — context management, token costs, latency characteristics.

2. **Ignoring cost entirely.** In 2026, cost is a first-class design constraint. Not discussing cost signals you haven't built production AI systems.

3. **Over-engineering the retrieval.** Starting with a complex hybrid retrieval + re-ranking + knowledge graph pipeline when simple semantic search would suffice. Start simple, then add complexity with justification.

4. **No evaluation strategy.** If you can't evaluate the AI component, you can't improve it. Always include evaluation in your design.

5. **Forgetting the non-AI parts.** The database, the API layer, the authentication, the monitoring — these still matter and interviewers will notice if you skip them.

6. **No fallback plan.** What happens when the LLM is down? When latency spikes? When cost exceeds budget? Production systems need graceful degradation.

7. **Ignoring safety.** Even if the interviewer doesn't mention safety, bring it up. PII handling, prompt injection defense, and content policy are now table stakes.

8. **Not asking clarifying questions.** Jumping into design without clarifying requirements wastes time and signals poor communication.

9. **Designing for the wrong scale.** Ask about scale early. Designing for 10M users when the system will serve 10K users (or vice versa) shows poor judgment.

10. **No diagram.** System design requires visual communication. If you're not drawing, you're not communicating effectively.

---

## Sources

[^1]: "Designing LLM Applications", Eugene Yan, 2024–2025.
[^2]: "Machine Learning System Design Interview", Ali Aminian and Alex Xu, 2024.
[^3]: "Building LLM Apps", Valentina Alto, 2024.
[^4]: Interview reports from Blind, Glassdoor, and LeetCode Discuss, 2025–2026.
[^5]: Company engineering blogs: Doctolib, Uber, Airbnb, Perplexity, Slack, LinkedIn, Anthropic, DoorDash, Spotify, Notion — 2024–2026.
[^6]: "RAG Systems in Production", LangChain State of AI Engineering Survey, 2025.
[^7]: "AI System Design Patterns", emerging community resources, 2025–2026.
[^8]: "Cost Optimization for LLM Applications", OpenAI and Anthropic best practices, 2025.
[^9]: "Hallucination Mitigation in Production AI Systems", various industry reports, 2025.

---

> **Next**: [Behavioral Questions →](05-behavioral.md)
