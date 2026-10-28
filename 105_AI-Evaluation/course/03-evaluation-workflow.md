# 03 — How to Evaluate LLM Applications: The Complete Workflow

> **Lecture 3 of 19** · Unit 1: Foundations · ~17:00
> How to Evaluate LLM Applications: The Complete Workflow (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/03-evaluation-workflow.md)

---

## What this lecture covers

Lecture 2 answered *why* and *what*. This lecture answers **how** — again with the standing disclaimer that everything is taught **from the application-eval perspective**, because that's where an AI engineer lives.

The vehicle is a single worked example carried through every step: a small email-routing system for **Zomato**. By the end you have the complete evaluation loop — the same loop you will run for the rest of your career, just with more moving parts.

**The workflow at a glance** (the lecture's own map):

1. Define task & target
2. Define success criteria & metric
3. Build the dataset (the *golden dataset*)
4. Define the evaluation method (automated / human / LLM)
5. Run the model on the dataset
6. Evaluate the results
7. Analyze the results
8. Improve the system → re-run (iterate)
9. Deploy
10. Monitor → feed production failures back into the dataset → repeat forever

---

## 1. The running example: Zomato's email router (01:17–03:21)

We are engineers at a company — say **Zomato**. Because it's a big company with many customers, **lots of emails arrive daily**, and manually replying is hard. The company wants to automate the setup:

> Build a system that **reads each email and classifies its content** — is this a **billing-related** question, a **technical problem**, or a **general query**?

Why classify? **Routing**: billing queries go straight to the billing team, technical queries to the technical team, general queries to customer support. No person is needed to sit and manually read emails and tag teams.

The build itself is deliberately trivial — "you can literally build it in 5–10 minutes":

- an **LLM** sits in the middle,
- given a **prompt**: "You are a customer agent who reads emails and decides where to route them,"
- user email in → routing decision out.

But now the real question: **can we deploy this directly?** No — that's exactly what the whole course is about. We evaluate first.

> 💡 **Expert commentary.** Notice what the instructor did *not* build: no RAG, no agent, no tools. A single-prompt classifier is the smallest possible LLM application — and it already needs an eval suite before it touches production. If a 10-minute app needs evaluation, your multi-component RAG pipeline certainly does.

---

## 2. Step 1 — Define the task & target (03:21–04:29)

What exactly are we evaluating?

- **Target** — the *entire system / whole workflow* we built (not the model in isolation; that was lecture 2's model-eval track).
- **Task** — evaluate whether this system **works correctly**: does it route/classify correctly?

Everything downstream hangs off this definition. If you can't state in one sentence what "working correctly" means for your application, you are not ready to evaluate it.

---

## 3. Step 2 — Define success criteria & metric (04:29–05:09)

For this use case:

- **Success criterion:** correct **classification** (did the email land in the right bucket?)
- **Metric:** **accuracy** — if 100 queries come in and 90 get routed to the right place, the system is **90% accurate**.

That's the whole step — but don't let its simplicity hide the lesson: *criterion* (what does success mean for this product) and *metric* (the number that measures it) are separate decisions. For the email router they collapse into one obvious pair; for a chatbot they won't (lecture 5 is entirely about that harder case).

---

## 4. Step 3 — Build the dataset — the golden dataset (05:09–06:38)

Prepare a dataset where **one side has the message/email content** and the other side has the **manually assigned type**:

| Email content | Type |
|---|---|
| "My card was charged twice" | billing |
| "The app crashes on login" | technical |
| "What are your hours?" | general |

Practical guidance from the lecture:

- The three rows above are just an illustration — **generally create 50–500 rows**.
- **Best practice: use your actual data.** If this is Zomato, pull **past chats/emails** and build the dataset from them.
- **Label manually** — have someone sit and assign the labels ("get someone seated and have them label it").

In the language of LLM evals, this is called the **golden dataset** — the labeled reference your evaluations run against, forever.

> 💡 **Expert commentary.** The 50–500 row guidance matches widespread industry practice: small enough to label by hand in a day or two, large enough to catch more than toy failures. Two additions worth knowing: (1) keep a **held-out slice** you never tune against, so you can detect overfitting-to-the-eval-set; (2) version the dataset like code — when lecture 18 adds production failures back into it, you'll want to know *which* system version was measured against *which* dataset revision.

---

## 5. Step 4 — Define the evaluation method (06:38–08:40)

Now decide **who performs the evaluation** — who compares your system's outputs to the expected labels. Three options:

| Method | How it works | When it fits |
|---|---|---|
| **Automated (code)** | A script compares predicted vs expected | When outputs are objectively checkable |
| **Human** | A person judges the outputs | When judgment is needed, budget exists |
| **LLM** | Another LLM judges the outputs | The middle ground |

**For the email router:** run the dataset through the system — for the first message it says *billing*, second *general*, third *general* — then compare against the labels and compute accuracy. Who computes it?

> "In this case, why would you seat a human? You'd needlessly pay their salary. There's no need to bring in an LLM either. You simply write a Python script that checks the accuracy score."

So the eval method is **automated** — because this is a simple LLM application.

**The contrast case (08:05):** imagine a **chatbot** where the expected answer and the LLM's answer are both *long text*. Now:

- Can code compare two paragraphs and say whether one is right? **No** — you'd have to know whether the *semantic meaning* matches, which code can't easily check.
- A **human** could judge, but humans are **costly** — heavy testing means salary.
- The third option sits in between: use an **LLM** to do the testing.

> 💡 **Expert commentary.** This triangle — code / human / LLM-as-judge — is the single most consequential design decision in any eval pipeline, and it drives both cost and trustworthiness. Lecture 5 develops it fully (reference-based vs reference-free judging, LLM-as-a-Judge); lecture 15 (G-Eval) shows the most disciplined version of the LLM path. The industry rule of thumb the course is leading you toward: automate everything objectively checkable, use LLM judges for semantic properties, and reserve humans for calibrating the judges and adjudicating disagreements.

---

## 6. Steps 5 & 6 — Run the model, evaluate the results (09:16–10:32)

- **Run the model:** send the dataset through your system; it generates its answers (one routing decision per row).
- **Evaluate the results:** your Python code computes the accuracy score.

Worked numbers from the lecture: you sent 100 rows; 80 classified correctly, 20 wrong → **80% accuracy**.

---

## 7. Step 7 — Analyze the results (10:32–11:38)

Now think about **where the mistakes are happening** — what's the scope of improvement? The instructor's question to you:

> "If you're building a system whose simple job is to read text and classify it as billing / technical / general, and it's wrong 20% of the time — **what is the thing you would change?**"

For this system, the candidate fixes:

1. **Fix the system prompt** — maybe it's defined in a way that confuses *billing* and *technical* (e.g., vague category definitions).
2. **Change the model** — maybe the LLM you're using, a low-parameter model, isn't capable enough for this task.

---

## 8. Step 8 — Improve the system, then re-evaluate (11:38–13:06)

The manager says "80% — improve it." So you tweak the prompt or change the model — and here the instructor is emphatic about wording:

> "Here it should not be *model* — here it should be *system*. **You try to improve the system.**"

(You're not retraining an LLM; you're improving *your* application around it.)

Immediately after improving, **trigger the evaluation again**. This is exactly what *repeatable* (lecture 2) was building toward:

- Your golden dataset is fixed; you keep changing the system.
- **Iteration 1:** change the prompt → re-run on the dataset → accuracy jumps to **90%**.
- Manager: "still improve it" → **Iteration 2:** swap in the heavier/bigger LLM → re-run → **95%**. Now the manager is happy, and you stop.

You iterate in this loop — dataset → run → evaluate → analyze → improve → re-run — until you reach a place where you feel **the system is worth deploying**.

> 💡 **Expert commentary.** This loop is the eval-driven development habit that separates teams that ship reliably from teams that guess. In mature form it lives inside CI/CD as a **release gate**: every prompt/model/config change re-runs the suite automatically, and a regression blocks the merge — which is exactly where lecture 18 (regression testing) takes this idea.

---

## 9. Steps 9 & 10 — Deploy, then monitor — and the big feedback loop (13:06–14:46)

**Deploy** the system online. But the job does **not** end at deployment:

> "Without monitoring, a system can fail online too."

**Monitoring** means watching whether **production failures** are happening:

- Your system was 95% accurate *on your test dataset* — but when **new customer data** arrives, it starts making new mistakes.

When a production failure occurs, there is an **important step**: take that failure — the email content that should have been *billing* but was routed as *technical* — **add it back into your golden dataset**, then **restart the whole evaluation loop**.

The result is a *big* outer loop around everything:

> **Define → dataset → run → evaluate → analyze → improve → (re-run…) → deploy → monitor → production failures → back into the dataset → re-evaluate → keep doing it forever, as long as the system is deployed.**

That is how you build **reliable LLM-based applications** — the golden dataset keeps getting richer, and you keep improving against it, deployment after deployment.

---

## 10. Who flags wrong outputs in production? (14:46–15:55)

A question the instructor raises for the monitoring phase: *who decides the output is wrong?*

His example: a customer emails a **billing issue**, but the system **redirects it to the technical team**. The technical team follows up; the customer replies "I have nothing to do with you — I need billing." Now a **process** catches it: the technical team **flags the case** ("we were sent wrong information"), and that flagged case flows back into the dataset.

So monitoring is not only dashboards — it's an **organizational process** where the humans downstream of your classifier (the teams being routed to) become your error-reporting sensors.

> 💡 **Expert commentary.** In production systems this is formalized as **feedback capture**: thumbs-up/down UI, escalation logs, support-ticket re-tags, and LLM-judged sampling of live traffic. Lecture 19 (online evaluation with LangSmith) shows the tooling side of exactly this loop.

---

## 11. One application, many evals (15:55–16:36)

The lecture closes with "a very important point" — read this line twice:

> **One LLM-based application may have — might have — several LLM evals.**

The Zomato example had a single evaluation, but in general you run **multiple evals per application**. For a **RAG application**:

- one evaluation testing the **retriever's** performance,
- a separate evaluation checking the **embedding model's** performance,
- a separate eval testing the **entire RAG workflow** end-to-end,
- a separate eval checking the **whole system's latency**.

Generally, an LLM application **always runs more than one eval** — remember this; the rest of the course is largely the unpacking of this sentence (which is exactly where lecture 4 goes next: *why* you need multiple eval pipelines).

---

## Key takeaways

1. The **complete workflow**: define task/target → success criteria & metric → golden dataset (50–500 rows of *real*, *manually labeled* data) → eval method (automated / human / LLM) → run → evaluate → analyze → improve the **system** → iterate → deploy → monitor → feed failures back into the dataset → repeat forever.
2. The **golden dataset** is the fixed reference that makes the loop *repeatable* — production failures make it richer over time.
3. **Eval method selection is a cost/capability trade-off**: code for objective checks (accuracy on classification), LLM judges for semantic comparison of long text, humans where judgment and budget allow.
4. **Improve the system, not the model** — prompts, components, models-as-swappable-parts are all fair game; the LLM itself you don't retrain.
5. **Monitoring closes the loop** — and needs an organizational process (downstream teams flag misroutes), not just dashboards.
6. **One application, several evals** — retriever, embedding model, end-to-end workflow, latency… each is its own evaluation.

## Interview angles

- *"Walk me through how you would evaluate an LLM feature before launch."* → Recite the 10-step workflow with the email-router example; the structure itself is the answer interviewers want.
- *"Your classifier is at 80% accuracy. What do you do?"* → Analyze failure modes first (which category pairs get confused?), then fix prompt vs model vs components, re-run the same golden dataset — and quantify the improvement.
- *"What happens after deployment?"* → Monitoring + failure capture back into the golden dataset + re-evaluation — the reliability loop.
- *"How many evals does a RAG application need?"* → One per component plus end-to-end plus operational (latency/cost) — never a single number.

## Cross-links

- **Previous:** [02 — Model vs Application Evals](02-model-vs-application-evals.md) (the definitions this workflow instantiates)
- **Next:** [04 — Multiple Eval Pipelines](04-multiple-eval-pipelines.md) expands the "several evals" closer into a full design discussion.
- **Deeper:** [Section 105 note 1 — Evaluation Fundamentals](../01-evaluation-fundamentals.md) and [note 5 — Eval Engineering](../05-eval-engineering.md) (the CI/CD version of this loop).
- The monitoring handoff: [Section 104 — Observability](../../104_LLMOps/README.md); the online-eval tooling: [19 — LangSmith](19-online-eval-langsmith-monitoring.md).

<!-- nav-footer -->
---

**Navigate:** [← 02. Model vs Application Evals](02-model-vs-application-evals.md) · [Course hub](README.md) · [04. Multiple Eval Pipelines →](04-multiple-eval-pipelines.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
