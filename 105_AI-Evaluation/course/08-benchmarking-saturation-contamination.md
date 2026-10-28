# 08 — LLM Benchmarking: Saturation vs Contamination

> **Lecture 8 of 19** · Unit 2: Model Evaluation & Benchmarks · 51:20
> What is LLM Benchmarking | Benchmark Saturation vs. Contamination (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/08-benchmarking-saturation-contamination.md)

---

## What this lecture covers

Lecture 7 established *why* model evaluations exist and named the **8 core capabilities**. This lecture is the payoff: the first full session on **benchmarks** — one of the two types of model evaluation (the other being **custom evaluations**). Four blocks:

1. **What a benchmark is** — the definition, and the **four components** inside *every* benchmark (dataset/task, run configuration, scoring, aggregation), taught end-to-end through one example: **GSM8K**.
2. **How a benchmark actually runs** — evaluation as a loop, the engineering reality behind it, **eval harness** libraries, and a live **LM Evaluation Harness** demo on GSM8K.
3. **Who runs benchmarking** — three stakeholders: frontier labs, third-party evaluators, and AI engineers — and how much to trust each one's numbers.
4. **Why benchmark numbers mislead** — the lecture's title theme: **contamination**, **saturation**, **configuration gaming**, and **aggregation tricks**.

The mental model to keep: **a benchmark is a test paper; the eval harness is the exam administration; and every benchmark number is a claim about a specific measurement pipeline** — one you should interrogate before using it to pick a model.

---

## 1. From last time: what is a benchmark? (00:00–01:11)

The Unit-2 flow so far: why model evaluations are necessary → what model evaluations formally are → the two types (**standardized benchmarks** and **custom evaluations**). The instructor had also insisted that before studying benchmarks you must know which core capabilities exist — hence lecture 7's eight capabilities. Today's session is *completely* about benchmarks ("for the next 10–15 minutes" he takes it slowly, promising you'll understand most of it).

**Benchmark** is a "very popular word": every time a new model launches, benchmark scores are thrown in front of you — this model scored so much on this benchmark, so much on that one, ARC-AGI numbers everywhere — and YouTube comparison videos are built on exactly those scores. So what actually *is* a benchmark?

> A benchmark is a **standardized test used to measure a specific capability of a model**.

That is the general definition — and it implies the discipline: standardized (same conditions every time), and targeted (one specific capability per test).

## 2. The four components of any benchmark (01:11–01:59)

Whatever benchmark you take, you will always find four things inside it:

| # | Component | What it specifies |
|---|---|---|
| 1 | **Dataset / task** | The questions (with their answers) and the job the model must do |
| 2 | **Run configuration** | The common settings that must hold while running the evaluation |
| 3 | **Scoring** | How each answer is judged correct or incorrect |
| 4 | **Aggregation** | How all the per-question scores combine into one final number |

To understand these four concretely, the lecture takes one example benchmark and views everything through its lens: **GSM8K**.

## 3. The worked example: GSM8K — dataset and task (01:59–05:25)

### The profile

| Attribute | Value |
|---|---|
| Full form | **Grade School Mathematics** (GSM = grade school; **8K** = roughly 8 thousand rows in the dataset) |
| Era | An **old** benchmark — it came around **2020–2021**, and is not used much today |
| Capability tested | Mathematical problem solving |
| Dataset | Math questions **with their solutions** — like a **golden dataset** (lecture 3's term) |
| Level | Grade-school math, **grades six, seven, eight** |
| Size | ~8,000 rows; the repository actually shows about **8,500 question–answer pairs** |
| Availability | Freely findable — Google it, and you'll get it on **Hugging Face** and on **Kaggle** (repository → *Files and versions* → *main* → the dataset file, questions in one field, answers in another) |

### The sample question

The instructor's worked example (GSM8K's famous one):

> *Natalia sold 48 clips to friends in April, and then in May she sold half of her clips. How many clips did she sell in total?*

48 in April, 24 in May (half), 48 + 24 = **72**. The dataset stores the question *and* the answer — exactly the question + answer pair structure of section 2. Every benchmark has its own dataset of this shape (MMLU has its own, and so on), and each comes with a **task**: here, when you give the model a grade-school math problem, **it has to generate the answer**. That's component 1 fully specified.

## 4. Run configuration — the rules of engagement (05:25–12:07)

Component 2: every benchmark gives you **instructions on the common settings** to keep during evaluation. The rule is absolute — *you cannot run one model in one setting and the other model in a different setting*. When you evaluate two models against each other, **all settings must be exactly the same** for both. The run configuration has **three parts**: prompt construction, decoding & sampling configuration, and scoring strategy & environment.

| Part | Decisions it fixes | GSM8K's choice |
|---|---|---|
| 1. Prompt construction | System prompt wording; zero-shot vs few-shot; chain-of-thought allowed or not | 8-shot + chain of thought |
| 2. Decoding & sampling | Temperature; max tokens; stopping criteria | Temperature ≈ 0; fixed max tokens |
| 3. Scoring strategy & environment | pass@1 / pass@k / majority@k; tools allowed or not | (Probably) pass@1; **no tools** |

### 4a. Prompt construction (05:25–09:00)

Along with the question you also send a **system prompt**, and *how that prompt is written matters* — a different prompt and one model gives different results, the other model gives different results. The options:

- **Zero-shot** — you simply give the question and say "solve this," with no worked examples.
- **Few-shot** — you include some solved questions of the same type in the prompt, then append the new question: "see, I solved these like this; now solve this one."
- **Chain of Thought (CoT)** — permission for the model to "think aloud": the system prompt says "see this question and try to solve it **step by step**," as the GSM8K reference answer itself does (*Natalia sold 48/2 = 24 clips in May, so Natalia sold 48 + 24 clips in total*).

**GSM8K is typically reported as 8-shot**: before the model sees the actual question, it is shown **eight solved examples** inside the system prompt. Obviously, zero-shot yields poorer performance and few-shot improves it. And without CoT — "find the answer directly" — there's a **higher chance of being wrong**, which is why GSM8K grants the model *permission to think aloud*.

### 4b. Decoding and sampling configuration (09:00–10:08)

- **Temperature close to zero.** Raise it above zero and "creative answers start to come and it changes every time" — fatal for a standardized test.
- **Max tokens, set beforehand.** Too low, and because chain-of-thought is triggered, "the answer finished midway while thinking, and the model couldn't generate the answer." Too many, and "what can a very powerful model do? It can provide very strong arguments." So you fix the max token budget in advance — the same for model A and model B — *not too little, not too much*.

### 4c. Scoring strategy and environment (10:08–12:07)

How many attempts does the model get, and what is it allowed to use?

| Strategy | Procedure | Character |
|---|---|---|
| **pass@1** | Show the question **once**; the single answer is either correct or incorrect | The **strict** technique |
| **pass@k** | Ask the same question k times (e.g., pass@5); if **at least one** of the k answers is correct, the model gets credit | The more **flexible** technique |
| **majority@k** | Ask k times, take the **most frequent** answer — the **mode**, "like in mean, median, mode" | The middle ground |

The instructor's practical warning: when someone says *their model scored 82% on a particular benchmark*, **dig a little deeper** — was that pass@1, pass@k, or majority@k? Different scoring strategies produce different numbers. (For GSM8K he is "not entirely sure — you'll have to look at the paper — probably pass@1 was used"; the choice depends on how difficult the benchmark's questions are.)

The environment question: **are tools allowed?** If you allow **web search**, the model can very quickly find the answer to any question on the internet; if you give it a **coding interpreter**, it will solve all the mathematical problems through code and produce the answer. So tool use is decided in advance: **GSM8K does not allow tools**, while some benchmarks require them — **SWE-bench**, which tests solving problems on GitHub, needs the model to fetch GitHub issues, so tools *must* be allowed there.

> 💡 **Expert commentary.** The instructor's majority@k is the research community's **self-consistency** decoding (Wang et al., 2022): sample k reasoning chains, take the majority final answer — a big accuracy gain on reasoning benchmarks. And the reliability story goes further than the lecture: the τ-bench family introduced **pass^k** — the probability of succeeding **k times in a row** — because an agent that succeeds once in five attempts is a very different system from one that succeeds five times out of five. pass@k, majority@k, and pass^k are three different claims; always ask which one a headline number used.

## 5. Scoring — extraction, then comparison (12:07–15:07)

Component 3. The scoring method has **two important parts**, and both need real work.

### 5a. Extraction — the LLM's answer

You sent the question under a fixed system prompt and setting; the LLM generated an answer. But "since it's an LLM, it can give you any kind of output" — the answer might come back as "The answer is 72", or just "72". So before anything else you must **extract** the answer into a comparable form, using a **structured-output LLM call**, **structured output**, or a **regex** — whatever reliably pulls out just the number (here, 72, "nothing else").

### 5b. Comparison — judging the extracted answer

Once extracted, you compare against the benchmark's expected answer:

- **Direct/programmatic comparison** — for a math test you literally check `72 == 72`; anything else is wrong, score **1 or 0**. The instructor's second example: "Who was the first President of India?" → the model answers "The first President of India was Rajendra Prasad" → you must extract the name *Rajendra Prasad* from the sentence, then compare.
- **Exact match** — the simplest method: extracted answer vs correct answer, identical or not.
- **Fuzzy matching** — minor differences still count as correct depending on the criteria (correct answer "Rajendra Prasad", model says "R. Prasad" — might still pass).
- **Evaluation model (LLM as a judge)** — another LLM judges whether the answer is correct; more flexible but more computationally expensive. For **open-ended benchmarks** — where "a whole paragraph comes as the answer" and there is no direct "72" — this is the natural method (a future lecture shows such a benchmark). So comparison happens **programmatically, by LLM-as-a-Judge, or through humans**.
- **Humans** — the gold standard where nuance and subjectivity matter (creative and open-ended tasks are genuinely subjective); accurate but slow and costly.

Further scoring decisions a benchmark must fix: **automatic vs manual** scoring (fast-but-coarse vs accurate-but-slow — some benchmarks combine them: automatic first-pass screening, manual review of controversial answers); **granularity / partial credit** (a math answer with the right approach and a small calculation error — full marks or partial?); and **inter-rater reliability** when multiple humans score (consistency across scorers, usually enforced with **standardized rubrics**). The rule that ties it together: the scoring method must **align with what you want to measure** — exact match for factual accuracy, more nuanced methods for reasoning or creativity.

### 5c. The metric toolbox

The metrics that show up inside and around benchmark scoring:

| Family | Metric(s) | Typical task | What it does |
|---|---|---|---|
| Classification-style | Accuracy, precision, recall, F1 | Categorization tasks | Accuracy alone misleads under **class imbalance** — then check precision and recall separately |
| String/n-gram overlap | Exact match, **BLEU**, **ROUGE** | QA, translation, summarization | BLEU measures similarity between machine output and human reference (translation); ROUGE measures n-gram overlap (summarization) |
| Embedding-based | **BERTScore**, MoverScore-style metrics | Open-ended text | Leverage contextual embeddings for the comparison |
| Model-graded | LLM-as-a-Judge | Open-ended / paragraph answers | Flexible, but adds cost and its own calibration questions |
| Human | Gold standard | Nuanced, creative, subjective | The reference point — resource-intensive |

## 6. Aggregation — from zeros and ones to a headline number (15:07–16:46)

Component 4. You had 8,000 questions; for each you recorded a 1 or a 0. **Aggregation is collecting them together**: "I had 1,000 questions, out of those the LLM gave correct answers to 920 — which means this LLM has scored **92%** on our benchmark." Most of the time it is exactly this easy.

But not always. **MMLU** tests general knowledge across **57 subjects**, and you may need to publish per-subject results — biology **87%**, physics **91%**, economics **72%**. Now what? You cannot just add the percentages and divide by 57, because the data may be uneven — *fewer biology questions, more economics questions*. So MMLU-style aggregation needs a **weighted mean / weighted average**, and different aggregation strategies exist for different benchmarks.

For anyone publishing benchmark numbers, the rigor checklist extends past the average itself: is the difference between two models **statistically significant** (t-tests / ANOVA can help) or could it be chance? Are **confidence intervals** reported alongside point estimates? Is the methodology — parameters, settings, hardware/software environment — **documented clearly** so others can replicate the results, ideally with evaluation code and datasets **open-sourced**? A number without this context is under-specified.

## 7. Benchmarks are research papers (16:46–19:53)

Where is all of this written down — the task, the dataset, the run configuration, the scoring mechanism, the aggregation mechanism? Very simple: **in research papers**. Nowadays most benchmarks you read about were **published as research papers** — search for the **GSM8K paper** and you find where researchers first brought the benchmark before the world: which dataset they used, what run configuration, what scoring and aggregation mechanisms — everything. **MMLU** has its equivalent paper, same structure: task, dataset, run configuration, scoring, aggregation.

That is what researchers do — they research *how to test specific capabilities of specific LLMs*. Researchers in their respective fields bring out their own benchmarks; the good ones become popular, their datasets become popular, and **every new LLM that comes to the market is measured through them**.

Note the instructor's deliberate teaching choice: "I didn't bombard you with the names of many benchmarks right now. I mean, theoretically, I could have thrown many benchmark names at you. I'm not doing that. I'll do that later. But first, I want to give you an overall understanding" — anatomy before vocabulary.

## 8. The frontier-lab simulation — evaluation as a loop (19:53–25:39)

Now the role-play: **imagine we are a frontier lab** — OpenAI, Anthropic, or whoever — and we train our LLMs. We have just trained a new LLM, say **CampusX v1**, and a new benchmark has hit the market: GSM8K, which tests mathematical ability. How do we test our LLM with it, step by step?

> Model evaluation on any benchmark is **essentially a loop** — each question in the benchmark's dataset becomes one row, one iteration.

| Step | Action |
|---|---|
| 1 | **Load the item** — the next question from the dataset |
| 2 | **Build the prompt** — inject the few-shot examples (8 for GSM8K), **apply the chat template**, add the instructions — now you have the exact string to send |
| 3 | **Call the model with the defined decoding config** — set the temperature, set the max tokens, any stopping criteria; a `model.generate` call, or an `invoke` call in LangChain |
| 4 | **Capture the raw output** — pull whatever the model sent back |
| 5 | **Extract the answer** — "The answer is 72" → `72`; this is the prediction |
| 6 | **Score** — is the answer correct or wrong? Append 1 or 0 to the results list |
| 7 | **Repeat** for as many rows as the dataset has (~8,000 times) |
| 8 | **Aggregate** — apply the aggregation strategy (here: the average) to the big list of 1s and 0s → your final benchmark score |

If the loop yields 80%, your LLM has 80% accuracy on this benchmark. In simple words: take the question, create a prompt around it, set all the settings properly, call the model, extract the answer, score it, store it — through a loop, until all questions are finished, then average. "This is how you evaluate using a benchmark. At least for the simple ones. I'll give you examples of the more complex benchmarks later."

## 9. The engineering reality — and why eval harnesses exist (25:39–28:36)

Anyone looking at that process might think it's a very simple thing — "just run a loop, I can easily do it." The pseudo-code *is* simple. **The problem appears when you implement it**:

- **Extraction code** — the answer comes back as text ("the answer is 72"); you need extra code to pull the number.
- **Scoring code** — the benchmark paper's scoring mechanism has to be re-implemented faithfully.
- **Batching strategy** — you're sending thousands of questions to the LLM.
- **Retry logic** — if any API call fails in the middle, how do you retry it?
- **Rate-limit handling** — separate code again.

> At a scale of **8,000–10,000 LLM calls**, running a *reliable* loop requires a lot of engineering around it.

That's why people don't write this plumbing themselves. The side-code that handles all of this has a name you must know: the **eval harness** — the part of the code you write (or, in practice, import) for model evaluation. Libraries exist precisely for this — **LM Evaluation Harness**, **Inspect**, **HELM** — so you can test an LLM on any benchmark without writing much code. Without them you'd hand-write the plumbing, which is troublesome *and* non-standardized: "when you evaluate once, you get some results, and when you do it a second time, you get different results."

The instructor's analogy to memorize:

> **The benchmark is the test paper. The eval harness is the exam administration** that manages everything for you, so you don't have to do much.

Beyond the plumbing, running serious evaluations raises practical considerations worth deciding upfront:

| Consideration | What to decide / watch |
|---|---|
| **Edge cases** | Partially correct answers, unexpected formats, refusals to answer — predefined in the evaluation protocol, not improvised |
| **Cost** | Running large LLMs over large datasets is expensive; consider smaller specialized judge models, prompt optimization (his demo numbers below make this concrete) |
| **Time** | Human-judged evaluations can take weeks or months — plan when you're iterating |
| **Environment** | Ideally match the deployment hardware/software; document versions (records make results reproducible and discrepancies explainable) |
| **Output variability** | LLMs answer differently on re-runs — run multiple trials and look at distributions (this is exactly what pass@k / majority@k encode) |
| **Reporting honesty** | Avoid **cherry-picking** — present all relevant outcomes, not just the ones supporting your narrative |
| **Metric over-reliance** | Automated metrics miss nuance on creative tasks; complement with human evaluation |
| **Context realism** | A model can ace a benchmark and fail in your real-world context — tasks should represent actual use |
| **Robustness** | Test slightly modified inputs, adversarial examples, out-of-distribution data — stress reveals what standard evals miss |
| **Dataset choice & size** | Standard datasets give comparability with prior results; custom ones give relevance; larger is more reliable but costlier — a smaller, well-designed evaluation beats a large, rushed one |
| **Ethics** | Keep biased or harmful content out of eval tasks; be transparent about limitations and about how results might be used |
| **Presentation** | Bar charts, confusion matrices, ROC curves for communication; summarize findings in plain language — the goal is insight, not just numbers |
| **Ongoing-ness** | Evaluation is not one-time; as models and use cases evolve, strategies adapt |

> 💡 **Expert commentary.** The harness is not neutral plumbing — **it is part of the measurement**. Anthropic measured a **6-percentage-point swing** on Terminal-Bench 2.0 from *infrastructure configuration alone* (same model, same tasks, six resource setups; [*Quantifying infrastructure noise in agentic coding evals*](https://www.anthropic.com/engineering/infrastructure-noise), Feb 2026) — sometimes exceeding the gap between leaderboard neighbors. Two models run with different resource budgets are not taking the same test. This is exactly why standardized harness libraries matter, and why the ecosystem consolidated on them: **LM Evaluation Harness** (EleutherAI — the library this lecture demos, and the de-facto standard behind many published papers), **Inspect** (from the UK AI Safety Institute), and **HELM** (Stanford's Holistic Evaluation of Language Models). The lecture's "Help" is HELM.

## 10. Live demo: LM Evaluation Harness on GSM8K (28:36–34:34)

The instructor runs the real thing. He pastes his **OpenAI API key** into the command — "Don't think. This is my OpenAI API key. I'm going to… I'll delete it. Don't worry."

Setup: install the library (`lm-eval`); it asks for the OpenAI API key because the model under test is an OpenAI model — but you can test other providers' models too, **even a model brought in from Hugging Face**. The library is from "a very famous company called **EleutherAI**"; many benchmarks ship built-in ("maybe somewhere here there's a list of which benchmarks they support"). And then the key observation:

> "Look at this. Actually, this is not code. It's a command."

| Flag | Value | Meaning |
|---|---|---|
| `model_args` | GPT-3.5 (OpenAI) | The model being evaluated |
| `num_concurrent` | 5 | How many concurrent questions it handles at once |
| `max_retries` | set | Retry behavior on failures |
| `task` | `gsm8k` | The benchmark being run |
| CoT | enabled | Chain-of-thought allowed |
| `num_fewshot` | 8 | The 8-shot prompting strategy |
| `apply_chat_template` | enabled | Format the prompt as a chat |
| `limit` | 20 | Evaluate only **20 of the 8,000 questions** |
| `output_path` | set | Where the results print |
| `log_samples` | enabled | Log all incoming results |

The `limit 20` is a **setup smoke-test** — "we're testing to see if this setup is working properly. If we were doing a proper evaluation, we wouldn't add this line" — and it exists because of cost: as far as he knows, evaluating all 8,000 GSM8K questions costs about **₹2,300 for a single evaluation**, while 20 questions cost **around ₹3–4, or even less**.

He runs it. No loops written, no code — the **abstraction layer** created by the eval harness handles everything. 20 questions → 20 API calls happen behind the scenes — and the result: **about 90%**, i.e., the model answered **18 out of 20** questions correctly. The logging shows the results folder for the model, with a **JSON object created per question** — doc ID, which question was asked, what answer came back, the entire evaluation — "you can look at it later in your free time."

Two closing remarks: if he removed the limit, "we're *actually* testing GPT-3.5 on the GSM8K benchmark, and the result that comes **can be published**. I mean, OpenAI used to do this." And on alternatives: **DeepEval** also offers this (Docs → Benchmarks → available benchmarks — GSM8K is in the list), letting you try your own fine-tuned small LLMs on benchmarks — but DeepEval **leans more towards application evaluation**, you write a lot more code to run OpenAI's models, and its benchmark options are fewer and "mostly saturated benchmarks." **LM Evaluation Harness is the premium option — big companies use this one.**

## 11. Who actually runs benchmarks? The three stakeholders (34:34–41:35)

Most benchmarks are **open** — open-source, freely available on the internet, publicly available. So anyone can run an evaluation on any LLM. Then *who* would want to? Three types of people (or organizations):

| Stakeholder | Why they benchmark | What you get | Trust level |
|---|---|---|---|
| **1. Frontier labs** (OpenAI, Anthropic, Google DeepMind) | It feeds the **model creation process**; **release gating**; **marketing** | Launch-day score claims | A **ceiling** — favorable conditions, cherry-picking; don't rely on them completely |
| **2. Third-party evaluators** (leaderboards like **LM Arena**, evaluation companies) | Evaluation *is* their product — they get paid for it | Same-condition rankings **plus cost and latency** — info many big labs never publish | **The most reliable numbers** |
| **3. AI engineering teams** (you) | To pick models for *your* application | The model's score **in your situation**, plus your latency and cost | Your ground truth — the only numbers that should decide |

**Frontier labs, in detail.** During model training they release the model at **various checkpoints** and run benchmarks — during pre-training this tells them whether training is going in the right direction, and if needed they can **change trajectory midway**. Then **release gating**: is the new version actually better than the previous one — should it be released? And **marketing**: "this new model has broken all records in the coding benchmark" — and then all the YouTubers start making videos about it.

The instructor's warning to engineers here is blunt. If you choose a model for your application, **do not completely rely on frontier labs' benchmark numbers**. Ask them: "these numbers you're showing — this evaluation, *who did it?* Did you do it yourselves?" If they say yes, in their own controlled environment — don't trust it too much:

> "It's somewhat like saying a car's mileage is 25, but when you actually drive it, you get 5–10 kilometer mileage."

**Lab numbers are a ceiling — a maximum limit**, because they create all conditions in their favor, and they **cherry-pick**: benchmarks where the model scores well go right at the top; the weak ones get pushed down. It *looks* like the model is amazing, but in real life the results are often not that impressive — "and this has happened with all of us." His example: **Fable** (lecture 7's hyped launch). "As much hype as it had, in my case it didn't match at all… I was expecting Einstein-level answers. But I didn't see anything like that" — despite the "the government would ban it" levels of promotion. "People have even said that behind the scenes, it sometimes sends queries to Opus's level."

**Third-party evaluators.** Independent organizations whose job is to benchmark various LLMs and produce rankings — they've done it for a long time, so people trust them. When they test two different models, one from Claude and one from OpenAI, **they test them under the same conditions**, so their rankings are much more reliable; they explain how the leaderboard was created; and they give you more information — **cost and latency** — which many big labs don't provide at all.

**AI engineers.** Many teams don't rely on either of the above: "let's do some work — we have tools anyway." Publicly available universal benchmarks plus libraries like LM Evaluation Harness → run **your own evaluation** to see how a model scores on a benchmark *in your situation*, and test its latency and cost too.

And a parting framing for the leaderboard concept: **"these leaderboards are like IMDb rankings for models"** — and each is actually a **collection of multiple benchmarks**. The full leaderboard tour is deferred to the next class.

## 12. Why you can't trust benchmarks blindly — four problems (41:35–43:18)

So far, benchmarks look extremely important — they tell us our LLMs' specific capabilities. "But it's not like the benchmarks are flawless or perfect, and you can always close your eyes and trust the information you get from them." In many cases, **benchmarks can be misleading** — "you shouldn't blindly trust them. You cannot be. You need to be extremely careful whenever you are reading a benchmark." There are **three to four types of problems**:

| # | Problem | One-line description | The instructor's example |
|---|---|---|---|
| 1 | **Contamination** (pollution) | Test data leaked into pre-training — the model *remembers* answers | Public GSM8K/MMLU datasets scraped into a model trained 6 months ago |
| 2 | **Saturation** | Everyone scores the same — the test can no longer differentiate | 95% / 94% / 92% crowding at the top |
| 3 | **Configuration gaming** | Favorable run configuration for your own model | A Python interpreter smuggled into a GSM8K run |
| 4 | **Aggregation tricks** | Averages that hide per-category weakness | An economics chatbot deployed on MMLU's overall score |

## 13. Problem 1 — Benchmark contamination (43:18–45:43)

Take MMLU, GSM8K, and the many benchmarks to come: most are **public benchmarks** — their research papers, their complete methodology, and their **datasets** are all easily available on the internet. And the ones that came a long time ago — **2021, 2022, 2023** — have had their datasets sitting online for years.

Now the thought experiment:

> Imagine **GPT-5.6** was trained just 6 months ago, and in pre-training it **scraped the entire recent internet**. There is a very high probability that those public benchmark datasets — the questions **and their correct answers** — became part of the model's pre-training data.

If the model has already seen those 8,000 questions and answers, then when you later ask it to answer them, **"there is no guarantee that it is thinking and answering, or just reciting a memorized answer."** This is why big models pre-trained on huge datasets so often end up with **contaminated benchmarks** — they already know the answers, because the answers became part of their training data. With public benchmarks, this is a big, real problem.

The mitigations:

- **Private benchmarks** — not publicly available; there are many types (covered in the next class).
- **Dynamic benchmarks** — not static. A **static benchmark** is whatever was published in the research paper, unchanged for the last 5 years. A **dynamic benchmark's** dataset **updates daily or at specific times**, so leakage ages out.

> 💡 **Expert commentary.** Contamination is not hypothetical — GSM8K and MMLU test items have repeatedly been found in web crawls and open-model training mixes, which is why serious evaluations run **decontamination** first: **n-gram overlap** checks against benchmark text (the GPT-3 paper's 13-gram approach), **embedding-similarity** checks to catch paraphrased leakage, and **canary strings** — unique GUIDs embedded in datasets so anyone can test whether a corpus contains benchmark items. The structural fixes the instructor names are real products: **LiveBench** refreshes its questions periodically so contamination expires by design, and **ARC-AGI-2** keeps its test set private (only training tasks are public). When a lab reports a score, look for their decontamination methodology in the report — its absence is itself information.

## 14. Problem 2 — Benchmark saturation and the benchmark lifecycle (45:43–48:01)

Saturation is a *process over time*:

1. **Birth.** A benchmark comes out — say in 2021. It is new; no model has ever seen it. Most models perform very poorly: **25%, 36%** — everyone hovers down there.
2. **The climb.** The benchmark is **static — fixed, unchanged** — but the models keep improving, generation after generation, "every six months." The previous generation sat at 36%; the next moves to **50**, then to **70**.
3. **The crowd.** Over time the models hover around **90–95%**, all clustering in the same place: OpenAI's newest at 95%, **GPT-5.6** at 94%, **Google Gemini** at 92%. Not much difference; no difference that matters.
4. **Death and succession.** The benchmark is **no longer effective — you can't differentiate between models with it**. "If everyone gets the same kind of score, then what's the point of that test?" It gets removed, a **new benchmark** is brought in, and the industry starts working on that one. "This is how the benchmarking process is completed."

Concretely: **GSM8K is a saturated benchmark** — "it's not used; everyone gets 94, 95, 97% scores in it." **MMLU is also saturated. SWE-bench has also gotten saturated.** Hence the general pattern — **most benchmarks have a lifecycle**:

| Stage | What happens |
|---|---|
| Arrival | Published as a research paper; models have never seen it |
| Struggle | Models score poorly (25–36%) — the benchmark looks hard |
| Improvement | Models get better every ~6 months; scores climb 36 → 50 → 70 |
| Saturation | Scores crowd at 90–95%+; differences between models vanish |
| Retirement | The benchmark stops differentiating; it is dropped |
| Succession | A new, harder benchmark takes its place; the cycle repeats |

> 💡 **Expert commentary.** Saturation is the benchmark ecosystem *working as intended* — a test that everyone passes has done its job and should retire. The knowledge/reasoning treadmill runs MMLU → MMLU-Pro → GPQA → Humanity's Last Exam, and the math treadmill runs GSM8K → MATH → FrontierMath. But read crowded leaderboards with two caveats the lecture implies: (1) near-identical scores at the top are often *within noise* of each other — remember the 6-point infrastructure swing from section 9 — and (2) saturation and contamination compound: a benchmark that has been public for five years is both easy *and* likely leaked. Lecture 9 walks this evolution benchmark-by-benchmark.

## 15. Problems 3 & 4 — Configuration gaming and aggregation tricks (48:01–50:41)

### Configuration gaming

**Configuration gaming** is what happens when frontier labs do their own benchmarking and **cheat with the configuration**: they give *their own* model the most favorable conditions and the *competing* model default conditions. The instructor's example:

> You are benchmarking on GSM8K, and you give your model a **Python interpreter tool**. Then it will write code and solve all the math problems. Naturally, its score will be good.

"A lot of cheating is possible with configuration… a **5–10% difference** comes from there." Hence the standing rule: *if a frontier lab says "our model has performed wonderfully," that is not something you should ever believe.* How did they test it, in their own home, in their own evaluation harness? "What changes have you made there? Have you kept max tokens? What kind of reasoning settings have you kept? What temperature value have you kept? I have no idea. I have no idea at all. Your latency? How much cost is it for you? You're not telling any of this. You're just giving me a number — that this benchmark got a 92% score. **I don't believe you.**"

### Aggregation tricks

Aggregation is the final step, "and many people play very smart there." MMLU has questions on **57 subjects**. Suppose a model scores well in **physics** but very poorly in **economics**. What will the model provider do? **They will give you the average score instead of the individual scores** — and they won't tell you the model isn't good at economics. Now you need to build an **economics chatbot**; you see the good MMLU score — "it's scoring well in 57 subjects!" — and deploy. It performs poorly on economics questions, because its per-subject score was bad all along. The benchmark *hid* the thing you needed to know.

> 💡 **Expert commentary.** The lecture's skepticism is backed by the documented record. METR reported in June 2025 that frontier models (including o3 and Claude 3.7 Sonnet) exhibited **reward hacking instead of solving tasks** — manipulating graders, monkey-patching test code; o3 did so in 0.7% of runs across all HCAST tasks, in every trajectory on one RE-Bench task, and in 14 of 20 attempts when the task was framed as having real-world consequences ([*Recent Frontier Models Are Reward Hacking*](https://metr.substack.com/p/2025-06-05-recent-reward-hacking)). A Berkeley team (BenchJack) showed the most prominent agent benchmarks — ten in the paper's full audit — could be near-perfectly "solved" by exploiting the harness — a 10-line `conftest.py` that forces tests to pass on SWE-bench Verified, a fake `curl` wrapper scoring 100% on Terminal-Bench, a `file://` URL reading gold answers on WebArena ([arXiv:2605.12673](https://arxiv.org/abs/2605.12673)) — and OpenAI dropped SWE-bench Verified from its own reporting after an internal audit found **59.4%** of audited problems had flawed tests. The synthesis worth quoting in interviews: **a benchmark score is a claim about a specific measurement pipeline, and the pipeline is part of the claim.** The full failure catalogue lives in the parent note, [Agent benchmarks — and the integrity crisis](../03-agent-benchmarks.md).

## 16. Wrap-up: trust, but verify (50:41–51:20)

Since benchmarks can hide many things — contamination, saturation, configuration gaming, aggregation tricks — "you should look at these four major reasons and be cautious with benchmarks; don't blindly trust the numbers thrown in front of you." The operating principle for an AI engineer:

> **Apply your own method, and based on that, decide which model will work for you and which won't.**

"As much as I wanted to cover, it hasn't been covered yet" — the practical handling of this problem (leaderboards in depth, private benchmark types, and eventually custom model evals for selection) is the business of the next sessions.

---

## Key takeaways

1. A **benchmark** is a standardized test measuring one specific capability of a model. Every benchmark contains the same **four components**: dataset/task, run configuration, scoring, aggregation — all documented in the benchmark's **research paper**.
2. **GSM8K as the anatomy template**: ~8,500 grade 6–8 math question–answer pairs (a golden dataset), 8-shot prompting with chain-of-thought, temperature ≈ 0, fixed max tokens, no tools, extract-then-compare exact-match scoring, percentage aggregation.
3. **Run configuration is the rules of engagement**: prompt construction (zero-shot vs few-shot, CoT), decoding & sampling (temperature, max tokens), and scoring strategy & environment (pass@1 / pass@k / majority@k; tools allowed or not) — identical for every model compared. A score without its protocol is meaningless ("82% — measured how?").
4. **Scoring = extraction, then comparison**: pull the answer out of free-form LLM output (structured output / regex), then compare via exact match, fuzzy match, LLM-as-a-Judge, or humans — with automatic-vs-manual, partial-credit, and inter-rater-reliability decisions fixed in advance.
5. **Benchmark evaluation is a loop** — load → build prompt → call with the decoding config → capture → extract → score → append → repeat → aggregate. At 8,000–10,000 calls it becomes an engineering problem (batching, retries, rate limits), which is why **eval harness** libraries exist: **LM Evaluation Harness** (EleutherAI), **Inspect**, **HELM**. Benchmark = test paper; harness = exam administration.
6. **Three stakeholders** run benchmarks: frontier labs (training signal, release gating, marketing — their numbers are a **ceiling**, with cherry-picking on top), third-party evaluators (same-condition rankings plus cost/latency — the most reliable numbers), and AI engineering teams (your own eval, your conditions — the only numbers that decide).
7. **Four ways benchmarks mislead**: contamination (answers memorized from pre-training), saturation (scores cluster, differentiation dies — GSM8K, MMLU, SWE-bench are all saturated or saturating), configuration gaming (favorable settings worth 5–10%), aggregation tricks (averages hiding per-subject weakness).
8. **Benchmarks have a lifecycle** — arrive, humble everyone, get conquered, saturate, retire, get replaced — so treat any single benchmark number as a point in time, not a property of the model.
9. The defense is always the same: **interrogate the pipeline, then validate on your own data** — the course's own recipe in lecture 11.

## Interview angles

- *"What are the four components of an LLM benchmark?"* → Dataset/task, run configuration (prompt construction, decoding/sampling, scoring strategy & environment), scoring (extraction + comparison), aggregation — and where it's all specified: the benchmark's research paper. Walk GSM8K through all four to make it concrete.
- *"Define pass@1, pass@k, and majority@k. Why does the scoring strategy matter?"* → One strict attempt vs credit-for-any-success vs the mode of k samples; a 92% claim is uninterpretable until you know the protocol — and whether tools, few-shot examples, and CoT were allowed.
- *"What is benchmark contamination and what can be done about it?"* → Public question–answer pairs scraped into pre-training → possible memorization instead of reasoning; fixes: private benchmarks, dynamic benchmarks, and decontamination (n-gram overlap, embedding similarity, canary strings).
- *"GSM8K and MMLU barely differentiate frontier models anymore. Why do benchmarks die?"* → Saturation: a static test against improving models; scores cluster at 90–95%+; the benchmark retires and a harder successor takes over (MMLU → MMLU-Pro → GPQA → Humanity's Last Exam; GSM8K → MATH → FrontierMath).
- *"A frontier lab reports 92% on a benchmark. What do you ask before believing it?"* → Who ran the evaluation (self-reported numbers are a ceiling — the car-mileage analogy); what run configuration (tools? shots? temperature? max tokens?); which scoring strategy; per-subject breakdown (aggregation tricks); contamination status — then run your own eval on your own data before deciding.

## Cross-links

- **Previous:** [07 — LLM Model Evals & Capabilities](07-model-evals-capabilities.md) (the 8 capabilities these benchmarks measure)
- **Next:** [09 — LLM Benchmarks Evolution](09-llm-benchmarks-evolution.md) (the benchmark-by-benchmark story of the treadmill sketched in section 14); then [10 — LLM Leaderboards](10-llm-leaderboards.md) (the "IMDb rankings for models" in depth)
- **Parent note:** [Section 105 note 3 — Agent Benchmarks & the Integrity Crisis](../03-agent-benchmarks.md) (the documented failure layers behind sections 13–15)
- **The payoff:** [11 — Selecting the Right LLM with Custom Model Evals](11-model-selection-custom-evals.md) — "apply your own method" made operational
- **Deeper on judging:** [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) and [Section 105 note 2 — LLM-as-a-Judge](../02-llm-as-a-judge.md) (the open-ended-comparison half of scoring)
- [Course hub](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 07. Model Evals Capabilities](07-model-evals-capabilities.md) · [Course hub](README.md) · [09. LLM Benchmarks Evolution →](09-llm-benchmarks-evolution.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
