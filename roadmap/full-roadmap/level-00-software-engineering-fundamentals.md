# Level 0 · Software Engineering Fundamentals

> **Phase 1 · Foundations** · 8 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/0/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Become comfortable building, debugging, and deploying real software before adding LLMs. This is the engineering foundation for everything that follows.

## Why this level matters

**Interview weight: 9/10**

Many AI engineer roles **screen candidates as software engineers first**, with coding rounds, backend questions, and API design. If you fail these, **you never reach the AI rounds**.

**On-the-job weight: 10/10**

Most of the work is **regular software engineering**: APIs, databases, testing, debugging, deployments. Most production incidents are **ordinary software bugs**, not model problems.

---

## Modules

### 01 · Python for AI Engineering (M0.1 · 4 sessions)

- **Clean, idiomatic Python** — Write clean, idiomatic **Python** using functions, classes, modules, comprehensions, exceptions, and common standard-library utilities.
- **Core data structures** — Reason confidently about core data structures: lists, tuples, sets, dictionaries, iterators, generators, and when to use each.
- **Type hints & typed models** — Use type hints, **dataclass**/**Pydantic**-style models, and static analysis to make interfaces explicit and catch mistakes earlier.
- **Mutability, scope & failure modes** — Understand mutability, references, scope, exceptions, context managers, and common **Python** failure modes.
- **Files, paths, env vars & serialization** — Work with files, paths, environment variables, **JSON**, **CSV**, and basic serialization.
- **Sync vs async execution** — Understand synchronous vs asynchronous execution; use async / await to perform concurrent network/API calls without blocking.
- **Environments & dependencies with uv** — Manage virtual environments and dependencies with uv; understand pyproject.toml, dependency locking, and reproducible environments.
- **Modules & packages** — Structure larger programs into modules and packages instead of writing everything in one script.
- **Unit tests and debugging** — Write basic unit tests with **pytest** and learn to debug using stack traces, logs, and breakpoints.

**Outcome** · Build a small multi-file Python application that is typed, tested, dependency-managed, and capable of making concurrent external API calls.

### 02 · The Web: HTTP, REST & JSON (M0.2 · 3 sessions)

- **The HTTP request/response cycle** — Understand the full HTTP request/response cycle: URL, method, headers, body, server processing, response, and status code.
- **Methods & idempotency** — Work with common methods such as GET, POST, PUT/PATCH, and DELETE, and understand idempotency at a practical level.
- **Status codes** — Understand important status-code families and common codes such as 200, 201, 400, 401, 403, 404, 409, 429, and 500.
- **Headers, params, bodies & cookies** — Understand headers, query parameters, path parameters, request bodies, content types, and cookies at a practical level.
- **Working with JSON** — Produce, parse, validate, and manipulate **JSON** confidently.
- **RESTful resource design** — Understand RESTful resource design and design clean endpoints for a simple application.
- **Authentication basics** — Understand authentication basics: API keys, bearer tokens, authorization headers, and why secrets should not be embedded in URLs or client code.
- **Inspecting APIs with curl & Postman** — Use tools such as **curl**, **Postman**/**Bruno**, or **Python** **HTTP** clients to inspect and debug APIs.

**Outcome** · Read unfamiliar API documentation, construct requests manually, interpret responses, and design a sensible REST API.

### 03 · Building APIs with FastAPI (M0.3 · 3 sessions)

- **Routes, parameters & response models** — Build a **FastAPI** application with routes, path/query parameters, request bodies, and response models.
- **Validation with Pydantic** — Use **Pydantic** models for validation, serialization, typed inputs, and typed outputs.
- **Dependency injection** — Understand dependency injection at a practical level for reusable application dependencies.
- **Status codes & error responses** — Return appropriate **HTTP** status codes and design consistent error responses.
- **Clean exception handling** — Handle exceptions cleanly instead of leaking raw stack traces to clients.
- **Generated OpenAPI docs** — Use **FastAPI**'s automatically generated **OpenAPI**/**Swagger** documentation and understand how API schemas are derived.
- **Sync vs async endpoints** — Write synchronous and asynchronous endpoints and understand when each is appropriate.
- **Calling external services without blocking** — Call external **HTTP** services from async endpoints without blocking the server.
- **Startup, config & middleware** — Understand application startup/shutdown, configuration through environment variables, and basic middleware concepts.
- **Testing endpoints** — Test endpoints using **pytest** and **FastAPI**'s test client.

**Outcome** · Build a documented, validated, testable API that communicates with at least one external service.

### 04 · Data & Persistence Basics (M0.4 · 2 sessions)

- **Relational data modeling** — Understand relational data modeling: tables, rows, columns, primary keys, foreign keys, relationships, and basic normalization.
- **SQL with PostgreSQL** — Use **PostgreSQL** and write **SQL** for SELECT, INSERT, UPDATE, DELETE, filtering, sorting, grouping, joins, and basic aggregations.
- **Indexes & query performance** — Understand indexes conceptually and why query design affects performance.
- **Connecting a database to the app** — Connect **PostgreSQL** to a **Python**/**FastAPI** application using a database driver or ORM.
- **Credentials outside source code** — Keep database credentials outside source code and manage configuration through environment variables.

**Outcome** · Build an API whose data survives application restarts and supports real CRUD operations backed by PostgreSQL.

### 05 · Git & Collaboration (M0.5 · 2 sessions)

- **Repos, commits, branches & remotes** — Understand repositories, commits, branches, remotes, diffs, and the staging area.
- **The branch → PR → merge workflow** — Follow a practical workflow: branch → make changes → commit → push → pull request → review → merge.
- **Commit messages & history** — Write useful commit messages and inspect history using **Git** tools.
- **Resolving merge conflicts** — Resolve merge conflicts confidently rather than avoiding them.
- **Keeping secrets out with.gitignore** — Understand **.gitignore** and prevent secrets, virtual environments, generated files, and local configuration from entering the repository.
- **Writing a README** — Write a **README** that explains what the project does, how to install it, configure it, run it, test it, and call its API.
- **Code review & protected branches** — Understand basic collaboration concepts such as code review, pull requests, and protected main branches.

**Outcome** · Hand another developer your repository and have them understand, run, and contribute to it without needing you beside them.

### 06 · AI-Assisted Software Development (M0.6 · 5 sessions)

Agentic coding fundamentals

- **Autocomplete → assistants → agents** — Understand the progression from autocomplete, to chat-based assistants, to coding agents that can read a repository, edit code, run commands, inspect the results, and iterate.
- **AI-assisted engineering vs vibe coding** — Distinguish AI-assisted engineering, where you direct and verify the work, from blind vibe coding, where you accept whatever is generated.
- **Explore, implement & debug with an agent** — Use a coding agent such as Claude Code to explore an unfamiliar repository, implement targeted changes, and debug existing code.
- **The verification loop** — Work the verification loop on every change: give context → generate → inspect the Git diff → test → debug → review → accept.

Context, CLAUDE.md & planning

- **Minimum useful context** — Understand the finite context window and give the minimum useful context for a task instead of pointing the agent at the entire repository.
- **CLAUDE.md as project memory** — Keep architecture, conventions, project commands, and testing instructions in a project instruction file such as CLAUDE.md, separate from temporary task context.
- **Spec-driven development & planning** — Practice spec-driven development: write the requirement and the specification, then review a plan before the agent changes the repository.

Reusable workflows: commands & Skills

- **Slash commands & Skills** — Turn prompts you retype into custom slash commands, and understand Skills as reusable capabilities with instructions, metadata, and examples that load only when needed.
- **Skills worth building** — Build skills for recurring work such as code review, test generation, documentation, refactoring, and repository-specific conventions.

Subagents & external tools

- **Delegating to subagents** — Delegate specialized work to subagents such as a reviewer, tester, debugger, or researcher instead of forcing every responsibility into one context.
- **External systems through MCP** — Connect the agent to systems outside the repository through **MCP** (Model Context Protocol): databases, APIs, developer tools, and documentation.

Hooks, plugins & the professional loop

- **Hooks for deterministic checks** — Use hooks to make formatting, linting, testing, and validation deterministic instead of asking a model to remember them.
- **Plugins as capability bundles** — Understand plugins as reusable bundles that package commands, skills, hooks, agents, and integrations together.
- **Skills that transfer across agents** — Understand that these skills transfer to any coding agent — Claude Code, Codex, Cursor, **GitHub** Copilot, Gemini CLI — because the durable parts are context, specifications, planning, delegation, automation, and verification.

**Mental model** · AI coding proficiency does not replace software engineering fundamentals. It multiplies them.

**Try it** · Build a small multi-file application with a coding agent — spec it, plan it, add one command or Skill, one subagent, one MCP integration, and one hook, then review every diff, run the tests, and fix at least one thing the agent got wrong.

**Outcome** · Use a coding agent as an engineering collaborator across exploration, implementation, debugging, refactoring, and testing, with planning and verification around every meaningful change.

- Use AI aggressively for leverage and verify aggressively for correctness: a coding agent produces plausible but incorrect code as fast as it produces correct code, and correctness, architecture, security, and maintainability stay yours.

### 07 · Containers & Deployment (M0.7 · 2 sessions)

- **App vs environment vs machine** — Understand the practical distinction between your application, its environment, and the machine running it.
- **Containers & images** — Understand containers and images conceptually and why **Docker** improves reproducibility.
- **Writing and running a Dockerfile** — Write a **Dockerfile**, build an image, run a container locally, expose ports, and pass environment variables safely.
- **Layers, logs & startup failures** — Understand image layers, **.dockerignore**, container logs, and common container startup failures.
- **Containerizing a FastAPI app** — Containerize a **FastAPI** application and connect it to its required configuration/services.
- **Deploying to a public URL** — Deploy a service to a cloud/platform provider and expose it through a publicly reachable URL.
- **Production env vars & secrets** — Configure production environment variables and secrets separately from local development.

**Outcome** · Take a service that works locally, containerize it, deploy it, and debug it when the production environment behaves differently.

#### Capstone: Ship a No-AI REST Service

- The full no-AI stack Build a complete application using **Python** + **FastAPI** + **PostgreSQL** + **Git** + **Docker** + deployment, with no LLM or AI dependency.
- Choosing a realistic domain Design a small but realistic domain such as task management, bookmarks, expense tracking, inventory, notes, or support tickets.
- REST endpoints with persistent CRUD Implement multiple **REST** endpoints with validated request/response schemas and persistent CRUD operations.
- An external API integration Include at least one external API integration and use async execution where appropriate.
- Handling every failure path Handle validation failures, missing resources, external-service errors, and unexpected server errors cleanly.
- Tests, config & logging Add basic automated tests, configuration via environment variables, and useful application logging.
- Clean repo and README Maintain the project in **Git** with a clean repository structure and a **README** containing setup and usage instructions.
- Docker packaging & deployment Package the service with **Docker** and deploy it to a publicly reachable URL.
- Verifying the deployed API Verify the deployed API using its **OpenAPI** docs, **curl**, or an API client.
- Coding agent during the build Use a coding agent for meaningful parts of the build; "no-AI" means the deployed product needs no LLM, not that you code without AI tools.
- Diff review before accepting Review every meaningful generated change through its **Git** diff before accepting it.
- Validating generated code Validate generated code through tests, type checking, linting, logs, and manual API calls.
- Explain it without the agent Explain the architecture and the important code paths yourself, without asking the coding agent.
- Document one AI failure Document one case where the coding agent produced an incorrect, incomplete, insecure, over-engineered, or otherwise suboptimal solution: what it proposed, why it was wrong, how you detected it, what you changed, and the engineering lesson you took from it.

a real service that another person can clone, run, test, call over HTTP, and inspect without any AI component hiding weak software-engineering fundamentals.

- Agentic Coding using Claude Code YouTube playlist

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [Harvard CS50P — Introduction to Programming with Python](https://cs50.harvard.edu/python/) — free full course with problem sets covering functions, data structures, exceptions and testing.
- [The Python Tutorial (official)](https://docs.python.org/3/tutorial/) — canonical reference for the language, standard library and idioms.
- [uv documentation](https://docs.astral.sh/uv/) — official guide for the environment and dependency manager used throughout the roadmap (`pyproject.toml`, locking, reproducible environments).
- [MDN HTTP guide](https://developer.mozilla.org/en-US/docs/Web/HTTP) — request/response cycle, methods, status codes, headers and cookies.
- [FastAPI tutorial (official)](https://fastapi.tiangolo.com/tutorial/) — step-by-step: routing, Pydantic validation, dependency injection, async endpoints, testing.
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) — SQL from SELECT to joins and aggregations on PostgreSQL.
- [Pro Git book (free)](https://git-scm.com/book/en/v2) — the complete Git reference: branches, remotes, merge conflicts, workflows.
- [GitHub Skills](https://skills.github.com/) — interactive free courses on PR workflows, code review and protected branches.
- [Docker Get Started (official)](https://docs.docker.com/get-started/) — images, layers, Dockerfiles, containerizing a web API.
- [pytest documentation](https://docs.pytest.org/en/stable/) — writing and organizing unit tests.
- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/overview) — agentic coding, CLAUDE.md project memory, hooks, subagents and MCP integrations.
- [GitHub Copilot documentation](https://docs.github.com/en/copilot) — AI-assisted development with Copilot agents and best practices.

## In this repository

- [General learning path](../../learning-paths/README.md)
- [Curated engineering resources](../../awesome.md)

---

[Roadmap map](README.md) | [Level 1 · LLM 101 →](level-01-llm-101.md)
