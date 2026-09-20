# Design

## Context

See proposal.md for motivation. The engine working tree is based on
52197201e525a584fb9490be22b1d064b0c666e1 with completed minimal-runtime-profile
changes. That profile supplies NauKernel, NauFrameworkMinimal and explicit bundled
dependency/module lists, but kernel/src/CMakeLists.txt still collects all kernel
sources. The user approved replacing this selection for the minimal profile;
desktop defaults and the prior native lifecycle contract remain authoritative.

Observed portability seams:
- utils/preprocessor.h selects Windows platform headers unconditionally; kernel
  CMake defines _TARGET_PC_WIN. UID headers include guiddef.h.
- async/cpp_coroutine.h accepts only _MSC_VER despite the successful SDK C++20 probe.
- threading/event.cpp contains a standard-library backend without Event::reset;
  critical-section storage sizes require target-specific verification.
- RuntimeStateImpl constructs a timer manager and thread-pool executor. The only
  default timer backend uses Win32 timer queues, including cancellation/disposal.
- module_manager.cpp includes a Windows error header even for static runtime.
- application_setup.cpp constructs virtual filesystem/global-property services
  and registers a known-folder resolver; these paths must survive source pruning.
- ModifiedSonyMath offers scalar selection but also includes SoA extensions.
  Existence of a scalar branch does not prove the required math API compiles.
- Kernel tests already cover allocation, UIDs, tasks, runtime state, serialization
  and work queues, but existing CMake enumerates broad suites with native helpers.

## Goals / Non-Goals

**Goals:** Share the minimal kernel's portable source set across targets, supply
real required backends, and demonstrate executable core behavior without requiring
the next browser platform/lifecycle changes.

**Non-Goals:** General filesystem/asset-pack portability, persistent browser storage,
SIMD optimization, dynamic modules, DOM/window integration, application scheduling,
full Chrome lifecycle acceptance, changing SDK/dependency revisions, or reducing
the previous native lifecycle guarantees to make a smaller graph pass.

## Decisions

### 1. Explicit source closure, shared across native and Wasm

Add a minimal kernel source manifest beside NauMinimalRuntime.cmake, consumed by
the existing NauKernel target. List common implementation files explicitly and
select native/Emscripten backend files separately. Keep the desktop glob and
dependency defaults unchanged. Do not create a second kernel implementation.

Start from application creation, runtime state, services, module registration,
work queues, logging, global properties and virtual filesystem construction.
Retain their transitive memory, RTTI, string, messaging, dispatch, serialization
and math dependencies. Record retained/excluded source groups and why each
exclusion is safe. Asset-pack/native disk IO and compression are candidates for
removal only after include/link references establish that they are unnecessary.
Keep required features when that proof fails; never stub them out. Split mixed
source files only where necessary to separate unused platform operations.

This deliberately supersedes the earlier design's whole-kernel choice. Update
its explanatory documentation and graph checks during implementation without
weakening its requirements or rewriting historical validation results.

### 2. Narrow platform backends and data contracts

Introduce Emscripten platform-header selection before generic Unix detection;
derive pointer width from the actual target. Remove Windows-only definitions and
includes from portable/static paths. Use standard C++20 coroutine support with
feature diagnostics instead of compiler-brand gating.

Preserve public allocator APIs, allocation contents, requested alignment and
deallocation pairing. Audit headers, pointer arithmetic and fixed storage sizes
on wasm32; do not infer correctness from x64 tests. Keep UID values 128-bit and
preserve canonical text, parsing, equality and hashing consistency. A portable
generation backend must provide thread-safe generation of non-null identifiers;
UIDs are not being introduced as security credentials.

Provide real core diagnostic output through a portable sink, with observable
fatal failure rather than Windows dialogs or a no-op. Browser-specific console
routing remains a platform-services concern. Required virtual filesystem and
global-property operations stay functional; unsupported host-only folder/IO
operations must report a documented error instead of a fabricated host path.
No general disk, persistence or asset-loading API is added by this milestone.

Confirmed during implementation: retained UTF conversion uses throwing checked
utfcpp routines, incompatible with the Wasm no-exceptions contract. The user
approved checked exception-free Wasm conversion that diagnoses malformed input
and returns an empty result, without partial output. Native throwing conversion
paths remain unchanged. Tests cover malformed UTF-8, invalid UTF-16 surrogate
sequences, valid surrogate pairs and the 32-bit wchar_t representation on Wasm.

### 3. Preserve threaded core semantics

Prefer existing standard C++ synchronization paths, completing missing methods
and explicit header dependencies. Verify auto/manual event reset, timeouts,
atomics, mutex behavior and thread-local cleanup on workers.

Implement an Emscripten-compatible timer backend behind ITimerManager with a
monotonic clock, deadline queue and bounded worker resources. A worker/condition-
variable implementation is the proposed default because it can progress while
the application thread waits; one JS callback tied to that blocked thread would
not preserve the existing semantics. Retain existing task/cancellation contracts:
explicit cancellation suppresses pending callbacks; disposal resolves pending
work according to the current timer contract. Account for callbacks already
running and avoid joining a timer worker while holding a callback-needed lock.

Exercise real RuntimeState, executors and queues through initialization and
shutdown. Keep application cadence, browser visibility/resumption and window
thread dispatch outside this layer. Emscripten blocking operations must execute
on workers, consistent with the existing pthread/PROXY_TO_PTHREAD strategy.

### 4. Required math and serialization, without an optimization mandate

Start with the bundled scalar math path and audit the exposed SoA/extensions used
by selected core code. Preserve required operations and alignment; if this path
is incomplete, implement the narrowly required portable operations rather than
silently removing math values from serialization. Test representative vectors,
matrices, strings, UIDs and JSON round trips. Use numerical tolerances for math;
preserve established text/identifier compatibility. SIMD tuning is deferred.

### 5. Independent core validation entry point

Add a focused CMake validation entry point under cmake/probes/wasm_core (proposed
path). It must reuse production source manifests, NauKernel target definitions,
dependency lists and compile-option helpers. It selects kernel tests without
creating PlatformApp or a fake platform module. Static-module tests can register
a small test module through the existing generator to exercise real registration.

Use isolated native and Emscripten Debug/Release directories. Reuse SDK identity
checks and pthread options. Compile selected shared framework sources as an
additional compatibility check, without claiming to link/run the browser app.
Keep the full browser application guard for still-missing capabilities; allowing
the core test entry point must not bypass SDK checks or imply application support.

Adapt relevant existing GTest cases into an explicit focused list and add missing
semantic regressions. Run Wasm core tests under the pinned SDK's Node runtime,
on a pthread worker, with process timeouts and nonzero failure exits. Native tests
exercise the same core contracts. Node success establishes core behavior only;
Chrome window/lifecycle and hosting acceptance remain downstream work.

## Risks / Trade-offs

- Hidden source dependencies -> combine explicit source review, link closure,
  framework compilation and existing native lifecycle regression.
- wasm32 alignment defects -> test multiple alignments, grow/shrink reallocation,
  pointer-bearing structures and repeated cross-thread allocation lifetimes.
- Timer/disposal races -> test cancellation before expiry, concurrent completion,
  pending-timer shutdown and callback-initiated operations with bounded execution.
- Scalar math gaps -> verify exact required API/serialization cases before pruning
  dependencies; record failures as unresolved work, not unsupported silent paths.
- Narrower minimal API surface -> document exclusions and keep desktop builds
  unchanged; public headers alone do not claim every desktop feature is linked.
- Node/browser differences -> label execution evidence precisely and retain
  separate browser platform/lifecycle acceptance gates.

## Migration Plan

Implement source selection first with native regression, then foundational types
and backends, then focused Wasm execution. Update the minimal profile graph audit
to the justified dependency set and document native/Wasm commands and results.
Handoff concrete targets/source revision to emscripten-build when verified.
Rollback restores the prior minimal source manifest and backend selection;
desktop defaults, external SDK installation and user data are unaffected.
