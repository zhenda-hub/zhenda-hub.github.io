#!/usr/bin/env python3
"""按文章标题生成字标封面（1600x900 PNG）。

用法：
    python scripts/gen-covers.py --limit 3              # 只生成 3 张（抽样看效果）
    python scripts/gen-covers.py --only ai/prompts      # 只生成指定文章
    python scripts/gen-covers.py --all --force          # 全部生成，已存在的覆盖
    python scripts/gen-covers.py --all --dry-run        # 只列出将要生成的文件

输出：<文章 bundle>/featured.webp
      content/posts/ai/prompts.md -> content/posts/ai/prompts/featured.webp

设计：深色底 + 左上分类标签 + 衬线大标题 + 金色细线 + 底部站名，
      与站点（星图与尘埃）的深色中式排版保持一致。
"""
from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"
COVER_NAME = "featured"  # bundle 内封面文件名（blowfish 自动识别 feature*）

SITE_NAME = "星图与尘埃"
W, H = 1600, 900

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
]

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\NotoSerifSC-VF.ttf",
    r"C:\Windows\Fonts\NotoSansSC-VF.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    exe = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")
    if exe:
        return exe
    sys.exit("找不到 Chrome/Edge，无法渲染封面")


def find_font() -> str | None:
    for f in FONT_CANDIDATES:
        if Path(f).exists():
            return Path(f).as_uri()
    return None


def read_frontmatter(path: Path) -> dict:
    """极简 TOML frontmatter 解析，只取封面需要的几个字段。"""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("+++"):
        return {}
    end = text.find("\n+++", 3)
    fm = text[3:end] if end != -1 else ""
    out: dict = {}
    for key in ("title", "subtitle", "description", "date", "featureimage"):
        # 值可能带引号，也可能是不带引号的日期/裸值
        pat = r'''^\s*''' + re.escape(key) + r'''\s*=\s*(?:(["'])(.*?)\1|([^\s#]+))'''
        m = re.search(pat, fm, re.M | re.S)
        if m:
            out[key] = (m.group(2) if m.group(1) else m.group(3) or "").strip()
    for key in ("series", "tags", "categories"):
        m = re.search(rf"^\s*{key}\s*=\s*\[(.*?)\]", fm, re.M | re.S)
        if m:
            out[key] = re.findall(r"['\"](.*?)['\"]", m.group(1))
    return out


def title_size(title: str) -> int:
    n = len(title)
    if n <= 8:
        return 118
    if n <= 12:
        return 104
    if n <= 18:
        return 88
    if n <= 26:
        return 72
    if n <= 36:
        return 60
    return 50


def build_html(title: str, label: str, date: str, font_uri: str | None) -> str:
    face = (
        f"@font-face{{font-family:'CoverSerif';src:url('{font_uri}');}}"
        if font_uri
        else ""
    )
    esc_title = html.escape(title)
    esc_label = html.escape(label)
    esc_date = html.escape(date)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{face}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{background:#12100d;color:#efe7da;
  font-family:'CoverSerif','Noto Serif SC','Songti SC',serif}}
.canvas{{position:relative;width:{W}px;height:{H}px;
  background:
    radial-gradient(900px 620px at 82% 8%, rgba(201,168,106,.16), transparent 62%),
    radial-gradient(760px 520px at 6% 96%, rgba(201,168,106,.08), transparent 60%),
    linear-gradient(158deg,#1b1712 0%,#12100d 52%,#171310 100%);}}
.frame{{position:absolute;inset:52px;border:1px solid rgba(201,168,106,.22)}}
.inner{{position:absolute;inset:52px;padding:74px 86px;display:flex;flex-direction:column;justify-content:center}}
.label{{font-size:24px;letter-spacing:.42em;color:#c9a86a;text-transform:uppercase;margin-bottom:44px}}
.label::before{{content:"";display:inline-block;width:44px;height:1px;background:#c9a86a;
  vertical-align:middle;margin-right:22px;opacity:.75}}
h1{{font-weight:600;font-size:{title_size(title)}px;line-height:1.34;letter-spacing:.02em;
  color:#f6efe4;max-width:1220px;word-break:break-word}}
.rule{{width:120px;height:3px;margin:52px 0 0;
  background:linear-gradient(90deg,#c9a86a,rgba(201,168,106,0))}}
.foot{{position:absolute;left:86px;right:86px;bottom:78px;display:flex;
  justify-content:space-between;align-items:baseline;font-size:26px;color:#8d8377;
  letter-spacing:.16em}}
.site{{color:#d8cbb4;letter-spacing:.24em}}
</style></head><body><div class="canvas">
  <div class="frame"></div>
  <div class="inner">
    <div class="label">{esc_label}</div>
    <h1>{esc_title}</h1>
    <div class="rule"></div>
  </div>
  <div class="foot"><span class="site">{html.escape(SITE_NAME)}</span><span>{esc_date}</span></div>
</div></body></html>"""


def label_for(fm: dict, rel: Path) -> str:
    for key in ("series", "categories", "tags"):
        vals = fm.get(key) or []
        if vals:
            return str(vals[0])
    return rel.parts[0] if len(rel.parts) > 1 else "post"


def bundle_dir(md: Path) -> Path:
    """文章所在的 bundle 目录：index.md 用自身目录，叶子 md 用 <目录>/<文件名>/。"""
    if md.name == "index.md":
        return md.parent
    return md.parent / md.stem


def collect(fmt: str) -> list[tuple[Path, Path]]:
    """返回 [(md 路径, 输出图片路径)]，只收 regular page（跳过 _index.md）。"""
    items = []
    for md in sorted(POSTS.rglob("*.md")):
        if md.name == "_index.md":
            continue
        items.append((md, bundle_dir(md) / f"{COVER_NAME}.{fmt}"))
    return items


def to_webp(src: Path, dst: Path, quality: int) -> None:
    """Chrome 只能截 PNG；再用 Pillow 压缩成 WebP（体积约 1/17，肉眼无差）。"""
    from PIL import Image

    with Image.open(src) as im:
        im.convert("RGB").save(dst, "WEBP", quality=quality, method=6)
    src.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 篇")
    ap.add_argument("--only", default="", help="只处理路径包含该子串的文章，逗号分隔")
    ap.add_argument("--all", action="store_true", help="处理全部（默认跳过已存在的图）")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的图")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不生成")
    ap.add_argument("--jobs", type=int, default=6, help="并发数（默认 6）")
    ap.add_argument("--format", choices=("webp", "png"), default="webp",
                    help="输出格式，默认 webp（PNG 体积大约 17 倍）")
    ap.add_argument("--quality", type=int, default=85, help="WebP 质量，默认 85")
    args = ap.parse_args()

    chrome = find_chrome()
    font_uri = find_font()
    items = collect(args.format)

    if args.only:
        keys = [k.strip() for k in args.only.split(",") if k.strip()]
        items = [(md, png) for md, png in items if any(k in md.relative_to(POSTS).as_posix() for k in keys)]
    if args.limit:
        items = items[: args.limit]
    if not args.all and not args.only and not args.limit:
        ap.error("请指定 --limit N / --only 子串 / --all")

    def has_cover(md: Path, png: Path) -> bool:
        """bundle 里已有任何 feature/cover/thumbnail 图片就跳过（不只是 featured.webp）。"""
        if png.exists():
            return True
        d = bundle_dir(md)
        return d.is_dir() and any(
            re.search(r"(?i)(feature|cover|thumbnail)", x.name)
            for x in d.iterdir()
            if x.is_file() and re.search(r"(?i)\.(jpg|jpeg|png|webp|avif|gif)$", x.name)
        )

    todo = [(md, png) for md, png in items if args.force or not has_cover(md, png)]
    print(f"待生成 {len(todo)} 张（候选 {len(items)}）")
    if args.dry_run:
        for md, png in todo:
            print(f"  {md.relative_to(ROOT).as_posix()} -> {png.relative_to(ROOT).as_posix()}")
        return

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)

        def render(idx_md_png):
            i, (md, png) = idx_md_png
            fm = read_frontmatter(md)
            title = fm.get("title") or md.stem
            rel = md.relative_to(POSTS).with_suffix("")
            label = label_for(fm, rel)
            date = (fm.get("date") or "")[:10]
            # 每个任务用独立 HTML，避免并发写同一个文件
            page = tmpdir / f"cover_{i}.html"
            page.write_text(build_html(title, label, date, font_uri), encoding="utf-8")
            png.parent.mkdir(parents=True, exist_ok=True)
            shot = tmpdir / f"shot_{i}.png"
            r = subprocess.run(
                [
                    chrome,
                    "--headless=new",
                    "--disable-gpu",
                    "--hide-scrollbars",
                    "--allow-file-access-from-files",
                    f"--window-size={W},{H}",
                    "--virtual-time-budget=1500",
                    f"--screenshot={shot}",
                    page.as_uri(),
                ],
                capture_output=True,
            )
            if r.returncode == 0 and shot.exists():
                try:
                    if args.format == "webp":
                        to_webp(shot, png, args.quality)
                    else:
                        shot.replace(png)
                except Exception as exc:  # 转换失败不拖垮整批
                    print(f"  [{i}/{len(todo)}] 转换失败 {md}: {exc}", flush=True)
                    return False
            ok = png.exists()
            msg = (
                f"  [{i}/{len(todo)}] {png.relative_to(ROOT).as_posix()}  ({title})"
                if ok
                else f"  [{i}/{len(todo)}] 失败 {md}: {r.stderr.decode('utf-8', 'ignore')[:160]}"
            )
            print(msg, flush=True)
            return ok

        # Chrome 启动占大头，并发跑能快 4~6 倍
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(render, enumerate(todo, 1)))
        print(f"完成 {sum(results)}/{len(todo)}，失败 {len(results) - sum(results)} 张", flush=True)


if __name__ == "__main__":
    main()
