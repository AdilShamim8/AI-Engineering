# Module 1 · LLM Fundamentals

> **100 Days of AI Engineering** · Days 1–6 · 6 units

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/llm-fundamentals/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

## Units

#### 01 · What an LLM Does (Unit 1.1 · Day 1)

- **Next-token prediction** — An LLM generates text by predicting the next token, choosing one, adding it, and repeating.
- **What an LLM is not** — It is not a database, a search engine or a fixed program, and it does not look up stored answers.
- **The path through the model** — Text becomes tokens, tokens become numbers the model can work with, its layers refine them, and it outputs the likelihood of each possible next token.
- **What parameter counts mean** — Sizes like 8B or 70B count what the model has learned; more can mean more capability, but bigger is not automatically better for your task.
- **Why chat models behave as they do** — Extra training on instructions and human feedback is why assistants follow instructions, answer conversationally, refuse some requests and hedge.

**Mental model** · Text → Tokens → Numbers → Model layers → Next-token likelihoods

**Try it** · Send the same prompt five times and note how the answers vary.

**Outcome** · Explain in two sentences how an LLM produces an answer and why it can sound confident while being wrong.

#### 02 · Tokens, Context and Latency (Unit 1.2 · Day 2)

- **Tokens, not words** — Models read and charge in tokens, and the same sentence can be split differently by different models.
- **Why some text costs more** — Hindi, mixed Hindi-English, code and numbers often use far more tokens than plain English for the same meaning.
- **Input vs output tokens** — You pay for both; output is usually priced higher and is generated one token at a time.
- **Latency you can feel** — Time to first token and generation speed decide how fast a response feels; long answers take longer than long questions.
- **What fills the context window** — Instructions, conversation history, documents, examples, tool results and the model's own answer all share one limit.
- **Context is not knowledge or memory** — What's in the window is temporary, the model's training knowledge is fixed, and long-term memory is something you have to build.
- **Bigger windows aren't better windows** — Facts buried in the middle of long inputs are often missed, and extra text dilutes the model's focus.

**Try it** · Count the tokens in an English paragraph, its Hindi translation, a piece of code and a list of numbers. Then estimate the cost of sending each one 10,000 times.

**Outcome** · Estimate what a request will cost and roughly how long it will take, and decide whether a task needs more context or better-chosen context.

#### 03 · Beyond Text: Images, Audio and PDFs (Unit 1.3 · Day 3)

- **Models that see and hear** — Many models now accept images, audio and documents as well as text, and answer in text.
- **Images cost tokens too** — An image is turned into tokens, and the cost grows with its resolution, so crop or resize to what the question needs.
- **PDFs come in two kinds** — Digital PDFs carry their own text; scanned ones are just pictures of pages, and the model has to read them like an image.
- **Audio** — You can transcribe speech to text first and send the text, or send the audio to a model that understands it directly and keeps tone and emphasis.
- **What models read well** — Text in images, the main point of a chart, and named fields on forms.
- **Where they slip** — Counting objects, small or dense text, exact table values, and confidently describing details that aren't really there.
- **Image or extracted text?** — When clean text is available, sending text is usually cheaper and more accurate; send images when layout, charts or handwriting matter.

**Try it** · Send the same chart to a model once as an image and once as text extracted from it. Ask both the same three questions and compare the answers and tokens used.

**Outcome** · Choose when to send images, audio or documents to a model, and predict what each will cost and where it may go wrong.

#### 04 · Controlling Output (Unit 1.4 · Day 4)

- **Temperature** — Lower temperature makes answers more consistent; higher makes them more varied.
- **Length limits and stop points** — Cap how long an answer can be and where it should stop, to control cost and format.
- **Match randomness to the task** — Keep it low for extracting facts, classifying and factual answers; raise it for brainstorming and creative work.
- **Reasoning models** — Some models think longer before answering, which helps on hard math, code, planning and multi-step problems.
- **When reasoning is wasted** — For extraction, rewriting, simple classification and summaries, a fast model is usually just as good and much cheaper.
- **The trade-off** — More reasoning can improve quality but costs more and takes longer; reasoning models may also ignore some settings like temperature.

**Try it** · Run one fact-extraction task and one creative task at low and high temperature. Then give three hard problems to a fast model and a reasoning model, and compare accuracy, speed and cost.

**Outcome** · Choose settings and the type of model based on the task instead of guessing.

#### 05 · Where LLMs Fail (Unit 1.5 · Day 5)

- **Common strengths** — Summarizing, rewriting and extracting information, classifying, coding, translating and handling messy text.
- **Common failure modes** — Making things up, arithmetic slips, shaky reasoning, ignoring instructions, sensitivity to wording, outdated knowledge and giving different answers each time.
- **Why models make things up** — They are trained to produce a likely continuation, not to check facts, so fluent wrong answers are expected behavior.
- **Ask "how reliably?", not "can it?"** — The real question is how often a model gets your task right in your situation.

**Try it** · Write 10 questions: some the model should know, some it can't know, some built on a false premise, and some missing key information. Record each answer and how confident it sounds.

**Outcome** · Predict which tasks an LLM will handle well and which need safeguards such as giving it the right documents, checking its output, or a human review.

#### 06 · Choosing a Model (Unit 1.6 · Day 6)

- **Closed vs open models** — Models from API providers offer top capability with less control; open models you can run yourself offer control and privacy but take more work.
- **No single best model** — The right model depends on your task, budget, speed needs and data rules.
- **Knowledge cutoffs** — Anything newer than a model's training date has to be given to it, through documents or tools.
- **Pin your version** — The model behind a familiar name can change or be retired, so choose a specific version and re-test when it changes.
- **Leaderboards narrow the field; your examples decide** — Use public rankings to pick a shortlist, then test the shortlist on your own questions.
- **Five things to compare** — Quality on your task, speed, cost per request, how much input it can take, and any privacy or feature needs.
- **How to choose** — Define the task → shortlist → test on your own examples → compare quality, speed and cost → look at the failures → decide.

**Outcome** · Choose a model based on results from your own examples rather than popularity or rankings.

## What we skipped, and why *(optional)*

| Topic | Why it's skipped here | Where to find it |
|---|---|---|
| Attention and transformer internals | Interesting, but doesn't change what you build | Full roadmap, Level 1 |
| Mixture-of-Experts | Matters when hosting models, not when calling an API | Full roadmap, Levels 1 and 11 |
| Training methods in detail | One paragraph covers what you need | Full roadmap, Levels 1 and 13 |
| Advanced sampling settings | Temperature covers most real use | Full roadmap, Level 1 |
| Cloud AI platforms and model licenses | Deployment decisions for later | Full roadmap, Levels 1 and 11 |
| Named benchmarks | One rule replaces them: shortlist, then test | Full roadmap, Level 1 |

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included. The same topics map to [full roadmap levels](../full-roadmap/README.md) where they are covered in more depth.*

- [3Blue1Brown — Neural Networks series](https://www.3blue1brown.com/topics/neural-networks) — visual intuition for embeddings, attention and how models learn.
- [The Illustrated Transformer — Jay Alammar](https://jalammar.github.io/illustrated-transformer/) — the classic visual walkthrough of tokens, embeddings, queries, keys and values.
- [Andrej Karpathy — Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — build GPT from scratch; the deepest free intuition for next-token prediction.
- [Google Machine Learning Crash Course — LLM module](https://developers.google.com/machine-learning/crash-course/llm) — concise free coverage of language models, transformers and text generation.
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course) — free course from tokenizers to pretraining, fine-tuning and inference.
- [Turing Post — free LLM courses roundup](https://www.turingpost.com/p/llms-courses) — curated, regularly updated list of free university and industry LLM courses.
- [OpenAI and Anthropic model documentation](https://platform.openai.com/docs/models) and [Claude models overview](https://docs.anthropic.com/en/docs/about-claude/models/overview) — primary sources for model cards, context windows, pricing and capabilities.
- [LMArena (Chatbot Arena)](https://lmarena.ai/) — live human-preference leaderboard; practice reading rankings critically.
- [MMLU-Pro / GPQA / SimpleQA benchmark pages on Hugging Face](https://huggingface.co/datasets?search=gpqa) — inspect what popular benchmarks actually measure.

## In this repository

- [LLM Literacy curriculum](../../101_LLM-Literacy/README.md)

---

[100 Days map](README.md) | [Module 2 · Building with LLM APIs →](module-2-building-with-llm-apis.md)
