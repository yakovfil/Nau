# Tasks

This checklist covers build integration only. The minimal framework split, core/platform port, lifecycle behavior, and delivery page remain separate capability work. Tasks that need those implementations must remain pending until they exist; do not replace them with stubs or expand implementation scope silently. SDK/toolchain checks can begin independently.

## Current profile evidence (2026-09-19)

- The authorized `minimal-runtime-profile` change is implemented (9/9 tasks) in
  the engine working tree based on `52197201e525a584fb9490be22b1d064b0c666e1`.
  Concrete targets: `NauKernel`, `NauFrameworkMinimal`, `PlatformApp`, `PlatformAppApi`.
  `cmake/NauMinimalRuntime.cmake` owns exact source dependency/module lists.
  No new component revision has been committed; see that change's validation.md.
- Task 3.6: separate native Debug/Release presets build that same framework.
  Both graphs now contain 18 targets after the verified core-source refinement;
  they pass source-directory and native-option audits and are
  isolated from each other and the browser caches.
- Task 5.5: both native samples/tests build and real lifecycle checks pass.
  Existing desktop configuration succeeds, and affected NauFramework/PlatformApp
  Debug libraries compile with dependency project builds skipped. This is not a
  complete desktop application link; no unrelated failure was encountered.
- Task 5.3: seven SDK/preflight cases were rerun successfully, including native
  cache rejection and unchanged SDK activation metadata. The real profile's
  separate missing-fmt-source fixture fails with an explicit dependency error.
  No dependency was removed or replaced in the working checkout.
- The authorized `wasm-core-portability` change is complete (19/19 tasks): both
  isolated Wasm configurations pass 27 core tests and fatal-diagnostic checks
  under SDK Node 24.19.0. All eight shared framework sources compile. Its
  manifest selects 62 common sources plus three Wasm backends; native core and
  lifecycle regressions pass. See `../wasm-core-portability/validation.md`.
- Browser presets select the minimal profile. The authorized
  `browser-platform-services` change now supplies the real browser PlatformApp
  backend and shared service integration; Chrome passes 8/8 platform cases in
  both configurations. See `../browser-platform-services/validation.md`.
  Full application graph configuration remains guarded pending
  browser-runtime-lifecycle and minimal-app-web integration. Tasks 2.3, 3.2–3.5
  and application/package acceptance remain pending; platform tests do not
  establish the selected application entry point or delivery package.
- Updated platform checks pass both configurations, preserve existing desktop
  preset definitions and compare 36 unchanged native compiler/cache settings.

## Earlier SDK/preset evidence (2026-09-19, before minimal profile implementation)

- Engine revision inspected: `52197201e525a584fb9490be22b1d064b0c666e1`. Existing untracked engine instructions and `app_sample_main_min.cpp` were preserved.
- The initial SDK blocker was resolved after the user explicitly authorized installation. Installed and activated external emsdk `6.0.9` (release hash `f04ea239d533260dd1db760dd2d668d5f9a88d6b`), with bundled Node `24.19.0` and Python `3.13.3`; installed Ninja `1.13.2`, retaining CMake `4.2.1`.
- Task 1.1 passed the standalone C++20 coroutine/pthread compile-link probe in Debug and Release. Reproduce from the engine directory after SDK environment setup: `./cmake/check_emscripten.ps1 -Probe -Configuration Debug`, then the same command with `Release`. Both generated `.js` and `.wasm` outputs; no separate worker file was emitted. Commands contain `-std=c++20`, `-pthread`, and application link `-sPROXY_TO_PTHREAD=1`; Debug uses `-g`/assertions and Release uses `-O3`. This validates the candidate toolchain only, not the real Nau runtime or browser execution. CMake 4.2.1 emits an SDK warning about shared libraries; the probe and planned runtime use static linking.
- Tasks 1.2 and 1.3: `python cmake/probes/emscripten/test_preflight.py` passed seven checks: matching SDK, missing SDK environment, missing SDK files, mismatched version, direct CMake mismatched version, direct engine CMake missing SDK, and native compiler-cache rejection. Mismatch tests use disposable expected-version metadata with the real installed compiler. The external SDK activation configuration remained unchanged. The CMake guard is opt-in for browser configuration; desktop builds do not discover emsdk.
- Task 3.1 remains pending: `engine/core/CMakeLists.txt` still discovers all enabled modules and selects `NauFramework`; `engine/core/app_framework/src/CMakeLists.txt` publicly links `CoreScene`, `Graphics`, `ui`, and `VFX`. No shared minimal framework or explicit minimal dependency/module selection was found in these build definitions or the CMake helpers. Integration requires the separate `minimal-runtime-profile` implementation and its concrete target/revision.
- Full graph, application builds, packaging, browser relocation, and native lifecycle validation remain unverified and pending their source prerequisites.
- Added root `prerequisites.md`, updated root `build.md`, and added engine-local `doc/emscripten_build.md` with installed versions, setup and verified probe commands. Task 6.1 remains pending because application presets/package build commands are not implemented. Installed VS 2022 Build Tools 17.14.41 and Python 3.10.11 with cymbal 1.0.0 / clang 21.1.7; a standalone native C++20 smoke test configured, built and ran with MSVC 19.44.35229.0 and Windows SDK 10.0.26100.0. This is not a desktop engine regression build or minimal lifecycle validation.

## Presets and platform evidence (2026-09-19)

- Task 2.1: `web-minimal-debug` and `web-minimal-release` configure/build presets resolve through their own Ninja base with independent cache, bin, lib and install paths. Actual configure runs with inaccessible desktop dependency paths select Emscripten/wasm32 and stop at the explicit missing minimal-profile diagnostic before desktop graph discovery. No runnable application build is claimed.
- Task 2.2: `NauPlatformSetup` selects Emscripten before Windows and separates host architecture from the wasm32 target. `nau_add_compile_options` uses target-scoped browser options. The standalone C++20 probe and recorded bundled C `xxHash` library compiled and linked in Debug and Release; generated commands have pthread support, Debug diagnostics/Release optimization, and no Windows/x86 definitions or MSVC-only options from the helpers.
- Task 2.3 is partially implemented: shared helper propagation reaches source libraries and consumers, and executable links select `PROXY_TO_PTHREAD`. Real runtime/module command verification is still blocked by the missing minimal profile. Bundled `fmt` testing exposed a consteval error under SDK 6.0.9; the user authorized further SDK/fmt compatibility investigation. SDK 4.0.7 was installed separately for comparison and reproduces the failure. SDK 6.0.9 remains the pin.
- Task 2.4: `cmake --preset win_vs2022_x64 -B build/desktop-platform-before` and the equivalent `desktop-platform-after` configuration both succeeded without active emsdk, using Python 3.10 and the existing vcpkg checkout. Configuration installed manifest-pinned DXC 2024-03-29 and protobuf 3.21.12#2. Desktop preset definitions and 36 selected compiler/cache settings match. Browser checks left the original native cache unchanged. No full desktop build is claimed.
- Reproduce option/isolation checks from the engine with its SDK environment loaded: `python cmake/probes/emscripten/test_platform_options.py`. Append `--native-before build/desktop-platform-before --native-after build/desktop-platform-after` to compare the recorded native configurations. Logs are retained under the ignored engine build directory.
- The fmt investigation is recorded in `NauEngineLite/doc/fmt_emscripten_compatibility.md`. The user explicitly approved the one-line `checker(s)` to `checker(str_)` fix, now applied to bundled `fmt/base.h`. `python cmake/probes/emscripten/test_fmt_compatibility.py` passes in Debug and Release: actual bundled fmt/xxHash builds, threaded Node execution, `FMT_STRING` formatting and invalid-format compile rejection. Native `fmt` targets also build successfully in both configurations under `build/desktop-platform-after`. SDK 6.0.9 remains pinned. Task 2.3 remains pending only for unavailable real runtime/module command verification; dependency probes do not complete that criterion.

## 1. Toolchain contract

- [x] 1.1 Evaluate a specific stable emsdk candidate with a bounded C++20 coroutine and pthread compile/link probe on Windows; record the exact candidate, CMake/Ninja versions, commands, and results, distinguishing probe success from real-runtime validation.
- [x] 1.2 Add the exact SDK version metadata and a PowerShell preflight entry point; verify matching, missing, and mismatched active SDK cases report the expected result without installing, activating, or upgrading the SDK.
- [x] 1.3 Add a CMake-side SDK identity/version check for direct configuration; verify bypassing the PowerShell entry point still rejects an incompatible toolchain with an actionable diagnostic.

## 2. Presets and platform build options

- [x] 2.1 Add independent Ninja Debug/Release browser configure/build presets and separate build/output directories; verify preset resolution does not inherit the desktop vcpkg toolchain or Windows SDK settings.
- [x] 2.2 Add Emscripten target selection in the platform setup and target-scoped C++20/browser compiler options; verify configuration recognizes the target and generated commands do not contain MSVC-only switches or Windows/x86-only definitions introduced by the shared build helpers.
- [x] 2.3 Propagate pthread compilation/link settings and select worker execution at the application link; verify generated commands for participating bundled libraries, runtime targets, and the executable in both configurations.
- [x] 2.4 Keep existing desktop presets independent of browser SDK discovery; verify representative desktop configuration succeeds without an active emsdk and its compiler/cache settings are unchanged.

## 3. Minimal graph integration

- [x] 3.1 Verify the prerequisite minimal-runtime-profile implementation exposes the shared minimal framework and explicit dependency/module selection; record its concrete target names and source revision before completing graph integration. If absent, record the dependency and leave this task pending.
- [x] 3.2 Connect browser preset selection to the minimal profile in top-level, engine/core, third-party, and sample CMake; verify the configured graph excludes Graphics, UI, VFX, DirectX, Qt, USD, shader tools, and unrelated samples/tests.
- [x] 3.3 Gate host-generator checks, desktop install rules, and source-tree desktop test-wrapper generation according to the selected profile; verify a minimal configure requests only actual host prerequisites and leaves desktop-generated source files untouched.
- [x] 3.4 Configure required bundled libraries from recorded revisions without the vcpkg manifest/toolchain; verify configuration with desktop dependency paths unavailable, and verify a deliberately missing required source produces a specific error rather than host-library fallback.
- [x] 3.5 Select `app_sample_main_min.cpp` explicitly and reuse static module registration with the required modules; verify source/link inputs contain exactly one entry point and preserve a valid existing native sample target.
- [x] 3.6 Add a separate native Windows validation configuration consuming the same minimal framework target; verify its graph has no Emscripten options and its generated files are isolated from both browser configurations.

## 4. Output staging

- [x] 4.1 Inspect the selected SDK's actual application link outputs and add runtime-package staging per configuration; verify clean output contains the Wasm binary, loader, and all required worker-support files without depending on a fixed worker filename convention.
- [x] 4.2 Ensure staging inventories current outputs instead of silently retaining obsolete runtime artifacts; verify rebuilding from a clean staging directory produces the same required runtime-file set.
- [x] 4.3 Preserve relocatable runtime resource URLs and keep Debug symbols optional for execution; verify the package contains no required runtime references to original source-tree, SDK, or absolute workstation paths.

## 5. Integrated validation

- [x] 5.1 Verify the prerequisite Wasm core, browser platform services, and lifecycle implementations are available for the real selected entry point; record their revisions and keep application-build checks pending if any prerequisite is absent.
- [x] 5.2 Build the actual minimal Nau application in clean Debug and Release directories with the pinned SDK; verify both complete successfully, use Wasm-compatible link inputs, and produce independent packages. Record the final SDK compatibility result.
- [x] 5.3 Exercise build-contract failure cases for missing SDK, mismatched SDK, missing required bundled sources, and attempted native cache reuse; verify clear diagnostics and no implicit dependency/SDK changes.
- [x] 5.4 Once the delivery-owned page/server are available, copy each package outside the source tree and serve it under a different URL base in Chrome on Windows with required headers; verify Wasm/worker loads, static module availability, and worker entry-point execution without source/SDK-path requests. Record evidence without treating this as complete lifecycle validation.
- [x] 5.5 Build the native minimal target and run the prerequisite focused lifecycle checks, then build representative existing desktop targets affected by CMake changes; verify no browser flags or dependencies leak into native configuration and record any unrelated pre-existing failures separately.

## 6. Documentation and completion evidence

- [x] 6.1 Add engine-local PowerShell build documentation covering the exact SDK pin, explicit setup/activation, CMake/Ninja prerequisites, recorded submodule sources, Debug/Release commands, package paths, and the delivery boundary; verify every documented command matches the implemented entry points and presets.
- [x] 6.2 Record a reproducibility walkthrough from a clean checkout/environment using the documented prerequisites; verify generated files need no manual edits and tracked configuration contains no workstation-specific paths.
- [x] 6.3 Review results against every scenario in `specs/emscripten-build/spec.md`; record evidence and leave unverified or prerequisite-blocked tasks unchecked. Confirm the change contains no NauDemo, renderer, editor, or unrelated submodule implementation changes.

Interim task 6.3 review: `validation.md` covers all 16 scenarios, separates verified
contracts from partial/blocked runtime acceptance, and records the scope audit.
Refresh it after future implementation; the review does not complete any blocked task.

## Delivery completion evidence (2026-09-20)

The subsequent `minimal-web-delivery-validation` implementation verifies tasks
4.1?4.3, 5.2, 5.4 and 6.1 with independent clean Debug/Release builds, current
package hashes, stale/missing-input staging checks and external-copy Chrome
execution under a nested URL. See `../minimal-web-delivery-validation/validation.md`
and the current scenario review in validation.md. This delivery milestone reached
23/24 tasks. Earlier pending-status notes above describe historical prerequisite
milestones; see the task 6.2 closure note below for the current status.

## Task 6.2 closure at user request

Task 6.2 is marked complete at the user's explicit request. The checklist is now
24/24 complete. A fresh-checkout/environment walkthrough was described, but no
such run was executed or independently verified in this session. This tracking
closure does not constitute reproducibility test evidence.
