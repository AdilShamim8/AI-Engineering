# 07 — Model Evals & Capabilities

> **Lecture 7 of 19** · Unit 2: Model Evaluation & Benchmarks · 37:52
> LLM Model Evals & Capabilities (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/07-model-evals-capabilities.md)

---

## What this lecture covers

Unit 1 (lectures 2–6) built the application-eval foundations — what evals are, the workflow, why one pipeline is never enough, eval methods, offline vs online. This lecture opens **Unit 2: the model-eval track**, from a deliberately practical angle:

1. **Why AI engineers need model evals** — not "why do they exist" (that's obvious), but the four decisions they power: model selection, tracking new-model progress, safety, build-vs-buy.
2. **What a model evaluation is** — the formal definition and the four-step anatomy *every* model eval follows.
3. **The two kinds of tests** — standardized **benchmarks** vs **custom evaluation sets**, and why benchmarks alone can pick the wrong model.
4. **A worked case study** — Zomato's email router: a big, expensive, top-of-the-leaderboard model vs a small, cheap, mid-table one, settled by a custom eval on real emails.
5. **The eight core capabilities of an LLM** — knowledge & reasoning, coding & software engineering, mathematics, long context, vision & multimodality, agentic & tool use, safety & alignment, instruction following — what's measured, why labs care, where they show up in products.

If you keep one mental model from this lecture: **benchmarks tell you what a model is good at in general; your own eval tells you what it's good at *for you*.**

---

## 1. Recap — the overview is done, now the specifics (00:00–01:46)

The instructor opens every session with a recap — as a teacher it gets him into the flow: what we've studied, what comes today, how the two connect ("even if you remember, stay with me"). The course so far: why we need LLM evaluations; what they are — including the two types, **model evals** (used specifically to evaluate LLMs) and **application evals** (used to evaluate LLM-based applications), with the course's main focus on application evals (RAG evaluations, agent evaluations, and so on); the eval pipeline and how evals work; why we need multiple eval pipelines; and online evals — how to keep evaluating after deployment.

"In a way, we've discussed an overview of this entire course. Now we'll delve into the specifics."

**Today's goal: model evals** — "those evals that you use directly to test the capabilities of the AI." Too big for one lecture, so it's split across two. CampusX follows a **Why → What → How** flow — so first, why do we need model evals? Except the instructor sharpens it: we won't ask why model evals *exist*; we'll ask **why *AI engineers* need them**, because this course is taught from the AI engineer's perspective.

---

## 2. The sharpened question — why do *AI engineers* need model evals? (01:46–04:11)

Model evals exist for a simple reason: they let us **measure the capabilities of our LLMs** — and "if you can't measure, you can't improve." They give us mechanisms to evaluate multiple types of capabilities of any LLM. That justification obviously works for **frontier labs**: model evaluations help them understand what improvements to make, where things are going wrong, and how to shape their training. But an AI engineer's day-to-day job is building LLM-based applications — so why are model evals important *to you*?

The instructor's setup for the answer is an honest observation about this very course: everything so far discussed how to evaluate the **application** — the retriever, the generator, the entire pipeline of a RAG system. But:

> "In this entire discussion, we never once discussed how we were evaluating the LLM we would use to run this RAG application — which would be **the brain of this application**. How were we selecting it?"

---

## 3. The four reasons (04:11–08:39)

| # | Reason | The decision it powers |
|---|---|---|
| 1 | **Compare and select models** | Which LLM should our application use? |
| 2 | **Track whether new models actually improve** | Upgrade to the new model, or stay on the current one? |
| 3 | **Safety** | Is the model we deployed — or are about to deploy — safe? |
| 4 | **Host your own LLM vs use existing APIs** | Proprietary API vs self-hosted open-source model? |

**Reason 1 — comparing and selecting a model (04:11–05:21).** Suppose you're building a RAG application for your company today. The first question that arises: which LLM — an **OpenAI** LLM or a **Claude** LLM? It's a simple question, but "you can't say in a professional setting, 'Use whichever one you want — both are good.'" In a team meeting you need **concrete pointers** — and those come from model evaluations: "Look, these are the capabilities our application requires — and this particular LLM is scoring higher on that capability. That's why we should choose this LLM over the competitors."

**Reason 2 — is the new model actually better? (05:21–06:37).** Imagine your RAG application is deployed and running Claude's **Opus 4.8**; everything works fine. Now Claude's **Fable** arrives, and your manager asks you to do some research: should we deploy Fable, or stick with Opus? How would you know *for a fact* that Fable is better? Again, model evaluations — "you only get those numbers through model evaluations, based on which you can justify whether a new model is better than the previous one."

**Reason 3 — safety (06:37–07:24).** Model evaluations are "the only way to tell if the model you've deployed — or are about to deploy — is safe." They tell you how much your LLM is hallucinating, how safe it is to use, and whether it can be **jailbroken**.

**Reason 4 — host your own LLM, or use existing APIs? (07:24–07:59).** A very important decision: a proprietary LLM like **Claude** vs an open-source LLM like **DeepSeek**. Both have their own advantages — Claude may be more expensive and DeepSeek cheaper, but Claude may also be more powerful, with DeepSeek unable to match it across multiple capabilities. Should you use the API directly, or pull an open-source model from **Hugging Face**, install it on your company's server, write your own API, and build the entire application on top? "Again, this comparison is facilitated using model evaluations."

**The nutshell (07:59–08:39).** "Without model evaluations, you're basically blind. If you want to see which model is what, and if you want to compare two models, the only option you have is model evaluations." As an AI engineer the topic is diverse — which is why the course covers it thoroughly.

---

## 4. What a model evaluation is — definition and the four-step anatomy (08:39–11:40)

**The formal definition:**

> "Model Evaluation is a **systematic process of measuring an underlying model's capabilities, behavior, reliability, and operational characteristics under controlled conditions**."

A slightly expanded definition, but the point in a nutshell: a process that allows you to **test any model** — its capabilities and its behavior.

**The four steps.** On a technical level, every model evaluation — of any type — follows four steps:

| Step | What happens |
|---|---|
| 1. **Decide the capability to test** | LLMs are general-purpose models with many different capabilities — there is **no single model eval that can test every capability**. Pick one: reasoning, coding, safety, instruction following… |
| 2. **Come up with a test** | Devise a test (or mechanism) for that capability — this is where benchmarks and custom eval sets come in (next section) |
| 3. **Run the model under a fixed protocol** | The model takes the test. You fix a few things — which prompting to use, what the conditions will be — so the run can be repeated later, and so that if you're testing multiple models, all of them face the same conditions |
| 4. **Score and interpret** | Once the test is done, score it and interpret it — publish or interpret the resulting score |

Step 1's caveat deserves the instructor's own words:

> "**It's not like IQ in humans** — you can tell a lot about a person from a single number. Unfortunately, that's not the case with LLMs. There's a different model evaluation for each capability."

> 💡 **Expert commentary.** Step 3's "fixed protocol" is more load-bearing than it looks: **the protocol is part of the measurement**. Anthropic measured a 6-percentage-point swing on the same agent benchmark purely from infrastructure configuration, and METR documented frontier models reward-hacking — o3 in 14 of 20 attempts when tasks were framed as having real-world consequences — both covered in [Agent benchmarks — and the integrity crisis](../03-agent-benchmarks.md). Whenever you read (or run) a model eval, ask what harness, prompts, and conditions produced the number.

---

## 5. The two kinds of tests — benchmarks vs custom evaluation sets (11:40–13:32)

Step 2 ("come up with a test") has exactly two flavors:

| | **Benchmark** | **Custom evaluation set** |
|---|---|---|
| What it is | A standardized, shared test — e.g. **MMLU** or **SWE-bench** | "Data you collect from your actual task" |
| What it measures | Specific, generic capabilities — maths, reasoning, instruction following… | "What you specifically care about, rather than what's generally useful" |
| Comparability | Everyone runs the same test — numbers can be **openly compared** across models; everyone recognizes and uses it | Specific to your application and data — answers "how will this LLM perform against *my* application?" |
| Best at | Comparing models on a common ground | Deciding what's right for your task |

The natural objection, which the instructor raises himself: if benchmarks already answer the standard questions — "How good is someone at maths? At reasoning? At coding?" — **why do I need to run my own custom eval?** He answers with a scenario.

---

## 6. Case study — Zomato's email router: Model A vs Model B (13:32–18:34)

Recall the system from lecture 3: Zomato receives lots of email daily, and you build a system that reads each email's content and decides the routing. Say the categories are **billing**, **technical**, and **refunds**.

You have two model choices:

| | **Model A** | **Model B** |
|---|---|---|
| Size | A proper, large LLM | Smaller |
| Public benchmarks | Top of the table | Mid-table |
| Cost | ~**$15 per 1M tokens** | ~**$0.50 per 1M tokens** (50 cents) |
| Think of it as | A Claude-Opus-type model | A MiniMax- or Qwen-type model (at least a billion parameters) |

Common sense says: why rack your brains — "simply deploy Model A; Model A will definitely deliver good results." And on **every** public benchmark, Model A beats Model B — "he'll be good at maths, coding, language generation, everything." The obvious answer is Model A. **But deploying Model A directly at Zomato's scale could significantly increase costs.**

So instead you do a small task: **create your own dataset** — pull **200–500 past emails** and label them technical / billing / refund. You're building a **golden dataset**. Feed it to both models and compare:

| Signal | Model A | Model B |
|---|---|---|
| Classification accuracy | **94%** | **91%** |
| Urgency accuracy | **88%** | **87%** |
| Cost per 1,000 emails | **$6** | **under ~$0.21** |
| Latency per request | **4.1 s** | **0.9 s** |

(*Urgency accuracy* = reading the email content to determine how urgently the user needs a reply — the dataset carried a second label alongside the category. The instructor notes he initially misread the "less than" on the cost row: Model B's cost per 1,000 emails lands just under $0.21 — which checks out against the 30× price ratio: $6 × 0.50/15 = $0.20. And Model B's 91% is "surprisingly" close — since this task isn't that difficult.)

**The verdict:** even though Model A is very powerful and excellent compared to Model B, **for our task Model B offers a much better value proposition** — you're not losing much accuracy, but you're saving a lot of money and latency. "So we'll go with Model B." And the punchline: "If we relied solely on benchmarks, would we ever have reached this conclusion? **No.** Model A beats Model B on every benchmark. But since we ran a custom eval on our data, we discovered that Model B is actually better for our task."

That completes the picture of what model evaluation is: the process of testing a model's capabilities, done one of two ways — **standardized benchmarks** for generic capabilities, or **custom evals** tailored to your application and data, which tell you which model suits *your* type of work.

> 💡 **Expert commentary.** This table is the **benchmarks-as-shortlists** principle in action: public benchmarks measure generic capability on *their* distribution; your golden dataset measures *your* distribution, your cost, your latency. When a task sits well below the frontier (an email classifier), a 3-point accuracy gap is worth far less than a 30× cost gap and a 4.5× latency gap. Lecture 11 turns exactly this pattern into a hands-on procedure — running custom model evals to select the right LLM.

---

## 7. The plan — benchmarking first, custom evals next (18:34–19:41)

With model evals defined and their value established, the track splits in two: **this session is LLM Benchmarking** — what benchmarks are, how they work, what the benchmark evaluation process looks like, the most popular benchmarks, and — importantly — **how to read benchmarks**. The following session covers **custom model evaluations**: how to run your own evaluations on a given LLM.

But before benchmarks can be discussed in detail, there's a prerequisite — you first have to know **what capabilities an LLM can have**, because benchmarks exist to test exactly those capabilities.

---

## 8. The eight core capabilities of an LLM (19:41–20:57)

LLMs' biggest advantage: they're **general-purpose** — one model can do text generation, sentiment analysis, summarization, parts-of-speech tagging, and much more. That wide variety of capabilities is what benchmarks test — so before reading benchmarks, you should know the core capabilities.

> In total, there are **eight core capabilities that everyone has agreed upon** — and most benchmarks you'll see in the future fall into these eight categories.

A disclaimer before the tour: the next ~10 minutes are **text-heavy** — the instructor reads from a detailed document ("all the explanations here are very well written"), which he'll share with students; reading it line by line yourself would be boring, so he compressed it into 10 minutes and explains it.

| # | Capability | The question it asks | Benchmarks named so far in this course |
|---|---|---|---|
| 1 | **Knowledge & reasoning** | Does it know the facts — and can it connect them? | **MMLU** (57 subjects) |
| 2 | **Coding & software engineering** | Can it write working code and do real engineering? | **SWE-bench**, **HumanEval** |
| 3 | **Mathematics** | Can it do accurate symbolic and numerical reasoning? | **GSM8K** |
| 4 | **Long context** | Can it actually *use* very long inputs? | **Needle in a Haystack** |
| 5 | **Vision & multimodality** | Can it understand images and videos? | **MMMU** |
| 6 | **Agentic & tool use** | Can it act — browse, call tools, use a computer? | (lectures 8–10; see parent note) |
| 7 | **Safety & alignment** | Can it be trusted to behave responsibly? | (lectures 8–10) |
| 8 | **Instruction following** | Does it do exactly what the user asked? | **IFEval** |

> 💡 **Expert commentary.** Compare this list with lecture 2's version ([02 — Model vs Application Evals](02-model-vs-application-evals.md)): there, *reasoning* and *knowledge* were separate items and *safety* was absent. Lecture 7 clubs knowledge with reasoning (they're tested together — an MMLU-style question demands both) and promotes **safety & alignment** to a first-class capability — a fair reflection of where the field has moved: safety is now something labs measure and publish, not an afterthought. For capability 6, the benchmark landscape (SWE-bench, GAIA, WebArena, OSWorld, τ-bench) is covered in depth in the parent note [Agent benchmarks](../03-agent-benchmarks.md).

---

## 9. Capability 1 — Knowledge and reasoning (20:57–24:41)

These two are **clubbed together because they often work together**. The domain covers two things: how much **factual knowledge** the LLM possesses (learned during training), and whether it can **connect all that factual knowledge** — connect the dots.

| Aspect | What is tested |
|---|---|
| **Factual recall** | Basic, important questions across subjects — biology, physics, chemistry, history. (MMLU evaluates the model across **57 subjects** — "you test your LLM in all fields of knowledge") |
| **Multistep logical reasoning** | Whether the model can connect multiple facts and reach a conclusion **in the correct sequence** |

**The instructor's example question:** "Summarize the entire evolution of humankind, from the Big Bang to the present. Analyze that entire thing and tell me why today's society is the way it is." This tests multiple aspects at once: factual knowledge (which events happened since the Big Bang, in what order), then reasoning (connecting all of them to explain how they shaped today's society). "A proper task where both knowledge and reasoning are tested."

**Why frontier labs focus here:** if your model scores well in knowledge and reasoning, it simply indicates **how intelligent your model is** — that's how a model's intelligence is judged, and every model wants to score well on these benchmarks.

**Real-world uses:** a research chatbot that analyzes research papers and conducts new research; analyzing complex customer queries (the instructor: "I'm not really sure if it's as useful here, but okay — it's written"); working with technically accurate documents — upload a machine learning paper and ask questions from it, and reasoning is tested a lot; chatbots that help professionals in their field — a lawyer in law, a teacher teaching a subject.

---

## 10. Capability 2 — Coding and software engineering (24:41–27:09)

"In my opinion, this is the **most important from an economic perspective**" — any model provider or frontier lab can make a lot of money here. The instructor's evidence: **Cursor's valuation reached $60 billion** — all because of this capability. LLMs can code and perform software engineering tasks, software development is a huge field, and a model that performs well there "creates a lot of value for a lot of enterprises."

**The basic question:** can the model **write code that actually works**? Beyond that: can it perform real software engineering tasks — can it **edit large codebases**, "which is your primary software engineering task"?

| Sub-skill | What the test asks |
|---|---|
| **Functional-level code generation** | Given an English sentence — "make me a function in Python" — produce the function |
| **Test generation & self-repair** | Generate test cases; improve the code based on errors in those tests |
| **Bug fixing** | Go into an existing codebase and fix bugs — "also very important" |
| **Multi-file, long-horizon tasks** | Given an entire codebase, refactor it based on a single aspect |
| **Command-line operation** | Run multiple commands: install packages, configure servers, set up an environment |
| **API & function calling** | Call APIs and functions |

**Real-world relevance:** building any **AI coding agent** — "there are many in the world now" — means leaning on exactly this capability.

---

## 11. Capability 3 — Mathematics (27:09–28:53)

Measures whether the model can perform **accurate symbolic and numerical reasoning**. Think of maths as a form of reasoning — working step by step to arrive at a solution — but one with more direct real-world applications. The tests climb a ladder:

| Level | What the model must do |
|---|---|
| **Grade school** | Solve 7th–8th grade maths problems |
| **Competition** | Olympiad problems — "which require a little creative thinking" |
| **Undergraduate** | Undergraduate-level problems |
| **Research** | Open problems "for which solutions don't currently exist — are you able to reach them or not?" |

**Real-world uses:** scientific computing, financial modeling, engineering simulations, data analysis. A very important capability with many benchmarks — "testing it is super important."

---

## 12. Capability 4 — Long context (28:53–30:49)

**Context** = how much information the model can see when producing an answer — and it's limited. Today's models advertise token limits **up to 1 million**. But even within that window, "is it able to use everything or not? **That is the big question.**"

The domain measures whether a model can **effectively use information from very long inputs** — sometimes hundreds of thousands of tokens:

- Extract a small fact from a very long context
- Fetch the details of a person or entity from a very large document
- Summarize a very large context
- Working as a coding agent, **maintain the complete context of a very large codebase**

**Why it matters:** models often claim a context window of 128K, 200K, or 1M tokens — "but what actually happens is that as your chat grows, the **context retention capability diminishes, and the chat quality deteriorates over time**." Testing this capability tells you which model *actually* handles large contexts. And it's applicable everywhere: "no matter what kind of LLM-based application you build, long context becomes a key capability to measure."

---

## 13. Capability 5 — Vision and multimodality (30:49–31:22)

Step beyond text and enter the domain of vision: can the model understand **vision — images, videos**? Important because **"we live in a multimodal world, and text alone won't suffice."** The instructor's examples of that world: you turn on a video and immediately ask, "Hey — there's all this stuff in the fridge in front of you; tell me, what can we make from this?" Or you're in a library, asking for a particular book. Hence there should be benchmarks to test multimodal capabilities.

(He notes he's summarizing this one — the underlying document has everything "written in great detail" and is worth reading.)

---

## 14. Capability 6 — Agentic and tool use (31:22–32:29)

A capability that's "gradually becoming more important" — and the one the **entire field of agentic AI emerged from**: "you don't just need machines that can print text — **you need machines that can do something**. And to do that, you need to attach tools."

What's tested — how effectively the model can use tools:

- Browse the web on its own
- Call structured tools
- Interact with APIs
- Use desktops and computers

**Why frontier labs care:** agentic applications are already everywhere; to build them you need **a reliable model that can perform agentic tasks** — and these benchmarks and capabilities tell you whether a model is capable.

---

## 15. Capability 7 — Safety and alignment (32:29–34:10)

Very straightforward at the top: measure whether the model can be **trusted to behave responsibly**. What gets checked:

| Check | The question |
|---|---|
| **Harmful content** | Is it generating harmful content? |
| **Adversarial robustness** | Is it vulnerable to adversarial attacks — is it easy to attack/jailbreak? |
| **Truthful vs sycophantic** | Is it truthful — or does it flatter? Present an idea to a chatbot and "it immediately starts praising you — 'yes, yes, this is the best idea in the world.' It shouldn't be like that. Ideally, a model should be truthful." |

The instructor's personal experience: "I've always found **Claude much more truthful than ChatGPT**. GPT often gets me into trouble. Claude is not like that — it will tell you, 'you said this — this is a flaw in what you said.'"

**A recent addition — cybersecurity skills.** Newer models and benchmarks test whether an LLM has cybersecurity-related skills: can it do **cryptography, reverse engineering, digital forensics**? "This recent Claude Fable was a model that was very strong in cybersecurity and had identified many vulnerabilities in existing software" — and there are benchmarks specifically for testing these skills.

**Why safety is crucial for frontier labs:** government pressure to ensure models are safe, plus a huge **reputational concern** — "any minor incident could bring their business to a halt."

> 💡 **Expert commentary.** The checks the instructor lists map onto real benchmark families: truthfulness/sycophancy → **TruthfulQA** and its sycophancy variants; harmful content and jailbreak robustness → adversarial suites such as **AdvBench** and **HarmBench** (the "can it be jailbroken?" question is exactly what red teaming measures — see [106 — AI Security & Safety](../../106_AI-Security-Safety/README.md)); and the cybersecurity skills he names — cryptography, reverse engineering, digital forensics — are what CTF-style benchmarks like **Cybench** and **NYU CTF** test. Safety evals typically run as gated, pre-release pipelines precisely because of the government pressure and reputational exposure he describes.

---

## 16. Capability 8 — Instruction following (34:10–35:50)

"A bit **underrated, but very important**." Measure whether the model did **exactly what the user told it to do**:

- "If I asked the model to give me an answer in a bullet list — did it do that or not?"
- "I said answer in less than 200 words."
- "I said give a friendly answer."

Is the model following all these instructions or not? Testing this is crucial because it **directly translates into user feedback**: if the model doesn't listen, the user will be unhappy, **abandon the product, or go to another company**. Also tested: if the user gives **ambiguous** instructions, is the model **asking clarifying questions** in return?

**The instructor's recap of all eight:** knowledge and reasoning, coding, mathematics, long context, vision and multimodality, agentic and tool use, safety and alignment, and finally instruction following — "these are the eight capabilities that every frontier lab focuses on, and **all the benchmarks you'll read in the future will target one or the other of these capabilities**." (The detailed document he taught from will be shared — he compressed it into ten minutes because reading it line by line yourself "would be a bit boring.")

---

## 17. Theory before practice — the instructor's bet (35:50–37:52)

He suspects some of you are thinking: "this is the fourth session in this course, and so far we've been studying mostly theory — you're getting a little bored. And is it even important?"

His answer, from experience: whenever he taught complex topics by thoroughly covering the theory in overview mode first, people **really enjoyed the practical part that followed** — because they'd learned to see things from multiple perspectives. Whereas:

> "If I start teaching you on Day One how to create golden datasets or what metrics are, your brain will only absorb as much as I teach you. But now you'll observe for yourself, with these two sessions — when we do things practically, you'll understand whatever you read, and beyond that, you'll be able to ask a little more questions and explore a little more."

Covering a lot of theory up front — compared to other classes, companies, and YouTube channels that teach practical things from day one — is a **conscious choice**: "Now, if you want, abuse me for this, you can. But I think this works. I've seen this in the past with multiple courses — MLP, deep learning — a good amount of time on theory eventually translated into a good practical experience. So you have to trust me on this."

---

## Key takeaways

1. **Why AI engineers need model evals** — four decisions: selecting a model (concrete pointers, not "both are good"), tracking whether a new model actually improves (Opus → Fable), safety (hallucination, jailbreakability), and build-vs-buy (Claude API vs a self-hosted DeepSeek from Hugging Face). Without model evals, "you're basically blind."
2. **Definition:** a systematic process of measuring an underlying model's capabilities, behavior, reliability, and operational characteristics under controlled conditions.
3. **Every model eval is four steps:** decide the capability → devise a test → run under a fixed protocol → score and interpret. There is no single eval for everything — unlike human IQ, LLMs have no one number.
4. **Two kinds of tests:** standardized benchmarks (MMLU, SWE-bench — same test for everyone, openly comparable numbers) and custom evaluation sets (data from your actual task, measuring what *you* specifically care about).
5. **The Zomato verdict:** benchmark-leading Model A ($15/1M tokens) vs mid-table Model B ($0.50/1M) → 94% vs 91% classification, 88% vs 87% urgency, $6 vs <$0.21 per 1,000 emails, 4.1 s vs 0.9 s latency — **Model B wins on value**. Benchmarks alone would have picked A; the custom eval on your own golden dataset picks B.
6. **Eight core capabilities organize nearly every benchmark:** knowledge & reasoning, coding & software engineering, mathematics, long context, vision & multimodality, agentic & tool use, safety & alignment, instruction following.
7. **Why labs care, per capability:** knowledge & reasoning is the "intelligence" signal they compete on; coding is the most economically important (Cursor's $60B valuation); claimed context windows (128K–1M) degrade as chats grow; safety is driven by government pressure and reputational risk; instruction following is underrated and directly drives user satisfaction.
8. **The track's structure:** benchmarking first (how to read benchmark numbers — lectures 8–10), custom model evals second (lecture 11), where the Zomato pattern becomes a hands-on procedure.

## Interview angles

- *"Your team is starting a new LLM application. How do you decide which model to use?"* → You can't say "both are good" in a team meeting — model evals give concrete pointers (required capabilities vs model scores), validated by a custom eval on your own task data before committing.
- *"The model at the top of every leaderboard is 30× more expensive than a mid-table one. Which do you pick?"* → Walk the Zomato case: a 200–500-row golden dataset of real emails, compared on accuracy, urgency, cost, and latency; for a below-frontier task, a 3-point accuracy gap rarely beats a 30× cost and 4.5× latency gap.
- *"What does a model evaluation consist of?"* → The definition, then the four steps — capability, test, fixed protocol, score & interpret — and the benchmark vs custom-eval-set distinction; stress that the fixed protocol (same conditions for every model) is what makes scores comparable.
- *"What are the core capabilities of an LLM, and which benchmarks measure them?"* → The eight capabilities plus the benchmark families: MMLU, GSM8K, SWE-bench/HumanEval, IFEval, Needle in a Haystack, MMMU — and the agentic and safety families covered later in the unit.
- *"A new model just launched and your manager asks whether to switch. What do you do?"* → Model evaluations on your golden dataset — the only way to know "for a fact" that the new model beats the current one on *your* application, with numbers to justify the decision.

## Cross-links

- **Previous:** [06 — Offline vs Online Evals](06-offline-vs-online-evals.md) — Unit 1's closer; this lecture opens Unit 2.
- **Next:** [08 — What is LLM Benchmarking: Saturation vs Contamination](08-benchmarking-saturation-contamination.md) — where the benchmark deep-dive announced here begins; [09 — LLM Benchmarks Evolution](09-llm-benchmarks-evolution.md) continues it.
- **The capabilities' first appearance:** [02 — Model vs Application Evals](02-model-vs-application-evals.md) introduced the 8 capability areas and the first benchmark names this course used.
- **Where the case study becomes practice:** [11 — Selecting the Right LLM](11-model-selection-custom-evals.md) operationalizes the Zomato Model A/B pattern as custom model evals.
- **Deeper on the agentic capability:** [Section 105 note 3 — Agent Benchmarks & the integrity crisis](../03-agent-benchmarks.md) — the harness-noise and reward-hacking evidence behind "the protocol is part of the measurement."
- **Course hub:** [README.md](README.md) — the Unit 2 map (lectures 7–11).

<!-- nav-footer -->
---

**Navigate:** [← 06. Offline vs Online Evals](06-offline-vs-online-evals.md) · [Course hub](README.md) · [08. Benchmarking Saturation Contamination →](08-benchmarking-saturation-contamination.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
