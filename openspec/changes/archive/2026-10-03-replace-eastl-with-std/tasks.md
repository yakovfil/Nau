# Tasks

## 1. Migration baselines

- [x] 1.1 Record engine/editor/sample/demo revisions, toolchain/STL identities, clean build locations, and the exact existing failure exclusions in validation.md; verify every recorded input and exclusion against the checkout and failed-tests.md.
- [x] 1.2 Produce a symbol-to-replacement inventory for the observed EASTL families, public headers, optional modules, bundled integration, CMake exports, and independent EABase consumers; verify tracked-source searches account for each family and identify concrete replacement contracts.
- [x] 1.3 Capture focused pre-migration value/serialization fixtures and allocation/object-lifetime observations for inline overflow, unique/multi ordered containers, bits, timer membership, tuple-vector columns, fixed-map nodes, bounded callbacks, intrusive references, and LRU eviction; verify fixtures distinguish required behavior from implementation-specific growth/layout and record existing failures without treating them as passes.

## 2. Standard allocator integration

- [x] 2.1 Implement typed adapters for array/pool allocation with checked sizing, alignment, rebind, equality, and explicit propagation traits; verify over-aligned sequence and node containers, invalid requests, and paired release using instrumented resources.
- [x] 2.2 Implement resource-bound frame/stack adapters and safe unequal-resource transfer behavior; verify copy/move/swap contracts, correct originating-resource release, and destruction before frame/stack reset.
- [x] 2.3 Migrate Nau vector/map/list aliases to standard containers and new adapters; verify node allocation without EASTL internal node types and compile representative existing consumers.
- [x] 2.4 Port retained allocator regression coverage and add a real native DLL allocation/release probe; verify value preservation, alignment, resource identity, and deallocation across MSVC and clang-cl module boundaries, explicitly mapping old EASTL test names to retained coverage.

## 3. Specialized containers

- [x] 3.1 Implement the required Nau inline vector operations with explicit live-object management and overflow allocator policy; verify below/at/above capacity, no backing allocation in the inline range, disabled overflow, move-only and over-aligned values, and exact destruction counts.
- [x] 3.2 Replace required fixed-string uses with inline-preserving Nau support; verify terminators, lengths, moves, and overflow policy against recorded call-site contracts, or document a zero-use inventory if no live consumers exist.
- [x] 3.3 Implement sorted vector map/set adapters over standard contiguous storage; verify comparator ordering, duplicate insertion, transparent lookup, erase, and iterator behavior relied upon by consumers.
- [x] 3.4 Implement the required dynamic-bit operations over standard word storage; verify resize/shrink, tail masking, word-boundary indexes, bulk operations, and serialized bit representation where used.
- [x] 3.5 Implement non-owning intrusive list support and migrate timer membership; verify stable node identity, insertion/removal, cancellation, and destruction without membership allocations or ownership changes.
- [x] 3.6 Replace EASTL helpers in Dagor relocatable containers and audit relocatability traits for migrated types; verify nontrivial standard strings/containers retain valid ownership through growth and destruction, using focused lifetime tests and diagnostic builds.
- [x] 3.7 Implement sorted vector multimap/multiset behavior using the contiguous adapters from 3.3; verify duplicate retention, equal-range boundaries, equivalent-key ordering and selective/range erasure against ECS acknowledgement and graphics packing fixtures.
- [x] 3.8 Implement inline-node fixed maps with resource-safe copies/moves and designated overflow; verify full inline element capacity including any implementation sentinel, aligned rebound nodes, erase/reuse, reference stability and destruction of the source before destination use.
- [x] 3.9 Implement tuple-vector column storage and coordinated row operations; verify contiguous typed access, column alignment, row-index correspondence, nontrivial/move-only lifetimes and partial-construction cleanup where supported against ECS fixtures, preserving any demonstrated single-allocation requirement.
- [x] 3.10 Implement copyable fixed-storage callable support and remove EASTL internals from the existing fixed move-only wrapper; verify zero heap spill, copy/move/reset/destruction, empty invocation behavior, supported qualifiers and compile-time rejection of oversized/over-aligned captures.
- [x] 3.11 Implement intrusive reference handles with the existing ownership hooks; verify copy/move/adopt/null/self-assignment/const-conversion behavior and final pooled-resource return exactly once, without a new control block or changed thread-safety policy.
- [x] 3.12 Implement the required LRU operations over standard storage; verify hit/touch/update recency, capacity and zero-capacity behavior, eviction/callback order, clear/destruction and shader-cache reference lifetime under its existing locking model.

## 4. Kernel and minimal runtime migration

- [x] 4.1 Replace kernel configuration macros, traits, algorithms, spans, and ordinary utility types with standard/Nau equivalents, including the C++20 enum helper; verify representative public headers compile independently without EASTL transitive includes.
- [x] 4.2 Migrate string views/conversions and fmt integration while retaining tiny_utf8-backed Nau strings; verify valid Unicode, embedded-null handling where supported, formatter output, and malformed Web diagnostic-plus-empty cases against fixtures.
- [x] 4.3 Consolidate serialization/reflection/container overloads and hash integration after type replacement; verify no duplicate specializations and unchanged persistent IDs, canonical output, and value round trips across native and Web.
- [x] 4.4 Migrate kernel async, services, diagnostics, filesystem, and runtime ownership types; verify focused completion, cancellation, timers, thread cleanup, and allocation tests with exact prior exclusions recorded.
- [x] 4.5 Migrate minimal framework and platform consumers and run native/wasm32 focused core and minimal lifecycle suites in Debug/Release; verify real startup/step/shutdown and exception-free Web compilation with bounded timeouts.

## 5. Desktop modules and tools

- [x] 5.1 Migrate renderer public/common container and string APIs, including nonstandard growth/erase operations; verify affected common renderer targets compile and resource/container lifetime tests pass.
- [x] 5.2 Migrate DX12 driver containers and ownership operations; verify driver compilation and multi-swapchain creation/destruction checks with migrated allocators.
- [x] 5.3 Migrate Dagor ECS containers, callbacks, lookup, and bit operations; verify affected ECS targets and focused ordering, identity, component lifecycle, and serialization checks.
- [x] 5.4 Migrate scene, asset, and animation interfaces and implementations; verify target builds, heterogeneous asset lookup, scene value fixtures, and applicable module tests.
- [x] 5.5 Migrate UI, VFX, and graphics integration, including directly coupled bundled code; verify affected targets build with no remaining EASTL includes and record any necessary third-party patch provenance.
- [x] 5.6 Migrate remaining physics, input, networking, audio, application-framework, and optional module uses; verify the inventory is exhausted for these areas and affected targets/tests compile and execute where supported.
- [x] 5.7 Migrate asset, shader, material, USD, and project/build tool consumers; verify affected tool targets and representative asset/project generation workflows using matching migrated engine outputs.

## 6. Consumers and dependency removal

- [x] 6.1 Migrate NauEditorPublic engine integration to the new public types; verify Debug/Release editor builds and unit/UI suites with actual test counts and exact existing exclusions.
- [x] 6.2 Migrate NauSamples and NauDemo native/Web consumers; verify all supported sample targets, both demo native build routes, and Web demo compilation in Debug/Release.
- [x] 6.3 Migrate generated project templates and SDK export/import interfaces; verify a generated project and installed samples configure and build without EASTL package discovery.
- [x] 6.4 Remove bundled EASTL, allocator hooks, target definitions, natvis, browser debug-break support, preset switches, and install exports after consumer migration; verify active tracked code/build interfaces have no remaining EASTL dependency and clean minimal/full configuration succeeds.
- [x] 6.5 Resolve EABase independently and document retained consumers or remove it if unused; verify consumer searches and affected clean target graphs agree with the recorded decision.
- [x] 6.6 Add a focused dependency-regression check over active sources and SDK/build interfaces, allowing only documented historical/attribution text; verify it rejects an EASTL dependency fixture and passes the migrated tree without relying on stale outputs.

## 7. Integrated acceptance

- [x] 7.1 Build and test MSVC static and DLL Debug/Release from clean migration directories; verify affected engine/module suites and sample outputs, recording all pass/skip/failure counts and exact exclusions.
- [x] 7.2 Build and test clang-cl static and DLL Debug/Release with recorded dependency preparation; verify the same preserved allocation/container contracts and affected runtime suites, separating known async failures from new results.
- [x] 7.3 Run representative ASAN and allocation/lifetime probes plus the recorded representative allocation/timing comparison; verify no migration-introduced memory errors and document investigated behavior/performance differences.
- [x] 7.4 Rebuild minimal and NauDemo Web Debug/Release packages and run existing delivery, scene, lifecycle, pending-work, and negative fixtures; verify expected results and actual browser execution with exceptions still disabled.
- [x] 7.5 Install and relocate the SDK outside the checkout, then build representative installed samples and a generated consumer in Debug/Release; verify resource roots stay within the relocated SDK and record launch/shutdown results separately from existing deferred failures.
- [x] 7.6 Obtain human acceptance for migrated SceneBaseSample, inputDemo, and NauDemo in Debug/Release; verify expected scene/input behavior and normal close for all six runs, recording the new binary paths and user results.
- [x] 7.7 Obtain human acceptance for migrated editor Debug/Release; verify project opening, viewport/basic interaction, and normal close, recording the new binary paths and user results.
- [x] 7.8 Reproduce documented native and Web entry points from clean recorded inputs with no EASTL or copied build outputs; verify input hashes/revisions, toolchain identity, target graphs, and output provenance are captured.

## 8. Documentation and completion evidence

- [x] 8.1 Update engine coding guidelines and applicable AGENTS.md guidance to prefer standard facilities and document the preserved Nau adapters; verify no current guideline still directs new code to EASTL.
- [x] 8.2 Update build.md, prerequisites.md, and affected engine/editor/sample/demo guides with standard-library selection, source/ABI migration examples, clean coordinated rebuilds, and any retained EABase rationale; verify paths and commands against completed validation.
- [x] 8.3 Finalize validation.md with requirement-to-evidence mapping, test replacement mapping, toolchain/STL versions, remaining failures and deferrals, and coherent repository inputs; verify every task status reflects its evidence and run strict OpenSpec validation without claiming excluded or unexecuted checks passed.
