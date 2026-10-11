# Tasks

## 1. Portable vector presentation

- [x] 1.1 Add bounded scene-owned world/overlay line snapshots and explicit presentation settings to SceneRenderer; verify vector-only readiness, contributor removal, absent-vector compatibility, invalid data and overflow with focused contract tests.
- [x] 1.2 Implement shared homogeneous clipping and stroke tessellation with documented width/aspect rules; verify near-plane crossings, offscreen and degenerate segments, non-finite input, viewport resize and depth conversion with CPU tests.
- [x] 1.3 Implement unlit vector shaders, reusable buffers and world/HUD submission in the Windows backend; verify a native checkpoint visibly renders outlines and overlays and cleans up on shader/buffer failure and repeated Stop.
- [x] 1.4 Implement the equivalent browser backend path; verify a real-browser checkpoint, resize/zero-size recovery and context-loss cleanup, comparing its framing and stroke appearance with the native checkpoint.

## 2. Game content and simulation

- [x] 2.1 Add the authored Battlezone scene, project component registration, versioned edge/layout content and packaging dependency closure; verify deterministic preparation, supported-component decoding and identifying errors for missing geometry, invalid indices and changed content.
- [x] 2.2 Implement the fixed-step planar tank simulation, movement bounds, obstacles, swept projectile collision and enemy aiming/firing; verify deterministic tests for nearest-hit blocking, no tunneling, cooldown, one-shot press behavior and bounded projectile/spawn handling.
- [x] 2.3 Add score/lives, enemy destruction and replacement, player protection/respawn, game over and restart; verify exactly-once score/life changes, three-life exhaustion, reset state and equivalent outcomes across different presentation step sequences.
- [x] 2.4 Connect the simulation to live scene transforms, camera and focused portable input; verify W/S drive, A/D turn, merged Space/mouse action, focus/visibility pause, stale-event cancellation and no suspension catch-up on both hosts.
- [x] 2.5 Author/refine tank silhouettes, obstacles, horizon/volcano/moon, crosshair, radar, stroke HUD and destruction visuals; verify opening, turned, hit and game-over screenshots against the reference checklist and confirm radar follows live enemy bearing.

## 3. Packaged game audio

- [x] 3.1 Generalize named short-sound mappings consistently across Python preparation/validation, archive checks and CMake policy generation while retaining click-only declarations; verify valid multi-effect and legacy declarations, malformed names/paths, bounds, missing/corrupt WAVs, deterministic archives and freshness.
- [x] 3.2 Author packaged firing/explosion effects with provenance and connect accepted simulation events to the existing portable audio service; verify distinct non-silent output, first trusted fire gesture, no generic gameplay clicks, bounded blocked activation and clearing pending effects on restart/focus loss/Stop.

## 4. Default selection and compatibility

- [x] 4.1 Scope existing free-camera/click services to the original demonstration and game services to Battlezone; verify each selected scene has only its intended controllers and deactivation releases scene contributions and pending audio.
- [x] 4.2 Make the game declaration/default startup active and add the backward-compatible [configuration] [battlezone|original] launcher selection plus an original declaration; verify both literal root launchers, declaration-switch rebuild freshness and unchanged independent legacy/non-rendering startup.
- [x] 4.3 Update README controls/selection and make existing rendering, billboard, camera and audio tests explicitly select the original fixture; verify their original assertions still pass rather than being relaxed for the changed default.

## 5. Acceptance and evidence

- [x] 5.1 Add production game acceptance with deterministic scenario setup/observation separated from visible-output checks; verify movement, fire, enemy hit, obstacle blocking, score/lives/restart, focus recovery, readable HUD and reference-inspired silhouettes through the real scene/rendering path.
- [x] 5.2 Run Windows and real-browser Debug/Release game and original-scene acceptance with matching per-scene archive hashes, relocated native packages and nested browser URLs; collect screenshots and actual audio evidence without autoplay-policy overrides.
- [x] 5.3 Run missing/corrupt game-data/sound, vector capacity, graphics failure, zero-size recovery and repeated Stop/pending-startup cases, plus affected non-rendering/no-audio/legacy/common-host regressions; verify identifying failures and eligible resource cleanup.
- [x] 5.4 Record commands, tool versions, component revisions, archive hashes, visual checklist/tolerances and results in validation.md; verify every requirement has evidence or an explicit unexecuted limitation before marking validation complete.
