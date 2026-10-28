#!/usr/bin/env python3
"""Build index.html — the monograph-style site map of this repository.

Run from the repository root:  python tools/build_site.py

Assembles tools/site/part*.html into index.html, injecting:
  - FILE_INDEX   : every repo file, scanned from the tree (never hand-typed)
  - LEDGER/FACTS : generated counts (md notes, files indexed, links verified)
  - LECTURE_ROWS : the verified 19-lecture course table

Then verifies every GitHub blob/tree URL embedded in the final HTML resolves
to a real file in this repository. The build fails if any link is broken.
"""
import json, os, re, sys
from urllib.parse import quote, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PARTS = os.path.join(HERE, "site")
OUT = os.path.join(ROOT, "index.html")
GH = "https://github.com/AdilShamim8/AI-Engineering/blob/main/"

SECTION_KEYS = ["101_LLM-Literacy", "102_AI-Application-Development", "103_Agentic AI",
                "104_LLMOps", "105_AI-Evaluation", "106_AI-Security-Safety", "roadmap",
                "interview", "learning-paths", "portfolio", "research", "role", "tools", "webinars"]

UPPER = {"llm","llms","ai","rag","mcp","api","apis","ux","ci","cd","owasp","nist","eu",
         "rlhf","dpo","peft","sft","dsa","ats","aiid","aria","aim","asi","nlp","crm",
         "mmlu","gsm8k","swe","wmdp","orbench","biann","json","txt"}
SPECIAL = {"lora":"LoRA","qlora":"QLoRA","ragas":"RAGAS","trulens":"TruLens",
           "deepeval":"DeepEval","langsmith":"LangSmith","geval":"G-Eval","llmops":"LLMOps",
           "graphrag":"GraphRAG"}
SMALL = {"a","an","the","of","in","vs","for","and","to","with","on","at","by","from","as"}

# The verified course table (titles/durations from 105_AI-Evaluation/course/README.md,
# cross-checked against the CampusX playlist on October 27, 2026).
LECTURES = [
    (1,  "Master LLM Evaluations — playlist overview", "23:24",  "01-course-overview"),
    (2,  "Introduction — Model Evals vs Application Evals", "24:32",  "02-model-vs-application-evals"),
    (3,  "How to Evaluate LLM Applications — the Complete Workflow", "17:00",  "03-evaluation-workflow"),
    (4,  "Why Your AI Application Needs Multiple Eval Pipelines", "28:06",  "04-multiple-eval-pipelines"),
    (5,  "LLM Eval Methods — LLM-as-a-Judge, Reference-Based vs Reference-Free", "53:10",  "05-eval-methods-reference-based-vs-free"),
    (6,  "Offline Evals vs Online Evals", "1:21:09", "06-offline-vs-online-evals"),
    (7,  "LLM Model Evals & Capabilities", "37:52",  "07-model-evals-capabilities"),
    (8,  "What is LLM Benchmarking — Saturation vs Contamination", "51:20",  "08-benchmarking-saturation-contamination"),
    (9,  "What are LLM Benchmarks — Evolution of AI Knowledge Benchmarks", "1:50:47", "09-llm-benchmarks-evolution"),
    (10, "How to Use LLM Leaderboards", "30:07",  "10-llm-leaderboards"),
    (11, "Selecting the Right LLM — Running Custom Model Evals", "1:56:53", "11-model-selection-custom-evals"),
    (12, "How to Answer \"How Do You Evaluate Your RAG App?\" in Interviews", "46:20",  "12-rag-eval-interview-answer"),
    (13, "How to Test RAG Retrievers (Hands-On)", "1:47:02", "13-testing-rag-retrievers"),
    (14, "Evaluating RAG — Generator & Full Pipeline with the RAG Triad", "1:21:29", "14-rag-triad-generator-pipeline"),
    (15, "Mastering G-Eval — the Deterministic LLM-as-a-Judge Framework", "1:26:52", "15-geval-deterministic-judge"),
    (16, "Securing Your RAG Application — Toxicity, Leakage & Scope Drift", "1:35:19", "16-rag-security-toxicity-leakage-scope-drift"),
    (17, "RAG Operational Evals — Building Faster & Cheaper RAG Systems", "1:19:32", "17-rag-operational-evals"),
    (18, "RAG Regression Testing — Preventing Silent AI Failures", "54:16",  "18-rag-regression-testing"),
    (19, "Online Evaluation & Monitoring with LangSmith", "—", "19-online-eval-langsmith-monitoring"),
]

def prettify(filename):
    stem = filename
    for ext in (".md", ".py", ".json", ".txt"):
        if stem.endswith(ext):
            stem = stem[:-len(ext)]
            break
    m = re.match(r"^(\d+)[\s._\-]+(.+)$", stem)
    num, rest = (m.group(1), m.group(2)) if m else (None, stem)
    if " " in rest and any(c.isupper() for c in rest):
        title = rest
    else:
        date = ""
        dm = re.search(r"(\d{4}-\d{2}-\d{2})$", rest)
        if dm:
            date = dm.group(1)
            rest = rest[:dm.start()].strip("-_")
        words = []
        for i, w in enumerate(re.split(r"[-_ ]+", rest)):
            if not w:
                continue
            lw = w.lower()
            if lw in SPECIAL:
                words.append(SPECIAL[lw])
            elif lw in UPPER:
                words.append(lw.upper())
            elif i > 0 and lw in SMALL:
                words.append(lw)
            else:
                if any(c.isupper() for c in w[1:]):
                    words.append(w)
                else:
                    words.append(w[0].upper() + w[1:])
        title = " ".join(words) + ((" " + date) if date else "")
    return (num + " · " + title) if num else title

def natkey(path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path)]

def scan():
    entries = []
    md_count = 0
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in sorted(dirs, key=natkey) if d not in (".git",)]
        for f in sorted(files, key=natkey):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT)
            if rel in ("index.html",):
                continue
            top = rel.split(os.sep)[0]
            if top in SECTION_KEYS:
                s = top
                d = os.path.dirname(rel[len(top)+1:]) if len(rel.split(os.sep)) > 2 else ""
            else:
                s = "root"
                d = ""
            if f.endswith(".md"):
                md_count += 1
            if not f.endswith((".md", ".py", ".json", ".txt")) and rel != "LICENSE":
                continue
            entries.append({
                "p": rel.replace(os.sep, "/"),
                "u": GH + quote(rel.replace(os.sep, "/")),
                "t": "LICENSE (MIT)" if rel == "LICENSE" else prettify(f),
                "s": s,
                "d": d.replace(os.sep, "/"),
            })
    return entries, md_count

def lecture_rows():
    base = "https://github.com/AdilShamim8/AI-Engineering/blob/main/105_AI-Evaluation/course/"
    rows = []
    for n, title, dur, slug in LECTURES:
        rows.append(
            f'      <tr><td class="num">{n}</td><td>{title}</td><td class="dur">{dur}</td>'
            f'<td data-th="Study materials"><a href="{base}{slug}.md">Notes</a> · '
            f'<a href="{base}transcripts/{slug}.md">Transcript</a></td></tr>'
        )
    return "\n".join(rows)

def build():
    parts = []
    for i in (1, 2, 3, 4, 5):
        with open(os.path.join(PARTS, f"part{i}.html"), encoding="utf-8") as fh:
            parts.append(fh.read())
    html = "\n".join(parts)
    entries, md_count = scan()
    idx = json.dumps(entries, ensure_ascii=False, separators=(",", ":"))
    html = (html
            .replace("__FILE_INDEX__", idx)
            .replace("__LECTURE_ROWS__", lecture_rows())
            .replace("__MD_COUNT__", str(md_count))
            .replace("__FILE_COUNT__", str(len(entries)))
            .replace("__BUILD_DATE__", "2026-10-27"))
    # count actual repo links from the final HTML (includes the JSON file index)
    links = re.findall(r'https://github\.com/AdilShamim8/AI-Engineering/(?:blob|tree)/main/[^\s"\'<>)]+', html)
    html = html.replace("__LINK_COUNT__", str(len(links)))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {OUT} ({len(html):,} bytes, {len(entries)} indexed files, {md_count} md notes, {len(links)} repo links)")
    return html, entries, links

def verify(html, entries):
    urls = re.findall(r'https://github\.com/AdilShamim8/AI-Engineering/(?:blob|tree)/main/([^\s"\'<>)]+)', html)
    bad = []
    for u in urls:
        path = unquote(u).rstrip("/")
        if not os.path.exists(os.path.join(ROOT, path)):
            bad.append(path)
    print(f"URL check: {len(urls)} repo links, {len(bad)} broken")
    for b in sorted(set(bad))[:25]:
        print("  BROKEN:", b)
    # lecture completeness
    for _, _, _, slug in LECTURES:
        for sub in (f"105_AI-Evaluation/course/{slug}.md", f"105_AI-Evaluation/course/transcripts/{slug}.md"):
            if not os.path.exists(os.path.join(ROOT, sub)):
                bad.append(sub)
                print("  MISSING LECTURE FILE:", sub)
    return len(bad) == 0

if __name__ == "__main__":
    html, entries, links = build()
    ok = verify(html, entries)
    sys.exit(0 if ok else 1)
