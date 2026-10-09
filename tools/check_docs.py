"""Check rendered Python fences and relative Markdown file targets, offline."""

import argparse
import ast
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


def check(root):
    parser = MarkdownIt("commonmark")
    documents = python_blocks = local_links = 0
    errors = []
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "node_modules"} for part in path.relative_to(root).parts):
            continue
        documents += 1
        for token in parser.parse(path.read_text(encoding="utf-8")):
            line = token.map[0] + 1 if token.map else 1
            if token.type == "fence" and token.info.strip() in {"python", "python3"}:
                python_blocks += 1
                try:
                    ast.parse(token.content)
                except SyntaxError as error:
                    errors.append(f"{path.relative_to(root)}:{line}: Python syntax: {error}")
            for child in token.children or []:
                attr = {"link_open": "href", "image": "src"}.get(child.type)
                if not attr:
                    continue
                target = child.attrGet(attr)
                if not target:
                    continue
                url = urlsplit(target)
                if url.scheme or url.netloc or not url.path:
                    continue
                local_links += 1
                resolved = root / unquote(url.path[1:]) if url.path.startswith("/") else path.parent / unquote(url.path)
                if not resolved.exists():
                    errors.append(f"{path.relative_to(root)}:{line}: missing file target: {target}")
    return documents, python_blocks, local_links, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error("--root must be a directory")
    documents, blocks, links, errors = check(root)
    if not documents:
        print("No Markdown documents checked", file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    print(f"Checked {documents} documents, {blocks} Python fences, {links} relative file targets; {len(errors)} errors")
    print("Scope: no external URL, anchor, factual-claim, dependency, or application-runtime verification.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
