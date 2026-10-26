# 11 — Selecting the Right LLM: Running Custom Model Evals

> **Lecture 11 of 19** · Unit 2: Model Evaluation & Benchmarks · 1:56:53
> Selecting the Right LLM for Your AI App: Running Custom Model Evals (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/11-model-selection-custom-evals.md)

---

## What this lecture covers

The theory is done. From this session to the end of the course, everything is **hands-on** — and the instructor argues the practicals will land precisely *because* the theory was built first. This lecture is the capstone of Unit 2: the complete, real-world process of **picking the LLM that will power a new product feature**, carried by a single case study.

The vehicle: you are an AI engineer at **ESPN Cricinfo**, asked to build **Ask Cricinfo** — a Text-to-SQL feature that turns cricket fans' English questions into SQL queries. The lecture walks the full three-stage journey:

1. **Stage 1 — Write down requirements**: the task, a ₹3-lakh/month cost ceiling (derived with a full token-by-token cost model, including a detour into **prompt caching**), a 2–3-second latency target, context-window and deployment decisions, and an absolute accuracy requirement.
2. **Stage 2 — Shortlist 5–10 candidates from leaderboards**: why the Text-to-SQL leaderboards get rejected, how a coding leaderboard is used as a **proxy**, how a **blended price** works, and how 146 models get filtered (cost), normalized, and weighted (9:1) down to a top 10 — then cut to five live candidates.
3. **Stage 3 — Run the custom model eval**: build a golden dataset of 20 hard questions, write an execution-based evaluator, orchestrate the run over five models via OpenRouter, watch the live results (Grok 90%, Sonnet 85%, GPT-5.6 Tera 80%, MiniMax 65%, Kimi K3 55%), and make the final Grok-vs-Sonnet decision.

If you keep one mental model from this lecture: **leaderboards filter; your own eval decides.**

---

## 1. From theory to practice — recap and agenda (00:00–02:22)

The lecture opens with a quick recap of the course so far. At the very beginning of the course, we established that LLM evaluations are of two types — **model evaluation** and **application evaluation** — and that the course would focus on application evaluation, but study a bit of model evaluation first. Within model evaluation, there are again two types:

| Type | What it does | Uses |
|---|---|---|
| **Benchmark evaluation** | Tests specific capabilities of LLMs — knowledge, reasoning, math — using **generic, ready-made datasets** | Lectures 7–10 |
| **Custom model evaluation** | Runs the LLM **with your own data and your own application** to learn which model is best *for you* | **This lecture** |

The motivating question: suppose you're building a chatbot for your company and you need a brain — an LLM. Benchmarks might point you to the top four or five models in the market, but *among those*, which one is best **for your application**? That answer comes only from a custom model evaluation. Today's agenda, in the instructor's words: **how to run custom model evals** — no more theory, everything shown practically, through a case study chosen after going through many problem statements.

---

## 2. The case study: Ask Cricinfo (02:22–10:16)

### The problem at scale

The instructor asks who follows cricket — "this class is taking place in India," so plenty of hands. If you follow cricket, you know **ESPN Cricinfo**, one of the top websites for live cricket scores ("I personally use it too, I've been using it for years"). During a live match, people send questions and commentary to the feed — at massive scale, **literally 500 questions in 5 minutes** during something like an India–Pakistan match. Questions like:

- "Tell me Virat Kohli's batting average against Pakistan."
- "The last time India–Pakistan played, how many wickets did Jasprit Bumrah take?"

Cricinfo has a **commentary team**, and alongside them sit **analysts/experts** with access to Cricinfo's database. The commentary team hands them questions; the analysts write **on-the-spot queries**, hand the answers back, and the feed is updated — all happening live. Cricinfo has done this for years, but eventually realized it doesn't scale: on big-match days the volume is simply too high to answer everyone.

### The feature

So Cricinfo built **Ask Cricinfo**: during a match they share a link where any cricket fan can ask any cricket question. You pick a topic (say **IPL**), type something like *"who has scored the most runs against Bumrah?"* — and the live demo, to the instructor's mock embarrassment, refuses to cooperate ("Something is happening. I don't know… it's not my fault. You can go check it after class ends").

What's happening under the hood is the architecture for the whole lecture:

1. Your **English question** goes to the backend.
2. An **LLM** receives the question **plus the database schema** — it knows how the database is structured, what columns exist.
3. The LLM **generates an SQL query**.
4. Your system **runs that query on the database** and shows the result on screen.

The analysts' job is now done by the system, and the whole thing scales to any number of queries.

### Our assignment

Now the role-play: **we are the engineers at Cricinfo**, we've received the feature request, and before building it, the biggest question is — **which LLM will we use?** The LLM is the brain doing the main work. And here the instructor is emphatic about professional norms:

> "You can't just randomly tell your team, 'Come on, let's use a model. This is the best model right now.' You can't talk like that in companies. You have to provide proper reasoning and inputs as to why you are choosing a particular model."

So: **proper evaluation before model selection**. In technical terms, we're building a **Text-to-SQL application** — and one clarification matters. This is **not a RAG chatbot**: we're not giving the model external documents to answer from. We only provide the **database schema, which stays the same every time**. Today's goal is not to build the system — it is to **select the best model that will be the brain of this system**.

---

## 3. The three-stage selection flow (10:16–12:54)

The model-selection journey does **not** start by running a custom evaluation directly. It's a three-stage process (and stage 2 reuses the previous lecture's lesson):

| Stage | What you do | Output |
|---|---|---|
| **1. Requirements** | The AI engineering team writes down its requirements very clearly | A requirement sheet (cost, latency, context, deployment, accuracy) |
| **2. Leaderboard shortlist** | Take those requirements to the LLM leaderboards and **shortlist 5–10 candidate models** | A candidate list |
| **3. Custom model eval** | Run your own evaluation on those candidates with **your own data** | The winning model |

The instructor explicitly re-quotes lecture 10's golden line here: **the job of LLM leaderboards is to filter, not to select**. The leaderboards tell you which candidate models exist and are worth considering; the custom eval tells you which one is actually best for your application.

---

## 4. Stage 1, part 1 — the task and the cost ceiling (12:54–16:52)

The requirements gathering is run as a live Q&A. First question: **what is the task, at a technical level?** We already know it — a **Text-to-SQL application**.

Second question — one you should actually ask your **product manager or engineering manager**: **what is the cost ceiling?** How much can we spend running this application? Before settling a number, the instructor forces a business-analysis detour: *why* does Cricinfo answer user questions at all?

> "The real reason behind this is… how much money you can spend behind this. It's a **retention play**. What is the **North Star metric** of any website in the world? That users stay on the website for as long as possible."

The logic chain: the more time you spend on the site → the more ads you see → the more revenue. "You ask us questions, we'll answer" is a retention strategy, and this feature is helping increase revenue. With that framing, the viewers guess budgets ("2 lakh, 5 lakh?" — the instructor averages the crowd, calling it the **wisdom of the crowd**), and the scene is set: the business manager says, *"brother, if it stays below 3 lakh, everything fine. Don't cross 3 lakh."*

**The budget: ₹3 lakh per month.**

One important point the instructor stamps on: **figuring out what your cost will be is your job as an engineer** — nobody hands you this number per model. So how does a Text-to-SQL system spend money? The biggest expense is the **LLM's per-token charge** (assume a paid API like OpenAI or Anthropic). Deployment costs are ignored — the website already runs; we're integrating a feature into it.

> 💡 **Expert commentary.** This is **eval-driven procurement** in miniature: the business gives a constraint (₹3 lakh/month), and engineering converts it into a model-selection criterion. Mature teams go one step further and compute a **cost-quality frontier** — the accuracy (or task win-rate) each candidate delivers *per rupee* — because the real question is never "which model is best?" but "which model is best *at this spend level*?" Notice also that the instructor derived the budget from a **business metric** (retention → ad revenue): tying your eval budget to the revenue the feature protects is the single best way to get leadership to fund evaluation work.

---

## 5. Stage 1, part 2 — modeling the cost of a Text-to-SQL call (16:52–30:44)

### The prompt

You don't send the raw question to the LLM. You build a **prompt** — and the instructor shows the actual system prompt he wrote:

- **Role/task:** "You are a text-to-SQL generator."
- **The database schema** is provided (only then does the model know which SQL query to write).
- **Instruction:** return an SQL query that uses **SQLite syntax** (today's class database is SQLite; PostgreSQL or MySQL would work too), and **return only the SQL query** — "I don't need any other explanation… You just give me the SQL query. I'll run it in the database."
- **The user's question** at the bottom.

The schema in the demo has **two tables** (the domain is deliberately narrowed to **IPL** only — cricket also has international T20, Tests, separate women's/men's formats, so scope is kept small):

| Table | Contents |
|---|---|
| **`matches`** | One row per IPL match: which two teams played, where, on what date, who umpired |
| **`deliveries`** | **Ball-by-ball data** for each match — a T20 has 240 balls (40 overs across both innings): batsman, bowler, six, four, dismissal, who took the wicket |

The demo question he feeds in is deliberately nasty: *"Which bowler has the best economy rate among those who have bowled at least 500 legal balls?"* — "a very complex question" — and the LLM returns a working SQL query.

### The four numbers of the cost model

| Parameter | Value | How it was derived |
|---|---|---|
| **Input tokens per request** | **400** | He pasted the full prompt into a token-counting website: **352 tokens** — "let's make it simple… take 400." (System prompt + schema are constant; only the question varies, and not by much.) |
| **Output tokens per request** | **100** | The generated SQL is ~100 tokens; queries differ in length, so take the average |
| **Requests per day** | **50,000** | His cricket-informed estimate — "spiky": demand spikes on big match days (a CSK vs MI match will definitely spike it); he first muses ~5,000/day, then fixes **50,000** for the class arithmetic |
| **USD → INR** | **×95** | "The magic number" — provider rates are in dollars |

A detail everyone is expected to know: providers charge **separately for input tokens and output tokens**, and **output tokens are more expensive** than input.

### The Haiku calculation — and the fall

A viewer (the "new intern") suggests **Claude Haiku** — "it's a great model." Its pricing: **$10 per million input tokens, $50 per million output tokens**. The per-query cost:

> ($10 × 400 / 1M) + ($50 × 100 / 1M) = 4/1000 + 5/1000 = **$0.009 per query**

He does the arithmetic live (and catches his own slip — "9×5 is 45… 450 USD is correct"):

| Step | Computation | Result |
|---|---|---|
| Cost per query | 400 in @ $10/M + 100 out @ $50/M | $0.009 |
| Per day | $0.009 × 50,000 questions | **$450/day** |
| Per month | $450 × 30 | **$13,500** |
| In rupees | $13,500 × 95 | **₹12.82 lakh/month** |

> "Now you tell us — can we use Haiku? Our budget was 3 lakhs. 12 lakhs means it's becoming **4 times more**. So it's clearly understood that this is a model outside our budget. **We need to go down**."

Down means roughly to a **quarter** of that bill — somewhere around **Claude Sonnet 3.5** on the pricing page he's reading ("it operates at 1… I think Sonnet will come within our budget"). The cost discussion closes with the budget locked: we need a model that keeps us **within ₹3 lakh/month**.

---

## 6. Stage 1, part 3 — prompt caching, the hidden lever (30:44–38:47)

While reading the pricing page, the instructor notices rows he decides not to skip: **5-minute cache writes, 1-hour cache writes, cache hits and refreshes**. "Has anyone heard this term — **prompt caching**?"

### The concept

Many parts of your prompt **stay the same across queries**. The system prompt and the schema are identical for all 50,000 daily questions — only the question at the bottom changes. But you're paying the model full input price **every time** for the same repetitive text. Providers therefore offer caching: **cache part of your prompt on their server**, and subsequent requests stop paying for it.

### The pricing (Haiku's page)

| Event | Price (per 1M tokens) | vs regular input ($10) |
|---|---|---|
| Regular input | $10 | — |
| **5-minute cache write** | **$12.50** | More expensive — "you are not just providing input, you are also doing caching processing" |
| **Cache hit (read)** | **$1** | 10× cheaper |
| **1-hour cache write** | **$20** | For slower-traffic apps |

So the **first** query of the day pays $12.50 (write), and every query after that pays only **$1** for the cached prefix. The **refresh cycle** matters: if the next question arrives after 7 minutes, the entry has been evicted and you pay the $12.50 write price again; if it arrives within 3 minutes, you pay just $1.

- **Cricinfo's case (50,000 questions/day):** the 5-minute cycle is ideal — within every 5 minutes some question will always arrive. Even if no query comes between 2 AM and 6 AM, no problem: the first query after the gap pays the write price ($12.50) again, and it's back to $1 hits.
- **A quieter app (~1,000 questions/day):** choose the **1-hour cache** — pay $20 to write, and every question within that hour costs $1.

The savings are dramatic: his back-of-envelope says a bill of roughly **₹12.8 lakh can come down to about ₹6.7 lakh** — "with the help of this optimization, you can actually save a lot of money."

### KV cache, and when caching does *not* help

If you wonder how this works internally — "I can't teach you, but I can guide you": the whole thing runs on **KV caching**, tied to the **attention mechanism** — the **K and V vectors** in attention are what get cached, and that's why this optimization exists. It's a future topic in his larger curriculum.

The caveat: **RAG chatbots get little benefit** — a large part of a RAG prompt is *context*, and context changes with every query. Here, in Text-to-SQL, the static prefix (system prompt + schema) dominates, so caching pays off handsomely. A viewer (Srinivas) asks: *how will the LLM understand what's in the tables beyond column names?* Answer: if your database is private or domain-specific, **add a paragraph describing each column** to the system prompt — yes, it gets bigger and costs more, "but again, using prompt caching, that problem can also be solved."

> 💡 **Expert commentary.** The multipliers in the lecture's fictional price table mirror real provider mechanics: Anthropic's published prompt-caching pricing is **1.25× the base input price for a 5-minute write, 2× for a 1-hour write, and 0.1× for a cache read** — exactly the $12.50 / $20 / $1 structure shown here. Under the hood it is literally the **KV cache**: during prefill, attention computes key/value tensors for every prefix token; caching them on the provider's servers means subsequent requests skip re-computing the prefix and only pay a cheap lookup. Note also that cache matching is **token-level and prefix-anchored** — the static part must come *first* in the prompt (schema before question), which the instructor's prompt already does. Even RAG apps can benefit by caching the fully static prefix (system prompt + tool definitions) and leaving only the retrieved context uncached.

---

## 7. Stage 1, part 4 — latency, context, deployment, accuracy (38:47–44:47)

The remaining requirement questions, each answered with live-audience reasoning:

| Requirement | Decision | The instructor's reasoning |
|---|---|---|
| **Latency** | **2–3 seconds**, hard ceiling | Live-match curiosity Q&A needs speed. Viewers suggested 5 s — "even 5 seconds feels like a lot to me… if it's more than three seconds, our OCD gets triggered that something's not happening, there's some glitch." Crucially: **no reasoning models** — a model that reasons at length before answering is disqualified here. (Contrast: a **research assistant** that searches the internet and returns a report — latency is not a big issue there.) |
| **Context window** | **Not important** | "Here context is not much of a consideration" — the user asks one question; the next question is unrelated; **no multi-turn conversation, no user session**. If you were building a chatbot or a coding assistant, context *would* matter. We can even pick a model with a small context window. |
| **Deployment** | **Public APIs preferred, no privacy constraint** | "There is no such issue here" — no data that must stay on our servers, so Anthropic/OpenAI APIs are all fine. And the preference is *for* public APIs: their **infrastructure and reliability are much better**. Self-hosting needs a large technical team and still won't be very reliable. |
| **Accuracy** | **Absolutely critical** | Cricket fans "are very finicky about records." Ask for IPL's top run-scorer and get "Yashasvi Bumrah" by mistake, and "immediately screenshots will be posted everywhere on Instagram, Twitter, and ESPN Cricinfo will be greatly insulted." You cannot hallucinate. |

How do you *verify* the accuracy requirement? Two ways: (1) check the **leaderboards** for coding capability — "creating SQL is like a coding task"; (2) find out how good the model is **on your data and your tasks** via your own custom evaluations. With that, the requirements sheet is complete — and the instructor's closing point for the stage: with requirements in hand, "you definitely shouldn't do something like go and see the first model and immediately say, 'Yes, this is it.'" You're now mentally prepared to read the leaderboards with intent.

---

## 8. Stage 2, part 1 — finding a leaderboard you can trust (44:47–49:12)

Stage 1 done. Stage 2: **shortlist 5–10 potential models from the leaderboards.** First question — *which* leaderboard? It would be best if a **Text-to-SQL leaderboard** existed; you'd take its suggestions directly and run custom evals on those. And they do exist — search "Text-to-SQL leaderboards" and you'll find two or three:

| Leaderboard | Why the instructor rejected it |
|---|---|
| **BIRD** (Bird SQL) | **Not updated** — old models, plus **fine-tuned models** in the rankings (there's no "SQL-specific" foundation model, so entries are likely models fine-tuned on SQL data — useless for a "which foundation model?" decision). Also rankings that look like **complete harnesses, not models** — an entry like "J Loop Sentinel Agent V2 Pro" is some company's full system, "I don't know what model this is." And a personal grievance, half-joking: the naming — "they took B from BIG and the middle R from Large and made *Bird*. So I got very angry about this. That's why I rejected it." |
| **Spider** (Text-to-SQL) | Same staleness problem |
| **LiveSQL Bench** | Has a leaderboard, but **not updated** — Claude 3.5 is the most recent model listed, GPT-4.0-era, while next-generation models have shipped — and, critically, "I don't fully know **what data** they used for this entire benchmarking." |

> "In short, I couldn't trust these Text-to-SQL leaderboards."

The alternative: use the **coding leaderboard** instead — because **generating SQL is a type of coding activity**. Coding capability becomes a **proxy** for SQL-generation capability: how good a model is at SQL will be inferred from how good it is at coding in general.

> 💡 **Expert commentary.** This is a textbook **proxy-metric** decision, and it deserves scrutiny. BIRD and Spider *are* the canonical Text-to-SQL benchmarks in the research literature, and the instructor's complaints are the exact reasons niche leaderboards lose value in practice: **stale rankings, fine-tuned leaderboard-chasing entries, and opaque harnesses** (lecture 8's "harness is part of the measurement" problem). The proxy move inherits a known risk — SQL generation is a narrow, schema-grounded, dialect-sensitive sub-skill, and a model can be a great general coder yet a mediocre SQL writer on *your* schema. That's precisely why the proxy is only used to *shortlist*: the final arbitration happens in stage 3, on your own data.

---

## 9. Stage 2, part 2 — LLMstats and the blended price (49:12–55:28)

The leaderboard he found and liked most: **LLMstats.com** — a third-party site that **collects data from various leaderboards** and computes an overall rating from its own analysis. Its **"Best AI for Coding"** section is completely updated — the most recent models (Gemini 3.5 and friends) are rated, with cost, speed, and context-window columns — and it **aggregates almost all coding benchmarks** into one rating. At the top of the board: **GPT-4.5**, then Gemini 3, Mixtral 3.5, Llama 2.0 ("you must have heard the news a few days ago… it created a huge stir"), Kimi 3, Claude Opus 4.8, and o1 — **146 models in total**.

### Reading a blended price

One confusing detail he pauses on: the leaderboard shows **one** price number per model, not separate input/output rates. Hovering reveals the definition: **"blended price per million tokens, 4:1 input-output ratio."** The worked example, using **Fable 5** (input $10, output $50):

> Blended = (4 × $10 + 1 × $50) / 5 = (40 + 50) / 5 = **$18 per million tokens**

Two lessons:

1. **Always check the blend ratio** — different leaderboards use 4:1, 8:1, different conventions.
2. A lucky coincidence for this application: our prompt is **400 input : 100 output — exactly 4:1**. "Right now I'm very happy that we don't need to do any more calculation. This blended number is exactly for our situation." So the monthly cost for any model is one formula:

> **Monthly cost = (400 + 100) tokens × blended price / 1M × 50,000 questions × 30 days × 95 ₹/$**

---

## 10. Stage 2, part 3 — filtering 146 models down to a top 10 (55:28–01:03:28)

### Step 1: the cost filter

He **downloaded the data for all 146 models** and computed the monthly cost for each with the formula above — e.g., **Claude 2 came to ~₹1.2 lakh**, other (pricier) models to ₹8 lakh and beyond. Then he **rejected every model above the budget**, leaving "about 50–60 models" survivors (the expensive ones gone).

One honesty note he volunteers: the numbers on screen come from his **pre-class exercise, which used a ₹5-lakh budget** — the live discussion revised the ceiling to ₹3 lakh, "so the models you're seeing here, you will see some models around 4 lakh."

### Step 2: normalize, then weight

Among the survivors, he needs a single ranking number from two criteria — **coding capability** and **latency/throughput** (characters printed per second). The method is straight out of ML class:

1. **Min-max normalize** the rating column: (value − min) / (max − min) — e.g., **GPT-4.1 nano** has the lowest rating, **−1.1**, so a model rated 50 becomes (50 − (−1.1)) / (max − min). After normalizing, every model's rating sits **between 0 and 1** (GPT-5.6, the highest-rated, gets exactly 1).
2. **Normalize the speed column** the same way (throughput in characters/second — one model gives 17 chars/s, "very low," another 63).
3. **Combine with weights:** score = **9 × normalized rating + 1 × normalized throughput**.

### Why 90/10 and not 50/50?

Because the output is just **a single ~100-token SQL query**:

> "Even if a model is a bit slow, it won't take too long to print a single query… If my output was a large essay, then latency would be much more important… a model giving three-four characters per second would take a long time to print the entire response. But since I only need to print a query, even a slow model will give me good results within a reasonable time — 1 or 1.5 seconds… some very slow models might take 2–4 seconds."

And it's explicitly a judgment call: "This is my personal opinion. You can change it… a 98:2 split, a 75:25 split." Sort by the weighted score, and you get the **top 10**.

### What the top 10 revealed

The #1 model: **GPT-5.6 Tera**. But two things happen on the list:

- **Miu Spark 1.1** (Facebook/Meta) is removed — it's **only usable in the US**, so it's out.
- An observation about the market: the paid models (GPT, Claude) are expensive, but **open-source models are very cheap and not that far behind** — if GPT-5.6 Tera gives you the top latency-plus-coding package, **Mixtral M3 gives you a 76** (on the same overall scale) **at a fraction of the cost**. "Not that far behind… it still needs to be tested which model works better in your application." **Qwen** and **GLM** keep getting cheaper; GPT-class models trend expensive; **Sonnet sits somewhere in the middle**.

---

## 11. The five live candidates (01:03:28–01:07:49)

The remaining models now go into the **custom model eval**. Since this is a live class, he tests **five** (you can test all ten — or "the remaining nine," since Miu Spark isn't available; the method is just "create a list, add the model name"):

| # | Candidate | Why it made the live test |
|---|---|---|
| 1 | **GPT-5.6 Tera** (OpenAI) | "A top contender. It might be a bit expensive, but it's the best contender." |
| 2 | **Kimi K3** (Moonshot AI) | "I personally want to test it — I have heard a lot of praise for it in the last one week." |
| 3 | **Grok** (xAI) | "We will definitely do Grok, because you never know what Elon Musk will do." |
| 4 | **Claude Sonnet** (Anthropic) | "From the Anthropic family, that's the only one available here." |
| 5 | One of **GLM / Qwen / MiniMax** | "Because all three are Chinese models… at very low cost it can bring us results." (He lands on MiniMax.) |

Deliberately skipped: **GPT-5.6 Luna** ("we are doing Tera… there is a good chance Tera will perform better than Luna, because both are coming from the same company") and **Gemini 3.6 Flash**.

Before moving on, the instructor pauses on the theory-first question — did the practical session land better *because* ten lectures of theory came first? His honest answer, from years of teaching: "I know many people will leave after the first, second, or third session. But those who stay, from the seventh or eighth session onwards, will start to extract a lot." And he previews the question the eval will answer:

> "Does GPT-5.6 actually prove its worth for its price, or should we use MiniMax M3 because it's close enough? … This varies by application. If it's a very sensitive application, like a **medical application** where you can't make a mistake, you will pay extra to be correct. But if it's a **consumer-focused application** where a small mistake isn't a big problem, you will probably choose a slightly less powerful model to save costs."

---

## 12. Stage 3, part 1 — designing the custom eval (01:07:49–01:18:29)

The last and most important part: five candidates, choose one. **Run them on your dataset and see how they perform on your task.** The full flow needs two assets:

### Asset 1: The database

Cricinfo already has the data; the instructor brought his copy **from Kaggle** — the complete IPL dataset, **2008 to 2024**.

### Asset 2: The golden dataset

A dataset of **at least 30–50 questions**, where each row pairs a question with its **correct SQL query, written by a data analyst** who runs it against the database and verifies it actually answers the question. Example rows:

| Question | Golden query |
|---|---|
| "How many sixes did Virat Kohli hit in the IPL from 2018 to 2022?" | *(analyst-written, verified SQL)* |
| "Which player played the most matches on the field from 2012 to 2016?" | *(analyst-written, verified SQL)* |

**Representativeness is the make-or-break property.** Cover the question types your users will actually ask — highest run-scorers, highest wicket-takers, player statistics, match outcomes, team performance over the years. "If your golden dataset only has questions about highest run-scorers, and you test your model and it performs 95% accuracy on that, but when a user asks about wicket-takers it gives wrong answers — your evaluation is not complete." Design guidance:

- **Difficulty mix** (for a 50-question set): **10 easy + 20 medium + 20 difficult**.
- **Topic diversity**: five questions on **joins**, five on **sub-queries and window functions** — "try to include every possible topic."
- **Creation**: mostly manual; if an LLM helps generate it, verify the topics are absolutely correct.

### The evaluation loop

Take each candidate model **one at a time** (testing GPT-5.6 Tera first, say). For each question: send it to the model → the model generates SQL → **run both queries** (the generated one and the golden one) on the database → **compare the two result sets**.

The critical design decision — **how do you judge the generated query?** Can you do **string matching**, comparing the generated SQL character-by-character with the golden SQL? **No:**

> "For a single result, multiple queries can be written… the query written by your data analyst and the query generated by your LLM for solving the same problem might be different textually."

So compare **result tables**: run both queries, get table 1 and table 2, and check whether the two tables are the same. Same tables → correct query. Repeat across all 50 questions → count correct → **accuracy**. (Other metrics exist — precision, recall, F1, especially for classification tasks — but for factual questions, "accuracy is a good starting point.")

### Accuracy is the headline, not the verdict

Suppose the run gives Model A 95%, Model B 92%, Model C 90%, Model D 88%, Model E 85%. Model A wins on accuracy — but that's not the whole story: Model A might also be the **slowest** and the **most expensive**; Model B might be 3% less accurate but **50% faster and 30% cheaper**. The principle the instructor names is **fitness for purpose**: the best model is the one that best meets *your application's* requirements, not the one with the highest accuracy in isolation. Two further corollaries he draws:

- **Evaluation is not one-time.** The model landscape changes constantly — new releases, improved models. "What's the best model today might not be the best model six months from now."
- **Design for swappability.** Build the system modularly, on standard APIs, so switching models later is cheap.

### How big should the golden dataset be?

A viewer asks: 100 questions — is there a limit? No limit, but two costs grow with size:

1. **Golden datasets are usually created by humans** — labeling takes time, effort, and money.
2. **Every question is an LLM call per model.** Five models × 50 questions = **250 calls**; at 500 questions it's **2,500 calls** — "in your evaluation too, you are spending money."

His guidance: **50–500 questions**, and in production the set keeps growing — when you deploy, keep adding the new questions **where your model is failing** back into the golden dataset. For today's classroom run: **20 questions, all very difficult** — deliberately hard to separate the models ("I had to show you which model is performing well and which one poorly"). A question about doing this with frameworks like **DeepEval** (from viewer Tushar) is explicitly deferred: "This is not the topic of today's discussion… when we study it later, the frameworks will definitely give you a lot of benefits."

---

## 13. Stage 3, part 2 — the build: twelve steps of code (01:18:29–01:40:35)

The instructor shows a written step list and walks it file by file ("I've written most of the code, but at the end I'll run it and show you"). By the golden-dataset step, "out of 12 steps, 6 are completed."

| # | Step | File / artifact | What happens |
|---|---|---|---|
| 1 | **Get the dataset** | `data/deliveries.csv`, `data/matches.csv` | Downloaded from Kaggle; trimmed from 2008–2024 down to **2020–2024** to keep the live eval fast |
| 2 | **Load into a database** | `db.py` | Reads the two CSVs, keeps the four years, stores them into a **SQLite** database created on the fly — the two tables (`deliveries`, `matches`) now accept SQL |
| 3 | **Extract the schema** | `schema_extractor.py` → `schema.sql` | Generates the schema (tables, columns, types) into one file — because this must go **into the system prompt**, sent to the LLM every time, so extract it once beforehand |
| 4 | **Create the golden dataset** | `golden_data_set_generator.py` | 20 hard questions; each dictionary = question + query + difficulty label (e.g., *"Tell the average runs per match as a number"*). Ideally done manually; he had an **LLM** generate a difficult set — "this is not the correct method," but it differentiates the models |
| 5 | **Validate the golden queries** | (same file, run) | Runs all 20 queries: **20/20 passed** — checking for **SQL errors only** ("are the queries at least correctly formed?"), not answer correctness |
| 6 | **Export the golden CSV** | `make_golden_data_set.py` → `golden_hard.csv` | 20 rows: question, golden query, **expected row count** (e.g., 1), and an **order-sensitive flag** (whether the query relies on `LIMIT` / `ORDER BY` asc/desc — "why this clause matters, we'll discuss in a moment") |
| 7 | **Flow test** | `first_test.py` | One question through the whole pipeline via **ChatOpenRouter** using **GPT-4o** — explicitly *not* a candidate, just a smoke test: question in → SQL out, "nothing else is visible" → the flow works. ("It's okay if you don't do this.") |
| 8 | **Pick candidate models** | `model_openrouter_slug.py` | A list of **five tuples**: model name + its **OpenRouter slug** (searched per model on OpenRouter — "if I had to do ten, I would have searched for ten"). "A kind of model database." |
| 9 | **Build the evaluator** | `evaluator.py` | The comparison rule — see below |
| 10 | **Orchestrate** | `main.py` | Loads schema + golden dataset + DB connection; loops per model: call model → get SQL → execute → evaluate → **log scores**. Depends on `schema.sql`, the golden dataset, `model_openrouter_slug`, and `evaluator.py` |
| 11 | **Run the eval** | `python3 main.py` | All five models × 20 questions, live |
| 12 | **Analyze and decide** | (results) | Section 14 |

**Why OpenRouter (step 7–8):** the five candidates come from five different providers — OpenAI, Anthropic, xAI, and two Chinese labs — each with different APIs. "Is there any place where we can get all models in one place?" A viewer (Saurav) answers it: **OpenRouter** — any model's API (Kimi K3, Tera, Sonnet, all available), with **direct LangChain integration** ("just like ChatOpenAI, you use ChatOpenRouter"). It even offers **free credits** — enough to test one or two models; the instructor's own full run cost **about $5 (₹500)**.

**The evaluator's comparison logic (step 9)** — given the golden dataframe (golden query's result) and the generated dataframe (generated query's result):

1. **Row count check.** If the row counts differ, the tables can't be equal — "you search for the top five batsmen, in one you see five rows, in the other three rows — obviously the query with three rows is wrong." If unequal, "the matter ends there."
2. **Value normalization** (not the min-max kind): `2.0` vs `2` (decimal vs integer) must count as the same, and `2.999` vs `2.99` too — otherwise correct queries would be marked wrong.
3. **Row-as-tuple + sort, then compare.** Write each table's rows as tuples in a list, **sort both**, then compare — because reordering can legitimately happen (a value at row 1 in one table, row 2 in the other, depending on the query). (He briefly mixes up the order on stream, then re-walks it: rows → normalize → tuples → sort → compare.)
4. **Order-sensitive queries skip the sort.** The golden dataset's flag tells you whether order matters; if the query has an `ORDER BY`, compare **directly without sorting** — a match without sorting proves both queries used the `ORDER BY` clause correctly; otherwise it's a fail.
5. Plus **"two or three more checks"** he doesn't detail live.

His study advice for the code: don't pressure yourself to read it line by line — "What is the whole file doing? What is the function doing? If you can understand that, then you are in control." When the code is shared, run it through Claude and ask it to *summarize the logic*.

---

## 14. Stage 3, part 3 — the live run and the results (01:40:35–01:53:53)

First run stumbles on a classic: the code expects a file named `golden_dataset` but the export was `golden_hard` — renamed, re-run. **The evaluation starts live**, model by model, question by question, printing **match** or **mismatch** per question.

### GPT-5.6 Tera — 80%

Q1 match, Q2 **mismatch**, Q3 match… at seven or eight questions only one wrong; then failures on **Q10 and Q11** ("these are very difficult questions… I called these difficult because they are actually very complex"). Out of 18 questions, four wrong. **Final: 80%.**

### Kimi K3 — 55%, the disaster

Context first, as the instructor introduces it: K3 is Moonshot AI's freshly launched **2.7-trillion-parameter** model, hyped as "very close to **Fable 5** at one-third the cost," which "created quite a stir in the US stock market" — a frontier-class model from China released as **open weights** ("not exactly open source, but open weights"). Then the run: **SQL errors** — "the SQL that was generated has an error in itself. So it doesn't matter whether it's correct or wrong. It has become a syntax error." Five-six SQL errors plus two mismatches; and it is **very slow** — "maybe it's a big model; besides, it's a **reasoning model** — I haven't changed any of the reasoning settings… there might be latency issues." Final: **55% (11 of 20 correct)** — "for a frontier model on this scale, this is very bad. 2.7 trillion parameters means it's no small matter."

> "If you see that some outstanding model has come up on the leaderboard — that doesn't guarantee it will perform as well in **your** work… The full headline has Kimi K3, but when we applied it to our work, see what's happening. **This is a very good lesson that you've seen practically.**"

He connects it to the community: "The reviews of K3 on **Reddit** are not good… People have definitely tested it in their own way. They might have run this kind of custom evaluation." (A viewer's quip mid-carnage: "There's that famous saying — *Chinese goods*.") One admitted gap: **latency was not measured** — "we could have seen how much time was spent in the entire activity, but I didn't write that code, I'll do that tomorrow."

### Grok 4.5 — 90%, the surprise winner

"Clearly faster than K3," and early on: **no errors at all** — and it **solves Q2**, the question that had defeated both GPT-5.6 Tera and Kimi K3. "I always feel Grok is very underrated. And **Elon Musk should never be underestimated**." Heading into the brutal Q9/Q10 territory that broke the earlier models, the instructor wonders aloud whether it will finally err — it doesn't there; total: **two mistakes → 90%**, fast, and the cost check lands at **₹2.5 lakh/month — almost half of Tera's**. "So far, this is clearly the winner."

### Claude Sonnet 5 — 85%, the fastest

"Look how fast Sonnet is! It has already finished seven questions." The fastest of the three seen so far; two wrong, plus one more in the brutal section. **Final: 85%, cost ₹2.84 lakh.** (Mid-run he notes it's a good model in the Sonnet line — capability comparable to the previous generation's Opus.) A budget note from the discussion: "since Sonnet's latency is very good, we can push extra 25K" — the kind of trade-off talk a real team has.

### MiniMax M3 — 65%, the dark horse

"Oh, our dark horse has arrived. Oh ho, it went wrong on the second question itself." Q2 (now failed by **three** models), Q10, Q11 — the brutal ones. **Five-six wrong → 65%.** And the pattern that sparks the lecture's best running joke: **the Chinese models threw SQL syntax errors while the American models "are at least getting the syntax right… with these, the syntax is just disappearing midway. Are they writing in Mandarin?"** ("Everything has been banned, so we'll have to create our own.")

### In-run Q&A (while the APIs grind)

- *Can I build this with AI tools?* (Varun) — "Coding it by hand is also not a big deal… I myself generated the code. It's very easy to understand" — understand file-level function, not line-by-line syntax.
- *Can we do a proper end-to-end Text-to-SQL project with complex joins?* (Sourabh) — "The **goal of this course is not to create projects. The goal is to evaluate projects**… I will create something and bring it and then test it."
- *Is database normalization better than one big table — won't it increase SQL-generation errors?* — First the funny confusion: "Which normalization are you talking about? The one we applied on the LLM leaderboard or the one we apply on data?" Then the real answer: **normalized schemas for transactional databases, denormalized for analytical ones** — **OLTP** (Online Transaction Processing) vs **OLAP** (Online Analytical Processing). The Cricinfo team has surely normalized its data; for analysis you keep it denormalized.
- *Is GPT-4.5 the latest GPT?* — "I haven't checked… Does anyone know? Yes, young man!"
- *Who does this work — a project manager?* — "**AI engineers do this job, because it's quite a technical task.** Then you give the report to the project manager, and then they make the final decision."

### Statistical honesty

> "This is a small dataset. Ideally, it should have been a bit larger. **20 questions means, literally, each question carries 5% importance.** But I think even with a larger dataset, Grok will still perform better. Also, you can run the same dataset multiple times, because each API call is independent… you will get more statistical proof — even after running this entire evaluation five times, Grok has scored the highest… it will cost a bit more, but you will have this confidence."

> 💡 **Expert commentary.** The instructor's instinct here is exactly right, and worth quantifying: with n = 20, the 95% confidence interval around 18/20 (90%) spans roughly **70–97%**; around 17/20 (85%) it spans **64–95%**; around 16/20 (80%), **58–92%**. The gaps between Grok, Sonnet, and Tera are *within sampling noise* — which is precisely why he suggests averaging **five independent runs** (variance estimation) and a larger golden set before signing a contract. The same caution applies to his per-question commentary: Q2 defeating three models is a great *lead*, but each single question is 5% of the score; failure analysis (which we saw in lecture 3's "analyze the results" step) is how you turn leads into knowledge.

---

## 15. The verdict — and closing Unit 2 (01:53:53–01:56:53)

### The scoreboard

| Model | Accuracy | Speed (observed) | Monthly cost | Verdict |
|---|---|---|---|---|
| **Grok 4.5** | **90%** | Fast (leaderboard throughput also says fast) | **₹2.5 lakh** (cheapest finalist, ~half of Tera) | Finalist |
| **Claude Sonnet 5** | **85%** | **Fastest in practice** | ₹2.84 lakh | Finalist — the instructor's lean |
| **GPT-5.6 Tera** | 80% | Fine | ~₹5 lakh (the pre-class-budget pick) | Eliminated: "Tera is very expensive… then why should we spend behind that?" |
| **MiniMax M3** | 65% | OK | (the budget Chinese pick) | Out — syntax errors on brutal questions |
| **Kimi K3** | 55% | **Slowest** (reasoning model, default settings) | — | "The worst was K3" — the leaderboard-hype cautionary tale |

### Grok vs Sonnet

The decision comes down to **Grok 4.5 vs Claude Sonnet 5**: costs are almost the same, their leaderboard indexes were equal, and speed is contradictory — "the throughput is saying Grok is fast, but according to our experience Claude was fast." The tiebreaker is qualitative:

> "The **reliability of Anthropic's API** with Sonnet is a bit more… I am leaning a bit towards Sonnet, because I find the company more reliable… There is a bit of **Elon's personality in Grok**, so it doesn't seem very reliable to me — maybe I will go with Sonnet because it is more stable in that aspect. But yes, this can be your decision. **When companies can't make a decision, voting is done.**"

> 💡 **Expert commentary.** Notice what just happened: the final tiebreak was **vendor reliability**, a criterion no benchmark measures. In real procurement this is standard — provider uptime/SLA history, enterprise support, rate limits, data-retention terms, and *organizational* stability all sit alongside accuracy and cost. Notice also the quiet **vendor lock-in** win in this architecture: because every candidate was called through **OpenRouter's uniform API** (and swapped via a five-tuple list), nothing in the pipeline cares who wins. That's the modular, swap-friendly design principle the lecture preaches — and it cuts both ways: it makes switching cheap when Grok 4.6 lands tomorrow, and it keeps the eval harness reusable for the *next* selection round.

### Closing

The instructor's summary of the session: "It really feels like we're colleagues, working for some company, and today we're finishing a project." Housekeeping and send-off:

- The **code explanation was rushed** ("in two hours I tried to explain the whole thing") — the code ships tomorrow; the GitHub repo doesn't exist yet ("Sorry Upendra… I was working on my own local machine").
- **Homework:** run this custom-eval pattern yourself, on any other application type — "Text-to-SQL is just one subject; there can be other things too. If you do it once, the understanding will become very deep."
- Future teasers: **system design** case studies using the same thinking, and **AI security** as a later course.
- **Unit 2 closes**: "This part regarding Model Evals is over. The benchmarks are also done. You have also learned to run custom evals. After that, we move to **application evaluation**" — which is where the course spends the rest of its life, starting with the RAG-evaluation interview answer.

---

## Key takeaways

1. **Model selection is a three-stage process**: write clear requirements → shortlist 5–10 candidates from leaderboards → run a custom model eval on your own data. Leaderboards filter; the custom eval decides.
2. **Requirements are engineering, not vibes**: task (Text-to-SQL), cost ceiling (₹3 lakh/month from the business), latency (2–3 s, no reasoning models), context window (irrelevant here — no multi-turn), deployment (public APIs preferred for reliability), accuracy (non-negotiable for finicky cricket fans). Write them down *before* opening a leaderboard.
3. **Cost modeling is arithmetic, not mystery**: tokens in (400) + tokens out (100) per request × requests/day (50,000) × 30 × ₹95/$. Know what a **blended price** is (e.g., 4:1 ratio: (4×10 + 1×50)/5 = $18/M) and always check the blend ratio your leaderboard uses.
4. **Prompt caching nearly halves the bill** when the prefix is static: pay a premium to write ($12.50 vs $10), ~1/10th to read ($1); pick the 5-minute vs 1-hour refresh cycle to match your traffic. It's powered by the **KV cache** (attention's K/V tensors), and it helps Text-to-SQL far more than RAG (whose context changes every query).
5. **Proxy selection is legitimate but provisional**: no trustworthy Text-to-SQL leaderboard (stale, fine-tuned entries, opaque harnesses) → use a coding leaderboard as a proxy; filter 146 models by budget, min-max normalize rating and throughput, combine with task-appropriate weights (9:1 here — output is only ~100 tokens, so latency matters less).
6. **Custom eval = golden dataset + execution-based comparison**: 30–50+ questions (up to 500), analyst-verified SQL, representative of real user questions, mixed difficulty and SQL topics; judge by **comparing result tables, never string-matching queries** (many queries yield one result); respect order-sensitivity.
7. **Golden datasets cost money twice** — human labeling and LLM calls (5 models × 50 questions = 250 calls) — and grow forever as production failures are fed back in.
8. **Leaderboard stardom ≠ task performance**: Kimi K3 (2.7T parameters, Fable-5-class hype) finished last at 55% with SQL syntax errors and the worst latency. Reddit reviewers had run their own "custom evals" and said as much.
9. **The final call balances accuracy, cost, speed, and vendor reliability**: Grok 4.5 (90%, ₹2.5 lakh) vs Claude Sonnet 5 (85%, ₹2.84 lakh) — the instructor leans Sonnet on API/company reliability; and this is a **repeat decision**, not a one-time one, so design for model-swappability.
10. **This is the AI engineer's job**: you run the technical evaluation and hand the report to the project manager, who makes the final call.

## Interview angles

- *"Your team is adding a new AI feature. How do you decide which LLM to use?"* → Walk the three stages with the Ask Cricinfo story: requirements first (cost ceiling from the business, latency target, context/deployment/accuracy), leaderboard shortlist as *filtering*, then a custom eval on your own data as the *decision*. Mention that you'd hand a report to the PM, not a hunch.
- *"The best model on the leaderboard is 4× your budget. What now?"* → Build the cost model (tokens per request, requests/day, blended price, FX), consider prompt caching for static prefixes, fall back to cheaper tiers, and let the custom eval tell you whether the cheap model is "close enough" — the answer depends on the application (medical vs consumer tolerance for error).
- *"How would you evaluate a Text-to-SQL system?"* → Golden dataset (representative questions, difficulty mix, joins/sub-queries/window functions, analyst-verified), then **execution accuracy**: run generated and golden queries, compare result sets with normalization (2.0 vs 2), row-count checks, and order-sensitivity — never string-match SQL. Distinguish SQL syntax errors from result mismatches.
- *"Your eval shows Model A at 95% and Model B at 92%, but B is 50% faster and 30% cheaper. Which do you ship?"* → Fitness for purpose; check statistical significance first (20 questions → 5% per question, overlapping confidence intervals; average multiple runs), then weigh accuracy against latency, cost, and vendor reliability.
- *"What is prompt caching and when does it help?"* → Static prompt prefixes cached at the provider (KV cache); write premium, cheap reads; refresh windows (5 min vs 1 h) matched to traffic; huge for schema-heavy Text-to-SQL, limited for RAG where context changes per query.
- *"How large should your eval dataset be?"* → 50–500 questions as a working range; constrained by labeling cost and inference cost (models × questions = calls); representative and diverse by design; grows from production failures.

## Cross-links

- **Previous:** [10 — How to Use LLM Leaderboards](10-llm-leaderboards.md) — the "filter, don't select" rule this lecture executes, and the reading checklist that feeds stage 2.
- **Next:** [12 — "How Do You Evaluate Your RAG App?" (Interview Answer)](12-rag-eval-interview-answer.md) — the course pivots from model evals to application evals, opening Unit 3.
- **Parent notes:** [Section 105 note 1 — Evaluation Fundamentals](../01-evaluation-fundamentals.md) (golden datasets, metric design, release decisions — the concepts this run instantiates) and [note 3 — Agent Benchmarks](../03-agent-benchmarks.md) (the benchmark-literacy backdrop for stages 1–2).
- **Foundations:** [02 — Model vs Application Evals](02-model-vs-application-evals.md) (where this lecture was first promised) · [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) (the 10-step loop, of which this is the model-selection instance) · [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) (the judging-method toolbox behind execution-based checking).
- **Unit 2 context:** [07 — Model Evals & Capabilities](07-model-evals-capabilities.md) · [08 — Benchmarking: Saturation vs Contamination](08-benchmarking-saturation-contamination.md) · [09 — Benchmark Evolution](09-llm-benchmarks-evolution.md) (why leaderboard claims need stage-3 verification).
- **Where the hands-on continues:** [13 — Testing RAG Retrievers](13-testing-rag-retrievers.md) and [17 — Operational Evals](17-rag-operational-evals.md) (latency and cost become first-class metrics).
- **Course hub:** [README.md](README.md).
