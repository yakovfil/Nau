# Spec Delta

## ADDED Requirements

### Requirement: Shared portable project application

The project SHALL provide Windows and web Debug and Release builds of its packaged non-rendering scene application using the same entry source, project component sources and startup implementation. Platform selection SHALL be independent of the portable scene feature profile. Both targets SHALL apply the same scene, reference and supported-component checks before normal updates. Windows portable execution SHALL NOT require rendered desktop services or browser tooling.

#### Scenario: All portable configurations execute
- **WHEN** the project is built for Windows and web in Debug and Release
- **THEN** all four deliveries execute the shared application and activate the same supported scene data without rendering, physics, audio, animation playback or input-service implementations

#### Scenario: Native compilation has no browser SDK
- **WHEN** native build and cooking prerequisites are available but Emscripten is absent
- **THEN** the Windows portable build succeeds without activating or discovering browser tools

### Requirement: Single portable project declaration

The portable project SHALL declare its runtime profile, modules, startup configuration and supported component identities once. Target builds, asset preparation and runtime validation SHALL consume that declaration without separately maintained platform-specific lists. Unsupported modules or malformed declarations SHALL cause actionable failure. Reusable integration SHALL accept explicit project and engine locations without depending on the NauDemo name or checkout layout.

#### Scenario: Supported component declaration changes
- **WHEN** a registered project component is added to or removed from the declaration
- **THEN** cooking and both runtime targets use the changed policy after rebuilding without editing a second platform list

#### Scenario: Excluded module is declared
- **WHEN** the portable scene profile requests an excluded module
- **THEN** both platform builds reject it with an identifying diagnostic rather than silently dropping it

### Requirement: Shared prepared content across platforms

One successful native preparation SHALL produce an archive that both portable targets can consume without target-specific recooking or rewriting its contents. Required configuration and reference identities SHALL remain portable. Normal builds SHALL prepare current inputs or verify their freshness; preparation failure SHALL prevent publishing or launching a stale delivery as a new success. Explicit delivery of an already prepared archive SHALL be supported separately from preparation and SHALL NOT require cooking tools.

#### Scenario: One archive is delivered twice
- **WHEN** a prepared archive is selected for Windows and web delivery
- **THEN** the native archive and the archive embedded in browser preload data are byte-identical to that input and both runtimes load its scene

#### Scenario: Inputs change or preparation fails
- **WHEN** authored content, metadata, project component definitions or the declaration changes, or native preparation fails
- **THEN** the normal build uses newly prepared or verified current content, or fails without launching an old package

### Requirement: Consistent isolated build and delivery workflow

The project SHALL expose a documented common build interface selecting Windows or web and Debug or Release. Generated host-tool, prepared-content, target and delivery outputs SHALL stay under ignored project build directories with separate target/configuration caches. Each delivery SHALL run after relocation without accessing the checkout or host SDK. Existing web entry commands SHALL remain supported, and missing or incompatible prerequisites SHALL produce actionable failure without implicit SDK installation.

#### Scenario: Platforms are built consecutively
- **WHEN** Windows and web configurations are built through the common interface
- **THEN** each uses the appropriate compiler and dependencies without overwriting or consuming the other platform's target outputs

#### Scenario: Deliveries are relocated
- **WHEN** the native delivery is launched outside the checkout from an unrelated working directory and the web delivery is served under a nested URL with isolation headers
- **THEN** both resolve their delivered archive and configuration without source paths, development asset caches or installed SDK access

### Requirement: Rendered Windows route remains available

The existing rendered Windows SDK build SHALL remain independently selectable with its current scene, graphics, input and physics startup behavior. Selecting the portable profile SHALL NOT change the rendered route's dependency graph, generated outputs or asset configuration. Existing browser non-rendering contracts SHALL remain supported.

#### Scenario: Rendered and portable Windows builds coexist
- **WHEN** the existing rendered Release build and a portable Windows build are configured and run
- **THEN** each retains its intended runtime features and content-loading behavior without requiring changes to authored project content

### Requirement: Cross-platform packaged project acceptance

Acceptance SHALL exercise the production project and an independent scene observer on Windows and real-browser web in Debug and Release. It SHALL compare authored hierarchy, identities, transforms, properties and component execution using the same archive, and verify missing/corrupt content, unsupported components, activation failure, Stop during pending startup, logging and cleanup. Native failures SHALL return nonzero after eligible cleanup; browser failures SHALL retain terminal diagnostics. Timing-dependent transforms SHALL be compared under controlled elapsed time or against behavior invariants rather than assumed equal frame timing.

#### Scenario: Successful execution is compared
- **WHEN** the main scene and component fixture run on both targets
- **THEN** evidence verifies matching initial scene data, real component updates, visible lifecycle diagnostics and completed orderly cleanup

#### Scenario: Failure and Stop are compared
- **WHEN** invalid package inputs, unsupported components, activation failures or repeated Stop during pending startup are exercised
- **THEN** both targets preserve the common startup gate and owner lifetimes, report the outcome accurately and finish eligible cleanup without later application updates
