# LLM-as-a-Judge

> Part of [105 — AI Evaluation](README.md) · Reviewed October 17, 2026

Using one model to grade another's outputs is the industry's workhorse technique for measuring semantic quality at scale. It is also a measurement instrument with documented biases that must itself be evaluated. This note covers what the research established, the failure modes, and the engineering discipline — judge calibration — that makes the technique trustworthy.

## Where it came from: MT-Bench and the founding result

The technique was formalized in *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (Zheng et al., NeurIPS 2023 Datasets & Benchmarks Track, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)). The paper introduced:

- **MT-Bench** — 80 multi-turn questions designed to be open-ended enough that exact-match metrics fail, and
- **Chatbot Arena** — the crowdsourced head-to-head comparison platform that evolved into today's LMArena.

The headline finding: **GPT-4 as judge agreed with human preferences at over 80% — roughly the same level of agreement humans reach with each other.** That single result is what licensed the field to use model-graded metrics for open-ended tasks where nothing else scales.

The same paper also did the field the favor of documenting the judge's biases at birth (next section), which is why "LLM-as-a-judge is biased" is not a critique of the technique but part of its operating manual.

Since then the literature has grown into a research area of its own — the survey by Gu et al. ([arXiv:2411.15594](https://arxiv.org/abs/2411.15594), revised through October 2025) catalogs the biases, mitigation techniques, and application domains — and practitioner tooling ([DeepEval](https://github.com/confident-ai/deepeval), [promptfoo](https://github.com/promptfoo/promptfoo), [Ragas](https://github.com/vibrantlabsai/ragas), Langfuse, Arize Phoenix) has made judge-based metrics a default component of eval suites.

## The documented biases

| Bias | What it looks like | Standard mitigation |
|---|---|---|
| **Position bias** | In A-vs-B comparison, the judge prefers whichever answer is presented first | Swap order and average; report disagreement rate |
| **Verbosity bias** | Longer answers score higher at equal quality | Length-controlled scoring (the fix used by [Length-Controlled AlpacaEval](https://arxiv.org/abs/2404.04475), Dubois et al., COLM 2024); penalize length deltas |
| **Self-enhancement bias** | Judges rate outputs from their own model family higher | Use a *different* strong model as judge than the one being tested |
| **Style/authority bias** | Confident tone, markdown formatting, and citations win points independent of substance | Rubrics that score substance; blind formatting; adversarial calibration pairs |
| **Sycophancy / agreement bias** | Judges over-reward answers that flatter the question's framing | Include counterfactual cases in calibration set |

Two structural failure modes sit above these: **judge knowledge limits** (the judge cannot verify claims outside what it can check from the provided context — so give it the sources) and **judge prompt sensitivity** (the same rubric reworded can shift scores; version judge prompts like code).

## Judge calibration: the engineering discipline

An uncalibrated judge score is a number; a calibrated one is a measurement. The calibration protocol, distilled from the survey literature and practitioner guidance:

1. **Build a human-labeled calibration set** — 50–200 cases sampled from your actual task distribution, labeled by people, kept separate from anything used to develop the judge prompt. Include the slices where judges are known to wobble: very long answers, refusal formats, sparse answers.
2. **Measure agreement, overall and per slice.** Report agreement with humans under *your actual rubric* — Cohen's kappa or percent agreement, plus a per-slice breakdown. There is no universal "85% agreement makes it valid"; the threshold depends on what the metric gates.
3. **Fix the top disagreement causes, then re-measure.** Rubric wording, context provided to the judge, output schema, position swapping. Iterate against the *fixed* calibration set; do not tune and test on the same cases.
4. **Operationalize the judge like any model call.** Pin judge model version, temperature (0), and prompt hash. Record parse failures separately from low scores — an unparseable judgment is not a zero.
5. **Re-calibrate when anything changes.** New judge model, new judge prompt, new domain slice appearing in traffic. Calibration decays silently; schedule the re-check.

LangChain's [*How to calibrate LLM-as-judge with human corrections*](https://www.langchain.com/resources/llm-as-a-judge) (March 2026) is a good practitioner walkthrough of step 3 in particular.

## Rubric design: what the judge prompt should contain

A production judge prompt is a measurement instrument, not a conversation:

- **The construct definition** — one sentence, matching the written spec from [evaluation fundamentals](01-evaluation-fundamentals.md).
- **The evidence** — the question, the retrieved context (for groundedness), reference materials, and the candidate answer(s). For factuality, the judge needs sources; without them it judges plausibility, not truth.
- **A scoring scale with anchors** — "2 = all claims supported by the provided context; 1 = most claims supported, minor unsupported additions; 0 = fabricates or contradicts the context." Anchored scales beat 1–10 vibes.
- **Output schema** — machine-parseable JSON with score and a one-line rationale. The rationale is for your debugging, not for the score's defense.
- **Anti-bias instructions where cheap** — "length is not quality" — while remembering that instructions mitigate biases only partially; the structural mitigations (order swapping, different-family judges) do the real work.

## Pairwise vs pointwise; single vs panel

- **Pointwise** scoring (grade each answer independently) is stable and parallelizable but drifts with judge version — good for regression suites.
- **Pairwise** comparison (A vs B) is more reliable for detecting small quality deltas but suffers position bias — always swap and average.
- **Judge panels** (multiple judges, majority or mean) reduce single-model idiosyncrasy at multiplied cost; worth it for release-gating metrics, overkill for exploratory sweeps.

## Agent-as-a-Judge: judging trajectories, not just answers

The newest branch of the field extends judging from outputs to *agent behavior*: scoring the trajectory — plan quality, tool selection, step efficiency, recovery from errors — rather than only the final answer. The survey by You et al. ([arXiv:2601.05111](https://arxiv.org/abs/2601.05111)) frames the design space. In practice this means the judge receives the full trace (user goal, steps, tool calls and results, final state) and scores dimensions like "were any tool calls unnecessary?" or "did the agent notice the failure and recover?" This connects directly to [agent benchmark](03-agent-benchmarks.md) measurement and to the trace-evaluation survey ([arXiv:2606.04990](https://arxiv.org/abs/2606.04990)).

Anthropic's engineering posts on agent evals ([*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), January 2026; [*Effective harnesses for long-running agents*](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), November 2025) describe the production version of this: pass/fail end-state checks plus LLM-graded rubrics over transcripts, with infrastructure that keeps long-running evals cheap and reproducible.

## What LLM-as-a-judge must never be used for

- **Self-verification.** A model grading its own output to "prove" correctness is circular; at minimum use a different model family, ideally verify claims against retrieved sources instead.
- **Compliance or safety sign-off on its own.** Judge scores feed the decision, but safety determinations need the adversarial testing of [red teaming](../106_AI-Security-Safety/03-red-teaming.md) and the human accountability of [governance](../106_AI-Security-Safety/06-responsible-ai.md).
- **Un-bounded leaderboarding.** Comparing two *different* systems with a judge whose calibration you only established for one of them.

## References

- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023 — [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)
- Gu et al., *A Survey on LLM-as-a-Judge*, 2024 (last revised v6, October 2025) — [arXiv:2411.15594](https://arxiv.org/abs/2411.15594)
- Dubois et al., *Length-Controlled AlpacaEval*, COLM 2024 — [arXiv:2404.04475](https://arxiv.org/abs/2404.04475)
- You et al., *Agent-as-a-Judge* — [arXiv:2601.05111](https://arxiv.org/abs/2601.05111)
- *From Agent Traces to Trust: A Survey of Evidence in LLM Agent Evaluation* — [arXiv:2606.04990](https://arxiv.org/abs/2606.04990)
- LangChain, [*How to calibrate LLM-as-judge with human corrections*](https://www.langchain.com/resources/llm-as-a-judge) (March 2026)
- Tooling with first-class judge metrics: [DeepEval](https://github.com/confident-ai/deepeval) · [promptfoo](https://github.com/promptfoo/promptfoo) · [Ragas](https://github.com/vibrantlabsai/ragas) (RAG-specific judges)

Previous: [Evaluation fundamentals](01-evaluation-fundamentals.md) · Next: [Agent benchmarks](03-agent-benchmarks.md)
