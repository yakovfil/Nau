# Proposal

## Why

NauDemo needs a small repeatable rendering workload with visible performance feedback. A static 1,024-cube scene provides an initial baseline for comparing Windows and browser deliveries without gameplay or animation variability.

## What Changes

- Add an explicitly selectable `benchmark` scene on Windows and web in Debug and Release; keep shooter as the default.
- Display exactly 1,024 stationary cube objects in a spaced 32 by 32 grid with a fixed angled view and shared geometry/material.
- Display averaged FPS, milliseconds per frame and cube count through the packaged renderer's existing vector HUD support.
- Measure successful frame-submission cadence using a monotonic clock, excluding startup and resetting across focus/visibility or drawable suspension.
- Document repeatable Release runs and frame-pacing limits; verify the workload and overlay on both platforms.

## Capabilities

### New Capabilities

- `naudemo-cube-benchmark`: selectable static cube workload, trustworthy frame-cadence display and repeatable validation.

### Modified Capabilities

None. The new scene extends explicit routing without changing the default or existing scenes' requirements.

## Impact

NauDemo scene/configuration/declaration assets, a benchmark component and frame observer, launchers, preparation integration, tests and documentation. Reuse SceneRenderer's existing mesh, vector and frame-observer interfaces and existing packaged stroke glyphs. No new third-party dependency or general screen-text integration is planned. Existing shooter, Battlezone and original paths remain supported.
