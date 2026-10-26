# Evaluation dataset engineering: the golden set is the moat

> Part of [105 — AI Evaluation](README.md) · Reviewed October 27, 2026

Models are commodities — you swap them with a config change. Prompts are cheap — anyone can write one. The artifact that actually determines whether your evaluation tells you the truth is the **dataset you evaluate on**. A great judge scoring the wrong cases is a precise instrument measuring the wrong thing. This note is about building that dataset deliberately: the taxonomies, the creation methods, the statistics of "how many cases," and the governance that keeps a golden set honest for months instead of weeks.

The [LLM Evaluations course](course/README.md) builds golden datasets hands-on in lectures [13](course/13-testing-rag-retrievers.md) (retriever goldens), [14](course/14-rag-triad-generator-pipeline.md) (golden contexts), [15](course/15-geval-deterministic-judge.md) (judgment goldens) and [16](course/16-rag-security-toxicity-leakage-scope-drift.md) (adversarial/benign/mixed safety cases). This note generalizes those into reference material.

## Why the dataset is the bottleneck

Every evaluation pipeline is `dataset × metric × judge` — and of the three, the dataset is the one that encodes *your* product. MMLU measures nothing about a CampusX doubt solver; a generic "helpfulness" golden set measures nothing about your refund-policy chatbot. The failure pattern is always the same:

- The team reuses a public benchmark or a template dataset, gets a passing score, ships, and the first week of production traffic produces failure modes the eval never sampled.
- Or the team hand-writes 10 cases in an afternoon, iterates the prompt against them, and the eval becomes a mirror — the system looks perfect because the cases stopped being hard the moment the prompt fit them.

Both failures are dataset failures, not metric failures. Faithfulness computed on 15 representative, adversarial, and fresh cases is more informative than faithfulness computed on 200 template-generated variants of the same question.

## The taxonomies: four cuts through the same data

### Cut 1 — what the case *contains* (the reference structure)

| Golden type | Fields | Evals it powers | Built in |
|---|---|---|---|
| **Ideal-answer goldens** | `input`, `ideal_output` | Reference-based correctness, exact/semantic match | Course lecture 13 |
| **Golden-context goldens** | `input`, `ideal_context` (or chunk IDs) | Retriever recall/precision, RAG Triad isolation | Lectures 13–14 |
| **Judgment goldens** | `input` + rubric expectations (no reference) | Reference-free metrics: style, helpfulness, toxicity | Lecture 15 |
| **Trajectory goldens** | task, tool-call sequence or final state | Agent evals, [SWE-bench](03-agent-benchmarks.md)-style task completion | — |
| **Preference pairs** | `input`, `chosen`, `rejected` | Pairwise judges, RLHF-style scoring | — |

The field names matter less than the discipline: a case that doesn't declare what "correct" means cannot be reused by the next person who inherits the eval.

### Cut 2 — adversarial, benign, mixed

Safety evals ([lecture 16](course/16-rag-security-toxicity-leakage-scope-drift.md)) need all three case types, and the pattern generalizes to quality evals:

- **Adversarial cases** — the attack or the hard edge: the jailbreak, the multi-part question with a poisoned second half, the query that tempts the model off-policy.
- **Benign cases** — the false-positive guards. If your toxicity eval only contains attacks, a chatbot that refuses *everything* scores perfectly. The benign case ("How do I evaluate my chatbot on toxic questions?") is what catches over-refusal.
- **Mixed cases** — "explain MMLU, then roast the leaderboard newbies": the ideal behavior is partial compliance (answer part one, refuse part two). These are the only cases that test *boundary navigation* rather than blanket refusal or blanket compliance.

A dataset with only one case type measures a system's reflex, not its judgment.

### Cut 3 — frozen core vs. rolling fresh

The pattern from [eval engineering](05-eval-engineering.md), restated as a dataset property:

- **Frozen core** (50–300 cases, semver-ed, changes only via review) — this is the release gate. Its stability is what makes metric movements *meaningful*: if case 37 passed yesterday and fails today, a diff caused it.
- **Rolling fresh** (re-synthesized or re-sampled monthly, or promoted from production) — this is the reality check. It catches drift the frozen core is structurally blind to, because the core was drawn from last quarter's traffic.

Running both and *reporting them separately* is the honest configuration: gate on the frozen core, alarm on the divergence between core and fresh.

### Cut 4 — provenance

Where a case came from predicts how it fails:

- Hand-written by the builder: highest intentionality, highest risk of "the author's blind spot" (you write cases for failure modes you already imagine).
- Synthesized by an LLM: broad coverage, risk of [contamination and circularity](#the-circularity-problem) (see below).
- Mined from production: the most honest distribution, but needs PII hygiene, sampling discipline, and labeling before reuse.
- Promoted from incidents: the highest value per case — every escaped failure becomes a permanent regression test.

## Creation methods compared

| Method | Quality | Effort | Cost | Coverage | Best for |
|---|---|---|---|---|---|
| **Manual authoring** by domain expert | Highest intent, verifiable | Slow (30–60 min/case for RAG goldens with references) | People-time | Narrow but deep | The frozen core's seed; safety policy cases |
| **LLM-synthesized** (DeepEval Synthesizer, RAGAS testset evolution) | Good breadth, needs human review pass | Fast to generate, nontrivial to review | Judge-model tokens | Broad | Scaling 15 → 150 cases; coverage sweeps |
| **Production mining** | Most realistic | Medium (sampling + PII + labeling) | Infra + labeling | Exactly your traffic | Rolling-fresh sets; incident promotion |
| **User-feedback distillation** | Noisy but directional | Medium | Analytics time | Where users struggle | Finding *what to test next*, not the tests themselves |
| **Public benchmark adaptation** | Off-distribution | Low | Low | Wrong product, usually | Smoke tests and teaching examples only |

The practical sequence almost every mature team converges on: **hand-write 15–30 seeds → synthesize to 100–300 with review → mine production monthly → promote incidents forever.** The [course's four ways to create goldens](course/13-testing-rag-retrievers.md) (manual, from documents with an LLM, Synthesizer, production) are the same ladder.

### What the real synthesizers actually do

- **DeepEval Synthesizer** — takes a document corpus (or a URL, or raw text), generates question–answer pairs per chunk with configurable evolution styles (reasoning, multi-hop, multi-context), and emits `Golden` objects directly usable by its metrics. The [course lecture 13](course/13-testing-rag-retrievers.md) demonstrates it live on the lecture-transcript corpus.
- **RAGAS testset generation** — builds knowledge triples from documents and evolves simple questions into harder ones (in-breadth, in-depth, multi-hop, hypothetical), producing inputs plus expected outputs plus an `evolution_type` tag you can stratify on. The evolution taxonomy is the useful part: it forces the dataset to contain *difficulty structure*, not just volume.
- **OpenAI evals** — the registry format (`.yaml` + `.jsonl`) is minimal but the model is instructive: an eval is a folder with declared test cases, a grading config (model-graded, string-match, or a custom script), and nothing else. The registry's real contribution is **social** — evals are meant to be forked, so schema discipline matters more than generation cleverness.
- **HELM scenarios** — the academic version of the same discipline: every scenario declares its data source, its license, and its metrics; the framework handles sampling and aggregation so results are comparable across models. Steal the *declaration* pattern even if you never run HELM.

> 💡 **Expert commentary — synthesis diversity needs active management.** Left alone, an LLM asked for "50 diverse questions about these transcripts" produces 50 paraphrases of the same six questions. The synthesizers that work force diversity structurally: RAGAS anchors each case to different knowledge triples, DeepEval varies evolution styles per chunk, and both let you inspect per-case provenance. When you write your own synthesis prompt, cluster the outputs (embedding + HDBSCAN is enough) and re-prompt for the empty clusters — "generate questions that are NOT about X" is the cheapest diversity lever there is.

## The circularity problem

Synthesizing eval data with the same model family you are evaluating creates two failure modes:

1. **Contamination in the small** — the generator writes cases whose phrasing the model-under-test already produces naturally, so scores inflate. The system is being graded on its own accent.
2. **Circular judging** — LLM-as-a-judge scoring LLM-generated "ideal" answers measures agreement between two samples of the same distribution, not correctness. A wrong-but-fluent synthesized reference teaches your judge that fluent-wrong is the shape of "correct."

Mitigations, in decreasing order of effectiveness:

- Generate with a *different* model family than the system under test, and judge with a third (or a [calibrated](02-llm-as-a-judge.md) pinned judge).
- Human-review a random 20% of synthesized references; track the rejection rate as a quality metric of the synthesizer itself.
- Prefer **golden-context goldens** over ideal-answer goldens for synthesis: extracting the supporting chunk from the source document is a much easier (and more verifiable) task than writing the ideal answer — the document *is* ground truth by construction, which is why lecture 14 builds its faithfulness dataset by pairing chunks with Claude-generated questions rather than Claude-generated answers.

## How many cases? The statistics

The honest answer is a function of what the dataset is for:

| Purpose | n (cases) | Why |
|---|---|---|
| Smoke test / debug loop | 10–20 | Fast iteration; catches gross breakage; never a basis for claims |
| CI regression gate | 50–100 | At n=50, one flipped case moves a pass rate by 2 points — your noise floor is visible and your gate threshold must exceed it |
| Release gate | 200–500 | Detects 3–5 point regressions with acceptable false-alarm rates; supports per-slice reporting at 30–50 cases/slice |
| Judge validation | 300+ per compared condition | Human–judge agreement estimates need the sample size; ±5% on an agreement rate needs ~380 paired samples |
| Safety coverage | As many adversarial types as you can enumerate | Safety failure modes are long-tailed; volume matters less than *type* coverage — 15 well-chosen cases covering 15 attack families beat 500 variations of one attack |

The two pieces of arithmetic worth internalizing:

- **Sensitivity**: a pass rate at n=50 quantizes to 2-point steps; at n=15 (the course's datasets) to ~6.7-point steps. Any threshold you set inside one quantization step is decoration. Either raise n or widen the threshold beyond the step size.
- **Confidence intervals**: a 90% pass rate at n=100 has a 95% CI of roughly ±6 points (Wilson). "We improved from 90% to 93%" on the same n is indistinguishable from noise. Report intervals, or don't report deltas.

> 💡 **Expert commentary — the smallest useful eval set is one you can explain.** Teams agonize over n and then ship datasets whose cases they cannot describe. A better audit than counting: sample five random cases and ask "what failure mode does this case exist to catch?" If you can't answer for two of them, the dataset has padding — delete it. Fifteen intentional cases with a written answer beat fifty with three stale.

## Versioning and governance

Golden datasets decay silently. Governance is what converts them from a one-time artifact into durable infrastructure:

- **Semantic versioning with teeth**: `core-v12 → core-v13` is a reviewed diff with a changelog entry ("added 12 cases from the March refund-policy incidents; removed 3 cases invalidated by the product rename"). Anyone can diff the *behavior* between versions.
- **Dataset cards**: a README per dataset stating purpose, provenance (hand-written / synthesized by *which model* / mined from *which period*), labeling rubric, license constraints, known gaps ("no multilingual cases yet"), and the review date. This is the HELM declaration pattern, applied internally.
- **One-way promotion**: production incidents enter the golden set with a date and a link, and never silently disappear — the rule from [eval engineering](05-eval-engineering.md), restated because it is the single highest-ROI dataset habit.
- **Drift audit, quarterly**: embed your golden inputs and a fresh production sample; compare distributions (topic mix, length, language, intent). A golden set that has drifted from traffic is measuring a product you no longer have.
- **Access hygiene**: goldens contain real-looking data; if mined from production, PII scrubbing (e.g., [Presidio](../106_AI-Security-Safety/06-responsible-ai.md)) happens *before* the case enters the repo, not at eval time.

## Failure cases worth remembering

- **Overfitting the prompt to the goldens** — the [course's explicit warning](course/14-rag-triad-generator-pipeline.md): after 3–4 rounds of feeding failures back into the prompt, your metrics rise because the prompt has memorized the cases. The fix is a held-out slice you never iterate against (the same discipline as a train/test split, applied to prompt engineering), refreshed when the working set has been fully absorbed.
- **The golden-set pivot gap** — the product changes its answer format, every ideal-answer golden silently becomes wrong, and pass rates crater (or worse, the team "fixes" the goldens to match the new output without checking correctness). Version the dataset *with* the product's format changes.
- **Judge-prompt leakage into goldens** — if the person writing judge prompts is also generating the goldens, the rubric's vocabulary leaks into the references, and the judge scores phrase-matching instead of quality. Separate the authors, or at least review with fresh eyes.
- **The synthetic-only safety set** — a toxicity dataset where every adversarial case came from one synthesis prompt has one attack *style*; the first real attacker differs in style, not just content. Seed adversarial sets from documented incident patterns ([106 red teaming](../106_AI-Security-Safety/03-red-teaming.md)) before synthesizing variations.

## Checklist: building your first golden dataset

1. [ ] Write down the failure modes you're testing for *before* writing any case (the safety-policy pattern from [lecture 16](course/16-rag-security-toxicity-leakage-scope-drift.md)).
2. [ ] Choose the reference structure deliberately (ideal answer vs golden context vs judgment-only) — it decides which metrics you can run.
3. [ ] Hand-write 15–30 seed cases spanning those failure modes, including at least 3 benign (false-positive guards) and 3 mixed.
4. [ ] Label each case with its intended failure mode and provenance.
5. [ ] Synthesize toward 100+ only after the seeds look right; review 20% of synthesized references by hand and track the rejection rate.
6. [ ] Compute your noise floor: run the suite twice with no changes; the spread is your minimum detectable effect.
7. [ ] Set thresholds outside the quantization step (n=50 → at least 4 points; n=15 → at least 14).
8. [ ] Split frozen core from rolling fresh; gate on the former, alarm on divergence from the latter.
9. [ ] Add the promotion pipeline: every production incident becomes a case with a date and a link.
10. [ ] Write the dataset card, pick a version, and date the next drift audit.

## Cross-references

- [Eval engineering](05-eval-engineering.md) — where datasets live in the CI/release-gate system
- [LLM-as-a-Judge](02-llm-as-a-judge.md) — judging is the other half; a great dataset with an uncalibrated judge still lies
- [Agent benchmarks](03-agent-benchmarks.md) — the contamination and dataset-integrity literature, at benchmark scale
- [RAG evaluation](04-rag-evaluation.md) — which golden structure fits which RAG metric
- Course lectures: [13 — retriever goldens](course/13-testing-rag-retrievers.md) · [14 — golden contexts](course/14-rag-triad-generator-pipeline.md) · [15 — judgment goldens](course/15-geval-deterministic-judge.md) · [16 — adversarial/benign/mixed design](course/16-rag-security-toxicity-leakage-scope-drift.md)
- [106 — AI Security & Safety](../106_AI-Security-Safety/README.md) — incident-driven case promotion and red-team seeding
