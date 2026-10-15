# Spec Delta

## Purpose

Provide a repeatable static cube workload and visible frame-cadence measurements in NauDemo on Windows and web.

## ADDED Requirements

### Requirement: Selectable benchmark delivery

Both root launchers SHALL accept `benchmark` in Debug and Release. Omitting the scene argument SHALL still select shooter, and explicit shooter, Battlezone and original selections SHALL retain their behavior. Benchmark delivery SHALL use the shared packaged application and byte-identical prepared content on Windows and web.

#### Scenario: Benchmark selected
- **WHEN** either launcher receives the benchmark scene argument
- **THEN** the benchmark scene starts without another scene's gameplay or camera controller taking control

#### Scenario: Existing selection retained
- **WHEN** no scene argument or an existing explicit selection is supplied
- **THEN** the previous default or selected scene runs as before

### Requirement: Static 1024-cube workload

The scene SHALL contain exactly 1,024 separately transformed solid cube objects arranged in a spaced 32 by 32 grid, sharing cube geometry and a material. Cubes SHALL remain stationary. A fixed angled camera SHALL frame the entire grid with visible gaps and room for the overlay; resizing SHALL preserve cube proportions and full-grid framing. Movement keys and pointer dragging SHALL NOT alter this benchmark view. The scene SHALL contain no gameplay, animated workload or automatic camera tour.

#### Scenario: Stable workload
- **WHEN** the benchmark renders successive frames without a resize
- **THEN** all 1,024 cube objects contribute to rendering with unchanged transforms and camera pose

#### Scenario: Viewport changes
- **WHEN** the drawable changes between wide and tall shapes
- **THEN** the entire grid remains framed and the overlay remains readable without stretching the cubes

### Requirement: Visible frame-cadence statistics

A top-left in-renderer overlay SHALL display FPS, milliseconds per frame and `CUBES 1024`. FPS SHALL equal completed frame intervals divided by their monotonic elapsed time; milliseconds per frame SHALL equal the reciprocal rate in milliseconds, using the same sampling window. The counter SHALL use successful scene-frame submissions, not simulation updates. Statistics SHALL refresh approximately once per second while active, show a pending indication before a complete sample, and never show non-finite values. Documentation SHALL identify these as submission-cadence measurements subject to presentation pacing, not GPU execution time or guaranteed physical display refreshes.

#### Scenario: Known frame cadence
- **WHEN** successful frames arrive at a known steady cadence for a complete sampling window
- **THEN** the overlay reports the corresponding average FPS and reciprocal frame time within documented rounding tolerance

#### Scenario: No completed sample
- **WHEN** the scene has just started or no complete active sampling window exists
- **THEN** the overlay shows pending statistics instead of a fabricated performance number

### Requirement: Measurement suspension and lifetime

Startup loading, unfocused or hidden periods, and zero-drawable suspension SHALL NOT enter active statistics. Resuming or changing drawable dimensions SHALL start a fresh sampling window. Scene removal or Stop SHALL release benchmark presentation state and prevent stale callbacks from accessing removed components. Required benchmark assets that are missing or malformed SHALL fail with identifying diagnostics through the existing checked startup path.

#### Scenario: Suspend and resume
- **WHEN** the application loses focus, is hidden, or has a zero-sized drawable and subsequently recovers
- **THEN** the next complete sample contains only fresh active frame intervals

#### Scenario: Stop or remove scene
- **WHEN** Stop is requested during startup or rendering, or the benchmark scene is removed
- **THEN** cleanup completes without stale benchmark draws or access to destroyed scene state

### Requirement: Reproducible benchmark verification

Validation SHALL cover Windows and a real browser in Debug and Release, with visible cube and overlay evidence plus an independent check of the 1,024-object workload and stable transforms. It SHALL cover counter arithmetic, resize and suspension recovery, required-content failure, Stop, and launcher selection regressions. Records SHALL include configuration, drawable dimensions, browser/device information, prepared-content hashes and frame-pacing limitations. Acceptance SHALL NOT require a machine-independent minimum FPS; unexecuted checks SHALL be identified.

#### Scenario: Results reported
- **WHEN** benchmark validation is reported complete
- **THEN** all four platform/configuration combinations have visible output and workload evidence, with measured rates described in their execution context
