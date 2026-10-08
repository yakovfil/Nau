# Design

## Context

See proposal.md for motivation and specs/portable-scene-rendering/spec.md for observable requirements. This is a cross-module change requiring a design.

- `cmake/NauPackagedProjectRuntime.cmake` builds the portable PlatformApp/CoreAssets/CoreScene/CoreSceneFormats graph. CMake and `tools/asset_tools/packaged_project.py` currently admit only `non-rendering-scene`.
- `prepare_packaged_project.py` cooks scene/mesh data but retains material metadata as passive payloads. Presence checks are not renderability checks.
- `modules/browser_renderer` owns one mesh/program and clears the drawable inside each draw; it also presents screen text. `assets_cpu` restricts glTF to one mesh/primitive, non-interleaved positions/normals and 16-bit indices.
- Native `GraphicsScene` already observes scenes, but the Graphics graph includes animation, input, VFX and the full material/render-graph pipeline. Reusing that observer while also introducing a portable observer would duplicate scene ownership.
- `modules/render` contains the existing DX12 driver. `tests/test_render/test_std_swapchains.cpp` demonstrates direct driver initialization/teardown without Graphics. Its CMake still has desktop dependencies including DXC; it is not a ready-made portable target.
- `ICameraManager` provides world camera snapshots and main-camera selection. The common host's post-update callback follows the scene-manager call but is not a fence for asynchronous work.

## Goals / Non-Goals

**Goals:** Keep application logic, scene selection and renderable content semantics common; keep graphics resource execution with the platform owner; reuse the existing native driver; make supported content and failure behavior explicit.

**Non-Goals:** A general rendering hardware abstraction, a replacement for full Graphics, PBR/material graphs, texture sampling, shadows, animation/skinning, transparency, arbitrary glTF support, light components, input, editor UI changes, multi-window rendering or automatic device recovery. The original editor main scene is not promised equivalent appearance in this profile. Runtime mesh/material replacement and asset hot reload are deferred; object activation/removal and ordinary transform/visibility updates are supported.

## Decisions

### 1. Separate profile and isolated build selection

Add `basic-rendering-scene` to the existing versioned project declaration; retain version 1 and all existing non-rendering inputs. Add a rendering section with explicit material mappings and simple lighting settings. CMake, Python preparation and generated runtime policy must validate the same fields. A logical scene-presentation module selects platform adapter dependencies internally; projects do not maintain per-platform module lists.

Use separate profile/platform/configuration build and delivery paths for new rendering builds, while preserving existing non-rendering paths. EditorProject batch launchers explicitly select the rendering declaration; direct build-driver calls retain their non-rendering default. Reuse `-Declaration` and the existing shared build driver rather than adding parallel scripts. The prepared archive's profile must match its selected declaration. Explicit prepared-archive mode still bypasses asset cooking; target shader compilation remains an ordinary build dependency.

Alternative: changing the default non-rendering profile would invalidate its exclusion and startup contracts. That is deliberately avoided. The new spec supplements those contracts rather than weakening them.

### 2. Shared scene presentation, narrow backend interface

Add a module under `modules/scene_renderer` (working name) which owns scene membership, asset requests, readiness and a frame snapshot. Register through existing service/component lifecycle interfaces. Capture scene state on the scene owner thread, using engine synchronization for any unfinished scene work; do not assume post-update has completed asynchronous updates. Use component world transforms, not just parent-object transforms, and camera-manager snapshots for the active/default world. Select its main camera using existing semantics, including its existing fallback; do not invent a second camera-priority system.

Frame data contains camera properties, copied matrices, stable component/asset identities, visibility and references to immutable prepared resources. Backends receive no live SceneObject pointers. Registration/removal uses stable identities and generation/lifetime checks so asynchronous loads cannot resurrect removed components. Cache geometry by asset identity; repeated instances share the resource. New supported objects may appear after their resources are ready; failures remain terminal. Track submitted-frame resource ownership until GPU completion permits release.

The interface is limited to resource preparation/release, drawable status, frame submission and shutdown. Use one begin/clear, all opaque draws and one end/present per frame. Scene transforms, camera selection and material interpretation stay above the backend. Projection conversion for each clip-space/depth convention stays below it. Normal matrices use inverse-transpose transforms. Reject non-finite/singular transforms and unsupported reflected scale explicitly; positive non-uniform scale is required.

Alternative: generalizing the demo's `draw(mesh, camera)` call alone cannot support safe resource membership and multiple-object frames. Extracting the entire GraphicsScene is substantially broader and brings excluded feature systems.

### 3. Reuse DX12 Render and WebGL, without a second native driver

Create a Windows adapter implementing a minimal opaque pass using the existing Render driver's buffers, shaders, render targets, commands and swapchain APIs. Reuse or extract only the initialization/resize/teardown helpers it needs; do not instantiate GraphicsScene, the full render graph or its second scene observer. Explicitly configure Render and its required bundled/Windows dependencies in this profile. Keep this target selection separate from the full desktop and minimal graphs. First implementation checkpoint is a real driver-backed triangle, resize and shutdown in the packaged scene graph, including a link audit. This verifies the extraction boundary before layering assets and scene membership onto it; a failing checkpoint must be repaired within the chosen backend, not silently replaced with a new D3D11 or other renderer.

Build the minimal HLSL shaders with the existing native DXC/shader tooling, delivering generated bytes as target resources. The browser adapter uses corresponding GLSL sources and never depends on native shader tools in its target graph. Shaders are versioned renderer implementation resources, not per-platform recooks of project content; archive bytes stay identical.

Refactor BrowserRenderer's context, mesh and frame operations so several geometry resources can be drawn between clear and present. Keep a compatibility facade for NauDemo's existing entry points and its text pass, or adapt its platform presentation code while preserving appearance and lifecycle. Do not generalize screen text or port NauDemo to the new project profile in this change.

Alternative: a fresh native GPU backend could be small initially, but duplicates device/window/resource lifetime and would undermine the unification goal. Linking full Graphics avoids driver extraction but introduces an unrelated renderer pipeline and feature graph.

### 4. Explicit content subset and portable material mapping

Keep the first mesh subset intentionally bounded: one indexed triangle primitive per geometry asset, float32 positions/normals, uint16 indices, one external buffer, finite attributes and in-range indices. Multiple geometry assets and repeated instances are supported. Optional UV/tangent attributes may be validated without being consumed. Use native cooking to emit the supported representation; where cooked layout differs, normalize supported static data in preparation with checked bounds and stable asset identities. Unsupported source features fail rather than being stripped. Keep the existing bounded loader protections and add focused acceptance for actual cooked fixture output.

Define versioned portable material JSON containing only opaque linear RGB base color. The rendering section maps source material UIDs to these records, with an optional explicit default record for meshes with no material reference. Missing mappings fail. This mapping is an intentional authored choice of simplified appearance, recorded in the generated manifest; it does not claim to translate a desktop PBR material. Both targets resolve the same mapping and records. Never use object names or hard-coded fixture paths to select materials.

Define one normalized world-space direction toward the light, ambient RGB and directional RGB in common rendering configuration. Both shaders compute `baseColor * (ambient + directional * max(dot(normal, lightDirection), 0))`, clamp to the display range and apply the same documented linear-to-display conversion once. No scene light component is required. Reject invalid colors, direction and unsupported fields/version with identifying errors.

Preparation validates this complete renderable closure and packages the scene, asset database, geometry buffers, materials and rendering settings. The shared runtime revalidates selected prepared inputs so bypassing cooking does not bypass safety or feature checks. Freshness includes declaration/mapping/material changes. Preserve scratch cooking, immutable authored inputs and failure-safe publication.

Alternative: automatically reducing every native material to an arbitrary color would conceal unsupported content; supporting native material graphs on WebGL is outside the milestone.

### 5. Presentation readiness and ordered shutdown

Extend the packaged application composition with an optional presenter selected by profile; the non-rendering branch has no presenter. Service initialization creates platform resources, while checked application startup awaits scene activation, required asset readiness and one submitted frame. Startup presentation uses lifecycle progress, not ordinary game updates. Once Running, capture and submit through post-update with the real scene synchronization described above. A zero-sized drawable suspends submissions; startup remains pending and Stop-responsive until an initial frame can be submitted.

Implementation inspection found that optional graphics polling currently exists only in `browser_runtime.cpp`, while native `ApplicationImpl::pollLifecycle` only advances executor/startup/shutdown work. The user approved extending the change with a generic common-host hook. Add `IApplicationRuntimeService::pollApplicationRuntime() -> Result<>` in the application framework and invoke it from the shared lifecycle on its owner thread. Adapt the existing `IBrowserRuntimeService` interface to forward its legacy method through the generic contract and remove browser scheduling's separate dispatch. Define registration/cleanup eligibility explicitly so a service can return a harmless no-op before presentation setup and after its own shutdown, and no released services are called. Runtime errors are retained by the shared application lifecycle and request Stop, so the native runner returns nonzero and browser status observes the same failure. The host references only this generic interface and has no scene or graphics dependency. Independent common-host consumers verify progress during pending startup, once-only compatibility forwarding, failure gating, cleanup progress and lifetime on both platforms.

Shutdown order: stop accepting frames and new loads; settle/cancel accepted scene and asset work; drain submitted GPU work; release per-frame and cached resources, shaders and render targets; release driver/context; then allow owning platform/window teardown. Partial initialization follows the same eligible cleanup ordering. Resource cache owners cannot outlive driver teardown. Preserve failure even when cleanup succeeds. Device/context loss is terminal; no recovery loop is added.

### 6. Dedicated editor-authored acceptance scene

Add a separate rendering declaration and authored scene in EditorProject using its shared portable entry. Preserve its existing main scene and default declaration. Fixture geometry includes at least two distinct supported assets and repeated instances, overlapping objects, parent and component offsets, positive non-uniform scale, distinct colors and a camera. Existing project components drive observable motion; a separate observer/probe validates changes, camera selection, removal and resource cleanup without adding test hooks to production demo code.

Compare semantic output rather than exact cross-backend pixels: projected object regions, occlusion, color regions within documented tolerances and visible movement under controlled steps. Pair screenshots with independently inspected scene/resource IDs and archive hashes. Exercise relocatable production deliveries as well as probes, native and real-browser Debug/Release. Fail tests on blank output, graphics warnings indicating leaked live resources, timeout, unexpected startup success or missing terminal cleanup. A GPU fault-injection seam may test device failure propagation independently of platform-supported real context loss; clearly distinguish those results.

## Risks / Trade-offs

- Render's CMake/initialization may rely on full-desktop assumptions -> make the direct-driver triangle/resize/shutdown and graph audit the first executable checkpoint; record required native dependencies explicitly.
- Cooked editor geometry may exceed the current CPU subset -> normalize only supported layouts and reject unsupported features; keep acceptance content explicit and do not claim arbitrary project support.
- Native/browser color, handedness and depth conventions differ -> paired geometric/color tests and explicit shader/projection conversion; no exact pixel promise.
- Asynchronous scene work can race frame capture or removal -> snapshot at a real scene synchronization boundary and retain resources through accepted work, rather than forwarding live pointers.
- Shared renderer changes can break NauDemo text or shutdown -> maintain the compatibility path and run its native/browser visual and lifecycle regressions.
- A new profile adds maintenance beside full Graphics -> share the driver and scene/asset services; limit the adapter API to the agreed pass rather than growing a competing full renderer.

## Migration Plan

Introduce profile parsing and isolated targets first, then the Windows driver checkpoint, shared assets/presentation and WebGL integration. Add the opt-in EditorProject content and common build invocation only after both adapters are available. Document prerequisites and supported content next to the packaged-project guide. Direct build-driver invocations remain non-rendering unless explicitly selecting the new declaration. Following the user-approved launcher change, run_windows.bat and run_web.bat explicitly select portable_rendering_project.json by default. Rollback is selecting the prior declaration and its separate output directory; no authored main-scene conversion or destructive migration is required.
