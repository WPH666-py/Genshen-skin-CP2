# JetBrains 系 IDE (PyCharm / WebStorm / IntelliJ / GoLand) — 原神CP2 背景图

JetBrains 的背景图是官方 UI 功能, 脚本负责生成高清素材, 之后只需 2 次点击。

## 步骤(可让 AI 自动执行)

1. 生成全部素材:

   ```bash
   genshen-cp2 all --out "%USERPROFILE%\GenshinCP1-Backgrounds"   # Windows
   genshen-cp2 all --out ~/GenshinCP1-Backgrounds                 # macOS / Linux
   ```

   源码形态: `python -m genshen_skin_cp2.engine.cli all --out 目录`

   输出 3 张(同一张素材的三种呈现方式): `single1-*.jpg`(卡片) / `cover1-*.jpg`(满屏) / `showall-*.jpg`(完整不裁)

2. 打开 IDE:
   **Settings / Preferences → Appearance & Behavior → Appearance → Background Image**

3. 点 `+` 添加图片 → 选择刚生成的任意一张。

   - **编辑器区推荐 `single1-*.jpg`**: 卡片居中、四周留白, 代码可读性最好
   - **欢迎页 / 工具窗口推荐 `cover1-*.jpg`**: 满屏插画, 视觉冲击强
   - 想让代码更清晰: 把下方的 **Opacity** 调到 10%~20%

4. 可对 **Editor / Welcome screen / Menus and tool windows** 分别设置不同图片。

## 说明

- 这些图片也通用: 任何支持背景图的 JetBrains IDE、以及 Windows/macOS 桌面壁纸都能直接用。
- 想换壁纸时重复第 3 步选另一张即可。
- 与桌面壁纸互不影响: 桌面用 `genshen-cp2 2`, IDE 背景图单独设。
