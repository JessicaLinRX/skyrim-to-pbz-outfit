# Skyrim SE Outfit Porting for Phantom Blade Zero

这份技能面向第一次把 Skyrim SE 服装移植到《影之刃零》（PBZ）的开发者。以一套可在 PBZ 换装界面独立选择的服装为目标，涵盖资源提取、Blender 蒙皮、UE 材质与 Cook、OutfitFramework 注册、IoStore 打包和实机验收。

- **开发者**可以从 [SKILL.md](SKILL.md) 按顺序执行。先查[软件与前置](references/setup.md)，确认游戏版本、资源读取工具、DCC 和 OutfitFramework 开发包与运行包。
- **Codex 用户**可以将整个 `skyrim-to-pbz-outfit` 目录放入技能搜索目录，然后调用 `$skyrim-to-pbz-outfit`。例如「用此技能移植这套 Skyrim SE 服装。按 BodySlide 预设生成原衣原身，沿用 PBZ 原版男主头模，材质烘焙后先给我看预览。」

仓库内容包括流程、示例清单和 AIO 打包工具。制作时请从各作者的发布渠道获取游戏、框架及插件，发布移植 Mod 前核对源服装、头模、纹理和其他第三方资产的跨游戏使用与再分发条件。
