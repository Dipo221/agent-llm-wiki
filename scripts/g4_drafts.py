#!/usr/bin/env python3
"""G4 忠實度（腳本部分）：逐頁稿只能用大綱指定的卡，數字與出處都要在卡上。
AI 審查另外由新的 subagent 執行，結果存在 reviews/。
用法：g4_drafts.py RUN [S03 S07 ...]   # 不給頁碼＝全部檢查"""
import re
import sys
from pathlib import Path
from slidelib import ROOT, CITE_RE, parse, listval, numbers, blocks, has_number, norm, report

run = Path(sys.argv[1])
only = set(sys.argv[2:])
outline = (run / "outline.md").read_text()
plan = {sid: re.findall(r"c\d\d", (re.search(r"卡片[:：]\s*(.*)", body) or [None, ""])[1])
        for sid, body in re.findall(r"^## (S\d\d) .+?\n(.*?)(?=^## S\d\d |\Z)", outline, re.M | re.S)}
problems, checked = [], 0
for d in sorted((run / "drafts").glob("s*.md")):
    meta, body, start = parse(d)
    sid = meta.get("slide", "")
    if only and sid not in only:
        continue
    checked += 1
    used = listval(meta.get("cards", ""))
    if sid not in plan:
        problems.append(f"{d.name}：slide {sid} 不在大綱裡")
        continue
    extra = set(used) - set(plan[sid])
    if extra:
        problems.append(f"{d.name}：用了大綱沒指定的卡 {sorted(extra)}")
    cardtext = "\n".join(parse(run / "cards" / f"{c}.md")[1] for c in used if (run / "cards" / f"{c}.md").exists())
    fig = meta.get("figure")
    figtext = ""
    if fig:
        f = ROOT / "slides" / "figures" / f"{fig}.svg"
        if not f.exists():
            problems.append(f"{d.name}：圖 {fig}.svg 不存在")
        else:
            figtext = re.sub(r"<[^>]+>", " ", f.read_text())
    if "💭" in body:
        problems.append(f"{d.name}：用了 💭 個人筆記")
    for ln, blk in blocks(body, start):
        cites = CITE_RE.findall(blk)
        for slug, loc in cites:
            if norm(f"[@{slug},{loc}]") not in norm(cardtext):
                problems.append(f"{d.name}:{ln} 出處 [@{slug}, {loc}] 不在這頁的卡片上")
        nums = numbers(blk)
        if nums and not cites and not blk.startswith(">"):
            problems.append(f"{d.name}:{ln} 有數字 {nums[:3]} 但沒有出處")
        for n in nums:
            if not has_number(n, cardtext):
                problems.append(f"{d.name}:{ln} 數字 {n} 不在這頁的卡片上")
    for n in numbers(figtext):
        if not has_number(n, cardtext):
            problems.append(f"{d.name}：圖 {fig}.svg 裡的數字 {n} 不在這頁的卡片上")
ok = report(run, "G4 忠實度（腳本）", problems,
            [f"檢查 {checked} 頁" + (f"（只檢查 {' '.join(sorted(only))}）" if only else "")])
sys.exit(0 if ok else 1)
