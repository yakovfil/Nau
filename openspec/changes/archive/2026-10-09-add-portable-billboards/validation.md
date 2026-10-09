# Validation

Validated on 2026-10-09 in the local Windows checkout. The change was subsequently synced and archived on the same date; committed component revisions are recorded below. No changes have been pushed.

## Source and toolchain

Starting revisions:

| Repository | Revision |
| --- | --- |
| Parent | `992ab2ab5ea8f68ccfa0af981538dc58a8a063c2` |
| NauEngineLite | `c2cddda56a8b910b3cee4ff991e5f628b5658c73` |
| NauEngineModules | `08ea5737e7b70d1fb5cfd66dbce9bd349f02964a` |
| NauDemo | `de8b9d622bcd0a3fb68b1b7914b19e1dea350c32` |
| NauEditorPublic | `d812c10a64817eec63f8298b5b7805fbffdc4f70` |
| NauSamples | `2c99b984f07c5ad200070a0852c162a473c06670` |

VS 2026/v145, MSVC 19.51.36260, Windows SDK 10.0.26100.0, CMake 4.2.1, Emscripten 6.0.9, SDK Node 24.19.0, OpenUSD 24.08. Native preparation uses Python 3.10.11 and Pillow 12.3.0; validation scripts use Python 3.14.2, Pillow and Playwright/installed Chrome. Native inspection used Orca computer-use 1.4.223.

The actual native USD Python initially lacked Pillow. Its prerequisite diagnostic worked; Pillow was installed into that interpreter. Generic setup is documented, and non-rendering preparation remains usable without the decoder.

`NauDemo/build/billboard-source-snapshot.json` records SHA-256 values for all changed/new module and demo files. Tests and documentation remain in their component repositories; generated binaries, logs, images, packages and temporary projects are ignored build artifacts. Engine, editor and sample working trees have no source changes.

## Build and archive

All four rendering deliveries used the same prepared archive:

`33c243b1d2fe19cc98d25bd0bcfb4caced6b5bd028535303a9a57a49a5e5cd2d`

`billboard-final-archives.json` independently compares the prepared archive, both Windows package archives and both Web `.data` payloads. All five hashes match. Probe deliveries use that same selection.

Representative commands from the checkout root (set matching host SDK/tools/USD paths and activate Emscripten as documented):

```powershell
cmake --build NauEditorPublic/build/latest-release --config Release --target AssetToolCmd UsdTranslator UsdTranslatorWrapper --parallel 8
./NauDemo/build.ps1 -Platform Windows -Configuration Debug -Acceptance -Declaration ./portable_rendering_project.json -HostSdk <native-sdk> -HostTools <native-tools> -UsdSdk <usd-sdk>
./NauDemo/build.ps1 -Platform Windows -Configuration Release -Acceptance -Declaration ./portable_rendering_project.json -PreparedArchive <prepared-archive>
./NauDemo/build.ps1 -Platform Web -Configuration Debug -Acceptance -Declaration ./portable_rendering_project.json -PreparedArchive <prepared-archive>
./NauDemo/build.ps1 -Platform Web -Configuration Release -Acceptance -Declaration ./portable_rendering_project.json -PreparedArchive <prepared-archive>
```

Relative declaration paths are relative to the consumer project. Actual runs used the absolute NauDemo declaration. The host SDK used for component registration was the relocated SDK from the preceding standard-string migration, and tools were rebuilt in the editor Release graph. The new runtime texture path has no USD, Qt or PNG decoder dependency.

Final build logs: `NauDemo/build/billboard-repeat-preparation.log` and `billboard-final-<Windows|Web>-<Debug|Release>.log`; intermediate failures and repairs are retained separately.

## Completed checks

| Validation | Result |
| --- | --- |
| PNG, identity normalization and declaration Python tests | 9/9 |
| CPU texture/projection contract, native Debug | 28 checks |
| CPU texture/projection contract, Web Debug under SDK Node | 28 checks |
| Real host preparation/publication cases | 7/7 |
| Billboard runtime/visual cases, Windows Debug | 22/22 |
| Billboard runtime/visual cases, Windows Release | 22/22 |
| Billboard runtime/visual cases, Web Debug | 22/22 |
| Billboard runtime/visual cases, Web Release | 22/22 |
| Production demo rendering, Windows/Web Debug/Release | 4/4 |
| Existing native rendering regression cases, Debug | 27/27 |
| Existing browser rendering regression cases, Debug | 30/30 |
| Non-rendering packaged native startup, Release | 18/18 |
| Common-host native Release CTest | 18/18 |
| Common-host browser Release CTest | 18/18 |
| Shader delivery/fault tests | 5/5 |
| Legacy SceneBaseSample Release | built; displayed scene/ImGui; primary close returned 0 |

### Contract and preparation

```powershell
python -m unittest test_portable_texture test_portable_scene_identity test_packaged_declaration -v
cmake -S NauEngineLite -B NauDemo/build/basic-rendering-scene/windows-debug -DNAU_BILLBOARD_TESTS=ON
cmake --build NauDemo/build/basic-rendering-scene/windows-debug --config Debug --target NauBillboardContractTests --parallel 8
./NauDemo/build/basic-rendering-scene/windows-debug/bin/Debug/NauBillboardContractTests.exe
# Activate the SDK, configure the equivalent web build with NAU_BILLBOARD_TESTS=ON, then:
cmake --build NauDemo/build/basic-rendering-scene/web-debug --target NauBillboardContractTests --parallel 8
& $env:EMSDK_NODE ./NauDemo/build/basic-rendering-scene/web-debug/bin/NauBillboardContractTests.js
python NauDemo/tests/verify_billboard_preparation.py
```

The Python unit command runs from `NauEngineModules/tools/asset_tools`. Checks cover canonical little-endian header and pixel orientation, RGB alpha expansion, rejected bit depths/modes/animation, malformed dimensions/lengths, missing decoder diagnostics, generated identity uniqueness, authored UID preservation and reference remapping.

Real preparation was repeated both on NauDemo and on an isolated copy. Archives were byte-identical. Changing a PNG changed its packed pixels; missing/corrupt PNGs and missing Pillow failed with nonzero exits and did not replace the last successfully published archive. Non-rendering preparation succeeded with Pillow intentionally unavailable. A before/after hash comparison confirmed authored content was unchanged. Evidence: `billboard-determinism.json`, `billboard-preparation-validation/results.json` and its seven logs.

The generic USD component adapter originally lost the texture reference. Its explicit metadata-to-UID conversion now preserves the authored USD attribute, and preparation asserts that the cooked component references the expected texture UID. The user approved the additional generated-identity normalization needed for deterministic repeated scene cooking; proposal, design, spec delta and task 2.3 were updated accordingly.

### Runtime and visual acceptance

```powershell
python NauDemo/tests/verify_billboards.py Windows Debug
python NauDemo/tests/verify_billboards.py Windows Release
python NauDemo/tests/verify_billboards.py Web Debug
python NauDemo/tests/verify_billboards.py Web Release
python NauDemo/tests/verify_production_rendering.py Windows Debug
python NauDemo/tests/verify_production_rendering.py Windows Release
python NauDemo/tests/verify_production_rendering.py Web Debug
python NauDemo/tests/verify_production_rendering.py Web Release
```

Native deliveries were copied outside the checkout and launched with a restricted runtime PATH. Web deliveries were served under `/relocated/nested/application/` in real Chrome/WebGL, using SwiftShader in headless acceptance. Both root launchers retain their existing shared build/entry workflow; their selected rendering packages were exercised directly rather than leaving their interactive server/application running.

The 22 cases per configuration cover billboard-only output, distance/FOV independence, camera facing, scaled/rotated parent transforms, shared resources, texture replacement, visibility/removal, behind/near/far camera rejection, mesh depth occlusion, alpha holes, viewport-edge clipping, repeated Stop during pending texture loading, removal/replacement during loading, missing/corrupt/oversized textures and invalid size. Default construction and JSON serialization round trips are checked in the scene probe. Independent observations prove component/texture IDs and hashes of actual CPU texture bytes; backend cleanup logs confirm shared billboards use one GPU texture.

Tests compare asymmetric corner colors within 25 channel values and colored marker width within 5 pixels of the independently expected `0.12 * drawableWidth * 56/64`. Source parent transforms are checked independently; native scene SSE reciprocal estimates have a documented subpixel tolerance (0.005 world units for the parent case and 0.01 at depth 12). Screenshot calculations account for the native drawable's actual aspect ratio after resizing. Screenshot evidence is under `NauDemo/build/basic-rendering-scene/billboards-<platform>-<configuration>/` and `production-<platform>-<configuration>/`.

Existing browser regression runs exercise DPR 2, tall/wide resizing, zero-size suspension/recovery and context loss. Independent marker-width checks were also applied to their resize/recovery images and all four production images; `billboard-viewport-evidence.json` records measured/expected widths. Initial native upload used a legacy flag that aliases a different DX12 flag; the implementation now uses the existing checked staging-image upload route. Both backends use sRGB texture sampling followed by the scene output conversion.

### Regressions

```powershell
python NauDemo/tests/verify_native_rendering.py Debug
python NauDemo/tests/verify_web_rendering.py Debug
./NauDemo/build.ps1 -Platform Windows -Configuration Release -Acceptance
python NauDemo/tests/verify_native_startup.py --configuration Release
cmake --build NauEngineModules/build/common-host-native --config Release --parallel 8
ctest --test-dir NauEngineModules/build/common-host-native -C Release --output-on-failure
cmake --build NauEngineModules/build/common-host-web-release --parallel 8
ctest --test-dir NauEngineModules/build/common-host-web-release --output-on-failure
python NauEngineModules/modules/scene_renderer/tests/verify_shader_delivery.py --output NauDemo/build/billboard-shader-delivery
cmake --build NauEditorPublic/build/latest-release --config Release --target SceneBaseSample --parallel 8
```

Rendering regression evidence is under `native-observer-debug/` and `web-observer-debug/`; it includes initialization/upload/submission failures, pending work and graphics loss. Non-rendering evidence is `native-acceptance-release.json`. Common-host CTest logs are `billboard-common-host-<native|web>-tests.log`.

The legacy sample was launched from the SDK working directory, inspected using its owned window and closed normally. Evidence: `billboard-legacy-sample/{runtime.log,scene.png,result.json}`. Its default view displays ImGui and scene data; camera navigation to isolate the legacy billboard scene was not exercised. A pre-existing DX12 pipeline-cache missing-folder diagnostic remained nonfatal, with exit 0 and graphics teardown completed. Portable billboard pixels and lifetime have the dedicated four-configuration acceptance above.

## Limits and final checks

No required implementation behavior or validation was waived. Supported targets are Windows and Web; soft transparency, world-sized billboards, general textured mesh materials, hot pixel-file reload and automatic graphics recovery remain outside the planned subset. Browser GPU validation used software rendering; additional physical browser GPU/vendor coverage was not performed. Editor UI authoring controls were not modified or separately validated.

`openspec validate add-portable-billboards --strict`, component `git diff --check`, Python syntax checks and engine clang-format checks pass. Final source formatting and additional assertions applied to already captured independent evidence do not change the runtime behavior validated above. All 17 implementation tasks are complete.

## Committed revisions

- NauEngineModules: `5d8b6028874b9473d65e2e7cccd2078c0e287cf0` ? portable billboard rendering, CPU textures and deterministic preparation.
- NauDemo: `7baefcb63c068d5ca2df7af7cf7240bf6719b93c` ? authored marker assets, scene integration and acceptance checks.
- The parent commit records these revisions, the synced main specification and this archived change.
