# windows-native-toolchain Specification

## Purpose

Provide a consistent supported Windows compiler baseline across Nau source builds, applications, editor and installed SDK consumers, with actionable migration guidance.

## Requirements

### Requirement: Supported Windows MSVC baseline

Native Windows MSVC builds SHALL use the Visual Studio 2026 v145 compiler family on x64. Documented Visual Studio workflows SHALL require CMake 4.2 or newer and select the Visual Studio 18 2026 generator, x64 target and v145 toolset explicitly. Selection SHALL NOT silently fall back to VS 2022 or v143.

#### Scenario: Multiple toolchains are installed
- **WHEN** a supported Visual Studio preset is configured with VS 2022 and VS 2026 installed, including older tools inside VS 2026
- **THEN** the resulting build selects VS 2026 and v145 for x64 and reports its actual compiler identity

#### Scenario: Supported installation is missing
- **WHEN** a native Visual Studio workflow is requested without the required CMake or VS 2026 C++ tools
- **THEN** it fails with prerequisite guidance rather than selecting an older installation

### Requirement: Obsolete MSVC inputs are rejected

Native configuration SHALL reject VS 2022 generators, v143 toolsets and MSVC compiler families outside the supported VS 2026 baseline before compiling project targets. Diagnostics SHALL identify the expected baseline, the detected selection where available, and the need for a clean supported configuration. The same compiler baseline SHALL apply to native Ninja/MSVC builds.

#### Scenario: Old compiler is explicitly selected
- **WHEN** a developer configures a native build with VS 2022, v143 or an older MSVC compiler through a direct command or custom preset
- **THEN** configuration fails with actionable migration guidance

#### Scenario: Ninja selects old MSVC
- **WHEN** a native Ninja build discovers an older MSVC compiler from the environment
- **THEN** configuration rejects it even though no Visual Studio generator was selected

### Requirement: Consistent public native entry points

The engine, editor and exported SDK SHALL replace public `win_vs2022_x64*` presets with corresponding `win_vs2026_x64*` presets, retaining the available static, DLL and diagnostic variants. Active build helpers, installer commands, validation probes and generated-project workflows SHALL select the supported baseline. Native minimal preset names SHALL remain available. Retired VS 2022 preset names SHALL NOT remain supported aliases.

#### Scenario: Developer selects a native variant
- **WHEN** a developer uses a documented engine, editor or SDK native preset or helper
- **THEN** it selects the supported compiler and architecture with the requested configuration and linkage/diagnostic settings

#### Scenario: Old preset name is used
- **WHEN** a developer requests a retired VS 2022 preset
- **THEN** it is unavailable and the migration documentation identifies its replacement

### Requirement: Compatible native build inputs

Native applications and SDK consumers SHALL use engine outputs and dependencies compatible with the supported compiler and configuration. NauDemo's fast build workflow SHALL verify its engine build's toolchain provenance before reusing those outputs and SHALL reject obsolete inputs with rebuild guidance. Qt, USD and other dependency support SHALL be based on successful compilation, linking and runtime validation, rather than package naming alone.

#### Scenario: Fast builder receives an old engine build
- **WHEN** NauDemo's fast builder is given a VS 2022/v143 engine build directory
- **THEN** it rejects that input before linking and identifies how to build a supported engine configuration

#### Scenario: Supported consumers are built
- **WHEN** native engine, samples, NauDemo and editor are built with the supported dependency set
- **THEN** their applicable tests and documented startup, resource loading and normal shutdown behavior succeed

#### Scenario: Installed SDK is relocated
- **WHEN** a supported SDK is installed and copied outside the source checkout
- **THEN** representative installed samples build with the supported compiler and resolve their runtime resources without source-tree dependencies

### Requirement: Separate clang-cl compatibility

Existing clang-cl presets SHALL remain available and use a validated VS 2026 Windows SDK/STL environment. Compiler checks SHALL distinguish clang-cl from MSVC and SHALL NOT apply MSVC numeric compiler-version rules to Clang. Documentation SHALL identify the independently validated Clang version and required environment.

#### Scenario: clang-cl is selected
- **WHEN** a developer builds using a retained clang-cl preset and its documented prerequisites
- **THEN** configuration recognizes Clang separately, and the selected native build and affected tests succeed with compatible Windows development dependencies

### Requirement: Reproducible migration guidance

Current build and prerequisite documentation SHALL provide the supported tool versions, old-to-new preset mapping, clean native build instructions and dependency setup. Completion evidence SHALL identify repository revisions, toolchain/dependency identities, commands and actual results for supported native routes and browser regression checks. Unavailable or failed acceptance checks SHALL remain explicitly incomplete; historical VS 2022 evidence SHALL NOT be relabelled as VS 2026 validation.

#### Scenario: Developer migrates an existing checkout
- **WHEN** a developer follows the migration instructions with an existing VS 2022 cache present
- **THEN** the new native build uses a clean supported configuration without requiring VS 2022 to be uninstalled

#### Scenario: Fresh checkout reproduces the build
- **WHEN** a developer initializes the recorded repository inputs and follows the documented prerequisites and commands without copied native build outputs
- **THEN** the documented native build succeeds using the supported compiler, with evidence sufficient to identify the tested inputs
