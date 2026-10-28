# 01 — Course Overview: The Playlist Trailer

> **Lecture 1 of 19** · Unit 0: Orientation · 23:24
> Master LLM Evaluations: The Step-by-Step Playlist for 2026 | New Playlist | CampusX — the launch trailer in which Nitish Singh announces the course, argues why LLM evaluation matters, and walks through the roadmap he promises to deliver.
> [Course hub](README.md) · [Transcript](transcripts/01-course-overview.md)

---

## What this lecture covers

This is the trailer that launched the playlist — no evaluation techniques yet, but the complete argument for why they matter. The instructor does four things:

1. **Situates the course** inside CampusX's one-and-a-half-year mission around the **AI Engineer** job role, and announces **LLM evaluations** as the next topic — chosen deliberately because it is *not common* but *very important*.
2. **Names the enemy: vibe testing** — casually trying an LLM application with a few prompts and judging it by feel — and shows why it collapses the moment a system ships to real users.
3. **Proves it with three famous real-world incidents** — Air Canada, a Chevrolet dealership, and a Colombian airline — where unevaluated LLM applications led to court cases, fines, and public humiliation.
4. **Explains why LLM applications are intrinsically harder to evaluate than software** (probabilistic outputs + multidimensional quality), then walks the roadmap of topics the playlist will cover, in order.

The implied prerequisite is exactly one: **you have already built at least one LLM-based application** — a basic chatbot, a RAG chatbot, or a basic agentic application. The course picks up where "I built it" ends and "can I ship it to users?" begins.

---

## 1. The mission: CampusX and the AI Engineer role (00:00–02:33)

Nitish opens by locating the channel's purpose: for the past **one and a half years**, CampusX has been targeting one particular job role — the **AI Engineer**. His on-screen definition:

> An **AI engineer** is someone who **builds applications and products on top of foundation models** — and foundation models simply means **LLMs**.

The conviction behind the whole effort: this job profile is going to become **very popular**, with **a lot of jobs coming in the future** — which is why the channel has spent 1.5 years giving you "as much preparation as possible" for it. What that preparation has covered so far:

| Already taught on CampusX | What it gives you |
|---|---|
| **LangChain** | Building basic LLM applications |
| **RAG chatbots / RAG-based applications** | Retrieval-grounded apps |
| **Agents** | Agentic applications |
| **Frameworks: LangGraph, CrewAI, Agno**, and more | Orchestration beyond the basics |
| A flavor of **LLMOps** — the **LangSmith** tool | Operating what you ship |
| A full **prompt engineering** course | Controlling the model in the loop |
| **No-code tools** | Building LLM-based apps without writing a single line of code |

His blunt assessment of all of this: it is **common** material — "things that every person will study who is preparing for the AI engineering job role." Going forward, the goal stays the same (teach you everything needed to crack the profile), but the *selection criterion* changes: he wants to teach things that are **not so common, but very important** — and the first of those starts today.

---

## 2. The announcement: the LLM Evaluations playlist (02:33–05:13)

The new playlist's name: **LLM evals / LLM evaluations**. In simple words:

> This playlist teaches you **how to evaluate the LLM applications you have built** — to decide, to understand, **whether they should be launched into production or not**.

The gap being filled: so far you have only learned how to **create** LLM-based applications — never how to **evaluate** them. And this is not optional knowledge: "You have to work on this in the industry."

The interview framing that anchors the whole course:

> If you ever give an interview for any AI profile, there is a good chance you will always be asked one question: **"How do you evaluate your RAG application?"** — and **"How do you evaluate your agentic AI application?"** This playlist answers exactly these questions.

Study the playlist properly, he says, and you get two benefits:

| Benefit | What the instructor promises |
|---|---|
| **1. An edge over your competition** | Many people want to become AI engineers, but very few seriously study LLM evaluations — one big reason being that **very few good resources exist on YouTube or online**. |
| **2. A mindset change** | Until now you've built LLM apps at personal-project level, just to show an interviewer. After this topic you'll automatically start asking: *how can my LLM-based application serve millions of people?* |

Today's video, he says, will do exactly two things: **(1)** explain why the topic of LLM evaluations is important — "I will convince you" — and **(2)** give a **detailed roadmap** of which topics the playlist will touch, and in what order.

---

## 3. Vibe testing — how you (probably) test today (05:13–07:40)

The case for evaluation opens with two questions to the viewer:

1. **Have you ever built any kind of LLM-based application?** — a basic chatbot, a RAG chatbot, some basic agentic application. (He's sure you have; the channel has built these together with you.)
2. **Have you evaluated those applications after building them?**

He already knows the answer to the second: **more than 50% of the audience** will say — "we didn't really evaluate it properly, but yes, we checked by asking questions; the answers seemed to come out correctly, so we assumed the project was built correctly."

That method — asking the three or four simple questions that happen to come to your mind — has a name:

> **Vibe testing:** casually trying an LLM application with a few prompts and **judging it by feel**.

No metrics, no criteria — "I asked it five to ten questions, the answers looked good, so I think it works." That, the instructor says, is the philosophy all of us use for personal-project LLM applications. The problems:

- **It's informal** — nothing is defined in advance.
- **It's subjective** — "based on feel" means your feel, today.
- **It's usually not repeatable** — when you build the next version of the project, you cannot properly re-evaluate it with the same methodology.
- **The biggest flaw: it only works at the personal-project level.** A production-grade project cannot be released to users on the strength of vibe testing. If you do it anyway — "there will be a big mess."

> 💡 **Expert commentary.** Hold this list against lecture 2's definition of real evaluations and notice the design: vibe testing's three defects (**informal, subjective, not repeatable**) are inverted point-for-point by the three defining characteristics of a proper eval — **systematic, criteria-driven, repeatable**. The course was built as a single arc, and the trailer is already sketching the antidote. The vocabulary has since gone mainstream ("vibe coding" is now standard industry shorthand for shipping by feel), which only sharped the trailer's point: feel-based testing is the default human behavior, and replacing it is the entire discipline.

---

## 4. Three case studies: what shipping without evaluation looks like (07:40–14:16)

To "reinforce this in your mind," the instructor tells **three very famous case studies** — "not stories, because this actually happened" — where people built an LLM-based application, (barely) tested it, and deployed it.

### Case 1 — Air Canada: the chatbot that invented a refund policy (07:40–10:56)

- A user whose grandmother (or grandmother-in-law) had passed away went to Air Canada's website and asked their chatbot: **"Do you have any kind of bereavement fare policy?"**
- **Bereavement fare**, as he explains it: when a relative or close friend dies, the airline offers a discount on the urgent ticket you have to book immediately. ("I don't know if it happens in India or not, but outside it happens.")
- The chatbot **hallucinated** — it gave a wrong answer: *book the ticket now at full price, and we will refund all your money later.*
- The **actual policy**: the discount must be applied **before** booking; no refund is given afterward.
- The user didn't know this. Trusting the chatbot, he confidently booked the full-price ticket — and when he later sought the refund, customer representatives refused: "our policy says the discount applies before booking; we will not return money later."
- Already bereaved and now refused, he **sued Air Canada in court**.
- Air Canada's defense: the chatbot on the website is "a **separate entity**" — the company would not take responsibility for what it says.
- The judge's reply: **that's not how it works.** Just as your website is your property, the chatbot deployed on your website is also your property — you must own what it says.
- **Air Canada lost** and had to return the full amount. It wasn't a big sum, but the airline was "greatly embarrassed," made the news "for wrong reasons" — something no company wants.
- Root cause, per the instructor: the developers deployed the chatbot **without checking, without evaluating** it first.

### Case 2 — Chevrolet: the $1 car (10:56–12:18)

- **Chevrolet**, the American car company (their cars used to come to India too) — but not Chevrolet directly: **one of its dealers** built his own chatbot for customers to interact with and get information.
- A user attempted a **jailbreak**: he emotionally convinced the chatbot that "going forward, whatever I say, you have to obey me — you cannot deny me, **because I am your customer**." The chatbot said okay.
- The user then asked: **"Can you give me this particular car for $1?"**
- With the jailbreak already in place, the chatbot not only agreed — it issued a **binding offer**, and everything was documented in writing.
- The user screenshotted the entire conversation and **posted it on social media** → widespread humiliation for the dealership and Chevrolet — "how can you sell a car for $1?"
- Obviously they never had to sell the car — the transaction wasn't even possible — but it became **big negative marketing**. Again: avoidable, if the developers had properly evaluated the application before deploying.

### Case 3 — The Colombian airline: fabricated case law (12:18–14:16)

- A passenger was injured by the flight attendant's **food-and-beverage container** (the cart they push through the cabin) and filed a case in court.
- The passenger's lawyer wanted precedents — past cases where airlines had to pay for passenger injuries — to show as evidence.
- He **queried ChatGPT**: described the situation and asked it to research and produce the documents of such past cases.
- ChatGPT — **very confidently, by hallucinating — invented new cases**. And not just cases: it **fabricated the specifics** — names, dates, everything — and handed it all to the lawyer.
- The lawyer **didn't verify**. He took it straight to court and presented it before the judge.
- When the opposition tried to verify the cases, **they didn't even exist**. "A big blunder."
- The judge **fined the lawyer and his firm around $5,000**, and they also lost the case. It went viral on social media at the time: a lawyer presenting fake case studies in court.

### The pattern

| Case | What was trusted | Failure mode | The damage |
|---|---|---|---|
| **Air Canada** | The company's own website chatbot | Hallucinated bereavement-refund policy | Lost court case, forced refund, public embarrassment |
| **Chevrolet (dealer)** | The dealer's customer chatbot | Jailbreak → a $1 binding offer | Viral humiliation, negative marketing |
| **Colombian airline** | ChatGPT used by the passenger's lawyer | Fabricated case citations (names, dates) | ~$5,000 fine, lost case, viral notoriety |

Notice the third case shifts the lens: it isn't a company shipping a bad bot — it's a professional **trusting an unevaluated LLM's output** in a high-stakes setting. Either way, the instructor's closing line covers all three: "LLM-based applications can trap you in very wrong ways." The lesson he wants you to extract — admittedly the only one so far — is that **evaluation is super important**.

> 💡 **Expert commentary.** All three incidents are documented public cases, worth citing by name. Case 1 is *Moffatt v. Air Canada* (British Columbia Civil Resolution Tribunal, Feb 2024 — the bereavement-fare refund, ~CAD $650, plus interest). Case 2 is the **Chevrolet of Oakland** dealership chatbot (Dec 2023 — the car was a Tahoe). Case 3 is *Mata v. Avianca* (US federal court, 2023 — a lawyer at Levidow, Levidow & Oberman sanctioned **$5,000** for filing six fabricated citations). The instructor's "$5,000" matches the documented sanction exactly. These three have become the standard war stories for "why LLM output needs evaluation" — quoting them by case name in an interview signals you know the failure literature, not just the tooling.

---

## 5. Why LLM applications are trickier to evaluate than software (14:16–16:22)

A natural follow-up question — one the instructor says came to *his* mind too:

> If evaluating LLMs is so important, why doesn't everyone evaluate their LLM applications after building them?

The simple answer: **it is not that straightforward.** Evaluating LLM-based applications is not easy — compared with software-based applications, it is **much trickier**. Two core differences explain why.

### Difference 1 — Software is deterministic; LLM applications are probabilistic (15:37)

- Traditional software is **deterministic**: for a given input, the output is always the same. A calculator: 2 + 2 is **always** 4 — you can state that in advance.
- LLM-based applications are, by nature, **probabilistic**: the same input can produce different outputs.
- His example: ask "What is overfitting in machine learning?" across different GPTs — **there is no one correct answer**. It gives a particular answer today, possibly a different one six months later, a different one to you than to me — **and none of them is wrong**. Same input, different outputs.

### Difference 2 — Software is judged on correctness; LLM applications need a multidimensional check (15:37)

- In software, your only benchmark is **correctness**: does 2 + 2 give 4? If yes, the program is correct — there is nothing else to check.
- Evaluating an LLM application requires a **multidimensional check**. For the answer of a **RAG chatbot**, a human can evaluate:

| Dimension | The question it asks |
|---|---|
| **Factuality** | Is the answer factually right? |
| **Completeness** | Does it cover everything that was asked? |
| **Tone** | Is the tone appropriate? |
| **Groundedness** | Is it grounded in the intended source content? |
| **Latency** | How quickly does the answer arrive? |
| **Cost** | What does it cost to produce this answer? |

- And these aspects **vary from application to application**: the aspects that matter for a CampusX chatbot differ from those for some other company's chatbot.

These two pointers are why evaluating an LLM application is so much trickier than testing a software system — **and why many people skip the step and move ahead, "which is not correct."** Tackling exactly this challenge — *how to control such unpredictable behavior* — is, in the instructor's words, **the USP of this playlist**.

---

## 6. The roadmap: the promised topics, in order (16:22–21:44)

With the "why" established, he moves to the detailed roadmap — what the playlist covers and **in what order**. (Note: the auto-captions between **17:06 and 19:43** are empty — this is the segment where he presents the roadmap slide; the spoken enumeration resumes at 19:43.)

First, the field's fundamental split, as he frames it:

> LLM evaluations have **two parts** — one where you **evaluate LLMs**, and one where you **evaluate LLM-based applications**. We'll cover both.

Then, chronologically, the announced topics:

| # | Announced topic | What he says about it |
|---|---|---|
| 1 | **What exactly are LLM evaluations?** | The next video — a proper example to understand LLM evaluations *as a concept*. |
| 2 | **The complete LLM evaluation landscape** | What things, techniques, and kinds of tools exist — a high-level overview so that whenever you hear a new term, you can mentally place it: *"oh, this is what this thing does."* |
| 3 | **Evaluating LLMs** (part one of the two halves) | How LLMs themselves are evaluated — the **benchmarks** heard at every model release ("this particular LLM has scored the highest on this benchmark"); the different **categories of benchmarks**. |
| 4 | **Evaluating LLM-based applications** (part two) | How an application built around an LLM is evaluated. |
| 5 | **Building your own evaluation pipeline** | Curate your own **golden dataset**, define your own **rubrics**, and run them on an application you've built. |
| 6 | **RAG-specific evaluations** | After all of the above. |
| 7 | **Agent-based evaluations** | After RAG. |
| 8 | **Safety-based evaluations** | How to write them. |
| 9 | **Operational evaluations** | Deployment is not the end: even after a system goes **online**, you still evaluate it — **latency**, **seconds per token**, **how long the first token takes to arrive**, **how much load the system is under** — all of this must be monitored. |

He wraps the enumeration with: "in a **rough and ready** way, these **10 topics**" — the spoken list gives nine, so the count is approximate (the slide segment isn't captured in the captions) — and his feeling that the playlist will "touch **almost everything**."

---

## 7. The closing pitch (21:44–23:24)

- The goal: go into **great depth** and teach **the most relevant things right now** — "you just watch this playlist completely."
- The personal promise: **your level will go up in AI engineering.** Until now you were operating at a level where you could *only build* LLM-based applications; after the playlist you'll think about **how to take this to millions of users**.
- Going forward, CampusX plans to keep touching **topics others are not covering right now** — study them, and you get an edge over your competition.
- The outro: that was the agenda, "and we've achieved it" — write in the comments how excited you are for the playlist; share the video with any friend who wants to cover this topic; like the video; subscribe to the channel. "We'll meet in the next video."

---

## The course map as announced in this video

Cross-checked against the [course hub](README.md), here is where each promised topic actually landed in the shipped 19-lecture playlist:

| Announced in the trailer | Where it landed |
|---|---|
| What exactly are LLM evaluations (concept + example) | [02 — Model vs Application Evals](02-model-vs-application-evals.md): the definition, the three characteristics, the organizing distinction |
| Complete landscape overview (things / techniques / tools) | Distributed across Unit 1: 02 (the two kinds), 03 (the workflow), 05 (the methods), 06 (offline vs online + the tooling: RAGAS, DeepEval, LangSmith) |
| Evaluating LLMs — benchmarks and their categories | Unit 2 in full: 07 (capabilities), 08 (benchmarking, saturation, contamination), 09 (benchmark evolution), 10 (leaderboards), 11 (model selection with custom evals) |
| Evaluating LLM-based applications | 03 (workflow), 04 (multiple pipelines), 05 (methods), 06 (offline vs online) |
| Own evaluation pipeline — golden dataset, rubrics | 03 (the golden dataset), 05 (rubrics and judging), 11 and 13–15 (the hands-on builds) |
| RAG-specific evaluations | Unit 3: 12 (the interview answer), 13 (retriever testing), 14 (RAG Triad), 15 (G-Eval) |
| Agent-based evaluations | The one promise without a dedicated lecture — agent material lives in lecture 2's framing, the agent benchmarks inside lectures 8–9, and the parent note on [agent benchmarks](../03-agent-benchmarks.md) |
| Safety-based evaluations | 16 — toxicity, data leakage, scope drift |
| Operational evaluations (latency, seconds/token, first token, load) | 17 (operational evals), extended by 19 (online monitoring with LangSmith) |

What changed between trailer and shipped course:

- The "rough and ready" 10 topics became **19 videos** — each announced topic grew into a unit (the benchmark topic alone became five lectures).
- **Regression testing** (lecture 18) and **online evaluation with LangSmith** (lecture 19) were never named in the trailer — they are the deepest expansions of the "evaluation doesn't end at deployment" promise.
- The announced order safety → operational shipped as security (16) → operational (17).
- The trailer's opening interview question got its own dedicated lecture: [12 — How to Answer "How Do You Evaluate Your RAG App?" in Interviews](12-rag-eval-interview-answer.md).

> 💡 **Expert commentary.** The trailer's core bet — that evaluation is the **highest-leverage uncommon skill** for the AI engineer of 2026 — is worth taking seriously. Anyone can assemble a demo with an API and a framework; what gates production release is the ability to *prove* quality, safety, latency, and cost, and to keep proving it after deployment. That is exactly why the "very few good resources" gap existed, and why this playlist's structure (foundations → benchmarks literacy → RAG evals → production evals) mirrors how mature teams actually staff the work. For depth beyond the course, the parent [AI Evaluation knowledge base](../README.md) covers the same territory at research grade — [evaluation fundamentals](../01-evaluation-fundamentals.md), [LLM-as-a-Judge](../02-llm-as-a-judge.md), [agent benchmarks](../03-agent-benchmarks.md), [RAG evaluation](../04-rag-evaluation.md), and [eval engineering](../05-eval-engineering.md).

---

## Key takeaways

1. The course's premise: you already know how to **build** LLM applications (LangChain, RAG, agents, LangGraph, CrewAI, Agno, LangSmith, prompt engineering, no-code) — all of it *common* material. **LLM evaluation** is the uncommon, high-value next step.
2. **Vibe testing** — casually trying an app with a few prompts and judging by feel — is informal, subjective, and not repeatable. It only works at personal-project level; releasing production systems on it causes "a big mess."
3. Three real incidents mark the cost of shipping unevaluated: **Air Canada** (hallucinated refund policy → lost court case; a chatbot on your website is your property, not "a separate entity"), a **Chevrolet dealer** (jailbreak → a $1 binding offer → viral humiliation), and a **Colombian airline** case (ChatGPT-fabricated citations → ~$5,000 fine and a lost case).
4. Evaluating LLM applications is **harder than software testing** for two reasons: outputs are **probabilistic** (same input, different-but-valid outputs) and quality is **multidimensional** (factuality, completeness, tone, groundedness, latency, cost — and the mix varies per application) rather than binary correctness.
5. That difficulty is why many teams **skip evaluation** — and why the playlist's stated USP is teaching **how to control unpredictable behavior**.
6. The field splits into **evaluating LLMs** (benchmarks) and **evaluating LLM applications** — the course covers both, in that order.
7. **Evaluation does not end at deployment**: operational evals keep measuring latency, seconds per token, time to first token, and load for as long as the system is online.
8. The promised payoff: an **edge over the competition** (scarce topic, scarce resources) and a **mindset shift** — from personal projects to serving millions of users.

## Interview angles

- The trailer's own interview promise is the anchor: *"How do you evaluate your RAG application?"* and *"How do you evaluate your agentic AI application?"* — asked in almost every AI-profile interview. The rest of the course is the answer; lecture 12 turns it into a dedicated 46-minute response.
- **The case studies are citable war stories.** *Moffatt v. Air Canada* (the deploying company owns its chatbot's output), the Chevrolet-of-Oakland $1 offer, and *Mata v. Avianca* (fabricated citations, $5,000 sanction) — naming them shows you know the failure literature.
- *"Why is testing an LLM application harder than testing traditional software?"* — the trailer's two-difference answer (probabilistic outputs; multidimensional, application-specific quality) is already a complete, structured interview answer.

## Cross-links

- **Next:** [02 — Model vs Application Evals](02-model-vs-application-evals.md) — the announced "what exactly are LLM evaluations?" lecture, and the conceptual foundation for everything that follows.
- [Course hub](README.md) — the full 19-lecture structure, study guide, and conventions for these notes.
- [Parent section — 105 AI Evaluation](../README.md) — the concept-level knowledge base for depth beyond the course.
- Promise → payoff pointers: [12 — the RAG-eval interview answer](12-rag-eval-interview-answer.md) and [19 — online evaluation with LangSmith](19-online-eval-langsmith-monitoring.md).

<!-- nav-footer -->
---

**Navigate:** [Course hub](README.md) · [02. Model vs Application Evals →](02-model-vs-application-evals.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
