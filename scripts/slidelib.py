"""簡報流程各關卡共用的小工具。"""
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lint  # noqa: E402  重用 lint 的出處／數字規則

ROOT = lint.ROOT
WIKI = lint.WIKI
CITE_RE = re.compile(r"\[@([a-z0-9\-]+),\s*([^\]]+)\]")
PAPERS = sorted(p.stem for p in (ROOT / "raw" / "papers").glob("*.txt"))


def parse(path):
    """回傳 (frontmatter dict, body, body 起始行號)。"""
    return lint.parse_page(Path(path))


def listval(v):
    return [x.strip() for x in v.strip("[]").split(",") if x.strip()] if v else []


def numbers(text):
    return lint.numbers_in(text)


def blocks(body, start):
    return lint.blocks(body, start)


def has_number(num, text):
    core = re.sub(r"[%×xB]$", "", num)
    return re.search(r"(?<![\d.])" + re.escape(core) + r"(?![\d])", text) is not None


def norm(s):
    return re.sub(r"\s+", "", s)


def report(run, gate, problems, notes=()):
    """把一次關卡結果附加到 report.md，回傳是否通過。"""
    rp = Path(run) / "report.md"
    old = rp.read_text() if rp.exists() else "# 檢查報告\n\n> 每一關的結果由腳本自動附加；AI 審查與人工確認由執行者補記。\n"
    n = len(re.findall(rf"^## {re.escape(gate)} — 第 ", old, re.M)) + 1
    ok = not problems
    lines = [f"\n## {gate} — 第 {n} 次（{datetime.now():%Y-%m-%d %H:%M}）", "",
             f"結果：{'✅ 通過' if ok else f'❌ {len(problems)} 個問題'}", ""]
    lines += [f"- {n_}" for n_ in notes]
    lines += [f"- ❌ {p}" for p in problems]
    rp.write_text(old + "\n".join(lines) + "\n")
    print(f"{gate} 第 {n} 次：{'通過' if ok else f'{len(problems)} 個問題'}")
    for p in problems:
        print("  ❌", p)
    for n_ in notes:
        print("  ·", n_)
    return ok
