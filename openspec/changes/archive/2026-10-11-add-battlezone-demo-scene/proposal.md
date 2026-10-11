# Proposal

## Why

NauDemo currently opens a rendering and input demonstration. A playable Battlezone-style scene will demonstrate the engine through a recognizable retro game, prioritizing the original's vector appearance rather than arcade-accurate simulation.

## What Changes

- Make an authored Battlezone-style scene the default for the root Windows and web launchers in Debug and Release.
- Add green wireframe tanks and obstacles on black, mountain/volcano/moon scenery, crosshair, radar, score, lives, and game-over/restart presentation.
- Add simple shared C++ tank combat: forward/reverse driving, turning, firing, enemy tanks, collision, destruction, respawn, and restart. Use W/S to drive, A/D to turn, Space or left mouse to fire, and R to restart after game over.
- Extend the portable scene renderer with bounded world-line and screen-line presentation suitable for wireframe geometry and a vector HUD, including stroke text.
- Package short firing and explosion sounds through the existing portable audio backend, generalizing the click-only sound declaration compatibly.
- Retain the existing mesh/billboard scene as an explicitly selectable demonstration and regression fixture, with its free camera and click feedback scoped to that scene.
- **BREAKING**: default launcher output and controls change from the free-camera demonstration to tank combat. Existing scene behavior remains available through documented selection.
- Exclude arcade timing/AI fidelity, ROM emulation, original assembly translation, missile/saucer gameplay, coin handling, persistent high scores, continuous engine audio, and CRT post-processing from this change.

## Capabilities

### New Capabilities

- `naudemo-battlezone`: Default retro scene, visual identity, simple combat, controls, packaged content, sound events, and cross-platform acceptance.

### Modified Capabilities

- `portable-scene-rendering`: Add scene-owned portable vector world/HUD drawing; scope existing billboard launch and free-camera expectations to the selectable original demonstration.
- `portable-audio`: Support named packaged one-shot effects while preserving legacy click declarations, scope click feedback to the original demonstration, and generalize activation/acceptance to gameplay sound events.

## Impact

- NauDemo scene content/configuration, declaration, game module services/components, launch/build helpers, README, and acceptance tests.
- NauEngineModules SceneRenderer frame representation and both graphics backends; packaged declaration validation/preparation and CMake policy generation; portable audio consumption without a new backend.
- Existing renderer/input/audio acceptance must select the original fixture explicitly; new acceptance must exercise the default production game on Windows and a real browser in both configurations.
- No new platform, external runtime dependency, desktop-only rendering dependency, or page-side simulation is planned. Historical references inform newly authored geometry, sounds, and C++ behavior.
