#!/usr/bin/env python3
"""json_to_dataset.py

Convert the structured JSON produced by `text_to_json.py` into a tidy dataset
(CSV + JSONL) suitable for analysis and visualization.

Design goals
- Keep the dataset *long/tidy*: one row per atomic note item (bullet/step/quote/etc.).
- Preserve provenance: section key/heading, order, and (best-effort) session metadata.
- Be resilient to messy handwritten transcripts (missing fields, inconsistent formatting).

Typical usage
  python3 json_to_dataset.py \
    --input  ../data/a3_fieldnotes.json \
    --output ../data/a3_fieldnotes_dataset.csv \
    --jsonl  ../data/a3_fieldnotes_dataset.jsonl

If you don’t specify --output/--jsonl, the script will write next to the input.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass, fields as dc_fields
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

TIME_RANGE_RE = re.compile(
    r"(?P<start>\d{1,2})\s*(?:-|–|—|to)\s*(?P<end>\d{1,2})\s*(?P<unit>min|mins|m)\b",
    re.IGNORECASE,
)

DURATION_RE = re.compile(
    r"\b(?:total\s*time|duration)\s*[:=]?\s*(?P<mins>\d{1,3})\s*(?:min|mins|minutes)\b",
    re.IGNORECASE,
)

DATE_RE = re.compile(
    r"\b(?:date)\s*[:=]?\s*(?P<date>\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|[A-Za-z]+\s+\d{1,2},\s*\d{4})\b",
    re.IGNORECASE,
)

TIME_RE = re.compile(
    r"\b(?:time)\s*[:=]?\s*(?P<time>\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)\b",
    re.IGNORECASE,
)

PARTICIPANT_ID_RE = re.compile(
    r"\bparticipant\s*id\s*[:=]?\s*(?P<pid>.+)\b",
    re.IGNORECASE,
)

NOTE_TAKER_RE = re.compile(
    r"\bnote\s*taker\s*[:=]?\s*(?P<nt>.+)\b",
    re.IGNORECASE,
)

FACILITATOR_RE = re.compile(
    r"\bfacilitator\s*[:=]?\s*(?P<fac>.+)\b",
    re.IGNORECASE,
)

LOCATION_RE = re.compile(
    r"\blocation\s*[:=]?\s*(?P<loc>.+)\b",
    re.IGNORECASE,
)

# e.g. "Participant: Franky (Graduate Student, lives off campus, no meal plan)"
PARTICIPANT_LINE_RE = re.compile(
    r"^\s*participant\s*[:=]\s*(?P<name>[^()]+?)(?:\s*\((?P<details>.*)\))?\s*$",
    re.IGNORECASE,
)


def clean_text(s: str) -> str:
    """Normalize whitespace, keep punctuation."""
    s = s.replace("\u00a0", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def looks_like_quote(s: str) -> bool:
    return bool(re.match(r"^[\"“”']", s.strip()))


def strip_leading_bullet(s: str) -> Tuple[str, Optional[str]]:
    """Remove leading bullet/number markers and return (text, marker)."""
    raw = s
    s = s.strip()

    # Numbered list: "1." / "1)" / "1 -" etc.
    m = re.match(r"^(?P<num>\d{1,2})\s*(?:[.)]|-)?\s+(?P<rest>.+)$", s)
    if m:
        return clean_text(m.group("rest")), m.group("num")

    # Bullets: "-" / "•" / "*"
    m = re.match(r"^(?:[-•*]+)\s+(?P<rest>.+)$", s)
    if m:
        return clean_text(m.group("rest")), "-"

    return clean_text(raw), None


def parse_time_range(s: str) -> Tuple[Optional[int], Optional[int]]:
    m = TIME_RANGE_RE.search(s)
    if not m:
        return None, None
    try:
        return int(m.group("start")), int(m.group("end"))
    except Exception:
        return None, None


# -----------------------------------------------------------------------------
# Output schema
# -----------------------------------------------------------------------------

@dataclass
class Row:
    doc_source: str
    page_index: int
    section_key: str
    section_heading: str
    section_index: int
    item_index: int
    item_type: str  # bullet | step | quote | line
    marker: Optional[str]
    text: str

    # best-effort extracted metadata
    session_index: int
    participant_id: Optional[str]
    participant_name: Optional[str]
    location: Optional[str]
    facilitator: Optional[str]
    note_taker: Optional[str]
    date: Optional[str]
    time: Optional[str]
    duration_mins: Optional[int]

    # optional timing inside the session (e.g., "5–12 min")
    start_min: Optional[int]
    end_min: Optional[int]


# -----------------------------------------------------------------------------
# Core conversion
# -----------------------------------------------------------------------------

def extract_session_metadata(lines: List[str]) -> Dict[str, Optional[str]]:
    """Scan a block of text lines and pull out common header fields.

    Note: the JSON produced by `text_to_json.py` stores text across multiple lists.
    This function expects a simple list of strings.
    """
    out: Dict[str, Optional[str]] = {
        "participant_id": None,
        "participant_name": None,
        "location": None,
        "facilitator": None,
        "note_taker": None,
        "date": None,
        "time": None,
        "duration_mins": None,
    }

    for raw in lines:
        s = clean_text(str(raw))
        if not s:
            continue

        # Participant line variant
        m = PARTICIPANT_LINE_RE.match(s)
        if m and not out["participant_name"]:
            out["participant_name"] = clean_text(m.group("name"))

        m = PARTICIPANT_ID_RE.search(s)
        if m and not out["participant_id"]:
            out["participant_id"] = clean_text(m.group("pid"))

        m = LOCATION_RE.search(s)
        if m and not out["location"]:
            out["location"] = clean_text(m.group("loc"))

        m = FACILITATOR_RE.search(s)
        if m and not out["facilitator"]:
            out["facilitator"] = clean_text(m.group("fac"))

        m = NOTE_TAKER_RE.search(s)
        if m and not out["note_taker"]:
            out["note_taker"] = clean_text(m.group("nt"))

        m = DATE_RE.search(s)
        if m and not out["date"]:
            out["date"] = clean_text(m.group("date"))

        m = TIME_RE.search(s)
        if m and not out["time"]:
            out["time"] = clean_text(m.group("time"))

        m = DURATION_RE.search(s)
        if m and not out["duration_mins"]:
            try:
                out["duration_mins"] = str(int(m.group("mins")))
            except Exception:
                pass

    return out


def is_session_boundary(line: str) -> bool:
    s = clean_text(line).lower()
    if not s:
        return False

    # Common cues that a new "sheet" / session is starting
    return (
        "contextual inquiry field notes" in s
        or s.startswith("=== page")
        or s.startswith("participant:")
        or s.startswith("participant :")
        or s.startswith("date:")
    )


def section_all_lines(sec: Dict[str, Any]) -> List[str]:
    """Return a best-effort list of all text lines for a section.

    `text_to_json.py` commonly emits: raw_lines, bullets, steps, quotes.
    We merge them for boundary/metadata detection.
    """
    lines: List[str] = []
    for k in ("raw_lines", "bullets", "steps", "quotes"):
        v = sec.get(k)
        if isinstance(v, list):
            lines.extend([str(x) for x in v if str(x).strip()])
    return lines


def iter_atomic_items_from_section(
    sec: Dict[str, Any], section_key: str
) -> Iterable[Tuple[int, str, str, Optional[str]]]:
    """Yield (item_index, item_type, text, marker) from a section dict.

    Prefer structured lists (quotes/steps/bullets) and fall back to raw_lines.
    """
    idx = 0

    # Quotes first
    quotes = sec.get("quotes")
    if isinstance(quotes, list):
        for q in quotes:
            t = clean_text(str(q))
            if not t:
                continue
            yield idx, "quote", t, None
            idx += 1

    # Steps (numbered)
    steps = sec.get("steps")
    if isinstance(steps, list):
        for i, st in enumerate(steps, start=1):
            t = clean_text(str(st))
            if not t:
                continue
            yield idx, "step", t, str(i)
            idx += 1

    # Bullets
    bullets = sec.get("bullets")
    if isinstance(bullets, list):
        for b in bullets:
            t = clean_text(str(b))
            if not t:
                continue
            yield idx, "bullet", t, "-"
            idx += 1

    # Fallback: raw lines (avoid emitting exact duplicates of already-emitted text)
    seen = set()
    for k in ("quotes", "steps", "bullets"):
        v = sec.get(k)
        if isinstance(v, list):
            for x in v:
                seen.add(clean_text(str(x)))

    raw_lines = sec.get("raw_lines")
    if isinstance(raw_lines, list):
        for raw in raw_lines:
            s = clean_text(str(raw))
            if not s:
                continue
            if s in seen:
                continue

            text, marker = strip_leading_bullet(s)

            if section_key in {"notable_quotes"} or looks_like_quote(text):
                item_type = "quote"
            elif marker and marker.isdigit():
                item_type = "step"
            elif marker == "-":
                item_type = "bullet"
            else:
                item_type = "line"

            yield idx, item_type, text, marker
            idx += 1


def iter_atomic_items(section_lines: List[str], section_key: str) -> Iterable[Tuple[int, str, str, Optional[str]]]:
    """Backward-compatible iterator (expects pre-flattened lines).

    This is kept for minimal disruption, but the main conversion path uses
    `iter_atomic_items_from_section`.
    """
    dummy_sec: Dict[str, Any] = {"raw_lines": section_lines}
    yield from iter_atomic_items_from_section(dummy_sec, section_key)


def convert(doc: Dict[str, Any]) -> List[Row]:
    rows: List[Row] = []

    doc_source = doc.get("source_path") or "(unknown)"
    pages = doc.get("pages") or []

    for page in pages:
        page_index = int(page.get("page_index", 0))
        sections = page.get("sections") or []

        # We maintain a rolling session index and rolling metadata *within the page*.
        session_index = 0
        session_started = False
        session_meta: Dict[str, Optional[str]] = {
            "participant_id": None,
            "participant_name": None,
            "location": None,
            "facilitator": None,
            "note_taker": None,
            "date": None,
            "time": None,
            "duration_mins": None,
        }

        for s_i, sec in enumerate(sections):
            section_key = sec.get("key") or "(unknown_section)"
            section_heading = sec.get("heading") or ""
            section_lines = section_all_lines(sec)

            # Detect session boundaries inside the stream of sections/lines.
            # If this section contains a boundary cue, increment session index.
            if any(is_session_boundary(x) for x in section_lines):
                # Start a new session when we hit a boundary after a session has started.
                if session_started:
                    session_index += 1
                session_started = True

                # Refresh session metadata from this section
                extracted = extract_session_metadata(section_lines)
                for k, v in extracted.items():
                    if v:
                        if k == "duration_mins":
                            try:
                                session_meta[k] = int(v)  # type: ignore[assignment]
                            except Exception:
                                pass
                        else:
                            session_meta[k] = v

            # If we don’t have good metadata yet, keep trying to extract
            # from important sections like body/observation_notes.
            if section_key in {"body", "observation_notes", "additional_session_field_notes"}:
                extracted = extract_session_metadata(section_lines)
                for k, v in extracted.items():
                    if v and not session_meta.get(k):
                        if k == "duration_mins":
                            try:
                                session_meta[k] = int(v)  # type: ignore[assignment]
                            except Exception:
                                pass
                        else:
                            session_meta[k] = v

            # Produce atomic rows
            for item_index, item_type, text, marker in iter_atomic_items_from_section(sec, section_key):
                start_min, end_min = parse_time_range(text)

                rows.append(
                    Row(
                        doc_source=str(doc_source),
                        page_index=page_index,
                        section_key=section_key,
                        section_heading=section_heading,
                        section_index=s_i,
                        item_index=item_index,
                        item_type=item_type,
                        marker=marker,
                        text=text,
                        session_index=session_index,
                        participant_id=session_meta.get("participant_id"),
                        participant_name=session_meta.get("participant_name"),
                        location=session_meta.get("location"),
                        facilitator=session_meta.get("facilitator"),
                        note_taker=session_meta.get("note_taker"),
                        date=session_meta.get("date"),
                        time=session_meta.get("time"),
                        duration_mins=session_meta.get("duration_mins"),
                        start_min=start_min,
                        end_min=end_min,
                    )
                )

    return rows


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Convert fieldnotes JSON (from text_to_json.py) into a tidy dataset (CSV/JSONL)."
    )
    p.add_argument("--input", required=True, help="Path to a3_fieldnotes.json")
    p.add_argument(
        "--output",
        default=None,
        help="Path to write CSV dataset (default: same folder as input, *_dataset.csv)",
    )
    p.add_argument(
        "--jsonl",
        default=None,
        help="Optional path to write JSONL dataset (one row per line)",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress summary prints",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    in_path = Path(args.input).expanduser().resolve()
    if not in_path.exists():
        raise FileNotFoundError(f"Input JSON not found: {in_path}")

    out_csv = (
        Path(args.output).expanduser().resolve()
        if args.output
        else in_path.with_name(in_path.stem.replace(".json", "") + "_dataset.csv")
    )

    out_jsonl = Path(args.jsonl).expanduser().resolve() if args.jsonl else None

    doc = json.loads(in_path.read_text(encoding="utf-8"))
    rows = convert(doc)

    if not rows and not args.quiet:
        print("WARNING: Produced 0 rows. This usually means the input JSON has no section text content.")
        print("         Inspect ../data/a3_fieldnotes.json to confirm it contains pages/sections with raw_lines/bullets/steps/quotes.")

    # Write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        fieldnames = [f.name for f in dc_fields(Row)]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(asdict(r))

    # Write JSONL (optional)
    if out_jsonl:
        out_jsonl.parent.mkdir(parents=True, exist_ok=True)
        with out_jsonl.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(asdict(r), ensure_ascii=False) + "\n")

    if not args.quiet:
        print(f"Wrote CSV:  {out_csv}")
        if out_jsonl:
            print(f"Wrote JSONL:{out_jsonl}")
        print(f"Rows: {len(rows)}")

        # quick sanity checks / counts
        by_section: Dict[str, int] = {}
        for r in rows:
            by_section[r.section_key] = by_section.get(r.section_key, 0) + 1
        top = sorted(by_section.items(), key=lambda x: x[1], reverse=True)[:12]
        print("Top sections by row count:")
        for k, n in top:
            print(f"  {k:<28} {n}")


if __name__ == "__main__":
    main()