# 14 — Evaluating the Generator & Full Pipeline: The RAG Triad

> **Lecture 14 of 19** · Unit 3: RAG Evaluation · 1:21:29
> Evaluating RAG: Testing the Generator & Full Pipeline with the RAG Triad (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/14-rag-triad-generator-pipeline.md)

---

## What this lecture covers

Lecture 13 completed the component level, retriever half — the RAG Eval Project now has a working, evaluated retriever (contextual recall and contextual precision). This session finishes the component level and then moves up a level, completing **two tasks in one sitting**:

| # | Task | Level | Outcome |
|---|---|---|---|
| 1 | Build and evaluate the **generator** | Component | **Faithfulness** and **answer relevance**, a golden dataset of golden contexts, DeepEval run, and a prompt-improvement loop (91/73 → 96/92) |
| 2 | Build and evaluate the **full RAG pipeline** | Pipeline | The **RAG Triad** — faithfulness + answer relevance + **contextual relevancy** — plus the "curious case" of a retriever that scores 99/89 in isolation yet 42 on contextual relevancy |

If you keep one mental model from this lecture: **the same metric means something different at pipeline level, because the context stops coming from your golden dataset and starts coming from the retriever.**

---

## 1. Where we are: two jobs on today's agenda (00:00–03:26)

Two classes ago the course started RAG evaluation with a detailed plan; the current work item is the **RAG eval suite** — a set of evaluations run together to evaluate the whole application — being assembled at **three levels** (component, pipeline, application). Last session the component level began — RAG has only two components, **retriever** and **generator** — and the retriever half finished, with two metrics tracked: **recall and precision**. Today: **evaluate the generator, then the complete RAG pipeline** — both in this one session.

The operating rule is restated: *not* build-the-whole-application-then-test — component by component, build it, test it, move on, exactly as in software development. Retriever built and evaluated; today the generator.

Mechanically the generator is very simple. The retriever, on receiving a query, embeds it, searches the vector database, and fetches five or ten relevant docs; those docs plus the question go to the generator, whose job is to answer from them:

```
generator(question, relevant_documents) → answer
```

A function with **two inputs** (question, relevant documents) and **one output** (the answer). It basically uses an LLM — that's it.

---

## 2. Building the generator: `generator.py` (03:26–07:40)

The instructor won't write code from scratch (it takes time); he uses the code already pushed to the same GitHub repo shown last session — **new files have been pushed today**. In `src/` there is now a `generator.py` — "a very simple, sweet little piece of code," studied quickly:

- **Imports + `load_dotenv`** — the OpenAI API key is needed.
- **The LLM** — **GPT-4o-mini** (cheap), with **temperature set to 0**. Side remark: "most of the time, at evaluation time we set temperature zero" — though this here is the RAG-*building* process, not the eval. Either way, deterministic output is the default.
- **The generator's system prompt**:

> You are a helpful teaching assistant for a course on LLM evaluations. Answer the student's question only from the context provided below.
> Rules: **Use only information present in the context — do not add outside knowledge** (RAG chatbots answer from context, not from their training knowledge, so this is written explicitly). **If the context does not contain enough information to answer: "I don't have enough information in the course material to answer that"** — say it straight, *don't hallucinate*. **Keep the answer clear and concise.**

- **A simple LangChain chain** — the prompt (which receives the context from the retriever and the question from the user) goes to the LLM, and the response goes through a **StrOutputParser** to extract a plain string.
- **A `generate` function** — two inputs (query, context), returns the answer the generator generates. Below it, test code — "you can ignore it."

He copies the file into `src/generator.py` in the project and saves.

**The smoke test (06:21).** A **dummy context created by hand** — deliberately *not* from the retriever — and a self-made question: *"What is online eval?"* Both go to the `generate` function; the LLM should answer with their help. Running it works — the answer comes back: *"Online eval means evaluating your system on live production traffic after deployment. It works without an answer key, unlike offline eval…"* — clearly produced from the given context, which shows **the code is working. "We haven't proven anything more than that."** The generator exists; whether it works *well* is exactly what evaluation will tell.

---

## 3. How a generator fails, part 1: the unfaithful response (07:40–11:35)

Before writing evaluation code, the first-principles question: **whenever you evaluate any system, the way to think is — where and how can this system fail? Find its failure modes.** The generator has **two very major** ones.

**Failure mode 1 — the unfaithful response.** You gave the generator a question and some context and said: read this context, answer this question from it. But the generator read the context **and also added some information from its own side**. That is an unfaithful response.

The instructor's worked example:

| Item | Content |
|---|---|
| **Question** | "Does the CampusX AI engineering program include live classes?" |
| **Context** | "The AI engineering program includes recorded lessons, coding assignments, projects and weekly doubt solving sessions." — nothing here says live sessions exist or not |
| **Generated answer** | "**Yes. The program includes two live classes every week** along with weekly doubt solving sessions." |

Is that answer faithful to the context? **Clearly not.** The LLM is hallucinating — it created the response from its own end when it couldn't find the answer in the context. This is the **hallucinated / unfaithful response**, and "this is very, very dangerous" — if it lives inside your RAG application it can create massive problems. The class has seen it before: the **Air Canada case study** from the start of the course, where the chatbot said "book the ticket, we'll reimburse you later" — **that was a generator problem.** The generator failed there: it ignored the context, created information on its own, and handed it to the user. This is the situation you must avoid, and the metric that tests it is **faithfulness** — simply, *how faithful your generated answer is toward your context.*

One important subtlety before moving on: sometimes the retrieved context itself will be **completely wrong**. A *correct* generator will still build the answer from that wrong context — even if the answer is completely wrong. So remember: **being faithful does not mean being correct.** Faithful means only: whatever context arrived, right or wrong, I will create the answer entirely from it — not one bit of information from my side. **That is the promise of faithfulness.**

> 💡 **Expert commentary.** The naming across the ecosystem: what TruLens calls **groundedness**, RAGAS and DeepEval call **faithfulness** — same metric, claims-from-answer verified against context. The parent note's warning applies verbatim here: *groundedness is not factual truth* — an answer can faithfully repeat a stale or wrong document, which is why factual **correctness** remains a separate, fourth metric (this lecture defers it, and lecture 15 builds it with G-Eval). The Air Canada ruling is the canonical demonstration that courts treat "the AI said it" as the company saying it — Moffatt v. Air Canada, the same case lecture 01 opened with.

---

## 4. How a generator fails, part 2: the irrelevant answer (11:35–15:15)

**Failure mode 2.** Same question — "Does the CampusX AI engineering program include live classes?" — but this time the generated answer is: *"The program includes coding assignments, projects, recorded lessons and weekly doubt solving sessions."*

Two questions, asked in order: **is this answer faithful to the context?** Yes — fully faithful; it was prepared from exactly what the context contained, almost word for word the same. **Is this answer relevant to the question — is it answering what the user asked?** **No.**

That is the second failure mode: the generator grips the context and generates from it, but the answer simply **is not relevant to answering the question** — and in this case too, the user didn't get their answer.

The *ideal* answer here would have been: *"The provided context does not confirm that the program includes live classes. It only mentions recorded lessons, coding assignments, projects and weekly doubt solving sessions."* — at least **relevant** to the question (it addresses live classes), **and** faithful (it creates no information of its own).

So the second metric is **answer relevance**. There are more generator-testable metrics — **citation accuracy, completeness, correctness** — but those will be tested at the **application level**, not now. Today's goal is exactly two quantities:

| Metric | Question it answers |
|---|---|
| **Faithfulness** | Did the answer come out of the context — or is the generator inventing something? |
| **Answer relevance** | Is the generated answer relevant to the question — does it actually answer it? |

The lecture has covered *what*; next is *how* these two are calculated, then implementing them in DeepEval and running them to see whether the generator truly works.

---

## 5. The golden dataset for faithfulness: question + golden context (15:15–17:27)

Calculating faithfulness needs a **dataset** (where it comes from is discussed shortly — for now, what it *is*) with two columns: **the question** and **the golden context**. For a question like *"What is RAG Triad?"* (discussed in some session), the corresponding golden context is built by a person who goes through **all the chunks in the vector database**, filters out the chunks where the RAG Triad was discussed, and puts **all of those chunks** into this cell. For the next question — *"What are online evals?"* — the same: find every chunk that discusses online evals and place them all there. Repeat for **10, 15, 50 questions**.

The result is a **golden dataset containing golden contexts** — and note how it differs from lecture 13's retriever golden dataset: there the second column held an *ideal answer*; here it holds the *ideal context* itself.

---

## 6. Calculating faithfulness: claims + LLM-as-a-judge (17:27–21:32)

The process, step by step:

1. **First, the LLM-as-a-judge is NOT in the picture.** Take the first question and its golden context and send **both to the generator** — it always needs exactly two things, a question and a context. **Critical clarification:** since we are evaluating the generator **in isolation**, the retriever→generator connection is *not* in the picture — the context comes **from the golden dataset, not from the retriever**. "This is a very critical point": the generator is tested independently, with hand-fed input.
2. The generator reads the question and the golden context and **generates an answer**.
3. **Now bring in the LLM-as-a-judge.** Give it the answer; it **breaks the answer into claims** — say five — then takes **each claim** and checks: does this claim exist **anywhere in the golden context**? Claim by claim, all five.

Suppose claim 1 existed in the golden context, claim 2 too, claim 4 too — but claim 3 and claim 5 did not. Faithfulness for this question:

```
faithfulness = (# answer claims found in the golden context) / (total # claims in the answer)
             = 3/5
```

Repeat for every question, then average. **The on-screen graphic example (20:20)** — question: *"What does it mean for a benchmark to get saturated?"* — with the golden context provided **from our dataset, not the retriever**. The answer is generated, then broken by the judge into three claims:

| Claim | Exists in golden context? |
|---|---|
| Claim 1 | ✅ Yes — good |
| Claim 2 | ✅ Yes — good |
| Claim 3 | ❌ No — bad |

**2/3 → the faithfulness score for this particular question is 67** (0.67), averaged over every question in the golden dataset. The instructor's end-to-end recap: golden dataset (questions + golden contexts) → both to the generator → answer generated → broken into claims → each claim checked against the golden context, yes or no → claims found ÷ total claims. **This is how you calculate faithfulness.**

---

## 7. Q&A: any-app evals, the full golden set, and faithfulness vs recall (21:32–23:48)

**Harry's question:** *"Is there any way to evaluate LLM applications in general, other than RAG and agentic-AI-based systems — for example, an application that acts as an interview synthesizer?"* — Yes, obviously. DeepEval has every kind of metric: **multiturn** metrics for chatbots; and for something completely different — not a chatbot, not RAG, not an agent — **custom metrics** (next class). Evaluation isn't limited to RAG and agents: **any LLM-based application can be evaluated — completely possible.**

**"Do we pass a subset of the golden dataset, or a completely new one built just for faithfulness?"** — The faithfulness score is computed over the **whole dataset**: 15 questions → all 15; 50 → all 50.

**"Are we checking precision/recall for the generator?"** — No, no, no — this is completely different. In fact, notice something: **faithfulness is the exact inverse process of recall.** In recall (lecture 13) you generate the *context* and compare it against an *ideal answer*; here you have the *ideal context* and the *generated answer*. Calculating recall and calculating faithfulness are "like two opposite things." But if the parallel triggered in your head, that's a good thing — it means you're recalling and reconnecting the earlier material.

---

## 8. Calculating answer relevance: the reference-free mirror (23:48–27:50)

Answer relevance is a bit easier — "honestly, you don't even need a golden dataset for it." In that sense, **answer relevance is a reference-free eval**: no references are needed. How it works:

1. Question + context go to the generator; it produces an answer.
2. Bring in an LLM-as-a-judge: *here is the question, here is the answer — tell me whether this answer is relevant to this question.* Its method: **break the answer into claims** (claim 1, 2, 3), then compare **each claim with the question** — does this claim help answer the question, or is it irrelevant? If it helps → relevant. Does claim 2 help? Yes. Does claim 3? No.
3. Two of three claims relevant, one irrelevant → **answer relevance = 2/3** for this question — repeated for as many questions as you like.

The precise framing of the dataset's role — "please keep this in mind": **the golden dataset is needed to generate multiple answers, but not as a reference.** Nothing in it is ever consulted as the correct answer. That is the main difference from faithfulness: *we use the dataset, but not as a reference.*

**The worked example (26:35).** Query: *"What does it mean for a benchmark to get saturated?"* Generated answer: *"A benchmark gets saturated when model scores cluster high and close together, so it can no longer tell models apart. Separately, benchmark contamination happens when test data leaks into training data."* Three claims:

| Claim | Content | Verdict |
|---|---|---|
| 1 | Saturation is when all models cluster — their scores become alike | Relevant |
| 2 | The benchmark cannot differentiate between two good models | Relevant |
| 3 | Benchmark contamination is test-data leaking | A bit off-topic → **irrelevant** |

**Score = 2/3 = 67.** And so on for every question. This one is even simpler than faithfulness — no comparisons are made; it's left to a single LLM judgment per claim: "does this claim answer the question, yes or no?" Nothing more.

> 💡 **Expert commentary.** The claim-level version taught here is the conceptually transparent one — but it's worth knowing how the libraries actually implement answer relevancy: both RAGAS's *answer relevancy* and DeepEval's `AnswerRelevancyMetric` **reverse-generate questions from the answer** (the judge spins up the questions this answer would be an answer to) and then measure their **embedding similarity to the original question**. It's a probabilistic cousin of the same idea — an answer is relevant if it "looks like" an answer to that question. Two practical consequences: the metric is fully reference-free (only input + output needed), and it inherits judge/embedding noise, so pin the model and expect a few points of wobble between runs — exactly the variance lecture 13 measured on n = 15.

---

## 9. Q&A: judges, claims, and the correctness boundary (27:50–32:07)

A dense round of student questions:

- **"What if the generator misses some claim points — how is relevancy calculated then?"** — Its relevancy will simply come out poor. *That's the whole point* — we are judging whether the generator is good or bad; if it's missing the good claims, it's bad. Our job is to evaluate, not to rescue.
- **"Is the LLM used for breaking into claims the same LLM used to analyze the answer?"** (Prem) — **Yes, both are the same.** In DeepEval's implementation, the LLM that breaks the answer into claims and the one that then analyzes each claim against the question are one and the same. And it doesn't matter either way: **every LLM API call is independent** — no context is shared between them. The first call is "break down this answer" (one API call); the next takes the question plus one statement and asks "related or not?" (a separate call, nothing carried over). So it makes no sense to use two different LLMs — **use one good LLM.**
- **"Since it's one LLM doing the reasoning, there will be chances of false positives and false negatives?"** — Yes, obviously — every LLM-as-a-judge method carries a real chance the judge errs; the theory classes said it plainly: you cannot completely rely on LLM-as-a-judge. **But run the same judge twice and it makes the same mistakes both times.** The analogy: **if a cricket pitch is bad, it's bad for both teams** — the match's evaluation still happens on a fair, common basis. A faulty judge run twice is at least *consistently* faulty — the bias cancels. Maybe the true faithfulness is 40 but the judge reports 30; next run it sits around 30 again — **two evaluations remain comparable.** The one real mitigation: **a good, powerful judge** — it doesn't cost much (you're testing on samples, not serving tens of millions of users); a little expense buys a strong model in the judge's seat.
- **"Is the final score the average as the number of claims changes?"** (Aman) — Yes — everything so far was for *one* question. With 15 questions in the dataset, every question has its own faithfulness score and its own answer-relevance score; **average them all** → the final faithfulness score and final answer-relevance score *for the generator*.
- **"Is the number of claims decided as a hyperparameter?"** (Rahul) — No. There is no restriction where you decide how many claims to break an answer into; "that is not a hyperparameter, in my opinion."
- **"If for the same query the generator gives statement 2, misses statement 1 (the main answer), and also emits irrelevant statement 3 — what's the score?"** — **50%.** Two claims, one right, one wrong → 50% answer relevance. And here, "we are not talking about correctness" — burn this in:

| Metric | Tells you | Does NOT tell you |
|---|---|---|
| **Faithfulness** | How faithful the answer is to the context | Not correctness |
| **Answer relevance** | How relevant the answer is to answering the question | Not correctness |
| **Correctness** | Whether the answer is actually right | A different metric — next class |

---

## 10. Creating the golden dataset: 862 chunks → Claude, step by step (32:07–35:40)

How was the (question, golden context) dataset built? The instructor's way:

1. **Exported the entire vector database.** A GitHub script — `export_chroma_chunks` — shows how to export **all the chunks** in one go; his **862 chunks** all went into a **JSON file**.
2. **Put the whole JSON on Claude**: *create this dataset for me* — with one important instruction: **step by step** — one question + one golden-context pair at a time, not the whole set at once.
3. Claude analyzed all 862 chunks and generated the first question. He read it and the context it pulled — "I took all these classes, I know what I taught, when, and where" — and **when it looked right, added it to a JSON file**. This way, **15 questions**.

The three ways to do it (echoing lecture 13's four): **manually**; **with an LLM's help but you do the reviewing** (his way); or **DeepEval's Synthesizer** (shown last class — "I haven't been able to use it properly yet, so I'll show it properly in some future class").

The dataset lives in `goldens/faithfulness_dataset.json` — each row a question plus its ideal context, **15 questions**, all manually verified. Copy the file into your project's goldens folder under the same name, paste, save — the golden dataset is ready.

---

## 11. The eval pipeline: `eval_generator.py` (35:40–38:46)

Now a DeepEval script to evaluate the generator on both metrics — `eval_generator.py` on GitHub in `evals/`, "the same kind of file you saw for the retriever." Reading it: load the golden dataset just created (`faithfulness_dataset.json`); set the **judge model** — **GPT-4o-mini** ("you can use a somewhat more powerful model if you like") — and a **threshold** (below it a test case fails, above it passes); then loop over the dataset rows, building one **LLMTestCase** per question — and here is the interesting part, traced input by input:

| LLMTestCase field | Where it comes from |
|---|---|
| `input` | The question **from the golden dataset** |
| `actual_output` | The **answer** — produced by calling the `generate` function **inside the generator**, fed with that question and that context |
| `retrieval_context` | The **golden (ideal) context from the golden dataset** — *not* the retriever |

So both the question and the context go to the generator from the golden dataset; the generator returns the answer; DeepEval judges the answer against the golden context. Two metrics are defined — **Faithfulness** and **Answer Relevancy**, both **built-in DeepEval metrics** — each configured with `threshold`, `model` (the judge), and **`include_reason=True`** so a failed test case explains *why* it failed — then the **`evaluate`** call with all test cases and both metrics. "Exactly the same code we saw for the retriever — exactly the same. There too, two metrics and your evaluate function." (He didn't add all of evaluate's hyperparameters here; you can.)

Copy into `evals/eval_generator.py`, save — "now we are ready to run our first eval on the generator": `python3 -m evals.eval_generator`. DeepEval starts work on the two metrics.

---

## 12. First results: 91 / 73 — and why faithfulness starts high (38:46–42:07)

Reminder mid-run: **at this point the generator is not connected to the retriever** — it's isolation; the context comes from the dataset, not the retriever.

A live-class aside: the run is slow — "somehow in live class one test case always remains, taking more time; normally everything is very fast — saw it last class too; maybe the system is more loaded during live class. It's not a money problem: I recharged my OpenAI wallet with **$10** just today — the time is something else."

**The first aggregate results:**

| Metric | Score | Verdict |
|---|---|---|
| **Faithfulness** | ≈ **91%** | Quite good — anything above 90 is good |
| **Answer relevance** | **73** | Not that great — needs improvement |

Before touching anything, the instructor poses the question: *why did faithfulness come out at 91 directly — no code tweaks, no effort, first run?* The reason is simple: **faithfulness demands almost nothing of the system.** You hand an LLM a question and a context with the instruction "answer this question using this context" — the probability is very high that the answer gets built from that context, because **today's LLMs have quite high instruction-following capability.** Answer relevance is lower because there you're asking a subtler question — is the generated answer relevant *to answering the question*? Scoring well on faithfulness is simply easier than on answer relevance.

---

## 13. Improving the generator: the refined system prompt → 96 / 92 (42:07–48:53)

The retriever had three–four fix levers — chunk size, embedding model, reranker (recalled from last class). **The generator doesn't give you many options** — the two biggest: **switch to a better model** (one with better instruction following), and **the generator's system prompt**, which "matters a lot" — tweak the prompt properly and you get better results.

The instructor did exactly this and shows the **final version** — with an honest disclaimer: "I can't show you all the tweaks; I took multiple runs, and in every run I tried to improve the system prompt." The loop that produced it:

> Run the eval → read **which test cases failed and the judge's stated reasons** → put it all into an LLM (Claude) → gradually refine the prompt → **three to four iterations** → the final prompt with the best results.

Compared to the original three-rule prompt, the rules grew — each addition coming from an individual failed test case:

- *Use only information present in the context; do not add outside knowledge* (already there)
- **Do not strengthen or overstate claims** — if the context says two different things, they are different; do not upgrade them into separate methods with strong wording
- **The context is an informal lecture transcript — synthesize and rephrase what is there**
- **Do not require the question's exact wording to appear** (in the context)

A mechanical aside worth knowing: **DeepEval's `evaluate` runs test cases in parallel** — 15 test cases run in parallel, not sequentially, "that is why evaluation is very fast."

**Second run — with the refined prompt:**

| Run | Change | Faithfulness | Answer relevance |
|---|---|---|---|
| 1 | Baseline (GPT-4o-mini, simple prompt) | 91 | 73 |
| 2 | **Refined system prompt** (3–4 iterations) | **96** | **92** |

"92 — which is a very good score." So the whole improvement story for a generator: you don't have many options — **tweak the system prompt considerably, and/or change to a better model** (a good model improves both quantities automatically).

**The overfitting warning (47:07).** One test case is still failing and could be analyzed further — but be careful: **tune the entire system prompt too closely to the golden dataset and it's kind of overfitting** — great on the test data, yet when new data arrives and context comes from the real retriever, the faithfulness score could crash. That gets tested shortly, once the pipeline exists (he tells you in advance: it will score well there too, because it's a fairly *general* prompt).

**Component level: complete.** Back on the plan-of-action slide: retriever and generator are both built **and** evaluated — four metrics learned across two lectures:

| Component | Metrics |
|---|---|
| Retriever | Recall, precision |
| Generator | Faithfulness, answer relevance |

**These are reproducible results** — on your machine, plus–minus the same numbers; "it won't happen that I'm seeing 96 and you see 76." Some variation always exists because LLMs are probabilistic, but not much. The running narrative: evaluate a RAG application → build an eval suite at three levels → **level one done**, four new metrics implemented in DeepEval.

> 💡 **Expert commentary.** The prompt-improvement loop the instructor just ran — *failures + judge reasons → LLM → refined prompt → re-run* — is metric-driven prompt engineering, the same shape automated frameworks like DSPy formalize as prompt optimization against a scoring function. His overfitting worry is exactly right, and the standard defenses are the ones lecture 13 already flagged: keep a **held-out slice** of goldens you never tune against, and stop refining when gains fall inside the noise band (with n = 15, one flipped case moves an aggregate ~6.7 points — the 91→96 jump is roughly one-to-two cases, so treat it as directional, not exact). Also remember both 96 and 92 are **judge-derived numbers**: they measure "GPT-4o-mini's opinion of your generator," which is why pinning the judge model and prompt matters before any of these numbers gate a release.

---

## 14. Q&A: open-source judges, the five core RAG metrics, G-Eval ahead (48:53–52:25)

**"Can we do the entire evaluation using open-source models, including generation of goldens? I saw rate-limiting issues."** — Yes; rate limits do hit certain models — tweak the settings, or use somewhat smaller models. (The instructor hit the same wall: some models limit **how many parallel LLM calls** you can fire at once — **GPT-4o-mini had no such restriction**, hence his choice; GPT-4.1 or GPT-5.6 work too, with some settings to check in the OpenAI dashboard.) For fully open-source, **Himanshu** (chat) says there *is* a way — "set up a sync config, but a lot of glue code" — which is exactly the advantage of open-source libraries: you can tweak things at your level. A demo comes next class.

**"We do recall and contextual precision for the retriever, and answer relevance and faithfulness for the generator — is that always true for all RAG apps, or does it change per use case?"** — For RAG, it's true. In fact, open DeepEval's documentation and select **RAG**: you will see **exactly five metrics**, of which four are now done:

| # | DeepEval RAG metric | Status |
|---|---|---|
| 1 | Answer relevancy | ✅ This lecture |
| 2 | Faithfulness | ✅ This lecture |
| 3 | Contextual precision | ✅ Lecture 13 |
| 4 | Contextual recall | ✅ Lecture 13 |
| 5 | **Contextual relevancy** | ⬜ Coming in this session |

These five are the **core metrics** — build any RAG application and these four-to-five will be there. Beyond them sit the custom ones — **correctness, styling, completeness**, defined your way — built with a concept called **G-Eval** (visible in the docs), which is next session's topic.

**"When we changed multiple prompts, should we save all prompts and their scores — is there an option?"** — Yes, the option exists: **Confident AI**. DeepEval's output offers: *"run `deepeval view` to analyze and save testing results to Confident AI."*

---

## 15. Experiment tracking: the Confident AI demo (52:25–54:24)

Running that command stores everything just evaluated to **Confident AI — DeepEval's parent company** (DeepEval is their library) — a way to save **every run across all the prompt changes**, i.e. experiment tracking. Live demo: run `deepeval view` → Confident AI opens → log in → it asks for an **API key**, created inside a project there ("test three, create, copy — this is my last try; if it works this time, fine, otherwise we'll look at it again" — same project, new key, done). The whole evaluation just run is now logged in its dashboard:

Test pass: **14 out of 15** — the one failure is visible; click it to inspect everything, every individual row — and **configs are stored with the run**: which system prompt, your chunk size, all the parameters.

"In a way, you're doing experiment tracking — the same thing you did in **MLflow**." Honest framing afterwards: "we gave this a bit too much time, but you can do it. This became a bit of the **LLMOps** part — rather than hardcore evals, it's not part of what we're studying here; it connects to what Himanshu is teaching (though he's using MLflow for it). But Confident AI also has this option."

---

## 16. Building the RAG pipeline: `rag_pipeline.py` (54:24–59:43)

Status check: the retriever is built, the generator is built, and — the good part — **both are verified working**. Now connect them: the moment they're connected, the **RAG pipeline is complete**, and then it gets evaluated at the **pipeline level**. Step 1: build; step 2: evaluate.

Building is very simple — join the two files into a single component. In `src/` on GitHub: `rag_pipeline.py`, "a very simple code": import the retriever — specifically the **re-ranking retriever** (the tuned one from lecture 13's improvement loop) — and the generator; then a class named **`RAGPipeline`** whose flow is simply: **fetch the context** via the retriever, **convert it into a string**, send context + question **to the generator**, **return the answer** (below it, the same code wired as a test). It is **glue code** joining the two: question → retriever → context → context + question → generator → answer → display. Copy into `src/rag_pipeline.py`, paste, save, run once.

**The smoke test (56:59).** Question: **"What is drift and why does it matter after deployment?"** — this time it goes to the **real retriever**, which fetches context, and then question + context go to the **real generator**. "This is like a real thing — this is our application that we just created." Run as a module (imports require it): `python3 -m src.rag_pipeline`. The answer comes back — *"Drift refers to the gradual change in a system's performance and the relevance of its evaluation setup over time, particularly after deployment. It matters because as a business operates…"* (the shared screen renders it too small, "but you can read it") — **produced from the retrieved context**, with the **five retrieved chunks** displayed alongside. The pipeline works fine, no errors.

One clarification "at the very start": **this is not application-level evaluation — it is pipeline-level.** We are evaluating the RAG pipeline.

---

## 17. The RAG Triad — and what changes at pipeline level (59:43–01:03:11)

Go search the internet for *"how do you evaluate a RAG pipeline"* and you will see essentially **one keyword: the RAG Triad.** That *is* RAG-pipeline evaluation.

The setup: the user asked a **question** → it went to the retriever → the retriever generated the **context** → from question + context the **answer** was generated. On the three pairwise combinations of these three artifacts, **three metrics exist**:

| Relationship | Metric | Notes |
|---|---|---|
| Question ↔ Context | **Contextual relevancy** | Discussed last in this lecture |
| Answer ↔ Context | **Faithfulness** | Learned today — is the answer built from the context? |
| Answer ↔ Question | **Answer relevance** | Just discussed — is the answer relevant to the question? |

These three metrics together are called the **RAG Triad**. If you're doing well on all three, your RAG pipeline is working fine — that's the basic funda.

> 💡 **Expert commentary.** The triad's lineage is worth knowing for interviews: the name and the triangle diagram come from **TruLens** (context relevance → groundedness → answer relevance, wired to traces as "feedback functions"); RAGAS ships the parallel suite as faithfulness / answer relevancy / context precision / context recall; DeepEval consolidated the same ideas into its five built-in RAG metrics — which is exactly the five-metric page the instructor shows from the docs. The diagnostic power demonstrated live in this lecture — each weak leg pointing at a different component — is the parent note's "triad as diagnostic triangle": weak contextual relevancy with strong faithfulness means a noisy-but-honest pipeline; strong component metrics with weak contextual relevancy means chunk-*interior* noise, as section 20 discovers.

**The pop quiz:** we already calculated faithfulness and answer relevance at component level. How are the pipeline-level versions different — why calculate them again? **Prem answered it exactly right: this time, the context is different.**

| | Component level (generator eval) | Pipeline level (RAG Triad) |
|---|---|---|
| Context source | **Golden dataset** (ideal context) | **The retriever** (whatever it actually returned) |
| Faithfulness | Answer claims vs golden context | Answer claims vs **retrieved** context — same method, different input |
| Answer relevance | Answer vs question | Answer vs question — **identical** calculation |
| Scores | 96 / 92 | **Will be different numbers** |

That is the main change between pipeline level and component level: the calculation method stays exactly the same — for faithfulness, the only difference is "this time you use the retriever's context instead of the ideal context"; answer relevance is the same anyway (generated answer + question to the judge). But because the input context changed, the scores change too.

---

## 18. Contextual relevancy: the third leg of the triad (01:03:11–01:07:08)

The one metric not yet discussed. In simple words: **how relevant is the context my retriever pulled for me to answering the question.** How it's calculated:

1. Give the retriever a **question** — that's all it ever needs — and it produces the **context** (k = 5 → five contexts).
2. Bring in an LLM-as-a-judge and give it each context in turn: *break this context into claims* — claim 1, claim 2, claim 3 — then the second context, then the third, and so on. Suppose the retrieved contexts decompose into **15 claims total**.
3. Now take **each claim individually, plus the question**, and ask the judge: **is this claim related/relevant to this question? Yes or no.** — fifteen yes/no answers (say claim 1 related, claim 2 related, claim 3 not, claim 4 related…). Suppose **10 of the 15 claims** are actually relevant to answering the question → **contextual relevancy = 10/15** for that question.

Repeat for multiple questions — the golden dataset has 15, so all 15 go to the retriever. And note: **this is also a reference-free evaluation** — the golden dataset is needed only because some questions are needed; no reference is used at all.

The instructor's recap: question → retriever → context → break the context into claims → each claim + question to the LLM, related or not → the ratio is the per-question contextual relevancy → do it for 10–15 questions → average → **the entire RAG pipeline's contextual relevancy**.

It is all LLM-as-a-judge *because* these are reference-free evals — and here you genuinely cannot do any other kind of evaluation: you'd have to bring in an LLM, or bring a human into the judgment (which would be costly). **So the LLM is the solution.**

---

## 19. The pipeline eval: `eval_rag_pipeline.py` and the RAG Triad numbers (01:07:08–01:11:21)

One more eval file on GitHub in `evals/`: `eval_rag_pipeline.py` — "again very simple code, all of it for importing": the **RAG pipeline** just created; dataset **`faithfulness_dataset.json`** (the same one — only the questions are consumed); same judge model (GPT-4o-mini), same threshold; load the golden dataset and build one **LLMTestCase** per row — with the one field that *changed*:

| LLMTestCase field | Source in the pipeline eval |
|---|---|
| `input` | Golden dataset question |
| `actual_output` | What the **RAG pipeline** produced |
| `retrieval_context` | **What the RAG pipeline returns — i.e., what the retriever sent** (last time this field held the golden context) |

Simple: question from the golden dataset; output **from the RAG pipeline**; context **from the RAG pipeline**. All **three metrics** are defined — faithfulness, answer relevancy, contextual relevancy, all three built-in — then the `evaluate` call: "the same format we keep repeating — nothing special." Copy → `evals/eval_rag_pipeline.py` → paste → save → run: `python3 -m evals.eval_rag_pipeline`.

**The output — the summary of the RAG Triad:**

| RAG Triad metric | Score | Verdict |
|---|---|---|
| **Faithfulness** | ≈ **92–93** | "A very good sign" |
| **Answer relevance** | ≈ **86–87** | Good |
| **Contextual relevancy** | **just 42–43** | Not good — "the only problem in this entire evaluation piece" |

One thing clearly proved along the way: **the system prompt written for the generator was written correctly.** Even after swapping the context source — now coming from the retriever, not the golden dataset — the answer-relevance score did not fall much. So the earlier overfitting worry is settled: the prompt generalizes. The one remaining problem is contextual relevancy — "now, that's a bit of a curious case."

---

## 20. The curious case: recall 99, precision 89, contextual relevancy 42 (01:11:21–01:17:56)

First question: if contextual relevancy is low, **who's the main culprit?** Think and answer — the **retriever**: bringing the context is its job. But here's the curious part — the instructor **re-runs last class's `eval_retriever.py`** right then (on recall and precision): "does anyone remember last class? Recall, I remember, was 90-plus." This run:

| Retriever, evaluated independently | Score |
|---|---|
| **Recall** | **99%** |
| **Precision** | **89%** |

So independently the retriever's own metrics are excellent — yet dropped into the pipeline, contextual relevancy is **just 42%**. *"Can someone explain how a retriever can be good and bad at the same time?"* Recall good: of 100 correct contexts needed, it brings 99. Precision good: of 100 fetched, 89 helpful. Contextual relevancy: how relevant is the pulled context to answering the question. And don't precision and contextual relevancy look like **very similar metrics** — of what you brought, how much is useful vs how related your context is to the answer? Yet 89 vs 42. "Now someone tell me — I've laid the answer wide open."

**Rahul got it exactly right: too much noise per chunk.** The resolution:

- k = 5 → five contexts, **C1–C5**. Suppose **four of the five contain relevant chunks** — the information needed to answer the question is available in C1, C2, C3, C4; only C5 misses it. In this situation **precision will obviously be high.**
- **But there is one more situation: noise *inside* every context.** Suppose a given context has five lines and only two of them are useful — the other three lines are about something else. Break it into claims: **five claims, two useful → contextual relevancy for that chunk = 2/5.** In another chunk, of five claims only one is useful — and since that one *is* useful, the whole **chunk still counts as useful at the precision level** — but inside, the chunk is full of noise.
- That is exactly what's happening here: the retrieved chunks, on the whole, contain **one or two sentences that help answer** — and the rest is a lot of noise. **This is what contextual relevancy measures.**

The clean summary of the three metrics' division of labor:

| Question | Metric that owns it |
|---|---|
| Of the correct contexts that exist, how many did we bring? | **Recall** |
| Of the contexts we brought, how many chunks are useful? | **Precision** |
| **Inside a single context, how much is noise?** | **Contextual relevancy** |

Until now, nothing was checking that third question — contextual relevancy is what tells us. "Is the curious case of the retriever settled now?"

> 💡 **Expert commentary.** This chunk-level vs claim-level granularity split is the real precision-vs-contextual-relevancy distinction: **contextual precision judges whole chunks** (helpful or noise), while **contextual relevancy judges claim/sentence-level content** (how much of each chunk is on-topic). RAGAS implements the sibling idea by having the judge *select the relevant sentences* from each retrieved chunk and scoring the fraction kept. Two production angles the lecture's fix (smaller chunks) doesn't mention: noisy context is primarily a **cost and latency** problem — you pay tokens for noise and dilute the generator's attention (the lost-in-the-middle effect from lecture 04) — and the instructor's acceptance argument ("answers are good, so it can be tolerated") is legitimate *precisely because* the triad's other two legs already measure the answer-side consequences of that noise.

---

## 21. Fixing contextual relevancy — and what remains (01:17:56–01:21:29)

So which parameter would you tweak to improve contextual relevancy? **Exactly — chunking.** Reduce the chunk size: smaller chunks → less chance of noise inside each one.

From here it's the audience's homework — "I've taken you to this level; now it's your work." His pragmatic position: if faithfulness, answer relevance, recall and precision are all good, then contextual relevancy being mediocre **doesn't really matter — because at the end of the day, your answers are coming out good.** What difference does it make that one context carries noise? Obviously, reducing noise a bit would nudge the other values up a little too; but since the other four things are working well, a lower contextual relevancy **can be accepted**. You can always go try — "I'm not burning another ₹70–80 for it" — reduce the chunk size, reduce the overlap a bit, experiment with different parameters, and contextual relevancy might rise. **But beware the trade-off: contextual relevancy could go up while the other four go down. That's possible too.**

**Where the eval suite now stands.** This part of the suite is done. What remains:

| Remaining work | Lecture |
|---|---|
| **Application level** — is the answer *correct*? (never checked so far) — is it *complete*? — does its *style* match the CampusX teaching style? | 15 |
| **Safety evals** (toxicity, leakage, scope drift) and **ops evals** | 16–17 |
| **Regression testing**, then **online eval** | 18–19 |

"We're on track." The closing reflection: two important things got done today — the payoff the course promised at its start: *you will understand better than others, and persevere.* Everybody builds RAG applications; "I think you've leveled up a bit — you'll look at a RAG application through a different lens," and in interviews you will likely perform better **because of this scarce knowledge**. A candid sign-off: "Not finding it boring, right? One metric is clearly how many people attend — very few. So it might be boring! But I'm trying to keep it very logical, very narrative-driven, with a logical progression." On YouTube he notices hardly **3,000–5,000 people** watching — it's OK; the topic is niche, not many people are serious about evaluations yet, **"but they will be, within a year."**

---

## Key takeaways

1. **The build-test-build discipline continues**: retriever built and evaluated (lecture 13) → generator built and evaluated (today) → pipeline built and evaluated (today) → application level next. Never build the whole application first and test later.
2. **A generator fails in two major ways**: it produces **unfaithful responses** (adds information beyond the context — the Air Canada failure mode) and **irrelevant answers** (faithful to the context but not answering the question). Hence two metrics: **faithfulness** and **answer relevance**. Citation accuracy, completeness and correctness are deferred to application level.
3. **Faithful ≠ correct**: a correct generator answers *even from a wrong context*; faithfulness only promises the answer is built entirely from the context with nothing invented. Correctness is a separate metric (lecture 15).
4. **Faithfulness is claims-based and reference-based**: golden dataset of (question, **golden context**) → generator answers in isolation → judge decomposes the *generated answer* into claims → faithfulness = claims found in the golden context / total claims (worked: 3/5, and 2/3 = 67 on the benchmark-saturation example) → average over all questions.
5. **Answer relevance is reference-free**: break the generated answer into claims, judge each against the *question* (does it help answer it?) — 2/3 = 67 on the worked example. The golden dataset is needed only to generate answers, never as a reference.
6. **Judge hygiene from the Q&A**: use one good LLM for decomposition and judging (API calls are independent anyway); a faulty judge run twice is consistently faulty — the cricket-pitch argument — so comparisons stay valid; mitigate with a **powerful judge** (cheap at eval scale); the claim count is *not* a hyperparameter.
7. **Golden dataset creation, instructor's way**: export all **862 chunks** from Chroma (`export_chroma_chunks`) → Claude, one (question, golden context) pair at a time → human review (he knows what he taught where) → **15 questions** in `faithfulness_dataset.json`.
8. **DeepEval pattern is unchanged**: LLMTestCase (`input` = golden question, `actual_output` = generator's answer, `retrieval_context` = golden context) + built-in **Faithfulness** and **AnswerRelevancy** metrics (threshold, judge model, `include_reason=True`) + `evaluate` — which runs test cases **in parallel**.
9. **Generator improvement has two levers**: a better model, and the system prompt. The prompt loop (failed-case reasons → Claude → refine, 3–4 iterations) took the scores from **91/73 to 96/92** — with an explicit **overfitting warning** against tuning the prompt too tightly to the golden set. Faithfulness starts high because modern LLMs simply follow the "answer only from this context" instruction well.
10. **The RAG Triad is the pipeline-level eval**: on the three artifacts (question, context, answer), three pairwise metrics — **contextual relevancy** (Q↔C), **faithfulness** (A↔C), **answer relevance** (A↔Q). These plus contextual precision/recall are DeepEval's **five core RAG metrics**; beyond them, custom metrics via **G-Eval** (next lecture).
11. **Pipeline level differs from component level in exactly one way**: the context now comes from the **retriever**, not the golden dataset — same calculations, different (and more honest) numbers: faithfulness ≈ 92–93, answer relevance ≈ 86–87, contextual relevancy ≈ 42–43.
12. **The curious case**: the retriever scores **recall 99 / precision 89** in isolation yet **contextual relevancy 42** in the pipeline, because precision judges whole chunks while contextual relevancy judges the noise *inside* each chunk. Fix: smaller chunks / less overlap — with a trade-off warning — or simply accept it while the other four metrics (and the answers) are good.

## Interview angles

- *"Your RAG answers look wrong. How do you decide whether the generator is to blame?"* → Evaluate the generator **in isolation**: hand it a golden dataset of (question, golden context), score faithfulness and answer relevance. Only a generator that passes deserves to be connected to the retriever — then re-score everything at pipeline level with the RAG Triad.
- *"What's the difference between faithfulness and correctness?"* → Faithfulness = every claim in the answer is supported by the retrieved context; it stays meaningful even when the context itself is wrong. Correctness compares against what is actually true — a separate, reference-based metric.
- *"Walk me through the RAG Triad."* → Question, context, answer; three pairwise metrics — contextual relevancy, faithfulness, answer relevance. All three good → pipeline healthy. Bonus points: name the fifth core pair (contextual precision/recall) and the custom-metric extension (G-Eval).
- *"Your retriever has 99 recall and 89 precision, but contextual relevancy is 42. What's going on?"* → Noise *per chunk*: precision counts a chunk as useful if any of it helps; contextual relevancy decomposes chunks into claims and measures the on-topic fraction. Fix with smaller chunks or tighter overlap — accepting the trade-off against recall.
- *"You improved answer relevance from 73 to 92. How, and what did you watch out for?"* → Two generator levers — better model or better system prompt; I refined the prompt over 3–4 iterations using the judge's failure reasons. Watch-out: prompt-overfitting to the golden set — validate at pipeline level where context comes from the real retriever.
- *"Isn't an LLM judge unreliable?"* → Yes — false positives and negatives exist; but a pinned judge is *consistently* biased (the cricket-pitch argument), so comparisons across runs remain valid. Use the strongest model you can afford at eval scale, pin it, and calibrate against a few human-labeled cases.

## Cross-links

- **Previous:** [13 — Testing RAG Retrievers (Hands-On)](13-testing-rag-retrievers.md) — the retriever half of the component level; the golden-dataset methods, DeepEval pattern, and improvement loop this lecture reuses.
- **Next:** [15 — Mastering G-Eval](15-geval-deterministic-judge.md) — the custom-metric framework for correctness, completeness and style (the application-level metrics deferred all session).
- **Parent note:** [Section 105 note 4 — RAG Evaluation](../04-rag-evaluation.md) — the four-level model behind component/pipeline/application, the triad's diagnostic-pair logic, and the judge-calibration rules that govern all three triad metrics.
- **Foundations:** [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) (the improve-the-system loop this code-along instantiates) · [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) (reference-based vs reference-free and LLM-as-a-Judge — the axis this lecture applies to every metric) · [12 — How to Answer "How Do You Evaluate Your RAG App?"](12-rag-eval-interview-answer.md) (the roadmap these two hands-on lectures execute).
- **Where the suite goes:** [16 — RAG Security Evals](16-rag-security-toxicity-leakage-scope-drift.md) · [17 — RAG Operational Evals](17-rag-operational-evals.md) · [18 — RAG Regression Testing](18-rag-regression-testing.md) — the eval suite's destination · [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md).
- **Course hub:** [README.md](README.md)

<!-- nav-footer -->
---

**Navigate:** [← 13. Testing RAG Retrievers](13-testing-rag-retrievers.md) · [Course hub](README.md) · [15. G-Eval Deterministic Judge →](15-geval-deterministic-judge.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
