#!/usr/bin/env python3
"""G3 大綱自查：頁數、教學結構、每頁的卡、6 篇論文是否都出場。"""
import re
import sys
from pathlib import Path
from slidelib import PAPERS, CITE_RE, parse, report

ROLES = {"封面", "問題", "概念", "例子", "比較", "小結"}
run = Path(sys.argv[1])
text = (run / "outline.md").read_text()
slides = re.findall(r"^## (S\d\d) (.+?)\n(.*?)(?=^## S\d\d |\Z)", text, re.M | re.S)
cards = {c.stem: c for c in (run / "cards").glob("c*.md")}
problems, used_papers = [], set()
if not 10 <= len(slides) <= 15:
    problems.append(f"共 {len(slides)} 頁，規定 10–15 頁")
for k, (sid, title, body) in enumerate(slides):
    role = re.search(r"角色[:：]\s*(\S+)", body)
    role = role.group(1) if role else None
    if role not in ROLES:
        problems.append(f"{sid}：角色 {role!r} 不在 {sorted(ROLES)}")
    if k == 0 and role != "封面":
        problems.append(f"{sid}：第一頁要是封面")
    if k == len(slides) - 1 and role != "小結":
        problems.append(f"{sid}：最後一頁要是小結")
    if not re.search(r"目標[:：]\s*\S", body):
        problems.append(f"{sid}：沒寫這頁要讓讀者懂什麼（目標）")
    m = re.search(r"卡片[:：]\s*(.*)", body)
    ids = re.findall(r"c\d\d", m.group(1)) if m else []
    if role != "封面" and not ids:
        problems.append(f"{sid}：內容頁沒有指定卡片")
    for cid in ids:
        if cid not in cards:
            problems.append(f"{sid}：卡片 {cid} 不存在")
        else:
            used_papers |= {s for s, _ in CITE_RE.findall(parse(cards[cid])[1])}
for slug in PAPERS:
    if slug not in used_papers:
        problems.append(f"論文 {slug} 沒有在任何一頁出場")
ok = report(run, "G3 大綱自查", problems,
            [f"{len(slides)} 頁；出場論文 {len(used_papers & set(PAPERS))}/{len(PAPERS)} 篇"])
sys.exit(0 if ok else 1)
