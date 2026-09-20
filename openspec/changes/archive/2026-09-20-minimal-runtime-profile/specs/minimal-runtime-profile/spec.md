# Spec Delta

## Purpose

Provide a shared non-rendering Nau application runtime with explicit build
dependencies and native lifecycle validation for downstream browser integration.

## ADDED Requirements

### Requirement: Non-rendering runtime selection
The build SHALL provide an opt-in minimal profile that configures only the
application kernel, required platform module and bundled dependencies. It SHALL
exclude rendering, UI, VFX, scene modules, Qt, USD and shader/content tools.

#### Scenario: Minimal native configuration
- **WHEN** the minimal profile is configured on Windows with its recorded bundled sources
- **THEN** configuration succeeds without desktop vcpkg, Qt or USD and its target graph excludes the listed desktop features.

#### Scenario: Unsupported required module
- **WHEN** a module outside the supported minimal set is explicitly required
- **THEN** configuration fails and identifies the unsupported module rather than silently enabling the full desktop graph.

#### Scenario: Missing required bundled source
- **WHEN** a required bundled source is missing
- **THEN** configuration identifies the missing dependency and fails without installing a replacement or finding a host binary.

### Requirement: Shared application lifecycle
The minimal framework SHALL use the existing application/service/work-queue
startup, stepping and shutdown implementation. Removing rendering integration
SHALL NOT substitute a simulated application or a second lifecycle implementation.

#### Scenario: Create and initialize
- **WHEN** the native minimal application registers its required platform module and window service and starts
- **THEN** real core services and the platform-window API become available without initializing a renderer.

#### Scenario: Repeated steps and orderly stop
- **WHEN** the initialized native minimal application advances multiple steps and requests stop
- **THEN** registered update callbacks execute, service shutdown completes, background/platform threads terminate and the application reports completion.

### Requirement: Explicit entry point and static modules
The minimal sample SHALL select the agreed app_sample_main_min.cpp entry point
and statically register the required platform module without dynamic loading.

#### Scenario: Both sample entry-point files exist
- **WHEN** both existing sample sources are present during a minimal build
- **THEN** the sample links exactly one entry point and has the required static platform module available.

### Requirement: Native and desktop coexistence
The minimal framework SHALL support isolated native Windows validation builds.
The full desktop framework and existing preset behavior SHALL remain compatible.

#### Scenario: Native validation
- **WHEN** the focused native minimal lifecycle suite is built in Debug or Release
- **THEN** it links the shared minimal framework with native compiler options and passes bounded lifecycle checks.

#### Scenario: Existing desktop selection
- **WHEN** an existing desktop preset is configured without minimal selection
- **THEN** it retains its full-framework features, dependency/toolchain settings and a valid sample entry point.
