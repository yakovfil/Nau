# Widget transform validation

Validated on 2026-10-04 in D:/Programming/github/Nau. Implementation changes are confined to five files under NauEngineModules/modules/ui: public header, implementation, README, focused unit tests, and consumer main. No CMake or dependency changes were required.

## Results

| Check | Result |
| --- | --- |
| Native Debug focused suite | 12/12 passed |
| Native Release focused suite | 12/12 passed |
| Emscripten Release consumer through Node | 1/1 passed |
| Relocated SDK Debug consumer | 1/1 passed |
| Relocated SDK Release consumer | 1/1 passed |
| CMake File API dependency/SDK-path audit | Passed |
| Four affected C++ files: clang-format dry run with Werror | Passed |
| Component/root git diff --check | Passed |
| openspec validate add-widget-transforms --strict | Passed |

Native suites retain the eight previous widget ownership/state/death tests, add three spatial tests, and run the expanded consumer. New coverage verifies identity/defaults and const-safe access; valid signed/zero scale and zero size; external pivots; all transform components receiving NaN/infinity; both size/pivot components receiving non-finite values; negative size; zero/nonunit quaternion rejection; no silent quaternion normalization; root/three-level composition with X/Y/Z rotation; independently constructed expected matrices and points; actual shear measured through nonorthogonal basis columns; immediate ancestor edits; size/pivot independence; and retained local geometry/UID through rejected attachment, detach, and reparent.

The public consumer executes representative geometry, nonuniform-scale/rotation composition, size/pivot independence, invalid-state preservation, detachment, and singular/reflected forward-transform checks in native, Node, and installed SDK configurations. Emscripten validation is headless WebAssembly execution through Node; no browser visual check is needed for this mathematical API.

## Commands and artifacts

Existing focused source build directories were reused. Native compiler: VS 18 2026 x64/v145, MSVC 19.51.36260; CMake 4.2.1. Emscripten SDK: C:/Users/Yakov/emsdk, Node v24.19.0. Activate Emscripten with its emsdk_env.ps1 before the web commands.

```powershell
cmake --build NauEngineModules/build/nau-widget-native --config Debug --target test_widget NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-native -C Debug --output-on-failure
cmake --build NauEngineModules/build/nau-widget-native --config Release --target test_widget NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-native -C Release --output-on-failure
cmake --build NauEngineModules/build/nau-widget-web --target NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/nau-widget-web --output-on-failure
```

SDK configure/install used a fresh configured prefix, rather than an install-time override:

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/nau-widget-native -DCMAKE_INSTALL_PREFIX=D:/Programming/github/Nau/NauEngineModules/build/widget-transforms-sdk-stage-complete
cmake --install NauEngineModules/build/nau-widget-native --config Debug
cmake --install NauEngineModules/build/nau-widget-native --config Release
```

After checking that both absolute paths were inside NauEngineModules/build and the destination was absent, the complete prefix was moved to widget-transforms-sdk-relocated-complete. The original stage-complete path is absent. The SDK contains 447 files, including the updated widget header and Debug/Release NauUi libraries.

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/widget-transforms-sdk-consumer -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_SDK=D:/Programming/github/Nau/NauEngineModules/build/widget-transforms-sdk-relocated-complete
cmake --build NauEngineModules/build/widget-transforms-sdk-consumer --config Debug --target NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/widget-transforms-sdk-consumer -C Debug --output-on-failure
cmake --build NauEngineModules/build/widget-transforms-sdk-consumer --config Release --target NauWidgetConsumer --parallel 6
ctest --test-dir NauEngineModules/build/widget-transforms-sdk-consumer -C Release --output-on-failure
python NauEngineModules/build/widget-evidence/transforms-audit.py
openspec validate add-widget-transforms --strict
```

Ignored logs and audit output are under NauEngineModules/build/widget-evidence with transforms- prefixes. The File API audit verifies all generated SDK consumer configurations use includes from the relocated complete prefix and libraries without source or former-stage paths. Compiled widget closure remains CoreAssets, CoreScene, NauKernel, NauUi, fast_float, fmt, jsoncpp, vectormath (plus native ZERO_CHECK); no Cocos, graphics, input, window, Qt, USD, or DirectX dependency was introduced. Existing default-build codemodel snapshots were inspected for independence; those default builds were not rebuilt in this change.

## Corrections and limits

An initial spatial test had an incorrect handwritten expected X coordinate: translation 3 plus scaled coordinate -2 equals 1. Correcting that expectation produced the passing native runs above; no production change was needed.

The initial SDK install attempt used --prefix without updating the configured prefix. Existing absolute install destinations placed some headers in the old stage path, causing consumer configuration to fail. Reconfiguring CMAKE_INSTALL_PREFIX, reinstalling into a fresh stage-complete directory, and relocating it resolved the check without modifying build infrastructure. The incomplete first SDK is ignored diagnostic output and was not used for successful verification.

Emscripten emits existing string/Unicode header warnings. No warning-free claim is made. Ordinary floating-point range limits and O(depth) accumulated queries are documented. No requirements or validations were waived. Changes have not been committed or archived by this apply step.
