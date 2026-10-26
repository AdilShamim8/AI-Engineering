# 05 — Eval Methods: LLM-as-a-Judge, Reference-Based vs Reference-Free

> **Lecture 5 of 19** · Unit 1: Foundations · 53:10
> LLM Eval Methods | LLM-as-a-Judge | Reference Based Evals Vs Reference Free Evals (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/05-eval-methods-reference-based-vs-free.md)

---

## What this lecture covers

Lecture 4 ended with the list of eval pipelines your application needs. This lecture answers the question every one of those pipelines forces: **who — or what — actually executes the evaluation?**

1. **The three evaluation methods** — programmatic (deterministic), human, and model-graded (LLM-graded). Every eval pipeline you will ever create is executed by one of these three: "only these three things happen, nothing else happens beyond this."
2. **One worked example per method** — a RAG **retriever** scored with **recall@k** by a Python program; a chatbot's **helpfulness** scored against a 1–5 rubric by human graders; and a **UPSC mains answer-grading platform** whose LLM judge is calibrated against human experts with **MAE** — the lecture's flagship **LLM-as-a-Judge** case study.
3. **Reference-based vs reference-free evaluation** — the vocabulary for whether your golden dataset contains correct answers in advance, plus a one-question test to classify any pipeline you ever meet.

Along the way: the five distinct ways humans participate in evaluation, why human judgment is at once the most reliable and least scalable instrument in the field, and the mindset shift from application *builder* to *production engineer*.

The mental model to keep: **the method is the pipeline's engine.** The dataset and the criterion may stay the same; whether a program, a person, or an LLM turns outputs into judgments changes everything else — cost, scale, reliability, and how you debug it.

---

## 1. What is an evaluation method? (00:00–03:31)

The lecture opens with a definition worth memorizing:

> An **LLM evaluation method** is **the mechanism you use to decide whether an LLM's output is good or not** — the actual procedure that takes an output and produces a judgment about it.

Why do we create evaluation pipelines at all? To know whether our **components, workflows, and applications** are working correctly. But then — *who makes the evaluation pipeline effective?* **The method.** A pipeline without a method is a dataset with nobody to grade it.

### The three methods

| # | Method | Also called | Who executes the pipeline | Best for |
|---|---|---|---|---|
| 1 | **Programmatic** | Deterministic | A program — code you write | Objectively checkable outputs (accuracy, recall@k, schema checks) |
| 2 | **Human** | — | A person — human judgment | Subtle quality judgments where reliability matters most |
| 3 | **Model-graded** | LLM-graded | An LLM — another model judges | Semantic judgment at scale |

The instructor's simplification: whenever you create any evaluation pipeline, ask **who is executing it** — is some program executing it, some human, or some LLM? "Only these three things happen. Nothing else happens beyond this."

### Recap: which method did the Zomato pipeline use? (02:13)

Recall the running example from lecture 3 — the **Zomato email router**: an email arrives, goes to an LLM, and the LLM classifies it as **billing**, **technical**, or **general**. We first established that we needed to measure **accuracy** — and who calculated that accuracy? **Python code.** So that pipeline's method was **programmatic**.

The plan for today: one worked example of each of the three method types — a new, more relevant programmatic example even though one was already given ("I know I've given an example of programmatic before, but today I'll give another relevant example of it").

> 💡 **Expert commentary.** This lecture is step 4 of lecture 3's ten-step workflow — *define the evaluation method* — expanded into its full design space. It is also exactly how eval tooling is organized in industry: frameworks like **DeepEval**, **RAGAS**, and **promptfoo** expose all three lanes — deterministic assertions and code metrics, LLM-judge metrics, and hooks for human feedback. The word **deterministic** matters: same inputs, same verdict, every time — which is what lets programmatic checks run as unattended CI gates.

---

## 2. Method 1 — Programmatic: evaluating the retriever with recall@k (04:13–08:58)

### The setup

The scenario: we are building a **RAG chatbot for CampusX**, so that whenever any user comes, they can interact with the chatbot and get help — and we no longer need to manually answer through emails. And because we want to build this chatbot *well*, we will create **all kinds of evaluation pipelines** for it — starting, naturally for this course, at the **component level**: the **retriever**.

What does the retriever do? As soon as any question reaches it, it **fetches the most relevant documents from the vector database**. That is its entire job — and that is what we must test.

- **Task:** the retriever works correctly.
- **Target:** a single component — the retriever.

### The success metric: recall@k

The instructor asks the audience first — how can we measure whether a retriever is working correctly? — and then gives the answer: the metric **recall@k**.

> **Recall@k:** out of all the correct items that exist, how many has the system been able to find in its top *K* results?

**The worked example.** Take the question *"What are the prerequisites for the ML course and its duration?"* All CampusX documents have been chunked and stored in the vector store. For this question we already know the correct answer is hidden in **documents 1001 and 1003** — those are the two correct documents. We send the question to the retriever and ask it to bring **k = 5** documents. It returns: **1001, 102, 104, 105, 106**.

| | |
|---|---|
| Correct (relevant) documents | 1001, 1003 — two items |
| Retrieved (top-5) documents | 1001, 102, 104, 105, 106 |
| Found of the correct ones | 1 of 2 |
| **Recall** | **1/2 = 50%** |

The recall here is **50%**. What should it ideally be? **100%.** It cannot be more than 100, and it cannot be less than 0. Generalizing the same arithmetic: two relevant documents, both retrieved → 100%; one retrieved → 50%; none retrieved → 0% — you have brought zero relevant documents.

There are other metrics in this family — **precision** is also a topic, and you can compute **rank** too — but the lecture deliberately keeps it simple: **our success metric is recall@k.**

> 💡 **Expert commentary.** Recall@k has a known blind spot: it is **rank-blind** — a correct document at position 1 and at position k count identically. That is why the retrieval-eval family also includes **precision@k** (how much of what you retrieved was worth retrieving), **MRR** (mean reciprocal rank), and **nDCG@k** (graded, rank-aware satisfaction) — and why the lecture's later "add a ranker" fix is the classic companion to a recall problem: widen the net first, then fix the ordering. Lecture 13 of this course implements exactly this recall@k evaluation hands-on.

---

## 3. Running the retriever eval end-to-end (08:58–12:20)

### Building the golden dataset

We build the dataset: **50–100 questions** that users might ask in the future once the chatbot website goes live — deliberately mixing **all types of cases: edge cases, difficult questions, easy questions, and random questions**. Then we **hired an expert** and told him: take each question, go to our vector database, and find out **in which document the correct answer to this question is hidden**. That expert-produced mapping — question → known-correct documents — is our **golden dataset**.

### The method and the run

The evaluation method is decided: **we will determine recall through programming.** How? Very simple:

1. Take the 50 questions and send them to the retriever — **just the retriever**, not the entire RAG chatbot.
2. k = 5: for each question, collect the five documents the retriever returns.
3. Compare against the golden dataset's known-correct documents and **calculate recall per question (per row)**.

Worked rows from the lecture:

| Question | Correct documents | Retrieved | Recall |
|---|---|---|---|
| Q1 | 1001 | includes 1001 | **100%** — all the information was in one document, and the retriever brought it |
| Q2 | 1001, 1003 | includes 1001, misses 1003 | **50%** |
| … | … | … | computed for every row |

Keep calculating for each question, then **average over the whole dataset** → **recall@k for the entire dataset**. Now you can say *"our retriever is working at X% recall@k"* and set a benchmark:

- **≥ 80%** — the acceptable floor ("our retriever should work at least at 80% recall@k")
- **90%** — even better
- **70%** — the retriever needs improvement

**Side remarks on the metric family.** The lecture also walks through **precision** — of the documents the retriever brought, what percentage were actually relevant: bring five documents, all five relevant → precision **100%**; bring five, only one relevant → **20%**. **F1 score** is the harmonic mean of precision and recall. But "for now, recall@k is sufficient — start with recall@k and add more metrics as you go along."

### The verdict

We write the program, it does all of this work, we evaluate the results — and **our recall comes to 67%.**

---

## 4. Analyze, improve — and who defines "relevant"? (12:20–16:34)

### Analyzing the failures

With recall at 67%, the next move is to **deeply observe the cases — the questions — where recall was very poor**, analyze them, and then improve the model, in this case the retriever. The lecture's fix menu:

| Fix | What you do | The reasoning |
|---|---|---|
| **Better embedding model** | Swap the embedding model | Maybe it isn't capturing the meaning correctly |
| **Query expansion** | Expand the query before retrieval | Instead of sending the exact question the user asked, first expand it through an LLM, then send the *expanded* question to the retriever |
| **Increase k** | k = 5 → k = 10 | Cast a wider net |
| **Add a ranker** | Put a reranker after retrieval | Maybe the right topic was in your top 10 but couldn't make the top 5 — with a ranker, what was at #8 comes to #3, and you see good results automatically |

Then re-run the same golden dataset — the improvement loop from lecture 3.

**Did we need any human help to evaluate the retriever?** No — and this is the instructor's point: *"if a program can do it, why should we bring a human into this process? Humans are very expensive — we have to pay their salaries."*

### The three aspects of relevance (13:28)

Relevance, the lecture clarifies, can have many aspects — and recall@k covers exactly one:

1. **How many of the correct documents were you able to retrieve** from the vector database — this is recall.
2. **How many of the documents you retrieved were not necessary** — precision territory.
3. **Whether the documents that came were ranked correctly** — ranking.

### Who decides what "correct" means?

Who told us that documents 1001 and 1003 are the relevant ones for that question? **The person who created the golden dataset** — "he told us, see brother, in our vector database there is only one document related to this question, which is 1001." Bring both relevant documents → you brought the most relevant information; bring one → half; bring none → zero relevant documents.

Two consequences follow:

- **The quality of your evaluation depends on who created the golden dataset.** If that person made mistakes, your evaluation will also be flawed.
- **Scale caveat:** in real-world scenarios the underlying data may be huge, and manually creating a golden dataset for all of it is not feasible — you can evaluate on a **smaller subset**, or use semi-supervised approaches (a small amount of labeled data plus a large amount of unlabeled data), though the lecture flags these as more advanced topics.

### An important clarification (15:52)

> Any evaluation can be program-based, human-driven, or model-generated. What decides the label is **who implements, runs, and scores the evaluation**. **Creating the golden dataset is a separate task** — and naturally, a human does that regardless of the method.

This answers the question a student raised during the programmatic example ("humans were needed there too") — yes, for the *dataset*; the *method* is about who executes the pipeline. The two must not be conflated.

---

## 5. Method 2 — Human: evaluating chatbot helpfulness (16:34–19:52)

### The setup

Now the CampusX website gets a **general chatbot** — one you can ask any type of question: *When is the next course starting? What is the fee for any course? Will a certificate be given? What is the duration of the course?* It answers based on our documents.

We need to evaluate whether this chatbot is working correctly — and note the scope: we are **not** evaluating the safety and operations part; we are evaluating the **application quality** part, specifically the **helpfulness or utility** of the answer — when a user asked a question, was the answer they received actually helpful?

- **Target:** the **entire application** — not any specific component or workflow.
- **Task:** evaluating its **utility**.

**Utility** is defined as three things at once: the answer you received was **correct**, its **tone/posture** was correct, and the answer itself was **complete**.

### The success criteria: a rubric

Here, defining a success benchmark is **very complex** — you are evaluating a complete application's helpfulness, and there is **no single correct metric; it varies by business**. So CampusX defines a **rubric**: a helpfulness criterion scored **from one to five**.

| Score | Meaning |
|---|---|
| **5** | The answer is correct, precise, complete, and in exactly the right posture/tone |
| **3** | Partially helpful |
| **1** | Completely unhelpful — "started saying something else" |

### The dataset

Again 50–100 questions (~50 samples given), with **coverage** in mind — general questions, difficult questions, edge cases, random questions — "a reflection of whatever our user might ask." But notice the crucial difference from the retriever dataset: **this dataset has only one column — the question**:

> "How long is the ML course?" · "Is the ML course right for me if I already know Python?" · "What's the fee for the DL course?" · "Do I get a refund if I drop out midway?" · "Can I pay the fee in installments?"

No expected answers anywhere in the data. Remember this — it decides this pipeline's classification at the end of the lecture.

---

## 6. Running the human eval — and debugging the rubric with graders (20:24–23:56)

### Can code do this?

The instructor poses the question directly: can you write a program that automatically tells you *"your chatbot is 70% helpful"* or *"90% helpful"*? No — the matter is too subtle. **Human judgment is needed.** The evaluation method is **human**.

### The pipeline

1. Take one question at a time and send it to the chatbot.
2. The chatbot generates an answer.
3. Seat one of your workers and give them instructions: *"Look at this question. Look at this answer. Give a grade"* — a number according to the grading rules (the rubric).
4. Take the next question, send it, get the answer, ask for the grade — for the entire dataset.
5. At the end, **calculate the average** → your **helpfulness score**. "It came because of your human."

### Why sit more than one grader? (22:31)

Normally you seat **multiple people** — say **Grader A** and **Grader B**. What's the advantage? The instructor's reasoning:

- If the two graders' grades **don't match on many questions** — one says *"I will give it two marks,"* the other says *"four marks"* — and this disagreement repeats, what can you conclude?
- **Your rubric has some ambiguity.** There is a problem in the criteria you set — the instruction is unclear, and *both* graders are getting confused.
- If they **start to agree a lot**, the instruction is quite clear.

> That is why multiple graders are seated — **to perfect the rubric.** Grader disagreement is treated as a *rubric bug*, not a people problem.

(For the rest of the example, assume a single person is doing all the grading — the multi-grader point is what needed covering.)

> 💡 **Expert commentary.** What the instructor just described is **inter-annotator agreement** — percent agreement or **Cohen's kappa** between graders — a standard measurement in its own right. Production teams annotate a sample with multiple humans precisely to detect ambiguous specs, and iterate the rubric until agreement rises. Keep the pattern in mind: it returns verbatim when the grader is an LLM — **judge calibration** (measuring judge-vs-human agreement, then fixing the prompt/rubric) is the same discipline with a machine in the grader's seat. The parent note on [LLM-as-a-Judge](../02-llm-as-a-judge.md) covers the full protocol.

---

## 7. The five ways humans evaluate (23:56–27:43)

A clarification the instructor wants on record: **in LLM evals, humans don't evaluate just one way — they evaluate in multiple ways.** The direct-grading flow above is the simplest and the most common, but there are **five types** of human evaluation in total:

| # | Type | What it looks like |
|---|---|---|
| 1 | **Direct grading and rating** | The flow just shown: look at the chatbot's answer to a question and give a score per the rubric — the most common human evaluation |
| 2 | **Red teaming** | A group of people **intentionally attacks** an LLM-based system to find where it breaks. Before big LLM launches, a red-teaming team tries to break the system; wherever it breaks, that data is extracted, sent back to the development team, and fixed |
| 3 | **A/B testing** | Two versions of your chatbot in production; you tell users to rate their experience; the better-rated version is selected and deployed to the entire region — **your users are evaluating your application in production** |
| 4 | **Creating golden datasets (and rubrics)** | "If I go and say the answer to this specific question is hidden in this document, then I'm also doing a type of evaluation." (A student raised exactly this during the programmatic example — labeling is evaluation work too) |
| 5 | **Human in the loop** | Complex cases where you cannot rely solely on programmatic or LLM-based evaluation: a threshold is crossed, a **gray area** is created, and you transfer the responsibility of judgment to a human, who answers by their own judgment |

---

## 8. The human trade-off — and the opening for a third method (27:43–30:26)

**The advantage of human evaluation:** judgment is **reliable**. If you consider someone competent and employ them, you trust their judgment — a human brain can understand the subject much more easily than a machine. Compared to any program or LLM, the reliability is much higher, and **more trust is placed in the system**.

**The disadvantage:** **cost** — the biggest negative aspect. You have to spend money to hire humans. And therefore, if your application works at a very large scale — **millions of people use it** — you probably cannot use humans for evaluation at all. It would be extremely expensive.

That leaves a dilemma with no good options:

- Some targets are **too vague for programmatic checks** — "is this chatbot helpful?" cannot be scored by code.
- But those same targets are **too expensive for humans** at scale.

**What sits between the two — with the qualities of both program and human?** The answer is the **LLM**: the third category, **model-graded / LLM-graded** evaluation — which the instructor calls *"the most effective category, if you use it in the right way."* This is why **most LLM evaluation pipelines are basically built on top of LLMs**, and it introduces the technique you will study throughout the rest of this course:

> **LLM-as-a-Judge** — you use the LLM like a judge to evaluate something.

---

## 9. Method 3 — LLM-graded: the UPSC case study (31:01–34:18)

The lecture's flagship example — "a lot of effort has gone into creating this" — is built on India's toughest exam.

### The setup

You run a website/YouTube channel that helps with **UPSC preparation** — UPSC is "India's most difficult exam," and cracking it makes you an **IAS officer**. The exam pattern has three stages (the instructor checks the pattern with the audience as he goes):

1. **Prelims** — MCQ-based
2. **Mains** — subjective; you write subjective answers
3. **Interview** — and after that, selection

Your website, **CampusX UPSC**, prepares students for both prelims and mains. The business insight: you can conduct **automated tests**. For prelims this is trivial — MCQ grading is easy, "anyone can easily manage it." For **mains it is difficult**: the answers are subjective, and evaluating them requires **subject matter experts or specialists**.

### The economics problem

Millions of students come to the YouTube channel — the test can be taken by millions, so this is a big earning opportunity. Suppose even **10,000 students** sit your mock mains test: you must evaluate the subjective copies of these 10,000 students. Now think about how many experts you would need — and these experts have to be **paid according to the evaluation of each copy**. Your profit decreases.

### The platform

So a platform is built (in the story: a company pitches it — "so we have to build this platform. I mean, we have already built it. Now we need to evaluate it; that's our job"): send it **as many students as you want**; an **LLM-based system evaluates the copies of lakhs of students according to your specified rubric**, and you pay a small amount for it. Commercially, this works.

The engineering problem — *our* problem in this course: **verify that this platform is working correctly**, i.e., that it evaluates copies the way humans would. That verification cannot be done by humans at large scale — so it must be done through LLMs. The method of this verification pipeline is **model-graded**.

---

## 10. Success metric and the rubric (34:18–37:35)

### The task

- **Goal/task:** verify that the application we've built **evaluates the copies correctly — efficiently, like humans**.

### The success metric (audience discussion)

The instructor throws the question open — and deliberately asks something ambiguous that can have multiple correct answers ("I'm actually asking a somewhat vague question; it can have multiple answers"). One student, Harry, suggests a **similarity score** — and the instructor pushes back with the right question: *similar to what?*

The lecture's chosen success metric:

> The platform is successful if it can **evaluate the answer papers of UPSC exactly the way human experts do**. Then we accept the platform is successful — we can deploy it, launch it, and earn money from it.

Note the sequencing the instructor is careful about: this is the **success criterion** — what success looks like — not yet the **metric**, the number that measures it. "What's the correct metric? I'm not telling you right now. I'll tell you the metric a bit later."

### The rubric

First, determine a rubric. Assume the UPSC paper has **three questions** (there could be more):

| # | Question | Marks |
|---|---|---|
| 1 | "Discuss that ethical governance is impossible without administrative accountability" | 15 |
| 2 | "Examine the role of the governor in center-state relations" | 10 |
| 3 | "In India, federalism is more cooperative than competitive" — critically analyze | 15 |

Now bring in an **expert who evaluates papers very well** and ask: *what aspects should I check for, for this answer to count as a good answer?* For question 1, the expert defines **five dimensions**:

1. The answer **mentions ethical governance and accountability**
2. It **explains the connection** between them
3. It **mentions methodology**
4. It **gives examples**
5. It has a **balanced conclusion**

Repeat per question → each question gets its own five-dimension rubric. And the instructor's explicit warning: **"it's not a dataset, friends — it's a rubric that can evaluate a question."** Rubric first; dataset next.

---

## 11. The golden dataset: human-graded answers (39:25–40:41)

Now the dataset is built, and it looks like this:

| Column | Content |
|---|---|
| **Answer ID** | which answer this is |
| **Question** | which question's answer this is |
| **Answer text** | what the student actually wrote — the full written answer, not a summary |
| **Human evaluator's marks** | the expert's score — this is the reference |

Scale: **50–100 rows** — "we only had to evaluate 50 to 100 answers, and just one subject matter expert. So you can understand it wasn't a huge task."

**How the expert grades:** read the answer → check it against the question's rubric → tick which dimensions are covered → assign marks:

- **Answer 1:** covers all five dimensions → **13 out of 15**
- **Answer 2** (another student, same question): partially covers dimension 1, misses dimensions 2–4, has dimension 5 → **4 marks**

This is literally how a human evaluates a UPSC mains paper — and it is the golden dataset against which the platform will be judged.

---

## 12. The judge prompt (40:41–43:41)

### Choosing the method — by elimination

- **Programmatic?** Is there any way Python code can evaluate these written answers and compare against human evaluation? **No — not possible.**
- **Human?** Defeats the entire business case — experts are expensive.
- **LLM it is.** The evaluation method is set: **model-graded**.

### Running the evaluation = instructing the judge

"Running the evaluation" here means bringing an LLM into the process and giving it instructions. The judge prompt is assembled from the pieces already built — question from the question paper, marks from the paper, rubric from the rubric store — plus the student's answer:

| Prompt ingredient | Content |
|---|---|
| **Role** | "You are grading the answer of UPSC mains according to an evaluation rubric" |
| **The question** | taken from the question paper |
| **The marks** | what the question is worth (15, 10, …) |
| **The rubric** | the expert-defined dimensions for that specific question |
| **The answer** | the test-taker's answer — what the user has written |

Then the instructions that do the real work:

> For each dimension, decide whether the answer has properly addressed it, and then give a score. **Do not give points for extra talk, keyword stuffing, or unsupported claims. Reward constructive, relevant examples, and balanced reasoning.**

And the output contract: the LLM must report **which dimensions it covered**, **the score it is giving**, and **a justification — the reason why it is giving that score**.

Every student answer goes through this judge, and for each (question, answer) pair you get the LLM's score — across all the answers.

---

## 13. Grading the grader: MAE against human scores (43:41–47:12)

### The two columns

Now, side by side, you have — for the **same answers**, graded against the **same rubric** (the human saw the same rubric as the LLM; both give scores in their own way):

| Answer | Human expert's score | LLM judge's score |
|---|---|---|
| A1 | 13 | 12 |
| A2 | 4 | 8 |
| A3 | 8 | 8 |
| … | … | … |

**The success criterion is hidden between these two columns:** if they are very similar, it means the LLM is evaluating the answers the way humans do — the system is working correctly, *at least for these 50 questions and answers*.

### The metric: MAE

Can you give me a metric? (You've studied so much machine learning — say something.) A student, Himanshu, gives the perfect answer: **MAE — Mean Absolute Error.**

- Take the differences: 13−12, 4−8, 8−8, … for all 50 answers (as absolute differences).
- Divide by 50.
- Suppose the result is **2.3**.

What does 2.3 mean? **On average, the LLM deviates ±2.3 marks from humans when evaluating the answers.** The goal now writes itself: **drive this number down toward zero.** MAE = 0 means your LLM evaluates the answers exactly like humans — the success criterion, expressed as a number.

### The improvement loop

Your whole job becomes minimizing that MAE, and the levers are the ones the lecture lists:

- **Bring in a better LLM**
- **Change the system prompt**
- **Change the rubric** (bring changes to the rubric)

…keep doing various types of work inside the loop. Also examine the **individual cases where the LLM and human scores differ significantly**, to understand *why* — those disagreement cases are the debugging surface. Iterate until the evaluation system aligns with human judgment: this is an **evaluation framework where LLM evaluations are compared with human evaluations** — the difference is the error, the error is the metric, and the metric is what you minimize.

The instructor's summary: a mechanism has been introduced through which you can define how to build a system that evaluates UPSC answers **exactly the way a human would** — *that* is how **LLM-as-a-Judge** works. (And his aside: "A lot of effort has gone into creating this example, trust me. The examples that were coming to my mind earlier were very boring — after a lot of searching, I came to the conclusion that this might be interesting.")

> 💡 **Expert commentary.** This case study independently reconstructs how the field validated LLM-as-a-Judge in the first place. The technique was formalized in *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* (Zheng et al., NeurIPS 2023): GPT-4 as judge agreed with human preferences at **over 80% — roughly the level at which humans agree with each other** — the result that licensed model-graded evaluation for open-ended tasks. The same paper documented the judge's biases at birth: **position bias** (prefers the first-presented answer), **verbosity bias** (rewards length), and **self-enhancement bias** (favors its own model family) — so an uncalibrated judge score is a number, not a measurement. The instructor's "do not give points for keyword stuffing" instruction is exactly the anti-gaming guardrail production judge prompts carry, and his MAE-against-humans loop *is* judge calibration: fix a human-labeled set, measure agreement, fix the top disagreement causes, re-measure. The [LLM-as-a-Judge note](../02-llm-as-a-judge.md) has the full protocol and citations.

---

## 14. The mindset shift: from builder to production engineer (47:48–48:24)

A short, deliberate pause before the final topic:

> "So far, you've just been happy creating LLM-based applications. Are you now feeling a slight change in mindset? Now you're thinking like a **production engineer**, who first ensures that our application will actually work correctly — and *then* deploys it."

And the line worth reading twice:

> **Building the LLM-based application is the easy part. The difficult part is to ensure that it will work every time, and in all places.**

---

## 15. Reference-based vs reference-free evaluation (48:24–53:10)

The final topic is vocabulary — "sometimes you are asked to know this, so we are discussing it" — two terms you will read online: **reference-based** and **reference-free** evaluation. You have already seen both; the lecture only names them.

### The definitions

> **Reference-based evaluation:** for each test case, a correct answer — or what should be in a correct answer — is **given as a reference in advance**. You compare the output with the reference and give it a grade.

> **Reference-free evaluation:** you have **no pre-defined correct answer**. You judge the output's quality **directly, on its own terms, against a criteria or rubric**.

### Classify today's three pipelines

Quick quiz — of the three examples in this lecture (retriever / chatbot helpfulness / UPSC), which are reference-based? In which did we already know the correct answer?

- **UPSC platform — reference-based.** Did we know the answers in advance in its golden dataset? Yes: the human evaluator's marks are the correct answer. We *want* to evaluate like a human, so **who is correct? The human's evaluation** — "for each answer, I am being told the human gave this many marks; the system should try to give those marks too."
- **Retriever eval — reference-based.** For each question, we declared in advance which documents are correct — "the answer is in document 1001"; "in documents 1001 and 1003." The correct concept is defined beforehand.
- **Chatbot helpfulness — reference-free.** The dataset was *simply a list of questions* — that's all we gave the human. The chatbot answers; the human reads the rubric and decides, **based on their own judgment**, what score between one and five the answer deserves. No correct answer is defined anywhere in the data.

| Pipeline | Golden dataset contains | Classification |
|---|---|---|
| Retriever (recall@k, programmatic) | Correct documents per question | **Reference-based** |
| Chatbot helpfulness (human graders) | Questions only — no answers | **Reference-free** |
| UPSC platform (LLM judge) | Human expert's marks per answer | **Reference-based** |

**The subtlety:** the helpfulness eval *did* have a rubric — but **a rubric is a scale standard, not the correct answer for each item**. Having a rubric does not make an evaluation reference-based; having per-case expected outputs does.

### The one-question classifier

> Ask of any pipeline: **does the golden dataset have correct answers in it?**
> — Not provided → **reference-free**.
> — Provided → **reference-based**.

That's the entire difference — and that is why the instructor deliberately picked the human example as one *without* references.

> 💡 **Expert commentary.** The industry metric landscape splits along exactly this line. **Reference-based** metrics range from exact match, through classic text-overlap scores (BLEU, ROUGE), to **BERTScore** and plain **cosine similarity** between embeddings of the output and the reference. Two caveats before reaching for the embedding-based ones: cosine similarity is **embedding-model sensitive** — swap the embedding model and your scores (and system rankings) move — and it rewards **topical overlap, not correctness**: a confident wrong answer that borrows the reference's vocabulary can outscore a terse correct one. **Reference-free** metrics are dominated by LLM-as-a-Judge with a rubric — **G-Eval** (lecture 15 of this course) is the disciplined version, and RAGAS's RAG metrics (faithfulness, answer relevancy) are built reference-free so they can run where nobody has written gold answers. Rule of thumb: use references when you can afford them — they make judgments cheap and grounded; go reference-free where you can't.

### What's next (52:46)

One very important topic is still left: **offline versus online evaluation**. What we've been reading so far can be called a kind of **offline evaluation**; when the system goes into production, evaluation continues — which we call **online evaluation**. That is the next lecture.

---

## Key takeaways

1. **An LLM evaluation method is the mechanism that decides whether an output is good** — the procedure that turns an output into a judgment. Every pipeline is executed by exactly one of three things: a **program** (programmatic/deterministic), a **human**, or an **LLM** (model-graded/LLM-graded) — nothing else exists beyond this.
2. **Programmatic example:** a retriever evaluated with **recall@k** — of all the correct documents, how many appeared in the top-k — computed by a Python script over a 50–100-question golden dataset (expert-mapped question → correct documents), benchmarked at ≥80%. Worked arithmetic: 2 relevant documents, 1 retrieved → 50%. Fix menu for a weak retriever: better embedding model, query expansion, larger k, a ranker.
3. **The method is who implements, runs, and scores the pipeline — not who builds the dataset.** Golden datasets are (naturally) human-made regardless of method, and eval quality inherits the golden-dataset creator's quality.
4. **Human example:** chatbot helpfulness graded 1–5 against a rubric. Multiple graders exist to **debug the rubric** — repeated disagreement (2 vs 4) means the criteria are ambiguous. Humans evaluate in **five ways**: direct grading/rating, red teaming, A/B testing, golden-dataset (and rubric) creation, and human-in-the-loop.
5. **Human evaluation is the most reliable and least scalable method** — trusted judgment, but salary costs that explode at millions of users. Vague targets can't be programmatic and can't afford humans; the LLM sits in between, with qualities of both — "the most effective category if used in the right way."
6. **LLM-as-a-Judge (the UPSC case):** build a per-question rubric with experts; collect a golden dataset of human-scored answers; have an LLM judge grade every answer with the rubric (role, question, marks, rubric, answer, anti-keyword-stuffing instructions, dimensions + score + justification output); then **calibrate the judge against the human scores with MAE** and iterate — better LLM, better prompt, better rubric — until the deviation approaches zero.
7. **Reference-based vs reference-free:** does the golden dataset contain correct answers per test case? Yes → reference-based (retriever eval, UPSC judge). No → reference-free (rubric-judged helpfulness). A rubric is a scale standard, not a per-item answer.
8. **The mindset:** building the application is the easy part; the production engineer's difficult part is ensuring it works *every time, in all places* — evaluation is how.

## Interview angles

- *"What are the possible evaluation methods for an LLM application?"* → Three, and only three executors: programmatic (deterministic — accuracy on a classifier, recall@k on a retriever), human (rubric grading, red teaming, A/B tests, golden datasets, human-in-the-loop), and model-graded (LLM-as-a-Judge). Anchor each with today's worked example, and note that method ≠ dataset creation.
- *"How would you evaluate whether an LLM judge is any good?"* → Reproduce the UPSC design: a human-scored golden set graded against the same rubric, then MAE (or agreement) between judge and human; iterate prompt/rubric/model on the biggest disagreements. Mention MT-Bench's >80% human-judge agreement and the known judge biases (position, verbosity, self-preference) as context.
- *"What is the difference between reference-based and reference-free evaluation?"* → Reference-based compares output to a pre-defined correct answer per test case (exact match, BERTScore, cosine similarity, recall@k against known documents); reference-free judges quality against criteria/a rubric with no per-case answer (rubric scoring, G-Eval). The classifier question: does the golden dataset contain answers?
- *"Your two human graders disagree on half the items — what do you do?"* → Treat it as a rubric bug: inter-annotator agreement exposes ambiguity in the criteria; fix the rubric and re-grade before trusting the scores. Bonus: this same discipline calibrates LLM judges.
- *"Why not just use humans for everything?"* → Reliability is highest, but cost per judgment makes human evaluation impossible at scale (10,000 essays, millions of users); the industry default is programmatic where objective, LLM-graded where semantic, humans for calibration and gray areas.

## Cross-links

- **Previous:** [04 — Multiple Eval Pipelines](04-multiple-eval-pipelines.md) — whose pipeline inventory this lecture supplies with an execution method (step 4 of the lecture-3 workflow, expanded).
- **Next:** [06 — Offline vs Online Evals](06-offline-vs-online-evals.md) — the timing axis that pairs with today's method axis.
- **Where the course takes these methods hands-on:** [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) (recall@k in code), [14 — The RAG Triad](14-rag-triad-generator-pipeline.md) and [15 — G-Eval](15-geval-deterministic-judge.md) (judge-based metrics), [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md) (A/B testing and monitoring in production).
- **Reference depth:** [LLM-as-a-Judge](../02-llm-as-a-judge.md) — MT-Bench lineage, documented judge biases, and the calibration protocol (this lecture's course-level companion); [Evaluation Fundamentals](../01-evaluation-fundamentals.md) — the eval-target taxonomy and golden-dataset discipline.
- **Course hub:** [README.md](README.md)
