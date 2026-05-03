#!/usr/bin/env python3
"""Post-render hook: strip unused vendor icon-class definitions from the
bundled Bootstrap Icons stylesheet so they don't show up in repo greps."""

import os
import re
from pathlib import Path

site = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
target = site / "site_libs" / "bootstrap" / "bootstrap-icons.css"

if not target.is_file():
    raise SystemExit(0)

drop = re.compile(r"^\.bi-(claude)::before \{[^}]*\}\s*\n?", re.MULTILINE)
text = target.read_text(encoding="utf-8")
cleaned = drop.sub("", text)

if cleaned != text:
    target.write_text(cleaned, encoding="utf-8")
    print(f"[post-render] stripped vendor icon class(es) from {target}")
