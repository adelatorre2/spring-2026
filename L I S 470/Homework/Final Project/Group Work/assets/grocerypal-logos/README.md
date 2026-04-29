# GroceryPal Logo System — Usage Guide

**Version:** 1.0 — Final, April 28, 2026

This pack contains 16 logo files: 5 lockup types × 3 color variants + 1 dedicated app icon. All text has been outlined to paths, so files render identically in Figma, browsers, and exported assets — no font dependency.

---

## File Index

```
logos/
├── horizontal/                          ← The workhorse — use these most often
│   ├── horizontal-color.svg              Login screen, marketing materials
│   ├── horizontal-black.svg              Print, monochrome contexts
│   ├── horizontal-white.svg              On dark or green backgrounds
│   ├── horizontal-compact-color.svg     ← In-app screen headers (use this!)
│   ├── horizontal-compact-black.svg      Compact monochrome
│   └── horizontal-compact-white.svg      Compact on dark/green
├── stacked/
│   ├── stacked-color.svg                 Splash screen, presentation title slide
│   ├── stacked-black.svg                 Monochrome stacked
│   └── stacked-white.svg                 Stacked on dark/green
├── wordmark/
│   ├── wordmark-color.svg                Tight horizontal spaces, no icon needed
│   ├── wordmark-black.svg                Monochrome wordmark
│   └── wordmark-white.svg                Wordmark on dark/green
├── icon/
│   ├── icon-green.svg                    Standalone bag icon
│   ├── icon-black.svg                    Monochrome icon
│   └── icon-white.svg                    Icon on dark/green
└── app-icon/
    └── app-icon.svg                      iOS-standard 1024×1024, rounded square
```

---

## Quick "Where Do I Use What?" Guide

| Context | Use this file | Notes |
|---|---|---|
| Login screen (large, hero placement) | `horizontal-color.svg` | Resize to ~280px wide |
| Header on every other screen | `horizontal-compact-color.svg` | Resize to ~140px wide, place at top center |
| App splash screen / loading state | `stacked-color.svg` | Or in presentation title slide |
| Presentation title slide / cover page | `stacked-color.svg` | Or app-icon for variety |
| Mobile app icon (mockup of the icon itself) | `app-icon.svg` | The green-square version |
| Favicon / tiny placement | `icon-green.svg` | Or app-icon at small size |
| Avatar placeholder for "GroceryPal" itself | `icon-green.svg` | E.g., system messages |
| Print materials, single-color requirement | `*-black.svg` | Pick the lockup that fits the layout |
| On a green background or dark mode | `*-white.svg` | All-white silhouette versions |

---

## How to Use in Figma

1. **Drag any SVG directly onto the canvas** — Figma will import it as a vector group. You can resize freely without quality loss.
2. **For consistent header placement across screens:**
   - Open one screen (e.g., Home / List Builder)
   - Drag `horizontal-compact-color.svg` onto the canvas
   - Resize to ~140px wide and position in the existing header bar (replacing the current "GroceryPal" text)
   - Right-click → Create Component (Cmd+Option+K)
   - Now you can drag that component onto every other screen's header, replacing the existing text
3. **For the Login screen replacement:**
   - Delete the current image-placeholder box at the top
   - Drag `horizontal-color.svg` onto the canvas
   - Resize to ~280px wide and center horizontally in the upper third of the frame

---

## Sizing Recommendations

| File | Designed at | Min recommended size | Max recommended size |
|---|---|---|---|
| Horizontal Color | 360×80 | 200px wide | No max — vector |
| Compact Horizontal | 200×40 | 100px wide | 200px wide (then use full Horizontal) |
| Stacked | 240×180 | 160px wide | No max |
| Wordmark only | 280×60 | 120px wide | No max |
| Icon only | 64×64 | 16px (favicon) | No max |
| App Icon | 1024×1024 | 60px (smallest iOS) | 1024px (largest iOS) |

---

## Color Reference

The logo uses the locked palette colors:

- **Brand Green:** `#2D8B3F` — used for "Pal" wordmark text and icon strokes
- **Text Primary:** `#1F2937` — used for "Grocery" wordmark text in color version, and for entire wordmark in black version

Don't recolor these manually — if you need a one-off color, ask before doing it. If you need any other variant beyond the 16 included here, file a request and we can generate it consistently.

---

## What's Different From the Earlier Placeholder

The previous placeholder wordmark (`wordmark-placeholder.svg` in the asset pack) is now superseded by this system. You can delete it from Figma if you've used it anywhere — replace with `horizontal-color.svg` (for the login) or `horizontal-compact-color.svg` (for in-app headers).

---

## Don't

- Don't squish, stretch, or skew the logo — always resize proportionally
- Don't add drop shadows, glows, or gradient effects
- Don't separate the icon from the wordmark in horizontal lockups (use the icon-only or wordmark-only variants instead)
- Don't recolor "Pal" to anything other than Brand Green
- Don't put the color logo on a green background (use the white variant instead)
