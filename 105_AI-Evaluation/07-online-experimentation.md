# Online evaluation and experimentation: testing where the users are

> Part of [105 — AI Evaluation](README.md) · Reviewed October 27, 2026

Offline evals answer "did this change make the system better on cases I chose?" — and they can't, even in principle, answer "does it work for the users we actually have?" The distribution gap between your golden set and production traffic, the behavior of real people (who rephrase, rage-click, and leave), and the slow drift of the world are all invisible offline. This note covers the online half: experiment designs (A/B, interleaving, shadow, canary), the metric taxonomy (captured vs computed), judge-in-the-loop production eval, and the statistical hygiene that separates trustworthy results from plausible ones.

The [course's lecture 6](course/06-offline-vs-online-evals.md) draws the offline/online boundary, and [lecture 19](course/19-online-eval-langsmith-monitoring.md) builds the online loop hands-on with LangSmith; [104 — LLMOps](../104_LLMOps/README.md) owns the observability machinery. This note is the reference beneath both.

## The handoff: what each half can see

| Question | Offline eval | Online eval |
|---|---|---|
| Did the prompt change break faithfulness? | ✅ golden-set regression | ➖ (only via sampled judging) |
| Is the system good *for our actual traffic mix*? | ➖ (golden ≠ traffic) | ✅ |
| Do users *like* the new answer style? | ❌ | ✅ (captured signals) |
| What's the P95 latency under real concurrency? | Approximation only | ✅ |
| Is a fix worth shipping before exposure? | ✅ | ❌ (can't run pre-launch) |
| Cost of a single data point | Judge tokens, seconds | Real user sessions, days |

The pattern that works: **offline filters, online confirms.** Never A/B test a change your golden suite already flags; never ship on green offline scores alone when the change touches UX. [Lecture 19](course/19-online-eval-langsmith-monitoring.md) closes the loop further — production traces that fail online judging get promoted back into the golden set, so next quarter's offline suite contains this quarter's incidents.

## Experiment designs

### A/B testing — the workhorse

Randomize *units*, not requests. For LLM applications the unit choice matters more than in classic web experiments because a single user generates many requests and answers within a session are correlated (same persona, same topic, same annoyance):

- **User-level** randomization — cleanest inference, but needs stable user IDs and enough users; wrong for anonymous-heavy products.
- **Session-level** — the usual right answer for chat: one session sees one variant end-to-end, session-level metrics (resolved-without-escalation, thumbs rate per session) are well-defined, and contamination is contained.
- **Request-level** — maximizes sample size and destroys it: interleaved variants inside one conversation confuse the user and violate consistency; only acceptable for stateless, single-shot endpoints (e.g., a reranking toggle behind an API).

**Power analysis, worked.** Detecting a 2-percentage-point lift on a 70% baseline (satisfaction-style binary metric) at 80% power and α=0.05 needs roughly ~8,000 users per arm — the two-proportion sample size, a number worth re-deriving rather than trusting, because traffic volume determines which effects are *measurable at all* this quarter. When your traffic is 10× smaller than the requirement, the options are: measure a bigger effect, run longer, use interleaving, or accept that the decision is judgment-based and say so.

Design hygiene:

- **Guardrail metrics** — the metrics that must not move (latency P95, cost/query, refusal rate, escalation rate). An experiment can win its primary metric by being sycophantic and still be a bad ship.
- **Novelty and primacy effects** — new answer *styles* score differently in week 1 vs week 4; run long enough to see the plateau or state that you didn't.
- **One primary metric declared before launch** — the "we'll see what wins" experiment reliably finds a winner by chance among 20 metrics.

### Interleaving — 5–10× more efficient for comparisons

Instead of splitting users into arms, **each user sees both systems' answers merged** — team-draft style: for each request, a fair coin picks which system answers first; the "draft" alternates. Users implicitly choose by engaging (copying, upvoting, continuing on one branch), and the per-user preference aggregation cancels user-level heterogeneity — the same reason interleaving beat A/B for search ranking a decade ago.

- **Where it works for LLMs**: comparing two generation configs on answer quality where a merged or alternating presentation is tolerable (side-by-side or alternating turns).
- **Where it doesn't**: anything where the *system's* behavior must be internally consistent across a session (tool-use agents, personalization), latency comparisons, cost comparisons, and any metric that depends on the user experiencing one coherent product.
- **The canonical large-scale relative** is [Chatbot Arena](https://lmarena.ai) — pairwise human preference at scale, whose Elo-style ratings ([arXiv:2403.04132](https://arxiv.org/abs/2403.04132)) are effectively the industry's model-selection online eval. Its lesson transfers: preference *pairs* are dramatically easier for humans to produce than absolute scores.

### Shadow deployment — test without exposure

The new pipeline receives duplicated production traffic; users still see only the current system's output. What shadowing measures honestly: **latency under real load, error rates, cost per query, and judge-scored quality of the new outputs** (via sampled LLM judging of the shadow responses). What it cannot measure: anything about user behavior — no clicks, no satisfaction, no retention, because no user ever sees the shadow. Shadow → canary → A/B is the standard risk ladder: shadow first for engineering metrics, canary for early exposure with rollback, A/B for the behavioral claim.

### Canary / gradual rollout

1% → 5% → 25% → 100%, with **pre-registered automatic rollback triggers** (latency P95 budget, error rate, safety-metric threshold, cost ceiling). The engineering discipline is in the triggers: they must be computed fast enough to fire within a rollout stage, and the rollback must be tested, not assumed. Canary is a risk-reduction technique, not an inference technique — a 1% stage can't detect small quality changes; it exists to catch catastrophic ones.

> 💡 **Expert commentary — pick the design from the claim you need to make.** The unifying decision table: *engineering claim* (nothing broke) → shadow + canary; *relative quality claim* (A better than B) → interleaving if presentation permits, else A/B; *absolute behavior claim* (users are more satisfied) → A/B with session-level randomization and power analysis; *no measurable claim possible* (traffic too low) → judgment + offline evals, stated as such. Most org dysfunction in this space is a traffic problem disguised as a design problem — teams A/B test because it's the design they've heard of, on user volumes where the honest answer is "we cannot know yet."

## The online metric taxonomy

### Captured signals — what users tell you, unprompted

Thumbs up/down, regenerate clicks, copy-button presses, explicit escalation to a human, session length, retention proxies, edit distance on regenerated answers. Two properties to hold in mind:

- **Selection bias is severe**: unhappy users click; content users leave silently. Absolute rates are uninterpretable; *changes* in rates under randomization are the usable signal.
- **The metric can be gamed by the system**: optimizing thumbs-up produces sycophancy — longer, more agreeable, more confident answers that score well and serve users worse. This is Goodhart applied to UX, and it's why guardrail metrics (task completion, escalation rate, retention) must ride alongside any engagement primary.

### Computed signals — what you measure yourself

Latency percentiles (TTFT and total), tokens, cost per query, cache hit rates, refusal rates, tool-call failure rates — and, the interesting one, **online quality via sampled LLM judging** (below). Captured signals tell you users reacted; computed signals tell you why. The debugging loop almost always runs computed → captured: "satisfaction dropped Tuesday" → "faithfulness on sampled traces dropped Tuesday" → "the retrieval index re-built Monday night."

### Pairing discipline

Report captured with computed or not at all. A satisfaction drop with no quality movement is a UX bug; a quality drop with no satisfaction movement is a metric calibration problem; both together are a regression you can act on.

## Judge-in-the-loop: LLM-as-a-judge on production

The pattern from [lecture 19](course/19-online-eval-langsmith-monitoring.md): sample a fraction of production traces, run the same judges you use offline (faithfulness, relevance, toxicity), and alert on drift.

- **Sampling rate vs cost**: 100% sampling of 500 traces/day × ~3 judge metrics is ~1,500 judge calls/day — affordable; 100% of 500k traces/day is not, and 1–5% sampling with stratified oversampling of low-confidence or high-severity slices is the standard compromise. Rare-event detection (a new jailbreak family appearing 50 times in 500k traces) needs dedicated keyword/anomaly lanes, not uniform sampling.
- **The same-evaluator golden rule** (lecture 19): when comparing online scores to your offline suite, the judge prompt, judge model, and thresholds must be identical, or the deltas you see are instrumentation, not system.
- **Alert on the judge's drift too**: judges are part of the measurement chain; a judge-model silent update can move your "quality" number while nothing changed in production. Pin judge versions; treat judge changes as requalification events ([eval engineering](05-eval-engineering.md)).

> 💡 **Expert commentary — online judging is an instrument, and instruments drift.** The three drifts — input distribution (traffic changes), system behavior (your own deploys), and judge behavior (provider updates) — are separable only if you log enough to attribute: version pins on system *and* judge, plus a frozen golden set run weekly through the same online judge as a control chart. That control-chart run is the cheapest possible answer to "did quality drop, or did our ruler change?" — and almost nobody runs it.

## Statistical hygiene

- **Multiple comparisons**: an experiment reading 20 metrics will find ~1 "significant" winner by chance at α=0.05. Pre-register the primary; treat the rest as exploratory (Bonferroni or Benjamini–Hochberg if you must formalize).
- **Peeking and early stopping**: checking daily and stopping at the first significant day inflates false positives dramatically. Use fixed horizons, or group-sequential/always-valid inference (alpha spending, mSPRT) if early stopping is genuinely needed.
- **Simpson's paradox**: aggregate wins can hide segment losses — the new prompt wins on English traffic and loses on Hindi; if your traffic mix shifts mid-experiment, the aggregate flips. Segment by the dimensions you'd act on (language, intent, plan tier) with enough per-segment n to matter.
- **Minimum detectable effect as a design input**: choose the effect size that would change your decision, then power for it; if the required n exceeds a quarter's traffic, the experiment as designed is not the tool — say so before, not after.
- **Interference between arms** (rare but real): if variant B's users generate content that variant A's users retrieve (community RAG), user-level randomization leaks; cluster randomization is the fix.

## Failure modes worth remembering

- **Sycophancy gaming**: thumbs-rate optimization producing longer, more confident, less correct answers — caught only by guardrail task metrics.
- **The underpowered win**: a "significant" 1-point lift at n=900/arm that was really α-spending across weeks of peeking; shipped, no effect, months of confusion.
- **Metric-target contamination**: training or prompt-tuning on the feedback signal the experiment measures — the experiment stops measuring the product and starts measuring the feedback loop.
- **Judge-version roulette**: an unannounced provider update to the judge model moved online faithfulness 4 points overnight; the war room lasted two days; the fix was the weekly control-chart run (above).

## Decision framework

| You need to claim… | Traffic | Design |
|---|---|---|
| "Nothing broke" (latency/errors/cost/safety) | Any | Shadow → canary with rollback triggers |
| "A > B on answer quality" | Low–medium | Interleaving (if presentation permits) |
| "A > B" (can't interleave) | Medium+ | Session-randomized A/B, one primary metric, power analysis |
| "Users are better off" | High | A/B on behavioral primary + guardrails + 4-week horizon |
| Anything, on low traffic | Low | Offline suite + judgment; state the epistemic status honestly |

## Cross-references

- [Eval engineering](05-eval-engineering.md) — the release gates online results feed back into
- [LLM-as-a-Judge](02-llm-as-a-judge.md) — the judge machinery running on sampled traces
- [Evaluation dataset engineering](06-evaluation-datasets.md) — where promoted production traces land
- Course lectures: [06 — offline vs online](course/06-offline-vs-online-evals.md) · [19 — LangSmith monitoring](course/19-online-eval-langsmith-monitoring.md)
- [104 — LLMOps](../104_LLMOps/README.md) — tracing, observability, and the infrastructure this runs on

<!-- nav-footer -->
---

**Navigate:** [← 06. Evaluation Datasets](06-evaluation-datasets.md) · [Section hub](README.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
