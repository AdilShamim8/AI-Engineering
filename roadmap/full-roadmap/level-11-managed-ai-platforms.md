# Level 11 · Managed AI Platforms

> **Phase 5 · Production** · 10 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/11/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Ship an AI application on the platforms teams actually buy — a cloud provider's managed platform, an open-weight hosting provider, or a router spanning several — and know which parts to hand over and which to keep.

## Why this level matters

**Interview weight: 6/10**

Matters a lot at enterprises and IT services companies, where Bedrock, Azure OpenAI, or Vertex experience is often a **hard filter**. **At startups it matters much less**.

**On-the-job weight: 7/10**

Often required, since companies frequently run AI inside their **existing cloud for compliance**. You mostly **learn the specific platform on the job**.

---

## Modules

### 01 · The three ways to consume a model (M11.1 · 1 session)

- **Three ways to consume a model** — Understand the three paths an organization can take: a provider's public API, a managed platform inside its own cloud account, or open weights it hosts itself or through an inference provider.
- **Open weights without running GPUs** — Recognize that open weights no longer imply operating GPUs, since managed platforms and inference providers serve the same open models on demand.
- **Why regulated teams cannot use a public API** — Understand why most regulated organizations cannot use a public API directly, and why that constraint decides architecture long before quality does.
- **Comparing the three paths** — Compare the three paths on identity, data handling, region, capacity, price per token, operational effort, and how quickly new models reach you.
- **Platform, gateway, or both** — Understand where a managed platform sits relative to the model gateway pattern: it can be your gateway, sit behind one, or be one provider among several that a gateway routes to.

**Mental model** · One application, three consumption paths → public API · managed platform in your cloud · open weights you or a provider host

**Try it** · Take an application you have already built against a public API and list every component that would change if the same app had to run inside a cloud account.

**Outcome** · Place any AI workload on the right consumption path and defend the choice with reasons other than familiarity.

### 02 · Platform anatomy: Bedrock, Vertex AI & Azure AI Foundry (M11.2 · 2 sessions)

What a managed platform gives you

- **The shape all three share** — Understand the shape all three share: a catalog of closed and open-weight models, one endpoint style, one identity system, one network boundary, and one bill.
- **Reading a model catalog** — Read a platform's model catalog the way you read a model card, noting which providers are offered, which regions carry them, and which versions are pinned or retired.
- **Invoking through the platform** — Understand how invocation differs from a provider SDK, including the platform's own request format, its converse-style unified API, and the provider-native passthrough where one exists.
- **Same ideas, different vocabulary** — Recognize the platform-specific vocabulary for the same ideas, so a Bedrock, Vertex AI, or Azure AI Foundry document reads as a variation rather than a new subject.

Working on one platform

- **Calling a hosted model** — Call a hosted model on one platform from application code and confirm the response, usage, and cost reporting you get back.
- **Swapping models inside one catalog** — Compare the same prompt across two models in the same catalog without changing how you authenticate, network, or bill.
- **What the platform does not give you** — Understand what the platform does not give you: prompt quality, retrieval design, evaluation depth, and product behavior remain yours.

**Try it** · Run one prompt against a closed model and an open-weight model in the same catalog, and compare quality, latency, and price per thousand tokens.

**Outcome** · Work confidently on at least one managed platform and map its concepts onto the other two.

### 03 · Identity, networking & tenancy (M11.3 · 2 sessions)

Identity and access

- **Cloud identity instead of API keys** — Replace API keys with cloud identity: roles, service accounts, and workload identity that grant a service the right to invoke a model.
- **Least privilege for model access** — Apply least privilege to model access, scoping which models, regions, and actions an application or team may use.
- **Auditing who invoked what** — Understand how platform access is audited, and why an audit trail of who invoked which model matters in regulated environments.

Network boundary and tenancy

- **Private connectivity, no public egress** — Reach a model over private connectivity so requests never traverse the public internet, and understand what that buys you and what it costs.
- **Tenant isolation on shared infrastructure** — Design tenant isolation on a shared platform: separate accounts or projects, scoped credentials, per-tenant keys, and retrieval that cannot cross a tenant boundary.
- **Encryption & customer-managed keys** — Understand encryption and key management options, including customer-managed keys for data at rest.

**Try it** · Invoke a model from a private network path with no public egress, then verify from the logs that the request never left the account.

**Outcome** · Deploy an AI workload whose identity, network path, and tenant boundaries would survive a security review.

### 04 · Regions, residency & compliance (M11.4 · 1 session)

- **Models exist per region** — Understand that a model exists in specific regions, and that the region you are permitted to use often decides which models you may design around.
- **Data residency & localization** — Plan for data residency requirements, including Indian data-localization expectations and the sector rules that sit above them.
- **Retention & training terms in writing** — Understand retention and training terms in writing: what the platform logs, for how long, who can see it, and whether your data may be used to improve a model.
- **Connecting back to governance** — Connect these controls to the governance work of Level 8, where residency, deletion, and third-party processing were named as requirements.
- **When your model is not in your region** — Handle the common case where the model you want is unavailable in your required region, through cross-region reasoning, a different model, or an exception you can document.

**Outcome** · State, for a given workload, exactly where the data goes, where it is processed, how long it is kept, and under whose terms.

### 05 · Capacity, quotas & cost (M11.5 · 2 sessions)

Capacity

- **On-demand vs provisioned throughput** — Distinguish on-demand capacity from provisioned or reserved throughput, and understand why committed capacity changes both price and rate limits.
- **Reading the quota model** — Read the quota model of a platform: requests per minute, tokens per minute, concurrent requests, and per-model limits that differ by region.
- **Planning for burst traffic** — Plan for burst traffic with queueing, backpressure, and batch endpoints instead of assuming the platform will absorb a spike.
- **Defending a quota increase** — Request and defend a quota increase with traffic evidence, since capacity is an approval process rather than a setting.

Cost

- **Cost per request, end to end** — Model cost per request end to end, including input and output tokens, retrieval calls, and any managed component you invoke along the way.
- **Attributing spend per team or tenant** — Attribute cost to a project, team, or tenant using the platform's own tagging and billing views, which a shared API key cannot do.
- **Budgets & runaway-cost alerts** — Set budgets and alerts so a runaway agent loop is caught by spend monitoring rather than by the monthly invoice.
- **Which pricing model wins at your volume** — Compare on-demand, committed, and self-hosted economics at your actual volume rather than at the volume in the pricing example.

**Try it** · Take a week of real traffic and price it three ways: on-demand, committed capacity, and open weights on your own inference.

**Outcome** · Size capacity and forecast spend for a real workload, and know at what volume each pricing model wins.

### 06 · Open-weight model platforms (M11.6 · 2 sessions)

Where open weights actually run

- **The open-weight hosting ladder** — Understand the spectrum between calling an API and operating hardware: model hubs, serverless inference providers, GPU compute platforms, and your own servers.
- **Model hubs & checkpoint trust** — Use a model hub such as Hugging Face to find open-weight models, read their cards, check licences and gated access, and judge whether a checkpoint is trustworthy.
- **Serverless inference providers** — Call an open-weight model through a serverless inference provider such as Together, Fireworks, Groq, or Replicate, where you pay per token and never see a GPU.
- **GPU compute platforms** — Understand what a GPU compute platform such as Modal, Baseten, or RunPod adds: you bring the serving stack and they schedule, scale, and bill the hardware.
- **Serving it yourself with vLLM** — Serve a model yourself with **vLLM**, TGI, or Ollama, and understand continuous batching, **KV**-cache reuse, and why a naive request loop wastes most of a GPU.

Choosing and paying for open-weight serving

- **Per-token vs per-GPU-hour** — Compare per-token pricing with per-GPU-hour pricing, and find the utilization point at which renting hardware becomes cheaper than paying per token.
- **Cold starts & scale-to-zero** — Understand cold starts and scale-to-zero, and why a deployment that idles cheaply may answer its first request slowly.
- **Sizing hardware for a model** — Size hardware for a model from parameter count, precision, quantization, and **KV**-cache growth with context length, since memory decides which GPU you need.
- **What hosting open weights buys** — Understand what hosting open weights gives you — predictable cost at volume, data that never leaves your boundary, and full control of versions — and what it asks of you in return.
- **Open vs closed on your own task** — Evaluate an open-weight model against a closed one on your own task before assuming that either is obviously better.

**Mental model** · Open weights are a ladder: someone else's API → someone else's GPUs → your GPUs

**Try it** · Serve one small open-weight model three ways — a serverless provider, a GPU platform, and locally — and compare setup effort, latency, and the cost of a thousand requests.

**Outcome** · Run an open-weight model on the right rung of the hosting ladder and justify the choice on cost, latency, control, and effort.

### 07 · Model routers & LLM gateways (M11.7 · 2 sessions)

What a router is for

- **One endpoint, many providers** — Understand a gateway as one endpoint in front of many providers: it holds the credentials, accepts one request format, and hides which model actually served the request.
- **Hosted routers vs self-hosted proxies** — Compare hosted routers such as OpenRouter and Portkey with self-hosted proxies such as LiteLLM, and with the routing built into cloud platforms and framework gateways.
- **Routing rules & automatic failover** — Route by rule — task type, cost ceiling, context length, latency target, region, or risk — and fail over automatically when a provider errors or throttles.
- **Virtual keys, budgets & quotas** — Use a gateway's spend controls: virtual keys per team or per feature, budgets, quotas, and per-key rate limits that stop one client exhausting shared capacity.
- **One view of usage and cost** — Get one view of usage, latency, errors, and cost across every provider instead of stitching separate dashboards together.

Operating a router

- **The router is on the critical path** — Understand the failure mode you have introduced, since a gateway now sits on the critical path and needs its own availability, timeouts, and a bypass plan.
- **Differences a router cannot hide** — Handle the provider differences a gateway cannot hide: tool-calling formats, structured-output support, token limits, and prompts that behave differently on each model.
- **Caching at the gateway** — Cache at the gateway, both exact-match and semantic, and decide which requests must never be answered from a cache.
- **When a router earns its place** — Decide when a router earns its place — several providers, several teams, or spend worth governing — and when one provider and a client library is the honest answer.
- **Routing changes who answers** — Keep evals in the loop, because a routing rule change swaps the model answering your users without a single line of application code changing.

**Try it** · Put a router in front of two providers, force the primary to fail, and confirm the fallback answers inside your latency budget.

**Outcome** · Run model traffic through a router that gives you failover, spend control, and one view of usage, without pretending that providers are interchangeable.

### 08 · Managed building blocks: build or buy (M11.8 · 3 sessions)

Retrieval and agents

- **Managed retrieval & knowledge bases** — Understand managed retrieval offerings such as knowledge bases and enterprise search, which package ingestion, chunking, embedding, and retrieval behind a configuration.
- **Managed retrieval vs your own stack** — Compare a managed knowledge base with the retrieval stack you built in Level 4 on control over chunking, retrieval tuning, evaluation depth, and cost at your corpus size.
- **Managed agent & workflow runtimes** — Understand managed agent and workflow runtimes, and what they assume about tools, memory, and orchestration compared with the agents you built in Level 5.

Safety, evaluation and adaptation

- **Managed guardrails** — Understand managed guardrails for content filtering, topic restriction, and sensitive-data redaction, and where they sit relative to your own checks.
- **Managed evaluation** — Understand managed evaluation offerings and judge whether their metrics answer the questions your eval suite from Level 7 was built to answer.
- **Managed fine-tuning & distillation** — Understand managed fine-tuning and distillation, including which base models can be adapted, where the resulting weights live, and whether you can take them with you.

Deciding, layer by layer

- **Deciding layer by layer** — Decide each layer separately, since adopting a managed retrieval service does not commit you to managed agents, guardrails, or evaluation.
- **What to judge each candidate on** — Judge each candidate on control, transparency, evaluation depth, cost at your volume, and how much of the behavior you must be able to explain to an auditor.
- **Measuring the portability cost** — Measure the portability cost before adopting: a prompt moves between providers in minutes, while a knowledge base, agent, or guardrail configuration usually does not.
- **When buying is the honest call** — Recognize the honest cases for buying: a small team, a standard use case, a compliance deadline, or a workload whose quality bar the managed component already clears.

**Mental model** · Buy the plumbing you cannot differentiate on, build the layer your product is judged by

**Try it** · Rebuild one component of an existing application on a managed equivalent, then compare quality, cost, and how much control you gave up.

**Outcome** · Make a defensible build-or-buy call for every layer of an AI system instead of adopting or rejecting managed services wholesale.

### 09 · Portability, lock-in & migration (M11.9 · 2 sessions)

Designing for exit

- **What travels and what does not** — Separate what is portable from what is not: prompts, evals, and application code travel easily, while managed indexes, agent definitions, and platform-specific APIs do not.
- **Keeping an abstraction in place** — Keep an abstraction between application code and provider so a model swap is a configuration change rather than a rewrite.
- **The real costs of lock-in** — Understand the real costs of lock-in beyond price: model availability, feature pace, negotiating position, and the work of proving a new platform is safe.

Moving

- **Migration as an evaluation exercise** — Plan a migration between platforms or providers as an evaluation exercise, re-running your eval suite before, during, and after the move.
- **Catalog lag & deprecation** — Handle catalog lag and platform-side deprecation, since managed catalogs trail the frontier and retire versions on their own schedule.
- **Running two platforms in parallel** — Run two platforms in parallel where the workload justifies it, using a gateway to route by capability, region, cost, or availability.
- **Multi-cloud, honestly** — Understand multi-cloud honestly: it buys resilience and leverage, and it costs duplicated evaluation, duplicated security review, and duplicated operational knowledge.

**Outcome** · Adopt a platform without being trapped by it, and move a workload between platforms without discovering the coupling too late.

#### Capstone: deploy on a managed platform (M11.10 · 1 session)

- Redeploy an app you already built Take an application you built in an earlier level and redeploy it against a managed platform, keeping the behavior and changing the plumbing.
- Cloud identity, no API key Authenticate through cloud identity with least-privilege access to a named set of models, and remove the provider API key from the application entirely.
- Private path & recorded data handling Route model traffic over a private network path, and record where the data is processed, how long it is retained, and under which terms.
- One component bought, one built Replace at least one hand-built component with a managed equivalent, and keep at least one hand-built because you can defend why.
- Re-run your evals after the move Re-run your evaluation suite on the migrated system and report what changed in quality, latency, and cost.
- A gateway with a working fallback Route the application's model calls through a gateway with a working fallback, or state why direct calls to one provider are enough at your scale.
- Capacity sizing & budget alert Size capacity for your expected traffic, set a budget alert, and state the volume at which a different pricing model would win.
- A platform decision record Write a one-page platform decision record: the workload, the constraints, the path chosen, the components bought and built, and the exit plan.

the same application, running where a regulated employer could actually run it, with the identity, network, residency, capacity, cost, and portability decisions written down.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/) — managed platform fundamentals: catalogs, IAM, guardrails, knowledge bases.
- [Google Vertex AI documentation](https://cloud.google.com/vertex-ai/docs) — model garden, endpoints and private connectivity.
- [Azure AI Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/) — Microsoft's platform for serving and adapting models.
- [Hugging Face Hub documentation](https://huggingface.co/docs/hub) — model discovery, licenses, gated access and model cards.
- [Together AI docs](https://docs.together.ai/), [Fireworks AI docs](https://docs.fireworks.ai/), [Groq docs](https://console.groq.com/docs/overview) and [Replicate docs](https://replicate.com/docs) — serverless open-weight inference providers.
- [Modal documentation](https://modal.com/docs), [Baseten docs](https://docs.baseten.co/) and [RunPod docs](https://docs.runpod.io/) — GPU compute platforms for serving open weights.
- [vLLM documentation](https://docs.vllm.ai/) — high-throughput serving with continuous batching and multi-LoRA.
- [Ollama (GitHub)](https://github.com/ollama/ollama) — run open-weight models locally in one command.
- [OpenRouter documentation](https://openrouter.ai/docs) and [LiteLLM docs](https://docs.litellm.ai/) — hosted routers and self-hosted gateways with budgets, failover and spend controls.
- [Portkey documentation](https://docs.portkey.ai/) — hosted gateway with caching, guardrails and observability.

## In this repository

- [Model serving (self-hosted) note](../../104_LLMOps/2.%20Deployment/4.%20Model%20Serving%20%28Self-Hosted%29.md)
- [Scaling & performance note](../../104_LLMOps/2.%20Deployment/5.%20Scaling%20%26%20Performance.md)
- [Curated platform and serving resources](../../awesome.md)

---

[← Level 10 · LLMOps: From Development to Production](level-10-llmops.md) | [Roadmap map](README.md) | [Level 12 · Multimodal 101: Beyond Text →](level-12-multimodal-101.md)

<!-- nav-footer -->
---

**Navigate:** [← Level 10 LLMOps](level-10-llmops.md) · [Section hub](README.md) · [Level 12 Multimodal 101 →](level-12-multimodal-101.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
