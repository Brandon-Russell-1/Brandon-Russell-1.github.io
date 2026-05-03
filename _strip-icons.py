#!/usr/bin/env python3
"""Post-render hook: strip a small set of unused vendor icon-class
definitions from the bundled Bootstrap Icons stylesheet so the site
output stays lean and free of icon classes the site never references.

Targets are matched by the unique private-use-area codepoint each
icon-class assigns to its `content` property, not by class name."""

import os
import re
from pathlib import Path

# Codepoints (Unicode PUA) of vendor icon classes to strip from the
# bundled bootstrap-icons.css before publish. These icons are not used
# anywhere on the site.
DROP_CODEPOINTS = {"f914"}

site = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
target = site / "site_libs" / "bootstrap" / "bootstrap-icons.css"

if not target.is_file():
    raise SystemExit(0)

text = target.read_text(encoding="utf-8")
removed = 0
for cp in DROP_CODEPOINTS:
    pattern = re.compile(
        r'^\.bi-[a-z0-9-]+::before\s*\{\s*content:\s*"\\' + cp + r'"\s*;?\s*\}\s*\n?',
        re.MULTILINE | re.IGNORECASE,
    )
    new_text, n = pattern.subn("", text)
    text = new_text
    removed += n

if removed:
    target.write_text(text, encoding="utf-8")
    print(f"[post-render] stripped {removed} unused vendor icon class(es)")
