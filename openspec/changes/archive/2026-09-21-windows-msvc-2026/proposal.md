# Proposal

## Why

Native Windows builds still select Visual Studio 2022/v143 even though Visual Studio 2026 is installed and the user wants it to replace the supported MSVC baseline. Updating presets alone would leave helpers, SDK consumers and validation probes selecting obsolete tools or reusing incompatible build outputs.

## What Changes

- **BREAKING**: replace the Windows MSVC baseline with Visual Studio 2026, the `Visual Studio 18 2026` generator, x64 and toolset `v145`; require CMake 4.2 or newer for these native workflows.
- **BREAKING**: replace `win_vs2022_x64*` presets with `win_vs2026_x64*` in the engine, editor and installed SDK. Remove VS 2022 aliases and reject explicit obsolete native MSVC toolchains with migration guidance.
- Update native minimal presets, probes, installer helpers, generated-project defaults and NauDemo's fast builder to select and validate the new toolchain. Preserve sample/application target names and native minimal preset names.
- Retain clang-cl presets as a separate compiler route using the VS 2026 Windows development environment; validate their compatibility separately from MSVC. Plain Clang and MinGW support are not expanded.
- Validate engine-owned source builds, third-party dependency compatibility, Qt/USD editor integration, native samples and SDK consumers using clean build directories. Retain working dependency versions where compatibility is demonstrated.
- Update current build guides and prerequisites with the renamed presets, toolchain requirements, clean-cache migration and measured validation results. Preserve archived evidence.
- Keep browser presets, Emscripten SDK 6.0.9, dependency exclusions and runtime behavior unchanged.

## Capabilities

### New Capabilities

- `windows-native-toolchain`: VS 2026/v145 selection, obsolete-toolchain rejection, consistent Windows entry points, dependency compatibility and evidence for native builds.

### Modified Capabilities

- `external-samples`: replace the blanket promise to preserve old engine presets with the explicit VS 2026 migration while retaining sample targets, resources and runtime behavior.
- `emscripten-build`: migrate native coexistence validation to VS 2026 and preserve browser independence without promising support for retired VS 2022 presets.

## Impact

Affected areas include root guides/AGENTS, NauEngineLite presets/platform setup/SDK export/probes/project helpers, NauEditorPublic presets/installer/dependency configuration, NauDemo build.py and documentation, and current NauSamples usage guidance. Dependencies include MSVC v145, Windows SDK, CMake, vcpkg, Qt and OpenUSD; compiler-family and prebuilt-library compatibility require measured checks. This is not an instruction to uninstall VS 2022, upgrade Emscripten, rewrite historical documentation, introduce new architectures, or publish commits. Implementation begins only after a separate apply request.
