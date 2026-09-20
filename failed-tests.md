# Temporarily skipped tests

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

## Evidence and other status

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
