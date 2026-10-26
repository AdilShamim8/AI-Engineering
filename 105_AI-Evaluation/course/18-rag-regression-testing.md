# 18 — RAG Regression Testing: Preventing Silent AI Failures

> **Lecture 18 of 19** · Unit 4: Production Evaluation · 54:16
> RAG Regression Testing Explained: How to Prevent Silent AI Failures (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/18-rag-regression-testing.md)

---

## What this lecture covers

For the past five-six sessions the course has been building one thing: a **RAG evaluation suite** — a bunch of evals that can evaluate *any* RAG application, at three levels (component, pipeline, application) and in three classes (quality, safety, operational), roughly **14 metrics** in all. That suite is now finished. This lecture adds **zero new metrics**. Instead, it wires everything together into **regression testing** — the production discipline that catches *silent* quality drops whenever anything in the system changes:

1. **What "regression" means** — a system returning to a previous, worse state — told through the instructor's war story: you push recall from 85% to 90%, deploy, and only then discover you silently damaged three-four other things.
2. **The five-step process** — one script runs the whole suite; the first run is saved as `baseline.json`; after any change you re-run and save `candidate.json`; a `compare.py` computes per-metric deltas against the baseline.
3. **Two complications and their fixes** — metrics don't all point the same way (→ the **metric registry**), and LLM-as-a-judge scores wobble run-to-run (→ the **noise threshold**: two standard deviations from repeated baseline runs).
4. **The live demo** — chunk size 1500→500 to fix low contextual relevancy, the Chroma store rebuilt, all six evals / 14 metrics re-run, then the verdict: the metric you tried to improve *regressed* (≈45 → 38), a safety metric collapsed, and `promote.py` says **block**.
5. **Where this lives in production** — "local CI" today; GitHub Actions, MLflow, Confident AI in companies; and the statistics (p-values, hypothesis testing) that serious teams layer on top when crores of rupees are at stake.

If you keep one mental model from this lecture: **a change that improves one metric is not an improvement until you've proven it didn't degrade the other thirteen.**

---

## 1. Where we are: the eval suite is complete (00:00–02:01)

The opening recap compresses the last five-six sessions of RAG evals into one diagram: a **RAG evaluation suite** — a bunch of evals with which you can evaluate any RAG application — evaluated at **three levels**: component level, pipeline level, and application level. The good news: all three sets of evals are built, and in the process the course explored **~14 different metrics** — faithfulness, answer relevancy, contextual relevancy, safety metrics, operational metrics. "So now we are at a point where we can proudly say we have built the complete RAG eval suite."

| Level | Evals built (lectures 13–17) | Metrics in the suite |
|---|---|---|
| **Component** | Retriever eval, generator eval | recall, precision; faithfulness, answer relevancy |
| **Pipeline** | RAG Triad | contextual relevancy (with the triad's pairwise checks) |
| **Application** | Quality, safety, operational suites | correctness, completeness, style; toxicity, PII leakage, scope adherence; latency, cost, reliability |

Today's session is **regression testing** — how to execute this entire RAG eval suite from a **single script** and directly generate a summary of how the application is currently performing: did the changes we made *improve* things, or did they *create problems*? After this session you can answer that question. One session then remains in RAG evals — **online evals**, where the whole thing goes online so the RAG system can be evaluated in the production setup too.

---

## 2. What regression means — and the recall war story (02:01–05:24)

The term comes from the word **regression**, whose plain English meaning the instructor writes out: *"returning to a previous, less developed or worse state."* If your system reaches a worse state than before, that is regression — and testing for exactly this is **regression testing**.

**The war story (this is the "silent AI failure" of the title):**

1. You have a working RAG application. At some point you notice **recall** isn't good and you want to improve it.
2. The standard moves to improve recall: **increase the value of K**, or **use a reranker**. Suppose you did both — raised K and added a reranker. You have changed your system.
3. Naturally, recall improves — say from **85% to 90%**. Good news.
4. The problem: one aspect of your RAG application improved, but the others regressed — **precision decreased**, **contextual relevancy went down**, or **latency increased** (because you added a reranker). And you never measured any of that, because your entire focus was recall: "recall was bad → recall must be improved → you made the changes → recall improved → you became happy → you deployed the new system."
5. Only after deployment do you realize that in the chase for recall you damaged **three-four other important aspects** of your RAG application — and that can be very harmful.

Hence the rule: **whenever you make any change to your system, you must ensure the application works correctly in all aspects, exactly as it did before the change — no regression should occur.** In practice, regression testing means: after any change (raising K, adding a reranker), **re-run the complete RAG eval suite** — all ~14 metrics — then compare the new values against the previous values, which you call the **baseline**, and analyze whether your change made the system regress. Only if it didn't do you decide to go ahead and deploy. "That's the whole story behind regression testing."

---

## 3. An old software concept, taught bare-bones (05:24–07:39)

Regression testing is **not something new**, and it is not done only on LLM-based applications. It is a very old concept that already exists in software: when you build websites, Android apps, or desktop applications, the same idea applies — you brought in a new change, now check whether the system as a whole got better or worse.

The instructor's example: you built **API V2** — the API was first written in **Flask**, then you moved it to **FastAPI**. When the new system goes live, you test overall performance: is it better or worse than before? So regression testing is fundamentally a **software development concept** that applies very well to LLM-based application development — which is why you should know it.

**Disclaimer 1:** this whole concept is explored at a very **conceptual level**, not too practically (though everything is shown via code). The regression testing process at the company you join may not look like what we see today — but the **concepts, the theory, and the idea will be exactly the same**; only the execution/implementation can differ. What we build is a deliberately **bare-bones method** — all code hand-written — whereas companies have **dedicated tools** for regression testing. The instructor deliberately avoids teaching a specific tool: understand how the thing works conceptually, and you can adopt *any* tool.

---

## 4. The setup problem: three eval classes, every eval run by hand (07:39–10:06)

The application under test is **CampusX Doubt Solve**, and its RAG eval suite contains three types of eval tests:

| Eval class | What it tests | Metrics named |
|---|---|---|
| **Quality evals** | The application's quality | faithfulness, answer relevancy, contextual relevancy |
| **Safety evals** | The safety aspect | toxicity, PII leakage, scope adherence |
| **Operational evals** | The operations aspect | latency, cost (plus reliability from the last class) |

What's needed: **one script** with the property that running it automatically starts all three sets of evals and produces their results. The current pain: everything lives as **standalone Python files** — to run a specific eval, you type the command for that specific eval, hit enter, and that eval runs. Operational evals have their separate files, safety evals theirs, quality evals theirs — so to run the whole suite you must manually run *every* eval. The fix: automate the process with a script, so that as soon as it runs, all the evals run **in sequence**, and at the end you have the results of all **14 metrics**.

---

## 5. The five-step regression testing process (10:06–13:59)

| Step | What you do | Artifact |
|---|---|---|
| **1** | Build the script — nothing but simple Python code that calls the other three Python eval programs and executes them in sequence | the run script |
| **2** | Run it for the first time; save the 14 metric results somewhere (a JSON file is fine). This is your **baseline** — what later runs are compared against to know "what state were we in before; is the new state worse?" | `baseline.json` |
| **3** | Make your change — whatever it is: **decrease or increase K, change chunk size, change the model, or change the system prompt**. All of these count as "a change" | the changed system |
| **4** | Re-run the script with the new version of the software; a new set of results arrives, again saved as JSON | `candidate.json` |
| **5** | Compare the two results **metric by metric** — what was this metric's value before, what is it after; and the second metric's; and so on — checking each individually for any metric that got worse. *That* is regression testing | the verdict |

Now the code-level flow. Two scripts: call the first one **`run_eval`** (or something like it) — the script that runs all the evaluations — and write a second one, **`compare.py`**. The flow diagram:

- `run_eval`, **first run** → produces `baseline.json` (the state before the changes).
- `run_eval`, **every later run** → produces `candidate.json` (results based on the current changes). Both files hold all 14 metric results.
- `compare.py` takes the two files as input and computes a **delta** (difference) for each of the 14 metrics, per-metric. **If the delta is negative, a metric has regressed** — its value decreased from before — and you know regression happened there.

---

## 6. Complication 1: not all metrics point the same way (13:59–15:35)

The only problem: there's a bit of complexity here. **The first complexity — "all metrics are not the same."** Some metrics are considered better the *higher* they are; others are better the *lower* they are:

| Direction | Meaning | Examples from the lecture |
|---|---|---|
| **Higher is better** | the closer to 100, the better | faithfulness, recall, precision |
| **Lower is better** | the smaller, the better | latency, cost, toxicity (as seen in lecture 16) |

So somewhere you must **store, for every metric, which type it is** — better when it increases, or better when it decreases. That's one piece of information the comparison logic cannot live without.

---

## 7. Complication 2: the LLM judge is probabilistic (15:35–17:48)

**The second complexity:** the evals being run are all **LLM-as-a-judge** — most of them. Leave the operational evals aside; look at the quality evals and safety evals — under the hood they use an LLM judge. Which means, **run-to-run, the system has a probabilistic nature**.

Concretely: you run your pipeline and all 14 metrics once and get some numbers — say **precision = 85.6**. Now you measure precision again **without changing anything in the system** — there is a big possibility the next run gives **84.8**. Why? Because under the hood these metrics are computed using LLMs, and **LLMs are probabilistic** — the same setup can give you different results.

Now the problem: if a metric drops 85.6 → 84.8 *in the same setup*, `compare.py` will simply declare "your metric has regressed." But no regression has occurred — you didn't change the system at all. So you must somehow **suppress this non-deterministic behavior** in your regression testing. The instructor pauses here for the live class: *"this is a live class and interaction is good — can you tell me how we'd solve this?"* Amarjeet answers "**noise threshold**"; Harry answers "**variance**". "Basically you already know the answer."

---

## 8. The fix: noise thresholds from repeated baseline runs (17:48–21:49)

The `baseline.json` is **not built from a single run**. With the same initial setup, you run the whole pipeline **5 to 10 times**:

1. Run 1 → 14 metric scores. Run again with zero changes → 14 slightly different scores. …Ten runs → **ten sets of 14 values** — ten values per metric.
2. Example with recall, measured ten times in the same setup: **90, 90.8, 89.7, …** — ten values.
3. Compute the **standard deviation** of those ten values — just to know how much variability lives in these numbers.
4. Then, to stay on the safe side, take **two standard deviations** as the **noise threshold**. Worked numbers: if the standard deviation comes out as 5, then 2 × 5 = **10** is your noise threshold.

Meaning: in any future experiment, if the recall delta is *less than* the threshold, count it as **noise**, not regression. Second worked example: recall was **90**; you change **K from 3 to 5** and re-run the pipeline; recall comes back 90.5 — or say **89.5**. Clearly it moved 90 → 89.5. Is that a regression? **No** — it falls within the acceptable ±1 range, so the reason for the drop is *not* your change but the noise the LLM judge injects into the system. **But** if the value had been **87.5** instead of 89.5 — now outside the noise limit — you'd say **regression has occurred**.

---

## 9. The metric registry (21:49–23:17)

So for every metric — recall, precision, each of the 14 — you need exactly **two pieces of information**:

| # | Fact | Why |
|---|---|---|
| 1 | Its **type/direction** — increasing or decreasing; better when higher or better when lower | without it you can't even interpret a delta's sign |
| 2 | Its **noise threshold** — 1 for some metrics, 5 for others, even more for others | without it you can't tell regression from judge wobble |

These are collected and stored in a **third file — the metric registry**. With these three pieces — the run pipeline (`run_eval`), `compare.py`, and the metric registry — you can do regression testing easily. Conceptually, **no other machinery is needed**.

---

## 10. Disclaimer 2: tiny golden datasets, wild numbers (23:17–24:36)

A second disclaimer, after "conceptual level, no tools": the **golden datasets** used throughout the course are **very small** — **10, 5, 15** entries — so the numbers show a lot of **variability**. Honestly: in one run your **PII leakage might be 60%**, in another **80%** — you've seen it jump 60 → 80 just by re-running the system. That much variability exists, and all of it is because the golden datasets are really very small. As you keep increasing the dataset's size, you'll see the system become **more stable**.

Also: most of the code is pre-written — don't focus too much on the code. Everything will be explained, but the real purpose is to **see the whole thing working**.

> 💡 **Expert commentary.** The PII 60→80 jump is not a bug — it's binomial noise at tiny n: on a 5-case safety set, **one flipped case moves the metric by 20 points**. At n=15 (the course's golden sets), one case is worth ~6.7 points, so a 7-point drop like the demo's contextual-relevancy 45→38 is *one flipped case plus judge wobble*. The remedies stack: grow the dataset (50–500 rows, per lecture 3's guidance), repeat runs (lecture 11's 5-run advice), and keep a held-out slice you never tune against (lecture 13). Rule of thumb: when a metric gates releases, size its dataset so the noise threshold sits comfortably below the smallest delta you would actually act on.

---

## 11. Reorganizing the codebase for automation (24:36–30:44)

Step by step, the changes to the existing codebase. Current setup: an **`evals/` folder** holding the separate eval files.

| Before (lectures 13–17) | After (this lecture) |
|---|---|
| `eval_reliability`, `eval_cost`, `eval_latency.py` — three operational files (built in the last class) | **`eval_ops`** — one merged file; running it runs all three operational evals |
| `eval_leak`, `eval_toxicity`, `eval_scope` (scope adherence) — three safety files | **`eval_safety`** — one merged file; running it runs all three safety evals |
| Four quality files — retriever, generator, pipeline, application (built first of all) — plain procedural scripts printing to the terminal | Same four files, **refactored** (see below) and standardized by **`harness.py`** |

Notes on this reorganization:

- **Keep or delete is your choice.** Once the merged files exist you can delete the individual ones for a cleaner repo; the instructor kept both — the individual files are *easier to understand*, the merged files are what regression testing uses.
- **Quality evals are *not* merged** into one file — the four files (retriever, generator, whole pipeline, application) remain four. (The instructor momentarily can't recall whether it's three or four, checks `eval_retriever`, and confirms four.)
- **The refactoring:** those four files had one problem — their output was printed to the terminal. The code stays exactly the same, but it's now wrapped in a **`run` function** inside an **`if __name__ == "__main__"`** structure, so the file can be run by *you* AND called and executed by an *external* script. Before, it was simple procedural, line-by-line code. The same change was applied to all four files — generator, application, pipeline — with the logic untouched.
- So the first three steps: quality evals refactored; safety evals consolidated into a single file; operational evals consolidated into a single file.
- **One more piece — `harness.py`:** to join the four quality evals together — so the *same input* can be given to them and output received *in the same format, from the same place* — the instructor wrote a small **harness** (he didn't write it himself; **he had Claude write it**). Its only job: **standardize** the four application quality evals — standardize their method of running. Nothing else. Without `harness.py`, you cannot send the same input to the four files and extract output in the same standard format.

---

## 12. The three regression-testing files in code (30:44–34:03)

| File | Job |
|---|---|
| **`run_suite.py`** | The main file that carries the code to run *all* the scripts. Behind the scenes it runs **quality evals first, then safety, then operational**, and generates a complete report of the situation. **First run saves to `baseline.json`; every subsequent run saves to `candidate.json`.** From now on, regression testing = run `run_suite.py` |
| **`metric_registry`** | Solves the two problems: for each of the 14 metrics, its **direction** ("higher means better") and its **noise tolerance** |
| **`compare.py`** | Takes `baseline.json` + `candidate.json` + the metric registry → computes the **delta for each metric** → tells you which metrics **regressed**, which **didn't change**, and which **improved** |

**Where did the noise tolerances come from?** Very simple: the instructor ran `run_suite.py` several times, using the method from section 8. It *should* be run 10 times — he ran it only **twice**, because it takes time and costs money. The ideal setup: run it **10 times with no code changes**, use the ten runs' values to compute the **standard deviation per metric**, **multiply by two**, and write that number into the registry for each metric.

---

## 13. The demo: change the chunk size, rebuild, run the suite (34:03–38:20)

Current state: `baseline.json` already exists (the baseline everything will be compared against); a `candidate.json` also exists — delete it and create a fresh one.

**The change.** Open `retriever.py` and **reduce chunk size and chunk overlap** — currently, say, **1500** → set it to **500**, and the overlap to **100**. Save. The narrative: our **contextual relevance was coming very low — around 43–44%** (if you remember lecture 14) — and we want to raise it; one way to raise it is **reducing the chunk size**. Done. And since these values changed, the **Chroma store — the vector database — must be deleted** so the whole embedding is created fresh (the chunking changed).

**The run.** From the `evals` folder, run `run_suite`, passing an input that gets **logged** with the run: *"chunk size now 500 and overlap now 100."* As soon as it runs, the entire eval suite built over the last five sessions starts executing on its own; when execution finishes, all the metrics are logged into a `candidate.json` that can be compared. It takes time — **you're literally running 14–15 evaluations** — and because the vector database was deleted, the pipeline is rebuilt first, then the pipeline runs, then all the evaluations run on top of it. (Live-class aside: the instructor fiddles with the terminal font size — too small, then too big.)

**Six evaluations** run, and the instructor explains exactly why six:

| # | Evaluation | What's measured |
|---|---|---|
| 1 | Retriever eval | recall, precision |
| 2 | Generator eval | faithfulness, answer relevance |
| 3 | Pipeline eval | the RAG Triad |
| 4 | Application eval | application quality |
| 5 | Safety eval | toxicity, PII leakage, scope adherence |
| 6 | Operational eval | latency, cost, reliability |

First to finish: the **retriever** values arrive — **recall 96, precision 90** ("I don't remember what the baseline was, but whatever"). Second begins: the **generator** eval, tracking **faithfulness** and answer relevance ("what was the other one? — answer relevance"); it takes about **5 minutes** by his calculation, so the chat is opened for questions meanwhile. Third up: the **RAG Triad**.

---

## 14. Live Q&A: direction flags, fault attribution, CI time, the online teaser (38:20–42:35)

| Student | Question / remark | Instructor's answer |
|---|---|---|
| Amar | Can we multiply the diff with the direction (−1 or 1), now that we have a standard definition of higher-is-better? | Yes — it's the same thing; the code implements exactly that; you can use −1 and 1. That's what the metric registry carries: the metric's nature (better when higher or lower) and the noise threshold computed by repeatedly running the baseline and measuring the standard deviation. Both facts are needed at comparison time — direction to interpret the delta, threshold to ensure the change is bigger than noise |
| Amarjeet | How do you determine whether a wrong answer is caused by **retrieval or generation**? | It depends on the metrics — **all the metrics together tell you**. If recall, precision, and contextual relevancy are good *but the answer is wrong* → the **generator's** fault. If the generator's own metrics are fine but a retriever metric is bad → the **retriever's** fault |
| Harry | (these tests take time) | Of course — if you integrate this into **CI**, the tests take time to run. There's no hurry to deploy; you can take your time, because you want the **best software** deployed. How long the process takes is not the concern — **the work happening correctly is the priority** |
| Harry | (next session?) | **Online evaluation** — everything learned so far, run in an online setup. "Did you not expect we'd study online too?" Without online, you only know **half the story** — if after deployment you can't evaluate, what's the benefit? |

The run continues: **safety** evaluations are measured ("just 2 minutes — the safety numbers arrive"), then the **operational** numbers: **latency first, then cost, then reliability** — and the run completes. All the behavior is exactly what you saw in previous sessions — just joined together, bound into a single script so an automated script runs them behind the scenes instead of you running each one. **"In today's class we did nothing new. We just combined them."**

A student remarks: *"you can call this local CI."* The instructor agrees — yes, this is **local CI**. When you take this to GitHub with **GH Actions** (GitHub Actions), you're basically performing a kind of **CI** — and regression testing, conceptually, in a proper production setup, **is part of CI; it's utilized within CI**.

> 💡 **Expert commentary.** "Part of CI" has a concrete meaning worth memorizing: the eval suite becomes a **required status check** on a pull request — the PR that touches `retriever.py` (chunk size, k, model) triggers `run_suite.py` in a GitHub Actions workflow, and the merge button stays locked until `compare.py` reports no regression. Mature teams add **path filters** (run the full suite only when prompts/retrieval/config change, not on a README edit) and **tiered speed** — fast deterministic checks on every PR, the golden suite on qualifying PRs, the full suite nightly or pre-release — because a 40-minute gate gets skipped while a 6-minute core gate gets obeyed. That layering is the core design of [Section 105 note 5 — Eval Engineering](../05-eval-engineering.md).

---

## 15. The cost of evaluating — and the composite-metric temptation (42:35–43:47)

**Cost.** "This is quite expensive, by the way — an important point." Despite the small dataset, a **single execution of the pipeline costs around ₹25–30 or more**. Now imagine the golden datasets were bigger — **50, 100, or 500 rows instead of 15** — this whole process has a cost you must keep in mind. It's not only about running the software; when you're **evaluating**, you have to be smart.

**The composite-metric question (Amar).** It really depends on your application. If you're a **domain expert** — you understand how your RAG application works, which quality metrics matter there, and whether they relate to each other — then maybe you can build a **composite number or formula**, assign weights, and read your overall quality off a single number. **But in the instructor's experience, that is generally not done** — and there's a reason the separate metrics exist: they each tell you about a *different aspect* of your RAG application, so merging them all into a single dimension is most likely not useful. "A tempting idea, though."

> 💡 **Expert commentary.** The instructor's "tempting but don't" verdict matches industry practice. A weighted one-number score is fine for **screening** — lecture 11 used aggregate comparisons to *pick a model* — but dangerous as a **gate**: a composite lets a latency win cancel out a safety loss, which is precisely the trade no product should make silently. If you must summarize, keep the components visible — per-metric history with decision boundaries drawn on the dashboard, SRE-style — and reserve hard gates for individual metrics, especially safety. This is Goodhart's-law territory: optimize the weighted number and the system will find ways to pump it that the individual metrics would have caught.

---

## 16. The verdict: reading the compare.py report (43:47–47:48)

The run's output — all **14 metrics and their complete results** — is in front, logged into `candidate.json`. At this point you hold: the **baseline** (the state before) and **`candidate.json`** (the results after the change). To compare them you need the third file, the **metric registry** — it tells you whether a number going up is good or bad, and what the noise threshold is. Then it's one command: run **`compare.py`** with input **`all`**, and it reports *every* metric — improved, worse, or the same.

**The result:**

| Verdict | Metrics | Detail |
|---|---|---|
| **Flat / unchanged** | most metrics | not much change — whatever change exists sits **within the noise threshold**, so it's considered negligible |
| **Improved** | ~4–5 metrics | a fair number of metrics genuinely improved |
| **Regressed** | 2 metrics | **contextual relevancy** — the very thing all this work was for — dropped from near **45 to 38**; and the **PII leak score** came down to **6** — another big regression |

**"Even the one that was supposed to improve — that one decreased."**

Now you look at this entire report and decide whether your system regressed. Sometimes it's very clear: one of your **safety** metrics dropped a lot — a big warning, a **red flag**. "If suddenly, after a system change, a safety metric drops by **20%**, that's a big red flag that the changes you made are not good. **Why would you compromise with safety?**" And contextual relevancy is being hurt too. So the system is regressing because of two metrics, even though some improvements happened. At this point **a human comes in and decides** whether the change is good — it's subjective and depends on the application. But the report is in front of you: which metrics went up and which went down after the change. **That is the entire goal of regression testing.**

---

## 17. promote.py: automating the promote/review/block decision (47:48–50:15)

One more small file: **`promote.py`** — a kind of decision-making code. It **reads the report** and generates a summary: should we approve this new change or not? The logic assigns every metric to a **tier** (defined as classes — a small decision framework that will differ from application to application):

| Tier | If this metric drops… |
|---|---|
| **Non-negotiable** | "chalega hi nahi" — it simply won't do; the change cannot be accepted |
| **Discussable** | we can discuss whether to maybe deploy this new version anyway |
| **Doesn't matter** | a decrease makes no real difference |

The verdicts it can return: **promote** (take the change forward for deployment/consideration), **review** (human experts come and decide whether to accept it), or **block** (the change brings such bad results there's no point taking it forward). "It's not at all necessary — I just made it anyway," so decisions arrive quickly.

**Running it on the demo:** it takes `compare.py`'s output and returns the verdict — **block**, because a very important metric, **safety, dropped 20%**, so there's no point approving this change. **The counterfactual:** had the safety metric *not* dropped — only contextual relevancy — then per `promote.py`'s logic the change would go to **review**: human experts would weigh "contextual relevancy came down a bit, but **five metrics improved** — do we take it forward or not?", run more tests, decide, and then upgrade and deploy that version.

> 💡 **Expert commentary.** `promote.py` is a miniature **release gate**, and its three-state verdict is the industry pattern: *block* (fail-closed, non-negotiable metrics — safety, data leakage), *review* (a human weighs the trade-off — exactly the "five improved vs one regressed" judgment the demo needs), *promote* (ship it). Two production hardenings worth naming in an interview: make tier assignments **reviewable configuration**, not buried code — a threshold change should be a diff with a written rationale — and **test the gate itself**: inject a known-bad change once in a while and confirm the suite catches it. A gate that has never fired is theater.

---

## 18. Tools, scope, and the statistics beyond (50:15–54:16)

**Tools.** In practice you usually do all of this with the help of software. **Himanshu** teaches the same concept in the LLM Ops course using **MLflow**; another team might use **Confident AI** or some other tool. The instructor showed it via complete, hand-written code so the concept sticks. The main idea stays the same everywhere — the noise-threshold procedure is the same, the decision-making framework gets built there too, baselines are computed multiple times. The only difference: hand-written code vs a more advanced tool ("of course that's much better").

**Scope.** This is all we'll cover on the topic, because it is **not directly part of LLM evals** — related, yes, but no new *evaluation* is being learned here, so the instructor deliberately doesn't go further. The goal was a high-level overview of how the effort of the last five sessions gets used in a production setup. A deliberately small one-hour class (online evals would take 2+ hours; he didn't want a 3-hour class). You didn't learn anything deep — you took away the concept: **what regression testing is, why it's important, and how it's implemented practically in an eval setup.**

**Harry's closing question:** *"For noise threshold calculation, are we only taking the parameter values at the time of standard deviation computation?"* — Yes, that's right. The instructor ran it **twice** in his setup; when you work at a company, on a real project, run it **at least 5–10 times** to get a correct standard deviation value.

**And beyond.** Many more ideas are involved when you do this properly — the concepts of **statistics** come in: **p-values**, whether a result is **statistically significant**, and all the ideas of **standard deviation and hypothesis testing** applied here. It's a huge field: think of ChatGPT-scale software — you make one improvement, and now you must **prove** the whole system didn't regress anywhere; only when you're certain do you go ahead and deploy. "Think — where **crores of rupees** are at stake, how important this regression testing is." All those statistical concepts are used to deal with the uncertainty; there's a lot to study here and **many experts are needed**. This course covered it at a top level — enough to crack interviews.

> 💡 **Expert commentary.** The 2σ noise threshold is a 95% intuition borrowed from normal-distribution statistics: an unchanged system produces a swing that large only ~5% of the time. Two refinements matter in practice. **Small samples:** with 5–10 runs, the sample standard deviation is itself noisy — a t-distribution or bootstrap confidence interval is the honest version. **Multiple comparisons:** you're testing 14 metrics at once, so a ~5% false-alarm rate *per metric* means roughly a coin-flip chance that *at least one* metric flags on an unchanged system. Real suites handle this by tightening per-metric thresholds, tracking false-positive rates over time, or treating "one metric barely outside noise" as a *review* signal rather than a *block* — which is exactly what the promote/review/block tiers accomplish. And the cheapest fix comes *before* statistics: reduce variance at the source with temperature-0 judges, pinned judge versions, and fixed seeds where the API allows — every threshold shrinks at once.

---

## Key takeaways

1. **Regression** = a system returning to a previous, worse state. **Regression testing** = after *any* change (K, chunk size, model, system prompt), re-run the complete eval suite and compare every metric against the baseline before you deploy.
2. **The war story:** recall 85% → 90% via bigger K + a reranker silently cost precision, contextual relevancy, and latency — invisible until after deployment if nobody re-runs the suite. That is the "silent AI failure" this layer prevents.
3. **The five-step process:** build the run script → first run saved as `baseline.json` → make the change → re-run and save `candidate.json` → `compare.py` computes per-metric deltas; a negative delta (direction-aware) flags a regression.
4. **The metric registry:** every metric needs two facts stored — its direction (higher-is-better vs lower-is-better) and its noise threshold.
5. **LLM-as-a-judge makes evals non-deterministic:** the same unchanged setup can score precision 85.6 then 84.8. The fix: run the baseline 5–10 times, take the standard deviation per metric, and set the **noise threshold at 2× σ** — deltas inside it are noise (recall 90 → 89.5 with K 3→5), deltas outside it are regressions (90 → 87.5).
6. **Tiny golden datasets (5–15 entries) mean wild swings** — PII leakage jumping 60 → 80 between runs is expected at that n. Grow the dataset to stabilize the numbers.
7. **The code shape:** merge operational evals into `eval_ops` and safety evals into `eval_safety`; refactor the four quality eval files behind a `run()` function + `if __name__ == "__main__"`; standardize them with `harness.py` (Claude-written); orchestrate everything with `run_suite.py` (quality → safety → operational → report).
8. **The demo's lesson:** the change made *to fix* contextual relevancy made it worse (≈45 → 38) and collapsed the PII leak score (→ 6) — caught only because the whole suite re-ran. Most metrics were flat, 4–5 improved, two regressed.
9. **`promote.py` tiers → promote / review / block.** Safety is a hard gate: a 20% safety drop blocks outright ("why would you compromise with safety?"); quality trade-offs (5 improved vs 1 regressed) go to human review.
10. **This *is* CI:** local CI today, GitHub Actions in a repo; MLflow (Himanshu's LLM Ops course) and Confident AI implement the same ideas with dedicated tooling.
11. **Evaluation costs money** — ₹25–30 per full-suite execution even at n=15 (and 10× that for the baseline runs) — so be smart about when and how often the suite runs.

## Interview angles

- *"What is regression testing in the context of LLM applications?"* → Definition (returning to a worse state), the recall-85→90 war story, then the mechanics: full suite re-run, baseline comparison, deploy only if nothing regressed. Mention that it's an old software concept (Flask→FastAPI V2) that transfers directly.
- *"Your LLM-judge metrics change between runs with no code change. How do you build a regression gate that isn't flaky?"* → Repeated baseline runs (5–10 in production), per-metric standard deviation, 2× σ noise threshold, direction-aware comparison via a metric registry; deltas within noise are ignored. Bonus points for mentioning judge pinning/temperature-0 and false-positive rates across 14 metrics.
- *"How do you attribute a wrong answer — retrieval or generation?"* → Read the metrics together: retriever metrics good + answer wrong = generator's fault; generator metrics good + a retriever metric bad = retriever's fault.
- *"Would you collapse all quality metrics into one weighted score?"* → Generally no — separate metrics exist because they measure different aspects; composites hide the exact trade-offs (a latency win canceling a safety loss). Fine for screening (model selection), wrong for gating.
- *"Walk me through your release gate for a RAG change."* → `run_suite.py` → `candidate.json` vs `baseline.json` + registry → `compare.py` per-metric verdict → tier-based promote/review/block, with safety fail-closed and humans adjudicating quality trade-offs.
- *"How does this connect to CI/CD, and what does it cost?"* → GitHub Actions as required status checks on PRs that touch prompts/retrieval/config; path filters and tiered speed to control cost; each full run costs real money (₹25–30 at n=15) — plus time, which is acceptable because the best software shipping is the priority.

## Cross-links

- **Previous:** [17 — RAG Operational Evals](17-rag-operational-evals.md) — the last piece of the suite that this lecture wires together.
- **Next:** [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md) — takes the suite online, into production monitoring ("without online you know half the story").
- **Parent note:** [Section 105 note 5 — Eval Engineering](../05-eval-engineering.md) — CI quality gates, noise floors, and tiered suites are its core topic.
- **Foundations:** [12 — RAG Eval Interview Answer](12-rag-eval-interview-answer.md) (where regression testing and the manual → MLflow → GitHub Actions maturity ladder was first sketched) · [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) (the improve → re-run loop this lecture industrializes).
- **Deep background:** [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) and [14 — RAG Triad](14-rag-triad-generator-pipeline.md) (the contextual-relevancy metric the demo regresses, and chunk-size tuning) · [15 — G-Eval](15-geval-deterministic-judge.md) (the judge whose noise the threshold tames) · [16 — RAG Security](16-rag-security-toxicity-leakage-scope-drift.md) (the safety metrics that hard-gate the release).
- [Course hub](README.md)
