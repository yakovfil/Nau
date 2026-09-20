# Proposal

## Why

The selected minimal application currently links the full rendering framework,
so Emscripten build integration cannot select a non-rendering runtime. A shared
minimal framework with native lifecycle validation is the next prerequisite.

## What Changes

- Add an opt-in minimal runtime profile with explicit bundled dependency and
  module lists, a dedicated `NauFrameworkMinimal` target, and native Windows presets.
- Compile the existing application/service/work-queue/main-loop lifecycle sources
  for the minimal framework while excluding scene, Graphics, UI, VFX and ImGui
  integration, default rendering delegates and content configuration helpers.
- Preserve platform-window services and existing static module registration;
  explicitly select the minimal entry point and keep the desktop sample valid.
- Add focused native tests for real application creation, initialization, steps,
  service availability, and orderly shutdown, plus graph exclusion checks.
- Preserve existing desktop presets and full-framework behavior.

## Capabilities

### New Capabilities

- `minimal-runtime-profile`: A non-rendering shared Nau framework and explicit
  source dependency/module selection, validated with the real native lifecycle.

### Modified Capabilities

None. The in-progress `emscripten-build` change consumes this capability.

## Impact

Changes belong to NauEngineLite framework internals, existing CMake selection,
minimal sample and focused tests. Keep public application APIs and desktop
defaults compatible. No renderer, editor, NauDemo or unrelated submodule changes.
Browser platform services, Wasm core portability, browser scheduling and delivery
remain separate work; a successful native profile does not claim a Wasm port.
