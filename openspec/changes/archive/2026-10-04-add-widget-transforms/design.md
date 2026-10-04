# Design

## Context

See proposal.md for motivation. NauWidget currently stores name, visibility, a weak parent, and ordered exclusively owned children. NauUi publicly links CoreScene, which already exposes kernel math. Existing headless tests and the tests/consumer fixture support native, Emscripten, and relocated SDK validation.

Kernel math::Transform stores Vector3 translation/scale and Quat rotation, provides isValid(), and converts to Matrix4 using T * R * S. Its transform multiplication returns decomposed TRS state rather than a general affine matrix. scene::TransformControl also requires world-transform mutation; adopting that interface would introduce semantics beyond this widget foundation.

## Goals / Non-Goals

**Goals:** Add validated local geometry and exact affine ancestry composition within NauWidget, retaining its caller-controlled single-thread access model and portable dependency closure.

**Non-Goals:** No transform-control inheritance, inverse/world setters, preserve-world reparenting, caching, scene coordinates, rendering, geometry submission, layout, input, persistence, or production subclasses. Size is a rectangle extent, not scale or a layout constraint.

## Decisions

### Store engine TRS and two-dimensional geometry

Add math::Transform m_localTransform, math::Vector2 m_size, and math::Vector2 m_pivot. Initialize identity, (0, 0), and (0.5, 0.5). The engine 3D transform and parent-pivot origin are user decisions. Zero size and centered pivot are the proposed defaults carried into this plan. Use the existing vector type instead of introducing a parallel geometry library or a 3D size with unused depth.

Expose localTransform() as a const reference, size()/pivot() as values, and Result<> setters setLocalTransform(), setSize(), setPivot(). Do not expose mutable references or duplicate component setters in this increment; callers can edit a transform copy and submit it. Names follow the existing widget accessors. Keep reflection and serialized fields for the deferred persistence change.

### Pivot defines origin; size describes geometry around it

For normalized rectangle coordinates u and v, local point = ((u - pivot.x) * width, (v - pivot.y) * height, 0). Thus minimum = -pivot * size and maximum = (1 - pivot) * size. Document this formula and test representative points; no bounds or rendering API is required yet. Coordinates follow engine math axes; assigning screen-up/down or pixel units belongs to future presentation.

Parent pivot is the child's coordinate origin. Parent size/pivot are absent from child matrix composition. A corner-based origin was rejected in discussion because resizing or changing pivot would reposition children. A child pivot edit moves its own rectangle around its fixed transform origin, without moving descendant origins. Finite external pivots are allowed instead of clamping to the rectangle.

### Accumulate matrices on demand

Expose math::Matrix4 accumulatedMatrix() const by value. Begin with the widget's local matrix and iteratively pre-multiply each ancestor's local matrix. This avoids recursive stack growth and costs O(depth) time with O(1) temporary storage. A root still contributes its own local transform; accumulated coordinates are outside the root, not root-local or scene-world coordinates.

Use toMatrixWithScale() and matrix multiplication, never math::Transform multiplication or decomposition. A rotated child beneath a nonuniformly scaled parent can generate shear, which TRS cannot exactly preserve. On-demand evaluation avoids dirty propagation and stale caches during ancestor changes or detach/attach; caching can be considered later with profiling.

### Validate before assignment

Use math::Transform::isValid() for submitted transforms, including its existing squared-quaternion-length tolerance of 1e-3. Explicitly check each size/pivot component for finiteness and require nonnegative size. Reject invalid input with an error Result before mutation in every configuration. Accept finite signed and zero scale and external pivots. Do not normalize or clamp implicitly. Validation and const-only transform access avoid debug-assert-only enforcement.

These are planning defaults for error handling consistent with addChild's Result-based failure semantics. No inverse is needed, so singular transforms are useful and supported. Finite input does not promise overflow-free arithmetic for arbitrarily large values or deep hierarchies; use ordinary engine floating-point behavior.

### Reuse existing verification paths

Extend tests/test_widget.cpp with defaults, setters/rejection, quaternion and matrix behavior, rectangle formula, and subtree state preservation. Include three-level composition, nonuniform scale with rotation causing shear, negative/zero scale, and size/pivot edits that leave descendant origins unchanged. Compare matrices and points using tolerances and independently constructed expected matrices/points.

Extend tests/consumer/main.cpp so native, browser Node execution, and relocated SDK consumption exercise the public geometry API and representative composition/rejection behavior. Retain all existing ownership tests. No visual application is necessary for this mathematical API.

## Risks / Trade-offs

- O(depth) per query can become costly for bulk drawing -> begin without caching; future rendering can traverse once and carry parent matrices.
- Confusing size with scale or pivot with a child offset -> document formulas and examples, with regression tests for independent effects.
- Native SIMD and browser scalar math differ slightly -> use non-boundary quaternion inputs and numeric tolerances in cross-platform checks.
- Extremely large finite values can overflow derived matrices -> document ordinary float limits; do not imply arbitrary-range geometry support.

## Migration Plan

This is an additive API change. Rebuild NauUi and its consumers because widget object size changes; there is no persisted widget format to migrate. Install and relocate a fresh SDK for consumer verification. Rollback consists of reverting the additive API, implementation, tests, and documentation together. Existing module selection and ownership semantics remain unchanged.
