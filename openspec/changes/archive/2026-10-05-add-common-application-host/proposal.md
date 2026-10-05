# Proposal

## Why

Native and browser applications currently use different high-level delegates and runners, leaving NauDemo with two entry points and duplicated lifecycle wiring. A common engine-owned host will let applications share their entry point and update callbacks while preserving each platform's scheduling and cleanup requirements.

## What Changes

- Extend the existing application delegate/runner API to support native and browser builds, with platform implementations selected by the build.
- Add explicit pre-update and post-update callbacks around the scene manager update; preserve the legacy `onApplicationStep()` callback through the default post-update implementation.
- Own the delegate through asynchronous startup, execution and completed teardown, including browser event-loop handoff; propagate startup and cleanup failures through existing lifecycle reporting.
- Migrate NauDemo to one `main.cpp` and shared demo behavior. Advance rotation and submit text in pre-update; retain browser drawing in post-update.
- Keep demo asset configuration and renderer-specific adapters in NauDemo for this stage. Do not introduce a generic renderer or asset packaging abstraction.
- Align the NauDemo lifecycle requirement with its existing presentation-driven browser cadence and programmatic status/Stop interface; preserve the minimal browser runtime's existing fixed cadence.

## Capabilities

### New Capabilities

- `common-application-host`: Shared delegate, runner, update phases, ownership, failure handling and platform scheduling for native and browser applications.

### Modified Capabilities

- `naudemo-web`: Require a shared demo entry point and pre-update behavior, preserving browser post-update presentation and existing frame-driven timing.

## Impact

- `NauEngineLite/engine/core/app_framework`: public delegate/runner API, common lifecycle adapter, native/browser host implementation, build selection and module-neutral tests.
- `NauEngineModules`: integration/probe builds using production platform services, and scene-dependent phase-order validation. No new scene or renderer dependency in the common host contract.
- `NauDemo`: entry point, shared behavior, platform-specific presentation/configuration sources, CMake and documentation.
- Existing sample delegates remain source-compatible. Added virtual methods require coordinated rebuilding; binary compatibility with previously compiled delegates is not promised.
- Existing low-level lifecycle APIs and `runBrowserApplication()` callers remain supported. No test hooks are reintroduced into NauDemo.
- Approved implementation follow-up: repair the desktop runtime-drain stall exposed by rejected demo startup, including a targeted kernel/feature lifecycle fix if required and regression coverage.
