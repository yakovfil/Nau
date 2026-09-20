# Tasks

## 1. Shared minimal kernel selection

- [x] 1.1 Add an explicit common/platform kernel source manifest consumed by NauKernel for the minimal profile; record retained and excluded groups with include/link evidence from application setup, runtime state, services, static modules, work queues, logging, global properties and virtual filesystem construction.
- [x] 1.2 Refine minimal dependency lists only for proven-unused source groups, preserving desktop defaults; verify native Debug/Release builds and the existing minimal lifecycle test before proceeding with platform backends.
- [x] 1.3 Add an isolated core validation CMake entry point reusing production targets/manifests/options and explicit test sources; verify its native graph excludes PlatformApp, rendering and unrelated suites, and SDK checks remain active for its Wasm configuration.

## 2. Platform and value foundations

- [x] 2.1 Add Emscripten platform-header/type selection and remove Windows-only definitions/includes from selected common/static paths; verify wasm32 pointer-width assertions and generated compiler commands, retaining native target selection.
- [x] 2.2 Enable standard C++20 coroutine support through feature detection; verify core task headers compile with both MSVC and pinned Emscripten, and unsupported configurations report an actionable error.
- [x] 2.3 Port required allocation backends and correct target-dependent layout/alignment assumptions; verify allocation, grow/shrink content preservation, supported alignments and cross-thread lifetimes in focused tests.
- [x] 2.4 Supply portable UID representation/generation support preserving canonical text and equality semantics; verify native/Wasm shared fixtures, malformed input rejection, equal-value hashing and concurrent non-null generation.
- [x] 2.5 Provide required core diagnostics and explicit unavailable-host-operation behavior; verify observable error output, fatal subprocess failure, and retained virtual-filesystem/global-property paths without fabricated host results.

## 3. Synchronization and runtime backends

- [x] 3.1 Complete the standard synchronization backend, including Event::reset and header dependencies, and verify fixed storage/alignment assumptions; run auto/manual reset, timeout, atomic/mutex coordination and thread-local cleanup cases.
- [x] 3.2 Implement the required monotonic timer backend with bounded worker resources; verify expiry, cancellation before execution, completion/cancellation races and callback reentrancy without duplicate completion.
- [x] 3.3 Integrate real core runtime, queue and executor disposal with the portable timer backend; verify task suspension/resumption and bounded shutdown with pending work, released captures and terminated owned threads.
- [x] 3.4 Remove native dynamic-loader dependencies from the selected static-module path while retaining production registration; verify a test module registers, initializes and cleans up through the existing static generator and manager.

## 4. Required math and framework compatibility

- [x] 4.1 Validate bundled scalar math and required SoA/extensions, implementing only missing operations used by the selected core; verify representative vector/matrix behavior and alignment with numerical tolerances.
- [x] 4.2 Preserve required string, UID, JSON and math serialization; run shared round-trip/invalid-input fixtures on native and Wasm and verify established representations remain compatible.
- [x] 4.3 Compile the selected shared framework sources against the portable core and platform API headers without creating a placeholder PlatformApp implementation; verify no unresolved compile-time Windows dependency remains and record that browser application linkage is still a separate prerequisite.

## 5. Integrated validation and handoff

- [x] 5.1 Build and execute focused core tests under the pinned SDK Node runtime on a pthread worker in isolated Debug and Release directories; verify bounded process timeouts, nonzero failure propagation and actual Wasm source-built link inputs.
- [x] 5.2 Run focused native core and existing real minimal lifecycle tests in Debug/Release, compile representative affected desktop targets, and audit graphs/commands for source parity and native/browser isolation; record exact commands and any unrelated failures separately.
- [x] 5.3 Update graph-audit expectations, engine build documentation, root prerequisites.md/build.md and minimal-profile source-selection documentation; verify documented commands and distinguish core test success from browser platform/lifecycle/package acceptance.
- [x] 5.4 Review every specification scenario, validate OpenSpec artifacts and record concrete target names, source revision/working-tree status and evidence for emscripten-build; leave any unverified scenario or downstream browser prerequisite explicitly pending.
