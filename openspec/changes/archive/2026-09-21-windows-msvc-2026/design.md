# Design

## Context

See proposal.md for motivation. Engine, editor and exported SDK presets select VS 2022/v143. Native minimal and browser-validation probes also name the old generator. NauDemo's fast builder emits v143 projects and discovers the latest MSBuild without constraining the VS generation; the editor installer selects an old preset. Several DLL presets bypass the existing x64/toolset base, so renaming one base is insufficient.

This workstation has CMake 4.2.1 and VS Community 2026 alongside VS 2022 Build Tools. The VS 2026 instance contains MSVC 14.29, 14.44 and 14.51.36231: discovering that instance alone does not guarantee the intended compiler. No VS 2026 build has been validated during planning. Existing extraction evidence uses VS 2022 and remains historical.

## Goals / Non-Goals

**Goals:** Make compiler selection consistent across entry points, reject obsolete selections early, and establish measured compatibility for desktop dependencies and SDK consumers.

**Non-Goals:** Change runtime behavior, add architectures, uninstall installed toolchains, upgrade browser dependencies, or promise plain Clang/MinGW compatibility.

## Decisions

### Explicit generator and toolset selection

Use `Visual Studio 18 2026`, `v145,host=x64` and x64 for VS presets. CMake introduced this generator in 4.2, with v145 as its default ([CMake documentation](https://cmake.org/cmake/help/v4.2/generator/Visual%20Studio%2018%202026.html)). Explicit toolset selection prevents older tools installed inside VS 2026 from being selected accidentally. Do not pin the local installation path or exact servicing version into tracked configuration.

Require CMake 4.2 for the native workflow and report missing prerequisites before useful build work begins. Scope checks so the unchanged Emscripten workflow does not acquire a VS installation or higher CMake requirement solely because the host is Windows. A global minimum increase affecting every browser entry point is unnecessary.

For native MSVC, validate the actual compiler and selected generator/toolset rather than preset names alone. MSVC_VERSION 1950 through 1959 identifies VS 18/v145 ([CMake compiler mapping](https://cmake.org/cmake/help/latest/variable/MSVC_VERSION.html)). Reject VS 2022, v143, older MSVC and unsupported compiler generations with expected/detected identity and clean-configuration guidance. Native Ninja/MSVC receives the same compiler check. The Emscripten platform branch must remain ahead of Windows host checks.

### Preserve interfaces except the requested preset migration

Rename public `win_vs2022_x64*` presets to `win_vs2026_x64*`, including DLL and ASAN variants, across engine, editor and installed SDK. Ensure every variant inherits the selected architecture and toolset. Update configure references in build presets and all active helper defaults. Retain generic build-preset labels where useful, native minimal preset names, sample targets and configuration-relative output layouts. Old preset aliases are deliberately removed to make the support boundary unambiguous.

Update the editor installer, native scene/profile probes, SDK install helper and generated-project entry points. Replace any test that assumes all old preset objects are unchanged with checks for the intended native migration and unchanged browser settings. Do not rewrite archived evidence or indiscriminately replace version strings in bundled sources.

NauDemo's fast builder must select an eligible VS 18 instance with C++ tools and verify that its source engine cache/projects use the supported toolchain before linking their outputs. Generate a valid MSBuild project with v145; select project-schema fields according to MSBuild semantics rather than mechanically changing every `17` to `18`. A renamed output folder is not sufficient proof of compiler provenance.

### Validate dependencies without assuming a package rename is required

Use clean engine and application build trees. Select a consistent VS 2026 environment for vcpkg, compiler and SDK discovery, recording the resulting tool identities and dependency revisions. Keep existing Qt 6.4.1 and OpenUSD 24.08 inputs if compilation, linking and runtime checks demonstrate compatibility. A package labelled `msvc2022` describes its producer and does not by itself require the old compiler to remain supported.

Rebuild incompatible dependencies with the selected toolchain and make focused compatibility fixes where needed. Do not bypass library version guards or suppress errors to claim support. If a major Qt/USD upgrade is necessary, revise the affected plan before broadening implementation. Microsoft's compatibility statement is useful context but is not evidence that this repository's dependencies work ([MSVC release notes](https://learn.microsoft.com/en-us/cpp/overview/what-s-new-for-msvc?view=msvc-170)).

### Keep clang-cl distinct

Retain existing clang-cl presets and validate them with the VS 2026 Windows SDK/STL environment. CMake's MSVC compatibility flag is also true for clang-cl, so compiler-family checks must distinguish the compiler ID before applying the MSVC version rule. Record the tested Clang version separately. Do not silently remove this route or treat an MSVC-only success as proof of Clang compatibility.

### Acceptance evidence covers consumers

Use separate clean trees and preserve logs by configuration to avoid shared CTest discovery files masking the compiler/configuration actually tested.

| Area | Required evidence |
| --- | --- |
| Selection | Preset inventory; detected compiler/toolset/SDK; rejection of old MSVC/toolsets and old fast-builder inputs; no fallback when VS 2026 is absent |
| Engine and samples | Static Debug/Release sample target baseline; runtime and allocator tests; native minimal lifecycle suite; SceneBaseSample and inputDemo startup, input and close checks |
| Desktop variants | DLL Debug/Release and exposed ASAN/RelWithDebInfo routes configured and built with representative affected targets |
| NauDemo | CMake and fast-builder Debug/Release builds, resources, scene behavior and normal close |
| Editor | Debug/Release builds, applicable tests and editor startup/project loading/close with Qt/USD dependencies |
| clang-cl | Existing documented static/DLL routes built and affected runtime tests run using a recorded compatible Clang version |
| SDK | Install, relocate outside source checkout, build representative minimal/scene/input/script consumers, and verify runtime asset discovery |
| Browser | Minimal/demo Debug/Release builds and existing delivery/lifecycle/relocation checks with SDK 6.0.9, plus configuration without native VS discovery |
| Reproduction | Fresh checkout using documented prerequisites and commands, with no copied native caches or generated projects |

Unavailable checks remain incomplete. Human visual acceptance must refer to the new binaries; previous VS 2022 acceptance cannot be reused.

## Risks / Trade-offs

- New STL/compiler diagnostics in bundled dependencies → isolate compatibility fixes and run affected regression tests; avoid unrelated third-party edits.
- Qt/USD or other prebuilt binaries fail to link or run, especially with LTCG → verify producer settings and rebuild affected libraries; revise the plan if a major dependency upgrade is required.
- Co-installed VS versions or vcpkg caches select old tools → constrain discovery and inspect compiler/cache provenance on each supported route.
- Removing preset aliases breaks scripts and caches → provide an explicit old-to-new mapping and use fresh native build directories.
- clang-cl may need a newer compiler for the selected STL → measure compatibility and document the tested version independently.

## Migration Plan

Implement engine selection and native presets first, then dependent editor/SDK/demo/probe entry points. Validate clean builds before publishing updated support claims. Update current root/component guides, prerequisites and applicable AGENTS instructions together with command examples. Preserve browser commands and archived history.

Use new native directories; do not retarget an existing VS 2022 CMake cache in place. Native minimal presets retain names, so their old build trees require explicitly documented cleanup or replacement. Rebuild consumers and any incompatible dependencies before running acceptance checks.

If rollback is needed, restore the coordinated parent and component revisions and use separate old-toolchain build trees. Commit/push operations are outside this planning request.
