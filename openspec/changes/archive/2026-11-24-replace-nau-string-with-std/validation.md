# Validation

## Repository and toolchain inputs

Implementation was performed on dirty working trees based on parent commit 3fe47ea. Component HEADs and final tracked binary-diff SHA-256 hashes are recorded below; the implementation was subsequently committed in the revisions below.

| Component | Starting HEAD | Final tracked diff SHA-256 |
| --- | --- | --- |
| NauEngineLite | `b5d605ef904c37012c9d13d0123ed0199f24b779` | `a1b10ae9c875edf7a3c0c40c8dc7921a500823555d635c87a174197960ba8fac` |
| NauEngineModules | `3d136dd86f85ea2e146a465ecbcc5c4fe2d6249b` | `69e923a9fef1aa80603b22e575b9c9c85ddec6bac5b13eb2466bb589016beccb` |
| NauEditorPublic | `b21cabbc9a1323f2eb462a52eb8fb0203133b3f1` | `744fee373eb2ff3123437b529f7e916af4a3e54ac7a7dce7db5f1210e0a535c9` |
| NauDemo | `3ac239953e03c332c3b2ff8be35abaef24d47198` | `5e94072258f9cf613469d28049d127fe254ac187d33112fcb8b6f8c6b611a127` |
| NauSamples | `44b574e34e0e90cec039af2f30483eea743d0c14` | `388667807a2f76ef1d5845e75fb8e9fc86b8b8e7123e3bb47f65433a845987fa` |

New files (not included in tracked diff hashes):

- `NauEngineLite/doc/string_migration.md`: `5e09a3ce1d15a9f0888488ac2b712ff24b4b6619271a75c6bf8c48a3f5ed13a4`
- `NauEngineLite/engine/core/kernel/src/string/unicode.cpp`: `142579687a790daa13b6b22c2021eb84b96e633f8c766bd70062586b4d9e0b5c`
- `NauEngineLite/engine/core/kernel/tests/datablock_strings/CMakeLists.txt`: `f8bad0c2e690f46070028377fc8b273feed2fa4d510e06e0ed4894412aa40d31`
- `NauEngineLite/engine/core/kernel/tests/datablock_strings/README.md`: `cd10895cf1130bf9d854a1e60960ad89af4ebdbf1be232fd14930b99485b01f6`
- `NauEngineLite/engine/core/kernel/tests/string_migration/CMakeLists.txt`: `52e2fbbe5b0bc5737626909c0a82e51e37037b286a537eaa36e8e0ca12c5845d`
- `NauEngineLite/engine/core/kernel/tests/string_migration/README.md`: `61376c1dca2a3a0436903d8d80ea7aa3bc743bb6bdc6a142426d28f7fd02f903`
- `NauEngineLite/engine/core/kernel/tests/string_migration/test_values.cpp`: `d821971f26607a7b850e04362c0e785eef0ad63d408a613bfa33a50defa1517c`

Native: Visual Studio 18 2026, MSVC 19.51.36260/v145, Windows SDK 10.0.26100.0, x64 Microsoft standard library. Web: Emscripten 6.0.9, wasm32 SDK libc++, exceptions disabled. CMake 4.2.1. Editor uses the existing Qt 6.4.1 and locally built OpenUSD 24.08 SDK. Runtime acceptance uses installed Python/Pillow/Playwright and Orca accessibility for owned editor windows.

## Baseline and focused checks

A native Release fixture passed before replacing storage. It recorded embedded-null formatting, exact JSON escaping, ASCII identifier hashes, and UTF-8 byte/code-point lengths. The pre-migration hash algorithm was inspected to record the non-ASCII answers: 0xbb2a0c587af258e5 for 64-bit and 0xaa920425 for 32-bit, using A, Cyrillic Zhe and rocket. First-null termination and hash-only equality remain intentional.

| Check | Configuration | Result |
| --- | --- | --- |
| Focused strings, conversions, formatting, hashes, views, module identity and version | Native Debug | 23/23 pass |
| Same focused suite | Native Release | 23/23 pass |
| Same focused suite, exception-disabled | Web Release | 23/23 pass |
| Broader core portability/serialization/reflection | Native Release | 156/156 pass |
| Broader core portability/serialization/reflection | Web Release | 157/157 pass |
| Renderer containers | Native and Web Release | 3/3 pass on each |
| DataBlock value access and nullable source load/copy/include against relocated DLL SDK | Native Release | 3/3 pass |

Focused commands:

```powershell
cmake -S NauEngineLite/engine/core/kernel/tests/string_migration -B NauEngineLite/build/string-migration -G "Visual Studio 18 2026" -A x64
cmake --build NauEngineLite/build/string-migration --config Release --parallel 8
ctest --test-dir NauEngineLite/build/string-migration -C Release --output-on-failure
# Repeat build/CTest with Debug.
# Web uses the same source, Ninja, activated Emscripten toolchain and SDK Node emulator.
cmake -S NauEngineModules/cmake/probes/wasm_core -B NauEngineModules/build/string-core-native -G "Visual Studio 18 2026" -A x64
cmake --build NauEngineModules/build/string-core-native --config Release --target NauCorePortabilityTests NauRendererContainerTests --parallel 6
ctest --test-dir NauEngineModules/build/string-core-native -C Release -R "^(CorePortability|RendererContainers)$" --output-on-failure
# Repeat that probe with activated Emscripten toolchain, Ninja and string-core-web.
```

String suite build roots/logs: NauEngineLite/build/string-migration (baseline-build.log, final-build.log, debug-build.log), string-migration-web (build.log, final-build.log). Broader graph logs: NauEngineModules/build/string-core-{native,web}/build.log. Web result logs record exact counts. The pre-existing disabled fatal-diagnostic fixture in the Web core suite was not selected and is not counted as a pass; no requested string behavior was excluded.

The DataBlock fixture is documented in engine/core/kernel/tests/datablock_strings/README.md; its final build.log uses the physically relocated SDK below.

## Full builds and packaged runtime

Native editor/tools/modules/sample build succeeded:

```powershell
cmake --build NauEditorPublic/build/latest-release --config Release --target NauEditor BuildToolCmd ProjectToolCmd AssetToolCmd AssetPackToolCmd SceneBaseSample inputDemo NetworkTransportSample ScriptsLua --parallel 8
```

The existing editor cache still registered the replaced standalone NauDemo as an engine external project. It was reconfigured locally with NAU_EXTERNAL_PROJECT_DIRS pointing to NauSamples; the editor's module attachment remains active. This build-cache repair is not a tracked product change.

Fresh Windows Debug/Release and Web Debug/Release rendering demo graphs built successfully. Existing Debug build directories were renamed to *-before-std-string; Release directories were fresh. Initial builds used the existing prepared archive to isolate runtime migration. Each configuration passed:

```powershell
python NauDemo/tests/verify_production_rendering.py Windows Debug
python NauDemo/tests/verify_production_rendering.py Windows Release
python NauDemo/tests/verify_production_rendering.py Web Debug
python NauDemo/tests/verify_production_rendering.py Web Release
```

These tests relocate packages to an external nested directory and check visible geometry/motion, logging, cleanup and exit. Native checks also cover resize/minimize/restore. Browser checks repeat stop/cleanup. Logs are NauDemo/build/std-string-{windows,web}-{debug,release}*.log; Debug runtime logs omit the configuration suffix.

Fresh asset preparation with rebuilt tools and the relocated SDK also succeeded:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File NauDemo/build.ps1 -Platform Windows -Configuration Debug -Declaration portable_rendering_project.json -HostSdk '<relocated SDK>' -HostTools '<checkout>/NauEditorPublic/build/latest-release/bin/Release'
```

Windows Debug was rebuilt and passed production runtime acceptance from the regenerated archive. Web Debug was rebuilt with that archive and passed the same browser check. Evidence: std-string-fresh-preparation.log, std-string-fresh-runtime.log, std-string-fresh-web.log and std-string-fresh-web-runtime.log. Prepared content.nau_pack SHA-256: 7b6aafa964cc18836238bcb651ee735bd950bd14db041be032757fc8e29ee2e9. Release runtime checks used the earlier prepared archive, not the regenerated Debug archive.

## Unicode editor and relocated SDK acceptance

A fresh SDK was installed using the engine/module install script with an empty alternate prefix. Existing install rules write some scaffold files to the configured distribution regardless of prefix, so missing scaffold files were copied from that updated distribution without overwriting fresh installed payloads or copying retired headers/packages. The SDK was then physically moved to:

`D:/Programming/Nau String Migration Checks/2026-10-09/relocated-sdk`

A fresh StringStarter project was created under a directory containing Cyrillic characters, compiled through the full legacy application/shader/game-module route, opened in the editor, and closed with exit 0. Orca verified the Project Browser accessibility tree; all 24 registered asset payloads exist. A second fresh StringRelocated project was created and compiled after the SDK move, with NAU_ENGINE_SOURCE_DIR and NAU_MODULES_SOURCE_DIR environment variables cleared. It also opened/loaded its module and closed with exit 0, with all 24 payloads present.

Commands were `NauEditor.exe project create --directory <Unicode parent> --name <name>`, `project compile --project <project> --config Release`, and `project open --project <project>`, with NAU_ENGINE_SDK_DIR set to the selected SDK. Owned session checks used verify_project_sessions.session and verify_assets. No other running editor was closed.

Project/evidence parent: `D:/Programming/Nau String Migration Checks/2026-10-09/Unicode проект`. Each project's build/string-session contains runtime.log, ui.json and result.json. CLI logs and string-fixture-path.json are in NauEditorPublic/build/latest-release.

SDK inspection found no retired string.h or tinyutf8 paths/export references. Maintained tracked source scans found no qualified retired string/view API uses or old header includes. Generated consumer compilation used SDK imports after relocation without engine/module source-path environment variables.

## Migration issues repaired and audit

- Standard construction would have changed the logging scratch-buffer constructor: it now explicitly allocates null-filled bytes and trims to the formatted length.
- Duplicate custom/standard view overloads and obsolete enum overloads were merged; custom format/hash specializations were retired.
- Renderer names retain explicit char8_t boundaries; required direct includes and explicit std::string_view ownership conversions were added.
- Former formatted string constructors/member formatting now use the shared formatting utility. Legacy leading capacity arguments were removed where they are not standard string arguments.
- Sample shader generation initially crashed in strlen. Symbol-assisted diagnosis identified DataBlockParser inserting an absent filename into a standard-string include stack. Nullable filename insertion, source assignment and related boundaries now handle null explicitly. The direct shader reproduction exits 0, full editor/sample builds pass, and load/copy/include regression tests pass. Debug symbols were enabled only in an ignored generated VS project for diagnosis.
- Module names/version fields use bytes. Module paths explicitly convert native wide paths to UTF-8 and back at Windows loading.
- DataBlock tokens/include paths and enum names use byte offsets and ASCII delimiters. Standard split uses byte views. Character-semantic tests use explicit decoding, iteration/mutation and code-point slicing.
- Borrowed views are tied to live owners. Breakpoint removal retains an owned lookup copy while vector elements move; event segment growth copies its previous segment.
- No authorized validation exclusions were needed. Intermediate compiler/linker/crash failures were repaired and are not counted as successful checks. Generated translation churn and test Python caches were removed.

## Specification coverage

Standard consumer/multibyte units: focused byte/view tests, generated SDK consumers and dependency scans. Unicode round trip/code-point slice/malformed conversion/nullable input: focused native/Web tests and DataBlock regressions. Persisted values/hash fixtures: recorded formatting/JSON/identifier tests. Unicode project runtime: all four packaged scene checks plus two Unicode editor sessions. `openspec validate replace-nau-string-with-std --strict` and component `git diff --check` passed.

## Committed implementation revisions

- NauEngineLite: `c2cddda56a8b910b3cee4ff991e5f628b5658c73`
- NauEngineModules: `08ea5737e7b70d1fb5cfd66dbce9bd349f02964a`
- NauEditorPublic: `d812c10a64817eec63f8298b5b7805fbffdc4f70`
- NauDemo: `de8b9d622bcd0a3fb68b1b7914b19e1dea350c32`
- NauSamples: `2c99b984f07c5ad200070a0852c162a473c06670`
