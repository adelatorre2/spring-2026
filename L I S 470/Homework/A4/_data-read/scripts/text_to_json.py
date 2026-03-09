

#!/usr/bin/env python3
"""text_to_json.py

Reads the plain-text contextual inquiry fieldnotes transcript (a3_fieldnotes.txt)
and converts it into a structured JSON representation.

Design goals:
- Be robust to messy OCR / handwritten transcription.
- Preserve the raw text while also extracting useful structure.
- Produce JSON that downstream scripts can turn into a dataset and visuals.

Expected input characteristics (best-effort):
- Pages/sections often begin with markers like: [PAGE] ...
- Within a page, there may be headings like:
  - Observation Notes
  - Areas to Document
  - Breakdowns & Successes
  - Post-Session Reflection
  - Photo Documentation
  - Additional Session Field Notes
- Bullet lines often begin with '-' or '•'
- Quotes may appear in quotation marks.

Output:
- Writes `a3_fieldnotes.json` alongside the input file by default.

Usage:
  python3 text_to_json.py \
    --input  ../data/a3_fieldnotes.txt \
    --output ../data/a3_fieldnotes.json

"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# -----------------------------
# Helpers / Regex
# -----------------------------

PAGE_RE = re.compile(r"^\s*\[PAGE\]\s*(?P<title>.+?)\s*$")

# Common headings you might see inside a page
HEADING_RE = re.compile(
    r"^\s*(?P<h>(Observation Notes|Areas to Document|ACTIVITY\s+—|CONTEXT\s+—|NEEDS\s*/\s*VALUES\s+—|ASSUMPTIONS\s+—|Breakdowns\s*&\s*Successes|BREAKDOWNS|SUCCESSES|Notable Quotes|Photos Taken|Post-Session Reflection|Top 3 Insights|Biggest Surprise|Questions for Follow-up\s*/\s*Things to Explore|How does this connect to our Focus Objectives\?|Team Debrief Notes|Photo Documentation|Additional Session Field Notes|Additional Screenshots))\s*:?\s*$",
    re.IGNORECASE,
)

# Participant metadata blocks (best-effort)
KEYVAL_RE = re.compile(
    r"^\s*(?P<k>Date|Time|Location|Participant ID|Facilitator|Note Taker|Duration|Participant)\s*:\s*(?P<v>.+?)\s*$",
    re.IGNORECASE,
)

BULLET_RE = re.compile(r"^\s*([-•\u2022]|\*)\s+(?P<text>.+?)\s*$")

# Quote-like lines: either double quotes or single quotes at start
QUOTE_RE = re.compile(r"^\s*[\"“”'](?P<q>.+?)[\"“”']\s*$")

# Time-range line like: 0–5 minutes, 5-12 min, etc.
TIME_RANGE_RE = re.compile(
    r"^\s*(?P<start>\d+)\s*(?:-|–|—)\s*(?P<end>\d+)\s*(?P<unit>min|mins|minutes)\s*$",
    re.IGNORECASE,
)

# Numbered step line like: 1. ..., 2) ...
STEP_RE = re.compile(r"^\s*(?P<n>\d+)\s*[\.|\)]\s+(?P<text>.+?)\s*$")


def normalize_heading(h: str) -> str:
    """Normalize heading strings into stable keys."""
    h = h.strip().lower()
    h = re.sub(r"\s+", " ", h)
    # map some variants
    mapping = {
        "activity —": "activity",
        "context —": "context",
        "needs / values —": "needs_values",
        "assumptions —": "assumptions",
        "breakdowns & successes": "breakdowns_successes",
        "questions for follow-up / things to explore": "follow_up_questions",
        "how does this connect to our focus objectives?": "focus_objectives_connection",
        "photo documentation": "photo_documentation",
        "additional session field notes": "additional_session_field_notes",
        "post-session reflection": "post_session_reflection",
        "notable quotes": "notable_quotes",
        "photos taken": "photos_taken",
    }
    for k, v in mapping.items():
        if h.startswith(k):
            return v
    # fallback
    return re.sub(r"[^a-z0-9]+", "_", h).strip("_")


def strip_invisible(s: str) -> str:
    return s.replace("\ufeff", "").rstrip("\n")


# -----------------------------
# Data structures
# -----------------------------


@dataclass
class Section:
    heading: str
    key: str
    raw_lines: List[str]
    bullets: List[str]
    steps: List[Dict[str, Any]]
    quotes: List[str]
    time_ranges: List[Dict[str, Any]]


@dataclass
class Page:
    title: str
    page_index: int
    metadata: Dict[str, str]
    sections: List[Section]
    raw_lines: List[str]


@dataclass
class Document:
    source_path: str
    created_by: str
    pages: List[Page]


# -----------------------------
# Core parsing
# -----------------------------


def parse_sections(lines: List[str]) -> Tuple[Dict[str, str], List[Section]]:
    """Parse intra-page metadata and sections.

    We scan top-to-bottom. If a line looks like Key: Value, store metadata.
    If a line looks like a heading, start a new section.
    Otherwise, append to current section's raw_lines.

    Additionally, we opportunistically extract bullets, numbered steps,
    quotes, and time ranges inside each section.
    """

    metadata: Dict[str, str] = {}
    sections: List[Section] = []

    current_heading = "body"
    current_key = "body"
    current_raw: List[str] = []

    def flush_current() -> None:
        nonlocal current_heading, current_key, current_raw
        if not current_raw:
            return

        bullets: List[str] = []
        steps: List[Dict[str, Any]] = []
        quotes: List[str] = []
        time_ranges: List[Dict[str, Any]] = []

        for ln in current_raw:
            m_b = BULLET_RE.match(ln)
            if m_b:
                bullets.append(m_b.group("text"))

            m_s = STEP_RE.match(ln)
            if m_s:
                steps.append({"n": int(m_s.group("n")), "text": m_s.group("text")})

            m_q = QUOTE_RE.match(ln)
            if m_q:
                quotes.append(m_q.group("q").strip())

            m_t = TIME_RANGE_RE.match(ln)
            if m_t:
                time_ranges.append(
                    {
                        "start": int(m_t.group("start")),
                        "end": int(m_t.group("end")),
                        "unit": m_t.group("unit").lower(),
                    }
                )

        sections.append(
            Section(
                heading=current_heading,
                key=current_key,
                raw_lines=current_raw,
                bullets=bullets,
                steps=steps,
                quotes=quotes,
                time_ranges=time_ranges,
            )
        )
        current_raw = []

    for ln in lines:
        ln = strip_invisible(ln)
        if not ln.strip():
            # preserve blank lines in raw but don't treat as signals
            current_raw.append(ln)
            continue

        # metadata key/value (best effort)
        m_kv = KEYVAL_RE.match(ln)
        if m_kv:
            k = m_kv.group("k").strip()
            v = m_kv.group("v").strip()
            metadata[k] = v
            # Also keep it in raw in case downstream wants the exact phrasing
            current_raw.append(ln)
            continue

        # headings
        m_h = HEADING_RE.match(ln)
        if m_h:
            flush_current()
            current_heading = m_h.group("h").strip()
            current_key = normalize_heading(current_heading)
            # store heading line in the new section for traceability
            current_raw.append(ln)
            continue

        current_raw.append(ln)

    flush_current()
    return metadata, sections


def split_into_pages(all_lines: List[str]) -> List[Tuple[str, List[str]]]:
    """Split the document into pages based on [PAGE] markers.

    If no [PAGE] markers exist, treat the entire file as a single page.
    """

    pages: List[Tuple[str, List[str]]] = []
    current_title: Optional[str] = None
    current_lines: List[str] = []

    def flush() -> None:
        nonlocal current_title, current_lines
        if current_title is None and not current_lines:
            return
        title = current_title or "Untitled"
        pages.append((title, current_lines))
        current_lines = []

    for ln in all_lines:
        m = PAGE_RE.match(strip_invisible(ln))
        if m:
            # new page begins
            flush()
            current_title = m.group("title").strip()
            continue
        # if first page has no title, we'll assign later
        current_lines.append(strip_invisible(ln))

    flush()

    if not pages:
        return [("Untitled", all_lines)]

    # If first page title is Untitled but the file starts without [PAGE],
    # keep it; downstream can still use it.
    return pages


def parse_fieldnotes(text: str, source_path: str) -> Document:
    all_lines = text.splitlines()
    page_blocks = split_into_pages(all_lines)

    pages: List[Page] = []
    for i, (title, lines) in enumerate(page_blocks):
        metadata, sections = parse_sections(lines)
        pages.append(
            Page(
                title=title,
                page_index=i,
                metadata=metadata,
                sections=sections,
                raw_lines=lines,
            )
        )

    return Document(source_path=source_path, created_by="text_to_json.py", pages=pages)


# -----------------------------
# CLI
# -----------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Convert a3_fieldnotes.txt into structured JSON.")
    p.add_argument(
        "--input",
        required=True,
        help="Path to input transcript (e.g., ../data/a3_fieldnotes.txt)",
    )
    p.add_argument(
        "--output",
        default=None,
        help="Path to output JSON (default: alongside input as a3_fieldnotes.json)",
    )
    p.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON with indentation.",
    )
    return p


def main() -> None:
    args = build_arg_parser().parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        raise FileNotFoundError(f"Input file not found: {in_path}")

    out_path = Path(args.output).expanduser().resolve() if args.output else in_path.with_suffix(".json")

    text = in_path.read_text(encoding="utf-8", errors="replace")
    doc = parse_fieldnotes(text=text, source_path=str(in_path))

    payload = asdict(doc)

    if args.pretty:
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        out_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote JSON: {out_path}")
    print(f"Pages parsed: {len(doc.pages)}")


if __name__ == "__main__":
    main()