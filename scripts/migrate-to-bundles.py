#!/usr/bin/env python3
"""把 content/posts 下的叶子 md 迁移成 page bundle。

规则：
  1. 已有封面的生成图 assets/img/covers/<路径>.webp → <bundle>/featured.webp，
     frontmatter 改成 featureimage = "featured.webp"
  2. 文件名与所在目录同名（如 pyqt5指南/pyqt5指南.md）→ 就地变成 <目录>/index.md
     URL 会少一段，因此自动补 aliases 指向旧地址
  3. 其余 → <目录>/<文件名>/index.md，URL 不变
  4. 目录里只有这一篇文章时，同级 imgs/ 等资源目录一起搬进 bundle，
     正文引用 ../imgs/ → imgs/
  5. 同一目录下多篇文章之间 ./x.md 链接 → ../x/
  6. 与已有 bundle 重复的叶子文件（creed.md / multi-user.md）直接删除，
     bundle 版本内容更全

用法：
  python scripts/migrate-to-bundles.py --dry-run
  python scripts/migrate-to-bundles.py --apply
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"
COVERS = ROOT / "assets" / "img" / "covers"

# 与已有 bundle 重复、内容更少，直接删掉
DUPLICATES = ["bible_stu/creed.md", "system/multi-user.md"]
# 单篇文章目录里的资源子目录
ASSET_DIRS = ("imgs", "gallery", "images")


def split_frontmatter(text: str):
    if text.startswith("+++"):
        end = text.find("\n+++", 3)
        return text[:end], "+++", text[end + 4:]
    if text.startswith("---"):
        end = text.find("\n---", 3)
        return text[:end], "---", text[end + 4:]
    return "", "", text


def rewrite_body(body: str, flat: bool) -> str:
    if not flat:
        # 资源被搬进 bundle 后，../imgs/ 变成 imgs/
        body = body.replace("../imgs/", "imgs/")
    else:
        body = body.replace("../imgs/", "imgs/")
    # 同目录文章之间的 ./xxx.md → ../xxx/
    body = re.sub(r"\]\(\./([^)/\s]+)\.md\)", r"](../\1/)", body)
    return body


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not (args.dry_run or args.apply):
        ap.error("请指定 --dry-run 或 --apply")
    dry = args.dry_run

    md_files = sorted(
        p for p in POSTS.rglob("*.md") if p.name not in ("index.md", "_index.md")
    )
    # 每个目录里有几篇文章（决定资源归属）
    per_dir: dict[Path, int] = {}
    for p in md_files:
        per_dir[p.parent] = per_dir.get(p.parent, 0) + 1

    plan = []
    for p in md_files:
        rel = p.relative_to(POSTS).as_posix()
        if rel in DUPLICATES:
            plan.append(("delete-dupe", p, None, None))
            continue
        flat = p.stem == p.parent.name
        target_dir = p.parent if flat else p.parent / p.stem
        plan.append(("flat" if flat else "nest", p, target_dir, flat))

    for kind, p, target_dir, flat in plan:
        rel = p.relative_to(POSTS).as_posix()
        if kind == "delete-dupe":
            print(f"[删除重复] {rel}")
            if not dry:
                p.unlink()
            continue

        dest_md = target_dir / "index.md"
        assert not dest_md.exists() or dest_md == p, f"目标已存在: {dest_md}"

        # 资源：独占目录才搬
        moves = []
        if per_dir[p.parent] == 1:
            for name in ASSET_DIRS:
                src = p.parent / name
                if src.is_dir() and target_dir != p.parent:
                    moves.append((src, target_dir / name))

        # 封面
        cover = COVERS / p.relative_to(POSTS).with_suffix("").with_suffix(".webp")

        print(f"[{kind}] {rel}")
        print(f"        → {dest_md.relative_to(POSTS).as_posix()}")
        for s, d in moves:
            print(f"        资源 {s.name}/ → {d.relative_to(POSTS).as_posix()}")
        print(f"        封面 {'有' if cover.exists() else '无'}"
              f"{' → featured.webp' if cover.exists() else ''}")

        if dry:
            continue

        text = p.read_text(encoding="utf-8", errors="ignore")
        fm, fence, body = split_frontmatter(text)
        body = rewrite_body(body, flat)

        if cover.exists():
            fm = re.sub(r'featureimage\s*=\s*"[^"]*"', 'featureimage = "featured.webp"', fm)
            fm = re.sub(r'featureimage\s*:\s*\S+', 'featureimage: featured.webp', fm)

        if flat:
            old_url = f"/posts/{p.relative_to(POSTS).with_suffix('').as_posix()}/"
            if "aliases" not in fm:
                fm += f'\naliases = ["{old_url}"]'
            else:
                fm += f'\n# 旧地址（bundle 化后 URL 少一段）： {old_url}'

        target_dir.mkdir(parents=True, exist_ok=True)
        dest_md.write_text(fm + fence + body, encoding="utf-8", newline="\n")
        if p != dest_md:
            p.unlink()

        for s, d in moves:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(s), str(d))
            print(f"        moved {s.name}/")

        if cover.exists():
            cover.replace(target_dir / "featured.webp")
            print("        moved cover")

    if not dry:
        # 清掉空的 covers 目录
        if COVERS.exists():
            shutil.rmtree(COVERS)
            print("删除 assets/img/covers/")

    print(f"\n{'[dry-run] ' if dry else ''}共处理 {len(plan)} 篇")


if __name__ == "__main__":
    main()
