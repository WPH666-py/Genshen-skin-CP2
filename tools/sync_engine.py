# -*- coding: utf-8 -*-
"""
引擎同步工具 —— 让 CP1 与 CP2 共用同一套皮肤引擎, 不再各改一份。

背景
----
CP1(Genshen-Skin-CP1 · 米提亚×沃雅妮莎)先做出来, 引擎代码直接放在
`src/genshin_skin_cp1/` 里; CP2 起把通用逻辑抽到 `src/genshen_skin_cp2/engine/`,
角色数据放 `src/genshen_skin_cp2/characters/`。
两个包名/目录不同, 但引擎文件本该一致, 否则修一个 bug 要改两处。

用法
----
    python tools/sync_engine.py --to CP2 --dry-run     # 看会把 CP1 的引擎盖到 CP2 哪些文件
    python tools/sync_engine.py --to CP2               # 实际同步(会先备份)
    python tools/sync_engine.py --check                # 只报告两边差异

注意
----
* 只同步**引擎**文件; 角色数据(characters/、skin.json、CSS、素材)从不同步。
* CP2 的引擎比 CP1 多了这些改进, 同步到 CP1 时会被保留:
    - repo_root() 要求 skin.json + src/client 同时存在
    - pkg_root() / api_root() 区分「仓库根」与「包目录」
    - find_css 只认 <根>/src/client/*.module.css
    - find_mascots 排除 engine/assets 与 vscode/media
    - compose_cover 支持 cover_bias 取景偏向
  因此默认方向是 CP2 -> CP1(把改进带回去), 而不是反向覆盖。
"""
import argparse
import difflib
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# tools/ 在仓库里, 所以工作区还要再往上一层
WORKSPACE = os.path.dirname(os.path.dirname(HERE))

# 引擎文件清单(相对包内 engine/ 目录)
ENGINE_FILES = [
    "_color.py",
    "skin_core.py",
    "cli.py",
    "switcher.py",
    "pet.py",
    "mcp_server.py",
    "autoinstall.py",
    "gui_launch.py",
    "deepking.py",
    "deepking_cli.py",
    "deepking_skin.py",
]

# 每个套件: 名字 -> (仓库目录, 引擎目录, 角色数据模块路径)
PACKS = {
    "CP1": {
        "repo": os.path.join(WORKSPACE, "Genshen-Skin-CP1"),
        "engine": os.path.join(WORKSPACE, "Genshen-Skin-CP1", "src", "genshin_skin_cp1"),
        "chars": None,  # CP1 尚无独立角色模块, 常量就在 config.py 里
        "slug": "genshin_skin_cp1",
    },
    "CP2": {
        "repo": os.path.join(WORKSPACE, "Genshen-skin-CP2"),
        "engine": os.path.join(WORKSPACE, "Genshen-skin-CP2", "src",
                               "genshen_skin_cp2", "engine"),
        "chars": os.path.join(WORKSPACE, "Genshen-skin-CP2", "src",
                              "genshen_skin_cp2", "characters"),
        "slug": "genshen_skin_cp2",
    },
}


def sha(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:12]


def normalize(text, src_slug, dst_slug, dst_key=None):
    """把源套件的包名/命令名换成目标套件的, 使文件内容可直接落盘。

    还要改写「常量模块」的导入:
      CP2 的角色数据在 characters/<角色>.py, 引擎用
          from ..characters import odette_voj as C
      导入; CP1 没有 characters 包, 常量就在 config.py, 用
          from . import config as C
      两者暴露的常量名一致, 所以换掉这一行即可。
    """
    src_short = src_slug.replace("genshin_", "").replace("genshen_", "")   # skin_cp1
    dst_short = dst_slug.replace("genshin_", "").replace("genshen_", "")
    pairs = [
        (src_slug, dst_slug),
        (src_slug.replace("_", "-"), dst_slug.replace("_", "-")),
        (src_short.replace("_", "-"), dst_short.replace("_", "-")),
    ]
    out = text
    for a, b in pairs:
        out = out.replace(a, b)

    if dst_key == "CP1":
        # CP1 是扁平包: characters/<角色>.py -> config.py
        out = out.replace("from ..characters import odette_voj as C",
                          "from . import config as C")
        out = out.replace("from ..characters.odette_voj import (",
                          "from .config import (")
        out = out.replace("from ..engine import _color as col",
                          "from . import _color as col")
    return out


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def sync(src_key, dst_key, dry_run=False, backup=True):
    src, dst = PACKS[src_key], PACKS[dst_key]
    src_slug, dst_slug = src["slug"], dst["slug"]
    changed, same, missing = [], [], []

    for name in ENGINE_FILES:
        sp = os.path.join(src["engine"], name)
        dp = os.path.join(dst["engine"], name)
        if not os.path.exists(sp):
            missing.append(name)
            continue
        s_text = normalize(read(sp), src_slug, dst_slug, dst_key)
        d_text = read(dp) if os.path.exists(dp) else None
        if d_text == s_text:
            same.append(name)
            continue
        changed.append(name)
        print("  ~ %-20s %s -> %s" % (name, sha(sp) or "(新)", sha(dp) or "(缺失)"))
        if not dry_run:
            if d_text is not None and backup:
                shutil.copy2(dp, dp + ".bak")
            write(dp, s_text)

    print()
    print("  %s -> %s : 改动 %d, 一致 %d, 源缺失 %d"
          % (src_key, dst_key, len(changed), len(same), len(missing)))
    if missing:
        print("  源里没有这些文件, 跳过: %s" % ", ".join(missing))
    return changed


def check():
    a, b = PACKS["CP1"], PACKS["CP2"]
    print("  %-20s %-14s %-14s %s" % ("引擎文件", "CP1", "CP2", "状态"))
    print("  " + "-" * 62)
    diff = 0
    for name in ENGINE_FILES:
        pa = os.path.join(a["engine"], name)
        pb = os.path.join(b["engine"], name)
        ha, hb = sha(pa), sha(pb)
        if ha is None or hb is None:
            status = "缺失"
        elif ha == hb:
            status = "一致"
        else:
            status = "不同"
            diff += 1
        print("  %-20s %-14s %-14s %s" % (name, ha or "-", hb or "-", status))
    print()
    print("  两边哈希不同的文件: %d 个" % diff)
    print("  说明: CP2 的引擎含若干改进(repo_root/pkg_root/find_css/find_mascots/"
          "cover_bias),")
    print("        这些是**有意**的差异, 不是漂移。以 CP2 为准, 不要反向覆盖。")
    return diff


def main():
    ap = argparse.ArgumentParser(description="CP1/CP2 皮肤引擎同步工具")
    ap.add_argument("--to", choices=sorted(PACKS), help="目标套件")
    ap.add_argument("--from", dest="src", choices=sorted(PACKS), default="CP2",
                    help="源套件(默认 CP2, 它是包含最新改进的一份)")
    ap.add_argument("--check", action="store_true", help="只报告两侧差异")
    ap.add_argument("--dry-run", action="store_true", help="只显示将要改动什么")
    args = ap.parse_args()

    if args.check:
        return 0 if check() >= 0 else 1
    if not args.to:
        ap.error("请用 --to 指定目标套件, 或用 --check 只看差异")
    if args.to == args.src:
        ap.error("源和目标不能相同")

    print("=== 同步引擎 %s -> %s%s ===" % (args.src, args.to, "(dry-run)" if args.dry_run else ""))
    changed = sync(args.src, args.to, dry_run=args.dry_run)
    if changed and not args.dry_run:
        print()
        print("  已写入。原文件备份为 *.bak, 确认无误后请删除。")
        print("  下一步: 重建受影响套件的 wheel / vsix 并推送。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
