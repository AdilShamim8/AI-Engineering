# Verification Methodology

How we verify interview questions against real first-person accounts. Many "interview question" articles (especially on Medium) may be AI-generated or speculative.


## Tools

1. Arctic-Shift API (Reddit data, free)

Script: `interview/_internal/fetch_reddit.py`

```bash
cd interview/_internal
uv run python fetch_reddit.py 'https://www.reddit.com/r/ExperiencedDevs/comments/...'
uv run python fetch_reddit.py --batch ../../_work-in-progress/reddit-urls-to-fetch.txt
```

API: `https://arctic-shift.photon-reddit.com/api`. No auth, max 100 comments per request. Saves `.md` and `.json` to `_work-in-progress/reddit-posts/`.

2. x.ai Grok API with search tools (paid)

Script: `interview/_internal/xai_search.py`

```bash
uv run python xai_search.py \
  'Your natural language research prompt here.' \
  --tools web_search,x_search \
  --system 'System prompt' \
  --label 'descriptive-name'
```

Write a natural language prompt, not search-engine keywords. Explicitly tell it which sources to check (Reddit, HN, X/Twitter, Medium). Ask it to be honest when it can't find something. Output saved to `_work-in-progress/grok-responses/`. Cost: typically $500-1000 per query with search tools.

3. Manual verification

For links found by AI agents (ChatGPT, Grok research), we verify each URL directly or via Arctic-Shift. Fabricated/hallucinated links are flagged. Results tracked in `_work-in-progress/link-summaries/`.


## Verification Process

1. Identify single-sourced questions in `questions.md` (especially from potentially AI-generated sources)
2. Search for corroboration using Grok + Arctic-Shift
3. Map corroboration in `_work-in-progress/link-summaries/`
4. Add references to `questions.md` using footnote format `[^source-name]`
5. Discover new questions from fetched threads


## Citation Format

```markdown
- How do you sandbox tool execution safely? [^techeon] [^reddit-expdevs-agentic]
```

Footnotes at the bottom of questions.md:

```markdown
[^reddit-expdevs-agentic]: [Reddit - Agentic AI System Design Interview](https://reddit.com/...) (r/ExperiencedDevs, Feb 2026)
```


## File Structure

```
_work-in-progress/
├── reddit-posts/              # Fetched Reddit threads (.md + .json)
├── reddit-urls-to-fetch.txt   # Batch URLs for fetch_reddit.py
├── grok-responses/            # Full Grok API responses
├── link-summaries/            # Link verification and corroboration maps

interview/_internal/
├── fetch_reddit.py            # Arctic-Shift Reddit fetcher
├── xai_search.py              # Grok API search
├── pyproject.toml
└── main.py
```
