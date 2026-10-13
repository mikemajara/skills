# Scene patterns cookbook

Each pattern lists its **characters**, its **steps (with snap end states)**, and **build notes**. All snippets assume
`var S = ScrollStory, U = S.util;` and an SVG with a `viewBox="0 0 360 300"`-ish canvas.

---

## Table → chart (rows become points)
*Characters:* data rows. *Steps:* (1) the table is readable; (2) rows fly to their (x, y) positions and the axes fade in.
- Draw the table *inside the SVG* as `<text>` rows, plus a small dot at each row's start. Then the dots are the characters.
- Let each row fade as its dot leaves (`U.seg(t, a + i*d, b + i*d)`), so text and axes never overlap for long.
- Use `S.morph(rowPts, chartPts, t, {stagger:.3, arc:10, xLead:.4})`. With a small arc and x leading, it reads like "flying". A large arc looks like a vertical column of dots mid-flight.
- If the table is HTML, use `S.pointsFromDOM(rowEls, svg)` for the start points.

## Formula assembly
*Characters:* formula tokens. *Steps:* tokens appear one by one; the knobs (parameters) get highlighted; the formula shrinks to a corner and stays as a chip for the next scene.
- Use HTML `<span>` tokens with `opacity` and `translateY` set from `t`.

## Sweep to the best (parameter search)
*Characters:* points, a line, residual lines. *Steps:* bad guess → overshoot → close → best.
- Interpolate the parameters between keyframes `[{p, a, c}, …]`. Recompute the residuals and the counter (`error`) on every render.
- Color the counter with `tone` (good when within 15% of best) so the ✓ appears exactly when the line is right.

## Misses → squares → average (explaining a squared loss)
*Characters:* three residual bars. *Steps:* bars grow; bars widen into squares (a negative one flips up); squares merge into one average square with the number.
- Use unit `U = 22px` per value. Square side = |miss|·U. Average square side = √mean·U.

## Scrubbed algorithm (iterations)
*Characters:* the model (line, curve, state) and a history chart. *Steps:* start; first big moves; convergence; "this is what `fit()` does".
- Precompute all iterations up front. In `render`, map `t` to a fractional iteration `k`, interpolate between `k` and `k+1`, and draw the history polyline up to `k`.
- Use `Math.pow(t, 1.5–1.8)` to give the fast early iterations more scroll room.

## Complexity morph (simple → just right → too much)
*Characters:* one curve, two error lines. *Steps:* simple; good; too flexible.
- Precompute samples for each discrete model (for example degree 1…12). For a continuous `d`, interpolate between `floor(d)` and `ceil(d)` samples, so the curve *morphs* smoothly instead of jumping.
- Use a log scale for error charts. Draw the error lines only up to the current `d` so they visibly diverge as you scroll.
- Clip the curve to the plot (`clip-path`) so wild fits don't cover the captions.

## Timeline split (time-based vs. random)
*Characters:* N time points. *Steps:* points draw left to right; the last K slide right into a TEST zone (✓); they return and K random ones light up (✗).
- Interpolate the fill color with `gsap.utils.interpolate(colorA, colorB)` and pair it with a lift (y −10 px) and a label.

## Counting combinations (pairs, paths, possibilities)
*Characters:* N items in a ring. *Steps:* the connections draw in (counter counts up); one highlighted connection carries the punchline.
- Shuffle the draw order with a seeded `U.rng` so lines fill the shape evenly.

## Before / after (product or process pitch)
*Characters:* the same 5–7 task cards. *Steps:* "today" (scattered, red ✗ counters for time/cost); the cards slide into the new flow; the counters tick to the new values (✓).
- Show the value change in one counter per metric. Don't add a separate chart.

## Zoom into a part (anatomy / architecture)
*Characters:* one diagram. *Steps:* whole system; scale/translate the SVG `viewBox` toward one component; that component expands into its parts.
- Animate the `viewBox` (x, y, w, h) by lerping the four numbers. Text stays crisp.

## Sticky card stack (questions, takeaways, options)
- Not pinned. Each card is `position: sticky; top: calc(84px + i*14px)`, and earlier cards scale to about 0.92 as the next arrives (one `gsap.to` per card with `scrub:true`). Good for 3–5 short items near the end.

## Hands-on (one per presentation)
- Put it in an **unpinned** `.sp-section`. Wrap the SVG in `.sp-dragbox` and add `S.dragHandle(box, {get, set, axis, bounds})`.
- Readouts next to the chart: "your value" vs. "best possible", plus a one-line hint that changes with closeness.
- Add a "Show answer" button that tweens to the best state, and a "Reset" button.
