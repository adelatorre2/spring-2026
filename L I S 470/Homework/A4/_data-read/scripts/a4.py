#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


# -------------------------
# Helpers
# -------------------------

def clean_text(s: str) -> str:
    s = "" if s is None else str(s)
    s = re.sub(r"\s+", " ", s).strip()
    # remove OCR page markers / noise you often don’t want on sticky notes
    s = re.sub(r"^=== Page \d+ ===\s*", "", s).strip()
    return s

def wrap_for_note(s: str, width: int = 26, max_lines: int = 6) -> str:
    """
    Wrap text for a sticky-note sized box.
    """
    s = clean_text(s)
    if not s:
        return ""
    lines = textwrap.wrap(s, width=width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # add ellipsis to the last line if truncated
        if len(lines[-1]) >= 3:
            lines[-1] = lines[-1][:-3] + "..."
        else:
            lines[-1] = lines[-1] + "..."
    return "\n".join(lines)

def infer_note_type(section_key: str) -> str:
    """
    Map your section_keys to a simple note_type.
    This is mainly for filtering & optional color coding later.
    """
    if section_key in {"notable_quotes"}:
        return "quote"
    if section_key in {"breakdowns", "breakdowns_successes"}:
        return "breakdown"
    if section_key in {"successes"}:
        return "success"
    if section_key in {"observation_notes", "areas_to_document"}:
        return "observation"
    if section_key in {"post_session_reflection", "biggest_surprise"}:
        return "insight"
    if section_key in {"follow_up_questions"}:
        return "question"
    return "other"


# -------------------------
# Step A: Export coding sheet
# -------------------------

def export_notes_to_code_sheet(df: pd.DataFrame, out_csv: Path, min_chars: int = 15) -> pd.DataFrame:
    # keep only sections that typically contain good affinity-note content
    keep_sections = {
        "observation_notes",
        "breakdowns_successes",
        "breakdowns",
        "post_session_reflection",
        "biggest_surprise",
        "follow_up_questions",
        "areas_to_document",
        "team_debrief_notes",
        "additional_session_field_notes",
    }

    d = df.copy()

    # normalize text
    d["text"] = d["text"].map(clean_text)

    # drop empty / tiny lines
    d = d[d["text"].str.len() >= min_chars]

    # keep relevant sections
    d = d[d["section_key"].isin(keep_sections)]

    # add note_type
    d["note_type"] = d["section_key"].map(infer_note_type)

    # stable note_id
    d = d.reset_index(drop=True)
    d["note_id"] = d.index.astype(int)

    # create "sticky-note sized" suggestion (optional)
    d["note_text_wrapped"] = d["text"].map(lambda x: wrap_for_note(x, width=28, max_lines=6))

    # a blank theme column you’ll fill in
    d["theme"] = ""

    # columns to export
    cols = [
        "note_id",
        "participant_id",
        "participant_name",
        "section_key",
        "note_type",
        "text",
        "note_text_wrapped",
        "theme",
        "date",
        "time",
        "location",
    ]
    for c in cols:
        if c not in d.columns:
            d[c] = ""

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    d[cols].to_csv(out_csv, index=False)
    return d[cols]


# -------------------------
# Step B: Render affinity diagram from coded sheet
# -------------------------

@dataclass
class Note:
    note_id: int
    participant_id: str
    theme: str
    text_wrapped: str
    note_type: str

def draw_affinity_diagram(
    coded_df: pd.DataFrame,
    out_png: Path,
    notes_per_col: int = 14,
    note_w: float = 3.2,
    note_h: float = 1.5,
    pad_x: float = 0.25,
    pad_y: float = 0.28,
) -> None:
    """
    Draws themes as columns of sticky notes.
    This looks like an affinity diagram photo: clusters + headers + many small notes.
    """

    # require theme labels
    coded_df = coded_df.copy()
    coded_df["theme"] = coded_df["theme"].fillna("").map(lambda s: s.strip())
    coded_df = coded_df[coded_df["theme"] != ""]

    if coded_df.empty:
        raise ValueError("No themed notes found. Fill in the 'theme' column in output/notes_to_code.csv first.")

    # group by theme
    themes = []
    for theme, g in coded_df.groupby("theme", sort=True):
        g = g.sort_values(["participant_id", "note_id"])
        themes.append((theme, g))

    # figure out layout: each theme is a block with one or more columns
    theme_blocks: List[Tuple[str, List[List[Note]]]] = []
    max_cols = 0

    for theme, g in themes:
        notes = []
        for _, r in g.iterrows():
            notes.append(Note(
                note_id=int(r["note_id"]),
                participant_id=str(r.get("participant_id", "") or ""),
                theme=theme,
                text_wrapped=str(r.get("note_text_wrapped", "") or wrap_for_note(r.get("text", ""))),
                note_type=str(r.get("note_type", "") or "other"),
            ))

        cols = []
        for i in range(0, len(notes), notes_per_col):
            cols.append(notes[i:i + notes_per_col])
        theme_blocks.append((theme, cols))
        max_cols = max(max_cols, len(cols))

    # Canvas sizing
    n_themes = len(theme_blocks)
    # each theme gets (max_cols) columns width
    total_cols = sum(len(cols) for _, cols in theme_blocks)
    fig_w = total_cols * (note_w + pad_x) + 2
    # height = header + notes_per_col notes
    fig_h = (notes_per_col * (note_h + pad_y)) + 2.2

    fig = plt.figure(figsize=(fig_w, fig_h), dpi=220)
    ax = plt.gca()
    ax.set_axis_off()

    # drawing cursor
    x = 1.0
    top_y = fig_h - 1.0

    # simple palette by note_type (kept subtle)
    # NOTE: matplotlib default colors are okay; we’re not setting explicit colors per your earlier preference.
    type_to_alpha = {
        "quote": 0.95,
        "observation": 0.90,
        "insight": 0.90,
        "breakdown": 0.88,
        "question": 0.88,
        "other": 0.85,
    }

    # draw each theme block
    for theme, cols in theme_blocks:
        # theme header spanning its columns
        block_w = len(cols) * (note_w + pad_x) - pad_x
        ax.text(
            x,
            top_y + 0.35,
            theme,
            fontsize=14,
            fontweight="bold",
            va="bottom",
        )
        # underline
        ax.plot([x, x + block_w], [top_y + 0.28, top_y + 0.28], linewidth=1)

        # notes in columns
        for col_idx, col_notes in enumerate(cols):
            col_x = x + col_idx * (note_w + pad_x)
            y = top_y

            for row_idx, note in enumerate(col_notes):
                y0 = y - (row_idx + 1) * (note_h + pad_y)

                # “sticky note” rectangle
                rect = FancyBboxPatch(
                    (col_x, y0),
                    note_w,
                    note_h,
                    boxstyle="round,pad=0.03,rounding_size=0.08",
                    linewidth=1,
                    facecolor="white",
                    alpha=type_to_alpha.get(note.note_type, 0.88),
                )
                ax.add_patch(rect)

                # small participant label (top-right)
                pid = note.participant_id.strip() or "P?"
                ax.text(
                    col_x + note_w - 0.12,
                    y0 + note_h - 0.12,
                    pid,
                    fontsize=8,
                    ha="right",
                    va="top",
                )

                # note text
                ax.text(
                    col_x + 0.12,
                    y0 + note_h - 0.2,
                    note.text_wrapped,
                    fontsize=9,
                    va="top",
                )

        # move cursor to next theme block
        x += block_w + 0.9

    # bounds
    ax.set_xlim(0, fig_w)
    ax.set_ylim(0, fig_h)

    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png, bbox_inches="tight")
    plt.close(fig)


# -------------------------
# Step C: Generate theme summary + needs + POV templates
# -------------------------

def write_theme_summary(coded_df: pd.DataFrame, out_md: Path, examples_per_theme: int = 6) -> None:
    coded_df = coded_df.copy()
    coded_df["theme"] = coded_df["theme"].fillna("").map(lambda s: s.strip())
    coded_df = coded_df[coded_df["theme"] != ""]
    if coded_df.empty:
        raise ValueError("No themed notes found for summary. Fill in the 'theme' column first.")

    lines: List[str] = []
    lines.append("# Themes (from affinity diagram)\n")

    for theme, g in coded_df.groupby("theme", sort=True):
        lines.append(f"## {theme}\n")
        lines.append("**Brief description (edit this):**\n")
        lines.append("- \n")
        lines.append("**Example notes / quotes:**\n")

        # pick a variety
        g2 = g.sort_values(["note_type", "participant_id", "note_id"])
        for _, r in g2.head(examples_per_theme).iterrows():
            pid = str(r.get("participant_id", "") or "P?")
            txt = clean_text(str(r.get("text", "") or ""))
            if len(txt) > 180:
                txt = txt[:177] + "..."
            lines.append(f"- ({pid}) {txt}")
        lines.append("")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def write_user_needs_template(out_md: Path) -> None:
    # This matches the assignment-required pattern.
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(
        "\n".join([
            "# User Needs (pick the 5 strongest)\n",
            "Write each as: **“___ needs a way to ___ because ___.”**\n",
            "1. ___ needs a way to ___ because ___.\n",
            "2. ___ needs a way to ___ because ___.\n",
            "3. ___ needs a way to ___ because ___.\n",
            "4. ___ needs a way to ___ because ___.\n",
            "5. ___ needs a way to ___ because ___.\n",
            "\n",
            "## Extra candidates (optional)\n",
            "- ___ needs a way to ___ because ___.\n",
        ]),
        encoding="utf-8"
    )


def write_pov_template(out_md: Path) -> None:
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(
        "\n".join([
            "# Point of View (10–20 words)\n",
            "Write a short, concrete POV that points toward designs but doesn’t lock into one solution.\n",
            "\n",
            "**POV:** ________________________________\n",
        ]),
        encoding="utf-8"
    )


# -------------------------
# CLI
# -------------------------

def build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="A4 pipeline: export coding sheet + render affinity diagram.")
    p.add_argument("--dataset", required=True, help="Path to a3_fieldnotes_dataset.csv (from json_to_dataset.py)")
    p.add_argument("--outdir", default="../output", help="Output directory (default: ../output)")
    p.add_argument("--make_coding_sheet", action="store_true", help="Export output/notes_to_code.csv")
    p.add_argument("--render", action="store_true", help="Render affinity diagram from output/notes_to_code.csv")
    return p


def main() -> None:
    args = build_argparser().parse_args()
    dataset_path = Path(args.dataset)
    outdir = Path(args.outdir)

    df = pd.read_csv(dataset_path)

    coding_csv = outdir / "notes_to_code.csv"
    affinity_png = outdir / "affinity_diagram.png"
    themes_md = outdir / "themes_summary.md"
    needs_md = outdir / "user_needs.md"
    pov_md = outdir / "pov.md"

    if args.make_coding_sheet:
        export_notes_to_code_sheet(df, coding_csv)
        print(f"Wrote coding sheet: {coding_csv}")

    if args.render:
        if not coding_csv.exists():
            raise FileNotFoundError(f"Missing {coding_csv}. Run with --make_coding_sheet first.")
        coded = pd.read_csv(coding_csv)
        draw_affinity_diagram(coded, affinity_png)
        print(f"Wrote affinity diagram: {affinity_png}")

        write_theme_summary(coded, themes_md)
        print(f"Wrote theme summary: {themes_md}")

        write_user_needs_template(needs_md)
        print(f"Wrote user needs template: {needs_md}")

        write_pov_template(pov_md)
        print(f"Wrote POV template: {pov_md}")


if __name__ == "__main__":
    main()