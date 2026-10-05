## Purpose

Deliver NauDemo assets through engine archives in native and browser builds while preserving appearance and allowing execution away from source checkout directories.

## ADDED Requirements

### Requirement: Build-generated demo archives

Debug and Release native and browser builds SHALL generate `NauDemo.nau_pack` from explicit platform-specific inputs. Relevant source or manifest changes SHALL rebuild the archive and dependent delivery artifacts. Generated packaging tools, caches, archives and validation artifacts SHALL reside under NauDemo/build, with separate host and target build directories. Existing native binary deployment locations remain supported.

#### Scenario: Packaged input changes
- **WHEN** a font, mesh, material, shader or manifest entry changes
- **THEN** rebuilding updates the appropriate archive and deploys or preloads those updated bytes

### Requirement: Demo assets resolve through engine packages

Both demo variants SHALL mount their archive through the engine's portable package filesystem and load mesh and font assets through the existing asset services. Platform-specific material, shader, environment and configuration assets SHALL be supplied by the delivery. Required asset reads SHALL NOT fall back to loose source-tree files. Native and web archive contents can differ for their renderers.

#### Scenario: Native delivery is relocated
- **WHEN** the native executable, runtime dependencies and packaged content are copied outside the checkout and started from an unrelated working directory without access to source assets
- **THEN** the existing cube, environment lighting and Nau Demo text render, rotation and resize work, and ordinary close completes

#### Scenario: Web delivery is relocated
- **WHEN** the web delivery is served from a nested URL outside the checkout
- **THEN** the engine reads its archive and displays the rotating cube and font text without requests to source paths or loose asset substitutes

### Requirement: Package failures participate in startup

A missing or invalid package or required entry SHALL fail demo startup with a diagnostic identifying the archive or entry. The browser SHALL NOT report Running for these failures, and both platforms SHALL complete applicable cleanup and report unsuccessful termination. No partial mount SHALL be treated as successful initialization.

#### Scenario: Archive or required entry is invalid
- **WHEN** the demo is started with a missing archive, truncated archive or archive missing its required font or mesh buffer
- **THEN** it reports the relevant failure and does not display substitute content or continue as a successful demo

### Requirement: Existing demo behavior is preserved

Package integration SHALL preserve shared scene construction, pre-update rotation and text submission, post-update browser presentation, fullscreen canvas, native appearance, resizing and orderly shutdown. It SHALL NOT add demo-specific test hooks or external HTML controls.

#### Scenario: Both configurations run
- **WHEN** Debug and Release native and browser deliveries are exercised
- **THEN** rendered-output, rotation, resize and lifecycle acceptance checks pass using packaged assets
