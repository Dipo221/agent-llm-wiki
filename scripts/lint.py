#!/usr/bin/env python3
"""Wiki 健檢腳本（規則見 AGENTS.md 第 9 節 Lint）。

用法：python3 scripts/lint.py [--quiet]
全部通過 exit 0；有問題 exit 1，並列出每個問題的檔案與行號。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
RAW = ROOT / "raw" / "papers"
REQUIRED = ["type", "title", "sources", "updated"]
TYPES = {"paper", "concept", "comparison", "benchmark"}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(#[^)]*)?\)")
CITE_RE = re.compile(r"\[@([a-z0-9\-]+)(?:,[^\]]*)?\]")
# 要求出處的數字：百分比、小數、兩位以上整數（排除年份 19xx/20xx 與 arXiv 編號）
NUM_RE = re.compile(r"(?<![\w.\-/])(\d+(?:\.\d+)?)(%|×|x\b|B\b)?")
CONVERTED = "由原文數字換算"


def load_txt(slug, cache={}):
    if slug not in cache:
        p = RAW / f"{slug}.txt"
        cache[slug] = re.sub(r"\s+", " ", p.read_text(errors="ignore")) if p.exists() else None
    return cache[slug]


def parse_page(path):
    text = path.read_text()
    meta, body, body_start = {}, text, 1
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip()
            body = text[end + 4:]
            body_start = text[:end + 4].count("\n") + 1
    return meta, body, body_start


def blocks(body, start):
    """把內文切成要各自標出處的單位：段落、列表項、表格列、引用區塊。"""
    out, cur, cur_line, in_code = [], [], None, False
    for i, line in enumerate(body.splitlines(), start):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        standalone = s.startswith(("- ", "* ", "|", "> ")) or re.match(r"\d+\. ", s)
        if not s or s.startswith("#") or standalone:
            if cur:
                out.append((cur_line, " ".join(cur)))
                cur = []
            if standalone and not re.fullmatch(r"\|[\s\-:|]+\|", s):
                out.append((i, s))
            continue
        if not cur:
            cur_line = i
        cur.append(s)
    if cur:
        out.append((cur_line, " ".join(cur)))
    return out


def numbers_in(text):
    clean = CITE_RE.sub("", text)
    clean = LINK_RE.sub("", clean)
    clean = re.sub(r"`[^`]*`", "", clean)
    clean = re.sub(r"(§|Table |Fig\. |Figure |Appendix )[\dA-Z][\d.–\-§]*", "", clean)  # 章節／表號不是數字主張
    clean = re.sub(r"\$[^$]*\$", "", clean)          # LaTeX 不算數字主張
    clean = re.sub(r"[A-Za-z]+[\-]?\d+[\w\-]*", "", clean)  # GPT-3、PaLM-540B 之類的名稱
    nums = []
    for m in NUM_RE.finditer(clean):
        n, unit = m.group(1), m.group(2)
        if re.fullmatch(r"(19|20)\d\d", n) and not unit:
            continue
        if "." not in n and len(n) < 2 and not unit:
            continue
        nums.append(n + (unit or ""))
    return nums


def found_in_sources(num, slugs):
    core = re.sub(r"[%×xB]$", "", num)
    pat = re.compile(r"(?<![\d.])" + re.escape(core) + r"(?![\d])")
    for slug in slugs:
        txt = load_txt(slug)
        if txt and pat.search(txt):
            return True
    return False


def main():
    problems = []
    pages = sorted(p for p in WIKI.rglob("*.md") if p.name not in ("index.md", "log.md"))
    index_text = (WIKI / "index.md").read_text()
    log_text = (WIKI / "log.md").read_text()
    inbound = {p: 0 for p in pages}
    index_links = {(WIKI / m.group(1)).resolve() for m in LINK_RE.finditer(index_text)}

    # index.md / log.md 本身的連結也要存在
    for special in (WIKI / "index.md", WIKI / "log.md"):
        for m in LINK_RE.finditer(special.read_text()):
            if not (special.parent / m.group(1)).resolve().exists():
                problems.append(("連結", special, 0, f"連到不存在的檔案 {m.group(1)}"))

    n_blocks = n_nums = 0
    for page in pages:
        meta, body, start = parse_page(page)
        rel = page.relative_to(ROOT)
        # 1. 開頭欄位
        for k in REQUIRED:
            if not meta.get(k):
                problems.append(("欄位", rel, 1, f"缺少 {k}"))
        if meta.get("type") and meta["type"] not in TYPES:
            problems.append(("欄位", rel, 1, f"type 不合法：{meta['type']}"))
        srcs = re.findall(r"[a-z0-9\-]+", meta.get("sources", ""))
        for s in srcs:
            if load_txt(s) is None:
                problems.append(("出處", rel, 1, f"sources 裡的 {s} 在 raw/papers/ 找不到"))
        # 2. 連結
        for m in LINK_RE.finditer(body):
            target = (page.parent / m.group(1)).resolve()
            if not target.exists():
                problems.append(("連結", rel, 0, f"連到不存在的檔案 {m.group(1)}"))
            elif target in inbound and target != page.resolve():
                inbound[target] += 1
        # 3. 出處與數字
        for line_no, blk in blocks(body, start):
            n_blocks += 1
            if blk.startswith("> 💭"):
                continue
            cites = CITE_RE.findall(blk)
            for c in cites:
                if load_txt(c) is None:
                    problems.append(("出處", rel, line_no, f"引用的 {c} 在 raw/papers/ 找不到"))
            nums = numbers_in(blk)
            if not nums:
                continue
            n_nums += len(nums)
            if not cites:
                problems.append(("出處", rel, line_no, f"有數字 {nums[:4]} 但沒有 [@slug, ...] 出處"))
                continue
            if CONVERTED in blk:
                continue
            for n in nums:
                if not found_in_sources(n, cites):
                    problems.append(("數字", rel, line_no, f"{n} 在 {cites} 的原文找不到"))
        # 4. 矛盾區塊要有 log
        if "⚠ 說法不一致" in body and page.stem not in log_text:
            problems.append(("矛盾", rel, 0, "有 ⚠ 說法不一致區塊，但 log.md 沒有提到這頁"))

    # 5. 孤兒頁
    for page in pages:
        rel = page.relative_to(ROOT)
        if page.resolve() not in index_links:
            problems.append(("孤兒", rel, 0, "沒有列在 index.md"))
        if inbound[page] == 0:
            problems.append(("孤兒", rel, 0, "沒有被任何其他 wiki 頁面連到"))

    print(f"Wiki lint：{len(pages)} 頁、{n_blocks} 個段落、{n_nums} 個數字")
    cats = ["欄位", "連結", "孤兒", "出處", "數字", "矛盾"]
    for c in cats:
        items = [p for p in problems if p[0] == c]
        print(f"  {'✅' if not items else '❌'} {c}：{len(items)} 個問題")
        if "--quiet" not in sys.argv:
            for _, f, ln, msg in items:
                print(f"      {f}:{ln}  {msg}" if ln else f"      {f}  {msg}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
