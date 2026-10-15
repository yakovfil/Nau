# Proposal

## Why

The extracted WarBirds aircraft and carrier provide recognizable assets for a compact playable demonstration. A single 1942-inspired sortie will exercise NauDemo's shared scene, input, audio and packaging on Windows and web.

## What Changes

- Make a single ocean scrolling-shooter scene the default in Debug and Release; retain explicit Battlezone and original-demo selection.
- Use the extracted P38 player, ZERO21 fighters, D3A2 dive bombers, G4M2 bombers and the user-selected CBSINK carrier.
- Add automatic carrier takeoff and recovery around six authored waves, movement, held forward fire, three lives, scoring, game over and restart.
- Prepare a curated subset of extracted geometry with original polygon colors into portable meshes; use existing sound and HUD facilities.
- Keep this iteration to one scene without bosses, upgrades, additional levels, flight simulation or textured-mesh renderer expansion.

## Capabilities

### New Capabilities

- `naudemo-carrier-shooter`: Default single-scene sortie, curated extracted art, three enemy behaviors, controls, combat, mission progression and Windows/web acceptance.

### Modified Capabilities

- `naudemo-battlezone`: Replace default Battlezone startup with explicit selection and update regression acceptance to cover the new default alongside both existing selectable scenes.

## Impact

NauDemo game components, scene/content, portable declarations, root launchers, asset conversion tooling, tests and documentation change. Selected inputs originate in `WBFree_extract/extracted/all`; self-contained curated copies belong in NauDemo so builds and deliveries do not depend on that sibling directory or `C:\WBFree`. Existing engine portable static meshes, flat materials, input, audio and scene-owned HUD presentation are reused. This proposal does not require a new graphics backend or third-party runtime dependency.
