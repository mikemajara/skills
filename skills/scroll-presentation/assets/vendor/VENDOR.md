# Vendored libraries

| File | Library | Version | License |
|---|---|---|---|
| `gsap.min.js` | GSAP core | 3.15.0 | GSAP Standard "No Charge" License, https://gsap.com/standard-license |
| `ScrollTrigger.min.js` | GSAP ScrollTrigger plugin | 3.15.0 | same as above |

The files come unmodified from the npm package `gsap@3.15.0` (`node_modules/gsap/dist/`). If a release ever ships a trailing `//# sourceMappingURL` comment, remove it so browsers don't request a `.map` file. 3.15.0 has none, so these files are byte-identical to npm. The license header comment at the top of each file is kept on purpose. Don't strip it when bundling.

GSAP has been free for all uses, including commercial ones, since 3.13 (it is now a Webflow product). The standard license still has restrictions, for example on building a competing no-code animation tool. Read it before you redistribute GSAP in an unusual context.

## Pinned CDN fallback (online only)

You only need this when you are not bundling, for example during quick prototyping:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/ScrollTrigger.min.js"></script>
```

Published presentations should inline the vendored files with `scripts/sp.py build`. Then the page works offline and makes no third-party requests.

## Updating

```bash
npm pack gsap@<version> && tar -xzf gsap-<version>.tgz
cp package/dist/gsap.min.js package/dist/ScrollTrigger.min.js assets/vendor/
sed -i '/sourceMappingURL/d' assets/vendor/*.js
```

After an update, change the table above, run `scripts/test_presentation.mjs` on a presentation, and note the bump in the CHANGELOG.

## Lenis (optional, not bundled)

Smooth wheel scrolling is optional. If a presentation wants it, vendor `lenis@1.3.x` (`dist/lenis.min.js`, MIT) next to these files and enable it only for `(pointer: fine)` with motion allowed. See `references/snapping.md`.

Checksums (sha256):
    92bb9a96476f983d212a2bc4f54c889039c1696dd4461d40a736860938570fbb  gsap.min.js
    b0b14d67b55b0c43c756ac0b106cfcb09d0879945f6ead64451065b0672916a2  ScrollTrigger.min.js
