# Design

## Context

See proposal.md for motivation. The existing sample calls createApplication,
startupOnCurrentThread and step with a 100 ms sleep. ApplicationImpl starts in
Active, ignores startupServices errors and requires an initialized main loop for
normal stepping and stop. Its creation helper can return null after partial setup.

ServiceProviderImpl discards already-ready independent initialization tasks and
does not consistently propagate errors from pending independent tasks. Shutdown
has similar omissions, and a dependent shutdown error can skip later disposal.
The browser platform fixture directly tests its service result, so it does not
cover this application-wide failure path.

The kernel has worker queues, timers and cooperative tasks, but arbitrary executor
invocations have no rejection/cancellation API. PlatformApp supplies a real browser
window, readiness, document visibility and disposal; its UI proxies require a
responsive browser thread. Existing native minimal tests exercise successful
application startup, updates, stop and destruction.

## Goals / Non-Goals

**Goals:**
- Reuse shared application/service lifecycle code with explicit phase results.
- Keep application ownership on one worker and browser controls asynchronous.
- Separate game-step deadlines from executor and cleanup progress.
- Make failures terminal for this page instance while retaining safe ownership
  until cleanup actually completes.

**Non-Goals:**
- Recreating the runtime in-page, including after an ordinary completed stop.
- Forced destruction of suspended coroutines, worker termination as clean shutdown,
  or guaranteed cleanup after browser/process termination or a fatal Wasm trap.
- Product page design, selected sample adaptation, packaging or rendering.

## Decisions

### Checked shared lifecycle instead of a parallel browser application

Introduce an additive checked creation/startup/control contract implemented by
ApplicationImpl. Keep existing Application virtual signatures intact; legacy
startup delegates to shared logic and diagnoses failure, and subsequent legacy
step must not enter an uninitialized main loop. Browser code consumes the checked
path, whose result includes the failing phase and diagnostic. Do not merely
inspect window readiness: unrelated services can also fail.

Track creation, service preInit/init, running and cleanup phases explicitly.
Creation failure must unwind already-created diagnostics, services, modules and
runtime ownership instead of returning null with unfinished global state.
Startup progress must remain pumpable so the application worker can receive Stop
while a service initialization task is pending. A blocking legacy adapter may
pump this same progress path; the browser UI never waits on it.

Alternative: changing startupOnCurrentThread from void to Result would break
existing implementations/callers. A browser-only replacement application would
duplicate the lifecycle and leave shared errors unresolved. The additive path
avoids both while intentionally correcting shared failure handling.

### Service results and partial cleanup

Retain and inspect all returned initialization tasks, including already-ready
ones. For an independent batch, settle all started tasks and collect their errors
before advancing; do not start dependent phases after prerequisite failure.
Preserve dependency ordering and report the first error plus additional diagnostics.

Record which objects exist and which lifecycle phases succeeded. Cleanup calls
shutdown hooks only for services that completed initialization, in reverse
dependency order, and disposes all instantiated services, including partially
initialized ones. A shutdown/disposal error is recorded but must not prevent
cleanup of other eligible services. Wait for started tasks before releasing their
objects. Reuse existing disposal interfaces and prevent duplicate disposal from
application and runtime-registry paths where ownership overlaps.

Stop during startup latches cancellation intent, prevents new initialization
phases and prevents transition to Running. Allow already-started tasks to settle;
use cooperative cancellation only where an existing API supports it. A generic
forced task-cancellation facility is neither available nor needed for this scope.

### Browser driver and status bridge

Provide a reusable browser driver callable from the eventual selected entry point.
The lifecycle fixture invokes this driver with real application/module/service
setup; minimal-app-web will later connect it to app_sample_main_min.cpp.
PROXY_TO_PTHREAD remains the execution model. Retain platform and background
workers, and marshal all page operations to the UI thread.

Publish snapshots containing state, completed game-step count, diagnostic phase
and message, cleanupComplete and a monotonically increasing sequence number.
Use Starting, Running, Stopping, Stopped and Failed. A failure publishes Failed
promptly with cleanupComplete=false, and updates that flag only after cleanup.
An ordinary Stop reaches Stopped only when cleanup is complete. Once failed, the
state never changes to Stopped or Running; retry requires reload, as confirmed.

The page-facing Stop request sets thread-safe intent and wakes the driver without
acquiring application ownership or waiting for completion. Requests before ready,
during cleanup and after completion are idempotent. Bridge callbacks use a lifetime
token/generation and immutable snapshots so delayed delivery cannot access a
destroyed application or overwrite a newer status. Remove owned callbacks only
after final status delivery is accounted for.

### Cadence and background behavior

Use a monotonic 100 ms nominal deadline. The first game step follows successful
startup; no startup work is counted as a game step. Wake the worker for executor
work or Stop as well as deadlines, and service those wakes without producing an
extra game step. Use existing work-queue notification facilities, with narrowly
required wake integration rather than a separate queue implementation.

Advance deadlines normally when on time. If delayed, skip missed deadlines and
schedule from current time rather than replaying them. Hidden tabs continue on a
best-effort basis; no hidden-tab frequency is guaranteed. Consume document
visibility from the platform service. Reset the timing baseline when returning
to visible and after a detected long scheduling gap.

Proposed timing default: game-step elapsed time is nonnegative and capped at the
nominal 100 ms interval, so a suspension is not converted into a huge simulation
update even when no extra steps are emitted. Use actual elapsed time below that
cap. This is browser-driver policy, not a change to native desktop timing.

Alternative: requestAnimationFrame on the UI thread introduces display cadence
and UI ownership; unconditional sleep_for delays Stop and queue progress. The
worker deadline loop fits the agreed non-rendering 10 Hz runtime.

### Stop, failure and cleanup progress

On Stop or a reported recoverable runtime error, stop scheduling new game updates
and drive shared cleanup promptly, without the normal 100 ms cadence delay.
An update already executing can finish; callbacks must cooperate by returning.
Provide cleanup progress independently of game updates rather than using the
existing shutdown branch that can continue mainGameStep while waiting.

Native scene updates install their own update executor and also use a post-update
queue. Suspended component work can capture those executors, so polling only the
application queue during shutdown can strand continuations. Extend the internal
scene/main-loop lifecycle with a cleanup-only pump for both scene queues. Run it
on the owning application thread while scene shutdown is pending, preserving and
restoring the appropriate executor context. It may resume work already started
before Stop, but must not invoke the normal game/component update traversal or
start a new update. Retain scene/component ownership until that work settles.
This native compatibility extension does not add scene dependencies to the
minimal browser runtime or change native running-state timing.

Validate the extension using the real native scene lifecycle: start a controlled
asynchronous component update, request Stop while it is suspended, release its
pending work after Stop and drive cleanup without game updates. Assert the
continuation completes, cleanup finishes, and game/component update counts do
not advance after Stop. Run this regression in Debug and Release alongside the
existing minimal lifecycle tests; queue-only substitutes do not establish scene
integration correctness.

Treat platform host loss as a reported runtime failure. Retain the original
diagnostic while collecting cleanup errors. Do not claim every exception or trap
is recoverable: expose an observed fatal runtime abort as Failed with incomplete
cleanup; do not call back into a corrupted/aborted Wasm runtime to fake cleanup.

Use a configurable lack-of-progress deadline, default 10 seconds of observable
foreground time for this milestone. On expiry, report Failed with an identified
phase and cleanupComplete=false. Keep necessary owners alive and continue safe
cooperative cleanup if work later settles. Do not free live task contexts or mark
Stopped merely because a timeout elapsed. Reset/suspend this deadline while the
page is hidden to avoid treating browser suspension as proof of an engine failure.
A main-thread status watchdog can report absent worker progress, but cannot
guarantee recovery from non-returning synchronous code.

### Acceptance integration

Extend the existing isolated Chrome fixture infrastructure with an independent
lifecycle build target linking the real shared application and production static
PlatformApp. Inject controlled services for immediate/deferred initialization
failure, delayed startup, shutdown failure and pending work; these are test inputs,
not substitutes for the application or platform backend.

Run Chrome Debug/Release with real visibility transitions (Playwright focus
emulation disabled), UI heartbeat/control checks, step timestamps/counters and
cleanup assertions. Normal foreground acceptance is 8–12 completed steps/second
over a five-second unloaded interval. Deterministic clock/deadline tests verify
missed-deadline skipping and the elapsed-time cap without depending on OS timing.
Test stalled cleanup with a short injected threshold, then release the pending
work and verify eventual cleanup without changing Failed into success.

Run native service failure tests, existing minimal lifecycle tests and browser
platform/core regressions affected by shared lifecycle changes. Include the
native pending-scene-update shutdown regression in Debug and Release. Keep production
browser sample/preset and relocation acceptance pending in their owning changes.

## Risks / Trade-offs

- Shared error propagation changes previously silent behavior -> regression-test
  immediate/deferred failures and dependent ordering on native and Wasm targets.
- Partial initialization and rejected shutdown tasks can skip disposal -> track
  lifecycle phases and continue cleanup while aggregating errors.
- Non-returning callbacks cannot be cooperatively cancelled -> report incomplete
  cleanup and retain ownership; page reload is the user recovery boundary.
- Browser suspension makes wall-clock deadlines unreliable -> use visibility-aware
  progress deadlines and deterministic scheduling tests.
- Delayed page callbacks can outlive application state -> lifetime tokens, ordered
  snapshots and explicit final delivery/teardown accounting.

## Migration Plan

Add checked shared APIs and regression coverage first, then the browser driver and
fixture. Existing successful native callers continue using the same signatures.
Document corrected failure behavior and the browser driver's integration contract
for minimal-app-web. Roll back driver/fixture separately if needed; retain shared
error fixes only with their tests and compatible legacy adapter. Update build and
dependency documentation after implementation validation; leave application
packaging guards and unrelated desktop build issues in their owning work.
