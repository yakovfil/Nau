# Design

## Context

See proposal.md for motivation. NauDemo's portable rendering declaration selects CoreInput and its shared DemoFreeCamera consumes held state in gamePreUpdate. PortableInputState currently derives pressed state from consecutive snapshots, losing a down/up pair between publications. Existing input acceptance drives real native/DOM events and verifies camera changes.

The Audio module has a miniaudio backend and AudioService, but its file loading expects native paths, its initialization result is not propagated, and its legacy scene components depend on DataBlock/native asset resolution. Portable rendering declarations currently reject Audio. The package reader already supports independent read/seek access on both platforms. Bundled miniaudio contains a Web Audio backend; its fallback unlock handlers listen to document click/touchend rather than all requested controls. Existing emitter/container bugs are outside the one-shot path.

## Goals / Non-Goals

**Goals:** A small engine-owned audio service consumed by shared demo code, with packaged bytes, bounded ownership and explicit browser state. Preserve ordinary input frame ordering and dependency isolation.

**Non-Goals:** Adapting legacy scene emitter/container loading, a new UI system, spatialization, general streaming/codec support, or extending operating-system support. Headless/non-rendering demos stay audio-free; the four acceptance targets are the current root rendering launchers on Windows/web in Debug/Release.

## Decisions

### 1. Reuse Audio and miniaudio behind a narrow one-shot API

Add a portable service surface for checked clip loading, playback requests, output readiness and shutdown inside the existing Audio module. Keep legacy interfaces source-compatible. In the portable selection compile/register only the service/backend subset needed for one-shots, avoiding DataBlock-based emitter/container integration. Use the same miniaudio decoder/mixer path on both targets; do not implement browser-only HTMLAudio playback or introduce another middleware dependency.

Initialize devices through the existing asynchronous service lifecycle. Expose Initializing, AwaitingGesture, Ready, Failed and Stopping/Stopped states. Required preparation/device failures propagate through checked application failure, while AwaitingGesture permits the scene to run. Do not let a void legacy initialization API turn a new portable failure into successful startup.

### 2. Load a bounded WAV from the existing archive

Add an explicit optional audio section to the rendering declaration mapping the click source to a package path. Include it in host preparation dependencies and the package manifest. A declaration requesting audio assets without Audio is invalid. Add one original or appropriately licensed short click WAV with provenance; it is a regular shipped asset, not a runtime synthesized substitute.

The initial accepted subset is RIFF/WAVE PCM signed 16-bit, mono or stereo, 44.1 or 48 kHz, at most one second and 256 KiB. Validate chunk ranges, format and decoded size in preparation and runtime. Read through IVirtualFileSystem into owned memory, decode once, and keep PCM storage alive until every voice is released. Both platforms use exactly the same archive. Native temporary file extraction and web-only preloaded sound paths were rejected because they complicate relocation and diverge from package semantics.

### 3. Preserve presses without altering camera held-state behavior

Add bounded per-control press counts to pending/published portable input state and an additive query for consumers; leave existing held/movement queries compatible. Count only up-to-down transitions. Accept up to eight presses per control per publication, dropping additional presses until publication; reset clears counts. Preserve counts across normal release/capture completion so a short click is not mistaken for focus cancellation. Unexpected capture loss, focus loss, hidden document, host removal and Stop discard pending feedback. Apply equivalent behavior to the packaged Win32 and browser adapters without forcing it into the legacy gainput path.

A demo service consumes the published counts once per frame for the nine eligible controls, after input publication. It never synthesizes clicks from held state or changes the camera controller. Ignore pre-Running input and unrelated keys/wheel motion. Pointer presses inside the host can focus it and count once; page controls outside it remain unaffected. Handle middle/right-button browser defaults only within the focused demo host when necessary to keep the gesture usable.

Keep press counts stable even if cancellation arrives after publication. Expose live and published cancellation epochs; the demo cancels queued audio and rejects a frame whose epoch has been invalidated, while accepting a newly published press after refocus. Browser mouse down/up events track individual buttons in chords; pointer events continue to own movement and capture.

Use the packaged-scene ready callback to discard pre-Running press transitions without clearing held state. Initial motion suppression does not discard presses arriving after this boundary, so the first eligible click survives. Platform adapters ignore explicit keyboard repeat events, including after focus cancellation.

### 4. Separate gesture activation from playback requests

Bind lifetime-scoped browser handlers to the existing demo host for eligible trusted keyboard/pointer interactions. Invoke activation from the browser UI event stack, with any Emscripten main-thread proxy work respecting current application threading. Activation must not generate an additional sound request: input publication remains the sole source of click counts.

Do not consume a sound into a suspended output context. Retain at most nine activation-pending requests for up to one second while activation is in progress; drop excess/new requests when full and clear expired requests, failed attempts, focus loss and Stop. A successful first gesture plays its request once after readiness; blocked activation reports AwaitingGesture and a later eligible gesture can retry. Generation/lifetime guards prevent late promises or device callbacks from reaching stopped owners. Audit and contain miniaudio's built-in unlock callbacks so they cannot duplicate activation or outlive teardown, without patching bundled third-party code.

Prefer the bundled Web Audio device path compatible with the current delivery headers/threading configuration. Verify its asynchronous startup and linker requirements early; do not silently introduce new server-header requirements or a separate browser audio engine to make the test pass.

Proxy complete miniaudio device calls to the UI thread with the Emscripten system proxy queue, preserving the library's normal embedded JavaScript calls. Export HEAPF32 for its growable-memory output buffer. Preflight browser context availability so a constructor rejection becomes a checked initialization diagnostic. Audio callbacks use a non-blocking mixer lock on the UI thread; failed acquisition yields a silent buffer rather than blocking UI progress. Activation attempts have generation guards and a one-second timeout that permits a later gesture to retry.

### 5. Bound voices and clean up on the owner lifecycle

Use a fixed pool of sixteen independent non-spatial voices referencing shared decoded PCM. Reclaim completed voices on the owner thread; if all are busy, stop/reuse the oldest voice. This makes rapid input deterministic without unbounded allocations. Avoid callback-driven game ownership mutations; audio callbacks only access storage guaranteed live through device shutdown.

Stop rejects new requests, clears activation/input queues, stops voices, detaches gesture handlers, settles/cancels pending initialization, closes the device and releases decoded storage in that order as applicable. Partial initialization follows the same checked ownership rules. Focus loss discards pending feedback; an already playing short click may finish. Physical device failure is terminal for this narrow profile rather than attempting automatic device recovery.

### 6. Validate output and behavior separately

Extend the existing NauDemo input acceptance pattern with request/voice observations plus production-path audio output evidence. Use native loopback capture and real-browser output capture where available; otherwise record an explicit human listening check alongside automated decoded/mixed PCM assertions. A spy counter alone is insufficient. Run with ordinary browser autoplay policy and include first input by keyboard as well as mouse in fresh sessions.

Test all nine controls, between-frame taps, repeats, simultaneous presses, focus/visibility changes, normal versus unexpected capture loss, bounded overflow, first-gesture delay/rejection, corrupt/missing assets, device/init failure and Stop during playback/activation. Reuse rendering and camera checks, relocation/nested hosting, byte-identical archive hashes and no-audio dependency audits. Record any unavailable output check as unvalidated rather than claiming full acceptance.

## Risks / Trade-offs

- Browser backend readiness and user activation cross thread boundaries -> separate activation from request submission and validate first-gesture output before completing integration.
- Existing backend uses legacy ownership/error conventions -> isolate the portable one-shot path and cover partial initialization and shutdown without broad unrelated fixes.
- Input release and capture-loss notifications can coincide -> distinguish normal capture completion from cancellation and test taps that fit within one frame.
- Very rapid input can exceed finite capacity -> document eight presses/control/frame, nine activation-pending requests and sixteen voices with deterministic drop/steal policies.
- Playback counters can pass while output is silent -> require actual production-path output evidence and preserve the distinction in validation records.

## Migration Plan

Add opt-in Audio and declaration support, then enable it only in NauDemo's rendering declaration. Existing declarations remain valid and no-audio graphs unchanged. Shared legacy APIs remain usable. Roll back by removing the demo's optional Audio selection, sound mapping and feedback consumer; retain existing camera input. Sync the three delta specs only when the completed change is archived or explicitly synced.
