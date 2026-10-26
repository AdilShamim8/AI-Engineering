# 12 — How to Answer "How Do You Evaluate Your RAG App?"

> **Lecture 12 of 19** · Unit 3: RAG Evaluation · 46:20
> How to Answer "How Do You Evaluate Your RAG App?" in GenAI Interviews (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/12-rag-eval-interview-answer.md)

---

## What this lecture covers

Unit 2 closed with custom model evals; this lecture opens **Unit 3 — the application-eval half of the course**, where the playlist spends the rest of its life. The framing is unusual and deliberate: the next four sessions are built backwards from a single **GenAI interview question** — *"How do you evaluate your RAG chatbot?"* — asked, in the instructor's estimate, in **about 8 out of 10 interviews**, and almost never answered well. This session delivers the complete answer as a framework, staged around one running case study:

1. **The three-level eval suite** — component level (retriever: recall, precision; generator: faithfulness, answer relevance, citation accuracy), pipeline level (the **RAG Triad**), application level (quality, safety, operations)
2. **The tooling choice** — **DeepEval** over Ragas
3. **Regression testing** at three maturity levels — manual baseline comparison, MLflow experiment tracking, CI gating with GitHub Actions
4. **Online evaluation** — tracing/observability, drift alerts, and the self-improving loop feeding production failures back into the golden dataset

If you keep one mental model from this lecture: **nobody who has actually shipped a RAG system answers that question with metric names — they answer with a layered framework: eval suite at three levels → regression testing → online evaluation.**

---

## 1. Where we stand — the pivot to application evals (00:00–02:03)

The lecture opens with a recap of the entire playlist — "we've already covered **two major milestones**. So we need to know where we stand in the entire curriculum":

| Milestone | Where | What it established |
|---|---|---|
| **Foundations** | First 3–4 lectures | Why we need LLM evaluations; what LLM evaluation is; **reference-based vs reference-free** eval; **online vs offline** eval |
| **The organizing distinction** | Lecture 2 | LLM evals are of two types — **model eval** and **application eval** — and the course would focus on application eval |
| **Model eval** | Last 2–3 sessions | Itself of two types: **standardized eval (benchmarks)** — the knowledge-capability study across various benchmarks — and **custom model evals** — choosing a model for your own application by creating your own dataset (last lecture) |

And now: "the most important part of this playlist is coming up, which is this **application eval**. And we will start this from today." From today onward: if you have an **LLM-based application**, how do you evaluate it, based on the knowledge gained so far?

---

## 2. Which applications to teach — RAG and agents — and the interview question (02:03–05:46)

LLM-based applications come in different types, and the instructor inventories them before choosing what to teach:

| Application type | Example | Status in this course |
|---|---|---|
| **General chatbot** | A chatbot with no RAG or agent functionality | Not taught — "a kind of easy"; do the easy topics yourself once you've studied the difficult ones |
| **RAG-based chatbot** | The CampusX Doubt Solver (this unit) | **Taught first** |
| **Agents** | Agent-based applications | **Taught second** — "agents are also very important" |
| **Multimodal apps** | An image generator — "work is being done in some other modality besides text" | Not taught — "a bit different" (not difficult); rare in production |
| **Fixed-schema output apps** | The Zomato case study: read an email, classify it as a **support / refund / technical** email — "the output will follow a specific schema" | Not taught — also "a kind of easy" |

The teaching decision is stated honestly: "To be honest, it's not possible for me to teach you all types of applications and their application evals." He chose **two topics**: **RAG** first, "because it's extremely important. In your professional journey, most of the chatbots that you will build will have RAG functionality" — and **agent application evaluation**, because agents are equally important. The rest is left to you ("if you guys study the difficult topics, then you can do the easy topics on your own"), and the multimodal app is "a bit different" rather than difficult — in production "very few companies exist, very few projects are there which are of multimodal nature. In most cases, you will see **RAG and agent design patterns**."

Today's session and the next two-three are all RAG evaluation: "basically we will create a RAG chatbot and evaluate it correctly." After these three-four sessions, you will be able to answer the question this unit is built around:

> **"How do you evaluate your RAG chatbot?"** — "This is a very popular question for GenAI interviews. **In about 8 out of 10 interviews, this is asked.**"

"Most of the time, students cannot give a very satisfactory answer. Many of them don't even know about this because they have never studied evaluation. Those who have studied evaluation also cannot give a well-structured and correct answer." The instructor's guarantee: pay attention to today's session and the next three-four, and "you will be able to give a very beautiful answer to this question and **impress the interviewer. This is my guarantee**." (Section 12 delivers the answer itself.)

---

## 3. The case study: the CampusX Doubt Solver (05:46–09:07)

The plan: "learn RAG evaluation through a **case study**, using what we have learned so far." First, a RAG project to evaluate — and the problem statement is deliberately simple. "Very good problem statements were coming to my mind, where in the process of creating an application you can do various types of work. But I felt that here our goal should be to **learn how to evaluate a simple RAG application well**, rather than creating a very complex RAG application." The result: "a RAG chatbot which is simple, but you will enjoy evaluating it a lot."

**The CampusX Doubt Solver:**

- You are taking this LLM course, which delivers **approximately two lectures per week**, and at the end of each lecture students receive the **recording** and the **transcript** — so a transcript exists for every lecture.
- **Use these transcripts as documents**, feed them into the LLM — and now anyone can ask any question or doubt about the entire playlist.
- It is a RAG chatbot **specifically for this course**: "I am not talking about other courses. Only the LLM course. Because for this course, we have the transcript of every lecture."

He refuses to re-teach RAG mechanics — "I am quite sure that you have read it so many times that you know how RAG works. There is a **retriever**, there is a **generator**, and there is a **vector database**. There is an **embedding model**" — and states the build/eval relationship up front: "First, we will create this chatbot or RAG project, and then we will evaluate it. **Actually, we will keep evaluating it during the process of creating it.**"

---

## 4. The strategy — an eval suite at three levels (09:07–10:25)

Once the chatbot is created, "we are going to create a proper **eval suite**." The instructor reminds you of a lesson from earlier in the course: when you create any LLM-based application, "it doesn't have just one evaluation. **It has multiple evaluations.**" So the doubt solver will be evaluated "from different perspectives at various levels" — "and only after passing all those evaluations will we deploy it, and even after deployment, we will evaluate it with the help of online evaluations." The structure — "first and the most important thing":

| Level | What it tests |
|---|---|
| 1. **Component level** | Each part in isolation — the retriever, the generator |
| 2. **Pipeline level** | The retriever and generator connected — the RAG pipeline |
| 3. **Application / system level** | The whole doubt solver, as users experience it |

"I have taught you before that you can evaluate any LLM-based application at these three levels" — the three-level structure formalized in lecture 4 (where the middle level was called the workflow level).

---

## 5. Component level — build each part, test each part (10:25–15:18)

At the component level, "at the time when you are creating the RAG chatbot, **at that time only you start evaluating the components**." A quick architecture refresher places them: a **retriever** and a **generator**, plus a **vector database** where all your documents are stored in the form of vectors; a query arrives → it is sent to the vector database → the vector database returns **the four most relevant documents** ("basically, this entire task is of the retriever"); the retriever hands **question + relevant context** to the generator, and the generator creates an answer based on those two things. Connecting the two is what makes the pipeline: "you will create the generator and establish a connection between these two. **This pipeline is what you call RAG.**"

The build plan is four steps — build a part, immediately test it:

| Step | Action | Metrics |
|---|---|---|
| 1 | **Create the retriever** (write its code): load the documents → **chunk** them → feed them to an **embedding model** to convert into vectors → fetch the relevant documents for a new query. "We call this entire work the retriever." | — |
| 2 | **Evaluate the retriever — individually.** "Just the retriever. We are not focusing on the entire application." | **Recall** — of all the correct documents that exist, how many was I able to retrieve? · **Precision** — of the documents I retrieved, how many were actually useful? |
| 3 | **Create the generator**: "basically an LLM where you provide a question and relevant context, and in return, the generator gives you an answer." Built **in isolation**. | — |
| 4 | **Evaluate the generator — in isolation** | **Faithfulness** — did the generated answer come from the given context, "or has the model created some wrong information (**hallucination**) on its own"? · **Answer relevance** — is the generated answer relevant to the question? · **Citation accuracy** — are the citations real and correct? |

**What "the retriever works" means** — the instructor narrows it to one sentence: "when a question is given, **can my retriever fetch the correct documents from the vector database?**" Recall and precision test exactly that.

On **citation accuracy**, in the instructor's framing: "You must have seen that when ChatGPT answers after seeing some document, it sometimes refers that it has taken this information from **this line of this document or from this link**. So we call this citation." For the doubt solver it is concrete: it solves the question **and** "will also tell us in which session Sir Nitish had discussed this question," providing the link to that transcript — "so we'll verify the citations in the generator."

**The key design point — isolation (14:37):** "We will evaluate the generator in isolation. This means that at this stage, your generator is **not connected to the retriever**." You manually give the generator some questions and some context — "kind of like a **golden dataset**" — provided independently, not coming from the retriever, because the pipeline doesn't exist yet; that is what makes it component-level evaluation. Phase complete when: "Our retriever is working well in isolation. Our generator is working well in isolation. **Our first phase is complete.**"

> 💡 **Expert commentary.** Evaluating each component in isolation is unit testing transplanted into AI engineering — and it is a controlled experiment: by hand-feeding the generator a fixed question–context golden dataset, you hold the context variable constant, so any failure is attributable to the generator alone. This blame localization is the entire economic argument for component evals: debugging a monolithic RAG failure costs hours; debugging "generator failed on good context" costs minutes. Note also which metric teams skip in practice: **citation accuracy**. It is the one users notice first — a broken or fabricated citation destroys trust even when the answer text is right — and verifying it is mechanical: does the cited chunk exist, and does it contain the cited claim?

---

## 6. Pipeline level — the RAG Triad, and testing as you build (15:18–18:37)

**Step 5 — create the RAG pipeline:** "The simple meaning of creating a RAG pipeline is that we will connect our retriever and generator. It's very simple code. Connected."

**Step 6 — test the pipeline.** The moment the two are wired together, the combination needs its own evaluation — "and here, evaluation is a very popular term. We call this the **RAG Triad**." Why "triad"? Because three artifacts exist in every RAG interaction — the user's **question**, the **context** that came from the vector database (fetched by the retriever), and the **answer** generated through the generator — and there is one metric per pair:

| Pair | Metric | Question it answers |
|---|---|---|
| Question ↔ Context | **Context Relevance** | Is the context that came from the retriever relevant to this specific question? |
| Answer ↔ Context | **Faithfulness** | Did the generated answer come from the context, or did the model create wrong information (hallucination)? |
| Answer ↔ Question | **Answer Relevance** | Is the answer relevant to the question that was asked? |

"We separately test these three metrics for our RAG pipeline. **If these three metrics work correctly, it means your RAG pipeline is working correctly**" — and this level is complete.

### Creating and evaluating go together (16:36)

The instructor pauses to name the methodology, because it is the opposite of what beginners assume:

> "We're not doing that we create the entire RAG chatbot first and then evaluate it. No, it doesn't work that way. **Creating your chatbot and evaluating it — they work together.** It's just like software. In software, you don't create the entire application and then test it. You test at the feature level too. You test at the function level too. Here it's the same."

> 💡 **Expert commentary.** The RAG Triad is the popularized name (via **TruLens**) for the three pairwise checks over question, context, and answer — the same triad in the parent note on RAG evaluation. Its diagnostic power comes from reading the metrics **in pairs**: low context relevance with high faithfulness means the generator is honest but starved (fix retrieval); high context relevance with low faithfulness means the generator ignores good evidence (fix prompting or the model). One limit to keep in mind, stated plainly in the parent note: **groundedness is not factual truth** — an answer can faithfully repeat a stale or wrong document. That residual is exactly what the application level's correctness metric (next section) covers. Lecture 14 implements the triad hands-on.

---

## 7. Application level — quality, safety, operations (18:37–22:17)

"So that means you have tested your components. When the components were put together, you have also tested the pipeline. The pipeline is also now built. Now your application has come up, so now you will also test at the **application level**."

**Step 7 — application-level (quality) testing:** mainly, is the doubt solver working correctly? "Here many more types of metrics come":

| Metric | Question it answers | The instructor's illustration |
|---|---|---|
| **Correctness / accuracy** | Is the answer that came out correct or not? | — |
| **Completeness** | Does the answer completely answer the question? | "Suppose your question has two parts but your answer is only answering one part. The other part has been ignored, so there is no completeness here. **Even though one part's answer is correct, still there is no completeness.**" |
| **Style** | Does the answer read like CampusX? | "We will try to make the explanation style of our CampusX Doubt Solver similar to the teachers of CampusX. We will also evaluate this — and you can do it." |

**Steps 8–9** round out the application level — safety, then operations:

| Step | Family | Check |
|---|---|---|
| 8 | Safety | **Toxicity** — is the response toxic or not? |
| 8 | Safety | **PII leakage** — is the response providing any personally identifiable information? |
| 8 | Safety | **Jailbreak resistance** — "is it possible to jailbreak your CampusX Doubt Solver?" |
| 9 | Ops | **Latency** — how quickly does the application answer? |
| 9 | Ops | **Cost per query** — how much cost is the application incurring per query? |
| 9 | Ops | **Token spend** — how many tokens are you spending? |

### The eval suite — and the golden-dataset question (20:22)

Component + pipeline + application: "we are evaluating our entire application at these three levels. **We call this collectively the eval suite.**"

> "It's like our entire test suite. Whenever we need to test this application — instead of running just one test, we run all these tests together. Then we can understand whether our application is working correctly **from every angle**."

A live question from the chat (Sameer): *are we going to generate a golden dataset?* The answer: "Yes Sameer — there are **many evaluations in this for which you will have to generate a golden dataset. There are some evaluations where you don't need a golden dataset.**" And a note on implementation: in the classes so far, "we ourselves were writing code" — especially the last lecture's custom model eval, where "I myself was writing the code." But not this time:

> "If we were to write this entire code ourselves, it would become a very large project. Instead, what we're going to do is **use a library**."

---

## 8. The tooling choice — DeepEval, not Ragas (22:17–23:56)

The library is **DeepEval**. Touring its documentation, the instructor points out that most of the eval suite's metrics already exist there — in the **RAG** section: answer relevance, faithfulness, contextual precision, contextual recall, contextual relevance ("all of this is already there"); in the **safety** section: toxicity, PII leakage ("all of these topics are already there"). So instead of writing custom code to evaluate the RAG application, the course will use "this fantastic library, which is currently a **state-of-the-art library**. Most large companies use this library for LLM-based evaluation." And "the best thing about this library is that its entire syntax is built on **pytest**, which is the main library for software testing in Python. So if you've ever used pytest to do software testing, this library will feel very familiar to you."

**Why not Ragas?** "We're not using Ragas, because **you can use either**. You can do all of this work with Ragas as well, and you can also do it with DeepEval." He is specifically choosing DeepEval, for two reasons: first, "we've already covered Ragas in our advanced RAG course"; second, "DeepEval is a much more extensive library. Its scope extends to many other things" — agents, multi-turn chatbots, non-LLM applications, image-based applications "and so on" — "and that's why its acceptance is also much higher." Plus a prediction: "There's a very good chance that **within one to two years, this will become the benchmark library for LLM evaluation**" — the standard — "so it's a good strategy that we give more importance to DeepEval." Ragas remains fine — "Ragas is good. Of course, there's no problem with it" — but DeepEval is the more advanced library of the two.

---

## 9. Regression testing — the suite as a version comparator (23:56–29:03)

"Now, a very important discussion. Once you've created your eval suite… comes a very important task which we call **regression testing**."

**Definition:** "Regression testing is essentially a process of **running your eval suite on your application**." What we've done so far is *create* the suite — separate evaluation code for the components, the pipeline, and the application. "Once the entire thing is created, when you run it together on the entire application, we call that regression testing."

**The problem it solves:** "If version one of your software is running, now you've created version two of the same software — then how will you know **objectively** that version two is worse than version one? … How do I test it? The answer you'll get in regression testing."

**The mechanics:** "There's nothing special in regression testing. Basically, you run the entire eval suite you've created **all at once**, and by running it, you get the results. You get a complete report showing **which metric's value has decreased, which metric's value has increased**" — a clear picture of "whether the new version of the software we've created is objectively better than the previous version. And based on that, the decision is made whether we should deploy the new version or not."

**The project layout (26:19)** — "we will create a project folder step by step":

| Location | Contents |
|---|---|
| `src/` | The source code of the RAG chatbot: the retriever file, the generator file, the RAG pipeline file — "maybe we will use **FastAPI** to create an API, maybe we will use **Streamlit** to create the UI" |
| `evals/` | All the evaluation files: `eval_retriever.py` (or `retriever.py`), `eval_generator.py`, a separate file for the RAG pipeline, one for testing the application, one for security, one for operations — "all these files in this eval folder, where we have written all our tests, we call it our **eval suite**" |
| `run_evals.py` | Outside all folders. "As soon as this file is triggered, it will run all these tests one by one on our application and **create a report** for us." |

Reading the report is component-wise: "Your retriever file is telling you whether your new retriever is better than the previous retriever. The generator file is telling you whether the new generator is better than the previous generator. And it will go on like this." The habit: whenever the application is complete, or you make some change to it, run `run_evals.py` → full report → new version vs previous version → deploy or not. (This manual run is "a very basic method," the instructor notes — the next section upgrades it.)

---

## 10. Leveling up — experiment tracking, dashboards, CI gating (29:03–37:53)

A disclaimer first: "the discussion we're about to have now will somewhat fall under the **LLMOps** domain. It will lean more towards the engineering domain, instead of just evaluation. But I want to tell you because it's related."

### Level 2 — experiment tracking (29:03)

"If you have studied MLOps, then you might have heard about **MLflow**, which we use to run multiple experiments in our application. Here too, you can do exactly the same thing." The workflow:

1. Every application configuration has **settings** — "for chunking, how many characters are you using? Overlap — how much? What **temperature** are you using? … some settings related to your **embedding model**." Keep them all in one place.
2. Run the eval suite for the first time → numbers for every metric — "for example, let's say your retriever's **recall came 82, and precision came 68**," and so on — and log configuration + metrics in MLflow: "experiment 1 — these configuration values were; in contrast, we got these metric values."
3. This first run becomes your **baseline**: "when we ran the software for the first time, we got these readings."
4. Improve something — "you increased the chunking size, you reduced the overlap size" — and re-run via the eval file; new settings → new readings → also logged. Compare easily — "visually, you will get a dashboard here, and going to that dashboard, you can compare each metric to see how these metrics have been fluctuating over the **last 10 runs**."

So regression testing gains experiment tracking and dashboarding: "this can be the primary level regression testing, and if you want to make it even better, then adding an experiment tracker and a dashboard tool makes it even better."

### Level 3 — CI gating (32:10)

"Actually, you can make it even better by adding **CI** to it. CI stands for **Continuous Integration**." The setup: take a CI tool — for example **GitHub Actions** — and add conditions: "as soon as you make any change in your code and do a git push… suppose you change the value of chunking size and you push it. Then what happens? Your CI tool will **automatically run this evaluation file. And then it will automatically log the metrics.**" That is how you continuously monitor the application's performance and automate the regression-testing process — "a very good practice in production systems."

**The gating mechanism (33:34):** push → CI re-runs the entire eval suite → new readings → compare against the current baseline → apply a threshold — "you'll set a threshold that **it shouldn't be more than 3 less** than before." If below it: "You will stop your new deployment. You'll say that I cannot deploy this new change because my new change is worse than my current baseline. **So the software has regressed. It has gotten worse.**" If the change improves on the baseline: "you'll allow it to go ahead and deploy now."

> "Essentially with the help of CI, you can also create a **gating mechanism**. You can easily change, improve, and deploy your software — and it will **only deploy when your changes have a positive impact on the current baseline**, otherwise it will be rejected."

This is "how an engineering team is handling the entire thing": the eval suite you built becomes the release gate. (Whether he can demo CI here: "I'm not sure. But probably **Himanshu** will show you this, because in the LLMOps class you will all be taught this. I could have avoided this topic, but I felt that since it's related, I'll go through it once with you all.")

### The three levels of regression testing (35:30)

| Level | Setup | What you do |
|---|---|---|
| **1 — Basic** | Eval suite + `run_evals.py` | Run once → baseline scores; after every change, re-run and **manually compare** the scores obtained |
| **2 — Experiment tracking** | + MLflow (or similar) + dashboard | Every eval-pipeline run automatically logs **configuration settings and metric values**; compare visually over time |
| **3 — CI automation** | + a CI tool (GitHub Actions) | On every push: auto-run the suite, auto-compare to baseline, **auto-deploy if better, auto-reject if worse** |

At level 3, "your entire process is automated. You just make a change, push it, and the CI will automatically run the evaluation pipeline. If the evaluation passes — meaning the metrics are better than the baseline — then it will automatically proceed with deployment. Otherwise, it will reject the deployment." Then deploy, **shift the baseline to the new metrics**, "and you keep doing this continuously."

### Concepts over tools (36:56)

MLflow is not the only option — for experiment tracking "you can use many other types of software": **Confident AI** ("DeepEval company's another software" — also does this work), **Weights & Biases** ("this work is also done there"), and "in this area, there are many companies or players." The instructor's rule:

> "Don't get stuck with the tool. Understand the concept or idea, so that once you understand the concept, **you can learn any tool in one week**."

The goal is not to teach MLflow specifically — "it's not necessary that wherever you get a job, that company is using MLflow. There's no such compulsion. **Even now, no standard tool has been created for LLMs.** Yes, for Machine Learning, MLflow has become the de facto standard. Here, no such standard has been created yet. So focus on the concept."

> 💡 **Expert commentary.** Two production realities to attach to the "not more than 3 points less" threshold. First, **noise**: on a 50-question golden dataset, one flipped question moves a metric by 2 points — a 3-point drop can be statistical weather rather than regression. Mature gates use relative thresholds, repeat runs, or confidence intervals before blocking a release (the same caution lecture 11 applied to 95%-vs-92% accuracy comparisons). Second, **fail-open vs fail-closed**: this lecture's gate blocks deployment on regression — the safe default — but many teams start fail-open (report and warn, don't block) until the suite's false-alarm rate is trusted. Notice, too, that the lecture's two threads meet here: DeepEval's **pytest-native** syntax is precisely why its eval files drop into GitHub Actions so naturally — the CI runner already knows how to execute pytest.

---

## 11. Online evaluation — the loop that never stops (37:53–41:30)

"Once you've done your regression testing and understood that the new version's metrics are better than the baseline — now you'll deploy that software. **But evaluation doesn't stop after deployment.** I had taught you all this." This final phase is **online evaluation**: "once the software is live online, you measure three to four things."

### Captured signals — tracing and observability (38:35)

Every time a student comes to the chatbot and asks a question, capture: **latency** (how long the answer took), **cost** (how much it incurred), and **thumbs up / thumbs down** (the student's feedback). The instructor polls the chat for the tooling, then answers himself: "**LangSmith** is an option. We also have **Langfuse** in our hands. Actually, **Confident AI** also does this work. In the world of LLMs, we call this **tracing or observability**." The implementation: "we will add a bit of **tracing code** to our code. And because we add this tracing code… when the software is live, all the data related to whatever interactions happen, we will capture it — **latency, cost, tokens, thumbs up, thumbs down** — and we'll be able to see it in a dashboard, which is LangSmith's dashboard."

### Computed signals, drift, and the self-improving loop (39:44)

Beyond storing whatever comes in "exactly like that," you also calculate more values — the **online versions of the offline metrics**: "its **online faithfulness**, **relevance of the answer**, or **how accurate it is** — i.e., **the things we tested offline, we also test the same things online**."

Then check for **drift**: "the main meaning of drift is — whether our software's performance is **getting worse over time**." The instructor's concrete picture: "We will have a graph of the **last 24 hours**. There, we will track one metric — for example, reliability or faithfulness. If suddenly the faithfulness graph drops in the **last 8 hours**, then this is a type of drift that we are detecting — and then we send an **alert** and make arrangements to improve it."

Finally, "there will be a **self-improving or automatic improvement loop**. Sometimes there might be a chat with some student where our software behaves incorrectly. If our application behaves incorrectly, then we will **take those specific examples and make them a part of our offline evaluation** — we will include them in our offline dataset, so that our offline datasets or golden datasets **become richer**," and the next version gets evaluated against the failures that actually happened. "And that's why a loop is also added here."

> 💡 **Expert commentary.** This is lecture 6's online-eval machinery attached to a RAG system, and one distinction does most of the work: **captured** signals (latency, cost, tokens, thumbs — essentially free, automatic, on 100% of traffic) vs **computed** signals (online faithfulness, relevance, accuracy — an LLM judge must run, so they cost money per request). Production teams do not compute judge metrics on every request; they **sample** (lecture 6 develops stratified sampling). On drift: in RAG systems the usual culprit is the corpus — documents get added, edited, or go stale, and retrieval quality silently shifts — but user-population shifts and upstream model updates cause it too. The 24-hour faithfulness graph with an alert on a sudden 8-hour drop is the simplest workable version of what observability platforms formalize.

---

## 12. The road ahead — and the model interview answer (41:30–46:20)

**The plan for the next four sessions (41:30):**

| Session | Coverage |
|---|---|
| Next class (lecture 13) | Full **component-level** evaluation: create the retriever → test it; create the generator → test it — "and in that same process, you will use **DeepEval for the first time**" |
| Session 2 (lecture 14) | Create the **RAG pipeline** and run the **RAG Triad** — "that is, three metrics" |
| Session 3 | Full evaluation at the **application level** — "or maybe a bit earlier. I'm actually not sure, because I don't know how this will progress in the future" |
| Session 4 (final) | **Regression testing** and **online evaluation** |

"In the next four sessions, we will practically complete the entire framework that we have created for testing the RAG application." None of it starts today, deliberately: "this entire topic is about **2 hours**, and I want to complete this 2 hours in one go. I don't want that we study for one hour today, then one hour on Saturday. **This breaks the flow.** So I have kept today's class specially for this entire discussion." (As shipped, the plan stretched slightly — the final arc runs lectures 13–19, with G-Eval (15) inserted and the application-level session splitting into security evals (16) and operational evals (17).)

### The model answer (42:13)

"Do you all think that if someone asks you this question now — how do you evaluate your RAG chatbot — will you be able to answer? Think about it once. **It's very simple.**" The scripted exchange:

| The other person says | You say |
|---|---|
| "How do you evaluate your RAG chatbot?" | "First, I create an **evaluation suite**." |
| "What is an evaluation suite?" | "I create it at **three levels**: I test at the **component level** — the retriever and the generator" — and name the metrics. "Then I test at the **pipeline level** — the RAG Triad. Then I test at the **application level** — relevance, completeness — and I also test for **safety and operational metrics**." |
| (then what?) | "Once the entire thing is done, I use these to do **regression testing**. Regression testing can also have three levels — basic, experiment tracking, and CI/CD. **I work at any one level according to my company's requirements.**" |
| (and after that?) | "Once regression testing is done and I get a new baseline, I deploy — and even after deploying, I won't stop. I run **online evaluations**" — and say what you'd run online as well. "And there, whatever errors are caught, I collect them and include them in my offline evaluation." |

The verdict: "When you answer this way in an interview, the other person will clearly understand that **this person knows the subject**. Because there's nothing else to RAG evaluation beyond this. This is the answer to this question."

### What most candidates do (44:03)

The instructor speaks from the other side of the table: "Since I myself have taken interviews, I can tell you. When I ask candidates how to evaluate a RAG chatbot — many don't know the answer, because they have never studied evaluation. Those who have studied evaluation, most of them answer: 'we will do recall check, we will do precision check, we will do answer relevance check.' **Three to four metric names they tell, and they feel that's the answer.**"

> "But trust me, there's a **framework** for this. When you give an answer like a framework, the person in front will respect you — yes, boss, he knows this. He knows this deeply. **He has done this.**"

Doing it practically over the next four sessions "will embed it more deeply in your mind" — and behind the series sits an ambition: "to create a resource such that **anyone in the world who wants to understand RAG evaluation can understand it just by watching these four lectures**. The whole subject is this." The close: "I am ending this lecture with the promise that the next four lectures are going to be very great. So yes, that's all for today."

---

## Key takeaways

1. **The course pivots to application evals**, teaching exactly two application types — **RAG** (now) and **agents** (later) — because those are the design patterns production actually uses; general chatbots are "easy" once you can evaluate RAG, and multimodal projects are rare.
2. **"How do you evaluate your RAG chatbot?" is asked in ~8 out of 10 GenAI interviews** — and the winning answer is a layered framework, not a list of metric names; most candidates recite three-four metrics (recall, precision, answer relevance) "and feel that's the answer."
3. **The case study is deliberately simple**: the CampusX Doubt Solver, a RAG chatbot over this course's lecture transcripts (~2 lectures/week, recording + transcript each) — chosen so the focus stays on *evaluating well*, not on building something complex.
4. **Build and evaluate together**: "creating your chatbot and evaluating it — they work together," exactly like software, where you test at feature level and function level, not only after the whole application exists.
5. **Component level**: build the retriever, immediately test it (**recall, precision**); build the generator, immediately test it **in isolation** on a hand-fed golden dataset (**faithfulness, answer relevance, citation accuracy** — including the "which session, which transcript link" citations).
6. **Pipeline level**: connect the two ("it's very simple code. Connected.") and run the **RAG Triad** — context relevance (question↔context), faithfulness (answer↔context), answer relevance (answer↔question); all three green ⇒ the pipeline works.
7. **Application level**: quality (**correctness, completeness, style**), safety (**toxicity, PII leakage, jailbreak**), operations (**latency, cost per query, token spend**). All three levels together = the **eval suite**; many of its evals need a golden dataset, some don't.
8. **Tooling: DeepEval over Ragas** — pytest-based syntax, state-of-the-art, most large companies use it, broader scope (agents, multi-turn chatbots, non-LLM apps, image-based apps); "within one to two years, this will become the benchmark library for LLM evaluation."
9. **Regression testing** = running the whole suite (`run_evals.py` over `src/` + `evals/`) to compare versions objectively — at three maturity levels: manual baseline comparison → MLflow experiment tracking (baseline: recall 82, precision 68; dashboards; last-10-runs fluctuation) → CI gating (GitHub Actions auto-runs on push, threshold ≈ 3 points, auto-deploy or auto-reject, then re-baseline). **Concepts over tools**: MLflow / Confident AI / Weights & Biases — for LLMs, no de facto standard exists yet.
10. **Online evaluation never stops**: tracing/observability (LangSmith, Langfuse, Confident AI) captures latency, cost, tokens, thumbs up/down; computed signals re-test offline properties online (faithfulness, relevance, accuracy); drift is caught on a 24-hour metric graph (a sudden 8-hour faithfulness drop → alert); and the **self-improving loop** feeds production failures back into the offline golden dataset.

## Interview angles

This is the lecture's whole point, so learn the answer as a **layered script**, not a list. The 60-second version, in order:

1. **"I build an eval suite at three levels."** (Expect the follow-up: *what's an evaluation suite?* — answer with the levels.)
2. **Component level** — retriever (recall, precision) and generator (faithfulness, answer relevance, citation accuracy), each tested **in isolation** on a hand-fed golden dataset.
3. **Pipeline level** — the **RAG Triad**: context relevance, faithfulness, answer relevance.
4. **Application level** — correctness, completeness, style, plus **safety** (toxicity, PII leakage, jailbreak) and **operational** metrics (latency, cost per query, tokens).
5. **The suite doubles as the regression-testing harness** — basic, experiment-tracking, or CI/CD-gated, "according to my company's requirements."
6. **After deployment, online evaluation** — tracing for latency/cost/tokens/feedback, online judge metrics, drift alerts — and failures flow back into the offline golden dataset.

Follow-up angles to be ready for:

- *"Why evaluate components separately if you'll evaluate end-to-end anyway?"* → Blame localization and cost: an isolated generator test on a fixed golden dataset holds the context constant, so a failure points at the generator in minutes instead of a monolithic debug; and the triad's pairwise readings localize problems (honest-but-starved generator vs ignoring-good-evidence generator).
- *"What exactly is the RAG Triad?"* → Question, context, answer; one metric per pair; what each failing pair means for where you fix the system.
- *"Which tools have you used?"* → DeepEval (pytest-native, so eval files drop straight into CI), Ragas as the equivalent alternative, MLflow / Weights & Biases / Confident AI for experiment tracking, LangSmith / Langfuse for observability — then the concept-over-tools point: no de facto LLM-eval standard exists yet, so learn the idea; any tool then takes a week.
- *"How do you prevent regressions when you change chunk size, overlap, or prompts?"* → Baseline from the first suite run (e.g., recall 82, precision 68); re-run the whole suite on every change; threshold-based CI gating (block the deploy if a metric drops more than ~3 points); promote and re-baseline when the change wins.
- *"What do you monitor after launch?"* → Captured signals on all traffic (latency, cost, tokens, thumbs), computed judge metrics by sampling, drift alerts on a rolling metric graph, and the self-improving loop into the golden dataset.
- *"Have you actually done this?"* → The honest differentiator the instructor points at — "he has done this" — which is exactly what the next four hands-on lectures are for.

## Cross-links

- **Previous:** [11 — Selecting the Right LLM: Custom Model Evals](11-model-selection-custom-evals.md) — Unit 2's capstone; this lecture pivots the course to application evals.
- **Next:** [13 — Testing RAG Retrievers (Hands-On)](13-testing-rag-retrievers.md) — steps 1–2 of this framework implemented: build the retriever, test recall/precision, first use of DeepEval.
- **Parent note:** [Section 105 note 4 — RAG Evaluation](../04-rag-evaluation.md) — the four-level model, retrieval-metric definitions (recall@k, nDCG@k), RAG-triad diagnostics, DeepEval/Ragas/TruLens tooling, and the safety level.
- **Foundations:** [04 — Multiple Eval Pipelines](04-multiple-eval-pipelines.md) (where the three levels and the quality/safety/operations split were first established) · [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) (the judging machinery behind every metric named here) · [06 — Offline vs Online Evals](06-offline-vs-online-evals.md) (the online-eval concepts section 11 instantiates).
- **The hands-on arc:** [14 — RAG Triad](14-rag-triad-generator-pipeline.md) · [16 — Security: Toxicity, Leakage & Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) (step 8) · [17 — Operational Evals](17-rag-operational-evals.md) (step 9) · [18 — Regression Testing](18-rag-regression-testing.md) · [19 — Online Eval with LangSmith](19-online-eval-langsmith-monitoring.md) · [Section 105 note 5 — Eval Engineering](../05-eval-engineering.md) (the CI/CD release gate).
- **Interview practice:** [Interview questions bank](../../interview/questions/questions.md) — rehearse this framework answer against the real question list.
- **Course hub:** [README.md](README.md).
