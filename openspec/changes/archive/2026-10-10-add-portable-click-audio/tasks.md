# Tasks

## 1. Portable engine audio

- [x] 1.1 Add the opt-in portable Audio service/backend build subset and checked readiness API while preserving legacy consumers; verify native and Emscripten builds and absence of DataBlock/USD/Qt dependencies in the portable audio graph.
- [x] 1.2 Implement archive-backed bounded WAV loading and shared decoded storage; verify valid mono/stereo clips, supported rates, truncated/oversized/unsupported inputs and storage lifetime with focused tests on native and wasm.
- [x] 1.3 Implement sixteen one-shot voices, completion reclamation and oldest-voice reuse; verify nonzero mixed PCM, independent rapid playback, bounded allocations and deterministic overflow.
- [x] 1.4 Implement browser gesture activation and observable blocked/ready/failure states, with bounded pending requests; verify a fresh real-browser session plays its first keyboard or mouse request under normal autoplay policy using the production backend.
- [x] 1.5 Complete partial-initialization, device-failure and Stop cleanup, including pending browser callbacks; verify injected failures, repeated Stop and no sound/callback access after disposal.

## 2. Reliable input feedback

- [x] 2.1 Add bounded portable press-count publication and queries for Windows/web while preserving held-state APIs; verify between-frame taps, multiple presses, repeats, invalid controls, capacity and cancellation in input tests.
- [x] 2.2 Integrate focus-scoped gesture handling and distinguish normal pointer release from lost capture; verify all three mouse buttons, keyboard-only activation, refocus/visibility/host removal, unrelated page controls and existing camera input tests.

## 3. Packaged NauDemo integration

- [x] 3.1 Extend rendering declaration validation, module selection and preparation with optional Audio and explicit sound mapping; verify matching Python/CMake acceptance/rejection, no-audio declarations and portable runtime dependency audits.
- [x] 3.2 Add the short click WAV with provenance and preparation dependencies; verify identical archive hashes for repeated unchanged preparation, correct packaged bytes, and failure/freshness on changed, removed or invalid sound inputs.
- [x] 3.3 Add the shared demo feedback consumer and enable it in the rendering declaration; verify exactly one request per eligible mouse/W/A/S/D/Q/E press, no hold/release/wheel/unrelated-key sounds, and unchanged camera/scene behavior.

## 4. Acceptance and documentation

- [x] 4.1 Extend acceptance tooling with actual production audio output evidence and input observations; verify all nine controls, brief/simultaneous/rapid presses, first-gesture activation, focus/visibility, errors and Stop in Windows and real-browser Debug/Release with the same archive.
- [x] 4.2 Run relocated native and nested-URL browser root-launcher checks plus affected camera/rendering, lifecycle, legacy desktop and minimal/non-rendering graph regressions; record commands, tool versions, revisions, archive hash, output evidence and any unexecuted checks in validation.md.
- [x] 4.3 Update NauDemo and packaged-project documentation with controls, optional audio declaration, supported WAV subset, activation behavior and capacity policies; verify documented launch/build commands and run strict OpenSpec validation.
