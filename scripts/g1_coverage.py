#!/usr/bin/env python3
"""G1 覆蓋率關卡：sources.md 挑的 wiki 頁夠不夠、6 篇論文有沒有都涵蓋。"""
import re
import sys
from pathlib import Path
from slidelib import WIKI, PAPERS, parse, listval, report

run = Path(sys.argv[1])
text = (run / "sources.md").read_text()
pages = re.findall(r"\]\((?:\.\./)*(?:wiki/)?([\w\-/]+\.md)\)", text)
problems, covered = [], set()
for p in pages:
    f = WIKI / p
    if not f.exists():
        problems.append(f"sources.md 列的 {p} 不存在")
        continue
    covered |= set(listval(parse(f)[0].get("sources", "")))
if len(pages) < 3:
    report(run, "G1 覆蓋率", [f"相關頁只有 {len(pages)} 頁（< 3），依規則停下，不硬湊"])
    sys.exit(2)
for slug in PAPERS:
    if slug not in covered:
        problems.append(f"論文 {slug} 沒有任何被選的頁面涵蓋 → 退回 N1 補檢索")
ok = report(run, "G1 覆蓋率", problems,
            [f"選了 {len(pages)} 個 wiki 頁，涵蓋論文 {len(covered & set(PAPERS))}/{len(PAPERS)} 篇"])
sys.exit(0 if ok else 1)
