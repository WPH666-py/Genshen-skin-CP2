# -*- coding: utf-8 -*-
"""
原神CP2 · 纳西妲×安柏 —— DeepKing 皮肤(手工校色版)

DeepKing 支持两种接入方式:

  A. 在「设置 → 界面皮肤」粘贴本仓库地址 —— DeepKing 抓 skin.json + CSS 变量,
     按内置规则自动推导 32 槽位调色板。这条路的「亮色」精确取自
     src/client/genshen-cp2.module.css, 「暗色」由其内置算法从亮色派生。

  B. 直接用本文件: 下面两套调色板是**逐槽位手工校色**的结果, 不经过任何推导,
     夜景保留素材的深林墨绿, 而不是派生算法给出的中性灰。

安装器(genshen-cp2 deepking)会把本调色板写成 genshen-cp2.skin.json,
并生成可视化预览 genshen-cp2-preview.html, 方便导入前先看效果。
"""
from ..characters import odette_voj as C

SKIN_ID = C.DEEPKING_SKIN_ID
SKIN_NAME = C.DEEPKING_SKIN_NAME
SKIN_DESC = C.DEEPKING_SKIN_DESC

# ─────────────────────────────────────────────── 亮色 · 晨光米白(林间日光)
LIGHT = {
    "bg": "#fffdf6",
    "bgText": "#1d2b16",
    "sidebarBg": "#eef4e6",
    "sidebarText": "#28381e",
    "sidebarHover": "#e2eed8",
    "sidebarSelected": "#cbe0bb",
    "sidebarHeader": "#7b8c6b",
    "editorBg": "#fffdf6",
    "tabsBg": "#f3f7ec",
    "tabBg": "#e9f0df",
    "tabText": "#5c6f4b",
    "tabActiveBg": "#fffdf6",
    "tabActiveText": "#1d2b16",
    "aiBg": "#f6faf0",
    "aiText": "#1d2b16",
    "aiTabText": "#5c6f4b",
    "userBubbleBg": "#d5e8c4",
    "userBubbleText": "#1d2b16",
    "aiBubbleBg": "#fffdf6",
    "aiBubbleText": "#1d2b16",
    "aiBubbleBorder": "#c7dab4",
    "systemBubbleBg": "#fff6dd",
    "systemBubbleText": "#8a6200",
    "inputBg": "#fffdf6",
    "inputText": "#1d2b16",
    "inputBorder": "#a9c894",
    "accent": "#4f9e4a",
    "accentText": "#ffffff",
    "border": "#c7dab4",
    "chipBg": "#dcecd0",
    "chipText": "#2f6b2c",
    "chipBorder": "#a9c894",
}

# ─────────────────────────────────────────────── 夜景 · 深林墨绿(树影)
DARK = {
    "bg": "#141c10",
    "bgText": "#e6efdb",
    "sidebarBg": "#1d2816",
    "sidebarText": "#c2d4ae",
    "sidebarHover": "#28371e",
    "sidebarSelected": "#354828",
    "sidebarHeader": "#83966f",
    "editorBg": "#141c10",
    "tabsBg": "#182112",
    "tabBg": "#1d2816",
    "tabText": "#8fa07c",
    "tabActiveBg": "#28371e",
    "tabActiveText": "#e6efdb",
    "aiBg": "#1d2816",
    "aiText": "#e6efdb",
    "aiTabText": "#8fa07c",
    "userBubbleBg": "#3d5a2c",
    "userBubbleText": "#eef5e4",
    "aiBubbleBg": "#22301a",
    "aiBubbleText": "#e6efdb",
    "aiBubbleBorder": "#3a4d2c",
    "systemBubbleBg": "#3a3118",
    "systemBubbleText": "#e8d9a0",
    "inputBg": "#1e2a17",
    "inputText": "#e6efdb",
    "inputBorder": "#3a4d2c",
    "accent": "#78c46c",
    "accentText": "#0c1408",
    "border": "#3a4d2c",
    "chipBg": "#2f4522",
    "chipText": "#cfe4bd",
    "chipBorder": "#597a44",
}

PALETTE_SLOTS = (
    "bg", "bgText", "sidebarBg", "sidebarText", "sidebarHover", "sidebarSelected",
    "sidebarHeader", "editorBg", "tabsBg", "tabBg", "tabText", "tabActiveBg",
    "tabActiveText", "aiBg", "aiText", "aiTabText", "userBubbleBg", "userBubbleText",
    "aiBubbleBg", "aiBubbleText", "aiBubbleBorder", "systemBubbleBg", "systemBubbleText",
    "inputBg", "inputText", "inputBorder", "accent", "accentText", "border",
    "chipBg", "chipText", "chipBorder",
)


def definition(mascot_light=None, mascot_dark=None, source=None):
    """返回完整的 DeepKing SkinDefinition(手工校色版)。"""
    skin = {
        "id": SKIN_ID,
        "name": SKIN_NAME,
        "builtin": False,
        "description": SKIN_DESC,
        "palettes": {"light": dict(LIGHT), "dark": dict(DARK)},
    }
    if source:
        skin["source"] = source
    if mascot_light or mascot_dark:
        skin["mascot"] = {
            "light": mascot_light or mascot_dark,
            "dark": mascot_dark or mascot_light,
        }
    return skin


def validate():
    """自检: 槽位齐全、色值合法、亮暗确实一浅一深、文字对比度够。"""
    from ..engine import _color as col

    problems = []
    for label, pa in (("light", LIGHT), ("dark", DARK)):
        missing = [k for k in PALETTE_SLOTS if k not in pa]
        extra = [k for k in pa if k not in PALETTE_SLOTS]
        if missing:
            problems.append("%s 缺少槽位: %s" % (label, ", ".join(missing)))
        if extra:
            problems.append("%s 多余槽位: %s" % (label, ", ".join(extra)))
        for k, v in pa.items():
            if not col.is_hex(v):
                problems.append("%s.%s 不是合法 # 十六进制: %r" % (label, k, v))
    if not col.is_light_color(LIGHT["bg"]):
        problems.append("light.bg 不是浅色: %s" % LIGHT["bg"])
    if col.is_light_color(DARK["bg"]):
        problems.append("dark.bg 不是深色: %s" % DARK["bg"])
    for label, pa in (("light", LIGHT), ("dark", DARK)):
        for fg, bg in (("bgText", "bg"), ("sidebarText", "sidebarBg"),
                       ("aiBubbleText", "aiBubbleBg"), ("tabText", "tabsBg")):
            lf = sum(col.to_rgb(pa[fg])) / 3.0
            lb = sum(col.to_rgb(pa[bg])) / 3.0
            if abs(lf - lb) < 60:
                problems.append("%s: %s 与 %s 亮度太接近(%d), 文字可能看不清"
                                % (label, fg, bg, abs(lf - lb)))
    return problems
