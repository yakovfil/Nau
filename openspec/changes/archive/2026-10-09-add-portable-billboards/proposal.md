# Proposal

## Why

NauDemo's shared Windows/Web renderer cannot display the engine's existing BillboardComponent. Adding portable billboards lets the demo demonstrate scene-attached textured markers with the same authored content, constant screen-relative size and behavior on both platforms.

## What Changes

- Render existing BillboardComponent instances through the basic-rendering-scene profile on Windows and Web in Debug and Release.
- Keep camera-facing, constant screen-relative sizing: full billboard width is screenPercentageSize times drawable width; world position follows the component, while object rotation and scale do not size or rotate the quad.
- Support unlit PNG textures with alpha cutout and depth-tested occlusion. Preserve the existing square billboard geometry and fixed alpha cutoff for the first version.
- Prepare portable texture payloads with preserved asset identities in the same archive as scene geometry, with checked loading and graphics resource lifetime.
- Stabilize generated identities and their references in prepared rendering scenes so repeated preparation is deterministic while authored UIDs remain intact.
- Add an authored billboard and texture to NauDemo and extend production rendering validation.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `portable-scene-rendering`: extend supported scene content and frame presentation to textured billboards, define their sizing and appearance, and require cross-platform demo acceptance and failure checks.

## Impact

- NauEngineModules: scene component defaults; assets_cpu texture views; scene_renderer frame data, resource loading, native/browser backends and shaders; asset_tools preparation and validation; packaged-project documentation and tests.
- NauDemo: rendering declaration, authored scene and PNG asset, shared production acceptance tests and usage documentation.
- Host preparation may gain an explicitly checked PNG decoder dependency; runtime must not acquire desktop image-import, USD or Qt dependencies. Existing package format and BillboardComponent serialized field names remain compatible.
- Legacy desktop graphics and non-rendering profiles retain their behavior; no platform-specific demo rendering code is introduced.
- Out of scope: world-sized or axis-constrained billboards, soft alpha blending, particles, animation atlases, widget rendering, general textured mesh materials and new platforms beyond Windows/Web.
