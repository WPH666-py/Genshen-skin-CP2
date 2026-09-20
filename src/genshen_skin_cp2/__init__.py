# -*- coding: utf-8 -*-
"""
原神 CP 壁纸套件 2 —— 奥黛塔 × 沃雅妮莎
单张样式一键切换壁纸 / 桌面桌宠 / 多 IDE 皮肤 / DeepKing 界面皮肤

    import genshen_skin_cp2 as gs
    gs.build("single2")          # 合成第 2 张壁纸, 返回文件路径
    gs.set_wallpaper(path)       # 设为系统壁纸

本包与 CP1(Genshen-skin-CP2 · 米提亚×沃雅妮莎)并列, 命名空间完全隔离:
包名 genshen-skin-cp2 / 命令 genshen-cp2 / 运行时目录 ~/.genshen-cp2,
两个套件可同时安装、各自切换。
"""
from .characters.odette_voj import (  # noqa: F401
    APP_DIR,
    APP_NAME,
    APP_SLUG,
    DEFAULT_MODE,
    DEEPKING_SKIN_ID,
    DEEPKING_SKIN_NAME,
    DISPLAY_NAME,
    IMAGE_FILES,
    IMAGE_META,
    IMAGE_NAMES,
    MODES,
    PACKAGE_NAME,
    PAIR,
    REPO_NAME,
    REPO_URL,
    SERIES,
    VERSION,
)
from .engine.skin_core import (  # noqa: F401
    asset_path,
    build,
    build_all,
    compose,
    ensure_dirs,
    ensure_pillow,
    mode_label,
    prepare_console,
    screen_size,
    set_wallpaper,
    wallpaper_path,
)

__all__ = [
    "APP_DIR", "APP_NAME", "APP_SLUG", "DEFAULT_MODE",
    "DEEPKING_SKIN_ID", "DEEPKING_SKIN_NAME", "DISPLAY_NAME",
    "IMAGE_FILES", "IMAGE_META", "IMAGE_NAMES", "MODES",
    "PACKAGE_NAME", "PAIR", "REPO_NAME", "REPO_URL", "SERIES", "VERSION",
    "asset_path", "build", "build_all", "compose", "ensure_dirs",
    "ensure_pillow", "mode_label", "prepare_console", "screen_size",
    "set_wallpaper", "wallpaper_path",
]

__version__ = VERSION
