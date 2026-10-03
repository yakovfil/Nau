# Proposal

## Why

Nau currently exposes bundled EASTL throughout its engine and consumer APIs while also using the toolchain standard library. Removing this parallel container dependency simplifies toolchain integration and maintenance; the migration must preserve the allocation and specialized-container behavior explicitly selected during exploration.

## What Changes

- Replace EASTL facilities with the toolchain's C++20 standard library in the engine, editor integration, samples, NauDemo, tools, and project templates.
- Preserve frame, stack, and pool allocation through standard-compatible Nau allocator adapters, including alignment and allocator ownership across module boundaries.
- Replace specialized EASTL containers with focused Nau implementations/adapters where standard C++20 facilities cannot preserve their required inline storage, overflow, ordering, bit operations, or intrusive ownership contracts.
- Preserve Unicode conversion, formatting, serialization, and exception-free Web behavior; retain the existing tiny_utf8-backed Nau string abstraction.
- **BREAKING**: Replace EASTL types in public interfaces and remove EASTL SDK exports. Rebuild engine modules, editor, applications, and SDK consumers together; binary compatibility with old outputs is not promised.
- Remove bundled EASTL and its build/install hooks once all consumers are migrated. Remove EABase only if an independent consumer audit proves it unused; otherwise retain and document its remaining purpose.
- Update coding guidance, prerequisites, build instructions, and reproducible validation evidence for native and browser routes.

## Capabilities

### New Capabilities

- `toolchain-standard-library`: EASTL-free public/build interfaces using toolchain standard facilities, with preserved Nau allocation and specialized-container contracts and coordinated consumer migration.

### Modified Capabilities

None. Existing Windows toolchain, minimal-runtime, Wasm portability, browser, and external-sample requirements remain applicable. Their dependency lists change as implementation details; their runtime contracts are preserved.

## Impact

Primary impact is in NauEngineLite kernel headers, allocators, strings, serialization, async facilities, renderer/ECS modules, third-party integration, CMake exports, and tools. NauEditorPublic, NauSamples, and NauDemo must migrate their exposed engine types. The initial tracked C++ scan found EASTL references in approximately 1,120 engine files, 16 editor files, 23 sample files, and two demo files, excluding common third-party directories but including comments and potentially inactive code.

This is a staged, cross-repository source/ABI migration. It does not upgrade C++20, replace fmt/tiny_utf8/Qt/USD, promise performance improvements, or fix unrelated failures already recorded in `failed-tests.md`. Newly introduced failures and preserved-contract failures remain visible rather than being represented as passes.
