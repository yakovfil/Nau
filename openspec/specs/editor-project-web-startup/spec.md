# editor-project-web-startup Specification

## Purpose

Build editor-created projects for a non-rendering browser runtime and prove that packaged project data becomes a live scene with supported components and checked application startup and shutdown.

## Requirements

### Requirement: Independent browser project builds

The project SHALL provide documented Debug and Release browser builds of the editor-created project using the recorded browser SDK. Project code SHALL be linked statically into the browser application. Browser builds SHALL have separate host-tool, target and delivery outputs under ignored project build directories and SHALL NOT link desktop SDK binaries, USD, Qt, rendering, physics, animation, audio or input-service implementations. Required missing tools or dependencies SHALL cause actionable build failure without implicit SDK installation.

#### Scenario: Both configurations build
- **WHEN** the documented prerequisites are provisioned and Debug and Release browser project builds run
- **THEN** each produces its own application and asset delivery, including the project's game module, without reusing desktop binary inputs

#### Scenario: Native-only module is requested
- **WHEN** a browser project declares a module outside the supported runtime profile
- **THEN** the build fails identifying the unsupported module rather than linking a host binary or silently omitting it

### Requirement: Native preparation of editor assets

The build SHALL use host-native asset tools to convert editor-authored startup scene data into the engine's compiled runtime representation and package its required configuration, asset mappings and data dependencies. Registered project component identities and serialized properties SHALL survive conversion. Changes to relevant source assets, metadata, project component definitions or package inputs SHALL invalidate their dependent outputs. Missing inputs or failed preparation SHALL prevent successful delivery even when old outputs exist. Asset preparation SHALL NOT modify authored project content.

#### Scenario: Authored scene or component data changes
- **WHEN** a startup-scene transform or serialized project-component property changes and the browser project is rebuilt
- **THEN** the delivery contains the updated value and the browser scene observes it after loading

#### Scenario: A required dependency disappears
- **WHEN** a required scene or referenced input is removed after a successful build
- **THEN** the next build fails with the identifying asset path or identity and does not report the old delivery as a successful new result

#### Scenario: Native cooking targets WebAssembly
- **WHEN** a native 64-bit tool cooks a component for the 32-bit browser runtime
- **THEN** the compiled record carries its type name and the browser resolves its local registered type without relying on the native numeric hash
- **AND** existing native scene records without type names remain readable on their original platform

### Requirement: Package-backed project resolution

The runtime SHALL mount the delivered archive and resolve project configuration, startup scene and required asset identities through engine asset and filesystem services. The delivery SHALL be complete for its declared non-rendering data profile, work under a nested serving URL outside the checkout, and require no source-tree or host SDK access. Configuration and scene data SHALL be parsed; required packaged reference targets SHALL be validated for presence and readability. Mesh and material references SHALL be retained as data without requesting GPU views or claiming rendering support.

#### Scenario: Delivery is relocated
- **WHEN** the complete delivery is served from a nested URL outside the checkout with required browser isolation headers
- **THEN** startup resolves its configuration, scene and required references from the delivered package with no host-path or loose-source fallback

#### Scenario: Required package content is invalid
- **WHEN** the archive is missing or corrupt, project configuration is malformed, an asset mapping is unresolved, or a required packaged entry is absent
- **THEN** startup fails with an identifying diagnostic and never reports Running

### Requirement: Actual scene and supported component activation

Successful startup SHALL deserialize and activate the configured scene as real engine scene objects, preserving hierarchy, object/component identities, local transforms and serialized properties. The supported set SHALL include scene transforms, camera data, static-mesh reference data and registered project components whose execution does not require excluded services. Project component registration SHALL precede deserialization. Unknown component types and components requiring excluded services SHALL fail with diagnostics identifying the scene object and component; silently removing them or substituting missing-component placeholders SHALL NOT satisfy startup.

#### Scenario: Supported scene activates
- **WHEN** a compiled scene containing nested objects, camera/static-mesh data and supported project components is loaded
- **THEN** the activated scene contains the expected objects and components with their authored transforms, identities and properties
- **AND** project component updates execute on that scene after successful startup

#### Scenario: Unsupported component is present
- **WHEN** a scene contains an unknown component or one declared to require physics, animation playback, audio, input handling or rendering services
- **THEN** preparation or startup fails identifying the component and object, and the browser does not reach Running with a degraded replacement scene

### Requirement: Checked startup and orderly lifecycle

The application SHALL use the engine's common host and browser lifecycle. Running and ordinary game updates SHALL require successful package mounting, configuration loading, component registration, scene deserialization and scene activation. Pending startup SHALL permit required asynchronous work and browser responsiveness. Startup errors SHALL propagate to terminal failure and eligible cleanup. Stop SHALL be asynchronous and idempotent, prevent further application updates once observed, and retain necessary owners until pending work and teardown settle.

#### Scenario: Scene activation is pending
- **WHEN** startup awaits scene loading or activation
- **THEN** the page remains responsive and the runtime does not report Running or dispatch ordinary application updates early

#### Scenario: Scene loading fails
- **WHEN** the configured required scene cannot be loaded or activated
- **THEN** the application reports failure rather than treating a logged error or an empty scene as successful startup

#### Scenario: Stop overlaps startup or execution
- **WHEN** Stop is requested repeatedly during pending startup or after component updates begin
- **THEN** no new application updates occur after Stop is observed, accepted work settles safely, and terminal status accurately reflects cleanup success or failure

### Requirement: Existing consumers remain supported

The change SHALL preserve the generated project's native Release build, existing rendered NauDemo native/browser behavior, and the minimal/common-host and portable-package contracts. Reusable build and runtime integration SHALL NOT hard-code NauDemo project paths. Rendering and excluded service execution SHALL NOT be introduced into this milestone's browser profile.

#### Scenario: Existing builds are exercised
- **WHEN** the new profile is added and existing native project and demo/minimal browser configurations are rebuilt and checked
- **THEN** their existing supported behavior remains available without selecting the new non-rendering profile

### Requirement: Browser acceptance demonstrates runtime state

Acceptance SHALL run the actual editor project's Debug and Release browser deliveries in a real browser, plus an authored fixture exercising its registered project components. Evidence SHALL verify loaded hierarchy, identities, transforms, properties, required asset resolution, component updates and terminal cleanup through the real runtime. It SHALL cover relocation, missing/corrupt assets, unknown and unsupported components, startup failure and Stop during startup. Build success, package-byte reads alone or page-side simulated objects SHALL NOT count as scene-startup acceptance. Commands, revisions, tool versions and untested limits SHALL be recorded.

#### Scenario: Milestone is declared complete
- **WHEN** implementation validation is reported
- **THEN** reproducible evidence covers successful and failing startup in both browser configurations, real component execution and cleanup, relocation and affected consumer regressions
- **AND** the result is explicitly described as non-rendering startup support rather than arbitrary editor-project web compatibility

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
