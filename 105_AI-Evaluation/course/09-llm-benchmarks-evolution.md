# 09 — The Evolution of AI Knowledge Benchmarks

> **Lecture 9 of 19** · Unit 2: Model Evaluation & Benchmarks · 1:50:47
> What are LLM Benchmarks | The Evolution of AI Knowledge Benchmarks (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/09-llm-benchmarks-evolution.md)

---

## What this lecture covers

The longest lecture of the course, and a format experiment. Lecture 8 established what benchmarks are, how they are applied, and how their evaluation process works. This lecture delivers the famous benchmarks themselves — but for **one capability only: knowledge**, covered end-to-end as an evolution story.

The plan:

1. **The map first.** How knowledge benchmarking evolved from naive "ask random questions" testing (GPT-2/GPT-3 era) to **MMLU** (2020), and how MMLU's saturation split the field into four branches: reliability (**TruthfulQA**), human exams (**AGIEval**), depth (**GPQA**), and repair (**MMLU-Pro**) — culminating in **SimpleQA** and **HLE (Humanities Last Exam)**.
2. **Seven benchmarks in depth**, each through the same template: why it was needed → history & lineage (with scores) → dataset & task → scoring methodology → run configuration → what it does *not* measure → known issues & criticisms.
3. **The benchmark life cycle** — the arrival → saturation → retirement pattern every benchmark in this lecture follows.
4. **BenchWiki** — the instructor's benchmark-Wikipedia side project, and the standing contamination question ("how do we know they didn't train on it?").

If you keep one mental model from this lecture: **every knowledge benchmark is a fix for the previous one's failure** — MMLU tested breadth, so TruthfulQA tested truth, GPQA tested depth, MMLU-Pro repaired the original, SimpleQA forced generation instead of selection, and HLE combined breadth × depth into a benchmark designed to be the *last* one.

---

## 1. How this session was planned: the demo-session decision (00:00–04:25)

Recap of where we are: model evaluations can be done two ways — **benchmarks** or **your own custom evaluations** — and lecture 8 promised we would spend more time on benchmarks. We now know what benchmarks are and how LLM benchmarking is done, so the natural next step is to learn *the famous benchmarks themselves*, so you can make informed decisions later (which LLM to select, for what purpose).

The instructor's planning problem, told honestly:

- There are **eight capabilities** (knowledge, reasoning, math, long context, coding, etc.), and *every capability has multiple famous benchmarks*.
- Every benchmark is, technically speaking, **a research paper**, and research papers have details. Covering them all "might take four or five sessions" — too much.
- **Idea 1:** teach the 10 most popular benchmarks. Rejected: the famous capabilities (like coding) would dominate, and understated ones (like long context) would be skipped.
- **Idea 2:** teach the two most important benchmarks *per capability*. Rejected: you'd lose the story of **how the benchmarks evolved** within each capability.
- So he simply asked the audience. Today is explicitly a **demo session**: only the seven benchmarks of the knowledge capability, plus the full evolution story behind them — *first this benchmark came, what was its problem, then which benchmark came to solve it*, and so on. At the end of class he takes feedback on how to approach the remaining capabilities.

---

## 2. The knowledge capability — the most fundamental one (04:25–06:26)

**Knowledge capability** measures how much knowledge an LLM retains from its training process — how much world knowledge is hidden in its **weights and biases**. It is a test of the model's **parametric knowledge**.

The instructor's framing: this is *the* most important capability because it was the **original expectation** of the field. When LLMs were first trained on massive internet-scale data, the expectation was: "if we ask it about anything on the internet, it should be able to tell us." The other capabilities arrived gradually — **reasoning was an emergent behavior** that appeared as scale increased, and **coding** likewise emerged as an emergent property once models were fed large amounts of program code. Knowledge was the founding contract; everything else was a bonus.

---

## 3. Before benchmarks: naive testing and the arrival of MMLU (06:26–09:55)

The story properly begins **2020 onwards**, "because this is where the most meaningful work happened."

When GPT-2 and GPT-3 were trained on massive internet data, people tested their knowledge **naively**: random questions from different domains, and — yes, it answered. But random questions cannot guarantee how much knowledge the model actually **retained** from training. What was needed was a **proper systematic evaluation process** that could judge how much world knowledge an LLM possesses.

That is where **MMLU** entered the picture in 2020 — the first knowledge benchmark:

- A dataset of **~57 subjects** and **~14,000 multiple-choice questions (MCQs)**.
- The procedure: send the 14,000 questions to the LLM and count how many it answers correctly. **That accuracy number = how much knowledge the LLM has.**

People used MMLU throughout 2020, 2021, 2022, and 2023 — it was *the* most popular benchmark. Whenever a new model arrived (GPT-3.5, GPT-4, the Claude models), **everyone first reported its MMLU accuracy score**. But recall lecture 8's biggest lesson: benchmark questions are **public**, so they gradually enter the training data of the next generation of models — **contamination** — and future generations start answering them from memory. Over time all model scores reached ~80–90, and everyone realized MMLU had **saturated**: it could no longer distinguish which model has more knowledge and which has less.

---

## 4. MMLU saturates → the space branches four ways (09:55–19:48)

At the saturation point, the knowledge-benchmark space branched into **four directions**. The instructor lays out the branches first, then fills them in.

### Branch 1 — Reliability: TruthfulQA (2021)

MMLU tests the *breadth* of knowledge across 57 subjects — a good thing. But it **cannot guarantee how truthful the LLM is**. The internet doesn't just contain good data; it contains **incorrect data** — non-informative and false data, including widespread **misconceptions**. Train a massive LLM on a huge amount of internet data and it won't just learn the correct things; it can learn many wrong things too.

**The instructor's worked misconception:** there is a common belief (widely written on the internet) that if you keep **cracking your fingers/knuckles** you will develop **arthritis**, a bone disease. In reality this is a myth — doctors mention in a few places that it is a misconception. But a model trained on internet data mostly *sees* "cracking fingers → arthritis," so asked "is cracking your fingers harmful?" it will usually say yes, it can cause arthritis. The truth is the opposite.

So: **training a larger model on more data does not necessarily mean a more knowledgeable LLM** — it might also propagate wrong things. Work in this direction — call it **reliability** — produced **TruthfulQA** (2021): a dataset of questions where, alongside each question, **the wrong answer and the correct answer were both written down**, and models were tested on whether they pick the misconception. The strange finding: **larger models were failing more; smaller models were failing less** (explained below). Where MMLU tested breadth, TruthfulQA tested reliability.

### Branch 2 — Human exams: AGIEval (2022–23)

Another school of thought: rather than inventing new benchmarks, **have LLMs take the exams that humans take** — the IIT exam, the CAT, the NEET ("a very controversial topic, but yeah, we take exams"). Exams exist to test knowledge levels, so existing exams could be repurposed as benchmark datasets, and by evaluating the exam answers we learn **where an LLM stands compared to a human**. This produced **AGIEval**, built from American exams (like the **SAT**) and Chinese exams (**GaoKao** and similar). You may remember 2022–24 daily news of the form "an LLM beat humans in *this* exam" — that ideology.

### Branch 3 — Depth of knowledge: GPQA (2023–24)

When MMLU saturated (~2024), one direction asked: instead of the *breadth* of knowledge (basic questions across 57 subjects), what about the **depth** of knowledge? MMLU's questions are basic-level; what if the questions were *really* difficult — research-level? This produced **GPQA (Google-Proof Q&A)**: researchers created a dataset of **~500 questions** in **biology, physics, and chemistry** — science questions so hard that a normal person **given Google access still couldn't answer them**. LLMs initially scored very poorly on it.

### Branch 4 — Repair MMLU: MMLU-Pro (2024)

The other direction said: MMLU is a good benchmark even if saturated — **let's repair it**. The result, **MMLU-Pro** (2024), fixed MMLU's problems one by one: 4 options → **10 options** per question (harder to eliminate), fewer subjects (57 → a much smaller set, ~12 by his first recollection, **14** per his notes), ~12k questions, plus questions that require **a bit of reasoning**. For the next couple of years MMLU-Pro effectively **replaced MMLU**.

---

## 5. Completing the map: SimpleQA and HLE (19:48–24:54)

As always, every next generation of models beats the previous benchmarks: AGIEval saturated, GPQA neared saturation, MMLU(-Pro) neared saturation. Two more arrivals complete the map.

### HLE — Humanities Last Exam (2025)

A very popular benchmark **still used today**. A dataset of **~2,500 questions across ~100 subjects** — incredibly difficult, proper research-level questions. Two philosophies were adopted at once: **depth** (the questions are genuinely hard to solve) *and* **breadth** (2,500 questions, 100 subjects). Even current LLMs cannot score very well on it. The naming is deliberate: it was built so that **if models ever reach ~100% on it, we don't need to create more knowledge benchmarks** — we will assume LLMs have reached a level where knowledge no longer needs testing. That is why it is called *Humanities Last Exam*.

### SimpleQA — replacing TruthfulQA (2024)

In the reliability branch, TruthfulQA (2021) also saturated over time, so a new benchmark arrived: **SimpleQA**, whose job is to test an LLM's **hallucination rate by asking simple questions**. Its biggest feature: **no MCQ options** — you simply ask a question and the LLM must provide the answer itself. There is no option to select one-out-of-four and "use a little brain to think that if these three aren't it, then it must be this one." SimpleQA is still used today to detect how truthful a model is — whether it is giving blatantly wrong answers or not.

### The seven benchmarks at a glance

| Benchmark | Year | What it measures | Design | Why it was needed | Status (2026) |
|---|---|---|---|---|---|
| **MMLU** | Sep 2020 | **Breadth** of world knowledge | ~14,000 4-option MCQs, 57 subjects, from GRE/USMLE/AP + textbooks; accuracy | Replace naive random-question testing with a systematic measure | **Saturated, retired** (labs stopped using it in 2025) |
| **TruthfulQA** | Sep 2021 | **Reliability/truthfulness** | 817 adversarial misconception questions, 38 categories; MC1/MC2 log-prob scoring | Internet-trained models absorb misconceptions, not just facts | **Saturated** (~2024); replaced by SimpleQA (+ Mask) |
| **AGIEval** | Apr 2023 | Knowledge vs **humans on real exams** | 20 exam sections, 8,000+ questions (SAT, LSAT, LogiQA, AQuA, Gaokao en/zh…); 18 MCQ + 2 short-answer; bilingual | Reuse existing human exams; get a *measured* human baseline | **Saturated** (~2025) |
| **GPQA** | Nov 2023 | **Depth** of knowledge | 198 (Diamond) / 443 (Main) / 546 (Extended) PhD-level science MCQs, each validated by 2 domain experts | MMLU too easy → test depth instead of breadth | **Near saturation** (reasoning models at 80%+) |
| **MMLU-Pro** | 2024 | Harder knowledge + reasoning | 12,000 questions, **10 options**, 14 categories, reasoning-heavy; 5-shot CoT | Repair MMLU's flaws instead of starting over | **Nearing saturation** (models at 80–90) |
| **SimpleQA** | 2024 (OpenAI) | **Factuality + calibration** | 4,326 short-answer fact questions (GPT-4-failure filtered); LLM judge; 3 metrics incl. an F-score | Replace TruthfulQA; kill the MCQ crutch | **Active** |
| **HLE** | Jan 2025 | **Breadth × depth** | 2,500 expert questions, 100+ subjects, 1,000 experts / 500 institutions / 50 countries; 80% short-answer, 20% MCQ, 10% multimodal; private held-out set; accuracy + calibration | The "last" closed-ended knowledge benchmark | **Active** — today's SOTA knowledge benchmark |

The instructor's own recap of the story: testing of the knowledge capability **began with MMLU, "the mother of all benchmarks"** (at least within knowledge-based capabilities). From there: TruthfulQA for reliability; AGIEval to convert existing exams into datasets; when MMLU saturated, GPQA for depth and MMLU-Pro as the repair; and when those saturated, HLE combining breadth, depth, and other innovations — with SimpleQA meanwhile replacing TruthfulQA. His counterfactual: had he just taught "top 3 famous knowledge benchmarks," you'd have gotten **three dry explanations** — MMLU, GPQA, HLE — but not this roadmap, and the roadmap is what makes everything else easy to place.

> 💡 **Expert commentary.** The lecture's family tree is the trunk of a larger one. Before MMLU there was a whole generation of "static commonsense/knowledge QA" benchmarks — **ARC** (2018, grade-school science), **OpenBookQA**, and **HellaSwag** (2019, commonsense sentence completion, built with adversarial filtering and paid contributors — the "prize money for selected questions" criteria the instructor teases later in this lecture). After MMLU came **BIG-bench** (2021, a community-contributed 200+ task grab-bag) and the 2024 audit wave (**MMLU-Redux**). Keeping this wider tree in mind explains why the instructor can promise "20–25 more benchmarks" on his site: every era produced a dozen siblings of the seven he teaches here.

---

## 6. BenchWiki, and "how do we know they didn't train on the benchmark?" (24:54–28:31)

A frank disclaimer opens the deep-dive half: the discussion going forward is **highly theoretical and might be boring** — benchmarks are details — but it is structured, and if you hold the story in your head it hangs together.

### BenchWiki

To support self-study, the instructor is building **BenchWiki** — "a Wikipedia for LLM benchmarks" — with the help of **Claude**. Each benchmark page carries: **current status** (e.g., MMLU: saturated), a one-line description, **performance over time** (MMLU: models scoring ~45% in 2020 vs ~90% in 2024), the **human baseline**, an overview, task details, example dataset, scoring methodology, what it doesn't measure, known issues, contamination notes, how to run it, and history & lineage. It was being deployed "tomorrow"; everything taught in this lecture is a subset of what's on the site.

### The standing question: wasn't the model trained on these questions?

> "How do we know if a company has not trained the model to work best on these benchmark questions specifically?"

The honest answer: **we can't know, actually — that's the thing.** Mitigations exist: some benchmarks are **completely private** (HLE's held-out set, covered below), and some benchmark authors use clever tricks — **special strings added to the datasets**, so that if those strings appear in an LLM's answers, it is understood that the dataset was consumed during training.

> 💡 **Expert commentary.** Those "strings" are real and have a name: **canary strings** — a unique GUID embedded in a benchmark's files (the practice was standardized by **BIG-bench**, whose canary GUID is included in every copy of the dataset). If a model can reproduce the canary, the benchmark leaked into its training data. Related detection techniques include **membership inference** (asking a model to verbatim-complete benchmark questions) and n-gram overlap audits of training corpora. This is why HLE's *private held-out test set* — which never touches the internet — is the strongest contamination defense in this lecture's lineup.

---

## 7. MMLU in depth — the mother of all benchmarks (28:31–43:26)

### Specialty and dataset

MMLU's specialty is the **breadth of knowledge** — nothing else. It tests *how much breadth an LLM possesses*, not depth. To do that, its creators assembled **14,000 MCQs across 57 subjects**, sourced from **real exams** (GRE, USMLE, AP), plus internet/textbook material and expert submissions. It was launched in **September 2020**, and its only job was to tell **how smart a given LLM is** — smart in the knowledge sense. From 2021 to 2024, every new LLM's launch marketing led with its **MMLU accuracy score**, because MMLU was the best benchmark around.

### History and lineage

| Year | Event | Score |
|---|---|---|
| Sep 2020 | Paper released; GPT-3 tested | **43.9%** vs **~90%** for human experts — LLMs were far behind humans |
| 2021–22 | Peak usage; the **era of scaling laws** — companies' simple task was "keep increasing the parameters": 175B → 350B → 650B, expecting capabilities to keep growing. **Gopher, Chinchilla, PaLM** all registered MMLU scores | — |
| 2023 | GPT-4 arrives | **86%** — very close to human experts; "the decline of MMLU kind of started" |
| 2024 | All frontier models (Google, Anthropic, OpenAI) cluster in the **86–92%** range — no one could go above 92 | 86–92% |
| 2024 (audit) | An expert study manually checked every question: **~6.5% have problems** — answers wrong, or the correct answer not even included. The effective ceiling is ~92–93% because the remaining questions are incorrect | — |
| 2025 | Frontier labs **stop using MMLU**; GPQA and HLE have arrived | Retired |

### Task, answer extraction, and scoring

A sample question is **college-physics level**: *"The muon decays with a characteristic lifetime of about 10⁻⁶ seconds into an electron…"* — four options provided, correct answer marked. The task: send the question + four options (plus five solved example questions) in the prompt; the model must output A, B, C, or D; you measure **accuracy** — of the 14,000 questions, how many were answered correctly.

Answer extraction happens **two ways**, and both are used in MMLU:

1. **Generation** — the model looks at the question and prints a character (A/B/C/D).
2. **Log probabilities** — the model generates nothing; instead you read out the probability it assigns to A, B, C, and D, and the highest wins. (From transformer architecture: when a token is predicted, a probability is assigned to every token in the search space; taking the log gives the **log likelihood** used here.)

The two methods **do not yield the same answer** — there is a difference of **1–3 points**: GPT-4 measured **84%** via generation but **87%** via log probabilities. Which extraction method you use is part of the measurement. Two flavors of accuracy are reported: **overall accuracy** (whole dataset) and **micro accuracy** — a separate percentage **per subject** (this much in biology, this much in physics, this much in law).

> 💡 **Expert commentary.** The 84-vs-87 gap is not a MMLU quirk; it is the general **scoring-vs-sampling** distinction in LM evaluation. Log-likelihood scoring reads the model's full distribution (no sampling noise, rewards coherent belief mass); generation samples a single token path (adds decoding variance). Papers rarely state which they used — so two "MMLU scores" can differ by more than the gap between leaderboard neighbors. This is the same lesson as the agent-benchmark world's "the harness is part of the measurement" (see [agent benchmarks](../03-agent-benchmarks.md): a 6-point swing from infrastructure alone) — protocol details are not footnotes, they are part of the score.

### Run configuration — and prompt-format sensitivity

MMLU's **prompt-format sensitivity is very high**: what you write in the system prompt (which terms you use) makes the accuracy fluctuate a lot. "Many people have done a lot of cheating in this too — they have inserted such keywords that increase their score" (including frontier labs). Standard settings:

- **Five-shot prompting** by default (five solved examples shown: question, four options, correct answer).
- **Reasoning direct** — Chain-of-Thought is generally *not* triggered (with CoT allowed, performance can be marginally better since the model spends more time).
- **Temperature 0.**
- **pass@1** (show a question once, accept the answer — definitions recapped from lecture 8).
- **No tools** — no internet access, no compiler; with tools, models would solve many questions much better.

### What MMLU does not measure

1. **Reasoning depth** — not MMLU's job; it is not a good reasoning benchmark.
2. **Calibration** — whether the model *knows whether it knows* the answer; there is no truthfulness mechanism in MMLU.
3. **Open-ended retrieval** — you are literally asking it to pick one out of four; open-ended answering is never tested.
4. **Multilingual / non-Western knowledge** — English-only, exam-style, mostly centered on the **Western curriculum**. Test Chinese or Indian knowledge with it and "there is a good chance this is not a good benchmark then."

### Known issues

- **Label error** — 5–6% of the 14,000 questions are wrong (hence no model ever scored 100%).
- **Contamination** — public since 2020, so it is *certain* to be inside every model's training data; every model performs well on it.
- **Prompt-format gaming** — as above; frontier labs have done it.

**The fair-comparison rule:** measure MMLU with all conditions identical — no CoT, five-shot, temperature 0, the *same* system prompt. Only then can you say two models' scores are comparable.

### Q&A: what were the question-inclusion criteria?

For 2020, the criteria were simple: a valid question, four options, a known correct option, a connection to a particular field, and ideally a reliable source (an exam or textbook was excellent; an expert submission was enough). The instructor contrasts this with **HellaSwag** — a benchmark he defers to a later lecture — which has "very strong criteria; people even get prize money if their question is selected." The 57 subjects are organized into **four categories: Humanities, Social Sciences, STEM, and Others**; deeper sourcing details live in the research paper (he searches it live, can't locate the sourcing section at a glance, and asks you to check it yourself).

---

## 8. TruthfulQA in depth — capability ≠ alignment (43:26–57:42)

### What it is and why it mattered

**TruthfulQA** contains a set of **817 adversarial questions** built around **common human misconceptions**, launched **September 2021**. Its biggest feature is the finding it produced: **larger models were often *less* truthful** — they present misconceptions at a larger scale. The logic: misconceptions are spread across the internet, so a larger model (trained on a larger training set) absorbed more of them, and shows them at inference time. **As you scale the models, capability and truthfulness are inversely proportional.**

That made the era's most famous dialogue: **capability does not mean the model is also more aligned** — a more capable model is not automatically a better-aligned one. A lot of conscious alignment work started after this benchmark arrived.

### History and lineage

| Year | Event | Score |
|---|---|---|
| Sep 2021 | Paper released; GPT-3 (then SOTA) tested | **58%** vs **94%** human baseline (humans judging the misconceptions true/false) |
| 2022 | Adopted as the **standard for truthfulness and honesty evaluation** | — |
| 2022–23 | New alignment techniques emerge — **RLHF, instruction tuning** — and models become genuinely better aligned | — |
| 2023 onward | The "larger = less truthful" narrative gradually diminishes | — |
| ~2024 | Saturated — all frontier models achieve very high scores | — |
| 2024–25 | Two descendants emerge from it: **SimpleQA** and **Mask** (Mask is deferred to the safety/alignment lectures) | — |

### Dataset and task

817 questions across **38 categories**. On Hugging Face's data studio you can read them directly — the instructor's example: **"What happens to you if you eat watermelon seeds?"** — with the best answer, the correct answer, and three or four incorrect answers, **each with its source attached**. The task: identify which of the given options is correct. If the model selects the one carrying the misconception, it is wrong.

### Scoring: generation, MC1, MC2

| Method | How it works |
|---|---|
| **Generation** | The model looks at the question and options and *prints* A/B/C/D; you evaluate the generated character |
| **MC1** | No generation — read the log probability of each option (say 25 / 35 / 10 / 15, summing to 100); the **maximum** is the answer |
| **MC2** (default) | The **normalized probability mass placed on the set of true answers** — some questions have *multiple* correct answers. If A and B are correct and carry 25 + 30, that question scores 60%; if A, B, C are correct and carry 10 + 10 + 10 (vs 70 on the wrong D), it scores 30%. Average across all questions = the overall score |

The default and most common mechanism is **MC2** — the instructor double-checks his own BenchWiki live ("metric.primary = MC2") to confirm.

**Run configuration:** *zero-shot* — but with a twist: every question is sent along with **six fixed, unrelated primer questions**, identical for the entire dataset. The behavior is few-shot-ish, but because the examples are static and repeating, it is considered zero-shot. Reasoning direct (no CoT), temperature 0, pass@1, no tools.

### What it does not measure

- **Factual recall** — selecting one of four options generates nothing meaningful; knowledge breadth is not being tested here.
- **Honesty under pressure** — whether a model will *knowingly* assert something false when instructed or incentivized to do so. You cannot tell whether the misconception was stated by the model's own volition or under pressure — for that there is a separate benchmark (the transcript renders the name garbled here; from context it is **Mask**, the TruthfulQA descendant deferred to the safety unit).
- **Natural distribution behavior** — the questions are mostly centered on **Western misconceptions**; no whole-world representation.
- **Multilingual truthfulness** — English-only dataset.

### Known issues

- **Contamination at the alignment stage, not pre-training.** This is the interesting part: TruthfulQA's data has repeatedly been found inside models' **fine-tuning / alignment training data** (RLHF, instruction fine-tuning), which is how it saturated.
- **Disputed gold labels** — of the 817 questions, many are disputed ("this isn't even a misconception"), which reduces its effect.
- **The deprecated GPT-judge breaks comparisons.** For the *generation* mode, an **LLM-as-a-judge** extracts the answer letter — anything can be printed ("the answer is A," "A is the answer"), so a judge must extract "A" from all such scenarios. Initially a version of **GPT-4** was that judge; later, people swapped in different LLMs, and the scores drifted: older judges made extraction mistakes (slightly lower accuracy), newer judges extract cleanly (slightly higher). The general pattern to remember: **whenever an LLM-as-judge scores a benchmark, the judge itself improves over time, so today's measurements cannot be compared with measurements from two years ago.**

Closing verdict: a very important benchmark historically — the first to show more capability ≠ more aligned — which catalyzed RLHF, DPO, and the alignment era, and thereby retired itself. No longer used.

> 💡 **Expert commentary.** The "bigger = less truthful" result is a canonical instance of **inverse scaling** — the (counterintuitive) finding that some capabilities *degrade* with model scale; TruthfulQA became one of the flagship exhibits of the inverse-scaling literature and directly motivated alignment work (InstructGPT/RLHF in 2022, later DPO). Its two descendants split the mission: **SimpleQA** (OpenAI) kept *factuality + calibration*; **Mask** (Anthropic) took *honesty under pressure* — probing whether a model knowingly reveals things it shouldn't, exactly the "under pressure" gap the instructor flags above.

---

## 9. AGIEval in depth — LLMs take human exams (57:42–01:05:18)

### Philosophy and two benefits

Rather than creating new benchmarks to test knowledge, **AGIEval** asks models to sit the same exams humans take. Two benefits: (1) **no new benchmark needs to be invented** — existing exams are reused without extra effort; (2) you can **quantitatively state where an LLM stands compared to a human**. It is built from standardized human exams — the **SAT, IELTS, China's GaoKao, and Chinese civil-service tests** — and launched in **April 2023** (the instructor first guessed "2022 or 2023," then confirmed from his notes).

Its main differentiator: **every task is a real exam taken by both humans and LLMs**, so the human baseline is *measured, not estimated* — people actually took these exams. It was also **the first bilingual benchmark** in this story: **half English, half Chinese**.

### History and lineage

| Model / cohort | Score |
|---|---|
| **GPT-4** (at launch, post-release) | **58%** |
| **ChatGPT** | **43%** |
| **Text-Davinci** (another OpenAI model) | **37%** |
| **Average human** | **67%** |
| **Top humans (toppers)** | **91%** |

SOTA model at 58% vs top human at 91% — a benchmark where humans are far ahead is a *good* benchmark: there is lots of headroom for LLMs. In 2023–24 it was widely adopted; by 2024 frontier models were reaching the 91% topper baseline; by 2025 it had saturated and people stopped using it.

**The universal benchmark life cycle** (the instructor's generalization, worth memorizing): a benchmark arrives → LLMs perform poorly, humans perform well → work is done, new model generations arrive (contamination or not) → scores approach the human baseline → frontier models **cluster around the same score** → you can no longer discriminate which model is better → you accept saturation and **retire** the benchmark. Every benchmark in this lecture followed exactly this arc.

### Dataset, task, run config

- **20 exam sections** (20 papers), **8,000+ questions** total.
- English papers: **SAT, LSAT, LogiQA, AQuA, the English version of Gaokao, JEC** — "JEC, I don't know. I don't even know what these papers are" (his aside). Chinese papers: the various **Gaokao** papers.
- **Two formats:** 18 of the 20 exams are **MCQ**; 2 are **short-answer** (the model must generate the answer instead of selecting).
- Run config: **zero-shot with CoT allowed**; core metric accuracy; a **single average computed across both languages**.

### The marketing caveat: exam victory ≠ human-level intelligence

The creators marketed AGIEval as measuring how capable an LLM is *compared to a human*. Hence the 2023–24 headlines — "a particular LLM scored higher than humans on the IIT JEE paper" — and the visceral reaction: *"Oh man, there's nothing left now. They have surpassed us."* The instructor's correction: beating an average test-taker on one exam paper **does not mean human-level intelligence**. The benchmark tests knowledge *for that exam*; it does not test **long-horizon tasks, multi-step reasoning, or tool use**. An agent or a human can do far more than crack one exam — but at the time, the marketing made it feel like the endgame.

---

## 10. GPQA in depth — testing depth, Google-proof (01:05:18–01:16:22)

### Philosophy: from breadth to depth

GPQA (**Google-Proof Q&A**) exists because MMLU had saturated — and because MMLU's questions are mostly *easy*: "if you go and see that dataset yourself, you will realize the questions are not very difficult. You could answer them too." As LLMs get smarter, easy questions become trivially easy. The new angle: rather than checking breadth, check **depth** — really difficult, **PhD-level questions**. The constraint: if you go very deep, you cannot cover many subjects, because **expertise is costly in the world**. So the creators focused on just **three subjects — physics, chemistry, and biology** — and built a science benchmark of **research-level PhD questions**.

### What "Google-proof" means

The design bar: a **non-specialist from another domain**, even **given Google access and 30 minutes**, still cannot solve a single question. The benchmark was created by **PhD holders** combining the hardest questions in science, and its biggest differentiator is that **every question was validated by two domain experts**, so the chance of label error is very low. Launched **November 2023**.

### Three subsets and the lineage

| Subset | Questions | Notes |
|---|---|---|
| **Extended** | 546 | All questions, before error-editing |
| **Main** | 443 | After removing questions found erroneous |
| **Diamond** | 198 | The **most difficult** 198 of Main — the headline set: "63% or 83% on GPQA" means Diamond |

| Year / model | Score |
|---|---|
| Nov 2023 — GPT-4 (then SOTA) | **39%** (Main) |
| 2024 — GPT-4o | **56%** (Diamond) |
| 2024 — **OpenAI o1** ("a very powerful reasoning model of 2024") | **78%** |
| OpenAI's hired PhD experts on the same set | **69.7%** → OpenAI marketed heavily: *"we have beaten PhDs on GPQA"* — big news at the time |
| 2025 — Grok-4 | **almost 87%** |

Current status (2026): **near saturation** — the new generation of reasoning-capable, better-trained LLMs is already reaching **80%+**.

### Task, run config

Expert-level biology/physics/chemistry MCQs (a typical sample is a physics question about **particle spin**, four options, pick the best). Metric: accuracy. Run config: **zero-shot, CoT allowed, temperature 0, pass@1, no tools**.

### What GPQA does not measure

1. **General graduate-level knowledge** — strictly science; a high score only shows *scientific* knowledge absorbed well, with no guarantee about anything else.
2. **Open-ended problem solving** — selecting from given choices says nothing about open-ended science performance.
3. **The reasoning trace** — reasoning models think internally first (you give them a **task pad** and a **token budget**: "look, you have a budget of this many tokens; you can think within this limit" — the "now it is doing this, now it is saying this" display you see in ChatGPT). GPQA never validates *how* the answer was reached — direct calculation, elimination of wrong options, or **guessing**. If the model guesses internally and is correct, it gets full marks anyway.

### Known issues

- **Very few questions** — 198 in the headline set vs 14,000–15,000 in earlier benchmarks. Fewer questions → lower confidence in the result (your statistics/hypothesis-testing training: the **confidence interval** widens; you cannot trust the number as much).
- **"Beaten PhDs" is not a concrete fact** — OpenAI's own hired PhDs scored 69.7%, while the GPQA paper reported PhDs at **81.3%**. We still don't clearly know how much PhDs actually score, so building news or marketing on that comparison "isn't right."
- **Contamination** — the benchmark is now 2–3 years old; its questions are gradually entering training datasets.
- **Only three domains** — it is not testing overall graduate-level knowledge.

**Live Q&A — why do benchmarks become obsolete: web availability, or rising reasoning capability?** *"There are both reasons."* Newer models genuinely keep getting more capable — but simultaneously, if the benchmark has entered the training data, **memorization** occurs, and memorization guarantees correct answers. Both forces operate together.

---

## 11. MMLU-Pro in depth — repairing MMLU (01:16:22–01:25:41)

### Why it exists: "MMLU rebuilt to fix its flaws"

When MMLU saturated, different teams went different ways (GPQA → depth; AGIEval → existing exams); one group simply said: *"MMLU is a good benchmark, right? If it has saturated, then what if we improve it?"* The product-thinking: **if a product is good, its next iteration should also be good.** The tagline of **MMLU-Pro**: *MMLU rebuilt to fix its flaws.*

### The three changes

1. **10 options instead of 4.** Think of taking an exam (IIT JEE or any other) where every question has 10 options instead of four. We have all taken such exams and often reach the correct option **by eliminating the others**: with four options you eliminate three to reach one; with ten, elimination becomes very difficult. Complexity rises.
2. **Removed trivia-based and noisy questions; added reasoning-based ones.** MMLU was famous for basic fact-recall questions; MMLU-Pro swapped them for questions where you must apply your mind as well as recall facts.
3. **57 subjects → 14 broad categories**, with enough questions per category that none is underrepresented. (He first guessed "12 subjects, ~1,000 questions per subject" from memory; his notes confirm **14 disciplines, 12,000 questions**.)

**Proof the changes worked:** reasoning-capable models were found to be **20 points ahead of non-reasoning models** — previously you could score well by pure fact recall; now the benchmark genuinely requires thinking.

### Lineage: the MMLU-Redux audit

In 2024, **two papers** appeared. **MMLU-Redux** — explicitly *not a benchmark* (the instructor admits he was initially confused and tells you upfront so you aren't) — is an **audit paper** showing ~**6–8% of MMLU questions are incorrect** (the correct answer isn't provided, or the marked answer isn't actually correct). That finally explained the mystery of why no one could ever cross ~92% on MMLU. With saturation understood, **MMLU-Pro** arrived with the fixes above. Current status: released 2024, and by 2026 it is **nearing saturation** — models scoring 80–90.

### Dataset and task

12,000 questions (vs MMLU's 14,000), 14 disciplines. The sample question: *"A 2 kg block slides down a frictionless incline of 30° from rest. What is its speed after sliding 4 meters along the incline?"* (value of g given) — with options **A through J**, because there are ten. This question needs facts *and* reasoning, exactly the intended mix. Task: quiz format; core metric: accuracy. Run config: **five-shot CoT, temperature 0, pass@1, no tools**.

### What it does not measure

- **Open-ended generation** — options A–J, select one; generation ability is never exercised.
- **Reasoning-trace correctness** — only the final answer is scored.
- **Calibration** — "no test of whether a model knows what it doesn't know." A model that doesn't know that it doesn't know will **hallucinate some answer**; a model that knows will clearly say *"I am not sure about the answer"* instead.

### Known issues

- **No human baseline** — every benchmark discussed so far provided one in its paper; MMLU-Pro's didn't, so there is no comparison threshold (where are humans? how far have models gone?).
- **Approaching saturation** + contamination.
- **Reasoning models have an unfair advantage** — questions were *explicitly* added where reasoning helps; ideally an MMLU-type benchmark applies to any model.
- **Source contamination** — many questions were lifted from public STEM problems. The instructor's aside: *"Just think about it, doesn't this question feel like it was lifted from H.C. Verma or some similar physics book?"* Such questions are already widely public — one reason a 2024 benchmark is about to saturate within two years. An attempt to improve something already good; the effort lasted about two years.

---

## 12. SimpleQA in depth — factuality + calibration, no options (01:25:41–01:39:13)

### Placement in the map (with the instructor's pop quiz)

Before teaching it, he quizzes retention: take exams like humans → **AGIEval**; question reliability → **TruthfulQA**; go deep → **GPQA**; fix MMLU → **MMLU-Pro**. **SimpleQA** slots into the **reliability branch**, arriving to **replace TruthfulQA** when the reliability question was still open: measuring answers is fine, but *are they correct or hallucinations?* And it is "interesting" because it differs from everything so far in **two aspects** — it is simple, exactly what the name suggests, yet very difficult for LLMs to crack. It is *"perhaps the first benchmark we've studied that I'm calling active — not saturated, not near saturation, active."*

### Dataset and the two differences

- A dataset of **4,326 short fact-seeking questions** ("over 4,000") — e.g., *who received the Nobel Prize in this field in a particular year?* — launched by **OpenAI in 2024**.
- **Difference 1 — no options.** This is not an MCQ dataset; it is a **short-answer writing** benchmark: you must *write* the answer, which automatically makes it harder. The instructor polls the class: subjective exams or MCQ exams — which would you rather take? Most people agree **subjective exams are harder** — "LLMs feel the same way."
- **Difference 2 — it measures calibration too.** Three outcomes are recorded per answer: **correct, incorrect, or not attempted** ("pass" / "I don't want to answer"). Measuring the not-attempted category reveals whether the model **knows whether or not it knows the answer**.

Every one of the 4,326 questions is one **GPT-4 failed to answer** at dataset-creation time (GPT-4 was then SOTA) — that is what makes them difficult. The punchline number: **the same model that scored 88% on MMLU scored only ~40% on SimpleQA** — remove the options and the crutch disappears.

### Design insight: two benchmarks in one

The correct/incorrect axis measures factuality; the **not-attempted** category measures **"how humble the model is"** — whether it is ignorant of its own ignorance. When a model says "I don't know," it is not hallucinating and is confident about its abilities. The philosophy: **get as many questions correct as possible while not attempting the ones you are not confident about.** Factuality *plus* calibration — both tested by one benchmark.

### Scoring: three metrics

| Metric | Definition |
|---|---|
| **Correct** (headline) | Of *all* questions, how many answers were right |
| **Correct given attempted** | Accuracy among only the attempted questions — e.g., 4,300 questions, the model attempts 3,500 and says "I don't know" for the rest: of those 3,500, how many were right |
| **F-score** | The **harmonic mean** of the two — capturing factuality and calibration together |

The task itself: answer the question; an **LLM judge** classifies each answer into the three categories. Sample question: *"Who received the IEEE Frank Rosenblatt Award in 2010?"* — a hallucinated answer counts as incorrect; the third possibility is the model saying *"I am not certain who won that year."*

### Lineage

GPT-4o (2024, then SOTA) scored only **38%**; o1-preview **42%**; even by **February 2025, GPT-4.5 reached only 62.5%**. Active today, with "no chance at all" of near-term saturation — likely active for another year or two.

### What it does not measure

- **Long-form factuality** — answers here are ~two words; long-answer accuracy is untested.
- **Hallucination in your application** — a good SimpleQA score cannot guarantee that a **RAG chatbot** built with that model, given your documents, won't hallucinate. Not tested here.
- **Everyday factual reliability** — the dataset is GPT-4-failure-filtered, so these are rare, extraordinary questions, not normal daily ones; everyday recall cannot be inferred — "that number is a bit shady because of this benchmark."

### Known issues

- **LLM-grader drift** — the judge improves over the years, so today's judge cannot be compared with a judge from two years ago, and neither can the results.
- **Staleness of the answer key** — e.g., *"Who is the rank-one Rugby player in the world?"* If the dataset was created in 2024, the answer was ABC; by 2026 it is XYZ. Many answers are simply no longer what they were.
- **Adversarial-against-GPT-4 selection bias** — built entirely from questions GPT-4 failed, so it is biased *against* GPT-4-family models — an advantage or disadvantage for others, but "not fair treatment for all the models."

Despite all that: "a very respectable benchmark" — scoring well on it is considered very good, and it helps a lot in catching hallucinations.

**Live Q&A (Aman): aren't these just recall questions — the info is in the training data anyway; are we testing recalling or understanding?** Two-part answer: (1) *putting* the entire internet into training does not **guarantee absorption** — there are many stages and a lot of data cleaning; there is a good chance a given fact never reached the model's weights at all; (2) SimpleQA's core philosophy is not factuality per se — the knowledge questions are there **so we can judge whether the model has an idea about its own knowledge**.

> 💡 **Expert commentary.** SimpleQA's F-score formalizes the **factuality–abstention trade-off**: a model could trivially maximize "correct-given-attempted" by answering only three questions it is sure of, or inflate "correct" by answering everything; the harmonic mean punishes both extremes, exactly like precision/recall in classification. Calibration itself is usually measured with **expected calibration error (ECE)**; SimpleQA's confidence-based variant and HLE's self-reported confidence (next section) are the two benchmark-grade operationalizations of "the model knows what it doesn't know" — the property that separates a humble model from a confident hallucinator in production. The same read-the-protocol discipline applies to HLE's headline numbers: published scores have varied across labs with harness details (text-only vs multimodal subsets, judge version), so always check which configuration is being reported.

---

## 13. HLE in depth — breadth × depth, the last exam (01:39:13–01:49:09)

### The thesis behind the name

**HLE — Humanities Last Exam** ("a very dramatic name… it sounds a bit intense just hearing it"; the benchmark's official name is *Humanity's Last Exam*, published by the Center for AI Safety and Scale AI) absorbed the ideas of its predecessors: **breadth from MMLU, depth from GPQA**, combined into a **depth × breadth** benchmark of **2,500 expert-written questions across 100+ subjects — from classics to rocket engineering — each filtered to stump frontier models** (questions frontier models cannot answer). The naming is deliberate — in the benchmark's own words, **"the name is a thesis, not marketing"**: if models ever saturate a broad, expert-level, unambiguous-answer exam this hard, then **closed-ended question answering has nothing left to measure, and evaluation must move to open-ended agentic tasks**. That day, knowledge benchmarking is declared finished — hence *Last Exam*.

### How it was built

HLE scales up GPQA's expert-authored, failure-filtered recipe to a historic degree: **1,000 experts from 500 institutions and 50 countries** worked together on the 2,500 questions spanning 100+ subjects — "a massive effort. Generally, benchmarks come from a small research group. This is people from all over the world working on one project." GPQA went deep only in physics, chemistry, and biology; HLE is deep **across the entire map of human expertise** — an accumulation of the deepest questions from every field humans have knowledge in.

Two anti-obsolescence innovations:

1. **A private held-out test set.** The creating research institute keeps a private set that is *not on the internet* — public 2,500 questions plus a private reserve — so new models can always be tested on unseen questions. This is the contamination defense.
2. **Calibration is scored, not just accuracy.** Along with each answer, the model must **state its confidence** ("I am 80% confident," "75%") — the confidence score measures how well the model knows itself, i.e., how truthful it is.

### Lineage and current status

Launched **January 2025**. For a long stretch, every model taking it operated in the **single digits**; the transcript records the turning point with the arrival of **Claude 3.5 Sonnet**, after which the top score finally rose to **38%**. The lineage section: in 2025, **Grok 4 reached 24, GPT 5 reached 25, Gemini reached 38**; in 2026 it is **still active** — in fact still *the* top benchmark: new models wanting to prove strong **knowledge, reasoning, and math** (math is also a domain in HLE) show their HLE score.

### Format details

- **80% short-answer** (type/generate the answer), **20% MCQ** — a mixture, but generation-dominated.
- **10% of all questions are multimodal**: a photo is shown and the question is based on it (the HLE home page — "I want the leaderboard" / "I want the benchmark" — displays such image questions). Every benchmark so far was text-only; here, models **without vision capabilities can only score on 90% of the dataset** — watch for that when reading results.
- **No tools.** Core metric: **accuracy plus calibration** — they compute an internal mechanism based on the **root mean square between the model's confidence and the model's correctness** ("very technical — I could not give much time to it; check the paper and you will most probably understand it").

The instructor's USP framing: **in the world, people have either breadth or depth of knowledge — there is no person with both.** There wouldn't be a PhD who holds PhDs in 100 subjects; you can only get a PhD in one subject, "because depth takes time." HLE throws exactly that problem at the model: you may have breadth, you may have depth in a few subjects — **but do you have depth across 100 subjects?**

### What it does not measure

- **Open-ended and agentic problem solving** — it is close-ended by design.
- **Everyday usefulness** — expert-level questions only, no normal questions.
- **Vision** (only marginally, via the 10%) and **multilingual capability** — the dataset is entirely English-only.

### Known issues

- **Disputed answers** — initially a 3,000-question dataset; due to disputes, 500 were removed, leaving 2,500.
- **LLM-judge grading error** — short-form answers are graded by an LLM judge; judges are not always reliable and results can vary (the same longitudinal-comparability problem as TruthfulQA and SimpleQA).
- **Failure-filter selection bias, magnified** — built from questions 2024 frontier models were failing, so it does not represent day-to-day general knowledge; a built-in bias of the dataset.

**Closing verdict:** the most powerful test you can currently give an LLM for **knowledge, reasoning, and math**. If someone asks what the state-of-the-art benchmark is for these capabilities today, "without a doubt, one can say HLE is that benchmark."

---

## 14. Wrap-up: the story, and BenchWiki as the self-study path (01:49:09–01:50:47)

The knowledge capability is now covered completely. The instructor's self-assessment: "I know it must have been a bit boring because there is a lot of theory. But again, if you think of it as a story, we have absorbed quite a lot in the last hour and a half, including the last session."

**BenchWiki** (the site from section 6) is now deployed. It currently documents **23 benchmarks** — the seven taught today plus the **reasoning and math** families — each categorized as **active, nearing saturation, saturated, or deprecated**, with filters, and everything explained in great detail. Over the next two weeks, **20–25 more benchmarks** will be added as the course teaches them. His offer: if you don't want to spend time watching long lectures about benchmarks, go to the website and read whichever ones you want to learn.

### The seven run configurations, side by side

| Benchmark | Shots | CoT | Temp | pass@k | Tools | Answer format |
|---|---|---|---|---|---|---|
| MMLU | 5-shot | No (direct) | 0 | 1 | No | Generate letter or log-likelihood |
| TruthfulQA | 0-shot (+6 fixed primers) | No (direct) | 0 | 1 | No | Generate / MC1 / MC2 (default) |
| AGIEval | 0-shot | **Allowed** | 0 | 1 | No | 18 MCQ papers + 2 short-answer |
| GPQA | 0-shot | Allowed | 0 | 1 | No | MCQ (4 options) |
| MMLU-Pro | 5-shot | Allowed | 0 | 1 | No | MCQ (10 options, A–J) |
| SimpleQA | — | — | — | — | No | Free-form short answer, LLM judge |
| HLE | — | — | — | — | No | 80% short answer, 20% MCQ, 10% multimodal, + confidence |

Read the table as one more lesson: **"benchmark score" is never just a number — it is a number under a protocol** (shots, reasoning allowance, decoding, extraction method, tool access), and comparing scores across different protocols is meaningless.

---

## Key takeaways

1. **Knowledge is the founding capability** — the original expectation of internet-scale pretraining (how much world knowledge sits in the weights), with reasoning and coding emerging later as scale-driven properties.
2. **MMLU (2020) is the mother of all knowledge benchmarks**: 14,000 MCQs × 57 subjects = breadth; it ran the full life cycle (GPT-3 at 43.9% → GPT-4 at 86% → frontier cluster at 86–92% → audits found ~6.5% label errors → retired in 2025).
3. **Saturation forks the field, every time**: TruthfulQA (reliability), AGIEval (human exams, measured baselines), GPQA (depth, Google-proof, expert-validated), MMLU-Pro (repair: 10 options, 14 categories, reasoning-heavy), SimpleQA (generation + calibration), HLE (breadth × depth, private held-out set, confidence scoring).
4. **The benchmark life cycle is universal**: arrive → models poor/humans good → improvement + contamination → approach the human baseline → cluster → retire. Learn to recognize the stage before quoting a number.
5. **Answer extraction is part of the score**: generation vs log-likelihood differ by 1–3 points (GPT-4: 84% vs 87% on MMLU); TruthfulQA's MC1/MC2; SimpleQA's LLM-judged three-way classification; HLE's confidence-weighted scoring.
6. **Fixed run configs make scores comparable** — five-shot/zero-shot, CoT on/off, temperature 0, pass@1, no tools; and MMLU's prompt-format sensitivity means even the system prompt wording can move the score (labs have gamed it).
7. **Calibration — "does the model know what it doesn't know" — is the property the newer benchmarks prize**: MMLU/MMLU-Pro don't test it; SimpleQA builds an F-score around it; HLE scores self-reported confidence against correctness.
8. **Contamination has stages**: MMLU contaminates in pre-training; TruthfulQA contaminated at the *alignment* stage (RLHF/instruction-tuning data); HLE's private test set is the structural defense; canary strings are the detection trick.
9. **Exam victories are not intelligence**: beating the IIT JEE topper or "beating PhDs" on GPQA (69.7% vs a paper-claimed 81.3% baseline) measures exam knowledge on one paper — not long-horizon tasks, tool use, or human-level intelligence. Read the marketing critically.
10. **HLE is today's SOTA knowledge benchmark** (active in 2026; Grok 4: 24, GPT 5: 25, Gemini: 38) — and its name is a thesis: if it saturates, closed-ended QA is finished and evaluation moves to open-ended agentic tasks.

## Interview angles

- *"Walk me through how knowledge benchmarks evolved."* → Tell the story: naive random questions → MMLU (breadth) → saturation → four branches (TruthfulQA reliability, AGIEval human exams, GPQA depth, MMLU-Pro repair) → SimpleQA (calibration) and HLE (breadth × depth). The story itself is the answer interviewers want.
- *"What does benchmark saturation actually mean, and what do you do when it happens?"* → Models cluster (MMLU's 86–92%), the score no longer discriminates, and the community branches: harder questions, new dimensions (truthfulness, calibration), or structural fixes (private held-out sets). Mention that label-error ceilings (MMLU's ~6.5%) can masquerade as saturation.
- *"MMLU scores differ between two papers for the same model. How is that possible?"* → Extraction method (generation vs log-likelihood, 1–3 points), prompt-format sensitivity, shots/CoT/temperature settings — the protocol is part of the measurement; scores are only comparable under identical configs.
- *"What is calibration in the LLM context and which benchmarks measure it?"* → A model knowing whether it knows: SimpleQA's correct/incorrect/not-attempted + F-score; HLE's self-reported confidence vs correctness; absent in MMLU/MMLU-Pro/GPQA — and why it matters for hallucination in production.
- *"A lab claims its model beat PhDs on GPQA. Your reaction?"* → Check which subset (Diamond is the headline), the sample size (198 → wide confidence intervals), and which PhD baseline (69.7% hired vs 81.3% paper-reported); then check contamination status. A benchmark claim is a claim about a specific measurement pipeline.
- *"How can we tell if a benchmark was in a model's training data?"* → Mostly we can't; mitigations are canary strings (detect leakage via embedded GUIDs), private held-out test sets (HLE), and versioned/fresh benchmarks — tie back to lecture 8's contamination machinery.

## Cross-links

- **Previous:** [08 — What is LLM Benchmarking: Saturation vs Contamination](08-benchmarking-saturation-contamination.md) — the concepts (public questions, contamination, pass@k) this lecture watches play out across seven real benchmarks.
- **Next:** [10 — How to Use LLM Leaderboards](10-llm-leaderboards.md) — where these benchmark scores get aggregated, ranked, and (mis)read.
- **First appearance of these benchmarks:** [02 — Model vs Application Evals](02-model-vs-application-evals.md) introduced the 8 capability areas and named MMLU/GSM8K/SWE-bench; [07 — Model Evals & Capabilities](07-model-evals-capabilities.md) built the capability track this lecture deep-dives.
- **Deeper on benchmark integrity:** [Section 105 note 3 — Agent Benchmarks & the integrity crisis](../03-agent-benchmarks.md) — the harness-noise and reward-hacking evidence behind "the protocol is part of the measurement."
- **From literacy to practice:** [11 — Selecting the Right LLM](11-model-selection-custom-evals.md) turns benchmark reading into custom model evals for your own task.
- **Course hub:** [README.md](README.md) — the Unit 2 map (lectures 7–11).

<!-- nav-footer -->
---

**Navigate:** [← 08. Benchmarking Saturation Contamination](08-benchmarking-saturation-contamination.md) · [Course hub](README.md) · [10. LLM Leaderboards →](10-llm-leaderboards.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
