# GroceryPal Color Palette

**Version:** 1.0 — Locked April 27, 2026
**Use these exact hex codes.** Anyone editing the Figma file should add these as Color Styles in the file's local styles so they're reusable across screens.

---

## Primary

| Role | Hex | Use |
|---|---|---|
| **Brand Green** | `#2D8B3F` | Primary CTAs (LOG IN, Import Recipe, View Map), active nav state, savings/positive indicators, logo accent, progress bars (in-budget) |
| **Brand Green Dark** | `#1F6B2D` | Hover/pressed state for primary CTAs, secondary accents within green elements |
| **Brand Green Light** | `#E8F5EC` | Backgrounds for green-tinted callouts (e.g., "You Saved $28.70" pill background), success message backgrounds |

## Neutrals

| Role | Hex | Use |
|---|---|---|
| **Text Primary** | `#1F2937` | Body text, headings, default icon color |
| **Text Secondary** | `#6B7280` | Subheadings, captions, less important info, placeholder text |
| **Text Tertiary** | `#9CA3AF` | Disabled text, meta info (timestamps, "1 hour ago") |
| **Border** | `#E5E7EB` | Card borders, dividers, inactive progress track, input field borders |
| **Background** | `#FFFFFF` | Default screen background, card backgrounds |
| **Background Subtle** | `#F9FAFB` | Section backgrounds, alternate row striping |

## Semantic

| Role | Hex | Use |
|---|---|---|
| **Success / In Budget** | `#2D8B3F` | Same as Brand Green — for budget bar when under threshold |
| **Warning / Approaching** | `#F59E0B` | Budget bar between 80–95% used; "almost out" indicators |
| **Error / Over Budget** | `#DC2626` | Budget bar over 100%; over-budget alerts; destructive action buttons |
| **Info** | `#3B82F6` | Current location pin on map, informational tooltips |

---

## Usage Rules

1. **Only one accent color in any single screen.** Don't mix the warning amber and the brand green on the same view unless one is conveying a meaningful state (e.g., budget bar is amber because spending is at 85%).
2. **Active nav state is always Brand Green.** Inactive nav icons use Text Primary (`#1F2937`).
3. **Savings and positive financial indicators are always Brand Green** — both background pills (Brand Green Light fill, Brand Green text) and standalone text (Brand Green directly).
4. **Don't introduce new colors without team agreement.** If a screen seems to need a color that's not in this palette, raise it in the group chat first.

## Quick Reference for the Demo Flow

- **Login screen:** LOG IN button = Brand Green fill with white text
- **Home / List Builder:** Active "Home" nav icon = Brand Green Filled variant
- **Recipe screen:** "Import" button = Brand Green fill with white text; "Cancel" = Border/Text Secondary
- **Optimized Grocery List:** "You Saved $28.70" = Brand Green Light pill background with Brand Green text; "View Map" button = Brand Green fill
- **Map:** Pins = Brand Green; current location = Info Blue
- **Dashboard:** Progress bar (31% — well under budget) = Brand Green fill; pie chart can use a mix of brand green tints for category differentiation
