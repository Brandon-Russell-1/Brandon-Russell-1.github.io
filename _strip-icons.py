#!/usr/bin/env python3
"""Post-render hook: tree-shake the bundled Bootstrap Icons stylesheet.

Quarto ships the full Bootstrap Icons CSS (~2,000 icon classes, ~100KB+).
This site uses only a handful of them in the navbar and footer. This
script scans the rendered HTML for `bi-<name>` class references, then
removes every `.bi-<name>::before` rule that isn't referenced anywhere.

The result is a much smaller stylesheet that contains only the icons
the site actually uses."""

import os
import re
from pathlib import Path

site = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
css_path = site / "site_libs" / "bootstrap" / "bootstrap-icons.css"

if not css_path.is_file():
    raise SystemExit(0)

# Collect every bi-* class name referenced anywhere in rendered HTML.
used = set()
class_pat = re.compile(r"\bbi-([a-z0-9-]+)\b")
for html in site.rglob("*.html"):
    try:
        for m in class_pat.finditer(html.read_text(encoding="utf-8")):
            used.add(m.group(1))
    except (UnicodeDecodeError, OSError):
        continue

# Strip every .bi-<name>::before rule whose name isn't in the used set.
css = css_path.read_text(encoding="utf-8")
rule_pat = re.compile(
    r'^\.bi-([a-z0-9-]+)::before\s*\{[^}]*\}\s*\n?',
    re.MULTILINE | re.IGNORECASE,
)

dropped = 0
def keep_or_drop(match):
    global dropped
    name = match.group(1).lower()
    if name in used:
        return match.group(0)
    dropped += 1
    return ""

new_css = rule_pat.sub(keep_or_drop, css)

if dropped:
    css_path.write_text(new_css, encoding="utf-8")
    print(f"[post-render] tree-shook bootstrap-icons.css: removed {dropped} unused icon rule(s)")
