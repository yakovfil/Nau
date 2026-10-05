# Validation

Validated on Windows on 2026-10-05. The implementation is uncommitted; `source-hashes.json` records the component baseline revisions and SHA-256 hashes of the changed/new source and documentation files.

## Toolchain

- Visual Studio 18 2026, v145/MSVC 19.51, Windows x64.
- CMake 4.2.1; Python 3.14.2.
- Emscripten SDK 6.0.9, activated from `C:/Users/Yakov/emsdk`.
- Installed Chrome, real browser execution through Playwright; native screenshot inspection through Orca computer-use.
- vcpkg at `D:/Programming/vcpkg` for the full native demo graph.
- Engine `.clang-format` applied to new C++ files and changed regions of existing files.

## Package implementation

The reader exposes the established uncompressed version 0.1 format through an owned seekable stream. It validates bounded headers/indexes, kind/version/compression, wide integer ranges, canonical paths, duplicates/conflicts and payload bounds before publishing a filesystem. Legacy single-NUL compression markers and header separator bytes are retained. Backing storage survives filesystem release while streams remain open; interleaved/concurrent reads use independent cursors and synchronized backing IO.

The focused packer build uses kernel dependencies and AssetPackTool, with no graphics, editor, USD or application framework. The CLI sorts explicit manifest entries, propagates IO failures, validates staging output and publishes by replacement. The native and browser demos mount the archive through engine VFS. Native bootstrap checks every generated manifest entry before graphics initialization. Native shader caches and packaging outputs are generated under NauDemo/build and archive-only rebuilds update deployment.

## Executed checks

| Check | Debug | Release | Evidence |
|---|---:|---:|---|
| Native portable reader, writer, CLI and legacy Windows-reader suites | 4/4 CTest | 4/4 CTest | `NauDemo/build/asset-pack-host/Testing/`, `cli-Debug.json`, `cli-Release.json` |
| Portable reader in real Chrome | Passed | Passed | `NauDemo/build/asset-pack-web-{debug,release}/browser-results.json` |
| Native file-logging shutdown regression | Passed | Passed | `NauDemo/build/file-log-unique-{Debug,Release}-tests.log` |
| Native common host and minimal lifecycle suite | 13/13 | 13/13 | `NauDemo/build/minimal-final-{Debug,Release}-tests.log` |
| Borrowed browser runtime/minimal regression suite | 13/13 | 13/13 | `NauDemo/build/browser-minimal-final-{debug,release}-tests.log` |
| Actual browser demo acceptance | 11/11 scenarios | 11/11 scenarios | `NauDemo/build/asset-pack-acceptance/browser-final-checks.json` |
| Source-inaccessible native rendering/rotation/resize/close and font override failure | Passed | Passed | `NauDemo/build/asset-pack-acceptance/final-relocation-complete/{Debug,Release}/` |
| Native missing/corrupt archive and missing font/buffer entry | 4/4 | 4/4 | `NauDemo/build/asset-pack-acceptance/final-relocation-complete/{Debug,Release}-failures/` |
| Asset-change rebuild and stale-output rejection | Passed | Not separately repeated | Native and web build `package-build-check.json` |

Reader tests cover exact legacy offsets and bytes, directories, empty files, seek/EOF/write rejection, backing lifetime, simultaneous independent streams, truncation, malformed JSON, wrong kind/version, limits, numeric overflow, traversal, duplicate paths and file/directory conflicts. Writer tests inject missing/read/short-write/write failures and cross-read a new archive through the existing Windows backend. CLI checks cover deterministic output, duplicate/invalid paths, changed inputs, missing inputs after successful publication and failed publication with staging cleanup.

Each browser configuration ran success, missing-buffer, missing-font, bad-shader, missing-archive, corrupt-archive, truncated-archive, no-context, text-upload, host-loss and context-loss. Success includes actual scene-derived pixels and font coverage, rotation, full-viewport canvas, resize/DPR/zero-area/graphics limits, visibility, repeated Stop and reload. Failure cases check diagnostics, absence of Running where required, and cleanup. The Chrome probe's native-executable CTest entry is intentionally disabled on Emscripten; the real-Chrome entry runs the portable C++ tests.

## Native teardown repair

The user explicitly approved extending this change after visible native Debug resize/close exposed GPU resources surviving driver shutdown. The repair adds ownership cleanup for texture views, static-mesh buffers, environment resources, ImGui resources and the default graphics texture. Scene asset-update work is awaited by its owning graphics frame instead of detached, preventing late asset/GPU work after the render worker exits. File logging checks the background executor and does not depend on a stopped caller continuation; its focused test uses a unique output directory and checks accepted and late log messages.

Final native checks require orderly exit and reject GPU resource-lifetime assertions, null-executor messages and blocked completion. They passed with source assets absent. Early native screenshots that captured an occluding window were discarded; final checks place the owned demo window visibly above other windows, retain Orca metadata, and were inspected. Screenshot pixel checks account for antialiasing/scaling. Rotation capture waits for an observed image change within a bounded interval.

Existing native DX12 pipeline/input-layout diagnostics remain in logs. Acceptance establishes visible cube/environment/text, rotation, resize and successful cleanup; it does not claim every renderer diagnostic is resolved. Temporary queue/resource/runtime diagnostics were removed and restored sources were rebuilt.

## Relocation and fresh checkout

`tests/prepare_fresh_checkout.py` made separate local Git clones of NauEngineLite, NauEngineModules and NauDemo beneath `NauDemo/build/fresh-checkout/source`, then overlaid this uncommitted change. The googletest checkout uses its recorded revision and excludes the original checkout's pre-existing dirty files. No old build cache or target binaries were copied into these initial builds.

Executed `web/build.ps1 -Configuration Debug` in that checkout: it built its own native Release packer and Debug browser demo. A final overlay and incremental build verified the completed sources. `source-snapshot.json`, `final-overlay.json`, `build.log` and `final-build.log` record this separately from the ordinary build directories. This is an executed local-clone walkthrough, not a claim of independent network dependency provisioning or a second full native-engine source build.

The resulting web package was copied to a separate delivery and served under `/nested/demo/`. During actual acceptance, original demo assets, sample content/resources and the isolated source checkout were temporarily unavailable. The native deliveries were also copied out of their binary directories and launched from unrelated working directories under the same source-unavailable condition. The validation wrapper restores all source directories in a finally block; they are restored. Final fresh web evidence is `NauDemo/build/asset-pack-acceptance/fresh-web-final-results/results.json`.

## Commands and dependency evidence

Principal build/test commands, from the workspace root:

```powershell
cmake -S NauEngineModules/cmake/probes/asset_pack -B NauDemo/build/asset-pack-host -G "Visual Studio 18 2026" -A x64
cmake --build NauDemo/build/asset-pack-host --config Debug --parallel 8
ctest --test-dir NauDemo/build/asset-pack-host -C Debug --output-on-failure
cmake --build NauDemo/build/asset-pack-host --config Release --parallel 8
ctest --test-dir NauDemo/build/asset-pack-host -C Release --output-on-failure

. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake -S NauEngineModules/cmake/probes/asset_pack -B NauDemo/build/asset-pack-web-debug -G Ninja -DCMAKE_TOOLCHAIN_FILE=C:/Users/Yakov/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake -DCMAKE_BUILD_TYPE=Debug
cmake --build NauDemo/build/asset-pack-web-debug --parallel 8
ctest --test-dir NauDemo/build/asset-pack-web-debug --output-on-failure
# Repeat the portable browser probe for Release in asset-pack-web-release.
NauDemo/web/build.ps1 -Configuration Debug
NauDemo/web/build.ps1 -Configuration Release

$env:VCPKG_ROOT = 'D:/Programming/vcpkg'
cmake --preset win_vs2026_x64 -S NauEngineLite -B NauDemo/build/common-host-native-demo -DCMAKE_PROJECT_NauEngine_INCLUDE=D:/Programming/github/Nau/NauDemo/cmake/attach_demo.cmake
cmake --build NauDemo/build/common-host-native-demo --config Debug --target NauDemo --parallel 8
cmake --build NauDemo/build/common-host-native-demo --config Release --target NauDemo --parallel 8

python NauDemo/tests/test_package_build.py --build NauDemo/build/common-host-native-demo --configuration Debug
python NauDemo/tests/test_package_build.py --build NauDemo/build/web-demo-debug --web
python NauDemo/tests/audit_package_dependencies.py
python NauDemo/tests/test_source_independence.py --package NauDemo/build/asset-pack-acceptance/fresh-web-relocated --output NauDemo/build/asset-pack-acceptance/final-relocation-complete --native-root NauDemo/build/asset-pack-acceptance/relocated
python NauDemo/web/test_package.py --package NauDemo/build/web-demo-debug/package --output NauDemo/build/asset-pack-acceptance/final-web-debug-success --scenario success
# Both configurations ran the full 11-scenario list above.
```

`asset-pack-dependency-audit.json` records actual CMake File API target names for the isolated host packer, native minimal graph and both browser demo graphs. Forbidden graphics/editor/USD/concrete scene dependencies are absent from host/minimal graphs as applicable; the browser graph contains its selected scene/CPU asset/browser renderer services without desktop renderer or import tools.

Native Debug/Release common-host CTest and browser Debug/Release borrowed-runtime CTest commands were run after rebuilding the affected targets; the log locations above retain results. Final source checks passed `git diff --check` in all three components and strict OpenSpec change validation. Changed-region clang-format checks passed for 20 C++ files (`asset-pack-format-check.json`). Generated builds, packages, screenshots, logs and temporary diagnostics remain ignored. Existing googletest and NauSamples changes were untouched. No commits or push were made.
