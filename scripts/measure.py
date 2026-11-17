"""用 Chrome headless 量測簡報每頁有沒有溢出（G4 v2.1 與 G5 共用）。"""
import json
import re
import subprocess
import tempfile

CHROME = "google-chrome"
THEMES = ["tech", "textbook", "sketch"]
BASE = ["--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1"]
# headless=new 的視窗含約 88px 瀏覽器框；量測用 1280×720（舞台縮放不影響版面量測），截圖用 1280×808
MEASURE, SHOT = "--window-size=1280,720", "--window-size=1280,808"


def chrome(args, url):
    with tempfile.TemporaryDirectory() as prof:
        return subprocess.run([CHROME, *BASE, f"--user-data-dir={prof}", *args, url],
                              capture_output=True, text=True, timeout=120)


def measure(html_path, theme):
    r = chrome([MEASURE, "--virtual-time-budget=40000", "--dump-dom"],
               f"file://{html_path}?check=1&noui=1&theme={theme}")
    m = re.search(r'<pre id="check-result"[^>]*>(.*?)</pre>', r.stdout, re.S)
    if not m or not m.group(1).strip():
        return None
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&"))


def problems_of(res, theme, only=None):
    out = []
    for s in res["slides"]:
        if only and s["slide"] not in only:
            continue
        if s["overflowY"] > 2:
            out.append(f"[{theme}] {s['slide']} 內容超出版面 {s['overflowY']}px（字太多 → 退回 N4 縮短這頁）")
        if s["overflowX"] > 2:
            out.append(f"[{theme}] {s['slide']} 內容橫向超出 {s['overflowX']}px")
        if s["footerOut"] > 2:
            out.append(f"[{theme}] {s['slide']} 頁尾出處被擠出版面 {s['footerOut']}px")
        if s["emptyFigures"]:
            out.append(f"[{theme}] {s['slide']} 圖沒有顯示")
    return out
