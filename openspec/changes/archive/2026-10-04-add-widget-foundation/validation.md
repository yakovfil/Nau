# Widget foundation validation

Validated on 2026-10-04 using Visual Studio 18 2026 / v145 and external Emscripten 6.0.9 on Windows. Paths below are relative to `D:/Programming/github/Nau` unless absolute.

## Implementation scope

New static `NauUi` library, concrete Widget, headless tests, source/installed consumer fixture, and module README under `NauEngineModules/modules/ui`. The modules-owned SDK import list adds NauUi after NauKernel. No application, framework, default runtime profile, legacy asset handler, or third-party source changes were made.

## Native widget tests

Reconfigured the existing full static native graph with `cmake -S NauEngineLite -B NauDemo/build/retire-ui-native`. For each of Debug and Release:

```powershell
cmake --build NauDemo/build/retire-ui-native --config Debug --target test_widget --parallel 8
ctest --test-dir NauDemo/build/retire-ui-native -C Debug -R WidgetTests --output-on-failure
cmake --build NauDemo/build/retire-ui-native --config Release --target test_widget --parallel 8
ctest --test-dir NauDemo/build/retire-ui-native -C Release -R WidgetTests --output-on-failure
```

Both configurations: **6/6 passed**. Coverage includes construction/defaults/identity, compile-time non-copy/move and const-pointer contracts, ordered attachment, self/ancestor-cycle/null rejection without ownership loss, direct and non-direct removal, reparenting with stable state and identity, multi-level exactly-once destruction, parent references cleared before child destruction, detached subtree survival with preserved descendants, and immediate ancestry-based visibility.

The already-parented attachment guard was reviewed rather than exercised by manufacturing invalid duplicate ownership. Initial build attempts identified a missing regenerated target and a test-entrypoint CRT mismatch; the final test target uses its own main and existing correctly configured gtest target. No third-party changes were required. The final six tests were repeated after strengthening detached-subtree lifetime coverage.

## Focused source and SDK consumers

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/widget-native -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_ENGINE=D:/Programming/github/Nau/NauEngineLite -DCMAKE_INSTALL_PREFIX=D:/Programming/github/Nau/NauEngineModules/build/widget-sdk
cmake --build NauEngineModules/build/widget-native --config Debug --target NauWidgetConsumer --parallel 8
ctest --test-dir NauEngineModules/build/widget-native -C Debug --output-on-failure
cmake --build NauEngineModules/build/widget-native --config Release --target NauWidgetConsumer --parallel 8
ctest --test-dir NauEngineModules/build/widget-native -C Release --output-on-failure
cmake --install NauEngineModules/build/widget-native --config Debug
cmake --install NauEngineModules/build/widget-native --config Release
```

Source consumers: **1/1 passed per configuration**. The fixture explicitly selects the widget module over the standalone minimal kernel. An initial fixture build exposed parent/subdirectory CMake scope differences in CRT settings; platform setup now precedes adding the widget directory and static runtime selection is explicit in the fixture.

Moved the complete fresh installation from `NauEngineModules/build/widget-sdk` to `NauEngineModules/build/widget-sdk-relocated` after verifying both paths stay inside the owned build directory. The original prefix no longer exists. The installation has 371 files, including the public widget header and both configuration libraries/exports.

```powershell
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/widget-sdk-consumer -G "Visual Studio 18 2026" -A x64 -DNAU_WIDGET_SDK=D:/Programming/github/Nau/NauEngineModules/build/widget-sdk-relocated
cmake --build NauEngineModules/build/widget-sdk-consumer --config Debug --parallel 8
ctest --test-dir NauEngineModules/build/widget-sdk-consumer -C Debug --output-on-failure
cmake --build NauEngineModules/build/widget-sdk-consumer --config Release --parallel 8
ctest --test-dir NauEngineModules/build/widget-sdk-consumer -C Release --output-on-failure
```

Installed consumers: **1/1 passed per configuration**. The fixture exercises the module README example's API and checks ownership transfer, parent references, visibility, and returned ownership. CMake File API inspection confirms public includes come from the relocated SDK and link inputs contain no implementation checkout paths.

## Emscripten

```powershell
. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake -S NauEngineModules/modules/ui/tests/consumer -B NauEngineModules/build/widget-web -G Ninja -DCMAKE_TOOLCHAIN_FILE=C:/Users/Yakov/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake -DNAU_BUILD_BROWSER=ON -DCMAKE_BUILD_TYPE=Release -DNAU_WIDGET_ENGINE=D:/Programming/github/Nau/NauEngineLite
cmake --build NauEngineModules/build/widget-web --target NauWidgetConsumer --parallel 8
ctest --test-dir NauEngineModules/build/widget-web -R WidgetConsumer --output-on-failure
```

Compile/link: **passed**. Generated JS/Wasm consumer executed under the activated SDK's Node: **1/1 passed**. This is headless Wasm validation; there is no rendering or browser-window acceptance requirement in this change. Existing kernel/header compiler warnings were emitted; no claim of a warning-free build is made.

## Dependency and default-profile checks

Added CMake File API codemodel queries in ignored build directories, then reconfigured:

```powershell
cmake -S NauEngineLite -B NauDemo/build/kernel-check
cmake -S NauEngineLite -B NauDemo/build/minimal-check
cmake -S NauDemo/tests/demo_scene -B NauDemo/build/text-tests-native
python NauEngineModules/build/widget-evidence/audit_graphs.py
```

All configurations inspected pass:

- Standalone kernel: 79 targets, no NauUi.
- Existing minimal profile: 24 targets, no NauUi.
- Existing scene profile: 32 targets, no NauUi.
- Focused native widget graph: 20 targets; NauUi's compiled dependency closure is NauKernel, fmt, jsoncpp, vectormath, fast_float, and the generator's ZERO_CHECK utility. Header-only dependencies remain in the kernel's public interface.
- Focused Emscripten graph: 35 targets including CTest utilities; the compiled NauUi closure is the same portable libraries without ZERO_CHECK.
- Relocated SDK contains no Cocos or legacy ui_manager artifacts; consumer public include and link paths use installed interfaces.

The audit output and build/test logs are retained locally under ignored `NauEngineModules/build/widget-evidence/`. Default module selection files and legacy rejection code have no changes. No broad engine runtime suite or visual checks were required or claimed for this headless foundation.

## Final checks and identities

Changed C++ formatted with Visual Studio's x64 clang-format and `NauEngineLite/.clang-format`. `git diff --check`, formatter verification, and `openspec validate add-widget-foundation --strict` pass. No validation exceptions were accepted.

Base revisions:

- Parent: `51e0d720f702295b221754454906c470a1e6a5fd`
- NauEngineModules: `fe0d648491247a3684ad867efa5f3f11e924ffba`
- NauEngineLite: `c4952d9f2ee2836ccd9941e82be743c6191aa987`

`working-tree-identities.json` records SHA-256 identities of all changed implementation files at validation. Existing unrelated dirty googletest content and generated sample files were retained and not edited. No commit or push was performed.
