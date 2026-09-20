# Spec Delta

## Purpose

Maintain Nau samples in an independently versioned repository while preserving complete source ownership, reproducible checkout and existing native, SDK and browser usage.

## ADDED Requirements

### Requirement: Complete independent sample repository

Nau SHALL record NauSamples as a submodule at `NauSamples` using `https://github.com/yakovfil/NauSamples.git`. All tracked content previously owned by NauEngineLite under `samples/` SHALL be represented at the new repository root, with changes needed for integration explicitly accounted for. Original sample history and copyright/license notices and the existing NauSamples initial commit SHALL remain available. Generated untracked build outputs SHALL NOT become migration inputs.

#### Scenario: Extraction is audited
- **WHEN** the migration is reviewed against the recorded engine source revision
- **THEN** every previously tracked sample path has a destination or an explicit integration-change record, historical sample commits are traceable, and the destination initial commit remains an ancestor
- **AND** the engine no longer owns duplicate sample sources

#### Scenario: Recorded repositories are initialized
- **WHEN** a developer initializes the Nau checkout's recorded submodules from repositories containing the selected revisions
- **THEN** NauSamples appears at the documented path with the compatible sample sources and retained license notices

### Requirement: Explicit external sample selection

Engine builds SHALL support a configurable samples source directory, defaulting to the sibling NauSamples checkout. Configurations that require samples SHALL fail with actionable initialization/path guidance when that source is missing or invalid. Configurations with no sample dependency SHALL remain configurable without NauSamples. Configuration SHALL NOT fetch or initialize repositories implicitly or fall back to stale engine-local sources.

#### Scenario: Default or custom checkout is used
- **WHEN** required samples exist at the default sibling location or an explicitly configured different location
- **THEN** sample targets use that location, including when the path contains spaces

#### Scenario: Required checkout is unavailable
- **WHEN** a sample-dependent build selects a missing or invalid samples directory
- **THEN** configuration fails before compilation and identifies the selected directory and recovery action

#### Scenario: Engine-only configuration is selected
- **WHEN** samples are disabled and no selected application needs them
- **THEN** the engine configuration does not require a samples checkout

### Requirement: Preserved build and runtime interfaces

Existing engine presets, sample target names and configuration-specific binary/package locations SHALL remain supported after extraction. Native samples and native NauDemo SHALL resolve required sample assets, shader inputs and shared support code from the selected checkout. Browser minimal and demo packages SHALL preserve existing rendering, timing, lifecycle and relocation behavior without new desktop dependencies.

#### Scenario: Native consumers run
- **WHEN** native samples and NauDemo are built and launched through documented commands using the extracted checkout
- **THEN** their required assets resolve and existing behavior is retained without recreating the old engine-local samples tree

#### Scenario: Browser consumers are exercised
- **WHEN** minimal and demo Debug/Release packages are built and served after extraction
- **THEN** existing acceptance checks pass, including startup, Stop, failure reporting and package relocation

#### Scenario: Over-aligned native sample allocations
- **WHEN** inputDemo creates an additional swapchain using an over-aligned EASTL container node
- **THEN** the engine allocator honors the requested alignment without an allocator assertion
- **AND** allocation, reallocation and deallocation remain compatible on native and browser platforms

### Requirement: Installed sample distribution remains usable

The native SDK installation SHALL continue to distribute samples under its `samples/` directory with their required support files. Installed-sample build and resource discovery SHALL resolve the installed layout without requiring the original engine or NauSamples source directories.

#### Scenario: Installed SDK is relocated
- **WHEN** the SDK and its installed samples are copied outside the source checkout and built using the documented installed-SDK workflow
- **THEN** sample discovery and representative sample compilation/resource lookup succeed using installed paths

### Requirement: Migration evidence identifies all repository inputs

Migration validation SHALL record engine, samples, demo and parent source identities, extraction provenance, commands and results. It SHALL include tracked-file accounting, default/custom/missing source checks, native and browser regressions and a fresh checkout with no copied generated build inputs. Historical archived evidence SHALL remain historical; current guides SHALL document the new paths and prerequisites.

#### Scenario: Migration is declared complete
- **WHEN** completion is recorded
- **THEN** the evidence identifies the tested repository combination and covers every migration scenario, including independent checkout reproduction
- **AND** unavailable or failed checks remain explicitly incomplete rather than being counted as successful relocation
