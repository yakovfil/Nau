# Proposal

## Why

The editor-created NauDemo project builds against the desktop SDK, but cannot use the engine's existing browser lifecycle and package reader through its generated build. A non-rendering browser startup milestone will establish the editor-to-runtime path using real compiled assets, scene objects and project components before expanding platform services.

## What Changes

- Add reusable browser project build integration and apply it to `NauDemo/EditorProject`, with separate Debug/Release outputs and a statically linked game module.
- Prepare editor-authored assets with native tools, then package configuration, compiled startup scene, asset mappings and its required data dependencies for browser delivery.
- Expose portable compiled-scene loading without enabling the full desktop asset-format or graphics graph.
- Use the common application host to mount content, register project components, deserialize and activate the actual startup scene, run updates and stop safely.
- Validate supported component types and required assets explicitly; failure prevents Running instead of substituting missing components or an empty scene.
- Verify hierarchy, transforms, properties, component updates and lifecycle completion in real-browser Debug and Release runs.

Non-goals: rendering or GPU views, physics simulation, animation playback, audio, input handling, browser USD importing, editor UI export controls, arbitrary desktop-module portability, and changing the existing rendered NauDemo web application.

## Capabilities

### New Capabilities

- `editor-project-web-startup`: Build and deliver editor-created projects for a non-rendering browser runtime, including native asset preparation, real scene/component loading and checked startup/shutdown.

### Modified Capabilities

None. This capability composes the existing common host and portable package contracts. The rendered `naudemo-web` capability and its acceptance requirements remain unchanged.

## Impact

- `NauEngineModules`: reusable browser project CMake integration, portable scene-format registration, selected runtime modules, host asset-tool integration, tests and applicable project-template support.
- `NauEngineLite`: only generic framework/VFS/configuration or checked startup changes needed by the new consumer; no project-specific paths or concrete feature dependencies in the kernel/common host.
- `NauDemo/EditorProject`: browser build selection, delegate/service setup, package inputs, delivery helpers and acceptance fixtures.
- Dependencies: existing pinned Emscripten SDK and native toolchain, host OpenUSD/tools, existing portable package format and browser lifecycle. Native SDK binaries and USD remain outside the WebAssembly link graph.
- Compatibility: retain the desktop project build and existing native/browser demo, minimal runtime and package-reader behavior. Generated outputs remain inside ignored project build directories.
