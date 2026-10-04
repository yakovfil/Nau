# Validation

Validated on 2026-10-04 against the uncommitted implementation working tree. Base revisions: parent `02e62e3ce626009ecf2676f63787013e198fcb83`, NauEngineModules `4170b4b553ccf60906a24b86980245c0d2ef76c1`, NauEngineLite `c4952d9f2ee2836ccd9941e82be743c6191aa987`. Toolchain: CMake 4.2.1, Visual Studio 18 2026/v145 x64 (MSVC 19.51), Emscripten 6.0.9 with its bundled Node runtime. Implementation file identities are recorded in working-tree-identities.json.

## Native ownership, state, and source consumer

From the parent checkout:

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/nau-widget-native -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_ENGINE=D:/Programming/github/Nau/NauEngineLite -DNAU_WIDGET_TESTS=ON -DCMAKE_INSTALL_PREFIX=D:/Programming/github/Nau/NauEngineModules/build/nau-widget-sdk-stage
cmake --build NauEngineModules/build/nau-widget-native --config Debug --target test_widget NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-native -C Debug --output-on-failure
cmake --build NauEngineModules/build/nau-widget-native --config Release --target test_widget NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-native -C Release --output-on-failure
```

Debug: **9/9 passed**. Release: **9/9 passed**. Each configuration runs seven WidgetTests, the owned-base-destruction death test, and the source consumer.

Coverage includes generated non-null distinct UID, base RTTI, deleted default/copy/move construction, borrowed const access, child ordering, empty/self/ancestor rejection without ownership loss, middle-child removal, non-child removal, retained subtree identity/state, descendant lifetime, weak invalidation before concrete destruction, surviving detached references, effective visibility, and concrete allocator deallocation exactly once. A counting allocator validates real aligned allocation addresses and deallocations for both concrete test subclasses and factory-created NauWidget instances. No application/scene manager, window, GPU, or service startup occurs.

The already-parented guard remains in the implementation. No test manufactures duplicate ownership of an attached child, which would violate the pointer contract before exercising that guard.

## Relocated installed SDK

Installed both native configurations after the final all-build destruction change:

```powershell
cmake --install NauEngineModules/build/nau-widget-native --config Debug
cmake --install NauEngineModules/build/nau-widget-native --config Release
```

Moved the entire owned `NauEngineModules/build/nau-widget-sdk-stage` prefix to `NauEngineModules/build/nau-widget-sdk-relocated` after verifying both absolute paths belong to the component build directory. The original stage prefix no longer exists. The fresh relocated SDK has **447 files**, including the renamed public header, Debug/Release libraries, and scene/assets/kernel dependency exports. It has no old widget.h, Cocos/ui_manager artifacts, or GoogleTest installation.

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/nau-widget-sdk-consumer -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_SDK=D:/Programming/github/Nau/NauEngineModules/build/nau-widget-sdk-relocated
cmake --build NauEngineModules/build/nau-widget-sdk-consumer --config Debug --target NauWidgetConsumer
ctest --test-dir NauEngineModules/build/nau-widget-sdk-consumer -C Debug --output-on-failure
cmake --build NauEngineModules/build/nau-widget-sdk-consumer --config Release --target NauWidgetConsumer
ctest --test-dir NauEngineModules/build/nau-widget-sdk-consumer -C Release --output-on-failure
```

Debug: **1/1 passed**. Release: **1/1 passed**. Consumer checks factory UID/RTTI, attachment, visibility, detachment, retained weak references, and owner-release invalidation. File API evidence confirms consumer include paths are entirely within the relocated SDK and link inputs include CoreScene/CoreAssets without source-checkout or former-install library paths.

## Emscripten

```powershell
. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/nau-widget-web -G Ninja -DCMAKE_BUILD_TYPE=Release -DNAU_BUILD_BROWSER=ON -DCMAKE_TOOLCHAIN_FILE=C:/Users/Yakov/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake -DNAU_WIDGET_ENGINE=D:/Programming/github/Nau/NauEngineLite
cmake --build NauEngineModules/build/nau-widget-web --target NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-web --output-on-failure
```

Compiled and linked JS/Wasm; headless Node consumer **1/1 passed** after the final implementation change. The consumer executes the same UID/RTTI/ownership/weak-reference smoke checks as native. Existing kernel/header compiler warnings remain; this is not a warning-free build claim. No visual browser test is required for this non-rendering feature.

## Default selections and dependency audit

Configured these existing selections into new ignored build directories with File API codemodel queries:

```powershell
cmake -S NauEngineLite -B NauEngineModules/build/nau-widget-default-standalone -G "Visual Studio 18 2026" -A x64 -DNAU_RUNTIME_PROFILE=minimal
cmake -S NauEngineLite -B NauEngineModules/build/nau-widget-default-minimal -G "Visual Studio 18 2026" -A x64 -DNAU_RUNTIME_PROFILE=minimal -DCMAKE_PROJECT_NauEngine_INCLUDE=D:/Programming/github/Nau/NauEngineModules/cmake/attach_modules.cmake
cmake -S NauDemo/tests/demo_scene -B NauEngineModules/build/nau-widget-default-scene -G "Visual Studio 18 2026" -A x64
```

Standalone minimal kernel: 17 targets; modules minimal: 19; existing scene fixture: 32. Each excludes NauUi in all four generated configurations. These are configuration/dependency checks, not claims that the entire default graphs were rebuilt or their unrelated suites rerun.

The explicit widget source fixture is independent of NauDemo and selects only assets, scene, and ui with framework disabled. Native has 28 targets including focused test support; Emscripten has 37 including CTest support. Compiled NauUi dependency closure is CoreScene, CoreAssets, NauKernel, fmt, jsoncpp, vectormath, fast_float, and NauUi (plus VS ZERO_CHECK). Header-only interface dependencies are imported separately by the SDK consumer. No graphics/input/window/rendering, Cocos, Qt, USD, or DirectX target/include dependency appears in the focused closure. Native system/runtime libraries remain normal platform toolchain inputs.

The ignored audit script `NauEngineModules/build/widget-evidence/nau-widget-audit.py` follows generated target dependencies, checks focused include paths, checks relocated consumer library/include paths, checks default target selections, and checks SDK artifacts. Its successful result is `nau-widget-graph-audit.json` in that directory. Build, configure, install, and CTest logs use the `nau-widget-` prefix in the same ignored evidence directory.

## Corrected attempts and approved design correction

- Initial Debug death test expected stderr text, but the engine fatal path emitted none. The corrected test creates a valid owned widget before the death expression and asserts process death without a stderr requirement.
- Release then revealed the planned inherited guard was compiled out with NAU_FATAL. The user explicitly approved enforcing rejection in NauWidget itself. The private final override now aborts unconditionally; native Debug and Release death tests both pass. Design and delta requirements describe the approved behavior. Qualified calls bypassing virtual dispatch remain unsupported; NauObject itself is unchanged.
- Initial SDK installation encountered an unbuilt gtest_main install target. The focused fixture disables bundled GoogleTest installation. A fresh stage prefix was installed and relocated successfully; the earlier partial ignored prefix is not the SDK used for validation.

## Final checks and scope

Engine clang-format dry run with --Werror, component/root git diff --check, and `openspec validate rework-widget-as-nau-object --strict` pass. Repository searches find no live old type/header/source API usages outside the migration explanation and historical specs. Changes are confined to the UI module and this OpenSpec change. Existing unrelated NauEngineLite/GoogleTest and NauSamples working-tree changes are preserved.

All required validation is complete, with no skipped acceptance checks. Save/load, reflected persistence fields, SceneQuery widget resolution, scene attachment, layout, input, rendering, and production subclasses remain deferred as agreed. No commit, push, spec sync, or archive was performed by this apply operation.
