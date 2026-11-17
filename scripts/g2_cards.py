#!/usr/bin/env python3
"""G2 卡片檢查：每張卡只來自一個 wiki 頁，句子、出處、數字都要能在那一頁找到。"""
import sys
from pathlib import Path
from slidelib import WIKI, CITE_RE, parse, numbers, has_number, norm, report

run = Path(sys.argv[1])
problems, n_claims = [], 0
cards = sorted((run / "cards").glob("c*.md"))
for c in cards:
    meta, body, start = parse(c)
    name = c.name
    src = meta.get("wiki", "")
    page = WIKI / src
    if not src or not page.exists():
        problems.append(f"{name}：wiki 欄位 {src!r} 不是存在的 wiki 頁")
        continue
    ptext = page.read_text()
    psrc = parse(page)[0].get("sources", "")
    if "💭" in body:
        problems.append(f"{name}：引用了 💭 個人筆記（簡報不可用）")
    for i, line in enumerate(body.splitlines(), start):
        s = line.strip()
        if not s.startswith("- "):
            continue
        n_claims += 1
        cites = CITE_RE.findall(s)
        if not cites:
            problems.append(f"{name}:{i} 這句沒有 [@出處]")
        for slug, loc in cites:
            if slug not in psrc:
                problems.append(f"{name}:{i} 引用 {slug}，但 {src} 的 sources 沒有這篇")
            elif norm(f"[@{slug},{loc}]") not in norm(ptext):
                problems.append(f"{name}:{i} 出處 [@{slug}, {loc}] 在 {src} 找不到同樣的標記")
        for num in numbers(s):
            if not has_number(num, ptext):
                problems.append(f"{name}:{i} 數字 {num} 在 {src} 找不到")
ok = report(run, "G2 卡片檢查", problems, [f"{len(cards)} 張卡、{n_claims} 句"])
sys.exit(0 if ok else 1)
