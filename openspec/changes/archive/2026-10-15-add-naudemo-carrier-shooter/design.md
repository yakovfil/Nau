# Design

## Context

See proposal.md for motivation. NauDemo's `portable_rendering_project.json` currently starts Battlezone; both batch launchers default to it and accept `original`. `DemoBattlezone` demonstrates a shared component, standalone simulation, portable audio and scene-owned vector HUD, with unit and production acceptance tests. The rendering profile accepts static glTF geometry normalized by `NauEngineModules/tools/asset_tools/portable_render_assets.py`; it currently requires one mesh/primitive and excludes glTF materials. `SceneDraw` supplies one flat color per draw. Billboard textures do not imply textured static meshes.

The extracted models contain multiple object/detail variants and conditional polygon groups. CBSINK is a complete single object with 1,601 vertices and 484 polygons. P38 has two complete exports. The full extraction remains separate working-tree data; only selected inputs are required by this feature.

## Goals / Non-Goals

**Goals:** Reuse the existing portable rendering contract; isolate deterministic gameplay from scene/audio adapters; make assets and mission data reproducible and independently packageable; bound runtime entities and mesh instances.

**Non-Goals:** Decode WarBirds runtime animation or flight behavior, extend textured mesh rendering, import the entire model catalog, introduce a general shooter framework, or simulate authentic P-38 carrier operations.

## Decisions

### 1. Solid models through existing static meshes

Curate these complete source sets: `P38_60d15d697083`, `ZERO21_a21eae00ef0a`, `D3A2_aedd3d3bf678`, `G4M2_c92a2833e933`, and user-selected `CBSINK_2e5b082f055d`. Record hashes, selected object keys, selected part groups, axis conversion, origin and scale in a conversion manifest. Inspect the candidate aircraft objects to choose a coherent external flight variant and exclude cockpit, damaged and alternate detail geometry. This is asset selection with a fixed output requirement, not permission to guess or silently repair extraction defects.

Store curated OBJ/MTL inputs and provenance under NauDemo, with a deterministic converter in its tools directory. Triangulate polygons with a concave-capable planar triangulator, calculate normals, and split by original polygon color into single-primitive portable geometry plus simple material declarations. Triangulated USD batches pass through the existing host importer to portable glTF. Preserve relative transforms through a common model root. This avoids extending the backend for textures or vertex colors; a wireframe version would lose the intended solid-aircraft appearance. Retain texture references in provenance without making unused PNGs runtime dependencies.

User-approved repair policy: preserve curated source OBJ files unchanged and record exact source face tokens for any conversion repair. Normalize repeated adjacent/closing vertices; omit the two explicitly identified CBSINK zero-area faces, and reorder the two identified self-crossing island polygons along their visible boundary before triangulation. The converter must check those source tokens before applying a repair, report every repair, and reject all other invalid faces. Verify repaired output visually and with regression fixtures.

Conversion must produce bounded color batches and report triangles/draws per model. Select a suitable detail variant at the target viewing scale and test the maximum planned scene population on both targets. Do not silently discard parts or exceed renderer limits to improve performance. Inspect converted top and oblique views before gameplay integration.

### 2. One scene with a bounded planar simulation

Add a shooter simulation and a dedicated scene component alongside Battlezone. The simulation owns player position, finite waves, enemy paths, projectiles, hit protection, score, lives and event output. Use a fixed simulation step with bounded accumulation, swept projectile collision and deterministic authored spawn order. Use circles or simple extents in the flight plane; visual banking does not alter collision shapes. Scene adapters apply transforms and dispatch accepted sound events without embedding platform logic.

Use finite reusable entity slots with explicit capacities derived from authored waves and projectile lifetimes; validate mission data against them. Inactive slots hide all mesh children and cannot collide or emit audio. Deactivation removes scene owners, clears pending events and releases audio references through existing lifecycle facilities.

### 3. Fixed overhead composition

Use the existing camera projection configured above a horizontal flight plane, looking down with minimal tilt. Keep the combat rectangle and UI safe region visible across aspect ratios by adjusting camera framing; no new orthographic-camera feature is required. Scroll a tiled ocean surface and simple wake/detail geometry downward, while aircraft remain near the origin. Recycle scenery instead of accumulating world distance. Use flat original model colors, modest ambient/directional lighting and readable projectile colors. Reuse scene-owned HUD lines/stroke text for score, lives, wave, controls and terminal prompts; no HTML overlay.

### 4. Explicit sortie phases and tuning defaults

`Takeoff -> Combat -> Recovery -> Complete`; fatal combat damage enters `GameOver`. R from either terminal state resets to Takeoff. Takeoff and recovery animate the P-38 along the CBSINK deck; the carrier exits below at launch and returns into the same scene during recovery. These are arcade animations. Combat input is disabled in automatic phases; hazards are cleared before recovery.

Initial tuning defaults, adjustable without expanding scope: approximately three minutes total; six timed waves (fighters, dive bombers, bombers, fighters plus divers, all three, final bomber formation); player fire every 0.15 seconds; enemy health 1/2/6 and scores 100/200/500; two seconds of protection after damage. Waves use finite spawn schedules and a deadline, removing remaining escaped enemies when necessary. At the final deadline, stop spawning and transition to safe recovery. Three lives are fixed by the spec.

WASD/arrows map to normalized planar movement. Space/mouse share one held-fire state. Focus/visibility loss pauses timers and clears held controls; refocus requires fresh input. Use existing packaged fire/explosion clips, with bounded event playback and browser gesture activation.

### 5. Scene selection and packaging

Make the default declaration target the shooter. Preserve a dedicated Battlezone declaration and existing original declaration; document the same `shooter|battlezone|original` arguments for both launchers. Scene ownership prevents cross-activation of controllers and generic click feedback. Include converter inputs, selection manifest, generated geometry/material metadata, scene, mission data and audio in freshness dependencies. Preparation must run from curated NauDemo inputs without the extraction sibling or original installation. Runtime only reads packaged content.

The existing Battlezone default-startup requirement is intentionally modified. Its main-spec Purpose still calls it a default scene; update that descriptive sentence during final spec synchronization, alongside the delta requirements, to avoid stale documentation.

## Risks / Trade-offs

- Overlapping aircraft parts or inconsistent source scale -> explicitly select variant/parts, normalize coordinates and review silhouettes before integration.
- Many polygon colors create excessive draw calls -> measure chosen variants at maximum wave occupancy and use lower-detail coherent variants where needed; keep renderer limits explicit.
- Concave polygons, winding or handedness errors -> triangulation fixtures, finite/bounds checks and top/oblique rendered comparisons.
- Flat colors omit extracted texture markings -> deliberate first-version limitation, documented in acceptance images; textured mesh support remains a separate change.
- Camera/aspect changes can hide the player or HUD -> fit a fixed gameplay rectangle and validate wide/tall views and zero-size recovery.
- Existing default-dependent tests can accidentally test the shooter as Battlezone -> update selectors explicitly and test default routing separately.

## Migration Plan

Prepare and validate curated art, implement the simulation and adapter, then switch default declarations and launcher routing. Exercise all three selections before accepting the default change. Rollback restores the prior default declaration and launch selection while keeping Battlezone's independent assets and controller intact. No persistent save-data migration is required.
