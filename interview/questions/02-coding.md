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

---

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
- **Build a tool-calling agent**: Implement an agent that can use 2–3 tools to answer queries
- **Build an evaluation pipeline**: Given a set of model outputs, implement automatic evaluation
- **Implement guardrails**: Add input/output filtering to an existing LLM pipeline
- **Build a semantic cache**: Implement a cache that returns semantically similar responses

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
