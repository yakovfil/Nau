# Design

## Context

See proposal.md for motivation. The previous Cocos implementation is retired and the durable retirement specification must remain satisfied. The modules root discovers subdirectories in full builds; minimal and scene builds use explicit module lists. `screen_text/CMakeLists.txt` demonstrates a small static library with public include paths and SDK installation. Existing module tests use Google Test and CTest under `NAU_CORE_TESTS`.

This change establishes a new data model, so a design is required even though the implementation is small.

## Goals / Non-Goals

**Goals:** Establish stable object addresses, explicit ownership transfer, consistent parent/child relationships, and simple queryable state. Keep the foundation usable without application startup or service registration.

**Non-Goals:** All exclusions in proposal.md apply. Visibility is only data and an ancestry query; it does not trigger rendering or layout. No production subclasses, lifecycle callbacks, automatic reparenting, reference-counted handles, or global widget registry are introduced.

## Decisions

### One concrete, non-copyable, non-movable Widget

Expose `nau::ui::Widget` from `modules/ui/include/nau/ui/widget.h`, implemented in `src/widget.cpp`. Give it a public virtual destructor for future extension, but no abstract methods. Delete copy and move construction/assignment: moving ownership handles is sufficient, while moving widget objects would invalidate parent references. A test-only destructor probe is allowed; it is not a production widget derivative.

Use a process-local, immutable runtime ID and optional debug name. Default name is empty. IDs distinguish live objects and survive detachment/reattachment; they are not asset IDs or persistent identifiers. Use a monotonic 64-bit counter with explicit overflow guard rather than a registry or asset UID. Construction defaults to visible, no parent, and no children.

### Exclusive child ownership with borrowed parent references

Store ordered children as `std::vector<std::unique_ptr<Widget>>`; store the parent as a private `Widget*`, initially null. Provide const and non-const parent accessors and indexed child access with a child count. Do not expose a mutable ownership container or a parent setter. Borrowed pointers are valid only while their widget is alive; callers cannot delete attached widgets or manufacture a second owner from a borrowed pointer.

Prefer exclusive ownership to shared ownership because the tree has one clear lifetime owner and no reference cycles. Root ownership belongs to the caller; no UiRoot type is necessary.

### Validated attachment and explicit detachment

Use an attachment API equivalent to `Result<> addChild(std::unique_ptr<Widget>&& child)`. The rvalue-reference argument is validated before moving it into storage. On a contract-validation failure, the caller's owning handle and the tree are unchanged; a by-value parameter would destroy the rejected object unless the error also returned ownership.

Reject null, self-attachment, an already-parented child, and attaching an ancestor beneath its descendant. Walk this widget's parent chain to detect the latter. This matters even with valid unique ownership: a descendant can be asked to adopt the owning handle of its root. Do not write tests that invent duplicate unique ownership to simulate invalid inputs.

Successful attachment appends the child and sets its parent pointer. `removeChild(Widget& child)` returns the owning pointer only for a direct child, clears its parent pointer, and preserves the order of remaining siblings. A non-child returns an empty pointer without side effects. Reparenting consists of successful removal followed by attachment; no atomic cross-parent operation is included.

Destroying a parent destroys still-attached descendants exactly once. During teardown, clear each direct child's parent link before destroying it. Detached subtrees remain intact and can outlive the former parent. No callbacks are emitted during attachment, detachment, or destruction.

### Visibility is local state plus an ancestry query

Provide `isVisible()`, `setVisible(bool)`, and `isEffectivelyVisible()`. Effective visibility is true only when this widget and every ancestor are locally visible. Compute it on demand, avoiding cached subtree state and invalidation machinery. Hiding a parent never rewrites descendant flags. There is no hidden-versus-collapsed distinction because layout is excluded.

### A portable optional library

Create static target `NauUi`, using existing compile options and installation helpers, with no runtime module registration. Depend at most on NauKernel for established result/error support; no graphics, input, ScreenText, Cocos, Qt, USD, or native binary dependencies. Wire SDK import through the modules-owned SDK CMake integration if required by its existing export convention. No framework dependency on NauUi is added.

Full module discovery can build the new directory. Existing minimal/scene lists stay unchanged; a focused validation fixture can explicitly select the foundation to compile it with Emscripten. Unit tests live under `modules/ui/tests/`, run headlessly, and are gated by `NAU_CORE_TESTS`. No demo or visual sample is required.

### Threading and error scope

Tree and state access are confined to one caller-controlled thread, with no internal locking or dispatch queue. Runtime ID generation may use an atomic counter so separate trees can be constructed independently. Validation errors use the engine result convention, not exceptions. Allocation failure follows existing engine allocation policy and is not a recoverable attachment error promised by this API.

## Risks / Trade-offs

- Borrowed pointers can dangle after destruction -> document lifetime rules and test detachment/destruction boundaries; weak handles are deferred.
- Reusing `modules/ui` could be mistaken for restoring Cocos -> document the new target and API, keep legacy asset rejection and existing default profile selections intact.
- Recursive destruction consumes stack proportional to depth -> treat this as an ordinary application widget tree, not an untrusted arbitrary-depth graph; do not promise unbounded-depth support.
- Linear removal and ancestry queries -> acceptable for this small foundation; avoid indexes and caches until measured use warrants them.
- A headless foundation produces no visible UI -> acceptance is ownership/state tests, portability, and SDK consumption, not screenshots.

## Migration Plan

Add the library, tests, exports, and a brief module README. Existing consumers require no migration and legacy UI assets remain unsupported. Rollback removes the new target and its integration without changing application data. Build artifacts stay in ignored build directories; no generated artifacts are committed.
