"""Audit a local, pinned field-guide dataset; never scrape or call an LLM."""

import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import yaml


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of silently overwriting evidence."""


def mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)


def read(path):
    record = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)
    if not isinstance(record, dict):
        raise ValueError(f"{path}: expected a YAML mapping")
    return record


def histogram(counter):
    return dict(sorted(counter.items(), key=lambda item: (-item[1], item[0])))


def analyze(checkout, expected_commit):
    checkout = checkout.resolve()
    commit = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if commit != expected_commit:
        raise ValueError(f"source commit mismatch: expected {expected_commit}, got {commit}")
    base = checkout / "job-market"
    dirty = subprocess.check_output(
        ["git", "-C", str(checkout), "status", "--porcelain", "--untracked-files=all", "--", "job-market"],
        text=True,
    )
    if dirty:
        raise ValueError("source job-market files are modified or untracked")
    structured = base / "data_structured"
    raw = base / "data_raw"
    if not structured.is_dir() or not raw.is_dir():
        raise ValueError("both data_structured and data_raw directories are required")
    dates = sorted(p.name for p in structured.iterdir() if p.is_dir())
    if not dates:
        raise ValueError("no scrape directories found")
    for date in dates:
        datetime.date.fromisoformat(date)
    latest = dates[-1]
    counts = {}
    ids = set()
    fingerprint = hashlib.sha256()
    roles = collections.Counter()
    skills = collections.Counter()
    companies = set()
    descriptions = collections.Counter()
    models = collections.Counter()
    prompts = collections.Counter()
    missing_urls = 0
    missing_descriptions = 0
    for date in dates:
        files = sorted((structured / date).glob("*.yaml"))
        if not files:
            raise ValueError(f"empty scrape directory: {date}")
        raw_files = {p.name for p in (raw / date).glob("*.yaml")}
        if raw_files != {p.name for p in files}:
            raise ValueError(f"raw/structured file membership mismatch: {date}")
        seen = set()
        for path in files:
            for source in (path, raw / date / path.name):
                fingerprint.update(str(source.relative_to(base)).encode() + b"\0")
                fingerprint.update(hashlib.sha256(source.read_bytes()).digest())
            record = read(path)
            meta = record.get("meta")
            position = record.get("position")
            if not isinstance(meta, dict) or not isinstance(position, dict):
                raise ValueError(f"{path}: missing meta/position mapping")
            job_id = str(meta.get("job_id", "")).strip()
            if not job_id or job_id in seen:
                raise ValueError(f"{path}: empty or duplicate job_id in scrape")
            seen.add(job_id)
            ids.add(job_id)
            original = read(raw / date / path.name)
            if str(original.get("job_id", "")) != job_id:
                raise ValueError(f"{path}: raw/structured job_id mismatch")
            if date != latest:
                continue
            role = position.get("ai_type")
            if not isinstance(role, dict) or not isinstance(role.get("type"), str):
                raise ValueError(f"{path}: missing classification")
            roles[role["type"]] += 1
            categories = position.get("skills")
            if not isinstance(categories, dict):
                raise ValueError(f"{path}: missing skills mapping")
            tags = set()
            for values in categories.values():
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    raise ValueError(f"{path}: skill categories must be lists of strings")
                tags.update(values)
            skills.update(tags)
            company = record.get("company")
            if not isinstance(company, dict) or not isinstance(company.get("name"), str):
                raise ValueError(f"{path}: missing company name")
            companies.add(company["name"])
            models[str(meta.get("model") or "unknown")] += 1
            prompts[str(meta.get("prompt_sha") or "unknown")] += 1
            description = original.get("description")
            if not isinstance(description, str) or not description.strip():
                missing_descriptions += 1
            else:
                normalized = " ".join(description.split()).casefold()
                descriptions[hashlib.sha256(normalized.encode()).hexdigest()] += 1
            if not original.get("url"):
                missing_urls += 1
        counts[date] = len(files)
    n = counts[latest]
    return {
        "schema_version": 1,
        "source_repository": "https://github.com/alexeygrigorev/ai-engineering-field-guide",
        "source_commit": commit,
        "data_fingerprint_sha256": fingerprint.hexdigest(),
        "scrape_record_counts": counts,
        "total_observations": sum(counts.values()),
        "distinct_job_ids_across_scrapes": len(ids),
        "latest_scrape": latest,
        "latest_scrape_records": n,
        "latest_distinct_company_names": len(companies),
        "latest_extracted_role_labels": histogram(roles),
        "latest_extraction_models": histogram(models),
        "latest_extraction_prompt_hashes": histogram(prompts),
        "latest_raw_missing_urls": missing_urls,
        "latest_raw_missing_descriptions": missing_descriptions,
        "latest_duplicate_description_groups": sum(v > 1 for v in descriptions.values()),
        "latest_records_in_duplicate_description_groups": sum(v for v in descriptions.values() if v > 1),
        "latest_exact_skill_tags": [
            {"tag": tag, "records": count, "percent_of_latest_records": round(100 * count / n, 2)}
            for tag, count in histogram(skills).items()
        ],
        "limitations": [
            "Single-source convenience sample; not a worldwide labor-market estimate.",
            "Scrape dates are observations, not job publication dates or new-hire counts.",
            "Repeated job IDs across scrapes are not independent openings.",
            "Exact extracted tags are LLM annotations, not verified skill requirements.",
            "Company names are counted as stored; subsidiaries and spelling variants are not merged.",
            "Duplicate descriptions are counted, not silently removed from the denominator.",
            "No salaries, causal trends, regional shares, or extraction accuracy are inferred.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="local checkout of the upstream field guide")
    parser.add_argument("--expected-commit", required=True, help="full reviewed upstream SHA")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.expected_commit) != 40 or any(c not in "0123456789abcdef" for c in args.expected_commit):
        parser.error("--expected-commit must be a full lowercase Git SHA")
    try:
        result = analyze(args.checkout, args.expected_commit)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    except (ValueError, OSError, yaml.YAMLError, subprocess.CalledProcessError) as error:
        print(f"Analysis failed: {error}", file=sys.stderr)
        return 1
    print(f"Analyzed {result['total_observations']} observations; latest scrape {result['latest_scrape']}: {result['latest_scrape_records']} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
