# Level 13 · Fine-Tuning

> **Phase 6 · Frontier & Proof** · 10 modules

> **Source:** the level structure, description, interview/on-the-job weights, session counts, modules, outcomes and capstone text on this page are adapted verbatim from the [CampusX AI Engineering Roadmap 2026](https://ai-engineer-roadmap-2026.vercel.app/level/13/) (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

Fine-tune a model only when prompting, retrieval, and orchestration have measurably run out, and prove with evaluation numbers that the tune was worth its data, training, and serving cost.

## Why this level matters

**Interview weight: 7/10**

You’ll rarely do it on the job, but interviewers love asking about “**fine-tuning vs RAG**” and LoRA basics, and it’s a common job-description keyword. **Knowing the concepts is worth more** than hands-on training experience.

**On-the-job weight: 3/10**

**Rarely needed**. Better prompts, retrieval, or a different model usually solve the problem more cheaply. Mostly done by **specialist teams**.

---

## Modules

### 01 · Should you fine-tune? (M13.1 · 1 session)

- **Fine-tuning as the costliest option** — Decide between a better prompt, retrieval, tool use, a stronger base model, fine-tuning, or a combination, and treat fine-tuning as the most expensive option on that list.
- **What fine-tuning is good for** — Understand what fine-tuning is good for: consistent behavior and style, output formats a prompt cannot hold, narrow structured tasks, shorter prompts, and specializing a smaller model.
- **What it is not good for** — Understand what fine-tuning is usually not good for: teaching facts that change, which retrieval can supply fresh, and fixing a task nobody has yet defined well enough to evaluate.
- **Start from a measured failure** — Start from a named failure mode: the prompted system fails a specific, measured way, and the failure persists after reasonable prompt and retrieval work.
- **The full cost of a tune** — Estimate the full cost before starting, including data creation, training runs, evaluation, serving the tuned model, and retraining when the base model is replaced.
- **Tied to one base model** — Understand that a fine-tune ties you to one base model version, so a better base model next quarter means repeating the work rather than changing a model name.

**Mental model** · Prompt → retrieval → tools → stronger model → fine-tune, climbing only when the rung below has measurably failed

**Try it** · Take one task where a prompt is struggling, spend an hour improving the prompt and adding examples, and record how much of the gap closes before any training happens.

**Outcome** · Decide whether a task justifies fine-tuning, and state the failure it fixes, the metric that will prove it, and what the tune will cost to own.

### 02 · Data curation for fine-tuning (M13.2 · 2 sessions)

Sourcing and formatting examples

- **Specify the behavior first** — Define the behavior you want in writing before collecting data, so every example can be checked against the same specification.
- **Where examples come from** — Source examples from real usage logs, expert-written demonstrations, or carefully filtered synthetic data, and understand the bias each source brings.
- **Match the chat template** — Format examples in the chat template the base model was trained with, since a mismatched template silently degrades the tune and the model that serves it.
- **Loss on responses, not prompts** — Decide what the model should learn from each example, and mask the loss so training targets the assistant's responses rather than the prompts.
- **Few clean beats many noisy** — Understand why a few hundred clean, representative examples often beat thousands of noisy ones for a narrow task.

Cleaning, balancing and splitting

- **Cleaning bad examples** — Remove duplicates, contradictions, wrong labels, truncated responses, and synthetic examples that repeat the same phrasing.
- **Balancing edge cases** — Balance common cases with the difficult and important edge cases, so the model does not learn that the easy path is always right.
- **Leak-free splits** — Split data into training, validation, and held-out test sets, and keep near-duplicates from leaking across the split.
- **PII & licensed content** — Check the data for personal information, licensed content, and anything you would not want a model to repeat word for word.
- **Versioning the dataset** — Version the dataset alongside the training configuration, so every tuned model can be traced back to exactly what it learned from.

**Try it** · Write fifty examples by hand, generate fifty synthetically, then read all hundred and count how many of each you would actually keep.

**Outcome** · Produce a clean, versioned, correctly formatted dataset with a held-out test set that can support an honest before-and-after comparison.

### 03 · Supervised Fine-Tuning (SFT) (M13.3 · 2 sessions)

The training loop

- **What SFT changes** — Understand how supervised fine-tuning nudges a pretrained or instruction-tuned model toward labelled examples by minimizing loss on the target responses.
- **Hyperparameters that matter** — Learn the hyperparameters that matter first: learning rate, epochs, batch size, sequence length, and gradient accumulation.
- **Full vs parameter-efficient** — Understand full fine-tuning versus parameter-efficient methods, and why updating every weight is rarely necessary for a narrow task.
- **A first SFT run with TRL** — Run a small **SFT** job with a library such as TRL and confirm that the loss falls on both training and validation data.

Reading the run

- **Reading the loss curves** — Read training and validation curves to recognize underfitting, overfitting, and an unstable run that needs a lower learning rate.
- **Catastrophic forgetting** — Recognize catastrophic forgetting, where the model gains the narrow skill and loses general abilities it had before.
- **Read outputs, not just loss** — Inspect sample outputs at each checkpoint rather than trusting the loss curve alone, since a lower loss does not guarantee better answers.
- **Choosing a checkpoint** — Choose the checkpoint to keep from validation behavior, not from whichever epoch happened to finish last.

**Mental model** · Examples → loss on the target tokens → small weight updates → checkpoint chosen on validation, not on training loss

**Try it** · Train the same dataset for one, three, and eight epochs, then compare the validation curves and read ten outputs from each checkpoint.

**Outcome** · Run a supervised fine-tune, read its training curves, and pick a checkpoint you can defend.

### 04 · LoRA & QLoRA (M13.4 · 2 sessions)

How adapters work

- **LoRA adapters** — Understand **LoRA** as freezing the base model and training small low-rank adapter matrices that are added to selected layers.
- **QLoRA on a quantized base** — Understand **QLoRA** as loading the frozen base model in quantized form so the same tune fits on a much smaller GPU.
- **Rank, alpha & target modules** — Reason about the settings that matter: rank, alpha, target modules, dropout, precision, and quantization type.
- **Adapters vs full fine-tuning** — Understand the trade-off between adapter-based tuning and full-model fine-tuning on quality, memory, training time, and storage.

Running a tune on one GPU

- **PEFT with Unsloth or Axolotl** — Fine-tune an open-weight model with **PEFT** through tooling such as **Unsloth** or **Axolotl**, using a configuration file you can rerun exactly.
- **Estimating GPU memory** — Estimate GPU memory from parameter count, precision, sequence length, and batch size before renting hardware.
- **Tracking runs** — Track each run with its dataset version, configuration, and evaluation results so experiments can be compared rather than remembered.
- **DIY vs managed fine-tuning** — Compare running the tune yourself with a managed fine-tuning service, including which base models it offers and whether you can take the weights away.

**Mental model** · Frozen base model + small trained adapter = tuned behavior, at a fraction of the memory and storage

**Try it** · Run the same tune as LoRA at two ranks and as QLoRA, then compare peak GPU memory, training time, adapter size, and held-out score.

**Outcome** · Fine-tune an open-weight model efficiently on a single GPU, with a configuration and results another engineer can reproduce.

### 05 · Preference tuning & DPO (M13.5 · 2 sessions)

Preference data

- **Demonstrations vs preferences** — Understand the difference between demonstration data, which shows one correct answer, and preference data, which says that one answer is better than another.
- **Building preference pairs** — Create preference examples containing a prompt, a preferred response, and a rejected response that differ in the quality you care about.
- **Sources & rater agreement** — Collect preferences from human raters, from your own eval judges, or from production feedback, and check how often raters agree with each other.
- **Avoiding length bias** — Avoid preference pairs that differ in irrelevant ways, such as length, which teach the model the wrong lesson.

Running DPO

- **DPO intuition** — Understand the intuition behind Direct Preference Optimization without reinforcement-learning mathematics: raise the likelihood of preferred answers relative to rejected ones.
- **DPO after SFT** — Run **DPO** on top of an **SFT** checkpoint, and understand why preference tuning usually follows supervised tuning rather than replacing it.
- **What preference tuning is for** — Use preference tuning for qualities that are hard to write as a single correct answer, such as tone, helpfulness, refusal behavior, or concision.
- **When SFT is enough** — Know when **SFT** alone is sufficient and when preference optimization adds measurable value.

**Try it** · Build fifty preference pairs for a tone you want, run DPO on your SFT model, and have a blind judge compare outputs before and after.

**Outcome** · Use preference data when the desired behavior is better expressed as "A is better than B", and show that it moved the metric you targeted.

### 06 · Reinforcement Fine-Tuning (RFT) (M13.6 · 1 session)

- **Reward-based tuning** — Understand reward-based fine-tuning, where the model's outputs are scored and training pushes it toward higher-scoring behavior.
- **RFT vs SFT vs DPO** — Distinguish RFT from SFT and preference optimization by what each one learns from: examples, comparisons, or a reward.
- **Tasks with gradable outputs** — Identify tasks suited to **RFT**, where outputs can be graded reliably and automatically, such as code that must pass tests, math with checkable answers, or structured outputs with verifiable fields.
- **Reward design & reward hacking** — Understand reward design as the hard part, and recognize reward hacking, where the model optimizes the grader instead of the real objective.
- **Reaching RFT in practice** — Understand why **RFT** is usually reached through a managed service or a specialized framework rather than built from scratch.

**Mental model** · Model output → grader → reward → policy update, so the grader decides what the model learns

**Try it** · Write a grader for one task, then try to fool it by hand with outputs that score well but are wrong, and fix the grader before training against it.

**Outcome** · Recognize when reward-based tuning is justified and write a grader that rewards the behavior you actually want.

### 07 · Distillation (M13.7 · 1 session)

- **Teacher → student** — Understand teacher-to-student distillation: a stronger model produces outputs that train a smaller model for one narrow workload.
- **Generating & filtering teacher outputs** — Generate teacher outputs on inputs that resemble real traffic, and filter them with your evals before they become training data.
- **Capability for cost & latency** — Use distillation to trade a small amount of capability for lower cost, lower latency, and a model you can host yourself.
- **Copied mistakes, low diversity** — Understand the risks of copying teacher mistakes and of low-diversity synthetic data that narrows what the student can handle.
- **Teacher terms of use** — Check the teacher model's terms of use, since some providers restrict using their outputs to train competing models.

**Try it** · Distill a large model's answers on one task into a small open model, then compare quality, latency, and cost per thousand requests.

**Outcome** · Specialize a smaller model to approximate a stronger one on a specific task, with the capability given up and the cost saved both measured.

### 08 · Evaluating fine-tunes (M13.8 · 2 sessions)

Baselines and the held-out test

- **Baselines before training** — Establish the baselines before training: the base model, the best prompted version of it, and a stronger model with the same prompt.
- **Same held-out set, same judge** — Evaluate every candidate on the same held-out test set with the Level 7 evaluation framework, using the same metrics and the same judge.
- **Beyond a single score** — Compare quality, latency, cost per request, output consistency, and specific failure cases rather than a single aggregate score.

Regressions and the decision

- **Regressions outside the task** — Check for regressions outside the narrow capability you tuned, including general instruction-following, safety behavior, and formats the tune never saw.
- **Reading individual failures** — Read individual failures from the tuned model, since an average improvement can hide a new failure the base model never had.
- **Simpler alternatives, one last time** — Compare against simpler alternatives one final time, and accept the result when a better prompt or a stronger base model wins.
- **Writing the decision down** — Write the decision down: what improved, by how much, what regressed, and whether the gain justifies serving and maintaining the tune.

**Try it** · Run the base, prompted, and tuned models through your eval suite, then add ten off-task prompts and see which model holds up.

**Outcome** · Demonstrate that a fine-tune provides measurable value on the target task without unacceptable regressions elsewhere, or show convincingly that it does not.

### 09 · Serving the adapter (M13.9 · 2 sessions)

Getting the tune into production

- **Separate adapter or merged weights** — Choose between keeping a **LoRA** adapter separate from the base model and merging it into the weights, and understand what each choice means for storage, loading, and swapping.
- **Save, load & merge** — Save, load, and merge adapters, and confirm that the merged model reproduces the adapter's evaluation results.
- **Multi-LoRA serving with vLLM** — Serve the base model with one or several adapters through **vLLM**, where many adapters can share one base model on the same GPU.
- **Quantized export for Ollama** — Export the tuned model to a quantized format for local runtimes such as Ollama, and re-run evaluation after quantization, since it can undo part of the gain.
- **Managed & serverless adapter hosting** — Host an adapter on a managed platform or a serverless inference provider that serves adapters on shared base models, and compare that with running your own GPU.

Owning it in production

- **Matching template & tokenizer** — Serve with exactly the chat template and tokenizer used in training, since a template mismatch is the most common reason a good tune behaves badly in production.
- **Versioning & rollback** — Version the adapter, base model, dataset, and configuration together, and keep the previous version deployable for rollback.
- **Gradual rollout via the gateway** — Route traffic between the base model and the tuned model through your gateway, and roll the tune out gradually while watching evaluation and production metrics.
- **Latency & cost vs baseline** — Measure latency and cost per request for the served tune and compare them with the prompted baseline the tune replaced.
- **Retraining triggers** — Plan for retraining: decide what triggers it, such as a new base model, drifting inputs, or new failure cases, and how the eval suite gates each new version.

**Mental model** · Base model + versioned adapter + matching chat template → served behind your gateway → evaluated in production

**Try it** · Serve two adapters on one base model, send requests to each, then swap one for a new version without restarting the server.

**Outcome** · Deploy a fine-tuned model behind your existing gateway with versioning, rollback, and measured latency and cost, and know when it needs retraining.

#### Capstone: a LoRA that beats a prompted baseline

- A narrow task with a measured failure Choose one narrow, real task where the best prompt you can write still fails in a way you can measure.
- Metric & threshold up front Write down the failure, the metric that will judge success, and the threshold the tune must clear before any training starts.
- A strong prompted baseline Build the strongest prompted baseline you can, including few-shot examples and retrieval where relevant, and record its score on a held-out test set.
- Clean, leak-free dataset Create a clean, versioned dataset with training, validation, and held-out splits that do not leak into each other.
- Reproducible LoRA/QLoRA run Run an **SFT** tune with **LoRA** or **QLoRA** from a configuration file someone else can rerun, and add preference tuning only if the evaluation shows a gap it can close.
- Same-set comparison & cost Evaluate the tuned and prompted models on the same held-out set, and report quality, latency, tokens per request, and cost per thousand requests.
- Regressions & one failure Test for regressions on prompts outside the target task, and document at least one failure the tune introduced or failed to fix.
- Serve it, reproduce the numbers Serve the adapter behind an endpoint with the correct chat template, and confirm the served model reproduces the offline evaluation numbers.
- A fine-tuning decision record Write a one-page fine-tuning decision record: the failure, the data, the configuration, the before-and-after numbers, the cost to serve, and the retraining trigger.

a served fine-tuned model that beats a strong prompted baseline on a stated metric, with the evaluation numbers, the regressions checked, and the cost of owning it written down.

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included.*

- [Unsloth documentation — Fine-tuning guide](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide) — the fastest free path to LoRA/QLoRA fine-tuning on a single GPU, with free Colab notebooks.
- [Unsloth notebooks (GitHub)](https://github.com/unslothai/unsloth) — ready-to-run fine-tuning notebooks for popular open models.
- [Hugging Face LLM Course — fine-tuning chapters](https://huggingface.co/learn/llm-course/chapter11/1) — free coverage of SFT, instruction tuning and evaluation.
- [TRL documentation](https://huggingface.co/docs/trl/index) — SFTTrainer, DPOTrainer and reward-based training from the source.
- [PEFT documentation](https://huggingface.co/docs/peft/index) — LoRA, QLoRA and adapter management.
- [Build a Large Language Model (From Scratch) — Sebastian Raschka (GitHub)](https://github.com/rasbt/LLMs-from-scratch) — code repository accompanying the book; the pretraining-to-finetuning mechanics, free to study.
- [Axolotl documentation](https://axolotl-ai-cloud.github.io/axolotl/) — configuration-driven fine-tuning.
- [Google Colab](https://colab.research.google.com/) and [Kaggle Notebooks](https://www.kaggle.com/code) — free GPU access for small tunes.
- [vLLM — multi-LoRA serving](https://docs.vllm.ai/features/compatibility.html) — serving many adapters on one base model.

## In this repository

- [Fine-tuning curriculum (13 notes)](../../102_AI-Application-Development/05-Fine-Tuning/1.%20Fine-Tuning%20Fundamentals.md)
- [LoRA note](../../102_AI-Application-Development/05-Fine-Tuning/6.%20LoRA%20%28Low-Rank%20Adaptation%29.md)
- [QLoRA note](../../102_AI-Application-Development/05-Fine-Tuning/7.%20QLoRA%20%28Quantized%20LoRA%29.md)
- [Fine-tuning vs RAG vs prompt engineering note](../../102_AI-Application-Development/05-Fine-Tuning/9.%20Fine-Tuning%20vs%20RAG%20vs%20Prompt%20Engineering.md)

---

[← Level 12 · Multimodal 101: Beyond Text](level-12-multimodal-101.md) | [Roadmap map](README.md) | [Level 14 · Projects →](level-14-projects.md)
