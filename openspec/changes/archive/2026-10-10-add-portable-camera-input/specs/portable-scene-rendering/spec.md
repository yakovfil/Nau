# Spec Delta

## MODIFIED Requirements

### Requirement: Explicit portable rendering profile

The packaged project workflow SHALL offer an opt-in `basic-rendering-scene` profile for Windows and web in Debug and Release using the same application entry and project component sources. One project declaration SHALL define the profile, logical modules, supported components, startup configuration and rendering content policy for both targets. The rendering profile SHALL permit an explicitly declared optional CoreInput module on both targets. The existing non-rendering profile, minimal applications, native full-rendered project and native/browser NauDemo SHALL retain their supported behavior. Browser runtime targets SHALL NOT link desktop rendering binaries, USD or Qt. Unsupported declarations SHALL fail with identifying diagnostics.

#### Scenario: Rendering and non-rendering builds coexist

- **WHEN** the project builds both profiles for Windows and web
- **THEN** rendering deliveries display supported scene content, non-rendering deliveries retain their rendering-free graph, and their target and delivery outputs remain isolated

#### Scenario: Supported input module is requested

- **WHEN** a rendering declaration includes CoreInput on Windows or web
- **THEN** its packaged application starts with the input service available and uses the same authored archive as a rendering delivery without CoreInput

#### Scenario: Unsupported module is requested

- **WHEN** the rendering declaration requests a module outside its supported set
- **THEN** both target builds reject it without silently omitting the module or enabling the full desktop graph

## ADDED Requirements

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
