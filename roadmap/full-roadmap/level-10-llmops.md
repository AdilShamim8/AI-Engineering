# Level 10 · LLMOps: From Development to Production

> **Phase 5 · Production** · 11 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/10/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Take the RAG application and the agent you have already built into production — versioned, evaluated on every change, guarded, containerized, deployed on AWS, and monitored — and keep them improving once real users arrive.

*Short on time? Do the 17-day version in 100 Days of AI Engineering*

## Why this level matters

**Interview weight: 7/10**

Saying you **deployed and monitored** something on your resume shows you’ve worked in production. Docker, AWS, and CI/CD keywords also help with **automated screening**. Interview questions on it are moderate: cost, monitoring, versioning.

**On-the-job weight: 9/10**

Monitoring, versioning, cost tracking, and safe rollouts take up a **large share of the work** once a product has real users.

---

## Modules

### 01 · What LLMOps adds (M10.1 · 1 session)

- **LLMOps vs MLOps** — Understand LLMOps as the practice of shipping, operating, and improving LLM applications, and where it overlaps with and departs from classic MLOps.
- **Application vs model LLMOps** — Distinguish application LLMOps, which runs products on top of existing models, from model LLMOps, which trains and hosts the models themselves, and recognize that most teams practise the first.
- **Why LLM systems are hard to operate** — Understand what makes LLM systems harder to operate: non-deterministic outputs, prompts that change behavior without a code change, provider-side model updates, and a cost attached to every request.
- **What a release consists of** — Define what a release actually is for an LLM application: code, prompts, model version, retrieval configuration, index contents, and tool definitions, all of which must be versioned together.
- **Operating RAG vs agents** — Understand how operating a **RAG** application differs from operating an agent, from stale indexes and retrieval drift on one side to runaway loops and tool failures on the other.
- **The lifecycle of this level** — Map the lifecycle this level follows: track → evaluate → guard → serve → ship → deploy → monitor → improve.

**Mental model** · Code + prompts + model + data + tools = one release, and every part of it can change behavior

**Try it** · List every change that could alter your RAG application's answers tomorrow without anyone editing its code, and note which of them you could currently detect.

**Outcome** · Explain what has to be versioned, tested, and watched for an LLM application to be safe to change.

### 02 · Preparing your apps for production (M10.2 · 1 session)

- **Reuse your Level 4 and 5 apps** — Take the **RAG** application from Level 4 and the agent from Level 5 as the two systems this level operates, rather than building new ones.
- **Configuration, not code** — Separate configuration from code, so the model, prompts, retrieval parameters, and tool set can change without a rewrite.
- **Pinned model & dependency versions** — Pin model versions and dependency versions, so a rebuild next month produces the same system as today.
- **Traceable from the first request** — Make each request traceable from the start by attaching a request ID, the prompt version, and the model version to everything it touches.
- **The Level 7 eval set as yardstick** — Carry the evaluation dataset from Level 7 forward as the fixed yardstick every later change will be measured against.

**Try it** · Change the chunk size and the model of your RAG application through configuration alone, and confirm that no code had to change.

**Outcome** · Have two applications structured so that every behavior-changing setting is explicit, versioned, and recorded.

### 03 · Experiment tracking & prompt versioning (M10.3 · 2 sessions)

Tracking experiments

- **Experiments in MLflow** — Record each experiment in **MLflow** with its parameters, such as chunk size, top-k, model, temperature, and tool set.
- **Scores, prompts & outputs per run** — Log evaluation scores as metrics and keep prompts, configurations, and sample outputs as artifacts of the run.
- **Comparing runs** — Compare runs side by side to see which change actually moved quality, latency, or cost.
- **A baseline before changes** — Record a baseline run for both applications before changing anything.

Versioning prompts

- **A prompt registry** — Store prompts in a prompt registry such as **Langfuse**, so they are versioned, reviewed, and deployed independently of code.
- **Staging & production labels** — Label prompt versions for staging and production, and promote a version by moving the label rather than editing text in place.
- **Runtime fetch with a fallback** — Fetch prompts at runtime with caching and a pinned fallback, so a registry outage does not take the application down.
- **Rollback by moving a label** — Roll back a bad prompt by moving the production label back to the previous version.
- **Traces linked to prompt versions** — Link every trace to the prompt version that produced it, so a regression can be traced to the change that caused it.

**Try it** · Ship a second version of a prompt behind the staging label, compare it with production on your evaluation set, then promote or reject it.

**Outcome** · Keep a reproducible history of every prompt and configuration, and change either one without a code deployment.

### 04 · Evaluation as a release gate (M10.4 · 2 sessions)

Wiring the suite into the build

- **The eval suite as DeepEval tests** — Turn the Level 7 evaluation suite into automated tests that run with **DeepEval** inside an ordinary test runner.
- **RAG & agent metrics** — Score the **RAG** application on faithfulness, answer relevance, and contextual precision, and the agent on tool selection, task completion, and step efficiency.
- **Per-metric thresholds** — Set a threshold per metric against the recorded baseline, and fail the build when a change falls below it.
- **Reviewed synthetic cases** — Extend coverage with synthetic test cases generated by **DeepEval**, reviewed by a person before they join the suite.

Making the gate trustworthy

- **Handling non-determinism** — Handle non-determinism by repeating runs, using tolerance bands, and fixing sampling settings where the task allows it.
- **Fast subset vs full suite** — Budget evaluation cost and time by running a fast subset on every change and the full suite before release.
- **Prompt & model changes gated too** — Treat a prompt change, a model change, and a retrieval change exactly like a code change, so all of them pass through the same gate.
- **Gated runs logged in MLflow** — Record every gated run in **MLflow**, so the history of a metric shows which release moved it.

**Try it** · Deliberately weaken a prompt, push it, and confirm that the gate blocks it with a clear report of which metric failed.

**Outcome** · Make it impossible for a change that lowers measured quality to reach production unnoticed.

### 05 · Runtime guardrails (M10.5 · 2 sessions)

Validating inputs and outputs

- **Level 8 threats as runtime checks** — Turn the threat model from Level 8 into runtime checks that run on every request, in front of and behind the model.
- **Schema validation & re-asking** — Enforce structured outputs with **Guardrails AI**, validating against a schema and re-asking the model when validation fails.
- **Topical rails with NeMo Guardrails** — Define topical and conversational rails with **NeMo Guardrails**, and understand when that framework suits better than a validator.
- **Input & output checks** — Check inputs for prompt injection attempts and personal data, and outputs for ungrounded claims, off-topic answers, and leaked secrets.

Limiting agents and measuring the guards

- **Agent tool, step & spend limits** — Validate tool arguments before execution, and cap agent steps, retries, and spend per request so a loop cannot run unbounded.
- **Guardrail latency & false positives** — Measure what each guardrail costs in latency and how often it blocks a legitimate request.
- **Logging every block** — Log every block and every re-ask, so guardrail behavior can be reviewed and tuned rather than trusted blindly.

**Try it** · Send ten injection attempts and ten legitimate edge cases through your guarded application, then count what was blocked wrongly in each direction.

**Outcome** · Run both applications behind input, output, and agent guardrails whose cost and false-positive rate you have measured.

### 06 · Application serving & containerization (M10.6 · 3 sessions)

A production backend

- **A FastAPI backend** — Move application logic out of notebooks and scripts into a **FastAPI** backend with validated requests and typed responses.
- **Streaming with server-sent events** — Stream responses token by token with server-sent events, so users see the answer forming instead of waiting for all of it.
- **Timeouts & disconnects** — Set timeouts and handle client disconnects, so an abandoned request stops consuming model tokens.
- **Health & readiness endpoints** — Expose health and readiness endpoints that report whether the model provider and vector database are reachable.

A thin frontend

- **A thin Streamlit frontend** — Build a **Streamlit** frontend that only renders the interface and calls the backend, holding no application logic of its own.
- **Showing streams & errors** — Render the streamed response and surface errors, timeouts, and guardrail blocks to the user in plain language.

Containers

- **Docker images** — Package the backend and frontend as **Docker** images with small, reproducible builds.
- **The stack in Docker Compose** — Run the backend, frontend, and the vector database your **RAG** application already uses together with **Docker Compose**.
- **Secrets at runtime, not in images** — Supply secrets and API keys through the environment at runtime, never baked into an image.

**Try it** · Start the whole stack with one Docker Compose command on a clean machine, and confirm that streaming still works through every layer.

**Outcome** · Serve both applications as a streaming, containerized stack that runs the same way on any machine.

### 07 · CI/CD with GitHub Actions (M10.7 · 2 sessions)

- **Tests → eval gate → build** — Build a **GitHub Actions** pipeline that runs unit tests, then the evaluation gate, then builds an image, in that order.
- **Commit-tagged images** — Tag every image with the commit it was built from, and push only images that passed the gate to a registry such as **Docker Hub**.
- **Pipeline secrets** — Store provider keys and registry credentials as pipeline secrets, and keep them out of logs and pull-request builds from forks.
- **Manual approval for production** — Require a manual approval before a release reaches production, while allowing staging to deploy automatically.
- **Rollback to a known tag** — Keep the previous image deployable, so a rollback is a redeploy of a known tag rather than a rebuild.

**Mental model** · Push → unit tests → eval gate → build & tag → registry → staging → approve → production

**Try it** · Open a pull request that changes only a prompt, and follow it through the gate, the build, and the push.

**Outcome** · Automate the path from a commit to a tested, tagged, deployable image, with quality enforced before anything ships.

### 08 · Deployment on AWS (M10.8 · 3 sessions)

Servers, identity and secrets

- **EC2 with an IAM role** — Provision **EC2** instances for the application, install **Docker**, and attach an IAM role instead of storing access keys on the machine.
- **Secrets Manager** — Store provider API keys in **AWS** **Secrets Manager** and load them when the container starts.

Automated releases

- **Releases with CodeDeploy** — Use **AWS** **CodeDeploy** to pull a tagged image and replace running containers, with health checks deciding whether the release continues.
- **In-place vs blue/green** — Choose between in-place and blue/green releases, and roll back automatically when the new version fails its health checks.

Traffic and scale

- **Load balancer & streaming timeouts** — Put an Application **Load Balancer** in front of the instances, and raise its idle timeout so long streamed responses are not cut off.
- **Auto Scaling groups** — Add an **Auto Scaling** group that adds instances when busy and removes them when quiet.
- **Scale on concurrency, not CPU** — Scale on request concurrency rather than CPU, since an LLM application spends most of its time waiting on the model provider.
- **Provider rate limits cap first** — Recognize that provider rate limits usually cap throughput before your servers do, and size scaling with those limits in view.

**Try it** · Load-test the deployed application until it scales out, then check whether the bottleneck was your instances or the provider's rate limit.

**Outcome** · Run both applications on AWS with automated releases, health-checked rollbacks, load balancing, and scaling.

### 09 · Monitoring & observability (M10.9 · 3 sessions)

Infrastructure and application metrics

- **Prometheus & Node Exporter** — Run **Prometheus** to collect metrics from every instance, using **Node Exporter** for CPU, memory, disk, and network.
- **Application metrics** — Export application metrics from the backend: requests, latency percentiles, errors, model calls, tokens, and guardrail blocks.

Dashboards and alerts

- **Grafana dashboards** — Build **Grafana** dashboards that show server health, traffic, latency, error rate, and token spend side by side.
- **Alerts that need a human** — Alert on the signals that need a human, such as error-rate spikes, latency beyond budget, failed scaling, and spend above a daily limit.

Tracing and online evaluation

- **Tracing in Langfuse** — Trace every request in **Langfuse** through retrieval, model calls, and tool calls, with latency and cost recorded at each step.
- **Online evals & user feedback** — Run online evaluations on a sample of live traffic, and collect user feedback alongside them.
- **Failures back into the suite** — Turn production failures found in traces and feedback into new cases for the Level 7 evaluation suite.

**Try it** · Find the most expensive request of the past day in your traces, and explain where its tokens went.

**Outcome** · See server health, application behavior, cost, and answer quality for the live system, and feed what you find back into evaluation.

### 10 · Incidents, rollbacks & change management (M10.10 · 1 session)

- **LLM-specific incidents** — Recognize the incidents specific to LLM applications: a provider outage, a silent model update, a prompt regression, a stale index, a runaway agent, and a cost spike.
- **The lever for each cause** — Respond with the lever that matches the cause: a model fallback, a prompt rollback, an image rollback, an index rebuild, or a spend cap.
- **Runbooks** — Write a short runbook per incident type, naming the signal that detects it, the first action to take, and the person who decides.
- **Re-evaluate on model changes** — Re-run the evaluation suite whenever the provider announces a model change, before the change reaches your users.
- **Blameless reviews** — Run a blameless review after each incident, and add the case that caused it to the evaluation suite.

**Try it** · Simulate a provider outage in staging and time how long the application takes to fall back and recover.

**Outcome** · Detect, contain, and recover from LLM-specific incidents with a practised response rather than improvisation.

#### Capstone: LLMOps Project (M10.11 · 3 sessions)

- One app, the whole lifecycle Take the agent from Level 5 or the **RAG** application from Level 4 through the whole lifecycle of this level.
- Versioned prompts & tracked runs Version every prompt in a registry with a production label, and record experiments with their parameters, metrics, and artifacts.
- A CI gate that blocks a regression Gate every change in **CI** with the evaluation suite, and show the gate blocking a deliberately regressed prompt.
- Guardrails with logged blocks Run the application behind input, output, and agent guardrails, with every block logged.
- A streaming stack in Compose Serve it as a streaming **FastAPI** backend and a **Streamlit** frontend, packaged with **Docker Compose**.
- CI/CD to EC2 via CodeDeploy Build and push commit-tagged images through **GitHub Actions**, and deploy them to **EC2** with **CodeDeploy** behind a load balancer with **Auto Scaling** and **Secrets Manager**.
- Dashboards, alerts & traces Monitor it with **Grafana** dashboards and at least one working alert, and trace requests with cost and latency per step.
- A rollback & a runbook Demonstrate one rollback, of either a prompt or an image, and write the runbook for one incident type.

a deployed LLM application where every change is versioned and evaluated before release, and whose health, quality, and cost you can see while it runs.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

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

- [LLMOps curriculum (deployment, observability, safety, governance)](../../104_LLMOps/README.md)
- [CI/CD for AI systems note](../../104_LLMOps/2.%20Deployment/6.%20CI/CD%20for%20AI%20Systems.md)
- [Alerting & incident response note](../../104_LLMOps/3.%20Observability/5.%20Alerting%20%26%20Incident%20Response.md)

---

[← Level 9 · AI System Design](level-09-ai-system-design.md) | [Roadmap map](README.md) | [Level 11 · Managed AI Platforms →](level-11-managed-ai-platforms.md)
