# Spec Delta

## Purpose

Build editor-created projects for a non-rendering browser runtime and prove that packaged project data becomes a live scene with supported components and checked application startup and shutdown.

## ADDED Requirements

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
