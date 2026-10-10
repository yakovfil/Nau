# Proposal

## Why

NauDemo has portable camera input but no audible feedback in its Windows and browser rendering deliveries. A short click on mouse-button and camera-key presses provides a small, testable first use of portable engine audio.

## What Changes

- Enable optional Audio in the portable rendering profile, reusing the bundled miniaudio backend for non-spatial one-shot playback.
- Package one short WAV with the scene and load it through the engine filesystem on both targets.
- Play a click for each left/middle/right mouse-button or W/A/S/D/Q/E press while the demo owns focus, without repeat sounds from holding or dragging.
- Preserve brief presses between frames, browser user-gesture activation, bounded playback resources and checked shutdown.
- Validate Windows and real-browser Debug and Release, including actual audio output and existing camera behavior.
- Exclude visible buttons, spatial emitters/listeners, music, streaming, mixer controls, new operating-system targets and general legacy audio repairs.

## Capabilities

### New Capabilities

- `portable-audio`: Packaged one-shot audio, browser activation, lifetime and NauDemo input feedback.

### Modified Capabilities

- `portable-input`: Preserve eligible press transitions between published frames without changing held-state camera semantics.
- `portable-scene-rendering`: Permit explicitly selected Audio alongside optional CoreInput in the rendering profile.

## Impact

NauEngineModules audio/input services, packaged-project declaration/build/preparation support and affected tests; NauDemo rendering declaration, bundled sound, shared game service, README and acceptance harnesses. Bundled miniaudio is reused without adding middleware. Existing default/minimal/non-rendering module graphs and legacy desktop audio consumers retain their behavior. Main specifications remain unchanged until a later sync.
