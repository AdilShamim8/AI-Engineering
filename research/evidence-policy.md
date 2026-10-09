# Evidence policy

Reviewed October 9, 2026.

Every empirical statement needs a source that permits a reader to check the claim. An update date alone does not provide that evidence. This policy applies to legacy material as well as new additions.

## Label the kind of statement

| Kind | Required support | Example |
|---|---|---|
| Reproduced measurement | Pinned inputs, executable method, denominator, output, limitations | The September 23 source folder contains 1,086 records |
| Source-reported result | Primary citation, publication date, exact task/version and conditions | A benchmark maintainer announces a release |
| Design target | Explicitly labeled target, workload assumptions, acceptance criterion | A team chooses a latency budget before load testing |
| Teaching illustration | Explicitly labeled hypothetical input or output | A fictional support question used to explain evaluation |
| Recommendation | Reasoned tradeoff, conditions and failure cases | Start with a lexical retrieval baseline before adding components |
| Unverified legacy claim | Visible qualification or removal from factual summaries | An older salary table without records or sampling details |

Do not present invented numbers, generated labels, example workloads, or an LLM-produced answer as measured ground truth. A benchmark score measures the selected benchmark under a particular protocol. It is not an estimate of all customer outcomes.

## Required provenance for datasets and results

- Source owner and URL; dataset version, immutable revision, or content checksum.
- Publication/release date, collection/observation period, and review date as separate fields. Unknown dates stay unknown.
- Population, sampling frame, geographic/language coverage, missingness, duplicate policy, exclusions, and denominator.
- Raw versus derived fields, annotation method, human-review procedure, and known measurement errors.
- License, access restrictions, consent/privacy handling, and permission to redistribute.
- For experiments: code/package/model versions, task IDs and split, seeds/trials, prompt and judge versions, hardware, run logs, cost and timing definitions.
- Results with uncertainty and failure slices; no zero-error or causal claim inferred from a small convenience sample.

Confidence intervals quantify specified sampling uncertainty; they do not repair a biased sampling frame. A job-board convenience sample remains a convenience sample even if every arithmetic calculation is correct.

## What the October 9 review does and does not certify

The [audit](audit-2026-10-09.md) records a full structural scan of the original 151 Markdown documents and targeted technical/source review. The [source manifest](sources.json) pins the external documents inspected. The [job summary](job-market-summary.json) contains reproduced counts. These artifacts do **not** certify every historical factual claim, company interview account, package example, legal statement, or model name in the long-form lessons.

Legacy labels such as “Verified & Updated: September 16, 2026” are historical editorial labels, not proof that every statement was checked. Legacy numerical examples without provenance must be treated as illustrations or unresolved claims, not cited as factual results. Model capabilities, pricing, package APIs, and laws require source-specific review before reuse.

## Contribution review

For each changed file, explain the problem, the resulting behavior or interpretation, the supporting evidence, the checks run, and the remaining limits. Do not advance unrelated dates or rewrite correct material to make a change look larger. Add claim-level citations where the reader needs them, and retain negative results rather than replacing them with a success story.
