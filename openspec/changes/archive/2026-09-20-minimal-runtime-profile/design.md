# Design

## Context

See proposal.md for motivation. ApplicationImpl owns the real service startup,
application work queue, stepping and multi-phase shutdown. Its UI/VFX updates and
MainLoopService's scene/ImGui calls pull in the rendering framework. Default
delegates and application utility/configuration sources add scene/assets/input
dependencies that the selected direct createApplication entry point does not use.
NauKernel already declares bundled dependencies, while core and third-party CMake
currently enumerate broad desktop target sets.

## Goals / Non-Goals

**Goals:** Share lifecycle implementation, expose a concrete minimal target and
dependency selection, and demonstrate native initialization/step/stop behavior.

**Non-Goals:** Browser service implementations, Wasm source portability, renderer
changes, redesigning application startup error semantics, or a copied/mock runtime.

## Decisions

- Add `NAU_RUNTIME_PROFILE` with desktop default and explicit minimal selection.
  `cmake/NauMinimalRuntime.cmake` owns `NAU_MINIMAL_MODULES` (`PlatformApp`), matching
  module directories and bundled dependency directories/targets. Reject unknown
  profiles and unsupported requested modules with actionable configure errors.
  Minimal native configuration uses the VS 2022 toolchain without vcpkg; all
  selected dependencies come from recorded bundled sources.
- Add `NauFrameworkMinimal` using an explicit list of existing sources:
  application_impl/setup, background_work_service, global_properties_impl,
  logging_service, platform_window_service, main_loop_service and
  concurrent_execution_container. It links NauKernel and PlatformAppApi.
  Exclude run_application, default_application_delegate, application_utils and
  application_init_delegate implementation because these expose desktop rendering
  or asset-configuration behavior beyond the direct minimal entry point.
- Compile those same lifecycle files with private `NAU_MINIMAL_RUNTIME` selection.
  Guard only optional scene/UI/VFX/ImGui includes, members and calls. Existing
  full-framework builds compile their existing feature paths. This avoids copying
  or independently rewriting startup/shutdown algorithms. A larger abstract hook
  hierarchy is unnecessary for this single opt-in profile.
- The Windows window manager also guards its optional renderer resize/close calls
  under the private profile definition, retaining native window/message behavior.
- Retain the kernel's current source set and declared low-level dependencies,
  including compression libraries required to compile its existing IO sources.
  Do not claim this profile already provides Wasm-compatible kernel internals.
  Filter dependency/module/sample enumeration before entering their CMake files;
  gate unused generators and desktop installation/wrapper generation.
- Native presets use separate Debug/Release build directories and enable focused
  minimal tests without enabling the full kernel/framework suites. The sample
  selects app_sample_main_min.cpp explicitly; the existing desktop sample selects
  app_sample_main.cpp. Both reuse generated static PlatformApp registration.
- Native tests exercise the same minimal framework with real PlatformApp/window
  services, pre/post update service callbacks and orderly stop, bounded by CTest
  timeout. Add graph inspection and missing-source/unsupported-module cases.

## Risks / Trade-offs

- Hidden kernel dependencies -> compile/link the full selected native source graph
  and record the actual list; keep unrelated rendering dependencies excluded.
- Conditional feature paths drift -> retain shared lifecycle source files and
  configure/build representative full-framework targets for regression evidence.
- Threaded window shutdown hangs -> run the real platform service with bounded
  lifecycle tests; report runtime defects rather than replacing services with mocks.
- Native success mistaken for browser completion -> keep the browser guard until
  emscripten-build graph integration; portability and browser services stay separate.

## Migration Plan

Opt in using native minimal presets; existing desktop presets keep defaults.
Consumers link one framework variant in a process. Rollback removes the opt-in
profile and target without modifying saved data or user SDK installations.
