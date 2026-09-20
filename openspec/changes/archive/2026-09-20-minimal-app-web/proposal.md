# Proposal

## Why

The real browser lifecycle and platform services are validated, but the selected
minimal sample still uses a native sleep loop and the browser presets stop at an
obsolete prerequisite guard. Connecting the actual sample now gives developers
a buildable browser application and establishes the input for later delivery work.

## What Changes

- Adapt `samples/minimalApp/app_sample_main_min.cpp` to the existing worker-owned
  browser lifecycle, preserving the native sample path and checking module/setup
  failures instead of ignoring them.
- Enable `web-minimal-debug` and `web-minimal-release` to build the actual
  `MinimalAppSample` through the production minimal dependency graph, with exactly
  one main and static threaded PlatformApp registration.
- Expose the existing lifecycle status, completed-step count and asynchronous Stop
  contract through a small sample acceptance harness using a real DOM host.
- Validate the actual sample in Chrome on Windows in both configurations, including
  startup, five-second foreground cadence, UI responsiveness, visibility, Stop,
  cleanup and terminal failure behavior; retain native regression coverage.
- Record build-graph evidence against the overlapping `emscripten-build` tasks
  without marking package, relocation or clean-checkout delivery work complete.

## Capabilities

### New Capabilities

- `minimal-app-web`: Build and execute the selected real minimal sample in the
  browser through the existing lifecycle driver, with observable status and Stop,
  browser preset integration and native coexistence.

### Modified Capabilities

None. The durable spec inventory is currently empty. Related build and lifecycle
requirements remain in their existing change deltas; this change consumes those
contracts rather than redefining them.

## Impact

Affected areas are the minimal sample, top-level/profile/sample CMake integration,
browser preset descriptions/options, sample acceptance helpers and build/prerequisite
documentation. Reuse `NauFrameworkMinimal`, `NauKernel`, production static
`PlatformApp`, `runBrowserApplication()` and SDK 6.0.9. No SDK upgrade, additional
runtime dependency or public lifecycle redesign is proposed.

The user explicitly confirmed enabling the real browser presets with sample
adaptation. Build-graph work is coordinated with `emscripten-build`; complete
runtime staging belongs there. A finished delivery page/server, missing-isolation
delivery UX, relocation and clean-checkout package acceptance remain outside this
change. No renderer, scene, GPU, asset, editor, in-page restart or standalone mock
application is added. The acceptance harness is test infrastructure, not the
delivery package.
