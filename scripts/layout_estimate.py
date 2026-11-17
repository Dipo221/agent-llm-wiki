"""[已停用] v2 的版面高度「估算」。v2.1 起 G4 改用 measure.py 實際渲染量測（估算誤差約 ±30px，會漏抓也會誤報）。保留作為 workflow 演進紀錄。"""
"""版面高度預估（把 G5 的溢出檢查往前移到 G4 用）。

依 slides/template.html 的 CSS 粗估每頁內容高度：中文字寬＝字級、英數約 0.55 字級，
換行後乘上行高，加上區塊間距。用 G5 實際量到的溢出值校準過（見 docs/workflow-design.md）。
"""
import math
import re

from slidelib import CITE_RE

AVAIL = 600          # 內容區可用高度（720 − 上邊距 52 − 頁尾約 68；頁尾只有 1 行出處時）
NAMES = {"wei2022-chain-of-thought": "Wei 2022 (CoT)", "yao2022-react": "Yao 2022 (ReAct)",
         "schick2023-toolformer": "Schick 2023 (Toolformer)", "shinn2023-reflexion": "Shinn 2023 (Reflexion)",
         "park2023-generative-agents": "Park 2023 (Generative Agents)", "wang2023-agent-survey": "Wang 2023 (Survey)"}


def avail(body):
    """頁尾會依出處數量換行：每多一行出處，內容區就少約 19px（v2.1 修正，G5 第 2 次發現漏抓）。"""
    refs = []
    for m in CITE_RE.finditer(body):
        k = (m.group(1), m.group(2).strip())
        if k not in refs:
            refs.append(k)
    if not refs:
        return AVAIL + 19
    width = sum(text_width(f"{i} {NAMES.get(s, s)}，{l}", 13) + 18 for i, (s, l) in enumerate(refs, 1))
    return AVAIL - (math.ceil(width / W_FULL) - 1) * 19
W_FULL = 1152        # 一般版面文字寬
W_SPLIT = 578        # split 版面左欄寬（52%）
GAP = 18


def text_width(s, size):
    s = CITE_RE.sub("¹", s)
    s = re.sub(r"\*\*|`", "", s)
    w = 0.0
    for ch in s:
        w += size if ord(ch) > 0x2E7F else size * 0.55
    return w


def lines(s, size, width):
    return max(1, math.ceil(text_width(s, size) / width))


FIG_TITLE = 170 + 40  # 封面版型：時間線圖高度＋文字與圖之間的間距


def estimate(body, layout="default"):
    width = W_SPLIT if layout == "split" else W_FULL
    gap = 26 if layout == "title" else GAP
    h, blocks = 0.0, 0
    in_code, code = False, 0
    rows = 0
    ls = body.strip().splitlines()
    i = 0
    while i < len(ls):
        s = ls[i].strip()
        i += 1
        if s.startswith("```"):
            if in_code:
                h += code * 28.5 + 32
                blocks += 1
                code = 0
            in_code = not in_code
            continue
        if in_code:
            code += lines(s, 19 * 0.6, width - 40)   # 等寬字：英數約 0.6 字級
            continue
        if not s:
            continue
        if s.startswith("# "):
            size = 68 if layout == "title" else 44
            h += lines(s[2:], size, width) * size * 1.2
        elif s.startswith("## "):
            h += 27
        elif s.startswith("- "):
            h += lines(s[2:], 24, width - 30) * 36 + 12
        elif s.startswith("|"):
            if re.fullmatch(r"\|[\s\-:|]+\|", s):
                continue
            cells = [c for c in s.strip("|").split("|")]
            colw = width / max(1, len(cells)) - 28
            h += max(lines(c, 21, colw) for c in cells) * 31.5 + 19
            rows += 1
            continue
        elif s.startswith("> "):
            h += lines(s[2:], 22, width - 45) * 34 + 28
        else:
            h += lines(s, 24, width) * 38.4
        blocks += 1
    return h + gap * max(0, blocks - 1) + (FIG_TITLE if layout == "title" else 0)
