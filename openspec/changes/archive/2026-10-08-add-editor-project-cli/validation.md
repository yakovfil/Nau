# Validation: add-editor-project-cli

Validated on Windows x64 on 2026-10-08. Commands ran against the deployed editor,
not a source-tree wrapper. Implementation commits: NauEngineLite `b5d605ef`, NauEngineModules `e6b9b48`,
and NauEditorPublic `b21cabb`.

## Revisions and prerequisites

Base revisions, with this change applied in the working trees:

| Repository | Base revision |
| --- | --- |
| Nau | `1e15a6e070f817ecebefebe39d367044142eef51` |
| NauEditorPublic | `8f90bd5340fdb9eff0e117915d6383a73c5e2567` |
| NauEngineModules | `3e6512a887c61a05588cbf75fcf90d3d7e37f41b` |
| NauEngineLite | `c9c98d388fae1ed0f250cdf0899e194c1b783bf2` |

Editor 0.10.3 beta, Qt 6.4.1, Visual Studio 2026/v145, CMake 4.2.1,
OpenUSD 24.08 with usdGltf_plugin, native Python 3.10 and Emscripten 6.0.9.
Python test tools, Pillow, Playwright/Chrome and Orca were provisioned locally.
Environment setup follows `NauEditorPublic/doc/project_cli.md`; no command
installed dependencies implicitly. The matching kernel/framework SDK was
refreshed after the approved Unicode repairs.

Editor distribution: `NauEditorPublic/build/latest-release/Release/NauEditor`.
External fixtures: `D:/Programming/Nau CLI Checks/2026-10-08`, including the
`Unicode пространство` directory.
Names include `CliStarter`, `CliAsciiFresh`, `UnicodeStarter` and
`UnicodeLegacyFresh`. Fixtures, builds, screenshots and logs are not committed.

## Focused checks

| Check | Result |
| --- | --- |
| QtCore/GTest CLI parsing, identity and subprocess checks | 6/6 passed |
| Deployed CLI checks | 39 passed |
| Windows Unicode filesystem root, filename, resolution and actual stream read | 1/1 passed |
| Real shader compiler with Unicode source/include/cache-name/output paths | Passed; nonempty cache |
| Fresh ASCII editor sessions and registered payload checks | Passed |
| Unicode editor sessions and registered payload checks | Passed |
| Native Release compilation, full legacy target graph | Passed |
| Native compiler flag preservation | `/DCLI_UNICODE_FLAG_PRESERVED` retained alongside `/utf-8` |
| Real native source error | Result 4; expected `#error` diagnostic; source restored |
| Failed preparation with an older portable delivery present | Result 4; no success claim; material restored |
| Explicit initialization failure (missing distribution plugin metadata) | Result 4; diagnostic captured |
| Editor guard occupied | Second open returned 5; independent inspect/create returned 0 |

Reproducible commands from the checkout root:

```powershell
cmake --build NauEditorPublic/build/latest-release --config Release --target NauEditor --parallel 8
cmake -S NauEditorPublic/editor/tests/cli -B NauEditorPublic/build/editor-cli-tests -G "Visual Studio 18 2026" -A x64 -DCMAKE_PREFIX_PATH='<Qt-prefix>'
cmake --build NauEditorPublic/build/editor-cli-tests --config Release
# Put the matching Qt bin directory on PATH.
ctest --test-dir NauEditorPublic/build/editor-cli-tests -C Release --output-on-failure
python NauEditorPublic/editor/tests/cli/verify_project_cli.py --editor '<editor-distribution>/NauEditor.exe'
cmake -S NauEngineLite/engine/core/kernel/tests/native_file_system -B NauEngineLite/build/native-fs-regression -G "Visual Studio 18 2026" -A x64
cmake --build NauEngineLite/build/native-fs-regression --config Release --target NauNativeFileSystemTests
ctest --test-dir NauEngineLite/build/native-fs-regression -C Release --output-on-failure
python NauEngineModules/tools/shader_compiler_tool/tests/verify_unicode_paths.py --tool '<editor-distribution>/ShaderCompilerTool.exe' --sdk '<native-SDK>'
```

Use a subprocess API, or explicit shell waiting as documented, when checking
GUI-subsystem executable completion. Session checks operate and close their own
PIDs only:

```powershell
python NauEditorPublic/editor/tests/cli/verify_project_sessions.py --editor '<editor-distribution>/NauEditor.exe' --project '<fresh-external-project>' --creation-parent '<existing-parent>' --creation-name '<unused-name>'
```

Both ASCII and Unicode runs verified direct chooser bypass and a `Project Browser`
accessibility tree, ordinary native module loading, `--ignore-project-modules`,
`create --open`, and the unchanged no-command `MY PROJECTS` chooser. Project
sessions closed with result 0. Canceling the ordinary chooser retained its
existing initialization-failure result 4. Asset checks require a nonempty database
and every registered payload to exist in the intended project directory.

Native Unicode compilation produced `MainGameModule.dll`, the legacy executable
and a nonempty shader cache without disabling PCH or narrowing target selection.
CMake codemodel declarations repaired the generated ANSI PCH wrappers; authored
headers and caller compiler flags were retained.

The 39 deployed checks cover help/version, option errors, malformed project and
declaration JSON, ambiguous directories, relative/Unicode inputs, preset
includes/inheritance/user presets and independently conditioned configure/build names, missing selections, missing tools, child
nonzero results, incompatible editor versions, unsafe source-overlapping legacy
outputs and preservation of existing creation destinations. Inspection hashes
remain unchanged without SDK/compiler/Emscripten provisioning.

## Portable application acceptance

All four normal generated build presets completed through the deployed CLI for
`CliStarter`. Profile: `basic-rendering-scene`.

| Preset | Configuration | Delivery directory under the project |
| --- | --- | --- |
| `portable-windows-debug` | Debug | `build/basic-rendering-scene/windows-debug/package` |
| `portable-windows-release` | Release | `build/basic-rendering-scene/windows-release/package` |
| `portable-web-debug` | Debug | `build/basic-rendering-scene/web-debug/package` |
| `portable-web-release` | Release | `build/basic-rendering-scene/web-release/package` |

```powershell
# Repeat for each of the four presets.
& $editor project build --project $project --preset portable-windows-debug
python NauEngineModules/tools/project_tools/tests/verify_generated_delivery.py --project $project --target CliStarterMain --platform Windows --configuration Debug
```

The production delivery verifier relocated each package to an independent nested
folder. Native runs verified visible blue/orange geometry, motion, resize,
minimize/restore and orderly closure. Browser runs used Chrome with the required
headers, verified geometry and motion at a nested URL, then repeated Stop and
checked the stopped lifecycle. Results and screenshots are in
`CliStarter/build/acceptance/{windows,web}-{debug,release}`.

A final Windows Debug CLI cook/build and relocated runtime check passed after the
asset/filesystem repairs: 28,386 blue pixels, 26,256 orange pixels, archive SHA256
`3d6da944e602bf96a077be22567e6f4f06b3d3ac3676dc1b9f5c21b862fc9115`.

Preset parity used a distinct configure name `cli-parity-configure` and build name
`cli-parity-build` in the fixture's user presets. Both CLI and direct CMake
selection succeeded using the same prepared archive, produced the same delivery
location and preserved its bytes. The final distinct-name CLI build also passed after the namespace/condition fix (`editor-cli-preset-parity-final.log`). Independent normal cooks can generate new
metadata UIDs; the four independently cooked archives are not claimed identical.

## Legacy Release acceptance

The full explicit legacy build succeeded for the ASCII fixture and for the
fresh Unicode fixture using `win_vs2026_x64_dll`, Release and an external
output directory. It compiled application/module sources and shaders, imported
assets, packaged them and copied staged resources/configuration. All 24 records
in the repaired Unicode fixture have real payloads in `assets_database`.

```powershell
& $editor project create --directory $parent --name UnicodeLegacyFresh --template empty
& $editor project build --project "$parent/UnicodeLegacyFresh" --preset win_vs2026_x64_dll --config Release --output "$parent/UnicodeLegacyDelivery"
# Launch from the delivery directory; close its own primary window.
```

The fresh Unicode Release executable reached its visible native window, survived
resize/minimize/restore and exited 0 after primary-window closure. The legacy
starter scene is empty and its captured drawable is blank, as expected; colored
scene rendering was verified separately in all four portable deliveries.
Snapshots/result are in `NauEditorPublic/build/latest-release/legacy-acceptance`.
Delivered `vfs.json` uses `${projectDir}/resources` while authored configuration
retains `${projectDir}/build/legacy-resources`. The editor uses staged resources
when available and retains the existing resources fallback.

A preservation check hashes authored project/preset/declaration/configuration
files and the existing four portable package contents before and after an
explicit legacy build. All 22 sampled files were unchanged. Its evidence is `editor-cli-legacy-preservation.json`.

## Evidence and limits

Ignored logs under `NauEditorPublic/build/latest-release` include:

- `editor-cli-build-complete.log`, `editor-cli-native-fs-build.log`
- `editor-cli-native-compile.log`, `editor-cli-unicode-compile.log`, `editor-cli-unicode-flags.log`
- `editor-cli-compile-failure.log`, `editor-cli-stale-preparation-failure.log`
- `editor-cli-coexistence-results.json`, `editor-cli-preset-parity.log`
- `editor-cli-portable-*.log`, `editor-cli-delivery-*.log`
- `editor-cli-portable-final-regression.log`, `editor-cli-portable-final-runtime.log`
- `editor-cli-sessions.log`, `editor-cli-sessions-ascii.log`
- `editor-cli-unicode-fresh-legacy.log`, `editor-cli-legacy-build.log`

Session results, accessibility snapshots and asset counts also live in each
fixture's `build/cli-sessions`. Earlier failed attempts were retained externally
for inspection, including wrongly encoded directories/database files. One reused
ASCII fixture timed out during desktop inspection after loading its assets;
fresh ASCII and Unicode session suites pass, and only successful recorded runs
support acceptance claims.

Existing USD duplicate-type/schema warnings and optional DX12 pipeline-cache
warnings appeared during editor startup. They did not prevent the successful
recorded sessions or orderly closure. This validates the Windows editor host and
its generated Windows/web routes, not a Linux/macOS editor host or arbitrary
third-party templates/projects. The CLI does not upgrade existing source templates
or install missing prerequisites.

Final checks: strict OpenSpec validation and component/root whitespace checks.
