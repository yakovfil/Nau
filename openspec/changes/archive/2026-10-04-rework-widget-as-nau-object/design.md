# Design

## Context

See proposal.md for motivation. The current UI library links only NauKernel. Widget uses a process-local integer ID, public construction, standard unique pointers, and a raw parent pointer. Its tests include stack instances and test-only derived lifetime probes.

NauObject lives in CoreScene, whose public dependency is CoreAssets. Its allocator-aware factory records the concrete destructor. ObjectUniquePtr releases ownership before invoking deleteObjectNow; that function invalidates weak references before running disposal, destruction, and allocator deallocation. Its inherited destroy() rejects an object still held by an owner in assertion-enabled builds; NAU_FATAL is compiled out in Release, so it cannot provide the required all-build widget guarantee. Some header comments incorrectly describe shared reference counting; implementation behavior is authoritative.

Scene asset traversal and SceneQuery currently recognize scene objects and components, not arbitrary NauObject subclasses. Inheritance therefore provides identity and lifetime machinery, not persistence or scene membership.

## Goals / Non-Goals

**Goals:** Integrate the public widget object model with NauObject while preserving existing tree/state semantics and headless native/browser use. Make the ownership contract usable without scene-manager startup.

**Non-Goals:** No widget serializer, reflected persistence schema, scene query category, component wrapper, asset format, editor integration, or new production subclass. No extraction of NauObject into the kernel, and no general rewrite of scene ownership pointers.

## Decisions

### Public type and creation

Use `nau::ui::NauWidget : public scene::NauObject`, with engine RTTI registered through the existing NauObject pattern. Rename public files to `nau_widget.h`/`nau_widget.cpp`; remove the old type/header without compatibility shims. Keep the NauUi target and existing state/hierarchy method names except `id()`.

Provide `NauWidget::create(IMemAllocator* allocator = nullptr)` returning `scene::ObjectUniquePtr<NauWidget>`, delegating to NauObject::classCreateInstance. Use a public constructor taking a construction key whose creation is restricted to NauWidget and its subclasses. This permits the base factory's std::is_constructible check while preventing ordinary callers from constructing the concrete widget directly. The create method supplies the key to classCreateInstance. Preserve test-only subclass construction through the same allocator-aware machinery. Do not support stack allocation or std::make_unique.

Generate inherited UID on construction with Uid::generate(), as SceneObject does. Remove the separate counter and id(). getUid() is stable across tree/state operations. Inherited setUid() remains available but manual UID reassignment is outside the widget identity guarantee; uniqueness applies to freshly created widgets. Do not promise immutable IDs or persistence semantics that NauObject does not provide.

### Tree ownership and references

Use an ordered vector of ObjectUniquePtr<NauWidget> and an ObjectWeakRef<NauWidget> parent. addChild takes an rvalue reference to an owning handle, validates before consuming it, and preserves rejected handles. removeChild returns the intact subtree owner. Keep pointer-based, const-correct borrowed accessors; expose weak references using the existing scene pointer API rather than a new handle system.

Preserve all existing cycle checks, ordering, visibility calculations, and direct-child-only detachment. Clear child parent references before destroying attached descendants. Detachment does not invalidate external weak references; destruction does. Retain explicit deleted copy/move operations.

This replaces std::unique_ptr because NauObject requires allocator-aware destruction and weak-reference invalidation. Shared ownership would violate the confirmed single-owner tree contract.

### Destruction remains owner-controlled

Reset or destroy the owning handle to destroy a root; detach a child and release its returned owner to destroy that subtree. Do not implement self-removal or scene-manager destruction.

Hide direct calls to destroy() on NauWidget with a private final override that unconditionally terminates with std::abort(). This ensures normal virtual calls through a NauObject reference are rejected in every configuration, independently of NAU_FATAL and custom diagnostic handlers. The user approved this correction after Release validation exposed the disabled inherited guard. Document and test the rejection with native Debug and Release death tests; ordinary lifecycle tests use owner release. ObjectUniquePtr deletion bypasses this virtual entry point and remains supported. Explicit qualified calls to NauObject::destroy() bypass virtual dispatch, are unsupported, and cannot be prevented by access hiding; the base implementation itself is unchanged.

### Dependencies and consumers

Link NauUi publicly to CoreScene and ensure SDK imports load its dependency closure before NauUi. Keep UI optional and leave standalone kernel and minimal/scene default selections unchanged. Update the focused source consumer to opt into the existing portable scene profile through the modules hook and then explicitly select UI, replacing its kernel-only assumption. Installed consumers import the corresponding portable scene closure. Do not enable rendering, windows, or application services just to create widgets.

Retain native and Emscripten coverage. Inspect generated dependency graphs and actual link inputs so the newly allowed scene/assets closure does not accidentally acquire platform-only binaries. A broader scene dependency is accepted here; extracting a generic base into the kernel is a separate architectural change.

## Risks / Trade-offs

- Larger dependency closure -> validate native/browser and relocated SDK consumers; keep UI opt-in.
- ObjectUniquePtr differs from std::unique_ptr, including ownership flags and conversions -> exercise vector movement, middle removal, return/move assignment, rejection, and derived destruction with real handles. Avoid constructing duplicate owners to test invalid input.
- Inherited public destroy()/setUid() have broader semantics -> document the restrictions and test virtual destruction through the base interface in every configuration; do not claim a fully sealed lifetime or identity API.
- Allocator creation may conflict with constructor access traits -> resolve using the narrowly scoped factory/construction-key approach, with native and Emscripten compile coverage.
- Weak references do not provide thread synchronization -> retain single-threaded, caller-controlled tree access.
- Inheritance may be mistaken for serialization support -> explicitly document that widget weak references are in-memory only in this change and are not routed through SceneQuery serialization.

## Migration Plan

Rename the public type/header and migrate all live consumers, examples, and tests. Replace stack/std ownership creation with the factory and engine owners, and numeric identity reads with getUid(). Update source/SDK build integration and README together. Do not rewrite archived OpenSpec history. Validate before committing; rollback can revert the cohesive API/build/test change and its parent gitlink without a data migration because no persisted widget format exists.
