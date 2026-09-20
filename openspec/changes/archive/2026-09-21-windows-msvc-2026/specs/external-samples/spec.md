# Spec Delta

## MODIFIED Requirements

### Requirement: Preserved build and runtime interfaces

Engine presets SHALL remain supported except that `win_vs2022_x64*` presets SHALL be replaced by corresponding `win_vs2026_x64*` presets for the Windows MSVC baseline migration. Sample target names and configuration-specific binary/package layouts relative to their selected build directories SHALL remain supported. Native samples and native NauDemo SHALL resolve required sample assets, shader inputs and shared support code from the selected checkout. Browser minimal and demo packages SHALL preserve existing rendering, timing, lifecycle and relocation behavior without new desktop dependencies.

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

#### Scenario: Native presets migrate
- **WHEN** a developer switches from a retired VS 2022 preset to its documented VS 2026 replacement in a clean build directory
- **THEN** the same sample targets and configuration-relative output layouts remain available using VS 2026/v145
