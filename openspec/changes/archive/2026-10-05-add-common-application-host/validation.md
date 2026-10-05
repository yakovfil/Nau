# Validation

Validated on Windows on 2026-10-05. All 21 implementation tasks are complete.
Changes are uncommitted; no push was performed.

## Source and tools

`source-hashes.json` records the 29 changed/new component source and documentation
files, the removed browser entry point, and baseline repository revisions:

- Root: `4916a1324068aeb5138eb12ea453fa3062e696cc`.
- Engine: `c4952d9f2ee2836ccd9941e82be743c6191aa987`.
- Modules: `a1eae7d32f6fd58c3a094c02d143e114a3a1284a`.
- Demo: `cfb3f530d829afda271ea698539953ade6223960`.

Tools: Visual Studio 2026/v145, CMake 4.2.1, Emscripten SDK 6.0.9,
Python 3.14.2, Chrome 154.0.8037.97 through Playwright/CDP, and Orca computer
inspection for native screenshots. Native desktop dependencies use the existing
`D:/Programming/vcpkg` installation. All generated files are under the component
build directories or the demo's existing binary directory.

Pre-existing googletest submodule changes and the untracked
`NauSamples/uiSampleApp/` remain untouched. Temporary kernel tracing and queue
names used to diagnose cleanup were removed; the final kernel source is unchanged.

## Results

| Check | Configurations | Result |
|---|---|---|
| Independent common host and existing minimal lifecycle | Native Debug and Release | 12/12 CTest checks each |
| Independent common host using production browser services | Chrome Debug and Release | 13/13 CTest checks each |
| Pre-update / real scene component / post-update ordering | Native Debug and Release | 1/1 each |
| Existing borrowed browser runner regression suite | Chrome Debug and Release | 13/13 each |
| Scene/CPU/text fixtures and font-reference generation | Native Debug | 1/1 CTest suite |
| Native demo rendering, text, rotation, resize and orderly close | Debug and Release | Passed; exit 0 |
| Native missing-font startup and completed teardown | Debug and Release | Passed; diagnosed exit 1 |
| Browser demo success and injected failures | Debug and Release | 16/16 scenarios total |
| Minimal host dependency closure | Native and both browser profiles | No scene or renderer targets |
| Formatting, diff checks and strict OpenSpec validation | Changed sources/artifacts | Passed |

The browser demo scenarios are success, missing font, missing buffer, invalid
shader, unavailable context, text upload failure, host loss and context loss.
Success checks rendered scene pixels and font-derived glyph coverage, rotation,
foreground update rate, responsive heartbeat, genuine visibility transitions,
full-viewport canvas, resize/DPR, zero-area recovery, graphics limits, repeated
Stop and reload. Fault scenarios use externally instrumented responses and do not
add hooks to production demo sources.

The native runner waits for initial text presentation, captures and checks the
actual application window, compares central cube pixels across frames, resizes
the window, closes through the normal window message, and waits for process exit.
It rejects missing-font runs that time out or emit null-executor assertions or
the runtime completion-blocked warning. Debug and Release screenshots were
visually inspected for the existing cube, label and environment appearance.

The host fixtures exercise immediate/deferred delegate startup rejection,
configuration/setup failure, default and explicit phase dispatch, legacy-only
forwarding, overriding both callback forms, Stop during pending startup or from
pre-update, cleanup failure, browser timeout followed by safe cleanup, visibility
resumption and delegate destruction after application/service teardown. Native
test commands pass the selected configuration explicitly so Release exercises
the Release executable. Dedicated fixture controls remain outside NauDemo.

## Reproducible commands and evidence

Run from the parent checkout with the toolchain active. Configure commands for
the independent host are in
`NauEngineModules/cmake/probes/common_host/README.md`.

```powershell
cmake --build NauEngineModules/build/common-host-native --config Debug --parallel 8
ctest --test-dir NauEngineModules/build/common-host-native -C Debug --output-on-failure
cmake --build NauEngineModules/build/common-host-native --config Release --parallel 8
ctest --test-dir NauEngineModules/build/common-host-native -C Release --output-on-failure
ctest --test-dir NauEngineModules/build/common-host-web-debug --output-on-failure
ctest --test-dir NauEngineModules/build/common-host-web-release --output-on-failure
ctest --test-dir NauEngineModules/build/common-host-scene -C Debug --output-on-failure
ctest --test-dir NauEngineModules/build/common-host-scene -C Release --output-on-failure
ctest --test-dir NauEngineModules/build/browser-runtime-host-debug --output-on-failure
ctest --test-dir NauEngineModules/build/browser-runtime-host-release --output-on-failure
```

Native demo build and acceptance:

```powershell
$env:VCPKG_ROOT = 'D:/Programming/vcpkg'
cmake --preset win_vs2026_x64 -S NauEngineLite -B NauDemo/build/common-host-native-demo -DCMAKE_PROJECT_NauEngine_INCLUDE=D:/Programming/github/Nau/NauDemo/cmake/attach_demo.cmake
cmake --build NauDemo/build/common-host-native-demo --config Debug --target NauDemo --parallel 8
cmake --build NauDemo/build/common-host-native-demo --config Release --target NauDemo --parallel 8
python NauDemo/tests/test_application_host_native.py
```

Browser demo build and acceptance (repeat for Release and each listed scenario):

```powershell
. C:/Users/Yakov/emsdk/emsdk_env.ps1
./NauDemo/web/build.ps1 -Configuration Debug
python NauDemo/web/test_package.py --package NauDemo/build/web-demo-debug/package --output NauDemo/build/common-host-browser-final/debug-success --base-path /relocated/demo/ --scenario success
```

Font references are generated by configuring `NauDemo/tests/demo_scene` into
`NauDemo/build/text-tests-native`, building `NauDemoSceneTests` in Debug and running
CTest. The browser runner's default font-reference path matches that directory.

Machine-readable results and diagnostic logs are retained under:

- `NauEngineModules/build/common-host-native/results/Debug` and `Release`.
- `NauEngineModules/build/common-host-web-{debug,release}/results`.
- `NauEngineModules/build/common-host-native/dependency-audit.json`.
- Scene and borrowed-runner build directories listed in the commands above.
- `NauDemo/build/common-host-native-demo/acceptance/results.json`, screenshots and logs.
- `NauDemo/build/common-host-browser-final/checks.json` and each scenario's `results.json`.

## Desktop cleanup diagnosis and repair

Before repair, a missing font rejected delegate startup immediately after native
window initialization. Window sizing had already queued a resize on the graphics
pre-render executor. The old disposed render-frame branch released graphics
without polling that queue. Temporary runtime tracing identified that queue as
the only executor with pending work after graphics shutdown; the process then
stalled and emitted null-executor assertions.

The approved repair drains accepted graphics jobs on the render worker before
resource release, reports a drain error through the existing shutdown task, and
prevents window requests made after disposal begins from adding more queued work.
The missing-font integration scenario now completes in both native configurations.
No timeout or forced process termination is counted as a passing cleanup result.

One initial native Release shader-cache generation reported an access violation
in the existing shader compiler tool. Retrying the build and the final Debug and
Release builds succeeded. No shader compiler source was changed. Existing native
DX12 input-layout diagnostics remain visible in logs; the requested rendering,
text and lifecycle checks passed without broad renderer or shader-tool changes.
