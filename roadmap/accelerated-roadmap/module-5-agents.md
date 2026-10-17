# Module 5 · Agents

> **100 Days of AI Engineering** · Days 57–83 · 22 units

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/agents/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

## Units

## Part 1 · Days 57–63

### Build an Agent

#### 01 · What Is an Agent? (Unit 5.1 · Day 57)

- **The agent loop** — Goal → decide what to do → act → look at the result → repeat until done.
- **Who decides what happens next** — In a single call or a chain, your code decides the steps; in an agent, the model does.
- **Where agents help** — Open-ended, multi-step tasks where you can't map out every step in advance.
- **When a chain is better** — If you can write the steps down, a chain is simpler, cheaper and more reliable than an agent.
- **What an agent is made of** — A model, instructions, tools, memory, a loop, and rules for when to stop.

**Try it** · List five tasks your users might want done. Mark which ones need an agent and which a simple chain could handle.

**Outcome** · Decide whether a problem genuinely needs an agent, and name the parts every agent needs.

#### 02 · The Agent Loop (Unit 5.2 · Day 58)

- **Reason, then act (ReAct)** — The agent alternates between deciding what to do and doing it, using each result to choose the next step.
- **Build the loop yourself once** — Using the tool calling you learned in Module 2, write a simple loop that keeps calling tools until the task is done.
- **When to stop** — Set a maximum number of steps and a clear finish condition, and detect when the agent is repeating itself.
- **Step by step vs plan first** — Some agents decide one step at a time; others write a plan first and then follow it.

**Try it** · Give your loop a task that needs three tool calls in a row. Then give it an impossible task and confirm your step limit stops it.

**Outcome** · Explain how an agent loop works and build one that always stops.

#### 03 · Building Agents with LangGraph (Unit 5.3 · Days 59–60)

- **Why LangGraph** — It gives you explicit control over each step, saves the agent's progress, and supports pausing for human approval.
- **State, nodes and edges** — State holds what the agent knows; nodes do the work (call the model, run a tool, make a decision); edges decide what runs next.
- **Branches and loops** — Use conditional edges to choose the next step and loops to repeat tool use until the task is done.
- **Ready-made vs custom** — Start with **LangGraph**'s ready-made tool-using agent, then build your own graph when you need more control.
- **See what happened** — Inspect the agent's state after a run to understand why it took the path it did.

**Try it** · Rebuild your Unit 5.2 loop as a LangGraph graph, then add a branch that sends simple questions straight to an answer without using tools.

**Outcome** · Build a controllable agent in LangGraph and debug it by inspecting its state.

#### 04 · Tools for Agents (Unit 5.4 · Day 61)

- **Your RAG pipeline becomes a tool** — Wrap the **RAG** system from Module 4 as a search tool the agent can choose to use.
- **Tools the agent can choose between** — Clear names, descriptions and inputs matter even more when the agent picks from several tools on its own.
- **Keep tool results small** — Return only what the agent needs, so long results don't fill its context.
- **When tools fail** — Return useful error messages so the agent can retry, try another tool, or give up gracefully.
- **Looking vs changing** — Separate tools that only read information from tools that change things, and treat the second kind with care.

**Try it** · Give your agent your RAG search tool and a tool that takes an action, such as creating a support request. Ask one question that needs only search, and one task that needs search followed by an action.

**Outcome** · Give an agent a well-designed set of tools, including your own RAG system.

#### 05 · Planning and Reflection (Unit 5.5 · Day 62)

- **Plan before acting** — For longer tasks, have the agent write a short plan, then work through it.
- **Change the plan** — Let the agent revise its plan when a step fails or new information appears.
- **Check its own work** — Have the agent review its result before finishing and try again if it falls short.
- **The cost of thinking** — More planning and checking can improve results but adds time and cost; use it where tasks are genuinely complex.

**Try it** · Give your agent a multi-part task with and without a planning step, and compare success, steps and cost.

**Outcome** · Add planning and self-checking where they help, and leave them out where they don't.

#### 06 · Saving Progress and Asking for Approval (Unit 5.6 · Day 63)

- **Save as you go** — LangGraph can save the agent's state after each step, so a long task survives a crash or restart.
- **Resume, don't restart** — Pick up an interrupted run from where it stopped.
- **Pause for a human** — Stop before important actions, show the person what the agent wants to do, and continue only once they approve.
- **Safe to retry** — Design actions so that running them twice doesn't do the thing twice, such as creating the same support request again.

**Try it** · Add an approval step before a tool that changes something runs. Approve one request, reject another, and confirm the agent handles both.

**Outcome** · Build an agent that saves its progress, resumes after interruptions, and waits for approval before acting.

## Part 2 · Days 64–76

### Advanced Agents

#### 07 · MCP Fundamentals (Unit 5.7 · Day 64)

- **Why MCP exists** — A standard way to connect AI apps to tools and data, so one integration works with many apps instead of being rebuilt for each.
- **Host, client and server** — The app (host) uses a client to talk to MCP servers; each server exposes capabilities from one system.
- **What a server can offer** — Tools the model can call, resources (data the app can read, such as files or records), and ready-made prompts.
- **Tool calling vs MCP** — Tool calling is how a model asks for an action; MCP is how tools and data are packaged and shared between apps.
- **Using existing servers** — Many systems already have **MCP** servers, such as file systems, code repositories and databases.
- **Connecting your agent** — Use **LangChain**'s **MCP** support to load a server's tools into your **LangGraph** agent.

**Try it** · Connect your agent to an existing MCP server, such as a file-system server pointed at a folder of your documents, and ask it to find and summarize a file.

**Outcome** · Explain how MCP works and connect your agent to existing MCP servers.

#### 08 · Building MCP Servers (Unit 5.8 · Days 65–66)

- **Build your own server** — Expose a real system, such as support requests, as an **MCP** server.
- **Tools, resources and prompts** — Offer actions as tools (create or check a request), reference data as resources (your policies), and common tasks as prompts.
- **Good server design** — Clear names and descriptions, typed inputs, useful error messages, and small, focused results, just like good tools in Module 2.
- **Local and remote servers** — Servers can run on the same machine as the app or be reached over the internet; remote servers need authentication.
- **Test before you connect** — Use an **MCP** inspector tool to call your server's tools directly and check what they return.
- **Several servers, one agent** — Connect your agent to more than one server and make sure tool names don't clash or confuse it.
- **Changing a server safely** — Adding or renaming tools changes what every connected agent sees; version your server and test agents after each change.

**Try it** · Build an MCP server for support requests with at least two tools and one resource. Test it with an inspector, connect your agent and an MCP-compatible AI app to it, and complete one task from each.

**Outcome** · Package your own systems as MCP servers that any compatible app or agent can use.

#### 09 · Memory (Unit 5.9 · Days 67–68)

- **Short-term and long-term** — Short-term memory lasts for one conversation or task; long-term memory carries over between conversations.
- **Kinds of long-term memory** — Facts about the user (preferences, details), records of past events (what happened last time), and lessons about how to do things better.
- **Where memories live** — Store them in a database or **LangGraph**'s memory store, organized per user so they never mix.
- **When to save** — During the conversation, when something important comes up, or in the background afterwards, so saving doesn't slow the user down.
- **What to save** — Have the model pull out useful facts in a structured form, and avoid duplicates or saving every message.
- **When facts change** — Update or replace memories that are out of date, and decide what wins when two memories disagree.
- **Recalling the right memories** — Look up memories by relevance and recency, and add only the few that help with the current request.
- **Forgetting** — Let memories expire, and delete them completely when a user asks, including from backups and logs.
- **Is memory helping?** — Check whether the agent recalls the right things, and whether it ever remembers something wrong or outdated.

**Try it** · Tell your agent a preference ("always reply in Hindi") and a fact ("my team is in Pune") in one conversation. Check both are used in a new conversation, then change the fact and confirm the old one is replaced.

**Outcome** · Build an agent that remembers what matters across conversations, keeps its memories accurate, and forgets on request.

#### 10 · Context Engineering Basics (Unit 5.10 · Day 69)

- **Context is a budget** — Instructions, history, retrieved passages, memories, tool descriptions and tool results all compete for limited space.
- **Long runs go wrong** — As context grows, agents lose track of the goal, miss details buried in the middle and cost more with every step.
- **See what's really in there** — Inspect exactly what the agent sends the model at each step and spot what's useful and what's noise.
- **Split the budget** — Give rough limits to each part: instructions, history, retrieved passages, memories and tool results.
- **Build it on purpose** — Decide what's always included, what's looked up when needed, what's summarized and what's left out.
- **Order and label** — Keep instructions, evidence, memories and user input clearly separated so the model doesn't mix them up.

**Try it** · Log the full context your agent sends at step 1, step 10 and step 20 of a long task. Measure how big each part has grown and mark what's no longer useful.

**Outcome** · Diagnose when an agent's problems are really context problems, and plan what goes into its context.

#### 11 · Compaction, Offloading and Tool Context (Unit 5.11 · Days 70–71)

- **Summarize without losing the plot** — Compress older history while keeping the goal, constraints, decisions and unfinished work.
- **Rolling summaries** — Update a running summary as the task goes on instead of re-summarizing everything each time.
- **Keep exact details exact** — Store numbers, IDs and other precise data separately, since summaries can blur them.
- **Write things down** — Let the agent keep notes, plans and progress in a scratchpad or file outside its context and read them back when needed.
- **Trim tool results** — Filter or summarize large results before they go back to the model, and keep the full version outside in case it's needed later.
- **Only the tools it needs** — Load only the tools relevant to the current step, since every tool description takes space.
- **Use caching** — Keep fixed instructions and tool descriptions at the start so they can be cached, and measure how much caching saves.
- **Give sub-tasks their own context** — Hand a self-contained sub-task to a separate agent with a fresh context, so its working details don't crowd the main one; you'll build this in the multi-agent units.

**Try it** · Run a task of 20 or more steps three ways: keeping everything, summarizing history, and summarizing history plus trimming tool results and keeping notes. Compare success, tokens and cost.

**Outcome** · Keep long, tool-heavy agent runs focused and affordable without losing the information that matters.

#### 12 · Harness Engineering (Unit 5.12 · Day 72)

- **What a harness is** — Everything around the model that turns it into a working agent: the loop, instructions, tools, how context is built and trimmed, memory, permissions, approvals, error handling and the checks on its work.
- **The harness matters as much as the model** — The same model can do very well or very badly depending on its harness; when an agent fails, the fix is usually in the harness, not a bigger model.
- **Designing the tool set** — Choose between a few general tools and many narrow ones, decide what each tool's results show, and remove tools the agent rarely uses well.
- **Let the agent check its own work** — Give it ways to verify results, such as running tests, validating output against a schema or re-checking a source, and feed errors back clearly so it can fix them.
- **Instructions on demand** — Keep the core instructions short and load detailed guidance for a specific kind of task only when that task comes up.
- **Fit the harness to the model** — Different models respond differently to the same tools and instructions; re-test your harness whenever you change models.
- **Change one thing at a time** — Treat every harness change like a code change: make one change, run your test tasks, and keep it only if results improve.
- **Learn from existing harnesses** — Study how well-known coding agents structure their loop, tools, instructions and checks.

**Try it** · Make three separate changes to your agent's harness: rewrite its tool descriptions, add a step that checks its answer against the retrieved sources, and load detailed instructions only for request-handling tasks. Measure each change on the same 10 tasks.

**Outcome** · Improve an agent by changing its harness rather than its model, and prove each change with measurements.

#### 13 · Multi-Agent Patterns (Unit 5.13 · Day 73)

- **Why more than one agent** — Different parts of a task may need different tools, instructions, models or permissions, and splitting work keeps each agent's context small.
- **Supervisor and specialists** — One agent plans and hands work to specialist agents, then combines their results.
- **Handoffs** — Agents pass a task along in sequence, each doing its part, like a support desk transferring a call.
- **Parallel specialists** — Several agents work on parts of a task at the same time, and their results are merged.
- **Teams of teams** — For large tasks, supervisors can manage other supervisors, each with their own specialists.
- **What goes wrong** — Duplicated work, agents talking past each other, lost information between agents, conflicting results, and much higher cost.
- **One strong agent is often enough** — Add more agents only when splitting the work clearly helps.

**Try it** · Sketch two designs for your agent: a single agent and a supervisor with specialists. For each, list which tools and permissions every agent gets, and predict which will cost more.

**Outcome** · Choose a multi-agent pattern that fits the task, or decide that a single agent is better.

#### 14 · Building Multi-Agent Systems (Unit 5.14 · Days 74–75)

- **Build a supervisor** — Use **LangGraph** to build a supervisor that decides which specialist handles each part of a task.
- **Handoffs between agents** — Pass a task, with the context it needs, from one agent to another.
- **What each agent sees** — Decide whether agents share one state or pass messages, and give each only the information it needs.
- **Right tools, right model** — Give each specialist only its own tools and permissions, and use cheaper models for simpler specialists.
- **Combining results** — Merge specialists' outputs and resolve conflicts when they disagree.
- **When a specialist fails** — Retry, reassign the work to another agent, or escalate to a person.
- **Track the cost** — Measure steps, tokens, time and cost per agent and for the whole task.
- **Agents from other teams (A2A)** — A2A is an emerging standard for connecting agents built by different teams or companies, the way MCP connects tools.

**Try it** · Build a supervisor with two or three specialists, such as one for answering questions, one for handling requests and one for checking policies. Compare it with your single agent on the same ten tasks for success, cost and time.

**Outcome** · Build a working multi-agent system and judge with numbers whether it beats a single agent.

#### 15 · Reliability and User Experience (Unit 5.15 · Day 76)

- **Common agent failures** — Wrong tool, bad inputs, tools that are down, repeating itself, incomplete plans and running too long.
- **Budgets** — Limit steps, time, retries and cost for every task.
- **Know when to hand over** — When the agent can't continue safely, fall back to a simpler path or pass the task to a person.
- **Show progress** — Let users see what the agent is doing, which tool it's using, and what it found.
- **Keep users in control** — Let them cancel, pause, resume or change direction during long tasks.

**Try it** · Stream your agent's progress to the user step by step, and add a cost limit that stops any task above a set amount.

**Outcome** · Build agents that fail predictably, hand over when stuck, and keep users informed and in control.

## Part 3 · Days 77–79

### Evaluating Agents

#### 16 · Why Agent Evals Are Different (Unit 5.16 · Day 77)

- **The final answer isn't enough** — An agent can reach the right answer the wrong way, or the wrong answer for a fixable reason; you need to see the steps.
- **Read the traces** — Look through 20 full agent runs step by step, using the tracing you set up in Module 2.
- **Group the failures** — Note what went wrong in each run (wrong tool, bad inputs, loops, gave up early, lost context, bad handoff) and count each type.
- **What to measure** — Decisions, tool use, the path taken, task success, recovery from problems, memory, efficiency and safety.

**Try it** · Read 20 traces from your agent, write a one-line note on each problem you find, and group them into failure types.

**Outcome** · Find your agent's most common failures by reading what it actually did, not just what it answered.

#### 17 · Evaluating Tool Use and Task Success (Unit 5.17 · Day 78)

- **An agent test set** — A list of tasks, each with what success looks like and, where it matters, the tools that should be used.
- **Right tool, right inputs** — Check whether the agent picked the correct tool and filled in its inputs correctly.
- **A sensible path** — Check for unnecessary tool calls, repeated steps, wrong order and stopping too early.
- **Did it get the job done?** — Measure how often the agent completes each task successfully.
- **Judging the path** — Use a model as a judge for whether the steps were reasonable, and check it against your own scores as you did in Module 4.

**Try it** · Build an agent test set of 15 tasks and score your agent on tool choice, inputs and task success.

**Outcome** · Measure whether your agent makes good decisions and completes its tasks.

#### 18 · Testing Recovery, Memory and Efficiency (Unit 5.18 · Day 79)

- **Break things on purpose** — Make tools fail, return bad data or become unavailable, and leave out information the agent needs.
- **Did it notice and recover?** — Check whether the agent retries, tries another tool, changes its plan or asks for help.
- **Test memory** — Check that the agent recalls the right facts across conversations and never uses outdated or another user's memories.
- **Efficiency** — Track steps, tool calls, tokens, time and cost per task alongside success.

**Try it** · Make your search tool fail on three tasks and return empty results on two more. Then run three tasks that depend on remembered facts. Record how the agent handles each.

**Outcome** · Measure how well your agent copes when things go wrong, whether its memory can be trusted, and what each task costs.

## Part 4 · Days 80–83

### Securing Agents

#### 19 · Agent Threats and Least Privilege (Unit 5.19 · Day 80)

- **The dangerous combination** — An agent that reads untrusted content, has access to private data or powerful tools, and has a way to send information out can be turned against its users.
- **Least privilege** — Give each agent only the tools and permissions its task needs, and nothing more.
- **Check tool use in code** — Validate which tool is used, its inputs and the user's permissions outside the model, before anything runs.
- **Memory can be attacked** — Injected instructions saved as memories can affect every future conversation, and memories must never leak between users.
- **Limits stop runaways** — Step, time and cost limits also protect against attacks designed to make the agent loop or spend.

**Try it** · List every tool and permission each of your agents has. For each one, write what an attacker could do with it, then remove or restrict anything not essential.

**Outcome** · Explain how agents can be attacked and give yours only the access they truly need.

#### 20 · Approval Gates and Sandboxing (Unit 5.20 · Day 81)

- **Approval for anything irreversible** — Sending messages, changing or deleting records, payments and running code should wait for a person.
- **Run generated code in a sandbox** — Never run code the model writes inside your app; use an isolated environment such as E2B, Modal or a container.
- **Restrict the sandbox** — Limit file access, network access, credentials, run time and computing power.
- **Generated commands are untrusted** — Treat database queries, shell commands and web addresses written by the model as untrusted input.
- **Limit the damage** — Design so that even a fully tricked agent can only do a small amount of harm.

**Try it** · Give your agent a tool that runs Python in a sandbox. Ask it to read a file outside the sandbox and to make a network request, and confirm both are blocked.

**Outcome** · Let agents take powerful actions safely, with approval and isolation around anything risky.

#### 21 · Securing MCP and Tools (Unit 5.21 · Day 82)

- **Untrusted MCP servers** — Connecting to someone else's MCP server gives them a way to influence your agent; treat third-party servers like third-party code.
- **Hidden instructions in tools** — Tool descriptions and tool results can contain instructions aimed at the model, just like documents can.
- **Servers that change** — A server you approved can change its tools or behavior later; review what it offers before every update.
- **Over-broad access** — Give each server the narrowest permissions and credentials it needs.
- **Hijacked tool use** — Injected instructions from documents or tool results may try to make the agent call tools it shouldn't; your code checks from Unit 5.19 are what stop them.

**Try it** · Change one tool description on your MCP server to include a hidden instruction, and one tool result to include another. See whether either changes your agent's behavior.

**Outcome** · Connect agents to MCP servers and tools without handing control to whoever wrote them.

#### 22 · Red-Teaming Your Agent (Unit 5.22 · Day 83)

- **Attack your own agent** — Try to make it misuse tools, go beyond its permissions, reveal secrets, take actions without approval, poison its memory, or loop and run up costs.
- **Attack through every door** — Use the user's messages, retrieved documents, tool results, **MCP** tool descriptions and saved memories.
- **Measure unsafe actions** — Track how often attacks succeed and how often the agent attempts an action it shouldn't.
- **Every successful attack becomes a test** — Add each attack that worked to your regression suite.
- **Safety vs usefulness** — Check that your defenses haven't made the agent unable to do its job.

**Try it** · Write 10 attacks on your agent across messages, documents, tool results, MCP and memory. Record how many succeed, fix what you can, and run them again.

**Outcome** · Test your agent the way an attacker would and turn what you find into permanent tests.

## What we skipped, and why *(optional)*

| Topic | Why it's skipped here | Where to find it |
|---|---|---|
| CrewAI, Agno, Google ADK and the OpenAI Agents SDK | One framework, learned well, teaches the same ideas; compare others once you've shipped with one | Full roadmap, Level 5 |
| Building with A2A | Still emerging; MCP and LangGraph handoffs cover what most agent systems need today | Full roadmap, Level 5 |
| Long-context strategies for very long documents | A specialist topic; Units 5.10–5.11 cover what agents need | Full roadmap, Level 6 |
| Cybersecurity capability benchmarks | A concern for model builders, not for teams building agents | Full roadmap, Level 7 |
| Deploying agents to production | Covered in Shipping to Production | Full roadmap, Level 10 |
| A security review of the whole app | Covered in Shipping to Production, once the app is complete | Full roadmap, Level 8 |

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included. The same topics map to [full roadmap levels](../full-roadmap/README.md) where they are covered in more depth.*

- [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course) — free certified course covering agent fundamentals, frameworks and MCP.
- [LangGraph documentation](https://langchain-ai.github.io/langgraph/) — state, nodes, edges, checkpointing, human-in-the-loop interrupts.
- [LangChain Academy — Introduction to LangGraph](https://academy.langchain.com/courses/intro-to-langgraph) — free hands-on course building agents with LangGraph.
- [Model Context Protocol — official docs](https://modelcontextprotocol.io/) — the MCP specification, SDKs and guides (current spec version 2026-07-28).
- [Anthropic — Introduction to MCP (free course)](https://anthropic.skilljar.com/introduction-to-model-context-protocol) — official free course on building and connecting MCP servers.
- [MCP server reference implementations (GitHub)](https://github.com/modelcontextprotocol/servers) — read production-grade server code.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — handoffs, guardrails, sessions and tracing.
- [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/) — Google's open-source agent framework with multi-agent and A2A support.
- [smolagents documentation](https://huggingface.co/docs/smolagents) — lightweight code-first agents from Hugging Face.
- [Agent2Agent (A2A) protocol (GitHub)](https://github.com/a2aproject/A2A) — the emerging agent-to-agent interoperability standard.
- [E2B documentation](https://e2b.dev/docs) and [Modal documentation](https://modal.com/docs) — sandboxed code execution for agents.

## In this repository

- [Agentic AI curriculum](../../103_Agentic%20AI/README.md)
- [Context Engineering curriculum](../../101_LLM-Literacy/03-Context%20Engineering/1.%20Introduction%20to%20Context%20Engineering.md)

---

[← Module 4 · RAG](module-4-rag.md) | [100 Days map](README.md) | [Module 6 · Shipping to Production →](module-6-shipping-to-production.md)
