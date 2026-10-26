# 13 — Testing RAG Retrievers (Hands-On)

> **Lecture 13 of 19** · Unit 3: RAG Evaluation · 1:47:02
> How to Test RAG Retrievers (Hands-On) (CampusX, LLM Evaluations playlist)
> [Course hub](README.md) · [Transcript](transcripts/13-testing-rag-retrievers.md)

---

## What this lecture covers

Lecture 12 set the problem statement — a RAG doubt-solver chatbot whose knowledge base is the course's own lecture transcripts — and drew the step-by-step evaluation roadmap. The next three lectures (including this one) execute that roadmap and assemble a **RAG eval suite**: the application gets evaluated at **three levels**, and all the evaluation pipelines built along the way are collectively called the eval suite, which will later power **regression testing** (lecture 18).

| Level | Question it answers | Where |
|---|---|---|
| **Component** | Is the retriever good? Is the generator good? | **This lecture** (retriever) → lecture 14 (generator) |
| **Pipeline / workflow** | Does retrieve → generate work end to end? | Lecture 14 |
| **Application** | Is the whole product good — quality, safety, operations? | Lectures 15–19 |

This session is a full code-along that completes the component level, retriever half:

1. **Project setup** — a standardized `RAG Eval Project` directory (data / src / evals / goldens), UV environment, dependencies.
2. **Build the retriever** — `retriever.py` line by line: transcripts → timestamp stripping → chunking → Chroma → retriever with k = 5, plus a smoke test.
3. **The theory** — the two failure modes of a retriever, the two metrics they spawn (**recall**, **precision**), the k trade-off between them, and why both are reference-based.
4. **The wrong method** — a golden dataset of chunk IDs — and exactly why it collapses for this application.
5. **The right method** — a golden dataset of **ideal answers**, judged claim-by-claim by an LLM: **contextual recall** (the RAGAS technique) and **contextual precision** (DeepEval's rank-aware version).
6. **Golden dataset creation** — four ways, with a live (and honest) demo of DeepEval's Synthesizer.
7. **The eval pipeline and the improvement loop** — DeepEval's three-part pattern, `eval_retriever.py`, and a real tuning session that takes the retriever from **0.80 / 0.80** to **~0.95+ recall / ~0.85 precision**.

If you keep one mental model from this lecture: **don't test which chunk IDs came back — test whether what came back covers the ideal answer.**

---

## 1. Where we are: from roadmap to eval suite (00:00–02:50)

The session picks up exactly where the previous one ended: the problem statement (what kind of RAG application we will build) and the complete roadmap for evaluating it step by step were both set in lecture 12. Going forward, across the next three classes, the goal is to build the **RAG eval suite** — evaluating the application at the **component level**, the **pipeline (workflow) level**, and the **application level**.

Today's goal is the first part: the component level. The two most important components of any RAG application:

| Component | Job |
|---|---|
| **Retriever** | Fetch relevant context from the vector database for a given query |
| **Generator** | Produce an answer relevant to the question, given the query and the relevant context |

We have certainly *built* these components in past courses — but we never learned how to *evaluate* them. Today we do, starting with the retriever, then (next class) the generator.

---

## 2. Project setup: the RAG Eval Project (02:50–08:39)

Since this project will run for the next two–three classes, setting it up properly is worth the time. A new folder — **RAG Eval Project** (under Documents/Work) — opened in VS Code, following "completely standardized project setup instructions." The directory structure comes first, so files are never created randomly:

| Folder | Purpose |
|---|---|
| `data/` | The data of all lecture transcripts — the **knowledge base** of the RAG application |
| `src/` | Every file used to *build* the application — retriever, generator, RAG pipeline, and later perhaps a Streamlit app |
| `evals/` | All the **evaluation pipelines** — the retriever eval, the generator eval, the whole-pipeline eval |
| `goldens/` | The **golden datasets** |

**The transcripts.** Eight lectures exist so far, so the instructor copies the transcripts of the first eight sessions into `data/` (this being roughly the ninth session, he allows he might have missed one or two — no matter). Each transcript looks "just like movie subtitles": a timestamp, then what the teacher or students said at that time — long files, because these are two-hour lectures. This is the knowledge base the RAG chatbot will work on.

**The environment.** A new project needs dependencies isolated rather than installed globally, so he uses **UV**, initializing with **Python 3.11** and installing all libraries together:

| Library | Why it's needed |
|---|---|
| **LangChain** | "A lot of the work will be done through LangChain" |
| **OpenAI** | The OpenAI API (embeddings + judge LLM) |
| **DeepEval** | "We will do our testing through it" |
| **Pytest** | A dependency of DeepEval |
| **python-dotenv** | Working with environment files |

UV sets the whole project up quickly — `pyproject.toml` and `.gitignore` appear. One last step: a **`.env`** file holding the **OpenAI API key** (he pauses the screen share while copying it). With that, the basic steps are done and the session proper begins.

---

## 3. The development philosophy: build, test, then move forward (08:39–10:28)

The rule from the last session, restated as the organizing principle of the next three lectures: **you never build the entire application first and then test it.** You operate exactly like software development — build a new module, write a new function, *test it*, then move forward and test the next thing. Applied here:

> Build the **retriever** → evaluate it → when satisfied, build the **generator** → evaluate it → build the **pipeline** → evaluate it → once the application exists, do **application-level** evaluation. "This is how you develop an LLM-based application."

So the first move is building the first component. What is a retriever, mechanically? A component that **receives a query as input**, converts it into a vector **with the help of an embedding model**, and searches for that vector in a **vector database** where our chunks are already stored in vector form. It fetches the five or ten nearest vectors — that set is what we call our **context**. The full setup to create now: fetch the documents (the transcripts), chunk them, embed them, and create the retriever object we will use whenever we run or evaluate the retriever.

---

## 4. Building the retriever: `retriever.py`, line by line (10:28–19:07)

The instructor shows the reference project (same folder structure: data, evals, golds, src — he had already built this project entirely in another location and copies from there as-is) and pastes `retriever.py` into `src/`. It is deliberately simple code — "you will understand it instantly":

- **Imports + `load_dotenv`** — the OpenAI key comes from the environment file.
- **Data and store directories** — `data` for the transcripts, and a `chroma_store` directory for the vector database. It doesn't exist yet; it gets created the moment the code first runs, and all chunks in vector form will live in it.
- **`build_retriever()`** — the entry point, which calls…
- **`load_store()`** — brings in the embedding model, **`text-embedding-3-small`** (OpenAI's embedding model), and checks whether the vector database already exists: if it does, reuse it; if not, create a new one.
- **`load_transcripts()`** — the creation path. It enters the directory inside `data/`, loads **all `.vtt` files** (every transcript has the vtt extension), and reads them **line by line** with one question per line: *does this line contain timestamps?* If yes → ignore it. If no → keep appending it to the text.

Why strip timestamps? "If we keep the timestamps, the quality of our retriever will be very poor" — text, then a sudden timestamp, then text again means "the task of capturing the semantic meaning won't be done well." So a **filter removes the timestamp lines** and the normal text is stored inside a **LangChain document**. Crucially, the document's **metadata records which session each line was spoken in** — so the chatbot can later provide a citation: *the answer to your question was taught by the sir in this session.*

- **Chunking** — chunk size **750**, chunk overlap **100** ("let's assume for a moment that we start with something small").
- **Vector store + retriever** — a **Chroma** database via `from_documents` (chunks + embeddings), then `as_retriever()` to create the retriever object, with **k set to 5**.
- **Invocation** — give the retriever any question; it converts the question into vectors, goes to the vector database, fetches the **five nearest vectors** into a result variable, and loops through to display them.

| Parameter | Value |
|---|---|
| Embedding model | `text-embedding-3-small` (OpenAI) |
| Vector store | Chroma, persisted in `chroma_store/` |
| Chunk size / overlap | 750 / 100 |
| k | 5 |
| Documents | 8 session transcripts (.vtt, timestamps stripped, session metadata attached) |

**Smoke test (17:18).** The question: *"What is regression testing?"* — explained in detail in the previous session, so the retriever should find it. The first run takes time because the vector database is being created from scratch. `chroma_store` appears, and five chunks come back — one visibly on-topic: *"you get into regression testing. So there is nothing special in regression testing. Basically the eval suite you have made. Run it once."* Verdict: **we have built our retriever — it is working.** How *well* it works is exactly what we have not evaluated yet.

---

## 5. Housekeeping: document changes, and why the code is deliberately simple (19:07–20:28)

A student asks: **how do we handle changes to the document?** Say session 10's transcript arrives — you paste it into `data/`, then (with the current setup) you must **delete the `chroma_store` folder and run `retriever.py` again**, re-embedding and re-vectorizing the documents. Every document change repeats this step. Ideally, the instructor agrees — "Is that correct, Saurav?" — **data ingestion and retrieval should be decoupled**; but right now the focus is the evaluation side, not application development.

His explicit disclaimer: don't expect production-grade code. "I am simplifying it on purpose. If I write too much production-grade code here, then I will spend all my time explaining what is happening… when I had Claude generate the code, my instruction was to include very basic level code that anyone could understand at a glance. So it's a conscious choice." (Note the admission: the code was **Claude-generated** under exactly that instruction.)

---

## 6. How a retriever fails: the two failure modes (20:28–24:59)

Before writing evaluation code, a discussion — because understanding *how a retriever fails* tells you what to measure. A retriever is a **function**: you give it a query, and in output it gives you five (or ten) relevant contexts. If someone asks "in what scenarios does a retriever fail?", there are ideally **two scenarios**, worked through with chunks numbered 1–100 in the vector database and a question "ABC" whose correct answer is hidden in chunks **1, 13, and 15**:

| # | Failure mode | Example | Consequence |
|---|---|---|---|
| 1 | **It could not fetch the correct context** | The retriever returns 27, 28, 29 — not a single relevant chunk | The evidence never reaches the generator at all |
| 2 | **It brings the right context but it is noisy** | The retriever returns 1, 13, 27, 28, 29 — two correct chunks plus three useless ones | The generator receives information **plus noise**, "so there is a good chance that the answer that finally comes out won't be good" |

Around these two failure modes sit **one metric each** (both discussed in the past — lecture 05):

- To measure **how many correct contexts the retriever was able to bring** → **recall**.
- To measure **how many of the contexts it brought are actually useful** → **precision**.

An ideal retriever does neither of the two bad things: it fetches all the needed context *and* brings no noise.

---

## 7. Recall, precision, and the k trade-off (24:59–28:52)

The formal definitions, in the instructor's words:

- **Recall** — out of all the correct contexts that exist in our vector database, how many was the retriever able to bring? There were five correct ones and it brought three → recall = **3/5**.
- **Precision** — out of the contexts it brought, how many were correct? It brought five and only two are useful → precision = **2/5**.

```
recall    = (# relevant chunks retrieved) / (# relevant chunks that exist)
precision = (# relevant chunks retrieved) / (# chunks retrieved)
```

The closer recall and precision are to **1**, the better the retriever. But there is a problem: **a tension — a trade-off — between recall and precision**, and it runs straight through **k**:

1. Suppose recall is **0.6 (3/5)** — the retriever fetches only three of the five correct contexts.
2. What is the quick hack to improve recall? **Increase k.** It is 5 now; make it 10, and "there is a good chance that you will also get the remaining two."
3. **Increasing k always increases recall** — but as soon as k = 10, precision takes the hit: now five of the ten are correct and five noisy ones have come in.
4. So as recall moves toward 100%, **precision starts moving toward zero** — "the number itself trades off between precision and recall," and taking both up "is a bit of a tricky task."

> 💡 **Expert commentary.** The recall/precision pair derived from the two failure modes is the classic information-retrieval duo — but as plain set-based ratios both are **rank-blind**: neither cares *where* in the top-k the good chunks sit. The IR position-aware alternatives are **MRR** (reciprocal rank of the first relevant chunk — use it when only the first hit matters), **nDCG@k** (graded, log-discounted gains — use it when ranking quality across the whole list matters), and **MAP** (a running precision averaged over ranks — exactly the calculation the instructor does by hand in section 14). This lecture's contextual precision is MAP's LLM-judged cousin. On choosing k in production: it is usually bounded by the *generator's* effective context budget, not by retrieval metrics alone — a 95%-recall k = 10 is worthless if the generator only attends to the top two or three chunks (the lost-in-the-middle effect from lecture 04).

---

## 8. Both metrics are reference-based (28:52–30:59)

Next, a true/false question to the class: *the process of evaluating recall and precision is a reference-based eval.* The answer: **yes**. Reference-based evaluation requires a **golden dataset / golden answer** at evaluation time; reference-free evaluation needs none (lecture 05's distinction). Here, to say whether recall is low or high, **you must know what the correct context looks like for every query** — which means specifying a golden context per query, which makes it reference-based.

"I could have skipped this point if I wanted to. But it is very important": to really understand the many evaluations of the next three classes, you must be clear in your mind about **which evaluation is reference-based and which is reference-free**. These two metrics today are reference-based — they will need a golden dataset and a golden context.

---

## 9. The tempting method: a golden dataset of chunk IDs (30:59–36:05)

So how exactly are the two numbers calculated? The step-by-step process starts with the golden dataset — and for now, park the question of *where it comes from*; just assume it exists. It has **two columns: the question, and the document/chunk ID**:

| Question | Golden chunk IDs |
|---|---|
| What is regression testing? | 72, 89, 100 — after studying all chunks, these are the only ones that discuss it |
| What is RAG Triad? | 120, 111 |
| What are online evals? | 151, 121, 130 |

…around 50 questions like this, each with the IDs of the chunks where its context lives. Then the evaluation loop:

1. **Feed question 1 to the retriever** (k = 5). It returns **72, 81, 89, 99, 100**.
2. **Recall for this question:** of those that should have come, how many did? 72 came, 89 came, 100 came — all three of three → **recall = 1**. "For this question, our retriever is behaving perfectly."
3. **Feed question 2** ("What is RAG Triad?"). The retriever returns **1, 2, 3, 120, 5**. Needed: 120 and 111; only 120 arrived → **recall = 1/2 = 0.5**.
4. Repeat for all 50 questions, then **average** → the **average recall value**.
5. **Precision works the same way:** question 1 → five chunks came, three correct, two noisy → **3/5**; question 2 → only one correct, four noise → **1/5**; average over every row → the **average precision**.

These two numbers together tell us how well the retriever is performing. Conceptually clean — and, as the next section shows, wrong for this application.

---

## 10. Why the chunk-ID method fails: the classroom puzzle (36:05–46:00)

Now the important statement: **"you cannot use this method for your application. In fact, for many types of RAG applications, you cannot use this method"** — the method of writing down correct document IDs and computing recall and precision against them. The instructor makes the class think through why ("I will wait for your answers because I really want you to think"), and works through the guesses:

| Student guess | Instructor's verdict |
|---|---|
| "We should look at the content of the chunks, not the numbers" | Not the reason — the ID *represents* the chunk's content anyway |
| "The answer may exist in any of the chunks but not in all" (Shruti) | Not really — a question may legitimately be discussed in three different places and need all three combined; the dataset creator is assumed knowledgeable, studies everything, and manually creates the dataset without useless entries |
| "A change in the document's content will change the IDs" | "At least it's not entirely correct, but you are speaking in that direction" (Patalay — whose name he apologizes for mispronouncing; Rupesh said it somewhat correctly too) — the closest guess |

Then the two real reasons:

**Reason 1 — the labeling job is inhumane.** Think about whoever gets this job: for one question, they must read **all ~800+ chunks** (the instructor tries to print the chunk count live — the print doesn't trigger — "no problem, I will tell you: currently, we have roughly 800+ chunks") and decide which chunks contain answer-worthy content. Then the next question — all 800 chunks again. **Fifty times.** "Will they be happy in their life, or will they feel like committing suicide? What kind of work have we given them?" Nobody would take this job.

**Reason 2 — every improvement invalidates the dataset.** Suppose someone did sit all night and finish it. The retriever runs, recall comes out **65** — obviously needing improvement. The ways to improve: increase k (5 → 8 — the instructor starts this example, then catches himself mid-flow) or **adjust the chunking parameters** (currently 750/100 → try **1000/150**). But the moment chunk size changes, the chunks change; the entire vector database must be recreated; the 800 chunks may become ~700 new chunks — and **the golden dataset becomes void**, because every ID in it was valid only for the previous chunk size. So you must recreate the golden dataset from scratch — and again for every future chunking tweak. "This golden dataset was already such a hectic task to create… This will not work. This is a very bad example of engineering."

**The exception.** There are applications where this method *can* work: RAG chatbots built on **cleanly separated documents** — document one very different from document two, document two very different from document three — where you won't tamper with the chunking parameters at all; whatever you set at the beginning, you keep. If chunking is frozen, an ID-based golden dataset is fine. **Our case is the opposite:** the documents are related and information spreads from one to another (a question might be answered in session one *and* session five), so the chunking parameters *will* be tweaked — and each tweak voids the golden dataset. Too much effort; a different method is needed.

> 💡 **Expert commentary.** The chunk-ID golden dataset the instructor just dismantled is exactly how classic IR benchmarks (TREC, later **BEIR**) are built: a fixed corpus, fixed segmentation, human-judged pools of relevant document IDs. It *is* the right protocol when those preconditions hold — corpus frozen, chunking frozen, labeling budget spent once. The instructor's two objections (labeling cost scales with questions × chunks, and any re-chunking invalidates the labels) are precisely why the RAG tooling ecosystem (RAGAS, DeepEval, TruLens) moved to **judge-derived** retrieval metrics scored against reference *answers* instead of ID lists. One classic-IR caveat the ideal-answer approach also sidesteps: in BEIR-style datasets, unlabeled documents are *unknowns, not negatives* — an ID-based recall quietly depends on how completely the pool was judged (see the parent note, [../04-rag-evaluation.md](../04-rag-evaluation.md)).

---

## 11. The real method: a golden dataset of ideal answers (46:00–48:58)

The method we will actually use needs **a new type of golden dataset** — again two columns:

1. **The question**
2. **The ideal answer** — no context IDs this time.

The definition of *ideal answer* carries the whole idea: **it is not what we found on Google.** It is the answer created **based on what was taught in our vector database** — the person building the dataset goes to the (three) relevant chunks and combines them into an answer. "It is not necessary that this answer is correct. But this is the answer that I taught you in class." So for "What is regression testing?", the column holds the actual definition taught in class; for "What is RAG Triad?", the material of the two relevant chunks combined into one answer. And so on — for 50 questions, or 100, or 500. (How this dataset gets built is the very next topic; for now, just what it *is*.)

---

## 12. Contextual recall: claims + LLM-as-a-judge (48:58–57:07)

How to calculate recall with the new golden dataset:

1. Give the first question — "What is regression testing?" — to the retriever. It fetches five contexts: **72, 81, 89, 99, 100**.
2. **The main step: bring in an LLM — an LLM-as-a-judge.** Tell it: *this is our ideal answer — first break it down into claims.* For an ideal answer about regression testing, three claims form:
   - Claim 1: regression testing is basically a way to test whether your **new version is better than your previous version**
   - Claim 2: it **runs an eval suite** against your software
   - Claim 3: it **can be used for CI** as well
3. Then tell the *same* LLM: now go into all these contexts **one by one** and tell how many of these claims exist in them:

| Claim | Found where |
|---|---|
| C1 — tests new version vs previous version | chunk 72 |
| C2 — runs an eval suite against your software | chunk 89 |
| C3 — usable for CI | chunk 100 |
| — | chunks 81 and 99 cover nothing |

All three claims were found somewhere in the five contexts → the retriever retrieved **100% of the context required** to answer this question → **recall = 3/3 = 1**.

Repeat for question 2, "What is RAG Triad?" → the retriever returns **1, 2, 3, 120, 5**. The judge decomposes the ideal answer into two claims — (1) *a RAG Triad is basically a combination of three metrics*; (2) *it includes answer relevance, faithfulness, and context relevance* — then verifies: no claim in chunks 1, 2, 3 or 5; claim 2 is covered in 120. One of two claims found → **recall = 1/2**. And so on for every question; average them at the end.

```
contextual recall (per question) = (# ideal-answer claims found in the retrieved contexts)
                                   ────────────────────────────────────────────────────
                                   (total # of claims in the ideal answer)
```

**Why this trick wins.** Suppose recall comes out 65, and you increase the chunk size from 750 to 1000. Does the golden dataset need to change? **No.** The ideal answer was written once; if the chunks shift and information moves from one chunk to another — "what difference does it make? The ideal answer is still the same." The one-time effort survives every re-chunking, which is exactly what saves us from creating the golden dataset over and over.

**The naming.** This technique is the one **RAGAS** uses — in RAGAS language it is called **Contextual Recall**. What he taught before was **Recall@K**, and "we are not using that. We are using this one." The metric is indeed recall, "but it has a different flavor — an **LLM-as-a-judge flavor**."

**Q&A — won't the judge merge multiple claims into one** while the retrieved context covers them in *different* chunks? Chances exist, but two design choices guard against it: (1) the golden-dataset creator **constructs the answer as a combination of atomic claims** — a deliberate design choice, so that when an LLM sees the answer it can break it into claims very easily; and (2) use a **good-quality LLM as judge whose system instructions are written very well** and are followed effectively. "These are the only two design choices."

> 💡 **Expert commentary.** Decompose-then-verify is the same machinery behind RAGAS's **faithfulness** metric — there, the claims come from the *generated answer* and are verified against retrieved context; here, the claims come from the *ideal answer* and verify the retriever. Note the cost shape: contextual recall costs O(claims × chunks) judge calls per question and contextual precision O(chunks) — trivial at 15 questions × 5 chunks, but a 500-question suite with k = 10 and six claims each is thousands of judge calls. Two rules from the parent note apply directly: **pin the judge model and prompt** (a drifting judge silently redefines the metric) and calibrate judge verdicts against a few human-labeled examples before letting them gate anything. Lecture 15 (G-Eval) shows the most disciplined version of this judging.

---

## 13. Contextual precision: helpful-or-noise judging (57:07–01:00:52)

Precision uses a similar technique, with one simplification — **you don't need to convert the ideal answer into claims.** Take the first question again; the retriever again provides 72, 81, 89, 99, 100. Bring in the LLM-as-a-judge and give it, per chunk, the question, the ideal answer, and one retrieved chunk (say chunk 72). Its job: take every chunk and see **whether the content of this chunk helps in providing this answer** — if yes, it is a **correct/helpful chunk**; if not, it is **noise**. The system prompt, as written on the instructor's slide:

```
Is this chunk relevant?
Does it contain information that helps produce the expected answer?
Answer yes or no and give a reason.
```

With this method every retrieved chunk gets labeled — correct, correct, correct, noisy, noisy in the worked example — and precision for the question is simply **3/5**. Repeat for all questions, average, and you have the precision. (The yes/no-plus-reason output is also what makes DeepEval's `include_reason` logging possible — section 17.)

---

## 14. Rank awareness: DeepEval's contextual precision (01:00:52–01:08:46)

One more nuance the instructor wants nailed: **precision also considers the rank of the retrieved chunks.** Two cases, five chunks each, two correct and three noisy:

- **Case A:** correct, correct, noisy, noisy, noisy
- **Case B:** noisy, noisy, noisy, correct, correct

By the plain formula — how many of the received chunks are useful — both cases have precision **2/5**; the two are identical. But which case would you rather send to the generator? **Obviously Case A**: it brought the two correct chunks to the top, ranked them higher, "versus the second one, which kept them at the very bottom." Case A is the better retriever — yet plain precision cannot differentiate between them.

In **DeepEval**, the precision metric — what we are calling **contextual precision** — is **rank-aware**, and it is calculated like this. At each position, compute the running precision (*of the chunks seen so far, how many are correct*), then average:

| Position | Case A (✓ ✓ ✗ ✗ ✗) | Case B (✗ ✗ ✗ ✓ ✓) |
|---|---|---|
| 1 | 1/1 = 1.00 | 0/1 = 0.00 |
| 2 | 2/2 = 1.00 | 0/2 = 0.00 |
| 3 | 2/3 ≈ 0.67 | 0/3 = 0.00 |
| 4 | 2/4 = 0.50 | 1/4 = 0.25 |
| 5 | 2/5 = 0.40 | 2/5 = 0.40 |
| **Average = contextual precision** | **≈ 0.71** | **≈ 0.13** |

```
precision@i                = (# correct chunks among the first i retrieved) / i
contextual precision (q)   = mean( precision@1, precision@2, …, precision@k )
```

Case A's average is obviously higher — which is exactly what we wanted: the concept of precision (*of all that came, how much is correct*) **plus** whether the correct ones are ranking higher, captured in one number. "This method of calculating precision while being rank-aware is used in DeepEval." (He showed it informally and in a hurry — but the differentiation is plain to see.)

**Theory recap.** The discussion of the last 15–20 minutes — the new golden-dataset approach, the ideal answer, and the recall and precision calculated from it — is the method we will follow for our retriever. The important consequence: **we are going to use LLM-as-a-judge for both calculations. This is not a programmatic evaluation anymore.** According to the initial plan it *was* programmatic; a problem emerged in it, and because of that problem the plan changed.

---

## 15. Creating the golden dataset: four ways (01:08:46–01:18:52)

The biggest question that arises: **how will this golden dataset be created?** Three or four ways:

| # | Method | How it works | Verdict |
|---|---|---|---|
| 1 | **Hand-authored** | A person who knows the entire corpus writes questions and ideal answers from the actual chunks | **The best way** — human judgment, low error chance — but **not scalable** |
| 2 | **LLM-assisted drafting** | Upload the corpus to Claude with clear instructions; the LLM drafts, the human reviews | Cost, time, and effort drop; error chance rises — **the instructor's choice** |
| 3 | **DeepEval Synthesizer** | Load transcripts, chunk, feed random chunks to the Synthesizer class (an LLM inside) with formatting instructions | "My experience was not that great" — see the demo below |
| 4 | **Production logs** | After deployment, mine positive-signal interactions (thumbs-up etc.) into golden entries | Realistic and free — but "obviously cannot be the first way," since you need entries at the beginning |

**Way 1, hand-authoring, in detail.** It requires knowledge of the entire data — and the instructor is in a very good position: he took all these classes, he knows what he taught and in which session. He can think of a question — *"What is the RAG Triad?"* — and he knows he taught it in **session number eight**, the last session. So he goes to session eight's chunks (say 15, 20, 25, or 30 of them), finds the ones that mention the RAG Triad, takes those chunks and constructs an answer from them (or gets it done with an LLM's help) — and repeats the process 15–50 times. Best because human judgment is used and the chance of error is low; the only problem is scalability — even he would get tired after 50 questions, or you have to pay someone.

**Way 2, LLM-assisted drafting, in principle.** The creation job is the LLM's; **the review job is yours.** If Claude drafts 15–20 questions, he actually reads each question and its ideal answer, and from the ideal answer can tell whether he taught this or not. Benefits: costs, time, effort all decrease. Risk: errors increase — "the LLM might include something in the answer that perhaps I haven't taught in class. Regarding RAG Triad, it might write something it learned on the internet." Human review removes those points. (His exact run of this method — section 16.)

**Way 3, the DeepEval Synthesizer, live.** Inside the `goldens/` folder there is a `generate_gold.py` (he copies it to `goldens_generator.py` and runs it). He declines to explain the code in depth — for a specific reason: the output wasn't good. Roughly, the code loads all transcripts, chunks them, **picks some random chunks**, and sends them to DeepEval's **Synthesizer** class, inside which an LLM has been placed with instructions to create a golden dataset in a particular format. Running it prints verbose DeepEval statements ("generating a golden dataset from the context" — the mechanics are deferred to another day; not today's agenda) and produces **`retriever_dp_golden.json`**: an ID, the question, the ideal answer — and a *source* field that **we** have to fill in, because DeepEval can't tell which session a chunk came from; it doesn't have that information. His manual review of what it generated:

| Generated question | Instructor's review |
|---|---|
| "What specific grade school math problems does the GSM8K dataset contain for model training?" | Seems good — plausibly drawn from the benchmarks class |
| "Access methodologies to validate LLMs' robustness against adversarial exploits and misinformation generation." | "Do you ever feel that a student would come to our doubt solver and ask a question like this? This cannot be their language at all" — DeepEval "kind of over-optimized" the question; not a good golden entry |
| "Is the platform's success criteria to evaluate UPSC answers exactly as human experts do with consistent accuracy?" | Built on the old UPSC example from some session — "not exactly useful," because the course is about LLM evaluations, not the specifics of that UPSC application |
| "If schema details are omitted, how might adding descriptive prompts aid LLMs in parsing technical columns?" | Same pattern — the question quality "didn't seem sufficient for me to evaluate my retriever" |

DeepEval has no idea where to give importance or what kinds of questions people actually ask when they have doubts — "it is just fetching and extracting questions from whatever transcripts it received." His verdict: the method might have more nuances to figure out going forward, but his **first interaction with the Synthesizer didn't yield impressive results, at least for his application** — so we are not using it (though it is a technique people do use, and DeepEval gives you the option). Even here, human review after generation remains mandatory — at the end, an LLM did the work. The file is on GitHub too; your generated questions may differ.

**Way 4, production logs.** Once the app is deployed, people come and ask questions; sometimes it answers wrong, sometimes right. Interactions with **positive signals — thumbs up and all** — become golden dataset entries, because there the retriever and the entire chatbot demonstrably worked correctly. But it cannot be the *first* way: you need some entries in the beginning.

So: do it manually yourself, do it with an LLM's help, do it with DeepEval, or fetch from production and keep adding — the three–four ways to create a golden dataset.

---

## 16. The 15-question golden set for this project (01:18:52–01:21:24)

Which method did the instructor use? **The second one — LLM-assisted drafting.** He took all the transcripts, put them on **Claude**, and gave very clear instructions: *I want to build a RAG chatbot. I need to evaluate its retriever. To evaluate the retriever, I need to measure contextual precision and contextual recall. For that, I need a golden dataset — this will be column one (question), this will be column two (ideal answer). Can you create it for me?*

One deliberate choice: **he did not create too many questions at once** — 15 questions were created one by one (first the first, then the second, third, fourth…). The result is `retriever_golds.json`, and reading the questions, "you will feel that yes, a student could ask this":

- *"What is an online eval and how is it different from offline eval?"*
- *"What is faithfulness versus groundedness?"*
- *"How do I know if my eval is reference-based or reference-free?"*
- *"Why can't we test LLM apps the same way we test normal software?"*

The language is student-like, the answers are taken from the transcripts — **and he manually checked all 15 questions at least.** This file is now the golden dataset.

A quick position check before the code: we started from *evaluate the components first*; among those, *the retriever first*; then built the retriever; then had the long discussion — first the wrong way, then why it was wrong, then the right way, then how to create the golden dataset. We now know what to do **and** hold the golden dataset — so we are ready to carry out the evaluation.

> 💡 **Expert commentary.** The four methods form a quality/effort frontier, and the instructor's pick — LLM-assisted drafting with mandatory human review — is the widely recommended middle. Two additions worth knowing: RAGAS ships its own **testset generator** with question-evolution patterns (conditioning, reasoning, multi-hop) designed precisely against the "over-optimized, unnatural question" failure he hit with DeepEval's Synthesizer; and production mining (way 4) is the same self-improving loop that lectures 03 and 19 formalize — seed the set synthetically, then let real traffic take over. Keep expectations calibrated: a 15-question set is a smoke test, not a statistic (section 19 makes the consequences concrete).

---

## 17. DeepEval's three-part pattern (01:21:24–01:26:43)

Before showing the evaluation code, a short introduction to DeepEval's philosophy and common pattern. Whenever you perform an evaluation with DeepEval, you primarily use **three things**:

| Component | What it is |
|---|---|
| **LLMTestCase** | Represents **one row of your golden dataset** — multiple rows, multiple test cases |
| **Metric** | The metric to evaluate against — with parameters you can set |
| **`evaluate`** | The function that runs the metric(s) on the test case(s) and gives you a score |

The example on screen tests the **Answer Relevancy** metric (itself one of the RAG Triad metrics — lecture 14). The example golden dataset has two rows, so there is a first LLMTestCase and a second, and inside every test case there are **fields** — e.g., `input`, which represents the question ("What is the capital of France?"), and `actual_output`, the system's answer ("The capital of France is Paris."), and so on for the second case.

Inside every **metric** there are parameters:

- **`model`** — which LLM you want to calculate the metric with; this LLM acts as the judge ("let's say we want to use 4.1", i.e., GPT-4.1).
- **`threshold`** — if the score falls **below** this threshold, that particular test case is a failure; score higher and it passes. His illustration: if we were calculating precision in a particular case it would come to 1/2 = 0.5 — had *that* been set as the threshold, this test case would fail; the point is that **whether a test case passes or fails depends on the threshold**, it is not part of the metric itself.
- **`include_reason = True`** — a reason is provided for why each test case passed or failed.

And **`evaluate`** "simply runs this metric on this test case and gives you a score. That's it." So the general structure of any DeepEval code is always: **LLMTestCases (the golden rows) + one or more metrics + the `evaluate` call.**

---

## 18. The eval pipeline: `eval_retriever.py` (01:26:43–01:33:46)

Using that structure, the code that evaluates our retriever on two metrics — **Contextual Recall** and **Contextual Precision** — lives in `evals/`. Reading it top to bottom:

- The **imports**, including the retriever itself.
- The important parameters: the **path of the golden dataset**, the **judge model** (LLM-as-a-judge), and the **threshold**.
- Load the golden dataset — the JSON file just created — and **loop over it**: the file holds 15 questions, IDs **G01 to G15**, so the loop runs 15 times.
- Inside each iteration: call the retriever with that row's question → it brings back **five contexts** → extract the text of all five into a variable.
- Build one **LLMTestCase** per row:

| Field | Value in our pipeline |
|---|---|
| `input` | The golden question |
| `expected_output` | The ideal answer from the golden dataset |
| `retrieval_context` | Whatever the retriever sent (the five chunk texts) |
| `actual_output` | A placeholder — "Generator not evaluated in this run" — since the generator is not in the picture yet; ignore it |

- The two metrics — the **Contextual Recall metric** and the **Contextual Precision metric** — each configured with `threshold`, `model` (the judge model), and `include_reason=True`.
- The **`evaluate`** call: all 15 test cases in `test_cases`, the two metrics in `metrics`.
- A final block of **configuration logging**: for this entire retriever-running process, we used *this* embedding model, *this* chunk size, *this* chunk overlap, top **five**, this judge model, this golden dataset — "basically, we are logging the configuration. But the main code is just these two lines" (the metric setup and the evaluate call).

The code is copied into `evals/eval_retriever.py` (word wrap first), saved, and run.

**First run — and the classic Python gotcha.** `python3 evals/eval_retriever.py` → **`ModuleNotFoundError: No module named 'src'`**. The problem is the line importing the retriever: `build_retriever` lives in `src/retriever.py`, but when you run `eval_retriever.py` this way, you are already inside the `evals` folder — "from that perspective, the src folder doesn't even exist." The fix: **turn both folders into packages** — create an `__init__.py` inside `src` and an `__init__.py` inside `evals` — and run it as a module: **`python3 -m evals.eval_retriever`**. No error now; the eval starts and runs through all the test cases.

---

## 19. Results: baseline and the improvement loop (01:33:46–01:46:53)

**The baseline** (text-embedding-3-small · chunk 750/100 · k = 5 · no reranker): the overall numbers come out **80 for both** — contextual recall **0.80** and contextual precision **0.80** — with **10 of 15 test cases passing and 5 failing**. "Congrats, you just ran your first eval." And the immediate next step is *not* a tuning knob: go study the individual test cases and **read the reasoning the judge provided** — "only then will you be able to understand what kind of mistakes are happening in these test cases."

Then the improvement loop, suggestion by suggestion:

| Run | Change | Contextual recall | Contextual precision | Failing test cases |
|---|---|---|---|---|
| 1 | Baseline (small embeddings, 750/100, k=5) | 0.80 | 0.80 | 5 of 15 |
| 2 | Chunking 750/100 → **1000/150** (DB rebuilt; 697 chunks) | **0.97** | **0.83** | 3 of 15 |
| 3 | + **reranker** (Hugging Face sentence-transformer) | 0.92 | **0.85** | 2 of 15 |
| 4 | Embeddings → **text-embedding-3-large** (DB rebuilt) | **0.99** | 0.85 | 3 of 15 |
| 5 | k 5 → 3 | (fluctuates) | 0.84 | — |

**Iteration 1 — chunking parameters (the instructor's first suggestion).** The simplest lever: the two chunking parameters, chunk size and overlap — "I have intentionally set it low." Change 750/100 → **1000/150** in `retriever.py`, match the config log in the eval file, **delete the existing vector database** (otherwise a new one won't be created), and re-run. This time the chunk-count print actually fires — **697** — the total chunk count that failed to print back in section 10. Result: recall **80 → 97** ("as soon as we increased the chunk size, the contextual recall increased significantly"), precision **80 → 83**, failures **5 → 3**. This is the new baseline — and with recall now at "a 93% pass rate," the instruction is: don't worry too much about recall anymore; **how do we increase precision?**

**Iteration 2 — the reranker (Rahul's suggestion).** (A student first suggests changing the overlap; "Yes, perfect — Rahul said exactly the right thing: what if we implement a reranker?") Bringing a **reranker** into the picture **always increases precision**, and the reason follows directly from section 14: contextual precision is rank-aware, and the reranker's job is to take the retriever's contexts and **rerank** — move the most meaningful chunks to the top, the non-meaningful ones (the noise) to the bottom — so "by default, by definition, the precision value should increase." Today is not about *teaching* rerankers — Himanshu already covered that in the advanced track course (watch that video if you haven't); here we only implement one to see the benefit. Practically: copy `reranker.py` from the GitHub `src/` folder into `src/`; in the eval, replace the `build_retriever` line with the **re-ranking retriever**; update the config logging (the retriever entry changes from the base retriever to the reranker, with the 1000/150 settings). On the run, something downloads — **a sentence-transformer model from Hugging Face is powering the reranker**. Result: precision **83 → 85**, recall dips a bit **97 → 92**, and now **only two test cases are failing** (against the 0.7 threshold). "There is some benefit… I was expecting it to increase a bit more."

**Iteration 3 — the embedding model (Shivani's suggestion).** Increasing k is tricky (recall might rise, precision might fall), but the **embedding model** is "also a very important thing": swap `text-embedding-3-small` for **the large version** — obviously the cost will increase, but let's see if there's any benefit. Two changes: the config log gets the large version too, and — because the embeddings changed — **delete the vector database** so it is recreated fresh with the new embedding model. The current baseline going in: 92 and 85, two failing. Result: "it helped a little. No, actually, three cases failed again" — recall **92 → 99**, precision still **85**, three cases failing.

**Iteration 4 — reduce k.** Since precision won't climb, "maybe you can think about decreasing K a little now. K is 5 — maybe make it K = 3. That will hit the recall a bit, but precision might go up." (For this change the vector database does *not* need rebuilding — only the k value in the retriever.) Mid-run, Himanshu's remark in chat: we used a very basic reranker — a slightly better-quality reranker would be more beneficial; the reranker *was* providing visible benefit. Result: **reducing k actually made precision lower — it came down to 84.** And an important observation: "some variation comes like this as well. If you run it again with the same settings, there will be some variation. The reason is that there are very few rows — you only have 15 rows in the golden dataset. So some variation will come just like that. That variance will always be there." No benefit in reducing k.

**Where it lands.** Roughly: **recall of 95-plus, which is very good, and precision of around 85, which is also kind of good.** The levers left: a **better reranking model** (per Himanshu), and more chunking experiments (the overlap sits at 150 — you could try values around 150–200).

The big-picture close, in the instructor's words: maybe for the first time you built a RAG project, built its retriever — "and along with building it, now you also have an important piece of information about how its retrieval quality is. You can actually say that the retrieval quality of my retriever is good — recall is above 95 and precision is around 85. So you can move forward with some confidence and build the generator," which is exactly the next class. Per the plan: components first — **the retriever part is done; the generator is left.**

> 💡 **Expert commentary.** With n = 15, a single flipped test case moves any aggregate by ~6.7 points — the 0.83 → 0.85 → 0.85 → 0.84 precision sequence is mostly noise, compounded by judge nondeterminism (which is exactly why the instructor warns that identical settings give different numbers on re-runs). Two habits make this loop trustworthy: report a mean over several runs, or a binomial confidence interval — 85% on 15 questions is roughly a 58–98% interval at 95% confidence, so "85 vs 84" is unresolvable; and keep a **held-out slice** of goldens you never tune against, otherwise the loop optimizes the retriever to answer *these 15 questions* rather than student doubts. This is the same statistics lecture 11 applied when it advised running a 20-question eval five times before trusting a model ranking.

---

## Key takeaways

1. **The eval suite is assembled level by level** — component, pipeline/workflow, application — and the collected pipelines later serve regression testing (lecture 18). This lecture completes the component level, retriever half.
2. **Build-test-build:** never build the whole application and then test; build the retriever, evaluate it, *then* build the generator, evaluate it, then the pipeline, then the application.
3. **Two failure modes, two metrics:** a retriever can miss the correct context (**recall**) and it can bring correct context mixed with noise (**precision**). Increasing k always raises recall and drags precision down — k itself is the trade-off dial.
4. **Recall and precision are reference-based** — they require knowing the correct context (or its substance) per query, i.e., a golden dataset.
5. **The chunk-ID golden dataset fails twice:** the labeling cost (≈800 chunks read per question × 50 questions) and total invalidation on any chunking-parameter change. It only works for cleanly separated documents with frozen chunking.
6. **The fix is the ideal answer:** a golden dataset of (question, ideal answer), where the ideal answer is built from what the corpus actually teaches — not from Google. It survives every re-chunking; invest once.
7. **Contextual recall** (the RAGAS technique): the judge decomposes the ideal answer into atomic claims and checks how many appear in the retrieved contexts. **Contextual precision** (DeepEval): the judge labels each chunk helpful-or-noise, and the score is a rank-aware running average — so good chunks at the top score higher than the same chunks at the bottom.
8. Both metrics are **LLM-as-a-judge evaluations, not programmatic ones** — the plan changed when the programmatic method's flaw emerged. Guard rails: write ideal answers as atomic claims; use a good judge with well-written system instructions.
9. **Golden datasets come four ways:** hand-authored (best, unscalable), LLM-assisted drafting with human review (the instructor's choice — 15 questions via Claude), DeepEval's Synthesizer (his first experience: over-optimized, unnatural questions), and production logs (only after deployment).
10. **DeepEval is always three things** — LLMTestCase (one golden row; `input`, `expected_output`, `retrieval_context`, `actual_output`), Metric (with `model`, `threshold`, `include_reason`), and `evaluate`. The improvement loop took the retriever from **0.80/0.80 → 0.97/0.83 (chunking 1000/150) → 0.92/0.85 (reranker) → 0.99/0.85 (large embeddings)**; k=3 hurt (0.84). Final: **recall 95+, precision ~85** — good enough to move on to the generator.

## Interview angles

- *"Your RAG system gives bad answers. How do you know whether to blame the retriever or the generator?"* → Evaluate components separately before the pipeline: score the retriever with contextual recall/precision against a golden dataset; only a retriever that passes deserves a generator built on top of it.
- *"What's the difference between recall@k and contextual recall?"* → recall@k matches retrieved chunk IDs against a labeled set — programmatic, rank-blind, and invalidated by re-chunking; contextual recall decomposes the ideal answer into claims and asks a judge whether each claim is covered by the retrieved text — it survives re-chunking and needs no ID labels.
- *"Why is contextual precision rank-aware, and why does that matter?"* → plain precision scores {2 correct of 5} identically whether the good chunks sit at ranks 1–2 or 4–5; a generator-fed-by-top-context cares deeply about the difference; the running-precision average rewards good chunks ranked high — which is also why adding a reranker raises it by definition.
- *"How would you build a golden dataset for a new RAG app with no production traffic?"* → the four ways, in order of preference: hand-author if you know the corpus; LLM-assisted drafting with mandatory human review; DeepEval/RAGAS synthesizers with review; then mine positive-signal production interactions once live.
- *"Your contextual precision is 0.85. What do you try first?"* → the lecture's exact menu: chunk size/overlap (cheap, big recall wins), a reranker (rank-aware precision by construction), a stronger embedding model (recall), and k — carefully, since k trades precision against recall. And before tuning: read the judge's per-case reasons.
- *"How do you handle evaluation when you keep changing chunking parameters?"* → never key golden data to chunk IDs; key it to ideal answers written from the corpus, so re-chunking never invalidates the dataset.

## Cross-links

- **Previous:** [12 — How to Answer "How Do You Evaluate Your RAG App?" in Interviews](12-rag-eval-interview-answer.md) — the roadmap this lecture executes.
- **Next:** [14 — Evaluating RAG: Generator & Full Pipeline with the RAG Triad](14-rag-triad-generator-pipeline.md) — the generator and pipeline levels; Answer Relevancy, used as this lecture's DeepEval example, is one of the Triad's three metrics.
- **Parent note:** [Section 105 note 4 — RAG Evaluation](../04-rag-evaluation.md) — the four-level model behind the component/pipeline/application split, retrieval-metric definitions, and the judge-calibration rules that govern contextual precision/recall.
- **Foundations:** [03 — The Complete Evaluation Workflow](03-evaluation-workflow.md) (the golden dataset and improve-the-system loop this code-along instantiates) · [05 — Eval Methods](05-eval-methods-reference-based-vs-free.md) (where recall@k, LLM-as-a-Judge, and reference-based vs reference-free were introduced) · [04 — Multiple Eval Pipelines](04-multiple-eval-pipelines.md) (the three-level architecture and the reranker fix).
- **Where the suite gets used:** [18 — RAG Regression Testing](18-rag-regression-testing.md) — the eval suite's destination · [19 — Online Evaluation with LangSmith](19-online-eval-langsmith-monitoring.md) — production-log mining of golden entries (way 4).
- **Course hub:** [README.md](README.md)
