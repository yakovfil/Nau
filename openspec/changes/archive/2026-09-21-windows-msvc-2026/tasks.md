# Tasks

User decision (2026-09-20): temporarily exclude observed failed tests from validation and record them in the root `failed-tests.md`. The exact Release exclusions are in `NauEngineLite/cmake/probes/windows_toolchain/failed-tests-release.txt`. Deferred failures remain visible and are not counted as passes; this exception does not waive build compatibility or other outstanding tasks.

## 1. Engine toolchain selection

- [x] 1.1 Migrate engine Visual Studio preset inheritance to VS 2026/v145/x64, rename public presets and update build references while retaining native minimal names; verify resolved static, DLL and ASAN presets and unchanged browser preset settings.
- [x] 1.2 Add scoped native CMake/toolchain prerequisite checks and compiler identity diagnostics; verify supported VS and Ninja/MSVC configuration, rejection of VS 2022/v143/older MSVC, and no native fallback when VS 2026 is unavailable.
- [x] 1.3 Preserve clang-cl compiler-family handling and Emscripten platform precedence; verify focused configuration checks distinguish MSVC, clang-cl and Windows-hosted Emscripten correctly.

## 2. Dependent build entry points

- [x] 2.1 Migrate editor presets and installer defaults to the supported generator, toolset and architecture; verify all native configure/build references resolve and no active installer path selects a retired preset.
- [x] 2.2 Migrate exported SDK presets, install helpers and native generated-project defaults; verify generated configurations select v145 and contain no active VS 2022 defaults.
- [x] 2.3 Update NauDemo's fast builder defaults, constrained VS/MSBuild discovery and generated project toolset; add regression coverage for supported input, obsolete engine cache rejection and missing eligible installation, then verify generated projects with MSBuild.
- [x] 2.4 Update native scene/profile probes and preset-preservation assertions; run the affected probe tests and verify they allow the intended native migration while retaining browser isolation checks.

## 3. Compiler and dependency compatibility

- [x] 3.1 Establish clean native build directories and consistent VS 2026/v145 selection for compiler, Windows SDK and vcpkg; capture source identities, dependency revisions and configure logs proving the selected tools, without importing old engine outputs.
- [x] 3.2 Build engine and the existing native sample target baseline in static Debug and Release; resolve focused compiler/STL compatibility failures and verify both builds plus affected regression tests succeed.
- [x] 3.3 Build native DLL Debug/Release and representative exposed ASAN/RelWithDebInfo targets; validate linkage and diagnostic settings from build outputs and record successful commands and results.
- [x] 3.4 Validate Qt 6.4.1/OpenUSD 24.08 integration with editor Debug/Release builds; rebuild incompatible dependency inputs or apply focused fixes as needed, recording producer/runtime compatibility and revising the plan before any required major dependency upgrade.
- [x] 3.5 Validate retained clang-cl static/DLL routes with the VS 2026 SDK/STL environment; record the working Clang version and successful builds and affected runtime tests separately from MSVC evidence.

## 4. Consumer and runtime acceptance

- [x] 4.1 Run the engine runtime and allocator regression suites with NAU_CORE_TESTS enabled, plus native minimal lifecycle validation in Debug/Release; preserve per-configuration test logs and investigate failures without reusing historical acceptance.
- [x] 4.2 Build NauDemo through CMake and its fast builder in Debug/Release; verify source-cache selection, resource loading and successful launches for each workflow.
- [x] 4.3 Run SceneBaseSample, inputDemo and NauDemo in Debug/Release, capturing startup/close logs; obtain visual/input acceptance for these new binaries and verify inputDemo's additional swapchain does not trigger an alignment assertion.
- [x] 4.4 Run applicable editor tests and verify Debug/Release editor startup, project/resource loading and normal close; record any required human visual acceptance against the new builds.
- [x] 4.5 Install and relocate the native SDK outside the source checkout; build representative minimal, scene, input and script consumers with the supported compiler and verify runtime resource discovery without original source paths.
- [x] 4.6 Rebuild browser minimal/demo Debug/Release with SDK 6.0.9 and run existing delivery, lifecycle and relocation acceptance; verify browser configuration does not invoke native VS discovery or inherit native baseline checks.

## 5. Documentation and reproducibility

- [x] 5.1 Update current root/component build guides, prerequisites and applicable AGENTS instructions with VS 2026/v145, CMake requirements, tested dependency/Clang versions, preset mappings and clean-cache migration commands; verify active instructions do not require VS 2022 while historical records and legitimate dependency producer labels remain intact.
- [x] 5.2 Perform a fresh-checkout native reproducibility walkthrough without copied build outputs; record repository inputs, setup/configure/build/test commands and results, and fix any undocumented prerequisite or workstation-specific assumption exposed by the walkthrough.
- [x] 5.3 Review acceptance evidence against every spec scenario and the design validation matrix, keeping failed/unavailable checks incomplete; run strict OpenSpec validation and verify the final change is limited to the planned toolchain migration and required compatibility fixes.
