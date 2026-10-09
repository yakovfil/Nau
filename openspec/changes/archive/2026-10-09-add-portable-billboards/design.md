# Design

## Context

See proposal.md for motivation and the portable-scene-rendering delta for the behavior contract.

- `modules/scene/include/nau/scene/components/billboard_component.h` already reflects texture, visibility and screenPercentageSize. Size and texture-dirty members currently lack explicit initializers.
- Legacy `graphics` uses BillboardsManager and `billboards.hlsl`: square quads offset in projected coordinates, screen-width sizing, alpha cutoff 0.01 and opaque depth behavior. GraphicsScene propagates component world position, size and visibility. This full graphics path is not the portable SceneRenderer.
- `modules/scene_renderer/include/nau/render/scene_backend.h` currently carries only CPU mesh draws. Its native backend uses Render/DX12, and its browser backend uses the browser renderer's context. Shared lifecycle owns startup, updates and checked cleanup.
- `modules/assets_cpu` supplies checked CPU mesh loading, but no equivalent texture view. `tools/asset_tools/prepare_packaged_project.py` records referenced textures as passive data. Normal asset-tool texture cooking targets DDS, which is not the chosen portable payload.
- NauDemo's rendering declaration permits scene, camera and static-mesh components plus project scripts. Its authored rendering scene is `content/scenes/portable_rendering.nausd_scene`. Existing production tests launch relocated packages and a nested browser URL.

## Goals / Non-Goals

**Goals:** Extend the existing component and shared renderer contract without duplicate demo draw code; preserve asset identities from authored scene through preparation to GPU resources; make rendering failures and cleanup observable in both builds.

**Non-Goals:** New billboard component types, general textured mesh materials, legacy renderer replacement, automatic device recovery, runtime file hot reload, soft transparency, world-size mode, batching/instancing optimizations or an editor UI redesign. A texture-reference change is supported; editing source pixels requires normal asset preparation/rebuild.

## Decisions

### 1. Reuse the existing scene component and profile

Keep serialized field names and public setters. Initialize size to 0.1f, visibility to true and the dirty flag deterministically. Validate finite positive size and finite world position in portable scene extraction and preparation when fields are authored. Do not impose mesh determinant/normal-transform checks on billboards: only the resulting translation contributes to the draw.

Enable the component in NauDemo's rendering declaration. Keep the non-rendering declaration and legacy graphics semantics unchanged. Adding another scene component would split authoring and serialization unnecessarily.

### 2. Match existing square, screen-width-relative geometry

Let `s` be screenPercentageSize, and `W,H` the drawable dimensions. Project world position with the shared view-projection matrix. Reject centers with nonpositive homogeneous w or depth outside the shared clip interval. Form corners using NDC offsets `(+-s, +-s * W/H)` and preserve center depth. Multiplying offsets by clip w before adding to clip xy keeps homogeneous clipping valid. Full pixel width and height are `s * W`; this is neither a fixed pixel count nor a percentage of viewport height. Zero drawable size follows existing suspension.

Use explicit, equivalent UV orientation and backend depth conversion. Quads remain screen-aligned even when the camera rotates. Rotation/scale of ancestors can move the world position but cannot size or rotate the quad. Source PNGs map to the whole square; automatic source aspect preservation is deferred to avoid changing legacy geometry semantics.

### 3. Prepare bounded, backend-neutral texture data on the host

Extend preparation to distinguish render-required billboard textures from passive references. Resolve metadata and source PNGs, preserve their authored UID mapping before scene compilation, and publish texture payloads with that identity instead of leaving them as PassiveData. Register a distinct portable texture asset kind for the CPU loader; reuse of a texture by several billboards produces one payload. Do not introduce a second user-authored mapping when TextureAssetRef already identifies the asset.

Use Pillow in the existing Python preparation process for single-image 8-bit RGB/RGBA PNG decoding. It is already used by visual tests, but it is not currently a guaranteed preparation dependency: document and explicitly preflight it with the actual host Python interpreter before preparation starts. Unsupported PNG modes/bit depths and animated images fail with a source diagnostic rather than implicit conversion. Treat RGB bytes as sRGB and alpha as linear; do not apply embedded color-profile transforms. RGB sources acquire alpha 255.

Write a versioned, little-endian portable texture header (magic, version, width, height, RGBA8 format and payload length) followed by top-row-first tightly packed pixels. Initial limits: each dimension 1..4096, payload at most 64 MiB, checked width*height*4 and exact file length. Check input dimensions/mode before decoding and enforce limits again in the C++ loader before allocation. Tests fix canonical header encoding, orientation and pixel bytes. PNG decompression stays out of runtime. The archive envelope does not change.

Alternatives: DDS cooking couples the portable subset to desktop formats; runtime PNG decoding adds codecs to both builds. Host normalization costs archive size, but makes upload behavior simple and deterministic for this limited feature. Existing preparation scratch/publication rules remain authoritative, including dependency tracking for PNG and metadata changes.

The user approved stabilizing generated prepared-scene identities after repeated cooking exposed random object/component UIDs. Normalize cooked scene containers before packaging: preserve every UID authored in the composed USD scene, assign UUIDv5 identities to generated object/component IDs using the scene asset UID and stable serialized local IDs/component slots, and remap matching references consistently. Preserve hierarchy, authored asset references and component values. Canonicalize block/object ordering and validate uniqueness. This applies to the rendering profile's prepared scenes, including validation scenes, without changing authored sources or the legacy cooker. Repeated preparations must produce the same archive with unchanged inputs; changing an input must change the relevant payload. Use source-preserved timestamps in the asset database rather than scratch-directory publication time if cooking introduces transient times.

The generic USD component adapter also needs a specific billboard metadata-reference conversion: resolve the authored texture asset metadata to its UID before assigning TextureAssetRef, while retaining the original authored USD asset attribute. Preparation checks the resulting cooked identity before publication.

### 4. Add typed CPU texture ownership and shared frame data

Add CpuTextureView plus loader/factory beside CpuMeshView, preserving typed TextureAssetRef identity while requesting the CPU view. The view owns immutable decoded RGBA8 data. Extend SceneFrame with separate billboard draws containing component identity, texture identity/view, world position and screen-relative size. Backend caches reuse one GPU texture per shared asset view; different views for replacement references cannot alias stale data. Include billboard identities in the existing observer contract for independent tests.

SceneRenderer enumerates billboards in the active world and resolves textures through the existing asset system. Initial required loads and uploads must finish before the initial frame succeeds. During a reference change, omit that billboard until the new asset is ready, retaining errors; do not display its old texture as the requested replacement. Associate pending work with component UID and requested texture so removal or a newer request invalidates stale completions. Re-evaluate live scene state rather than retaining raw component pointers across asynchronous work. A missing texture on an active required component is an error, not a placeholder.

### 5. Implement a small dedicated billboard pass in each backend

Upload RGBA8 textures once, draw quads with an unlit shader, and use linear clamp sampling without mipmaps. Convert sampled sRGB RGB to linear consistently with the current scene output conversion; alpha remains linear. Native and browser implementations must avoid double sRGB decoding/encoding. A known-color fixture tests this boundary.

Use the fixed alpha threshold 0.01, no blending, depth test and depth writes. Retained fragments output alpha one. Draw meshes and billboards in the same frame/depth target; discarded pixels never write depth. Extend `NauSceneRendererShaders.cmake` delivery/embedding for the new HLSL and browser shaders. Own and restore/bind all required render state, including sampler, texture, shader and depth state.

Prune unused textures only when submitted work no longer needs them; release caches, samplers and billboard shader resources before stopping the backend context/driver. Follow the existing pending-startup and Stop contract, including partial initialization and upload failure. No new common-host lifecycle mechanism is planned.

### 6. Demonstrate through authored content and test externally

Add a small asymmetric RGBA marker PNG with distinct corner colors and transparent holes, plus metadata and a billboard in the demo's authored rendering scene. Place it near existing geometry so both marker and scene remain visible. Use the normal asset pipeline and root launchers, without HTML or demo-only render calls.

Use unit/fixture tests for dimension/size errors, pixel orientation, reference identity, shared resources, texture replacement, visibility/removal and Stop during pending work. Extend production visual tests for visible marker output and existing mesh motion. Controlled test scenes/camera changes verify distance and field-of-view independence, camera facing, nested transforms, occlusion, viewport edge/near-plane behavior and resize/DPR/zero-size recovery. Test controls belong in fixtures, not production demo hooks. Run Windows/Web Debug/Release, reusing the same prepared archive; record tolerances, hashes and commands. Re-run affected legacy billboard and non-rendering checks.

## Risks / Trade-offs

- Raw texture payloads enlarge archives: cap dimensions and use a small demo marker; compression is deferred.
- Pillow is available for tests but may be absent in a host SDK Python: explicit preflight and generic installation instructions make this a reported prerequisite.
- Different UV, sRGB and clip conventions can produce misleading partial success: asymmetric colors, occlusion and camera-plane fixtures exercise the actual submitted image.
- Alpha cutout has hard edges and does not model smoke: use a marker texture and document the subset.
- Asynchronous loads may outlive components or Stop: immutable view ownership and request-identity checks prevent stale submissions; inject failures and pending-load Stop in tests.
- Legacy billboard members have unspecified initial state today: deterministic defaults preserve explicit authored values; targeted legacy regressions verify the change.

## Migration Plan

Land component defaults and texture preparation/loading, then shared draw data and both backends, then demo content and acceptance. Existing archives without billboards remain valid. New billboard archives require the updated renderer/loader and matching component declaration. Rebuild host preparation tools and runtime consumers together. Rollback restores the prior demo scene/declaration and rebuilds its archive, then reverts the added loader/backend paths; no authored-source conversion or archive-format migration is required.
