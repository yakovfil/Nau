# Proposal

## Why

The working browser build runs Nau's non-rendering lifecycle, while NauDemo's rotating cube still depends on the desktop scene, asset and DX12 rendering stack. A bounded scene-driven browser demo will establish the next usable rendering milestone without requiring desktop visual parity.

## What Changes

- Add a separate NauDemo browser profile with isolated Debug/Release builds and explicit scene, asset and rendering dependencies.
- Port the real scene/camera/mesh subset and integrate it with the shared checked worker lifecycle.
- Add a browser rendering path for an opaque blue static mesh, perspective camera, depth testing and simple directional lighting.
- Share the cube's scene construction and elapsed-time Y-axis rotation between native and browser demo paths, allowing platform-specific startup and materials.
- Package the cube mesh, browser shaders and configuration for relocatable delivery; provide canvas presentation, resize handling and lifecycle controls.
- Validate actual rendered output, scene-driven motion, failure cleanup, package relocation and native/minimal regressions.

## Capabilities

### New Capabilities

- `naudemo-web`: Real Nau scene-driven rotating-cube execution and delivery in Chrome on Windows with simplified rendering and native coexistence.

### Modified Capabilities

None. Existing minimal profiles remain non-rendering. Shared lifecycle cadence, platform CSS geometry, page ownership and reload policy remain unchanged; the new renderer owns graphics resources separately from PlatformApp.

## Impact

NauDemo source, configuration and build integration; NauEngineLite profile selection, framework scene integration, scene/assets portability and browser rendering services; browser packaging/tests; build and prerequisite documentation. Required dependencies must use recorded sources and the existing SDK pin unless concrete compatibility evidence requires a separately reviewed change. No editor or documentation-submodule implementation changes are planned.

## Non-goals

Desktop material/shader parity, HDR environment rendering, deferred rendering, shadows, post-processing, UI, VFX, animation, physics, general-purpose browser editor support, in-page restart and other-browser acceptance. This milestone does not promise a complete replacement for the desktop Render API or a new frame-rate contract.
