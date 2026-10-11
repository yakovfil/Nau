# Spec Delta

## MODIFIED Requirements

### Requirement: NauDemo portable billboard acceptance

NauDemo's explicitly selectable original demonstration scene SHALL contain an authored billboard and PNG texture rendered through its existing root Windows/Web launchers and shared rendering declaration, without platform-specific demo draw code or HTML overlays. Acceptance SHALL cover Windows and a real browser in Debug and Release using the same prepared archive. Evidence SHALL verify visible textured output, distance-independent size, facing, alpha cutout, depth occlusion, component and texture identity, live changes/removal, resource sharing, resize/zero-size recovery, checked texture failures and cleanup. Native validation SHALL include relocation and browser validation a nested URL. Existing mesh appearance, animation and startup/Stop regressions SHALL remain covered.

#### Scenario: Both launchers run the updated demo
- **WHEN** users run run_windows.bat or run_web.bat with the documented original-demo selection and supported toolchains
- **THEN** the existing scene and its billboard appear through the shared engine renderer from packaged assets

#### Scenario: Acceptance is reported complete
- **WHEN** billboard implementation is declared validated
- **THEN** recorded commands, configurations, revisions, archive identity and visual/behavioral evidence cover all four configurations, with any unexecuted checks explicitly identified

### Requirement: NauDemo portable free camera

NauDemo's explicitly selected original demonstration scene in its packaged rendering delivery SHALL let the user control the authored scene camera on Windows and web through the same game code. W/S SHALL move forward/backward along the camera's horizontal facing, A/D SHALL strafe, and Q/E SHALL move vertically. Holding the primary pointer button and dragging SHALL change camera yaw and pitch, with pitch bounded to avoid inversion. Translation SHALL scale with elapsed game time and remain bounded after browser suspension. Releasing the button or losing focus SHALL stop rotation and movement. With no input, the authored initial camera view and existing scene animation SHALL remain unchanged. Camera control SHALL not require a page overlay or platform-specific demo draw path.

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
- **THEN** each, with the original demonstration selected, demonstrates keyboard movement, drag rotation, focus-loss release, resize continuity and orderly Stop with the same prepared scene archive

## ADDED Requirements

### Requirement: Portable scene-owned vector presentation

The rendering profile SHALL support bounded unlit colored line segments in world coordinates and screen-relative overlay coordinates on Windows and web. World lines SHALL follow live scene ownership, transforms, visibility and selected camera; overlay lines SHALL support a vector HUD including stroke text. Lines SHALL use explicit edges, preserve documented drawable-pixel thickness, and clip safely at the camera near plane and viewport. Overlay content SHALL render after the world and remain independent of world depth. Vector-only scenes SHALL present successfully with a valid camera. Existing solid meshes and billboards SHALL preserve their appearance when vectors are absent. No platform-specific demo drawing or HTML HUD SHALL be required.

#### Scenario: Live vector scene
- **WHEN** scene-owned outlined objects move, hide or are removed
- **THEN** the next presented frame follows the updated state and cannot redraw a removed object through stale references

#### Scenario: Clipping and sizing
- **WHEN** a world segment crosses the near plane or viewport boundary, or the drawable is resized
- **THEN** only its valid clipped portion appears with finite geometry and consistent documented line width, without giant spikes or stretched HUD elements

#### Scenario: Vector-only presentation
- **WHEN** a valid scene contains only world lines and HUD lines
- **THEN** initial presentation succeeds and shows those lines without requiring a placeholder solid mesh

### Requirement: Checked vector resource lifetime

Vector data SHALL be checked for finite coordinates, valid ranges and documented finite capacities before drawing. Invalid required data or capacity overflow SHALL produce identifying failure rather than unchecked allocation or silent truncation. Zero-sized drawables SHALL suspend submission safely. Initial vector preparation SHALL precede Running; Stop SHALL prevent subsequent submissions and release resources before backend destruction. Existing checked graphics failure behavior SHALL also apply to vector shaders and buffers.

#### Scenario: Invalid vectors
- **WHEN** required segment data contains invalid coordinates, indices or excessive counts
- **THEN** preparation or runtime validation reports the owning asset or scene and follows checked cleanup

#### Scenario: Stop and drawable recovery
- **WHEN** a vector scene resumes from zero drawable size or receives repeated Stop during resource preparation
- **THEN** it either resumes correct presentation or completes eligible cleanup without later drawing or access to released scene data
