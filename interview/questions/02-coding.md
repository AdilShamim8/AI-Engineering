# Coding Problems

Coding-specific interview content: problems you code or implement, coding round formats, and implementation exercises.


## Coding Round Formats

Two broad categories:

- Implementation rounds (45-90 min): live-coding progressive/multi-level problems
- Algorithm rounds (25-70 min): LeetCode-style problems


## Implementation Rounds

Longer rounds (45-90 min) where you build, refactor, or complete something substantial. Interviewers evaluate code quality, extensibility, and engineering judgment. [^deepthi-sudharsan]

Usually it's a single problem with multiple levels that build on each other. Code must be extensible since each level builds on prior code.

- Implement a website crawler (my personal experience) [^linkjob-anthropic]
- Refactor 100-120 lines of convoluted, deeply nested code. [^exponent-openai]
- Build a key-value database starting with basic operations (SET/GET/DELETE). [^linkjob-anthropic]
- LeetCode 2408: Design SQL. [^hello-interview]
- Unix cd command with symbolic link resolution. [^hello-interview]
- In-Memory Database: Implement SQL-Like Operations. [^hello-interview]
- Credits management system - track credit state across issued and used credits with different expiration rules and usage requirements, with increasing complexity. [^exponent-openai]


### ML / AI Coding

- Debug code handling embeddings. [^promptlayer]
- Implement logistic regression with SGD, L2 regularization, and early stopping in NumPy. [^datainterview-mistral]



## Algorithm Rounds

Focused rounds (15-60 min) with specific problems testing problem-solving depth and DSA knowledge (hash maps, tries, linked lists, graphs, greedy algorithms).

Examples:

- RLE encoding (my personal experience).
- Prime numbers between 0 and 100. [^khushal-kumar]
- LRU Cache with O(1) time complexity. [^devto-xai]
- Reverse a linked list with constraints (AI-assisted coding round - candidate must prompt LLM effectively). [^reddit-microsoft-aiml]
- Find the Excel column name from its column number (e.g., column 702 = "AAA"). [^reddit-microsoft-aiml]



## How to Prepare

Solve LeetCode problems [^hello-interview] [^mimansa-jaiswal]

- Solve 75+ easy/medium problems
- Focus on data structures: lists, sets, hash maps, tries, linked lists

Build projects that mirror interview problems

- Pick a project that has layers of complexity you can add incrementally - this is exactly how progressive interview problems work
- Good project choices: a key-value store (start basic, add TTL, add persistence), a web crawler (start single-threaded, add rate limiting, add distributed)
- Build it clean first, then practice extending it under time pressure. If your initial design can't handle new requirements without rewriting, that's the signal to redesign
- The goal is not the finished project but the experience of making design decisions under constraints

Practice narrating your reasoning [^exponent-openai] [^khushal-kumar]

- AI tools are increasingly allowed during coding rounds
- Interviewers watch how you use them: understanding before implementing, not blindly pasting output
- Practice thinking out loud while coding, whether you're using AI tools or not

Common mistakes:

- Jumping into code without clarifying requirements or asking questions
- Writing rigid code that breaks when follow-up requirements arrive (progressive problems build on prior code)
- Blindly pasting AI tool output without understanding it - interviewers watch for reasoning, not copying
- Not discussing time/space complexity or optimization when prompted

## Sources

[^datainterview-mistral]: [DataInterview - Mistral ML Engineer Interview](https://www.datainterview.com/blog/mistral-machine-learning-engineer-interview)
[^deepthi-sudharsan]: [Medium - Deepthi Sudharsan](https://medium.com/@deepthi.sudharsan/inside-ai-interviews-stories-patterns-and-what-actually-matters-555684c38598)
[^devto-xai]: [dev.to - xAI](https://dev.to/net_programhelp_e160eef28/xai-software-engineer-interview-2026-full-recap-pitfalls-real-prep-tips-2fl0)
[^exponent-openai]: [Medium - Exponent, OpenAI](https://medium.com/exponent/what-its-actually-like-to-interview-at-openai-in-2026-03a646c9436c)
[^hello-interview]: [Hello Interview - OpenAI L5](https://www.hellointerview.com/guides/openai/l5)
[^khushal-kumar]: [Medium - Khushal Kumar](https://kaysnotes.medium.com/my-generative-ai-engineer-interview-experience-got-hired-6b3f1affc4e9)
[^linkjob-anthropic]: [linkjob - Anthropic](https://www.linkjob.ai/interview-questions/anthropic-software-engineer-interview/)
[^mimansa-jaiswal]: [Mimansa Jaiswal](https://mimansajaiswal.github.io/posts/llm-ml-job-interviews-resources/)
[^promptlayer]: [PromptLayer](https://blog.promptlayer.com/the-agentic-system-design-interview-how-to-evaluate-ai-engineers/)
[^reddit-microsoft-aiml]: [Reddit - Microsoft SWE Applied AI/ML Summer 2026](https://www.reddit.com/r/csMajors/comments/1nqfzhq/microsoft_swe_applied_aiml_summer_2026_redmond) (r/csMajors)
