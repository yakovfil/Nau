# Validation

Current progress: **21/21 tasks complete**. The real application browser fixture
passes 13/13 Chrome cases in both Debug and Release. Final evidence follows the
historical implementation notes below; earlier pending/blocker statements describe
intermediate states, not current limitations. Sample/preset integration and web
package delivery remain in their owning changes.

## Service lifecycle foundation — 2026-09-19

Tasks 1.1–1.3 are implemented. Remaining application/driver/timing tasks and full
real-application browser acceptance are pending. Existing platform fixture
results below are regression evidence, not browser application acceptance.

ServiceProviderImpl retains all independent tasks, including ready failures,
settles the started batch before returning aggregated errors, and prevents later
initialization after failure. It records successful final initialization against
the original service identity (including initialization proxies). Shutdown hooks
run only for initialized services, or services without initialization hooks;
disposal still covers all instantiated objects. Shutdown/disposal errors are
aggregated without skipping remaining eligible cleanup or pending tasks.

From the repository root:

```powershell
cmake --build NauEngineLite/build/native-minimal-debug --config Debug --parallel 8
ctest --test-dir NauEngineLite/build/native-minimal-debug -C Debug --output-on-failure
cmake --build NauEngineLite/build/native-minimal-release --config Release --parallel 8
ctest --test-dir NauEngineLite/build/native-minimal-release -C Release --output-on-failure
```

Both builds and CTest runs passed. Each configuration runs 9 Google Tests in
MinimalRuntime.Lifecycle: the real native PlatformApp application lifecycle,
four new service failure tests, two existing dependency-order tests and two
existing initialization-proxy tests. The failure tests cover immediate and
deferred errors, settling independent tasks, skipped dependent initialization,
pre-initialization failure, partial-object disposal, reverse shutdown order,
continued cleanup after failures and retaining pending disposal contexts.

```powershell
$env:PATH += ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
$env:EMSDK_QUIET = '1'
. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake --build NauEngineLite/build/browser-platform-debug --parallel 8
ctest --test-dir NauEngineLite/build/browser-platform-debug --output-on-failure
cmake --build NauEngineLite/build/browser-platform-release --parallel 8
ctest --test-dir NauEngineLite/build/browser-platform-release --output-on-failure
```

SDK 6.0.9 rebuilt and linked the changed kernel in both configurations. Existing
real Chrome platform scenarios passed 8/8 in each: valid, missing, ambiguous,
invalid, callbacks, backend, hostloss and dpr2. Existing bundled UTF conversion
warnings remain. No dependencies were installed for this increment.

## Scene scope investigation (extension approved)

Source inspection found a native scene shutdown dependency not covered by the
proposal's stated framework/kernel/browser implementation scope:

- `engine/core/modules/scene/src/scene_management/scene_manager_impl.cpp`:
  `update()` installs `m_updateWorkQueue` as the current executor and pumps it;
  its scope exit pumps `m_postUpdateWorkQueue`.
- `engine/core/kernel/include/nau/async/task.h`: task suspension captures the
  current executor for continuation dispatch.
- Scene deactivation retains a pending asynchronous component update in the
  component's task collection. `SceneManagerImpl::shutdown()` awaits scene
  cleanup tasks, but does not itself pump either scene queue.
- `ApplicationImpl::step()` currently calls `mainGameStep()` while awaiting
  main-loop shutdown. Removing this as required by task 2.4 can therefore strand
  a native scene continuation, even while the application work queue is pumped.

This is a source-derived compatibility risk, not a reproduced desktop hang.
The independent service changes do not alter the application shutdown loop.

Approved amendment: include a narrowly scoped scene cleanup-only
pump in the internal scene/main-loop lifecycle contract. During shutdown, pump
the scene continuation queues without starting new game/component updates.
Add a native regression with an asynchronous update started before Stop and
released afterward, proving cleanup finishes without additional game updates.
The user approved this extension, and proposal/design/spec/task 2.4 now include
it. Current implementation and validation limits follow.

## Checked application lifecycle — 2026-09-19

Tasks 2.1–2.3 are implemented and validated, bringing progress to 6/21.

- `createApplicationChecked(ApplicationInitDelegate&)` returns a Result owning
  the application or a phase-labelled diagnostic. Configuration/setup failures
  settle cleanup and release services, modules, diagnostics and runtime globals.
  The legacy factory preserves its signature and returns null with a diagnostic.
- `ApplicationLifecycle` is an additive RTTI interface with `beginStartup()`,
  `pollLifecycle()`, `getPhase()` and `getLifecycleError()`. Polling drives queued
  work and lifecycle phases without invoking game updates. Legacy startup pumps
  this interface; failed startup never reaches an uninitialized main loop.
- Stop latches intent during startup. The service provider observes the owner's
  stop token between initialization calls, settles started work and skips later
  phases. Repeated Stop remains safe through cleanup and after completion.
- Runtime ownership now begins before configuration. Background work explicitly
  stops and drains during disposal, before runtime teardown. Registered object
  disposal is claimed once across the provider, platform service and registry;
  pending asynchronous cleanup retains ownership without new game updates.

The native build/CTest commands above pass **16 Google Tests in each of Debug
and Release** (one CTest entry per configuration). The seven added application
tests cover configuration failure, setup failure after module loading, legacy
creation failure, immediate/deferred startup failure, Stop during pending
pre-initialization, and pending registered-resource disposal with no duplicate
disposal or additional updates.

Browser platform rebuilds and real Chrome regressions pass **8/8 in each
configuration** with SDK 6.0.9. Wasm core rebuilds and CTest pass **2/2 in each
configuration**, covering the existing core suite and isolated fatal diagnostic:

```powershell
# Activate the SDK as shown above before builds.
cmake --build NauEngineLite/build/wasm-core-debug --parallel 8
ctest --test-dir NauEngineLite/build/wasm-core-debug --output-on-failure
cmake --build NauEngineLite/build/wasm-core-release --parallel 8
ctest --test-dir NauEngineLite/build/wasm-core-release --output-on-failure
```

No new dependencies were installed. Full browser application driver acceptance
has not run; these remain platform/core regression results.

## Task 2.4 implementation and native scene validation blocker

The internal scene/main-loop `pollShutdown()` pump and its application hookup are
implemented. The new real-scene regression
`TestSceneShutdown.PendingUpdateCompletesWithoutNewUpdatesAfterStop` starts an
asynchronous component update on the scene executor, requests Stop, then releases
the update from the application executor. It checks completion/destruction and
that no new component update starts.

CoreScene and NauFramework Debug compile in the current desktop tree with
dependency builds skipped:

```powershell
$env:PATH = 'C:/Users/Yakov/AppData/Local/Programs/Python/Python310;C:/Users/Yakov/AppData/Local/Programs/Python/Python310/Scripts;' + $env:PATH
cmake --build NauEngineLite/build/desktop-platform-after --config Debug --target CoreScene NauFramework --parallel 8 -- /p:BuildProjectReferences=false
cmake --build NauEngineLite/build/desktop-platform-after --config Debug --target test_scene --parallel 8 -- /p:BuildProjectReferences=false
```

The scene test sources, including the new regression, compile. Linking fails with
LNK1104 for missing TestCommonLib.lib. Building test_scene with dependencies then
reproduces the recorded native kernel graph failure:

```powershell
cmake --build NauEngineLite/build/desktop-platform-after --config Debug --target test_scene --parallel 8
```

The Windows graph incorrectly includes `platform/emscripten/core_platform.cpp`.
That translation unit reports C2757 (`nau_utf8` namespace conflicts with the
native alias) and C2607 (Wasm platform static assertion). Logs are in the ignored
build directory: `scene-lifecycle-build.log` and
`scene-lifecycle-dependencies.log`. The old win_vs2022_x64 build cannot substitute:
its cache points to the former `D:/Programming/github/NauEngineLite` checkout.

Task 2.4 remains unchecked until its real scene regression runs in both
configurations. The user approved the following narrow source-selection
prerequisite; broader desktop build repairs remain outside this change.
In `engine/core/kernel/src/CMakeLists.txt`, correct the two source-list regexes
to match paths relative to src:

```diff
-  EXCLUDE "/platform/.*"
+  EXCLUDE "(^|/)platform/.*"

-      "/platform/windows/.*"
+      "(^|/)platform/windows/.*"
```

Apply these only to the source collectors; public-header paths use a different
relative root. Reconfigure, verify the Windows source list excludes Emscripten,
then rebuild and run the scene regression in Debug/Release. The source-selection
fix was applied following approval; results follow.

## Source-selection fix and completed scene validation — 2026-09-19

Applied the approved two source-collector regex changes. Inspection of the
regenerated NauKernel.vcxproj confirms **0 Emscripten source entries and 12 Windows
platform source entries**. The native kernel builds, and the previous C2757 and
C2607 errors no longer occur. Public-header collectors were left unchanged.

The full dependency build for test_scene succeeds in Debug and Release. The first
Debug regression run found a missing test-component registration; registering
PendingShutdownComponent before factory creation fixed the fixture. The regression
then passed, as did all affected scene update/deactivation tests:

```powershell
$env:PATH = 'C:/Users/Yakov/AppData/Local/Programs/Python/Python310;C:/Users/Yakov/AppData/Local/Programs/Python/Python310/Scripts;' + $env:PATH
cmake --build NauEngineLite/build/desktop-platform-after --config Debug --target test_scene --parallel 8
ctest --test-dir NauEngineLite/build/desktop-platform-after -C Debug -R 'TestScene(Update|Deactivate|Shutdown)\.' --output-on-failure --timeout 30
cmake --build NauEngineLite/build/desktop-platform-after --config Release --target test_scene --parallel 8
ctest --test-dir NauEngineLite/build/desktop-platform-after -C Release -R 'TestScene(Update|Deactivate|Shutdown)\.' --output-on-failure --timeout 30
```

Results: **12/12 in Debug and 12/12 in Release**, including
TestSceneShutdown.PendingUpdateCompletesWithoutNewUpdatesAfterStop. Together with
the 16 native minimal/service/application tests per configuration recorded above,
this completes task 2.4's cleanup, ownership and real-scene validation requirements.
Build logs are `scene-selection-fix-debug.log` and
`scene-selection-fix-release.log` in the ignored desktop build directory.
No new machine dependencies were installed. This validates the scene-test
dependency graph; it does not claim a complete desktop application or browser
application delivery build.

## Completed browser lifecycle acceptance — 2026-09-19

Tasks 3.1–5.6 are implemented. The reusable `runBrowserApplication()` worker driver
uses the real checked ApplicationImpl, service provider, runtime, work queue and
production static PlatformApp. Final cleanup snapshots follow Application
destruction. Page callbacks hold copied snapshots and page-lifetime atomic control
words, never application pointers. Old snapshot sequences are rejected, Stop
wakes the worker asynchronously, and failure/reload state remains terminal.

The generated Ninja link inputs contain `libNauFrameworkMinimal.a`,
`libPlatformApp.a`, `libNauKernel.a`, bundled source libraries and generated static
module registration. Options include `-pthread -sPROXY_TO_PTHREAD=1`, a 1 MiB
stack, `-sEXIT_RUNTIME=1`, pool size 12 and
`-sALLOW_BLOCKING_ON_MAIN_THREAD=0`. Debug uses `-O0 -g3 -sASSERTIONS=2`;
Release uses the shared optimized Emscripten options. The framework's new browser
source is selected only for Emscripten; the affected desktop target builds below
confirm it does not leak into Windows compilation.

Tested environment: Windows/PowerShell, external emsdk **6.0.9**, CMake **4.2.1**,
Ninja **1.13.2**, Python **3.14.2** at `C:/Python314/python.exe`,
Playwright **1.63.0**, Chrome **153.0.8010.52**. The SDK uses its own Python and
Node **24.19.0**. No additional dependency installation or SDK upgrade was needed.
The SDK's CMake shared-library warning does not affect these static targets.

From `NauEngineLite` (these are the exact locally tested paths):

```powershell
. C:/Users/Yakov/emsdk/emsdk_env.ps1
foreach ($configuration in @('Debug', 'Release')) {
    $runtimeBuild = "build/browser-runtime-$($configuration.ToLower())"
    cmake -S cmake/probes/browser_runtime -B $runtimeBuild -G Ninja -DCMAKE_TOOLCHAIN_FILE=C:/Users/Yakov/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake "-DCMAKE_BUILD_TYPE=$configuration" -DPython3_EXECUTABLE=C:/Python314/python.exe
    cmake --build $runtimeBuild
    ctest --test-dir $runtimeBuild --output-on-failure
}
```

Portable environment-based commands are in
`NauEngineLite/doc/browser_runtime_lifecycle.md`. Build directories are ignored;
`build.log`, `acceptance.log`, `acceptance-summary.json` and
`Testing/Temporary/LastTest.log` retain build, aggregate and structured evidence.

| Acceptance measurement | Debug | Release |
| --- | ---: | ---: |
| CTest cases | 13/13 | 13/13 |
| Five-second foreground completed updates/second | 9.5796 | 9.5840 |
| Stop to first Stopping snapshot, after an update | 1.355 ms | 1.250 ms |
| UI heartbeat callbacks over success fixture | 462 | 461 |
| Executor callbacks independent of cadence | 60 | 60 |
| Real Chrome hide/show | Passed | Passed |
| Elapsed time bounds / no catch-up burst | Passed | Passed |

The runner separately asserts at least 100 UI heartbeats during the measured
five-second interval, 8–12 completed updates/second, Stop latency below 90 ms,
0–100 ms update elapsed values and no update intervals below 50 ms. The hidden
tab test uses a real second Chrome tab and `document.hidden`, with Playwright
focus emulation disabled. Stalled cleanup uses a 250 ms injected deadline: 400 ms
hidden time does not fail it; visible lack of progress does, and releasing the
gate completes cleanup while Failed remains terminal.

| Specification scenario | Evidence, Debug and Release |
| --- | --- |
| Application starts successfully | `BrowserRuntime-success`: real modules, worker status, updates and responsive UI |
| Native lifecycle is exercised | Native minimal suite, legacy startup/step/stop and ordering |
| Independent initialization fails immediately | `immediate`: Failed/Initialization, zero completed updates; native dependent-skip tests |
| Initialization fails asynchronously | `deferred` and `batchfailure`: later independent rejection observed while earlier task remains pending; no updates, owners retained until release |
| Application creation fails after allocating resources | `configfail`, `setupfail`: Failed/Creation, partial cleanup, zero updates; native global-state unwind tests |
| Status is observed across startup and stop | `success`: increasing sequences, nondecreasing completed counts, final Stopped with cleanup complete |
| A callback arrives after teardown | Runner replays an old copied snapshot after exit and asserts rejection; no application pointer in callbacks |
| Foreground application runs normally | Five-second measurements above, UI heartbeat assertions |
| Executor work arrives between deadlines | 60 queued continuations during normal run; three native deterministic timing tests verify wakes do not advance deadlines |
| A backgrounded page resumes | Real Chrome hide/show, bounded dt/no update burst; native deterministic 5000 ms gap/reset checks |
| Stop arrives during an idle interval | Stop requested immediately after a completed update; latency above is below the next 100 ms deadline |
| Stop arrives during startup | `stopstartup`: pre-init gate, no later initialization, zero updates, release then cleanup |
| Stop is requested repeatedly | Stop called twice and again after completion; fixture disposal/destruction counts exactly once |
| Stop encounters pending work | `pending`: cleanup incomplete, completed count frozen, release then Stopped |
| A shutdown hook fails | `shutdownerror`: Failed/Cleanup, diagnostic retained, eligible disposal and destruction complete; native deferred disposal/error aggregation tests |
| Native scene update is pending at Stop | Real `TestSceneShutdown.PendingUpdateCompletesWithoutNewUpdatesAfterStop`, 12/12 affected scene tests per configuration |
| Running application loses its host | `hostloss`: remove real DOM host, Failed/Running, safe cleanup, no host retained |
| Start is requested after failure | Runner checks rejected `start()` after every non-abort exit; reload required, no runtime recreation |
| Runtime abort is observed | Isolated `abort`: C++ abort on worker reaches host hook, Failed/Fatal abort, cleanup false, runner/process result 1 |
| Cleanup stalls then becomes able to finish | `stall`: hidden time excluded, foreground deadline reports Failed/incomplete, gate release permits cleanup without changing Failed to Stopped |
| Lifecycle implementation is declared complete | This scenario audit, all browser/native regressions, tested guide and explicit delivery boundary |

Every non-abort fixture checks cross-origin isolation, zero remaining platform
hosts, expected terminal phase/state, completed cleanup, exact fixture disposal
and destruction counts, ordered snapshots, no terminal failure reverting to
success, restart rejection and stale delivery rejection. The deliberate
`fixture-failure` exits the application with code 2 and the runner with code 1.
The abort runner also exits 1. Separate CTest wrappers pass only when these
specific failures are observed; an unrelated runner/infrastructure error is not
accepted as fatal-abort evidence.

## Final shared regression results

| Suite / build boundary | Debug | Release |
| --- | --- | --- |
| Native minimal service/application/lifecycle/timing | 19/19 Google Tests | 19/19 Google Tests |
| Wasm core | 2/2 CTest: 27 focused tests plus fatal diagnostic subprocess | Same |
| Browser platform | 8/8 Chrome cases | 8/8 Chrome cases |
| Full `test_scene` dependency build including NauFramework, PlatformApp and CoreScene | Built | Built |
| Scene update/deactivate/shutdown | 12/12 | 12/12 |

Native tests use MSVC 19.44.35229.0 / VS 2022 and the Windows SDK recorded above.
Build/test commands, from `NauEngineLite`, after configuring the existing isolated
directories according to their engine guides:

```powershell
foreach ($configuration in @('Debug', 'Release')) {
    $nativeBuild = "build/native-minimal-$($configuration.ToLower())"
    cmake --build $nativeBuild --config $configuration --target NauMinimalLifecycleTests --parallel 8
    ctest --test-dir $nativeBuild -C $configuration --output-on-failure
}
# In the activated SDK shell:
foreach ($suite in @('wasm-core', 'browser-platform')) {
    foreach ($configuration in @('debug', 'release')) {
        $regressionBuild = "build/$suite-$configuration"
        cmake --build $regressionBuild
        ctest --test-dir $regressionBuild --output-on-failure
    }
}
# Desktop generation needs the installed generator Python and pip first on PATH.
$env:PATH = 'C:/Users/Yakov/AppData/Local/Programs/Python/Python310;C:/Users/Yakov/AppData/Local/Programs/Python/Python310/Scripts;' + $env:PATH
foreach ($configuration in @('Debug', 'Release')) {
    cmake --build build/desktop-platform-after --config $configuration --target test_scene --parallel 8
    ctest --test-dir build/desktop-platform-after -C $configuration -R 'TestScene(Update|Deactivate|Shutdown)\.' --output-on-failure --timeout 30
}
```

Logs are `runtime-final-{build,tests}.log` under each native minimal build,
`runtime-regression-{build,tests}.log` under each Wasm regression build, and
`runtime-regression-{debug,release}-{build,tests}.log` under the desktop build.
The earlier native kernel source-selection blocker is resolved by the approved
two-line fix. No other desktop dependency failure remains within this boundary;
full desktop application/editor builds are not claimed.

The final browser implementation fixes found during validation were a readiness
check before querying an asynchronous task error, visibility tracking independent
of platform disposal during pending cleanup, and retention of the original
failure phase through final teardown. All final suites above include those fixes
where applicable.

## Documentation and delivery handoff

`prerequisites.md`, `build.md`, the engine lifecycle/platform guides and the
`emscripten-build` validation handoff now describe the tested lifecycle integration.
`runBrowserApplication(delegate)` is the concrete hook for the selected sample.
The `web-minimal-*` application presets remain guarded; sample adaptation, complete
package staging, clean-checkout reproduction, missing-isolation delivery UI and
relocated Chrome acceptance remain pending. The owning `emscripten-build` task
checkboxes remain unchanged at 11/24. No package acceptance is inferred from this
independent test target. `openspec validate browser-runtime-lifecycle --strict`
and `openspec validate emscripten-build --strict` both pass. Root and engine
`git diff --check` pass. A final audit of all recorded non-abort results in both
configurations confirms no Running snapshot on startup failure/Stop, no count
increase after Stopping/Failed, and completed counts matching actual updates.
No archive or commit is performed by this change application.
