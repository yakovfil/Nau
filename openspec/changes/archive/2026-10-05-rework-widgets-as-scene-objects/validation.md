# Validation evidence

Validated on Windows on 2026-10-05. Change: `rework-widgets-as-scene-objects`.

## Results

| Check | Result |
| --- | --- |
| Native Debug focused CTest | 16/16 passed |
| Native Release focused CTest | 16/16 passed |
| Emscripten Release scene-stream consumer under Node | 1/1 passed |
| Relocated SDK Debug consumer | 1/1 passed |
| Relocated SDK Release consumer | 1/1 passed |
| clang-format dry-run with engine configuration | All 15 affected C++ headers/sources passed |
| Component and root `git diff --check` | Passed |
| Strict OpenSpec validation | Passed |

Native coverage comprises 14 widget regressions, one scene-only regression executable with no NauUi linkage, and the public scene-stream consumer. Coverage includes exact-root construction/callback ordering; RTTI, owner conversion and allocator lifetime; mixed hierarchy/visibility; reparent options; scene transform parity; weak references; active async attachment and delayed deactivation; atomic property validation; scene/prefab streams; identity/reference remapping; missing UI re-save/recovery; omitted fields and invalid scene properties.

The approved optional `IComponentPropertyValidator` runs before property assignment. Rejection logs the existing diagnostic and skips properties while continuing normal UID/transform restoration. Widget validation rejects explicit null state as well as malformed types and geometry. The existing writer omits null dictionary fields, so the explicit-null regression passes the malformed asset record directly to the scene factory; other malformed/default-field cases use actual scene streams. Generic RuntimeValue assignment remains unchanged.

## Commands and fixtures

All paths below are relative to `D:/Programming/github/Nau` unless absolute.

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/nau-widget-native -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_ENGINE=D:/Programming/github/Nau/NauEngineLite -DNAU_WIDGET_TESTS=ON -DCMAKE_INSTALL_PREFIX=D:/Programming/github/Nau/NauEngineModules/build/scene-widget-sdk-stage
cmake --build NauEngineModules/build/nau-widget-native --config Debug --target test_widget test_scene_factory_extension NauWidgetConsumer
ctest --test-dir NauEngineModules/build/nau-widget-native -C Debug --output-on-failure
cmake --build NauEngineModules/build/nau-widget-native --config Release --target test_widget test_scene_factory_extension NauWidgetConsumer
ctest --test-dir NauEngineModules/build/nau-widget-native -C Release --output-on-failure

. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake --build NauEngineModules/build/nau-widget-web --target NauWidgetConsumer
ctest --test-dir NauEngineModules/build/nau-widget-web --output-on-failure

cmake --install NauEngineModules/build/nau-widget-native --config Debug
cmake --install NauEngineModules/build/nau-widget-native --config Release
# After verifying both absolute paths are inside NauEngineModules/build:
Move-Item -LiteralPath D:/Programming/github/Nau/NauEngineModules/build/scene-widget-sdk-stage -Destination D:/Programming/github/Nau/NauEngineModules/build/scene-widget-sdk-relocated
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/scene-widget-sdk-consumer -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_SDK=D:/Programming/github/Nau/NauEngineModules/build/scene-widget-sdk-relocated
cmake --build NauEngineModules/build/scene-widget-sdk-consumer --config Debug
ctest --test-dir NauEngineModules/build/scene-widget-sdk-consumer -C Debug --output-on-failure
cmake --build NauEngineModules/build/scene-widget-sdk-consumer --config Release
ctest --test-dir NauEngineModules/build/scene-widget-sdk-consumer -C Release --output-on-failure

openspec validate rework-widgets-as-scene-objects --strict
```

The native and web source build trees were existing focused fixture configurations, regenerated for this change. Native uses CMake 4.2.1, Visual Studio 18 2026/v145, MSVC 19.51 and Windows SDK 10.0.26100.0. Web uses Emscripten 6.0.9 and Node 24.19.0. The web consumer enables memory growth for scene services and persistence. A Release fixture issue was repaired by moving stream-writing work out of a disabled assertion macro.

The SDK was installed into a newly configured staging prefix, then physically moved; the staging path no longer exists. It contains 457 files. Generated consumer project include/library entries point to the relocated SDK for every engine/module/bundled dependency, with ordinary compiler/system libraries unchanged. Both configurations exercise public widget creation, actual scene-stream persistence and cloning.

## Dependency and working-tree audit

CoreScene links CoreAssets and has no NauUi reference. The UI-neutral construction/validation interfaces contain no widget types. The separate scene-only executable links CoreScene, NauSceneSerialization and Google Test, without NauUi. Standalone engine defaults contain no modules attachment; standalone minimal defaults select no UI; the ordinary attached minimal runtime selects only platform_app. UI selection is explicit in the focused fixture. Full module builds discover UI as an ordinary module.

The web Ninja graph contains only fmt/jsoncpp, NauKernel, CoreAssets, CoreScene, NauUi and NauSceneSerialization compiled archives, plus the established header dependencies (tinyutf8, utf8cpp, vectormath, wyhash, fast_float, tinyimageformat). Portable serialization compiles the existing scene reader/writer and its public factory wrappers. No Cocos, renderer, platform-app, graphics, editor, Qt, USD or unrelated importers enter this fixture.

Baseline checkout identities:

- Root: `806fd8bf825404c358a08985b7245be2874ac385`
- NauEngineModules: `cc9c3a9a79725ccd77a2c84773f37c8380db0fde`
- NauEngineLite: `c4952d9f2ee2836ccd9941e82be743c6191aa987`

Changes are uncommitted module sources/tests/docs and this root planning directory. The pre-existing dirty NauEngineLite and NauSamples states were preserved. Build trees, logs, SDKs and binaries are ignored beneath NauEngineModules/build; generated outputs and bundled third-party changes are excluded. `source-hashes.txt` records the final module worktree files for this implementation.
