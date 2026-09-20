# emscripten-build Specification

## Purpose

Enable developers on Windows to reproducibly build the minimal Nau application into complete threaded WebAssembly runtime packages, independently of desktop rendering dependencies and native build caches.

## Requirements

### Requirement: Documented Windows build procedure

The project SHALL provide a Windows/PowerShell setup, configure, and build procedure for the minimal browser application. It SHALL identify required tool versions and repository dependencies without requiring edits to generated files or tracked workstation-specific paths.

#### Scenario: Build from a fresh checkout
- **WHEN** a developer initializes the recorded dependencies and follows the procedure with the documented prerequisites and required runtime implementations available
- **THEN** both supported browser configurations produce the actual minimal Nau runtime package without manual edits to generated files.

### Requirement: Explicit exact SDK selection

The project SHALL record one exact supported external emsdk release selected through compatibility validation. Configuration SHALL reject a missing or incompatible active SDK with an actionable diagnostic. Configure and build operations SHALL NOT install, activate, or upgrade an SDK implicitly.

#### Scenario: Supported external SDK
- **WHEN** the developer explicitly activates the recorded SDK release
- **THEN** the build accepts that toolchain and reports its identity in the configuration output.

#### Scenario: Missing or incompatible SDK
- **WHEN** the compiler or required SDK toolchain files are missing, or the active compiler version differs from the recorded version
- **THEN** configuration fails before compiling project targets and reports the expected version, the detected version when available, and setup guidance.

#### Scenario: No implicit SDK changes
- **WHEN** configure or build is invoked with an unsuitable SDK
- **THEN** the operation does not install, activate, or upgrade an SDK as a recovery action.

### Requirement: Isolated Debug and Release configurations

The project SHALL expose CMake/Ninja Debug and Release browser presets with distinct build and runtime-output directories. Debug SHALL enable diagnostic support and Release SHALL enable optimization. Browser configurations SHALL NOT reuse native CMake caches or inherit desktop-only toolchain settings.

#### Scenario: Both configurations coexist
- **WHEN** Debug and Release are configured and built in the same checkout
- **THEN** each produces its own runtime package without overwriting the other's generated artifacts.

#### Scenario: Native cache remains independent
- **WHEN** a developer configures the browser build beside an existing Windows build
- **THEN** the native cache and its compiler/toolchain selection remain unchanged.

### Requirement: Minimal dependency configuration

The browser build SHALL compile only the selected minimal runtime and its required bundled dependencies at recorded source revisions, without requiring the desktop vcpkg manifest or toolchain. Configuration SHALL exclude desktop rendering, UI, VFX, Qt, USD, and shader-tool dependency chains. Required target libraries SHALL be built for WebAssembly rather than reused from native Windows outputs.

#### Scenario: Desktop dependencies are unavailable
- **WHEN** the documented browser prerequisites and required bundled sources are available but vcpkg, Qt, USD, and DirectX development dependencies are unavailable
- **THEN** browser configuration does not require or discover those desktop dependencies.

#### Scenario: Native binaries are present
- **WHEN** prebuilt native engine libraries exist in the checkout during a browser build
- **THEN** the browser link uses WebAssembly-compatible dependencies built from the selected sources, not those native libraries.

#### Scenario: Required source is missing
- **WHEN** a required bundled source dependency is absent
- **THEN** configuration identifies the missing dependency and fails rather than substituting a host library or silently changing dependency revisions.

### Requirement: Static threaded application output

Both browser configurations SHALL statically link the selected runtime modules with consistent pthread support across the application and its compiled dependencies. The resulting package SHALL support execution of the Nau application entry point on a worker and SHALL NOT require desktop DLL loading or provide an implicit single-threaded fallback.

#### Scenario: Thread settings are consistent
- **WHEN** either configuration is compiled and linked
- **THEN** its application and participating runtime libraries use compatible threaded settings, and the final link selects worker execution for the application entry point.

#### Scenario: Static module integration
- **WHEN** the built package initializes with the prerequisite browser runtime available
- **THEN** the selected modules are available without fetching native DLLs or separately loading dynamic Wasm side modules.

### Requirement: Exact minimal entry-point selection

The browser target SHALL use `minimalApp/app_sample_main_min.cpp` from the selected external NauSamples checkout as its entry-point source and SHALL link exactly one application entry point. It SHALL consume the dedicated minimal framework shared with native validation rather than a mock runtime.

#### Scenario: Both existing sample sources are present
- **WHEN** the sample directory contains both existing source files defining an entry point
- **THEN** the browser target selects the requested minimal source without linking the other entry point.

### Requirement: Complete relocatable runtime packages

Each configuration SHALL produce a runtime package containing its Wasm binary, JavaScript loader, and every additional worker-support artifact required by the selected SDK. The package SHALL be loadable from a different serving location without access to the original source tree or SDK installation. The package SHALL NOT depend on stale outputs from a previous build for completeness.

#### Scenario: Package is copied
- **WHEN** a freshly built package is copied outside the checkout and loaded by the delivery test page under a different URL base in Chrome with the required hosting headers
- **THEN** its Wasm and worker runtime resources load without requests to the original source-tree or SDK paths.

#### Scenario: Clean output generation
- **WHEN** a configuration is built into a clean output location
- **THEN** it produces all runtime files needed by the selected SDK, whether worker support is emitted separately or embedded in the loader.

### Requirement: Native minimal build coexistence

The build integration SHALL support a separate native Windows build of the shared minimal framework using the supported VS 2026/v145 MSVC baseline and preserve desktop configuration and dependency behavior under the replacement VS 2026 presets. Native minimal preset names SHALL remain available; retired VS 2022 desktop presets SHALL NOT be required for coexistence. Browser-only flags and dependency substitutions SHALL NOT leak into native targets. Browser configuration SHALL remain independent of the native VS installation and toolchain baseline checks.

#### Scenario: Native validation configuration
- **WHEN** the shared minimal framework is built in its native Windows configuration
- **THEN** it links with the VS 2026/v145 Windows toolchain without Emscripten flags and is available for the native lifecycle validation suite.

#### Scenario: Existing desktop build
- **WHEN** a supported replacement VS 2026 desktop preset is selected without the minimal browser profile
- **THEN** it retains its desktop configuration and dependency behavior, with no requirement for emsdk.

#### Scenario: Browser build has no native toolchain
- **WHEN** the documented browser prerequisites are present but VS 2026 is unavailable
- **THEN** browser configuration and build do not require native VS discovery or apply MSVC compiler-version checks to Emscripten.
