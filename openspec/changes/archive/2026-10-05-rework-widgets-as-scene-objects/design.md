# Design

## Context

See proposal.md for motivation. NauWidget currently derives from NauObject and duplicates hierarchy, name, transform, and lifetime behavior. SceneObject is extensible but requires an owned SceneComponent at construction; destroy() is final and delegates to SceneManagerImpl. Its parent is a non-owning scene pointer, its children form an owned intrusive hierarchy, and its transform API delegates to the root component. SceneComponent composes cached math::Transform values and accepts transform setters without the widget's extra validation.

SceneObjectAsset stores UID, name, ordered child relations, and component records, but no object-subclass discriminator. SceneFactoryImpl currently always constructs SceneObject after creating its requested root component. SceneAssetWrapper exposes component RuntimeValue properties; SceneAssetVisitor recreates root components by registered type and assigns properties. The asset_formats scene container preserves these records. Scene finalization already handles scene-object/component UID regeneration and component reference resolution.

## Goals / Non-Goals

**Goals:** A real SceneObject-derived widget; one hierarchy and transform authority; scene/prefab stream round trips restoring widget RTTI, geometry, visibility, components, and references; a UI-independent scene extension.

**Non-Goals:** No changes to scene transform mathematics or general parenting validation, no parallel widget tree, no new scene container format, no generic serialization of arbitrary SceneObject subclass fields, no renderer/layout/input, no editor or USD integration, and no legacy Cocos migration. Only NauWidget is a supported widget runtime type in this increment.

## Decisions

### Adopt the scene API and lifecycle explicitly

NauWidget derives from SceneObject with engine RTTI. Keep allocator-aware NauWidget::create() and restricted construction, supplying a widget root component to the SceneObject constructor. Direct creation of an inactive object can remain headless; scene factory loading, queries, activation, and explicit destruction require the normal scene services.

Remove m_parent, m_children, m_localTransform, m_debugName, custom destroy(), and the widget-only hierarchy/transform API. Use getName/setName, getParentObject/getDirectChildObjects, attachChild/attachChildAsync, setParent, removeChild, destroy, getTransform/setTransform, and getWorldTransform. No compatibility aliases for semantics that changed. The migration table must emphasize that removeChild destroys and does not return ownership. For retaining a subtree, setParent moves it to another scene object; there is no new detach-to-owner API.

attachChild preserves local transform. setParent preserves world transform by default, with DontKeepWorldTransform selecting local preservation. Active operations obey existing scene activation/deactivation rules. Normal scene transform results, validation behavior, singular-scale limitations, and floating-point behavior apply; exact shear preservation and widget-specific transform errors are retired by explicit user choice. Size/pivot remain independent of transform and descendant origins.

### Store widget-specific state in its root component

Introduce a NauWidgetRootComponent derived from SceneComponent in NauUi. It stores local visibility, size, and pivot, with defaults true, (0,0), and (0.5,0.5). NauWidget delegates its existing visibility and geometry accessors/setters to that state. This uses the existing component serializer and keeps a single authoritative copy. It is the widget's root component, not a scene component owning a separate widget tree.

Serialize a structured widget-state property containing visibility, size, and pivot. Its runtime-value assignment path validates a complete candidate before committing it, preserving prior widget state on invalid geometry. Use the engine RuntimeValue adaptation mechanism instead of directly exposing writable raw fields that bypass setters. Missing state uses defaults; missing individual fields use their defaults within the candidate. Reject wrong types, non-finite geometry, and negative size without clamping; transform fields continue through the unchanged SceneComponent path. Follow the scene loader's existing log-and-continue failure policy: a fresh widget retains default widget state and a diagnostic identifies the failed restore. Whole-scene transactional loading is outside scope.

Name and UID use SceneObject state; transform uses SceneComponent state. Child structure/order uses scene traversal. Effective visibility and world transform are derived and are not additional serialized fields.

The generic runtime assignment skips explicit null properties. Add an optional UI-neutral IComponentPropertyValidator in CoreScene, queried before scene property assignment. It receives the original property record and validates without mutation, including present null values. On failure the loader skips property assignment and logs the existing restoration diagnostic; UID and transform restoration continue through their normal paths. Components without the interface retain existing behavior. NauWidgetRootComponent shares one candidate parser between this hook and direct widgetState assignment. This extension was approved during implementation after the null-state regression exposed the assignment limitation.

### Construct the scene-object subtype through the root component

Add a small UI-neutral construction interface in CoreScene, implemented optionally by root components. It accepts ownership of the already-created root component and returns an owned SceneObject. In SceneFactoryImpl::createSceneObject, after creating the root component, query this interface; invoke it when present, otherwise use the existing SceneObject construction path. Invoke onComponentCreated exactly once after the owner exists, preserving current callback ordering.

NauWidgetRootComponent implements the interface by constructing NauWidget around itself. The root component remains alive throughout ownership transfer. Contract: the result owns exactly the supplied component; it may not substitute, duplicate, or drop ownership. Construction does not inspect restored property values because restoration happens afterward. Component type alone selects widget construction. The allocator used for direct creation is propagated to both allocations; scene factory construction follows existing allocator conventions.

The serialized root-component type is therefore the durable widget discriminator. Adding an objectTypeId field and a second object factory registry was considered, but would duplicate the existing component registration/asset schema for this scope. A scene component owning an independent widget tree was rejected by the user's SceneObject decision.

Register the root-component class from an explicit NauUi registration entry point before the scene factory first enumerates component classes (its type list is cached). Invoke this entry from normal UI module initialization and expose it for static/headless/SDK consumers. Avoid relying on unreferenced static initializers in a static library. CoreScene contains only the generic hook and never names or includes NauWidget. Existing ordinary roots and missing-component roots retain the default path.

### Support mixed scene hierarchies and existing reference semantics

A widget can have an ordinary scene parent or ordinary scene children. Every ancestor contributes its normal scene transform. A widget ancestor's transform origin is its pivot; an ordinary ancestor contributes its ordinary scene origin. Effective visibility checks every widget ancestor, traversing through ordinary objects as well; ordinary objects contribute no UI visibility flag. Visibility remains independent of scene activation.

Because widgets are scene objects, existing Object-category SceneQuery resolution and serialized component weak references can target them. No Widget query category or second UID index is added. Ordinary scene load preserves object/component UIDs; clone/prefab instantiation and RecreateUid regenerate them using current scene finalization, including reference remapping. Old live weak handles do not magically retarget newly loaded instances.

### Preserve format and optional-module compatibility

Widgets appear beneath the ordinary scene root; changing the special IScene root runtime type is outside scope. A prefab root can be a widget. Existing ordinary scene assets load unchanged. If UI is unregistered, the existing missing-component fallback preserves the unrecognized root component's type/properties on an ordinary SceneObject, allowing later save and reload with UI registered to recover the widget. This fallback is not reported as an operational widget. Test this across separate service-provider instances to avoid cached component registrations.

Use the existing scene container reader/writer for persistence tests. Extend the focused UI fixture to compile/select only the portable scene serialization sources needed from asset_formats, following existing scene tests; do not pull in unrelated importers, desktop SDKs, or rendering. SDK consumer tests must exercise installed public API and stream save/load with the required installed serialization support. Production NauUi depends on CoreScene, not on a hard dependency from CoreScene to UI or from widget construction to all asset formats.

## Risks / Trade-offs

- Scene lifecycle replaces owner-only widget destruction -> replace abort death tests with ordinary SceneObject parity tests, including active removal and weak-reference invalidation.
- Generic root construction affects every scene object -> use a test-only derived root/object pair to test the hook and run ordinary scene regression tests without UI registration.
- Missing-component restoration can hide unavailable UI -> document that the fallback is an ordinary placeholder and verify data survives re-save.
- Raw reflection could bypass size/pivot validation -> test assignment through serialized RuntimeValue properties as well as direct setters.
- Root component is the type discriminator -> reserve this root component for NauWidget creation and keep state ownership singular.
- Old code expects local-preserving reparent/removal ownership -> publish explicit API migration and replace contradictory tests and spec requirements.

## Migration Plan

Implement the generic construction hook first with UI-independent tests. Migrate NauWidget and its callers/tests, then register and serialize root state. Add scene/prefab round trips, UID/reference and missing-module regressions. Validate native Debug/Release, Emscripten Node, and a fresh relocated SDK; inspect module graphs to confirm ordinary defaults remain UI-free.

There is no previously supported serialized NauWidget format to migrate. Rebuild library/SDK consumers for the class-layout and public-API change. Keep previous change archives historical. Rollback reverts the hook and widget migration together; newly saved widget records can survive as missing-component data when the new UI type is unavailable, but are not usable widgets until restored with its implementation.
