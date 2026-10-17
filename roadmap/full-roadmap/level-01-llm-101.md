# Level 1 · LLM 101

> **Phase 1 · Foundations** · 12 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/1/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Build a strong mental model of how LLMs work, why they behave the way they do, and how to choose and use the right model for a task.

*Short on time? Do the 6-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 8/10**

Conceptual questions are **very common in screening rounds**: tokens, attention, temperature, hallucination, context limits. Shaky answers here **end the interview early**, because they suggest you’ve only used LLMs, not understood them.

**On-the-job weight: 7/10**

It shapes good decisions about **cost, latency, and model behaviour**, and helps you debug odd outputs. But you use it as **background knowledge**, not every day.

---

## Modules

### 01 · What an LLM Actually Is (M1.1 · 1 session)

- **Next-token prediction** — Understand what a Large Language Model actually does, with next-token prediction as the core idea and generation as a repeated predict → choose → append → repeat process.
- **What an LLM is not** — Understand what an LLM is not: a database, search engine, deterministic program, or repository of stored answers.
- **Why one model does many tasks** — Understand why the same underlying model can perform writing, summarization, translation, coding, question answering, and classification.
- **Where capability comes from** — Build intuition for how capability improves through better data, more compute, larger models, and better training.

**Try it** · Give the same prompt multiple times and observe variation; predict the next word/token in simple sentences before asking the model.

**Outcome** · Explain an LLM simply: an LLM generates text by repeatedly predicting the most appropriate next token given the tokens it has already seen.

### 02 · Tokenization (M1.2 · 1 session)

- **Characters, words & tokens** — Distinguish characters, words, and tokens; understand token IDs, why LLMs operate on tokens, and why different tokenizers can split the same text differently.
- **Tokenizing across languages & code** — Explore tokenization of normal English, uncommon words, numbers, code, emojis, Hindi/Devanagari, and mixed Hindi-English text.
- **Why tokens drive cost and latency** — Connect tokenization to API pricing, context-window consumption, output length, latency, spelling difficulties, character-counting failures, and mathematical/numerical behavior.

**Try it** · Compare token counts for an English paragraph, its Hindi translation, source code, and a list of numbers.

**Outcome** · Explain why two texts with roughly the same number of words can have very different token counts and LLM costs.

### 03 · Inside an LLM: Embeddings, Attention & Transformers (M1.3 · 3 sessions)

Tokens → Vectors

- **From token IDs to embeddings** — Understand how token IDs become embeddings, what vectors represent conceptually, why concepts are represented numerically, and how representations change as they pass through transformer layers.
- **What parameter counts mean** — Understand what model parameters are and what sizes such as 8B, 70B, and 400B+ mean.
- **Why bigger is not automatically better** — Understand why more parameters can increase capacity, while larger does not automatically mean better.

Attention

- **The intuition behind attention** — Understand attention through the intuition: a token looks at other relevant tokens in the context to build a better representation of what it means.
- **Queries, keys, values & causal attention** — Build a high-level understanding of queries, keys, values, attention scores, transformer layers, and causal attention — without matrix mathematics.

Dense vs Mixture-of-Experts

- **Dense models** — Understand a dense model, where every parameter takes part in producing every token.
- **Mixture-of-Experts & routing** — Understand a Mixture-of-Experts (MoE) model, where the feed-forward layers are split into many experts and a router selects only a few of them for each token.
- **Total vs active parameters** — Distinguish total parameters from active parameters, and understand why an MoE model with a very large total size can cost far less to run than a dense model of the same size.
- **What MoE changes in practice** — Understand what MoE changes in practice: every expert still has to be held in memory, while the compute spent per token stays closer to that of a much smaller model.
- **Reading MoE model cards** — Read MoE descriptions on model cards, such as "8x7B" or "total vs active parameters", and know what they tell you about speed, cost, and hosting requirements.

**Mental model** · Text → Tokens → Embeddings → Transformer layers + attention → Next-token probabilities

**Try it** · Inspect an attention visualization for a sentence such as “The animal didn't cross the street because it was tired” and reason about what "it" should attend to.

**Outcome** · Explain conceptually what happens between a token entering the model and the model producing next-token probabilities.

### 04 · How LLMs Learn (M1.4 · 2 sessions)

Pretraining

- **Pretraining & self-supervision** — Understand pretraining, how enormous text datasets are used, why next-token prediction creates its own training signal, and what self-supervised learning means.
- **What pretraining teaches** — Understand how pretraining enables models to learn grammar, facts, patterns, concepts, relationships, coding syntax, and problem-solving patterns.
- **Memorization vs generalization** — Explore memorization vs generalization, including why an LLM can sometimes answer questions it has never seen verbatim.

Post-training

- **The post-training pipeline** — Understand the broad pipeline: Pretraining → Supervised Fine-Tuning → Preference / Reinforcement Training → Deployed Assistant.
- **SFT, RLHF & preference optimization** — Understand **SFT**, **RLHF**, **RLAIF**, preference optimization at a conceptual level, and safety tuning.
- **Why chat models behave as they do** — Connect post-training to why chat models follow instructions, answer conversationally, refuse certain requests, hedge, structure answers, and ask for clarification.

**Try it** · Compare a base model and an instruction-tuned model using identical prompts.

**Outcome** · Explain why a pretrained model may know a lot while still being a poor conversational assistant.

### 05 · How LLM Inference Works (M1.5 · 1 session)

- **What happens after you send a prompt** — Understand what happens after sending a prompt to an LLM API: Prompt → process input → predict token → generate token → repeat.
- **Prefill vs decode** — Distinguish prefill, where the model processes the input/context, from decode, where new tokens are generated one by one.
- **Tokens, TTFT & total latency** — Understand input tokens, output tokens, time to first token (**TTFT**), tokens per second, and total latency.
- **KV caching** — Build intuition for **KV** caching and why the model does not need to recompute the entire conversation from scratch after every generated token.
- **Why inference mechanics drive cost** — Connect inference mechanics to latency, cost, long prompts, long outputs, and reasoning models.

**Outcome** · Explain why generating 2,000 output tokens usually takes much longer than generating 50 tokens even with the same input.

### 06 · Sampling & Generation Parameters (M1.6 · 1 session)

- **From probabilities to a chosen token** — Start from the model's next-token probability distribution and ask: which token should actually be generated?
- **Temperature, top-p, top-k & penalties** — Understand greedy decoding, temperature, top-p, top-k, maximum output tokens, stop sequences, and repetition/frequency/presence penalties where supported.
- **Matching randomness to the task** — Understand task-dependent randomness: lower randomness for extraction, structured output, classification, and factual QA; higher randomness for brainstorming, creative writing, and diverse alternatives.
- **Differences across model APIs** — Understand that different model APIs expose different controls and that some reasoning models provide less direct control over traditional sampling parameters.

**Try it** · Run the same prompt at several temperature settings and compare consistency, creativity, and correctness.

**Outcome** · Choose sensible generation settings based on the task instead of changing temperature arbitrarily.

### 07 · Reasoning Models & Test-Time Compute (M1.7 · 1 session)

- **Why some models think longer** — Understand why some models spend substantially more compute before producing an answer.
- **Test-time compute & thinking budgets** — Build intuition for test-time compute, reasoning effort, thinking budgets, and internal reasoning tokens/compute.
- **Where reasoning helps** — Identify tasks where reasoning tends to help: difficult mathematics, complex coding, planning, multi-step logic, and constraint-heavy problems.
- **Where reasoning is unnecessary** — Identify tasks where it may be unnecessary: sentiment classification, simple extraction, rewriting, and straightforward summarization.
- **The quality / cost / latency trade-off** — Understand the trade-off: more reasoning can improve quality but generally increases cost and latency.
- **Prompting reasoning models** — Adapt prompting for reasoning models: move away from relying on “think step by step” and instead clearly state the goal, provide relevant context, specify constraints, and define what a good answer looks like.

**Try it** · Run the same problems through a fast general model and a reasoning model; compare accuracy, latency, and cost.

**Outcome** · Recognize when paying for extra reasoning compute is likely to be worthwhile.

### 08 · The Context Window (M1.8 · 1 session)

- **What occupies the context window** — Understand what the context window is and what can occupy it: system instructions, conversation history, user prompts, documents, examples, tool outputs, and generated content.
- **Context ≠ knowledge ≠ memory** — Distinguish context ≠ model knowledge ≠ long-term memory.
- **What goes wrong in long contexts** — Understand what can happen with very long contexts: truncation, attention degradation, lost-in-the-middle effects, and context dilution.
- **Why a big window is not enough** — Understand why a model supporting a huge context window does not mean it can use every token equally well.

**Try it** · Place an important fact near the beginning, middle, and end of a long document and compare retrieval performance.

**Outcome** · Decide whether a task needs a larger-context model or a better strategy for selecting what enters context.

### 09 · LLM Capabilities & Failure Modes (M1.9 · 1 session)

- **Common strengths** — Understand common strengths: summarization, text transformation, extraction, classification, semantic understanding, coding, translation, brainstorming, working with unstructured information, and few-shot adaptation.
- **Common failure modes** — Understand common failure modes: hallucination, arithmetic mistakes, brittle reasoning, instruction-following failures, prompt sensitivity, context failures, outdated knowledge, nondeterminism, and confident incorrect answers.
- **Why hallucination happens** — Understand hallucination mechanistically: an LLM is trained to generate a likely continuation, not to independently verify that every generated statement is true, which makes fluent incorrect answers possible.
- **Asking "how reliably?" instead of "can it?"** — Adopt the engineering question: instead of “Can GPT do this?”, ask “How reliably does this model perform this task under the conditions of my application?”

**Try it** · Create 10 questions where the model knows the answer, probably does not know it, receives misleading information, or receives insufficient information; observe how confidence changes.

**Outcome** · Predict which tasks are naturally well suited to LLMs and which require additional safeguards.

### 10 · Understanding the Model Landscape (M1.10 · 1 session)

- **Closed and API models** — Understand closed/API models through trade-offs involving frontier capability, convenience, infrastructure, privacy, vendor dependence, and control.
- **Open-weight models** — Understand open-weight models through self-hosting, privacy, customization, infrastructure requirements, and operational complexity.
- **Managed platforms & hosted open weights** — Understand the third path between them: managed platforms such as AWS Bedrock, Google Vertex AI, and Azure AI Foundry serve both closed and open-weight models inside your own cloud account, and inference providers host open weights for you without any hardware of your own.
- **Other useful distinctions** — Learn other useful distinctions: small vs large, dense vs Mixture-of-Experts, general-purpose vs specialized, reasoning vs non-reasoning, and text-only vs multimodal.
- **There is no universally best LLM** — Internalize the core principle: there is no universally best LLM; the best model depends on the workload.
- **Knowledge cutoffs** — Understand that a model's knowledge stops at its training cutoff, and that anything newer has to arrive through context, retrieval, or tools.
- **Versions, snapshots & deprecations** — Track model versions and dated snapshots, and expect deprecations: the model behind a familiar name can change or be retired, so pin a version and re-test when it moves.
- **Open-weight licensing** — Check the license before building on an open-weight model, since permissive, restricted-use, and non-commercial terms differ in what you are allowed to ship.

**Outcome** · Compare two models using meaningful architectural, capability, and deployment differences rather than relying purely on leaderboard rank.

### 11 · Benchmarks & Leaderboards (M1.11 · 1 session)

- **What a benchmark is** — Understand what a benchmark is: a fixed set of tasks with a fixed scoring method, used to measure different models against the same yardstick.
- **Benchmarks quoted on model cards** — Recognize the benchmarks quoted on model cards — knowledge and reasoning tests such as **MMLU** and **GPQA**, coding tests, and mathematics tests — and know roughly what each one measures.
- **Kinds of leaderboard** — Read the main kinds of leaderboard: human-preference rankings such as LMArena/Chatbot Arena, aggregated capability/cost/latency dashboards, and open-model leaderboards.
- **Why rank does not transfer** — Understand why a leaderboard rank rarely transfers to your application: different prompts, different tasks, averaged scores, and someone else's definition of a good answer.
- **What inflates published scores** — Understand the pitfalls that inflate published scores: data contamination, saturated benchmarks, overfitting to public test sets, and favorable run configurations.
- **From leaderboard to shortlist** — Use benchmarks and leaderboards for the one thing they do well — narrowing a crowded field to a shortlist — and then judge the shortlist on your own examples.

**Try it** · Shortlist three models from a leaderboard for a task you care about, then compare their published scores against how they perform on ten of your own examples.

**Outcome** · Read benchmark tables and leaderboards without being misled by them, and turn them into a shortlist rather than a decision.

### 12 · Choosing the Right Model (M1.12 · 1 session)

- **Eight dimensions for model choice** — Evaluate models across eight dimensions:
- **Capability** — Capability: Can it perform the task at all?
- **Quality** — Quality: How reliably does it perform your specific task?
- **Latency** — Latency: How quickly does it respond?
- **Cost** — Cost: What will each request cost at your expected usage?
- **Context** — Context: Can it accommodate the required input?
- **Modalities** — Modalities: Do you need text, images, audio, or video?
- **Privacy & deployment** — Privacy & deployment: Can you use an external API, do you need a managed platform inside your own cloud, or do you require self-hosting?
- **Product features** — Product features: Do you require structured outputs, function calling, tools, streaming, or caching?
- **Reading model cards & pricing pages** — Learn to critically read model cards, benchmark tables, pricing pages, context-window specifications, and API documentation.
- **Why benchmarks alone are not enough** — Understand why benchmark scores alone should not determine model selection.
- **The selection workflow** — Follow the workflow: Define task → Identify requirements → Shortlist models → Test on your own examples → Measure quality → Measure latency → Measure cost → Inspect failures → Choose the model.

**Outcome** · Select models based on application requirements and empirical performance rather than popularity or leaderboard position.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [3Blue1Brown — Neural Networks series](https://www.3blue1brown.com/topics/neural-networks) — visual intuition for embeddings, attention and how models learn.
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — the classic visual walkthrough of tokens, embeddings, queries, keys and values.
- [Andrej Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — build GPT from scratch; the deepest free intuition for next-token prediction.
- [Google Machine Learning Crash Course — LLM module](https://developers.google.com/machine-learning/crash-course/llm) — concise free coverage of language models, transformers and text generation.
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) — free course from tokenizers to pretraining, fine-tuning and inference.
- [Turing Post — free LLM courses roundup](https://www.turingpost.com/p/llms-courses) — curated, regularly updated list of free university and industry LLM courses.
- [OpenAI and Anthropic model documentation](https://platform.openai.com/docs/models) and [Claude models overview](https://docs.anthropic.com/en/docs/about-claude/models/overview) — primary sources for model cards, context windows, pricing and capabilities.
- [LMArena (Chatbot Arena)](https://lmarena.ai/) — live human-preference leaderboard; practice reading rankings critically.
- [MMLU-Pro / GPQA / SimpleQA benchmark pages on Hugging Face](https://huggingface.co/datasets?search=gpqa) — inspect what popular benchmarks actually measure.

## In this repository

- [LLM Literacy — LLM 101 curriculum (8 notes)](../../101_LLM-Literacy/README.md)
- [Transformer architecture note](../../101_LLM-Literacy/01-LLM%20101/2.%20Transformer%20Architecture%20%28System%20Layer%29.md)
- [Tokenization & embeddings note](../../101_LLM-Literacy/01-LLM%20101/3.%20Tokenization%20%26%20Embeddings%20%28Representation%20Layer%29.md)

---

[← Level 0 · Software Engineering Fundamentals](level-00-software-engineering-fundamentals.md) | [Roadmap map](README.md) | [Level 2 · Working with LLM APIs (Orchestration) →](level-02-working-with-llm-apis.md)
