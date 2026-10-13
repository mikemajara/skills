# Worked example: "what does fitting a model mean?" (generic)

This is a storyboard for a data-science explainer. It shows how one set of characters carries a 9-scene story. All data is synthetic.

**Takeaway:** "Fitting = turning a formula's knobs until its guesses match past data as closely as possible."
**Characters:** 10 example rows (price, weekend, units sold) → 10 dots → a line with red miss lines → three miss bars.
**Key transformation:** the table rows fly into a scatter plot (scene 1). Everything after happens to those dots.

| # | Scene | Steps → snap end states | Kit pieces |
|---|---|---|---|
| 1 | The goal | table readable → rows fly into dots, axes in | `morph` (xLead, small arc), example-data note |
| 2 | Formula with knobs | tokens assemble → two knob cards → formula shrinks to a chip | HTML tokens |
| 3 | Hunting for the best line | bad guess → overshoot → best line (error ✓) | parameter keyframes, `counter({tone})` |
| 4 | The loss | bars grow → bars become squares → squares merge into the average | unit-square geometry |
| 5 | Hands-on | drag two handles to fit the line; "your error" vs. "best possible" | `dragHandle` ×2, unpinned |
| 6 | What `fit()` does | start → big steps → convergence (the loss curve draws in) | precomputed iterations |
| 7 | More inputs, more knobs | knob rows arrive one by one → "same recipe" note | HTML rows |
| 8 | Underfit → overfit | simple → good → wiggly; train vs. test error diverge | interpolated curve samples, log chart |
| 9 | Honest testing | 52 weeks draw in → last 8 = TEST ✓ → random 8 = ✗ | color interpolate + lift + label |
| — | Questions, recap | sticky card stack; list reveal | unpinned |

**What changed after review** (these lessons are encoded in the kit):
- Handles drawn as SVG groups scrolled the page while dragging on phones. They became HTML buttons over the SVG.
- A big arc in the rows-to-dots flight looked like a vertical column mid-way. The fix was a small arc with x leading.
- Readers stopping mid-step saw half-finished frames, so steps now snap to end states with no inertia.
- The first draft used many accent colors and glows. It was cut back to one accent, with red/green only for good/bad, each with ✓/✗.
- Some scenes were too long, about 3 screens each. Tightening them to about 0.55 screens per step made the page feel faster and less "stuck".
