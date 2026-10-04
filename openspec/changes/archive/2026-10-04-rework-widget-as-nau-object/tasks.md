# Tasks

## 1. Object model and ownership

- [x] 1.1 Rename the public Widget type/header/source to NauWidget, add NauObject RTTI and factory construction with a restricted construction key, and adopt generated inherited UID; verify compilation, base-type casts, non-null distinct UIDs, and rejection of ordinary default construction in focused tests.
- [x] 1.2 Convert children to ObjectUniquePtr and parent to ObjectWeakRef while retaining borrowed const-correct accessors; verify ordered attachment, empty/self/cycle rejection with retained ownership, middle-child removal, reattachment, and unchanged UID/address/state.
- [x] 1.3 Implement owner-controlled subtree teardown and private final destroy override; verify concrete destruction and allocator deallocation exactly once, parent clearing, retained detached lifetime, and a native death test for owned destruction through NauObject.
- [x] 1.4 Add weak-reference regression coverage for root/descendants, transfer, detachment, and invalidation before concrete destruction; run the focused ownership/state tests including the existing visibility scenarios and copy/move restrictions.

## 2. Build and consumer migration

- [x] 2.1 Add the public CoreScene dependency and adjust module/SDK import integration as necessary; verify configuration resolves NauUi and its scene/assets closure without making UI part of standalone, minimal, or scene defaults.
- [x] 2.2 Migrate the focused source consumer to explicit UI selection on the portable scene profile and migrate the installed consumer to its exported dependency closure; verify factory creation, base RTTI, attachment, detachment, and weak invalidation in the consumer executable.
- [x] 2.3 Update live public API usages, README examples, and ownership/identity documentation; verify repository searches find no obsolete live Widget API usages and explicitly document deferred serialization/scene attachment, inherited destroy/setUid restrictions, and single-threaded access.

## 3. Integration validation

- [x] 3.1 Build and run the focused native widget tests and source consumer in Debug and Release with CTest; record commands and results, including allocator and lifetime coverage, without requiring window/GPU/application startup.
- [x] 3.2 Install the required native SDK closure in Debug and Release, relocate the install, then build and run both installed consumer configurations; verify public includes and link inputs do not use source-checkout or original-install paths.
- [x] 3.3 Build the Emscripten widget consumer and run its headless JS/Wasm smoke test; record successful UID/RTTI/ownership/weak-reference behavior and confirm no platform-only binary dependency enters the build.
- [x] 3.4 Inspect generated target graphs for the explicit widget consumers and standalone/minimal/scene defaults; record the allowed scene/assets closure and absence of UI in defaults, rendering/window dependencies in focused consumers, and retired UI dependencies.
- [x] 3.5 Run formatting and diff checks for changed code, strictly validate this OpenSpec change, and record final validation evidence and any remaining limitations in the change directory; verify all required checks are accounted for before marking tasks complete.
