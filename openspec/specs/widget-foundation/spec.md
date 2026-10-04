# widget-foundation Specification

## Purpose

Provide a portable basic widget with explicit tree ownership and queryable state as the foundation for future engine UI capabilities.

## Requirements

### Requirement: Basic widget state and stable identity

The foundation SHALL expose `nau::ui::NauWidget` as a NauObject-compatible type with engine runtime type identification, an inherited UID, optional debug name, and local visibility. Supported creation SHALL return exclusive engine ownership using allocator-aware construction, with a generated non-null UID. Direct stack construction and standard unique-pointer construction SHALL NOT be supported. New widgets SHALL be visible, unnamed, parentless, and childless. Distinct freshly created widgets SHALL have distinct identities. A widget SHALL NOT be copyable or movable as an object; transferring its ownership SHALL preserve its identity and address. Widget state and hierarchy operations SHALL NOT reassign UID; explicit inherited UID reassignment is outside this stability guarantee. The former Widget type and numeric id() API SHALL be replaced without compatibility aliases.

#### Scenario: Independent widgets are constructed
- **WHEN** two widgets are created through the supported factory
- **THEN** each has the specified defaults, a distinct non-null UID, exclusive engine ownership, and runtime type compatibility with NauObject

#### Scenario: State changes and ownership transfer
- **WHEN** a widget is renamed, hidden, detached, and attached to another parent
- **THEN** its identity and address remain unchanged and its local name and visibility are retained

### Requirement: Parent-owned ordered hierarchy

A parent SHALL exclusively own its attached children through engine object ownership handles and expose them in attachment order. Each child SHALL retain a non-owning engine weak reference to its immediate parent. Successful attachment SHALL transfer ownership from the caller, append the child, and establish its parent reference. Public access SHALL NOT allow callers to replace parent references or mutate the ownership container independently of hierarchy operations. Borrowed access through a const widget SHALL NOT expose mutable parent or child pointers.

#### Scenario: Child is attached
- **WHEN** a caller transfers an unattached child to a parent with existing children
- **THEN** the caller relinquishes ownership, the child references that parent, and existing children precede it in their original order

### Requirement: Invalid attachment preserves ownership

Attachment SHALL reject empty ownership, self-attachment, an already-parented child, and any operation that would create a hierarchy cycle. Rejection SHALL report failure without changing existing relationships, child order, or the caller's ownership. Callers MUST supply valid exclusive ownership; manufacturing a second owner from a borrowed pointer is outside the API contract.

#### Scenario: Empty child is supplied
- **WHEN** attachment is requested with empty ownership
- **THEN** it fails and the parent's child list remains unchanged

#### Scenario: Root is offered to itself or its descendant
- **WHEN** the caller offers its valid owning root handle to that root or a descendant of that root
- **THEN** attachment fails, the caller retains the root, and the entire tree remains unchanged

### Requirement: Detachment returns ownership

Removing a direct child SHALL return exclusive ownership of its intact subtree and clear only that child's parent reference. Remaining siblings SHALL retain their relative order. Removing a widget that is not a direct child SHALL return no ownership and leave all trees unchanged.

#### Scenario: Middle child is removed and reattached
- **WHEN** a middle child with descendants is removed and then attached to another parent
- **THEN** it survives with the same descendants and identity, its parent reference changes through an unattached state, and the original siblings retain their order

#### Scenario: Non-child removal is requested
- **WHEN** removal is requested for an unrelated widget or a non-direct descendant
- **THEN** no ownership is returned and no parent reference or child list changes

### Requirement: Owned subtree lifetime

Releasing a widget's exclusive owner SHALL destroy it and all still-attached descendants exactly once using their recorded concrete destructors and allocators. Detached subtrees SHALL survive destruction of their former parent while retained by their new owner. A child's parent reference SHALL be cleared before the parent initiates that child's destruction. Parent references and other borrowed widget pointers SHALL NOT extend object lifetime. Destruction SHALL remain owner-controlled: the direct destroy() operation SHALL NOT be public on the widget interface; invoking it through normal virtual dispatch on the base object interface SHALL terminate the process in every build configuration rather than delete an owned widget. Explicit qualified base calls that bypass virtual dispatch are outside the supported widget API.

#### Scenario: Tree owner releases a root
- **WHEN** the owner destroys a root containing multiple levels of attached children
- **THEN** each attached widget is destroyed exactly once and child destruction observes no parent reference to the owner initiating that destruction

#### Scenario: Detached subtree outlives parent
- **WHEN** a subtree is detached and its former parent is destroyed
- **THEN** the retained subtree remains usable with no parent reference at its root and unchanged internal relationships

#### Scenario: Owned widget is destroyed through its base interface
- **WHEN** a caller invokes the base object destruction entry point on a widget still held by an owning handle
- **THEN** the call terminates the process in both Debug and Release instead of freeing the widget and leaving a dangling owner

### Requirement: Effective visibility follows ancestry

Widgets SHALL expose local visibility independently from effective visibility. Effective visibility SHALL be true exactly when the widget and all its ancestors are locally visible. Ancestor visibility changes SHALL NOT modify descendants' local flags. Reparenting and detachment SHALL be reflected by the next effective-visibility query without a frame update.

#### Scenario: Ancestor is hidden then shown
- **WHEN** a visible subtree's ancestor is hidden and subsequently shown
- **THEN** effective visibility follows that ancestor while descendant local flags remain unchanged and locally hidden descendants remain effectively hidden

#### Scenario: Widget leaves a hidden parent
- **WHEN** a locally visible widget is detached from a hidden parent
- **THEN** it immediately reports effective visibility as true

### Requirement: Portable independent foundation

The widget foundation SHALL build for supported native Windows and Emscripten targets and support headless native tests without a window, GPU, or application service startup. Its public dependency closure SHALL include the engine scene object support needed by the new object model. Installed SDK consumers SHALL be able to link the library and its dependency closure and use its public API. The foundation SHALL NOT require graphics, input, text rendering, Cocos, Qt, USD, or platform-specific binary dependencies. Standalone kernel builds and existing minimal/scene default module selections SHALL remain independent of this feature; consumers SHALL explicitly opt into UI.

#### Scenario: Headless native and browser compilation
- **WHEN** the foundation and its focused consumers are built for native Windows and Emscripten with the required scene dependency closure
- **THEN** they compile without rendering or window dependencies and native ownership/state tests execute headlessly

#### Scenario: Relocated SDK consumer
- **WHEN** an installed SDK is relocated and a small consumer creates, attaches, references, and removes widgets
- **THEN** the consumer builds and runs using the installed public interface and dependencies without source-checkout paths

#### Scenario: Existing minimal configuration
- **WHEN** standalone kernel or existing minimal/scene defaults are configured
- **THEN** they acquire no new dependency on the widget foundation or retired UI implementation

### Requirement: Invalidating non-owning widget references

Callers SHALL be able to retain engine weak references to widgets without extending their lifetimes. References SHALL remain valid across attachment, detachment, and ownership transfer while the referenced widget lives. All references to a widget SHALL become invalid before its concrete destructor executes. References to retained detached subtrees SHALL remain valid after destruction of their former parent. This contract SHALL apply to in-memory references only and SHALL NOT imply widget serialization, scene-query resolution, or scene attachment support.

#### Scenario: Reference follows ownership transfer
- **WHEN** a referenced widget is detached and attached to another parent
- **THEN** its weak references still resolve to the same live widget

#### Scenario: Tree destruction invalidates references
- **WHEN** an owner releases a tree with weak references to its root and descendants
- **THEN** each widget's weak references become invalid before its destructor executes and remain invalid afterward

#### Scenario: Detached references survive former parent
- **WHEN** a referenced subtree is detached and retained while its former parent is destroyed
- **THEN** references to the former parent become invalid and references to the retained subtree remain valid
