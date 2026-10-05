# Design

## Context

See proposal.md for motivation. This is a cross-repository lifecycle/API change, so a design is required.

The desktop `run_application.cpp` implements `ApplicationDelegate` and a `DelegateLoop` that calls `onApplicationStep()` from `IGamePostUpdate`. It uses the blocking native application loop. Minimal and scene profiles omit this source. Browser applications instead register services through `ApplicationInitDelegate` and call `runBrowserApplication()`; its cooperative mode allocates a persistent browser loop, hands control to Emscripten, then explicitly destroys the loop before process exit. The borrowed delegate API currently requires the caller to provide persistent storage.

`MainLoopService::doGameStep()` invokes pre-update services, the optional scene manager update, then post-update services. This ordering does not imply GPU completion or completion of asynchronous component work. Its current startup-task readiness check checks readiness, not successful completion, which must not become the new host's startup-success contract.

NauDemo native code derives from `SampleAppDelegate` and does rotation/text in the legacy callback. Browser `DemoService` performs startup, rotation/text in pre-update, drawing in post-update, and lifecycle polling/shutdown. Renderer polling must continue while startup and cleanup are pending. Native text startup waits for presentation, so an indiscriminate ban on all engine presentation work during startup could deadlock it.

The durable `naudemo-web` spec still describes a nominal 100 ms cadence, whereas the implemented demo explicitly selects cooperative frame-driven updates. Its delta records the existing behavior. The default non-rendering browser cadence remains unchanged.

## Goals / Non-Goals

**Goals:**
- One owned application-delegate path over the existing application/service lifecycle, with explicit pre/post callbacks.
- Common API headers and implementation usable without scene or graphics types; optional feature integration stays in existing profile wiring.
- One demo entry point and one implementation of rotation/text updates, with CMake-selected demo adapters for configuration and presentation.
- Deterministic lifetime and failure handling under browser event-loop handoff and partial startup.

**Non-Goals:**
- A generic scene renderer, native/browser material parity, generic asset packaging, or removal of all platform code from NauDemo.
- Removing the existing borrowed low-level browser runner, converting all samples, or changing default minimal runtime cadence.
- Making post-update a barrier for async scene work or GPU rendering.
- Moving concrete module dependencies into the kernel or broad restructuring of the existing framework build profiles.

## Decisions

### 1. Extend ApplicationDelegate and retain the existing runner overload

Add `onApplicationPreUpdate(std::chrono::milliseconds)` and `onApplicationPostUpdate(std::chrono::milliseconds)`. The pre callback defaults to no-op. The post callback defaults to calling the existing virtual `onApplicationStep(dt)` once. A delegate overriding the new post callback replaces that default; it can explicitly call the base implementation if it also wants the legacy behavior. The host never separately dispatches the legacy method.

Preserve `runApplication(ApplicationDelegate::Ptr)` and add an options overload for platform-neutral scheduling choices, with at least the existing/default cadence and presentation-driven execution. Existing native callers retain their scheduling. The browser default retains the minimal fixed cadence; NauDemo explicitly selects presentation-driven execution through shared application configuration. On native this mode uses the existing native loop/presentation policy, without promising browser-style display synchronization.

The runner accepts ownership by value. Common headers must not include Emscripten, renderer or scene APIs. Existing configuration, module-list, service-registration and asynchronous startup hooks remain the starting contract. Support static module lists as well as existing dynamic native loading without double registration.

Alternative: introduce an unrelated application class and runner. Rejected because it duplicates the current public lifecycle contract and makes sample migration larger. Alternative: replace the old step callback with pre-update. Rejected because it changes existing delegates' timing silently.

### 2. Share delegate adaptation; isolate only scheduling and platform startup

Extract the delegate adapter from desktop-only `run_application.cpp` into common framework sources compiled in full, scene and minimal profiles. Remove incidental unused feature includes rather than widening dependencies. Native and Emscripten runner implementations invoke this adapter and the real checked lifecycle. Window service creation remains through existing platform support; native-only visibility/setup stays in the native implementation.

Dispatch application pre/post callbacks inside their matching main-loop phases after application startup succeeds and while the application is not closing. Each eligible phase is dispatched once per step. Do not promise an ordering among unrelated services within the same phase. Check eligibility again before post-update so a pre callback that requests Stop cannot cause a new application post callback or demo draw submission.

No scene manager is required: a non-rendering host still has both callbacks, with no scene update between them. Real scene integration tests verify the enclosing order when a scene manager is present.

Alternative: keep two complete delegate adapters behind a common function name. Rejected because startup gating, callback dispatch and compatibility would diverge again.

### 3. Treat delegate startup as checked host readiness

After core/service initialization, invoke the initialized notification once, then begin `startupApplication()` once if Stop has not been observed. A pending delegate startup is part of host startup, not proof of Running. Await its result and retain its diagnostic; task readiness alone is insufficient. While it is pending, pump necessary executors and lifecycle/presentation services, including browser polling, without application update callbacks or incrementing completed application steps. Do not depend on pre/post application callbacks to finish startup.

Coordinate this host-readiness state with the existing lifecycle and browser status publisher so `Running` is not published prematurely. Existing service failure aggregation remains authoritative. Stop latches through pending startup, prevents later startup actions and callbacks, and settles or cooperatively cancels accepted work before freeing it. Preserve partial-resource disposal and existing progress-deadline behavior. The host must not create a second independent shutdown state machine.

Native exit returns zero for an orderly stop and nonzero for checked startup/runtime/cleanup failure. Browser immediate creation failure returns failure; cooperative execution completes via existing terminal status and final runtime exit code. Do not imply that the C++ runner returns synchronously with the eventual browser result.

Alternative: publish Running at core-service readiness and merely skip callbacks until the delegate task finishes. Rejected because it misreports failed or stopped startup as a running application.

### 4. Make delegate ownership part of the host session

The host session owns the delegate and application, with teardown ordered so the delegate remains alive through application/service disposal and all callbacks that reference it. Transfer ownership into the persistent browser loop/session before scheduler handoff; no stack reference or caller-owned static delegate is required for the common runner. Destroy the delegate exactly once after safe teardown, before final runtime exit. Retain it when unfinished work prevents safe cleanup; a watchdog timeout is not permission to free live state.

Keep the borrowed `runBrowserApplication(ApplicationInitDelegate&, ...)` signature and ownership behavior for existing callers. Share its scheduling, status bridge and cleanup machinery through an internal owned-session path rather than changing a borrowed API to take ownership implicitly.

Alternative: require every browser application to use a static delegate. Rejected because the common owning API would be misleading and difficult to reuse safely.

### 5. Migrate NauDemo with a narrow private adapter

Both builds compile one `src/main.cpp` calling the engine runner with an owned shared demo delegate. Shared demo code owns cube/camera references, text handle, and pre-update rotation/text behavior. The private build-selected demo adapter provides configuration, asset preparation, renderer-specific scene decoration, presentation setup/polling and shutdown. Native sample paths/materials/environment and web package validation/shader choices remain there.

The browser adapter keeps `IBrowserRuntimeService` and service shutdown integration for renderer progress outside game updates. Browser drawing is invoked from the demo's post-update callback after the scene manager call. It must not duplicate the shared rotation/text update via a second registered service. Preserve initialized-frame and text-presentation startup behavior, report text failures consistently, and preserve native failure exit behavior. JavaScript diagnostic publication stays in the browser adapter.

Delete `web_main.cpp` after extracting these responsibilities. Do not add a second platform `main`, relocate complete application implementations unchanged, or reintroduce `NAU_DEMO_TEST_HOOKS`. The adapter is private to NauDemo and is not a new engine renderer abstraction.

### 6. Prove reuse outside NauDemo

Add module-neutral lifecycle/adapter tests alongside existing framework tests. Build a small shared-source host consumer for native and real-browser execution using production platform services; keep its integration wiring in NauEngineModules' probe infrastructure. Scene-dependent phase validation belongs in module-side tests. Fault controls belong in dedicated test fixtures, not NauDemo production sources.

Verify explicit phases, legacy forwarding, startup gating/failures, stop during pending startup, shutdown failure, delegate lifetime after browser handoff and cleanup, and both supported scheduling policies. Reuse existing browser lifecycle probes for responsiveness, visibility and watchdog semantics. Rebuild affected consumers together because the delegate vtable changes.

## Risks / Trade-offs

### Approved desktop cleanup follow-up

Native missing-font rejection after desktop service initialization exposed a runtime-drain stall after Graphics reports shutdown completion, followed by repeated null-executor assertions. The user approved repairing this cleanup path within this change on 2026-10-05. The cause is an accepted window resize queued on GraphicsImpl's pre-render executor: an immediate startup rejection can enter render shutdown before the next normal frame polls that executor. Graphics shutdown must drain accepted render operations on its worker before releasing resources, preserving errors from that drain. Keep native font validation in checked application startup. Any necessary kernel/feature lifecycle repair is included in scope; preserve the normal rendering behavior and add a focused regression for the discovered cause.

- Browser scheduler handoff bypasses normal stack lifetime assumptions -> store ownership in the persistent session before registering the loop and validate destruction order with real browser tests.
- Startup work can require renderer/executor progress -> keep lifecycle polling and required presentation work active while application callbacks remain gated; specifically test native text readiness.
- A completed but rejected task could be mistaken for success -> consume and propagate startup results, including immediate and deferred rejection.
- New delegate phases can cause duplicate legacy callbacks -> use default post forwarding only and test a delegate overriding both interfaces.
- Registration order within a phase is not a synchronization contract -> specify only pre/scene/post ordering and keep cross-phase dependencies explicit.
- Existing unrelated dirty component changes exist -> record baselines and avoid including or overwriting them during implementation.
- Native and browser visuals intentionally differ -> validate each existing appearance without demanding renderer parity.

## Migration Plan

1. Introduce the common API and adapter with native regression coverage, keeping old signatures available.
2. Add the owned browser host path and shared-source probe, preserving low-level callers and default timing.
3. Migrate NauDemo to the shared delegate and entry point; retain its private rendering/configuration adapters.
4. Build and run native and Chrome Debug/Release validation, audit minimal dependency closure, update documentation and record commands/results.
5. If rollback is required, revert the coordinated consumer and framework changes and rebuild both; do not mix old delegate binaries with new framework libraries.
