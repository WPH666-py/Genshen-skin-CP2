# -*- coding: utf-8 -*-
"""
原神CP2 · 奥黛塔×沃雅妮莎 —— DeepKing 皮肤(手工校色版)

DeepKing 支持两种接入方式:

  A. 在「设置 → 界面皮肤」粘贴本仓库地址 —— DeepKing 抓 skin.json + CSS 变量,
     按内置规则自动推导 32 槽位调色板。这条路的「亮色」精确取自
     src/client/genshen-cp2.module.css, 「暗色」由其内置算法从亮色派生。

  B. 直接用本文件: 下面两套调色板是**逐槽位手工校色**的结果, 不经过任何推导,
     夜景保留「相依」插画的深海钴蓝, 而不是派生算法给出的中性灰。

安装器(genshen-cp2 deepking)会把本调色板写成 genshen-cp2.skin.json,
并生成可视化预览 genshen-cp2-preview.html, 方便导入前先看效果。
"""
from ..characters import odette_voj as C

SKIN_ID = C.DEEPKING_SKIN_ID
SKIN_NAME = C.DEEPKING_SKIN_NAME
SKIN_DESC = C.DEEPKING_SKIN_DESC

# ─────────────────────────────────────────────── 亮色 · 白日(相依)
LIGHT = {
    "bg": "#ffffff",
    "bgText": "#141c36",
    "sidebarBg": "#e9effc",
    "sidebarText": "#1c2749",
    "sidebarHover": "#dbe5fa",
    "sidebarSelected": "#c2d3f4",
    "sidebarHeader": "#7386ab",
    "editorBg": "#ffffff",
    "tabsBg": "#eef3fd",
    "tabBg": "#e3ecfb",
    "tabText": "#53648c",
    "tabActiveBg": "#ffffff",
    "tabActiveText": "#141c36",
    "aiBg": "#f1f5fd",
    "aiText": "#141c36",
    "aiTabText": "#53648c",
    "userBubbleBg": "#ccdcf7",
    "userBubbleText": "#141c36",
    "aiBubbleBg": "#ffffff",
    "aiBubbleText": "#141c36",
    "aiBubbleBorder": "#becfef",
    "systemBubbleBg": "#fff8e6",
    "systemBubbleText": "#8a6a00",
    "inputBg": "#ffffff",
    "inputText": "#141c36",
    "inputBorder": "#a3bdec",
    "accent": "#3a6fd8",
    "accentText": "#ffffff",
    "border": "#becfef",
    "chipBg": "#d8e4fa",
    "chipText": "#2a4f9e",
    "chipBorder": "#a3bdec",
}

# ─────────────────────────────────────────────── 夜景 · 深海(相依的深色底)
DARK = {
    "bg": "#0f1830",
    "bgText": "#e2e9fa",
    "sidebarBg": "#16213f",
    "sidebarText": "#c0cfeb",
    "sidebarHover": "#1f2d52",
    "sidebarSelected": "#2a3a66",
    "sidebarHeader": "#7688ae",
    "editorBg": "#0f1830",
    "tabsBg": "#131d38",
    "tabBg": "#16213f",
    "tabText": "#8496ba",
    "tabActiveBg": "#1f2d52",
    "tabActiveText": "#e2e9fa",
    "aiBg": "#16213f",
    "aiText": "#e2e9fa",
    "aiTabText": "#8496ba",
    "userBubbleBg": "#27407a",
    "userBubbleText": "#eaf0fc",
    "aiBubbleBg": "#1a2749",
    "aiBubbleText": "#e2e9fa",
    "aiBubbleBorder": "#2c3d6b",
    "systemBubbleBg": "#38301a",
    "systemBubbleText": "#e6d7a2",
    "inputBg": "#182444",
    "inputText": "#e2e9fa",
    "inputBorder": "#2c3d6b",
    "accent": "#5d8ce8",
    "accentText": "#0b1226",
    "border": "#2c3d6b",
    "chipBg": "#243559",
    "chipText": "#cbdcf6",
    "chipBorder": "#42639f",
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
