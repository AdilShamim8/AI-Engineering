# 15 — Mastering G-Eval: The Deterministic LLM-as-a-Judge Framework

> **Lecture 15 of 19** · Unit 3: RAG Evaluation · 1:26:52
> Mastering G-Eval: The Deterministic LLM-as-a-Judge Framework Explained (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/15-geval-deterministic-judge.md)

---

## What this lecture covers

Lecture 14 finished the pipeline level (the RAG Triad). This lecture opens the **application level** of the eval suite and builds its first piece: the **quality** eval suite for the CampusX Doubt Solver, using three metrics — **correctness**, **completeness**, and **style**. All three belong to a class the course has never handled before: **judgment-based metrics**, where the claim-decompose-count-ratio machinery of lectures 13–14 simply does not apply. The vehicle for judging them is **G-Eval**, the 2023 paper-backed framework that turns LLM-as-a-judge from a coin-flip into a measurement instrument:

1. **The problem** — the naive "give the judge one line of criteria and ask for a 0–10 score" recipe is theoretically fine but practically unreliable: the score has **very high variance**.
2. **G-Eval's two innovations** — (a) break the high-level criteria into **evaluation steps** via **Chain-of-Thought** (a written rulebook/constitution for the judge), and (b) replace the sampled score token with a **probability-weighted score** computed from the top tokens' log probabilities.
3. **The math** — top-k token probabilities → drop non-numeric tokens → normalize → weighted average → divide by 10 → compare to a threshold (worked example: 0.70/0.20/0.05 → **7.84**, not 8).
4. **The hands-on build** — correctness, completeness, and style implemented in **DeepEval** on the 15-question golden dataset, including the debugging loop (read the judge's failure reasons → refine the steps/rubric or the generator prompt → re-run) that takes correctness **66% → 84% → 83%**, completeness **0.68 → 75%**, and style **54% → 74%**.

If you keep one mental model from this lecture: **G-Eval is not a new technique — it is LLM-as-a-judge made deterministic. Give the judge a written rulebook (CoT steps + rubric) and read its score from its token probabilities, not from its tokens.**

---

## 1. Where we are: entering the application level (00:00–03:19)

Two or three sessions ago the course started RAG evaluation with a detailed plan: the primary goal is an **offline eval suite for the RAG pipeline**, prepared at **three levels**. Status check:

| Level | Status |
|---|---|
| **Component level** (retriever, generator) | ✅ Already built |
| **Pipeline level** (RAG Triad) | ✅ Done in the last session |
| **Application level** | ▶️ Starts today |

At the application level, **three types of eval suites** will be built:

| Eval suite | What it checks |
|---|---|
| **Quality** | Is the application's output good? — **today's topic, strictly** |
| **Safety** | The safety aspect of the application |
| **Operations** | The operations aspect of the application |

Safety and operations (plus **regression testing**) will most likely be covered in the next session. Today's plan is simple: build an evaluation pipeline that tests application quality on **three metrics**:

1. **Correctness** — is the answer coming from our RAG chatbot correct or incorrect?
2. **Completeness** — if a question contains two questions inside it (a question plus another question along with it), does the answer cover *both* sub-questions, or is it a partial answer?
3. **Style** — does the doubt solver's explanation style match the **CampusX teaching style**?

And in the process of learning all this, the course also introduces **G-Eval** — "a very important concept… kind of important for interviews." The instructor promises to conduct the entire lecture "in a very lucid style — at any point, you will know exactly what we are doing."

---

## 2. The five metrics so far share one pattern: they are count-based (03:19–05:59)

So far, five metrics have been covered to evaluate this RAG application: **Recall**, **Precision**, **Faithfulness**, **Answer Relevance**, and **Context Relevance**. There is a common pattern across all five: **they are all count-based metrics.**

The instructor explains what that means with the **faithfulness** example. Faithfulness tells us whether the answer our generator produced was generated completely from within the context, or whether the generator invented something on its own. How was it calculated in the previous sessions?

1. Take the **generated answer**.
2. Use an **LLM** to break it down into **claims** — claim one, claim two, claim three, claim four.
3. Take each claim and ask whether it exists within the context. If it does, that's a good thing; if it doesn't, that's a bad thing.
4. **Count** how many of the total claims exist within the context.

> Suppose three of the four claims came from within the context and one claim was invented by the generator itself. Then the faithfulness score is **3/4**.

Look at what is happening: "You are counting, in a way… you are literally counting, out of the total claims, how many claims are coming from the context." Across all five metrics — recall, precision, answer relevance, context relevance — the course did more or less the same thing: with the help of an LLM, break things into claims, count how many were in our favor and how many against, and apply some formula to calculate the score.

---

## 3. When counting doesn't exist: judgment-based metrics (05:59–10:33)

> "But what if we get stuck in a situation where we have metrics where the concept of counting doesn't even exist?"

**The style example.** Suppose we need to find out whether a generated answer is in CampusX's teaching style or not. Suddenly the method of counting and calculating a ratio won't work. You have an answer; suppose you break it down claim by claim or statement by statement — will you test whether *every statement* follows the CampusX style? Suppose CampusX's style is **Why-What-How**: that Why-What-How will **not** exist in every single sentence. It exists at the **answer level**, not at the **sentence level**. So a new class of metric — style — cannot be handled by breaking it into claims and counting. Here, instead of counting, you need **judgment**: someone who reads the answer and simply assigns a score — "on a scale of one to five, this particular answer rates a four in terms of CampusX's style," or a five, meaning the entire answering style matches CampusX.

**The correctness example.** Can correctness be measured with a count-based method? You would break the answer into claims again, and you have a **golden answer** (the correct answer). You take each claim and ask whether it is related to the golden answer — that is how you would count. But is it possible that every claim is *directly* related to the golden answer? **No.** The instructor's scenario:

> "Let's say our chatbot is using an **analogy** to explain something. If you analyze the analogy in isolation, it will make no sense. An analogy will make sense only when it is analyzed inside an answer."

An analogy is, by definition, a *different* example from the current scenario. If you take it as an independent claim and compare it to the golden answer, the judge LLM will say this statement is not related to the golden answer — a false claim — and penalize it. So correctness cannot be checked at the claim level; it must be checked at the level of the **entire answer**. Again: counting fails, judgment is needed — and that judgment could come from a **human or an LLM**.

**Members of this family:** style, correctness, **completeness**, **helpfulness**, and all metrics related to **safety**. All three metrics covered today are judgment-based, so all three will use an LLM to produce the score.

> 💡 **Expert commentary.** The lecture's examples echo the original G-Eval paper — Liu et al., *G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment* (EMNLP 2023, [arXiv:2303.16634](https://arxiv.org/abs/2303.16634)). The paper built judges for **summarization quality on four aspects — coherence, consistency, fluency, and relevance** — and for dialogue generation, and reported that G-Eval with GPT-4 achieved a **Spearman correlation of 0.514 with human judgments on SummEval**, the highest among all compared metrics (including GPT-3.5-based variants and classics like ROUGE/BERTScore). Coherence, fluency, and "does it read like the author's voice" are exactly the properties that cannot be counted — which is why the paper's framework maps so cleanly onto the lecture's style metric.

---

## 4. The naive LLM-as-a-judge recipe (10:33–15:20)

So what must be done for all of today's metrics? Simple: **use an LLM to find the score.** The instructor walks the recipe with correctness — measuring the correctness score of the RAG chatbot, i.e., if we ask it 10 questions, what percentage does it answer correctly?

**Step 1 — prepare a golden dataset.** You have to specify what a correct answer looks like. The dataset has a **question** on one side and its **correct answer** on the other. A "correct answer" means a **universally accepted answer — the same you would find on Google**. It does *not* have to be what the instructor taught in class. Assume 15 rows: 15 questions with their correct answers. (How this dataset is created is discussed later in the lecture.)

**Step 2 — bring in an LLM judge** and give it a prompt like this:

> "You are evaluating whether an AI's answer is correct. You will be given a **question** and an **expected answer** [and the **actual answer**]. Compare the actual answer against the expected answer and decide how factually correct it is. Give a score from **0 to 10**, where 10 is fully correct and 0 means completely wrong."

The question comes from the golden dataset, the expected answer comes from the golden dataset, and the actual answer is generated: we feed the question to the RAG chatbot, it gives back a generated answer, and we pass that same generated answer to the LLM judge.

**Step 3 — score and average.** The judge looks at all three things and returns a score telling us how accurate the RAG application is on that particular question. Do this for all 15 questions, then **take the average** of the 15 scores.

**The difference from everything before.** Earlier, the LLM-as-a-judge was used for a *small task* — breaking text into claims and checking whether they were in the context — and *we* derived the score by calculating a ratio. Here, **no such ratio exists**: we rely entirely on the LLM's judgment, asking it to look and simply give a number out of 10. "We haven't really studied anything special. It is actually *easier* than what we have studied so far, if you pay attention." And in this same flow, instead of correctness, you can extract **completeness** or **helpfulness** just as easily — the entire flow stays the same; keep switching the metric and the work is done.

---

## 5. Why the naive recipe is unreliable: variance (15:20–24:07)

> "This method will work theoretically. But when you go to implement this practically, this method does not give you very good results. This is not considered a very good evaluation method. Can anyone tell what is the problem?"

The instructor pauses the class to think ("take one or two minutes… think about it once and tell me what could be wrong with this"). The classroom's answers and his responses:

| Who | Proposed flaw | Instructor's response |
|---|---|---|
| **Harry** | The judge itself makes mistakes | True — but that is *always* true. Assume a state-of-the-art judge that makes no (or very few) mistakes |
| (chat) | Latency and cost | Real — you are using an LLM. But on just 15 questions the cost won't be that high |
| **Tushar** | The system prompt might become large and start missing relevant details | Honestly, no — the prompt is small: the question is 1–2 lines, the expected answer maybe 10 lines, the generated answer 10 lines |
| (chat) | Criteria need to be given through the prompt | We *did* specify the criteria — in exactly **one line** (that turns out to be part of the problem) |
| **Nidhi** | LLM issues like bias and hallucination | Bias is an issue — but not the main one |

**The major flaw: the score will have very high variance.** Evaluate once, you get one score; evaluate a second time, you get a different score. If the entire setup is the same — same question, same expected output, same generated output — the score *shouldn't* vary much between runs. In this technique, it does. There are **two reasons**, sharing a common theme:

**Reason 1 — no tight constitution.** You gave the judge a single loose line ("Compare the actual answer against the expected answer and decide how factually correct it is") and left it to interpret. Every subsequent question is an **independent call** to the LLM, and each call may perceive that statement differently — one call measures correctness from a certain aspect, the very next call measures it from a different angle. "You haven't provided a very tight constitution… a rulebook on how exactly to measure correctness."

**Reason 2 — sampling a single integer token.** You simply ask it to generate a score between 0 and 10. Everything is probabilistic — every token gets assigned a probability. The instructor's worked example of the same question run twice:

| Run | p(6) | p(7) | p(8) | Output (highest-probability token) |
|---|---|---|---|---|
| 1 | 9% | 40% | **51%** | **8** |
| 2 | 9% | **51%** | 40% | **7** |

In run 1 the model's internal calculation gave the 7 token 40%, the 8 token 51%, and the 6 token 9% — so it output 8. The next run had a slightly different interpretation: 8 got 40%, 7 got 51%, 6 stayed at 9% — so it output 7. The model had "a bit of doubt between seven and eight," and the printed integer keeps fluctuating. **The consequence at the aggregate level:** when you average over 15 questions, one run gives 60, another 70, another 75. Compare that to everything the course has run so far — "if it was 85, it would become 86 or 84, but there isn't a jump from 75 to 85." That instability is why **this method is not used directly in the industry**, and why you don't use LLM-as-a-judge "directly." The instructor's recommendation: if you are running this project on your machine, write code that measures correctness this way and run it three or four times — "I guarantee you that your result will vary a lot; it will vary significantly."

---

## 6. G-Eval: the paper and innovation #1 — criteria → evaluation steps via CoT (24:07–27:52)

> "To solve this very problem, who comes in? **G-Eval**. Exactly to solve this problem, G-Eval comes in."

**G-Eval is a research paper that came out in 2023** — the instructor shows it on screen and recommends reading it once, "especially now that you have attended today's class, you will understand very well what has been proposed in this paper." It is a technique that solves the variance problem. How?

**Step 1 — specify which metric you want to calculate.** In our case, correctness.

**Step 2 — specify the criteria.** The one-liner — "compare the actual answer against the expected answer and decide how factually correct it is" — is what G-Eval calls the **criteria**: the high-level instruction for calculating correctness (here, correctness based on factuality).

**Step 3 — G-Eval's first move.** It brings in an **LLM judge** — generally **GPT-4**; the paper states that G-Eval gives the best results with the GPT-4 model — and gives it a task: use **CoT (Chain of Thought)** to convert the criteria into **evaluation steps** — roughly four to five exact steps. In the instructor's words:

> "We are now creating a **rulebook**. We are creating a **constitution** on how we will measure correctness. As soon as you have this constitution, all the evaluation you do afterward is based on this constitution and this rulebook."

This is the first difference from a normal LLM-as-a-judge: the high-level criteria from the programmer/evaluator gets **broken down with the help of CoT**. (CoT = thinking step-by-step — the instructor recalls teaching it during the **ReAct pattern** in the LangChain playlist: Chain-of-Thought prompting breaks a given problem into steps.) Those evaluation steps are then used to actually calculate correctness.

---

## 7. The G-Eval judge prompt: evaluation steps + scoring rubric (27:52–30:32)

Once the evaluation steps exist, the next step (the instructor's "step number three") is to create the system prompt for the judge. The example G-Eval system prompt shown in the lecture:

> "You are an evaluator scoring the correctness of an AI-generated answer. You will judge the actual output against the expected output… using the evaluation steps below."

Where did the steps come from? The criteria was broken down through CoT. The steps on the slide:

1. Compare **only the factual claims** in the actual output against the expected output.
2. A claim is wrong **only if it contradicts** the expected output or is factually false.
3. A factually accurate answer **scores high even if it is shorter or covers fewer points**; do not deduct for brevity or omitted points; only wrong statements count.
4. *(one further step on the slide, not read aloud)*
5. **Additional correct information must never lower the score.**

Below the steps, the prompt also carries a **scoring rubric** — if the answer is like *this*, score it 9–10; like *this*, 5–8; like *this*, 0–4 — "I am guiding it even more on how the scoring should be done." And the concrete inputs are provided separately: the **question**, the **expected output**, and the **actual output**.

Why this solves variance problem #1: rather than a high-level criterion the model can re-interpret on every call, it now receives a four-five-bullet **constitution**. "Suddenly, it becomes more deterministic compared to before. Now we haven't left any scope for it to use its own brain. Just follow what we are saying."

---

## 8. Innovation #2: probability-weighted scores (30:32–37:13)

> "Now comes the next innovation of G-Eval."

Earlier the judge simply generated a score between 0 and 10 — and because it was generating an integer, the chance of variance was very high. G-Eval solves this with **probability-weighted scores**, and to understand it you need to know how any LLM/transformer generates output.

**The autoregressive primer.** The final layer of the network has as many nodes as there are output tokens — assume **10,000** output tokens containing everything: all the words, all the digits. Based on the input, the model assigns a **probability to each token** (this token "is" gets some probability, "the" gets another, "zero" another, "hello" another). The token with the **highest** probability is printed; it then gets added to the input, and the entire process repeats. "Your output gets printed in an **auto-regressive manner**."

**What a "score 0–10" prompt does to the distribution.** If the prompt explicitly says "analyze this and assign a score between 0 and 10," then — even though there are 10,000 tokens, each getting a probability — the larger probabilities will obviously concentrate on the tokens **0, 1, 2, … 10**. Words like "is" and "the" get lower probabilities; a word like "with" gets a *very* low probability, because for this prompt the output can never be "with" — it has to be some number.

**Extract top-k.** You cannot extract probabilities for all 10,000 tokens — too much compute. Any LLM lets you see the probabilities of the **top-k** tokens; assume we extract the **top five**. Suppose for the current prompt those five tokens are **8, 7, 9, and — by mistake — "the" and a colon**, with these probabilities:

| Top-5 token | Probability |
|---|---|
| **8** | 0.70 |
| **7** | 0.20 |
| **9** | 0.05 |
| "the" | 0.01 |
| ":" | (tiny) |

**Step 1 — ignore the non-numerical tokens**, because they don't matter; only numerical tokens matter. You are left with 8, 7, and 9 — whose probabilities sum to **0.95**, not 1 (many tokens were left out).

**Step 2 — normalize** so the remaining probabilities sum to one: divide each by 0.95.

| Token | p | Normalized p |
|---|---|---|
| 8 | 0.70 | 0.7368 |
| 7 | 0.20 | 0.2105 |
| 9 | 0.05 | 0.0526 |

**Step 3 — weighted average** (not the raw probabilities): score = 8 × 0.7368 + 7 × 0.2105 + 9 × 0.0526 = 5.89 + 1.47 + 0.47 ≈ **7.84**.

**The contrast.** In a normal setup — "if instead of taking log probabilities, we extracted an output and printed the actual token value" — the output would be **8**, obviously: out of all the tokens, the model assigned the highest probability to 8, so we would directly declare the correctness score of this question to be 8. G-Eval says no: "We will also see how sure you were about seven, how sure you were about nine, and how sure you were about eight — and we will factor in all three." That score is **7.84**.

**Why this kills the variance:** because we take a weighted average, the next run won't jump from six to eight. "Once it is 7.84, it won't vary too much the next time. It will go to 7.4 or 7.9 — but it won't jump from six to eight." The problem with the naive setup is solved "by simply not taking the output and instead taking the **log probabilities**. This is the main innovation of G-Eval."

> 💡 **Expert commentary.** Probability weighting is powerful but has real edges. (1) **Multi-token scores**: on a 0–100 scale the score is two tokens ("7", "8"), so you must combine probabilities across decoding positions — one reason implementations stick to single-token 0–10 scales. (2) **Bimodal judges**: if the judge genuinely wavers between "this is a 2" and "this is a 9," the weighted mean lands near 5.5 — a score *no one* would have assigned. Weighting smooths variance; it does not make an uncertain judge certain. (3) **API availability**: extracting top-token log probabilities requires the provider to expose them (OpenAI's `top_logprobs` does; some providers don't), which is why you hand-roll G-Eval less often than you use a library that already handled it. (4) It reduces, but does not eliminate, run-to-run variance — temperature settings still matter.

---

## 9. Threshold, recap, and the paper's own example (37:13–42:26)

**From score to pass/fail.** Once you have the number (7.84), **divide it by 10** — you always want the output between 0 and 1 → **0.784**. Then apply a **threshold**, as with every metric so far: **0.7**. Above 0.7 → pass ("yes, this answer is correct"); below 0.7 → fail ("the answer is incorrect").

**The two innovations, restated as a revision:**

| # | Innovation | What it replaces | Effect |
|---|---|---|---|
| 1 | **CoT breakdown of criteria into evaluation steps** | One loose criterion line in the system prompt | Every subsequent API call has more clarity; less scope to overthink; **more deterministic behavior** |
| 2 | **Probability-weighted score from top-k log probabilities** | Taking the sampled token value (7, 8, 9) | Scores stay **stable across evaluation runs** |

Use LLM-as-a-judge normally versus using G-Eval, "and you will see that G-Eval mostly gives you better results. It's a better evaluation technique." And exactly this point is in the paper: the instructor shows the paper's own weighted-sum illustration — what probability was assigned to 1, how much to 2, how much to 3 — "if we used standard token usage, the output would be **3**. But due to the weighting, the output is **2.59**." The jumping is reduced.

**The full trace-back** (the instructor's own recap of the progression so far): the five metrics covered previously were all count-based → some metrics don't depend on counts, they depend on **judgment** → for those we need LLM-as-a-judge → but its biggest flaw is that scores vary significantly from run to run, for two reasons (a high-level criterion the LLM re-interprets each call; taking its printed word directly) → G-Eval solves both, by breaking the criteria into proper evaluation steps via CoT and by taking a weighted log-probability score instead of the token value.

And the one-line answer for interviews:

> "**G-Eval is a way to improve LLM-as-a-judge. That is the answer.** If someone asks you why G-Eval is special — is there anything particularly new? No, this is also just LLM-as-a-judge. But there are two core innovations… That's it, guys."

---

## 10. G-Eval in DeepEval (42:26–45:30)

"You could have done all this work manually as well. But the DeepEval library said that they are providing the G-Eval implementation for you." The demo code (imports first — "you have probably seen this part multiple times"):

- Create an **LLM test case** with `input`, `actual_output`, and `expected_output`.
- Until now the course used **built-in metrics** — recall, precision. **There is no built-in metric for correctness in DeepEval**, so G-Eval is used. Create a `GEval` object and provide:

| Parameter | Value in the demo | Role |
|---|---|---|
| `name` | `"correctness"` | Identifies the metric; passed to `evaluate` |
| `criteria` | The high-level criteria (step one) | Will be broken into steps automatically |
| `evaluation_params` | The input question, its answer, and its expected answer | Extracted from the test case and fed to the judge |
| `model` | GPT-4o mini (any other GPT-4 model works) | The judge |
| `threshold` | 0.7 | The final score is compared against it → pass/fail, true/false |

Then call `evaluate` with `metrics=[correctness]` — "that correctness is being picked up from here. That's it. This is the implementation. You don't have to do anything else."

**What DeepEval does automatically when the code runs:**

1. Breaks the criteria into **evaluation steps** (the CoT step).
2. Creates the prompt.
3. Sends it to the judge model.
4. Extracts the **log probabilities** of the top tokens.
5. **Normalizes** those probabilities.
6. Calculates the **weighted average**.
7. **Divides by 10** → a number → compares it with 0.7 → states true or false for the question — correct answer or not.

> 💡 **Expert commentary.** Two production notes on the library path. First, `strict_mode`: the instructor describes setting it `True` as skipping the weighted calculation ("if it says eight directly, then eight will be printed") — DeepEval's own docs frame strict mode as a stricter, more deterministic binary-style evaluation, so his practical rule stands: **keep it `False` to retain the soft weighted score**. Second, **cost**: the CoT step costs one extra LLM call per metric, but it is generated *once* and reused across all test cases — the scoring call is what scales with dataset size. Either way, pin the judge like any measurement instrument: fixed model version, temperature 0, and a versioned prompt hash — the judge-calibration rules from the [LLM-as-a-Judge note](../02-llm-as-a-judge.md).

---

## 11. The full flow, the two-tab thought experiment, and classroom Q&A (45:30–50:34)

For anyone still confused about *when* the weighted average is calculated, the instructor re-traces the whole flow: you have a **question**, the RAG chatbot's **generated answer** for it, and its **correct answer** (from the golden dataset). You create the criteria — "check if this answer is correct based on factuality, given the reference answer" — and give it to the LLM judge. The judge breaks the criteria into evaluation steps, then builds the judge prompt: look at this question, this answer, and this correct answer, and score whether the answer is correct based on these evaluation steps. This goes to GPT-4o, whose job at this point is **simply to generate a number**, because the prompt says "score it between 0 and 10" — it will output 8, or 9, or 10.

**The two-tab thought experiment.** If you took this entire prompt and pasted it into ChatGPT, it would give you a number — 8, 9, or 10, depending on how correct the answer is. Open **another tab** of ChatGPT, paste the **same prompt**, and it may print 9 or 10 instead of 8 — "because I am simply asking it to print an integer value… it could get confused between eight or nine from turn to turn." So G-Eval eliminates that entirely:

> "I am telling it: don't print the score for me. You tell me how much probability you assigned to each token when you were calculating internally. How much you assigned to eight, to nine, to ten. I am pulling those **top five tokens**, normalizing their probabilities, calculating their **weighted average**, and that weighted average becomes my output — for every question."

An LLM can print any word in the world at any point; it prints one particular word only because that word's probability was the highest. "So we are just going **one step back**: we are not asking it to generate, we are asking it to generate probabilities — log probabilities — and we are using those to get the output." (The instructor is honest that this is the hardest part to internalize: "I don't know if you'll understand this right now, because it's a bit about how transformers generate… auto-regressive behavior.")

**Student questions:**

| Student | Question | Answer |
|---|---|---|
| **Harry** | What if we want to evaluate an LLM response based on specific guidelines but we do **not** have the expected answer? | "It depends on what you want to measure." (Style, later this lecture, is exactly this reference-free case.) |
| **Jitender** | Do we use only these eval methods like DeepEval and G-Eval, or are there others too? | You can simply use LLM-as-a-judge directly — that will also work. "But what's the problem? The score will jump around a lot. Ran it once and got 85. Ran it a second time and got 95." |
| **Ankush** | Are there other metrics in G-Eval apart from correctness? | Absolutely — any somewhat judgment-based metrics: correctness, completeness, style, helpfulness, safety-related metrics. For all of these, use G-Eval. |

---

## 12. Correctness vs faithfulness — and the golden dataset (50:34–53:30)

The step-by-step build begins with correctness. What does *correct* mean? **Correct in the eyes of the world.** This forces a distinction the course has been circling:

| Concept | Definition |
|---|---|
| **Faithfulness** | The answer is **grounded in the context** — extracted from what the instructor (Nitish) taught in this course |
| **Correctness** | On a **Google level, world level**, the answer is factually correct |

Your RAG application's answer should be **both**. But four possibilities exist:

| | Factually correct (world) | Factually incorrect (world) |
|---|---|---|
| **Faithful** (grounded in context) | ✅ **The ideal** | The teacher taught something wrong, and the generator gave exactly that answer — faithful to bad context |
| **Not faithful** | The teacher taught something wrong, so the generator **answered from its own training knowledge** instead of the context — accidentally right | Didn't pick up the context, **hallucinated** something — and the hallucination is also wrong |

**The golden dataset.** First you need a golden dataset: questions on one side, correct answers on the other — correct *by the world*, not by what was taught in class. Who creates it? **A human expert with significant knowledge of the subject.** The instructor created one of **15 questions** and shares it: in the repo, under `goldens/`, each row has the **question**, the **ideal answer**, and a note on **which session** the discussion took place in.

---

## 13. Building the correctness eval — evaluation steps provided directly (53:30–01:01:47)

The build is quick: copy the golden dataset into the project's `goldens/` folder as a new file (`correct_n_s_goldens.json`), then create the eval file **`eval_application.py`** in `evals/` — "I have already written the code for it. I'll paste it first, then explain it to you… a very simple code":

| Code block | What it does |
|---|---|
| Imports | Libraries + the golden dataset just created |
| Judge setup | Judge model = **GPT-4o mini**; correctness **threshold = 0.7** — any score below fails |
| Load goldens | Opens the golden dataset |
| RAG pipeline | Creates the pipeline, because the question must be sent to it to generate the actual answer |
| Loop ×15 | For each of the 15 golden questions: send it to the RAG pipeline → get the generated (**actual**, not ideal) answer |
| Test case | `LLMTestCase` with **question, actual output, expected output** — "the exact same code we have been using until now" |
| Metric | A new `GEval` metric named `"correctness"` — **the new thing** |
| Evaluate | `evaluate(..., metrics=[correctness])` |

**The one deliberate difference:** instead of providing `criteria`, the code provides the **evaluation steps directly**. If you provide criteria, G-Eval generates evaluation steps internally; if you provide the evaluation steps themselves, **the CoT step is skipped**. So which is better? The instructor poses it to the class: should we generate and provide the evaluation steps ourselves, or provide a high-level criterion and let it generate? Providing them ourselves is better: every next judge call then receives **exactly the same steps**. If you send criteria instead, "some evaluation steps would be generated this time; in the next call, maybe some slightly different evaluation steps would be generated" — variation creeps back in through the steps themselves.

**When to use which:**

| Stage of your eval pipeline | What to send |
|---|---|
| Just starting — you don't yet know how the model is evaluating, which questions go wrong/right | Send **criteria**, trust the LLM to generate good evaluation steps — a testing phase for the eval process itself |
| After running it two–three times, once you see which questions fail and why | Send **your own evaluation steps** — "that is the best" |

The code also passes the evaluation parameters (question, generated answer, ideal answer), the threshold, and the judge model. One more flag: **`strict_mode = False`** — keep it that way. If you make it `True`, "the entire weighted calculation won't happen — if it says eight directly, then eight will be printed." Set to `False`, the full weighted calculation runs, which is what we want.

**First run.** Terminal: `python3 -m evals.eval_application`. The output: **correctness 66%** — out of 15, **8 questions passed, 7 failed**. For the failures you get complete details: question, actual output, expected output, and the reason — e.g., one question's weighted average came out to **0.58**, with the reason attached. (A candid aside: live debugging in class is difficult — the instructor had tested all of this offline before the class.)

---

## 14. Reading failure reasons and taking control of the rubric (01:01:47–01:10:54)

**Root cause analysis.** In the golden dataset, every question was answered **very thoroughly** — "as a human expert, I wanted to write the correct answer." Reading all seven failure reasons revealed a common theme: *the answer your RAG pipeline generated is not providing the complete answer that is in the golden dataset.* If the question is "What is an offline eval?", the golden dataset defines offline eval very well, and the generated answer covers only **70%** of it — the judge marks it incorrect purely because coverage is incomplete.

**Version 1 steps** (what the first run used):

1. Compare the actual output against the **key facts** in the expected output.
2. **Heavily penalize** statements in the actual output that contradict the expected output or are factually wrong.
3. **Reward** statements that match the expected output in meaning, regardless of wording.
4. Do **not** penalize the actual output for omitting information; only wrong statements count.

Even with step 4, omissions were still being penalized — "I figured this out by reading the reasons for the incorrect test cases." So the instructor created a second, revised metric (plus one new import — the rubric class):

**Version 2 steps + rubric:**

| Component | Text |
|---|---|
| Step 1 | Compare **only the factual claims** in the actual output against the expected output |
| Step 2 | A claim is wrong **only if it contradicts** the expected output or is factually false |
| Step 3 | A factually accurate answer **must score at least nine** even if it is shorter, less detailed, or covers fewer points than the expected output; do not deduct for brevity |
| Rubric 0–4 | The generated answer contains any clear **factual error** |
| Rubric 5–8 | **Mostly correct** with just a couple of minor inaccuracies |
| Rubric 9–10 | **All claims factually correct** |

Step 3 is the leniency lever: if an answer is correct without being that long — missing elaboration, fewer examples, some omitted points — don't penalize it. "I am making my evaluation criteria a little bit more lenient… telling it not to seek absolute perfection in the generated answer."

And the rubric is the control lever: "if you don't provide this scoring rubric yourself, G-Eval decides on its own how much to score an answer based on the evaluation steps… **I want to take control of that too.** If this happens, give this many points; if that happens, give that many points." Earlier he was only telling it *what aspects* to evaluate on; now he also tells it *how the scoring is decided*. General rule: once you understand your evaluation pipeline, **provide both the evaluation steps and the rubric** — your quality pipeline becomes more deterministic.

**Where did the fix come from?** The seven failed test cases were studied — the judge's stated reasons, all of them — and the common pattern spotted: the golden ideal answers are written really well, correct from every angle; the RAG chatbot's answers aren't of that quality — they miss a few points but are correct in themselves. Hence: stop seeking absolute perfection.

**Results.** Re-running: the score improved to **84%**. (It could be improved further — change the retriever slightly, change the generator — but that would digress; today is about *how correctness is evaluated*, not how the system is improved.) Run it again: **83%** — "it will hardly move by one or two points… The whole point of G-Eval is to make the evaluation process **more deterministic, less probabilistic**." This time **14 passed, 1 failed** — and the failing one was **test case 7, the same one that failed last time**. Same input, same failure — "this is very, very deterministic."

> 💡 **Expert commentary.** This debugging loop is **judge calibration in miniature** — exactly steps 2–3 of the protocol in the [LLM-as-a-Judge note](../02-llm-as-a-judge.md): read the disagreement reasons, fix the top cause (rubric wording), re-measure. One caution the lecture doesn't dwell on: the "don't penalize brevity" leniency was fitted to *this generator's current failure mode*. When you later improve the generator (as the completeness fix below does), a rubric this lenient may start passing genuinely thin answers — so re-check the judge whenever the system under test materially changes, and **version judge prompts like code** so every score in your reports is traceable to the exact steps/rubric that produced it.

---

## 15. Completeness — the second metric and the generator-prompt fix (01:10:54–01:17:15)

> "Let's quickly cover the next one: completeness, because we don't have to do anything new."

**The concept.** Same golden dataset — question, ideal answer, plus the generated answer. Suppose the ideal answer is made of **three points: A, B, and C**, but the generated answer only covered **A and B**. You call an LLM: "Look, this is the generated answer, this is the ideal answer — compare the two and tell me how complete the generated answer is compared to the ideal." The judge sees three pointers discussed there, only two here, and says: out of 0 to 10, **this is a 6.5**. Again, something an LLM judges — "you don't have to do anything. Just bring in another metric."

**The implementation trick:** define `completeness` right below `correctness` — name, its own evaluation steps ("again, I will give you the code — read through it at your leisure"), and its own rubric (0–4 / 5–8 / 9–10 bands) — and modify the `evaluate` call to take **two metrics**. "We did nothing. We defined one more metric in the existing code."

**First result.** Correctness ≈ **0.83** (as discussed) — but completeness is **0.68**, and the more concerning part: only **5 questions passed, 10 failed**. Not a good result.

**Root cause — in the system, not the judge this time.** Studying the failure reasons showed the generator in the RAG pipeline had been **instructed to provide very concise answers from the context** — its scope was deliberately limited ("don't say too much; only speak as much as you have been told"). In `src/`, the generator prompt is very restricted: quietly generate an answer from the context, nothing else.

**The fix — prompt engineering the generator:**

> "Answer thoroughly, identify every distinct part of the question and cover each one, and include all the relevant points the context provides for answering it. If the question has multiple parts or the concept has multiple components, address all of them rather than stopping at the first."

This repeatedly motivates the model to look at the question from every angle and answer all its parts — **without** telling it to invent things: it still must answer from the context. "I did a little bit of prompt engineering here… a simple fix. There are other types of fixes too — we will discuss those later."

**Result:** completeness jumps to **75%**, with **14 passed and only 1 failed** (versus 5 passed / 10 failed before). "When we fine-tuned and improved the generator prompt, our completeness score improved significantly and failed test cases dropped drastically. This is how you improve the scores."

---

## 16. Style — reference-free judging and the over-correction lesson (01:17:15–01:25:38)

**The last metric of the class:** does the RAG pipeline's generated answer follow the **CampusX style** — the brand style? Note what's different: **you don't even need an ideal answer here.** There is no ideal answer for style. You simply define a **rubric that very clearly describes what the CampusX style is like**, and the LLM judge reads that rubric plus the generated answer and scores how well they match.

Again: just add a third metric to the existing code — correctness and completeness parts unchanged. The style rubric explicitly encodes the brand voice:

| Rubric element | Text |
|---|---|
| Reward 1 | An **intuitive explanatory tone**, plain language, **the idea explained before any formula or jargon**, and technical terms briefly unpacked when used |
| Reward 2 | A **direct conversational register** that addresses the student as a CampusX lecturer would — rather than a dry, formal, or textbook tone |
| Reward 3 | The use of a **concrete example, analogy, or "why it matters" framing** |
| Score 9–10 | Clearly in the CampusX teaching voice — intuitive, conversational explanations before it formalizes |
| Score 5–8 | Reasonably clear, but somewhat flat, formal, or textbook-sounding |
| Score 0–4 | Completely dry, stiff, jargon-heavy, or robotic — does not read like a teaching explanation |

**First run — predictable failure.** Correctness ≈ **0.80**, completeness **75%**, style **54%** — "just as I said" it would score poorly, because the generator prompt never told the chatbot anything about the CampusX style.

**Fix 1 — the generator prompt** (replacing the existing one; the slide's formatting "somehow got messed up," but the lines are):

> "Write in flowing conversational prose, the way a teacher explains something out loud, not as a bulleted or numbered list. Only use a list when the question genuinely calls for enumeration. Explain the intuition first in plain language, and briefly unpack any technical terms you use."

**Fix 2 — correcting the over-corrected rubric.** The instructor noticed that wherever style test cases were failing, the judge's reason was that *the answer lacked analogies or examples*. He initially took that to heart — deciding every answer must contain analogies or examples — "which is not correct. Not every answer should contain analogies or examples. So this was kind of an **over-correction**." The countermeasure is one added rubric line:

> "An analogy or concrete example is a **bonus** when the concept is abstract, but a clear, direct, well-explained answer is fully acceptable."

**Two changes, one final run:** refined generator prompt + fixed evaluator rubric → **style ≈ 74%**, with **9 questions passing and 6 failing**.

**The prompt-engineering aside** (the instructor is pointed here): "Prompt engineering, which is a famous topic often dismissed by people saying it doesn't really matter — **it actually matters**. To improve these metrics, you have to tweak your system prompts, and with the right adjustments, you can actually see improvements in your evaluation scores… Do it yourself or have an LLM do it for you. But prompt engineering matters."

**Two closing judgments.** First, the trade-off: this metric could be pushed higher, but "if this metric starts to reach too high, other metrics will start taking a hit — faithfulness and such will start taking a hit. So 74 is good." Second, the threshold: you could also reduce it slightly — "0.7 is a bit harsh, it is too much. You can bring it down to 0.6."

> 💡 **Expert commentary.** That trade-off remark is Goodhart's law applied to eval suites: **optimize the generator for one metric and the others degrade** — verbosity for completeness strains faithfulness; conversational flourish for style strains precision. Treat the eval suite as a multi-objective problem: after *any* generator change, re-run **all** metrics together (which is exactly what the instructor's final runs report — correctness, completeness, style side by side). And treat threshold changes (0.7 → 0.6) as governance, not tuning: a threshold moved after seeing the score is a moved goalpost — document the decision and the date so reports stay comparable across runs.

---

## 17. Beyond the three metrics (01:25:38–01:26:52)

This is how you create an **application evaluation pipeline using G-Eval** — and these three are just examples. You can create many custom metrics — **helpfulness**, for instance. The instructor points to the **DeepEval G-Eval page**: "they have a very good page where they have explained G-Eval — it's exactly the same things we discussed in today's class. Here they have listed what other things we can measure, how it is calculated, examples:"

| Measurable with G-Eval | Status in this course |
|---|---|
| Correctness | ✅ Done today |
| Coherence | Can be measured |
| Style | ✅ Done today |
| Tonality | Can be measured |
| Safety-related metrics | Next class — **G-Eval will be used there as well** |

The method stays the same as seen today for every one of them. Closing the loop on the plan of action from the first slide: the **quality** part of the application-level eval suite is now complete. What remains is **safety** and **operations** — the next class.

---

## Key takeaways

1. **Two classes of metrics.** Recall, precision, faithfulness, answer relevance, context relevance are all **count-based** (decompose into claims → count in-favor vs against → ratio). Style, correctness, completeness, helpfulness, and safety metrics are **judgment-based** — they must be scored at the whole-answer level by a human or an LLM judge.
2. **The naive judge recipe** — golden dataset (question + world-correct answer) + one-line criteria + "give a score 0–10" + average over 15 questions — works in theory but has **very high variance** in practice.
3. **Two sources of that variance:** a loose one-line constitution re-interpreted differently on every independent call, and sampling a single integer token whose probabilities (e.g., 7 at 40%, 8 at 51%) flip between runs.
4. **G-Eval = LLM-as-a-judge + two innovations.** (1) CoT turns the high-level criteria into 4–5 **evaluation steps** — a rulebook/constitution; add a **scoring rubric** to control scoring too. (2) Replace the sampled token with a **probability-weighted score**: top-k token log probabilities → drop non-numeric tokens → normalize → weighted average.
5. **The math:** probabilities 0.70 / 0.20 / 0.05 for tokens 8 / 7 / 9 normalize to 0.7368 / 0.2105 / 0.0526 → score = 8×0.7368 + 7×0.2105 + 9×0.0526 ≈ **7.84** (argmax would say 8) → ÷10 = **0.784** → threshold **0.7** → pass/fail.
6. **G-Eval is nothing more than a way to improve LLM-as-a-judge** — the interview-ready one-liner. The paper (2023) recommends **GPT-4** as the judge.
7. **DeepEval usage:** `GEval(name, criteria or evaluation_steps, evaluation_params, model, threshold, strict_mode=False)` + `evaluate(metrics=[...])`. Keep `strict_mode=False` to retain the weighted calculation.
8. **Criteria vs steps:** start with criteria and trust the LLM; after two–three runs, when you understand your failures, **hand-write the evaluation steps and the rubric** — zero variation in what the judge sees across calls.
9. **Correctness ≠ faithfulness.** Faithful = grounded in course context; correct = true at world/Google level. Four combinations exist; the ideal answer is both.
10. **The debugging loop:** read the judge's failure reasons → fix either the judge (tighten/loosen steps + rubric, as in 66% → 84%) or the system (generator prompt, as in completeness 0.68 → 75%, style 54% → 74%) → re-run everything — determinism check: 84 → 83 on re-run, the *same* test case failing both times. **Prompt engineering matters** — system-prompt tweaks visibly move eval scores — but metrics trade off against each other (style ↑ can push faithfulness ↓), so re-run the whole suite after every change.

## Interview angles

- *"Why is LLM-as-a-judge unreliable, and how does G-Eval fix it?"* → Two variance sources (loose criteria re-interpreted per call; single-token sampling) and the two fixes (CoT-derived evaluation steps = a written constitution; probability-weighted score from top-k log probabilities). Close with the one-liner: G-Eval is LLM-as-a-judge made deterministic.
- *"Walk me through the weighted score with numbers."* → 0.70/0.20/0.05 over tokens 8/7/9 → normalize by 0.95 → weighted average 7.84 instead of argmax 8 → ÷10 → 0.784 vs threshold 0.7.
- *"When would you send criteria vs hand-written evaluation steps to the judge?"* → Early: criteria (a testing phase for the eval itself). Once failure patterns are understood: your own steps + rubric — the judge then sees identical instructions on every call.
- *"What's the difference between correctness and faithfulness in a RAG app?"* → Grounded-in-context vs true-at-world-level, plus the four-quadrant table and which failure each quadrant implies (bad retrieval, bad source content, hallucination).
- *"Your G-Eval correctness score was 66% — what do you do?"* → Read the judge's reasons for each failure; identify the common pattern (e.g., penalizing omitted coverage); decide whether the *judge* is wrong (fix steps/rubric) or the *system* is wrong (fix the generator prompt); re-run and confirm stability.
- *"Can you use G-Eval without an expected answer?"* → Yes — reference-free judgment (the style metric): no ideal answer, just a rubric the judge scores the output against. It depends on what you want to measure.

## Cross-links

- **Previous:** [14 — Evaluating RAG: Generator & Full Pipeline with the RAG Triad](14-rag-triad-generator-pipeline.md) (the pipeline-level metrics whose count-based pattern this lecture transcends)
- **Next:** [16 — Securing Your RAG Application: Toxicity, Leakage & Scope Drift](16-rag-security-toxicity-leakage-scope-drift.md) (the safety eval suite — also built with G-Eval)
- **Parent note:** [Section 105 note 2 — LLM-as-a-Judge](../02-llm-as-a-judge.md) (judge biases, calibration protocol, rubric design — the research-grade version of this lecture's debugging loop)
- **The count-based metrics being contrasted:** [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) (recall/precision) and [14 — RAG Triad](14-rag-triad-generator-pipeline.md) (faithfulness/answer relevance)
- **Where the eval suite goes next:** [18 — RAG Regression Testing](18-rag-regression-testing.md) and [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md)
- **Course hub:** [README.md](README.md)
