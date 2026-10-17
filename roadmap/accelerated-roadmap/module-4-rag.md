# Module 4 · RAG

> **100 Days of AI Engineering** · Days 25–56 · 26 units

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/rag/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

## Units

## Part 1 · Days 25–36

### Build a Simple RAG

#### 01 · When to Use RAG (Unit 4.1 · Day 25)

- **The RAG pipeline** — A question comes in, the most relevant passages are found, they're added to the prompt, and the model answers from them.
- **What RAG solves** — Private documents, information that changes often, collections too large to send whole, and answers that need sources.
- **When not to use RAG** — When the model already knows enough, the task is just rewriting or transforming text, or all the information fits comfortably in one prompt.
- **Two kinds of failure** — A wrong answer can come from finding the wrong passages or from the model misusing the right ones.

**Try it** · Send a long document whole to your model with a question about it, and note the tokens, cost and time.

**Outcome** · Decide whether a problem genuinely needs RAG and explain what each step of the pipeline does.

#### 02 · Loading and Cleaning Documents (Unit 4.2 · Days 26–27)

- **Getting text out** — Load **PDFs**, web pages, Word files and other formats with **LangChain**'s document loaders, and recognize scanned pages that need text recognition first.
- **Clean without losing structure** — Remove clutter like repeated headers and footers, but keep headings, lists and tables that give text its meaning.
- **Keep the details** — Store each document's title, source, section and date alongside its text; you'll need them for filters and citations.
- **Changes over time** — Handle duplicate documents, updated versions and deleted files so your collection doesn't go stale.

**Try it** · Load your three messiest documents and read the extracted text. Note every place where tables, headings or layout came out wrong.

**Outcome** · Turn a real document collection into clean text with useful details attached, ready for searching.

#### 03 · Parsing Messy Documents (Unit 4.3 · Day 28)

- **Why basic loaders fail** — Multi-column pages, tables, headers and footers, forms and scanned pages often come out scrambled or empty.
- **Parsers that understand layout** — Layout-aware tools such as Unstructured or Docling detect headings, columns and tables instead of reading a page as one stream of text.
- **Scanned pages** — Use text recognition (**OCR**), or send the page image to a vision model to read it, as you saw in Module 1.
- **Tables** — Extract tables as tables, keeping column headers with every row so each row still makes sense on its own.
- **Check the result** — Compare extracted text with the original on a few sample pages, and pick a parsing approach per document type.
- **Cost and speed** — Vision-based parsing is slower and more expensive, so use it only for the documents that need it.

**Try it** · Parse your messiest PDF three ways: with the basic loader, a layout-aware parser and a vision model. Compare how each handles one table and one multi-column page.

**Outcome** · Turn messy real-world documents, including tables and scans, into clean text you can trust.

#### 04 · Chunking (Unit 4.4 · Day 29)

- **Why split documents** — Whole documents are too big to search precisely or send to the model, so you break them into smaller passages.
- **Ways to split** — By fixed size, by paragraphs and sentences, by the document's own sections, or by changes in meaning.
- **Size and overlap** — Small passages are precise but may miss context; large ones carry context but add noise. A little overlap stops ideas being cut in half.
- **Keep the labels** — Each passage should carry its document title and section so it still makes sense on its own.

**Try it** · Split the same document by fixed size and by its sections. Read five passages from each and judge which would make sense to a reader with no other context.

**Outcome** · Choose a chunking approach that fits your documents and the questions people ask about them.

#### 05 · Embeddings and Semantic Search (Unit 4.5 · Days 30–31)

- **What an embedding is** — A list of numbers that captures meaning, so passages about similar things end up close together.
- **Searching by meaning** — Turn the question into an embedding too, then find the passages closest to it.
- **Build it once by hand** — Search a small set of passages yourself, with no database, so you understand what a vector database will do for you.
- **Choosing an embedding model** — Compare quality, cost, speed and language support, especially for Hindi or mixed Hindi-English text if your users write that way.
- **Don't mix models** — Embeddings from different models can't be compared; changing the model means re-embedding everything.
- **Where meaning-based search fails** — Exact names, product codes, numbers and rare terms are often missed.

**Try it** · Search your passages for one question phrased in your own words and one containing an exact product name or code. Compare what comes back.

**Outcome** · Explain how semantic search works, choose an embedding model, and predict the questions it will struggle with.

#### 06 · Vector Databases (Unit 4.6 · Days 32–33)

- **Storing passages** — Save each passage with its embedding and its details (document, section, date) in a vector database such as **pgvector**, through **LangChain**.
- **Search with filters** — Find the closest passages while limiting results by details like document type or date.
- **Why databases use shortcuts** — Comparing against every passage gets slow at scale, so databases use approximate search that trades a little accuracy for a lot of speed.
- **Keeping it current** — Add, update and delete passages when documents change, without rebuilding everything.

**Try it** · Load all your passages into the database, then run the same question with and without a filter on document type.

**Outcome** · Store your whole collection in a vector database and search it quickly with filters.

#### 07 · Your First RAG Pipeline (Unit 4.7 · Days 34–35)

- **Put the pieces together** — Connect your search, a prompt and your model into one LangChain chain: question → passages → prompt → answer.
- **Prompt for grounded answers** — Tell the model to answer only from the passages provided, building on the system prompt you tested in Module 3.
- **When search comes back weak** — Handle results that are irrelevant or thin instead of letting the model guess.
- **How many passages, in what order** — More passages isn't always better; put the most relevant first and watch the total length.

**Try it** · Ask five questions with 3 passages and with 10 passages, and compare the answers, tokens and cost.

**Outcome** · Build a working RAG pipeline that answers from your documents instead of whole files.

#### 08 · Citations and Saying "I Don't Know" (Unit 4.8 · Day 36)

- **Answer from the evidence** — The answer should come from the retrieved passages, not from what the model happens to remember.
- **Cite your sources** — Link each claim to the document and section it came from.
- **A citation isn't proof** — A cited passage must actually support the claim; check that it does.
- **Say when the answer isn't there** — When the passages don't contain the answer, the assistant should say so instead of inventing one.
- **Keep evidence and explanation apart** — Make it clear what came from the documents and what the model added.

**Try it** · Ask three questions your documents can't answer. Then check five cited answers by opening the cited section and confirming it supports the claim.

**Outcome** · Produce answers people can verify, and an assistant that admits when it doesn't know.

## Part 2 · Days 37–44

### Advanced RAG

Each unit in this part tackles a specific way simple RAG fails.

#### 09 · Keyword and Hybrid Search (Unit 4.9 · Day 37)

- **Keyword search still matters** — Classic keyword search (**BM25**) finds exact names, codes and phrases that meaning-based search misses.
- **Combine both** — Hybrid search runs both kinds and merges the results into one ranked list.
- **Merging rankings fairly** — Reciprocal rank fusion combines lists by position rather than raw scores, so results from different search types can be compared.
- **When hybrid helps most** — Questions with names, technical terms, IDs, numbers or exact wording.

**Try it** · Run five questions containing exact names or codes through meaning-based, keyword and hybrid search, and see which finds the right passage each time.

**Outcome** · Add hybrid search to your pipeline and know which kinds of questions it helps with.

#### 10 · Smarter Chunks and Filters (Unit 4.10 · Day 38)

- **Search small, send big** — Search over small, precise passages, but send the model the larger section around the match so it has full context.
- **Give chunks their context** — Add a short line to each passage saying which document and section it comes from, so passages that make no sense alone still get found.
- **Tables and structured content** — Keep tables whole and describe them in words so search can find them and the model can read them.
- **Filters from the question** — Let the model pull filters out of the question itself, such as a product name, date range or document type, before searching.

**Try it** · Ask three questions that mention a specific product, date or document type. Compare results with plain search and with filters extracted from the question.

**Outcome** · Shape your passages and filters so search finds the right content and the model sees enough of it.

#### 11 · Reranking (Unit 4.11 · Day 39)

- **Search wide, then choose carefully** — Retrieve many candidate passages, then use a reranking model to pick the best few to send to the model.
- **Why it works** — A reranker reads the question and each passage together, so it judges relevance more accurately than search alone.
- **The cost** — Reranking adds time and cost to every question.
- **When it doesn't help** — If your search is already precise, reranking may add little.

**Try it** · For five questions where your assistant answered poorly, compare the top 3 passages with and without reranking.

**Outcome** · Add reranking to your pipeline and explain what it improves and what it costs.

#### 12 · Query Transformation (Unit 4.12 · Day 40)

- **Questions aren't always good search queries** — Users write vague, long or multi-part questions that search handles badly.
- **Rewrite the question** — Have the model turn the user's question into a clearer search query first.
- **Multiple queries** — Generate several versions of the question, search for each, and combine the results.
- **RAG-Fusion** — Combine the results of several queries with reciprocal rank fusion, so passages that rank well across many queries rise to the top.
- **Search with a draft answer (HyDE)** — Have the model write a short hypothetical answer and search for passages similar to it.
- **Break it down** — Split a multi-part question into sub-questions, answer each from its own search, then combine.
- **Weigh the cost** — Each technique adds model calls and time; use them only for the questions that need them.

**Try it** · Take three ambiguous questions and one multi-part question. Compare the passages found with plain search, multiple queries and breaking the question down.

**Outcome** · Turn hard questions into searches that find the right passages, and choose the right technique for each kind of question.

#### 13 · Routing and Adaptive RAG (Unit 4.13 · Day 41)

- **Not every question needs retrieval** — Greetings, follow-ups and general questions can be answered directly; searching for them wastes time and can confuse the model.
- **Route to the right source** — When you have several collections or tools, decide which one a question belongs to before searching.
- **Adaptive RAG** — Choose the strategy per question: answer directly, do a simple search, or use heavier techniques like query transformation only for hard questions.
- **Cost and speed** — Routing saves money and time on easy questions while spending more only where it helps.

**Try it** · Build a router that sends each of 20 questions to "answer directly", "simple search" or "transform and search". Check whether its choices make sense.

**Outcome** · Build a RAG system that adapts its effort to each question instead of treating every question the same.

#### 14 · Self-Correcting RAG (Unit 4.14 · Day 42)

- **Check what you found (Corrective RAG)** — Have the model grade the retrieved passages; if they're weak, rewrite the query and search again, or fall back to another source.
- **Check what you wrote (Self-RAG)** — Before returning an answer, check that it's supported by the passages and actually answers the question; if not, retry or say you don't know.
- **Search in steps (multi-hop)** — For questions that need several facts, search, read, then search again for what's still missing.
- **Know when to stop** — Limit how many times the system can retry, so a hard question can't loop forever or run up costs.
- **A step toward agents** — These loops let the system decide its next step, a first taste of the agents you'll build later in the track.

**Try it** · Add a step that grades retrieved passages and retries with a rewritten query when they're weak. Run the 5 questions your pipeline answers worst and see how often the retry helps.

**Outcome** · Build a RAG system that notices bad retrieval or unsupported answers and corrects itself within a set limit.

#### 15 · RAG over Structured Data (Unit 4.15 · Day 43)

- **Not all knowledge is in documents** — Much of what users ask about lives in spreadsheets and databases, and vector search is poor at counting, adding up and filtering.
- **Text-to-SQL** — The model turns the user's question into a database query, your code runs it, and the model explains the result.
- **Give it the map** — Provide the table structure, plain-language descriptions of each column, example values and a few example questions with their queries.
- **Keep it safe** — Use read-only access, allow only the tables it needs, check the query before running it, and limit how many rows come back; you'll go deeper in Part 4.
- **When the query fails** — Spot errors, empty or odd results, and let the model fix its query within a retry limit.
- **Show your working** — Show users the query or the figures behind an answer so they can check it.
- **Documents or database?** — Use the routing you built in Unit 4.13 to send each question to document search, the database, or both.

**Try it** · Put a spreadsheet related to your project into a small database. Answer five questions that need counts, totals or filters, once with text-to-SQL and once with document search, and compare.

**Outcome** · Answer questions from tables and databases accurately and safely, and route each question to the right source.

#### 16 · Graph RAG and Choosing a Pattern (Unit 4.16 · Day 44)

- **What Graph RAG is** — Pull out the people, products, places and relationships in your documents into a graph, then search through those connections instead of only by similarity.
- **When it helps** — Questions about relationships ("which teams use this product?") or about the whole collection ("what are the main themes?") that no single passage answers.
- **What it costs** — Building and updating the graph takes many model calls and is much harder to maintain than plain search.
- **Choosing a pattern** — Start from your actual failures. Missed exact terms → hybrid search. Right passages ranked low → reranking. Vague questions → query transformation. Weak retrieval → corrective **RAG**. Questions about numbers in tables → text-to-SQL. Relationship questions → **Graph RAG**.
- **More isn't better** — Every pattern adds cost, delay and things that can break; add one only when your failures call for it.

**Try it** · Go through the answers your simple pipeline got wrong and match each one to the pattern from this part most likely to fix it.

**Outcome** · Recognize when Graph RAG is worth its cost, and choose RAG patterns based on your own failures rather than novelty.

## Part 3 · Days 45–51

### Evaluating RAG

#### 17 · Why Evals, and Reading Your Failures (Unit 4.17 · Day 45)

- **Why "it looks fine" isn't enough** — You've just added several patterns because they seemed to help on a few questions. Teams that work this way ship embarrassing failures; real cases, like an airline chatbot inventing a refund policy, show the cost.
- **AI testing is different** — The same input can give different outputs, and many answers are neither simply right nor wrong, so you test with sets of examples and scores rather than single checks.
- **Read before you measure** — Look closely at 20–30 real answers, write down what went wrong in each, and group similar problems together.
- **Measure what actually fails** — Use those groups to decide what to measure and what to fix first.
- **The evaluation loop** — Define what good looks like → build examples → run → score → look at failures → improve → repeat.

**Try it** · Run 20 questions through your current pipeline and write a one-line note on every answer that isn't right. Group the notes into 3–5 failure types and count each.

**Outcome** · Explain why AI apps need systematic testing, and find your app's most common failures by reading its answers.

#### 18 · Test Sets and Scoring (Unit 4.18 · Days 46–47)

- **A golden test set** — A list of questions, each with its correct answer and the passage that contains it, built from your own documents.
- **Growing it quickly** — Write questions by hand, then use a model to suggest more from your documents, and check every suggestion yourself before keeping it.
- **Three ways to score** — Code checks for exact facts and formats, a model acting as a judge for questions of meaning, and your own review for anything subtle.
- **With or without an answer key** — Some checks compare against the correct answer; others, like "is this answer supported by the passages?", need no answer key.
- **Writing a good judge** — Give the judge one clear question at a time and ask for pass or fail rather than a score out of 10.
- **Check the judge** — Score 20 answers yourself, compare with the judge, and fix its instructions until you mostly agree. A judge you haven't checked can't be trusted.

**Try it** · Write a judge that decides whether an answer is supported by its passages. Score 20 answers yourself and with the judge, and count how often you agree.

**Outcome** · Build a golden test set from your documents and score answers with code checks and a judge you've verified.

#### 19 · Measuring Retrieval (Unit 4.19 · Day 48)

- **Test the search on its own** — If search doesn't find the right passages, no prompt can fix the answer, so measure it separately.
- **Recall@k** — Of your test questions, how often is the right passage in the top k results?
- **Precision** — How many of the passages you retrieve are actually useful, rather than noise that confuses the model?
- **Compare choices fairly** — Test chunk sizes, embedding models, search types, reranking and query techniques on the same test set.

**Try it** · Measure Recall@5 for meaning-based search, hybrid search, and hybrid search with reranking.

**Outcome** · Measure whether your search finds what users need, and know which of your Part 2 techniques actually improved it.

#### 20 · Evaluating RAG Answers (Unit 4.20 · Days 49–50)

- **Test each part, then the whole** — Check search on its own, the model on its own, the full pipeline, and finally the experience from the user's side.
- **Test the model on its own** — Give it the correct passages and check whether it answers faithfully; if it fails here, the problem isn't search.
- **The three core RAG checks** — Did search find relevant passages? Is the answer supported by them? Does the answer actually address the question?
- **Find where it broke** — For each failure, decide whether search, the assembled prompt or the model's answer was at fault.
- **What users care about** — Correct, complete answers with working citations, in the right tone and format.
- **Cost and speed per question** — Track them alongside quality, especially for patterns like self-correction that add extra calls.
- **Evaluation tools** — Use a library such as **DeepEval** or **RAGAS** for these checks, and make sure you understand what each score actually measures.

**Try it** · Score your test set on the three core checks. For your five worst answers, write down whether search, the prompt or the model was at fault.

**Outcome** · Evaluate a RAG system part by part and pinpoint where each failure comes from.

#### 21 · Automatic Regression Tests (Unit 4.21 · Day 51)

- **Save everything together** — Keep test questions, prompts, settings, model versions and results together so any result can be reproduced.
- **Compare against a baseline** — Every change is judged against the current best version, never in isolation.
- **Test on every change** — Run your evaluation automatically whenever you change a prompt, setting or model, and stop the change if quality drops.
- **Grow the test set** — Add every new failure you find, so the same mistake can't come back unnoticed.
- **Watch quality, cost and speed together** — A change that improves one and damages another needs a deliberate decision.

**Try it** · Set up a single command that runs your test set and fails if the score drops below your baseline. Then deliberately make your prompt worse and confirm it fails.

**Outcome** · Make it impossible to make your app worse without noticing.

## Part 4 · Days 52–56

### Securing a RAG Application

#### 22 · Threats to a RAG App (Unit 4.22 · Day 52)

- **Where untrusted text gets in** — User questions, your documents, uploaded files, web pages and anything else the model reads that your app didn't write itself.
- **Documents are data, never instructions** — Anything retrieved can contain text that tries to give the model orders; your app must never treat it as a command.
- **Model output is untrusted too** — The model's answer can carry injected content onward, into links, tool calls or other systems.
- **A standard checklist** — Use the OWASP Top 10 for LLM Applications as a checklist of the most common risks.

**Try it** · Sketch how data flows through your assistant. Mark every point where untrusted text enters and every action that could cause harm if the model were tricked.

**Outcome** · Map where your RAG app can be attacked before deciding how to defend it.

#### 23 · Hidden Instructions and Poisoned Documents (Unit 4.23 · Day 53)

- **Direct and indirect injection** — Attacks can come from the user typing instructions, or from instructions hidden inside a retrieved document, web page or file.
- **Poisoned documents** — If someone can add or edit a document, they can plant content designed to be retrieved and change the assistant's answers.
- **Leaking through answers** — Injected instructions can make the model include private information in a link or image that sends it elsewhere when displayed.
- **Defenses that work in code** — Clearly separate documents from instructions, limit what the model is allowed to do, check outputs before showing or acting on them, and control who can add documents.
- **Why "ignore malicious instructions" fails** — A prompt telling the model to resist attacks helps a little but can always be talked around; the real protection is in your code.

**Try it** · Add three planted documents to your collection: one that tries to change answers, one that tries to make your assistant use a tool it shouldn't, and one that tries to include a link containing the user's question. See which succeed.

**Outcome** · Recognize injection through documents and defend against it with controls in your code, not just your prompt.

#### 24 · Who Can See What (Unit 4.24 · Day 54)

- **Not every user should see every document** — Store who is allowed to see each document alongside its passages.
- **Filter during search, not after** — Apply the user's permissions as a search filter, so restricted passages never reach the model; hiding them afterwards is too late.
- **Keep users and customers apart** — If your app serves several teams or customers, make sure one can never retrieve another's data.
- **Other places data leaks** — Cached answers, conversation memory and citations that show restricted document titles can all leak information.

**Try it** · Create two users with different access. Ask, as each user, a question that only a restricted document can answer, and check both the answers and the citations.

**Outcome** · Make your RAG app show each user only the information they're allowed to see.

#### 25 · Personal Data and Secrets (Unit 4.25 · Day 55)

- **Find it before you index it** — Scan documents for personal details such as phone numbers, emails and ID numbers, and for secrets like passwords and keys.
- **Remove or mask what you don't need** — Strip or mask sensitive data before it goes into your index.
- **Keep it out of everything else** — Personal data easily ends up in logs, traces, caches and test sets; keep it out of all of them.
- **Deleting means everywhere** — When a document must be removed, remove it from the index, caches, logs and test sets too.
- **Know your provider's terms** — Check how long your model provider keeps your data and whether it can use it, and know the basics of India's data protection law (**DPDP**) if you serve Indian users.

**Try it** · Scan your document collection and your recent logs for phone numbers, email addresses and anything that looks like a key or password.

**Outcome** · Keep personal data and secrets out of your index, logs and test sets, and remove them completely when needed.

#### 26 · Red-Teaming Your RAG (Unit 4.26 · Day 56)

- **Attack your own app** — Systematically try injection, poisoned documents, permission bypasses, attempts to extract private data and attempts to get around your rules.
- **Input and output checks** — Add checks that block clearly harmful requests and catch unsafe or leaking answers, as one extra layer rather than your only defense.
- **Measure how often attacks work** — Track the share of attacks that succeed and how often private data leaks, before and after your fixes.
- **Every successful attack becomes a test** — Add each attack that worked to your regression suite so it can never quietly work again.
- **Security vs quality** — Some defenses make answers worse; check your quality scores after every security change.

**Try it** · Write 15 attacks across injection, poisoned documents, permissions and data extraction. Record how many succeed, fix what you can, and run them again.

**Outcome** · Test your RAG app's defenses the way an attacker would, and turn what you find into permanent tests.

## What we skipped, and why *(optional)*

| Topic | Why it's skipped here | Where to find it |
|---|---|---|
| How vector search shortcuts work inside | You need to know the trade-off, not the algorithms | Full roadmap, Level 4 |
| Similarity math in detail | One idea covers it: closer means more similar | Full roadmap, Level 4 |
| Building a full Graph RAG system | Here you learn when it's worth it; building one well is a project of its own | Full roadmap, Level 4 |
| Building RAG with LlamaIndex | One framework, used well, is enough | Full roadmap, Level 4 |
| Model benchmarks and leaderboards | Choosing a model was covered in Module 1 | Full roadmap, Levels 1 and 7 |
| Online evaluation after launch | Covered when you ship to production | Full roadmap, Levels 7 and 10 |
| Agent and tool security | Covered in the Agents module, where those risks appear | Full roadmap, Level 8 |
| A security review of the whole app | Covered in Shipping to Production, once the app is complete | Full roadmap, Level 8 |
| Responsible AI and regulation in depth | Beyond what a RAG app needs on day one | Full roadmap, Level 8 |

---

## Free learning resources

*Independently researched free worldwide resources (verified October 2026). No paid or CampusX course links are included. The same topics map to [full roadmap levels](../full-roadmap/README.md) where they are covered in more depth.*

- [DeepLearning.AI — Building and Evaluating Advanced RAG Applications](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/) — free short course covering retrieval, reranking and evaluation.
- [LlamaIndex documentation](https://docs.llamaindex.ai/) — ingestion, indexes, retrievers, query engines and RAG pipelines.
- [LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/) — build a RAG pipeline with chunking, embeddings and generation.
- [Qdrant documentation and tutorials](https://qdrant.tech/documentation/) — vector search, payload filters and hybrid retrieval.
- [pgvector (GitHub)](https://github.com/pgvector/pgvector) — vector similarity search inside PostgreSQL.
- [Unstructured (GitHub)](https://github.com/Unstructured-IO/unstructured) and [Docling (GitHub)](https://github.com/docling-project/docling) — layout-aware document parsing for messy PDFs and tables.
- [Sentence Transformers documentation](https://sbert.net/) — generating and working with open embedding models.
- [MTEB leaderboard](https://github.com/embeddings-benchmark/mteb) — compare embedding models on retrieval tasks.
- [Microsoft GraphRAG (GitHub)](https://github.com/microsoft/graphrag) — reference implementation of graph-based retrieval.
- [HyDE / RAG-Fusion notebooks](https://github.com/langchain-ai/langchain/blob/master/cookbook/) — community implementations of query transformation techniques in the LangChain cookbook.

- [Ragas and DeepEval docs](https://docs.ragas.io/) — the evaluation libraries used for RAG test sets and scoring in this module.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10) — the security checklist used in Part 4 of this module.

## In this repository

- [Complete RAG curriculum](../../102_AI-Application-Development/03-RAG/README.md)
- [RAG evaluation note](../../102_AI-Application-Development/03-RAG/6.%20RAG%20Evaluation%20%26%20Benchmarking%20%28RAGAS%2C%20TruLens%2C%20DeepEval%29.md)

---

[← Module 3 · Prompt Engineering](module-3-prompt-engineering.md) | [100 Days map](README.md) | [Module 5 · Agents →](module-5-agents.md)
