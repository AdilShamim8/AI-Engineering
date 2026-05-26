# GitHub Search Methodology

How we found 100+ actual take-home assignments on GitHub.

Primary tool: `gh search repos` (GitHub CLI).

Search query patterns:

- `gh search repos "ai engineer" "take home"` - 40+ actual take-home assignments
- `gh search repos "ai engineer" "assignment" OR "task"`
- `gh search repos "rag" "interview" OR "assignment"`
- `gh search repos "llm" "assignment" OR "task"`
- `gh search repos "genai" "assignment" OR "take-home"`
- `gh search repos "agent" "ai" "hiring" OR "interview"`
- `gh search repos "hiring" "challenge" "ai" OR "ml" OR "data"`

Parameters: `--limit 100`, `--json name,url,updatedAt,description`, `--jq` for filtering.

Filtering criteria (include only):

- Actual home assignments given to candidates
- Q4 2025 / Q1 2026 timeframe
- AI Engineer specific (LLMs, RAG, Agents, GenAI)

Excluded:

- Interview prep tools (e.g., "rag-interview-coach")
- Framework implementations (e.g., "ollama-langchain-agents")
- Coding challenge platforms
- Non-AI assignments (fraud detection, credit scoring)

Quality indicators for genuine assignments:

- Description contains: "take-home", "interview", "assignment", "assessment", "challenge"
- Repo name includes company name or role
- Recent updates (2025-2026)
- Clear problem statement in README


## Results

- 100+ genuine AI Engineer interview assignments found on GitHub
- RAG systems remain the most common (40%+)
- Agentic systems growing fast (30%+), including multi-agent orchestration
- LLM-as-judge evaluation emerging as a distinct assignment type
- Voice AI and real-time transcription as a new category
- Common tech stack: LangChain/LangGraph + OpenAI + FastAPI + vector DB + Groq

See [github-repos.md](github-repos.md) for the full list of repos.
