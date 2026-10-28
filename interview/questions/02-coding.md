# Coding Questions

> Coding interviews for AI engineering have evolved significantly. As of September 16, 2026, you're as likely to be asked to build a RAG pipeline or implement an async SSE streaming engine as you are to invert a binary tree. Here's what to expect and how to prepare.

---

## Coding Interview Formats

| Format | Frequency | Duration | What It Tests |
|--------|-----------|----------|---------------|
| Live Coding (traditional) | 60% | 45–60 min | Problem-solving, algorithms, communication |
| AI-Assisted Coding | 25% | 45–60 min | Tool fluency, verification, speed |
| Code Review | 15% | 30–45 min | Reading code, identifying bugs, judgment |
| Take-Home | 45% (separate round) | 2 hrs – 7 days | End-to-end building, documentation, design |

The key insight: **AI engineering coding interviews test a different skill set than traditional SWE interviews.** While you may still encounter algorithm questions at big tech, most AI-native companies are moving toward formats that test your ability to build, debug, and evaluate AI systems.

---

## DSA Problems: What's Still Asked

Traditional data structures and algorithms haven't disappeared entirely. They persist at:

- **Big tech companies** (Google, Amazon, Microsoft) that use standardized interview loops
- **Infrastructure-focused AI roles** (ML platform, model serving, data pipeline)
- **Quantitative AI roles** (Goldman Sachs, Citadel, Two Sigma)

### Most Common DSA Topics for AI Engineers

| Topic | Relevance to AI | Example Question |
|-------|----------------|------------------|
| Arrays & Hashing | High — embedding lookups, token counting | "Count token frequencies across a corpus" |
| Strings | High — tokenization, text processing | "Implement a basic BPE tokenizer" |
| Trees & Graphs | Medium — AST manipulation, dependency graphs | "Find the shortest path in a tool dependency graph" |
| Heaps & Priority Queues | Medium — re-ranking, top-k retrieval | "Return top-k similar documents by embedding distance" |
| Dynamic Programming | Low — rarely directly relevant | Standard LeetCode problems |

**Reality check**: If you're interviewing at Anthropic, OpenAI, LangChain, or most AI startups, you're unlikely to get classic DP problems. If you're interviewing at Google or Amazon, you should still prepare for them.

- **Arrays & Hashing** — "Count token frequencies across a corpus"
  - **A:** Prepare hash-map fluency: `Counter`/`defaultdict`, sets, sliding window, two pointers, prefix sums. In AI interviews this topic arrives dressed as NLP bookkeeping rather than raw LeetCode: count token frequencies across a corpus (one pass with `Counter` — O(n) versus O(n log n) for sort-and-count), build a vocabulary with minimum-frequency cutoffs, deduplicate training rows, or find top-k frequent tokens — LeetCode 347 with a heap or bucket-sort twist. Classic problems to drill: Two Sum, Group Anagrams, Longest Substring Without Repeating Characters, Product of Array Except Self, Contains Duplicate. Differentiators: complexity talk (amortized O(1) lookups, one-pass counting) and real-text messiness — Unicode normalization, case folding, hashing the normalized token rather than the raw string. This is the highest-yield DSA topic for AI roles: token counting, vocab maps, and id-to-token lookups are all arrays-and-hash-map problems inside production AI code.

- **Strings** — "Implement a basic BPE tokenizer"
  - **A:** Strings prep means slicing, two pointers, sliding windows, regex fluency, and Unicode awareness (code points versus grapheme clusters). The signature AI-flavored ask is "implement a basic BPE tokenizer": pre-tokenize text into words with a regex, count adjacent symbol pairs weighted by word frequency, merge the most frequent pair into a new symbol everywhere, and repeat until the vocabulary target; encoding replays the learned merges in rank order. Typical problems: Valid Anagram, Longest Palindromic Substring, Longest Substring Without Repeating Characters, String to Integer (atoi). Expect edge-case follow-ups: empty strings, emojis spanning multiple code points, casing, and how byte-level BPE eliminates UNK tokens by decomposing any unseen string into raw bytes. Production nuance: you never ship a hand-rolled tokenizer — use Hugging Face `tokenizers` or `tiktoken` — but interviewers want the merge-loop mechanics and the train-versus-encode distinction cold. Practice by training a tiny BPE on a text file and printing the merge table.

- **Trees & Graphs** — "Find the shortest path in a tool dependency graph"
  - **A:** Prepare BFS/DFS, adjacency lists, topological sort, Dijkstra, and Union-Find. In AI loops, graphs appear as systems rather than puzzles: "find the shortest path in a tool dependency graph" is BFS over an adjacency list — nodes are tools, edges are dependencies, unweighted so BFS suffices — with a visited set plus a parent map to reconstruct the path, and cycle detection because real dependency graphs can be cyclic. Sibling asks: topological sort for tool initialization order (Kahn's algorithm popping in-degree-zero nodes; a cycle exists if the output is shorter than the node count) and AST traversal for code analysis. Classic problems: Number of Islands, Clone Graph, Course Schedule I and II, level-order traversal, Lowest Common Ancestor. Follow-up flexes: bidirectional BFS, iterative DFS to dodge recursion limits, memoization on DAGs. Big tech asks these near-verbatim; AI-native companies frame them around agent tool graphs, MCP server dependencies, and workflow DAGs.

- **Heaps & Priority Queues** — "Return top-k similar documents by embedding distance"
  - **A:** Prepare Python's `heapq` (`heapify`, `heappush`/`heappop`, `nlargest`/`nsmallest`) and the size-k heap pattern. The canonical AI question — "return top-k similar documents by embedding distance" — is O(N log k) with a heap of size k: stream the N scores, keep the k smallest, evict the worst on overflow; `heapq.nsmallest(k, scores)` is the idiomatic one-liner. Tie it back to retrieval: top-k selection is exactly the post-ANN reranking step, and `torch.topk` on GPU is the production answer. Typical problems: Top K Frequent Elements, K Closest Points to Origin, Merge k Sorted Lists, Kth Largest Element in a Stream, Find Median from Data Stream. Follow-ups that decide hires: heap versus sort when k approaches N (sort wins), streaming and incremental updates, tie-breaking, and why `heapify` is O(N). Know the complexity table cold — that is what actually gets probed.

- **Dynamic Programming** — Standard LeetCode problems
  - **A:** Lowest-priority topic for AI engineering loops — budget accordingly. Targeting Anthropic, OpenAI, LangChain, or AI startups: classic DP essentially never appears; from-scratch ML components and system design crowd it out. Facing standardized loops at Google, Amazon, Microsoft, or quant firms: learn the core patterns — 1-D (House Robber, Coin Change), grids (Unique Paths, Minimum Path Sum), sequences (Longest Common Subsequence, Longest Increasing Subsequence, Edit Distance — the one DP with genuine NLP relevance, underlying fuzzy matching and diffs), knapsack, Word Break, Decode Ways. The method interviews reward: define the state, write the recurrence, pin base cases, choose memoization versus tabulation, then compress space with rolling rows. Drill 10–15 mediums, skip hards. The honest October 2026 answer: DP is a big-tech checkbox, not a daily AI-engineering skill — over-preparing it steals time from attention, RAG, and agent-building practice, which is what actually gets asked.

## ML Implementation: From-Scratch Coding

This is the most distinctive coding format in AI engineering interviews. You're asked to implement a core ML/LLM component from scratch, usually in Python, without using high-level libraries.

### Common From-Scratch Questions

| Component | Difficulty | Frequency | Time |
|-----------|-----------|-----------|------|
| Self-attention mechanism | Hard | High | 30–40 min |
| Multi-head attention | Hard | Medium | 40–50 min |
| LoRA adapter | Medium | Medium | 20–30 min |
| KV cache | Medium | Medium | 20–30 min |
| Simple autograd engine | Hard | Low | 40–60 min |
| Embedding layer | Easy | Medium | 15–20 min |
| Tokenizer (BPE) | Medium | Medium | 25–35 min |
| Cosine similarity search | Easy | High | 15–20 min |
| Temperature sampling | Easy | High | 10–15 min |
| Beam search | Medium | Low | 25–35 min |
| Simple RAG pipeline | Medium | High | 30–40 min |
| Tool-calling parser | Medium | Medium | 20–30 min |
| Async SSE Streaming & Abort Handler | Medium | High | 20–30 min |

- Implement self-attention from scratch in PyTorch.
  - **A:** The whole mechanism is softmax(Q @ K^T / sqrt(d_k)) @ V. Given x of shape (B, T, C): project Q = x @ Wq, K = x @ Wk, V = x @ Wv, each (B, T, C). Scores = Q @ K.transpose(-2, -1) / sqrt(d_k), giving (B, T, T); apply a causal mask by setting future positions to -inf (`torch.tril` or `masked_fill`) so softmax assigns them zero weight; softmax over the last dimension; out = attn @ V, back to (B, T, C); then the output projection W_o. The sqrt(d_k) scaling keeps logits near unit variance — omit it and softmax saturates and gradients vanish. Multi-head version: reshape Q, K, V to (B, h, T, C/h) via `view` + `transpose(1, 2)`, run identical math broadcast across heads, then transpose back and `.contiguous().view(B, T, C)` before W_o — that transpose-before-view step is where candidates crash. Interview flags: mask before softmax, softmax dim=-1, scale by head_dim, not embed_dim.

- Implement multi-head attention from scratch in PyTorch.
  - **A:** Multi-head attention runs h attention functions in parallel on channel slices and concatenates the results — shape choreography is the entire question. From x of (B, T, C): one big q/k/v projection (C to C — equivalent to h small projections, but a single matmul), then split: `q.view(B, T, h, d_h).transpose(1, 2)` gives (B, h, T, d_h) with d_h = C/h. Per head: scores = q @ k.transpose(-2, -1) / sqrt(d_h), giving (B, h, T, T); causal mask; softmax(dim=-1); out = scores @ v, giving (B, h, T, d_h). Merge: `out.transpose(1, 2).contiguous().view(B, T, C)`, then the output projection. Why heads: each learns a different relation — positional adjacency, syntax, coreference — in its own subspace; a single head would average them away. Points that score: grouped-query attention shares K/V across head groups to shrink the KV cache (standard in Llama-class models), and the layer wraps residually as x = x + attn(norm(x)) with pre-norm. Classic failure: forgetting `.contiguous()` before `.view()`.

- Implement a LoRA adapter from scratch in PyTorch.
  - **A:** LoRA freezes the pretrained weight W and learns a low-rank update: h = Wx + (alpha/r) * B(A(x)), with A shaped (r, d_in), B shaped (d_out, r), rank r typically 4–64. Implementation essentials: initialize A with Kaiming/uniform random, initialize B to zeros — so the update B @ A starts at exactly zero and fine-tuning begins from the pretrained function; that init asymmetry is the number-one interview detail. Alpha is a scaling hyperparameter, often set to r or 2r; dividing by r decouples update magnitude from rank. Trainables: a 4096x4096 linear at r=16 needs ~131K parameters versus 16.8M — under 1%. Apply to attention projections (q and v minimally; q, k, v, o all works). Production payoffs: adapters are megabyte-scale checkpoints, hot-swappable per task at serving time (keep W resident, add the delta), or mergeable as W' = W + (alpha/r) * B @ A for zero-overhead inference. QLoRA stacks LoRA on a 4-bit quantized base. Gotcha: merging then unmerging accumulates rounding error — multi-adapter servers stay unmerged.

- Implement a KV cache for autoregressive transformer inference.
  - **A:** A KV cache stores previously computed keys and values so each decoding step processes only the new token instead of re-running the whole prefix — without it, generating token T+1 recomputes attention over all T earlier positions, quadratic total work. With it: compute q, k, v for the single new token; append k and v to per-layer caches of shape (B, h, T, d_h); attend as scores = q_new @ K_cached^T / sqrt(d_h), giving (B, h, 1, T), softmax, then multiply by V_cached. Never cache q — queries are per-step. Memory math the interviewer wants: per token = 2 * layers * kv_heads * d_h * bytes; a Llama-7B-class model at fp16 (32 layers, 32 heads, d_h 128) costs ~0.5 MB per token — 2 GB at 4K context. That is exactly why grouped-query and multi-query attention (fewer K/V heads) and PagedAttention (vLLM's paged allocator, eliminating fragmentation) exist. Implementation details: preallocate a max-length buffer, track a write index, invalidate on prompt change, reuse shared prompt prefixes.

- Implement a simple autograd engine from scratch.
  - **A:** Build a scalar reverse-mode autograd (Karpathy's micrograd design): a Value class holding `.data`, `.grad`, a `._backward` closure, and `._prev` parents. Each operation returns a new Value and defines its gradient rule — for multiply, out = Value(a.data * b.data, (a, b)), and out._backward sets a.grad += b.data * out.grad and b.grad += a.data * out.grad. Backward is the chain rule via topological sort: topo-sort the graph, seed the output with .grad = 1.0, call ._backward() in reverse topological order. Two classic bugs: overwriting .grad instead of accumulating with += (a node feeding two paths must sum both) and forgetting to zero grads between steps. Ops needed: add, mul, pow, neg, sub, div (as x * y^-1), exp, log, tanh or relu. Then stack Neuron → Layer → MLP and train with p.data -= lr * p.grad. Extras: why reverse-mode (one pass yields every partial; forward-mode needs one pass per input), PyTorch's dynamic graphs, and no_grad/detach at inference.

- Implement an embedding layer from scratch in PyTorch.
  - **A:** An embedding layer is a trainable lookup table: a weight matrix E of shape (vocab_size, embed_dim), and forward(ids) simply returns E[ids]. From scratch: `self.weight = nn.Parameter(torch.randn(vocab, d) * 0.02)`; indexing with a (B, T) long tensor returns (B, T, d). It is mathematically a linear layer with one-hot input — one_hot @ W selects rows — which is why nn.Embedding is an index operation and why gradients touch only the indexed rows. Details that get probed: indices must be int64; out-of-range indices raise; `padding_idx=0` pins that row to zero so padding stops polluting training; initialization is low-stakes (GPT convention N(0, 0.02)). Extensions worth naming: positional embeddings are the same lookup keyed by position (versus sinusoidal functions of position); weight tying shares E with the output projection to cut parameters; the original Transformer scaled embeddings by sqrt(d_model). Sentence embeddings come from pooling transformer outputs — never the raw table.

- Implement a tokenizer (BPE) from scratch.
  - **A:** BPE builds a subword vocabulary by iteratively merging frequent pairs. Training: (1) pre-tokenize the corpus into words with a GPT-2-style regex (splitting contractions, numbers, punctuation); (2) represent each word as a symbol tuple — bytes for byte-level BPE, so "low" becomes (l, o, w); (3) count adjacent symbol pairs across words, weighted by word frequency; (4) merge the most frequent pair into one symbol everywhere and append it to the ordered merge table; (5) repeat until vocabulary size or a merge cap. Encoding: pre-tokenize, then replay learned merges on each word in rank order (a pair-to-rank dict, always applying the lowest-rank available merge) until none apply; map symbols to ids. Decoding: join symbols, concatenate, undo byte placeholders. Why BPE wins: fixed vocabulary, no UNK — any unseen string decomposes to bytes — and frequent words become single tokens while rare ones stay compositional. Know the train-versus-encode asymmetry cold; ship with HF tokenizers or tiktoken.

- Implement cosine similarity search from scratch.
  - **A:** Cosine similarity is dot(a, b) / (||a|| * ||b||), bounded [-1, 1]. The efficient implementation normalizes once: precompute unit vectors for the corpus (`E /= np.linalg.norm(E, axis=1, keepdims=True)`, plus an eps guard), so similarity collapses to a dot product and the entire search is one matrix-vector product: scores = E_norm @ q_norm, shape (N,). Top-k via `np.argpartition(-scores, k)[:k]` — O(N) selection — or `torch.topk` on GPU; batched queries become Q @ E.T, giving (B, N). Numerical hygiene: consistent float32 (dtype mismatch silently upcasts), zero-vector guard, eps in denominators. The expected interview arc: naive per-pair loop with a sqrt per pair, then vectorize — that contrast is the actual test. Production nuance: OpenAI's text-embedding-3 family returns pre-normalized vectors, so cosine equals dot and cosine distance is 1 - dot; at scale, vector databases approximate this with ANN indexes (HNSW) — exact cosine is for reranking or small corpora. Normalized vectors make cosine, dot, and Euclidean rankings identical.

- Implement temperature sampling from scratch.
  - **A:** Temperature divides logits before softmax: probs = softmax(logits / T). The sampling loop: forward the prompt, take last-position logits of shape (vocab,); apply T; optionally truncate first — top-k keeps the k highest logits, top-p keeps the smallest set whose cumulative probability reaches p — renormalize; draw one index with `torch.multinomial(probs, 1)` or `np.random.choice(len(probs), p=probs)`; append the token; repeat until EOS or max tokens. Behavior: T toward 0 approaches argmax (greedy); T = 1 samples the model's raw distribution; T above 1 flattens toward uniform — creative, noisier. Traps that get probed: T = 0 is division by zero — special-case it to argmax; renormalize after truncation so probabilities sum to one; the Gumbel-max trick (argmax over log-probs plus Gumbel noise) samples stably from log-space; and temperature belongs on logits, before softmax, never on probabilities. Production defaults: extraction and factual RAG at 0–0.3, chat 0.5–0.8, creative copy higher.

- Implement beam search from scratch.
  - **A:** Beam search tracks the B best partial sequences instead of one. State: a list of (tokens, cumulative log-prob). Each step: collect next-token log-probs for every beam, shape (B, vocab); extend all B*V candidates; keep the top B by cumulative score — one topk over the flattened candidate scores, or `heapq.nlargest`. When a beam emits EOS, move it to a finished list; stop when the best finished beam can no longer be beaten, all beams finish, or max length hits; return the top complete sequence. Scoring rules that decide hires: accumulate log-probs, never raw products (underflow), and normalize by length — score divided by length, or the alpha ~0.7 penalty from GNMT — or longer beams always lose. Complexity is O(B * V * T) with a B*V topk per step; B of 3–10, since returns saturate. Standing in 2026: still right for translation and structured output, wrong for open-ended chat — likelihood-maximizing text is repetitive and bland, so temperature and top-p sampling won.

- Implement a simple RAG pipeline from scratch.
  - **A:** Five components: chunker, embedder, index, retriever, generator — plus citation glue. Minimal flow to write live: split documents into ~300–800-token chunks with 10–15% overlap, respecting markdown or code boundaries; embed chunks in batches; store (text, vector, doc_id, chunk_id) — a NumPy matrix for the interview, pgvector or Qdrant in production. At query time: embed the query, take cosine top-k (k = 3–5, never top-1), assemble a prompt with numbered chunks [1]…[k] and a system instruction to answer only from context and cite [n] per claim; generate; parse [n] markers back to chunk and document for the UI. Gotchas that get probed: re-embedding the corpus on every query instead of precomputing at ingest; chunks too big (diluted embeddings) or too small (orphaned context); no refusal path when retrieval is empty; citations that resolve to nothing; no token budget on stuffed context; no error handling on API failure. Name reranking, hybrid BM25, and caching unprompted.

- Implement a tool-calling parser from scratch.
  - **A:** A tool-calling parser converts model output into validated, executable calls. The modern path is native function calling: send tools as name, description, and JSON Schema parameters; the API returns structured `tool_calls`; you execute and feed results back as tool-role messages in a loop. The from-scratch path the interview wants: constrain output to a grammar — a fenced JSON block or an XML-style tag pair (opening tag, JSON payload, closing tag) — then parse in three stages: extract (regex or first balanced JSON blob; a decoder with `raw_decode` tolerates stray prose), validate (pydantic model — unknown tool? missing required field? wrong type? → one retry with the validation error appended, not a crash), and execute (dispatch table mapping name → callable, per-tool timeouts, argument allow-listing, captured errors returned as observations). Loop until a final answer or a max-call cap. Real-world extras: models emit multiple calls per turn (`parallel_tool_calls`), markdown fences, or trailing commas — a json-repair pass is standard; vLLM ships `--tool-call-parser` for self-hosted serving.

- Implement async SSE streaming with an abort handler.
  - **A:** Use FastAPI's `StreamingResponse` wrapping an async generator, with `media_type="text/event-stream"` and headers `Cache-Control: no-cache` (plus `X-Accel-Buffering: no` behind nginx, or proxy buffering kills the stream). Protocol: every event is `data: {json}` plus a blank line — the double newline terminates the event; multi-line payloads must split so each line carries its own `data:` prefix; `data: [DONE]` is the conventional sentinel; comment lines starting with `:` serve as keep-alive heartbeats. Abort handling is the differentiator: `await request.is_disconnected()` inside the loop to break on client disconnect, and catch `asyncio.CancelledError` — Starlette cancels the response task when the client goes away, so catch-and-suppress prevents noisy tracebacks; close the upstream stream rather than leaking it. Use `AsyncOpenAI` — a sync client inside an async generator blocks the event loop and stalls every user. Extras: yield paces the producer (inherent backpressure); `id`/`event` fields enable resumption via `Last-Event-ID`.

### Example: Implement Self-Attention

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.head_dim = embed_dim // num_heads
        
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        self.out_proj = nn.Linear(embed_dim, embed_dim)
    
    def forward(self, x, mask=None):
        B, T, C = x.shape
        
        q = self.q_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(B, T, self.num_heads, self.head_dim).transpose(1, 2)
        
        attn = (q @ k.transpose(-2, -1)) / (self.head_dim ** 0.5)
        
        if mask is not None:
            attn = attn.masked_fill(mask == 0, float('-inf'))
        
        attn = F.softmax(attn, dim=-1)
        out = (attn @ v).transpose(1, 2).contiguous().view(B, T, C)
        
        return self.out_proj(out)
```

**What interviewers look for**: Correctness of QKV computation, scaling by √d_k, masking, reshaping for multi-head, and the ability to explain each step.

---

## AI Coding: Building AI Systems During Interviews

This format asks you to build a functional AI system component during the interview, typically using real APIs or libraries.

### Common AI Coding Questions

- **Build a RAG pipeline**: Given a set of documents, implement retrieval + generation with citations
  - **A:** Components: ingestion (parse → clean → chunk → embed → index), retrieval (embed query → top-k → optional rerank), generation (prompt assembly → LLM → citation parsing), plus evaluation. Minimal working flow: chunk documents (300–800 tokens, 10–15% overlap, respect heading boundaries); precompute and cache embeddings — never re-embed the corpus per query; retrieve top-k = 3–5 by cosine similarity; number the chunks [1]…[k] in the prompt; instruct "answer only from the context, cite [n] after every claim"; parse [n] markers back to source metadata for the UI. Gotchas that separate candidates: chunking (too big dilutes the embedding, too small orphans context — structure-aware beats fixed-size), retrieval (top-1 is the classic bug; add a similarity floor), generation (a refusal path when context is empty; token budgets; streaming), and citations (map markers to real chunk ids — never trust self-citation; verify claims against cited chunks post-hoc). Name reranking, hybrid BM25, semantic caching, and faithfulness evals unprompted.

- **Build a tool-calling agent**: Implement an agent that can use 2–3 tools to answer queries
  - **A:** Core is a loop, not magic: system prompt declaring tools and rules → LLM → either a final answer or tool calls → execute → append results → repeat, capped at 4–8 iterations with a forced-summarize fallback. With two or three tools (search, calculator, database lookup), define each as name, description, and JSON Schema parameters — descriptions are prompts; write them like few-shot examples ("use when the user asks X, requires Y"). Prefer native function calling (the model returns parsed `tool_calls`); a ReAct-style Thought/Action/Observation text loop is the from-scratch fallback. Engineering that gets probed: validate arguments (pydantic), execute with timeouts and sandboxing (tools touch the real world), return errors as observations so the model can self-correct, keep the transcript as the only state, and stop on answer, cap, or no-progress detection. Success depends on tool design: fewer, orthogonal, well-described tools beat a giant toolbox. Extras: parallel calls, human approval gates for side-effecting actions, tracing every hop.

- **Build an evaluation pipeline**: Given a set of model outputs, implement automatic evaluation
  - **A:** Three layers. (1) Golden set: 50–200 real queries with expected outputs or rubrics — sourced from production logs, not imagination. (2) Assertions: exact/contains/regex match for deterministic outputs; JSON schema validation for structured outputs; numeric thresholds for latency and cost per request. (3) LLM-as-judge for open-ended quality: a rubric prompt scoring 1–5 on correctness, relevance, faithfulness — run at temperature 0, and for pairwise comparisons run both orderings to cancel position bias. Driver code is pytest-shaped: for each case, run the pipeline, evaluate, emit pass/fail plus metrics; aggregate pass rate, mean score, p95 latency, cost per eval; fail CI below a threshold. Judge caveats to volunteer: LLM judges drift and prefer verbose answers (G-Eval-style probability weighting helps), so calibrate against ~50 human-labeled examples before trusting them; re-run on every prompt or model change. Store runs (inputs, outputs, scores, versions) in Langfuse, LangSmith, or Braintrust for regression diffs — the pipeline's value is catching regressions before users do.

- **Implement guardrails**: Add input/output filtering to an existing LLM pipeline
  - **A:** Two filters around the model. Input side: classify prompts for injection attempts, jailbreaks, banned topics, and PII (regex + NER — Microsoft Presidio is the standard — plus a fast classifier or Llama Guard); block, redact, or rewrite before the prompt is assembled. Output side: re-run PII redaction on generated text, moderation scoring for toxicity, schema validation when downstream code parses the output, and secret/API-key detection. Architecture is the interview: fail-open versus fail-closed (a guardrail outage should degrade, not take the product down — but a payment-support bot should fail closed), latency budget (regex and small classifiers run inline in microseconds; LLM-based checks add hundreds of milliseconds — run them in parallel with generation or asynchronously on logged output), and audit logging of every block. Nuances: layer cheap deterministic rules before model calls; keep an allow-list escape valve for benign matches (an oncology bot discussing "cancer"); treat prompt injection as an input-classification problem, not keyword matching. Never rely on prompting alone.

- **Build a semantic cache**: Implement a cache that returns semantically similar responses
  - **A:** Structure: precompute normalized embeddings for cached (query, response) pairs; at request time embed the incoming query, run cosine similarity against the cache, and on a hit above threshold — 0.95–0.98 — return the stored response in ~10–50 ms instead of a full LLM call. Miss path: generate, then store (query embedding, response, TTL, tenant, corpus version). Two design decisions dominate: the similarity threshold (0.95 catches paraphrases but risks false hits; 0.98+ is near-exact only — measure false-hit rate, not just hit rate) and key scoping (tenant, model, and corpus version must be part of the key, or you leak answers across customers and serve stale facts after re-indexing). Production notes: 20–40% hit rates are typical for support and docs workloads, and each hit saves the entire generation cost; evict aggressively (TTL plus corpus-version invalidation); audit sampled hits, because a wrong cached answer is deterministically re-served to every similar query. Tools: GPTCache, Redis, LangChain's SemanticCache.

### Example: Build a Simple RAG Pipeline

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

def embed(texts: list[str]) -> np.ndarray:
    response = client.embeddings.create(input=texts, model="text-embedding-3-small")
    return np.array([d.embedding for d in response.data])

def retrieve(query: str, corpus: list[str], top_k: int = 3) -> list[str]:
    query_emb = embed([query])
    corpus_emb = embed(corpus)
    scores = query_emb @ corpus_emb.T
    top_indices = np.argsort(scores[0])[-top_k:][::-1]
    return [corpus[i] for i in top_indices]

def generate(query: str, context: list[str]) -> str:
    context_text = "\n\n".join(context)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Answer based on the provided context. Cite sources."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {query}"}
        ]
    )
    return response.choices[0].message.content

def rag_query(query: str, corpus: list[str]) -> str:
    context = retrieve(query, corpus)
    return generate(query, context)
```

**What interviewers look for**: Understanding of the RAG pipeline structure, correct embedding usage, retrieval quality, prompt design, and awareness of production concerns (caching, error handling, cost).

### Example: Async SSE Token Streaming Endpoint (FastAPI)

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import openai
import json
import asyncio

app = FastAPI()
client = openai.AsyncOpenAI()

async def event_generator(prompt: str, request: Request):
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        async for chunk in response:
            # Check if client disconnected / aborted request
            if await request.is_disconnected():
                break
            delta = chunk.choices[0].delta.content or ""
            if delta:
                payload = json.dumps({"token": delta})
                yield f"data: {payload}\n\n"
        yield "data: [DONE]\n\n"
    except asyncio.CancelledError:
        pass

@app.post("/stream")
async def stream_completion(request: Request, body: dict):
    return StreamingResponse(
        event_generator(body.get("prompt", ""), request),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )
```

**What interviewers look for**: Handling client disconnection (`is_disconnected()`), SSE standard protocol (`data: ...\n\n`), async generator backpressure, and exception handling for cancelled tasks.

---

## AI-Assisted Coding Rounds

A growing number of companies now allow or require AI tool usage during live coding:

### How It Works

- You're given a problem and access to an AI coding assistant (Copilot, Cursor, or ChatGPT)
- You're evaluated on **how you use the tool**, not just whether you get the right answer
- Typical time: 45–60 minutes

### What Interviewers Evaluate

| Criterion | What They Look For |
|-----------|-------------------|
| Prompt quality | Can you write clear, specific prompts? |
| Verification | Do you check AI-generated code for correctness? |
| Debugging | Can you identify and fix errors in AI output? |
| Speed | Do you accomplish more with AI assistance? |
| Judgment | Do you know when AI output is wrong? |
| Integration | Can you incorporate AI suggestions into a larger system? |

### Companies Using This Format (2026)

- **Microsoft**: Explicitly encourages Copilot usage in coding rounds
- **OpenAI**: Tests ChatGPT-assisted problem-solving
- **Exponent**: AI-assisted coding as part of their interview process
- **Various startups**: "Use whatever tools you'd use on the job"

---

## Code Review of AI-Generated Code

The newest coding format: you're given AI-generated code and asked to review it.

### What This Tests

- Can you identify subtle bugs in AI-generated code?
- Do you notice security vulnerabilities?
- Can you improve prompt engineering that led to the code?
- Do you spot performance issues (N+1 queries, unnecessary API calls, missing caching)?
- Can you evaluate code quality (error handling, testing, documentation)?

### Example Review Task

You're given this AI-generated RAG pipeline and asked to find issues:

```python
def rag_query(query, documents):
    # Embed everything every time
    doc_embeddings = [embed(doc) for doc in documents]
    query_embedding = embed(query)
    
    # Find most similar
    similarities = [cosine_sim(query_embedding, d) for d in doc_embeddings]
    best_doc = documents[similarities.index(max(similarities))]
    
    # Generate answer
    response = llm.chat(f"Answer: {query}\nContext: {best_doc}")
    return response
```

**Expected findings**:
1. Re-embedding all documents on every query (should pre-compute and cache)
2. Only retrieving top-1 document (should retrieve top-k)
3. No error handling for empty documents or failed API calls
4. No citation or attribution mechanism
5. No input sanitization or guardrails
6. Prompt is poorly structured (no system message, no clear instructions)
7. No token budget management
8. `cosine_sim` not defined — would need to implement or import

---

## How to Prepare

### Week-by-Week Plan

| Week | Focus | Activities |
|------|-------|-----------|
| 1 | DSA fundamentals | LeetCode Medium — arrays, strings, hash maps (1–2/day) |
| 2 | ML implementation | Implement attention, LoRA, KV cache, tokenizer from scratch |
| 3 | AI coding | Build RAG pipelines, agent systems, evaluation frameworks |
| 4 | AI-assisted coding | Practice with Copilot/Cursor — focus on verification and debugging |
| 5 | Code review | Review AI-generated code, practice identifying issues |
| 6+ | Company-specific | Focus on formats most common at your target companies |

### Key Resources

- **LeetCode**: Still valuable for big tech, but prioritize Medium over Hard
- **Karpathy's "Neural Networks: Zero to Hero"**: Excellent for from-scratch implementations
- **LangChain tutorials**: Good for AI coding practice
- **Your own projects**: The best preparation is having built real AI systems

### Common Mistakes

1. **Over-preparing DSA at the expense of AI coding.** Unless you're targeting Google/Amazon, most AI engineering interviews will test AI-specific coding, not LeetCode Hards.
2. **Not practicing from-scratch implementations.** "Implement attention" comes up frequently and catches candidates off guard.
3. **Ignoring AI-assisted coding practice.** If your target company allows AI tools, practice using them under time pressure.
4. **Not verbalizing your thought process.** In live coding, communication is as important as correctness.
5. **Freezing on API syntax.** Interviewers don't expect you to memorize APIs. Ask to look up documentation — it's how you'd work on the job.

<!-- nav-footer -->
---

**Navigate:** [← 01. Theory](01-theory.md) · [Section hub](../README.md) · [03. Project Deep Dive →](03-project-deep-dive.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
