# Tasks

All 24 tasks are complete. Implementation, browser acceptance, fresh independent-checkout verification and the final evidence audit are complete. The user confirmed all native Debug/Release visual checks passed by direct observation. See validation.md for executed checks and evidence provenance.

## 1. Confirm integration boundaries

- [x] 1.1 Build a bounded SDK 6.0.9 WebGL 2/OffscreenCanvas fixture using the existing application-worker startup model; verify actual Chrome Debug/Release drawing, canvas transfer, resize, context-loss notification and teardown, and record exact headers/settings and commands.
- [x] 1.2 Trace and record the exact CoreScene, CoreAssets, camera, static-mesh CPU data and glTF parser source/dependency boundary; identify desktop-only references and concrete extraction points, and verify the proposed manifest excludes Render/DX12, UI, VFX, physics and desktop tools.

## 2. Scene and asset portability

- [x] 2.1 Add an explicit demo runtime profile with isolated source/module/dependency lists and native validation selection; verify graph audits, missing-source diagnostics and unchanged existing preset definitions.
- [x] 2.2 Port required CoreAssets and scene foundational sources using the established exception-free Wasm policy, including scalar Transform operations and the user-approved normalization-validity correction; verify Wasm compilation and focused native/browser ownership and error-path tests.
- [x] 2.3 Isolate CPU mesh decoding and asset views from desktop GPU material/rendering types; load the recorded cube.gltf/cube.bin through Nau assets and verify geometry, normals, indices and missing/corrupt-input diagnostics in focused tests.
- [x] 2.4 Integrate real scene initialization, updates and asynchronous shutdown with the shared checked framework independently of full Graphics/UI/VFX; verify scene activation and pending component work at Stop in native and browser fixtures.
- [x] 2.5 Extract shared cube/camera construction and Y-axis rotation from NauDemo's native adapter; verify 90-degree rotation after two seconds accumulated simulation time and compile the native demo with its existing material/environment setup.

## 3. Browser rendering service

- [x] 3.1 Add a renderer service and canvas bridge with application-worker graphics ownership, checked readiness and page-owned DOM lifetime; verify startup success, absent/invalid canvas and unavailable-context failure without changing PlatformApp geometry/context contracts.
- [x] 3.2 Implement mesh upload, simple blue diffuse shaders, directional light, perspective projection and depth-tested drawing from real scene/asset data; verify matrix provenance, shader failure reporting, occlusion and distinct rendered orientations.
- [x] 3.3 Connect drawing to completed scene updates at the existing nominal cadence; verify no page-side rotation, no extra game updates from executor wakes, foreground progress and bounded hidden-tab resumption.
- [x] 3.4 Implement ordered CSS-size/pixel-ratio propagation and owner-side drawable/viewport/projection updates; verify non-square resize, multiple pixel ratios, graphics-limit handling and zero-size recovery.
- [x] 3.5 Integrate context-loss and host-loss reporting with safe renderer teardown; verify terminal Failed, detached late callbacks, no new submissions after Stop/failure observation and no automatic context recreation.
- [x] 3.6 Verify Stop during asset/graphics initialization and pending scene work, repeated Stop and successful running shutdown; assert work settlement, resource ownership order, accurate cleanup completion and reload-to-retry behavior.

## 4. Actual NauDemo build and delivery

- [x] 4.1 Add web-demo-debug/web-demo-release presets and the actual NauDemo browser entry adapter with static modules; verify one entry point, consistent pthread options and real application linking in both configurations.
- [x] 4.2 Add browser-specific material/shaders, configuration and virtual asset mounts; verify actual cube loading without desktop shader cache, source-directory definitions or native DLL inputs.
- [x] 4.3 Stage runtime, mesh/buffer, material/shaders, configuration and hosting helpers from current inputs; verify clean/stale-output inventories and explicit missing-input failures in both packages.
- [x] 4.4 Provide the canvas delivery page with status, Stop and preflight diagnostics; verify responsive controls, required isolation/graphics checks, startup-load failure reporting and fresh-canvas reload behavior.

## 5. Integrated acceptance

- [x] 5.1 Extend the browser runner to test actual NauDemo Debug/Release packages with structured results, tolerant rendered-image checks and scene/asset provenance; verify blank output and deliberately broken assertions fail the runner.
- [x] 5.2 Run visible cube/rotation/camera, resize/pixel-ratio/zero-size, visibility, normal/repeated Stop, initialization/pending-work Stop, asset/shader/context failures, context/host loss and reload cases in both configurations; retain screenshots and diagnostics linked to each spec scenario.
- [x] 5.3 Copy both packages outside the checkout and serve under a different nested URL; verify rendering and orderly Stop with no source-tree/SDK requests and no stale asset dependence.
- [x] 5.4 Build native NauDemo in Debug/Release and visually check its retained appearance; run affected native scene/asset/lifecycle suites and existing native/browser minimal acceptance, verifying unchanged non-rendering graphs and timing.

## 6. Documentation and evidence

- [x] 6.1 Update NauDemo README, engine browser build documentation, root build.md and prerequisites.md with exact commands, profile boundaries, graphics requirements, package layout, timing limitation and simplified material scope; verify commands match implemented entry points.
- [x] 6.2 Execute the documented demo Debug/Release procedure from a fresh checkout with recorded dependencies and explicit SDK setup; record environment/tool/source identities, successful rendering/Stop and absence of generated-file edits or required workstation paths, separately from working-tree build evidence.
- [x] 6.3 Review every spec scenario against recorded evidence and record affected repository revisions, unresolved limitations and scope audit in validation.md; leave incomplete or unexecuted checks pending and verify strict OpenSpec validation.
