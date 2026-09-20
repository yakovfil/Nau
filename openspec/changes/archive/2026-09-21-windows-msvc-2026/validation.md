# Implementation evidence

Implementation started 2026-09-20. Working tree changes are not committed. Logs and source identities are under `NauEngineLite/build/windows-msvc-2026-evidence/`; `inputs.json` records base revisions and the modified-working-tree status.

## Completed checks

- Engine/editor/exported SDK preset inheritance checks pass; browser preset objects match their pre-migration definitions. Template/editor preset listing succeeds.
- Real native VS configuration selects MSVC 19.51.36257.0, v145 and Windows SDK 10.0.26100.0 with CMake 4.2.1. Ninja/MSVC configuration also succeeds using the VS 18 developer environment.
- Real VS 2022 and VS 18 with v143 configurations fail with migration diagnostics. An explicitly unavailable VS 18 instance fails without fallback.
- Four native guard tests pass, including obsolete inputs, architecture, clang-cl family discrimination and browser bypass. Four NauDemo fast-builder tests pass, including obsolete engine inputs and missing eligible MSBuild.
- Clean native minimal Debug and Release builds and their lifecycle CTest suites pass.
- Full static desktop Debug build succeeds. Its CTest run passes 579/580 cases, with the failure described below.
- NauDemo fast-builder Debug build succeeds against the new static engine outputs using MSBuild 18 and a v145 project.
- Demo-profile Debug/Release graph checks pass on native and browser configurations, including source diagnostics and unchanged browser preset assertions. Scene probes also pass on native, Node and Chrome in Debug/Release.
- Editor configuration succeeds with the existing Qt/USD dependency inputs after raising the editor-owned zlib and Countly overlay policy minima to CMake 3.5. Editor Debug/Release compilation and user runtime acceptance are now complete, as recorded below.

## Resolved thread-local test failure

`TestThreadLocalValue.MultipleThreadsReuse` crashes/fails under the new Debug compiler. The focused rerun reports a changed pointer-set size, invalid debug-heap pointers and SEH 0xc0000005. The test concurrently inserts into one `std::unordered_set` without locking its declared mutex, which is undefined behavior. No production thread-local defect has been established.

The existing VS 2022 binary passes ten repetitions, which does not establish that the test is race-free. Logs: `static-debug-tests.log`, `thread-local-repro.log`, `thread-local-vs2022.log`. The user approved the synchronization fix. Both insertions now use the declared mutex; thread-local value access remains concurrent. The fixed test passes 20 repetitions each under VS 2026 Debug, VS 2026 Release and VS 2022 Debug. The complete VS 2026 Debug runtime executable passes all 410 tests. The historical VS 2022 comparison rebuilt only the test project against its existing dependencies, without restoring VS 2022 support in the current build configuration.

## Further validation findings

- The full static Release build also succeeds. The initial Release runtime run hangs in `TestSpinLock.MultipleSubsequentLockMustFail`: it deliberately locks twice and expects an assertion, but `NAU_ASSERT_ENABLED` is absent in Release. A bounded full CTest run identified six failures in total. The user authorized temporary exclusions; all six names and reasons are recorded in the root `failed-tests.md`. With the explicit exclusion file, Release CTest reports 569 passed, zero failed, five existing skips and six excluded tests in 13.08 seconds. This is a qualified validation result, not proof that the deferred tests are fixed. The focused thread-local Release test passes 20 repetitions and remains enabled.
- Editor Debug compilation initially failed in Qt 6.4.1 `qvarlengtharray.h` because its iterator macros refer to `stdext` helpers removed in MSVC 14.51. The reproducible `scripts/prepare_qt_for_msvc.py` backport now applies the upstream portable fallback, preserves the SDK binaries and backs up its header. Both script tests and idempotence checks pass; editor Debug compiles and links with Qt 6.4.1/OpenUSD 24.08. Release also compiles and links; the user accepted runtime checks in both configurations on 2026-09-21.
- Qt reference: https://github.com/qt/qtbase/blob/6.8/src/corelib/global/qcompilerdetection.h
- MSVC removal reference: https://devblogs.microsoft.com/cppblog/c23-support-in-msvc-build-tools-14-51/

## User visual acceptance

The user confirmed all six VS 2026 source-build runs: SceneBaseSample and inputDemo from `build/windows-msvc-2026-static/bin/{Debug,Release}`, and NauDemo through `run.ps1 -Configuration {Debug,Release}`. Expected scene/input behavior and normal shutdown are accepted. This does not cover the separately relocated SDK runtime checks. NauDemo CMake and fast-builder Debug/Release compilation logs are preserved in the evidence directory.

On 2026-09-21, the user confirmed both editor configurations from `NauEditorPublic/build/windows-msvc-2026-editor/{Debug,Release}/NauEditor/NauEditor.exe`: startup, opening a known working project, viewport/basic interaction and normal close all pass. This validates the retained Qt 6.4.1/OpenUSD 24.08 integration under MSVC with the recorded compatibility fixes. It does not resolve the separate clang-cl or relocated SDK findings.

## Additional compiler and delivery checks

- ASAN Debug and static RelWithDebInfo representative `NauKernel` builds succeed. Native MSVC DLL Debug/Release outputs also compile/link as part of the completed editor builds.
- The native/Node/Chrome scene suite passes in Debug/Release (`build/demo-scene-evidence/results.json`). All four ordinary browser packages rebuild with SDK 6.0.9. The 56-case minimal/demo delivery matrix passes expected outcomes, including rejection of deliberate runner/blank-image faults (`browser-packages/results.json`). Separate Debug/Release fixture trees with `NAU_DEMO_TEST_HOOKS=ON` pass camera and pending-scene checks. Normal delivery trees retain hooks OFF. Package staging also passes exact inventory, hashes, stale removal and missing-input preservation checks. Delivery runners test copied packages independently of the build tree.
- Editor Debug and Release Qt UI validation each record eight successful cases including setup/cleanup. The first unit executable incorrectly ran zero tests after test libraries inherited DLL linkage; that is not a pass. Restoring static linkage of the editor's test libraries resolves registration: Debug passes all 64 unit tests; Release passes 60 and fails four assertion/death tests. With only the four recorded exclusions, Release passes all 60 selected tests. Logs: `editor-debug-unit-tests.log`, `editor-release-unit-tests.log`, `editor-release-unit-with-skips.log`; Release Qt UI XML: `editor-release-ui-tests.xml`. The user accepted editor startup, project/resource loading, viewport/basic interaction and normal close in both configurations on 2026-09-21. The four deferred Release test failures remain excluded, not fixed.
- clang-cl 22.1.3 exposed an undeclared helper in the Clang-only `v_abs` branch. It now uses the existing SSE2 sign-bit implementation also used by MSVC. Static kernel/scene and DLL kernel build results and remaining blockers are detailed below.

## Fresh native reproduction (2026-09-21)

Fresh local Git clones at `D:/Programming/NauVs2026-fresh-validation` contain Nau, NauEngineLite, NauSamples and the recorded engine Google Test submodule. Each clone checks out its recorded base revision, then applies a binary working-tree patch and individually hashed untracked source files. No build directories, native caches, libraries or generated projects were copied. No commits were created. `build/windows-msvc-2026-evidence/native-fresh/results.json` records revisions, hashes, every command and `passed: true`; `reproduce-native.py` preserves the walkthrough driver.

From the fresh engine directory, the validated commands are:

```powershell
foreach ($configuration in @('Debug', 'Release')) {
    $build = "build/native-minimal-vs2026-$($configuration.ToLower())"
    cmake --preset "native-minimal-$($configuration.ToLower())" -B $build -DNAU_MINIMAL_TESTS=ON
    cmake --build $build --config $configuration --target MinimalAppSample NauMinimalLifecycleTests --parallel 4
    ctest --test-dir $build -C $configuration --no-tests=error --output-on-failure
}
```

Both configurations build and pass `MinimalRuntime.Lifecycle`. The build leaves tracked source unchanged. This is fresh-checkout reproduction of the native minimal profile with the documented VS 2026/CMake prerequisites, not a claim that the full editor was rebuilt in this second checkout.

## clang-cl compatibility findings and resolutions

Static `NauKernel` and `SceneBaseSample` compile/link with LLVM 22.1.3; DLL `NauKernel` also links. The VFX include now names its public `nau/scene/scene_manager.h` path instead of relying on MSVC's enclosing include search. Google Test now compiles after the explicit-cast preparation. Static Debug runs all 410 tests: 409 pass and `TestAsyncFunctions.WhenAll_NoTimeout` raises `0xC000001D`. With that exact user-approved exclusion, all 409 selected tests pass.

The wider DLL/runtime graph initially failed compiling OpenUSD 24.08's `childrenProxy.h:58` (`SdfChildrenProxy` has no `_Set`) and its bundled TBB `task.h:590` (static member initializer is not a constant expression). The reproducible `prepare_clang_dependencies.py` resolves both header errors under Clang while retaining the MSVC-preprocessed declarations. The DLL build also needed Boost auto-link disabled on USD consumers: imported targets already specify the producer libraries. No package version or compiler diagnostic is bypassed. The DLL graph now compiles and links; its runtime results are recorded in the final matrix below. Logs: `clang-static-scene.log`, `clang-static-build-after-includes.log`, `clang-dll.log`.

Relocated SDK `ScriptsSample` launches and closes with exit code zero in Debug/Release. Its Debug log also reports an empty world without a camera and a missing pipeline-cache output directory, so this is not a clean rendering acceptance claim. MinimalAppSample runs its expected indefinite non-window loop and was stopped by the validation driver; this is not a shutdown pass. The earlier relocated inputDemo shutdown failures remain deferred and separate from the user's source-build acceptance. Task 4.5 resource discovery is now verified as detailed below; shutdown failures remain deferred.

## Relocated SDK resource proof (2026-09-21)

Task 4.5's Debug/Release minimal, scene, input and script consumers were built from the installed SDK at `D:/Programming/NauSdkVs2026-validation`. A validation-only trace was inserted in the copied SampleCommonLib's existing resource resolver, then scene/input/script binaries were relinked and launched from their SDK `bin/{Debug,Release}` directories. All six runs report only canonical sample roots below the relocated SDK. No `NAU_SAMPLES_ROOT` source-checkout compile definition is present in the installed consumer project. `sdk-resource-results.json` validates each path and its sample marker. The copied source was restored after the trace run; engine and NauSamples source were not instrumented.

The non-rendering minimal consumer uses no sample assets and starts its indefinite loop. The six traced consumers resolve sceneBase/shared and per-sample configuration roots from the SDK, so this completes resource-discovery acceptance. Earlier inputDemo shutdown failures remain in `failed-tests.md` and are not relabelled as successful shutdowns. The trace is deliberately separate from native human visual acceptance.

## Header preparation validation

Preparation tests pass for LF/CRLF, idempotence, preserved backups and refusal of unknown input before editing another header. `tbb-layout.log` compiles/links a layout probe with MSVC 19.51 and clang-cl 22.1.3 against the existing TBB binary; both report `kind=4 context=256 alignment=8`, and compile-time checks verify an `int` enum representation. Header changes retain MSVC preprocessing for USD/TBB. Static `NauKernel`, `SceneBaseSample` and `test_runtime` build with prepared Google Test; runtime results and the single exception are recorded above. See `cmake/probes/windows_toolchain/README.md` for reproducible preparation and original-header restoration.

## Final acceptance review (2026-09-21)

Implementation is complete under the user's explicit decision to defer observed test failures. Deferred checks remain unresolved in `failed-tests.md` and are not counted as passes. This decision does not waive compiler/build compatibility: both selected clang-cl graphs now build, including the USD-linked DLL dependencies. No new package major version, compiler version guard bypass, or diagnostic suppression was introduced.

| Required area | Result / evidence |
| --- | --- |
| VS 18/v145 identity and unavailable/obsolete inputs | Passed real VS/Ninja configurations and rejection probes; source/tool identities in `inputs.json` |
| Public presets and native helpers | Engine/editor/SDK/templates/demo/probes select VS 2026; four guard and four fast-builder regression checks pass |
| Static desktop and samples | Debug/Release builds pass; 24 sample/configuration outputs verified; all six source visual/input/close runs accepted by user |
| MSVC runtime tests | Debug runtime 410/410 pass; Release 569 pass, five existing skips and six explicitly deferred exclusions |
| DLL / ASAN / RelWithDebInfo | Representative affected targets compile/link; editor includes full native DLL Debug/Release graphs |
| Qt 6.4.1 / OpenUSD 24.08 editor | Both configurations build and user accepts startup/project/viewport/interaction/close; Debug unit 64 pass, Release 60 pass with four deferred exclusions; UI eight cases each including setup/cleanup |
| clang-cl static Debug | LLVM 22.1.3 kernel/scene/runtime-test targets build; 409 tests pass with one deferred async exclusion |
| clang-cl DLL Debug | Kernel, USD-linked dependencies and runtime-test target build; 406 tests pass with four deferred async/allocator exclusions |
| Relocated SDK | Minimal/scene/input/script consumers build in Debug/Release; six traced resource resolutions remain inside relocated SDK; separate input shutdown failures are deferred |
| Browser independence and regression | Four SDK 6.0.9 packages build; 56 delivery scenarios, four controlled fixture scenarios, staging and native/Node/Chrome scene probes pass |
| Fresh native reproduction | Fresh local clones plus hashed working-tree patches, no copied outputs; minimal Debug/Release builds and lifecycle tests pass |
| Documentation and scope | Current prerequisites/preset mappings/clean-cache commands and dependency preparation updated; historical VS 2022 evidence retained |

Clang final evidence: `clang-static-prepared-build.log`, `clang-static-runtime-ctest.log`, `clang-static-runtime-with-skips.log`, `clang-dll-prepared-link-build.log`, `clang-dll-runtime-tests.log`, and `clang-dll-runtime-with-skips.log`. Static filtered runtime took 7.31 seconds; DLL filtered runtime took 16.94 seconds. The DLL allocator failures are not inferred fixed from static success.

The Google Test dependency checkout was restored after verification; its prepared/original headers are preserved in the ignored evidence directory. Run the tracked preparation helper before subsequent clang-cl builds. USD/TBB preparation retains its original headers beside the installed SDK. These are dependency setup steps, not new submodule revisions. Generated editor translation changes were restored. No commits or pushes were performed.

`final-inputs.json` records the final base revisions, working-tree patch hashes and untracked source hashes, plus prepared dependency-header hashes. This identifies the uncommitted implementation precisely; no build is attributed solely to its unchanged base commit.

Final review: 21/21 implementation tasks complete under the recorded test-deferral decision. Strict OpenSpec validation and whitespace checks pass across the root and affected repositories. Failed test cases remain explicitly deferred in the failure ledger; none is counted as a pass.
