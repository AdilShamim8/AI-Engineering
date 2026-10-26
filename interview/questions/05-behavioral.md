# Behavioral Questions

> Behavioral interviews in AI engineering aren't just about culture fit — they test how you navigate the unique challenges of building systems that are non-deterministic, ethically complex, and constantly evolving. As of September 16, 2026, AI-specific behavioral and governance questions are standard at most companies.

---

## Format and What to Expect

| Aspect | Details |
|--------|---------|
| Duration | 30–45 minutes |
| Format | Structured questions, often with scoring rubric |
| Questions | 3–6 behavioral questions |
| Interviewers | Hiring manager, team lead, or cross-functional partner |
| Evaluation | Scored on specific competencies, not "vibe" |

**What makes AI behavioral interviews different**: Traditional behavioral interviews focus on teamwork, conflict resolution, and leadership. AI behavioral interviews add a layer: how you handle ambiguity, model failures, ethical dilemmas, and the rapid pace of change in AI.

---

## Values and Culture Questions

These questions test alignment with company values and culture:

- "What attracted you to this company/role specifically?"
  - **A:** Your engineering blog post on cutting support-copilot hallucination from 12% to 2% with citation verification — and publishing the eval methodology alongside it — is exactly the culture I want. Most teams chase demos; yours treats evals as product. I've spent two years building eval-gated pipelines, and I want to do that where correctness is user-visible at your scale — 40M monthly queries. Concretely: I cloned your public eval harness, reproduced two of your retrieval benchmarks, and your hybrid-rerank design solves the same recall/latency tradeoff I fought at my last company. That specificity is why it's this role, not "an AI role."

- "How do you stay current with the fast-moving AI landscape?"
  - **A:** A fixed weekly system, not doom-scrolling. Every Friday I spend 90 minutes on three curated sources — one model-release digest, one arXiv paper I actually reproduce in a notebook, and release notes for the two frameworks in my stack. Monthly, I rebuild one small side project against a new model to feel its failure modes firsthand. It pays off concretely: when our provider deprecated a model version in June 2026, I'd already benchmarked the successor two months earlier, so migration was a config change plus a 200-case eval rerun — one day of work instead of a two-week scramble. Staying current means small, regular, hands-on doses.

- "Describe a time when you had to make a decision with incomplete information."
  - **A:** During a provider outage, mid-launch. Our primary LLM went down and I had four hours to pick a fallback with no benchmark data on our workloads. I ran a 40-case smoke eval across two candidates, chose the one with solid format compliance and tool-calling even though its prose quality was unverifiable, and shipped it behind a flag at 5% of traffic with refusal-rate and cost dashboards watching. It carried full overflow for two days at a 2.1% defect rate on sampled review. The learning I lead with: make the decision reversible — a canaried "good enough" beats an unbounded search for certainty.

- "What's your approach to building trust with teammates who aren't AI experts?"
  - **A:** Replace jargon with demos and shared artifacts. I ran biweekly 30-minute "AI office hours" where non-engineers watched live failure modes — hallucinations, prompt sensitivity — before hearing any terminology, and I kept a one-page glossary mapping words like "confidence" to what the product actually does. The measurable shift: product managers began writing eval cases in plain language — 60+ cases in six months — and tickets asking us to "make it smarter" dropped from roughly a third of requests to near zero. Trust came from them watching the system misbehave and knowing exactly how we catch it.

- "How do you balance shipping quickly with building responsibly?"
  - **A:** I tier by blast radius. Low-risk outputs — drafts, internal suggestions — ship fast behind flags; anything user-facing or irreversible gets evals and a human checkpoint first. Concrete case: we shipped an email-drafting copilot in two weeks by cutting scope, not safety — it drafted, a human always sent, and every claim was grounded in CRM records with citations. Zero inappropriate sends in six months, and we beat a competitor to market by a quarter. Once faithfulness held at 98% across 500 sampled emails, we relaxed review only for the lowest-risk template class. Speed and responsibility trade off on scope — never on the gate.

- "What does responsible AI mean to you in practice?"
  - **A:** Four practices, not posters. First, evals that include harm cases — every suite I own carries a 40-case adversarial set, and it gates merges like unit tests. Second, monitoring for the real failure modes: hallucination rate, refusal skew, cost anomalies, with thresholds that page. Third, honest interface design — citations, surfaced uncertainty, and a visible escalation path instead of a confident veneer. Fourth, documented limits: every feature ships with a one-pager on what it must never be used for. On our support copilot this caught a policy-doc regression before users did, because the eval saw what the demo couldn't. Responsible AI is an engineering discipline with a budget, owners, and deadlines.

- "Tell me about a time you advocated for a user-centric approach when the team was focused on technical metrics."
  - **A:** Our summarizer hit 94% on the automatic eval, but when I read 50 real conversations, 15% of "passing" summaries omitted what users actually needed — refund timelines. I pushed to add a user-rated usefulness signal: thumbs plus task-completion follow-ups on 10% of sessions. It was initially unpopular because it made our number worse, but it redirected two sprints toward faithfulness on action items. Six months later, unassisted task completion rose from 61% to 79% while the automatic eval stayed green. I trust metrics only as far as they predict user value — and when they diverge, I side with the user.

---

## Leadership and Ownership Questions

These questions test initiative, accountability, and influence:

- "Tell me about a time you led a technical initiative without being asked."
  - **A:** I noticed prompt and model changes shipped with no regression net — one careless rewrite away from a silent quality collapse. Over two weeks of side-time I built a 120-case eval suite from production traces and support escalations, wired it into CI as a merge gate, and kept runs under four minutes so nobody bypassed it. It caught four regressions the next quarter, including a prompt rewrite that would have dropped tool-calling accuracy from 91% to 68%. Nobody asked for it; the win was making it cheap enough to adopt. Within six months two other teams copied the pattern, and it became the org's default safety net.

- "Describe a situation where you had to influence a decision without formal authority."
  - **A:** Our principal architect wanted to fine-tune a model for policy Q&A; I believed retrieval plus prompt engineering would get there faster and cheaper. I had no authority, so I ran a three-day bake-off on the same 150-question eval: RAG hit 88% faithfulness versus the fine-tune's 84%, cost roughly a tenth per query, and — decisive for him — updated via document refresh instead of training cycles. I presented the numbers, engaged his concerns directly rather than routing around him, and he changed his own recommendation. The fine-tune budget went to eval tooling instead. Influence without authority is data plus respect; arguing from intuition loses both.

- "How have you mentored or upskilled teammates on AI topics?"
  - **A:** I ran a six-week "Evals 101" lunch series for five backend engineers who'd inherited AI features without an AI background — one hour weekly, each session ending with them writing real eval cases for their own services. I paired on each person's first AI pull request and reviewed their guardrail designs before launch. Within a quarter all five had shipped AI changes without my sign-off, and their eval coverage went from zero to about 45 cases per service. The compounding effect was the real win: two of them now run the series themselves, and my review load dropped measurably.

- "Tell me about a time you pushed back on a requirement that you thought was technically infeasible or ethically problematic."
  - **A:** Leadership asked for a chatbot contractually guaranteed never to give a wrong answer, for an enterprise client. I pushed back in writing: our best system ran 2–3% error on sampled queries, and promising zero was misrepresentation risk, not ambition. I proposed what was buildable — confidence-gated routing to humans, citations on every claim, and an SLA on response quality rather than perfection. Legal and the client accepted the reframing; the feature shipped with a 1.1% escalated-error rate and the contract renewed. "Here's what true looks like" saved us from a promise we'd certainly break. I escalate early, in writing, with an alternative attached.

- "Describe a time when you took ownership of a production incident. What was the outcome?"
  - **A:** Our support copilot began citing a return policy that didn't exist — traced to a retrieval change that mixed stale documents into the index. I was on-call and took point even though the pipeline wasn't mine: disabled the affected tool within 20 minutes of the alert, identified all 2,300 exposed conversations across three days, and drafted the customer notification myself. Then the unglamorous half — I ran the RCA, added a citation-verification check that blocks answers whose claims don't match retrieved chunks, and a freshness canary on the index. Hallucination on policy questions fell from 11% to under 2%, and that incident class never recurred.

- "How do you decide what to build vs. what to buy vs. what to skip?"
  - **A:** Three questions: is it a differentiator, is it verifiable, what's the switching cost? We bought the vector database — commodity, well-operated, storage isn't our edge. We built the eval harness — differentiator, domain-coupled, and every vendor schema fought our trace format. We skipped "AI-suggested replies" entirely after I showed a 200-line rules heuristic matched the model on 88% of cases at 1% of the latency cost — the LLM now handles only the genuinely ambiguous 12%. The discipline I defend most is skip: sometimes AI is an answer to a problem that never needed it, and saying so early is the highest-leverage decision.

### Amazon Leadership Principles (Common Framework)

Amazon's 16 leadership principles are used as the basis for behavioral interviews at Amazon and increasingly adapted by other companies:

| Principle | AI Engineering Relevance |
|-----------|------------------------|
| Customer Obsession | Building AI systems that solve real user problems, not tech demos |
| Ownership | Taking responsibility for model behavior in production |
| Invent and Simplify | Finding simple solutions to complex AI problems |
| Are Right, A Lot | Having good judgment about when to use AI vs. traditional approaches |
| Learn and Be Curious | Staying current with the rapidly evolving AI landscape |
| Hire and Develop the Best | Mentoring others in AI engineering practices |
| Insist on Highest Standards | Not accepting high hallucination rates or poor evaluation |
| Think Big | Envisioning how AI transforms entire product categories |
| Bias for Action | Shipping AI features while maintaining safety guardrails |
| Frugality | Optimizing token costs and compute efficiency |
| Earn Trust | Being transparent about AI limitations with stakeholders |
| Dive Deep | Debugging complex AI system failures |
| Have Backbone | Pushing back on unethical AI applications |
| Deliver Results | Measuring and demonstrating AI impact |
| Strive to Be Earth's Best Employer | Creating inclusive AI teams |
| Success and Scale Bring Responsibility | Building AI systems that scale safely |

---

## Problem-Solving and Ambiguity Questions

These questions test how you navigate the inherent uncertainty of AI systems:

- "Tell me about a time when an AI system you built behaved unexpectedly in production. How did you diagnose and fix it?"
  - **A:** Three weeks post-launch, our copilot's citation accuracy slid from 93% to 81% with no deploy. Traces showed errors concentrated in recently updated documents — that was the clue. Root cause: a re-embedding job ran with a newer embedding model, so new chunks and old chunks lived in incompatible vector spaces; retrieval "worked" while returning semantically stale neighbors. I rebuilt the full index under a pinned model version, tagged every chunk with an embedding version, and made rebuilds canary against a 60-query golden set. Accuracy recovered to 96% and stayed. The fix was boring — the diagnosis was the work, and it came from diffing traces by document age, not luck.

- "Describe a situation where you had to make a decision without enough data. What did you do?"
  - **A:** We had to launch invoice extraction in a new market with zero labeled examples and a two-week deadline. Rather than wait, I manufactured a little evidence: 25 synthetic invoice variations, the model's output hand-checked on 30 real documents with a native-speaker reviewer, and three go/no-go signals — field accuracy above 90%, refusal rate under 5%, zero format crashes. We shipped behind a flag, reviewed a 10% sample daily, and fed every correction back as eval cases. Field accuracy reached 94% within three weeks. Waiting for perfect data would have cost the quarter; small data, tightly measured, kept us moving without gambling.

- "How do you approach problems where there's no clear 'right' answer? (e.g., model selection, prompt design)"
  - **A:** I convert it into a measurement problem and pre-commit to criteria. Choosing a model last spring, I defined the decision as: faithfulness ≥ 90% on our 200-case eval, p95 latency under 1.2 seconds, cost under $0.004 per query. One candidate scored a point higher on accuracy but cost 3x and added 400ms — under our criteria it lost, and the one-pager I wrote survived the next "but the leaderboard says" debate. Prompt design gets the same discipline: fixed bake-off, fixed eval, commit to the winner, log the tradeoff. "Right" in AI engineering is whatever your evals define — so the real work is writing honest evals.

- "Tell me about a time when the requirements for an AI feature were vague. How did you clarify and move forward?"
  - **A:** The request was "make search smarter." Instead of guessing, week one was five user interviews plus 200 real queries pulled from support logs, distilled into three measurable candidate definitions: correct-source retrieval, answer-with-citation rate, search-to-resolution time. The product lead picked "users find the answer in the first response," and we built the eval set from the support tickets themselves. We shipped hybrid retrieval with reranking; first-response resolution rose 12 points in two months. A vague requirement stops being vague the moment it has a number and a user quote attached. I treat ambiguity as an agenda for conversations, not a blocker.

- "How do you handle situations where different stakeholders have conflicting requirements for an AI system?"
  - **A:** Legal wanted the copilot to refuse anything uncertain; sales wanted confident answers everywhere — the same threshold, opposite directions. I refused to resolve it by seniority and made the tradeoff visible instead: I plotted refusal rate against accuracy across six confidence thresholds, showed legal their preferred setting refused 30% of good answers, and showed sales theirs let through 9% wrong ones. We landed on tiers: direct answers above 0.8 confidence, citations for 0.5–0.8, human handoff below. Both signed off because the number was theirs to move, not mine. Stakeholders stop fighting each other when they're arguing with data.

- "Describe a time when you had to pivot from one approach to another mid-project. What triggered the change?"
  - **A:** Six weeks into fine-tuning a ticket classifier, interim evals showed the prompted base model within one point — 87% versus 88% — while our fine-tune still needed data cleanup, a training pipeline, and an inference budget. The trigger was the eval, not an opinion. I wrote up the comparison, recommended pivoting to the prompted version with the fine-tune deferred, and we shipped two months early roughly $40K under budget. The fine-tune later became justified — once 50K clean labeled examples existed and the gap widened. Sunk cost is a fine-tune you keep training out of pride; the eval decides, not the calendar.

---

## AI-Specific Behavioral Questions

These are unique to AI engineering and test your experience with the realities of building AI systems:

### Handling Model Failures
- "Tell me about a time a model you deployed started producing bad outputs. What did you do?"
  - **A:** Contain first, diagnose second. Our extraction model's field accuracy fell from 96% to 79% over a weekend with no code change, so I routed the affected document class to manual review before bad data reached billing. An afternoon of trace-diffing found the cause: the provider had silently updated the default model snapshot. I pinned every call to an explicit version, added a daily 50-case canary eval on production traffic, and set an alert at a 3-point accuracy drop. Accuracy returned same day, and the canary has since caught two more snapshot drifts before users noticed. You don't own a model you can't pin.

- "How have you handled a hallucination incident in production?"
  - **A:** A customer escalated that our support copilot had invented a "30-day price-match guarantee" — complete with a fake policy citation. Within the hour I disabled the promotions tool, pulled every conversation touching refund or pricing policy — 412 over five days — and flagged them for review. The fix was two layers: generation constrained to retrieved passages with an entailment check that suppresses unsupported claims, and human routing when retrieval confidence runs low. Grounded-hallucination rate on sampled queries fell from 11% to 1.8% and has held for a year. I still open incident talks with that fake-guarantee screenshot — it's why evals aren't optional.

- "Describe a time when a model update caused a regression. How did you detect and respond?"
  - **A:** A prompt rewrite meant to tighten formatting dropped our tool-calling eval from 96% to 71% — caught in staging, not production, which is the part I emphasize. The new "output JSON only" instruction conflicted with the model's tool-call protocol and silently truncated arguments. I bisected the diff against the eval suite, isolated the offending instruction that afternoon, and shipped the fix in two days. Systemically, I converted the failure into 25 permanent regression cases; the suite then flagged three of the next four prompt-change regressions pre-merge. A regression that only happens once is wasted — converting incidents into eval cases is the whole return.

- "What's your process for responding to a prompt injection attack on a live system?"
  - **A:** Contain, patch, harden, review — I've run it live. A user hid instructions inside a document our RAG agent retrieved, telling it to email customer records "per policy." The output filter caught the unauthorized tool call and paged me; I revoked the session's tool grants within minutes and verified nothing left. Patch: instruction/data isolation so retrieved content can't carry directives, plus per-session tool allow-lists and confirmation gates on exfiltration-shaped actions. Harden: an 80-case injection eval suite now gates every release. Review: a joint postmortem with security made injection testing mandatory for each new tool. Preparation is what made the response boring.

### Autonomous Agent Safety & Incident Response (2026 Standard)
- "Tell me about a time an autonomous agent attempted an unintended destructive action (e.g., executing an unapproved API mutation, schema drop, or email blast). How did your human-in-the-loop guardrail catch it?"
  - **A:** Our ops agent, working an ambiguous cleanup ticket, planned a drop-and-recreate of an analytics table as step two — plausible-sounding, catastrophic, and outside the ticket's intent. The human-in-the-loop gate held it: destructive SQL requires a rendered plan with row-count previews and an explicit approver, and the on-call engineer rejected it in review. Root cause was an under-specified ticket plus a tool schema that permitted DDL at all. We scoped the agent's database role to read-only with writes through a narrow typed API, added plan diffs, and required second approval above 1,000 rows. That gate has since blocked two more plausible-looking mistakes. The safe default is "no."

- "How do you conduct post-mortems when an agentic swarm experiences an uncontrolled recursion loop or token cost explosion?"
  - **A:** Blameless, but built for agent failure modes. When our three-agent swarm looped — a reviewer kept rejecting a writer's output, the writer kept retrying — it burned 1.2M tokens and $1,900 in 18 minutes before on-call killed it. The postmortem reconstructed the message graph from traces, established that no per-run budget existed, and produced three controls: max iterations per node, a global token-budget circuit breaker, and escalation-to-human after three consecutive rejections. Recurrence in eight months: zero. The format is the discipline — timeline, blast radius in dollars, control gaps, owners, due dates — and it reopens monthly until every action item closes. Loops are an architecture smell; the postmortem should say so.

- "How do you define service-level objectives (SLOs) and rollback criteria for non-deterministic AI features?"
  - **A:** You can't SLO "correctness" directly, so I define observable proxies with statistical windows. For our copilot: faithfulness ≥ 95% on a daily 200-sample LLM-judge eval calibrated against human labels, refusal rate between 3% and 15% — both directions matter — p95 latency under 2.5 seconds, and cost per session under $0.08. Rollback is pre-agreed and mechanical: two consecutive daily windows below any threshold auto-rolls-back to the last green prompt and model pin; a single catastrophic window — faithfulness under 80% — rolls back immediately. Deciding thresholds before launch, with the PM in the room, is what makes rollback automatic at 2 a.m. instead of negotiable.

### Ethical Dilemmas
- "Tell me about a time you identified a potential bias in an AI system you were building. What did you do?"
  - **A:** While building evals for a support-triage classifier, I sliced error rates by customer locale and found it misrouted non-native English speakers to self-service at twice the rate — a 14-point gap our aggregate 92% accuracy completely hid. I paused the rollout that week, brought the slice data to the PM as a written launch blocker, and we fixed it: 800 balanced examples collected, a per-locale fairness threshold added to CI — builds fail on gaps over 4 points — and monthly slice monitoring. The gap closed to 3%. The habit I kept: aggregates are where bias hides, so my evals slice by default and fail loudly on disparities.

- "Have you ever refused to build something on ethical grounds? What was the situation?"
  - **A:** Once, and I'd do it again. A sales-led request asked for voice-emotion detection on support calls to auto-score agents — "for coaching," though the rollout plan included disciplinary dashboards. I declined in writing with three attachments: peer-reviewed evidence that affect recognition from voice is unreliable across accents, regulatory exposure under Illinois BIPA and the EU AI Act's emotion-recognition ban, and a proposed alternative — an opt-in, agent-visible QA rubric. Leadership took the alternative. The refusal landed because it was evidence-based and shipped with an option B, not just a "no." I refuse rarely; when I do, I bring receipts.

- "How do you handle requests to build AI features that could be misused?"
  - **A:** I threat-model the request before building it. Before shipping bulk content generation, the obvious misuse was spam and astroturfing at scale, so I wrote a one-page abuse model — top three misuses, each with a control priced in: per-account rate limits, domain blocklists, anomaly detection on volume spikes, and immutable generation logs for abuse response. Then I got product and legal to co-sign the abuse model, making the tradeoffs a joint decision rather than mine alone. In month one we throttled an account generating 40x normal volume. Anything powerful enough to be useful is misusable — the question is whether controls were designed in, not bolted on.

- "Describe a time when you had to balance business pressure with responsible AI practices."
  - **A:** Under a board-demo deadline, I was pressured to launch an agent feature without red-teaming — "it's just a demo." I bought three days by cutting scope, then ran a 48-hour focused red-team with two volunteers. We found a jailbreak that made the agent disclose internal pricing — which would have happened on screen, in front of the board. We shipped three days late with the jailbreak patched and a filter we kept permanently. The outlasting outcome: red-teaming became a scheduled pre-launch phase, not a negotiable line item. I don't frame this as saying no — I bring the risk quantified and the cheapest mitigation attached.

### Stakeholder Communication About AI Limitations
- "How do you explain LLM limitations to non-technical stakeholders?"
  - **A:** No jargon, live failure demos, and numbers tied to their decisions. I open alignment meetings by showing the model confidently wrong on a question from the stakeholders' own domain — watching it invent a plausible policy number does more than any slide. Then three failure archetypes in their language: it makes things up, it isn't consistent run-to-run, and it doesn't know what it doesn't know — each with our measured rate and mitigation. I close with what that means for their roadmap: safe now, needs human review, avoid for now. The test of a good explanation: they repeat the limitation accurately to their own team a week later.

- "Tell me about a time you had to push back on unrealistic AI expectations from leadership."
  - **A:** Leadership wanted a docs assistant "as good as ChatGPT, guaranteed accurate, live in two weeks." Instead of arguing, I spent one day prototyping on 50 real user questions and brought the transcript: 76% fully correct, 12% partially wrong, 12% confidently wrong — wrong ones highlighted. Then I negotiated scope: three weeks, citations on every claim, a feedback button, and a target of 90% on our own question set — not a guarantee. We hit 92% at three months and 96% at six, and the meeting ended with OKRs everyone had signed. Data drawn from the stakeholders' own questions beats opinion in every one of these conversations.

- "How do you set appropriate expectations about what AI can and cannot do?"
  - **A:** With an artifact, not a conversation. Every AI feature I ship carries a one-page internal system card in plain language: what it does well with our eval numbers, known failure modes with real examples, what it must never be used for, and the escalation path when it's wrong. I walk it through at kickoff — not post-launch — and keep a live quality dashboard public so expectations track reality instead of the launch demo. On our copilot, tickets tagged "AI gave wrong info" dropped about 40% after the card and dashboard shipped, mostly because people stopped asking it questions it was never designed to answer.

- "Describe a time when you had to communicate a production AI failure to executives."
  - **A:** Structure: what broke, who's affected, what we did, what it costs, what changes. When our copilot hallucinated refund policies, I sent a five-line email within two hours — plain numbers, no hedging: 412 customers saw incorrect policy info over five days, the tool was disabled at 09:40, outreach underway, root cause identified, permanent fix ETA Friday. A full RCA followed in 72 hours with owners and dates. What I deliberately avoided: burying it, blaming the vendor, or shrugging that "AI is unpredictable." Our VP of Support later opened an all-hands using my exact framing. Early, blunt, factual communication is how trust survives failures.

- "How do you explain the concept of hallucination to a product manager who wants guaranteed accuracy?"
  - **A:** I say it directly: it will sometimes produce fluent, confident nonsense, and no prompt or product choice eliminates that — you choose where the residual error goes. Then I make it concrete: our measured rate is 2–3% on your use case, so at 10,000 answers a week that's 200–300 wrong ones. Options for where those errors land: visible citations so users can verify, confidence gating so uncertain answers route to humans, or silent acceptance. What doesn't exist is zero — vendors claiming it are hiding their error rate. That conversation reliably ends with the PM choosing citations plus escalation, which is the right engineering answer.

### Working with AI Tools
- "How do you use AI coding tools in your workflow? What's your verification process?"
  - **A:** Daily, but asymmetrically. AI writes my boilerplate, tests, and refactor scaffolding — maybe 30–40% of code by volume — while architecture, prompts, and eval logic stay hand-written. Verification is boring and non-negotiable: every AI-generated line passes the same gates as human code — tests, type checks, review. I read every diff before commit, and for anything touching prompt or parsing logic I add a test the assistant didn't think of, because it optimizes for looking right. The number I watch: my PR revert rate hasn't moved since adopting these tools. The productivity is real; unverifiable code is how it evaporates.

- "Tell me about a time an AI tool gave you wrong output and how you caught it."
  - **A:** A coding assistant suggested a pandas merge using a parameter that doesn't exist — plausible name, clean code, fails at runtime. I caught it reading the diff: I couldn't find the flag in our pinned version's docs, checked, and the API test confirmed my read. Sneakier: it once summarized a dependency's license as MIT when it was Apache-with-clause — caught by opening the LICENSE file, which is now a checklist item for me. My rule since: the assistant's confidence carries zero information about correctness. That's not distrust — it's the same review bar I'd apply to any junior engineer's pull request.

- "How do you decide when to use AI assistance vs. doing something manually?"
  - **A:** Two axes: how verifiable the output is, and how much context matters. High-volume, mechanically checkable work — test variations, migration scripts, docstrings, regex — goes to AI because correctness is cheap to prove; it saved us roughly a week on a 400-file logging migration. Anything where being subtly wrong is expensive and hard to detect — system design, data contracts, eval design, anything shaping model behavior — I do manually, using AI only to enumerate alternatives I then check. The trap is delegating the second category because the first went well. My heuristic: if I can't say how I'd detect a wrong answer, I haven't earned the automation yet.

- "What's your approach to staying productive when the AI landscape shifts under you (new models, new frameworks)?"
  - **A:** I anchor on what doesn't change: retrieval, structured outputs, eval-driven iteration, and the operational layer — cost, latency, safety. Models are the most swappable layer, so I architect for it: every model call sits behind an interface with a pinned version, and a candidate swap is just a re-run of the 200-case eval suite. When a major new model landed last spring, my migration was one day and two config lines, while a peer team with prompt logic scattered everywhere spent three weeks. I also budget four hours weekly for deliberate learning so shifts feel scheduled, not traumatic. Depth in the stable layers makes the shifting layer cheap.

## STAR / SAIL Framework

### STAR Framework (Traditional)

| Component | Description | AI Engineering Example |
|-----------|-------------|----------------------|
| **S**ituation | Set the context | "Our RAG pipeline was hallucinating 15% of the time in production" |
| **T**ask | What you needed to do | "I needed to reduce hallucination to under 5% without increasing latency" |
| **A**ction | What you actually did | "I implemented a citation verification pipeline and adjusted retrieval parameters" |
| **R**esult | The measurable outcome | "Hallucination rate dropped to 3.2%, latency increased by only 80ms, and user satisfaction improved 22%" |

### SAIL Framework (Better for AI Engineering)

SAIL is a newer framework better suited for AI engineering because it emphasizes learning — critical in a field where hindsight always reveals better approaches:

| Component | Description | AI Engineering Example |
|-----------|-------------|----------------------|
| **S**ituation | Set the context | "Our agent system was getting stuck in loops 8% of the time" |
| **A**ction | What you did | "I implemented loop detection, max iteration limits, and a self-correction mechanism" |
| **I**mpact | Measurable outcome | "Loop rate dropped to 0.3%, cost per session decreased 40%" |
| **L**earning | What you'd do differently | "I learned that prevention is cheaper than correction — I'd design the agent with loop awareness from the start next time" |

**Why SAIL works better for AI**: The "Learning" component shows maturity. AI engineering is iterative — the best candidates demonstrate that they learn and adapt from every experience.

---

## AI Engineering-Specific Stories to Prepare

You should have 6–8 stories ready, each covering a different theme:

| # | Theme | Key Points to Hit |
|---|-------|-------------------|
| 1 | **Production failure** | What broke, how you detected it, how you fixed it, what you learned |
| 2 | **Ambiguous requirements** | How you clarified, what you built, how you validated |
| 3 | **Stakeholder pushback** | What they wanted, why you disagreed, how you navigated it |
| 4 | **Cost or latency optimization** | The problem, the solution, the measurable impact |
| 5 | **Ethical or safety concern** | What you noticed, what you did, the outcome |
| 6 | **Cross-functional collaboration** | Who you worked with, the challenge, the result |
| 7 | **Technical leadership** | What you led, the obstacles, the impact |
| 8 | **Learning from failure** | What went wrong, your role, what you'd do differently |

**Pro tip**: Each story should work for multiple questions. Your "production failure" story can also answer questions about ownership, problem-solving, and communication.

---

## Common Mistakes

1. **Being too vague.** "We improved the system" → "We reduced hallucination rate from 15% to 3% by implementing citation verification." Specifics matter.

2. **Taking all the credit.** Say "I" for your specific contributions, "we" for team achievements. Over-claiming is a red flag.

3. **No learning or reflection.** Stories without a "what I'd do differently" component signal a lack of growth mindset.

4. **Ignoring the human side.** Behavioral interviews test interpersonal skills, not just technical outcomes. Include how you communicated, collaborated, and navigated disagreement.

5. **Not preparing AI-specific stories.** Generic SWE behavioral stories (deployed a microservice) don't demonstrate AI engineering maturity. You need stories about hallucination, prompt injection, cost management, and stakeholder communication about AI limitations.

6. **Being negative about past employers.** Even if your last company made bad AI decisions, frame it constructively: "I advocated for X because Y, but the decision went another way. Here's what I learned from the outcome."

7. **Memorized, robotic delivery.** Your stories should feel natural, not rehearsed. Practice enough to be fluid, but not so much that you sound scripted.

8. **Not answering the actual question.** Listen carefully. If they ask about "influencing without authority," don't tell a story about technical debugging. Pick the right story for the right question.

9. **Focusing only on successes.** Your best behavioral stories include failure. "I tried X, it didn't work because Y, so I tried Z" shows adaptability and resilience.

10. **Underestimating the round.** Many candidates treat behavioral as a "soft" round and under-prepare. At companies like Amazon and Anthropic, behavioral rounds are heavily weighted and can be the deciding factor.

---

> **Next**: [Home Assignments →](06-home-assignments.md)
