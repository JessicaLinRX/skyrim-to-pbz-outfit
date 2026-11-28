# 软件、前置与源资产

## 制作端

| 工具 | 用途与启用条件 |
|---|---|
| Windows 版《影之刃零》 | 提供目标游戏包、原生骨架、动画、材质和实机环境。记下发行渠道、游戏 build 和框架支持范围。 |
| FModel（CUE4Parse） | 必需的资源读取环节可由 FModel 或兼容的 CUE4Parse 工具完成。挂载 PAK/IoStore，核对游戏资产与成品引用。FModel MCP 可选。 |
| Blender + PyNifly + UEFormat | 推荐 DCC 组合。PyNifly 导入 Skyrim SE NIF，UEFormat 导入 PBZ 参考网格、骨架与受支持的动画。Blender 负责对位、蒙皮、UV、烘焙和 FBX 导出。 |
| Unreal Engine Editor、UnrealEditor-Cmd、UnrealPak | 制作 SkeletalMesh、Material Instance、AnimBP 和表，执行 Windows Cook 及 IoStore 构建。先从框架工程的 EngineAssociation、发布说明和目标游戏数据确认兼容的 UE 版本。 |
| OutfitFramework 开发包 | 下载 For Modders Only 或当前发布页对应的开发包。用随包 UE 工程和插件生成独立外观与换装选项。若需要编译开发模块或自写编辑器 helper，按对应 UE 版本安装 Visual Studio C++ 工具链及 Windows SDK。 |
| BodySlide / Outfit Studio | 需要从预设生成体型、服装和完整原身，或源包只有滑块工程时使用。用户已有匹配的 NIF 成品时可直接导入。NifSkope 可辅助核查 NIF 形状、着色器标志、贴图槽与 alpha。 |
| Blender 烘焙、GIMP 或兼容 DDS 的图像工具 | 至少准备一条能正确读取 DDS、拆通道及写出 UE 可导入贴图的路径。Python 3.10+ 只在使用随附 AIO 打包器时需要。 |

若要自行取得 Skyrim 实机参考，需要运行 Skyrim SE 及源 Mod 实际要求的插件、体型与渲染配置。已有可用 NIF/DDS 和视觉参考时，可从这些输入开始。

工具发布渠道见 [FModel](https://github.com/4sval/FModel) · [Blender](https://www.blender.org/download/) · [PyNifly](https://github.com/BadDogSkyrim/PyNifly) · [UEFormat](https://github.com/h4lfheart/UEFormat) · [BodySlide / Outfit Studio](https://github.com/ousnius/BodySlide-and-Outfit-Studio) · [Unreal Engine](https://www.unrealengine.com/download) · [PBZ Outfit Framework](https://www.nexusmods.com/phantombladezero/mods/903)

## 游玩和测试端

| 前置 | 何时需要 |
|---|---|
| OutfitFramework 运行包 | 本流程的独立外观与原生换装选项依赖此包。安装与开发包兼容的运行版，并按该版本发布页安装它所列的加载器、菜单或其他必需前置。核对游戏能正常启动且能打开换装界面。 |
| PBZ 兼容 UE4SS | 使用 Lua 换色、脚底补偿、运行时姿势桥接等扩展时必需。若框架或加载器版本也要求 UE4SS，按其说明安装。核对游戏版本和实际脚本 API。 |
| UUEPBS for PBZ | 可选体型滑块兼容。只在项目支持且玩家启用该功能时安装。 |
| 头模或其他资源 Mod | 仅在成品保留指向该 Mod 的运行时引用时列为依赖。明确选用的游戏原生头部由 PBZ 本体提供。 |
| Mod 管理器 | 可选。若使用，先验证目标版本可以导入候选 ZIP；否则使用经验证的游戏相对路径手动安装。 |

运行依赖的发布渠道见 [OutfitFramework](https://www.nexusmods.com/phantombladezero/mods/903) · [PBZ 兼容 UE4SS 发行包](https://github.com/KintaroModding/ue4ss/releases) · [UUEPBS for PBZ](https://www.nexusmods.com/phantombladezero/mods/622)

## 从空白工程开始

1. **建立制作工程。** 解压框架开发包，以随包 `ProjectPBZ.uproject` 或当前框架开发模板为起点。有的模板使用 UE 5.7 工程关联，最终仍以开发包及目标游戏的兼容版本为准。必要时生成工程文件并构建 Editor Target。打开编辑器验证 OutfitFramework 插件、外观制作面板及共享选项结构能加载。给服装选一个私有资产前缀，如 `/Game/Mods/YourOutfit`。
2. **设置 FModel。** 选择目标游戏安装目录和当前兼容的 PBZ/UE profile。按实际包所需配置同 build 的 usmap、Oodle 和开发者可合法使用的 AES 密钥。先打开一项游戏本体的骨架或纹理并确认能解码。挂载失败时分别查 archive、密钥、压缩库、版本和 mappings。将密钥及本机工具配置留在本地。[PBZ usmap 来源](https://github.com/KintaroModding/phantombladezero_pbzusmap)
3. **提取 PBZ 参考。** 查找目标男主当前外观的 Body、Hairstyle、适用的过场变体及相关 Mesh；记录骨名、父级、参考变换、sockets、材质槽、PhysicsAsset、采样区、AnimBP 和后处理引用。导出用于对位的网格和骨架为 UEFormat，另存属性与材质参数。用工具实际支持的格式导出动作，并检查导入 Blender 后的单位、参考姿势及关键帧。
4. **整理 Skyrim 输入。** 保留原始 NIF、DDS、BodySlide 工程与预设的只读副本，在制作副本上操作。BodySlide 中选匹配服装的体型族、预设及输出目录，用同一预设生成服装和补全用的躯干、手脚。若源 Mod 以插件分配模型，可查其 Armor Addon 记录定位实际 NIF。逐形状记录贴图路径、材质标志、可见部件和缺失皮肤。比较 `_0` 与 `_1` 后再选用端点；命名相似的去底衣版本也需逐部件核对几何。

## 建议维护一份项目清单

分开放置只读源、Blender 候选、UE 工程、冻结与 Cook 输出、报告和发行包。清单记录以下内容，便于用户改模后复核和升级。

- Blender、UE、游戏、FModel profile、usmap 和框架版本，原始 NIF/DDS 与候选资产哈希。
- 身体族、预设、头部策略、部件分组、骨架和物理来源。每个组件的网格、父骨空间、后处理、材质槽及 LOD。
- Mod ID、Outfit 行名、slot、资产前缀、外部引用、发布白名单、ZIP 哈希及各层测试结果。

`/Game/...` 映射到工程 Content，插件虚拟根映射到相应插件 Content。若编辑器需以同路径占位来建立对游戏资源的引用，记录其类型及最终提供方，确保占位资产留在制作工程。
