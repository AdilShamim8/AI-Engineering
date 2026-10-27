# Security & safety datasets — what to actually test on

> Part of [106 — AI Security & Safety](README.md) · Reviewed October 27, 2026

The other notes in this section give you the *methodology* — threat models, defense layers, red-team loops. This note gives you the **data**: the public datasets and benchmarks that turn "we tested our system" into a number someone else can interpret. It is the dataset companion to [red teaming](03-red-teaming.md) and the security-side counterpart of the [evaluation-dataset methodology](../105_AI-Evaluation/06-evaluation-datasets.md) in 105.

Everything below is cross-checked against the [AI-Safety repository](https://github.com/AdilShamim8/AI-Safety)'s dataset catalog — 43 cards, each with provenance, license, and page-verified size facts, verified October 21–25, 2026 — where full per-dataset evidence lives. That catalog's discipline applies here too: every size claim carries its access level, and discrepancies between mirrors and canonical sources are recorded rather than smoothed over.

## How to read this catalog

Three rules before the tables:

1. **Attack corpora and control corpora are reported together.** A jailbreak set without its benign twin measures nothing you can act on: a system that refuses 100% of attacks and 40% of legitimate requests *failed the test*. This paired-ledger discipline is why JailbreakBench ships 100 benign behaviors alongside its 100 harmful ones, and why [XSTest](https://github.com/paul-rottger/xstest) and OR-Bench exist at all. When you report attack success rate, report over-refusal on the same run.
2. **Static sets age.** Attack knowledge is public knowledge — every listed dataset is in every attacker's and every lab's training mix. Benchmark numbers are for *comparison between systems under equal conditions*, never a security guarantee. AgentDojo's dynamic-environment design (below) is the field's structural response.
3. **Licenses are part of the catalog.** Two of the most useful safety datasets are **non-commercial** (BeaverTails, PKU-SafeRLHF — CC BY-NC 4.0); real-user corpora range from ODC-BY to custom impact licenses. Check before anything ships to production.

## 1. Direct jailbreak & harmful-behavior corpora

The workhorses: fixed sets of harmful instructions used to measure raw refusal robustness and attack success.

| Dataset | What it is | Verified composition | License |
|---|---|---|---|
| [AdvBench](https://github.com/llm-attacks/llm-attacks) | The target set for the GCG adversarial-suffix attack ("Universal and Transferable Adversarial Attacks on Aligned Language Models", Zou et al. — [arXiv:2307.15043](https://arxiv.org/abs/2307.15043)) | `harmful_behaviors.csv`: **520 data rows** (521 lines with header, 80.2 KB), plus `harmful_strings.csv`; ships inside the `llm-attacks` repo | MIT |
| [JailbreakBench (JBB-Behaviors)](https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors) | The standardized jailbreak benchmark — fixed behaviors, fixed protocol, public leaderboard, created because attack papers used incomparable targets and judges ([arXiv:2404.01318](https://arxiv.org/abs/2404.01318)) | **200 behaviors: 100 harmful + 100 benign**; 10 categories aligned with OpenAI usage policies; a `Source` field tracing each behavior to HarmBench/AdvBench/original; `judge_comparison` subset of 300 rows | MIT |
| [HarmBench](https://github.com/centerforaisafety/HarmBench) | Standardized evaluation framework for automated red teaming: behavior sets + attack-method registry + classifier judge; compared **18 red-teaming methods against 33 targets** ([arXiv:2402.04249](https://arxiv.org/abs/2402.04249), Mazeika et al., Center for AI Safety) | **400 text behaviors** (200 standard / 100 copyright / 100 contextual; test 320, val 80) + 110 multimodal; categories from cybercrime_intrusion (67) to chemical_biological (56) | MIT |
| [StrongREJECT](https://arxiv.org/abs/2402.10260) | The evaluation-methodology corrective: forbidden prompts **plus** a response-harmfulness scorer built after its authors documented that jailbreak papers "often boast near-100% attack success rates" that don't survive proper scoring ("A StrongREJECT for Empty Jailbreaks", Souly et al.) | Prompt set + evaluator rubric; composition at abstract level — the point is the *scorer*, not the prompt count | not yet verified |
| [WildJailbreak](https://huggingface.co/datasets/allenai/wildjailbreak) | The in-the-wild turn: **262K prompt-response pairs mined from real user–chatbot interactions** (WildTeaming, [arXiv:2406.18510](https://arxiv.org/abs/2406.18510)), with 5.7K unique clusters of novel jailbreak tactics — adversarial prompts up to 4.6× more diverse than curated sets | Contrastive design: harmful queries (vanilla + adversarial) **plus benign lookalikes** — the paired ledger built in | ODC-BY |

**The provenance lesson in this table.** Three generations are visible: curated lists (AdvBench, 2023) → standardized protocols with lineage fields (JailbreakBench, HarmBench, 2024) → mined-from-production distributions (WildJailbreak, 2024–25). For threat modeling, the third generation matters most: what real users actually try is the distribution you defend against, and it is broader than any curated list. For comparability, the second generation is the reference. And note the discrepancy discipline: AdvBench is commonly described as "500 harmful behaviors" from mirror pages, while the canonical CSV has 520 rows — the AI-Safety catalog records both numbers with their sources rather than picking the popular one. Do the same in your own reports.

**JailbreakBench's `Source` field is the detail to steal.** Every behavior records where it came from (HarmBench, AdvBench, or original). This is provenance-in-design — the benchmark equivalent of a package lockfile — and it is what makes derivative benchmark suites auditable instead of folklore. When you build your internal attack corpus, give every case a source field from day one.

## 2. Agent & indirect-injection benchmarks

Direct jailbreaks test the chatbot; these test the *system* — what happens when the adversary lives in content the agent processes, or in the task it is asked to perform. This is where [agent security](04-agent-mcp-security.md) meets measurement.

| Benchmark | Threat it measures | Verified composition | Source |
|---|---|---|---|
| [AgentDojo](https://github.com/eth-sri/agentdojo) | Prompt injection against tool-using agents: "data returned by external tools hijacks the agent to execute malicious tasks" | **97 realistic tasks**; explicitly *not a static test suite* but an extensible environment for tasks, defenses, **and adaptive attacks** — attack the defense, not just the model | Debenedetti et al., [arXiv:2406.13352](https://arxiv.org/abs/2406.13352) (ETH-SRI) |
| [InjecAgent](https://arxiv.org/abs/2403.02691) | Indirect prompt injection (IPI) against tool-integrated agents — malicious instructions embedded in emails, web pages, documents the agent touches | Abstract-verified scope; the design property that matters: **success criteria are actions taken, not text produced** — a compromised agent that never says anything harmful but calls the wrong tool still fails | Zhan et al., arXiv:2403.02691 |
| [AgentHarm](https://arxiv.org/abs/2410.09024) | Agent *misuse* — explicitly malicious multi-stage tasks for agents with tools, created because jailbreak research "has been studied primarily for LLMs acting as simple chatbots" while agent misuse "remains underexplored" | **110 explicitly malicious tasks, 440 with augmentations** — task *families*, so a defense can't pass by handling one phrasing; harm as a pipeline, not a single completion | Andriushchenko et al., arXiv:2410.09024 |
| [BIPIA](https://arxiv.org/abs/2312.14197) | Indirect injection through external content types (email, web, documents) integrated into LLM applications | Headline abstract finding: evaluated LLMs **universally vulnerable**; magnitudes at body level | arXiv:2312.14197 |
| [WebArena](https://arxiv.org/abs/2307.13854) | Realistic agent task execution in self-hosted web environments | Environment-first design with **executable success predicates** — success is a checked postcondition, not a judge's opinion | Zhou et al., arXiv:2307.13854 |

**Why this table is the one to care about in 2026.** The [Claude Code espionage campaign](04-agent-mcp-security.md) and the MCP tool-poisoning wave demonstrated that production AI incidents are now *agent* incidents: multi-stage, tool-using, driven by content the system legitimately fetched. The benchmarks that model this reality share three design properties worth copying internally:

1. **Action-level success criteria** (InjecAgent): score what the system *did*, not what it said. Text-level judges miss the dangerous class of failures entirely.
2. **Task families with augmentations** (AgentHarm): one vulnerability, many phrasings. If your eval has one case per vulnerability, you're measuring memorization, not robustness.
3. **Adaptive evaluation** (AgentDojo): the environment exists to attack *your defenses* — a static suite measures a snapshot that ages in months, because attack and defense techniques co-evolve.

## 3. Multimodal attack surfaces

Text-only security testing is incomplete for any vision-language system: the modality boundary is itself an attack surface.

- **[FigStep](https://arxiv.org/abs/2311.05608)** — jailbreaks vision-language models with **typography embedded in images**: the harmful instruction rendered as pixels, where text-side filters never see it. The canonical demonstration that alignment trained on text does not automatically transfer across modalities.
- **[MM-SafetyBench](https://arxiv.org/abs/2311.17600)** — scales the idea with **query-relevant image attacks**: images constructed to match and unlock a paired harmful textual query, giving a systematic multimodal safety evaluation rather than isolated tricks.
- Complementary research result (not a dataset, but the reason these matter): visual adversarial examples were shown to jailbreak aligned LLMs where pure-text attacks failed ([arXiv:2306.13213](https://arxiv.org/abs/2306.13213)).

The transfer lesson generalizes: every new input modality (images, audio, screen captures, tool outputs) resets the alignment work. Test the boundary explicitly, and prefer benchmarks whose payloads live *in the non-text modality* rather than text about it.
