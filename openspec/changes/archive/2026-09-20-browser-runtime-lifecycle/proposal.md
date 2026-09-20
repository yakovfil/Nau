# Proposal

## Why

The Wasm core and production browser platform services are validated, but the
application still discards startup errors and has no browser lifecycle driver.
The next milestone must run the real shared application safely on a worker and
make startup, stepping, failure and orderly stop observable.

## What Changes

- Add a worker-owned browser lifecycle driver with observable status, completed
  step count, diagnostics and an asynchronous stop request interface.
- Preserve the agreed nominal 100 ms cadence, with wakeable waits, best-effort
  background execution and resumption without accumulated catch-up steps.
- Correct shared service initialization/error aggregation and provide a checked
  application startup path, including cleanup after partial creation/startup.
- Support Stop during startup or execution, cooperative cleanup of pending work,
  and explicit reporting of cleanup errors or lack of progress.
- Preserve native scene shutdown progress with a cleanup-only continuation queue
  pump and regression coverage for asynchronous updates pending at Stop.
- Apply the confirmed failure policy: clean up, report Failed and require a page
  reload to retry. In-page restart is outside this milestone.
- Validate actual application lifecycle behavior in Chrome Debug/Release and run
  affected native lifecycle/service regressions.

## Capabilities

### New Capabilities

- `browser-runtime-lifecycle`: Observable worker-based application startup,
  approximately 10 Hz stepping, cooperative stop, failure handling and cleanup.

### Modified Capabilities

None. No durable capabilities exist in openspec/specs. The completed minimal
runtime, Wasm core and browser platform changes provide the implementation base.

## Impact

Changes belong in NauEngineLite's shared application framework, narrowly required
kernel application/service lifecycle APIs and aggregation, browser lifecycle
support, focused tests/build helpers and documentation. Include narrowly required
native scene-module/internal main-loop lifecycle changes to pump pending scene
continuations during cleanup without starting new game/component updates.
Include the approved two-line native kernel source-selection prerequisite so the
Windows scene regression can build without compiling Emscripten sources.
Preserve existing public
Application signatures through additive checked interfaces and legacy adapters;
native successful lifecycle behavior remains supported. Failure propagation is
an intentional correction in shared code and requires native regression coverage.

Reuse SDK 6.0.9, production static PlatformApp registration, the minimal runtime
dependency graph and existing Chrome test infrastructure. A focused lifecycle
fixture may expose test controls and status to validate the driver. Adapting the
selected sample app_sample_main_min.cpp and its user-facing controls belongs to
minimal-app-web; package staging and relocatable hosting belong to emscripten-build
and minimal-web-delivery-validation. This change supplies their lifecycle API and
acceptance evidence without marking application/package tasks complete.

No renderer, GPU, input port, editor, NauDemo, in-page restart, generic forced
coroutine cancellation or repair of unrelated desktop build failures is included.
