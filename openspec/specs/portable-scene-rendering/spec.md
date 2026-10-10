# portable-scene-rendering Specification

## Purpose

Present supported packaged engine scenes on Windows and web through a common rendering profile, with portable content, real scene-driven output and checked graphics lifetime.

## Requirements

### Requirement: Explicit portable rendering profile

The packaged project workflow SHALL offer an opt-in `basic-rendering-scene` profile for Windows and web in Debug and Release using the same application entry and project component sources. One project declaration SHALL define the profile, logical modules, supported components, startup configuration and rendering content policy for both targets. The rendering profile SHALL permit explicitly declared optional CoreInput and Audio modules on both targets. Audio selection SHALL enable portable one-shot playback without requiring legacy spatial audio components or enabling the full desktop graph. The existing non-rendering profile, minimal applications, native full-rendered project and native/browser NauDemo SHALL retain their supported behavior. Applications omitting Audio SHALL acquire no audio backend dependency. Browser runtime targets SHALL NOT link desktop rendering binaries, USD or Qt. Unsupported declarations SHALL fail with identifying diagnostics.

#### Scenario: Rendering and non-rendering builds coexist

- **WHEN** the project builds both profiles for Windows and web
- **THEN** rendering deliveries display supported scene content, non-rendering deliveries retain their rendering-free graph, and their target and delivery outputs remain isolated

#### Scenario: Supported input module is requested

- **WHEN** a rendering declaration includes CoreInput on Windows or web
- **THEN** its packaged application starts with the input service available and uses the same authored archive as a rendering delivery without CoreInput

#### Scenario: Supported audio module is requested

- **WHEN** a rendering declaration includes Audio on Windows or web
- **THEN** its packaged application exposes portable one-shot audio with checked lifetime and browser activation where required

#### Scenario: Audio is omitted

- **WHEN** a rendering, minimal or non-rendering application does not select Audio
- **THEN** it retains its supported behavior without acquiring audio services or backend dependencies

#### Scenario: Unsupported module is requested

- **WHEN** the rendering declaration requests a module outside its supported set
- **THEN** both target builds reject it without silently omitting the module or enabling the full desktop graph

### Requirement: Portable renderable content

One host preparation SHALL produce a validated archive consumed byte-identically by Windows and web rendering deliveries. Supported content SHALL include indexed static triangle geometry with positions and normals, explicit opaque base-color materials with ambient plus directional diffuse lighting, and PNG-sourced unlit billboard textures with alpha cutout. Preparation SHALL preserve scene hierarchy, component identities, geometry and texture references and authored transforms. Material selection SHALL be explicit and common to both targets. Unsupported geometry or required material/texture features, missing references and corrupt data SHALL fail preparation or checked startup with the relevant identity or path; silent replacement geometry, fallback materials or placeholder textures SHALL NOT count as success. Preparation SHALL NOT modify authored sources or publish stale outputs after failure.

#### Scenario: One archive renders on both targets
- **WHEN** an archive containing supported geometry, explicit simple materials and billboard textures is selected for both targets
- **THEN** both resolve the same scene, geometry, material and texture identities from that archive without target-specific recooking

#### Scenario: Content exceeds the supported subset
- **WHEN** required content uses unsupported topology, skinning, material or texture features or malformed geometry ranges
- **THEN** preparation or startup reports the offending input and does not enter Running with substituted content

#### Scenario: Material or geometry input changes
- **WHEN** an authored input or its explicit material mapping changes before a normal build
- **THEN** preparation incorporates the change or fails, without altering authored files or presenting a stale delivery as current

#### Scenario: Referenced texture changes or disappears
- **WHEN** a referenced billboard PNG changes, becomes corrupt or is removed before a normal build
- **THEN** preparation incorporates the new pixels or fails with the texture identity/path, without publishing stale content as current

#### Scenario: Unchanged rendering content is prepared again
- **WHEN** the same authored rendering inputs and preparation options are processed repeatedly
- **THEN** the prepared archives are byte-identical, authored UIDs remain unchanged, generated scene identities are stable, and hierarchy and references continue to resolve to the same targets

### Requirement: Scene-driven frame presentation

Rendering SHALL select the active world's main camera through existing engine camera-selection semantics and present all visible supported static-mesh and billboard components in that world. Geometry, component world transforms, texture references, camera properties and visibility SHALL come from the live engine scene. Multiple objects SHALL share one frame with depth-tested occlusion and mesh lighting that responds to transformed normals, including non-uniform positive scale. Supported component activation, removal, visibility, texture and transform changes SHALL be reflected in subsequent frames after required resources are ready, without dangling scene references. A removed component SHALL NOT be resurrected by completion of an earlier load. No camera, invalid camera parameters, non-finite billboard position or singular mesh render transforms SHALL produce an identifying failure rather than successful blank output. An empty visible renderable set with a valid camera SHALL render a cleared frame; a billboard-only scene SHALL render its billboards.

#### Scenario: Several components contribute to a frame
- **WHEN** a scene contains overlapping visible meshes, nested transforms and a static-mesh component with a local offset
- **THEN** all visible meshes appear at their component world transforms, nearer surfaces occlude farther surfaces, and shared geometry can be used by multiple objects

#### Scenario: Scene state changes
- **WHEN** project components move a mesh or billboard, change visibility, activate or remove a supported object, or change the selected camera
- **THEN** subsequent frames reflect the new live state and do not draw removed objects

#### Scenario: Camera or transform is invalid
- **WHEN** the active world lacks a camera or a required camera/transform cannot produce a valid view
- **THEN** the application reports the cause and fails through checked cleanup instead of reporting a healthy blank renderer

#### Scenario: Texture replacement completes after component removal
- **WHEN** a billboard texture load is pending and its component is removed
- **THEN** completion does not submit that component or access its destroyed scene state

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

### Requirement: Constant screen-relative billboards

The rendering profile SHALL support existing serialized billboard components with texture, visibility and screenPercentageSize fields. A billboard SHALL be centered at its component world position and face the camera as a screen-aligned square. Its full pixel width and height SHALL equal screenPercentageSize multiplied by drawable width, independent of camera distance and field of view. Component or parent rotation and scale SHALL NOT rotate or resize the quad, although parent transforms SHALL still affect the component world position. Screen-relative size SHALL be finite and positive; invalid size SHALL fail with a component diagnostic. Unspecified size SHALL have a deterministic positive default. Centers behind the camera or outside its near/far depth interval SHALL not render; quads crossing viewport edges SHALL be clipped. Resizing and browser device-pixel-ratio changes SHALL preserve these rules, including existing zero-drawable suspension and recovery.

#### Scenario: Camera distance changes
- **WHEN** the camera moves toward or away from a visible billboard without changing drawable dimensions or billboard size
- **THEN** its screen width and height stay constant while its position and occlusion follow scene projection

#### Scenario: Viewport aspect ratio changes
- **WHEN** the drawable changes aspect ratio or device pixel ratio
- **THEN** the billboard remains square and its full width remains the configured fraction of drawable width

#### Scenario: Parent transforms change
- **WHEN** a parent is translated, rotated or scaled
- **THEN** the billboard follows its resulting component world position without acquiring quad rotation or world-relative sizing

#### Scenario: Billboard crosses the camera plane
- **WHEN** a billboard center passes behind the camera or outside near/far depth bounds
- **THEN** it disappears without inverted geometry, invalid projection or a full-screen artifact

### Requirement: Portable billboard texture appearance

Billboard textures SHALL use unlit sRGB color and linear alpha with equivalent orientation, sampling and output conversion on Windows and web. Sampling SHALL use linear filtering and clamp-to-edge. Sampled alpha below 0.01 SHALL discard the fragment; retained fragments SHALL write opaque color and depth without alpha blending. Transparent cutouts SHALL leave existing scene color and depth unchanged. Billboard fragments SHALL participate in mesh and billboard depth occlusion. The first supported source subset SHALL be single-image 8-bit RGB/RGBA PNG, mapped over the entire square. Soft transparency, lighting and automatic source-aspect sizing SHALL NOT be implied.

#### Scenario: Transparent marker overlaps scene geometry
- **WHEN** a billboard overlaps a mesh with both transparent and retained texels
- **THEN** cutout texels reveal the existing scene, retained texels show unlit texture color, and nearer scene surfaces occlude farther fragments

#### Scenario: Asymmetric texture is used on both targets
- **WHEN** the same texture has distinct corners and colors
- **THEN** both targets display the same orientation and equivalent colors within documented tolerances

### Requirement: Checked portable texture resources

Portable billboard texture preparation and runtime loading SHALL preserve authored asset identities and validate dimensions, payload lengths and supported format before allocation/upload. Malformed, oversized, missing or unresolved required textures SHALL report identifying errors and follow checked cleanup. Shared texture use SHALL reuse resources within a backend. Initial required texture preparation SHALL complete before successful initial presentation and Running. Texture changes SHALL display the requested asset once ready; failed replacements SHALL remain observable failures rather than silently retaining a substitute. Once Stop is observed, outstanding preparation SHALL settle or safely cancel without subsequent frame submission, and texture resources SHALL be released before graphics context/driver destruction.

#### Scenario: Texture payload is invalid
- **WHEN** a prepared texture is truncated, oversized, missing or has inconsistent dimensions and byte length
- **THEN** startup fails with its identity/path in Debug and Release, without unchecked allocation or successful placeholder rendering

#### Scenario: Several billboards share one texture
- **WHEN** several active billboards reference the same texture
- **THEN** they render with independent positions and sizes using shared texture resources, and removing one leaves the others valid

#### Scenario: Stop overlaps texture preparation
- **WHEN** Stop is requested repeatedly while a texture load or upload is pending
- **THEN** no later frame is submitted, accepted work settles safely, and cleanup releases all texture owners before graphics shutdown

### Requirement: NauDemo portable billboard acceptance

NauDemo SHALL contain an authored billboard and PNG texture rendered through its existing root Windows/Web launchers and shared rendering declaration, without platform-specific demo draw code or HTML overlays. Acceptance SHALL cover Windows and a real browser in Debug and Release using the same prepared archive. Evidence SHALL verify visible textured output, distance-independent size, facing, alpha cutout, depth occlusion, component and texture identity, live changes/removal, resource sharing, resize/zero-size recovery, checked texture failures and cleanup. Native validation SHALL include relocation and browser validation a nested URL. Existing mesh appearance, animation and startup/Stop regressions SHALL remain covered.

#### Scenario: Both launchers run the updated demo
- **WHEN** users run run_windows.bat or run_web.bat with the supported toolchains
- **THEN** the existing scene and its billboard appear through the shared engine renderer from packaged assets

#### Scenario: Acceptance is reported complete
- **WHEN** billboard implementation is declared validated
- **THEN** recorded commands, configurations, revisions, archive identity and visual/behavioral evidence cover all four configurations, with any unexecuted checks explicitly identified

### Requirement: NauDemo portable free camera

NauDemo's packaged rendering delivery SHALL let the user control the authored scene camera on Windows and web through the same game code. W/S SHALL move forward/backward along the camera's horizontal facing, A/D SHALL strafe, and Q/E SHALL move vertically. Holding the primary pointer button and dragging SHALL change camera yaw and pitch, with pitch bounded to avoid inversion. Translation SHALL scale with elapsed game time and remain bounded after browser suspension. Releasing the button or losing focus SHALL stop rotation and movement. With no input, the authored initial camera view and existing scene animation SHALL remain unchanged. Camera control SHALL not require a page overlay or platform-specific demo draw path.

#### Scenario: Keyboard movement changes the view

- **WHEN** the running demo receives a held W, A, S, D, Q or E input for eligible updates
- **THEN** the live authored camera moves in the specified direction and subsequent rendered frames reflect its changed position

#### Scenario: Drag changes facing

- **WHEN** the user drags with the primary pointer button held
- **THEN** yaw and pitch change the live camera view, while release or focus loss stops further rotation

#### Scenario: No input preserves the scene

- **WHEN** the demo runs without camera input
- **THEN** its authored initial view, scene objects and animation remain visible as before

#### Scenario: Camera behavior is accepted on both platforms

- **WHEN** Windows and real-browser Debug and Release packages are validated
- **THEN** each demonstrates keyboard movement, drag rotation, focus-loss release, resize continuity and orderly Stop with the same prepared scene archive
