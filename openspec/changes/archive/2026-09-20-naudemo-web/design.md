# Design

## Context

See proposal.md for motivation and scope. Inspection found:

- NauDemo/CMakeLists.txt links SampleCommonLib, Animation, Physics, Graphics and VFX, registers additional modules and depends on SceneBaseSample shader generation.
- NauDemo/src/main.cpp constructs real scene objects and rotates a StaticMeshComponent owner; it embeds source directories for configuration and assets. Its material references the desktop shader cache.
- SampleCommonLib pulls in NauFramework, CoreInput and imgui. The full framework links scene, Graphics, UI and VFX. Minimal framework source guards exclude scene update and shutdown integration.
- CoreScene depends on CoreAssets; GraphicsAssets also links Render and D3DCompiler.lib. Render selects drv3d_DX12 and Windows/SSE definitions. The existing graphics render-scene implementation contains deferred, shadow and material-manager machinery.
- Browser platform services own a DOM host without creating graphics contexts. Existing lifecycle contracts specify worker ownership, nominal 100 ms game steps, cooperative cleanup and reload to retry.

## Goals / Non-Goals

**Goals:** preserve genuine scene/asset ownership, establish a small renderer boundary, and keep graphics lifetime aligned with checked application startup and shutdown. Compile a deliberate dependency graph with native regressions.

**Non-Goals:** implementing the entire desktop Render API, emulating unsupported modules, changing existing minimal cadence or substituting JavaScript scene simulation. Simplified materials do not authorize hardcoding a second cube mesh in the renderer.

## Decisions

### Separate profile and shared lifecycle

Introduce a demo-specific profile and web-demo-debug/web-demo-release presets. Keep web-minimal presets and their explicit exclusion contracts intact. Factor scene participation out of the current all-or-nothing minimal guards so the demo can use real CoreScene/CoreAssets and shared initialization/update/shutdown without full Graphics/UI/VFX. Register exact selected modules statically. Avoid SampleCommonLib in the browser entry adapter; extract reusable demo scene construction and rotation into platform-neutral code.

### Small engine rendering service

Add an engine-side browser renderer consuming scene-derived mesh geometry, world transform, camera view/projection and light parameters. Render one opaque indexed mesh with depth testing and a simple blue diffuse material plus constant ambient term. Obtain mesh data through Nau asset loading; isolate CPU mesh decoding from desktop GPU asset views. Reuse recorded glTF parser sources where feasible rather than inventing a glTF parser or invoking desktop content tools. Unsupported asset/material features must diagnose failure rather than produce an apparently successful empty scene.

This limited service is an explicit new rendering path, not a claim that existing Graphics/Render are ported. Porting their full API would import features unnecessary for the accepted milestone. A page-side independent cube would not satisfy scene-driven rendering.

### WebGL 2 on the application worker

Select WebGL 2 with an OffscreenCanvas transferred to the application worker. Keep scene access, mesh upload, draw submission and graphics destruction on that owner. The page provides a canvas host before startup and owns its DOM lifetime. PlatformApp continues handling CSS geometry and host discovery; a separate rendering bridge transfers canvas ownership and supplies measured drawable size. Require the needed graphics capabilities and fail explicitly when unavailable; no second backend or implicit fallback in this milestone.

Emscripten documents worker-pinned OffscreenCanvas contexts and startup transfer with PROXY_TO_PTHREAD in its [HTML5 API](https://emscripten.org/docs/api_reference/html5.h.html) and [settings reference](https://emscripten.org/docs/tools_reference/settings_reference.html). These rolling documents are guidance, not evidence of SDK 6.0.9 compatibility. Task 1.1 must verify the exact installed SDK's headers/settings and actual worker rendering in Chrome before engine integration. WebGPU is deferred: the accepted opaque cube does not require a second graphics API integration.

### Shared transform portability and approved validity correction

The scene build requires Transform operations that the earlier non-rendering
Wasm core never instantiated. Use scalar element operations for finite checks,
scale masks, point conversion, comparison and diagnostic Euler formatting, while
retaining existing native branches and using shared per-element multiplication
where equivalent. Bundled math edits are limited to the scalar Vector3/Quat
indexed accessors: Release testing demonstrated invalid cross-member pointer
arithmetic, replaced with explicit member selection including Vector3's W lane.
Do not change native composition, inverse or normalization algorithms as part of
this port.

The user explicitly approved correcting the inverted isRotationNormalized
predicate. Both native and Wasm now require finite squared quaternion length
within 1e-3 of one. This tolerance accommodates the existing native approximate
reciprocal-square-root normalizer; a tighter 1e-4 rejected its output. Tests cover
identity, rotation construction, normalize() output, small roundoff, non-unit and
non-finite inputs. Separate transform geometry tests retain native numerical
accuracy; they do not authorize changes to its existing algorithms.

### Timing and presentation policy

Render the updated scene after each completed game step, retaining the shared nominal 100 ms cadence and bounded elapsed-time policy. The milestone accepts discrete visual updates; no 60 FPS claim or JavaScript interpolation is introduced. Rotation remains 45 degrees per second of accumulated simulation time. Hidden time is not replayed. Startup prepares a valid scene, assets and graphics resources before Running; rendering errors thereafter enter terminal Failed.

### Assets, dimensions and lifetime

Stage cube.gltf and cube.bin, explicit browser material/shaders and demo configuration alongside runtime outputs. Preload required data into a virtual filesystem before asset initialization; use package-relative URLs and stable virtual mount paths, never source-tree paths. Keep native materials and environment setup in the native adapter. Shader compilation is part of checked browser renderer initialization.

Measure CSS client size on the UI thread and send ordered size/device-pixel-ratio snapshots to the owner. Compute a nonzero drawable extent from CSS size and pixel ratio, within reported graphics limits, and update viewport and camera aspect together. Zero-area hosts suspend drawing until positive size returns without inventing a graphics failure. Resize callbacks must not access released resources.

Stop prevents new scene updates and draw submissions, settles pending asset/scene tasks, disposes scene resources and renderer objects before tearing down platform/executors, and reports completion only after ownership is accounted for. Context loss and host loss are terminal failures; detach callbacks and attempt safe cleanup without automatic context restoration or canvas reuse. Fatal aborts retain incomplete-cleanup reporting. Page reload creates a fresh canvas.

The authorized task 1.1 follow-up verified owner-side emscripten_is_webgl_context_lost polling in Debug and Release without Asyncify. Poll before each render operation and at bounded owner-loop intervals during startup/running/cleanup; latch failure and reject new draws once detected. Do not rely on OffscreenCanvas event callbacks: the existing C++ worker loop does not yield to JavaScript events. This retains the selected lifecycle and its cadence. The fixture detects actual WEBGL_lose_context loss and rejects a subsequent draw; production integration remains task 3.5.

### Validation boundaries

Test the actual NauDemo packages in Chrome on Windows, Debug and Release. Combine screenshots/pixel checks with renderer/scene diagnostics: a non-background image alone is insufficient evidence of Nau scene integration. Change scene transforms and camera parameters in a controlled fixture and observe corresponding submitted matrices and pixels. Check rotation against accumulated simulation time, not wall time spent hidden. Use tolerant image assertions rather than GPU-specific pixel-perfect goldens.

Cover resize, pixel ratio, zero-size recovery, missing/corrupt assets, invalid shaders, unavailable context, context loss, Stop during initialization/pending scene work, normal Stop, host loss and reload policy. Reuse delivery infrastructure for isolated hosting, nested-URL relocation and structured failures. Run native scene/lifecycle and existing minimal browser suites. Record a real fresh-checkout walkthrough separately from clean build-directory evidence; never mark absent execution evidence as verified.

## Risks / Trade-offs

- Scene headers or CPU mesh loading may still pull desktop graphics dependencies -> capture exact transitive sources and blockers in task 1.2; split CPU data contracts narrowly, with native tests. If this requires excluded systems, revise the plan before expanding scope.
- Canvas transfer may conflict with DOM sizing or the current worker startup -> prove transfer, resize, context loss and teardown in the pinned-SDK fixture before selecting production bridge details.
- Asynchronous scene/asset work can outlive renderer teardown -> explicit owner order and pending-work failure/Stop fixtures.
- Shared source guards may regress native behavior -> native Debug/Release scene tests and actual native NauDemo build/visual check.
- WebGL 2 is a bounded milestone and does not establish general desktop renderer portability -> document the supported feature set and fail unsupported requests explicitly.
- Ten scene updates per second are visibly discrete -> retain the established timing contract; smoother presentation is separate future work.

## Migration Plan

Implement and validate the backend feasibility fixture and CPU scene/asset boundary first, then the profile, rendering service and actual demo package. Keep existing defaults unchanged. Rollback selects existing native or minimal presets; new renderer modules must not be required by those profiles. Commit component changes in their owning repositories and record revisions in validation; no commit or publication is part of proposal generation.

## Open Questions

Exact CPU mesh-view extraction points, required parser source list and SDK canvas-transfer settings are to be measured by the bounded initial tasks. They may refine implementation names and manifests, but cannot relax real-scene ownership, the selected backend, lifecycle contracts or accepted visual scope without revising the plan.

### Integrated presentation correction

The task 1.1 fixture verified WebGL buffer contents and context lifetime, but did
not prove browser compositing. Actual-package screenshots exposed blank output:
SDK 6.0.9 emscripten_webgl_commit_frame explicitly documents its current no-op
implementation. Chrome presents a transferred canvas when its worker returns to
the JavaScript event loop. NauDemo therefore opts into cooperativePresentation
in the shared browser runtime. A heap-owned BrowserLoop polls at bounded timer
intervals on the same application worker and retains the original StepDeadline
policy. Existing minimal callers retain the blocking path. No Asyncify, graphics
proxy, alternate backend, page-side simulation or increased game cadence is used.
The demo delegate has static lifetime because the cooperative entry unwinds to
the worker scheduler. Completion destroys Application before force-exiting the
runtime with the checked result. Runtime services can report graphics failure
through IBrowserRuntimeService during startup/running/cleanup polls.

Renderer snapshots synchronously read page CSS size/DPR; no size observer retains
C++ renderer memory. These owner-requested snapshots are ordered by the loop and
avoid stale callback races. Dimensions are proportionally clamped to reported GL
limits, and zero-area hosts suspend drawing. Matrix serialization uses explicit
columns/components: Release integration exposed invalid scalar dynamic matrix
access; the renderer avoids it without additional bundled-library edits.
