---
name: skyrim-to-pbz-outfit
description: 将 Skyrim SE 的服装 Mod 移植到《影之刃零》（Phantom Blade Zero），从 NIF、BodySlide 和 DDS 开始制作可通过 OutfitFramework 独立装备的 PBZ 外观。用于整套移植和移植修复，涵盖蒙皮、头模与颈部适配、材质烘焙、换装选项、Cook 和 AIO 交付。
---

# Skyrim SE 服装移植到《影之刃零》

以选定的原衣和配套身体为外形基准，保留服装轮廓与层间贴合，改用 PBZ 的参考骨架与动画。交付能独立装备的外观、依赖清单和单条目安装包。按需求加入部件显隐、配色、物理和 UUEPBS 兼容。

## 准备输入和环境

确认源 Mod、身体类型及 BodySlide 预设、已生成的 NIF、DDS、目标游戏版本、需要独立控制的部件及默认状态。约定预览和游戏验收由谁负责。已有用户修改的 Blender 文件时，以该版本为候选工作源，先复核蒙皮、接缝与材质槽，再做后续改动。

搭建 FModel/CUE4Parse、带 PyNifly 和 UEFormat 插件的 Blender、与目标游戏及框架匹配的 Unreal Engine、OutfitFramework 开发包和运行包。按需求准备 BodySlide、图像工具、C++ 工具链和 PBZ 兼容 UE4SS。先验证能读取一套游戏主角资产、打开框架工程，再进入制作。[软件与前置](references/setup.md)

先查看源服装与配套身体模型，确认目标角色体型。明确为女性服装的项目需要匹配的女性头模。用户未提供时，说明需要其提供或确认一个可用的女性头模。先继续几何和材质准备，待头模确认后再完成接颈和外观注册。使用用户提供或确认的头模，并核对配套发型、面部及材质依赖。[头部策略与颈部](references/head-and-neck.md)

## 制作与验收

1. **提取与对齐。** 从 FModel 导出目标原生骨架、参考网格和可用动作，从 NIF 导入原衣和同体型身体。整套先统一旋转、缩放和平移，再局部对齐关节。用原身与服装保留轮廓，用 PBZ 参考骨架配准动画。先用主体和一种头部策略完成小样，跨 Blender、FBX、UE 和 Cook 验证单位、骨架、UV 和基本渲染。[提取与工程清单](references/setup.md) · [几何与蒙皮](references/geometry.md)
2. **接颈、蒙皮和物理。** 按实际渲染头部对齐颈口，验证头发、头盔和领饰切换。检查显隐后的皮肤覆盖及肩臂、手腕、髋膝和靴底在动作中的变形。先完成基础蒙皮，有明确需求再加 Copy Pose、私有物理或布料。出现靴底下陷时先定位姿势、尺度与组件变换。[头部与颈部](references/head-and-neck.md) · [几何与蒙皮](references/geometry.md) · [靴底定位](references/runtime.md#靴底定位)
3. **烘焙并展示材质。** 根据 NIF 材质和 DDS 通道校准布料、皮革、金属及皮肤，复用已验证的 PBZ 父材质。烘焙完成后，先展示实际目标材质的全身和关键部件近景，再进入最终材质定版。告知用户，若目标是尽量接近这套服装在 Skyrim 中的实机观感，最好提供该 Mod 的 Skyrim 截图。没有截图也可用源材质、原作者实机图或第一轮 PBZ 实机图继续校准。[烘焙与材质预览](references/materials.md)
4. **注册独立外观。** 使用 OutfitFramework 的空闲 slot、稳定行名和私有资源路径，生成外观表。按请求制作同 slot 的换装选项表，将显隐和配色绑定到实际渲染网格、材质槽及参数。[外观与换装选项](references/outfit-framework.md)
5. **Cook、封包和回读。** 冻结工程与白名单，使用兼容的 Tagged Cook，生成 mod 自有的容器组。在游戏本体、框架运行包和候选包的上下文中解析外观、选项、头部策略、材质和依赖。[Cook 与 AIO](references/build-and-release.md)
6. **按分工实测并交付。** 核对启动、装备、预览和切换动作、领口与头盔、脚底、显隐、配色、存档和适用的过场。涉及 UE4SS 或 UUEPBS 时走对应验证。分别记录编辑器、Cook 回读、脚本回放及游戏结果，注明待实测的功能和候选包哈希。[运行时验证与故障定位](references/runtime.md)

交付版本化 AIO、安装路径或管理器导入说明、运行依赖及版本、外观名和选项入口、默认头部和部件状态，以及实测记录。可选使用 [AIO 打包脚本](scripts/package_aio.py) 与[清单示例](assets/aio-manifest.example.json)。
