# Awesome AI Engineering

A curated collection of interview preparation, books, implementation guides, datasets, evaluation tools and engineering references.

**Link review: October 9, 2026.** Every external destination retained below was fetched successfully during this review. Links use canonical repository locations, including verified redirects. The review date describes link checking, not a new publication date for the resources.

The previous list contained nonexistent repositories, placeholder discussion identifiers and unverified article paths. Those references have been replaced with checked resources whose descriptions match their contents. Availability does not certify a resource's advice or every link inside it.

## Interview preparation

- [AI Engineering Field Guide — original project](https://github.com/alexeygrigorev/ai-engineering-field-guide) — Job-posting research and interview materials; inspect the underlying records and methodology before quoting statistics.
- [Introduction to Machine Learning Interviews](https://github.com/chiphuyen/ml-interviews-book) — Chip Huyen's interview-preparation book and supporting material.
- [RAG Interview Questions and Answers Hub](https://github.com/KalyanKS-NLP/RAG-Interview-Questions-and-Answers-Hub) — Community practice questions; not a verified record of employer interviews.
- [Awesome Generative AI Guide](https://github.com/aishwaryanr/awesome-generative-ai-guide) — Community learning and interview-preparation resources.
- [This guide's interview preparation](interview/README.md) — Practice topics and the evidence limits of historical interview accounts.

Use the employer's current instructions for interview format and permitted tools. Question banks do not establish that a specific company currently asks a question.

## Books and foundations

- [AI Engineering — book resources](https://github.com/chiphuyen/aie-book) — Supporting resources for Chip Huyen's 2025 book.
- [Designing Machine Learning Systems — book resources](https://github.com/chiphuyen/dmls-book) — Summaries and resources for Chip Huyen's 2022 book.
- [Machine Learning Systems Design — booklet](https://github.com/chiphuyen/machine-learning-systems-design) — A separate booklet with exercises; this is not the repository for the book above.
- [Build a Large Language Model (From Scratch)](https://github.com/rasbt/LLMs-from-scratch) — Sebastian Raschka's implementation and book-support repository.
- [Neural Networks: Zero to Hero](https://github.com/karpathy/nn-zero-to-hero) — Andrej Karpathy's implementation course.
- [Hugging Face course](https://github.com/huggingface/course) — Course source material on Transformers.

## Courses and hands-on learning

- [Made With ML](https://github.com/GokuMohandas/Made-With-ML) — Developing, deploying and iterating on ML applications.
- [LangChain Academy](https://github.com/langchain-ai/langchain-academy) — Course notebooks and implementation exercises.
- [Anthropic's interactive prompt-engineering tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — Prompt-construction exercises.
- [Anthropic courses](https://github.com/anthropics/courses) — Educational material and notebooks.
- [Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners) — Microsoft's introductory lessons and examples.
- [This guide's advanced path](learning-paths/advanced-engineering.md) — Real-data projects, baselines, held-out evaluation and measurable exit criteria.

## Provider cookbooks

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) — Examples and guides for OpenAI APIs.
- [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) — Anthropic's recipes and notebooks; canonical destination of the older anthropic-cookbook URL.
- [Gemini Cookbook](https://github.com/google-gemini/cookbook) — Examples and guides for Gemini APIs.

Record package and model versions before running examples. A historical notebook does not establish current model availability, pricing or compatibility.

## Frameworks and application design

- [LangGraph](https://github.com/langchain-ai/langgraph) — Graph-based workflows and agents.
- [LlamaIndex](https://github.com/run-llama/llama_index) — Document processing and data-connected application tooling.
- [Vercel AI SDK](https://github.com/vercel/ai) — TypeScript tooling for AI applications and agents.
- [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python) — Agent-workflow SDK and examples.
- [Google Agent Development Kit](https://github.com/google/adk-python) — Python toolkit for agent applications.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) — Typed Python interfaces and application tooling.
- [smolagents](https://github.com/huggingface/smolagents) — Hugging Face's lightweight agent library.

Choose tools against a measured workflow. A framework alone does not establish correctness, authorization or production readiness.

## Protocols and integrations

- [Model Context Protocol specification](https://github.com/modelcontextprotocol/modelcontextprotocol) — Official specification, schemas and documentation source.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Official Python client/server SDK.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — Official TypeScript client/server SDK.
- [MCP server reference implementations](https://github.com/modelcontextprotocol/servers) — Inspect each server's permissions and maintenance status before deployment.
- [Agent2Agent protocol](https://github.com/a2aproject/A2A) — Canonical A2A project destination, replacing the redirected google/A2A URL and nonexistent comparison/design-file paths.
- [LangChain MCP adapters](https://github.com/langchain-ai/langchain-mcp-adapters) — MCP integration adapters.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) — Community server catalog; inclusion is not a security endorsement.

## Retrieval and storage

- [GraphRAG](https://github.com/microsoft/graphrag) — Microsoft's graph-based retrieval project.
- [Qdrant](https://github.com/qdrant/qdrant) — Vector-search engine.
- [Qdrant Python client](https://github.com/qdrant/qdrant-client) — Client API, local mode and examples.
- [pgvector](https://github.com/pgvector/pgvector) — Vector similarity search for PostgreSQL.
- [Weaviate](https://github.com/weaviate/weaviate) — Vector database and search implementation.
- [FAISS](https://github.com/facebookresearch/faiss) — Dense-vector similarity search and clustering library; not a complete application database.

## Evaluation and datasets

- [BEIR](https://github.com/beir-cellar/beir) — Retrieval benchmark datasets and evaluation utilities.
- [SciFact](https://github.com/allenai/scifact) — Scientific claim-verification data and models; preserve its task and split definitions.
- [MTEB](https://github.com/embeddings-benchmark/mteb) — Embedding evaluation across tasks, languages and modalities.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) — Real GitHub issues evaluated through a software harness. Run untrusted code in isolation.
- [τ³-bench](https://github.com/sierra-research/tau2-bench) — Agent evaluation in **simulated** customer-service environments; not real customer transaction records.
- [Ragas](https://github.com/vibrantlabsai/ragas) — Application-evaluation metrics and test-set tooling at its current repository location.
- [DeepEval](https://github.com/confident-ai/deepeval) — LLM application-evaluation tooling.
- [TruLens](https://github.com/truera/trulens) — Evaluation and tracking for LLM experiments and agents.
- [promptfoo](https://github.com/promptfoo/promptfoo) — Prompt/application testing and security-evaluation tooling.
- [This guide's reproducible research](research/README.md) — Pinned job-posting analysis, source dates, dataset limits and reproduction commands.

Inspect each dataset's license, origin, annotations and split. Keep real observations, model-derived labels and simulated/synthetic examples distinct. Scores are specific to a task, configuration and evaluation version.

## Observability, gateways and serving

- [Langfuse](https://github.com/langfuse/langfuse) — Tracing, evaluation and observability.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — AI application observability and evaluation.
- [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) — Python telemetry APIs and SDK.
- [LiteLLM](https://github.com/BerriAI/litellm) — Provider integration and gateway tooling.
- [vLLM](https://github.com/vllm-project/vllm) — Model inference and serving engine.
- [Text Embeddings Inference](https://github.com/huggingface/text-embeddings-inference) — Serving text-embedding models.

Protect sensitive data in traces. Measure first-token and full-completion latency separately and include infrastructure costs in serving comparisons.

## Engineering case-study collections

- [AI Engineering book resources](https://github.com/chiphuyen/aie-book) — Supporting references maintained with the book repository.
- [GenAI, LLM and ML case studies](https://github.com/themanojdesai/genai-llm-ml-case-studies) — Community-curated company reports; verify each original report before quoting outcomes.
- [AI system-design guide](https://github.com/ombharatiya/ai-system-design-guide) — Community design and evaluation guidance.
- [Applied ML](https://github.com/eugeneyan/applied-ml) — Eugene Yan's collection of company papers and technical posts.

Collections provide discovery, not independent verification of every deployment or numerical result.

## Security references

- [OWASP Top 10 for LLM Applications](https://github.com/OWASP/www-project-top-10-for-large-language-model-applications) — LLM application risks and mitigations.
- [garak](https://github.com/NVIDIA/garak) — LLM vulnerability-scanning project.

Test actual permissions, data boundaries and side effects. Passing a scanner does not establish complete resistance to injection or leakage.

## Model implementation references

- [DeepSeek-R1](https://github.com/deepseek-ai/DeepSeek-R1) — Model documentation and associated references.
- [Transformers](https://github.com/huggingface/transformers) — Model definitions and inference/training tooling.
- [PEFT](https://github.com/huggingface/peft) — Parameter-efficient adaptation tooling.

## Practitioner profiles and community discussions

- [Chip Huyen](https://github.com/chiphuyen) — Author-maintained repositories and resources.
- [Simon Willison](https://github.com/simonw) — LLM tooling, Datasette and related projects.
- [Hamel Husain](https://github.com/hamelsmu) — Public engineering and evaluation projects.
- [Eugene Yan](https://github.com/eugeneyan) — Applied ML projects and references.
- [Lilian Weng](https://github.com/lilianweng) — Public projects and writing-related resources.
- [LangChain discussions](https://github.com/langchain-ai/langchain/discussions) — Project community discussions.
- [Generative AI for Beginners discussions](https://github.com/microsoft/generative-ai-for-beginners/discussions) — Course questions and discussion.

These checked destinations replace unsupported social handles, placeholder thread IDs and unverified invite links. They are discovery resources, not evidence for market statistics or employer practices.

## Contributing

Check the actual destination and title, follow redirects to the canonical location, and give a description supported by the content. Remove nonexistent references instead of inventing article titles or discussion identifiers. Keep publication dates separate from link-review dates and follow [the evidence policy](research/evidence-policy.md).

This review checks this file's outbound destinations and local file targets. Links inside external collections need their own checking before reuse.
