# GroceryPal — Figma Audit Report

## 1. Frame Inventory

The file contains **13 mobile frames** plus a few floating canvas elements (a stray "image 1," "Top" label, Arrow shapes 15/16/20/21, and three "Contact" components). All mobile frames are 402 × 874 px with 30 px corner radius, suggesting a shared template.

| # | Frame name | Depicts | Fidelity / Notes |
|---|------------|---------|------------------|
| 1 | **Log In** | GroceryPal title, large placeholder image box, email + password fields, LOG IN button, Forgot Password / Create An Account links, social icons row (YouTube, Facebook, Twitter, Instagram, LinkedIn) | Medium. **Placeholder image box still visible** where a logo should be. No keyboard graphic. No bottom nav. |
| 2 | **Home / List Builder** | "GroceryPal" header, search bar, "Your Grocery List" with 3 items (Milk / Bananas / Cottage Cheese), "show more," and 4 large buttons: Import Recipe, History, Dashboard, Groups | Medium-high. Real text. **Full QWERTY keyboard occupies the bottom third** in place of a bottom nav. |
| 3 | **Loading Screen** | "Optimizing your grocery list" headline, **placeholder image box**, subhead "Finding the cheapest stores and best route for your items…" | Medium. Real copy, but the prominent placeholder image box is unfinished. No nav. |
| 4 | **Optimized Grocery List** | "Optimized Grocery List" with two store cards (Trader Joe's: 2% Milk $6.50, Cage-Free Eggs $5.25, Organic Raw Honey $8.00; Target: Blueberries $6.00, Non-Fat Greek Yogurt $5.80, Organic Avocados $4.35), Total Cost $125.50, You Saved $28.70, View Map / Edit List buttons, full bottom nav (Home / Lists / Dashboard / Groups) | **High.** Strongest screen. Only weakness: small placeholder image icons inside each store header tile. |
| 5 | **Map** | Static gray Apple/Google-style map with two map pins connected by a dotted line. Bottom nav present. | Medium. Real-looking map asset, but **no labels on pins** (no store names, no addresses, no distance/time, no current-location dot, no step-by-step). |
| 6 | **Dashboard** | "Alice's Dashboard," Monthly Budget bar ($125.50 spent of $400, 31%), Edit Budget button, Spending Categories pie chart with 4-item legend (Household Essentials / Food & Groceries / Health & Wellness / Other), Recent Purchases list (2% Milk $6.50, Cage-Free Eggs $5.25, Trash Bag $8.99), Suggested Restocks (Paper Towels $13.80, Fabric Softener $12.25), See More buttons, bottom nav | **High.** Densest, most polished screen. |
| 7 | **Recipe** (Import Recipe modal) | "Import Recipe" with instruction text, Take Photo / Upload Image buttons, "Or Paste Recipe Text" with empty box, **Cancle / Import** buttons (typo) | Medium. **Typo: "Cancle"** instead of "Cancel." Empty paste area is fine for a modal but the keyboard graphic + no bottom nav makes it feel chopped. |
| 8 | **Food Sharing-Pantry** | Header "Groups / Shared Pantry," tabs (Pantry / Chats / Activity, Pantry active), section "**Dariy**" (typo), Milk card (added by Amy, "I'll buy" CTA), Eggs card (added by Alice, Claimed). Bottom nav. | Medium-high. **Typo: "Dariy" → "Dairy."** Note "Pantry" tab here = the *shared* group pantry, not the personal pantry. |
| 9 | **Food Sharing-Activity** | Same Groups header; Activity tab active; one item: "Alice will buy Eggs · about 1 hour ago." Bottom nav. | Medium. Mostly empty space; only one event. |
| 10 | **Food Sharing-Chats** | Group chat bubbles: "Hey! Running low on milk again 1 PM," "Amy requested for Milk," "Alice will buy Milk," "I'll grab it on my way home! 1:34 PM." Full QWERTY keyboard, no bottom nav. | Medium. Real text. Avatars are gray silhouette placeholders. |
| 11 | **Food Sharing-Plus Sign** | Modal-style "Add Item" with Item name field (placeholder "e.g., Milk, Bread, Eggs"), Category chips Dairy / Snacks, **Cancle X / Add item +** | Medium. **Typo: "Cancle"** again. Only 2 categories is sparse. Keyboard, no nav. |
| 12 | **Grocery List History** | "Grocery List History," search bar, three list cards: Weekly Groceries (Apr 10, $42), Quick Shopping List (Apr 5, $8.50), Snack List (Apr 1, $18), each with View / Reuse buttons. Keyboard graphic, no bottom nav. | Medium-high. Real content. |
| 13 | **under construction** | "Under Construction — This feature is under construction" with Go Back / Home buttons and "💡 Tip: This feature is coming soon. Stay tuned for updates!" Bottom nav present. | **Low / placeholder.** Frame is literally labeled "under construction" in lowercase in the layers panel. **Will lose points.** |

Floating outside frames: a stray image-box icon, three orphan "Contact" components, several Arrow shapes, and a "Top" label.

---

## 2. Prototype Test (Present Mode)

I launched Present mode and tested every primary CTA on Log In, Home / List Builder, Optimized Grocery List, and Loading Screen, plus pressed F to flash hotspots.

**Result: the prototype is effectively dead.** No transitions fired on any of the following:

- Log In: LOG IN, Create An Account, Forgot Password? — **dead**
- Home / List Builder: Import Recipe, History, Dashboard, Groups, show more — **dead**
- Optimized Grocery List: View Map, Edit List, bottom-nav Home / Lists / Dashboard / Groups — **dead**
- Loading Screen: tap anywhere / auto-advance to Optimized Grocery List — **dead**
- Pressing F revealed **no hotspots** on any screen tested.

**The arrows visible between frames in the canvas are static decorative shapes (named "Arrow 15," "Arrow 16," "Arrow 20," "Arrow 21" in the layers panel), not Figma prototype connections.** Restarting the prototype with R also lands on an empty/non-existent flow start (node 30-1429), suggesting no Flow Starting Point is correctly configured.

Additionally, I saw a **rendering bug on Home / List Builder**: in Present mode the grocery items "Milk / Bananas / Cottage Cheese" do **not** appear — only the X icons render. The text layers are likely positioned outside the parent frame's bounds and get clipped at runtime even though they show in the editor.

**Net effect on grading: the "working prototype connections between screens" requirement is currently failing across the board.**

---

## 3. Visual Fidelity Audit

| Screen | Placeholder image? | Real text? | Issue |
|---|---|---|---|
| Log In | **Yes — large central image box** | Yes | Logo missing |
| Home / List Builder | No | Yes | Items hidden in Present mode |
| Loading Screen | **Yes — central image box** | Yes | Should be a spinner/animation |
| Optimized Grocery List | Small (per-store icon) | Yes | Minor |
| Map | No | Map has no labels/pins/route info | |
| Dashboard | No | Yes (real names + dates + dollars) | Cleanest screen |
| Recipe | No (intentional empty paste area) | Yes | Typo: "Cancle" |
| Food Sharing-Pantry | Avatar silhouette | Yes | Typo: "Dariy" |
| Food Sharing-Activity | Avatar silhouette | Yes | Mostly empty |
| Food Sharing-Chats | Avatar silhouettes | Yes | Fine |
| Food Sharing-Plus Sign | No | Yes | Typo: "Cancle"; only 2 categories |
| Grocery List History | No | Yes | Fine |
| under construction | N/A | "Under construction" copy | **Should be deleted before submission** |

**Consistency across screens:** the GroceryPal header, profile avatar, frame size (402×874), corner radius, and bottom nav (where present) are consistent — that's the foundation of a unified system. **Color is essentially monochrome (black on white)** with no accent color, no brand palette, no semantic color (e.g., green for "saved," red for "over budget"). Typography looks consistent (single sans-serif family at 2–3 weights). Spacing/grid is mostly 16 px padded, but a few elements drift left/right (the X close icons in the grocery list on Home are far right while the item text is mid-left, creating a visual gap).

**The keyboard graphic is the single biggest distractor.** It appears on Home / List Builder, Recipe, Food Sharing-Chats, Food Sharing-Plus Sign, and Grocery List History — five frames. On screens where the user is *not* actively typing (Home / List Builder, Grocery List History), it's not just distracting — it **occupies the bottom-nav slot and breaks the IA**. The keyboard should only appear on screens where a text field is genuinely focused (Recipe paste box, Plus Sign Add Item, Chats compose). For Home and Grocery List History, hide the keyboard and put the bottom nav back.

**No micro-illustrations, no logo, no real product imagery anywhere.** Even the Trader Joe's and Target store cards use the same generic "image" placeholder icon rather than the real store logos. For a "high-fidelity" deliverable that's going to cost points.

---

## 4. Information Architecture Audit

**Bottom navigation:** Home / Lists / Dashboard / Groups appears on Optimized Grocery List, Map, Dashboard, Food Sharing-Pantry, Food Sharing-Activity, and under construction — 6 frames. **It's missing on the other 7** (because the keyboard takes its place on Home, Recipe, Chats, Plus Sign, Grocery List History; Login predates the nav; Loading is full-screen). This inconsistency means a grader cannot orient themselves on roughly half the frames.

**Labels:** Mostly clear ("Dashboard," "Lists," "History," "Import Recipe"). **"Groups" is borderline** — the project goal is *roommate coordination*, but "Groups" could be read as Facebook-style social groups, food groups, or filter groups. A label like **"Roommates"** or **"Household"** would be more transparent. Also, inside the Groups feature, the subhead is "Shared Pantry" but the first **tab** is also called "Pantry" — that creates a label collision with the *project's* sixth feature ("pantry-aware list adjustments"). Two different concepts, same word.

**Hierarchy:** Strong on Dashboard (the budget bar is unmissable; pie chart, recent purchases, restocks each have clear H2-style headers) and Optimized Grocery List (store cards with bold names, prices right-aligned, savings call-out at the bottom). Weak on Home / List Builder — the four big buttons compete with the grocery list for attention, and "show more" sits awkwardly between them. On Map, **nothing draws the eye** because the pins have no labels, no info card, no list of stops.

**Grids / alignment:** Generally OK on a screen-by-screen basis but breaks down in cross-screen comparison. The "X" remove icons on Home are far-right while Optimized Grocery List uses checkboxes left-aligned — same conceptual list, two different patterns. Recent Purchases on Dashboard uses left-aligned name with right-aligned price; Suggested Restocks uses an inline X — two different list patterns next to each other.

---

## 5. Feature Coverage vs. Project Intent

| Core feature | Where shown | Coverage |
|---|---|---|
| 1. **Price comparison across stores** | Optimized Grocery List splits items into Trader Joe's vs. Target with prices and a "You Saved $28.70" total | **Strong** — best-supported feature |
| 2. **Real-time budget tracking** | Dashboard shows "$125.50 spent of $400, 31%" with a progress bar, plus pie chart and recent purchases | **Strong** |
| 3. **Recipe import → auto-generated grocery list** | Recipe screen offers Take Photo / Upload Image / Paste Text. **But** there is no second screen showing the *output* — i.e., extracted ingredients, "added 8 items to your list" confirmation, or differentiation from a normal list | **Partial** — the input exists, the result of importing is invisible |
| 4. **Roommate / group coordination** | Three Food Sharing frames (Pantry, Chats, Activity) plus the Add Item modal | **Adequate** — coverage is there but each tab is sparse |
| 5. **Store routing / map** | Map screen with 2 pins and a dotted line | **Weak** — no store labels on pins, no route order, no distance/time, no "next stop" affordance, no walking/driving toggle |
| 6. **Pantry-aware list adjustments** | **Not represented.** The "Pantry" tab inside Groups is the *shared* pantry, not the personal "you already have milk, removing from list" feature | **Missing** |

**Summary:** features 1, 2, and 4 are demonstrated; feature 3 is half-shown; feature 5 is shown but thin; feature 6 is **absent.**

---

## 6. Recommended 5-Screen Graded Flow

Pick the five strongest, fully-finished frames and wire them as one task. Drop the under-construction, Loading, Map, Login, and most Food Sharing screens from the graded path:

1. **Home / List Builder** (entry point — but hide the keyboard so the bottom nav can show)
2. **Recipe** (Import Recipe modal — the user pastes/uploads)
3. **Optimized Grocery List** (the auto-generated, store-split, price-compared list with "You Saved $28.70")
4. **Map** (route to the cheapest stores — needs labels added; see fixes below)
5. **Dashboard** (post-trip budget impact: $125.50 of $400)

**Task narrative to demonstrate:**
> "Alice opens GroceryPal, taps Import Recipe, pastes a recipe; the app auto-generates an optimized grocery list split between Trader Joe's and Target showing she'll save $28.70; she taps View Map to see the route between the two stores; then taps Dashboard to confirm the trip will only push her to 31% of her $400 monthly budget."

This narrative hits 4 of the 6 core features (price comparison, budget tracking, recipe import, store routing) end-to-end in 5 screens. Roommate coordination and pantry-awareness can be referenced verbally as out-of-scope-for-this-flow.

---

## 7. Top Priorities to Fix Before Submission

### Critical (will lose points if not fixed)

1. **Wire the prototype.** None of the buttons currently link anywhere. At minimum, connect the 5-screen flow above: Home → Recipe (Import Recipe button), Recipe → Optimized Grocery List (Import button), Optimized Grocery List → Map (View Map button), Optimized Grocery List → Dashboard (Dashboard nav button or Map → Dashboard). Set Home / List Builder as the Flow Starting Point. Without this, the "Working prototype connections" requirement fails completely.
2. **Fix the rendering bug on Home / List Builder.** In Present mode, "Milk / Bananas / Cottage Cheese" disappear and only the X icons render — the text layers are likely positioned outside the parent frame and get clipped. Move them inside the frame.
3. **Replace the placeholder image box on Log In** with the actual GroceryPal logo (or even a simple typographic logo). This is the first frame any grader sees and it screams "unfinished."
4. **Replace the placeholder image box on Loading Screen** with a real spinner, illustration, or animated icon. As-is it reads as a missing asset, not a loading state.
5. **Delete or hide the "under construction" frame** before exporting/submitting. It is explicitly flagged as incomplete and there is no reason a grader should land on it.
6. **Fix typos**: "Cancle" → "Cancel" (appears on Recipe and Food Sharing-Plus Sign); "Dariy" → "Dairy" (Food Sharing-Pantry).
7. **Hide the keyboard on screens where no field is focused** — specifically Home / List Builder and Grocery List History. The keyboard is currently sitting on top of where the bottom nav should be, so the IA looks broken on those screens. Keep the keyboard only on Recipe, Plus Sign Add Item, and Chats compose.

### Polish (will gain points)

8. **Add labels to the Map pins** — "Trader Joe's, 0.4 mi" / "Target, 1.1 mi" — and a small bottom card showing "Stop 1 of 2" and total estimated time/cost. Right now the screen reads as a generic map asset, not a routing feature.
9. **Introduce one accent color** (e.g., a green for savings/budget-good, a red/amber for over-budget) and apply it consistently to the "You Saved $28.70" pill, the budget progress bar, and selected nav state. The current monochrome palette is the single biggest reason the design reads as wireframe rather than hi-fi.
10. **Rename "Groups" → "Roommates"** (or "Household") in the bottom nav and rename the inner "Pantry" tab to **"Shared Items"** to eliminate the collision with the project's pantry-awareness feature. If you have time, add even a stub "Pantry" feature on the personal side (a checkbox "I already have this at home" on a list item) so feature 6 gets at least one screen of representation.

If you fix items 1–7 (the criticals), you'll meet the rubric's "5 connected screens, complete simple task, working prototype" line. Items 8–10 are what move the project from "passing" to "strong."