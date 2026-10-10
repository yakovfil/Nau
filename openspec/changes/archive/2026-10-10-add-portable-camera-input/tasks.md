# Tasks

## 1. Ordered portable input contract

- [x] 1.1 Add an optional input-frame stage before application pre-update in the common game step; verify a focused host test observes fresh input before the delegate without adding input dependencies to a minimal consumer.
- [x] 1.2 Consolidate CoreInput frame advancement for the new stage while preserving native gainput action/signal behavior; verify held and pointer-delta tests show exactly one advancement per game step and existing native input tests pass.
- [x] 1.3 Define and test the supported portable `nau/input.h` keyboard, button and pointer queries, including unknown codes and explicit diagnostics for unsupported browser APIs.

## 2. Platform event delivery

- [x] 2.1 Connect Windows active-window key, button, movement and focus events to the ordered frame state; verify press/hold/release, drag release and focus-loss cases in a native input fixture.
- [x] 2.2 Add browser host-scoped keyboard and pointer event delivery on the UI thread with owner-thread queueing, host focus and pointer capture; verify the production service in a real browser for movement, release outside the host and unrelated page interaction.
- [x] 2.3 Handle browser visibility loss, host loss, Stop and partial initialization by resetting state and detaching callbacks; verify repeated cleanup and events after Stop cannot access disposed state.
- [x] 2.4 Verify pointer coordinates and deltas use consistent client/CSS pixel units across Windows and web, including browser device pixel ratio and host resize cases.

## 3. Packaged project integration

- [x] 3.1 Extend CMake and Python declaration validation to accept optional CoreInput only with `basic-rendering-scene`; verify accepted and rejected declarations identify the same module set on both paths.
- [x] 3.2 Add the selected input sources, registration and platform dependencies to packaged Windows/web graphs without browser gainput or desktop binaries; verify Debug and Release configure/build and that non-rendering/minimal dependency audits remain unchanged.

## 4. Shared demo free camera

- [x] 4.1 Declare CoreInput in NauDemo's rendering profile and add shared authored-camera lookup/control after scene startup; verify camera identity and first-step view change from a held movement key.
- [x] 4.2 Implement WASD/QE elapsed-time movement and primary-button drag yaw/pitch with bounded pitch, diagonal speed and suspension time; verify unit or scene tests for directions, no-input identity and bounded updates.
- [x] 4.3 Exercise `run_windows.bat` and `run_web.bat` deliveries in Debug and Release with visible camera movement, drag, release, focus loss, resize and orderly Stop; record commands, prepared-archive identity, results and any unexecuted checks.
- [x] 4.4 Run affected native input, common-host, portable rendering and non-rendering regressions; verify no change to legacy desktop startup and document any concrete regression or limit.
