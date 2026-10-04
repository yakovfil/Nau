# Tasks

## 1. Library and basic state

- [x] 1.1 Add `NauEngineModules/modules/ui/` with static `NauUi` target, public `nau/ui/widget.h`, implementation, and headless Google Test/CTest wiring gated by `NAU_CORE_TESTS`; verify a native build discovers the target without adding graphics/input dependencies.
- [x] 1.2 Implement directly constructible, non-copyable/non-movable Widget with virtual destructor, stable runtime identity, optional debug name, and visibility defaults; verify defaults, distinct live identities, name mutation, and compile-time copy/move restrictions in focused tests.

## 2. Hierarchy and visibility

- [x] 2.1 Implement private ordered unique ownership, borrowed parent access, and child enumeration; verify attachment transfers ownership, sets parent references, and preserves order and object addresses.
- [x] 2.2 Implement attachment validation before ownership transfer; verify null, self, and ancestor-cycle rejection preserve caller ownership and existing trees, and review the already-parented guard without constructing duplicate owners in tests.
- [x] 2.3 Implement direct-child removal returning ownership; verify clearing the parent reference, non-child no-op behavior, preserved sibling order, and detach/reattach of intact subtrees with stable identity and state.
- [x] 2.4 Implement teardown clearing parent links before child destruction; verify exactly-once multi-level destruction and detached subtree survival with test-only lifetime probes.
- [x] 2.5 Implement local/effective visibility queries; verify ancestor hide/show preserves local flags and detachment/reparenting changes effective visibility immediately.

## 3. Integration and documentation

- [x] 3.1 Add SDK installation/export and modules-owned SDK import integration for NauUi; verify a relocated installed SDK consumer builds and runs attachment/removal using installed headers and libraries without source paths.
- [x] 3.2 Add a concise module README and public API lifetime/threading documentation, including ownership transfer, rejected attachment, borrowed-pointer lifetimes, visibility semantics, and scope exclusions; verify its example matches the public API through the consumer build.

## 4. Validation

- [x] 4.1 Build and run focused native Widget CTest tests in Debug and Release; record commands and results covering all state, hierarchy, and lifetime scenarios without application/window startup.
- [x] 4.2 Compile and link a focused Emscripten consumer of NauUi using existing portable build infrastructure and explicit module selection; record successful compilation and inspect its dependency graph for excluded rendering/window/native-binary dependencies.
- [x] 4.3 Verify standalone kernel and existing minimal/scene default configurations acquire no NauUi dependency, and inspect the new library/SDK graph for retired UI dependencies; record results without modifying default selections or legacy rejection behavior.
- [x] 4.4 Format changed C++ using the engine configuration, run diff checks and strict OpenSpec validation, and record affected revisions or working-tree identities and validation outcomes in change evidence; mark unavailable checks explicitly rather than passing them.
