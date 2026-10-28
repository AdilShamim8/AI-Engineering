# Module 2 · Building with LLM APIs

> **100 Days of AI Engineering** · Days 7–17 · 9 units

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/building-with-llm-apis/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

## Units

#### 01 · LangChain Basics and Conversations (Unit 2.1 · Day 7)

- **What LangChain is for** — LangChain gives you one consistent way to call models, build prompts, use tools and chain steps together, whichever provider you use.
- **Chat models** — Connect to the model you chose in Module 1 through **LangChain**, and switch providers by changing one line.
- **Messages and roles** — A conversation is a list of messages: system instructions, the user's words and the assistant's earlier replies.
- **The model has no memory** — Each call starts fresh, so your app must send the conversation history every time.
- **Prompt templates** — Write a prompt once with placeholders, then fill them in for each request instead of building strings by hand.
- **Keep your keys secret** — Store API keys outside your code and never put them in anything that runs in a user's browser.
- **Read the whole response** — Look at the token usage and why the answer stopped, not just the text; they tell you what it cost and whether it was cut off.

**Try it** · Have a three-turn conversation using a prompt template. Then drop the history from the third call and see what the model forgets.

**Outcome** · Call any model through LangChain, keep a conversation going, and explain why the model "remembers" only what you send it.

#### 02 · Open and Local Models (Unit 2.2 · Day 8)

- **Open models** — Some models publish their weights, so anyone can download and run them; check each model's license before you build on it.
- **Run one on your own machine** — Tools such as Ollama download and run open models locally with one command.
- **What your computer can handle** — Your computer's memory decides how big a model you can run; smaller and compressed versions trade some quality for fitting in less memory.
- **Same code, different model** — Swap a local model into your LangChain app by changing the chat model; many local tools offer the same interface as the big API providers.
- **Hosted open models** — If your machine is too small, providers host open models for you and charge per token.
- **The trade-offs** — Local models are free to run and keep data on your machine, but are usually slower and less capable than top API models.
- **A practical habit** — Use a cheap or local model while you build and experiment, and your chosen model for real use.

**Try it** · Run a small open model on your own machine. Send it your 10 project questions alongside the model you chose in Module 1, and compare answer quality and speed.

**Outcome** · Run open models locally or through a provider, swap them into your app, and judge when they're good enough.

#### 03 · Streaming (Unit 2.3 · Day 9)

- **Show answers as they arrive** — Streaming sends the answer piece by piece, so users see text immediately instead of waiting.
- **Streaming in LangChain** — The same model, template or chain you already built can stream with no extra setup.
- **Perceived speed** — Time to first token matters more to users than total time; streaming makes an app feel faster without making it faster.
- **Put the pieces back together** — Collect the streamed pieces into the full answer so you can save, check or log it.
- **When streams break** — Handle a user cancelling, a dropped connection, or an answer that stops halfway.

**Try it** · Ask for a long answer with and without streaming, and time when the first word appears in each case.

**Outcome** · Stream answers to the user and still end up with a complete, saved response, even when the stream is interrupted.

#### 04 · Structured Outputs (Unit 2.4 · Days 10–11)

- **Don't just ask for JSON** — Asking politely for JSON fails sometimes; use LangChain's structured-output support so the model must return the shape you define.
- **Describe the shape you want** — Define the fields, which are required, allowed values and nested lists as a schema, so your code knows exactly what it will get.
- **Check before you use it** — Validate every structured answer before it reaches the rest of your app.
- **Valid isn't the same as correct** — Perfectly formatted output can still contain wrong information.
- **Generate → check → decide** — When an answer fails validation, retry, ask the model to fix it, or reject it with a clear error.

**Try it** · Extract name, date, amount and category from 10 messy text receipts. Count how many come back valid, and how many are valid but wrong.

**Outcome** · Get structured data from a model that your code can rely on, and handle the cases where it can't.

#### 05 · Tool Calling (Unit 2.5 · Days 12–13)

- **The model asks; your code acts** — The model picks a tool and fills in its inputs; your app actually runs it.
- **Defining tools in LangChain** — Turn an ordinary function into a tool with a name, a description of when to use it, and typed inputs, then attach your tools to the model.
- **The full loop** — User message → model asks for a tool → your code runs it → the result goes back to the model → the model gives its final answer.
- **Matching results to requests** — Each tool request has an ID; send each result back with the right ID so the model knows which answer is which.
- **More than one call** — Handle several tool calls in one turn, the same tool called twice, and cases where one result decides the next call.
- **When tools fail** — Expect missing or invalid inputs and failing tools, and send a useful error back to the model instead of crashing.
- **Designing good tools** — Use precise names, few inputs and clear descriptions; overlapping or vague tools make the model pick the wrong one.
- **Never trust tool inputs** — Check every input the model provides, especially before anything that changes or deletes data.
- **Tool descriptions are instructions** — The model reads them to decide what to do, so write them as carefully as a prompt.

**Try it** · Give the model a weather tool and a currency tool. Ask a question that needs both, then one that needs neither, and check what it chose each time.

**Outcome** · Build the complete tool-calling loop in LangChain and give a model tools it uses correctly and safely.

#### 06 · Chaining Steps Together (Unit 2.6 · Day 14)

- **Beyond one call** — Real features often chain several model calls, tools and ordinary code together.
- **Chains in LangChain** — Connect a prompt, a model and an output step into one chain you can run, stream and reuse like a single piece.
- **Three common patterns** — A fixed sequence of steps, routing a request to the right path, and running parts in parallel then combining the results.
- **When to split a task** — Several small, focused steps are often more reliable and easier to debug than one giant prompt.
- **Chains vs agents** — In a chain your code decides the steps; in an agent the model decides. Agents come later in the track.

**Try it** · Build a chain that classifies a user question by type, then routes it to a different prompt for each type.

**Outcome** · Design a feature as a chain of small steps, and know when that beats a single prompt.

#### 07 · Handling Failures (Unit 2.7 · Day 15)

- **What goes wrong** — Wrong keys, bad requests, rate limits, server errors, timeouts, inputs that are too long, and malformed answers.
- **Retry or give up** — Retry temporary problems like server errors and rate limits; fail immediately on problems that won't fix themselves, like a bad key.
- **Retries in LangChain** — Add automatic retries to any model or chain, with a cap on attempts, and set a time limit on every call.
- **Backup models** — Give a model or chain a fallback to use when it fails, knowing the backup may answer differently.
- **Don't overload the API** — When running many requests at once, limit how many run together so you don't hit rate limits.
- **Fail gracefully** — When nothing works, give the user a clear message instead of an error.

**Try it** · Point your chain at a wrong model name, then at a very short timeout, and confirm each failure triggers the right retry or fallback.

**Outcome** · Make your app survive the everyday failures of model APIs without crashing or retrying forever.

#### 08 · Processing at Scale (Unit 2.8 · Day 16)

- **One at a time is slow** — When you have many independent requests, such as summarizing hundreds of documents, send them at the same time instead of waiting for each one.
- **Stay within your limits** — Cap how many requests run at once so you don't hit the provider's rate limits; LangChain's batch processing lets you set this.
- **Batch APIs** — Many providers offer a cheaper batch option for jobs that don't need an answer right away, such as processing a document collection or running tests overnight.
- **Don't lose progress** — Retry failed items on their own and save results as you go, so one failure or crash doesn't mean starting over.
- **Estimate before you run** — Work out the tokens and cost of a big job before starting it.

**Try it** · Summarize 200 short texts one at a time, then concurrently with a limit on how many run at once. Compare total time, errors and cost.

**Outcome** · Process large volumes of requests quickly and cheaply without hitting rate limits or losing work.

#### 09 · Cost, Logging and Tracing (Unit 2.9 · Day 17)

- **Record every request** — Model, input and output tokens, time taken, retries, errors, tools used and estimated cost.
- **Think in traces** — One user question can trigger several model and tool calls; tracing groups them so you can follow the whole journey.
- **Tracing LangChain apps** — Turn on tracing (for example with LangSmith) or hook into **LangChain**'s callbacks to capture every step automatically.
- **Find the problem step** — Use traces to see which step failed, which used the most tokens, and where the time went.

**Try it** · Run 10 questions through your app with tracing on and produce a short report: total cost, average time per question, and the most expensive question.

**Outcome** · Know exactly what your app costs to run and find the slow or failing step in any request.

## What we skipped, and why *(optional)*

| Topic | Why it's skipped here | Where to find it |
|---|---|---|
| Calling provider APIs directly | LangChain makes the same calls; learn one way well first | Full roadmap, Level 2 |
| Where to put retry logic | A design detail that matters at larger scale | Full roadmap, Level 2 |
| LlamaIndex, LangGraph and DSPy | Learning one framework well beats surveying four; LangGraph returns when you build agents | Full roadmap, Level 2 |
| Comparing orchestration frameworks | Useful once you've built with more than one | Full roadmap, Level 2 |

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included. The same topics map to [full roadmap levels](../full-roadmap/README.md) where they are covered in more depth.*

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

---

[← Module 1 · LLM Fundamentals](module-1-llm-fundamentals.md) | [100 Days map](README.md) | [Module 3 · Prompt Engineering →](module-3-prompt-engineering.md)

<!-- nav-footer -->
---

**Navigate:** [← Module 1 LLM Fundamentals](module-1-llm-fundamentals.md) · [Section hub](README.md) · [Module 3 Prompt Engineering →](module-3-prompt-engineering.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
