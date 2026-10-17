# Level 4 · RAG

> **Phase 2 · Retrieval** · 15 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/4/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Build the retrieval layer that RAG depends on — ingestion, chunking, embeddings, vector search, and hybrid retrieval — then ground LLMs in external knowledge, improve retrieval quality, and learn the major RAG architectures used beyond a naive retrieve-and-generate pipeline.

*Short on time? Do the 32-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 10/10**

The **most frequently asked topic** and the most common requirement in job descriptions. Expect detailed questions on chunking, embeddings, hybrid search, reranking, and why retrieval fails. You need to be **very strong here**.

**On-the-job weight: 9/10**

Most business AI products need answers **grounded in company data**. A lot of real work goes into **fixing bad retrieval, stale data, and messy documents**.

---

## Modules

### 01 · Data ingestion & document processing (M4.1 · 2 sessions)

- **Extracting from PDFs, HTML & DOCX** — Extract content from common sources such as **PDFs**, **HTML**, **DOCX**, and structured documents; understand when **OCR** is required.
- **Cleaning while keeping structure** — Clean and normalize messy text while preserving useful document structure and metadata.
- **Duplicates, updates & re-indexing** — Handle duplicate documents, document updates, and incremental re-indexing.

**Outcome** · Convert a real-world document collection into clean, structured data ready for retrieval.

### 02 · Chunking strategies (M4.2 · 2 sessions)

- **Why documents must be split** — Understand why documents must usually be split before embedding and retrieval.
- **Fixed, recursive, structural & semantic** — Apply fixed-size, recursive, structural, and semantic chunking.
- **Size, overlap, boundaries & metadata** — Reason about chunk size, overlap, boundaries, and metadata and how they affect retrieval quality.
- **Precise chunks vs context-rich chunks** — Understand the trade-off between small precise chunks and larger context-rich chunks.

**Outcome** · Choose a sensible chunking strategy based on document structure and query type.

### 03 · Embeddings fundamentals (M4.3 · 2 sessions)

- **What an embedding represents** — Understand embeddings as vector representations that capture semantic relationships between text.
- **Generating embeddings** — Generate embeddings for documents and queries using an embedding model.
- **Choosing an embedding model** — Understand dimensions, embedding model choice, multilingual/domain performance, cost, and latency trade-offs.
- **Vector spaces cannot be mixed** — Understand that embeddings from different models/vector spaces generally cannot be mixed directly.

**Outcome** · Select and use an embedding model appropriate for a retrieval task.

### 04 · Similarity & semantic search (M4.4 · 2 sessions)

- **Cosine, dot product & Euclidean** — Understand cosine similarity, dot product, and Euclidean distance and how they are used to compare vectors.
- **Semantic search from scratch** — Build a simple semantic-search system from scratch: query → embedding → similarity → top-k results.
- **Semantic similarity vs keyword match** — Understand the difference between semantic similarity and exact keyword matching.
- **Where semantic search fails** — Explore common failure cases such as exact names, IDs, numbers, and rare terminology.

**Outcome** · Build semantic search without relying on a vector database and understand exactly what the database will later automate.

### 05 · Vector databases & ANN search (M4.5 · 3 sessions)

- **Storing vectors in pgvector or Qdrant** — Store embeddings, documents, IDs, and metadata in a vector database such as **pgvector** or **Qdrant**.
- **Top-k search with metadata filters** — Perform top-k vector search with metadata filtering.
- **Why ANN search exists** — Understand why brute-force search becomes expensive at scale and why Approximate Nearest Neighbor (**ANN**) search exists.
- **HNSW & IVF trade-offs** — Build intuition for **HNSW** and **IVF** and their speed ↔ memory ↔ recall trade-offs without going deep into implementation mathematics.
- **Indexing, updates & deletes** — Understand indexing, updates, deletes, and basic operational considerations.

**Outcome** · Build and query a scalable vector-search index over a real corpus.

### 06 · Sparse & hybrid retrieval (M4.6 · 2 sessions)

- **Lexical retrieval & BM25** — Understand traditional lexical retrieval and **BM25**, and why keyword search can outperform embeddings for some queries.
- **Sparse vs dense retrieval** — Compare sparse/**BM25** retrieval with dense/vector retrieval.
- **Hybrid retrieval with RRF** — Combine dense and sparse results using hybrid retrieval and techniques such as Reciprocal Rank Fusion (**RRF**).
- **When hybrid retrieval helps** — Understand when hybrid retrieval helps, especially for queries containing names, technical terms, IDs, numbers, and exact phrases.

**Outcome** · Choose between dense, sparse, and hybrid retrieval rather than defaulting to vector search for every problem.

### 08 · RAG architecture & when to use it (M4.8 · 1 session)

- **The core RAG pipeline** — Understand the core pipeline: query → retrieve → assemble context → generate answer.
- **What RAG solves** — Understand what RAG solves: private knowledge, frequently changing information, large knowledge bases, and source-grounded answers.
- **When not to use RAG** — Know when not to use RAG: when the model already knows enough, the task is purely transformational, or the required knowledge can simply fit in context.
- **Retrieval failure vs generation failure** — Distinguish retrieval failure from generation failure.

**Outcome** · Decide whether a problem genuinely needs RAG.

### 09 · Baseline RAG from scratch (M4.9 · 2 sessions)

- **Building the pipeline by hand** — Build a complete **RAG** pipeline manually using the retrieval system built earlier in this level.
- **Retrieve, assemble, generate** — Retrieve top-k chunks, assemble them into the prompt, and generate an answer grounded in the retrieved context.
- **Prompting for grounded answers** — Design prompts that instruct the model to answer from supplied evidence and avoid unsupported claims.
- **Handling weak or missing context** — Handle cases where retrieval returns weak, irrelevant, or insufficient context.
- **The effect of k and chunk ordering** — Understand the effect of k, chunk ordering, and total context size on answer quality.

**Outcome** · Build a working RAG application without hiding the mechanics behind a framework.

### 10 · Reranking (M4.10 · 2 sessions)

- **Retrieve many, rerank, send the best** — Understand the two-stage pattern: retrieve many candidates → rerank → send the best chunks to the LLM.
- **Cross-encoder & reranking models** — Use cross-encoder or dedicated reranking models to reorder retrieved chunks.
- **Relevance gained, latency added** — Understand why reranking can improve relevance while adding latency and cost.
- **When reranking adds little** — Compare retrieval with and without reranking and understand when reranking provides little benefit.

**Outcome** · Improve the quality of context sent to the LLM without simply increasing the number of retrieved chunks.

### 11 · Query transformation & RAG-Fusion (M4.11 · 2 sessions)

- **Why the user question is a poor query** — Understand why the user's original question is not always the best retrieval query.
- **Rewriting, expansion, multi-query & HyDE** — Apply query rewriting, query expansion, multi-query retrieval, and **HyDE**.
- **RAG-Fusion** — Understand RAG-Fusion: generate multiple queries, retrieve for each, and combine rankings using techniques such as Reciprocal Rank Fusion.
- **Handling ambiguous questions** — Use multiple retrieval queries for ambiguous, multi-faceted, or poorly phrased questions.
- **The extra calls it costs** — Understand the trade-off between improved retrieval and additional LLM calls, latency, and cost.
- **When to skip transformation** — Avoid query transformation when baseline retrieval already performs well.

**Outcome** · Transform difficult user questions into better retrieval queries.

### 12 · Grounding, citations & abstention (M4.12 · 1 session)

- **Answering from evidence** — Generate answers grounded in retrieved evidence rather than unsupported model knowledge.
- **Attaching claims to sources** — Attach claims to their supporting documents/chunks and produce useful source citations.
- **Citations are not grounding** — Understand that having citations is not the same as being grounded; the cited source must actually support the claim.
- **Abstaining on insufficient evidence** — Detect insufficient evidence and respond with an appropriate “I don't know / insufficient information” instead of forcing an answer.
- **Keeping evidence and synthesis distinct** — Keep retrieved evidence and model-generated synthesis clearly distinguishable.

**Outcome** · Produce answers that are traceable to evidence and can abstain when the evidence is insufficient.

### 13 · RAG variants & advanced patterns (M4.13 · 3 sessions)

- **Naive → Advanced → adaptive RAG** — Understand the progression from Naive **RAG** → Advanced **RAG** → adaptive/self-correcting **RAG** architectures.
- **Self-RAG** — Learn **Self-RAG**: retrieval is performed when needed and the model reflects on retrieved evidence and its generated response.
- **CRAG (Corrective RAG)** — Learn CRAG (Corrective RAG): evaluate retrieved evidence and trigger corrective retrieval when the initial results are weak.
- **Adaptive RAG** — Learn Adaptive RAG: dynamically decide whether retrieval is required and which retrieval strategy should be used.
- **Iterative RAG** — Understand iterative **RAG**, where retrieval and generation repeat until enough evidence has been gathered.
- **Multi-hop RAG** — Understand multi-hop **RAG**, where answering requires several retrieval steps or combining evidence from multiple sources.
- **Graph RAG** — Learn Graph RAG: represent entities and relationships as a graph and retrieve/summarize information using graph structure rather than relying purely on vector similarity.
- **When Graph RAG is useful** — Build intuition for when Graph RAG is useful: highly connected knowledge, entity relationships, global questions, and information spread across many documents.
- **Choosing by failure mode, not novelty** — Compare advanced approaches on quality, complexity, latency, cost, and failure mode addressed rather than assuming more advanced **RAG** is always better.

**Outcome** · Recognize major RAG variants and choose an architecture based on why baseline RAG is failing.

### 14 · RAG with frameworks (M4.14 · 1 session)

- **Rebuilding with LlamaIndex or LangChain** — Rebuild the manually created **RAG** pipeline using **LlamaIndex** or **LangChain**.
- **Indexes, retrievers & query engines** — Work with framework abstractions for ingestion, indexes, retrievers, rerankers, query engines, and citations.
- **Framework reranking & query transforms** — Implement common **RAG** improvements such as reranking and query transformation using framework components.
- **Framework vs hand-built** — Compare the framework implementation with the hand-built version on control, development speed, debugging, and complexity.

**Outcome** · Use RAG frameworks productively while still understanding the retrieval and generation mechanics underneath them.

#### Capstone: Build a Hybrid Search Engine (M4.7 · 1 session)

- Ingest, chunk, embed & index a real corpus Ingest and clean a real document corpus, preserve useful metadata, chunk the documents, generate embeddings, and index them in a vector database.
- Dense + BM25 + hybrid retrieval Implement dense search + **BM25** + hybrid retrieval, including metadata filters where useful.
- Deploying a search API or UI Deploy a simple search API/UI that returns the most relevant chunks for a user query.

a working hybrid retrieval system ready to become the retrieval component of a RAG application.

#### Capstone: Deploy an Advanced RAG Application (M4.15 · 1 session)

- A document Q&A app end to end Build a document Q&A application over a real corpus with ingestion, chunking, retrieval, generation, citations, and abstention.
- A baseline plus one real improvement Establish a baseline **RAG** pipeline and add at least one meaningful improvement such as reranking, query transformation, **RAG-Fusion**, hybrid retrieval, or an advanced **RAG** variant.
- Degrading gracefully on weak evidence Handle weak retrieval and insufficient evidence gracefully.
- Tracking latency, tokens & cost Track latency, token usage, and cost across the pipeline.
- Deploying as an API or UI Deploy the application as an API or simple user interface.

a complete RAG application that goes substantially beyond a basic retrieve → stuff context → generate demo.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [DeepLearning.AI — Building and Evaluating Advanced RAG Applications](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) — free short course covering retrieval, reranking and evaluation.
- [LlamaIndex documentation](https://docs.llamaindex.ai/) — ingestion, indexes, retrievers, query engines and RAG pipelines.
- [LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/) — build a RAG pipeline with chunking, embeddings and generation.
- [Qdrant documentation and tutorials](https://qdrant.tech/documentation/) — vector search, payload filters and hybrid retrieval.
- [pgvector (GitHub)](https://github.com/pgvector/pgvector) — vector similarity search inside PostgreSQL.
- [Unstructured (GitHub)](https://github.com/Unstructured-IO/unstructured) and [Docling (GitHub)](https://github.com/docling-project/docling) — layout-aware document parsing for messy PDFs and tables.
- [Sentence Transformers documentation](https://sbert.net/) — generating and working with open embedding models.
- [MTEB leaderboard](https://github.com/embeddings-benchmark/mteb) — compare embedding models on retrieval tasks.
- [Microsoft GraphRAG (GitHub)](https://github.com/microsoft/graphrag) — reference implementation of graph-based retrieval.
- [LangChain — RAG tutorial](https://python.langchain.com/docs/tutorials/rag/) — official end-to-end retrieval tutorial; and the [Hugging Face Open-Source AI Cookbook's advanced RAG recipes](https://huggingface.co/learn/cookbook/en/advanced_rag) for query-transformation techniques.

## In this repository

- [Vector databases curriculum](../../102_AI-Application-Development/02-Vector%20Databases/1.%20Introduction%20to%20Vector%20Databases.md)
- [Complete RAG curriculum (7 notes)](../../102_AI-Application-Development/03-RAG/README.md)
- [Advanced RAG patterns note](../../102_AI-Application-Development/03-RAG/5.%20Advanced%20RAG%20Patterns%20%28GraphRAG%2C%20Self-RAG%2C%20Corrective%20RAG%29.md)

---

[← Level 3 · Prompt Engineering](level-03-prompt-engineering.md) | [Roadmap map](README.md) | [Level 5 · AI Agents →](level-05-ai-agents.md)
