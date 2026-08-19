#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""seo-check: 双语 SEO + GEO 体检脚本

用法:
  python scripts/seo-check.py            # 检查本地 public/ 构建产物
  python scripts/seo-check.py --live     # 检查线上站点 https://zhenda-hub.github.io

每次迭代博客后跑一遍：本地构建 -> 推送 -> --live 复查。
"""
import argparse
import json
import os
import re
import urllib.request
from urllib.parse import unquote

BASE = "https://zhenda-hub.github.io"
PUB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public")
AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-Web",
           "anthropic-ai", "PerplexityBot", "Google-Extended", "CCBot", "cohere-ai",
           "ai2bot", "Applebot-Extended", "meta-externalagent", "Bytespider"]

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 seo-check"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def read_local(path):
    if path == "/" or path.endswith("/"):
        path += "index.html"
    with open(os.path.join(PUB, path.lstrip("/")), encoding="utf-8") as f:
        return f.read()


def get_text(path, live):
    return fetch(BASE + path) if live else read_local(path)


def main():
    ap = argparse.ArgumentParser(description="双语 SEO + GEO 体检")
    ap.add_argument("--live", action="store_true", help="检查线上站点（默认检查本地 public/）")
    ap.add_argument("--summary", nargs="?", const="__env__",
                    help="输出 Markdown 报告到 GITHUB_STEP_SUMMARY（或指定文件路径）")
    args = ap.parse_args()
    live = args.live
    mode = "线上" if live else "本地 public/"
    print(f"===== SEO 体检 [{mode}] =====\n")

    # 1. robots.txt
    try:
        robots = get_text("/robots.txt", live)
        missing = [b for b in AI_BOTS if f"User-agent: {b}" not in robots]
        check("robots.txt 放行 + AI 爬虫",
              "Allow: /" in robots and not missing and BASE in robots,
              f"缺失AI爬虫: {missing if missing else '无'}")
    except Exception as e:
        check("robots.txt", False, str(e))

    # 2. llms.txt
    try:
        llms = get_text("/llms.txt", live)
        links = len(re.findall(r"https://zhenda-hub\.github\.io/posts/", llms))
        check("llms.txt 双语 + 文章清单", "中文为主" in llms and links > 50, f"{links} 个文章链接")
    except Exception as e:
        check("llms.txt", False, str(e))

    # 3. sitemap
    try:
        sm = get_text("/sitemap.xml", live)
        locs = re.findall(r"<loc>([^<]*)</loc>", sm)
        bad = [u for u in locs if "localhost" in u or not u.startswith(BASE)]
        check("sitemap.xml", len(locs) > 50 and not bad, f"{len(locs)} 个URL")
    except Exception as e:
        check("sitemap.xml", False, str(e))

    # 4. 首页
    try:
        home = get_text("/", live)
        check("首页 lang=zh-CN", re.search(r'<html lang="?zh-CN', home) is not None)
        title = re.search(r"<title>([^<]*)</title>", home)
        check("首页标题中文", bool(title and re.search(r"[\u4e00-\u9fff]", title.group(1))),
              title.group(1)[:40] if title else "无")
        desc = re.search(r'name="?description"? content="([^"]*)"', home)
        check("首页 description 双语",
              bool(desc and re.search(r"[\u4e00-\u9fff]", desc.group(1)) and "Zhenda" in desc.group(1)),
              (desc.group(1)[:50] + "…") if desc else "无")
        rmeta = re.search(r'name="?robots"? content="([^"]*)"', home)
        check("robots meta (GEO)", bool(rmeta and "max-snippet" in rmeta.group(1)))
        jsonld = re.findall(r'<script type="?application/ld\+json"?>(.*?)</script>', home, re.S)
        types = [json.loads(b).get("@type") for b in jsonld if b.strip().startswith("{")]
        check("首页 JSON-LD WebSite", "WebSite" in types)
        og = re.search(r'property="?og:image"? content="([^"]*)"', home)
        check("og:image 默认社交图", bool(og and "social-card" in og.group(1)))
    except Exception as e:
        check("首页", False, str(e))

    # 5. 文章页 JSON-LD（全量检查：从 sitemap 提取所有文章 URL）
    try:
        sm = get_text("/sitemap.xml", live)
        locs = re.findall(r"<loc>([^<]*)</loc>", sm)
        articles = [u for u in locs
                    if re.match(rf"^{re.escape(BASE)}/posts/[^/]+/[^/]+/$", u)]
        passed, fails = 0, []
        for u in articles:
            try:
                if live:
                    h = fetch(u)
                else:
                    with open(os.path.join(PUB, unquote(u.replace(BASE + "/", "")), "index.html"),
                              encoding="utf-8") as f:
                        h = f.read()
                ld = re.findall(r'<script type="?application/ld\+json"?>(.*?)</script>', h, re.S)
                types = []
                for b in ld:
                    try:
                        d = json.loads(b)
                        types += [i.get("@type") for i in d] if isinstance(d, list) else [d.get("@type")]
                    except Exception:
                        pass
                if "Article" in types and "BreadcrumbList" in types:
                    passed += 1
                else:
                    fails.append(u)
            except Exception as e:
                fails.append(f"{u} ({e})")
        detail = f"{passed}/{len(articles)} 篇通过"
        if fails:
            shown = "; ".join(fails[:3])
            more = "…" if len(fails) > 3 else ""
            detail += f"，失败: {shown}{more}"
        check(f"文章 JSON-LD 全量 ({len(articles)} 篇)", not fails, detail)
    except Exception as e:
        check("文章 JSON-LD 全量", False, str(e))

    # 6. 本地 description 覆盖率（仅本地模式）
    if not live:
        content_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "content", "posts")
        total = desc_count = 0
        for dp, _, fs in os.walk(content_root):
            for f in fs:
                if not f.endswith(".md"):
                    continue
                raw = open(os.path.join(dp, f), encoding="utf-8").read()
                m = re.match(r"^\+{3}\n(.*?)\n\+{3}\n", raw, re.S)
                if not m:
                    continue
                total += 1
                if re.search(r"^description\s*=", m.group(1), re.M):
                    desc_count += 1
        check("文章 description 覆盖率（本地）", desc_count >= 10, f"{desc_count}/{total} 篇")

    # 输出（终端）
    print(f"{'检查项':38s} {'状态':4s} 说明")
    print("-" * 80)
    for name, ok, detail in results:
        print(f"{name:40s} {'✅' if ok else '❌':4s} {detail}")
    fails = sum(1 for _, ok, _ in results if not ok)
    total_ok = len(results) - fails
    print("-" * 80)
    print(f"通过 {total_ok}/{len(results)} 项{'  → 可推送上线' if not live and fails == 0 else ''}")

    # --summary: 写 Markdown 报告（GitHub Actions Step Summary / 指定路径）
    if args.summary:
        if args.summary == "__env__":
            summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
            if not summary_path:
                print("[seo-check] 未设置 GITHUB_STEP_SUMMARY，跳过 summary 输出")
                summary_path = None
        else:
            summary_path = args.summary
        if summary_path:
            lines = ["## SEO/GEO 体检报告", "",
                     f"- 模式: {'线上' if live else '本地 public/'}", "",
                     "| 检查项 | 状态 | 说明 |",
                     "|--------|:----:|------|"]
            for name, ok, detail in results:
                lines.append(f"| {name} | {'✅' if ok else '❌'} | {detail} |")
            lines.append("")
            verdict = "✅ PASS" if fails == 0 else "❌ FAIL"
            lines.append(f"**结果: 通过 {total_ok}/{len(results)} 项 → {verdict}**")
            with open(summary_path, "a", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            print(f"[seo-check] 报告已写入: {summary_path}")

    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
