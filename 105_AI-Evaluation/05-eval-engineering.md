# Eval engineering: from measurements to release gates

> Part of [105 — AI Evaluation](README.md) · Reviewed October 17, 2026

Everything in notes 1–4 produces *measurements*. This note is about the engineering system that turns measurements into decisions: versioned eval suites that run in CI, block bad releases, and improve themselves from production. It is the AI-application version of the testing pyramid your software background already gave you — with the twist that the tests are probabilistic and the assertions are usually model-graded.

## The eval suite as a first-class artifact

Treat your eval suite like production code, because it *is* the quality control for a system that ships to users:

```
evals/
├── datasets/
│   ├── golden/                 # human-reviewed cases, versioned
│   │   ├── core-v12.jsonl      # the release-gating set
│   │   └── safety-v4.jsonl     # adversarial + policy cases
│   ├── prod-promotions/        # failures promoted from production, dated
│   └── README.md               # schema, labeling rubric, do-not-edit rules
├── configs/
│   ├── judges.yaml             # judge model, prompts, version pins
│   └── thresholds.yaml         # per-metric gates: hard blocks vs diagnostics
├── suites/
│   ├── test_rag_quality.py     # DeepEval/pytest-style suite
│   └── test_agent_trajectories.py
└── results/                    # run outputs, per-commit, for the decision log
```

The rules that make this an *engineering* artifact rather than a pile of scripts:

- **Everything in version control** — cases, judge prompts, thresholds, harness config. An eval result that can't name the commit of its own inputs is not reproducible.
- **Promotion is one-way** — production failures enter `prod-promotions/` with a date and an incident link; they never silently disappear.
- **Thresholds are configuration, not code** — changing a gate is a reviewable diff, and the PR that changes it should say why (calibration change, new slice, accepted risk).

## CI/CD integration: the quality gate

The pattern that works, layer by layer:

1. **Fast deterministic checks on every PR** — schema validation, refusal behavior, exact-format assertions, length and cost caps. Seconds, no LLM calls. Catches most regressions cheaply.
2. **Golden-suite run on PRs that touch prompts/retrieval/model config** — the 50–200 case core set with judge metrics. Minutes, some judge cost. This is the gate that *blocks*.
3. **Full suite + slice analysis nightly or pre-release** — including safety sets and trajectory evals. This is where per-slice regressions hiding behind stable averages get caught.
4. **Model/provider upgrades requalify from scratch** — a new model version is not a patch; it reruns everything, including [judge calibration](02-llm-as-a-judge.md) if the judge changed.

[promptfoo](https://github.com/promptfoo/promptfoo) and [DeepEval](https://github.com/confident-ai/deepeval) both plug into this directly — promptfoo's YAML matrix declarations map cleanly onto "compare prompt/model variants," and DeepEval's pytest integration means your eval *is* your test runner. The [CI/CD note in 104](../104_LLMOps/README.md) covers the pipeline mechanics; the [roadmap's eval module M7.7](../roadmap/full-roadmap/level-07-llm-evaluations.md) describes the same gate concept in syllabus form.

An honest gate needs three properties, or people route around it:

- **Trustworthy** — low flakiness. Stochastic metrics need either enough samples or a noise floor measured once and respected (a 1% change on a metric with ±3% run variance is not a regression; see the [infrastructure noise findings](03-agent-benchmarks.md) for how environment variance compounds this).
- **Fast enough to respect** — a 40-minute gate gets skipped; a 6-minute core suite gets obeyed.
- **Explainable when it fails** — the report shows *which slice regressed with example outputs*, not just a red X on "faithfulness: 0.78 < 0.80."

## The self-improving loop

The eval suite's compounding advantage is that it grows from reality:

```
production traffic
   → sampling + online judging (104/Observability)
   → failure triage (alerts, user reports, thumbs-down clusters)
   → promote real failures into golden/prod-promotions (with review)
   → next CI run gates against them
   → regression can never ship twice
```

The observability side of this loop — logging, sampling, dashboards, alerting — is [104 — LLMOps / Observability](../104_LLMOps/README.md) territory. The eval side owns two pieces: the **promotion pipeline** (triage → review → case with metadata) and the **feedback check** (did the fix that shipped actually flip the promoted cases from fail to pass?).

Online evaluation deserves one design warning: sampled LLM-judging of production traffic is a *monitor*, not a gate. It tells you quality moved; it cannot un-ship anything. Its job is to detect that reality drifted from your eval set fast enough for the offline loop to respond.

## Metrics dashboards that drive action

Report quality metrics the way SREs report reliability — per slice, over time, with the decision boundaries drawn:

- **Per-slice breakdowns**, not just averages — by query intent, language, document source, user tier. Averages hide the regressions that matter (the same lesson as [benchmark harness analysis](03-agent-benchmarks.md)).
- **Quality next to cost and latency** — the roadmap's M7.7 point: track them together so a quality "win" that triples cost per query is visible in the same view.
- **Judge health** — judge parse-failure rate, agreement on the rotating calibration sample. A sick judge invalidates every metric it computed this week.

## What good looks like (a review checklist)

Use this to audit your own team's setup, or to answer the interview question "how do you know your system works?" with a system instead of an anecdote:

- [ ] A golden dataset exists, is versioned, and its cases have defined provenance.
- [ ] Every release-gating metric has a written construct definition and a calibration status.
- [ ] The CI gate runs deterministic checks + core judge suite on relevant PRs.
- [ ] Judge model/prompt versions are pinned; judge parse failures are tracked.
- [ ] Production failures get promoted into the suite with a documented path.
- [ ] Thresholds live in reviewable config, with rationale in the change history.
- [ ] Per-slice reporting exists; at least one historical regression was caught by the gate (if not, the gate is theater — test it by injecting a known-bad change).
- [ ] Safety/eval overlap is deliberate: adversarial cases from [red teaming](../106_AI-Security-Safety/03-red-teaming.md) run in the same pipeline.

## References

- Hamel Husain, [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/) — the practitioner case for failure-driven eval suites.
- Anthropic Engineering, [*Demystifying evals for AI agents*](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) (Jan 2026) and [*Effective harnesses for long-running agents*](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) (Nov 2025).
- [Langfuse](https://langfuse.com/docs) and [Arize Phoenix](https://github.com/Arize-ai/phoenix) — open-source observability with dataset/eval loops for the online side.
- [promptfoo](https://github.com/promptfoo/promptfoo) · [DeepEval](https://github.com/confident-ai/deepeval) — CI-first eval tooling.
- [104 — LLMOps](../104_LLMOps/README.md) — deployment, CI/CD and observability curriculum.
- [Roadmap Level 7](../roadmap/full-roadmap/level-07-llm-evaluations.md) — module M7.7 (eval suites & regression testing) is the syllabus for this note.

Previous: [RAG evaluation](04-rag-evaluation.md) · [Back to section home](README.md)
