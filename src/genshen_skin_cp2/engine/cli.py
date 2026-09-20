# -*- coding: utf-8 -*-
"""
原神 CP 壁纸套件 2 —— 命令行

  genshen-cp2                 # 直接应用默认壁纸(第 1 张 比心)
  genshen-cp2 2               # 应用第 2 张 共舞
  genshen-cp2 3 --cover       # 第 3 张按 cover 满屏裁切
  genshen-cp2 list            # 列出所有可切换样式
  genshen-cp2 random          # 随机来一张
  genshen-cp2 all             # 生成全部样式到 ~/.genshen-cp2/wallpapers
  genshen-cp2 all --out DIR   # 生成到指定目录(JetBrains 背景图用)
  genshen-cp2 cycle 30        # 每 30 分钟自动随机换壁纸
  genshen-cp2 switcher        # 打开可视化切换器
  genshen-cp2 pet             # 启动桌面桌宠
  genshen-cp2 copy            # 只合成不设置
  genshen-cp2 info            # 环境与素材自检
"""
import argparse
import os
import sys
import time

from ..characters import odette_voj as C
from . import skin_core as sc


def _cmd_apply(args):
    mode = sc.resolve_mode(args.mode)
    if args.cover:
        mode = "cover" + mode.lstrip("single")
    size = sc.parse_size(args.size) if args.size else None
    out = sc.build(mode, size, force=True)
    print("[%s] 已生成: %s  (%s)" % (C.APP_SLUG, out, sc.mode_label(mode)))
    if args.no_set:
        return 0
    sc.set_wallpaper(out)
    return 0


def _cmd_list(args):
    size = sc.screen_size()
    print("%s  (%dx%d)" % (C.DISPLAY_NAME, size[0], size[1]))
    print("-" * 58)
    for key, label in sc.MODES:
        mark = " *默认" if key == sc.DEFAULT_MODE else ""
        print("  %-9s %s%s" % (key, label, mark))
    print("-" * 58)
    print("  用法: %s <模式名或数字>  |  %s random  |  %s switcher"
          % (C.APP_SLUG, C.APP_SLUG, C.APP_SLUG))
    return 0


def _cmd_all(args):
    size = sc.parse_size(args.size) if args.size else None
    rows = sc.build_all(args.out, size)
    print("[%s] 已生成 %d 个样式 尺寸 %dx%d:" % (
        C.APP_SLUG, len(rows), *(size or sc.screen_size())))
    for key, label, path in rows:
        print("  OK  %-9s %-14s %s" % (key, label, path))
    return 0


def _cmd_random(args):
    mode = sc.pick_random()
    size = sc.parse_size(args.size) if args.size else None
    out = sc.build(mode, size, force=True)
    print("[%s] 随机到: %s" % (C.APP_SLUG, sc.mode_label(mode)))
    if args.no_set:
        print("[%s] 已生成: %s" % (C.APP_SLUG, out))
        return 0
    sc.set_wallpaper(out)
    return 0


def _cmd_cycle(args):
    minutes = max(1, int(args.minutes))
    print("[%s] 每 %d 分钟随机换壁纸, Ctrl+C 停止。" % (C.APP_SLUG, minutes))
    try:
        while True:
            mode = sc.pick_random()
            sc.apply(mode)
            time.sleep(minutes * 60)
    except KeyboardInterrupt:
        print("\n[%s] 已停止。" % C.APP_SLUG)
    return 0


def _cmd_copy(args):
    size = sc.parse_size(args.size) if args.size else None
    rows = sc.build_all(args.out, size)
    print("[%s] 已生成 %d 张到 %s (未设置壁纸):" % (
        C.APP_SLUG, len(rows), os.path.abspath(args.out or C.WALLPAPER_DIR)))
    for key, label, path in rows:
        print("  OK  %-9s %s" % (key, path))
    return 0


def _cmd_gui(args, script):
    from . import gui_launch
    return gui_launch(script)


def _cmd_deepking(args):
    from . import deepking_cli
    argv = []
    if getattr(args, "check", False):
        argv.append("--check")
    if getattr(args, "what", False):
        argv.append("--what")
    if getattr(args, "out", None):
        argv += ["--out", args.out]
    return deepking_cli.main(argv)


def _cmd_info(args):
    print("=" * 58)
    print("  " + C.DISPLAY_NAME)
    print("=" * 58)
    print("  版本      : %s" % C.VERSION)
    print("  PyPI 包名 : %s" % C.PACKAGE_NAME)
    print("  仓库      : %s" % C.REPO_URL)
    print("  Python    : %s" % sys.version.split()[0])
    print("  运行目录  : %s" % sc.APP_DIR)
    try:
        print("  素材目录  : %s" % sc.assets_dir())
    except FileNotFoundError as e:
        print("  素材目录  : [缺失] %s" % e)
        return 1
    print("  屏幕尺寸  : %dx%d" % sc.screen_size())
    try:
        import PIL
        print("  Pillow    : %s" % getattr(PIL, "__version__", "?"))
    except ImportError:
        print("  Pillow    : [缺失] 将自动安装")
    print("-" * 58)
    for i, name in enumerate(sc.IMAGE_NAMES, 1):
        p = sc.asset_path(i)
        ok = os.path.exists(p)
        print("  %d. %-8s %s  %s" % (
            i, name, "OK " if ok else "缺失", sc.IMAGE_FILES[i - 1]))
    print("-" * 58)
    return 0


def build_parser():
    ap = argparse.ArgumentParser(
        prog=C.APP_SLUG,
        description="%s —— 单张样式壁纸一键切换" % C.DISPLAY_NAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = ap.add_subparsers(dest="cmd")

    def add_common(p):
        p.add_argument("--size", default=None, help="壁纸尺寸, 如 2560x1440(默认取屏幕分辨率)")
        p.add_argument("--no-set", action="store_true", help="只生成, 不设置为系统壁纸")

    p = sub.add_parser("list", help="列出所有可切换样式")
    p.set_defaults(func=_cmd_list)

    p = sub.add_parser("all", help="生成全部样式")
    p.add_argument("--out", default=None, help="输出目录")
    p.add_argument("--size", default=None)
    p.set_defaults(func=_cmd_all)

    p = sub.add_parser("random", help="随机换一张")
    add_common(p)
    p.set_defaults(func=_cmd_random)

    p = sub.add_parser("copy", help="只合成不设置")
    p.add_argument("--out", default=None, help="输出目录")
    p.add_argument("--size", default=None)
    p.set_defaults(func=_cmd_copy)

    p = sub.add_parser("cycle", help="定时自动随机换壁纸")
    p.add_argument("minutes", nargs="?", type=int, default=30, help="间隔分钟数, 默认 30")
    p.set_defaults(func=_cmd_cycle)

    p = sub.add_parser("switcher", help="打开可视化切换器")
    p.set_defaults(func=lambda a: _cmd_gui(a, "switcher.py"))

    p = sub.add_parser("pet", help="启动桌面桌宠")
    p.set_defaults(func=lambda a: _cmd_gui(a, "pet.py"))

    p = sub.add_parser("info", help="环境与素材自检")
    p.set_defaults(func=_cmd_info)

    p = sub.add_parser("deepking", help="接入 DeepKing 界面皮肤(生成皮肤 JSON + 预览)")
    p.add_argument("--check", action="store_true", help="只做 DeepKing 转换契约自检")
    p.add_argument("--what", action="store_true", help="显示 DeepKing 会从仓库提取到什么")
    p.add_argument("--out", default=None, help="输出目录")
    p.set_defaults(func=_cmd_deepking)

    # 位置参数兼容: genshen-cp2 2 / genshen-cp2 single2
    ap.add_argument("mode", nargs="?", default=None, help="样式名或序号: 1 2 3 / single1 / cover1")
    ap.add_argument("--cover", action="store_true", help="按 cover 满屏裁切(默认模糊填充+居中卡片)")
    ap.add_argument("--size", default=None, help="壁纸尺寸, 如 2560x1440")
    ap.add_argument("--no-set", action="store_true", help="只生成, 不设置为系统壁纸")
    return ap


def main(argv=None):
    sc.prepare_console()
    ap = build_parser()
    args = ap.parse_args(argv)

    if getattr(args, "func", None):
        sc.ensure_pillow()
        sc.ensure_dirs()
        try:
            return args.func(args)
        except KeyboardInterrupt:
            return 0
        except Exception as e:
            print("[%s] 出错: %s" % (C.APP_SLUG, e), file=sys.stderr)
            return 1

    # 无子命令: 直接应用壁纸
    sc.ensure_pillow()
    sc.ensure_dirs()
    try:
        return _cmd_apply(args)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print("[%s] 出错: %s" % (C.APP_SLUG, e), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
