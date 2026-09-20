# Tasks

## 1. Production backend and acceptance fixture

- [x] 1.1 Add Emscripten PlatformApp source selection and production module registration, preserving the Windows branch; verify the browser module compiles and static module generation includes PlatformApp exactly once.
- [x] 1.2 Add the focused browser platform test build using the production module, kernel and shared platform service; verify a link succeeds without the core probe's header-only runtime substitute or renderer dependencies.
- [x] 1.3 Add a test page, isolated local serving and Chrome runner with structured results and a bounded timeout; install any missing test dependencies and verify pthread isolation plus a deliberate fixture failure are reported correctly.

## 2. DOM-backed window

- [x] 2.1 Implement host configuration, default selector and single-window binding; verify valid-host identity, missing/ambiguous/non-HTMLElement failures and extra-window rejection in the browser fixture.
- [x] 2.2 Implement UI-thread DOM dispatch and CSS-pixel size operations; verify worker-origin mutation/read ordering, padding/border handling, page constraints, external resizing and device-pixel-ratio independence against real DOM measurements.
- [x] 2.3 Implement element visibility and separate document visibility status; verify hide/show preserves layout, ancestor display restrictions apply, and a real browser document visibility transition is observed independently.
- [x] 2.4 Implement accessible naming and documented unsupported desktop positioning; verify label changes, unchanged document title/layout, position fallback and diagnostics, and confirm no graphics context is requested.

## 3. Executor and service readiness

- [x] 3.1 Implement the service worker's wakeable executor/message pump and proxy-queue progress; verify idle enqueue executes exactly once, nonblocking pumping returns, and processing limits return under continuing producers.
- [x] 3.2 Add the optional readiness/status contract and integrate it into shared PlatformWindowService without changing public window signatures; verify readiness is delayed until DOM/executor setup succeeds and browser manager absence produces a service initialization error.
- [x] 3.3 Implement initialization failure propagation and partial-resource cleanup; inject a failure after resource allocation and verify the service result settles, its diagnostic is captured, and no worker or callback remains active.

## 4. Shutdown and host lifetime

- [x] 4.1 Implement host-detachment failure reporting without rebinding; verify removing the host updates status, emits a diagnostic and permits safe disposal.
- [x] 4.2 Implement closing/closed transitions, idle wake-up, callback detachment and in-flight proxy accounting; verify idle and repeated disposal finish within the fixture deadline without deleting the host or joining from the UI thread.
- [x] 4.3 Account for accepted executor work during shutdown and make retained references safe; verify queued/in-flight work completes or settles through supported cancellation, late window calls diagnose rejection, and releasing executor references after disposal causes no callback into freed state.

## 5. Integrated validation and handoff

- [x] 5.1 Run the full production browser platform acceptance suite in Debug and Release with emsdk 6.0.9 and Chrome on Windows; record commands, versions, results and diagnostics in this change's validation.md, covering every specification scenario.
- [x] 5.2 Run existing native minimal lifecycle tests in Debug and Release and compile representative desktop NauFramework/PlatformApp targets; record passing results or resolve regressions before marking complete.
- [x] 5.3 Run the affected Wasm core regression suites in both configurations using the SDK Node runtime; record results and confirm browser acceptance is separately satisfied by Chrome evidence.
- [x] 5.4 Update prerequisites.md with required tools, SDK and browser-test dependencies, then update build.md and engine platform documentation with tested commands and browser window semantics; verify all commands and paths match the recorded runs.
- [x] 5.5 Update the emscripten-build handoff to identify the completed platform prerequisite and remaining lifecycle/application/delivery tasks; verify no application/package task is marked complete without its own evidence and run strict OpenSpec validation for affected planning artifacts.




