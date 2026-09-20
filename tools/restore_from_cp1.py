# -*- coding: utf-8 -*-
"""
把 CP1 的干净引擎文件还原成 CP2 形态, 用于修复被误改的文件。

只还原指定文件, 用 sync_engine.normalize 做与同步完全一致的包名/导入改写,
因此结果与 CP2 原本的引擎逐字节等价(除了我们要修的那些文案)。
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sync_engine as se  # noqa: E402

RESTORE = ["cli.py", "autoinstall.py", "extension.js", "package.json"]

CP1 = se.PACKS["CP1"]
CP2 = se.PACKS["CP2"]


def main():
    for name in RESTORE:
        if name.endswith(".js") or name.endswith(".json"):
            # vscode 侧不参与引擎同步, 直接取 CP1 的对应文件再改写标识
            src = os.path.join(CP1["repo"], "vscode", name)
            dst = os.path.join(CP2["repo"], "vscode", name)
            text = se.read(src)
            text = (text.replace("genshin_skin_cp1", "genshen_skin_cp2")
                        .replace("genshincp1", "genshencp2")
                        .replace("genshin-cp1", "genshen-cp2")
                        .replace("genshin-skin-cp1", "genshen-skin-cp2")
                        .replace("Genshen-Skin-CP1", "Genshen-skin-CP2")
                        .replace("原神CP1", "原神CP2")
                        .replace("米提亚×沃雅妮莎", "奥黛塔×沃雅妮莎")
                        .replace("原神 CP 壁纸套件 1", "原神 CP 壁纸套件 2"))
        else:
            src = os.path.join(CP1["engine"], name)
            dst = os.path.join(CP2["engine"], name)
            text = se.normalize(se.read(src), CP1["slug"], CP2["slug"], "CP2")
        with open(dst, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        print("  restored %-16s <- %s" % (name, os.path.relpath(src, os.path.dirname(HERE))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
