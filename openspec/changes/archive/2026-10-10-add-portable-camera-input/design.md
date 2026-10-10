# Design

## Context

See proposal.md for motivation and the spec deltas for behavior. The current packaged entry uses `PackagedSceneDelegate`, which loads and activates the authored camera. The renderer reads the live main camera each frame. The legacy Windows application links CoreInput, but the packaged declaration validators accept an exact module set without it. CoreInput's current device implementation uses gainput and Windows message handlers; this bundled gainput version has no Emscripten backend. The main loop collects input and application pre-update callbacks without an ordering contract.

## Goals / Non-Goals

**Goals:**

- Keep one keyboard/pointer query surface and one free-camera controller source for both packaged targets.
- Establish input sampling before application pre-update without requiring scene or renderer dependencies in the host.
- Preserve native CoreInput consumers and the existing default profile dependency graphs.

**Non-Goals:**

- Browser parity for gainput actions, signals, gamepads, touch or text input.
- Changing editor navigation, authored camera transforms, or content archive format.
- Pointer lock or unbounded mouse look; the first behavior uses primary-button drag.

## Decisions

### Keep the public portable queries and split their platform backends

Use the keyboard and mouse query surface in `nau/input.h` for the controller. Keep gainput for existing Windows input, and add an engine-owned browser keyboard/pointer backend rather than trying to compile this gainput fork for Emscripten. Browser input provides the specified subset; gainput-only `IInputSystem` actions and signals remain outside the browser subset and must have an explicit unsupported diagnostic if requested. Native service registration and callers retain their current API. A new dependency on an updated gainput fork was considered, but would enlarge the change and affect bundled third-party code.

### Sample input at one defined game-step point

Add an optional, platform-neutral input-frame hook in the app framework, executed on the application owner thread before ordinary pre-update callbacks. CoreInput registers one provider for this hook. It drains pending platform events and publishes held state and accumulated pointer delta exactly once per eligible step. Existing input update paths must be consolidated or guarded to avoid advancing gainput twice. This is preferable to depending on the current incidental ordering of `IGamePreUpdate` services and the delegate loop. Pending startup may collect events, but the first ordinary step gets a coherent current state and no burst of stale movement.

### Bind browser input through the existing page-owned host

The browser adapter obtains the active host from the browser platform service and installs DOM keyboard, pointer, focus and visibility handlers on the UI thread. It focuses the host on primary-button interaction without replacing the page's host or adding HTML controls. Pointer capture keeps drag events paired with release outside the host. UI callbacks enqueue compact events for the application owner; no direct scene mutation or synchronous UI-thread wait occurs. Focus loss, visibility loss, lost capture and host disconnection enqueue a reset. Listener and capture teardown is accounted for before input context release. An independent page-wide event listener was considered, but would capture unrelated page input and duplicate host lifetime management.

### Control the authored camera from shared demo code

The demo declares optional CoreInput in `portable_rendering_project.json`. A small shared controller locates the authored active camera after scene startup and updates its live transform during application pre-update. It uses camera-local horizontal forward/right vectors for WASD, world vertical for Q/E, normalizes simultaneous movement and scales by bounded elapsed time. Primary-button drag applies yaw around world up and clamped pitch; pointer motion without drag has no effect. Camera UID or component ownership is checked on each use so scene replacement cannot leave a dangling pointer. With no input it writes no transform. This uses the existing scene camera and renderer, with no demo-specific renderer code.

### Extend the packaged graph only when declared

Both the CMake and Python declaration validators accept the base rendering module set or that set plus CoreInput. The source graph adds the required input source set and Windows-only gainput dependency only for the selected module; browser builds use the browser backend and no desktop input binary. Runtime registration names and generated module lists match on both targets. The non-rendering and minimal graphs continue to reject or omit CoreInput according to their existing contracts.

## Risks / Trade-offs

- [Input and delegate run in the wrong order] → Cover the new hook with a focused host test and a camera test that inspects the view after the first input step.
- [Browser UI callbacks outlive their worker service] → Use the browser host's existing ready/closing state, detach listeners and wait for accepted callback work before releasing input state.
- [Web and Windows pointer deltas use different units] → Normalize to CSS/client pixels, then apply one sensitivity rule and test equivalent drag distances at more than one device pixel ratio.
- [Windows gainput update is called twice] → Keep one frame advancement per game step and run native CoreInput regressions alongside portable camera tests.
- [A browser tab resumes after a long suspension] → Use the common host's bounded elapsed time and discard pending motion on visibility loss.

## Migration Plan

Add the optional host hook and CoreInput backend first, then enable CoreInput in the demo declaration and controller. Existing projects remain unchanged because their declarations do not select it. Rollback consists of removing the optional declaration entry and controller; the host hook remains inert without a registered input provider.
