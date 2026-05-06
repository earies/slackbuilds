#!/usr/bin/env python3
"""Apply Signal Desktop font overrides + zoom-step patch.

Usage:
  apply-font-overrides.py patch-zoom    <extracted-dir> <multiplier>
  apply-font-overrides.py apply-profile <extracted-dir> <profile.css>
"""
import sys
from pathlib import Path

CSS_BEGIN = "/* === CUSTOM SIGNAL FONT OVERRIDE === */"
CSS_END   = "/* === END CUSTOM SIGNAL FONT OVERRIDE === */"


def patch_zoom(extracted: Path, multiplier: str) -> None:
    js_path = extracted / "bundles" / "main.js"
    js = js_path.read_text(encoding="utf-8")

    old_in  = "async zoomIn(){let e=await this.getZoomLevel();await this.setZoomLevel(e+1)}"
    new_in  = (f"async zoomIn(){{let e=await this.getZoomFactor();"
               f"await this.setZoomFactor(Math.min(e*{multiplier},5))}}")
    old_out = "async zoomOut(){let e=await this.getZoomLevel();await this.setZoomLevel(e-1)}"
    new_out = (f"async zoomOut(){{let e=await this.getZoomFactor();"
               f"await this.setZoomFactor(Math.max(e/{multiplier},.25))}}")

    if js.count(old_in) != 1 or js.count(old_out) != 1:
        sys.exit("FATAL: zoomIn/zoomOut pattern not unique. Signal version drift.")

    js_path.write_text(js.replace(old_in, new_in).replace(old_out, new_out), encoding="utf-8")
    print(f"main.js: zoom step set to *{multiplier} / *(1/{multiplier})")


def apply_profile(extracted: Path, profile: Path) -> None:
    css_path = extracted / "stylesheets" / "manifest.css"
    css = css_path.read_text(encoding="utf-8")

    block = f"\n{CSS_BEGIN}\n{profile.read_text(encoding='utf-8').strip()}\n{CSS_END}\n"

    if CSS_BEGIN in css:
        i = css.index(CSS_BEGIN)
        j = css.index(CSS_END) + len(CSS_END)
        css = css[:i] + css[j:]
    css = css.rstrip() + block

    css_path.write_text(css, encoding="utf-8")
    print(f"manifest.css: applied profile {profile.stem}")


def main() -> None:
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    cmd, *rest = sys.argv[1:]
    if cmd == "patch-zoom":
        patch_zoom(Path(rest[0]), rest[1])
    elif cmd == "apply-profile":
        apply_profile(Path(rest[0]), Path(rest[1]))
    else:
        sys.exit(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
