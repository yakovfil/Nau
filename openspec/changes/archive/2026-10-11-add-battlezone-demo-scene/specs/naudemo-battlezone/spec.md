# Spec Delta

## Purpose

Present a playable Battlezone-style default NauDemo scene that reproduces the recognizable retro vector appearance on Windows and web with simple tank combat.

## ADDED Requirements

### Requirement: Default packaged game scene

The root Windows and web launchers SHALL open the Battlezone-style scene by default in Debug and Release through the shared packaged application. Both targets SHALL consume byte-identical prepared content. The original mesh/billboard scene SHALL remain explicitly selectable through a documented launcher option, retaining its camera and click feedback. Selecting one scene SHALL NOT activate the other's controllers. Existing non-rendering and legacy desktop entry paths SHALL retain their supported behavior.

#### Scenario: Normal launch
- **WHEN** either root launcher is run without a scene override
- **THEN** the production application displays the playable retro battlefield with score, lives, and controls rather than the previous mesh demonstration

#### Scenario: Original scene selected
- **WHEN** the user selects the documented original-demo option
- **THEN** the original animated meshes, billboard, free-camera controls, and click feedback operate without tank gameplay

### Requirement: Recognizable vector appearance

The game SHALL display a black background, predominantly green unlit wireframe tanks, pyramids and box obstacles, a mountain horizon with volcano and moon, a centered sight, radar, stroke-style score/lives text, and a visible destruction effect. World outlines SHALL be authored edges without filled faces or triangulation diagonals. A first-person ground-level camera SHALL turn with the player tank, while the HUD remains screen-relative. Visual reproduction SHALL prioritize composition and silhouettes over exact CRT output or arcade hardware behavior.

#### Scenario: Battlefield is visible
- **WHEN** a new game reaches its first presented frame
- **THEN** the view contains a recognizable outlined enemy tank, obstacles, horizon scenery, crosshair, radar and readable score/lives against black

#### Scenario: Turning and resize
- **WHEN** the player turns or the drawable aspect ratio changes
- **THEN** battlefield and horizon respond coherently to heading while tank proportions, line visibility and HUD readability are preserved

### Requirement: Simple focused tank controls

While the host has focus, W/S SHALL drive forward/backward and A/D SHALL turn left/right without strafing, vertical motion or free-camera drag. Space or left mouse SHALL request firing with a bounded cooldown; holding fire SHALL NOT generate additional shots. Simultaneous fire bindings within one update SHALL request at most one shot. Release and focus loss SHALL clear movement, and stale press events SHALL NOT fire after refocus. Gameplay SHALL pause while unfocused or hidden and resume without a suspension-sized simulation jump.

#### Scenario: Drive and fire
- **WHEN** the focused player holds W and A and newly presses Space or left mouse
- **THEN** the tank drives through a turn and fires once if its cooldown permits, without changing camera pitch or producing legacy click feedback

#### Scenario: Focus loss
- **WHEN** focus is lost during movement or firing and later restored
- **THEN** gameplay resumes from its paused state with no held movement, queued shot, damage catch-up or backlog of sound effects

### Requirement: Complete compact combat loop

The game SHALL begin with three lives and zero score. One hostile tank at a time SHALL pursue/aim and fire at the player; destroyed enemies SHALL be replaced after a visible destruction interval. Player projectiles SHALL destroy an enemy on impact and award 1000 points exactly once. Obstacles SHALL block tank movement and projectiles. A hostile hit SHALL consume one life, show a hit/destruction response, and respawn the player with a brief protection interval if lives remain. At zero lives gameplay SHALL enter game over and display an R-to-restart prompt; a new R press SHALL reset score, lives, enemies and projectiles. Radar SHALL reflect the live enemy's bearing relative to the player. Collision and gameplay timing SHALL remain stable across supported presentation frame rates.

#### Scenario: Destroy enemy
- **WHEN** a player shot reaches the enemy before a blocking obstacle
- **THEN** the enemy is destroyed, score increases by 1000 once, the destruction is visible, and another enemy subsequently appears

#### Scenario: Obstacle blocks combat
- **WHEN** a tank or shot reaches a blocking obstacle
- **THEN** the tank cannot pass through it and the shot cannot damage a target behind it

#### Scenario: Lose and restart
- **WHEN** hostile hits exhaust all three lives and the user newly presses R
- **THEN** game over transitions to a fresh playable game with three lives, zero score and no stale projectiles or input

### Requirement: Game sound events and packaged content

Accepted shots and tank destruction SHALL trigger distinct short packaged firing and explosion effects through portable audio. Gameplay SHALL remain visually usable while browser audio awaits a trusted gesture. Missing or corrupt required geometry, scene configuration or sound content SHALL cause an identifying preparation/startup failure rather than fallback content. Repeated unchanged preparation SHALL be deterministic, and changed or removed game inputs SHALL invalidate stale packages. Gameplay and presentation SHALL use engine scene state and shared native game code rather than browser-page simulation.

#### Scenario: Audible combat
- **WHEN** an eligible shot is accepted and a tank is subsequently destroyed with audio activated
- **THEN** distinct non-silent firing and explosion effects occur without an additional generic button click

#### Scenario: Required input changes
- **WHEN** a required game asset changes, disappears or becomes invalid before building
- **THEN** preparation includes the new valid content or fails with its path, and does not publish a stale successful package

### Requirement: Reproducible game acceptance

Acceptance SHALL cover Windows and a real browser in Debug and Release using the same prepared content. It SHALL include production screenshots establishing the reference-inspired composition and wireframe silhouettes, deterministic behavior checks for combat/score/lives/restart, actual non-silent sound output, focus/visibility recovery, resize and zero-drawable recovery, missing/corrupt content, and repeated Stop during play and pending startup. Native delivery SHALL run outside the checkout and web delivery under a nested URL without autoplay overrides. Both default and explicitly selected original scenes SHALL be exercised, and affected no-audio/non-rendering/legacy paths SHALL retain coverage. Evidence SHALL record commands, revisions, tool versions, archive hashes, visual tolerances and any unexecuted checks; observer counts alone SHALL NOT establish visible or audible success.

#### Scenario: Completion claimed
- **WHEN** this change is reported validated
- **THEN** all four target/configuration combinations have production visual and gameplay evidence, audible output evidence, lifecycle results and original-demo regression results
