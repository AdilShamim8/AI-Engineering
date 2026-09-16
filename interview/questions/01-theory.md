# Theory Questions

> Based on 150+ sources including interview reports, company blogs, and practitioner surveys — updated September 16, 2026. Theory questions are the backbone of AI engineering interviews — they test whether you understand *why* AI systems behave the way they do, not just *how* to build them.

---

## LLM Practice

### Reasoning Models & Test-Time Compute (2026 Meta)
- How does test-time compute scaling differ from pre-training compute scaling?
- Explain how reinforcement learning with verifiable rewards (RLVR) is used to train reasoning models (e.g., DeepSeek-R1, OpenAI o1/o3).
- What is the difference between an Outcome Reward Model (ORM) and a Process Reward Model (PRM)?
- When should you choose a fast standard model (Claude 3.5 Sonnet / GPT-4o) versus an extended reasoning model in production?
- How do you handle latency and token billing when using models that generate hidden or extended chain-of-thought tokens?

### How LLMs Work
- How do large language models generate text? Walk through the inference process step by step.
- What is the difference between autoregressive and masked language modeling?
- Explain the difference between greedy decoding, beam search, top-k, top-p (nucleus), and min-p sampling.
- What is a logit and how does it relate to probability distributions over vocabulary?

### Temperature and Sampling
- What does temperature control in an LLM? What happens at temperature=0 vs temperature=2?
- When would you use a low temperature vs a high temperature in production?
- How do top-k and top-p interact with temperature? What are reasonable defaults for a chatbot vs a code generator?
- What is min-p sampling and why might it be preferred over top-p? [^1]

### Context Window and Memory Management
- What is a context window and why does it matter for production systems?
- How do you handle conversations that exceed the context window?
- Explain sliding window approaches vs. summarization vs. retrieval-based memory.
- What is the difference between context window and effective context length?
- How do different models handle long contexts? Compare GPT-4o, Claude, Gemini, and open-source models.
- What is "lost in the middle" and how do you mitigate it? [^2]

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
