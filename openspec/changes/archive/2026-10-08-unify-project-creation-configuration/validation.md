# Validation

## Result (2026-10-08)

Generated portable project integration, script/preset selection, generation/rebuild handling and retained native compatibility passed the checks below. Implementation changes are in NauEngineModules; the editor's Build/Run controls were not edited. Actual editor creation and native module compilation/loading were confirmed by the user.

Baseline revisions before the uncommitted implementation: root `ba190a5`, NauEngineModules `a0ad422`, NauEngineLite `c9c98d38`, NauDemo `54a5f30`.

## Environment and generated projects

- Windows, Visual Studio 18 2026/v145, MSVC 19.51.36260, Windows SDK 10.0.26100.0, CMake 4.2.1, Ninja 1.13.2, Windows PowerShell 5.1.
- Emscripten 6.0.9; native cooking and legacy shader tools use OpenUSD 24.08 and Python 3.10.11. Acceptance uses Python 3.14.2, Pillow, Playwright and installed Chrome 154.0.8037.98. Browser visual checks enable SwiftShader; this establishes real-browser execution but not a hardware-specific WebGL performance result.
- Native tools/templates were deployed through `NauEditorPublic/build/latest-release/bin/Release/ProjectToolCmd.exe`. Editor templates and ProjectTool/Shared DLLs were also deployed to its Release editor directory. The editor's expected `NauEngineSDK` location was provisioned as a local junction to the existing SDK; this is ignored build state, not committed machine configuration.
- CLI project: `D:/Programming/Nau Generated Checks/2026-10-08/PortableStarter`, created by the deployed generator, outside the checkout with spaces in its path and a non-demo target name.
- Editor project: `D:/Programming/Nau Generated Checks/2026-10-08/EditorStarter`, created through the actual editor with template `empty`. User confirmation: "Created and opened; module compiled". The generated files, native DLL and compilation log were present. That check occurred before subsequent legacy-resource staging refinements; portable entry/declaration and game component sources were unchanged by those refinements. Final deployed generation and generated legacy Release builds were verified afterward.

## Portable builds and runtime evidence

All Windows/web Debug/Release combinations built through generated scripts and matching portable presets. A first Windows Debug preset build and a normal web Debug preset build performed host registration and fresh preparation without a separate cooking command. Explicit prepared-archive builds were exercised through both entry forms. Windows Release also built with deliberately unavailable HostSdk/HostTools/UsdSdk paths and an explicit Python interpreter, proving prepared-archive mode does not require cooking tools.

Final relocated production checks used one selected preparation snapshot, `PortableStarter/build/acceptance/shared-content.nau_pack`. All four delivered archives have SHA256:

`873ccb6403924bdafbce1930f33ba758e53e96980286603909a76176d6e3520e`

Fresh preparation was also repeated during freshness tests; final parity refers to this explicitly selected snapshot, not a claim that separate cooking runs produce identical records for unauthored identities.

| Delivery | Visible output | Lifecycle |
| --- | --- | --- |
| Windows Debug | 28,458 blue pixels; 26,313 orange pixels; observable motion | Running, resize/minimize/recovery, cleanup, exit 0 |
| Windows Release | 27,856 blue pixels; 26,090 orange pixels; observable motion | Running, resize/minimize/recovery, cleanup, exit 0 |
| Web Debug | Blue/orange meshes and observable motion | Running, repeated Stop, Stopped with cleanup complete |
| Web Release | 33,128 blue pixels; 30,522 orange pixels; observable motion | Running, repeated Stop, Stopped with cleanup complete |

Native deliveries were copied outside the checkout, launched from an unrelated working directory with a system-only PATH, and their actual drawable was captured through owned-window inspection. Browser deliveries were copied outside the checkout and served under `/nested/application/` with the staged isolation/no-store server. Assertions reject absent colors and unchanged frames. These checks use broad color regions and frame change, not pixel identity between backends. Existing rendering-specific observer coverage belongs to the preceding portable-scene-rendering change; it was not copied into generated production projects.

Per-configuration `results.json`, `first.png`, `second.png` and `runtime.log`, plus `archive-parity.json`, are under the external project's ignored `build/acceptance/`. Scene/geometry/material closure validation was performed by the shared preparation/runtime policy, and actual production rendering submitted the three mesh instances from that cooked closure.

## Generation, configuration and failures

`tools/project_tools/tests/verify_portable_generation.py` passed using deployed tools/templates. It exercises:

- Complete generated files, resolved non-demo names and the default rendering declaration.
- Scaffolding without engine SDK/source or EMSDK environment settings.
- Default `init --generate` selecting portable Windows Debug, explicit web generation and rejection of IDE opening for a preset without a Visual Studio solution.
- Native/web preset configuration; explicit alternate non-rendering selection; invalid declaration rejection.
- Selected target cleanup while sentinel files in other targets, host registration, prepared outputs and authored content survive.
- Rejection of project build root, outside-project, host-registration and shared-preparation cleanup paths.
- Rejection of a redirected child directory, with its destination sentinel preserved.

`verify_generated_build_failures.py` passed six checks: changed material invalidates preparation; script and preset builds reject invalid material; missing geometry fails; restoration/fresh preparation leaves authored inputs unchanged; and a prepared archive/profile mismatch fails. Failure logs and `results.json` are under `build/acceptance/failures/`. Accepted archive bytes were preserved on failed preparation. The generated ignore file was verified for build caches, native output and local preset settings.

An explicit alternate non-rendering declaration built and ran on Windows and web Debug after relocation. Both reached Running and completed Stop; its browser HTML has no renderer canvas. The final rendering preset was reset to the default declaration afterward.

## Legacy and existing-project compatibility

- Generated native host registration DLL compiled without Emscripten. The browser build used static project sources rather than that DLL.
- Generated legacy desktop Release compiled its shaders into `build/legacy-resources`, loaded the original empty legacy scene, opened its window and exited 0 after close. Its retained empty scene is not claimed as visible portable starter content.
- Legacy configuration explicitly reloads `config/scene.json`, preventing the portable startup configuration discovered alongside it from selecting another scene. Legacy resources are staged as a complete tree to avoid overlapping VFS mount behavior. Source resource changes invalidate that staging/shader output.
- Existing EditorProject rendering production checks passed Windows/web Debug/Release. Browser targets were rebuilt after the archive-path quoting correction.
- Existing EditorProject non-rendering Debug acceptance passed 18 native cases and 23 browser cases, including activation failures and Stop during pending work. Their acceptance packages were rebuilt with their fixture archive after an initial attempt revealed stale production-only staging.
- Existing EditorProject legacy Release still displayed the textured cube and sky, resized and exited 0. It retains the previously recorded `cache/dx12.cache` persistence warning/error at driver startup/shutdown; this change does not replace its SDK driver.
- Existing project files/default declarations were not migrated. Only the generated acceptance fixture was updated while testing template refinements. Root and component Git status confirmed no authored NauDemo/EditorProject changes.

## Reproduction

Provision the documented dependencies and environment locations. Use the generic generated README for portable/legacy selection and local overrides. Representative commands:

```powershell
cmake --build NauEditorPublic/build/latest-release --config Release --target ProjectToolCmd --parallel 8
python NauEngineModules/tools/project_tools/tests/verify_portable_generation.py --tools <deployed-tools-directory>
<deployed-tools-directory>/ProjectToolCmd.exe --tools <deployed-tools-directory> init --template empty --project '<external-parent>' --name PortableStarter --generate

# From the generated project:
cmake --preset portable-windows-debug
cmake --build --preset portable-windows-debug
./build.ps1 -Platform Web -Configuration Debug
./build.ps1 -Platform Windows -Configuration Release -PreparedArchive <selected-archive>
cmake --preset portable-web-release -DNAU_PROJECT_PREPARED_ARCHIVE=<selected-archive>
cmake --build --preset portable-web-release

# From the checkout:
python NauEngineModules/tools/project_tools/tests/verify_generated_delivery.py --project '<generated-project>' --target PortableStarterMain --platform Windows --configuration Debug
python NauEngineModules/tools/project_tools/tests/verify_generated_delivery.py --project '<generated-project>' --target PortableStarterMain --platform Web --configuration Release
python NauEngineModules/tools/project_tools/tests/verify_generated_build_failures.py --project '<generated-project>'
```

Repeat production checks for the other two configurations. Additional build/runtime logs and legacy screenshots are retained under ignored `NauEngineModules/build/project-generation-*`. ProjectTool path macros outside the documented supported source/preset/environment forms are rejected for cleanup rather than guessed. Native legacy Debug, arbitrary third-party templates, non-Windows host cooking, a newly published SDK and editor platform-selection UI are outside this acceptance.

## Requirement mapping

| Requirement | Evidence |
| --- | --- |
| Generated portable application | Deployed generation checks, external CLI project, user-confirmed editor creation, four production rendering runs |
| Consistent declaration selection | Default/alternate/invalid selection checks; script/preset matrix; selected archive hashes |
| Equivalent preparation/build behavior | First preset builds, freshness/failure suite, missing-cooking-tool prepared build |
| Isolated generation/rebuild operations | Sentinel cleanup checks and unsafe-path/redirected-child rejection |
| External locations/provisioning | External path with spaces, explicit environment locations, no-SDK scaffolding, generated ignore checks |
| Legacy/native editor compatibility | Host DLL build, user-confirmed editor module loading, generated and existing legacy Release runs |
| Generated-project acceptance | All checks above, relocation/nested URL evidence, recorded revisions and explicit limits |

Strict OpenSpec validation and Git whitespace checks passed at final completion.
