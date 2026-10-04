# Proposal

## Why

The current Widget has a separate identity and ownership model from Nau scene objects. Adopting NauObject now establishes a consistent object foundation for future widget persistence and scene use without implementing either feature yet.

## What Changes

- **BREAKING**: Rename `nau::ui::Widget` to `nau::ui::NauWidget`, with no compatibility alias, and derive it from `nau::scene::NauObject`.
- **BREAKING**: Replace direct construction and standard unique ownership with allocator-aware creation returning `ObjectUniquePtr<NauWidget>`; replace numeric `id()` with inherited `getUid()`.
- Keep ordered parent-owned children, using `ObjectUniquePtr` children and an `ObjectWeakRef` parent. Support invalidating external weak references.
- Preserve attachment rejection, detachment, subtree lifetime, name, and visibility behavior. Define destruction as owner-controlled, including the inherited `destroy()` limitation.
- Update build dependencies, focused tests, public documentation, and source/installed SDK consumers for the scene dependency.
- Defer save/load, scene attachment, scene-query support, layout, input, rendering, and production widget subclasses.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `widget-foundation`: NauObject-based widget identity, creation, ownership, weak references, and the expanded portable dependency closure.

## Impact

Implementation belongs in `NauEngineModules/modules/ui`, its tests and consumer fixture, and module/SDK build integration as needed. `NauUi` gains a public dependency on `CoreScene` and its existing `CoreAssets` closure. Standalone NauEngineLite stays module-neutral; existing minimal and scene defaults must not start selecting UI. Native Debug/Release, Emscripten, and relocated SDK consumers require renewed validation. Historical archived artifacts remain unchanged.
