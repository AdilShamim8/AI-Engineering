# Portfolio Projects

> **100 Days of AI Engineering** · after the 100 days

> **Source:** the module structure, unit topics, outcomes, 'try it' exercises and skipped-topic tables are adapted verbatim from the [CampusX 100 Days of AI Engineering](https://ai-engineer-roadmap-2026.vercel.app/100-days/projects/) companion track (retrieved October 17, 2026). The *Free learning resources* and *In this repository* sections are independently curated free worldwide alternatives — this repository is not affiliated with CampusX.

---

### How to use this section

- 01 Build two or three projects, not ten.
- 02 Make each one different.
- 03 Pick for the job you want.
- 04 Finish each in two to four weeks.

### Project guidelines

- 1 A real problem and a real user
- 2 A baseline first
- 3 A test set of 30+ cases, with before-and-after scores
- 4 A security pass, with proof attacks are blocked
- 5 Live, with a link anyone can try
- 6 Cost per request and response time
- 7 A README with results, trade-offs and failures
- 8 A two-to-three-minute demo video

### Self-review checklist

- I can explain the problem and user in two sentences.
- I measured a baseline first.
- My test set has 30+ cases, with baseline and final scores.
- My judge agrees with my own scores.
- I tried 10+ attacks, and all are blocked.
- No secrets or personal data in my code, logs or repository.
- It's live, and someone else has used it.
- I report cost per request and response time.
- My README covers the design, results, trade-offs and a failure.
- I have a demo video.
- I can answer: Why this design? What breaks at 100× the traffic? How would I halve the cost?

### The projects

### 01 · Invoice and Receipt Extractor *(Intermediate — Builds on Modules 1, 2 and 4)*

**What you'll build** · A pipeline that reads scanned bills, invoices and receipts, extracts key fields, checks them, and sends uncertain cases to a person for review.

Must-haves

- Extract vendor, date, invoice number, line items, tax and total into a fixed structure.
- Check the results: line items add up to the total, dates and tax numbers are valid.
- Send low-confidence or failed extractions to a review screen instead of saving them.
- Show which part of the page each value came from.

**Done when** · Field-level accuracy on 30+ documents is reported, and no invalid record is saved without review.

### 02 · Data Question Answerer *(Intermediate — Builds on Modules 2, 3 and 4)*

**What you'll build** · An assistant that answers plain-language questions about a real dataset by writing and running database queries, and explains the answer with the figures behind it.

Must-haves

- Load a real dataset into a database and describe every table and column in plain language.
- Turn questions into queries, run them with read-only access, and show the query and result.
- Retry failed queries within a limit, and say so when a question can't be answered from the data.
- Block anything that changes data, and limit how many rows can be returned.

**Done when** · Accuracy on 30+ questions with known answers is reported, including questions that need joins, totals and filters.

### 03 · Research Agent with Cited Reports *(Intermediate to Advanced — Builds on Modules 4 and 5)*

**What you'll build** · An agent that takes a research question, searches the web and documents, and writes a structured report where every claim links to its source.

Must-haves

- Break a question into sub-questions and research them in parallel.
- Attach every claim to a source, and check that each source actually supports its claim.
- Say clearly where sources disagree or where evidence is thin.
- Stay within a time and cost limit for each report.

**Done when** · Citation accuracy on 10+ reports is measured, and cost and time per report are stated.

### 04 · Codebase Assistant *(Advanced — Builds on Module 5)*

**What you'll build** · An agent that answers questions about a GitHub repository and proposes fixes for issues, checking each fix by running the tests in a sandbox.

Must-haves

- Answer questions about the code with references to the exact files and lines.
- Propose a fix for an issue, run the tests in a sandbox, and show the result.
- Never run code outside the sandbox or change the repository without approval.
- Keep long code-reading tasks within a context and cost limit.

**Done when** · The success rate on 20+ real issues is reported, with sandbox tests confirming each fix.

### 05 · Voice Booking Agent *(Advanced — Builds on Modules 1 and 5)*

**What you'll build** · A voice agent that books, changes and cancels appointments in a natural conversation, in English and mixed Hindi-English.

Must-haves

- Keep the gap between the caller finishing and the agent replying short enough to feel natural, and measure it.
- Handle interruptions, pauses and unclear speech.
- Check availability and create bookings through tools, confirming details before saving.
- Hand over to a person when the agent can't help.

**Done when** · Task success on 20+ test calls and the average response delay are reported.

### 06 · Contract and Policy Comparer *(Intermediate — Builds on Modules 3 and 4)*

**What you'll build** · A tool that compares two versions of a contract or policy and explains what changed and why it matters, with citations to both versions.

Must-haves

- Match sections between versions, even when they've moved or been renumbered.
- List additions, removals and changes, each linked to the exact text in both versions.
- Flag changes in key areas such as payment, liability, termination and data use.
- Never present the tool's output as legal advice.

**Done when** · Accuracy at finding real changes on 15+ document pairs is reported, including changes it missed.

### 07 · Visual Product Search *(Intermediate — Builds on Modules 1 and 4)*

**What you'll build** · A search over a product catalog that finds items from a photo or a description.

Must-haves

- Search by uploaded photo, by text, or both together.
- Filter by price, category and other product details.
- Compare joint image-text search with searching generated captions.
- Measure search quality on queries with known correct results.

**Done when** · Recall@10 on 30+ queries is reported for both search approaches.

### 08 · Browser Task Agent *(Advanced — Builds on Module 5)*

**What you'll build** · An agent that completes a real multi-step task on websites, such as comparing prices across stores or filling in a long form, and asks for approval before anything that commits you.

Must-haves

- Complete a chosen task end to end on real websites.
- Ask for approval before submitting, paying or sending anything.
- Recover when a page changes, loads slowly or shows an unexpected pop-up.
- Resist instructions hidden in web pages that try to redirect the agent.

**Done when** · Task success on 20+ runs and the result of 10+ hidden-instruction attacks are reported.

### 09 · Fine-Tuned Small Model *(Intermediate to Advanced — Builds on Modules 3 and 6)*

**What you'll build** · A small open model, fine-tuned for one narrow task, that matches or beats a large prompted model at much lower cost.

Must-haves

- Choose a narrow task, such as classifying customer messages written in mixed Hindi-English.
- Build a clean training set and a held-out test set that the model never trains on.
- Measure a prompted large model as the baseline.
- Fine-tune with LoRA, then compare accuracy, cost and response time.
- Serve the tuned model behind an API.

**Done when** · A results table compares the tuned and prompted models on accuracy, cost per thousand requests and response time.

### 10 · Published MCP Server *(Beginner to Intermediate — Builds on Module 5)*

**What you'll build** · An MCP server for a public API or developer tool, released so other people can connect it to their own AI apps.

Must-haves

- Expose useful tools, resources and prompts with clear names, descriptions and inputs.
- Handle errors, authentication and rate limits properly.
- Test it with an MCP inspector and at least two different AI apps.
- Publish it with setup instructions and examples.

**Done when** · It's published, works in two AI apps, and at least one other person has used it.

### 11 · Personal Knowledge Agent *(Intermediate — Builds on Modules 4 and 5)*

**What you'll build** · An agent that remembers and connects your notes, bookmarks and documents over time, answers questions about them, and reminds you of related things.

Must-haves

- Add notes from at least two sources and answer questions across them with citations.
- Remember preferences and facts, and update them when they change.
- Let the user see, edit and delete everything the agent remembers.
- Keep the data private, with an option to run on a local model.

**Done when** · Memory accuracy on 20+ test cases is reported, including updates and deletions.

### 12 · Cost-Cutting Model Gateway *(Advanced — Builds on Module 6)*

**What you'll build** · A gateway that sits in front of several model providers and cuts cost with caching, routing and fallbacks, with a dashboard showing usage and savings.

Must-haves

- One endpoint for several providers, with per-team keys and budgets.
- Exact and semantic caching, with rules for what must never be cached.
- Route easy requests to cheaper models, and fail over when a provider is down.
- A dashboard of requests, cost, savings, errors and response time.

**Done when** · Savings and quality are measured on replayed traffic, and failover works when a provider is shut off.

### Choosing your portfolio

| Target role | Suggested projects |
|---|---|
| AI application engineer | 1 3 12 |
| Agent engineer | 4 8 10 |
| Applied ML or model-focused engineer | 2 7 9 |
| Voice or multimodal engineer | 5 7 1 |

Your course project counts too. Pair it with two projects that show different skills.

### Projects to avoid

- **Another "chat with your PDF" app:** Your course project already covers this, and so does everyone else's portfolio.
- **High-risk uses without safeguards:** Automated résumé screening, medical or legal advice, and credit decisions can harm people. Avoid them unless you include bias testing, human review and clear limits.
- **Thin wrappers:** An app that only forwards prompts to a model shows little engineering.
- **Using data you don't have the right to use:** Check the license or terms of every dataset and website.

<!-- nav-footer -->
---

**Navigate:** [← Module 6 Shipping to Production](module-6-shipping-to-production.md) · [Section hub](README.md) · [Site index](https://adilshamim8.github.io/AI-Engineering/)
