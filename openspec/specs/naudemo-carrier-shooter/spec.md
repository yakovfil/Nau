# naudemo-carrier-shooter Specification

## Purpose

Provide a compact carrier-to-carrier scrolling shooter using extracted aircraft art through NauDemo's shared Windows and browser runtime.

## Requirements

### Requirement: Default single-scene sortie

The Windows and web root launchers SHALL default to the shooter in Debug and Release and accept explicit `shooter`, `battlezone` and `original` selections. The shooter SHALL use one continuous ocean scene with a fixed overhead view, downward scrolling scenery, automatic carrier takeoff, six finite authored enemy waves, automatic carrier recovery and a mission-complete state. Successful survival through all waves SHALL lead to recovery even when enemies escape. No enemies or hostile projectiles SHALL remain dangerous during takeoff, recovery or terminal states. Both targets SHALL consume byte-identical prepared shooter content.

#### Scenario: Launch and complete a sortie
- **WHEN** the default application starts and the player survives all six waves
- **THEN** the P-38 takes off from the carrier, fights above scrolling ocean, returns to the carrier and displays mission complete without loading another scene

#### Scenario: Scene selection
- **WHEN** a documented scene argument is supplied
- **THEN** only that scene's gameplay controller operates, and an unknown argument fails with usage information

### Requirement: Recognizable extracted aircraft and carrier

The player SHALL use extracted P38 geometry; the three enemy types SHALL use ZERO21, D3A2 and G4M2 geometry. Both mission endpoints SHALL use the CBSINK model from `CBSINK_2e5b082f055d`. Presentation SHALL retain recognizable silhouettes and original polygon colors with solid surfaces. Each aircraft SHALL show one coherent flight configuration without overlapping detail variants. The carrier SHALL show its flight deck and island. Textured mesh rendering and historically accurate carrier operation are outside this version's requirements. Aircraft proportions and readable HUD content SHALL survive drawable resize.

#### Scenario: Mission art is visible
- **WHEN** takeoff and all enemy types are displayed
- **THEN** the twin-boom player, three distinct enemy silhouettes and carrier deck are recognizable, without stacked variants or placeholder aircraft

### Requirement: Focused movement and continuous firing

WASD and arrow keys SHALL move the player within the visible combat area with normalized diagonal speed. Holding Space or primary mouse SHALL fire forward at a bounded cadence; simultaneous bindings SHALL NOT double the firing rate. Release SHALL stop the associated action. Focus loss or browser hiding SHALL pause gameplay and clear held input; recovery SHALL NOT advance suspended time or replay queued movement, shots or sound. Takeoff and landing SHALL control the player automatically. Gameplay SHALL remain usable while browser audio awaits a trusted gesture.

#### Scenario: Hold fire and move
- **WHEN** the player holds movement and both fire bindings during combat
- **THEN** movement remains bounded and forward shots occur at the same cadence as a single fire binding

#### Scenario: Suspend and resume
- **WHEN** focus is lost during combat and later restored
- **THEN** simulation resumes from the paused state with cleared controls and no catch-up damage or sound burst

### Requirement: Three enemy behaviors and finite waves

ZERO21 fighters SHALL enter in fast curved formations and fire sparse forward shots. D3A2 dive bombers SHALL make slower sweeping attacks and fire short spreads. G4M2 bombers SHALL move slowly, withstand more hits than the other types and fire slow aimed bursts. The six waves SHALL introduce the three types separately, then mix them and end with a bomber formation. Escaped enemies SHALL award no score and SHALL NOT block progression. Enemy and projectile populations SHALL be bounded.

#### Scenario: Distinct attacks
- **WHEN** the introductory waves play
- **THEN** fighter formations, sweeping dive bombers and durable aimed-fire bombers demonstrate their different movement and attack patterns

#### Scenario: Enemy escapes
- **WHEN** an enemy leaves its allowed lifetime or play bounds alive
- **THEN** it is removed without score and subsequent waves still proceed

### Requirement: Combat outcome and restart

A new sortie SHALL start with three lives and zero score. Destroying enemies SHALL award their configured score exactly once and show an explosion. Enemy shots or aircraft collisions SHALL consume at most one life per damage event and provide a visible hit response followed by brief invulnerability while lives remain. At zero lives the game SHALL display game over. A new R press in either terminal state SHALL reset the entire sortie, including waves, score, lives, projectiles and carrier sequence. The HUD SHALL show lives, score, current wave and applicable controls or terminal prompts. Accepted player shots and destruction SHALL play distinct packaged sound effects when audio is active. Gameplay outcomes SHALL remain stable across supported frame rates.

#### Scenario: Damage and scoring
- **WHEN** a player shot destroys an enemy and several hostile shots hit the player together
- **THEN** that enemy awards score once and protection prevents simultaneous hits from consuming multiple lives

#### Scenario: Restart after either outcome
- **WHEN** R is newly pressed after game over or mission complete
- **THEN** a fresh three-life, zero-score carrier takeoff begins without stale enemies, effects or input

### Requirement: Self-contained checked content

Builds SHALL use a curated, reproducible subset of extracted art stored with NauDemo, recording source identities, hashes and selected geometry variants. Preparation and delivery SHALL NOT depend on the installed source game or the sibling extraction directory. Missing, malformed or changed required assets SHALL cause identifying failure or regenerate dependent content rather than reuse stale successful output. Repeated unchanged preparation SHALL be deterministic. Gameplay and HUD SHALL use shared native game and engine scene facilities on both platforms.

#### Scenario: Independent delivery
- **WHEN** a native delivery is relocated or a browser delivery is served under a nested URL without source directories
- **THEN** all required shooter visuals and sounds load from packaged content

#### Scenario: Asset changes or corruption
- **WHEN** a required model or mission input changes, disappears or becomes corrupt
- **THEN** preparation updates dependent output or fails with the offending asset identified

### Requirement: Reproducible shooter acceptance

Validation SHALL cover Windows and a real browser in Debug and Release, recording commands, revisions, tool versions and prepared-content hashes. It SHALL include visible takeoff, all aircraft types, combat, landing, HUD and terminal states; deterministic gameplay tests; audible firing and explosions; focus/visibility, resize and zero-drawable recovery; repeated Stop during startup and play; relocated native and nested-URL browser delivery; and regression checks for explicitly selected Battlezone and original scenes. Unexecuted checks SHALL be identified and SHALL NOT count as passed.

#### Scenario: Acceptance reported
- **WHEN** implementation is declared validated
- **THEN** evidence covers all four platform/configuration combinations and both existing scene selections, including actual visible and audible output rather than observer counts alone
