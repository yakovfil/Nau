# Design

## Context

The completed minimal-runtime-profile and wasm-core-portability work provides a
non-rendering framework and a tested threaded Wasm kernel. PlatformApp still has
only Windows implementations. The existing core probe provides a header-only
PlatformAppApi, so its successful compilation is not evidence of a browser service.

PlatformWindowService discovers ICoreWindowManager, starts a dedicated service
thread, calls bindToCurrentThread and pumps messages. Its current readiness signal
does not accommodate asynchronous DOM initialization. Missing implementations are
silently ignored. ApplicationImpl also ignores startupServices errors in its public
startup method; changing that application-wide policy belongs to lifecycle work.

The agreed browser model is one window backed by a page-provided DOM element.
Existing public window signatures must remain compatible with native callers.

## Goals / Non-Goals

**Goals:**
- Supply the production statically registered browser PlatformApp backend.
- Bind exactly one existing host element and expose actual browser window state.
- Keep the service worker, with reliable queue wake-up and browser UI dispatch.
- Make platform initialization failure and disposal observable and testable.
- Validate production platform services in Chrome and preserve native behavior.

**Non-Goals:**
- Rendering, graphics contexts, full input, multiple windows or desktop chrome.
- Application stepping cadence, stop UI, background scheduling or catch-up policy.
- Resolving the public application's ignored startup result in this change.
- Deliverable application packaging, relocatability or removal of the remaining
  emscripten-build lifecycle guards.

## Decisions

### Production backend selection

Add an Emscripten source directory to platform_app and select it through the
existing module CMake machinery. Export the same PlatformApp module identity and
register the browser manager through production module/service discovery. Reuse
NauKernel, PlatformAppApi and the shared PlatformWindowService; do not introduce a
second kernel implementation or a test-only replacement manager. Windows keeps
its existing backend and module exports.

### Host ownership and window behavior

Use a configurable host selector supplied before service initialization, defaulting
to `#nau-window`. This identifier is a proposed default. Resolution must identify
exactly one connected HTMLElement. The page owns the element; the service neither
creates a fallback nor removes it during disposal. The active window has stable
identity for the service lifetime. Additional createWindow requests return an empty
pointer and a diagnostic.

Geometry uses integer CSS pixels: getSize reports the layout border box and
getClientSize reports the client area. setSize requests the outer layout size,
compensating for the element's box model. Layout constraints may clamp that request;
subsequent getters report measured results. Device pixel ratio does not scale these
values. External page layout changes are reflected on subsequent reads.

setVisible changes element visibility while preserving layout. isVisible reports
whether the connected element is eligible for display according to its and its
ancestors' display/visibility state, not occlusion or viewport intersection. A
display:none ancestor can therefore keep it invisible after setVisible(true).
Initial state comes from the page. A separate additive browser status interface
reports document visibility; hiding a tab must not redefine element visibility.

setName sets the host's accessible label, leaving the document title alone.
Desktop positioning is unavailable: setPosition diagnoses an unsupported operation
and leaves layout unchanged; getPosition returns the documented unavailable value
{0, 0}. These semantics are explicitly documented rather than implying a real
desktop location. Removing the host after readiness transitions browser status to
failed, reports a diagnostic and leaves the service disposable without rebinding.

### Thread ownership and execution

Preserve the application worker -> platform-service worker -> browser UI thread
separation. DOM access occurs only on the browser UI thread. Existing synchronous
window operations use short UI proxy calls from workers so that a setter followed
by a getter sees confirmed DOM state. Calls already on the UI thread execute there
directly. Never hold manager/queue locks across UI proxy calls, and never have the
UI thread synchronously wait for service-worker progress or join a worker.

Use the pinned SDK's proxying facilities and explicit queue processing where a
worker is blocked outside the JavaScript event loop. Browser event notifications
enqueue service work and wake its wait primitive. The message pump processes
executor invocations and state notifications; both enqueue and disposal wake an
idle wait. Nonblocking pumps return promptly, and a processing-time limit bounds
queue batches even with continuing producers. This mechanism introduces no
application stepping timer.

Reference: the installed SDK 6.0.9 proxying header and the Emscripten
[proxying API](https://emscripten.org/docs/api_reference/proxying.h.html) and
[pthreads guidance](https://emscripten.org/docs/porting/pthreads.html). In particular,
proxy work must not depend on a worker returning to a JS event loop it never enters.

### Readiness and failure

Add an optional platform initialization/status contract without changing existing
window method signatures. PlatformWindowService awaits that contract when provided
by the browser backend; native binding retains its existing path. Readiness is
resolved only after host validation, callback installation and executor availability.
On failure, settle the readiness task with an error and release partial resources,
wake/finish the worker and join from a worker context. No ready browser manager is
published to consumers before initialization succeeds.

The platform preInit operation must expose missing/ambiguous host and backend
initialization errors, with useful diagnostics. A browser configuration lacking its
manager must fail explicitly rather than taking the current silent no-op path.
Acceptance observes that service result directly. ApplicationImpl's handling of
that result remains a documented dependency for browser-runtime-lifecycle.

### Disposal and outstanding work

Use explicit Initializing, Ready, Closing, Closed and Failed states. Close event
ingress first, remove owned DOM callbacks, and wake the pump. Account for every
accepted executor invocation and in-flight UI proxy operation before releasing
their context: run accepted work or settle it through the existing cancellation
contract, never silently strand awaiting tasks. Reject new window operations with
a diagnostic after closing begins. Retained executor references must remain safe
to release after disposal; they must not resurrect the service.

Wait for in-flight UI callbacks before destroying callback context and release DOM
references without removing the host. Repeated disposal is safe. Partial startup
uses the same cleanup path. Worker joining remains off the UI thread.

### Validation integration

Add a focused browser platform fixture that links the actual production module,
static module registration and shared platform service. It may use a small test
page and local server with isolation headers required for pthreads. It must not
substitute the core probe's header-only PlatformAppApi for runtime acceptance.

Automated Chrome runs in Debug and Release exercise real DOM behavior, worker/UI
dispatch, idle wake-up, initialization errors and disposal races with a bounded
test timeout. Capture structured pass/fail results and diagnostics. Run existing
native minimal lifecycle tests in both configurations and compile representative
desktop framework/platform targets. Node core tests remain useful regression
coverage but do not satisfy DOM acceptance.

## Risks / Trade-offs

- Synchronous DOM proxies can deadlock if UI code waits on workers. Keep proxy
  operations short and lock-free across dispatch, and test worker-origin calls.
- Page CSS can constrain geometry and visibility. Return measured state and
  document these constraints rather than reporting requested values as actual.
- Callback/disposal races can retain or access freed contexts. Track in-flight
  work and test shutdown with queued work and browser events.
- A platform startup error is not yet a public application startup failure.
  Record the service result and keep the lifecycle integration blocker explicit.
- A focused isolated browser fixture adds test tooling. Record its exact dependency
  versions and commands in prerequisites.md and build.md after validation.

## Migration Plan

Implement the backend and optional readiness integration behind Emscripten source
selection, then validate platform fixtures and native regressions. Update build
documentation and the emscripten-build handoff with evidence of platform readiness
and the remaining lifecycle prerequisites. Existing native consumers need no API
migration. Rollback removes the browser backend and optional integration together;
the independent Wasm core work and existing application build guards remain valid.
