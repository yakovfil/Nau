# Proposal

## Why

NauWidget has an ownership hierarchy but cannot describe spatial placement or rectangular geometry. Parent-relative transforms, size, and pivot provide the next foundation for future UI rendering without requiring layout or scene integration.

## What Changes

- Give each widget an engine 3D math::Transform relative to its parent's pivot.
- Add unscaled two-dimensional size and normalized pivot for a rectangle in the local XY plane.
- Expose accumulated matrices that preserve hierarchical rotation and nonuniform scale, including resulting shear.
- Preserve local geometry state through attachment and detachment; size and pivot edits do not move descendant origins.
- Validate spatial state consistently in native and browser builds and document coordinate semantics.
- Keep layout, input, rendering, persistence, scene attachment, and derived widgets outside this change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `widget-foundation`: Add local spatial state, pivot-relative geometry, and accumulated matrix requirements to the existing widget foundation.

## Impact

Changes are confined to NauEngineModules/modules/ui public API, implementation, documentation, and focused tests/consumer. Reuse kernel math through the existing CoreScene dependency; no new module or platform dependency is needed. Existing ownership, identity, visibility, and default module selection remain intact.
