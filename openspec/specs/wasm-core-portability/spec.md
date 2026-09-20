# wasm-core-portability Specification

## Purpose

Provide the real core facilities required by the minimal Nau runtime on threaded
wasm32, with focused executable validation and preserved native behavior.

## Requirements

### Requirement: Explicit minimal core selection
The minimal profile SHALL select an explicit shared set of core sources and
required dependencies with target-specific backends. It SHALL retain all
facilities required by its real services and exclude only proven-unused features.
The desktop profile SHALL retain its existing feature selection.

#### Scenario: Required core is selected
- **WHEN** the minimal core is configured for native Windows or wasm32
- **THEN** its common source selection is shared, its platform backends match the target, and all retained dependencies are built from recorded sources.

#### Scenario: Unused features are excluded
- **WHEN** a source group or dependency is removed from the minimal profile
- **THEN** the exclusion is justified by dependency evidence and both focused core validation and native minimal lifecycle validation remain successful.

### Requirement: wasm32 platform and memory correctness
The selected core SHALL compile and link for wasm32 without requiring Windows
headers, native Windows binaries or x86-only operations. It SHALL support C++20
coroutines and preserve allocation size, alignment, contents and ownership contracts.

#### Scenario: Target width and allocation
- **WHEN** the wasm32 core allocates, grows, shrinks and frees memory using supported alignments
- **THEN** pointers and sizes use the target representation, returned storage meets the requested alignment, and retained bytes survive reallocation without invalid deallocation.

#### Scenario: Coroutine execution
- **WHEN** a core task suspends and resumes through a worker execution queue
- **THEN** it completes with its expected result and releases its captured resources.

### Requirement: Compatible core values and diagnostics
The core SHALL preserve identifier equality, canonical text and parsing behavior,
required string/serialization behavior and required math operations across targets.
It SHALL provide observable diagnostic output and explicit failures for unsupported
host-only operations reachable through retained APIs.

#### Scenario: Identifier generation and round trip
- **WHEN** identifiers are generated concurrently and valid canonical identifier text is parsed and formatted on either target
- **THEN** generated identifiers are non-null and distinct in the test sample, parsed values compare consistently, equal values hash consistently, and malformed text is rejected.

#### Scenario: Required value serialization
- **WHEN** required strings, identifiers and representative math values are serialized and deserialized
- **THEN** their established representation and values are preserved, with documented numerical tolerances for floating-point operations.

#### Scenario: Invalid Wasm UTF conversion input
- **WHEN** a checked exception-free Wasm string conversion receives malformed UTF-8 or an invalid UTF-16 surrogate sequence
- **THEN** it reports a diagnostic and returns an empty result without partial converted content; valid surrogate pairs and target-width wide strings retain their code points.

#### Scenario: Diagnostics and unsupported host operation
- **WHEN** the core reports an error or a retained API requests an unavailable host-only operation
- **THEN** the error is observable without a Windows dialog or fabricated success, and fatal diagnostics terminate the failing test process with failure status.

### Requirement: Threaded synchronization behavior
The core SHALL support real worker synchronization, including mutual exclusion,
atomic coordination, thread-local lifetime and event signaling/reset/timeouts.
Blocking validation operations SHALL execute on workers.

#### Scenario: Event reset modes
- **WHEN** workers wait on auto-reset and manual-reset events, signal them and explicitly reset them
- **THEN** auto-reset releases one waiter per consumed signal, manual-reset remains signaled until reset, and unsignaled timed waits expire without reporting success.

#### Scenario: Concurrent work and thread cleanup
- **WHEN** multiple workers coordinate shared updates and terminate
- **THEN** synchronized results match the expected totals and thread-local resources are released without corrupting subsequent worker state.

### Requirement: Core timers and orderly disposal
The core SHALL provide timers and delayed work that preserve existing completion,
cancellation and disposal contracts. Real runtime initialization and shutdown
SHALL account for outstanding tasks, timers and executors without deadlock.

#### Scenario: Expiry and cancellation
- **WHEN** one delayed operation expires and another is cancelled before execution
- **THEN** expiry completes once, explicit cancellation suppresses the pending callback, and no operation is completed twice.

#### Scenario: Shutdown with pending work
- **WHEN** the core runtime shuts down with queued work and pending timers
- **THEN** pending operations complete or cancel according to their documented contracts, owned workers terminate, and shutdown completes within the validation timeout.

### Requirement: Independently executable core validation
The project SHALL provide isolated Debug and Release core validation for native
Windows and wasm32 using the real selected core. It SHALL NOT depend on a browser
window implementation, renderer or simulated application runtime.

#### Scenario: Wasm core validation
- **WHEN** focused core tests are built and executed with the pinned threaded Wasm toolchain in either configuration
- **THEN** they pass on worker execution with bounded timeouts and report failures through a nonzero process exit, independently of browser application delivery.

#### Scenario: Native regression and coexistence
- **WHEN** the refined minimal profile is built on Windows in Debug and Release
- **THEN** the same focused core contracts and existing real minimal lifecycle tests pass, browser flags do not leak into native targets, and representative affected desktop targets remain buildable.
