# Tasks

## 1. Local spatial state

- [x] 1.1 Add local transform, size, and pivot storage/accessors to NauWidget with documented defaults and const-safe access; verify defaults and accessor types in focused widget tests.
- [x] 1.2 Implement Result-based validated setters without partial mutation or clamping; verify finite accepted values, external pivots, zero/negative scale, zero size, and rejection of negative size, NaN, infinity, and invalid quaternions in headless tests.

## 2. Hierarchy composition and geometry semantics

- [x] 2.1 Implement iterative accumulatedMatrix() using local matrices and ancestor pre-multiplication; verify root and three-level results, full 3D rotation, nonuniform-scale shear, and reflected/singular transforms against independent expected matrices or points.
- [x] 2.2 Extend hierarchy tests to verify immediate ancestor updates, preserved local geometry on detach/reattach and failed attachment, and unchanged descendant matrices after size/pivot edits; run the focused tests while retaining existing ownership and lifetime coverage.
- [x] 2.3 Document parent-pivot coordinates, rectangle formulas, axis/unit boundaries, defaults, validation, and example usage in the UI README/public API; verify examples agree with centered and external-pivot test cases and do not imply layout or scene support.

## 3. Portable consumer verification

- [x] 3.1 Extend the existing tests/consumer executable to exercise spatial state, composition, pivot/size independence, and invalid-input preservation through public API; verify native consumer CTest passes.
- [x] 3.2 Build and run the complete focused widget and consumer suites in native Debug and Release; record passing commands and results, including existing ownership/death tests and new geometry cases.
- [x] 3.3 Build the focused Emscripten consumer and run its CTest through the configured Node runtime; record successful portable geometry and rejection checks.
- [x] 3.4 Install a fresh Debug/Release SDK, relocate it, and build/run the updated consumer against that SDK in both configurations; verify include/link paths use the relocated prefix and no new rendering or platform dependency was added.
- [x] 3.5 Run affected-source clang-format checks, git diff --check, and strict OpenSpec validation; record final validation evidence and confirm implementation changes are confined to the intended UI area with generated files excluded.
