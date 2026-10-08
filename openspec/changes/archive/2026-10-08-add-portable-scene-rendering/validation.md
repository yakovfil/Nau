# Implementation validation (in progress)

## Production Debug smoke checks (broader acceptance pending)

The common build driver produced Windows and web `basic-rendering-scene` Debug packages under distinct profile/platform outputs. Production native execution from an unrelated temporary working directory reached initial-frame submission and Running, rendered the authored fixture, resized and exited 0 with presentation cleanup. Production web executed in installed Chrome through Playwright, rendered the fixture and reached terminal Stopped with cleanupComplete true. Native and browser screenshots are in the profile build directory. Runtime material/reference checks, renderer setup and initial frame are part of the same packaged application entry.

The original first production attempt exposed an existing lazy AssetRef bug: a full `mesh/0` reference created a container descriptor whose view request used an empty inner path. `preLoadAsset` now creates a container path and returns its inner descriptor, preserving the same serialized reference while requesting its intended resource. The CPU checkpoint also exercises passive reference restoration. Complete reference regressions are still pending.

Graph audit: no Graphics, Physics, Animation, VFX, CoreInput, Audio or Qt targets in either rendering build; native uses Render, browser uses NauBrowserRenderer. Existing non-rendering outputs remain separate. The first Debug archive and both selected inputs/deliveries had SHA256 `9e62f9cc17b1f79c7b7dffb0634b4e99d6443326aca5cbd423087d80de3f99ba`. This is an intermediate fixture revision; final acceptance will use the revised fixture with visible geometry rotation and a separate non-rendered MyMover object so cumulative movement cannot remove required geometry from the view.

## Shared lifecycle polling (tasks 1.5 and 1.6)

The user approved the common-host scope addition. The independent consumer now tests generic owner-thread progress during pending startup and cleanup, once-only legacy browser forwarding, polling failures during startup/running/cleanup, absence of premature/later updates, and lifetime through teardown. Original host scenarios remain included.

Native Debug and Release: 18/18 CTest cases each (common-host scenarios plus file logging and minimal lifecycle suites). Real Chrome web Debug and Release: 18/18 each. Total: 72/72 cases. Minimal source graphs continue to include kernel, framework and PlatformApp only; no renderer/scene module is added by the polling contract. Build and CTest logs are under `NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/`, named build-common-host-* and common-host-*. Structured per-scenario results remain under each `NauEngineModules/build/common-host-*` tree.

Commands use the existing documented common-host probe and CTest invocation. Existing browser services compile unchanged; their compatibility interface forwards through the shared lifecycle, and browser scheduling no longer separately dispatches those services.

## Declaration policy (task 1.1)

`python NauEngineModules/tools/asset_tools/test_packaged_declaration.py` passes. One parity test exercises 15 positive/negative declarations through Python and CMake, including the unchanged non-rendering declaration, rendering policy, module exclusions, duplicate components, invalid UUID/path, missing settings, unknown rendering fields and invalid finite/color/direction data. A second test covers simple material input validation. Production runtime/render integration remains pending.

## Native direct-driver checkpoint (task 1.3)

Configured an isolated Windows scene-profile source graph under the ignored `NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/native` directory using VS 2026/v145, MSVC 19.51.36260.0 and Windows SDK 10.0.26100.0. The temporary hook attaches NauEngineModules and its packaged runtime with a rendering declaration, without attaching the production EditorProject executable (SceneRenderer implementation is pending).

Build command:

```powershell
cmake --build NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/native --config Debug --target NauRenderingCheckpoint --parallel 8
python NauEngineModules/modules/scene_renderer/tests/verify_native_checkpoint.py NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/native/bin/Debug/NauRenderingCheckpoint.exe --output NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/native-debug.json
```

The real DX12 driver renders a visible blue triangle. Desktop inspection confirmed initial output and correct centered output after resize. The independent window helper performs three resizes and minimize/restore, closes the owned window and requires bounded exit, resize diagnostics and no error logs. Result: PASS, exit 0, five ResizeBuffers calls, no errors. GPU resources precede driver release. The checkpoint uses runtime D3DCompile for its test shaders; production build-time shader generation is task 1.4 and has not been implemented.

The driver initially linked against kernel facilities excluded from the ordinary scene profile. Rendering-only source additions provide DataBlock, legacy file IO, OS locks and associated zlib/zstd support. A default-compatible `dx12.persistentPipelineCache` setting now permits the checkpoint to use in-memory caches without writing relative cache files. Existing desktop behavior defaults to enabled persistence.

Evidence under `NauDemo/EditorProject/build/basic-rendering-scene/checkpoint/`: build-debug.log, native-debug.json/log, triangle-debug.png, resized-debug.png and graph-audit.json. The target audit contains no Graphics, Physics, Animation, VFX, CoreInput, Audio or Qt targets. Release, complete scene presentation, browser rendering and cross-platform acceptance remain pending.

## Portable materials and cooked meshes (tasks 2.1 and 2.2)

`python NauEngineModules/tools/asset_tools/test_portable_render_assets.py` passes three tests covering uint32-to-uint16 normalization, corrupt/unsupported input rejection and geometry hierarchy transform baking with inverse-transpose normals. The normalizer is integrated into rendering-profile preparation. The opt-in editor-authored cube/tetrahedron fixture cooks through native AssetToolCmd into a 14-file archive; neither the existing scene nor its default declaration is modified.

Material metadata is registered before scene translation, preventing AssetRef serialization from erasing bindings. Inspection of the compiled scene confirms two blue UID references and one orange UID reference. Preparation now rejects changed reference counts or missing mappings/defaults. Archive selection validates rendering settings, material records and prepared geometry without USD imports. Complete runtime material and renderer integration remains pending.

`NauCpuMeshCheckpoint` built in the same isolated Debug graph loads both real cooked assets through the production CPU mesh factory: cube 36 vertices/36 indices, tetrahedron 4 vertices/12 indices. It runs the common host, mounts the archive, resolves the asset database and exits 0 after successful loading and cleanup. Evidence: checkpoint/build-cpu-debug.log, checkpoint/cpu-debug.log and preparation-debug.log under the ignored rendering build directory. Full rendering acceptance has not run.

## Resumed observer and shader acceptance

The dedicated rendering probe now builds natively and in Emscripten. Relocated Windows Debug/Release deliveries passed 11 real-driver cases each: normal motion, visibility, removal, empty frame, component offset, camera selection, activation, partial initialization failure, partial resource work failure, submission failure and injected native device loss. Chrome Debug/Release passed the corresponding cases plus invalid GLSL compilation and real WEBGL_lose_context loss. Each case requires checked terminal state and completed owner cleanup. These are observer/lifecycle results; comprehensive visual tolerances, invalid-content and pending-load cases remain pending.

Commands:

```powershell
python NauDemo/EditorProject/tests/verify_native_rendering.py Debug
python NauDemo/EditorProject/tests/verify_native_rendering.py Release
python NauDemo/EditorProject/tests/verify_web_rendering.py Debug
python NauDemo/EditorProject/tests/verify_web_rendering.py Release
python NauEngineModules/modules/scene_renderer/tests/verify_shader_delivery.py --output NauDemo/EditorProject/build/basic-rendering-scene/shader-checks
```

Evidence is under the ignored `build/basic-rendering-scene/native-observer-{debug,release}`, `web-observer-{debug,release}` and `shader-checks` directories. The selected archive SHA256 is `d8af2df411246ba73eebe786305316d088daba6d54157f12d715f527f9f0fdbf`. Browser screenshots accompany successful observer cases, but automated geometric/color acceptance is not yet complete.

Production HLSL now uses build-time DXC and embedded resources; the earlier checkpoint note about pending shader implementation is historical. Isolated production-helper tests verify valid shader delivery, missing DXC configuration rejection, invalid HLSL build rejection and missing GLSL rejection. Actual invalid GLSL compilation fails checked browser startup. Browser generated resources contain GLSL without DXIL/native compilation.

Inspection identified outstanding async component updates after post-update. The scene manager now exposes owner-thread snapshot readiness and presentation defers capture while those updates remain outstanding. The pending-update shutdown regression checks readiness before and after the continuation settles; its affected suite still needs to run.

## Final acceptance (2026-10-08)

This section supersedes the earlier intermediate/pending notes. Implementation is complete; changes remain uncommitted.

### Environment and revisions

- Windows, VS 2026/v145, MSVC 19.51.36260.0, Windows SDK 10.0.26100.0.
- CMake 4.2.1, Ninja 1.13.2, Emscripten 6.0.9; Chrome 154.0.8037.98.
- Python 3.14.2 for acceptance; Python 3.10.11 and OpenUSD 24.08 for native preparation.
- Baseline root revision `6aa62de70a1b312efb5ec69b59d44bbad52e594b`.
- Baseline engine `ec5340ea9bc0cc8dbf465fb8a98a1f3c56ff23dd`, modules `eb379469300ffa549d69362501cc3ca56cb1040d`, demo `4c0030475b7d46074f1e2dea47bacc2f30a31dca`; acceptance includes the working-tree implementation.

### Production and independent observer matrix

All four production deliveries passed relocation, visible multiple-mesh output, real scene-driven motion and checked Stop. Windows launches use a temporary directory outside the checkout and a system-only PATH. Browser deliveries are copied outside the checkout and served at `/relocated/nested/application/` with COOP/COEP headers in real Chrome. Production receives no observer or fault services.

The independent observer suite passed 27 cases in each Windows configuration and 30 in each browser configuration: 114 cases total. Evidence includes owner-thread capture, archived mesh FNV64 hashes, component/geometry identities, nested transforms, additional-component offsets, camera selection, visibility/removal/activation, empty frames, updates, delayed async motion, removal during accepted geometry load, accepted upload work followed by repeated Stop, repeated Stop during load, invalid inputs and completed owner cleanup. Browser-only cases cover actual invalid GLSL and zero-size startup recovery/Stop.

Archive SHA256 is `d8af2df411246ba73eebe786305316d088daba6d54157f12d715f527f9f0fdbf` in Windows Debug/Release `package/content.nau_pack` and web Debug/Release `package/NauDemoMain.data`. Geometry provenance hashes are independently computed from archive accessors, not copied from runtime reports. Default declaration and original main scene are unchanged.

Pixel acceptance uses an independent CPU projection/rasterization of archived positions, normals, indices and observed immutable matrices. Interior samples compare the nearest surface and simple linear-to-sRGB lighting with a 25-channel-value tolerance and at least 94% agreement. All sampled pixels matched in final normal cases: native Debug 350/350, native Release 354/354, browser Debug/Release 1613/1613. Samples include differently colored overlapping geometry. Triangle-edge samples and four image-border pixels are excluded to avoid raster coverage/DWM corner differences. Authored position comparison allows 0.005 world units for existing native SSE transform estimates; scale and mesh hashes use tighter/exact checks. Inverse-transpose normal matrices are independently checked at 0.001 tolerance. Broad color-area checks reject blank or missing geometry; empty frames require no geometry color pixels.

Windows exercises repeated aspect changes and minimize/restore. Browser verifies DPR 2, two aspect changes, zero client size with unchanged submission count, and recovery with new submissions. Startup at zero size remains Starting with no game updates/frames; restoring dimensions allows Running, and repeated Stop while zero-sized completes cleanup.

Fault coverage is explicit: native device loss is injected; browser loss uses actual `WEBGL_lose_context`. Initialization, upload and submission failures are injected through a probe-only backend factory wrapping the real adapter. Upload failure/Stop occurs after accepting first-mesh GPU work, rather than forcing physical GPU memory exhaustion. Invalid GLSL uses real compilation; invalid/missing HLSL/DXC/GLSL build inputs use the production shader helper. No real native hardware removal, physical out-of-memory fault or device recovery is claimed. The adapter releases owned CPU jobs after resources and driver teardown; eligible cleanup remains checked.

### Preparation, graphs and regressions

- Nine prepared-archive checks pass: valid archive, profile/settings mismatch and missing/corrupt material/geometry, unsupported topology and invalid indices. These invoke the Python validator without cooking tools.
- Five isolated fresh-cooking checks pass: baseline, material edit, geometry edit, declaration edit and rejected invalid material. Accepted bytes reflect edits; a failed cook preserves prior accepted bytes and returns nonzero. Shared build-driver exit checks prevent later delivery/Run after that failure. Authored-input hashes remain unchanged through every preparation.
- Eight CMake file-API graph audits pass across both profiles and all platform/configuration selections. Rendering never enables full Graphics, physics, animation, audio, VFX, input, USD or Qt. Web excludes native Render; non-rendering excludes both presenters/backends. Shader resources are outside the common archive.
- Four adversarial acceptance checks reject wrong transforms, substituted geometry, missing instances and blank images. Readiness/process timeouts fail acceptance rather than becoming success; prior development runs demonstrated those bounded failures.
- Common-host native/web Debug/Release: 72 CTest cases passed, including generic polling and once-only legacy forwarding. Focused native scene-host Debug/Release tests passed, including pending-component snapshot readiness.
- Rebuilt CPU scene/mesh/screen-text suite: 29 Google Tests passed. CPU checkpoint also covers lazy asset reference loading of real cooked cube/tetrahedron data.
- Existing non-rendering packaged Windows/web Debug/Release independent startup, activation/failure and pending-Stop suites passed.
- NauDemo native Release presentation, motion, text, resize, close and missing-font checks passed using the existing SDK delivery. NauDemo browser Debug/Release rebuilt against the modified renderer and passed real presentation/text/resize/Stop acceptance using font-derived CPU references.
- Updated Render target builds in the full desktop editor Release graph. Existing full desktop EditorProject Release displays its original textured cube and sky, resizes and exits 0. Its existing SDK binary still logs a persistent pipeline-cache write warning (`cache/dx12.cache`); the portable profile disables persistence and has no such warning. A freshly reinstalled full SDK/editor delivery and native NauDemo Debug were not exercised. This is reported explicitly; no editor packaging/SDK publication is part of this change.

### Reproduction and evidence mapping

From the checkout root, with the documented native cooking prerequisites provisioned:

```powershell
powershell -NoProfile -File NauDemo/EditorProject/build.ps1 -Platform Windows -Configuration Debug -Acceptance -Declaration NauDemo/EditorProject/portable_rendering_project.json
# Activate EMSDK, then reuse the selected archive without native recooking:
powershell -NoProfile -File NauDemo/EditorProject/build.ps1 -Platform Web -Configuration Debug -Acceptance -Declaration NauDemo/EditorProject/portable_rendering_project.json -PreparedArchive NauDemo/EditorProject/build/basic-rendering-scene/windows-debug/selected-input/content.nau_pack
# Use Configuration Release for the other two deliveries, selecting the same archive.
python NauDemo/EditorProject/tests/verify_production_rendering.py Windows Debug
python NauDemo/EditorProject/tests/verify_production_rendering.py Web Debug
python NauDemo/EditorProject/tests/verify_native_rendering.py Debug
python NauDemo/EditorProject/tests/verify_web_rendering.py Debug
# Repeat the four acceptance commands with Release.
python NauDemo/EditorProject/tests/verify_rendering_archive.py
python NauDemo/EditorProject/tests/verify_rendering_guards.py
python NauDemo/EditorProject/tests/audit_rendering_graphs.py
python NauEngineModules/modules/scene_renderer/tests/verify_shader_delivery.py --output NauDemo/EditorProject/build/basic-rendering-scene/shader-checks
```

Freshness helper accepts generic prerequisite locations:

```powershell
python NauDemo/EditorProject/tests/verify_rendering_freshness.py --python <matching-python.exe> --tools <native-tools-directory> --usd <usd-install> --module <host-MainGameModule.dll>
```

| Spec scenario | Evidence under ignored `NauDemo/EditorProject/build/basic-rendering-scene/` |
| --- | --- |
| Both profiles coexist; excluded modules | `graph-audits.json`, declaration tests, non-rendering regression logs |
| One archive / unsupported content / edits | `archive-validation.json`, `freshness/results.json`, observer invalid-content logs, identical package hashes |
| Multiple components / state changes / invalid camera-transform | `native-observer-*/results.json`, `web-observer-*/results.json`, per-case logs/images |
| Framing, lighting and depth | observer `normal-projection.json` plus normal/resize images and independent rasterizer |
| Resize / zero-size suspension | native normal resize logs/images; browser resize/recovery images, zero-startup cases |
| Pending load/upload Stop; graphics failure | stop-load, remove-load, stop-upload, initialization/upload/submission/context-loss case logs and cleanup records |
| Production four-configuration relocation | `production-{windows,web}-{debug,release}/results.json`, images and runtime logs |
| Generic lifecycle progress/error/legacy forwarding | checkpoint common-host logs and common-host build/results files |
| Compatibility and retained desktop behavior | `regression-*` logs/results, `full-desktop-release.png/log`, full Render build log |

All generated builds, screenshots, archives and logs remain ignored. Native UI captures operate only on owned test windows. No change has been committed or pushed.


## Launcher and browser-cache follow-up (2026-10-08)

After the user reported blank output, all four existing production rendering deliveries were rerun successfully. The batch launchers still selected the non-rendering declaration. At the user's request, both launchers now explicitly select `portable_rendering_project.json`; direct build-driver defaults remain unchanged. Stubbed command execution verified Debug/Release argument forwarding, rendering declaration selection and exit-code propagation for both wrappers.

A subsequent browser canvas-transfer failure exposed stale delivery caching at the shared development URL. The rendering HTML had an older source timestamp than the non-rendering HTML; a conditional request using the non-rendering timestamp reproduced an incorrect 304 response from the running server. The development server now returns `Cache-Control: no-store` and ignores `If-Modified-Since`. `python NauEngineModules/cmake/browser_project/test_serve.py` passed, covering selection of an older-timestamp delivery and isolation headers. Chrome recovery from cached non-rendering content to rendering after clearing the prior browser cache reached Running and completed Stop. An ordinary reload could still retain previously cached child resources; users of an already-running old server must restart it and hard-refresh once. Existing staged Debug/Release server copies were updated.
