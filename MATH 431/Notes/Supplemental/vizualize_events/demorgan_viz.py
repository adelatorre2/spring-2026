

"""demorgan_viz.py

Generate and save Venn-style diagrams for common event algebra identities
(union, intersection, complement, set difference, symmetric difference,
De Morgan's laws) for two events A and B inside a sample space Ω.

Saves PNGs into the folder:
  /Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Notes/Supplemental/vizualize_events

Usage:
  python demorgan_viz.py

Notes:
- This draws Ω as a rectangle and A,B as overlapping circles.
- Shaded region corresponds to the event expression.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle


# -----------------------------
# Geometry for Ω, A, B
# -----------------------------

@dataclass(frozen=True)
class VennGeometry:
    # Ω box
    x0: float = 0.0
    x1: float = 1.0
    y0: float = 0.0
    y1: float = 1.0

    # Circle A
    ax: float = 0.38
    ay: float = 0.55
    ar: float = 0.28

    # Circle B
    bx: float = 0.62
    by: float = 0.55
    br: float = 0.28


def _circle_mask(xx: np.ndarray, yy: np.ndarray, cx: float, cy: float, r: float) -> np.ndarray:
    return (xx - cx) ** 2 + (yy - cy) ** 2 <= r ** 2


def build_masks(geom: VennGeometry, n: int = 900) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return (xx, yy, omega_mask, A_mask, B_mask)."""
    x = np.linspace(geom.x0, geom.x1, n)
    y = np.linspace(geom.y0, geom.y1, n)
    xx, yy = np.meshgrid(x, y)

    omega_mask = (xx >= geom.x0) & (xx <= geom.x1) & (yy >= geom.y0) & (yy <= geom.y1)
    A = _circle_mask(xx, yy, geom.ax, geom.ay, geom.ar)
    B = _circle_mask(xx, yy, geom.bx, geom.by, geom.br)

    # Only care about regions inside Ω
    A &= omega_mask
    B &= omega_mask

    return xx, yy, omega_mask, A, B


# -----------------------------
# Plotting helper
# -----------------------------

@dataclass(frozen=True)
class EventDiagram:
    filename: str
    title: str
    # compute shaded mask from (omega, A, B)
    expr: Callable[[np.ndarray, np.ndarray, np.ndarray], np.ndarray]


def draw_event_diagram(
    out_path: str,
    geom: VennGeometry,
    masks: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray],
    diagram: EventDiagram,
) -> None:
    xx, yy, omega, A, B = masks
    shaded = diagram.expr(omega, A, B) & omega

    # Plot: light gray background for Ω, then shade event region
    fig, ax = plt.subplots(figsize=(6, 4), dpi=200)

    # Background Ω
    omega_rect = Rectangle((geom.x0, geom.y0), geom.x1 - geom.x0, geom.y1 - geom.y0,
                           facecolor="#f5f5f5", edgecolor="black", linewidth=2)
    ax.add_patch(omega_rect)

    # Shaded region via image mask
    img = np.zeros((shaded.shape[0], shaded.shape[1], 4), dtype=float)
    # RGBA for shading
    img[..., 0] = 0.16  # R
    img[..., 1] = 0.55  # G
    img[..., 2] = 0.86  # B
    img[..., 3] = shaded.astype(float) * 0.55

    ax.imshow(
        img,
        extent=(geom.x0, geom.x1, geom.y0, geom.y1),
        origin="lower",
        interpolation="nearest",
        zorder=1,
    )

    # Circles A, B
    circA = Circle((geom.ax, geom.ay), geom.ar, fill=False, edgecolor="black", linewidth=2, zorder=2)
    circB = Circle((geom.bx, geom.by), geom.br, fill=False, edgecolor="black", linewidth=2, zorder=2)
    ax.add_patch(circA)
    ax.add_patch(circB)

    # Labels
    ax.text(geom.ax - geom.ar * 0.65, geom.ay + geom.ar * 0.9, "A", fontsize=14, weight="bold")
    ax.text(geom.bx + geom.br * 0.45, geom.by + geom.br * 0.9, "B", fontsize=14, weight="bold")
    ax.text(geom.x0 + 0.02, geom.y0 - 0.06, "Ω", fontsize=14, weight="bold")

    ax.set_title(diagram.title, fontsize=13)
    ax.set_xlim(geom.x0 - 0.05, geom.x1 + 0.05)
    ax.set_ylim(geom.y0 - 0.10, geom.y1 + 0.05)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


# -----------------------------
# Event expressions (2-set algebra)
# -----------------------------

def event_library() -> List[EventDiagram]:
    """Common event expressions to visualize for A,B in Ω."""
    return [
        # Basics
        EventDiagram("omega.png", "Ω (certain event)", lambda O, A, B: O),
        EventDiagram("empty.png", "∅ (impossible event)", lambda O, A, B: np.zeros_like(O, dtype=bool)),
        EventDiagram("A.png", "A", lambda O, A, B: A),
        EventDiagram("B.png", "B", lambda O, A, B: B),
        EventDiagram("Ac.png", "Aᶜ", lambda O, A, B: (~A) & O),
        EventDiagram("Bc.png", "Bᶜ", lambda O, A, B: (~B) & O),

        # Union / intersection
        EventDiagram("A_union_B.png", "A ∪ B", lambda O, A, B: A | B),
        EventDiagram("A_inter_B.png", "A ∩ B", lambda O, A, B: A & B),

        # Differences
        EventDiagram("A_minus_B.png", "A \\ B", lambda O, A, B: A & (~B)),
        EventDiagram("B_minus_A.png", "B \\ A", lambda O, A, B: B & (~A)),

        # Symmetric difference
        EventDiagram("A_symdiff_B.png", "A △ B  (symmetric difference)", lambda O, A, B: (A & (~B)) | (B & (~A))),

        # De Morgan (shown both ways)
        EventDiagram("demorgan1_left.png", "(A ∪ B)ᶜ", lambda O, A, B: (~(A | B)) & O),
        EventDiagram("demorgan1_right.png", "Aᶜ ∩ Bᶜ", lambda O, A, B: ((~A) & (~B)) & O),
        EventDiagram("demorgan2_left.png", "(A ∩ B)ᶜ", lambda O, A, B: (~(A & B)) & O),
        EventDiagram("demorgan2_right.png", "Aᶜ ∪ Bᶜ", lambda O, A, B: ((~A) | (~B)) & O),

        # Handy probability identities
        EventDiagram("A_union_Bc.png", "A ∪ Bᶜ", lambda O, A, B: (A | (~B)) & O),
        EventDiagram("Ac_inter_B.png", "Aᶜ ∩ B", lambda O, A, B: ((~A) & B) & O),
        EventDiagram("Ac_union_B.png", "Aᶜ ∪ B", lambda O, A, B: ((~A) | B) & O),
        EventDiagram("Ac_inter_Bc.png", "Aᶜ ∩ Bᶜ", lambda O, A, B: ((~A) & (~B)) & O),
    ]


def main() -> None:
    out_dir = "/Users/alexdelatorre/Documents/School/UW-Madison/SPRING 2026/MATH 431/Notes/Supplemental/vizualize_events"
    os.makedirs(out_dir, exist_ok=True)

    geom = VennGeometry()
    masks = build_masks(geom, n=900)

    diagrams = event_library()
    for d in diagrams:
        out_path = os.path.join(out_dir, d.filename)
        draw_event_diagram(out_path, geom, masks, d)

    # Also write a simple index text file so it's easy to see what's generated
    index_path = os.path.join(out_dir, "_index.txt")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("Generated event diagrams:\n\n")
        for d in diagrams:
            f.write(f"- {d.filename}: {d.title}\n")


if __name__ == "__main__":
    main()