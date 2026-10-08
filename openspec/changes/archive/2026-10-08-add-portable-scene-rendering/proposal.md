# Proposal

## Why

Packaged editor projects now build, load and update the same scene on Windows and web, but the shared profile cannot display it. NauDemo's browser renderer proves basic rendering works, but its single-mesh API and demo-specific asset selection cannot present a general supported scene.

## What Changes

- Add an opt-in `basic-rendering-scene` packaged project profile for Windows and web Debug and Release, retaining the existing non-rendering selection.
- Present multiple static meshes through one active camera, with component world transforms, visibility, depth testing and opaque color plus simple directional lighting.
- Share scene extraction, supported asset/material semantics and checked presentation lifecycle; use the existing DX12 Render driver on Windows and extend the WebGL renderer for frame-oriented submission.
- Prepare one validated rendering archive for both platforms, with explicit simple material data and actionable rejection of unsupported content.
- Exercise a dedicated editor-authored rendering scene in EditorProject using the shared application entry and build workflow; retain its full desktop route and existing main scene.
- Validate visible output, scene provenance, updates, resize, failure and resource cleanup on both targets.
- Add shared owner-thread polling of optional runtime services during startup, execution and cleanup, with checked errors and compatibility forwarding for browser services.

## Capabilities

### New Capabilities

- `portable-scene-rendering`: Optional packaged scene presentation, portable render assets, backend integration and cross-platform visual/lifecycle acceptance.

### Modified Capabilities

- `common-application-host`: Add a platform-independent runtime-service polling and failure contract, retaining existing browser service compatibility.

`editor-project-web-startup` continues to describe the non-rendering profile, including its rendering exclusions. Existing minimal and NauDemo requirements remain applicable without amendment.

## Impact

Changes primarily affect NauEngineModules' packaged project declaration/build integration, asset preparation, CPU assets, browser renderer and a new shared scene presentation module with a Windows adapter using Render. Existing Render initialization, shaders and build dependencies may need narrowly scoped extraction for this profile. No new native graphics backend is introduced. NauDemo/EditorProject gains a rendering declaration, authored fixture, portable materials and acceptance coverage. NauEngineLite's common host gains generic runtime-service polling while remaining renderer-independent. Host-native cooking remains required for fresh preparation; browser targets do not link desktop binaries, USD or Qt.
