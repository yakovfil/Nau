# Tasks

## 1. Generic scene construction

- [x] 1.1 Add the UI-neutral root-component construction interface and route SceneFactoryImpl through it with the existing ordinary fallback; verify a test-only derived scene object is constructed with the exact supplied root component and creation callbacks run once after ownership is established.
- [x] 1.2 Add ordinary scene and missing-root-component regression coverage for the factory extension; verify construction and scene/prefab restoration work without any UI registration or linkage.

## 2. Widget scene object migration

- [x] 2.1 Derive NauWidget from SceneObject, supply NauWidgetRootComponent with allocator-aware creation, and remove duplicate hierarchy/name/transform/destruction state and APIs; verify RTTI, defaults, owner conversion, allocator lifetime, and inherited name/component access in focused tests.
- [x] 2.2 Delegate size, pivot, and visibility to the root component and implement effective visibility through mixed scene ancestry; verify existing geometry validation/defaults and unchanged child origins after size/pivot edits.
- [x] 2.3 Replace old hierarchy/transform/death tests with scene behavior tests; verify mixed child order, both reparenting transform options, scene-transform parity under rotations/nonuniform scale, weak references, and inactive plus active destruction/deactivation behavior.

## 3. Registration and persistence

- [x] 3.1 Register the widget root-component type through an explicit static-consumer entry point and UI initialization before scene factory type enumeration; verify direct creation, scene-factory creation, and loading all yield NauWidget with a single root component and no CoreScene-to-UI dependency.
- [x] 3.2 Add structured runtime-value serialization of widget state with candidate validation before assignment; verify non-default fields, omitted fields/defaults, malformed types, non-finite geometry, and negative size through both direct property assignment and scene restoration, including retained state and diagnostics on failure.
- [x] 3.3 Extend focused fixtures with the existing portable asset_formats scene reader/writer support and necessary scene services; verify actual scene-stream round trips preserve mixed object/widget hierarchies, order, local transforms, geometry, visibility, names, UIDs, and additional component properties.
- [x] 3.4 Verify prefab-root widgets, SceneObject clone, and RecreateUid behavior; add tests for two independent prefab instances, fresh object/component identities, existing object-category queries, and serialized component references remapped to the proper instance.
- [x] 3.5 Verify unavailable-UI compatibility using separate service environments: save widgets, load/re-save as missing-component data without UI registration, then recover NauWidget type and properties with UI present; retain ordinary asset load coverage.

## 4. Consumers, documentation, and validation

- [x] 4.1 Migrate the public consumer and README/API documentation to scene operations and registration; verify examples compile and document destroying removal, reparent options, normal scene transform limitations, mixed visibility, service requirements, and save/load failure behavior.
- [x] 4.2 Build/run affected widget and scene regression suites in native Debug and Release, including headless persistence consumers; record commands and passing counts with no obsolete abort-on-widget-destroy expectations.
- [x] 4.3 Build/run the focused Emscripten consumer through Node using public widget creation and actual scene-stream save/load; record passing results and inspect its dependency closure for excluded platform/rendering dependencies.
- [x] 4.4 Install a fresh Debug/Release SDK with the required portable serialization support, relocate it, then build/run the public persistence consumer in both configurations; verify imported headers/libraries come from the relocated SDK and inspect ordinary default graphs for continued UI independence.
- [x] 4.5 Run clang-format checks on affected C++ files, component/root diff checks, and strict OpenSpec validation; record final validation evidence and working-tree identities, confirming generated outputs and unrelated component changes are excluded.
