#!/usr/bin/env python3
"""G5 渲染檢查（最終把關）：3 種風格 × 每一頁量測溢出、圖有沒有顯示，並存截圖給人看。
用法：python3 scripts/g5_render.py runs/ai-agents-intro [--no-shots]"""
import sys
from pathlib import Path
from slidelib import ROOT, report
from measure import THEMES, SHOT, chrome, measure, problems_of

run = Path(sys.argv[1])
deck = (ROOT / "slides" / "index.html").resolve()
shots = run / "screenshots"
shots.mkdir(exist_ok=True)
problems, notes, n_slides = [], [], 0
for t in THEMES:
    res = measure(deck, t)
    if res is None:
        problems.append(f"[{t}] 檢查模式沒有回傳結果")
        continue
    n_slides = len(res["slides"])
    notes.append(f"[{t}] 字型載入狀態：{res['fonts']}，共 {n_slides} 頁")
    problems += problems_of(res, t)
if "--no-shots" not in sys.argv and n_slides:
    for t in THEMES:
        for k in range(1, n_slides + 1):
            out = (shots / f"{t}-s{k:02d}.png").resolve()
            chrome([SHOT, "--virtual-time-budget=20000", f"--screenshot={out}"],
                   f"file://{deck}?check=1&noui=1&theme={t}&slide={k}")
    notes.append(f"截圖：{run.name}/screenshots/（{len(THEMES)} 種風格 × {n_slides} 頁）")
ok = report(run, "G5 渲染檢查", problems, notes)
sys.exit(0 if ok else 1)
