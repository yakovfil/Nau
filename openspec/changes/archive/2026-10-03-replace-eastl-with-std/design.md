# Design

## Context

See `proposal.md` for motivation and scope. This design is required because the change crosses public APIs, allocation domains, DLL boundaries, renderer/ECS internals, and browser runtime code.

Observed integration points:

- `engine/core/kernel/include/nau/memory/eastl_aliases.h` supplies vector, stack/frame vector, map, and list aliases. Map/list allocator sizing currently depends on EASTL internal node types. `eastl_aliases.cpp` routes requests to array, frame, and stack allocators; several alignment overloads currently ignore alignment arguments. Preservation means satisfying the intended alignment contract, not reproducing this defect.
- `engine/core/kernel/src/memory/eastl_new.cpp` provides EASTL allocation integration; `test_eastl_allocator.cpp` tests alignment, offsets, reallocation, invalid requests, and over-aligned containers. The failure ledger records clang-cl DLL failures in three cases, so this is not a universally passing baseline.
- `nau/string/string.h` wraps tiny_utf8 with standard allocation but exposes EASTL conversions. `format.h` and string utilities contain overloads accepting both standard and EASTL types; merging the types can create duplicate overloads and specializations.
- Renderer and Dagor ECS code uses fixed vectors, sorted vector maps/sets, dynamic bitvectors, custom relocation, and heterogeneous lookup. The Windows timer manager uses externally owned intrusive nodes.
- `kernel_config.h` imports EASTL configuration and force-inline definitions. Both full and minimal CMake graphs list EASTL/EABase, and installed SDK CMake imports EASTL. Editor integration, external samples, demo, and generated templates consume the types.
- Engine `AGENTS.md` and coding guidelines currently prefer EASTL; this conflicts with the new direction and must be updated during implementation. Current specs preserve native/Web behavior but do not require a named container library, so their requirements need no modification.

## Goals / Non-Goals

**Goals:** Make standard facilities the default; keep a small Nau layer only for contracts standard C++20 cannot directly express. Preserve value behavior and explicit storage/lifetime requirements, with migration evidence at each stage.

**Non-Goals:** Binary compatibility with EASTL-based outputs, a general EASTL compatibility namespace, a new third-party container suite, blanket conversion to PMR/default allocation, changing the language baseline, replacing tiny_utf8 or fmt, and unrelated test repairs. Ordinary standard-container growth factors and implementation layout need not match EASTL unless a consumer demonstrably relies on a specific behavior; such reliance must be removed or modeled explicitly.

## Decisions

### 1. Direct standard types with narrow Nau abstractions

Replace ordinary strings/views, sequence and associative containers, algorithms, traits, smart pointers, optional/variant/span, and callable wrappers with standard counterparts. Preserve existing useful Nau aliases with standard-backed definitions. Do not introduce `namespace eastl = std`, add nonstandard names to `std`, or retain copied EASTL implementation under a renamed directory.

Review semantics at each call site: constructors, comparators, transparent hashing, iterator invalidation, moved-from assumptions, and overload resolution. Replace conveniences such as `find_as`, string `sprintf`, and unordered erase explicitly. Keep move-only callable support through the existing Nau facility rather than forcing captures into `std::function`. Implement a small C++20 underlying-enum helper for existing `to_underlying` uses rather than raising the language standard.

Alternative: a broad compatibility shim would reduce initial edits but conceal remaining nonstandard contracts and leave public interfaces misleading.

### 2. Typed allocator adapters preserve resources

Introduce standard allocator adapters over the existing allocation domains. Each supplies typed allocation, checked byte sizing, alignment handling, rebind support, resource identity, equality, and explicit propagation traits. Capture the owning resource where required rather than consulting a different thread's current resource at deallocation. Do not promise resources outlive frame/stack reset; enforce/document the existing lifetime boundary.

For node containers, let standard allocator rebinding select the actual internal node type; pool storage must handle its size and alignment without naming implementation-specific node types. Unsupported backend alignment needs a correct aligned path or explicit rejection, never ignored arguments. If alignment adjustment is necessary, retain enough provenance to release the original block. Separate the low-level allocation failure contract from the typed adapter: an adapter must not return null as successful storage for a nonzero allocation; in exception-free builds use the established fatal diagnostic path when the request cannot be satisfied.

Use non-propagating resource-bound adapters by default, with equality based on resource compatibility; review copy construction and move assignment deliberately. Where a caller requires swap between unequal resources, implement a safe domain-aware operation rather than invoking standard-container swap outside its preconditions. Shared-library allocation resources must expose a compatible allocate/deallocate pair; tests must allocate in one module and release through its originating resource from another.

Alternative: global `std::allocator` or blanket PMR conversion would change frame/pool behavior or resource ownership. PMR may be used locally only where it fits these same contracts, not as the default redesign.

### 3. Specialized containers preserve concrete contracts

| Existing family | Replacement design | Required checks |
| --- | --- | --- |
| Fixed vector/string with inline storage | Focused Nau container with explicit live-object management and designated overflow allocator | No backing allocation within capacity; both overflow policies; alignment; move-only elements; destructor counts |
| Sorted vector map/set | Nau adapter over standard contiguous storage and standard search algorithms | Comparator order, uniqueness, transparent lookup, mutation and iteration semantics |
| Sorted vector multimap/multiset | Extend the sorted contiguous adapters with explicit duplicate-key policy | Preserve all equivalent entries, equal-range results and consumer-required equivalent-key ordering |
| Fixed map | Standard ordered map with a container-owned inline node resource and designated overflow resource | No node heap allocation through inline capacity; node alignment/rebinding; overflow; reference stability; safe copy/move ownership |
| Tuple vector | Nau structure-of-arrays container using standard-backed column storage and coordinated row operations | Contiguous typed columns, identical row counts, index correspondence, alignment, row insertion/erase and nontrivial lifetimes |
| Fixed function | Nau bounded inline callable wrapper with explicit copy/move/invoke/destroy operations | No heap spill, capture size/alignment rejection, copyability, empty-state behavior and single destruction |
| Intrusive pointer | Nau pointer wrapper retaining existing add-ref/release hooks | Copy increments, move transfers, reset/final release invokes the existing owner policy without a separate control block |
| LRU cache | Standard list plus lookup index with explicit recency/eviction operations | Hit/touch/update promotion, bounded capacity, eviction order, callback counts and cached-value lifetime |
| Dynamic bitvector | Nau bit container over standard word storage | Word boundaries, resize and tail masking, existing bit operations and any serialized representation |
| Intrusive list | Narrow Nau non-owning links/list implementation | Stable node identity, unlink/cancel/destruction, no membership allocation |
| Existing Dagor relocatable containers | Retain their role, replace EASTL helpers, audit relocatability declarations | Never byte-relocate a standard string/vector or another nontrivial type merely because its EASTL predecessor allowed it |

Implement only the operations used by repository consumers, with documented contracts. Do not substitute a tree map for a flat container or a heap vector for inline storage. Retain required node/reference stability at call sites; if standard storage has different invalidation rules, update the consumer without changing its external behavior.

The extension approved after the baseline inventory adds the following concrete constraints:

- ECS `template.h` accesses `componentTypes.get<COLUMN>()[row]`; `internal/eventsDb.h` and `internal/archetypes.h` use multiple typed columns. Preserve structure-of-arrays access rather than substituting a vector of tuples. Standard column vectors are acceptable where callers do not depend on a single backing allocation; retain a coordinated single-block storage path if the inventoried consumer requires that allocation contract. Commit a row only after all its fields are constructed; unwind partial construction where exceptions are enabled and keep exception-free failure behavior on Web. Do not expose inconsistent column sizes after a recoverable failure. Pointer invalidation is documented and call sites reacquire column pointers after growth.
- Graphics `daBfg/frontend/internalRegistry.h` and scheduler code use fixed maps. Their resource lives with the container and allocates rebound implementation node types at their actual size/alignment. Handle any standard-library sentinel allocation separately so it does not reduce the promised inline element capacity or introduce a hidden heap allocation. Resource-bound copies/moves rebuild nodes into the destination resource as needed; never transfer nodes whose allocator points into a destroyed source container. This fixed-node map differs from the flat vector-map replacement.
- ECS `ecsQuery.h` and renderer callback signatures use copyable fixed functions. The existing `FixedMoveOnlyFunction` is not a copyable substitute and itself includes EASTL internals; retain a separate copyable bounded wrapper while removing those internals from the existing move-only facility. Reject oversized or over-aligned captures at compile time, preserve supported signature qualifiers and empty-call diagnostics, and do not route fixed functions through potentially allocating `std::function`.
- `dag_resourcePool.h` uses intrusive `LeasedResource` references whose final `Release()` returns an object to its owner pool. Preserve that hook; final release does not necessarily delete an object. Keep adopt/add-reference construction, const conversions and null/self assignment correct. Existing non-thread-safe reference counting remains non-thread-safe; atomic ownership redesign is out of scope.
- `shadersBinaryData.h` uses an LRU cache for decompressed shader groups. Use a stable list to hold entries and a lookup index pointing to them. Preserve the actually used get/touch/insert/update/erase/resize callbacks and promotion rules, including capacity-zero behavior verified against the original implementation. Erase the index before destroying its referenced node. Keep returned spans/references valid for the required consumer lifetime and retain external locking; changing cache concurrency is out of scope.
- ECS acknowledgement tracking and graphics packing use multi-containers. Unique-container duplicate rejection must not leak into these replacements. Record equivalent-key ordering and range/removal behavior from current consumers and exercise duplicate-rich fixtures.

These additions refine the approved preservation goal and introduce no new external dependency or language-version requirement. Baseline observations for these families are part of task 1.3; implementation and focused checks have dedicated tasks before desktop migration. Historical inventory entries marked DESIGN GAP describe the discovery state and are resolved by this extension, not evidence of completed code.

Zero-capacity LRU policy (approved 2026-09-21): construction and resize to zero are allowed as empty states; operations requesting or inserting a cached value at zero capacity report a fatal diagnostic before creation, allocation or eviction. Queries, clear and resize remain usable. This replaces the bundled cache's empty-list access; it does not introduce disabled caching or a new temporary returned-value lifetime.

Alternative: newer standard-library containers do not solve the C++20 cross-toolchain baseline or all overflow/intrusive contracts. Introducing a separate general container dependency would undermine dependency removal.

### 4. Preserve string, hash, and serialization behavior explicitly

Keep tiny_utf8-backed `nau::string`, adapting its conversions to standard views and strings. Consolidate duplicate standard/EASTL overloads and serializers, formatter hooks, and traits. Preserve size-aware handling, embedded nulls where supported, UTF-8/16/wide conversions, and the checked Web diagnostic-plus-empty error path.

Classify hash uses as transient lookup or persistent identity. Standard hashes are acceptable for transient containers with matching equality; stable IDs and serialized hashes keep their existing explicit algorithm. Compare existing serialized fixtures and canonical output across native/Web. Preserve deterministic ordering where output depends on container traversal rather than assuming unordered iteration remains unchanged.

### 5. Coordinated public API cutover and complete dependency removal

Public types change directly, with migration notes and full rebuilds of all consumers. Reuse the supported VS 2026 environment for MSVC/clang-cl and the pinned Emscripten environment; record actual standard-library versions used. Do not mix old/new libraries or Debug/Release runtime settings across DLL interfaces.

After consumer migration remove EASTL sources, CMake targets and transitive definitions, natvis, browser debug-break hooks, exported SDK imports, preset settings, and EASTL allocator entry points. Replace any still-needed platform macros locally. Audit EABase independently because it can have non-EASTL consumers. Retain it with an explicit dependency justification if needed. Touch other bundled dependencies only for demonstrated EASTL coupling, preserving their licenses and avoiding unrelated upgrades.

A final tracked-source/build-interface audit includes optional/inactive engine code and dependency integration, not only the minimal profile. Historical archive text and third-party attribution can retain explanatory EASTL mentions; active code, exported interfaces, and build configuration cannot retain a dependency.

## Risks / Trade-offs

- [Large coupled edit] -> Migrate in dependency order with separate checkpoints; transitional EASTL may remain until the final cutover, but partial removal is not completion.
- [Resource propagation or alignment defect] -> Instrument resource identity, aligned allocation and paired release; test rebinding, unequal-resource moves, frame/thread lifecycle, and real DLL boundaries.
- [Changed inline allocation or relocation behavior] -> Assert allocation counts and object lifetimes around capacity boundaries and exercise renderer/ECS workloads. Record representative allocation/timing baselines; investigate regressions without inventing an unmeasured performance guarantee.
- [Serialization drift] -> Preserve stable hash algorithms and compare pre/post fixtures, including Unicode and iteration-dependent output.
- [Exceptions disabled on Web] -> Compile and run replacements with actual exception-free flags; exercise explicit diagnostics in isolated processes where fatal behavior is expected.
- [Old test failures obscure regressions] -> Retain exact exclusions and their history in `failed-tests.md`. Port preserved allocator coverage before removing obsolete EASTL tests; a renamed or removed test is not proof of a fix. Unpassed acceptance remains reported as such under the user's existing deferral instruction.

## Migration Plan

1. Capture reproducible pre-change inputs and focused baselines for allocation, strings/serialization, specialized containers, and runtime checks. Refine the existing scan into a symbol-to-replacement inventory including optional targets and externally bundled consumers.
2. Implement and test allocator adapters and specialized Nau containers alongside existing code.
3. Migrate kernel APIs, string/serialization integration, and minimal runtime; validate native and Web focused core/lifecycle checks.
4. Migrate renderer/ECS and other desktop modules, tools, editor integration, samples, demo, and templates. Rebuild the entire consumer set using matching inputs.
5. Remove the dependency and exports; validate clean builds and installed/relocated SDK consumption without EASTL. Update guidelines and migration instructions.
6. Run the integrated matrix and record actual results, failure exclusions, fresh-checkout evidence, and human visual acceptance obtained for the new binaries.

Validation matrix: MSVC native static and DLL Debug/Release; clang-cl static and DLL Debug/Release with supported dependency preparation; focused native minimal and Wasm core/lifecycle Debug/Release; minimal/demo browser delivery and scene checks; representative ASAN targets; editor unit/UI tests; installed SDK sample builds/resource checks. Human checks cover SceneBaseSample, inputDemo, NauDemo, and editor project/viewport interaction and normal close in Debug/Release.

Rollback uses matched pre-migration revisions of engine and consumers plus fresh build directories. Do not roll back a single ABI participant while reusing migrated binaries. Component commits and parent submodule pointers must remain a coherent set when changes are later submitted.

### Approved empty move-only callback behavior

Calling an empty FixedMoveOnlyFunction reports a fatal diagnostic and terminates in both const and non-const overloads, including Release and exception-free builds. This replaces the old unchecked null call/non-uniform assertion behavior, as explicitly approved by the user.


### Approved retained hash-table value contract

The retained raw-storage HashedKeyMap, FixedCapacityHashedKeyMap and HashedKeySet require trivially copyable keys and mapped values. Reject nontrivial mapped values at compile time; do not add owning-value construction/destruction semantics. This is the user's explicit choice following the task 4.1 audit and preserves the integral-key/value contract of current consumers. Typed standard allocators replace EASTL allocation helpers, and empty sentinels must not allocate during destruction or access an uninitialized allocator.


### Approved filesystem duplicate-removal repair

During utility migration, the user approved fixing findFiles.cpp duplicate cleanup: erase the entire tail returned by unique, including safe empty/unique input handling, rather than preserving the existing single-position erase defect. Keep sorted, case-sensitive path identity and cover empty, unique and repeated inputs with regression tests against the production helper. This repair does not change the public filesystem API or its return-count convention.


### Approved CancellationSource timeout-template repair

Correct the public setTimeout template to call the existing SetTimeoutInternal member. Retain the existing unsupported-operation diagnostic and do not schedule cancellation. The user explicitly selected this narrow repair rather than implementing timed cancellation. Cover template instantiation, the diagnostic, unchanged cancellation state and subsequent explicit cancellation.


### Approved length-aware formatting correction

The user approved respecting explicit string-view lengths and preserving embedded null bytes when consolidating formatting overloads. Normalize narrow and UTF-8 views to sized fmt string views, and copy formatted output with its explicit size. Do not retain the previous accidental C-string truncation or read beyond a bounded view. Preserve ordinary numeric formatting and the UTF-8 byte representation.
