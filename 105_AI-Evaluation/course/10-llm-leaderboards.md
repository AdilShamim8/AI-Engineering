# 10 — How to Use LLM Leaderboards

> **Lecture 10 of 19** · Unit 2: Model Evaluation & Benchmarks · 30:07
> How to Use LLM Leaderboards (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/10-llm-leaderboards.md)

---

## What this lecture covers

Lecture 9 dissected benchmarks one by one. This lecture is about the place where benchmark results get **published, compared, and consumed**: the leaderboard. The arc:

1. **What a leaderboard is** — the formal definition, and its relationship to a benchmark (the test vs. the results table)
2. **Why leaderboards exist** — the instructor's seven reasons
3. **Who uses them** — five stakeholders, from AI engineers to policy makers and the open-source community
4. **The four types** — benchmark-specific, multi-benchmark, human-preference, and application/task-specific — with the lecture's live examples (HLE, LiveBench, Artificial Analysis, LM Arena, the Berkeley Function Calling Leaderboard, MTEB, Vellum)
5. **Why you cannot blindly trust them** — seven reasons, from contamination to Goodhart's Law — and **the five-step reading guideline** for using a leaderboard for model selection

If you keep one sentence from this lecture, make it the instructor's own closing line: **a leaderboard is not a selection tool — it is a filtering tool, not a decision tool.**

---

## 1. What is a leaderboard? (00:00–00:39)

The lecture opens Socratically: *"Can anyone tell me what a leaderboard is before we start? Have you seen any LLM leaderboards anywhere — in your company, or ones you use in your daily work?"*

The bridge from lecture 9 is one sentence: a **benchmark** is basically **a test to evaluate LLMs from a specific perspective**. After taking the test, results come out — and those results need to be **published somewhere**. That place is the leaderboard. Just as your school had a board showing **who came first**, an LLM leaderboard shows who came first on a common test.

The formal definition from the slide:

> An **LLM leaderboard** is a **public ranking or comparative table that shows how different LLMs perform on a common set of evaluations**.

Benchmark results are shown *in* the leaderboard; the leaderboard is where you **compare different models based on a benchmark** — so you can quickly get an idea of **which model is the best on this benchmark**.

---

## 2. Why leaderboards exist (00:39–03:52)

The instructor's list of reasons runs to seven:

| # | Reason | The instructor's framing |
|---|---|---|
| 1 | **Comparison on a common reference** | All models have taken the *same* test — who came first, who came second, who came last — so you can understand which one to use in your application |
| 2 | **Trust through a third party** | If OpenAI or Anthropic themselves say "we scored so much on this benchmark," you believe it less — they obviously want more praise for their model; a third party **without a vested interest** that tested both is far more believable |
| 3 | **Model selection without resources** | Can you test the hundreds of models that exist in the world? Not possible — it would cost a lot of money, time, and effort. If someone else does it for you, you just go to the leaderboard, **take the top 10**, and select one model |
| 4 | **Saturation detection** | When many top models cluster around the same score — his example: a knowledge benchmark where the **top 10 LLM scores sit between 92 and 94** — the benchmark is becoming saturated |
| 5 | **Mapping benchmarks to applications** | A chatbot that needs math → math benchmarks; reasoning → reasoning benchmarks; coding → coding benchmarks — leaderboards tell you which benchmarks matter for your specific use case |
| 6 | **Tracking progress over time** | New models vs. older models on the *same* benchmarks → the rate of progress in the field |
| 7 | **Identifying biases** | If certain models consistently perform poorly on certain types of questions, it might indicate a bias that needs to be addressed |

Reason 2 is the ecosystem's foundation: **self-reported scores are marketing; third-party scores are (more) information** — the reason leaderboards are "important and widely used in the AI community."

---

## 3. How the instructor actually uses them: discovering models (03:52–04:31)

A personal aside: *"Very useful. I use it a lot. I've been doing this since 2022–23 — whenever I need to find a new model, I use the LLM leaderboards."*

His pattern: usually the **top 3–4 models are from Google, OpenAI, and Anthropic**. But **scroll down a bit** and you find new models at **positions 10, 12, 15, or 20** — *"these models might not be the best, but they might work for your needs, because they are generally cheaper."* So beyond comparison, leaderboards are also a **discovery tool for new models** — a use case he returns to for the open-source community below.

---

## 4. Who uses leaderboards — five stakeholders (04:31–07:46)

The instructor announces "three–four stakeholders" and then walks through five:

| Stakeholder | How they use leaderboards |
|---|---|
| **AI engineers** ("people like you and me") | **Shortlisting.** For a math application, go to the mathematics leaderboard and pick *candidate* models — "usually you don't select just one model from the leaderboard; you shortlist candidate models, then run your evals on them and get your best model." Leaderboards "help you **filter from 100 down to 5**" |
| **Frontier labs** | Know where they currently stand ("where they are surviving") and **whether they should release their next model at all** — plus stealth testing (below) |
| **Researchers** | Learn what's currently happening, which benchmarks are saturated, and where models perform well → new strategies, new ideas, and mainly **new research directions** |
| **Policy makers & safety institutions** | Regularly observe which model is at what stage and whether any new model is **leaving others far behind** — then they have to **intervene, stop it, or make changes in between** |
| **The open-source community** | **Discovery and overnight fame** — new labs and their models get discovered, publicized, and marketed through the boards |

### The frontier lab's release decision (05:02–06:10)

The instructor role-plays: *suppose I am OpenAI. My current model is **GPT-5.5**, and my competitor's is **Opus 4.8**.* On a particular benchmark, the next model I'm training **isn't even able to beat the competitor's 4.8**. Should I release it? **No** — the moment I release it, people will immediately say it's worse than their previous Opus 4.8, and "my marketing will be bad." Instead, I go to the *next* iteration and release only when I'm **significantly ahead of others on the leaderboard**. Labs build internal plans and strategies around *when* to bring which model to market, constantly checking their position — "so for frontier labs, leaderboards are a very good thing."

### Stealth mode and pseudonyms — the Nano Banana story (06:10–06:46)

Many models arrive on leaderboards **under pseudonyms**. **Nano Banana** — *"why is Nano Banana's name so funny?"* — first appeared **in stealth mode on the image leaderboard**; nobody knew it was Google's model. "A new model called Nano Banana came and **crushed all the benchmarks**." Only when they saw it significantly beating everything did they reveal it to the public — and by then it was so popular and so much marketing had already happened that **Google kept the name Nano Banana itself**.

### Famous overnight: the open-source community (07:16–07:46)

The instructor's own habit of hunting leaderboards for new models generalizes: a new research lab with **ten–twelve people** releases a small, beautiful model that scores very well on a single benchmark and lands in the **top three–four** → the lab gets widespread publicity and **the model becomes famous overnight**. "These Chinese labs — they all gained recognition this way: suddenly a new model came in the middle of the night and started challenging the best models on some benchmark" — and the discovery, publicity, and marketing followed.

For policy makers, his example (as he recalls it): with **Gemini 1.5**, "the US government came forward immediately because they understood that this model is dangerous" — the pattern of regulators stepping in when a model pulls too far ahead of the pack.

---

## 5. Type 1 — Benchmark-specific leaderboards (07:46–10:27)

The first and simplest type: a leaderboard whose ranking comes from **a single benchmark** — models are ranked based on the results of one specific benchmark, whether **MMLU**, **HumanEval** (coding), **GSM8K** (math), or **GPQA**. All models run on that one benchmark, and the ranking is shown as a leaderboard. The purpose is narrow and honest: **inform which model is performing the best on this benchmark**.

**The live example — HLE.** The instructor pulls up the website of **HLE (Humanity's Last Exam**, lecture 9's flagship knowledge benchmark): its leaderboard shows **Gemini 3 Pro at 38%**, along with per-model details like **calibration error**. And that's the general pattern — **most popular benchmarks have their own leaderboards, created and maintained by the research teams themselves**.

**The problem: a very narrow perspective.** You learn how a model performs on one particular benchmark — and form no idea of the model overall. His verdict is blunt: *"Leaderboards [of this type] aren't that useful."*

---

## 6. Type 2 — Multi-benchmark leaderboards (10:27–13:17)

"To be honest, what's useful is this second category." These leaderboards **compare models on multiple benchmarks and evaluation metrics at once, rather than relying on just one test**, building a **cumulative score** — a single board can cover **knowledge, reasoning, math, coding, instruction following, data analysis**, all combined.

**The live example — LiveBench.** Its own description, as he reads it off the site: *"a challenging **contamination-free** LLM benchmark that includes **23 objective tasks across seven categories** — reasoning, coding, agentic coding…"* The board shows each model's score **per category** plus an **overall score** — "a much more useful leaderboard, because it gives you a general idea of how a model is, generally, in terms of different capabilities."

**Beyond accuracy — the operational columns.** These boards also carry the numbers that decide production choices: **cost per token, latency (delay), output speed, and context window size**.

**The company example — Artificial Analysis.** A company whose *job* is creating leaderboards ("somewhat like proper products"):

- separate leaderboards for **Intelligence**, **Speed**, and **Cost per task** — "a really very detailed list" — plus dedicated boards for individual benchmarks (**HLE**, **GPQA Diamond**) and domains: **coding agents, speech, image, audio, hardware**
- and then an **overall leaderboard** that brings everything together

"This is the most useful section — the one I personally use the most, and others also use the most." These boards answer the question that actually drives model selection:

> **Which model provides the most powerful overall combination of capabilities, cost, and performance?**

> 💡 **Expert commentary.** LiveBench's "contamination-free" is a design commitment, not a slogan: it adds new questions regularly and **keeps them private until every listed model has been evaluated**, publishing them only afterwards — so no model could have met the questions in pretraining (lecture 8's contamination problem, answered by a *dynamic* benchmark; HLE's private held-out set from lecture 9 is the same idea). A historical note the lecture doesn't cover: the canonical multi-benchmark board of the open-model era was the **Hugging Face Open LLM Leaderboard**, which aggregated a rotating set of benchmarks (MMLU, ARC, HellaSwag — later MMLU-Pro, GPQA…) for hundreds of open models. Hugging Face archived it in March 2025 — a textbook case of this lecture's "leaderboards go stale" problem (reason 7, below).

---

## 7. Type 3 — Human-preference leaderboards (13:17–15:45)

The third type abandons benchmarks entirely: **rankings built from human votes.** The mechanics:

1. A user comes to the website and **asks a question**.
2. The same question goes to **two models, A and B** (the user doesn't know which).
3. Both answer; the user picks the better one — implicitly scoring on **helpfulness, clarity, writing quality, creativity, and style of answering**.
4. After **many votes** are collected, a ranking is created from them.

**The famous example — LM Arena.** The instructor demos **battle mode**: ask anything — he types *"What are the LM leaderboards?"* — and behind the screen, two unknown models answer ("I don't know which models they are"). He reads both and is asked which one he liked better, with four options: **"Is this better?" · "Both are good" · "Both are bad" · "B is better."** ("Now I haven't read them — let's say I say *B is better*.") Then it reveals who they were: **Claude Opus 4.8 Search** and **Gemini**. Votes are collected "from people all over the world, all day" to build the leaderboard.

The result is a live ranking — at demo time, **Gemini 5.5** and **Sonnet 4.8 Thinking** at the top — with **category boards for general chat, code, images, and video**. "This is a type of leaderboard that exists now and is very popular."

**The limitation — human bias.** If a user *thinks* an answer is good, that doesn't mean it *is* good: "many times we humans make mistakes because the answer is very nicely formatted, or it's an answer I personally like." The defense is **scale** — it happens on a massive scale, with people all over the world — "so you can still trust it," and indeed the top models also lead on these boards.

> 💡 **Expert commentary.** How do votes become a ranking? Arena platforms convert millions of pairwise battles into ratings using the **Elo** chess-rating method — more precisely its statistical cousin, the **Bradley-Terry model**, which LMArena (formerly Chatbot Arena, from LMSYS) adopted because batch estimation is more stable than online Elo updates (Chiang et al., *Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference*, ICML 2024). The instructor's "nicely formatted" worry is also documented: arena votes correlate with **answer length and markdown formatting** (headers, bold, lists), which is why LMArena later added **style control** — a statistical adjustment that discounts those factors. Other known criticisms: the voter population isn't representative of any particular workload, and battles sample casual chat, not your domain's tasks.

---

## 8. Type 4 — Application/task-specific leaderboards, and the four types compared (15:45–17:59)

The fourth (and newest) type: leaderboards **created for a specific domain or task** — a **dedicated coding leaderboard** (a single score computed from all the coding benchmarks), or separate leaderboards for **agent tasks**, for **generating SQL queries**, or for **medical questions**.

**The live example — the Berkeley Function Calling Leaderboard:** a leaderboard that specifically measures **how good your model's tool-calling ability is**, ranking models on that alone — "working within a single domain, although it is using multiple benchmarks." (There are separate benchmark boards for coding too.)

### The four types at a glance

| Type | What it measures | Methodology | Strengths | Weaknesses | Lecture examples |
|---|---|---|---|---|---|
| **1. Benchmark-specific** | Performance on one benchmark | All models run on a single fixed benchmark | Direct answer to "who's best on X" | **"Aren't that useful"** — very narrow perspective, no overall picture | HLE's own board (Gemini 3 Pro 38%) |
| **2. Multi-benchmark** | General ability across capabilities, plus cost/latency/speed/context window | Cumulative score from multiple benchmarks and metrics | **The most useful** — "a lot more information… cost, latency, everything" | Which benchmarks, which normalization, which weights — can stay hidden (reason 4) | LiveBench, Artificial Analysis |
| **3. Human-preference** | Whether *people* prefer the answers | Pairwise blind battles → votes → ranking | Massive scale; reflects the chat experience; **very useful for marketing** ("who's at the top in the LLM Arena") | Human bias — formatting, length, confidence, entertainment (reason 6) | LM Arena |
| **4. Application/task-specific** | One domain or task | Multiple benchmarks combined *within* a single domain | Directly relevant when your application lives in that domain | Only covers that domain | Berkeley Function Calling Leaderboard |

His summary: **the least effective is the single-benchmark leaderboard; the most effective is the multi-benchmark one that measures general ability**. Human-preference boards are "quite popular" and marketing-relevant; the domain-specific ones you use when building for a specific domain. "On the internet, you'll find these four types of leaderboards." He then wraps the taxonomy and sets up the rest — "let's quickly go through the rest of it, then we'll do the Q&A session together" — before the lecture's most important stretch.

---

## 9. Why you cannot blindly trust leaderboards — reasons 1–3 (17:59–21:15)

The setup is aimed squarely at you: leaderboards are very useful and give a **brief overview of the entire LLM landscape**, but as a future AI engineer, your application work starts with **model selection — and the first step of model selection is going to the leaderboard** to see which model is at the top. So the idea sneaks in: *"if it's on the leaderboard, it must be correct."* **That's not the case.** The seven reasons, at a glance:

| # | Reason | One-line essence |
|---|---|---|
| 1 | Benchmark performance may not work in real applications | Clean test data ≠ your messy world (the Kaggle analogy) |
| 2 | Benchmarks can be corrupted | Contamination → inflated leaderboard scores |
| 3 | Models can be over-optimized for leaderboards | **Goodhart's Law** — targeting the metric breaks the metric |
| 4 | Composite leaderboards hide their methodology | Which benchmarks, which normalization, which weights? |
| 5 | Small differences are not that important | 84.3 vs 84.1 is a tie (the IIT JEE analogy) |
| 6 | Human-preference leaderboards have human bias | Longer, more confident, well-formatted, entertaining answers win votes |
| 7 | Scores are outdated, incomplete, or self-reported | Stale boards, missing models, labs grading their own homework |

### Reason 1 — Benchmark performance may not work in real applications

A model scoring **80–90 on a leaderboard** doesn't mean it will give equally good results in your real application. His analogy:

> "There was a very common saying: **if you can solve problems on Kaggle, that doesn't mean you'll become a good data scientist in real life.**"

Why? The data you're given on Kaggle is **very clean** and the problem description is **very clear**, so your job becomes easier; in the real world, **everything is messy**. The same applies here: benchmark data is usually cleaned up, and models perform well on it. The real world brings **ambiguous requests, wrong information, company-specific data, tool failures, and unusual edge cases** — whether models can handle these properly, we don't know.

### Reason 2 — Benchmarks can be corrupted

"As we discussed" (lecture 8's contamination): benchmarks can be **very easily corrupted**, and if the benchmark is corrupted, its leaderboard scores are corrupted and **inflated** — they will show higher scores. The score you're seeing might be real — but it could also be that **the model has memorized it**, or it **had this kind of question beforehand**.

### Reason 3 — Models can be over-optimized for leaderboards (Goodhart's Law)

A "very real problem" that people have been discussing for the last one–two years. A specific leaderboard becomes very popular — **LM Arena** — and the discussion centers on "who's at the top in LM Arena?" Companies see this and conclude: *we need to be at the top.* Who gets to the top? **Whoever can make people happy.** And what makes people happy in a battle? "We'll format it a bit like this, we'll give a bit of a soft answer; if we give a slightly flattering answer, there's a high chance that our selected model will get votes."

So companies **feed this kind of data to the model during training or fine-tuning**, so that instead of performing well on its actual capabilities, it performs well **only in LM Arena-like situations**. The result: **leaderboard scores go up while real-world capabilities don't improve.**

This is **Goodhart's Law** — "a very famous rule":

> "When a measurement becomes a target, it ceases to be a good measurement."

His car example: in India, people **only care about mileage** when buying a car — so the entire engineering team centers on *how to improve mileage*, and **the overall car becomes bad**, because nobody is focusing on driving dynamics, or the 0-to-100 time. "If you make any metric your goal, then that metric is no longer a good metric." Nowadays companies are creating models *to stay at the top of the leaderboard* — while actual performance doesn't get any better.

> 💡 **Expert commentary.** The instructor's suspicion of arena-targeted tuning has a documented counterpart: a widely discussed Cohere-led study, *The Leaderboard Illusion* ([arXiv:2504.20879](https://arxiv.org/abs/2504.20879), April 2025), analyzed LMArena and argued that large labs benefit from **private pre-release testing** (evaluating many variants and publishing only the best — best-of-N submission), **asymmetric access to arena conversation data** for training, and the silent deprecation of open models. Whatever one concludes about specific labs, the pattern rhymes with the parent note's integrity crisis ([Agent benchmarks — and the integrity crisis](../03-agent-benchmarks.md)): METR's finding that frontier models **reward-hack — o3 in 14 of 20 attempts when tasks were framed as having real-world consequences** is Goodhart's Law operating inside the models themselves. Treat an arena rank as one signal among several — never as ground truth.

---

## 10. Reasons 4–7 — hidden weights, meaningless gaps, human bias, stale data (21:15–24:59)

### Reason 4 — Composite leaderboards hide their methodology

Especially for boards that combine multiple benchmarks: **which benchmarks is that leaderboard including? Which is it excluding?** That depends on the leaderboard. **How have the scores been normalized?** If an overall score combines different capabilities but you haven't been told **how much weightage each capability gets**, these things remain hidden — "and sometimes they can get you into trouble." The rule: **the more transparency a leaderboard has, the better** — the more you can know about it, the better.

### Reason 5 — Small differences are not that important

Two models: one scores **84.3**, the other **84.1** — one in third place, one in fifth. The difference is only **0.2**. The instinct is "we should take the third one, we won't choose the fifth" — but there's a high chance **both are very close**, and maybe the fifth would have been **better for your application**. Over-focusing on which rank your model holds creates a **bias towards rank — that's not a good thing**. If the difference is small, the models are **at the same level** — that's the real point.

His analogy: **in IIT JEE, there won't be a huge difference between rank 1 and rank 25 — any one of them could make one or two mistakes.** The same logic applies here.

### Reason 6 — Human-preference leaderboards have human bias

(Already discussed with LM Arena.) The model at the top **doesn't mean it's the objectively best model**: humans tend to prefer **longer answers, more confident answers, well-formatted answers, and more entertaining answers** — and it's possible that the model that's actually better doesn't know these tricks, in which case **it will fail in human-made leaderboard rankings**. "So that's also a problem."

### Reason 7 — Scores are outdated, incomplete, or self-reported

Back to the **HLE leaderboard**: **Gemini 3 Pro is there with a score of 38.3** — but the most recent models are not listed. "Where do you see **Fable** or **GPT-5.6**? No — because they haven't updated it yet." Often benchmark leaderboards are simply not updated: you'll get results of **old model versions**, or won't get the new ones, or you'll find **discontinued models** — "which are not good at all." And sometimes **companies themselves provide their own model results** on a leaderboard — "the company itself is providing its own results — then why should you believe it?"

The summary of all seven: **"For these six–seven reasons, you cannot blindly trust the leaderboards. Rather, you should look at them a bit carefully. It's a necessary thing — but you cannot be blind."**

---

## 11. The five-step way to read a leaderboard (24:59–29:36)

The final and most practical stretch: you're an AI engineer creating an LLM-based application, your first task is selecting a model — **how should you actually read the leaderboards?** The instructor's guideline:

### Step 1 — Clarify your constraints *before* opening any leaderboard

Clear four things in your mind — and write them all down clearly:

| Question | What it pins down |
|---|---|
| **What kind of application are you creating?** | The capability profile you need |
| **How much latency is required in that application?** | Speed vs. capability trade-off |
| **How much cost can you bear?** | Budget envelope |
| **What are your contextual/situational requirements?** | Deployment limitations — can you use publicly available (cloud) models, or do you have to use **on-premise** models? |

Once this is clear, **you won't be biased towards the rank-one model** — you automatically start thinking objectively: "if I have to set up an on-premise model, I definitely cannot use cloud models; I will have to go towards open-source models. **This will open up your perspective.**"

### Step 2 — Go to the *right* leaderboard

You won't go blindly to any leaderboard — you'll go to the one related to your work:

| If you're building… | Go to… | Why |
|---|---|---|
| An **agent** | Agent-related leaderboards | Tool/task ability is what matters |
| A **chatbot** | **LM Arena**-type leaderboards | "There you get direct, objective measurements of chatting" |
| **RAG** | **MTEB** | "A leaderboard for ranking **embedding models** — in RAG you need an embedding model" |
| Under **budget constraints** | **Artificial Analysis** or **Vellum**-type | Accurate information on which models are how fast and how much they cost |

> 💡 **Expert commentary.** **MTEB** (the Massive Text Embedding Benchmark), hosted on Hugging Face, is the de-facto standard for embedding models — ranking them across task families like classification, clustering, reranking, retrieval, and semantic textual similarity. The lecture's caveat pattern applies with full force: **MTEB's average does not tell you how a model embeds *your* corpus** — check the retrieval-specific subtasks (and your language and domain), then still run the retriever tests of [lecture 13](13-testing-rag-retrievers.md) on your own documents before committing. Likewise, the **Berkeley Function Calling Leaderboard** is the Gorilla project's board from UC Berkeley — an example of how a university project can end up owning the ranking for an entire capability category.

### Step 3 — Read the leaderboard itself, correctly

"Understand each subject well" — the checklist of questions to ask of any leaderboard:

| Question to ask | Why it matters |
|---|---|
| What score is being achieved — and **how is it being scored**? | Same benchmark name, different scoring pipelines |
| **Who has evaluated it?** | Third party vs. self-reported (reason 7) |
| What was the **inference budget**? What logic is being applied — or not? | The run config is part of the measurement (lecture 8) |
| **How old is the evaluation dataset?** Is it being updated? | Staleness (reason 7) |
| Is any **private test set** being maintained? | The contamination defense (lectures 8–9) |
| **Have the benchmarks been saturated?** | A crowded top can no longer differentiate models |
| If the dataset is small — **is a confidence interval stated?** | If not stated, two very close models are **essentially the same** |
| For a composite score — **what weights** were given to the different capabilities? | Hidden weighting (reason 4) |

And the reading discipline: **"you cannot blindly rely on a single number — you have to read the star marks below"** — the definitions, the key concepts, the **FAQs**. "If you read these FAQs, you will be in a good position to judge the leaderboard."

### Steps 4 & 5 — Shortlist, then run your own evals

- **Step 4:** using your own criteria, **shortlist the top three to five models**.
- **Step 5** — "your fifth and most important step": when those five models sit before you, **run your own evaluation on them** — your own evaluation set — and whatever results they give, **that is where you find your best candidate**.

### The most important line of the session

> **A leaderboard is not a selection tool. A leaderboard is a filtering tool, not a decision tool.**

Going to the leaderboard and deciding "I will use this model for my application" is the **wrong strategy**. The right one: use the leaderboard to **shortlist the top four–five models**, then **run your own custom evaluation on all of them**, and select one model for your application — "and that is what we will do in the next session."

---

## 12. Where the course goes next (29:36–30:07)

The upcoming classes turn practical: the next session is **how to run your own custom evaluation on an LLM** — "this whole process that I told you, you will see it done **by hand** in the next class." His status report on the course: "We have finished benchmarks — it doesn't mean that everything is finished, but at least conceptually we have seen what happens, and we have also completed the leaderboards. **Now we will do custom evals.** Once custom evals are done, we will move towards **application evals**, where we will cover both **RAG evals and agent evals**."

---

## Key takeaways

1. **Definition:** an LLM leaderboard is a *public ranking or comparative table showing how different LLMs perform on a common set of evaluations* — the benchmark is the test; the leaderboard is where the results are published and models are compared (the school "who came first" board for the same exam).
2. **Seven reasons they exist:** common-reference comparison, third-party trust, model selection without resources ("take the top 10"), saturation detection (the 92–94 cluster), benchmark-to-application mapping, progress tracking, and bias identification.
3. **Five stakeholders:** AI engineers (shortlisting — filter 100 down to 5), frontier labs (release decisions + stealth testing à la Nano Banana), researchers (research directions), policy makers & safety institutions (intervention), and the open-source community (overnight fame). Leaderboards are also **discovery instruments** — positions 10–20 often hide cheaper models that fit your need.
4. **Four types:** benchmark-specific (narrow — "aren't that useful"), multi-benchmark (**the most useful** — LiveBench, Artificial Analysis), human-preference (LM Arena — popular, marketing-relevant, but human-biased), and application/task-specific (Berkeley Function Calling Leaderboard, MTEB).
5. **The question multi-benchmark boards answer:** *which model provides the most powerful overall combination of capabilities, cost, and performance* — the leaderboard you will use the most.
6. **Seven reasons not to trust blindly:** benchmark ≠ your application (the Kaggle analogy), contamination, over-optimization for leaderboards (Goodhart's Law — the mileage car), hidden methodology and weights, meaningless small rank gaps (84.3 vs 84.1; IIT JEE rank 1 vs 25), human-preference bias (length, confidence, formatting, entertainment), and outdated/incomplete/self-reported scores.
7. **The reading discipline:** constraints first (application, latency, cost, deployment) → the *right* leaderboard (agents → agent boards; chatbot → LM Arena; RAG → MTEB; budget → Artificial Analysis/Vellum) → the methodology (scoring, evaluator, inference budget, dataset age, private test set, saturation, confidence intervals, weights, FAQs) → shortlist 3–5 → run your own evals.
8. **The golden line:** a leaderboard is a **filtering tool, not a decision tool** — never a selection tool.

## Interview angles

- *"What's the difference between a benchmark and a leaderboard?"* → The benchmark is the test that evaluates LLMs from a specific perspective; the leaderboard is the public ranking that publishes those results on a common set of evaluations so models can be compared — the school "who came first" board for the same exam.
- *"How do you select a model for a new LLM application?"* → The five-step guideline: constraints first, the right leaderboard for the domain (MTEB for RAG embedding models, agent boards for agents, Artificial Analysis/Vellum for cost and speed), read the methodology and FAQs, shortlist 3–5, then run your own evals — "a leaderboard is a filtering tool, not a decision tool."
- *"LM Arena says model X is #1. Should we use it?"* → Not automatically: human-preference rankings carry bias toward longer, more confident, well-formatted, entertaining answers; labs can over-optimize for arenas (Goodhart's Law); check the category board and style-controlled scores, and validate on your own use case.
- *"Two models score 84.3 and 84.1. Which do you pick?"* → Statistically the same model — ask about confidence intervals; decide on fit, cost, latency, and your own evaluation, not the 0.2 gap or the rank.
- *"Why might a leaderboard score be wrong?"* → Contamination/memorization, leaderboard-targeted fine-tuning, hidden benchmark selection and weighting, stale or missing entries, and self-reported results.
- *"Which leaderboards would you consult for a RAG system, and what would you do next?"* → MTEB for the embedding model plus a multi-benchmark board for the generator (capabilities, cost, latency) — then custom evals on my own documents, which is the lecture 11 workflow.

## Cross-links

- **Previous:** [09 — LLM Benchmarks Evolution](09-llm-benchmarks-evolution.md) — the benchmarks whose results these leaderboards publish (MMLU → … → HLE).
- **Next:** [11 — Selecting the Right LLM: Running Custom Model Evals](11-model-selection-custom-evals.md) — the hands-on version of steps 4–5.
- **Deeper on benchmark integrity:** [Section 105 note 3 — Agent Benchmarks and the integrity crisis](../03-agent-benchmarks.md) — reward hacking, benchmark exploits, and harness noise: the documented record behind "don't trust blindly."
- **Related lectures:** [08 — Benchmarking: Saturation vs Contamination](08-benchmarking-saturation-contamination.md) (who runs benchmarks, the four problems) · [07 — Model Evals & Capabilities](07-model-evals-capabilities.md) (the capability map leaderboards summarize) · [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) (what to do *after* MTEB).
- [Course hub](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 09. LLM Benchmarks Evolution](09-llm-benchmarks-evolution.md) · [Course hub](README.md) · [11. Model Selection Custom Evals →](11-model-selection-custom-evals.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
