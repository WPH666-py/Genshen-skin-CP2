# AGENTS.md — 原神 CP 壁纸套件2 · AI 自动安装指引(AI 助手必读)

> **给 AI 的话**: 当用户把本仓库地址发给你, 并说「安装原神CP2壁纸 / 原神CP2 / 奥黛塔沃雅妮莎壁纸 /
> 换个壁纸」时, **你就是安装器**。请直接替用户执行下面的步骤, 不要让用户自己敲命令。
> 所有命令都是幂等的, 重复执行安全。

## 这套东西是什么

**原神 CP 壁纸套件 2 · 奥黛塔 × 沃雅妮莎** —— **单张素材**壁纸包。

只有一张插画(「相依」: 白发紫瞳的奥黛塔与深蓝长发的沃雅妮莎相偎), 但提供**三种呈现方式**,
用户随时切换:

| 模式 id | 名称 | 说明 |
|---|---|---|
| `single1` | 卡片式 | **默认**。模糊填充背景 + 居中圆角卡片, 构图完整不裁切 |
| `cover1` | 满屏 | cover 铺满整屏, 无边框; 取景窗自动上移保住两人的脸 |
| `showall` | 完整 | 等比放进同色纯色底, **一个像素都不裁**, 两侧留边 |

素材已打进发行包, **离线可用**。跨平台 Windows / macOS / Linux。

> 用户如果说「换张别的」—— 本套件只有这一张素材, 请告诉他可以切换**呈现方式**
> (`genshen-cp2 cover` / `genshen-cp2 showall`), 而不是去找不存在的第二张图。

## 第 0 步: 选安装形态(优先 A)

```bash
# A. 用仓库里已打包的 wheel(不需要联网装依赖)
pip install "https://github.com/WPH666-py/Genshen-skin-CP2/raw/main/dist/genshen_skin_cp2-0.1.0-py3-none-any.whl"

# B. 源码
git clone https://github.com/WPH666-py/Genshen-skin-CP2.git "$HOME/Genshen-skin-CP2"
cd "$HOME/Genshen-skin-CP2"
```

验证: `genshen-cp2 info` 应打印素材路径与屏幕分辨率。
**若该命令不存在**, 说明 Scripts 目录不在 PATH, 改用 `python -m genshen_skin_cp2.engine.cli info`。

## 第 1 步: 识别用户环境

- 有 Python 3.9+ (`python --version` 或 `py -3 --version`) → 继续。
- 没有 Python → 先装:
  - Windows: `winget install Python.Python.3.11`
  - macOS: `brew install python`
  - Ubuntu/Debian: `sudo apt install -y python3 python3-pil`
- **Pillow 不用手动装**, 脚本检测到缺失会自动 `pip install pillow`。

## 第 2 步: 一键安装(所有平台)

```bash
genshen-cp2-install
```

依次完成: 装依赖 → 生成默认壁纸(按屏幕分辨率) → 设为系统桌面壁纸 →
自动注册已装 IDE(VSCode 系扩展 + JetBrains 背景图素材 + MCP 服务器 + DeepKing 皮肤)。

可选参数:

- `--no-wallpaper` 只做 IDE 注册, 不动桌面
- `--no-ide` 只换壁纸
- `--size 2560x1440` 指定分辨率
- `--only vscode jetbrains mcp deepking` 只处理指定目标

源码形态等价命令: `python -m genshen_skin_cp2.engine.autoinstall`

## 第 3 步: 按用户环境补做

### A. 换壁纸 / 换呈现方式(用户在聊天里说"换一张")

```bash
genshen-cp2            # 卡片式(默认)
genshen-cp2 cover      # 满屏, 无边框
genshen-cp2 showall    # 完整不裁, 两侧留边
genshen-cp2 card       # 显式指定卡片式
genshen-cp2 random     # 随机一种呈现方式
genshen-cp2 list       # 列出全部模式
genshen-cp2 all        # 一次生成三种到 ~/.genshen-cp2/wallpapers
```

### B. VSCode / Trae / CodeX / Cursor / Windsurf

```bash
genshen-cp2-install --only vscode
```

手动等价:
`code --install-extension <仓库>/vscode/genshen-skin-cp2-0.1.0.vsix`

无网时: 把 `vscode/` 整个目录复制到
`%USERPROFILE%\.vscode\extensions\wp666.genshen-skin-cp2-0.1.0\`, 然后重启编辑器。

装完提示用户: 活动栏 **原神CP2** 图标 → 皮肤画廊 → 三张卡片分别对应三种呈现方式,
点「设为壁纸」即可。命令面板搜 `原神CP2` 也能换 / 开切换器 / 开桌宠。

### C. PyCharm / WebStorm / IntelliJ

```bash
genshen-cp2 all --out "$HOME/GenshenCP2-Backgrounds"
```

生成 3 张(卡片式 / 满屏 / 完整)。再引导用户:
Settings → Appearance & Behavior → Appearance → **Background Image**
→ 点 `+` 选图片(编辑器区推荐 `single1-*.jpg`, 留白多、代码可读性好)。
细节见 [ide/jetbrains/README.md](ide/jetbrains/README.md)。

### D. DeepKing 界面皮肤(深度适配)

DeepKing 自带「界面皮肤」系统, 本仓库已按它的转换契约改造:

```bash
genshen-cp2 deepking           # 生成皮肤 JSON + 离线预览, 并打印接入步骤
genshen-cp2 deepking --check   # 校验仓库是否满足 DeepKing 转换契约
genshen-cp2 deepking --what    # 显示 DeepKing 会从仓库里提取到什么
```

给用户的两句话:

1. 打开 DeepKing → **设置 → 界面皮肤 / UI Skin**;
2. 粘贴 `https://github.com/WPH666-py/Genshen-skin-CP2` → 生成自定义皮肤。

也可离线接入(夜景保留素材的深海钴蓝, 不经过 DeepKing 的派生算法):
用 `genshen-cp2 deepking` 生成的 `~/.genshen-cp2/deepking/genshen-cp2.skin.json`,
先双击同目录的 `genshen-cp2-preview.html` 看效果。

**维护者注意**(改了皮肤文件务必重跑 `--check`):

| 文件 | 作用 |
|---|---|
| `skin.json` | DeepKing 读取 `name` / `accent` / `tagline`; `accent` 必须是 `#` 十六进制 |
| `src/client/genshen-cp2.module.css` | 配色变量 `--名: #hex`; 变量名需含 `bg-base`、`label-primary`、`brand-primary`、`border-l2` 等关键词 |
| `assets/background/mascot-cp2-light.jpg` / `-dark.jpg` | 编辑区右下角水印, 由同一张素材的两段取景生成 |

**两个容易踩的坑**(`--check` 会报出来):

- 色值必须是 `#` 开头的十六进制, `rgb()` / `hsl()` / 颜色名一律被忽略。
- **不要在暗色作用域里重复声明同名变量**。DeepKing 的 `extractVars()` 是无作用域
  全文扫描、后者覆盖前者, 于是暗色值会把**亮色调色板也刷成深色**, 两套都变深色。
  本仓库的做法: 亮色用 `:root` 的规范变量名, 暗色用不与关键词冲突的 `--duskcolor-*`
  前缀且选择器不含 `dark` 字样, 让 DeepKing 按内置规则从亮色派生暗色。

### E. Claude Code / Kimi Code / Harness 等(聊天窗口形态)

这些环境支持 MCP。注册后 AI 可以**直接调工具换壁纸**:

```bash
genshen-cp2-install --only mcp
```

等价 MCP 配置(写入配置文件的 `mcpServers`):

```json
{
  "mcpServers": {
    "genshen-cp2": {
      "command": "python",
      "args": ["-m", "genshen_skin_cp2.engine.mcp_server"]
    }
  }
}
```

MCP 暴露 5 个工具: `list_wallpapers` / `set_wallpaper` / `next_wallpaper` /
`generate_all` / `wallpaper_info`。用户说"换壁纸"时调用 `next_wallpaper` 即可。

### F. 桌面桌宠 / 可视化切换器(需要图形桌面)

```bash
genshen-cp2 switcher    # 可视化切换器: 左侧预览三种呈现方式, 右侧一键应用
genshen-cp2 pet         # 桌面桌宠: 左键拖动, 右键菜单, Esc 退出
genshen-cp2 cycle 30    # 每 30 分钟自动随机换
```

**注意**: 这三条需要本地图形会话。若你在远程/无桌面环境执行失败, 告诉用户在自己电脑上运行,
**不要说"安装失败"**。

## 约定与失败处理

- 只依赖 Pillow, 其余全部标准库; 素材已打进 wheel, 不联网也能用。
- 生成物放在 `~/.genshen-cp2/`(Windows: `C:\Users\<你>\.genshen-cp2`), **不会**改动仓库文件。
- 素材或代码更新后自动重新合成(热更新), 不需手动删缓存。
- Windows 控制台报 GBK/Unicode 错 → `chcp 65001` 后重跑(脚本已内置 UTF-8 兜底)。
- 装了 Microsoft Store 版 Python 找不到命令 → 用完整路径, 如
  `C:\Users\<user>\AppData\Local\Programs\Python\Python311\python.exe -m genshen_skin_cp2.engine.cli`
- 高分屏生成慢 → 加 `--size 1920x1080` 降一档。
- 桌宠在个别 Linux 桌面不支持透明色键 → 退化为白底卡片, 功能不受影响, 告知用户即可。
- **与 CP1 可共存**: CP1(`Genshen-Skin-CP1` · 米提亚×沃雅妮莎)与本套件的包名、命令前缀、
  运行时目录、vscode 扩展 ID、DeepKing 皮肤 id 全部独立, 同时安装不会互相覆盖。

## 一键复述(可直接念给用户)

> 已为你装好「原神 CP 壁纸套件2 · 奥黛塔 × 沃雅妮莎」。
> 这张图有三种摆法: `genshen-cp2`(卡片式)、`genshen-cp2 cover`(满屏)、
> `genshen-cp2 showall`(完整不裁);
> 可视化切换器: `genshen-cp2 switcher`; 桌宠: `genshen-cp2 pet`;
> DeepKing 皮肤: 设置 → 界面皮肤 → 粘贴 `https://github.com/WPH666-py/Genshen-skin-CP2`;
> VSCode 活动栏的「原神CP2」图标里也能一键换。
