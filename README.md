# 💙 原神 CP 壁纸套件 2 · 奥黛塔 × 沃雅妮莎

**单张素材**壁纸包: 一张同人插画, **三种呈现方式**随时切换 / 可视化切换器 / 桌面桌宠 /
多 IDE 皮肤 / DeepKing 界面皮肤。素材内置于发行包, **离线可用**;
跨平台 Windows / macOS / Linux。

![三种呈现方式](vscode/media/thumb-grid.png)

## ✨ 三种呈现方式

只有一张素材(「相依」: 白发紫瞳的奥黛塔与深蓝长发的沃雅妮莎相偎),
所以可切换的不是"换哪张图", 而是**这张图怎么摆**:

| 模式 id | 名称 | 效果 | 适合 |
|---|---|---|---|
| `single1` | **卡片式**(默认) | 模糊填充背景 + 居中圆角卡片, 构图完整不裁切 | 通用; 图标不被压住 |
| `cover1` | 满屏 | cover 铺满整屏, 无边框 | 想要沉浸感, 无边框 |
| `showall` | 完整 | 等比放进同色纯色底, **一个像素都不裁** | 一点画面都不想丢 |

> 这张素材是 1279×1706 的竖图(比例 0.75)。直接对 16:9 做正中对半裁会把两人的头切掉,
> 因此 `cover1` 会把取景窗上移, 优先保住脸和头发; 而 `showall` 干脆完全不裁, 两侧留同色边。

## 🚀 给 AI 一句话安装

把本仓库链接发给**任意 AI**(DeepKing、Claude Code、Kimi Code、CodeX、Trae、Cursor、
JetBrains AI、DSH Harness 等), 它会读 [`AGENTS.md`](AGENTS.md) 替你装完:

```text
请安装 https://github.com/WPH666-py/Genshen-skin-CP2 的原神CP2壁纸
```

## 🖥️ 手动安装

要求: Python 3.9+。Pillow 缺失时脚本会自动 `pip install`。

```bash
# 方式一: 用仓库里已打包好的 wheel(离线可用)
pip install dist/genshen_skin_cp2-0.1.0-py3-none-any.whl
genshen-cp2-install          # 一键: 生成壁纸 + 设为桌面 + 注册已装 IDE

# 方式二: 源码
git clone https://github.com/WPH666-py/Genshen-skin-CP2.git
cd Genshen-skin-CP2
python -m genshen_skin_cp2.engine.autoinstall
```

Windows 用户也可以直接双击 `install.bat`。

## 🎨 常用命令

```bash
genshen-cp2                # 卡片式(默认)
genshen-cp2 cover          # 满屏, 无边框
genshen-cp2 showall        # 完整不裁, 两侧留边
genshen-cp2 card           # 显式指定卡片式
genshen-cp2 random         # 随机一种呈现方式
genshen-cp2 list           # 列出全部模式
genshen-cp2 switcher       # 可视化切换器(预览 + 一键应用 + 自动随机)
genshen-cp2 pet            # 桌面桌宠(拖动 / 右键菜单 / Esc 退出)
genshen-cp2 cycle 30       # 每 30 分钟自动随机换
genshen-cp2 all --out DIR  # 一次生成三种到指定目录
genshen-cp2 deepking       # 生成 DeepKing 界面皮肤 + 离线预览
genshen-cp2 info           # 环境与素材自检
```

常用选项: `--size 2560x1440` 指定分辨率(默认取屏幕分辨率)、`--no-set` 只生成不设置。

## 🧩 IDE / 桌宠支持

| 环境 | 接入方式 |
|---|---|
| **VSCode / Trae / CodeX / Cursor / Windsurf** | 活动栏「原神CP2」→ 皮肤画廊三张卡片一键换; 命令面板搜 `原神CP2` |
| **DeepKing** | 设置 → 界面皮肤 → 粘贴本仓库地址, 自动生成星蓝配色皮肤 |
| **PyCharm / WebStorm / IntelliJ** | Settings → Appearance & Behavior → Appearance → **Background Image** |
| **Claude Code / Kimi Code / Harness 等** | 注册 MCP 服务器, AI 直接调 `set_wallpaper` / `next_wallpaper` |
| **桌面桌宠** | `genshen-cp2 pet` —— 透明置顶圆形立绘, 可拖动、右键菜单 |

一键注册全部已装 IDE:

```bash
genshen-cp2-install --only vscode jetbrains mcp deepking
```

## 📁 目录

```
src/genshen_skin_cp2/
  characters/odette_voj.py   角色与素材定义(换角色只改这一个文件)
  engine/                    皮肤引擎: 合成 / 壁纸设置 / CLI / 桌宠 / 切换器 /
                             MCP 服务器 / DeepKing 适配 / 自动安装
  deepking_skin.py           手工校色的 DeepKing 调色板(32 槽位)
src/client/                  DeepKing 配色变量 + 维护说明
assets/background/           DeepKing 编辑区水印(同一张素材的两段取景)
vscode/                      VSCode/Trae/CodeX 扩展(含打包好的 .vsix)
ide/jetbrains/               JetBrains 背景图指引
tools/                       维护脚本(推送 / 引擎同步 / 线上契约校验)
AGENTS.md                    给 AI 的自动安装指引
```

## ❓ 常见问题

- **想换别的图 / 加第二张**: 现在只有一张素材。加图只需把新图放进
  `src/genshen_skin_cp2/engine/assets/`, 在 `characters/odette_voj.py` 的
  `IMAGE_FILES` 追加文件名、`IMAGE_META` 补一条说明 —— 模式列表会自动跟着变。
- **壁纸尺寸**: 默认取主屏分辨率; 多显示器建议加 `--size 2560x1440` 并在系统设置里把壁纸设为「平铺/跨屏」。
- **命令找不到**: Scripts 目录不在 PATH, 改用 `python -m genshen_skin_cp2.engine.cli`。
- **桌宠不透明**: 个别 Linux 桌面不支持透明色键, 会退化为白底卡片, 功能不受影响。
- **切换器/桌宠没反应**: 两者需要本地图形桌面, 远程 SSH 会话下无法显示。
- **改了素材不生效**: 不会 —— 素材或代码更新后会自动重新合成(热更新), 无需清缓存。

## 🔗 与其它套件的关系

与 **CP1**(`Genshen-Skin-CP1` · 米提亚 × 沃雅妮莎)以及 WPH666-py 的其它皮肤套件
**完全独立**: 包名 `genshen-skin-cp2`、命令前缀 `genshen-cp2`、运行时目录 `~/.genshen-cp2`、
vscode 扩展 ID `wp666.genshen-skin-cp2`、DeepKing 皮肤 id `genshen-cp2-odette-voyanisa`
互不冲突, 可同时安装、各自切换。

两个套件共用同一套引擎, 用 `tools/sync_engine.py` 保持同步:

```bash
python tools/sync_engine.py --check      # 报告两边差异(应输出「没有漂移」)
python tools/sync_engine.py --to CP1     # 把本仓库的引擎改进同步到 CP1
```

## 🙏 素材说明

1 张奥黛塔 × 沃雅妮莎同人插画。**仅用于个人桌面美化, 请勿二次商用。** 版权归原作者所有。

## 📄 许可

代码以 MIT 许可发布(见 [LICENSE](LICENSE)); 插画素材不在 MIT 授权范围内。
