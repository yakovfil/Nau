# Spec Delta

## MODIFIED Requirements

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
