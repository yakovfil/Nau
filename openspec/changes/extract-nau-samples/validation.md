# Validation

Final result on 2026-09-20: extraction implementation and required migration acceptance are complete. Native builds and user visual acceptance, relocated SDK samples, browser acceptance and fresh committed-source reproduction pass. The chronological checkpoints below retain earlier failures and their resolution. All changes are committed locally; remote publication has not been performed.

## Source and extraction checkpoint

Implementation began on 2026-09-20. Baseline engine: 02574c7104725c6c60358c7d579a0e11da2f174b; demo: 6c3b738209cb5aa5e2ff1cd6fc7cba5452aa1919; parent: 66e8148. NauSamples initially contained commit bcf3bf4 and its LICENSE. Detailed initial identities and tracked sample inventory are in NauEngineLite/build/extract-samples-evidence/source-identities.json and source-tree.txt.

History was extracted in a disposable independent local engine clone using git subtree split --prefix=samples --branch extracted-samples. The extracted commit is b460dfaad4777ba4cfcd7d8ece808373ffa73b74. Its tree and the engine HEAD:samples tree are exactly 2477f7305511c21453dc164b1115aaffd9612c9b (414 tracked files). The destination merge is 81f3aee53ca57f4c8442f5a69359ec0fc25d6e1a; ancestry checks passed for both bcf3bf4 and the extracted commit. Existing engine history was not rewritten. No remote publication occurred.

Native baseline builds run per target/configuration in build/naudemo-desktop. Results and logs are recorded under build/extract-samples-evidence. Integration and final acceptance remain pending; this checkpoint does not claim the extraction is fully integrated.

## Integration checkpoints

All 24 native baseline builds passed: all3rdparty, AssetDbSample, AssetPackSample, inputDemo, KernelApp, MinimalAppSample, NetworkTransportSample, PhysicsSample, SceneBaseSample, ScriptsSample, UiSampleApp and NauDemo, each Debug/Release. The extracted file-accounting check identifies 406 unchanged files and eight integration-edited paths; all 414 original paths are present. Original ignored outputs were moved to build/extract-samples-old-generated rather than used as migration inputs. The extracted engine tree has been removed and NauSamples registered locally.

External source contract checks pass for desktop/minimal/custom paths with spaces, missing required sources and sample-free profiles. Both actual minimal browser presets build; a separate custom samples path and build path containing spaces also configure and build the package. Minimal graph checks pass in native Debug/Release and browser Debug/Release. Browser demo graphs configure and build with a deliberately unavailable samples path, confirming no new dependency. Preset objects remain unchanged.

All nine existing minimal delivery scenarios pass with expected outcomes in both configurations, including relocated serving, visibility, failure and intentional runner rejection. The staging/server unit checks pass. The demo image runner reported a near-edge depth/shading mismatch in its first migration run; that failed result is retained in demo-debug/success. A preserved pre-migration package passes its comparison run. No migration rendering success is inferred from that comparison; further demo acceptance remains pending.

Clean native Debug builds pass from build/external-samples-native. Release and SDK validation are still in progress. SDK installation first required additional ozz library targets not built by sample targets; missing output diagnostics are not treated as successful SDK installation. Detailed commands/logs remain under build/extract-samples-evidence.

## Native and browser follow-up

All 24 clean native target/configuration builds now pass. Native minimal lifecycle CTest passes in Debug and Release. SDK installation completes after building ozz_options, ozz_animation_offline, ozz_animation_tools, gltf2ozz, ozz_geometry, gmock, gmock_main, gtest_main, Audio and Shared; sample-only targets do not build every installed library. A relocated SDK configures after adding the missing miniaudio import, and MinimalAppSample, SceneBaseSample and inputDemo compile against it in Debug. Further installed runtime checks are pending.

The user approved replacing the single center-pixel demo assertion with multiple geometry-selected interior pixels at least 12 pixels from triangle edges. The same 22/channel shading tolerance and nearest-depth selection remain; both captured orientations are checked and at least four interior samples are required. All 19 default demo scenarios per Debug/Release pass with expected outcomes, including blank-image and deliberately broken-runner rejection. Detailed current results are in demo-final-{debug,release}; earlier failures remain separate.

The user reported inputDemo crashing during native visual acceptance. Agent reproduction confirmed Debug exited with Windows breakpoint exception 0x80000003. The fault maps to eastl::AssertionFailureFunctionDefault. Candidate saved-stack return addresses (not a verified unwind) include EASTL aligned node allocation and Device::createAdditionalSwachain; the original allocator::allocate(n, alignment, offset, flags) ignored alignment and called malloc. The pre-migration executable from build/naudemo-desktop reproduced the same exit code and last application message using a separate baseline runtime fixture that exposes current assets under the old samples layout. This fixture is under build and does not restore an engine-local samples tree. Logs, process records and dump analysis are in input-*.log/json and input-Debug-stack.txt. The first agent-launched Release process did not close through its main-window close request and was terminated after recording the timeout.

## Approved allocator repair

The user explicitly approved the focused allocator fix with regressions. The engine-owned EASTL allocator now uses portable malloc-backed metadata for both allocation overloads, preserving size, alignment and offset for reallocation and matching deallocation. Invalid alignment and allocation-size overflow return null; failed reallocation preserves the original block. No bundled third-party file was edited for this repair. The allocation header costs four machine words plus alignment padding, and reallocation copies to a new block.

The new AlignmentAndOffsets regression failed against the old implementation (`allocator-before-test.log`). After repair, all 15 allocator tests pass in both Debug and Release (`allocator-related-{Debug,Release}-test.log`), and the complete Debug runtime executable passes all 410 tests (`allocator-runtime-direct-Debug.log`). A broad CTest invocation was not clean: its shared generated discovery file selected the Release executable despite `-C Debug`, causing three assertion-dependent lock cases to fail/time out; seven other targets were unbuilt. Those six lock tests pass when run directly in Debug, and the full direct Debug run also covers them. The failed CTest log is retained and is not counted as a passing full CTest suite.

Both rebuilt inputDemo configurations remained running for 15 seconds with two visible NAU windows, then exited normally with code 0 after WM_CLOSE was posted to both windows. No forced termination was needed. Executable identities, process IDs and window records are in `input-fixed-{Debug,Release}-process.json`; stdout/stderr logs use the same prefix. The scripted run verifies startup/window creation/close. On 2026-09-20, after reviewing the repair results, the user explicitly confirmed: "Visual input-behavior is accepted". This supplies human visual acceptance for inputDemo. Task 4.2 remains incomplete for the separately required SceneBaseSample and NauDemo visual acceptance; this inputDemo confirmation is not recorded as acceptance of those applications.

Minimal and demo browser Debug/Release packages rebuild with the allocator repair. Chrome success checks pass for all four packages, including update/render progress and Stop cleanup; minimal checks serve the relocated package outside the workspace. Logs are `allocator-web-{minimal,demo}-{debug,release}-{build,run}.log`, with demo structured results under the corresponding `allocator-web-demo-*` directories. Minimal structured results are copied to this evidence directory. These are post-repair success checks; the full failure matrices recorded above preceded the allocator repair. Strict OpenSpec validation passes.

Independent fresh-checkout minimal/demo Debug/Release validation completed successfully before the allocator repair (`fresh-walkthrough.log`); it does not establish reproduction of the later allocator patch. Final SDK validation remains pending: adding ScriptsLua discovery exposed a missing installed public include directory, recorded in `sdk-relocated-configure.log`.

## Native visual acceptance completed

On 2026-09-20, after inputDemo acceptance was recorded and the remaining SceneBaseSample and NauDemo visual acceptance was identified, the user confirmed "both is accepted". This supplies the remaining human acceptance for the documented native Debug/Release checks and supersedes the earlier pending status for those applications. Task 4.2 is complete based on the recorded automated inputDemo startup/close checks and the user's explicit visual acceptance of all three applications. Other migration tasks remain independently tracked.

## Final integration verification

The installed SDK dispatcher now imports miniaudio, lua, LuaToolkit and ScriptsLua so migrated target discovery retains scripting support. ScriptsLua has no public include tree; its stale export/install paths were removed, and LuaToolkit exports its actual installed headers. ScriptsSample's installed link-directory assignment now names its own target. Final native configure and all 24 target/configuration rebuilds pass (`final-native-*.log`), as do both native NauDemo fast builds with explicit `--samples NauSamples` (`final-demo-fast-*.log`). The earlier clean native log records shader-cache generation under the new NauSamples sceneBase tree and UI sources.

The complete Debug SDK installation was copied to `%TEMP%/nau-extracted-samples-sdk-final-20260920`. Configuration and builds of MinimalAppSample, SceneBaseSample, inputDemo and ScriptsSample pass (`final-sdk-{install,configure,build}.log`). Inventory verifies all 414 original tracked sample paths, exclusion of Git/build-directory metadata, and no original checkout paths in compile sources or include directories across 26 generated sample projects (`final-sdk-inventory.json`). From the relocated SDK root, SceneBaseSample and inputDemo stay running for 15 seconds, create one and two visible windows respectively, then exit 0 after close requests without forced termination (`sdk-runtime-*-process.json` and stdout/stderr logs). Runtime lookup therefore uses the installed layout; existing DX12 validation/cache warnings remain in the captured logs and are not attributed to extraction.

External-path contract checks and browser/native demo graph checks pass again (`final-demo-graph.log`), including missing-source diagnostics and unchanged presets. Camera and pending-scene browser fixtures pass in Debug and Release (`final-fixtures-*/*/results.json`). Both normal delivery configurations are restored to `NAU_DEMO_TEST_HOOKS=OFF` and rebuilt. Current guides document external roots, the SDK build/install/relocation commands, and component-first publication. Existing absolute SDK installation destinations require using the preset's configured output directory and then copying the completed installation; `--prefix` override support was not introduced.

## Coordinated revisions and scenario coverage

Parent implementation commit: `c6ab80a` (`Extract NauSamples into a coordinated submodule`). Final validation-record updates may follow in the parent only; they do not change the component build inputs below.

| Repository | Validated component revision |
| --- | --- |
| NauEngineLite | `18fa929a2bbb30a53a37cf1e4cc14b8ae272aaee` |
| NauSamples | `10f0403e3f2e05611c8d297f27b9a4647501398b` |
| NauDemo | `f9aef46e275860f1883a48bdcace0c86d3dfe228` |
| NauEditorPublic (unchanged) | `ee980c3cb7eaa540e4dbb85ef869630ba7afbeb7` |
| NauDocsPublic (unchanged) | `f252ec3562112910d50cc153943860e811d18bbf` |

Final file accounting records 414 retained original paths: 405 unchanged Git blobs and nine integration edits (`final-file-accounting.json`). The nine edited paths are the root CMake dispatcher, networkTransport configuration, sample_common CMake/header/implementation, sceneBase CMake, scriptUsage CMake, and UI CMake/configuration. Original engine and destination license texts are unchanged; both imported-history ancestors remain reachable. The engine no longer contains a samples tree, its presets and nested submodule definitions are unchanged, and unrelated parent gitlinks are unchanged.

A separate clone of parent `c6ab80a` successfully runs `git submodule update --init NauSamples` using an explicit local URL override and checks out exactly `10f0403` (`final-submodule-init.log`). The committed URL remains `https://github.com/yakovfil/NauSamples.git`. This is evidence of local revision availability; no component or parent push was performed.

| Spec scenario | Evidence |
| --- | --- |
| Extraction audited | Exact pre-edit tree match, ancestry checks, final 414-path accounting and original licenses |
| Recorded repositories initialized | Fresh parent clone and real NauSamples submodule initialization at its recorded gitlink |
| Default/custom checkout | Compiler-free source contract plus actual minimal build with spaces in source/build paths |
| Required checkout unavailable | Missing/invalid source diagnostics; deleted minimal entry-point negative check |
| Engine-only selection | Sample-free desktop/minimal contract checks and actual demo graph with unavailable samples path |
| Native consumers run | 24 native target/configuration builds, both fast demo builds, user acceptance for all three visual applications |
| Over-aligned native allocations | Old-test failure, 15 allocator tests per configuration, 410 Debug runtime tests, clean inputDemo startup/close |
| Browser consumers exercised | Nine minimal and 19 demo scenarios per configuration, four camera/pending-scene fixtures, post-repair startup/Stop checks |
| Installed SDK relocated | 414-file SDK inventory, four representative sample builds, two asset-using sample launches outside checkout |
| Exact minimal entry point | Native/browser source and dependency graph audits, with unchanged profile exclusions |

After restoring normal delivery builds, complete demo packages were copied outside the checkout to `%TEMP%/nau-extracted-demo-final-{debug,release}-20260920`. Both pass rendering, rotation, resize and Stop checks at `/relocated/demo/` (`final-demo-relocated-*/results.json`). Minimal success checks also use relocated packages and real visibility changes. Earlier failed probes remain in the evidence directory and are distinguished from later passing results above.

## Final fresh committed-source walkthrough

With SDK 6.0.9 activated, ran:

```powershell
python -B NauDemo/web/reproduce.py --destination "$env:TEMP/nau-extracted-samples-final-repro-20260920" --sdk C:/Users/Yakov/emsdk
```

All 24 recorded helper commands succeed: four independent local clones/checkouts, tool identity checks, and minimal/demo configure/build/Chrome acceptance in Debug/Release. Parent input is `c6ab80a808e7651d1c9ca4db14ea81362fa585e6`; component inputs exactly match the table above. Every repository has the empty patch SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` and no copied untracked files. Builds leave tracked source unchanged. Minimal update/Stop and demo rendering/Stop pass in both configurations. Final results, command logs, tool identities and browser evidence are preserved under `NauEngineLite/build/extract-samples-evidence/final-fresh/`, with the main invocation log at `final-fresh-walkthrough.log`.

A separate configure in this fresh checkout with an unavailable `NAU_SAMPLES_SOURCE_DIR` fails with the expected missing-input and initialization/override guidance (`final-fresh-missing-samples.log`). This completes the fresh-checkout and migration-completion scenarios. Strict OpenSpec validation passes. The only parent changes after the tested implementation revision finalize this validation record and task checkboxes; component build inputs remain unchanged.
