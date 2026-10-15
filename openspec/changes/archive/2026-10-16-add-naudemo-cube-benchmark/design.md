# Design

## Context

See proposal.md for motivation. NauDemo selects scenes through project declarations and root launchers. SceneRenderer builds one SceneDraw per mesh component, shares geometry resources, and notifies ISceneFrameObserver only after successful backend submission. Its vector source interface already supplies the shooter and Battlezone HUDs. The separate ScreenText service is integrated into other rendering paths, not this packaged scene backend; extending that integration would broaden this change unnecessarily. Existing shooter preparation, probe targets and launcher tests provide local patterns.

## Goals / Non-Goals

**Goals:** a deterministic object workload, low-overhead cadence accounting, and verifiable statistics through the production renderer.

**Non-Goals:** renderer optimization, merged geometry or a new GPU-instancing path, GPU timers, percentile reports, variable cube counts, interactive camera controls, animation, benchmark scoring, VSync changes, or general text integration.

## Decisions

### Authored grid with shared resources

Generate a deterministic scene with one reusable unit cube mesh/material and 1,024 StaticMeshComponent objects at fixed grid positions. Use stable identities and the existing preparation pipeline; add a benchmark-specific declaration and configuration. A spaced XZ grid with an elevated angled camera exposes solid shaded faces. Fit the grid bounding volume to both axes of the drawable, reserving overlay margin; recompute framing only on resize. Do not update cube transforms each frame. This measures normal per-object traversal/submission; collapsing the grid into one mesh would measure a different workload.

### Monotonic submission intervals

Keep timing in a small pure accumulator with injected timestamps for tests. Use steady_clock rather than millisecond simulation dt. The first eligible successful submission seeds the sample; subsequent intervals accumulate until at least one second has elapsed. Publish FPS = intervalCount / elapsedSeconds and milliseconds = 1000 * elapsedSeconds / intervalCount, then begin the next window from the last timestamp. Round both to one decimal place and display pending values until a full window completes. Never average instantaneous reciprocal FPS values. The HUD uses the last completed sample, so the submitting frame cannot recursively change its own overlay.

Register an observer through the same service-provider mechanism demonstrated by shooter_probe.cpp. Gate it on the benchmark startup configuration and live scene ownership. Store shared benchmark statistics independently of scene-component pointers; observers must not mutate scene state or retain borrowed frame data.

### Explicit suspension detection

Use the existing ISceneBackendFactory extension to install a thin benchmark-only decorator around createSceneBackend(). Forward initialization, polling, submission, failure injection and Stop unchanged. Observe successful poll dimensions to invalidate samples at zero drawable or size changes; do not infer suspension from an arbitrary long-frame cutoff, which would hide genuine stalls. Combine this with the existing portable input/host focus and browser visibility state before admitting frame timestamps. Seed a fresh interval on recovery. Stop clears state before forwarding cleanup. This uses existing interfaces and avoids a new general renderer statistics API. Test composition with acceptance failure injection.

### Browser startup budget

The 1,024-object scene can exceed the default ten-second foreground watchdog during Debug browser initialization. Select a sixty-second foreground progress timeout through ApplicationHostOptions for this benchmark only, preserving the existing host failure/Stop machinery. Startup is excluded from cadence samples. Verify startup and Stop under that finite budget and record actual startup time; other scene selections retain their existing options.

### Existing vector HUD

Use packaged stroke glyph data already present in NauDemo, with only the required labels/digits/punctuation and original provenance retained. A benchmark scene component supplies a bounded top-left vector overlay after the solid pass. Cache formatted text/line geometry between sample changes; adjust layout for drawable changes. If needed, factor the existing glyph layout into a small shared demo helper while preserving game HUD output. Missing required glyphs are errors. A browser DOM overlay would not exercise the shared renderer; ScreenText integration is deferred.

### Routing and controller isolation

Add `benchmark` to both launcher usage/validation branches and choose its own project declaration. Keep shooter default and existing selections. Exclude benchmark from generic free-camera and click-feedback services; do not select Audio for a silent workload unless an existing build constraint requires it. Register benchmark behavior only in supported rendering builds, preserving non-rendering and legacy compilation. Scene data and runtime logic remain platform shared.

## Risks / Trade-offs

- Submission cadence includes pacing and CPU work and does not measure GPU completion. Document its meaning and record display/browser conditions; do not impose an FPS floor.
- HUD rendering adds overhead. Use a small fixed label set, one-second formatting updates and bounded cached line geometry; retain the same overlay in comparisons.
- Aspect changes alter pixel workload. Reset samples on resize and record actual drawable dimensions and browser DPR with results.
- A global observer can outlive the scene. Use lifetime-safe shared state, explicit activation/deactivation and Stop reset, and test repeated removal/Stop.
- Grid object count alone does not prove visible output. Combine frame-observer identities/transforms with production screenshots at wide and tall sizes.

## Migration Plan

Add the self-contained scene/preparation, timing and overlay, then routing and acceptance. No existing saved-content migration is required. Rollback removes the benchmark selection and assets/component registration; other scene declarations remain valid. Record validation under ignored build output and a concise checked-in evidence summary, following the shooter pattern.
