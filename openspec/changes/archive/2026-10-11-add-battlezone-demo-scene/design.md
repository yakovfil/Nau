# Design

## Context

See proposal.md for motivation and scope. NauDemo's root launchers currently select portable_rendering_project.json, whose startup configuration selects portable_rendering.nausd_scene. Its MainGameModule registers DemoFreeCamera and DemoClickFeedback globally when their build definitions are enabled. Both must become conditional on the selected scene rather than simultaneously controlling the new game.

The portable SceneRenderer frame currently contains static triangle meshes and billboards, with separate native/browser backends. It has no world-line or screen-line packet. Screen text exists elsewhere in the engine, but the portable scene backend does not consume it. Portable audio already loads short PCM WAVs and provides bounded one-shot playback; Python declaration validation and preparation currently require exactly an audio.click source. Existing production acceptance hardcodes the old scene's colors and billboard, so switching defaults requires explicit fixture selection rather than weakening those checks.

The reference inspected during exploration is https://6502disassembly.com/va-battlezone/ and its objects.html companion; it links https://github.com/historicalsource/battlezone. These provide visual and historical context. The implementation will author its own line geometry, stroke glyphs and short effects. Exact original object tables, assembly behavior and hardware emulation are unnecessary for the user's visual goal.

## Goals / Non-Goals

**Goals:** Keep gameplay in NauDemo, make vector presentation a small reusable engine capability, preserve the existing packaged lifecycle, and make visual/gameplay acceptance reproducible across Windows and web.

**Non-Goals:** A general UI framework, physics integration, a new renderer/backend, full audio synthesis/streaming, pixel-perfect CRT emulation, or changes to the independent legacy/non-rendering startup defaults. Enemy variants and exact arcade progression are outside this first scene.

## Decisions

### 1. Authored scene with a game component and shared simulation

Add an authored battlezone scene containing the camera and a registered project game component. The component owns bounded gameplay state, activates only with that scene, and updates live scene transforms and vector presentation data. Store reusable edge geometry, obstacle layout and visual constants in a versioned game-content asset referenced by the scene and included in preparation's dependency closure. Validate the scene component and asset through the existing supported-component/packaging contract before Running; no runtime checkout reads.

Use a plain C++ simulation core for player/enemy movement, cooldowns, projectiles, collision, score, lives and state transitions. Advance at a fixed 60 Hz with a bounded accumulator (at most five steps per update; discard excess), seeded randomness for reproducible tests, and no accumulated time across focus/visibility loss. Presentation reads the resulting live scene state. A scene-owned adapter feeds engine frame data; the renderer never advances the game.

Alternative: put gameplay into the renderer or browser script. Rejected because it bypasses scene lifecycle and splits platform behavior. A full physics module is unnecessary for planar tank motion and simple obstacles.

### 2. Explicit edge lists and a shared line pipeline

Extend SceneFrame with value-owned world/overlay line batches from a narrow optional scene presentation-provider interface. The game component registers its contribution for its active scene lifetime; collection happens on the application owner thread. Snapshot copies contain no dangling component pointers and are discarded after submission. Geometry stays in engine world coordinates and uses the selected camera's projection.

Use shared CPU clipping and tessellation into triangles, feeding a small unlit shader on both backends. Clip world segments in homogeneous coordinates before perspective divide, then expand to a documented two-drawable-pixel stroke. Screen lines use an aspect-preserving centered 4:3 logical view fitted into the drawable, with black margins. Scale the stroke with that logical view while clamping to at least one drawable pixel. This avoids reliance on unsupported/inconsistent wide GPU lines and avoids triangulation diagonals from polygon wireframe mode.

The retro scene draws background scenery first, world edges second and HUD last; world edges are intentionally transparent wire outlines rather than solid occluders. Other scene contributors may request depth-tested lines, with existing mesh/billboard behavior unchanged. The default scene's background is black through an explicit validated scene presentation setting; absent a setting the old renderer clear color stays unchanged. A valid camera plus vector content satisfies first-presentation readiness even without meshes.

Start with limits of 16,384 world segments and 8,192 overlay segments per frame, 64 geometry definitions and 4,096 vertices per definition. Validate finite coordinates, edge indices, colors, widths and lengths before buffer allocation. Fail with asset/component identity on overflow; never silently drop required content. Reuse bounded dynamic buffers, handle zero drawable sizes, and follow existing device/context failure and Stop cleanup paths.

Alternative: thin 3D solid meshes for every edge. Rejected because apparent width varies with distance and adds unnecessary mesh assets/draws. A general ScreenText integration is also unnecessary: the game's small stroke alphabet shares its vector overlay path, leaving existing text modules untouched.

### 3. Visual composition is the acceptance target

Author a recognizable tank silhouette with barrel, turret and tracks, boxes and pyramids, and a heading-relative panorama with mountains, volcano and moon. Use bright green unlit lines, dimmer distant scenery, a black field, a center sight and compact upper HUD/radar. Avoid filled polygon faces and mesh triangulation edges. A destruction effect splits outlines into short-lived moving fragments; a brief hit flash/shake communicates player damage.

Review deterministic opening, turned, enemy-hit and game-over captures against the linked visual reference. Record a checklist covering silhouette, composition, outline-only rendering, contrast, horizon and readable HUD, then use platform screenshot comparisons with tolerances for antialiasing. A green-pixel count alone is insufficient. Exact source pixels, flicker, phosphor trails and physical cabinet overlays are not acceptance criteria.

### 4. Compact combat with explicit defaults

Planning defaults: three lives, 1000 points per enemy kill, one hostile tank at a time, a 0.35-second player fire cooldown, a one-second enemy destruction interval, and two seconds of spawn protection. W/S drive and A/D turn; there is no strafe or free look. Space and left mouse share one edge-triggered fire action. R resets only from game over. Show controls in the scene HUD. Begin playable immediately; no coin/start menu is needed.

The enemy seeks a useful range, turns toward the player and fires when aligned, with a bounded interval. Model tanks as planar circles, obstacles as authored bounds, and test swept projectile segments against the nearest obstacle/tank hit to avoid tunneling. Cap projectiles at 32 and destruction fragments at 128 with explicit recycling; expire shots/fragments and constrain the battlefield to finite bounds. Spawn into validated free positions with a bounded fallback list, avoiding overlap with player and obstacles. These tuning defaults are not claims of original arcade behavior.

State transitions are Playing -> PlayerDestroyed -> Playing or GameOver; enemy destruction is an independent short interval. Pause simulation on host focus/visibility loss; clear the accumulator and action queue on resume. Use existing input reset epochs to prevent old transitions from leaking into the resumed game. Pause is separate from Stop and must not recreate scene resources.

### 5. Named short effects on the existing audio service

Generalize the existing audio object to a mapping of identifiers to short WAV paths; retain {"click":"audio/click.wav"} without migration. Permit 1-16 names with validated identifier/path syntax. Python validation, preparation, archive checks, CMake validation and generated policy must agree. Package all values, deduplicate repeated sources, and keep deterministic ordering. Retain the existing WAV limits and bounded voice pool.

Load required fire/explosion clips before Running; emit sounds from accepted simulation events rather than raw key events. Reuse browser trusted-gesture activation and pending-event bounds, clearing pending effects on focus loss, restart, scene deactivation and Stop. AwaitingGesture permits silent visual gameplay; actual decode/device failure remains checked failure. No looping/pitch API is added. The original scene alone retains its generic click service and nine-control acceptance.

### 6. Default selection with explicit regression selection

Keep portable_rendering_project.json as the default declaration but point it to a new battlezone startup configuration. Retain an original-demo declaration selecting the current render_scene.json and content. Extend run_windows.bat and run_web.bat with a backward-compatible second argument: [Debug|Release] [battlezone|original], defaulting to battlezone. Forward the selected declaration to the existing PowerShell helpers; direct build callers can keep using -Declaration.

Because both declarations use basic-rendering-scene output paths, selection must participate in configure/preparation dependencies: switching declarations must regenerate policy and recook required content, never reuse an incompatible package. Regression runners explicitly build/select the original declaration and new game acceptance explicitly builds/selects the default. Avoid assuming two declaration packages coexist in the same output directory. Keep config/scene.json and the independent legacy browser path unchanged.

Existing portable-scene-rendering requirements currently promise the old billboard scene at normal launcher startup and global free-camera controls; the deltas intentionally narrow those to explicit original selection. Portable-audio's click requirements similarly become original-scene requirements. The independent naudemo-web cube path remains supported and is not replaced by this packaged scene selection.

## Risks / Trade-offs

- [Line clipping errors cause large artifacts] -> Shared near-plane/viewport clipping tests, degenerate-segment cases and native/browser visual evidence.
- [A generic wireframe looks unlike Battlezone] -> Review silhouettes and full composition against the reference, not only rendering counters; keep visual refinement in implementation tasks.
- [Gameplay and original services fight over input] -> Scene-owned activation, explicit deactivation cleanup and acceptance of both selections.
- [Default switching invalidates old tests or reuses stale content] -> Explicit fixture declarations, declaration-switch freshness tests and preserved original assertions.
- [Packaging expands beyond the old click field] -> Paired Python/CMake validation tests and unchanged legacy declaration tests.
- [Frame-rate or focus transitions alter combat] -> Fixed-step core tests, swept hits, bounded elapsed time and real-host focus tests.
- [Dynamic line buffers outlive the scene/backend] -> Value snapshots, finite buffers, and Stop during preparation/submission acceptance.

## Migration Plan

Implement and validate vector support without changing the existing default first. Add the authored game and named effects, then enable scene-scoped services and launcher selection. Switch the default only after the new scene and original selection both run. Run all four configurations, relocated/nested deliveries, and affected existing suites; record results in validation.md during implementation. Rollback selects the retained original declaration and restores launcher defaults; generic vector/audio additions remain optional for other projects.
