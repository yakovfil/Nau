# Proposal

## Why

Widgets need to participate directly in scenes and survive scene save/load. Reusing SceneObject's hierarchy, components, lifecycle, and transforms gives them the scene behavior requested by the user and eliminates their separate hierarchy implementation.

## What Changes

- **BREAKING**: Derive NauWidget from SceneObject and adopt scene parenting, naming, destruction, activation, weak-reference, and transform APIs.
- **BREAKING**: Remove widget-only ownership-returning removal, Result-based attachment, local transform validation wrappers, and exact accumulated-matrix API. Use current scene transform composition and reparenting rules as-is.
- Retain local visibility, size, and pivot, with the parent's pivot as the child coordinate origin; allow ordinary scene objects and widgets in the same hierarchy.
- Persist widget type and properties through existing scene/prefab containers, restoring child order, components, identity, and references according to scene conventions.
- Add a generic scene construction extension driven by the root component and register the widget root component from NauUi. Keep CoreScene independent of UI.
- Preserve legacy ordinary-scene loading and missing-component behavior when UI is unavailable.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `widget-foundation`: Replace independent-widget hierarchy/lifetime/transform contracts with SceneObject behavior and add scene persistence and runtime-type restoration.

## Impact

NauEngineModules/modules/ui needs API, root-component state/registration, tests, consumer, and documentation changes. CoreScene needs a generic construction hook plus regression tests; focused persistence fixtures need the existing asset_formats scene reader/writer sources. No UI include or dependency is added to CoreScene or NauEngineLite. No new graphics, input, Cocos, Qt, or USD dependency is introduced. Native Debug/Release, Emscripten, and relocated SDK verification cover the new API and actual scene-stream round trips.

Layout, drawing, input, editor/USD authoring, legacy Cocos asset conversion, new widget subclasses, and changes to scene transform mathematics are outside scope.
