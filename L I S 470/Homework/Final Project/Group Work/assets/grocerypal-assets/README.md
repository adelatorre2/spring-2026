# GroceryPal Asset Pack

**Created:** April 27, 2026
**For:** LIS 470 Final Project — Interactive Mockup
**Team:** GroceryPal (Alejandro, Angelique, Helena, Peixin, Yanbin)

This folder contains all the design assets needed to bring the Figma mockup up to high-fidelity. Drag SVGs directly into Figma — they'll import as vector layers you can resize without quality loss.

---

## Folder Contents

```
assets/
├── colors.md                          ← Locked color palette — read this first
├── icons/
│   ├── nav/                           ← Bottom navigation icons (24×24)
│   │   ├── home-outline.svg
│   │   ├── home-filled.svg
│   │   ├── lists-outline.svg
│   │   ├── lists-filled.svg
│   │   ├── dashboard-outline.svg
│   │   ├── dashboard-filled.svg
│   │   ├── groups-outline.svg
│   │   └── groups-filled.svg
│   └── map/
│       ├── pin-1.svg                  ← Numbered pin for stop 1 (32×40)
│       ├── pin-2.svg                  ← Numbered pin for stop 2 (32×40)
│       └── current-location.svg       ← Blue "you are here" dot (24×24)
├── loading/
│   ├── spinner-static.svg             ← Use this in Figma (static image)
│   └── spinner-animated.svg           ← Animated version (works in browsers, not in Figma canvas)
└── branding/
    └── wordmark-placeholder.svg       ← Fallback logo until Canva version is ready
```

---

## How to Use in Figma

1. **Drag and drop** any SVG file directly onto the Figma canvas. It'll import as a vector group you can resize.
2. **Color edits:** since these SVGs use the locked palette, just open the SVG in Figma's right sidebar and change the fill if needed. To swap a nav icon's state, just replace the outline variant with the filled variant.
3. **For the bottom nav:** create one master nav component using outline icons, then on each screen, swap the icon corresponding to that screen's "active" state to the filled variant, and color its label with Brand Green (`#2D8B3F`).
4. **For the loading screen:** use `spinner-static.svg` — Figma can't render the animation in the canvas, but the static frame still looks like a real loading state.

---

## Icon Design Notes

- **Style:** Outlined / line-art, 1.5px stroke weight, rounded line caps and joins
- **Inactive state:** `#1F2937` (Text Primary)
- **Active state:** `#2D8B3F` (Brand Green) — use the `-filled.svg` variant
- **Grid:** 24×24 viewBox for nav, 32×40 for map pins (taller to accommodate the pin tail)
- **Why outlined?** Matches the existing aesthetic of the Figma file and reads as modern/iOS-native

---

## What's NOT in this pack (handle separately)

- **GroceryPal full logo** — being designed in Canva. Use `wordmark-placeholder.svg` as a fallback or until Canva version is finalized.
- **Trader Joe's logo** — download from https://www.traderjoes.com (check footer for press/media). Use the official PNG/SVG.
- **Target logo** — download from https://corporate.target.com/press/brand-assets. Official PNG/SVG.
- **User avatars** — pull from Canva's stock photo library. Search "diverse college student portrait." Need ~3-4 (Alice as primary, plus Amy and others for Food Sharing screens).
- **Food/grocery item thumbnails** — out of scope for this pass; not critical.

---

## Color Quick Reference

See `colors.md` for the full spec. Most-used colors:

- Brand Green: `#2D8B3F`
- Brand Green Light (for callout backgrounds): `#E8F5EC`
- Text Primary: `#1F2937`
- Border: `#E5E7EB`

---

## Questions?

Drop in the team chat. If anything in this pack doesn't match what you're seeing in Figma, flag it before improvising — better to clarify than to add inconsistency.
