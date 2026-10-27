# Red teaming AI systems

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 27, 2026

Red teaming is [evaluation](../105_AI-Evaluation/README.md) with an adversary: systematic, preferably automated, adversarial testing of an AI system *before* someone else tests it for you. This note covers the methodology, the 2026 tooling landscape, and — the part most teams skip — converting findings into permanent regression tests.

## What AI red teaming is (and isn't)

- **Is:** generating large, diverse corpora of adversarial inputs (injections, jailbreaks, poisoned documents, malicious tool sequences), running them against the real system, and scoring outcomes as *rates* — attack success rate, leakage rate, unsafe-action rate — because probabilistic systems need distributional verdicts.
- **Isn't:** a one-time penetration test with a report. Model updates, prompt changes, and new tools all reopen the surface; red teaming is a **continuous discipline** wired into CI like any other [eval suite](../105_AI-Evaluation/05-eval-engineering.md).
- **Also isn't:** a certification. A clean scan means your *tested attacks* failed, not that no attack exists. The [evidence policy](../research/evidence-policy.md) applies: report what was tested, when, with what result.

Microsoft's AI Red Team has published the most-cited operational framing (Perez et al. and the PyRIT papers below) with a useful decomposition of what you probe for: **security** harms (injection, exfiltration, privilege escalation) and **safety** harms (harmful content, bias, misinformation) — different judge criteria, same harness machinery.

## The methodology loop

1. **Scope by threat model.** Take the [threat model](01-threat-modeling.md)'s untrusted-input/capability/exfiltration triples; each triple suggests an attack family. Don't fuzz indiscriminately — test the boundaries you actually have.
2. **Generate adversarial inputs** — statically curated corpora (known jailbreak templates, encoding tricks, multilingual payloads), LLM-generated variants, and **multi-turn** attacks that escalate gradually (the hardest class for defenses; see the Crescendo strategy below).
3. **Execute against the real pipeline** — not the raw model. Attacks that die at your output filter are wins; attacks that only work on the naked API tell you little about the deployed system.
4. **Score automatically** — LLM judges for "did the system comply with the malicious goal," string/classifier checks for canary leakage, assertion checks for unauthorized tool calls. Same [judge calibration](../105_AI-Evaluation/02-llm-as-a-judge.md) discipline as quality metrics, since a miscalibrated attack-scorer means miscalibrated risk.
5. **Report rates with slices** — per attack family, per model version, over time. "17/200 injection attempts succeeded via Unicode-embedded payloads" is actionable; "model is vulnerable" is not.
6. **Promote confirmed attacks to regression tests** — the loop's exit condition. Each vulnerability becomes a case in the CI suite with expected-safe behavior; the fix must flip it, and no future change may regress it.

## The tooling landscape (October 2026)

All open-source, all actively maintained, different centers of gravity:

| Tool | Maintainer | Strength |
|---|---|---|
| [PyRIT](https://github.com/Azure/PyRIT) | Microsoft AI Red Team | Python framework for **multi-turn attack orchestration** — Crescendo, Tree of Attacks with Pruning (TAP), Skeleton Key — with pluggable scorers and memory across an engagement. The engine behind Microsoft's Azure red-teaming agent. |
| [garak](https://github.com/NVIDIA/garak) | NVIDIA | **Vulnerability scanner** model: ~100 probe categories (injection, jailbreak, hallucination, bias, data leakage), CLI-driven, JSONL reports. Best for broad baseline sweeps. |
| [promptfoo red team](https://www.promptfoo.dev/docs/red-team/) | promptfoo (acquired by OpenAI, March 2026) | **YAML-declared red-team configs in CI** — plugins mapped to OWASP LLM/ASI categories, strategies incl. multi-turn, integrated with its eval platform. 50+ vulnerability types. |
| [DeepTeam](https://github.com/confident-ai/deepteam) | Confident AI | Red teaming alongside [DeepEval](https://github.com/confident-ai/deepeval) — OWASP/framework-aligned attack libraries as Python, sharing the same pytest-style harness as quality evals. |
| [Giskard](https://github.com/giskard-ai/giskard) | Giskard AI Foundation | Scanning LLM apps & agents: injection, leakage, hallucination, bias probes in one run. |

A pragmatic pairing used in practice: **garak or promptfoo for breadth** (weekly scan, new CVE-style probes appear upstream), **PyRIT for depth** (a focused multi-turn campaign against your highest-risk workflow before each major release), and **DeepTeam/promptfoo for retention** (confirmed attacks as versioned CI cases).

Two selection notes: (1) match the tool to your *target type* — plain model endpoint vs HTTP app vs browser agent change what "execution" means; (2) every tool's attack corpus is public knowledge, so passing its scans is necessary and radically insufficient against adaptive adversaries — reserve budget for custom attacks specific to your domain and corpus.

## The corpora: what to generate *from*

Step 2 of the loop ("generate adversarial inputs") should not start from a blank page. The public ecosystem is cataloged in the [datasets note](07-security-safety-datasets.md); the red-teamer's selection problem is which layer to draw from:

- **Fixed attack sets** (AdvBench's 520 behaviors, JailbreakBench's 100+100, HarmBench's 400 behaviors across 7 semantic categories) — for baseline sweeps and comparability across model versions. Cheap, standardized, aging: treat as the *control group* of any campaign.
- **Mined adversarial behavior** (WildJailbreak: 262K prompt-response pairs from real user interactions, 5.7K distinct jailbreak-tactic clusters) — for realistic diversity, especially multi-turn and novel phrasings your team would never invent. This is the closest public analogue to what your production attackers actually do.
- **Domain corpora you build** — payloads embedded in *your* document types, targeting *your* tools, using *your* terminology. The only layer an adversary cannot download; the only layer that measures your actual system rather than the average system.

The discipline that separates a serious program from tool-waving: **attribute every case in your suite to its layer and source** (JailbreakBench's `Source` field design, applied internally), and re-baseline the fixed sets whenever you change model versions — attack-success rates on public corpora are only comparable within a fixed target.

## Metrics that matter

- **Attack success rate (ASR)** per family and per strategy — the headline number; track its trend, not one snapshot.
- **Canary leakage rate** — seeded secrets appearing in any outbound channel; the exfiltration-ground-truth metric.
- **Unsafe-action rate** — unauthorized/destructive tool calls per attack session.
- **Defense overhead** — false-positive rate of your guardrails on *benign* traffic. A filter that blocks 100% of attacks and 30% of legitimate requests is a broken filter; over-refusal is a safety failure of its own (see [alignment](05-ai-alignment.md)).
- **Time-to-detect** if you run continuous canaries in production — how long a novel attack pattern persists before alerting.

## From findings to fixes

Rank findings by *consequence × reachability*, then map each to a layer from the [defense stack](02-prompt-injection-defense.md): capability removal > external validation > approval gates > detection. The field's repeated lesson: fixes at the model-prompting layer (stronger refusal instructions) decay fastest; fixes at the architecture layer (remove the exfil path, sandbox the tool) survive model upgrades. Document residual risk for the [governance record](06-responsible-ai.md) — what you tested, what you accepted, who owns it.

## References

- [PyRIT](https://github.com/microsoft/pyrit) — Lopez Munoz et al., *PyRIT: A Framework for Security Risk Identification and Red Teaming in Generative AI System*, 2024 — [arXiv:2410.02828](https://arxiv.org/abs/2410.02828) (citation corrected October 27, 2026: the previously cited arXiv:2404.02144 is an unrelated astronomy paper; the repo also moved from Azure/PyRIT to microsoft/pyrit)
- [garak](https://github.com/NVIDIA/garak) — Derczynski et al., 2024 — [arXiv:2406.11036](https://arxiv.org/abs/2406.11036)
- [promptfoo red team documentation](https://www.promptfoo.dev/docs/red-team/) — includes the OWASP-mapped plugin list
- Dheekonda, Pearce & Landers, *Redefining AI Red Teaming in the Agentic Era: From Weeks to Hours*, 2026 — [arXiv:2605.04019](https://arxiv.org/abs/2605.04019)
- Microsoft, [*AI red teaming with PyRIT*](https://learn.microsoft.com/en-us/security/ai-red-team) — practitioner guidance
- [Roadmap Level 8, module M8.7](../roadmap/full-roadmap/level-08-ai-security.md) — the syllabus version of this note
- Cross-cutting: [eval engineering](../105_AI-Evaluation/05-eval-engineering.md) — the CI machinery that retains findings

Previous: [Prompt injection defense](02-prompt-injection-defense.md) · Next: [Agent & MCP security](04-agent-mcp-security.md)
