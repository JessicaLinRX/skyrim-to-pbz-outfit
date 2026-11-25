# Tagged Cook、IoStore 与 AIO 交付

## 冻结、Cook 和封包

1. 保存并冻结当前候选。准备一份自有包白名单，包含最终网格、私有骨架、资产实际用到的贴图及实例、动画、物理、外观表、所用选项表和必要的头部资产。另记游戏与框架提供的外部包、类型及软引用。
2. 简单项目可用开发包的 Build Mod。记录它实际走的 UE 版本、Cook 参数、chunk 和产物位置。已知版本会先重新运行 Write Mod，使用手工编辑的表时须确认最终修改仍在。优先带版本和 Tagged Properties 的 Cook，核对日志和成品后再采用该产物。使用 stock UE 对含游戏扩展属性的资源做 unversioned Cook 会有反射布局不匹配的风险，曾表现为 `Texture2D Serial size mismatch`。
3. Build Mod 的参数或白名单无法控制时，用匹配引擎的 `UnrealEditor-Cmd` 和 `UnrealPak` 独立构建。项目 mount 名与框架保持一致。Cook 根包括最终外观表、选项表和自有资产，逐包确认实际产物并收集 companion 文件。
4. 发布同 stem 的 Mod 容器组。框架开发文件、外部引用的占位资产、地图、临时探针、编辑器 DLL、scratch global 与游戏资源留在制作目录。基础设施文件由游戏和前置依赖提供。

## 自定义构建命令示例

以下使用 PowerShell。先进入冻结工程目录，设置对应引擎的 `Engine/Binaries/Win64` 目录环境变量 `PBZ_TOOLCHAIN_BIN`，再用自己的包清单替换示例 Cook 根。此处的 `<slot>` 代表实际槽号。

```powershell
$cookRoots = @(
    '/Game/Mods/YourOutfit/Meshes/SK_YourOutfit',
    '/Game/Mods/PBZOutfitSlots/DT_OutfitSlot_<slot>',
    '/Game/Mods/PBZOutfitSlots/DT_OptionsSlot_<slot>'
) -join '+'
& (Join-Path $env:PBZ_TOOLCHAIN_BIN 'UnrealEditor-Cmd.exe') '.\ProjectPBZ.uproject' `
    -run=Cook -TargetPlatform=Windows "-Package=$cookRoots" -NoDefaultMaps `
    -NoGameAlwaysCook -NoDev -SkipCookingEditorContent -unattended -stdout
```

根据 Cook 日志找到平台输出和 `ProjectPBZ/Metadata`。为每个发布包生成 response 行，将实际 cooked 文件映射到挂载路径。下面的行假定相对路径基于当前工程目录。

```text
"Saved/Cooked/Windows/ProjectPBZ/Content/Mods/YourOutfit/Meshes/SK_YourOutfit.uasset" "../../../ProjectPBZ/Content/Mods/YourOutfit/Meshes/SK_YourOutfit.uasset" -compress
```

检查 `.ubulk`、`.uptnl` 和 `.uexp` 等 companion 均被正确摄取。已知 UnrealPak 版本自动关联 `.uexp`，重复显式列入可能触发包名推导警告。记录白名单文件及哈希。为 `iostore-commands.txt` 写入一行，按情况使用解析无歧义的绝对路径：

```text
-Output="Build/YourOutfit_P.utoc" -ContainerName=YourOutfit_P -ResponseFile="Build/io-response.txt"
```

为输出和 scratch 目录创建对应文件夹，再调用工具。压缩格式由目标构建验证。示例采用 Oodle/Kraken。

```powershell
$cooked = Join-Path (Get-Location) 'Saved/Cooked/Windows'
$metadata = Join-Path $cooked 'ProjectPBZ/Metadata'
$unrealPak = Join-Path $env:PBZ_TOOLCHAIN_BIN 'UnrealPak.exe'
& $unrealPak -IoStore "-CookedDirectory=$cooked" `
    "-PackageStoreManifest=$(Join-Path $metadata 'packagestore.manifest')" `
    "-ScriptObjects=$(Join-Path $metadata 'scriptobjects.bin')" `
    '-Commands=Build/iostore-commands.txt' '-CreateGlobalContainer=Build/scratch/global.utoc' `
    -TargetPlatform=Windows -compressionformats=Oodle -compressmethod=Kraken -unattended
& $unrealPak 'Build/YourOutfit_P.pak' '-Create=Build/pak-response.txt' -unattended
```

`pak-response.txt` 使用同一「源文件、挂载路径」格式，可包含 Mod 自己的版本信息及实际需要随 PAK 挂载的文件。由工具生成的 `.pak/.utoc/.ucas` 使用同一 stem，确认都可挂载。上例面向单个未分片容器，分片容器需按工具实际输出和目标加载器规则封装。

## 回读实际候选

- 在 FModel 挂载游戏本体、前置运行包与 Mod 容器。确认 Cook 属性可读，贴图实际解码，网格骨架、LOD、UV 槽和物理绑定正确，实例的 Parent 由预期游戏包提供。
- 检查 AppearanceType、普通与过场头部引用、独立 outfit 和 slot、选项结构与表的实际导入。仅挂候选看到外部引用为 null 时，先做带依赖的解析。
- 记录工具版本、构建日志、容器清单、哈希和分层测试结果。对构建产物重新检查启动、换装和关键实机行为。[运行时排查](runtime.md)

## 生成一个可安装 ZIP

按目标安装方式写游戏相对路径。常见 Windows Steam 布局如下，同名容器三件套分别占一条文件记录。

```text
ProjectPBZ/Content/Paks/~mods/YourOutfit_P.pak
ProjectPBZ/Content/Paks/~mods/YourOutfit_P.utoc
ProjectPBZ/Content/Paks/~mods/YourOutfit_P.ucas
platform/steam/ue4ss/Mods/YourOutfitControls/enabled.txt
platform/steam/ue4ss/Mods/YourOutfitControls/Scripts/main.lua
```

后两项只用于需要脚本的项目，按玩家的加载器版本核对实际路径。使用 Python 3.10+ 运行随附 [AIO 打包工具](../scripts/package_aio.py)。将[示例](../assets/aio-manifest.example.json)复制到工程并写入实际文件名、依赖和 SHA256，`source` 相对于清单所在目录解析。带 Lua 时设置 `lua_mod_id` 并添加实际脚本记录。

```text
python scripts/package_aio.py --manifest aio-input.json --output dist/YourOutfit-AIO.zip
```

示例命令假定可从当前目录访问技能的 `scripts`，也可传入该脚本的实际路径。打包工具为上面的常见布局校验源文件哈希、同名非分片容器组及私有 Lua 路径，并在写入后重新校验 ZIP。不同发行渠道、分片容器或管理器格式按各自验证过的布局封装。

发行说明列明游戏与前置版本、管理器导入或手动放置路径、独立外观名称、默认头部、选项及默认值、升级或卸载步骤、文件哈希、已测及待测项目、资产来源和许可。升级先退出游戏，禁用旧版并保留可回退包，核对管理器缓存和手装重复容器。
