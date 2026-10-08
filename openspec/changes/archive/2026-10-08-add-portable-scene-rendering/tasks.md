# Tasks

## 1. Profile and native driver integration

- [x] 1.1 Extend the CMake/Python declaration validators and generated policy for `basic-rendering-scene`, material mappings and lighting settings; verify matching positive/negative declaration cases and unchanged version-1 non-rendering behavior.
- [x] 1.2 Add isolated profile/platform/configuration paths and the scene-presentation target with platform-selected adapters; verify Windows/web configure graphs and rejection of excluded modules without changing existing output paths.
- [x] 1.3 Integrate the existing DX12 Render target and required dependencies without full Graphics; implement the minimal native initialization, triangle pass, resize and release checkpoint, and verify real visible output, zero-size recovery, clean shutdown and a recorded link/dependency audit.
- [x] 1.4 Add target shader generation/delivery with existing native tooling and browser GLSL resources; verify missing/invalid shaders fail actionably and browser target builds do not consume native shader binaries or tools.
- [x] 1.5 Add generic owner-thread runtime-service polling to the common lifecycle with legacy browser forwarding and retained failure/Stop semantics; verify compilation of existing consumers and no duplicate browser dispatch or renderer references in host sources.
- [x] 1.6 Extend independent common-host native/browser acceptance for pending-startup progress, once-only legacy forwarding, polling failure, cleanup progress and owner lifetime; run Debug/Release checks on both platforms and confirm minimal graph exclusions.

## 2. Portable content preparation

- [x] 2.1 Add the versioned simple-material format, explicit source-material UID mappings/default selection and common lighting settings; verify valid records and identifying rejection of missing mappings, invalid values, unknown fields and versions.
- [x] 2.2 Extend preparation to validate/normalize the supported cooked static-mesh subset while preserving asset identities; verify actual cooked fixture geometry loads through CPU assets and malformed ranges, unsupported topology/skinning and invalid indices fail.
- [x] 2.3 Package the complete rendering closure and profile manifest with shared runtime validation; verify both targets can consume one byte-identical archive and that prepared-archive mode rejects profile mismatch or corrupt render inputs without running cooking tools.
- [x] 2.4 Include declaration, material and geometry dependencies in freshness/publication checks; verify edits appear in new packages, failed preparation cannot launch stale output, and authored files remain unchanged.

## 3. Shared scene presentation

- [x] 3.1 Implement scene membership and camera-manager snapshot extraction at a safe scene synchronization boundary; verify nested/component world transforms, camera selection, visibility, valid empty frames, invalid cameras and singular transforms with focused scene tests.
- [x] 3.2 Implement asynchronous resource preparation, identity-based geometry sharing and safe component removal; verify repeated instances share resources and removal during a pending load cannot resurrect an object or retain dangling scene pointers.
- [x] 3.3 Implement immutable frame submission data and resource retention through backend completion; verify transformed normals under non-uniform scale, scene updates reflected in later frames and resource release after the last accepted use.

## 4. Backend frame rendering

- [x] 4.1 Complete the Windows opaque mesh pass over Render with material/light uniforms, depth targets and backend projection conversion; verify multiple meshes, occlusion, colors, framing and repeated resize with the real driver.
- [x] 4.2 Refactor BrowserRenderer to separate resources from frame clear/draw/present and implement the shared adapter; verify multiple geometry assets, repeated instances, lighting, depth, DPR and zero-size recovery in a real browser.
- [x] 4.3 Preserve NauDemo's existing browser presentation and text path through compatibility integration; verify native/browser cube appearance, motion, text, resize and orderly close remain supported.

## 5. Application lifecycle and project integration

- [x] 5.1 Compose the optional presenter into packaged scene startup and post-update without renderer dependencies in the common host; verify initial-frame readiness gates Running, startup makes progress without ordinary updates and non-rendering startup is unchanged.
- [x] 5.2 Implement Stop, partial-startup failure, graphics loss and ordered resource/driver/window cleanup; verify repeated Stop during asset load/upload, submission failure and terminal loss without later draws or live-resource shutdown warnings.
- [x] 5.3 Add EditorProject's rendering declaration, explicit materials and editor-authored scene with distinct and repeated geometry, nested/component offsets and project-driven motion; verify the shared production entry builds and displays it on Windows and web while the default main scene/declaration stay intact.
- [x] 5.4 Document common build/run commands, native shader prerequisites, supported content and output locations in packaged-project and EditorProject guides; verify commands for fresh preparation and explicit prepared-archive reuse without hard-coded local SDK paths.

## 6. Integrated acceptance

- [x] 6.1 Add independent observer and visual acceptance checks for scene/resource identities, motion, camera selection, visibility/removal, non-uniform scale, occlusion and resize; verify test failures detect blank frames, wrong transforms, stale objects and timeout instead of reporting success.
- [x] 6.2 Run relocated production and observer deliveries on Windows Debug/Release and real-browser web Debug/Release using the same archive; record hashes, scene evidence and visual results with explicit tolerances and nested-URL browser serving.
- [x] 6.3 Run invalid-content and lifecycle cases in all four configurations, including missing/corrupt geometry/materials, unsupported content, invalid camera/transform, partial graphics startup, upload/submission failure, repeated Stop while pending and device/context loss; record real versus injected fault coverage and completed eligible cleanup.
- [x] 6.4 Run affected non-rendering packaged-project, common-host, minimal, CPU-asset and existing full desktop/NauDemo regressions; verify excluded dependencies remain absent from non-rendering/browser graphs and report any unexecuted checks explicitly.
- [x] 6.5 Record reproducible commands, revisions, tool versions, results and remaining limits in validation.md; verify each spec scenario maps to evidence and run strict OpenSpec validation before reporting completion.
