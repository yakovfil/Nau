# Tasks

## 1. Common delegate API and dispatch

- [x] 1.1 Add explicit pre/post callbacks to `ApplicationDelegate`, default post forwarding to `onApplicationStep`, and a platform-neutral runner-options overload while retaining the existing overload; verify legacy and new delegate consumers compile and common public headers introduce no concrete scene/renderer or Emscripten dependency.
- [x] 1.2 Extract common delegate registration/dispatch from desktop-only `run_application.cpp` and include it in full, scene and minimal framework profiles; verify native and browser link exactly one runner implementation and static/dynamic module registration is not duplicated.
- [x] 1.3 Dispatch eligible callbacks in their respective main-loop phases, including a closing-state check before post-update; verify module-neutral tests cover equal elapsed time, one dispatch per phase, legacy forwarding, explicit-post override and Stop from pre-update.

## 2. Checked startup and owned platform hosts

- [x] 2.1 Integrate asynchronous delegate startup readiness/results with checked host lifecycle progress and status; verify immediate/deferred startup rejection never reports Running or invokes application callbacks, while pending startup permits executor/presentation progress without counting game steps.
- [x] 2.2 Implement native owned-host execution over the checked lifecycle and preserve existing default timing/window startup; verify success and failure exit codes, notification/startup call counts, repeated Stop, partial startup disposal and delegate destruction after service teardown.
- [x] 2.3 Add the common browser runner path with delegate ownership transferred to the persistent session before scheduler handoff, reusing the existing runtime bridge and loop; verify the existing borrowed browser runner remains callable and ownership is not implicitly transferred for its callers.
- [x] 2.4 Map common scheduling options to existing browser default and cooperative presentation modes; verify fixed-cadence behavior remains available and presentation mode uses frame callbacks with bounded elapsed time and responsive Stop.
- [x] 2.5 Complete pending-startup and failed-cleanup ownership handling; verify dedicated fixture tests retain the delegate through accepted asynchronous work, do not free it on a progress timeout, and destroy it once after safe cleanup while retaining terminal failure diagnostics.

## 3. Independent host and scene integration coverage

- [x] 3.1 Add a shared-source native/browser host consumer with module-neutral test logic and production platform integration through NauEngineModules probe infrastructure; verify it starts, updates and stops without scene or rendering modules in both targets.
- [x] 3.2 Add scene-dependent phase-order coverage in NauEngineModules using the real scene manager; verify pre-update mutations are visible in component processing and post-update follows that call, without assuming completion of asynchronous component work.
- [x] 3.3 Run independent host coverage in native Debug/Release and Chrome Debug/Release for startup success/failures, explicit/legacy phase behavior, Stop during startup, cleanup errors and delegate lifetime across browser handoff; record reproducible commands and machine-readable results.
- [x] 3.4 Run affected existing minimal lifecycle/browser regressions and audit the minimal target graph; verify responsiveness, visibility/resume, default cadence and watchdog cleanup contracts, with no newly enabled scene or renderer dependency.

## 4. Migrate NauDemo

- [x] 4.1 Introduce the shared demo delegate and common `main.cpp` using the owning engine runner; verify both target source lists select the same entry and no demo entry calls a platform runner directly.
- [x] 4.2 Extract native and web configuration/presentation adapters selected by CMake, preserving asset paths, native materials/environment and web package/shader validation; verify each target links only its intended adapter and generic engine hosting contains no demo content or paths.
- [x] 4.3 Move rotation and text submission into the shared pre-update callback and web draw submission into post-update; verify no duplicate service-driven simulation remains and observed cube rotation follows elapsed time once per step.
- [x] 4.4 Preserve initialization rendering/text readiness, lifecycle polling and renderer shutdown through the adapters, then delete `web_main.cpp`; verify startup text/graphics failure still prevents successful execution and no demo test-hook option or fixture is reintroduced.

## 5. Acceptance and documentation

- [x] 5.0 Repair the approved desktop cleanup stall after rejected application startup; identify the retained work, add a regression for its cause, and verify native missing-font failure completes teardown with a nonzero exit without null-executor assertions or treating a timeout as completion.

- [x] 5.1 Build and run native NauDemo in Debug and Release; verify cube and text appearance, resize, text presentation readiness, ordinary close and diagnosed startup failure with nonzero exit, recording any unavailable prerequisite explicitly.
- [x] 5.2 Build and run browser NauDemo packages in Debug and Release; verify full-viewport canvas, cube/text rendering, frame-driven rotation, resize/DPR, visibility/resume, asynchronous Stop, missing assets and graphics/host failure through external acceptance fixtures without production test hooks.
- [x] 5.3 Document the common runner API, pre/post ordering, legacy forwarding, ownership, browser completion semantics and NauDemo's remaining private platform adapters; verify examples match the implemented API and build commands.
- [x] 5.4 Record source baselines, tools, commands and validation results for this change; run formatting/diff checks and strict OpenSpec validation, and verify unrelated existing component changes remain untouched.
