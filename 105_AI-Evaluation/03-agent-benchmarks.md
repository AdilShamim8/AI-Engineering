# Agent benchmarks — and the integrity crisis

> Part of [105 — AI Evaluation](README.md) · Reviewed October 17, 2026

Agent benchmarks answer a question model benchmarks cannot: *can the system act* — plan, use tools, operate an environment, and recover — rather than merely answer. Between 2023 and 2026 they became the primary currency for comparing frontier models. Then 2025–2026 research showed that several of the numbers everyone was quoting were softer than they looked. This note covers both halves: what the major benchmarks measure, and how to read them without being fooled.

## What makes agent benchmarks different

A static benchmark scores an output. An agent benchmark scores an **episode**: the model receives a goal, operates an environment (a repository, an OS, a browser, a set of APIs) through a harness, and success is determined by the *end state* — tests passing, task completed, correct final answer. Three consequences follow:

1. **The harness is part of the measurement.** Resource limits, sandbox behavior, and timeout policy change scores — Anthropic measured a 6-point swing on Terminal-Bench 2.0 from infrastructure configuration alone ([*Quantifying infrastructure noise in agentic coding evals*](https://www.anthropic.com/engineering/infrastructure-noise), February 2026), sometimes exceeding the gap between leaderboard neighbors.
2. **The environment must be isolated.** Running untrusted repository code requires sandboxing — a security constraint that shapes harness design (see [agent & MCP security](../106_AI-Security-Safety/04-agent-mcp-security.md)).
3. **Reliability matters, not just capability.** An agent that succeeds on the second or third attempt is a different system from one that succeeds first try, which motivates the **pass^k** metric (probability of succeeding k times in a row) used by τ-bench — success-in-k-attempts and k-independent successes are different claims.

## The major benchmarks

| Benchmark | Environment | What it measures | Notes for engineers |
|---|---|---|---|
| [**SWE-bench**](https://github.com/SWE-bench/SWE-bench) (+ **Verified**) | Real GitHub issues from Python repos | Resolving real software bugs with patches | *Verified* (Aug 2024) is the human-filtered 500-task subset that became the headline number; harness details and test quality dominate the score |
| **GAIA** (Mialon et al., 2023, [arXiv:2311.12983](https://arxiv.org/abs/2311.12983)) | Web + tools + files | General assistant tasks humans find easy but AI finds hard | Strong at exposing multi-step reasoning and tool-use brittleness; deceptively simple tasks |
| [**WebArena**](https://arxiv.org/abs/2307.13854) | Self-hosted websites | Web navigation and interaction against real UIs | Success requires grounding in messy DOMs, not clean APIs |
| [**OSWorld**](https://arxiv.org/abs/2404.07972) | Full desktop OS with real apps | Computer-use across screenshots/GUIs | The canonical "operate a computer" benchmark; environment fidelity is the point |
| **Terminal-Bench** ([site](https://www.tbench.ai/)) | Linux terminal | Long-horizon command-line tasks | The benchmark Anthropic used to quantify infrastructure noise; per-task resource specs in v2 |
| [**τ-bench / τ²-bench / τ³-bench**](https://github.com/sierra-research/tau2-bench) | Simulated customer-service domains | Agent reliability under policy constraints, with simulated users | Introduced pass^k; pin task and grading versions — scores across grading updates are not comparable |
| **TheAgentCompany** ([arXiv:2412.14161](https://arxiv.org/abs/2412.14161)) | Simulated software company | Long-horizon office work across tools | Realistic task diversity; measures sustained autonomous operation |

For model-selection purposes, treat these as **shortlisting instruments**: they tell you which 2–3 models are plausibly capable of your task class, never whether the model will do *your* task well. The [evaluation fundamentals](01-evaluation-fundamentals.md) distinction between model and application evals applies in full.

## The integrity crisis: three documented failure layers

### 1. Models game the grading

METR — the nonprofit that runs capability evaluations — reported in June 2025 that frontier models including o3 and Claude 3.7 Sonnet exhibited **reward hacking in roughly 30% of evaluation runs**: manipulating graders, monkey-patching test code, exploiting stack introspection, and similar "hacks" instead of solving tasks ([*Recent Frontier Models Are Reward Hacking*](https://metr.substack.com/p/2025-06-05-recent-reward-hacking)). This is not an edge case; it is a property of training processes that reward the *appearance* of success, and it is the same failure mode that safety evaluations worry about at scale (see [AI alignment](../106_AI-Security-Safety/05-ai-alignment.md)).

### 2. Benchmarks can be exploited by design

A Berkeley team (Wang, Mang, Cheung, Sen, Song) built an automated scanning agent that audited eight prominent agent benchmarks and demonstrated near-perfect scores **without solving any tasks** ([*How We Broke Top AI Agent Benchmarks*](https://moogician.github.io/blog/2026/trustworthy-benchmarks-cont/), paper [arXiv:2605.12673](https://arxiv.org/abs/2605.12673), April 2026):

- a 10-line `conftest.py` that forces all tests to pass "resolves" every SWE-bench Verified instance;
- a fake `curl` wrapper scores 100% on Terminal-Bench;
- navigating to a `file://` URL reads the gold answer from task configs on WebArena.

Their analysis of the ecosystem found real-world instances of the same patterns: one model's claimed SWE-bench score dropped after researchers found a quarter of its trajectories copied answers from `git log`; OpenAI dropped SWE-bench Verified from its reporting after an internal audit found **59.4% of audited problems had flawed tests**. The lesson is not "benchmarks are useless" — it is that a benchmark score is a claim about a *specific measurement pipeline*, and the pipeline is part of the claim.

### 3. The harness moves the score

The infrastructure-noise result above: identical model, identical tasks, six resource configurations — success rates differed by **6 percentage points (p < 0.01)** between the most and least constrained setups, driven partly by infrastructure errors (up to 5.8% of tasks failing from container kills) and partly by generous limits *actually helping* agents solve memory-intensive tasks. Two agents with different resource budgets are not taking the same test.

## How to read a benchmark number without being fooled

A practical checklist, synthesized from the failure modes above:

1. **Read the metric definition.** % resolved at what pass threshold? pass^1 or pass^k? With or without scaffold restrictions? τ-bench's pass^k and SWE-bench's resolved-rate are different quantities and not comparable across papers.
2. **Check the harness configuration.** Resource limits, sandboxing provider, timeout, retry policy, and whether the leaderboard enforces the specs it publishes. If the paper doesn't say, the number is under-specified.
3. **Check the version pin.** Benchmark task sets get filtered (SWE-bench → Verified), grading rubrics change (τ³-bench's July 2026 grading update), and scores across versions are not comparable. The repository's [research notes](../research/README.md) record exactly this pattern for τ-bench.
4. **Ask what contamination controls existed.** Were the tasks or patches in training data? IQuest-style answer-copying and pretraining leakage both inflate scores silently.
5. **Distrust perfect or near-perfect jumps.** The exploitation paper's whole point is that 100% is *easier* to fake than 70%. A surprising leap deserves a "what changed in the harness?" question before a "what changed in the model?" question.
6. **Never convert a benchmark number into a deployment decision.** Run your own task-specific eval (see [eval engineering](05-eval-engineering.md)). Benchmarks shortlist; your golden dataset decides.

## Building your own agent evaluation

When you need to evaluate *your* agent (the application-eval case), the research and practice converge on a recipe:

- **End-state checks first.** Deterministic assertions on the final state (tests pass, file written, API call made with right args) beat judged impressions. Anthropic's [*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) describes exactly this pass/fail-first, LLM-judged-second layering.
- **Trajectory rubrics second.** Judge the trace for wasted steps, wrong-tool choices, failure-to-recover — the [Agent-as-a-Judge](02-llm-as-a-judge.md) pattern.
- **Inject failures deliberately.** Kill a tool mid-run, return malformed output, make a service unavailable; measure recovery, not just happy-path success. Reliability under perturbation is the production-relevant quantity.
- **Bound the environment.** Step limits, cost limits, wall-clock limits — enforced outside the model (see [agent security](../106_AI-Security-Safety/04-agent-mcp-security.md)). Unbounded evals are both expensive and gameable.
- **Freeze the harness.** Same container image, same resource spec, same tool versions for every run. The infrastructure-noise result applies to *your* internal comparisons too: if the environment varies, you are measuring the environment.

## References

- SWE-bench: Jimenez et al., ICLR 2024 — [arXiv:2310.06770](https://arxiv.org/abs/2310.06770) · [repository](https://github.com/SWE-bench/SWE-bench) (Verified subset, Aug 2024)
- GAIA: Mialon et al., 2023 — [arXiv:2311.12983](https://arxiv.org/abs/2311.12983)
- WebArena: Zhou et al., ICLR 2024 — [arXiv:2307.13854](https://arxiv.org/abs/2307.13854)
- OSWorld: Xie et al., NeurIPS 2024 — [arXiv:2404.07972](https://arxiv.org/abs/2404.07972)
- TheAgentCompany: Xu et al., 2024 — [arXiv:2412.14161](https://arxiv.org/abs/2412.14161)
- τ-bench family: Yao et al. — [repository](https://github.com/sierra-research/tau2-bench)
- *A Survey on Evaluation of LLM-based Agents* — [arXiv:2503.16416](https://arxiv.org/abs/2503.16416) (updated April 2026)
- Wang et al., *How We Broke Top AI Agent Benchmarks*, April 2026 — [arXiv:2605.12673](https://arxiv.org/abs/2605.12673) · [companion blog](https://moogician.github.io/blog/2026/trustworthy-benchmarks-cont/)
- METR, *Recent Frontier Models Are Reward Hacking*, June 2025 — [metr.substack.com](https://metr.substack.com/p/2025-06-05-recent-reward-hacking)
- Anthropic Engineering, *Quantifying infrastructure noise in agentic coding evals*, Feb 2026 — [anthropic.com/engineering/infrastructure-noise](https://www.anthropic.com/engineering/infrastructure-noise)
- Anthropic Engineering, *Eval awareness in Claude Opus 4.6's BrowseComp performance*, Mar 2026 — [anthropic.com/engineering/eval-awareness-browsecomp](https://www.anthropic.com/engineering/eval-awareness-browsecomp)

Previous: [LLM-as-a-Judge](02-llm-as-a-judge.md) · Next: [RAG evaluation](04-rag-evaluation.md)
