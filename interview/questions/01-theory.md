# Theory Questions

> Based on 150+ sources including interview reports, company blogs, and practitioner surveys — updated September 16, 2026. Theory questions are the backbone of AI engineering interviews — they test whether you understand *why* AI systems behave the way they do, not just *how* to build them.
> **Expert answers** were added October 27, 2026 — each question now carries a concise, interview-ready answer (`**A:**`).

---

## LLM Practice

### Reasoning Models & Test-Time Compute (2026 Meta)
- How does test-time compute scaling differ from pre-training compute scaling?
  - **A:** Pre-training compute is spent *once* to bake broad capability into the weights — it improves the model for every future query but has diminishing returns and enormous fixed cost. Test-time compute is spent *per request* at inference: the model is allowed to generate longer chains of thought, self-verify, or search over multiple candidate solutions before answering. The same inference budget buys you a stronger effective model on hard problems while letting you pay nothing extra on easy ones. The strategic difference: pre-training scaling raises the floor for everyone; test-time scaling lets one model span a range of capability/latency operating points (e.g., "thinking" vs "non-thinking" modes of the same checkpoint).
- Explain how reinforcement learning with verifiable rewards (RLVR) is used to train reasoning models (e.g., DeepSeek-R1, OpenAI o1/o3).
  - **A:** In RLVR, the reward comes from a *verifier* — code that runs unit tests, checks a math answer against ground truth, or validates format — rather than from a learned reward model that approximates human preference. The model is prompted to emit long chain-of-thought, sampled at temperature, and trajectories whose final answers pass the verifier receive positive reward; policy-gradient updates (PPO/GRPO-style) reinforce the reasoning patterns that produced them. Because the reward can't be gamed by flattering prose, models learn genuinely useful intermediate steps — self-correction, backtracking, decomposition. DeepSeek-R1 demonstrated this can be done with pure RL plus cold-start SFT; o1/o3 use it at frontier scale. Key engineering detail: verifiers exist only for domains with checkable answers (math, code, formal logic), which is why reasoning gains concentrate there.
- What is the difference between an Outcome Reward Model (ORM) and a Process Reward Model (PRM)?
  - **A:** An ORM scores only the *final result* — "is this answer correct?" — cheap to define but credit-assignment-poor: the model gets no signal about *which* reasoning steps were good. A PRM scores *each intermediate step* — "is this step a valid, useful move toward the solution?" — giving dense supervision but requiring expensive step-level labels (often human-annotated or LLM-annotated with known label-noise issues). In practice: ORMs (and verifier-based outcome rewards) dominate RLVR training because they're automatic; PRMs are used at inference time to guide search (best-of-N step scoring, tree search) and to filter training trajectories. A strong interview point: PRM label noise is itself a research problem — annotators agree less on step validity than on final correctness.
- When should you choose a fast standard model (Claude 3.5 Sonnet / GPT-4o) versus an extended reasoning model in production?
  - **A:** Choose the fast standard model when: latency SLAs are tight (chat UX wants first token < 1–2s), the task is language-heavy rather than logic-heavy (extraction, summarization, rewriting, classification), traffic volume makes per-token reasoning cost explode, and the task is within the fast model's demonstrated competence band. Choose extended reasoning when: the task has verifiable structure (math, code, multi-step planning, constraint satisfaction), a wrong answer is far more expensive than a slow one, the request is async anyway (batch jobs, background agents), and you can absorb 10–100× token bills on the hard slice. Production pattern: a router sends easy traffic to the fast model and escalates the hard slice to the reasoner — you get most of the savings with most of the quality.
- How do you handle latency and token billing when using models that generate hidden or extended chain-of-thought tokens?
  - **A:** Three levers. (1) *Billing*: understand your provider's rules — hidden reasoning tokens are billed as output tokens (OpenAI o-series) or sometimes not surfaced at all; budget per request using max_output_tokens / reasoning_effort caps so a hard prompt can't burn unbounded spend; alert on cost-per-request percentiles. (2) *Latency*: expose time-to-first-visible-token rather than total latency, stream the visible portion, and set a client-side timeout that cancels the request — reasoning models can think for minutes. (3) *Tiering*: parameterize reasoning effort (low/medium/high) per request class, route only the hard classes to high effort, and cache repeated reasoning patterns where the provider supports it. Also verify the model still produces a usable partial answer on timeout rather than nothing.

### How LLMs Work
- How do large language models generate text? Walk through the inference process step by step.
  - **A:** (1) The prompt is tokenized into subword IDs via BPE/WordPiece. (2) Each token ID maps to an embedding vector; positional information is added (RoPE and successors). (3) The stack of Transformer blocks runs: each block computes self-attention (queries, keys, values; attention scores softmax-weight the values, letting every token attend to every other) followed by a position-wise MLP, with residuals and normalization. (4) The final hidden state of the last position is projected to vocabulary size, producing logits. (5) A softmax (temperature-scaled) turns logits into a probability distribution. (6) A decoding rule (greedy/sample/top-p) picks the next token. (7) That token is appended and steps 3–6 repeat — one forward pass per token, with the KV cache carrying previous keys/values so past tokens aren't recomputed.
- What is the difference between autoregressive and masked language modeling?
  - **A:** Autoregressive (AR) modeling predicts the next token given only the left context — a causal mask makes each position attend only to earlier positions. It's naturally generative: sampling repeats the prediction. GPT-family and all modern chat LLMs are AR. Masked language modeling (MLM) hides ~15% of tokens and predicts them from *both* sides of context (BERT-style) — bidirectional and great for understanding tasks (classification, NER, embedding) but not directly generative: you can't sample text from it naturally. Modern practice converged on AR because scaling AR on next-token prediction turned out to learn everything MLM could, plus generation; BERT-style encoders survive mostly as embedding models.
- Explain the difference between greedy decoding, beam search, top-k, top-p (nucleus), and min-p sampling.
  - **A:** *Greedy*: always take the argmax token — deterministic but prone to repetition loops and bland text. *Beam search*: keep the k highest-probability partial sequences and return the best full sequence — better for machine translation/formal outputs, but produces generic text in open-ended generation and is mostly obsolete for chat LLMs. *Top-k*: sample only from the k most likely tokens (k=50 typical) — fixed pool regardless of distribution shape. *Top-p (nucleus)*: sample from the smallest set of tokens whose cumulative probability ≥ p (p=0.9–0.95) — adaptive pool size: narrow when the model is confident, wide when uncertain; the default for chat. *Min-p*: keep tokens with probability ≥ min_p × p_max — scales the cutoff with the top token's probability, so it filters junk in confident distributions while keeping diversity in flat ones; claimed to outperform top-p at high temperature.
- What is a logit and how does it relate to probability distributions over vocabulary?
  - **A:** A logit is the raw, unnormalized score a model outputs for each vocabulary token at the final layer — one real number per vocab entry (e.g., 128k–256k of them), computed by projecting the last hidden state through the output (unembedding) matrix. Softmax converts logits to probabilities: p_i = exp(logit_i/T) / Σ exp(logit_j/T), where T is temperature — so logits determine the *shape* of the distribution and T controls its sharpness. Logits are the substrate for everything downstream: greedy takes the max, top-k/top-p truncate the set, logprob-based metrics (perplexity, G-Eval-style probability weighting, classification via token-odds) read them directly. "The model's uncertainty" literally lives in the logit gaps.

### Temperature and Sampling
- What does temperature control in an LLM? What happens at temperature=0 vs temperature=2?
  - **A:** Temperature divides the logits before softmax. T=1 leaves the model's distribution as trained; T<1 sharpens it (big tokens get relatively bigger); T>1 flattens it (small tokens get relatively bigger). At T=0 the softmax collapses to one-hot — pure argmax, fully deterministic (modulo kernel nondeterminism in some serving stacks), best for reproducible evals, extraction, and code, but prone to degenerate repetition. At T=2 the distribution is nearly uniform over plausible tokens — creative but incoherent, with frequent nonsense and token-salad failures; rarely usable. Practical range: 0–0.3 for deterministic pipelines, 0.7–1.0 for chat, 1.0+ only for deliberately divergent brainstorming — and always pair high T with top-p or min-p to chop the tail.
- When would you use a low temperature vs a high temperature in production?
  - **A:** Low (0–0.3): evals where you need reproducibility, structured extraction, classification via label tokens, code generation, SQL generation, any pipeline whose output is parsed or executed — variance is pure risk. High (0.7–1.2): marketing copy, brainstorming, persona-driven conversation, generating diverse candidates for a downstream reranker. The interview-worthy nuance: temperature is an *engineering* decision tied to who consumes the output — machines want determinism, humans tolerate (and sometimes want) variety. Also note temperature interacts with judges: run your LLM-as-a-judge at low temperature, or your metrics themselves become noisy (the CampusX evaluation course's G-Eval variance lesson).
- How do top-k and top-p interact with temperature? What are reasonable defaults for a chatbot vs a code generator?
  - **A:** They compose as successive filters: logits are divided by temperature, then the candidate set is truncated by top-k (fixed count) and/or top-p (cumulative mass), then one token is sampled from what remains. Temperature reshapes the distribution; top-k/top-p delete its tails. Defaults: chatbot — T≈0.7–1.0, top-p≈0.9–0.95 (top-k often disabled); code generator — T≈0–0.2, top-p≈0.9 or greedy entirely, because a single wrong token can break a program while variety buys nothing. Ordering matters conceptually: truncation after temperature scaling means T amplifies or suppresses differences *within* the surviving set.
- What is min-p sampling and why might it be preferred over top-p? [^1]
  - **A:** Min-p keeps only tokens whose probability ≥ min_p × (probability of the top token). Because the cutoff is *relative to the leader*, it auto-adapts: when the model is confident (top token 60%), the bar is high and junk is filtered aggressively; when the distribution is flat (top token 5%), the bar is low and legitimate diversity survives. Top-p instead uses an absolute cumulative-mass cutoff, which at high temperatures can either over-truncate uncertain-but-valid tokens or fail to remove noise. Min-p therefore lets you run higher temperatures (more diverse) without incoherence — reported to beat top-p on creative benchmarks — and it's now exposed by llama.cpp, vLLM, and some APIs. Default ballpark: min_p ≈ 0.05–0.1.

### Context Window and Memory Management
- What is a context window and why does it matter for production systems?
  - **A:** The context window is the maximum number of tokens (prompt + generated output) a model can process in one request — set by architectural choices like positional encoding schemes and attention memory. It matters in production because it is a hard wall: exceed it and the API errors out or silently truncates the start of your prompt. Every design decision flows from it — how much chat history you keep, how many retrieved chunks fit, how long documents can be, and your cost (you pay per token in the window). A 200k-token window does not mean "free memory": long contexts cost quadratic attention time (unless using efficiency tricks), and quality degrades before the hard limit is reached.
- How do you handle conversations that exceed the context window?
  - **A:** Layered strategy: (1) *Trim aggressively* — drop system-boilerplate duplication, cap tool outputs, truncate stale turns. (2) *Summarize* — when the transcript crosses a threshold, replace the oldest N turns with a running summary (summary + recent tail + system prompt). (3) *Externalize to retrieval* — write full history to a store and retrieve only relevant turns per query (the memory becomes RAG over the user's own past). (4) *Compress* — prompt-compression libraries (LLMLingua-style) remove low-information tokens. (5) *Escalate context* — route long-context users to a long-context model variant if economics allow. Production systems usually combine: keep the last K turns verbatim, one rolling summary, and retrieval for anything older.
- Explain sliding window approaches vs. summarization vs. retrieval-based memory.
  - **A:** *Sliding window*: keep only the last N turns, drop everything older — O(1) cost, zero latency, but the model forgets anything beyond the horizon (the user's name stated an hour ago is gone). *Summarization*: periodically compress old turns into a running summary — preserves gist and user facts but loses verbatim details, costs an extra LLM call, and summaries can drift or lose information cumulatively. *Retrieval-based memory*: store every turn (embedded) and retrieve the top-k relevant per request — scales to months of history and recalls specifics, but adds retrieval latency, can fetch the *wrong* memories, and needs hygiene (dedup, recency weighting, PII policy). The trade axis is fidelity vs. cost vs. recall; mature assistants stack all three: verbatim tail + rolling summary + long-term vector memory.
- What is the difference between context window and effective context length?
  - **A:** The context window is the *architectural maximum* — what the positional encoding and memory support (e.g., 1M tokens). Effective context length is the *quality-preserving* span — how far the model actually attends accurately before recall degrades, typically measured by needle-in-a-haystack or RULER-style tasks. A model may accept 128k tokens but effectively reason over only ~32–64k: lost-in-the-middle effects, degraded instruction-following, and weaker cross-document reasoning appear well before the hard limit. Providers now quote both (or get called out by independent long-context benchmarks). Engineering implication: don't fill the window just because it exists — retrieve and pack only what the task needs, and test *your* workload at *your* context lengths rather than trusting the spec sheet.
- How do different models handle long contexts? Compare GPT-4o, Claude, Gemini, and open-source models.
  - **A:** *Gemini* leads on raw size (1M–2M tokens) with decent long-context recall — good for whole-codebase or document-corpus tasks. *Claude* offers 200k with strong effective-length behavior and explicit long-context guidance (prompt caching, citations); a hallmark is high-quality needle retrieval across the full span. *GPT-4o* sits at 128k — smaller but with excellent density of reasoning per token. *Open-source* is split: Llama-class models reach 128k via RoPE scaling (quality varies; community long-context fine-tunes exist), Qwen and DeepSeek push 128k–256k, and MiniCPM/Yi-class experiments go further. All still show lost-in-the-middle and RULER-measured degradation; the practical rule is that frontier models handle "find the fact" at length but "reason across everything" still degrades — so relevance-filtering beats window-stuffing on every family.
- What is "lost in the middle" and how do you mitigate it? [^2]
  - **A:** The empirical finding (Liu et al., 2023) that LLMs recall information at the *beginning* and *end* of the prompt far better than the *middle* — a U-shaped performance curve, likely an artifact of pre-training and positional biases. Mitigations: (1) *Reorder* — place critical instructions and key documents at the start and end of the context, padding filler into the middle. (2) *Retrieve less, better* — rerank so only top few chunks enter the prompt instead of k=20 mediocre ones. (3) *Repeat key instructions* — state the task at both ends. (4) *Decompose* — answer per-document then synthesize, so no single prompt carries everything. (5) *Use long-context-optimized models* — newer models flatten the curve but don't eliminate it. For RAG specifically: relevance-order your chunks (best first) rather than leaving them in retrieval order.

---

## RAG Systems

### Fundamentals
- What is RAG and why has it become the dominant pattern for LLM applications?
- What are the core components of a RAG pipeline?
- How does RAG differ from fine-tuning? When would you choose one over the other?

### Text vs. Vector Search
- What is vector search and how does it differ from keyword/BM25 search?
- When would you use BM25 over dense retrieval? When would you combine them?
- What is hybrid search and why is it often better than either approach alone?
- Explain the role of embeddings in RAG. How do you choose an embedding model?
- What is chunking and why does chunking strategy matter? Compare fixed-size, semantic, and recursive chunking.

### Hallucination Handling
- How do you detect hallucinations in a RAG system?
- What strategies reduce hallucination? (grounding, citations, temperature tuning, chain-of-thought)
- How do you handle "I don't know" — teaching models to refuse when context is insufficient?
- What is the difference between faithfulness and relevance in RAG evaluation?

### Citations and Attribution
- How do you implement citation/attribution in a RAG pipeline?
- What are inline citations vs. end-of-response citations? Trade-offs?
- How do you verify that citations actually support the claims they're attached to?

### Semantic Caching
- What is semantic caching and when is it useful?
- How do you measure cache hit rate for semantic caches vs. exact caches?
- What are the failure modes of semantic caching? When does it hurt more than it helps?

### Scaling to Millions
- How do you scale a RAG system to millions of documents?
- What are the trade-offs between different vector databases at scale? (Pinecone, Weaviate, Qdrant, Milvus, pgvector)
- How do you handle real-time document updates in a RAG pipeline?
- What is the role of approximate nearest neighbor (ANN) search in scaling RAG?

### Trade-offs
- Latency vs. retrieval quality: how do you navigate this trade-off?
- Cost vs. accuracy: when is a cheaper model with more context better than an expensive model with less?
- Freshness vs. consistency: how do you handle documents that change frequently?

---

## Agents and Tool Use

### What Makes Systems Agentic
- What distinguishes an agentic system from a standard LLM pipeline?
- Explain the spectrum from zero-shot prompting → chain-of-thought → ReAct → full autonomy.
- When are agents the wrong choice? What problems are better solved with simpler pipelines?

### Essential Components
- What are the essential components of an agent system? (planning, tool use, memory, observability)
- How do you design a tool interface that an LLM can reliably use?
- What is tool selection and how do you handle the case where multiple tools could apply?
- How do you manage agent state across multiple turns and tool calls?

### When Agents Go Wrong
- What are the common failure modes of agent systems? (infinite loops, tool misuse, compounding errors, hallucinated tool calls)
- How do you prevent infinite loops in agent systems? (max iterations, budget limits, loop detection)
- How do you handle agent systems that spiral — making errors that compound with each step?

### Sandboxing and Security
- Why is sandboxing important for agent systems that execute code?
- What are the security risks of giving LLMs tool access? (prompt injection via tool output, data exfiltration, privilege escalation)
- How do you implement guardrails for agent systems without over-constraining them?
- What is the principle of least privilege and how does it apply to agent tool design?

### Agent Design Questions
- Design an agent that can research a topic and write a report. What tools does it need? What are the failure modes?
- How would you build a multi-agent system where agents collaborate? What coordination protocol would you use?
- When would you use a single agent with many tools vs. multiple specialized agents?

---

## Context Engineering

> **NEW for 2026**: Context engineering has emerged as a distinct discipline — the art and science of assembling the right information into the model's context window at the right time.

### What Is Context Engineering
- What is context engineering and how does it differ from prompt engineering?
- Why has context engineering become critical as context windows have grown to 1M+ tokens?
- Explain the analogy: "Context engineering is to LLMs what feature engineering was to traditional ML." [^3]

### Context Window Management
- How do you prioritize what goes into a finite context window?
- What is the "attention dilution" problem and how do you mitigate it?
- How do you handle multi-turn conversations without losing important earlier context?
- What is context window budgeting and how do you allocate tokens across system prompt, retrieved context, conversation history, and output space?

### Dynamic Context Assembly
- What is dynamic context assembly and why is it superior to static prompts?
- How do you build a context assembly pipeline that adapts to user queries?
- Explain query-driven context retrieval vs. pre-loaded context vs. hybrid approaches.

### Context Pruning
- What is context pruning and when is it necessary?
- How do you decide what to remove from context without losing critical information?
- What is "context compression" and how does it differ from summarization?
- How do re-ranking models play a role in context pruning?

### Multi-Source Context Fusion
- How do you combine context from multiple sources (RAG, tools, conversation, knowledge graph) without creating contradictions?
- What is the "context collision" problem and how do you resolve it?
- How do you maintain consistency when fusing context from sources with different recency and reliability?

### Context Caching Strategies
- What is prefix caching and how does it reduce latency and cost?
- How do Anthropic's prompt caching and OpenAI's cached responses work?
- When is context caching counterproductive? (frequently changing system prompts, per-user personalization)
- How do you measure cache hit rates and cost savings in production?

---

## Testing and Evaluation

### Consistency
- How do you measure consistency of LLM outputs? Why is it important?
- What is the difference between determinism and consistency in LLM outputs?
- How do you test for regression when updating prompts or models?

### Chatbot Evaluation
- How do you evaluate a chatbot? What metrics matter?
- What is LLM-as-a-judge and what are its biases?
- How do you create a golden dataset for chatbot evaluation?

### Metrics
- What are the standard metrics for evaluating LLM outputs? (BLEU, ROUGE, BERTScore, METEOR — and why most are inadequate)
- What is faithfulness, relevance, and coherence in the context of LLM evaluation?
- How do you measure answer quality when there's no single ground truth?

### Golden Datasets
- What is a golden dataset and how do you build one for AI systems?
- How do you keep golden datasets from going stale as models and prompts change?
- What is the minimum viable evaluation set size?

### Hallucination Detection
- How do you detect hallucinations in production? (self-consistency, entailment scoring, retrieval verification)
- What is the difference between intrinsic and extrinsic hallucinations?
- How do you build a hallucination detection system that doesn't itself hallucinate?

### RAG Evaluation
- What frameworks exist for RAG evaluation? (RAGAS, ARES, DeepEval, TruLens)
- What are the key RAG evaluation dimensions? (context relevance, answer faithfulness, answer relevance)
- How do you evaluate retrieval quality separately from generation quality?

### Agent Evaluation
- How do you evaluate autonomous agent systems? What makes this harder than evaluating single-turn outputs?
- What is trajectory evaluation and how does it work?
- How do you test edge cases in agent systems (tool failures, unexpected inputs, compounding errors)?

---

## Monitoring

### Operational Metrics
- What metrics should you monitor for an LLM application in production? (latency, error rate, token usage, cost, user satisfaction)
- How do you set up alerting for LLM-specific issues (hallucination spikes, cost anomalies, latency degradation)?
- What is "model drift" and how do you detect it?

### Production Evaluation
- How do you continuously evaluate LLM outputs in production without manual review?
- What is shadow evaluation and how does it work?
- How do you A/B test prompts and models in production?

### Model Testing
- How do you test LLM-based features before deployment?
- What is the difference between unit testing, integration testing, and end-to-end testing for AI systems?
- How do you write tests for non-deterministic systems?

### Hallucination Rate
- How do you measure hallucination rate in production?
- What is an acceptable hallucination rate for different applications? (medical: ~0%, search: ~5%, creative: ~20%)
- How do you balance false positives and false negatives in hallucination detection?

### Autonomous Agent Monitoring
- What additional monitoring is needed for autonomous agents vs. single-turn LLM calls?
- How do you track agent trajectories and detect anomalous behavior?
- What is "agent observability" and what tools exist? (LangSmith, Arize, Honeycomb)

---

## Cost and Latency Optimization

### Latency Reduction
- What is Time to First Token (TTFT) and why does it matter for user experience?
- How do you reduce TTFT? (speculative decoding, prefix caching, model distillation, streaming)
- What is the relationship between model size and latency? How do you choose the right model tier?

### Benchmarking
- How do you benchmark LLM performance in production?
- What are the standard benchmarks and why are they often misleading? (MMLU, HumanEval, MT-Bench, Arena)
- How do you create custom benchmarks that reflect your actual use case?

### Token Costs
- How do you estimate and control token costs for an LLM application?
- What is the cost breakdown of a typical RAG pipeline? (embedding, retrieval, generation, caching)
- How do you reduce token costs without sacrificing quality? (prompt optimization, context pruning, model tiering, caching)

### Cost vs. Quality
- When is it worth paying 10x more for a better model? When is a cheaper model sufficient?
- How do you build a model tiering system that routes queries to the cheapest adequate model?
- What is "quality-adjusted cost" and how do you measure it?

### Budget Estimation
- How do you estimate the cost of an AI feature before building it?
- How do you set and enforce token budgets for agent systems?
- What is "cost observability" and how do you implement it?

---

## Safety and Guardrails

### LLM Guardrails
- What are LLM guardrails and why are they necessary?
- How do you implement input and output guardrails? (NeMo Guardrails, Guardrails AI, custom classifiers)
- What is the tension between guardrail strictness and model capability?

### PII Handling
- How do you handle PII in LLM inputs and outputs?
- What is PII detection and redaction? How do you implement it in a pipeline?
- What are the regulatory requirements (GDPR, CCPA, HIPAA) for PII in AI systems?

### Prompt Injection
- What is prompt injection and why is it dangerous?
- What are the different types of prompt injection? (direct, indirect via tool output, jailbreaking)
- How do you defend against prompt injection? (input sanitization, output filtering, system prompt isolation, instruction hierarchy)
- What is the "instruction hierarchy" approach and how does Anthropic implement it? [^4]

### Content Policy
- How do you implement content policy enforcement in an LLM application?
- What is the difference between refusal and redirection?
- How do you handle edge cases where content policy is ambiguous?

### Code Execution Safety
- What are the risks of LLM-generated code execution?
- How do you sandbox code execution for AI systems? (Docker, gVisor, WebAssembly, firecracker)
- What is the principle of least privilege for AI code execution environments?

---

## Fine-Tuning and Training

### When to Fine-Tune
- When should you fine-tune vs. use RAG vs. use prompt engineering?
- What are the hidden costs of fine-tuning? (data collection, evaluation, maintenance, model updates)
- How do you decide between fine-tuning and using a larger model with better prompting?

### Instruction Tuning
- What is instruction tuning and why is it important?
- How do you create an instruction tuning dataset?
- What is the difference between instruction tuning and alignment tuning?

### PEFT / LoRA
- What is Parameter-Efficient Fine-Tuning (PEFT) and why is it important?
- Explain LoRA: how does it work and what are its advantages?
- What is QLoRA and how does it differ from LoRA?
- How do you choose the LoRA rank (r) and alpha parameters?

### RLHF / DPO
- What is RLHF and how does it work? Walk through the three steps.
- What is DPO and why has it become popular as an alternative to RLHF?
- What are the limitations of RLHF? (reward hacking, alignment tax, distributional shift)
- What is constitutional AI and how does Anthropic use it? [^5]

### Quantization
- What is model quantization and why is it important for deployment?
- Compare INT8, INT4, GPTQ, AWQ, and GGUF quantization methods.
- What is the quality-cost trade-off of quantization? When is INT4 acceptable?

### Training Signals
- How do you monitor training of a fine-tuning run? What signals indicate problems?
- What is catastrophic forgetting and how do you prevent it?
- How do you evaluate a fine-tuned model against the base model?

### Math Problem Design
- How do you design training data for mathematical reasoning?
- What is the difference between process reward models and outcome reward models?
- How do chain-of-thought and reasoning models change training data requirements?

---

## LLM Theory

### Transformers and Self-Attention
- Explain the transformer architecture. Why did it replace RNNs and LSTMs?
- How does self-attention work? Walk through the Q, K, V computation.
- What is multi-head attention and why is it important?
- What is the computational complexity of self-attention? How does it scale?

### Encoder vs. Decoder
- What is the difference between encoder-only, decoder-only, and encoder-decoder models?
- Why have decoder-only models (GPT, Claude, Llama) become dominant?
- When would you still use an encoder-only model (BERT-style)?

### KV Cache
- What is the KV cache and why is it critical for inference efficiency?
- How does KV caching work across multiple tokens and turns?
- What is PagedAttention and how does it improve memory efficiency? [^6]
- How do you handle KV cache for very long sequences?

### Mixture of Experts (MoE)
- What is Mixture of Experts and how does it work?
- Why have MoE models (Mixtral, GPT-4, DeepSeek) become popular?
- What are the trade-offs of MoE? (training efficiency vs. inference complexity, load balancing)
- How does expert routing work and why is it a challenging optimization problem?

### Tokenization
- How does tokenization work? BPE, WordPiece, SentencePiece, Unigram?
- Why does tokenization matter for multilingual models and code generation?
- What are "tokenization artifacts" and how do they affect model behavior?

### Reasoning Models
- What are reasoning models (o1, o3, DeepSeek-R1) and how do they differ from standard LLMs?
- What is chain-of-thought and how does it emerge during training?
- How do reasoning models affect evaluation and deployment? (longer generation, higher cost, latency trade-offs)
- What is test-time compute and why does it matter?

---

## MCP and Agent Protocols

> **NEW for 2026**: The Model Context Protocol (MCP) and Agent-to-Agent (A2A) protocol have emerged as key infrastructure for AI systems. Interviewers at companies building agent platforms are beginning to test knowledge of these protocols.

### What Is MCP
- What is the Model Context Protocol and what problem does it solve?
- How does MCP standardize the way LLMs connect to external tools and data sources?
- Why did Anthropic open-source MCP and what has the adoption looked like? [^7]

### How MCP Servers Work
- Explain the MCP client-server architecture.
- What are MCP resources, tools, and prompts? How do they differ?
- How do you build an MCP server? Walk through the setup process.
- What are the security considerations for MCP servers? (authentication, authorization, data exposure)

### A2A Protocol
- What is the Agent-to-Agent (A2A) protocol and how does it complement MCP?
- How do agents discover each other and negotiate capabilities?
- What are the challenges of agent-to-agent communication? (trust, verification, error handling)
- How does A2A differ from existing orchestration frameworks like LangGraph or CrewAI?

### Tool Discovery
- How does tool discovery work in MCP? How does an LLM know what tools are available?
- What is the role of tool descriptions in MCP and why do they matter for reliability?
- How do you version MCP tools without breaking existing clients?

### Agent Communication
- What patterns exist for multi-agent communication? (hub-and-spoke, peer-to-peer, hierarchical)
- How do you handle partial failures in multi-agent systems?
- What is "agent orchestration" and what are the trade-offs between centralized and decentralized orchestration?

---

## How to Prepare

### Common Mistakes

1. **Memorizing without understanding.** Interviewers probe depth. If you memorized "LoRA is parameter-efficient fine-tuning" but can't explain *why* it works, you'll get exposed.

2. **Ignoring production concerns.** Theory questions almost always have a production angle. "How does RAG work?" → "How would you scale RAG to millions of documents with sub-second latency?"

3. **Not knowing the latest.** In 2026, not knowing about context engineering, MCP, or reasoning models signals you're out of date. You don't need to be an expert, but you need awareness.

4. **Over-indexing on one topic.** Some candidates go deep on LLM theory but can't discuss evaluation or cost optimization. Balance your preparation.

5. **Ignoring safety.** Even if you're not interviewing at Anthropic, safety awareness (PII handling, prompt injection, guardrails) is now table stakes.

6. **Being too academic.** AI engineering is applied. If you can derive the attention formula but can't explain when to use RAG vs. fine-tuning in a real product, you'll struggle.

7. **Not having opinions.** Interviewers want to see that you've formed opinions through experience. "It depends" is fine, but follow it with the specific factors you'd consider.

### Preparation Strategy

- **Week 1–2**: Cover LLM practice, RAG, and agents. These are the most frequently tested topics.
- **Week 3**: Cover context engineering, evaluation, and monitoring. These are the fastest-growing areas.
- **Week 4**: Cover cost optimization, safety, fine-tuning, and LLM theory based on your target companies.
- **Week 5+**: Practice explaining concepts out loud. Form opinions. Write about what you've learned.

---

## Sources

[^1]: Min-p sampling: "Base Temperature Sampling" discussion, HuggingFace Blog, 2025.
[^2]: "Lost in the Middle: How Language Models Use Long Contexts", Liu et al., 2023. Updated findings in 2025 show the effect persists but is reduced in newer models.
[^3]: "Context Engineering" as a discipline: emerging from practitioner blogs and conference talks, late 2025. Popularized by Tilden Panksepp and others in the AI engineering community.
[^4]: Anthropic instruction hierarchy: "Anthropic's Approach to Prompt Injection Defense", Anthropic Blog, 2025.
[^5]: "Constitutional AI: Harmlessness from AI Feedback", Anthropic, 2022. Updated approach described in Claude 3.5 system card, 2025.
[^6]: "Efficient Memory Management for Large Language Model Serving with PagedAttention", Kwon et al., vLLM, 2023.
[^7]: "Model Context Protocol", Anthropic, November 2024. Adoption data from MCP ecosystem reports, 2025–2026.
[^8]: RAGAS framework: Es et al., 2024. ARES: Saad-Falcon et al., 2024. DeepEval: Confident AI, 2025.
[^9]: NeMo Guardrails: NVIDIA, 2023. Guardrails AI: Guardrails AI, 2024.
[^10]: "LoRA: Low-Rank Adaptation of Large Language Models", Hu et al., 2021.
[^11]: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model", Rafailov et al., 2023.
[^12]: Interview reports aggregated from Blind, Glassdoor, LeetCode Discuss, and candidate blogs, 2025–2026 (~200 unique reports).
[^13]: "Mixture of Experts Explained", various sources including Mistral AI blog and DeepSeek technical reports, 2024–2025.
[^14]: A2A Protocol: Google DeepMind and community specification, 2025–2026.
[^15]: Cost and latency data from LangChain production surveys, Anthropic usage reports, and OpenAI API documentation, 2025–2026.
