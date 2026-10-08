# portable-scene-rendering Specification

## Purpose

Present supported packaged engine scenes on Windows and web through a common rendering profile, with portable content, real scene-driven output and checked graphics lifetime.

## Requirements

### Requirement: Explicit portable rendering profile

The packaged project workflow SHALL offer an opt-in `basic-rendering-scene` profile for Windows and web in Debug and Release using the same application entry and project component sources. One project declaration SHALL define the profile, logical modules, supported components, startup configuration and rendering content policy for both targets. The existing non-rendering profile, minimal applications, native full-rendered project and native/browser NauDemo SHALL retain their supported behavior. Browser runtime targets SHALL NOT link desktop rendering binaries, USD or Qt. Unsupported declarations SHALL fail with identifying diagnostics.

#### Scenario: Rendering and non-rendering builds coexist
- **WHEN** the project builds both profiles for Windows and web
- **THEN** rendering deliveries display supported scene content, non-rendering deliveries retain their rendering-free graph, and their target and delivery outputs remain isolated

#### Scenario: Unsupported module is requested
- **WHEN** the rendering declaration requests a module outside its supported set
- **THEN** both target builds reject it without silently omitting the module or enabling the full desktop graph

### Requirement: Portable renderable content

One host preparation SHALL produce a validated archive consumed byte-identically by Windows and web rendering deliveries. Supported content SHALL include indexed static triangle geometry with positions and normals, and explicit opaque base-color materials with ambient plus directional diffuse lighting. Preparation SHALL preserve scene hierarchy, component identities, geometry references and authored transforms. Material selection SHALL be explicit and common to both targets. Unsupported geometry or required material features, missing references and corrupt data SHALL fail preparation or checked startup with the relevant identity or path; silent replacement geometry or fallback materials SHALL NOT count as success. Preparation SHALL NOT modify authored sources or publish stale outputs after failure.

#### Scenario: One archive renders on both targets
- **WHEN** an archive containing supported geometry and explicit simple materials is selected for both targets
- **THEN** both resolve the same scene, geometry and material identities from that archive without target-specific recooking

#### Scenario: Content exceeds the supported subset
- **WHEN** required content uses unsupported topology, skinning, material features or malformed geometry ranges
- **THEN** preparation or startup reports the offending input and does not enter Running with substituted content

#### Scenario: Material or geometry input changes
- **WHEN** an authored input or its explicit material mapping changes before a normal build
- **THEN** preparation incorporates the change or fails, without altering authored files or presenting a stale delivery as current

### Requirement: Scene-driven frame presentation

Rendering SHALL select the active world's main camera through existing engine camera-selection semantics and present all visible supported static-mesh components in that world. Geometry, component world transforms, camera properties and visibility SHALL come from the live engine scene. Multiple objects SHALL share one frame with depth-tested occlusion and lighting that responds to transformed normals, including non-uniform positive scale. Supported component activation, removal, visibility and transform changes SHALL be reflected in subsequent frames without dangling scene references. No camera, invalid camera parameters or singular render transforms SHALL produce an identifying failure rather than successful blank output. An empty visible mesh set with a valid camera SHALL render a cleared frame.

#### Scenario: Several components contribute to a frame
- **WHEN** a scene contains overlapping visible meshes, nested transforms and a static-mesh component with a local offset
- **THEN** all visible meshes appear at their component world transforms, nearer surfaces occlude farther surfaces, and shared geometry can be used by multiple objects

#### Scenario: Scene state changes
- **WHEN** project components move a mesh, change visibility, activate or remove a supported object, or change the selected camera
- **THEN** subsequent frames reflect the new live state and do not draw removed objects

#### Scenario: Camera or transform is invalid
- **WHEN** the active world lacks a camera or a required camera/transform cannot produce a valid view
- **THEN** the application reports the cause and fails through checked cleanup instead of reporting a healthy blank renderer

### Requirement: Consistent viewport and supported appearance

Both backends SHALL implement the same simple material and lighting semantics and equivalent camera framing, despite backend-specific projection conventions. Rendering SHALL use actual drawable dimensions, preserve depth behavior and update viewport and projection together after resize. Browser sizing SHALL account for client size and device pixel ratio. A zero-sized drawable SHALL suspend draw submission without division by zero and resume when drawable size becomes positive. Exact pixel identity between graphics backends SHALL NOT be required.

#### Scenario: A drawable is resized or temporarily hidden
- **WHEN** the drawable changes aspect ratio or becomes zero-sized and later returns
- **THEN** rendering resumes with correct framing and occlusion without stretching, invalid projection values or resource leaks

### Requirement: Checked graphics startup and shutdown

Running and ordinary application updates SHALL require successful package loading, scene activation, graphics initialization, required resource preparation and initial frame submission. Pending startup SHALL allow required asynchronous progress without ordinary updates. Once Stop is observed, no new scene frame SHALL be submitted; accepted work SHALL settle safely before resources, driver/context and window owners are released. Repeated Stop SHALL be harmless. Graphics initialization, resource upload, submission and device/context-loss failures SHALL remain observable and attempt eligible cleanup; cleanup failure SHALL NOT be reported as successful Stop. Lost graphics state SHALL require application restart or page reload in this profile.

#### Scenario: Stop overlaps resource preparation
- **WHEN** Stop is requested repeatedly while a required asset load or upload is pending
- **THEN** no later frame starts, accepted work settles or safely cancels, and owners remain alive through cleanup

#### Scenario: Graphics fails
- **WHEN** graphics initialization, upload or submission fails, or the device/context is lost
- **THEN** native execution returns nonzero after eligible cleanup or the browser reports terminal failure, with the cause retained and no automatic recreation

### Requirement: Reproducible rendering acceptance

Acceptance SHALL exercise an editor-authored supported scene through the production packaged application on Windows and a real browser in Debug and Release using the same prepared archive. Evidence SHALL combine visible output with an independent scene/resource observer proving actual asset identities, component transforms and updates. It SHALL cover multiple distinct meshes and repeated geometry, camera selection, component offsets, non-uniform scale, visibility/removal, depth occlusion, resize, zero-size recovery, relocation, invalid content, graphics failure and Stop during pending preparation. Visual comparison SHALL use documented geometric/color tolerances rather than timing-dependent pixel identity. Commands, tool versions, revisions and untested limits SHALL be recorded.

#### Scenario: Acceptance is reported complete
- **WHEN** implementation is declared validated
- **THEN** all four configurations have evidence for visible rendering and checked failures, with native deliveries launched outside the checkout and web deliveries served under a nested URL
- **AND** affected non-rendering, full desktop, NauDemo and common-host regressions pass or any unexecuted validation is explicitly identified
