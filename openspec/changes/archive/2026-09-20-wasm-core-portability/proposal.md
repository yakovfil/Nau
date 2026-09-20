# Proposal

## Why

The shared minimal framework passes native lifecycle tests, but its kernel still
selects Windows headers and runtime facilities. Porting the required core is the
next prerequisite for executing that same framework under Emscripten.

## What Changes

- Define an explicit minimal kernel source selection shared by native and Wasm
  configurations, with platform-specific backends. Exclude only proven-unused
  features and their dependencies; preserve existing desktop defaults.
- Support wasm32 platform types, C++20 coroutines, allocation/alignment,
  identifiers, diagnostics, synchronization, execution queues and core timers.
- Preserve real service/runtime infrastructure and required math, string and
  serialization behavior; do not substitute mocks or disable required operations.
- Provide isolated native/Wasm core test configurations using the existing
  pinned SDK and source-built dependencies, independent of browser window services.
- Validate behavior, source/link boundaries and native regression in Debug and
  Release, documenting what remains for browser integration.

## Capabilities

### New Capabilities

- `wasm-core-portability`: The core required by the minimal runtime can compile,
  link and execute focused behavioral tests on wasm32 with threading enabled.

### Modified Capabilities

None. No durable specifications exist. This refines the completed but unarchived
minimal-runtime-profile implementation, whose design retained the entire kernel.
The user explicitly approved narrowing that source selection while preserving
its real lifecycle and native acceptance requirements.

## Impact

Implementation belongs in NauEngineLite kernel source/platform selection,
minimal dependency lists, required framework compatibility points and focused
tests. Reuse recorded bundled revisions and emsdk 6.0.9, including the approved
fmt fix. No SDK upgrade or new system dependency is proposed.

Browser window/DOM services, application scheduling and stop controls, full
application packaging, Chrome delivery acceptance, rendering, editor and NauDemo
remain outside this change. Core tests must not require those missing capabilities.
