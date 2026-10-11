# portable-audio Specification

## Purpose

Provide simple packaged sound playback on Windows and web, demonstrated by focused mouse and camera-key feedback in NauDemo.

## Requirements

### Requirement: Portable packaged one-shot audio

Applications explicitly selecting Audio in the rendering profile SHALL be able to load a short PCM WAV from the mounted application archive and play it as a non-spatial one-shot on Windows and web. NauDemo SHALL retain its original-demo click sound and support named short gameplay effects, consuming byte-identical audio content on both targets without native source paths or separate browser sound assets. Missing, unsupported or corrupt required audio SHALL produce an identifying failure during preparation or checked startup, rather than successful silent substitution. Unchanged inputs SHALL package deterministically and changed or missing inputs SHALL invalidate prior preparation results.

Declarations SHALL support a bounded mapping of sound names to packaged WAV sources and continue accepting existing click-only declarations. All declared required sounds SHALL receive the same preparation, format and lifetime validation.

#### Scenario: Relocated delivery plays packaged audio
- **WHEN** the Windows delivery is moved outside the checkout or the web delivery is served under a nested URL
- **THEN** the click sound loads from the same prepared archive and can play without accessing the original source files

#### Scenario: Required sound is invalid
- **WHEN** the required WAV is missing, truncated or outside the supported format limits
- **THEN** preparation or startup fails with the sound path and cause, without publishing a successful replacement or using stale content as current

#### Scenario: Named effects and legacy declaration
- **WHEN** a project declares distinct firing and explosion effects or uses the existing click-only mapping
- **THEN** both targets resolve the declared names to the corresponding packaged sounds without changing the legacy click behavior

### Requirement: Focused NauDemo click feedback

The running original demonstration scene, when explicitly selected, SHALL play one click for each new left, middle or right mouse-button press and each W, A, S, D, Q or E key press while its host owns focus. A pointer press that focuses the host SHALL qualify. Releases, key auto-repeat, continued holds, pointer movement, wheel events and unrelated keys SHALL NOT produce clicks. Distinct rapid presses and simultaneous eligible controls SHALL remain distinct playback requests within the documented bounded capacity. Camera movement, primary-button dragging and scene rendering SHALL retain their existing behavior. No visible UI button SHALL be required.

#### Scenario: Hold and drag
- **WHEN** the user presses W and the primary mouse button, holds them and drags
- **THEN** two click requests occur, camera movement and rotation continue, and the hold, drag and releases add no clicks

#### Scenario: Brief and simultaneous presses
- **WHEN** eligible press/release transitions occur between game frames or multiple eligible controls are pressed together within capacity
- **THEN** each new press produces exactly one request on the next eligible update

#### Scenario: Focus is lost
- **WHEN** the host loses focus or the browser document becomes hidden
- **THEN** pending feedback is discarded, no unfocused input produces sound, and returning focus does not replay old presses

#### Scenario: Game scene selected
- **WHEN** the default Battlezone-style scene is active
- **THEN** generic original-demo click feedback is inactive and sound requests come from gameplay events

### Requirement: Browser audio activation

Browser audio SHALL respect normal user-activation policy and use an eligible trusted interaction with the demo host to activate output. Awaiting activation SHALL be distinguishable from device failure and SHALL NOT prevent the rendered demo from reaching Running. The first eligible press after Running SHALL produce its requested sound after successful activation without requiring a second press. Activation SHALL NOT duplicate the input-triggered request. If activation remains blocked, the application SHALL expose that state, discard stale requests and allow a later eligible gesture to retry without a backlog burst. Unrelated page interaction SHALL remain unaffected.

#### Scenario: First press unlocks audio
- **WHEN** a fresh browser session has suspended audio and the user presses an eligible control in the running demo
- **THEN** output activates and that press produces its requested sound once without autoplay-policy overrides

#### Scenario: Activation is delayed or blocked
- **WHEN** activation cannot complete immediately
- **THEN** pending feedback remains bounded, a blocked state is observable, and focus loss or Stop prevents delayed sounds

### Requirement: Bounded audio lifetime and failures

Audio playback resources and pending input feedback SHALL have documented finite bounds and deterministic overflow behavior. Finished voices SHALL be reclaimed. Once Stop is observed no new sound SHALL start; active playback SHALL stop and asynchronous initialization/activation work SHALL settle or cancel safely before referenced resources are released. Repeated Stop SHALL be harmless. Initialization, decode and device failures SHALL remain observable and follow checked cleanup; a browser awaiting a gesture SHALL not be misreported as device failure.

#### Scenario: Rapid repeated input
- **WHEN** presses exceed playback or pending-input capacity
- **THEN** the documented overflow policy applies without unbounded memory growth, crashes or later playback bursts

#### Scenario: Stop overlaps playback or activation
- **WHEN** Stop is requested during a sound or pending browser activation
- **THEN** playback stops, callbacks cannot restart it or access disposed owners, and repeated Stop is safe

### Requirement: Portable audio acceptance

Acceptance SHALL cover production NauDemo Windows and real-browser Debug and Release deliveries with the same archive, including first-gesture playback, gameplay firing/explosion effects, and, in the explicitly selected original demonstration, all nine eligible controls, repeat suppression, brief presses, focus/visibility loss, bounded rapid input, failures and Stop. Evidence SHALL demonstrate non-silent output from the production audio path in addition to request counts; logging a playback call alone SHALL NOT establish playback. Existing camera/rendering tests and affected legacy desktop and no-audio dependency graphs SHALL remain covered. Commands, revisions, archive identity and any unexecuted checks SHALL be recorded.

#### Scenario: Acceptance is reported complete
- **WHEN** implementation is declared validated
- **THEN** all four configurations have output evidence and behavior results, including relocated Windows and nested-URL browser execution without disabling autoplay policy
