# Spec Delta

## Purpose

Provide a small engine capability for drawing a single text line from a specified packaged TTF asset through the same application-facing contract on native and browser targets.

## ADDED Requirements

### Requirement: Specified font asset loading

The engine SHALL load a project-controlled TTF font from a caller-specified mounted virtual filesystem path and retain the bytes for every operation that depends on them. It SHALL use the specified font without substituting an OS-installed or browser-selected font. Missing, empty, detectably unsupported, or oversized font inputs SHALL return a diagnostic identifying the asset. Support for arbitrary untrusted fonts is outside this capability.

#### Scenario: Same asset on both targets
- **WHEN** native and browser applications load the same supported TTF bytes through their mounted asset filesystem
- **THEN** they obtain equivalent font metrics and glyph coverage for the same preparation inputs without consulting system fonts

#### Scenario: Font cannot be loaded
- **WHEN** the specified font path is missing, empty, detectably unsupported, or exceeds documented bounds
- **THEN** loading fails with an asset-specific error and no substitute font is selected

### Requirement: Single-line text preparation

The engine SHALL prepare a UTF-8 single line using the specified font and positive finite size, preserving glyph advances, pair kerning, whitespace, bearings, and descender extents. It SHALL expose line metrics sufficient to position and measure the result. The requested size SHALL represent ascent-minus-descent height in logical pixels. Empty text SHALL produce no drawable pixels. Missing codepoints SHALL use the specified font's missing-glyph representation. Invalid UTF-8, line breaks, invalid sizes, or requests exceeding documented memory/dimension limits SHALL return an error. Complex script shaping and bidirectional layout are outside this capability.

#### Scenario: Metrics and whitespace are preserved
- **WHEN** a supported line includes a kerning pair, spaces, and descenders
- **THEN** its metrics and visible coverage reflect the selected font without clipping glyph extents or drawing pixels for spaces

#### Scenario: Empty or unsupported input
- **WHEN** the caller prepares empty text or a codepoint absent from the selected font
- **THEN** empty text produces no visible output and the absent codepoint uses the selected font's missing-glyph representation

#### Scenario: Invalid preparation request
- **WHEN** the text contains malformed UTF-8 or a line break, the size is nonpositive/nonfinite, or a documented bound is exceeded
- **THEN** preparation fails diagnostically without publishing a partially prepared line

### Requirement: Shared rendering contract

Native and browser applications SHALL use the same engine-facing contract to submit prepared text at an upper-left screen-space position with a color and opacity. Coordinates SHALL use native engine client pixels on native targets and CSS pixels on browser targets. Both renderers SHALL present the text above the scene using glyph coverage for transparency, preserve the scene beneath transparent pixels, clip at the viewport, and avoid depth occlusion of the text. Application text code SHALL NOT require platform window text APIs or page text overlays.

#### Scenario: Text is composited above a scene
- **WHEN** a prepared line is submitted over rendered geometry with a chosen position, color, and opacity
- **THEN** glyphs appear at that position above the geometry, transparent regions preserve the existing image, and the caller uses the same contract on both targets

#### Scenario: Text extends outside the viewport
- **WHEN** a submitted line partly extends beyond a viewport edge
- **THEN** visible pixels are clipped to that viewport and drawing does not modify another surface or corrupt the scene pass

### Requirement: Stable preparation and viewport behavior

The engine SHALL reuse unchanged text preparation and backend uploads across frames. Position/color changes SHALL NOT require font parsing or glyph rasterization. Font, text, size, or raster scale changes SHALL refresh the affected prepared image or upload. Browser text SHALL retain its logical position and size when device pixel ratio changes, with raster resolution matching the drawable scale. A zero-area viewport SHALL skip rendering safely and positive resize SHALL resume drawing. Submission SHALL describe one frame rather than accumulate duplicate draws indefinitely.

#### Scenario: Repeated frames and changed color
- **WHEN** an unchanged prepared line is drawn repeatedly and its position or color changes
- **THEN** the engine reuses its coverage/upload, presents the changed appearance, and does not accumulate old submissions

#### Scenario: Browser ratio or viewport changes
- **WHEN** browser device pixel ratio changes or the viewport becomes zero-sized and then positive
- **THEN** logical placement and size are preserved, changed raster scale is reflected, and drawing pauses/resumes safely

### Requirement: Owned resources and shutdown

The engine SHALL keep font and prepared-text data alive while accepted work uses them, release unused cached resources, and perform graphics operations on the owning renderer thread or worker. Shutdown SHALL reject further submission, account for accepted work, release text resources together with renderer resources, and remain idempotent. Initialization/upload failure SHALL report an error and account for partial resources. Browser context loss SHALL preserve the existing terminal failure behavior without unsafe resource operations.

#### Scenario: Handles are released after submission
- **WHEN** the application releases its font or prepared-text handle while a submitted frame still refers to it
- **THEN** accepted work remains valid and the associated resources become reclaimable when no longer in use

#### Scenario: Stop or partial initialization failure
- **WHEN** Stop is repeated or initialization fails after some text graphics resources exist
- **THEN** new draws do not start, existing resource ownership is accounted for, and teardown does not double-release resources

### Requirement: Optional portable dependency graph

The text capability SHALL be buildable for the supported native Windows and Emscripten targets without requiring the existing full UI stack. The browser text path SHALL NOT require native rendering binaries, desktop shader tools, or system font installations. Feature implementation and concrete module integration SHALL remain outside the standalone engine kernel. Existing configurations that do not enable text SHALL retain their dependency/lifecycle behavior.

#### Scenario: Minimal configurations remain independent
- **WHEN** standalone kernel and existing minimal runtime configurations are configured after text support is introduced
- **THEN** they continue to build without acquiring text renderers or concrete feature-module references

#### Scenario: Browser text graph is configured
- **WHEN** the browser demo enables text
- **THEN** its build resolves the portable text dependencies without pulling in the desktop UI or native rendering stack
