#!/usr/bin/env python3
"""N5 渲染：把通過 G4 的逐頁稿「原封不動」轉成 HTML 簡報。

這支程式只做格式轉換（Markdown 子集 → HTML），不改任何文字，
所以「渲染時不能改字」由程式保證，而不是靠 AI 自律。
用法：python3 scripts/render_deck.py runs/ai-agents-intro
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from slidelib import ROOT, CITE_RE, parse, listval  # noqa: E402

REPO = "https://github.com/Dipo221/agent-llm-wiki/blob/main/"
NAMES = {"wei2022-chain-of-thought": "Wei 2022 (CoT)", "yao2022-react": "Yao 2022 (ReAct)",
         "schick2023-toolformer": "Schick 2023 (Toolformer)", "shinn2023-reflexion": "Shinn 2023 (Reflexion)",
         "park2023-generative-agents": "Park 2023 (Generative Agents)",
         "wang2023-agent-survey": "Wang 2023 (Survey)"}


def inline(text, cites):
    """行內格式：粗體、程式碼、出處 → 上標編號。文字本身不變。"""
    out, pos = [], 0
    for m in CITE_RE.finditer(text):
        out.append(fmt(text[pos:m.start()]))
        key = (m.group(1), m.group(2).strip())
        if key not in cites:
            cites.append(key)
        n = cites.index(key) + 1
        out.append(f'<sup class="cite" title="{html.escape(NAMES.get(key[0], key[0]))} {html.escape(key[1])}">{n}</sup>')
        pos = m.end()
    out.append(fmt(text[pos:]))
    html_ = "".join(out)
    # 連續的出處（中間只有空白或「、」）合併成一個上標「1,2」；中間有文字就不合併
    pat = re.compile(r'<sup class="cite" title="([^"]*)">([\d,]+)</sup>\s*、?\s*<sup class="cite" title="([^"]*)">([\d,]+)</sup>')
    while pat.search(html_):
        html_ = pat.sub(lambda m: f'<sup class="cite" title="{m.group(1)}；{m.group(3)}">{m.group(2)},{m.group(4)}</sup>', html_)
    return html_


def fmt(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def body_html(body, cites):
    lines, out, i = body.strip().splitlines(), [], 0
    while i < len(lines):
        s = lines[i].rstrip()
        if not s.strip():
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre>" + html.escape("\n".join(lines[i + 1:j])) + "</pre>")
            i = j + 1
            continue
        if s.startswith("# "):
            out.append(f"<h1>{inline(s[2:], cites)}</h1>")
        elif s.startswith("## "):
            out.append(f'<p class="kicker">{inline(s[3:], cites)}</p>')
        elif s.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(f"<li>{inline(lines[i][2:], cites)}</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.fullmatch(r"\|[\s\-:|]+\|", lines[i].strip()):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head = "".join(f"<th>{inline(c, cites)}</th>" for c in rows[0])
            rest = "".join("<tr>" + "".join(f"<td>{inline(c, cites)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rest}</tbody></table>")
            continue
        elif s.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith("> "):
                buf.append(inline(lines[i][2:], cites))
                i += 1
            out.append('<div class="callout">' + "<br>".join(buf) + "</div>")
            continue
        else:
            out.append(f"<p>{inline(s, cites)}</p>")
        i += 1
    return "\n".join(out)


def main():
    run = Path(sys.argv[1])
    slides = []
    for d in sorted((run / "drafts").glob("s*.md")):
        meta, body, _ = parse(d)
        cites = []
        content = body_html(body, cites)
        fig = meta.get("figure")
        figure = ""
        if fig:
            svg = (ROOT / "slides" / "figures" / f"{fig}.svg").read_text()
            figure = f'<figure class="fig">{svg}</figure>'
        wikis = []
        for c in listval(meta.get("cards", "")):
            w = parse(run / "cards" / f"{c}.md")[0].get("wiki")
            if w and w not in wikis:
                wikis.append(w)
        refs = "".join(f'<li><span>{n}</span>{html.escape(NAMES.get(s, s))}，{html.escape(l)}</li>'
                       for n, (s, l) in enumerate(cites, 1))
        wl = " · ".join(f'<a href="{REPO}wiki/{w}" target="_blank">{w}</a>' for w in wikis)
        foot = (f'<footer class="src"><ol>{refs}</ol>' if refs else '<footer class="src">') + \
               (f'<div class="wikis">本頁依據的 wiki 頁：{wl}</div>' if wl else "") + "</footer>"
        layout = meta.get("layout", "default")
        slides.append(f'<section class="slide {layout}" data-id="{meta.get("slide")}">'
                      f'<div class="content"><div class="text">{content}</div>{figure}</div>{foot}</section>')
    tpl = (ROOT / "slides" / "template.html").read_text()
    out = tpl.replace("<!--SLIDES-->", "\n".join(slides))
    dest = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "slides" / "index.html"
    dest.write_text(out)
    print(f"渲染：{len(slides)} 頁 → {dest}")


if __name__ == "__main__":
    main()
