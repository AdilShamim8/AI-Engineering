# Theory Questions

Based on candidate reports from Reddit, X, and personal blogs about what they were actually asked in AI engineering interviews.

This section covers knowledge-based questions: "What is X?", "How does X work?", "Explain Y".

## Format

Typically 45-60 minutes, conversational. The interviewer asks conceptual questions to probe your understanding of AI/ML topics. There is no coding or whiteboard - just a back-and-forth discussion.

Theory questions rarely appear as a standalone round. They're usually woven into other rounds: system design, project deep dives, or dedicated AI/ML technical screens. Some companies have a dedicated "LLM theory" or "AI deep-dive" round, but more commonly these questions surface as follow-ups when you mention a concept and the interviewer wants to see how deep your understanding goes.


## Interview Questions

Actual questions reported by candidates and interviewers, compiled from blog posts, video transcripts, and interview guides.

### LLM Practice

Understanding how LLMs work and how to control their behavior, without going into architecture internals.

- How do LLMs work? [^proptech-founder-2]
- What is temperature and top-p sampling? How do they affect outputs? [^fahd-mirza] [^reddit-genai-consulting] [^x-aryyann8]
- What is the context window and what happens when you exceed it? How do you handle long documents? [^fahd-mirza] [^exponent-openai-ml] [^hn-46319888] [^llmgenai]
- How do you do memory management and context management with LLMs? [^reddit-ai-eng-questions]

### RAG Systems

Connecting LLMs to external knowledge so they answer from your data.

- What's RAG? Explain the complete process. [^khushal-kumar] [^reddit-ai-eng-questions] [^reddit-genai-consulting]
- Text vs Vector search. When would you use each? [^reddit-clear-genai]
- You're making a system for huge PDF reports. How would you process them? [^proptech-founder-1]
- How would you handle the problem of a model hallucinating when no information is found in the given context? [^proptech-founder-2]
- What are common RAG failure points and how do you debug them? [^reddit-clear-genai] [^reddit-grilled-rag] [^x-athletickoder-2]
- How do you handle citations and source attribution in a RAG system? [^proptech-founder-1]
- What is semantic caching? [^designgurus-rag] [^hn-44796765]
- How do you scale a RAG system to 10M+ articles?  [^bhavishya-pandit]
- What are the key tradeoffs when designing a RAG system? [^reddit-genai-product]


### Agents and Tool Use

LLM-powered systems that can reason and take actions.

- What makes an AI system agentic? [^techeon] [^reddit-ai-agentic] [^reddit-devsindia-genai] [^hn-43884713] [^hn-42431361] [^x-aryyann8] [^process-analysis]
- What are the essential components of an agent beyond an LLM? [^techeon] [^reddit-expdevs-agentic] [^reddit-ai-agentic]
- How do agents decide which tool to use? [^techeon] [^reddit-csuk-agents] [^reddit-aiagents-prep]
- When agent is the wrong solution? [^techeon] [^reddit-csuk-agents]
- How do you explain agentic systems to non-technical stakeholders? [^techeon] [^reddit-expdevs-agentic]
- How do you detect and stop infinite planning loops? [^techeon] [^reddit-csuk-agents] [^reddit-expdevs-agentic]
- How do you implement termination conditions in long-running agents? [^techeon]
- How do you sandbox tool execution safely? [^techeon] [^reddit-expdevs-agentic]
- How do you handle tool failures, retries, and idempotency? [^techeon] [^reddit-expdevs-agentic] [^reddit-csuk-agents] [^reddit-aiagents-prep]
- What are the biggest security risks with tool-using agents? [^techeon] [^reddit-expdevs-agentic] [^datainterview-mistral]
- How do you create an agent for analyzing customer support tickets, drafting responses, and escalating complex issues. [^promptlayer]
- Build an agent reviewing code and suggesting improvements. [^promptlayer]


### Testing and Evaluation

The AI equivalent of software QA, made harder by non-deterministic outputs.

- How do you ensure the output from LLMs is consistent and accurate? [^proptech-founder-1]
- How do you evaluate a chatbot? [^process-analysis] [^reddit-clear-genai] [^exponent-openai] [^reddit-grilled-rag]
- What metrics do you consider when evaluating LLM performance? [^proptech-founder-1] [^fahd-mirza] [^reddit-genai-product] [^reddit-llm-interview-prep]
- How do you build a golden dataset for evaluation? [^proptech-founder-1]
- How do you detect and mitigate hallucinations? [^process-analysis] [^reddit-ai-eng-questions] [^reddit-genai-consulting] [^hn-41541053] [^hn-46873753] [^system-design-handbook]  [^interviewnode]
- How would you prevent factual errors in a summarization system? [^interviewnode]
- How do you debug a RAG chatbot giving confident but wrong answers? [^process-analysis] [^datainterview-mistral]
- How do you evaluate a RAG pipeline? [^mimansa-jaiswal]
- How do you evaluate agent performance? What metrics matter (tool selection quality, action advancement, context adherence)? [^reddit-aiagents-prep]


### Monitoring

What happens after you deploy.

- What operational/business metrics matter for AI systems? [^reddit-eightfold-ai]
- How would you evaluate and monitor a model in production, not just offline? [^reddit-swe-to-ai]
- How would you test a new model before full deployment? [^x-akshay-pachaar-1] [^hn-44875256]
- How do you measure hallucination rate in production? [^buildml] [^llmgenai] [^hn-46959695] [^hn-42313401]
- How do you monitor and observe autonomous agent behavior in production? [^reddit-expdevs-agentic] [^reddit-csuk-agents]


### Cost and Latency Optimization

Making AI systems affordable and fast.

- How do you reduce latency in GenAI applications? [^proptech-founder-2]
- What is time to first token and why does it matter for user experience? [^proptech-founder-1]
- How would you benchmark each LLM call in a multi-step pipeline to identify latency bottlenecks? [^proptech-founder-1]
- How do you reduce token costs? [^process-analysis] [^reddit-prep-ai-eng] [^hn-46229585] [^hn-46695170] [^system-design-handbook]
- Cost vs. quality trade-offs: when is a small open-source model "good enough"? [^reddit-genai-consulting] [^proptech-founder-2]
- What is model tiering? When do you route to a small distilled model vs. a large LLM? [^interviewnode] [^hn-42793253] [^hn-47150302]
- Your app gets 1M queries/day - how do you optimize cost? [^process-analysis [^fonzi-ai]
- Estimate the budget for a RAG pipeline at enterprise scale (e.g., 300,000 legal contracts). [^reddit-devsindia-genai]

### Safety and Guardrails

Preventing your AI system from being exploited or causing harm.

- When and how would you implement LLM guardrails? [^proptech-founder-1]
- How do you handle data privacy and PII in prompts and logs? [^reddit-genai-consulting] [^reddit-expdevs-agentic]
- How do you protect against prompt injection and jailbreaking? [^system-design-handbook] [^reddit-ai-eng-questions] [^reddit-expdevs-agentic] [^hn-44268335]
- How would you build a system that detects whether content violates policy or contains offensive material? [^igotanoffer]
- Your application generates code that gets executed. How do you prevent malicious code generation and execution? [^proptech-founder-1]


### ML Fundamentals

Classical ML: supervised/unsupervised learning, bias-variance, regularization, data handling, model architectures, interpretability, statistics.

See here: https://github.com/alexeygrigorev/data-science-interviews


## Specialized Topics

These topics are not asked by default in AI engineering interviews.

They come up when the job description specifically requires them - for example, a role focused on model training or a research-adjacent engineer role. If the posting doesn't mention fine-tuning or transformer internals, you're unlikely to be asked about them.

### Fine-tuning and Training

- When would you fine-tune vs use prompt engineering vs RAG? [^process-analysis] [^reddit-prep-ai-eng] [^reddit-genai-consulting] [^x-ashutosh-1]  [^system-design-handbook] [^reddit-prep-ai-eng] [^hn-39748537]
- What is instruction tuning and how does it differ from pre-training? [^hn-46319888] [^llmgenai] [^reddit-llm-interview-prep]
- What is PEFT/LoRA and when would you use it? [^fahd-mirza] [^reddit-genai-consulting] [^x-interviewstack-meta] [^x-aryyann8] [^reddit-llm-interview-prep]
- Explain the RLHF pipeline: supervised fine-tuning, reward model training, and PPO. How does DPO simplify this? [^proptech-founder-1]
- Explain quantization. What are the trade-offs between model size, speed, and accuracy? [^raghu-teja-2] [^reddit-llm-interview-prep]
- How do you convert implicit user behavior (edits, acceptance, rejection) into training signals for model improvement? [^bhavishya-pandit]
- How would you design a model that can solve math problems? Walk through data collection, supervised fine-tuning, post-training, and evaluation. [^igotanoffer]


### LLM Theory

- How do transformers work? [^proptech-founder-2] [^reddit-genai-consulting] [^reddit-ai-eng-questions] [^process-analysis]
- What is the self-attention mechanism? [^sundeep-teki]
- Explain the difference between encoder-only, decoder-only, and encoder-decoder Transformer architectures. When would you use each? [^tidorp] [^hn-46319888] [^reddit-llm-interview-prep]
- What is KV cache? How does it help in LLM inference? [^igotanoffer] [^reddit-llm-interview-prep]
- What is Mixture of Experts (MoE)? How does it improve efficiency? [^mimansa-jaiswal]
- What are the differences between BPE, WordPiece, and character-level tokenization? What are the trade-offs? [^fahd-mirza]



## How to Prepare

Focus on practice over theory. Interviewers care more about how you build, evaluate, and operate AI systems than about transformer internals. The most common questions test RAG systems, agents, and production concerns.

- RAG systems - build a working pipeline end-to-end
- Agents - understand the full architecture: planning, tool use, memory, termination. Key questions: when NOT to use agents
- Testing and evaluation - be able to describe how you build golden datasets

Common mistakes:

- Describing how to build systems but not how to evaluate or monitor them
- Not being able to explain trade-offs - just knowing what something is without knowing when to use it
- Ignoring cost, latency, and failure modes - interviewers want production thinking, not prototype thinking


## Sources

[^bhavishya-pandit]: [Bhavishya Pandit](https://bhavishyapandit9.substack.com/p/7-deep-cut-ai-system-design-interview)
[^buildml]: [BuildML](https://buildml.substack.com/p/top-24-llm-questions-asked-at-deepmind)
[^datainterview-mistral]: [DataInterview - Mistral ML Engineer Interview](https://www.datainterview.com/blog/mistral-machine-learning-engineer-interview)
[^designgurus-rag]: [DesignGurus - RAG System Design](https://www.designgurus.io/blog/system-design-for-rag)
[^exponent-openai]: [Medium - Exponent/Jacob Simon, OpenAI](https://medium.com/exponent/what-its-actually-like-to-interview-at-openai-in-2026-03a646c9436c)
[^exponent-openai-ml]: [Exponent - OpenAI ML Engineer Questions](https://www.tryexponent.com/questions?role=ml-engineer&type=technical)
[^fahd-mirza]: [YouTube - Fahd Mirza](https://www.youtube.com/watch?v=yr5dRHrnbCo)
[^fonzi-ai]: [Medium - Fonzi AI](https://medium.com/fonzi-ai/what-ive-learned-from-sitting-in-on-50-ai-engineer-interviews-c493696453c4)
[^hn-39748537]: [HN - RAG vs. Fine-Tuning](https://news.ycombinator.com/item?id=39748537)
[^hn-41541053]: [HN - LLMs Will Always Hallucinate](https://news.ycombinator.com/item?id=41541053)
[^hn-42313401]: [HN - Automated Reasoning to Remove LLM Hallucinations](https://news.ycombinator.com/item?id=42313401)
[^hn-42431361]: [HN - Agentic LLM Systems in Production](https://news.ycombinator.com/item?id=42431361)
[^hn-42793253]: [HN - AI Orchestration and LLM Routing](https://news.ycombinator.com/item?id=42793253)
[^hn-43884713]: [HN - Is an AI Agent Just an LLM Wrapper?](https://news.ycombinator.com/item?id=43884713)
[^hn-44268335]: [HN - Design Patterns for Securing LLM Agents](https://news.ycombinator.com/item?id=44268335)
[^hn-44796765]: [HN - Sleipner.ai LLM Cost Reduction](https://news.ycombinator.com/item?id=44796765)
[^hn-44875256]: [HN - Interview Questions for AI Product Engineering](https://news.ycombinator.com/item?id=44875256)
[^hn-46229585]: [HN - LLM API Costs in Production](https://news.ycombinator.com/item?id=46229585)
[^hn-46319888]: [HN - LLM Interview Questions](https://news.ycombinator.com/item?id=46319888)
[^hn-46695170]: [HN - Reduce LLM Token Costs with TOON](https://news.ycombinator.com/item?id=46695170)
[^hn-46873753]: [HN - Are LLM Failures Structurally Unavoidable?](https://news.ycombinator.com/item?id=46873753)
[^hn-46959695]: [HN - Early Detection of LLM Hallucinations via ONTOS](https://news.ycombinator.com/item?id=46959695)
[^hn-47150302]: [HN - InferShrink Model Routing](https://news.ycombinator.com/item?id=47150302)
[^igotanoffer]: [igotanoffer - Generative AI System Design Interview](https://igotanoffer.com/en/advice/generative-ai-system-design-interview)
[^interviewnode]: [InterviewNode - GenAI System Design Patterns](https://www.interviewnode.com/post/generative-ai-system-design-interview-patterns-you-should-know)
[^khushal-kumar]: [Medium - Khushal Kumar](https://kaysnotes.medium.com/my-generative-ai-engineer-interview-experience-got-hired-6b3f1affc4e9)
[^llmgenai]: [GitHub - LLM Interview Questions](https://github.com/llmgenai/LLMInterviewQuestions)
[^mimansa-jaiswal]: [Mimansa Jaiswal](https://mimansajaiswal.github.io/posts/llm-ml-job-interviews-resources/)
[^process-analysis]: [Process Analysis - Reddit r/cscareerquestions](https://www.reddit.com/r/cscareerquestions/)
[^promptlayer]: [PromptLayer](https://blog.promptlayer.com/the-agentic-system-design-interview-how-to-evaluate-ai-engineers/)
[^proptech-founder-1]: [YouTube - Proptech Founder Part 1](https://www.youtube.com/watch?v=leXRiJ5TuQo)
[^proptech-founder-2]: [YouTube - Proptech Founder Part 2](https://www.youtube.com/watch?v=Zt-h5BiBWH0)
[^raghu-teja-2]: [Medium - Raghu Teja, IBM Part 2](https://medium.com/@raghu_teja/how-i-cracked-my-ibm-ai-engineer-interview-part-2-ml-scenarios-88af2b46282e)
[^reddit-ai-agentic]: [Reddit - What Agentic AI Am I Supposed to Learn?](https://www.reddit.com/r/ArtificialInteligence/comments/1rceuef/what_agentic_ai_am_i_even_supposed_to_learn) (r/ArtificialIntelligence, Feb 2026)
[^reddit-ai-eng-questions]: [Reddit - AI Engineer Interview Questions](https://www.reddit.com/r/ArtificialInteligence/comments/1nybfr8/ai_engineer_interview_questions/) (r/ArtificialIntelligence)
[^reddit-aiagents-prep]: [Reddit - Interview Prep: Deep Learning to Agentic Systems](https://www.reddit.com/r/AI_Agents/comments/1qrxchn/interview_prep_deep_learning_agentic_systems_what) (r/AI_Agents, Jan 2026)
[^reddit-clear-genai]: [Reddit - How to Clear Interviews in AI/GenAI/RAG/LLM](https://www.reddit.com/r/generativeAI/comments/1p4yrjk/how_to_clear_interviews_in_ai_gen_rag_llm/) (r/generativeAI)
[^reddit-csuk-agents]: [Reddit - AI Engineering Agents Interview Prep](https://www.reddit.com/r/cscareerquestionsuk/comments/1qmybi3/ai_engineering_agents_interview_prep) (r/cscareerquestionsuk, Jan 2026)
[^reddit-devsindia-genai]: [Reddit - Generative AI Engineer Interview Prep](https://www.reddit.com/r/developersIndia/comments/1oq5fdi/got_an_interview_tomorrow_for_a_generative_ai) (r/developersIndia, Nov 2025)
[^reddit-eightfold-ai]: [Reddit - Need Advice for Eightfold.ai Agentic AI Engineer](https://www.reddit.com/r/developersIndia/comments/1pbaj11/need_advice_for_eightfoldai_agentic_ai_engineer) (r/developersIndia)
[^reddit-expdevs-agentic]: [Reddit - Agentic AI System Design Interview](https://www.reddit.com/r/ExperiencedDevs/comments/1r78ipa/agentic_ai_agents_system_design_interview) (r/ExperiencedDevs, Feb 2026)
[^reddit-genai-consulting]: [Reddit - Interview Questions Gen AI (consulting)](https://www.reddit.com/r/learnmachinelearning/comments/1ppgsf3/interview_questions_gen_ai) (r/learnmachinelearning)
[^reddit-genai-product]: [Reddit - Technical Interview for GenAI Engineer Role](https://www.reddit.com/r/leetcode/comments/1rd6yki/technical_interview_for_genai_engineer_role_for_a) (r/leetcode)
[^reddit-grilled-rag]: [Reddit - Got Grilled in an ML Interview for LangGraph/RAG Projects](https://www.reddit.com/r/LangChain/comments/1k662xc/got_grilled_in_an_ml_interview_today_for_my/) (r/LangChain)
[^reddit-llm-interview-prep]: [Reddit - LLM Interview Prep](https://www.reddit.com/r/MachineLearning/comments/1ein9vh/d_llm_interview_prep) (r/MachineLearning)
[^reddit-prep-ai-eng]: [Reddit - How to Prepare for AI Engineering Interviews](https://www.reddit.com/r/datascience/comments/1ovf9k2/how_to_prepare_for_ai_engineering_interviews/) (r/datascience)
[^reddit-swe-to-ai]: [Reddit - From Software Developer to AI Engineer](https://www.reddit.com/r/learnmachinelearning/comments/1pzcw2y/from_software_developer_to_ai_engineer_the_exact/) (r/learnmachinelearning)
[^sundeep-teki]: [Sundeep Teki](https://www.sundeepteki.org/advice/the-ultimate-ai-research-engineer-interview-guide-cracking-openai-anthropic-google-deepmind-top-ai-labs)
[^system-design-handbook]: [System Design Handbook](https://www.systemdesignhandbook.com/guides/generative-ai-system-design-interview/)
[^techeon]: [Medium - TechEon Agentic Guide](https://medium.com/@techeon/the-complete-agentic-ai-system-design-interview-guide-2026)
[^tidorp]: [GitHub - TidorP/MLJobSearch2025](https://github.com/TidorP/MLJobSearch2025)
[^x-akshay-pachaar-1]: [X - Akshay Pachaar, ML Deployment Testing (Netflix)](https://x.com/akshay_pachaar/status/1990034795909582860)
[^x-aryyann8]: [X - AI Engineer Intern Interview](https://x.com/aryyann8/status/2009314129878896960) (Jan 2026)
[^x-ashutosh-1]: [X - Ashutosh Maheshwari, Fine-Tuning vs. Prompting](https://x.com/asmah2107/status/1977413874702745794)
[^x-athletickoder-2]: [X - athleticKoder, RAG System Diagnostics](https://x.com/athleticKoder/status/2002355874786873383)
[^x-interviewstack-meta]: [X - InterviewStack.io, Meta LoRA Question](https://x.com/gnan54796/status/2007302142550565123)
