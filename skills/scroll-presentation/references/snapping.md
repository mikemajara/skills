# Snapping and anchoring steps

**Goal:** when the reader stops scrolling, the scene settles on a *finished* frame. That can be a result shown, a chart completed or a caption fully in.

## How the kit does it
Each step has an animated part (`dur`) followed by a `hold`. The kit builds one GSAP timeline per scene, adds a label at every step **end**, and passes ScrollTrigger a custom `snap.snapTo` function:

| where scrolling stopped | snaps to |
|---|---|
| inside a step's animation, scrolling **forward** | that step's end (the reader "eases on") |
| inside a step's animation, scrolling **backward** | the previous step's end |
| inside a hold (frame already complete) | stays on that end state |
| in the last hold, past halfway | the scene end (unpins cleanly) |

Settings: `duration {min:.2, max:.7}`, `delay: .08`, `ease: power2.inOut`, `inertia: false`.

- `inertia: false` matters. With velocity projection (the default), a quick flick or a programmatic jump projects far ahead and skips whole steps.
- An epsilon of about 0.006 absorbs pixel rounding, so a reader parked exactly on an end state isn't sent back a step.
- Snapping is not "scroll-jacking". It only acts after scrolling stops, it moves less than one step, and the reader can always keep scrolling.

## Tuning
- **Hold length**: `0.3–0.4` by default. Make it longer (`0.6`) after a punchline number so the reader can take it in. Use `0` between two steps that belong together.
- **Scroll length**: `vhPerUnit` about 0.5–0.6. If testers overshoot steps on phones, raise the hold rather than `vhPerUnit`.
- **Scrub**: 0.5–0.8 s feels smooth. Above 1 s the scene lags the finger.
- Disable snapping (`snap:false`) for a scene that is one continuous sweep with no meaningful intermediate frames.

## If you write your own timeline instead
```js
var tl = gsap.timeline({scrollTrigger:{trigger:el, start:'top top', end:'+=200%', pin:true, scrub:.6,
  snap:{snapTo:'labels', duration:{min:.2,max:.7}, delay:.08, ease:'power2.inOut', inertia:false}}});
tl.to(a, {...}).addLabel('step1').to(b, {...}).addLabel('step2');
```
`snapTo:'labels'` with `directional:true` (the default) is close to the kit's behavior. It does not treat holds specially.

## Optional smooth wheel (Lenis)
Only for `(pointer: fine)` and when motion is allowed. Never on touch, where native momentum is better.
```js
if (!ScrollStory.reducedMotion && matchMedia('(pointer: fine)').matches) {
  const lenis = new Lenis({lerp:.1, smoothWheel:true});
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
}
```
Vendor `lenis.min.js` (MIT) and add `lenis.css` (`html.lenis{height:auto}`). Test that snapping still lands on labels with the mouse wheel.
