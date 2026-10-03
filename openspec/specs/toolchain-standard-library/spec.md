# Toolchain Standard Library Specification

## Purpose

Allow Nau and its SDK consumers to use the supported toolchain standard library without EASTL, while preserving required allocation, container, and runtime behavior across native and browser targets.

## Requirements

### Requirement: EASTL-free source and SDK interfaces

Supported engine, editor, sample, demo, and generated-project builds SHALL compile and link without EASTL sources, headers, libraries, or package discovery. Public engine headers and installed SDK interfaces SHALL expose standard-library types or Nau abstractions without an EASTL dependency. The migration SHALL retain the C++20 baseline and the established native and Emscripten toolchain selections.

#### Scenario: Clean source build without EASTL
- **WHEN** a developer configures and builds each supported native and Web profile from clean recorded inputs with EASTL absent
- **THEN** the selected targets compile and link without fetching EASTL or finding it through an old build directory or host installation.

#### Scenario: External SDK consumer
- **WHEN** a generated project or installed sample builds against the relocated migrated SDK
- **THEN** its public headers, exported targets, and linked dependencies require no EASTL installation or source-tree fallback.

### Requirement: Preserved allocation domains and ownership

Migrated containers SHALL preserve their required frame, stack, and pool allocation domains and backing-resource lifetimes. Supported allocations SHALL satisfy requested alignment, avoid size overflow, preserve live values during growth and moves, and return storage to the correct owning allocator. Copy, move, swap, and node allocation SHALL respect allocator compatibility; module boundaries SHALL NOT cause mismatched deallocation.

#### Scenario: Aligned growth and node allocation
- **WHEN** over-aligned values are inserted into sequence and node containers and those containers grow, move, and release storage
- **THEN** every live value remains correctly aligned and intact, and every allocation is released through a compatible owning resource without leaks or invalid frees.

#### Scenario: Distinct resources and module boundaries
- **WHEN** containers are copied, moved, swapped, or destroyed across supported modules or between distinct allocator resources
- **THEN** the operation follows the documented propagation contract, retains the correct resource identity, and does not outlive its backing resource or free through a different allocation domain.

#### Scenario: Invalid allocation request
- **WHEN** an allocation request has an unsupported alignment or overflowing size
- **THEN** the allocation layer rejects it through its documented failure path without returning undersized or misaligned usable storage.

### Requirement: Preserved specialized container contracts

Replacements for specialized containers SHALL preserve the behavior required by migrated call sites: inline capacity, overflow policy, ordering, unique-key or duplicate-key policy, lookup equivalence, bit indexing, column-wise access, bounded callable storage, stable identity where relied upon, intrusive ownership, and cache eviction. The migration SHALL NOT silently substitute heap allocation for required inline storage or owning allocation for intrusive membership.

#### Scenario: Inline capacity and overflow
- **WHEN** a container receives values below, at, and above its configured inline capacity
- **THEN** the inline range performs no backing heap allocation, overflow-enabled containers preserve values while using their designated allocator, and overflow-disabled containers enforce their documented capacity failure behavior.

#### Scenario: Ordered and packed containers
- **WHEN** migrated ordered containers receive duplicate keys and heterogeneous lookups, or dynamic bit containers grow, shrink, and cross storage-word boundaries
- **THEN** ordering, uniqueness, lookup results, and logical bit values match the required pre-migration contracts.

#### Scenario: Intrusive lifecycle
- **WHEN** an externally owned timer or other intrusive node is inserted, removed, cancelled, and destroyed
- **THEN** membership operations preserve node identity and do not acquire ownership or independently allocate or delete the node.

#### Scenario: Duplicate-key containers
- **WHEN** a sorted multi-container receives several comparator-equivalent keys and a caller looks up or erases their range
- **THEN** all inserted entries remain represented until removed, equal-range results include the matching entries, and required ordering is preserved without imposing unique-key rejection.

#### Scenario: Fixed node storage
- **WHEN** a fixed-capacity ordered map inserts up to its inline element capacity, erases entries, and reuses released slots
- **THEN** its node storage remains inline without heap allocation, values are correctly aligned, and insertion preserves references to existing entries as required by its node-container contract.

#### Scenario: Fixed map move and overflow
- **WHEN** a fixed map exceeds its inline capacity under its configured overflow policy or is copied/moved into another container
- **THEN** overflow follows the designated allocation or failure policy, values are preserved, and the destination does not retain storage owned by a destroyed source container.

#### Scenario: Column-oriented rows
- **WHEN** a caller appends, grows, accesses, moves, or erases rows of a column-oriented container
- **THEN** each typed column remains contiguous, corresponding indexes refer to fields of the same row, all column row counts agree after completed operations or recoverable failure, and nontrivial fields are destroyed exactly once.

#### Scenario: Bounded callbacks
- **WHEN** a supported fixed-storage callback is constructed, copied, moved, invoked, reset, or destroyed
- **THEN** its callable remains in bounded inline storage without heap spill, copy/move and empty-state behavior match its documented contract, and unsupported capture size or alignment is rejected rather than silently allocated elsewhere.

#### Scenario: Intrusive reference release
- **WHEN** intrusive resource handles are copied, moved, adopted, converted to const, reset, and finally released
- **THEN** reference counts follow the existing add-reference/adoption contract, moves do not add ownership, and final release invokes the original owner policy exactly once without allocating an independent ownership control block.

#### Scenario: Cache recency and eviction
- **WHEN** cached entries are accessed, touched, updated, inserted beyond capacity, erased, or cleared
- **THEN** recency and eviction follow the existing cache policy, required creation/release callbacks occur at the corresponding transitions, and cached-value references are not used after eviction or destruction.

#### Scenario: Zero-capacity cache access
- **WHEN** a caller requests or inserts a cached value while the cache capacity is zero
- **THEN** the operation reports a fatal diagnostic and terminates before invoking a creation callback or accessing an empty eviction list; empty-state queries, clear, and resizing remain valid.

#### Scenario: Empty move-only callback invocation
- **WHEN** a caller invokes an empty FixedMoveOnlyFunction through its const or non-const overload
- **THEN** it reports a fatal diagnostic and terminates before attempting to invoke a null function pointer, independently of assertions and exception support.

#### Scenario: Retained raw hash-table values
- **WHEN** a retained raw-storage hashed map or set is instantiated with a nontrivially copyable key or mapped value
- **THEN** compilation fails with a contract diagnostic rather than permitting byte-copy ownership corruption; supported trivial values retain lookup, insertion and removal behavior.

### Requirement: Preserved values and exception-free Web behavior

The migration SHALL preserve supported string encoding and conversion behavior, formatting output, identifier equality, and serialized representations of required values. Persistent identifiers or serialized ordering SHALL NOT change merely because a toolchain hash or container implementation differs. Web error paths SHALL remain compatible with disabled exceptions, including diagnostic-plus-empty results for malformed UTF conversions.

#### Scenario: Value compatibility
- **WHEN** representative Unicode strings, identifiers, asset paths, and scene values are formatted and serialized before and after migration on native and Web targets
- **THEN** their documented output and round-trip values agree, including embedded nulls where supported and established numerical tolerances.

#### Scenario: Malformed Web conversion
- **WHEN** checked Web conversion receives malformed UTF-8 or invalid UTF-16
- **THEN** it reports a diagnostic and returns an empty result without partial content or requiring exception support.

### Requirement: Coordinated consumer migration

Migration guidance SHALL identify the source and ABI break and require clean, compatible rebuilds of engine modules, editor, applications, and SDK consumers. Supported public examples and project templates SHALL use the migrated interfaces. The release SHALL NOT claim compatibility with binaries exposing former EASTL types.

#### Scenario: Rebuild a dependent application
- **WHEN** a developer follows the migration instructions for an existing application
- **THEN** the instructions identify affected interfaces and clean rebuild steps, and the rebuilt application uses matching engine, configuration, and toolchain inputs.

### Requirement: Preserved integrated runtime behavior

The migrated native and browser applications SHALL retain existing startup, scene/input behavior, resource discovery, and shutdown contracts. Allocation and container replacements SHALL preserve asynchronous completion, cancellation, and worker/resource disposal behavior.

#### Scenario: Runtime with pending work
- **WHEN** the migrated minimal runtime starts, steps, and stops with pending timers and queued work
- **THEN** completion or cancellation follows the existing contracts, workers terminate, and shutdown completes within the validation timeout.

#### Scenario: Desktop and browser consumers
- **WHEN** migrated samples, NauDemo, and the editor execute their established automated and human acceptance checks
- **THEN** expected scenes, input, project interaction, resource loading, and normal shutdown behavior are retained on the applicable targets.

### Requirement: Reproducible migration evidence

Validation evidence SHALL record repository inputs, toolchain and standard-library identities, commands, actual test counts, and results for affected native static/DLL and Web routes. Known deferred failures SHALL remain distinguishable from new failures and passes. Retiring an EASTL-specific test SHALL retain equivalent coverage for any preserved allocation or container contract.

#### Scenario: Deferred failure accounting
- **WHEN** validation reuses a previously authorized exclusion or replaces an EASTL-specific test
- **THEN** the report identifies the exact exclusion and reason, maps retained behavior to replacement coverage, and does not count excluded, unexecuted, or failing checks as passes.

#### Scenario: Independent reproduction
- **WHEN** a developer follows recorded prerequisites and build instructions from clean inputs
- **THEN** the resulting build uses the toolchain standard library without hidden EASTL dependencies and produces attributable validation results.
