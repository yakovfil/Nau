# Tasks

## 1. Component and portable texture contract

- [x] 1.1 Initialize BillboardComponent size and dirty state deterministically while retaining existing reflected fields and setters; verify construction, explicit values and scene serialization round trips with component tests.
- [x] 1.2 Add the versioned bounded RGBA8 payload contract and CpuTextureView loader/factory to assets_cpu; verify canonical pixel bytes, RGB alpha expansion fixtures, truncated/oversized/overflowing/unsupported headers and exact payload lengths in native and Emscripten tests.

## 2. Host preparation and asset identity

- [x] 2.1 Add host PNG normalization and Pillow prerequisite checks using the selected preparation interpreter; verify RGB/RGBA success, rejected modes/bit depths/animation, dimension limits and actionable missing-decoder diagnostics with Python tests.
- [x] 2.2 Extend prepare_packaged_project.py to resolve billboard texture references, register preserved UIDs before scene compilation and emit one portable payload per texture; verify cooked scene references resolve to actual pixels and repeated references share an identity in a prepared fixture.
- [x] 2.3 Include PNG/metadata changes in preparation dependencies, stabilize generated prepared-scene identities and matching references while preserving authored UIDs, and preserve safe publication; verify identity/reference uniqueness, byte-identical repeated archives, changed pixels in a fresh archive, and missing/corrupt source failures without authored-file changes or stale success. Confirm non-rendering preparation remains usable without new texture decoding requirements.

## 3. Shared renderer integration

- [x] 3.1 Extend shared frame/observer data with billboard draws and extract active-world component positions, sizes, visibility and identities; verify billboard-only scenes, finite-positive size checks, nested transforms and selected-camera behavior in renderer fixtures.
- [x] 3.2 Add asynchronous CPU texture resolution with request identity checks and initial readiness gating; verify shared references, live texture replacement, load failure, visibility changes, component removal and stale completion rejection without retaining component pointers across loads.
- [x] 3.3 Implement or share the billboard projection contract, including square screen-width sizing and camera-depth rejection; verify distance/FOV independence, parent scale/rotation behavior, viewport edge clipping, near/far bounds and zero-drawable suspension with mathematical/scene fixtures.

## 4. Windows and browser rendering

- [x] 4.1 Add native billboard shaders, shader delivery, texture upload/cache and alpha-cutout depth rendering to the native scene backend; verify distinct corner colors, texture orientation, shared upload, mesh/billboard occlusion and unchanged mesh output in a native checkpoint.
- [x] 4.2 Add equivalent browser billboard shaders, textures and render state to the browser scene backend; verify the same texture/occlusion checkpoint in a real browser, including resize, DPR changes and color tolerances.
- [x] 4.3 Integrate texture/shader/sampler resource cleanup with existing backend lifecycle; verify partial initialization/upload failures, graphics loss, removal of shared users and repeated Stop during pending preparation without later submissions or shutdown leaks on both backends.

## 5. NauDemo and usage documentation

- [x] 5.1 Add an asymmetric alpha-cutout PNG, metadata and authored billboard to NauDemo's rendering scene and declaration; verify both root launchers display it alongside existing moving geometry from the prepared archive without demo-specific rendering or HTML overlays.
- [x] 5.2 Document constant screen-relative size, square mapping, alpha cutoff, supported PNG subset, generic host decoder setup and shared package usage in module/demo documentation; verify documented configuration and commands match the shipped helpers and avoid machine-specific prerequisite paths.

## 6. Integrated acceptance

- [x] 6.1 Extend rendering acceptance fixtures and the existing production visual scripts to cover billboard identity, visible pixels, distance/FOV sizing, camera facing, live changes/removal, cutouts, depth, viewport edges, resize and zero-size recovery; verify assertions use independent expected geometry/colors and documented tolerances without production test hooks.
- [x] 6.2 Build and run Windows Debug and Release production packages outside the checkout; verify billboard and mesh output, texture failures, startup/Stop behavior and clean closure, retaining logs/screenshots and archive hashes.
- [x] 6.3 Build and run Web Debug and Release under a nested URL using the same prepared archive as Windows; verify equivalent output/identity, DPR/resize behavior, texture failures and repeated Stop, retaining logs/screenshots and archive hashes.
- [x] 6.4 Run affected legacy billboard sample/component, non-rendering packaged-project, shader-delivery and common-host regressions; record commands, tool versions, revisions, pass/fail evidence and any unexecuted checks in validation.md, and run strict OpenSpec validation before marking the change complete.
