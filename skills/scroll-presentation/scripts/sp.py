#!/usr/bin/env python3
"""scroll-presentation helper (stdlib only).

  sp.py new   <dir> [--title "My story"]   scaffold <dir>/index.src.html + <dir>/kit/ (css, js, vendored GSAP)
  sp.py build <src.html> [-o out.html]     inline every local <link rel=stylesheet> and <script src> into ONE file
                                           and fail if any external (http/https//) reference remains.
"""
import argparse, pathlib, re, shutil, sys

SKILL = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SKILL / "assets"
EXTERNAL = re.compile(r"""(?:src|href)\s*=\s*["'](?:https?:)?//|url\(\s*["']?(?:https?:)?//|@import\s+["']?(?:url\()?["']?(?:https?:)?//""", re.I)


def cmd_new(a):
    d = pathlib.Path(a.dir)
    src = d / "index.src.html"
    if src.exists() and not a.force:
        sys.exit(f"{src} exists (use --force to overwrite)")
    (d / "kit" / "vendor").mkdir(parents=True, exist_ok=True)
    for f in ["kit.css", "kit.js"]:
        shutil.copy(ASSETS / f, d / "kit" / f)
    for f in (ASSETS / "vendor").iterdir():
        shutil.copy(f, d / "kit" / "vendor" / f.name)
    html = (ASSETS / "template.html").read_text(encoding="utf-8")
    if a.title:
        html = html.replace("<title>TITLE</title>", f"<title>{a.title}</title>")
    src.write_text(html, encoding="utf-8")
    print(f"scaffolded {src}\nedit it, then: {pathlib.Path(__file__).name} build {src} -o {d / 'index.html'}")


def _read_local(base, ref):
    if re.match(r"^(?:[a-z]+:)?//", ref, re.I) or ref.startswith("data:"):
        sys.exit(f"external reference not allowed in a bundled presentation: {ref}")
    p = (base / ref.split("?")[0].split("#")[0]).resolve()
    if not p.is_file():
        sys.exit(f"missing local file: {ref} (looked at {p})")
    return p.read_text(encoding="utf-8")


def cmd_build(a):
    src = pathlib.Path(a.src).resolve()
    base = src.parent
    html = src.read_text(encoding="utf-8")
    out = pathlib.Path(a.out) if a.out else base / "index.html"
    if out.resolve() == src:
        sys.exit("output would overwrite the source; pass -o")

    def css(m):
        body = _read_local(base, m.group("href"))
        return "<style>\n" + re.sub(r"/\*# sourceMappingURL=.*?\*/", "", body) + "\n</style>"

    def js(m):
        body = _read_local(base, m.group("src"))
        body = re.sub(r"^//# sourceMappingURL=.*$", "", body, flags=re.M)
        body = re.sub(r"</(script)", r"<\\/\1", body, flags=re.I)  # never close the inline tag early
        return "<script>\n" + body + "\n</script>"

    html = re.sub(r"""<link\b[^>]*\brel=["']stylesheet["'][^>]*\bhref=["'](?P<href>[^"']+)["'][^>]*>""", css, html, flags=re.I)
    html = re.sub(r"""<script\b[^>]*\bsrc=["'](?P<src>[^"']+)["'][^>]*>\s*</script>""", js, html, flags=re.I)
    leftovers = EXTERNAL.findall(html)
    if leftovers:
        sys.exit(f"external references remain: {leftovers[:5]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"built {out} ({len(html.encode()) // 1024} KB, self-contained)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("dir"); n.add_argument("--title"); n.add_argument("--force", action="store_true"); n.set_defaults(f=cmd_new)
    b = sub.add_parser("build"); b.add_argument("src"); b.add_argument("-o", "--out"); b.set_defaults(f=cmd_build)
    a = ap.parse_args(); a.f(a)


if __name__ == "__main__":
    main()
