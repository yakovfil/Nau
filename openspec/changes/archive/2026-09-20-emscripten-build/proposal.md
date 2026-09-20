# Proposal

## Why

Nau's build currently assumes Windows targets, desktop dependencies, and native toolchains, so it cannot produce the agreed minimal application as a threaded WebAssembly package. A reproducible Emscripten build is needed to support the non-rendering browser milestone without bringing the renderer or NauDemo into scope.

## What Changes

- Add native Windows/PowerShell build support using an external emsdk, with one exact SDK release recorded after compatibility validation and actionable version checks. Installation and upgrades remain explicit.
- Add independent CMake/Ninja Debug and Release browser presets, isolated caches/output directories, static linking, and consistent pthread settings.
- Select required bundled dependencies from recorded source revisions without using the desktop vcpkg toolchain or manifest. Exclude desktop-only dependencies during configuration.
- Integrate the dedicated minimal framework target and explicitly select `samples/minimalApp/app_sample_main_min.cpp` as the browser entry point, preserving valid native targets.
- Produce a relocatable runtime package containing Wasm, its JavaScript loader, and all generated worker-support files required by the selected SDK.
- Document and validate setup, negative configuration cases, dependency selection, package completeness, and native build coexistence.

## Capabilities

### New Capabilities

- `emscripten-build`: Reproducible Windows-hosted builds of the minimal Nau application into complete, statically linked, threaded browser runtime packages.

### Modified Capabilities

None. The project has no existing durable OpenSpec specifications.

## Impact

Implementation belongs primarily in the `NauEngineLite` submodule: top-level CMake and presets, platform/toolchain helpers, third-party selection, minimal-sample targets, and build documentation/checks. Root OpenSpec files hold this plan; engine implementation commits and the parent submodule revision must remain coordinated.

The complete build depends on the planned `minimal-runtime-profile`, `wasm-core-portability`, and browser platform/lifecycle work described in `web-port-spec-list.md`. Those capabilities do not yet exist as completed changes. This change owns their build integration, not their runtime implementation; final package validation cannot be marked complete until the real runtime is available.

## Non-goals

- Porting runtime algorithms, Windows service implementations, or shutdown semantics.
- Creating the browser test page, server, or isolation-error UI; these belong to delivery/lifecycle work.
- NauDemo, WebGPU/WebGL, rendering, editor support, and content-tool ports.
- WSL/Linux build-host support, browser coverage beyond desktop Chrome on Windows, dynamic linking, or a single-threaded fallback.
- Silently installing SDKs, updating dependency revisions, or changing existing desktop preset behavior.
