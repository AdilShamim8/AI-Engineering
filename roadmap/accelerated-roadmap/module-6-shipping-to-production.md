# Module 6 · Shipping to Production

> **100 Days of AI Engineering** · Days 84–100 · 15 units

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/shipping-to-production/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

## Units

#### 01 · Designing an AI System (Unit 6.1 · Day 84)

- **Start from the requirements** — Who uses it, how many people, how fast it must respond, how good answers must be, what it may cost, and what data rules apply.
- **Rough numbers first** — Turn expected users into requests per minute, tokens per day and cost per month before choosing anything.
- **Choose the simplest design that works** — Decide between plain prompting, **RAG**, an agent or a mix, and justify each extra piece.
- **The core trade-offs** — Quality, speed and cost pull against each other; every design choice favors one of them.
- **Plan for failure** — Decide what happens when the model, a tool or a provider is down or slow.
- **Write it down** — Record your design, the alternatives you rejected, and why.

**Try it** · Write a one-page design for your project: requirements, expected traffic, monthly cost estimate, a diagram of the main parts, and three decisions you made with the alternatives you rejected.

**Outcome** · Turn a product idea into a design you can defend, starting from requirements rather than favorite tools.

#### 02 · From Prototype to Service (Unit 6.2 · Day 85)

- **A backend for your agent** — Put your agent behind a web API so any frontend or other app can use it.
- **Stream through the API** — Send answers and agent progress to the user as they happen.
- **Know who's asking** — Identify each user so permissions, memory and cost tracking work per person.
- **Keep the app stateless** — Store conversations, agent progress and memories in a database, not inside the running app, so it can restart or scale without losing anything.
- **Long tasks in the background** — Run long agent tasks as background jobs that report progress, instead of holding a request open.
- **Protect the API** — Require authentication and limit how many requests each user can make.

**Try it** · Expose your agent through an API with a streaming endpoint. Call it from two different users and confirm each gets their own conversation and memories.

**Outcome** · Run your agent as a proper service that many users can use at once.

#### 03 · A Real Frontend (Unit 6.3 · Day 86)

- **A chat interface** — Build a simple chat page that streams answers as they arrive.
- **Show the evidence** — Display citations so users can open the source of each claim.
- **Show what the agent is doing** — Display progress, the tool in use and what it found during longer tasks.
- **Approval in the interface** — Show the user exactly what the agent wants to do and let them approve or reject it.
- **Collect feedback** — Add a simple way for users to rate answers and say what went wrong.
- **Handle failure in the interface** — Show clear messages when something fails, and let users retry or cancel.

**Try it** · Build a chat page for your agent with streaming, citations, an approval prompt and a thumbs-up or thumbs-down on each answer.

**Outcome** · Give users an interface that shows them what the agent knows, what it's doing and what it wants to do.

#### 04 · Packaging and Deploying (Unit 6.4 · Days 87–88)

- **Package everything** — Put your app in a container so it runs the same everywhere.
- **Run all the parts together** — Package your app with its database and vector database so the whole system starts with one command.
- **Deploy to a managed host** — Deploy to a hosting service that runs containers for you, so you don't manage servers yourself.
- **Secrets in the right place** — Keep API keys and passwords in the host's secret storage, never in your code or container.
- **Separate environments** — Keep development, testing and live versions apart, each with its own settings, data and keys.
- **Health checks** — Let the host check that your app is running properly and restart it if not.
- **Data changes on deploy** — Plan how database changes and re-indexing documents happen when you release a new version.

**Try it** · Deploy your app to a test environment, then to a live one. Change a setting only in the test environment and confirm the live one is unaffected.

**Outcome** · Deploy your app reliably to a live environment, with secrets and settings kept safe and separate.

#### 05 · Automatic Checks on Every Change (Unit 6.5 · Day 89)

- **Test on every change** — Run your tests automatically whenever you push code, using a tool such as **GitHub Actions**.
- **Your regression suite becomes a gate** — Run your **RAG** quality, **RAG** security, agent and agent security tests, and block a release if any of them get worse.
- **Fast checks and full checks** — Run a quick subset on every change and the full suite before each release, since evaluations cost time and money.
- **Prompts and models count as code** — A changed prompt, model version or setting goes through the same checks as a code change.
- **Release only what passed** — Build and deploy only the exact version that passed every check.

**Try it** · Set up automatic checks that run your quick test subset on every push. Push a deliberately worse prompt and confirm the release is blocked.

**Outcome** · Make it impossible to release a version of your app that's worse than the current one.

#### 06 · Releasing Safely (Unit 6.6 · Day 90)

- **Every release can be traced** — Record which code, prompt, model and settings are live, so any result can be traced to a version.
- **Release to a few users first** — Send a small share of traffic to the new version and widen it only if it behaves well.
- **Test in the shadows** — Run a new version on real questions without showing its answers to users, and compare it with the current one.
- **Compare versions with real users** — Run two versions side by side and compare quality, user ratings and cost before choosing.
- **Turn features on and off** — Release new behavior switched off and turn it on without a new deployment.
- **Roll back fast** — Be able to return to the previous version in minutes when something goes wrong.

**Try it** · Release a new prompt to 10% of traffic, compare it with the current version on quality and cost, then either roll it out to everyone or roll it back.

**Outcome** · Release changes gradually, compare them on real traffic, and undo them quickly if they cause harm.

#### 07 · Watching It in Production (Unit 6.7 · Days 91–92)

- **Trace live traffic** — Keep tracing every request in production, so you can follow any user's problem step by step.
- **The numbers to watch** — Requests, errors, response time (typical and slowest), tokens, and cost per request and per user.
- **Check quality on live traffic** — Regularly score a sample of real answers with your judges, since live questions differ from your test set.
- **Listen to users** — Collect ratings and comments, and watch signals like users rephrasing the same question or abandoning a task.
- **Spot changes over time** — Notice when the questions people ask, your documents or the model's behavior start to shift.
- **Alerts** — Get warned when errors, response times, costs or quality scores cross a limit you've set.
- **Close the loop** — Add real failures and poorly rated answers to your test set, so the regression suite learns from production.
- **Keep private data out** — Mask personal details in traces and logs, as you learned in Module 4.

**Try it** · Build a dashboard showing requests, errors, response time, cost and a live quality score. Set one alert, trigger it on purpose, and add three poorly rated answers to your test set.

**Outcome** · Know how your app is performing for real users and turn what you see into improvements.

#### 08 · Cost, Speed and Scale (Unit 6.8 · Day 93)

- **Find where time and money go** — Break each request into its parts (search, model calls, tools) and see which costs most.
- **Caching** — Reuse answers to repeated questions, cache fixed prompt sections, and cache search results.
- **Answer similar questions once** — Semantic caching reuses an answer when a new question means the same as an earlier one; decide which questions must never be answered from a cache.
- **Cheaper models for easy work** — Send simple requests to a fast, cheap model and only hard ones to a stronger model.
- **Do things at the same time** — Run independent steps in parallel instead of one after another.
- **Limits per user** — Cap usage per user so one person or a runaway agent can't run up the bill.

**Try it** · Add caching and route simple questions to a cheaper model. Measure cost per request and response time before and after, and confirm your quality score hasn't dropped.

**Outcome** · Make your app faster and cheaper without making it worse, and prove it with numbers.

#### 09 · Model Gateways and Managed Platforms (Unit 6.9 · Day 94)

- **One gateway for all models** — A model gateway sits between your app and model providers, holding keys, tracking usage and switching providers when one fails.
- **Backup providers** — Fail over automatically when a provider is down or slow, knowing the backup model may answer differently.
- **Changing models is a release** — A gateway can swap the model behind your app without a code change, so run your tests before every switch.
- **Cloud AI platforms** — Many companies can't send data to a public API and use their cloud provider's AI platform instead, which serves models inside their own account.
- **Choosing a path** — Compare public APIs, cloud AI platforms and hosting open models on data rules, cost, effort and how quickly you get new models.

**Try it** · Put a gateway in front of two model providers, make the main one fail, and confirm the backup answers within your response-time limit.

**Outcome** · Avoid depending on a single provider, and know when a cloud AI platform is the right choice.

#### 10 · Serving Open Models Yourself (Unit 6.10 · Day 95)

- **Why host your own** — Predictable cost at high volume, data that never leaves your control, and full control over which version runs.
- **The hosting ladder** — Call an open model through a provider, rent GPUs from a platform that runs it for you, or run it on your own servers.
- **Serving software** — Tools such as **vLLM** serve many requests efficiently by handling them together, which a simple loop can't do.
- **Smaller models, less memory** — Compressed (quantized) versions of a model need far less memory, with some loss of quality.
- **Sizing the hardware** — A model's size, its precision and the length of its inputs decide how much GPU memory you need.
- **Per token or per hour** — Paying per token suits low or uneven traffic; renting GPUs by the hour wins only when they're kept busy.
- **Cold starts** — A deployment that scales down to save money may answer its first request slowly.

**Try it** · Serve a small open model with vLLM or through a GPU platform. Send your test set through it and compare quality, response time and cost per thousand requests with your hosted model.

**Outcome** · Decide when serving an open model yourself is worth it, and choose the right way to host it.

#### 11 · Should You Fine-Tune? (Unit 6.11 · Day 96)

- **What fine-tuning changes** — It teaches a model a behavior, format, style or narrow skill from examples; it's a poor way to add facts that change, which is what RAG is for.
- **Prompt, RAG or fine-tune** — Try a better prompt first, add **RAG** for knowledge, and fine-tune only when your evals show those have run out.
- **When it wins** — A consistent format or tone, a narrow task like classifying or extracting at high volume, specialist language, or replacing a large model with a small one to cut cost and response time.
- **What it costs** — Collecting data, training, serving the tuned model, and tuning again whenever the base model changes.
- **Data is most of the work** — Gather examples from your traces and test set, clean them, remove duplicates and personal data, and format them as conversations.
- **Quality beats quantity** — A few hundred careful examples often beat thousands of messy ones.
- **Keep a held-out set** — Set aside examples the model never trains on, and never train on your test set.
- **Examples from a stronger model** — A stronger model can help write training examples; check the provider's terms first.

**Try it** · Pick a narrow task in your app, such as classifying incoming requests. Build 200 training examples from your traces and model-generated examples, plus 50 held-out examples, and measure how well your current prompted model does on the held-out set.

**Outcome** · Decide whether a task justifies fine-tuning, and prepare a clean dataset and a fair baseline.

#### 12 · Fine-Tuning with LoRA (Unit 6.12 · Day 97)

- **Full vs lightweight tuning** — Full fine-tuning updates every weight and needs a lot of hardware; LoRA trains a small add-on instead and gets most of the benefit.
- **Even less memory** — QLoRA trains on a compressed model, so a small model can be tuned on a single modest GPU.
- **Choosing a base model** — Pick a small open model that's good at your kind of task and whose license allows your use.
- **Tools** — Libraries such as Hugging Face PEFT and Unsloth handle LoRA training; free notebook GPUs or rented GPUs are enough for small models.
- **Key settings** — Learning rate, number of passes over the data and the size of the add-on; start from recommended values and change one thing at a time.
- **Watch for overfitting** — If the model keeps improving on training data but gets worse on held-out data, stop.
- **Managed fine-tuning** — Some providers tune models for you from an uploaded dataset, with no GPUs to manage; check where the tuned model lives and whether you can take it with you.
- **Forgetting other skills** — Tuning hard on one task can make the model worse at others.

**Try it** · Fine-tune a small open model with LoRA on your 200 examples using a free notebook GPU, and record training and held-out results as it trains.

**Outcome** · Run a LoRA fine-tune, choose sensible settings, and spot when it's overfitting.

#### 13 · Evaluating, Serving and Distilling Fine-Tuned Models (Unit 6.13 · Day 98)

- **Beat the baseline or don't ship it** — Compare the tuned model with your prompted model on the held-out set; keep it only if it's clearly better or much cheaper at the same quality.
- **Check what else changed** — Run your full regression suite to catch anything the tune made worse.
- **Cost and speed** — Compare cost and response time per request against the large model it might replace.
- **Learning from preferences** — Preference tuning (**DPO**) teaches a model from pairs of better and worse answers, useful for tone and judgment.
- **Distillation** — Use a strong model's answers to train a small model to do one task almost as well, much more cheaply.
- **Serving a tuned model** — Merge the **LoRA** add-on into the model, or serve several add-ons on one base model with tools like **vLLM**.
- **Treat it like any release** — Version the tuned model, release it gradually, and retrain when the base model or your data changes.

**Try it** · Compare your tuned small model with your prompted model on the held-out set for accuracy, cost and response time. Serve the tuned model, run your regression suite, and decide whether to use it.

**Outcome** · Prove with numbers whether a fine-tuned or distilled model earns its place, and serve it safely.

#### 14 · When Things Break (Unit 6.14 · Day 99)

- **Common incidents** — A provider outage, sudden slowness, a cost spike, a drop in answer quality, or the agent looping.
- **Decide what to do** — For each incident, know whether to roll back, switch provider, turn a feature off, or investigate first.
- **Runbooks** — Write short step-by-step guides for your most likely incidents, so anyone can act quickly.
- **Find the cause** — Use traces, dashboards and version records to work out what changed and when.
- **Learn from it** — After each incident, write a short blameless review and add a test so it can't happen the same way again.

**Try it** · Write runbooks for two incidents: a provider outage and a sudden drop in answer quality. Then simulate one and follow your own runbook.

**Outcome** · Respond to production problems calmly and quickly, and make each one less likely to happen again.

#### 15 · Whole-App Security Review (Unit 6.15 · Day 100)

- **Threat model the whole system** — Map every path for untrusted input and every action that could cause harm, across the frontend, API, **RAG** system, agent, **MCP** servers, memory, models and logs.
- **Secrets and personal data everywhere** — Check that no keys, passwords or personal details appear in code, containers, logs, traces, caches, test sets or fine-tuning data.
- **Checks at every boundary** — Make sure user input, documents, tool results and model output are each checked where they enter or leave the system.
- **The API and frontend** — Confirm authentication, per-user limits and permissions hold, and that answers can't send data to outside sites through links or images.
- **A final red-team** — Attack the live app through every door, including the parts that only exist now that it's deployed.
- **Use the checklist** — Run through the OWASP Top 10 for LLM Applications one last time against the finished app.

**Try it** · Run your full security test suite against the deployed app, then try five new attacks that target the API or frontend.

**Outcome** · Confirm that your complete, deployed app is secure from end to end, not just its individual parts.

## What we skipped, and why *(optional)*

| Topic | Why it's skipped here | Where to find it |
|---|---|---|
| Managing your own servers, load balancers and auto scaling | A managed host does this for you; learn it when your scale demands it | Full roadmap, Level 10 |
| Server-level monitoring tools | App-level metrics and live quality scores matter more for an AI app | Full roadmap, Level 10 |
| Cloud AI platforms in depth | Here you learn when they're needed; using one well is a project of its own | Full roadmap, Level 11 |
| Reinforcement fine-tuning | An advanced technique most teams don't need at first | Full roadmap, Level 13 |
| Design case studies beyond your own app | You'll find more in the interview prep section | Full roadmap, Level 9 |
| Responsible AI and regulation in depth | Beyond what your app needs to launch | Full roadmap, Level 8 |

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included. The same topics map to [full roadmap levels](../full-roadmap/README.md) where they are covered in more depth.*

- [LLM Zoomcamp (DataTalks.Club)](https://datatalks.club/blog/llm-zoomcamp.html) — a free, open-sourced course that takes an LLM application to production with evaluation, monitoring and deployment; the closest free equivalent to this level.
- [Made With ML](https://madewithml.com/) — free MLOps curriculum covering design, testing, deployment and monitoring that transfers directly to LLM applications.
- [Langfuse documentation](https://langfuse.com/docs) — open-source tracing, prompt management and cost analytics; self-hostable.
- [MLflow documentation](https://mlflow.org/docs/latest/index.html) — experiment tracking, prompt versioning and model registry.
- [GitHub Actions documentation](https://docs.github.com/en/actions) — CI/CD pipelines, gates and approvals.
- [Docker documentation](https://docs.docker.com/) — containerization, Compose and registry workflows.
- [AWS documentation — EC2, ALB, Auto Scaling, CodeDeploy](https://docs.aws.amazon.com/) — free official guides for the deployment stack used in this level.
- [Prometheus documentation](https://prometheus.io/docs/introduction/overview/) and [Grafana tutorials](https://grafana.com/tutorials/) — metrics collection and dashboards.
- [Guardrails AI documentation](https://www.guardrailsai.com/docs) and [NeMo Guardrails (GitHub)](https://github.com/NVIDIA/NeMo-Guardrails) — runtime guardrails and topical rails.
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/) — free course materials on shipping and monitoring ML systems.

## In this repository

- [LLMOps curriculum](../../104_LLMOps/README.md)
- [System design case studies](../../interview/09-real-world-case-studies.md)
- [Fine-tuning curriculum](../../102_AI-Application-Development/05-Fine-Tuning/1.%20Fine-Tuning%20Fundamentals.md)

---

[← Module 5 · Agents](module-5-agents.md) | [100 Days map](README.md) | [Portfolio projects →](projects.md)
