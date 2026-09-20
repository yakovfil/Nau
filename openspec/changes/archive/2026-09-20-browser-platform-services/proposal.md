# Proposal

## Why

The minimal Nau core now passes threaded Wasm tests, but PlatformApp supplies only
Windows implementations. A real browser window service is the next prerequisite
for linking and running the shared non-rendering framework in the browser.

## What Changes

- Register a browser implementation of the existing PlatformApp module and window
  interfaces through production static module/service discovery.
- Represent one window with a page-provided DOM element, as confirmed during
  exploration. Require that element to exist; explicitly reject additional windows.
- Provide real CSS-pixel geometry, element visibility and separate document
  visibility state without creating a graphics context.
- Preserve the platform-service worker and provide a wakeable executor/message
  pump, browser UI-thread dispatch, explicit initialization failure and orderly
  service disposal with outstanding work accounted for.
- Define diagnostics for unavailable desktop operations and expose browser state
  needed by subsequent lifecycle work without implementing application cadence.
- Add focused real-browser platform validation and preserve native lifecycle tests.

## Capabilities

### New Capabilities

- `browser-platform-services`: A statically registered, non-rendering browser
  PlatformApp service with one DOM-backed window, thread-safe dispatch and
  observable initialization/disposal behavior.

### Modified Capabilities

None. There are no durable specifications; completed minimal-runtime-profile and
wasm-core-portability changes provide the existing implementation foundation.

## Impact

Implementation belongs in NauEngineLite's platform_app module, narrowly required
shared PlatformWindowService integration, platform test/build helpers and docs.
Reuse the existing interfaces, kernel executors, diagnostics, emsdk 6.0.9 and
recorded dependencies. Preserve Windows behavior and avoid breaking existing
public window signatures.

A small browser test fixture and local isolated serving support are permitted
for platform acceptance; the deliverable application page/server and package
relocation acceptance remain in minimal-web-delivery-validation. Approximately
10 Hz stepping, stop controls, background/resumption scheduling and application
startup-result policy remain in browser-runtime-lifecycle/minimal-app-web.
No renderer, GPU context, input-system port, multiple windows, desktop browser
chrome manipulation, editor or NauDemo work is included. This change does not
complete the remaining emscripten-build application/package tasks.
