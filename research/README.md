# Evidence and reproducible research

Reviewed October 9, 2026. This is a review date, not a claim that the underlying data was collected today. Publication dates, scrape dates, and review dates are recorded separately.

## What has been verified

The job-posting analysis below was executed against a pinned checkout of the original field guide. The benchmark and protocol references were inspected at the commits in [sources.json](sources.json). Their model evaluations were **not** run here. A readable README or a published leaderboard does not verify a model's suitability for your product.

| Evidence | Original publication or observation date | What it supports | What it does not support |
|---|---|---|---|
| [Job postings](https://github.com/alexeygrigorev/ai-engineering-field-guide/tree/ed590319553252e2b8275486597b144ac55a4f3c/job-market) | Nine scrape folders, February 4–September 23, 2026 | Counts of available raw records and extracted tags | Worldwide demand, causal hiring trends, compensation premiums |
| [Extraction evaluation](https://github.com/alexeygrigorev/ai-engineering-field-guide/blob/ed590319553252e2b8275486597b144ac55a4f3c/job-market/_internal/eval/README.md) | Maintainer describes an August 2026 evaluation | Documented weaknesses of LLM enrichment and limits of a small, stratified review | Independent validation of every annotation or every extracted field |
| [BEIR](https://github.com/beir-cellar/beir) | NeurIPS 2021; resource paper 2024 | Retrieval evaluation across different task distributions | Current events, enterprise authorization, answer correctness |
| [SciFact](https://github.com/allenai/scifact) | Paper identifier `2004.14974`, April 2020 | Expert-written scientific claims linked to paper abstracts and evidence | Current medical advice; publicly labeled original test data |
| [MTEB / MMTEB](https://github.com/embeddings-benchmark/mteb) | Original paper October 2022; multilingual extension February 2025 | Task- and language-specific embedding evaluation | A universal best embedding model; a uniform license for every dataset |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | Original paper October 2023; Verified release August 13, 2024 | Real GitHub issues evaluated through a reproducible software harness | Permission to run untrusted repository code on a host; production reliability |
| [SWE-bench Multimodal v2](https://github.com/SWE-bench/SWE-bench) | README announcement September 1, 2026 | A dated release announcement for multimodal software tasks | A fresh run by this field guide |
| [τ³-bench](https://github.com/sierra-research/tau2-bench) | Voice/knowledge papers March 2026; grading update July 2026 | Versioned agent evaluation in **simulated** customer-service environments | Real customer transactions or real production outcome data |
| [MCP](https://github.com/modelcontextprotocol/modelcontextprotocol) | Schema revision July 28, 2026, identified in the reviewed README | A precise starting point for protocol implementation | Authorization, safe execution, or compatibility without implementation tests |

The older τ-bench README directs readers to τ³-bench. The current repository warns that `banking_knowledge` scores before and after version 1.0.1 are not comparable. Pin the task version and grading version before comparing results.

These are primary, identifiable resources. They are a selected evidence set, not a survey of every dataset in the world. Simulated tasks are labeled as such and are not used as evidence of real-world deployment outcomes.

## Reproduce the real job-posting analysis

Requires Python 3.10+ and Git. Run from this repository's root. Use a separate research checkout; this does not alter the field guide's source files.

```bash
python3 -m venv /tmp/ai-field-guide-research-venv
/tmp/ai-field-guide-research-venv/bin/python -m pip install -r research/requirements.txt
git clone https://github.com/alexeygrigorev/ai-engineering-field-guide.git /tmp/ai-field-guide-source
git -C /tmp/ai-field-guide-source checkout --detach ed590319553252e2b8275486597b144ac55a4f3c
/tmp/ai-field-guide-research-venv/bin/python research/analyze_job_postings.py \
  /tmp/ai-field-guide-source \
  --expected-commit ed590319553252e2b8275486597b144ac55a4f3c \
  --output /tmp/ai-field-guide-summary.json
```

If those directories already contain work, choose new paths. Do not reset or replace an existing checkout blindly. The source repository is substantially larger than this documentation repository; leave space for its raw data and Git history.

The analyzer verifies the exact commit, rejects modified dataset files, duplicate YAML keys and duplicate job IDs within a scrape, pairs raw and structured records, and records a SHA-256 fingerprint over all input files. It never invokes an LLM or scrapes a job board. It computes exact tag occurrences from upstream annotations; it does not validate those annotations against the original descriptions.

Compare the resulting JSON with [job-market-summary.json](job-market-summary.json). The reviewed run counted **8,051 stored observations across nine scrape folders**, with **1,086 records in the latest folder, September 23, 2026**. All 8,051 stored job IDs were distinct in this revision; that still does not prove distinct vacancies because employers can repost a role under different identifiers. The latest folder contains 22 groups of normalized identical descriptions, covering 50 records. These records remain in the reported denominator.

The upstream README still summarizes an earlier eight-scrape period. Read the actual files and state the observation period before reusing its headline number.

## Data rights and responsible interpretation

Raw job advertisements and benchmark datasets are not automatically covered by this repository's MIT license. Obtain data from its source, inspect the relevant dataset license and terms, record restrictions, and avoid redistributing third-party records without permission. This repository stores aggregate measurements and references, not a copied corpus of job advertisements.

For a new analysis, retain the source commit, record identifiers, observation dates, extraction prompt/model, exclusions, denominator, and code revision. Inspect a stratified sample against raw descriptions. Treat annotation quality, missingness, duplicated text, geography, job-board selection, and ambiguous titles as measurement problems before interpreting a percentage.

For production evaluation, public datasets provide a baseline. Add consented, de-identified examples from the actual workflow, reviewed by domain experts. Separate development, calibration, and final test sets by document family or time where appropriate. Publish failures and uncertainty alongside averages.

See [the evidence policy](evidence-policy.md), [the repository audit](audit-2026-10-09.md), and [the advanced learning path](../learning-paths/advanced-engineering.md).

## Offline documentation checks

After installing `research/requirements.txt`, run `python tools/check_docs.py` from the repository root. This checks rendered Python-fence syntax and relative file targets. It does not execute application examples, verify anchor fragments, check external URLs, or certify factual claims.
