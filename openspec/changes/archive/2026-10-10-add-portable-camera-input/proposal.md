# Proposal

## Why

NauDemo's packaged Windows and web scene renders the same camera view, but users cannot navigate it. The legacy Windows application links CoreInput, while the packaged runtime excludes it and the bundled gainput backend has no browser input path.

## What Changes

- Add a portable keyboard and pointer input path to the engine's CoreInput module, with Windows window messages and browser host events feeding one shared input contract.
- Permit an explicitly declared CoreInput module in the packaged `basic-rendering-scene` profile on Windows and web without adding input to minimal or non-rendering projects.
- Add shared NauDemo free-camera behavior: WASD moves relative to camera facing, Q/E moves vertically, and primary-button mouse drag changes yaw and pitch. Release or focus loss ends drag and clears held inputs.
- Validate camera movement, focus and resize behavior, and orderly shutdown in Windows and browser Debug and Release deliveries.

## Capabilities

### New Capabilities

- `portable-input`: Keyboard and pointer state, platform event delivery, update ordering, focus and lifecycle rules for CoreInput on Windows and web.

### Modified Capabilities

- `portable-scene-rendering`: Allow optional CoreInput in the rendering profile and require the shared NauDemo scene camera to respond to input on both platforms.

## Impact

NauEngineLite's optional game-step input phase; NauEngineModules CoreInput, browser platform integration and packaged project CMake/validation; NauDemo's rendering declaration, shared game code and acceptance tests. Existing non-rendering and minimal runtime graphs remain input-free. No authored scene or archive format change is required.
