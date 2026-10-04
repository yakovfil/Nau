# external-samples Specification

## Purpose

Maintain Nau samples in an independently versioned repository while preserving complete source ownership, reproducible checkout and existing native, SDK and browser usage.

## Requirements

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

Engine builds SHALL configure without a samples checkout by default. NauSamples SHALL own the hook that registers its configurable source directory with the engine, defaulting to the directory containing that hook. Configurations that select samples SHALL fail with actionable path guidance when the source is missing or invalid. Configuration SHALL NOT fetch or initialize repositories implicitly or fall back to stale engine-local sources.

#### Scenario: Default or custom checkout is used
- **WHEN** the NauSamples hook selects its own checkout or an explicitly configured different location
- **THEN** sample targets use that location, including when the path contains spaces

#### Scenario: Required checkout is unavailable
- **WHEN** a sample-dependent build selects a missing or invalid samples directory
- **THEN** configuration fails before compilation and identifies the selected directory and recovery action

#### Scenario: Engine-only configuration is selected
- **WHEN** no external project hook is selected
- **THEN** the engine configuration does not require a samples checkout

### Requirement: Preserved build and runtime interfaces

Engine presets SHALL configure the engine without external projects. The `win_vs2022_x64*` presets SHALL be replaced by corresponding `win_vs2026_x64*` presets for the Windows MSVC baseline migration. Project-owned hooks and build scripts SHALL preserve remaining sample target names after deliberate retirement of UiSampleApp and configuration-specific binary/package layouts relative to their selected build directories. Native samples and native NauDemo SHALL resolve required sample assets, shader inputs and shared support code from the selected checkout. Browser minimal and demo packages SHALL preserve existing rendering, timing, lifecycle and relocation behavior without new desktop dependencies.

#### Scenario: Native consumers run
- **WHEN** native samples and NauDemo are built and launched through documented commands using the extracted checkout
- **THEN** their required assets resolve and existing non-UI behavior is retained without recreating the old engine-local samples tree

#### Scenario: Browser consumers are exercised
- **WHEN** minimal and demo Debug/Release packages are built and served after extraction
- **THEN** existing acceptance checks pass, including startup, Stop, failure reporting and package relocation

#### Scenario: Over-aligned native sample allocations
- **WHEN** inputDemo creates an additional swapchain using an over-aligned EASTL container node
- **THEN** the engine allocator honors the requested alignment without an allocator assertion
- **AND** allocation, reallocation and deallocation remain compatible on native and browser platforms

#### Scenario: Native presets migrate
- **WHEN** a developer switches from a retired VS 2022 preset to its documented VS 2026 replacement in a clean build directory
- **THEN** the same non-retired sample targets and configuration-relative output layouts remain available using VS 2026/v145 when the sample hook is selected

#### Scenario: UI sample is retired
- **WHEN** source samples or installed samples are configured after UI retirement
- **THEN** UiSampleApp and its exclusive resources are absent, and current documentation identifies its removal
- **AND** the remaining sample discovery and configuration-relative layouts continue to work

### Requirement: Installed sample distribution remains usable

The native SDK installation SHALL distribute samples under its `samples/` directory when the sample project is attached during installation. An engine-only SDK installation SHALL remain usable without that directory. Installed-sample build and resource discovery SHALL resolve the installed layout without requiring the original engine or NauSamples source directories.

#### Scenario: Installed SDK is relocated
- **WHEN** the SDK and its installed samples are copied outside the source checkout and built using the documented installed-SDK workflow
- **THEN** sample discovery and representative sample compilation/resource lookup succeed using installed paths

### Requirement: Migration evidence identifies all repository inputs

Migration validation SHALL record engine, samples, demo and parent source identities, extraction provenance, commands and results. It SHALL include tracked-file accounting, default/custom/missing source checks, native and browser regressions and a fresh checkout with no copied generated build inputs. Historical archived evidence SHALL remain historical; current guides SHALL document the new paths and prerequisites.

#### Scenario: Migration is declared complete
- **WHEN** completion is recorded
- **THEN** the evidence identifies the tested repository combination and covers every migration scenario, including independent checkout reproduction
- **AND** unavailable or failed checks remain explicitly incomplete rather than being counted as successful relocation
