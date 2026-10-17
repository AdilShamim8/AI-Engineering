# Level 2 · Working with LLM APIs (Orchestration)

> **Phase 1 · Foundations** · 12 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/2/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Turn individual LLM calls into reliable software workflows — messages, streaming, structured outputs, tools, multi-step orchestration, concurrency, failure handling, and observability. RAG and agents come later.

*Short on time? Do the 11-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 8/10**

**Take-home assignments and live coding rounds** are usually built on this: call a model, get structured output, use a tool, handle failures. You show it more than you’re asked about it, so it matters **mainly through projects**.

**On-the-job weight: 10/10**

This is the **core of the daily work**: calling models, getting structured output, tool use, retries, streaming, handling rate limits and timeouts. **Almost every feature** you build goes through it.

---

## Modules

### 01 · First API calls & conversation state (M2.1 · 2 sessions)

- **Messages, roles & usage metadata** — Call OpenAI/Anthropic SDKs; work with models, messages, system instructions, user/assistant roles, response objects, stop reasons, and usage metadata.
- **APIs are stateless** — Understand that most LLM APIs are fundamentally stateless and learn to maintain conversation history explicitly.
- **Application state vs model context** — Distinguish application state from information currently present in the model's context.
- **Managing API keys safely** — Manage API keys safely using environment variables, .env files, or secret managers; never expose server-side credentials in frontend code.
- **Inspecting the full response object** — Inspect input/output tokens, request metadata, and model responses instead of treating the API as a simple prompt → string function.

### 02 · Streaming (M2.2 · 1 session)

- **Rendering output incrementally** — Stream model output incrementally and render partial responses in a terminal or UI.
- **TTFT & perceived latency** — Understand **TTFT**, generation speed, perceived latency, and total latency.
- **Accumulating and interrupting streams** — Accumulate streamed events into a complete response and handle cancellations, interrupted streams, network failures, and incomplete generations.

### 03 · LangChain fundamentals (M2.3 · 2 sessions)

- **Why orchestration libraries exist** — Understand why orchestration libraries exist and what **LangChain** abstracts over raw provider SDKs.
- **Models, templates & output parsers** — Work with chat models, messages, prompt templates, output parsers, streaming, and model configuration.
- **Working across providers** — Use **LangChain** with multiple model providers while understanding the underlying API calls it is making.
- **Composing pipelines with runnables** — Learn the core composition model and build simple pipelines using prompts, models, parsers, and runnables.
- **Raw SDK vs LangChain** — Compare equivalent implementations using raw SDKs and **LangChain** to understand convenience vs abstraction overhead.
- **LangChain is a layer, not the model** — Keep the mental model that **LangChain** is an orchestration layer, not the LLM itself.

### 04 · Structured outputs (M2.4 · 2 sessions)

- **Schema-constrained generation** — Generate schema-constrained outputs rather than relying on “please return **JSON**” prompting.
- **Defining schemas** — Define schemas using JSON Schema/Pydantic; work with required fields, optional fields, enums, lists, nested objects, and typed responses.
- **Provider-native vs framework support** — Implement structured outputs using both provider-native capabilities and **LangChain** abstractions.
- **Validating before use** — Validate model outputs before passing them into application logic.
- **Syntactic validity vs semantic correctness** — Distinguish syntactic validity from semantic correctness: valid JSON can still contain incorrect information.
- **Generate → validate → repair** — Implement a generate → validate → accept / retry / repair / reject workflow for invalid outputs.

### 05 · Function / tool calling (M2.5 · 3 sessions)

- **Who chooses and who executes** — Understand that the LLM normally chooses a tool and generates arguments; your application executes the actual function.
- **Defining a tool** — Define tools using names, descriptions, parameter schemas, types, and required arguments.
- **The full tool-calling loop** — Implement the full loop: user → LLM → tool request → execute tool → return result → LLM → final answer.
- **Tool-call IDs & returning results** — Work with tool-call IDs and correctly insert tool results back into the conversation.
- **Provider APIs vs LangChain tools** — Implement tool calling using provider APIs directly and understand how **LangChain** represents and executes tools.
- **Sequential, repeated & parallel calls** — Handle sequential calls, multiple calls to the same tool, parallel calls, and workflows where one tool result determines the next tool call.
- **Tool failures & malformed arguments** — Handle tool failures and malformed arguments instead of assuming every requested invocation is executable.

### 06 · Designing good tools (M2.6 · 1 session)

- **Names, descriptions & types** — Design tools with precise names, clear descriptions, minimal parameters, strong types, and useful error responses.
- **Ambiguous & overlapping tools** — Understand how ambiguous or overlapping tools can cause incorrect tool selection.
- **Too many undifferentiated tools** — Avoid giving the model huge numbers of poorly differentiated tools or unnecessary arguments.
- **Treating arguments as untrusted** — Treat model-generated arguments as untrusted input: validate types, values, permissions, and potentially destructive operations before execution.
- **Tool descriptions are context** — Understand that tool descriptions themselves are part of the context the model uses to decide what action to take.

### 07 · Multi-step LLM workflows (M2.7 · 1 session)

- **Beyond prompt → model → answer** — Move beyond prompt → model → answer and build workflows containing multiple LLM calls, tools, transformations, and application logic.
- **Sequential, routed & fan-out patterns** — Implement common orchestration patterns: sequential pipelines, routing, conditional branches, and fan-out/fan-in.
- **When to split a task** — Learn when to split a complex task into multiple specialized calls instead of using one enormous prompt.
- **Building by hand, then composing** — Build some workflows manually to understand their control flow, then reproduce them using **LangChain** composition primitives.
- **Workflows vs agents** — Understand the distinction between application-controlled workflows and the more autonomous agentic systems introduced later.

### 08 · Async, concurrency & batching (M2.8 · 1 session)

- **When concurrency helps** — Understand synchronous vs asynchronous API calls and when concurrency improves throughput.
- **Running requests concurrently** — Process many independent LLM requests concurrently rather than sequentially.
- **Bounded concurrency & rate limits** — Use bounded concurrency so higher throughput does not immediately create rate-limit failures.
- **Async and batch execution** — Apply async and batch execution using both provider SDKs and orchestration-layer abstractions.
- **The throughput / cost trade-off** — Understand the trade-off between concurrency, throughput, latency, API limits, resource consumption, and cost.

### 09 · Robustness: retries, timeouts & fallbacks (M2.9 · 2 sessions)

- **Common API failures** — Recognize common API failures: authentication errors, invalid requests, rate limits, server errors, network failures, timeouts, context-limit errors, and malformed model outputs.
- **What to retry and what to fail fast** — Decide which failures should be retried and which should fail immediately; for example, authentication errors generally should not be retried while transient server errors may be.
- **Backoff, jitter, timeouts & degradation** — Implement exponential backoff, jitter, maximum retry counts, sensible request timeouts, and graceful degradation.
- **Model and provider fallbacks** — Add model/provider fallbacks when appropriate, while understanding that fallback models may differ in quality and behavior.
- **Failures at the LLM and tool levels** — Handle failures at both levels: LLM API failure and tool/API failure.
- **Where reliability logic belongs** — Understand where reliability logic should live: provider SDK, orchestration layer, or your application code.

### 10 · Cost, usage & observability (M2.10 · 1 session)

- **What to record per request** — Track model, input tokens, output tokens, latency, retries, errors, tool calls, and estimated cost for every request.
- **Interactions as traces** — Treat a multi-step LLM interaction as a trace rather than an isolated API call.
- **Finding the failing step** — Inspect which step caused a failure, which call consumed the most tokens, which tool was selected, and where latency accumulated.
- **Tracing a full workflow** — Use callbacks/tracing to understand **LangChain** workflows and connect individual model and tool calls into a single execution trace.
- **Logging you can actually debug with** — Build enough logging and tracing that you can debug workflows without relying on scattered print() statements.

### 11 · Other orchestration frameworks (M2.11 · 2 sessions)

- **LangChain is one approach among many** — Understand that **LangChain** is one orchestration approach rather than a universal standard.
- **LlamaIndex** — Explore **LlamaIndex** and how its abstractions and emphasis differ from **LangChain**.
- **Graph & state-machine orchestration** — Explore graph/state-machine style orchestration for workflows containing branches, loops, persistent state, and more complex control flow.
- **LangGraph** — Get introduced to **LangGraph** as a graph-based approach for stateful LLM workflows.
- **DSPy** — Get introduced to **DSPy** as a more declarative approach where you specify desired input/output behavior rather than manually composing every prompt.
- **Comparing orchestration approaches** — Compare orchestration approaches on development speed, abstraction overhead, debugging, portability, dependency complexity, state management, and control.
- **Choosing one for your application** — Develop the ability to choose between raw SDKs, **LangChain**, graph-based frameworks, **LlamaIndex**, **DSPy**, or a custom orchestration layer based on the application.

#### Capstone: streaming tool-using assistant

- A streaming assistant with real tools Build a conversational assistant that maintains history, uses system instructions, streams responses, and exposes at least 2–3 real tools/APIs.
- Sequential or parallel tool use Support sequential or parallel tool use where appropriate and validate all model-generated tool arguments.
- Structured outputs, retries & timeouts Add structured outputs where useful, retry transient failures, enforce timeouts, and handle tool/API errors gracefully.
- Recording usage, latency & cost Record token usage, latency, retries, tool calls, and estimated cost so the entire workflow can be inspected.
- Building on LangChain, explaining the raw calls Build the main implementation using **LangChain** while being able to explain the raw API/tool-call mechanics underneath it.
- LLM + software + tools + reliability The final application should combine LLM + software + external tools + control flow + reliability, without relying on **RAG** or autonomous agents.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) — practical recipes for streaming, structured outputs, tool calling, batching and error handling.
- [Anthropic Courses (official repo)](https://github.com/anthropics/courses) — free notebooks on tool use, structured output and prompt engineering with the Claude API.
- [Gemini Cookbook](https://github.com/google-gemini/cookbook) — equivalent recipes for the Gemini API.
- [LangChain Python documentation](https://python.langchain.com/docs/introduction/) — chat models, prompt templates, runnables, composition.
- [LangChain Academy — free courses](https://academy.langchain.com/) — hands-on courses including "Introduction to LangChain".
- [DeepLearning.AI short courses](https://www.deeplearning.ai/courses/) — free short courses such as *Building Systems with the ChatGPT API* and *Functions, Tools and Agents with LangChain*.
- [Pydantic documentation](https://docs.pydantic.dev/) — schema-constrained structured outputs and validation.
- [LiteLLM documentation](https://docs.litellm.ai/) — one interface across providers; useful for understanding provider differences.
- [Tenacity (retry library) docs](https://tenacity.readthedocs.io/) — exponential backoff, jitter and retry policies in Python.

## In this repository

- [Orchestration curriculum](../../102_AI-Application-Development/01-Orchestration/1.%20Introduction%20to%20Orchestration.md)
- [Structured output note](../../102_AI-Application-Development/01-Orchestration/3.%20Structured%20Output.md)
- [Tool integration & function calling note](../../102_AI-Application-Development/01-Orchestration/4.%20Tool%20Integration%20%26%20Function%20Calling.md)

---

[← Level 1 · LLM 101](level-01-llm-101.md) | [Roadmap map](README.md) | [Level 3 · Prompt Engineering →](level-03-prompt-engineering.md)
