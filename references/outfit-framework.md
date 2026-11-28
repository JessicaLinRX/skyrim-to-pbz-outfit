# OutfitFramework 外观与换装选项

## 建立独立外观

1. 确认当前开发插件和运行包支持相同的表结构。开发包可查看 `PBZOutfitMod.h/.cpp` 与 `PBZAppearanceStruct.h`，运行侧可用 FModel 检查框架复合表和换装控件。挑选未占用的 slot，检查该值在运行包范围内，也不与常用依赖或已装 Mod 冲突。发布后保持 slot、Mod ID 和行名稳定。已知版本使用 `1000 + slot` 作为 chunk，按实际版本核对。
2. 在开发包的 Outfit Mod 工具内填写 ModName、OutfitName、图标和 BodyMesh，设置头部策略后运行 Write Mod。已知版本的 Body 网格要求有效 Physics Asset、LOD0 开启 Allow CPU Access、`UpperBody` 和 `Mesh` 两个 Sampling Regions，以及游戏骨架或列有游戏骨架的 Compatible Skeletons。按 FModel 导出的原网格配置构建 sampling regions 并保存，核对游戏使用的 sockets 和公共骨。以当前框架的实际检查项为准，处理 Write Mod 返回的错误。
3. 验证 `/Game/Mods/PBZOutfitSlots/DT_OutfitSlot_<slot>` 以及候选的行引用。Body 行的 `BodyMeshAsset` 指向目标网格，Outfit 行通过 `OutfitBodyItem` 引用 Body 行。检查独立名称、解锁状态及图标。所有自建资产归到 `/Game/Mods/<ModId>/...` 或框架指定的自有路径。
4. 项目明确选择原版男主头部时，填写对应的 `GameHairstyle`，回读普通和过场引用。使用开发者提供或确认的自定义头模时，验证普通与过场 Outfit 的 `OutfitHairStyleItem`、`OutfitSequenceHairStyleItem` 对应到私有 Hairstyle 行的 `HeadAsset` 与必要的头发资源，按需绑定 `OutfitBrowLashCardItem`。[头部选择](head-and-neck.md)

一个 Body 网格适合基础外观。确实需要多组件和独立 AnimBP 时，可用 Body 行提供主姿势，另建 Neck 行，将其 `NeckAsset` 指向可见服装网格，并从 Outfit 行通过 `OutfitNeckItem` 引用。在目标游戏里确认生成的真实服装组件和动画来源。用 `ClothMeshAsset` 或 `BodyClothDataArray` 时分别核对它们期待的资产类型与运行时挂载。

## 添加同 slot 的换装选项表

1. 通过开发插件写入 `/Game/Mods/PBZOutfitSlots/DT_OptionsSlot_<slot>`。手工创建时为 DataTable 指定框架提供的 RowStruct。已知版本为 `/PBZModLoader/Options/S_PBZOutfitOption.S_PBZOutfitOption`。可通过编辑器导入 JSON 行，先导出当前结构的示例行确认字段和枚举，再填入目标值。
2. 显隐使用 `Hide` 类型。已知版本包括 `Label`、`OutfitMesh`、`HideSlots`、`HideParts` 和 `DefaultOn`。使用带 Mod 前缀的稳定行名作为保存键。目标使用实际渲染的网格完整 soft object path，槽索引从零开始。勾选代表隐藏，`DefaultOn=true` 初始化为隐藏。独立组件显隐按当前运行蓝图确认 `HideParts` 的匹配方式。
3. 各 LOD 按可见 section、实际槽索引和框架 API 核对显隐范围。有些版本把同一索引同时用于材质 ID 和 section index。合并分区、重导模型或重建 LOD 后重查映射。一组部件可占多个槽，身体及需要保留的靴面应拥有独立槽位。
4. 若当前框架的 `Style` 行能覆盖所需材质参数，优先直接用它验证单参数换色。若一个选项必须同步多件服装或多个材质，可在换装页添加该版本支持的 `Choice` 等选择行，用私有运行逻辑读取选项值，将对应的一组材质资源应用到已验证的组件，保持默认配色和回切行为。[运行时换色与对象生命周期](runtime.md#ue4ss-对象生命周期)

下面是已知版本的最小显隐行示意。以目标 RowStruct 的导出格式为准，槽号 `5` 需替换成候选网格的实际值。

```json
[
  {
    "Name": "YourOutfit_HideCape",
    "Type": "Hide",
    "Label": "隐藏披风",
    "OutfitMesh": "/Game/Mods/YourOutfit/Meshes/SK_YourOutfit.SK_YourOutfit",
    "HideSlots": [5],
    "DefaultOn": false
  }
]
```

## Cook 前后核对

外观表与实际使用的选项表都进入 Cook 和白名单。挂载游戏本体、兼容框架运行包与候选容器，回读正确结构、各行稳定 ID 和引用。确认框架复合表实际导入了该 slot 的外观和选项。已知版本通过 `DT_PBZOutfitOptions.ParentTables` 关联选项表，索引规则须按实际版本查验。

在换装页选中目标外观，逐组验证部件、默认值及各配色实际应用。测试预览、游玩、换出换回、存档重载、过场接管与返场，确认操作不影响其他外观。有实机结果后记录普通和适用过场的支持范围。
