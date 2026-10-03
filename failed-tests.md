# Temporarily skipped tests

## Standard-library migration relocated SDK runtime (2026-10-03)

Later repair and rerun: Release inputDemo's 0xc0000005 crash came from an additional swapchain's COM descriptor heaps being destroyed by the static DX12 API state after the device had shut down. The driver now releases still-open additional swapchains before device teardown. The existing DX12 swapchain test now covers a window left open through driver teardown and passes in Debug/Release. The relocated SDK's SceneBaseSample/inputDemo Debug/Release early-close runs each pass 3/3; inputDemo secondary-first close also passes both configurations. The final relocated SDK generated consumer builds and launches/closes in both configurations. Evidence is `NauEngineLite/build/sdk-final-verified-runtime/results.json`, `sdk-swapchain-fixed-primary/results.json`, `sdk-swapchain-fixed-secondary-first/results.json`, and `sdk-final-dx12-suite-{Debug,Release}.log`. Earlier crash results below remain historical; no exclusion was added. Logs still report DX12 pipeline-cache file errors even after creating the SDK `cache` directory (`sdk-cache-directory-check`); the Dagor relative-path file API has no registered base path in this run. The empty generated consumer also reports missing default assets. Those diagnostics are separate from the now-repaired crash.

Startup-drain ordering repair: MainLoopService now owns the delegate startup task and waits for it before scene teardown, while scene queues and concurrent systems remain available. Startup rejection is reported after scene cleanup. Native minimal lifecycle tests pass, including new pending-startup and rejected-startup regressions. Framework and relocated installed samples rebuild in Debug/Release. The five-second primary-window close probe passes SceneBaseSample Debug/Release and inputDemo Debug, each 3/3. inputDemo Release still crashes with 0xc0000005, 3/3; the separate driver teardown failure remains unresolved. Evidence: `NauEngineLite/build/sdk-startup-drain-early-close/results.json` and adjacent per-run logs, `sdk-startup-drain-minimal-tests.log`, and `sdk-startup-drain-application-tests.log`. Task 7.5 remains open; no exclusion is added. Earlier SceneBaseSample failures below describe the pre-repair binaries.

Investigation follow-up: `CloseMainWindow()` selected inputDemo's secondary window, which is explicitly created with `exitAppOnClose=false`. The earlier inputDemo timeouts therefore do not establish an application shutdown hang. The new primary-window probe (`cmake/probes/sdk_shutdown/run.py`) targets the initial NAU window at (10, 10) and records real process exit codes. With restored production binaries and the five-second close delay, SceneBaseSample Debug crashes, inputDemo Debug exits zero, SceneBaseSample Release exits zero, and inputDemo Release crashes (`sdk-shutdown-restored-early-close/results.json`). With a 20-second close delay, SceneBaseSample Debug/Release and inputDemo Debug exit zero, while inputDemo Release still crashes (`sdk-shutdown-late-close/results.json`). Windows reports the Release inputDemo fault in D3D12Core.dll 10.0.26100.9278 at offset 0x53b7e, after graphics shutdown completes; its native stack/cause is not yet established. Fault events are preserved in `sdk-shutdown-windows-faults.json`.

SceneBaseSample Debug fault RVAs resolved through its PDB to `TextureAssetView::createFromAssetAccessor` (`texture_asset.cpp:110`, dereferencing the GPU texture) and, during an experimental rebuild, `SceneManagerImpl::activateComponents`' activation finalizer (`scene_manager_impl.cpp:297`). The delegate startup task is not awaited before `ApplicationImpl` starts scene teardown; the code and early/late-close comparison identify a pending-startup lifetime hazard. A render-only experiment awaiting each scene update did not fix the failure (SceneBaseSample Debug crashed 3/3); it was reverted, and original Graphics libraries and installed samples were rebuilt in both configurations. A broader startup/shutdown ordering decision is needed rather than adding an exclusion. Task 7.5 remains open.

Task 7.5 remains open. After a clean MSVC static Debug/Release rebuild/install and relocation to `C:/temp/nau-std-sdk-20261003-relocated`, SceneBaseSample Debug launches but exits with `0xC0000005` after a main-window close request. Its Release counterpart and the generated StdSdkConsumerMain in Debug/Release exit zero. Both relocated inputDemo configurations launch but do not finish within the 15-second close timeout and require termination. Debug inputDemo timeout was already deferred; Release now times out rather than reproducing the earlier access violation. These are failed shutdown checks, not passes or newly authorized exclusions. Logs and exact process results: `NauEngineLite/build/replace-eastl-sdk-final-*.log` and `replace-eastl-sdk-runtime-final-results.json`. The initial PowerShell probe returned null exit codes and is superseded by the Python-owned process probe, which records actual exit codes. SceneBaseSample logs also report DX12 pipeline-creation and outstanding-buffer diagnostics; no cause or migration attribution is established yet.

## Standard-library migration editor visual acceptance (2026-09-22; scheduler fix 2026-09-24)

The previously reported Debug editor assertion while loading `C:/temp/test1/test1.nauproject` was traced to `ResourceScheduler::scheduleEvents` dereferencing `eventStorage.end()`. The invalid iterator use was replaced with the reserved contiguous-storage insertion pointer and an explicit empty-span path. The affected `Graphics` and `test_runtime` Debug targets rebuild successfully after the fix. The editor project has not yet been relaunched for a new human acceptance result; task 7.7 remains open.

## EASTL replacement baseline (2026-09-21)

The isolated `cmake/probes/standard_library` baseline has an additional known failing case: `eastl_baseline --trivial-assignment`, reproduced in VS 2026 MSVC Debug and Release. Growing a fixed vector from two to three elements reports only one live instance for a type with nontrivial constructors/destructor and defaulted trivial assignment. Bundled `EASTL/memory.h` selects its uninitialized move shortcut using `is_trivially_copy_assignable`, bypassing construction of the two relocated elements. The case exits 1 and is retained as a separately invoked negative baseline, not a passing default CTest case or a fixed bug. The ordinary nontrivial-assignment fixture is a separate passing case. Standard-container replacements must retain regression coverage for the failing shape. Evidence: `openspec/changes/archive/2026-10-03-replace-eastl-with-std/baseline-results.json` and `NauEngineLite/build/replace-eastl-baseline/trivial-assignment-{Debug,Release}.log`.

## VS 2026 migration exclusions

User-authorized on 2026-09-20 for `windows-msvc-2026` validation. These failures are deferred, not fixed or counted as passes. Exclusions apply only to the Release validation command below; Debug coverage remains enabled. Test source and default CTest registration are unchanged.

Tested tools: VS 2026, MSVC 19.51.36257.0/v145, Windows SDK 10.0.26100.0, CMake 4.2.1.

| Test | Configuration | Observed failure | Follow-up |
| --- | --- | --- | --- |
| `TestSpinLock.MultipleSubsequentLockMustFail` | Release | Hangs on the second lock; timed out after 10 seconds. The recursive-lock assertion check is compiled out. | Make assertion-dependent coverage configuration-aware before removing the exclusion. |
| `TestSpinLock.DestructWhileLockedMustFail` | Release | Expected an assertion when destroying a locked mutex; assertions are disabled. | Review assertion-dependent coverage. |
| `TestRecursiveSpinLock.DestructWhileLockedMustFail` | Release | Expected an assertion when destroying a locked recursive mutex; assertions are disabled. | Review assertion-dependent coverage. |
| `TestAssetPath.ConstructFromInvalidString` | Release | Expected three assertion reports, received zero. | Separate invalid-input behavior checks from assertion checks. |
| `TestAssetPath.SetScheme` | Release | Expected an assertion report, received zero. | Separate setter behavior checks from assertion checks. |
| `TestAssetPath.SetContainerPath` | Release | Expected an assertion report, received zero. | Separate setter behavior checks from assertion checks. |

The machine-readable list is [failed-tests-release.txt](NauEngineLite/cmake/probes/windows_toolchain/failed-tests-release.txt). Run from `NauEngineLite` with CTest 4.2.1:

```powershell
ctest --test-dir build/windows-msvc-2026-static -C Release --timeout 30 --output-on-failure --exclude-from-file "$PWD/cmake/probes/windows_toolchain/failed-tests-release.txt"
```

Only these exact names are excluded. New failures must be recorded explicitly; this command does not suppress arbitrary failures. To retry the deferred tests, omit `--exclude-from-file` and retain a timeout to bound the double-lock hang.

## clang-cl 22.1.3 clean static Release observations (2026-09-25)

The clean clang-cl static Release graph in `NauEngineLite/build/replace-eastl-clang-static-release` builds successfully after the standard-library migration. Its full CTest run reports 8 failures: the six existing assertion-dependent Release exclusions listed above, plus the following two clang-cl-specific results. These are not converted into passes and are not related to the removed EASTL dependency.

| Test | Result | Follow-up |
| --- | --- | --- |
| `TestScopeGuard.ScopeFailure` | The failure guard callback remains false (`failure == false`) under clang-cl Release, while the MSVC Release matrix remains passing after its documented exclusions. | Investigate the clang-cl/C++20 uncaught-exception observation separately. |
| `Dx12SwapchainMigration` | Direct execution terminates with SEH `0xc0000005` in the test body; the same test passes in the clang-cl static Debug and MSVC Release matrices. | Retain as a reproducible clang-cl static Release failure pending renderer/runtime investigation. |

The six exact assertion-dependent Release cases are still controlled only by the existing exclusion file; no blanket exclusion was added.

The clean clang-cl DLL Release graph in `NauEngineLite/build/replace-eastl-clang-dll-release` builds through 1406/1406 targets. Its corrected 610-test CTest run reports 597 passes, 8 failures, and 5 existing self-skips. The eight failures are the same six assertion-dependent Release exclusions, `TestScopeGuard.ScopeFailure`, and `Dx12SwapchainMigration`; all USD, project, build, ECS, and other tool tests pass. The DLL Release result does not turn either clang-cl-specific failure into a pass.


### Deferred SDK runtime checks

The relocated VS 2026 SDK `inputDemo` launches in both configurations, but its automated shutdown checks did not pass: Debug did not exit within 10 seconds after `CloseMainWindow` (the validation process was then terminated), while Release exited with `0xC0000005`. Debug may require closing its additional window; neither result is counted as a successful shutdown. These checks are deferred under the user's instruction to record and skip failed tests. Logs and process records: `NauEngineLite/build/windows-msvc-2026-evidence/sdk-input-debug-*` and `sdk-input-release-*`. The user separately accepted all six source-build visual/input and shutdown checks in Debug/Release.

### Suite results

- clang-cl 22.1.3 DLL Debug: with the known async case excluded, 406 of 409 selected runtime tests pass. `EastlAllocator.AlignmentAndOffsets` and `EastlAllocator.RejectsInvalidAndOverflowingRequests` fail assertions; `EastlAllocator.ReallocationPreservesDataAndAlignment` crashes with a segmentation fault. These three DLL-specific allocator failures are deferred under the user's instruction. `failed-tests-clang-dll-debug.txt` contains these exact names plus the shared async exclusion. Initial evidence: `clang-dll-runtime-tests.log`. The passing static allocator tests do not establish DLL allocator correctness.

  The DLL rerun passes all 406 selected tests with those four exclusions (`clang-dll-runtime-with-skips.log`, 16.94 seconds). Both clang-cl production/runtime-test graphs compile and link after dependency preparation; the runtime failures themselves remain unresolved.

- clang-cl 22.1.3 static Debug: the prepared Google Test headers allow all 410 runtime tests to run. `TestAsyncFunctions.WhenAll_NoTimeout` terminates with `0xC000001D` (illegal instruction); the other 409 pass. The exact temporary exclusion is `NauEngineLite/cmake/probes/windows_toolchain/failed-tests-clang-debug.txt`. A filtered rerun passes all 409 selected tests. Logs: `clang-static-runtime-ctest.log`, `clang-static-runtime-with-skips.log`. No production async fix is claimed.

- Editor Release: 64 unit tests ran, 60 passed and four death tests failed to terminate as expected: `NauSettingsDeathTests.invalidRecentLauncherOutputDirectory`, `NauSettingsDeathTests.invalidRecentProjectDirectory`, `NauEditorVersionDeathTests.checkVersionFromInvalidText`, and `NauEditorVersionDeathTests.checkVersionFromTextInvalidFormat`. They expect assertion termination on invalid inputs, but Release disables those assertions. Exact exclusions are in `NauEditorPublic/scripts/failed-tests-release.txt`; full evidence is `editor-release-unit-tests.log`. Debug passes all 64. These Release failures are deferred under the user's instruction, not fixed.

- The initial clang-cl Google Test compile failure (`gtest-printers.h:502`, `-Werror,-Wcharacter-conversion`) is resolved by the reproducible explicit-cast header preparation. The cast preserves numerical code-unit printing. Initial evidence remains in `clang-static-build-after-includes.log`; actual runtime results are recorded above.

- Before exclusions: 580 registered tests, 569 passed, six failed and five existing assertion tests skipped. Log: `NauEngineLite/build/windows-msvc-2026-evidence/static-release-tests-before-skips.log`.
- After exclusions: 569 passed, zero failed, five existing skips and six explicitly excluded tests; 13.08 seconds. Log: `NauEngineLite/build/windows-msvc-2026-evidence/static-release-tests-with-skips.log`.
- Five existing Release skips are `Test_Asserts.DefaultAssert`, `Test_Asserts.FatalAssert`, `Test_Asserts.CombinedFailure`, `Test_Asserts.DefaultVerify` and `Test_Asserts.BreakContinueReturn`. These are separate from the six temporary exclusions.
- `TestThreadLocalValue.MultipleThreadsReuse` previously failed because of concurrent unsynchronized set insertions. The approved fix passes 20 repetitions each under VS 2022 Debug and VS 2026 Debug/Release. It is not excluded.
- Qt 6.4.1 header compilation was resolved by the reproducible upstream iterator-macro backport in `NauEditorPublic/scripts/prepare_qt_for_msvc.py`; editor Debug compilation now succeeds. Runtime and test acceptance are tracked separately in the change's validation record.


## Standard-library migration: focused kernel runner

The first combined-process NauKernelMigrationTests Debug run timed out at 180 seconds after entering TestAsyncFunctions.WhenAll_AllReady (section4-native-core-tests.log under NauEngineLite/build/replace-eastl-baseline). The case passes alone. The final runner uses CTest Google Test discovery, as the existing test_runtime target does: all 150 native kernel cases pass separately in Debug, and Release passes 145 with the five existing Test_Asserts self-skips listed above. No new test exclusion was introduced; the combined-process test-order interaction is not claimed fixed. See openspec/changes/archive/2026-10-03-replace-eastl-with-std/validation.md for the complete section 4 evidence.
