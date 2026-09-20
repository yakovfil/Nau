# Acceptance scenario review

Current update (2026-09-20): real Debug/Release packages build and pass relocated
Chrome acceptance through `minimal-web-delivery-validation`. Tasks are
**24/24 marked complete**, with task 6.2 closed at the user's explicit request.
The fresh-checkout/environment walkthrough has not been executed or independently
verified in this session; its evidence remains absent. Earlier prerequisite
limitations below are historical.
See the current delivery review at the end and
[delivery evidence](../minimal-web-delivery-validation/validation.md).

Review date: 2026-09-19. This is an interim review of all 16 scenarios in
`specs/emscripten-build/spec.md`, not a declaration of complete implementation.
The engine base revision is `52197201e525a584fb9490be22b1d064b0c666e1`; implementation
changes remain in the working tree. SDK 6.0.9 remains the exact pin.

| Scenario | Result | Evidence and remaining work |
| --- | --- | --- |
| Build from a fresh checkout | Blocked | The native minimal target exists, but application lifecycle integration and a full fresh-checkout application build are absent. SDK probes do not satisfy this scenario. Tasks 3, 5.2 and 6.2 remain pending. |
| Supported external SDK | Verified toolchain contract | The preflight and direct CMake guard accept and report 6.0.9. Debug/Release capability and bundled fmt/xxHash probes build. Compatibility with the real Nau runtime remains unverified. |
| Missing or incompatible SDK | Verified | `test_preflight.py` checks absent SDK environment, absent toolchain/compiler files, mismatched expected version and direct CMake rejection. Diagnostics identify the expected SDK and explicit setup commands. |
| No implicit SDK changes | Verified | Preflight/configure helpers contain no SDK install/activation/update action. Failure-case tests confirm `.emscripten` activation metadata remains unchanged. Installation and the separate 4.0.7 comparison were explicitly authorized operations. |
| Both configurations coexist | Partial | Both application presets resolve into independent caches and output directories. Debug/Release probes coexist. Actual Nau packages cannot be produced until the runtime ports exist. |
| Native cache remains independent | Verified isolation | Browser preset tests leave the original native cache unchanged; native compiler/toolchain settings match across before/after configurations. Browser configuration still stops at the missing Wasm core/browser platform/lifecycle diagnostic. |
| Desktop dependencies are unavailable | Partial | Browser preset resolution and production-helper probes work with inaccessible desktop dependency paths and do not invoke vcpkg. Successful configuration of the actual minimal graph remains blocked. |
| Native binaries are present | Partial | Probes build/link Wasm fmt and xxHash from source beside existing native outputs. Actual browser application link inputs await the source ports. |
| Required source is missing | Verified profile contract | The exact dependency set is defined. A separate source fixture missing fmt fails in the real profile CMake with a dependency-specific restoration diagnostic, without host fallback or checkout mutation. |
| Thread settings are consistent | Partial | Generated C/C++ and executable commands use pthreads; application probe links select PROXY_TO_PTHREAD. Both configurations build and run under SDK Node. Production platform fixture commands are now available; selected application link validation remains pending for task 2.3. |
| Static module integration | Platform prerequisite verified; application pending | Production PlatformApp static registration and shared service run in Chrome Debug/Release. The selected application entry point remains unintegrated. |
| Both existing sample sources are present | Verified natively, browser pending | Sample CMake explicitly selects app_sample_main_min.cpp for minimal and app_sample_main.cpp for desktop. Native sample links succeed; browser generated inputs await the source ports. |
| Package is copied | Blocked | No staged actual runtime package or delivery-owned Chrome page/server is available. Node probe execution is not Chrome relocation validation. |
| Clean output generation | Partial | Standalone probes emit JS/Wasm outputs; SDK 6.0.9 emits no separate worker script for these probes. Actual application output inventory, clean staging and stale-artifact tests remain pending. |
| Native validation configuration | Verified | Native Debug/Release presets build NauFrameworkMinimal and the real PlatformApp; both focused lifecycle checks pass. The 23-target graphs exclude desktop feature modules and browser options. |
| Existing desktop build | Verified for affected configuration/target | `win_vs2022_x64` configures without emsdk; preset definitions and 36 compiler/cache settings match. Native fmt builds pass in Debug and Release; affected NauFramework and PlatformApp Debug libraries also compile with dependency project builds skipped. Full desktop engine/editor builds remain unverified. |

## Reproducible evidence

From the engine directory after loading the pinned SDK environment:

```powershell
python cmake/probes/emscripten/test_preflight.py
python cmake/probes/emscripten/test_platform_options.py --native-before build/desktop-platform-before --native-after build/desktop-platform-after
python cmake/probes/emscripten/test_fmt_compatibility.py
```

The native comparison requires the previously configured directories; their
configuration procedure and tool versions are recorded in
`NauEngineLite/doc/emscripten_build.md`. Native fmt validation used:

```powershell
cmake --build build/desktop-platform-after --config Debug --target fmt
cmake --build build/desktop-platform-after --config Release --target fmt
```

Tests retain logs under the ignored engine `build` directory. SDK and platform
checks were rerun after native profile integration. Native commands and graph
audits are recorded in `NauEngineLite/doc/minimal_runtime_profile.md`.

## Scope audit

Implementation edits are confined to engine build/preset helpers, SDK/probe tests,
engine documentation, and the explicitly approved one-line fmt constexpr fix.
The separately authorized minimal-runtime-profile also updates shared framework
and platform-window source selection and supplies focused native tests. Root edits
hold planning, validation and build/prerequisite documentation.
No NauDemo, renderer, editor or unrelated submodule implementation was changed by
this workflow. Existing editor working-tree changes remain outside this work. The pre-existing
minimal sample source is now explicitly consumed without changing its contents.

Tasks with blocked or unverified implementation/acceptance remain unchecked.
Refresh this review after minimal-profile, runtime or packaging integration before
claiming final completion or archiving.

## Wasm core prerequisite handoff (2026-09-19)

`wasm-core-portability` now provides 62 common kernel sources plus platform backends,
the independent `cmake/probes/wasm_core` entry and focused executable validation.
NauKernel and all eight NauFrameworkMinimal sources compile for wasm32; both
configurations pass 27 core tests and a fatal diagnostic subprocess under SDK
Node 24.19.0. Native core and real minimal lifecycle Debug/Release tests also pass.
See `../wasm-core-portability/validation.md` and the engine core build guide.

Engine base remains `52197201e525a584fb9490be22b1d064b0c666e1` plus uncommitted
authorized changes. Browser platform services were subsequently validated (below); application lifecycle, real entry
point integration, staging and Chrome delivery remain pending. No application or
package acceptance task is completed by the core test executable.

## Browser platform prerequisite handoff (2026-09-19)

`browser-platform-services` implements the production browser PlatformApp factory,
window manager and shared PlatformWindowService readiness/disposal integration.
The focused `cmake/probes/browser_platform` executable statically registers the
actual module and passes 8/8 Chrome tests in Debug and Release with SDK 6.0.9.
It verifies real DOM state, initialization errors, worker/UI dispatch, idle wake-up,
processing limits, host removal and shutdown. See
`../browser-platform-services/validation.md` and the engine platform guide.

The browser fixture confirms the platform prerequisite. Application cadence,
startup-result policy, stop controls, the selected minimal sample entry point,
staging and relocation are still separate work. The existing browser preset guard
is preserved; application/package tasks remain unchecked. In particular, service
initialization failure is now observable, but ApplicationImpl still ignores the
startupServices result and requires lifecycle integration.

Native minimal lifecycle tests and Wasm core regressions pass in both configurations.
Affected desktop NauFramework/PlatformApp Debug targets compile with dependency
project builds skipped. A broader desktop build encounters existing kernel source
selection errors; see the platform validation record for the exact limitation.
No full desktop application success is claimed.

## Browser runtime prerequisite handoff (2026-09-19)

`browser-runtime-lifecycle` is now implemented and validated. Its independent
`cmake/probes/browser_runtime` target runs the real shared ApplicationImpl with
production static PlatformApp in Chrome: **13/13 cases in Debug and Release** on
SDK 6.0.9. Five-second foreground rates are 9.5796 and 9.5840 updates/second.
Checked creation/startup, asynchronous Stop, ordered snapshots, pending cleanup,
failure/reload policy, visibility, timeout and fatal-abort reporting are covered.
See `../browser-runtime-lifecycle/validation.md` and
`NauEngineLite/doc/browser_runtime_lifecycle.md` for commands and scenario evidence.
This supersedes the earlier notes about ApplicationImpl ignoring startup results.

Concrete `minimal-app-web` integration points:

- Select `app_sample_main_min.cpp` as the one sample main and invoke
  `nau::runBrowserApplication(delegate)` from its application worker.
- Link `NauFrameworkMinimal` and register production `PlatformApp` with
  `nau_target_link_modules`; the delegate loads `NAU_MODULES_LIST` and registers
  `createPlatformWindowService()`. Keep consistent static pthread/no-exception
  options across the sample and libraries.
- Supply the DOM host and bind page status/count rendering to
  `Module.nauRuntime.status`; call `Module.nauRuntime.stop()` from the Stop control.
  Retry requires page reload. The lifecycle driver owns startup and cleanup.
- Replace the generic prerequisite guard only when the selected sample and its
  complete web build graph are integrated. Stage the full JS/Wasm/worker artifact
  inventory, provide missing-isolation delivery diagnostics and a documented
  COOP/COEP server, then validate copied-package loading in Chrome without source
  or SDK access. Clean-checkout reproduction also remains required.

The fixture is not the selected sample or its delivery package. Accordingly,
`emscripten-build/tasks.md` remains **11/24**, with sample/link, packaging,
relocation and reproduction work unchecked. Native lifecycle now passes 19 tests
per configuration, browser platform 8/8 and Wasm core 2/2 CTest per configuration.
The approved kernel source-selection repair enables full Debug/Release builds of
the native `test_scene` dependency graph and 12/12 affected scene tests. Full
desktop application/editor builds remain outside the validated boundary.

## Actual sample and delivery handoff (2026-09-20)

`minimal-app-web` connects `app_sample_main_min.cpp` to the validated worker driver
and enables the actual `web-minimal-debug` / `web-minimal-release` presets. Both
build from empty output directories with SDK 6.0.9 and pass Chrome success,
missing-host, host-loss and deliberate runner-failure acceptance. Real foreground
rates are 9.7830 Hz Debug and 9.7711 Hz Release. See
`../minimal-app-web/validation.md` and the engine's `doc/minimal_app_web.md`.

Evidence now completes these previously pending build tasks:

| Task | Actual-sample evidence |
| --- | --- |
| 2.3 | 97 compile commands per configuration, consistent pthread settings and static real-runtime links with application worker execution |
| 3.2 | Presets configure the real minimal dependency/module/sample graph, excluding desktop feature chains |
| 3.3 | Minimal configure avoids desktop generators/install blocks and leaves source-tree run_tests.bat untouched |
| 3.4 | Bundled sources build as Wasm with unavailable desktop dependency paths; missing-source diagnostic checked using a disposable fixture |
| 3.5 | Exactly one app_sample_main_min.cpp entry, production PlatformApp registration, native sample builds and preserved desktop source selection |
| 5.1 | Required core/platform/lifecycle sources present at engine HEAD 52197201e525a584fb9490be22b1d064b0c666e1 plus recorded uncommitted prerequisite changes; actual sample execution verified |

The task count advances to **17/24**. Task 5.2 still requires complete independent
packages, and tasks 4.1–4.3, 5.4, 6.1 and 6.2 retain their unverified staging,
relocation, package-documentation and fresh-checkout criteria. Empty build
directories do not establish a fresh checkout/environment walkthrough.

Delivery now receives `build/web-minimal-{debug,release}/bin/MinimalAppSample.js`
and `.wasm`. The SDK embeds worker support in the loader for the tested links;
stage the current required outputs rather than assuming a worker filename.
The delivery page must supply the DOM host before loading the script, configure
Module hooks, display `Module.nauRuntime.status`, and forward Stop through
`Module.nauRuntime.stop()`. Preserve reload-only retry and final cleanup reporting.

The sample harness supplies only temporary test hosting and isolation headers.
The next delivery work still needs a finished page/server, clear missing-isolation
UX, output staging/stale-file handling and copied-package Chrome checks under a
different URL base without access to source or SDK paths. No runtime `package`
directory or relocation claim is introduced by this sample change.

## Current delivery scenario review (2026-09-20)

The subsequent delivery implementation stages the real sample by default and
validates copies outside the complete workspace. Both configurations build from
absent preset build directories (105 steps; 38 targets/97 compile commands),
then pass all nine delivery cases. The current package has JS/Wasm, page,
standalone server, README and configuration/SDK/hash manifest. Twelve workers
load the package-local loader under a nested base; no source/SDK/symbol fetch is
required. Stale/missing-input and staging-boundary checks pass. SDK 6.0.9 remains
compatible with the approved fmt fix and actual static Nau link.

| Scenario | Current result and evidence |
| --- | --- |
| Build from a fresh checkout | Task 6.2 closed at user request; no fresh-environment execution evidence supplied or verified in this session. Working-tree clean build-directory checks do not satisfy this requirement. |
| Supported external SDK | Verified 6.0.9 with actual clean Debug/Release application links and copied Chrome execution. |
| Missing or incompatible SDK | Existing seven-case preflight/direct CMake evidence retained; no guard changes in delivery. |
| No implicit SDK changes | No delivery SDK installation/activation mutation; external pin unchanged. |
| Both configurations coexist | Verified independent packages, manifests and different runtime hashes. |
| Native cache remains independent | Current application audit preserves native cache hashes; native graphs have no package target/browser flags. |
| Desktop dependencies are unavailable | Current graph audit configures actual presets with unavailable desktop dependency paths. |
| Native binaries are present | Actual links use Wasm-built libraries alongside existing native outputs; generated commands audited. |
| Required source is missing | Profile diagnostic rerun by native graph helper; missing runtime staging input separately fails without replacing the old manifest. |
| Thread settings are consistent | 97 compile commands and real sample links per configuration audited; all 12 worker loader requests observed. |
| Static module integration | Actual sample Running/steps/Stop and host-loss cleanup validate retained PlatformApp module integration. |
| Both existing sample sources are present | Current native/browser/desktop graph audits retain correct single entry-point selection. |
| Package is copied | Both external copies run under `/relocated/nau/`, packaged server only, no SDK/build environment or external runtime requests. |
| Clean output generation | Explicit JS/Wasm inventory, stale artifact removal, missing input failure and clean/repeated manifests verified. |
| Native validation configuration | Samples build, 18-target graphs pass, 19/19 shared lifecycle tests pass in both configurations. |
| Existing desktop build | Prior affected target build evidence retained; current desktop graph audit passes. Delivery adds only an Emscripten-guarded custom target. |

Tasks 4.1–4.3, 5.2, 5.4 and 6.1 now have full evidence in
`../minimal-web-delivery-validation/validation.md`. Root prerequisites/build and
engine build/sample/delivery guides describe tested build/package/serve commands;
the copied README is self-contained. Real browser lifecycle regressions pass
13/13 in each configuration, with real fatal abort distinguished from the page
hook simulation. No fresh-checkout claim, commit or archive is made.
