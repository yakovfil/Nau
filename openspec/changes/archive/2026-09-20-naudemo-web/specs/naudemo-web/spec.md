# Spec Delta

## Purpose

Run and deliver NauDemo's real scene-driven rotating cube in Chrome on Windows with simplified browser rendering, observable lifecycle and preserved native builds.

## ADDED Requirements

### Requirement: Independent demo browser builds

The project SHALL provide separate Debug and Release NauDemo browser builds using the recorded SDK and required source dependencies. They SHALL statically link the selected real runtime, scene, asset and renderer services with consistent threading support, isolated from native and minimal build caches. They SHALL NOT require desktop rendering binaries, Qt, USD, UI, VFX, physics or desktop shader tools.

#### Scenario: Both demo configurations build
- **WHEN** a developer builds both demo browser configurations with documented prerequisites
- **THEN** each produces an independent runnable demo package without native binary inputs or modifying existing minimal outputs

#### Scenario: Required dependency is missing
- **WHEN** a required source dependency or the supported SDK is unavailable
- **THEN** configuration fails with an actionable diagnostic rather than substituting a host library or installing dependencies implicitly

### Requirement: Real scene-driven cube

The browser demo SHALL use Nau scene objects, scene lifecycle, asset-loaded cube geometry and camera transforms to drive rendering. Native and browser variants SHALL share cube scene construction and elapsed-time rotation behavior while allowing platform-specific setup and materials. A page-side simulation or renderer-owned substitute cube SHALL NOT satisfy this requirement.

#### Scenario: Scene controls the rendered object
- **WHEN** the actual demo starts and its cube transform or camera changes through Nau scene APIs
- **THEN** the submitted geometry and transforms reflect that scene state and the rendered image changes accordingly

#### Scenario: Rotation advances
- **WHEN** completed game updates accumulate two seconds of simulation time
- **THEN** the cube rotates 90 degrees about its Y axis, within one degree numerical tolerance, and rendered frames reflect the changing orientation

### Requirement: Simplified visible rendering

The demo SHALL present a blue opaque cube with perspective projection, depth testing and directional lighting that distinguishes face orientation. Simplified browser shaders and material data are supported; desktop HDR environment and material parity are not required. Missing graphics capability, invalid shaders or unsupported required asset features SHALL produce diagnostic failure rather than a successful blank demo.

#### Scenario: Valid scene is presented
- **WHEN** required scene assets and graphics capabilities are available
- **THEN** the canvas displays a lit three-dimensional blue cube with correctly occluded faces and a visible change across different rotation angles

#### Scenario: Graphics initialization fails
- **WHEN** the required context cannot be created or a required shader fails to compile or link
- **THEN** startup reports Failed with a graphics diagnostic, never reports Running and accounts for partial resources

### Requirement: Canvas sizing and ownership

The page SHALL provide and retain ownership of the demo canvas. Rendering SHALL respect actual client size and device pixel ratio, update projection aspect and drawable dimensions together, and preserve platform geometry in CSS pixels. Graphics resources SHALL have a defined worker owner independent of DOM ownership.

#### Scenario: Canvas size or pixel ratio changes
- **WHEN** the page changes positive canvas dimensions or device pixel ratio during execution
- **THEN** the drawable size and viewport update within graphics limits and the cube keeps correct proportions

#### Scenario: Canvas temporarily has no drawable area
- **WHEN** its client size becomes zero and later becomes positive
- **THEN** drawing pauses safely and resumes at the new size without invalid dimensions or terminal failure solely from zero size

### Requirement: Lifecycle-integrated rendering

The demo SHALL use the shared checked worker lifecycle and nominal 100 ms game cadence. It SHALL report Running only after required scene, asset and graphics initialization succeeds. Rendering SHALL follow actual scene updates without independent page-side game simulation. Hidden-tab resumption SHALL preserve bounded elapsed time and skip missed updates. The page SHALL remain responsive and expose ordered status and Stop.

#### Scenario: Foreground execution and visibility
- **WHEN** the initialized demo runs, becomes hidden and returns to the foreground
- **THEN** real scene updates and rendering resume without catch-up rotation or suspension-sized elapsed time, and page controls remain responsive

### Requirement: Orderly stop and terminal graphics failure

Stop SHALL be asynchronous and idempotent, prevent new updates and draw submissions after observation, and account for pending scene, asset and graphics work before releasing resources. Context loss or host loss SHALL report terminal Failed and attempt safe cleanup. Stopped SHALL require completed successful cleanup. Retry after Stop or failure SHALL require reload; fatal aborts SHALL NOT claim cleanup that did not execute.

#### Scenario: Stop overlaps initialization or pending work
- **WHEN** Stop arrives during initialization, normal rendering or an outstanding scene or asset operation
- **THEN** no later game update or draw begins after Stop is observed, accepted work settles or cancels safely, and repeated Stop does not duplicate teardown

#### Scenario: Graphics context or host is lost
- **WHEN** the running demo loses its context or page host
- **THEN** it reports Failed with the cause, stops new draws, accurately reports cleanup completion and requires reload without automatic recreation

### Requirement: Complete relocatable assets and runtime

Each demo package SHALL contain its runtime artifacts, cube mesh data, browser material/shaders, configuration and serving instructions. Required resources SHALL resolve under the package serving base without original checkout or SDK access. Missing or corrupt required assets SHALL be diagnosed, and stale outputs SHALL NOT conceal missing inputs.

#### Scenario: Package is moved
- **WHEN** either package is copied outside the checkout and served under a nested URL with required hosting headers
- **THEN** the actual demo renders and stops successfully without source-tree or SDK-path requests

#### Scenario: Required asset is absent or corrupt
- **WHEN** a required mesh, buffer or material input is missing or malformed
- **THEN** staging or runtime initialization reports the identified input failure rather than using stale data or entering Running with substitute geometry

### Requirement: Existing configurations remain supported

Native NauDemo SHALL retain its existing scene appearance and rotation behavior. Existing native and browser minimal configurations SHALL preserve their non-rendering graph, timing and lifecycle contracts. Browser renderer options and dependencies SHALL NOT leak into those configurations.

#### Scenario: Existing targets are exercised after integration
- **WHEN** native NauDemo and native/browser minimal configurations are built and exercised after the change
- **THEN** native demo rendering remains supported and minimal graph and lifecycle regression checks pass

### Requirement: Consistent scene transform validity

Native and browser scene transforms SHALL accept finite rotations whose squared
quaternion length differs from one by at most 0.001, including identity and the
engine's normalized rotations. They SHALL reject non-finite rotation components
and rotations outside that tolerance. Non-finite translation or scale SHALL make
the transform invalid. This explicitly corrects the existing inverted rotation
normalization predicate on both platforms.

#### Scenario: A unit rotation is checked
- **WHEN** an identity quaternion, unit rotation or output of the engine's quaternion normalizer is checked
- **THEN** the rotation is reported normalized within the defined tolerance on native and browser builds

#### Scenario: Transform data is invalid
- **WHEN** a rotation is zero-length, outside the normalization tolerance or non-finite, or translation or scale contains a non-finite value
- **THEN** the transform is reported invalid without accepting the data as a normalized finite transform

### Requirement: Reproducible visual and lifecycle acceptance

Acceptance SHALL run the actual Debug and Release demo packages in Chrome on Windows and record source revisions, tools, commands and results. Evidence SHALL combine rendered-output checks with real scene/asset provenance and lifecycle assertions. It SHALL include relocation, resize, failures and native/minimal regressions. A fresh-checkout walkthrough SHALL be executed and recorded separately from clean build-directory checks before reproducibility is declared verified.

#### Scenario: Acceptance is recorded
- **WHEN** this milestone is declared validated
- **THEN** recorded results cover the specified scenarios in both browser configurations, native coexistence and an executed fresh-checkout walkthrough
- **AND** rendering failures, unexpected blank images and test infrastructure errors produce unsuccessful structured test results
