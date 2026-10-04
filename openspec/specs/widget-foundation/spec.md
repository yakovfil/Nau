# widget-foundation Specification

## Purpose

Provide a portable basic widget with explicit tree ownership and queryable state as the foundation for future engine UI capabilities.

## Requirements

### Requirement: Basic widget state and stable identity

The foundation SHALL expose NauWidget as a SceneObject-derived type with engine runtime type compatibility with SceneObject and NauObject, an inherited UID and scene object name, and local UI visibility. Supported direct creation SHALL use allocator-aware exclusive engine ownership. Direct stack and standard unique-pointer construction SHALL remain unsupported. New widgets SHALL be visible, unnamed, parentless, childless, and have a root scene component. Widgets SHALL NOT be copyable or movable as objects. State edits, attachment, and reparenting SHALL preserve address and UID; explicit UID reassignment and scene duplication are outside this guarantee. Widget-specific naming SHALL be replaced by the scene naming API without duplicate name storage.

#### Scenario: Independent widgets are constructed
- **WHEN** two widgets are created through the supported factory
- **THEN** each has the specified defaults, a distinct non-null UID, exclusive engine ownership, and runtime type compatibility with SceneObject and NauObject

#### Scenario: State changes and ownership transfer
- **WHEN** a widget is renamed, hidden, attached, and reparented using scene operations
- **THEN** its identity and address remain unchanged and its scene name and local visibility are retained

### Requirement: Parent-owned ordered hierarchy

Widgets SHALL use the existing scene hierarchy and ownership APIs with a single parent relationship and ordered children. A widget SHALL support both ordinary scene objects and widgets as parents or children. Attachment SHALL transfer exclusive ownership to the parent and append in scene child order. Parent/child access and mutation preconditions SHALL follow SceneObject behavior; no separate widget-only hierarchy or stronger const-access contract SHALL be maintained.

#### Scenario: Child is attached
- **WHEN** a caller transfers an unattached widget to an ordinary scene object or widget with existing children
- **THEN** the caller relinquishes ownership and scene traversal reports that parent and the new child after existing children

### Requirement: Owned subtree lifetime

Widgets SHALL adopt existing SceneObject lifetime behavior for exclusive owners, scene ownership, explicit destruction, component activation, and asynchronous deactivation. Releasing an inactive owning root SHALL destroy its owned hierarchy and components through engine ownership. Removing an attached child SHALL destroy it through scene lifecycle handling. Reparenting a subtree away SHALL preserve it when its former parent is destroyed. Borrowed and weak references SHALL NOT extend lifetime. The widget-specific abort-on-destroy override SHALL be removed; explicit destruction through the base interface SHALL follow normal scene behavior with the required services initialized.

#### Scenario: Tree owner releases a root
- **WHEN** an exclusive owner releases an inactive widget root containing children and components
- **THEN** scene ownership destroys each owned object/component exactly once with scene parent cleanup and weak-reference invalidation

#### Scenario: Detached subtree outlives parent
- **WHEN** a subtree is moved away from its former parent to another live scene object and the former parent is destroyed
- **THEN** the subtree survives under its new parent with its internal relationships intact

#### Scenario: Owned widget is destroyed through its base interface
- **WHEN** a caller uses the base destruction API on an inactive owned widget with scene services initialized
- **THEN** the result follows the same ownership and invalidation behavior as an ordinary owned SceneObject instead of invoking a widget-specific abort

#### Scenario: Active widget is removed
- **WHEN** an active widget is removed from its scene parent
- **THEN** its references and components follow normal scene destruction/deactivation, including completion of pending component work before final destruction

### Requirement: Effective visibility follows ancestry

Widgets SHALL retain local visibility independently from effective visibility. Effective visibility SHALL be true exactly when the widget and every widget ancestor in the scene hierarchy are locally visible. Traversal SHALL continue through ordinary scene objects, which contribute no UI visibility flag. Ancestor visibility edits SHALL NOT change descendant flags. Reparenting SHALL be reflected immediately without a frame update. Local UI visibility SHALL be independent of scene activation state.

#### Scenario: Ancestor is hidden then shown
- **WHEN** a visible subtree's widget ancestor is hidden and subsequently shown, including across ordinary scene ancestors
- **THEN** effective visibility follows that widget ancestor while descendant local flags remain unchanged and locally hidden descendants remain hidden

#### Scenario: Widget leaves a hidden parent
- **WHEN** a locally visible widget is reparented away from hidden widget ancestry into visible widget ancestry
- **THEN** it immediately reports effective visibility as true

### Requirement: Portable independent foundation

Widgets SHALL build for supported native Windows and Emscripten targets and support headless tests without a window or GPU. Basic inactive construction and state access SHALL remain usable without scene activation; scene loading, querying, and lifecycle operations SHALL use their normal scene services. SDK consumers SHALL be able to create widgets and save/load scenes using installed interfaces and required portable serialization support. CoreScene and standalone kernel/default minimal/scene selections SHALL remain independent of UI registration and dependencies. The feature SHALL NOT require graphics, input, text rendering, Cocos, Qt, USD, or platform-specific binary dependencies.

#### Scenario: Headless native and browser compilation
- **WHEN** focused widget and persistence consumers build for native Windows and Emscripten
- **THEN** their state and scene-stream checks execute headlessly with the required portable services and without window/rendering startup

#### Scenario: Relocated SDK consumer
- **WHEN** an SDK is relocated and a consumer creates, attaches, references, saves, restores, and removes widgets
- **THEN** it builds and runs using installed public interfaces and dependencies without source-checkout include or library paths

#### Scenario: Existing minimal configuration
- **WHEN** standalone kernel or existing minimal/scene defaults are configured and ordinary scenes are used
- **THEN** they acquire no dependency on UI or its registration and ordinary scene behavior remains available

### Requirement: Invalidating non-owning widget references

Widgets SHALL use scene-object weak-reference, query, and serialization semantics. References SHALL remain valid across attachment and reparenting while the object remains live, and SHALL invalidate according to scene destruction rules no later than concrete destruction. Widgets SHALL be addressable through the existing scene-object query category. Serialized component references to widgets SHALL resolve to the restored or duplicated scene objects using existing scene reference remapping. Reloading SHALL NOT retarget weak handles belonging to previous live instances.

#### Scenario: Reference follows ownership transfer
- **WHEN** a referenced widget is attached or reparented
- **THEN** its weak references still resolve to the same live scene object

#### Scenario: Tree destruction invalidates references
- **WHEN** a widget tree is destroyed through supported scene ownership or lifecycle operations
- **THEN** its weak references invalidate under scene rules and remain invalid afterward

#### Scenario: Detached references survive former parent
- **WHEN** a referenced subtree is moved to another parent and its former parent is destroyed
- **THEN** references to the former parent invalidate while references to the retained subtree remain valid

#### Scenario: Saved component references a widget
- **WHEN** a scene with a component weak reference targeting a widget is saved and restored or cloned
- **THEN** that reference resolves to the corresponding restored or cloned widget through the existing object query category

### Requirement: Parent-relative widget spatial state

Widgets SHALL use inherited scene local/world transform APIs and existing scene composition, caching, setters, and reparenting behavior unchanged. The widget origin SHALL remain its pivot; child translation SHALL be relative to the parent's scene origin, which is its pivot for a widget parent. Ordinary scene ancestors SHALL contribute their scene transforms. New widget local transforms SHALL be identity. Attachment SHALL preserve local transform; reparenting SHALL preserve world placement by default and preserve local transform when the scene option requests it. Size and pivot SHALL be preserved by hierarchy operations.

#### Scenario: New widget and local transform edit
- **WHEN** a new widget is assigned a transform through scene APIs
- **THEN** it starts with identity and exposes the assigned transform and resulting scene world transform using ordinary scene behavior

#### Scenario: Subtree changes parent
- **WHEN** a widget subtree is reparented using the default scene option or the local-preservation option
- **THEN** the result matches an equivalent ordinary SceneObject subtree under the same option, retaining widget size and pivot

#### Scenario: Rotation and nonuniform scale compose
- **WHEN** widget ancestors combine rotation and nonuniform scale
- **THEN** local and world results match the current scene transform system without a separate exact-matrix or shear-preservation guarantee

### Requirement: Widget rectangle size and pivot

Each widget SHALL expose an unscaled width and height and a dimensionless two-component pivot. Defaults SHALL be size (0, 0) and pivot (0.5, 0.5). The rectangle SHALL lie in the local XY plane at Z=0 with minimum coordinates equal to negative pivot times size and maximum coordinates equal to (1 minus pivot) times size, component by component. Pivot (0, 0) SHALL denote the minimum-coordinate corner and (1, 1) the maximum-coordinate corner. Finite pivots outside this interval SHALL be supported. Size and pivot edits SHALL NOT change the widget's transform or any descendant's local or accumulated transform.

#### Scenario: Centered rectangle
- **WHEN** size is (200, 100) and pivot is (0.5, 0.5)
- **THEN** its local rectangle spans (-100, -50, 0) to (100, 50, 0)

#### Scenario: External pivot and unchanged children
- **WHEN** a parent with attached children changes its size and sets pivot to (2, -1)
- **THEN** its rectangle uses that external pivot without clamping and all child origins retain their accumulated positions

### Requirement: Validated widget spatial updates

Widget size/pivot setters SHALL reject non-finite components and negative size, reporting failure and preserving previous geometry. Zero size and finite external pivots SHALL be accepted without clamping. Geometry getters SHALL NOT permit bypassing validation. Transform mutation and validation SHALL follow the existing scene API, replacing the previous widget-specific Result-based transform validation. These behaviors SHALL hold in Debug, Release, and supported browser builds.

#### Scenario: Rejected spatial edit
- **WHEN** a size/pivot setter receives NaN, infinity, or a negative size
- **THEN** it reports failure and leaves prior widget state and hierarchy unchanged

#### Scenario: Degenerate and reflected geometry
- **WHEN** zero size is assigned or scene transform APIs are used with zero or negative scale
- **THEN** zero size succeeds and transform results follow the same behavior and limitations as an ordinary SceneObject

### Requirement: Widget scene and prefab persistence

Saving and restoring through existing scene/prefab containers with UI types registered SHALL reconstruct NauWidget runtime types, object/component identities according to the selected scene UID policy, names, local visibility, size, pivot, local scene transforms, attached components, and ordered mixed child hierarchies. Effective state SHALL be recomputed. Ordinary scene restoration SHALL preserve saved UIDs; scene duplication and prefab instantiation SHALL use existing UID regeneration and reference remapping. Widgets SHALL be supported beneath the ordinary scene root and as prefab roots.

#### Scenario: Scene stream round trip
- **WHEN** a scene containing widgets, ordinary objects, non-default widget state, and attached components is written to a stream and restored
- **THEN** widget types, saved properties, identities, component data, and child order match the source under the selected UID policy

#### Scenario: Widget prefab is instantiated twice
- **WHEN** a prefab rooted at a widget is instantiated twice
- **THEN** both roots and widget descendants have the correct runtime types and state, each instance has fresh identities, and internal references target its own instance

### Requirement: Compatible widget construction and property restoration

Scene construction SHALL support widget runtime restoration without introducing a dependency from the scene module to UI. Ordinary assets SHALL retain their existing construction behavior. Without UI registration, widget root-component records SHALL use the existing missing-component representation, retaining data through re-save for later restoration with UI present. Missing widget properties SHALL use defaults. Invalid serialized widget geometry or property types SHALL report restoration failure, preserve prior widget-specific state as a group, and use the existing scene loader diagnostic/continuation policy. Scene transform deserialization SHALL retain its existing behavior.

#### Scenario: Ordinary scene loads without UI
- **WHEN** an existing ordinary scene asset is loaded with no UI registration
- **THEN** objects and components restore as before without requiring UI

#### Scenario: Widget type is temporarily unavailable
- **WHEN** widget records are loaded and re-saved without UI registered and subsequently loaded with UI registered
- **THEN** the intermediate object uses missing-component data and the final load recovers the widget runtime type and saved properties

#### Scenario: Serialized geometry is invalid
- **WHEN** widget-state restoration receives an invalid size, pivot, or property type
- **THEN** the widget state group remains at its prior values, a restoration diagnostic is produced, and scene loading follows its existing continuation policy

#### Scenario: Explicit null widget state is invalid
- **WHEN** a scene component record contains an explicit null widgetState
- **THEN** the UI-neutral component validation hook rejects it before generic property assignment, retains widget defaults, and reports a restoration diagnostic while normal UID and transform restoration continue

#### Scenario: Widget properties are omitted
- **WHEN** a widget record omits its widget state or individual optional widget fields
- **THEN** omitted values restore as visible, zero size, and centered pivot as applicable
