# Validation

Implementation and verification date: **2026-09-20**. The actual preset-built
`MinimalAppSample` passes Debug/Release Chrome acceptance. This record covers
sample integration and build-directory outputs, not staged-package or relocated
delivery acceptance.

## Source and environment

Root HEAD is `b7647ed488572f889d8c125ea75d3ef5a683bc98`; engine HEAD is
`52197201e525a584fb9490be22b1d064b0c666e1`, plus the uncommitted prerequisite and
sample changes. The completed minimal-runtime-profile, wasm-core-portability,
browser-platform-services and browser-runtime-lifecycle implementations are
present in this working tree. They do not yet have separate committed revisions.
No commit, submodule revision update or archive was performed.

Tools reused: external emsdk **6.0.9**, SDK Node **24.19.0**, SDK Python **3.13.3**,
CMake **4.2.1**, Ninja **1.13.2**, Chrome **153.0.8010.52**, test Python **3.14.2**
(`C:/Python314/python.exe`) with Playwright **1.63.0**, and VS 2022/MSVC
**19.44.35229.0** for native checks. No new dependencies were installed.

## Implementation boundary

The selected sample main now checks module loading in its delegate and uses
`runBrowserApplication()` on Emscripten. Native checked creation handles errors
without an empty-pointer dereference; successful native startup/step/100 ms sleep
behavior remains. No injected services or alternate browser main were introduced.

Top-level CMake now admits the supported browser/minimal/static configuration.
Unsupported desktop-profile/shared-library configurations fail explicitly. The
sample receives the proven runtime-exit/pthread-pool/main-thread-blocking options.
Existing minimal source/dependency gates were sufficient; no additional subsystem
port or third-party fix was required. Browser presets explicitly enable the sample
and disable native minimal tests. Ordinary builds do not discover runner Python.

## Actual sample builds and graph checks

From `NauEngineLite`, using the activated SDK:

```powershell
. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake --preset web-minimal-debug
cmake --build --preset web-minimal-debug --parallel 8
cmake --preset web-minimal-release
cmake --build --preset web-minimal-release --parallel 8
C:/Python314/python.exe cmake/probes/minimal_app_web/audit.py
C:/Python314/python.exe cmake/probes/emscripten/test_preflight.py
C:/Python314/python.exe cmake/probes/emscripten/test_platform_options.py --native-before build/desktop-platform-before --native-after build/desktop-platform-after
C:/Python314/python.exe cmake/probes/test_minimal_runtime.py --minimal build/native-minimal-debug --minimal build/native-minimal-release --desktop build/desktop-platform-after
```

Existing browser directories were preserved by moving them within the ignored
build tree to `web-minimal-debug-before-clean` and
`web-minimal-release-before-sample`. The final Debug/Release sample builds started
with absent preset build directories and each completed all 104 build steps.
The initial Debug integration build is not used as the clean-directory claim.
This is not a clean checkout or fresh SDK/environment walkthrough.

Both sample graph audits pass:

- 97 compile commands per configuration, consistent pthread/no-exception/no-RTTI
  settings, Debug diagnostics or Release optimization, no Windows compiler flags.
- One `app_sample_main_min.cpp` entry and generated production PlatformApp static
  registration; no `app_sample_main.cpp` in the browser target.
- Real `NauKernel`, `NauFrameworkMinimal`, `PlatformApp` and bundled Wasm libraries
  in the link, with `PROXY_TO_PTHREAD`, 1 MiB stack, runtime exit, pool size 12 and
  `ALLOW_BLOCKING_ON_MAIN_THREAD=0`; no native `.lib`/`.dll` inputs.
- Codemodel has 37 targets including CTest dashboard utilities; all source targets
  stay within the explicit minimal dependency/runtime/sample set. There are no
  unrelated application/test executables or desktop feature modules.
- Configuration succeeds with unavailable desktop dependency paths; no vcpkg,
  Qt, USD, graphics, shader tools or desktop generator packages are required.
- Desktop source-tree `run_tests.bat` and the existing native caches are unchanged.
  Desktop preset definitions and 36 selected before/after cache settings match.
- Unsupported browser desktop-profile/shared-library modes are rejected. Seven
  SDK/preflight checks pass, including missing/mismatched SDK and native compiler
  cache rejection, with unchanged SDK activation metadata. Separate source-fixture
  checks verify the specific missing-fmt and unsupported-module diagnostics.

Each `build/web-minimal-*/bin` contains `MinimalAppSample.js` and
`MinimalAppSample.wasm`. No separate worker-support file was emitted by this SDK.
Test HTML is additional harness material, not part of the runtime inventory.
No `package` output, staging cleanup or relocated resource-load claim is made.

Build logs: `build/minimal-app-{configure,build}-{debug,release}.log`.
Contract logs: `build/minimal-app-{graph-audit,preflight,platform-options,native-graph}.log`.
Detailed graph JSON and audit configure logs reside in each browser build directory.

## Chrome sample acceptance

The runner consumes existing `MinimalAppSample.js` output. It creates no C++ test
application, uses isolated Chrome profiles and a loopback COOP/COEP server, and
connects with Playwright `no_defaults=True` for real visibility transitions.
From the engine directory:

```powershell
foreach ($configuration in @('debug', 'release')) {
    $sampleBuild = "build/web-minimal-$configuration"
    foreach ($scenario in @('success', 'missing-host', 'host-loss', 'runner-failure')) {
        C:/Python314/python.exe cmake/probes/minimal_app_web/run.py --build $sampleBuild --scenario $scenario
    }
}
```

| Case / measurement | Debug | Release |
| --- | --- | --- |
| Success: application / runner exit | 0 / 0 | 0 / 0 |
| Five-second foreground updates/second | 9.782958 | 9.771068 |
| Foreground UI heartbeats | 501 | 501 |
| Real Chrome hide/show and resumed progress | Passed | Passed |
| Repeated Stop requests delivered during Stopping | 2 | 2 |
| Missing host: application / runner exit | 1 / 0 | 1 / 0 |
| Host loss: application / runner exit | 1 / 0 | 1 / 0 |
| Deliberate runner failure: application / runner exit | 0 / 1 | 0 / 1 |

`runner-failure` passes the successful sample checks before deliberately violating
an acceptance expectation. Both JSON results contain exactly the diagnostic
`Deliberately violated acceptance expectation`; an arbitrary infrastructure error
is not treated as evidence of correct negative-test behavior.

The initial harness assertion incorrectly treated a present null `abortReason`
field as an abort. It was corrected to check a nonempty reason, after which all
cases above passed. No runtime fix was needed. The rendered stopped-state page
was visually inspected; status, completed count, disabled Stop and reload guidance
are present. Running/stopped screenshots and full JSON evidence are stored as
`sample-running.png`, `sample-stopped.png` and `sample-<scenario>.json` in each
browser build directory.

| Specification scenario | Evidence in both configurations |
| --- | --- |
| Both browser presets build the sample | Clean-directory preset builds and source/link audits |
| Desktop-only dependencies are unavailable | Actual preset configuration with unavailable dependency paths; constrained codemodel and Wasm-only libraries |
| Sample starts with a valid host | Success case, Running worker and advancing real driver count |
| Required platform host is missing | Missing-host case: Failed/startup diagnostic, zero updates, no Running, cleanup complete, exit 1 |
| Foreground execution is observed | Five-second rates and heartbeat above; displayed status/count match bridge snapshots |
| Sample returns from the background | Real second-tab hide/show, resumed steps, no batched count increments or snapshot step intervals below 50 ms; existing driver elapsed-time tests remain complementary evidence |
| User stops the running sample | Page button click, frozen count after Stopping, Stopped only with cleanup complete and exit 0 |
| Stop is repeated during and after cleanup | Two additional requests on a Stopping snapshot, requests after final exit, unchanged final status/count |
| The running sample loses its host | Real DOM removal after two updates, Failed/Running diagnostic, frozen count after failure, cleanup complete, exit 1 |
| Retry is requested on a completed page | Start rejected with reload guidance after every applicable terminal result |
| Native minimal builds follow browser builds | Native sample compilation and 19-test suite, native graph/cache isolation audits |
| Sample integration is declared complete | This actual-output scenario audit and explicit staging/delivery exclusions |
| The acceptance check fails | Deliberate expectation violation returns runner 1 after a verified successful real sample run |

Every normal case also verifies ordered snapshot sequences, nondecreasing counts,
cleanup complete, application-worker status, zero retained platform hosts, no
Failed-to-Stopped transition, and final displayed values matching the snapshot.
The sample does not add dt instrumentation services; the unchanged driver supplies
the bounded-dt contract and its deterministic/lifecycle acceptance checks below.

## Native and shared regressions

```powershell
foreach ($configuration in @('Debug', 'Release')) {
    $nativeBuild = "build/native-minimal-$($configuration.ToLower())"
    cmake --build $nativeBuild --config $configuration --target MinimalAppSample NauMinimalLifecycleTests --parallel 8
    ctest --test-dir $nativeBuild -C $configuration --output-on-failure
}
# With the SDK active:
foreach ($suite in @('browser-runtime', 'browser-platform', 'wasm-core')) {
    foreach ($configuration in @('debug', 'release')) {
        $regressionBuild = "build/$suite-$configuration"
        cmake --build $regressionBuild
        ctest --test-dir $regressionBuild --output-on-failure
    }
}
```

| Boundary | Debug | Release |
| --- | --- | --- |
| Actual native minimal sample | Built | Built |
| Native lifecycle/service/application/timing | 19/19 Google Tests | 19/19 Google Tests |
| Browser runtime lifecycle | 13/13 CTest | 13/13 CTest |
| Browser platform | 8/8 CTest | 8/8 CTest |
| Wasm core | 2/2 CTest, 27 focused tests plus fatal diagnostic | Same |

Native sample builds ran without activating the SDK. Native codemodel audits pass
for both minimal configurations and preserve desktop selection of
`app_sample_main.cpp`. No shared runtime C++ implementation changed in this sample
integration, so the already validated full desktop scene build was not repeated.
Logs are `minimal-app-{build,tests}.log` under native build directories and
`minimal-app-regression-{build,tests}.log` under each regression build directory.

## Documentation, ownership and scope

The sample/build/lifecycle/platform/core guides and parent build/prerequisite
instructions now describe the enabled presets and actual sample acceptance.
`emscripten-build` tasks 2.3, 3.2–3.5 and 5.1 have concrete evidence here, advancing
that change from 11/24 to 17/24 after verification. Tasks requiring staged packages,
relocation or fresh-checkout reproduction remain unchecked, including 5.2's full
package criteria. The delivery handoff names actual output paths and bridge usage.

Implementation edits are restricted to sample setup, sample/top-level CMake,
browser preset fields, the existing platform/preflight helper messaging/check,
new sample acceptance/audit helpers, documentation and OpenSpec tracking. No
renderer, scene, third-party, editor or unrelated submodule implementation was
changed for this task. Existing prerequisite changes and unrelated editor dirtiness
were retained. Strict OpenSpec validation passes for minimal-app-web and emscripten-build.
Root and engine git diff --check pass. All 16 implementation tasks are complete;
all recorded sample outcomes were checked again against their expected exit and
diagnostic results. No archive or commit was performed.
