# Design

## Context

See `proposal.md` for motivation and scope. The accepted decisions are recorded in the repository-root `web-port-spec-list.md`.

Observed build constraints in `NauEngineLite`:

- `CMakePresets.json` puts the desktop vcpkg toolchain and Windows system version in its shared base preset.
- `cmake/platformSpec/NauPlatformSetup.cmake` rejects targets other than Windows and classifies pointer sizes as x86/x64.
- `engine/3rdparty_libs/CMakeLists.txt` configures a broad fixed list including DirectX, DXC, RenderDoc, Jolt, and animation tools. Disabling top-level tools alone is insufficient.
- `engine/core/CMakeLists.txt` discovers all modules, while `NauFramework` publicly links scene, graphics, UI, and VFX targets.
- Both minimal-sample source files contain `main()`, and its CMake target currently collects both.
- `nau_target_link_modules` already generates static module registration when shared libraries are disabled. Reuse this behavior rather than inventing another registry.
- The root build checks Python generator packages unconditionally, configures a source-tree `run_tests.bat`, and defines desktop SDK installation rules.
- Existing `test_app` links the full framework and ScriptsLua; it is not evidence that the future minimal profile passes lifecycle tests.

## Goals / Non-Goals

**Goals:** isolate target-platform selection from the Windows host, provide repeatable browser build commands and complete outputs, and integrate the same minimal framework that native validation will use.

**Non-Goals:** implement missing runtime services or use stubs to claim a successful application port. SDK probes verify toolchain capabilities only. Rendering and browser delivery implementation remain outside this change.

## Decisions

### 1. External SDK and an explicit preflight

Keep emsdk outside the repository. Record a validated exact release in `NauEngineLite/cmake/emscripten-sdk-version.txt` (proposed path). A PowerShell build entry script will check the active compiler version, SDK/toolchain availability, CMake, and Ninja before configuring. It will print expected/actual versions and explicit installation/activation instructions on failure, without installing anything itself. Recheck compiler identity inside the browser CMake configuration so direct preset invocation cannot bypass the version contract.

Choose the release during implementation using a bounded C++20/pthread compile-link check on Windows, then confirm it against the real dependency graph. Do not commit `latest` or treat a successful probe as final SDK validation. Record the selected version and validation evidence together.

Alternative: vendoring or automatically downloading emsdk would simplify discovery but contradict explicit external SDK management and add repository/download maintenance.

### 2. Browser presets independent of the desktop base

Add proposed presets `web-minimal-debug` and `web-minimal-release`, using Ninja, Emscripten's CMake toolchain, and `build/<preset-name>` directories. They must not inherit the existing desktop `config_base`. Use `CMAKE_BUILD_TYPE` for these single-configuration builds. Derive toolchain paths from the activated external SDK, not a tracked absolute workstation path.

Use C++20, static libraries, and the dedicated minimal profile. Debug enables usable diagnostics; Release enables optimization. Keep existing native preset settings intact. Native validation gets an independent minimal-profile configuration and cannot reuse a browser cache.

Alternative: invoking the Visual Studio preset through `emcmake` would retain incompatible generator, vcpkg, and Windows settings. A separate top-level build duplicating engine target definitions would drift from native code.

### 3. Filter the graph before configuring dependencies

Introduce build-side selection for the minimal profile in the existing top-level/core/third-party/sample CMake structure. Consume the profile's explicit module and dependency lists instead of recursive discovery. The runtime-profile work owns the exact required source set and minimal framework split; this change owns selecting that set in browser presets.

Build required bundled libraries from source at existing recorded revisions. Skip the desktop vcpkg manifest, USD discovery, shader tools, unrelated tests/samples, and desktop installation rules for the browser profile. Host Python can still be required for genuine generators; run `cymbal`/`clang` checks only if the selected graph uses those generators. Do not execute a Wasm-built generator as a Windows program.

Use Emscripten target detection before the existing Windows target branch; keep host-Windows checks separate. Update compile-option helpers so MSVC switches, Windows definitions, and x86 assumptions do not leak onto browser targets. Low-level source portability fixes are owned by `wasm-core-portability`.

Alternative: building everything and relying on linker dead stripping cannot avoid configure-time failures or compilation of unsupported libraries.

### 4. Thread settings and static registration

Apply `-pthread` consistently to participating source builds and final linking. Apply `-sPROXY_TO_PTHREAD` at the application link so the entry point runs on a worker. Keep flags target-scoped through a shared build-options target or equivalent propagation; verify actual compile/link commands rather than relying on a flag on the executable alone.

Reuse Nau's generated static module initialization, linking only the profile's required modules. Explicitly select `app_sample_main_min.cpp` for the minimal target. Preserve a single, valid entry point for the existing native sample when correcting source discovery.

Worker pool sizing remains a lifecycle integration detail determined by observed startup behavior. No single-threaded fallback, browser GPU flags, or dynamic side modules are introduced. Hosting headers belong to delivery, while the package must include everything needed by this threaded output format.

Reference: [Emscripten pthread support](https://emscripten.org/docs/porting/pthreads.html) and [CMake cross-compilation](https://emscripten.org/docs/compiling/Building-Projects.html).

### 5. Package boundary and relocation

Stage browser-consumed outputs into `build/<preset-name>/package/` (proposed layout). Include the Wasm binary, JavaScript loader, and any additional worker scripts actually emitted by the pinned SDK. Do not assume every SDK emits a separate `.worker.js`. Debug symbols can live alongside the package, but no runtime request may depend on their original source paths.

Stage from the current build's outputs so old worker files cannot disguise an incomplete package. The test page and server are separate consumers owned by delivery work. They must be able to load a copied package from a different directory and URL base with the required cross-origin isolation. Local source and SDK paths may occur in debugging metadata; they must not be required runtime fetch locations.

Alternative: shipping the whole build tree hides accidental dependencies and makes configuration isolation difficult to verify.

### 6. Integration prerequisites and completion evidence

Build infrastructure can be developed before the runtime port is complete. Full compile/link/package acceptance depends on the dedicated minimal framework, Wasm-compatible core, platform service, and application lifecycle implementations. Record these as explicit prerequisites in tasks; do not silently expand this build-only change to implement them or mark blocked checks passed.

The Chrome relocation/load check uses the delivery-owned test page once available. Native validation builds the same framework and runs its focused lifecycle checks once supplied. The existing full-framework test suite can provide regression evidence but cannot replace those minimal-profile checks.

## Risks / Trade-offs

- Hidden desktop dependencies -> inspect configured targets, compile commands, and link inputs; test with vcpkg/Qt/USD unavailable.
- Partial pthread configuration -> audit dependent library commands and validate Debug and Release separately.
- SDK behavior changes -> exact pin, explicit upgrades, and generated-output inventory checks.
- Runtime prerequisites are incomplete -> retain pending integration tasks and report the missing capability; never substitute a mock application.
- Native regressions from graph filtering -> keep the minimal profile opt-in and compare representative existing desktop targets plus native minimal validation.
- Cross-compilation runs target tools on the host -> identify host generators explicitly and exclude unused generator checks.

## Migration Plan

1. Add SDK metadata/preflight and browser presets without changing desktop defaults.
2. Integrate the minimal profile's dependency graph and explicit sample selection as its runtime work becomes available.
3. Add package staging and meaningful build-contract checks; document PowerShell commands and negative cases.
4. Validate actual Debug/Release packages and native coexistence after prerequisite implementations are ready. Record SDK/tool versions and limitations.
5. Commit implementation in the engine submodule and record its revision in the parent when integrating the change. Do not include unrelated submodule work or NauDemo changes.

Rollback disables/removes the opt-in browser build additions and their parent revision update; no saved-data migration is involved. Preserve user build directories and external SDK installations.

## Open Questions

- Which exact emsdk release passes the bounded compatibility checks and real minimal build? Version selection is explicitly deferred to validation; no release is claimed supported yet.
- Which SDK-generated auxiliary files must be staged? Inspect the selected release's actual link outputs and runtime requests.
- What minimum supported CMake/Ninja versions are demonstrated by validation? Record those prerequisites with the reproducible build procedure.
