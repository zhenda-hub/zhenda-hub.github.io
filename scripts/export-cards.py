#!/usr/bin/env python3
"""把文章里的 quotecard 台词渲染成小红书卡片图（1080×1440，3:4）。

用法：
    python scripts/export-cards.py                      # 默认 lol-cn-lines
    python scripts/export-cards.py --post games/lol-cn-lines
    python scripts/export-cards.py --post life/pc-rebuild --cover-only

做法：
  1. 解析 index.md 里的 {{< quotecard >}} 块（标题 / 中文 / 英文 / 判词）
  2. 生成一份 1080×1440 的卡片 HTML
  3. 用本机 Chrome 逐屏截图，输出 PNG 到 cards/<分类-slug>/（git 跟踪，public/ 被 ignore）

依赖：本机 Chrome、requests、websocket-client、python -m http.server（脚本自己起）
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import websocket

REPO = Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CARD_W, CARD_H = 1080, 1440

# ---------------- 解析 ----------------

QUOTE_RE = re.compile(
    r'\{\{<\s*quotecard\s+"([^"]+)"\s+"([^"]*)"\s+"([^"]*)"\s*>\}\}(.*?)\{\{<\s*/quotecard\s*>\}\}',
    re.S,
)


def clean_en(s: str) -> str:
    """弯撇号在衬线体里按全角排，卡片里一律换回直撇号。"""
    return s.replace("\u2019", "'").replace("\u02bc", "'").replace("\u2018", "'")


def parse_post(md_path: Path) -> tuple[dict, list[dict]]:
    text = md_path.read_text(encoding="utf-8")

    fm = {}
    m = re.match(r"\+\+\+(.*?)\+\+\+", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r"\s*(\w+)\s*=\s*(.+)", line)
            if kv:
                fm[kv.group(1)] = kv.group(2).strip().strip("'\"")

    cards = []
    for slug, alt, title, body in QUOTE_RE.findall(text):
        zh_lines, en_lines, note_lines = [], [], []
        for raw in body.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith(">"):
                content = line.lstrip(">").strip()
                if not content:
                    continue
                if content.startswith("*") and content.endswith("*"):
                    en_lines.append(clean_en(content.strip("*").strip()))
                else:
                    zh_lines.append(content)
            elif not zh_lines and not en_lines:
                continue
            else:
                note_lines.append(line)

        cards.append(
            {
                "slug": slug,
                "alt": alt,
                "title": title,
                "no": title.split("·")[0].strip() if "·" in title else "",
                "name": title.split("·")[1].strip() if title.count("·") >= 1 else alt,
                "role": title.split("·")[2].strip() if title.count("·") >= 2 else "",
                "zh": "\n".join(zh_lines),
                "en": "\n".join(en_lines),
                "note": " ".join(note_lines),
            }
        )
    return fm, cards


# ---------------- HTML ----------------

CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#dcdcdc; font-family:"Noto Serif SC","Source Han Serif SC","Songti SC","SimSun",serif; }
.card { width:1080px; height:1440px; background:#faf9f7; position:relative; overflow:hidden;
        color:#3f3830; display:flex; flex-direction:column; padding:96px 90px 84px; }
.card + .card { margin-top:40px; }
.top { display:flex; justify-content:space-between; align-items:baseline;
       font-family:Georgia,"Times New Roman",serif; font-size:31px; letter-spacing:.14em;
       color:#8f8474; margin-bottom:58px; }
.cover { justify-content:space-between; }
.cover__mid { margin-top:150px; }
.cover__kicker { font-size:32px; letter-spacing:.18em; color:#b07d18; margin-bottom:54px; }
.cover__title { font-size:96px; line-height:1.3; font-weight:700; }
.cover__title em { font-style:normal; color:#b07d18; }
.cover__rule { width:132px; height:3px; background:#b07d18; margin:58px 0 42px; }
.cover__sub { font-size:37px; line-height:1.8; color:#5b5248; }
.cover__foot { font-size:28px; letter-spacing:.12em; color:#8f8474;
               font-family:Georgia,serif; display:flex; justify-content:space-between; }
.head { display:flex; align-items:center; gap:40px; }
.head img { width:232px; height:232px; border-radius:128px; object-fit:cover;
            object-position:top center; filter:saturate(.92); }
.head__meta { display:flex; flex-direction:column; gap:16px; }
.head__no { font-family:Georgia,serif; font-size:88px; line-height:1; color:#d8cbb2; }
.head__name { font-size:46px; font-weight:700; letter-spacing:.04em; }
.head__title { font-size:32px; color:#7a7064; letter-spacing:.08em; }
.quote { flex:1; display:flex; flex-direction:column; justify-content:center; }
.quote__zh { font-size:68px; line-height:1.62; font-weight:600; white-space:pre-line; }
.quote__en { margin-top:48px; font-size:43px; line-height:1.62; color:#7a7064;
             font-style:italic; white-space:pre-line; }
.note { margin-top:auto; margin-bottom:96px; }
.note__rule { width:100%; height:1px; background:#e3dbcc; margin-bottom:38px; }
.note__text { font-size:38px; line-height:1.72; color:#5b5248; }
.note__text b { color:#b07d18; font-weight:600; }
.corner { position:absolute; right:90px; bottom:84px; font-family:Georgia,serif;
          font-size:24px; letter-spacing:.16em; color:#c0b49f; }
"""


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def bold_gold(s: str) -> str:
    """把 markdown 的 **xxx** 变成金色强调。"""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", esc(s))


def build_html(fm: dict, cards: list[dict], title: str, kicker: str, total: int) -> str:
    out = [
        '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>cards</title>',
        f"<style>{CSS}</style></head><body>",
    ]
    # 封面
    out.append(
        f"""<section class="card cover">
  <div class="top"><span>Starmap &amp; Dust</span><span>{esc(kicker)}</span></div>
  <div class="cover__mid">
    <div class="cover__kicker">{esc(kicker)}</div>
    <div class="cover__title">{title}</div>
    <div class="cover__rule"></div>
    <div class="cover__sub">{esc(fm.get('description', ''))}</div>
  </div>
  <div class="cover__foot"><span>中英对照</span><span>01 / {total:02d}</span></div>
</section>"""
    )
    for i, c in enumerate(cards, start=1):
        out.append(
            f"""<section class="card">
  <div class="top"><span>{esc(kicker)}</span><span></span></div>
  <div class="head">
    <img src="/cards-src/{c['slug']}.jpg" alt="{esc(c['alt'])}">
    <div class="head__meta">
      <div class="head__no">{esc(c['no'])}</div>
      <div class="head__name">{esc(c['name'])}</div>
      <div class="head__title">{esc(c['role'])}</div>
    </div>
  </div>
  <div class="quote">
    <div class="quote__zh">{esc(c['zh'])}</div>
    <div class="quote__en">{esc(c['en'])}</div>
  </div>
  <div class="note">
    <div class="note__rule"></div>
    <div class="note__text">{bold_gold(c['note'])}</div>
  </div>
  <div class="corner">{i + 1:02d} / {total:02d}</div>
</section>"""
        )
    out.append("</body></html>")
    return "\n".join(out)


# ---------------- 截图 ----------------

def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def shot(out_dir: Path, cdp_port: int, http_port: int) -> list[Path]:
    proc = subprocess.Popen(
        [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--remote-debugging-port={cdp_port}", "--remote-allow-origins=*",
            f"--user-data-dir={Path.home() / '.cache' / 'cards-chrome'}",
            "about:blank",
        ],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(40):
            try:
                targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{cdp_port}/json/list"))
                if targets:
                    break
            except Exception:
                time.sleep(0.5)
        ws = websocket.create_connection(
            [t for t in targets if t["type"] == "page"][0]["webSocketDebuggerUrl"],
            timeout=90, suppress_origin=True, max_size=120 * 1024 * 1024,
        )

        seq = [0]

        def cdp(method, params=None):
            seq[0] += 1
            ws.send(json.dumps({"id": seq[0], "method": method, "params": params or {}}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == seq[0]:
                    return msg

        def ev(expr):
            return cdp("Runtime.evaluate", {"expression": expr, "returnByValue": True})[
                "result"]["result"].get("value")

        cdp("Emulation.setDeviceMetricsOverride",
            {"width": 1200, "height": 1500, "deviceScaleFactor": 1, "mobile": False})
        cdp("Page.enable")
        cdp("Page.navigate", {"url": f"http://127.0.0.1:{http_port}/cards.html"})
        for _ in range(60):
            time.sleep(0.5)
            if ev("document.querySelectorAll('.card').length"):
                break
        time.sleep(3)  # 等字体/图片

        n = ev("document.querySelectorAll('.card').length")
        out_dir.mkdir(parents=True, exist_ok=True)
        files = []
        for i in range(n):
            y = ev(f"Math.round(document.querySelectorAll('.card')[{i}]"
                   f".getBoundingClientRect().top + window.scrollY)")
            r = cdp("Page.captureScreenshot", {
                "format": "png", "captureBeyondViewport": True,
                "clip": {"x": 0, "y": y, "width": CARD_W, "height": CARD_H, "scale": 1},
            })
            f = out_dir / f"{i + 1:02d}.png"
            f.write_bytes(base64.b64decode(r["result"]["data"]))
            files.append(f)
        ws.close()
        return files
    finally:
        proc.terminate()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--post", default="games/lol-cn-lines")
    ap.add_argument("--kicker", default="英雄联盟 · 经典台词")
    ap.add_argument("--cover-title", default="11 句被记住<br><em>十年</em>的话")
    args = ap.parse_args()

    bundle = REPO / "content" / "posts" / args.post
    md = bundle / "index.md"
    if not md.exists():
        sys.exit(f"找不到 {md}")

    fm, cards = parse_post(md)
    if not cards:
        sys.exit("没解析到 quotecard 块")

    # 图片先拷到 public/cards-src/，页面用相对路径引用
    src_dir = REPO / "public" / "cards-src"
    src_dir.mkdir(parents=True, exist_ok=True)
    for c in cards:
        found = next((bundle / "imgs-chars").glob(f"loading-{c['slug']}.*"), None) \
            or next((bundle / "imgs-chars").glob(f"{c['slug']}.*"), None)
        if found:
            shutil.copy(found, src_dir / f"{c['slug']}.jpg")

    total = len(cards) + 1
    html = build_html(fm, cards, args.cover_title, args.kicker, total)
    (REPO / "public").mkdir(exist_ok=True)
    (REPO / "public" / "cards.html").write_text(html, encoding="utf-8")

    # 起静态服务（根指向 public/）
    port = free_port()
    srv = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=str(REPO / "public"), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        time.sleep(1.5)
        out_dir = REPO / "cards" / args.post.replace("/", "-")
        files = shot(out_dir, free_port(), port)
    finally:
        srv.terminate()

    print(f"解析到 {len(cards)} 条台词，共输出 {len(files)} 张卡片")
    print(f"输出目录：{out_dir}")


if __name__ == "__main__":
    main()
