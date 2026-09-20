# Validation

## Current status

2026-09-20: **24/24 tasks complete**. Actual NauDemo Debug/Release browser builds,
scene-driven rendering, lifecycle/failure acceptance, package relocation and an
independent fresh-checkout walkthrough pass. Native builds and regressions pass.
The user confirmed all native Debug/Release visual checks passed by direct
observation, completing task 5.4. The change is ready for archive, but has not
been archived. See the final acceptance/source audit and fresh-checkout record below.

Earlier sections preserve investigation checkpoints, including failures and
proposals that were subsequently resolved. Their historical task counts do not
override this current status or the final audit.

## Task 1.1 fixture

Added engine cmake/probes/emscripten/webgl_worker.cpp and test_webgl_worker.py.
The runner uses installed Chrome, an isolated local HTTP server, bounded waits,
worker-side pixel readback, page heartbeats, screenshots and structured JSON.
It builds both configurations before browser execution. A failing Debug case
stops execution before Release browser acceptance; this is not a Release pass.

Environment: engine base 37e1f4ea00c826882567ba928f1f3d36c3128c01;
Emscripten 6.0.9 (4e4223852a0835923411059a3929907d7df1232e);
Chrome 153.0.8010.52; Python 3.14.2 with Playwright.

From the repository root, explicitly activate the SDK and run:

```powershell
. "$HOME/emsdk/emsdk_env.ps1"
python NauEngineLite/cmake/probes/emscripten/test_webgl_worker.py
python NauEngineLite/cmake/probes/emscripten/test_webgl_worker.py --blocking-worker
```

Each run prints its ignored engine build evidence directory and stores commands,
compiler logs, screenshots and results.json. Relevant settings are C++20,
-pthread, PROXY_TO_PTHREAD=1, PTHREAD_POOL_SIZE=2, EXIT_RUNTIME=1,
OFFSCREENCANVAS_SUPPORT=1, OFFSCREENCANVASES_TO_PTHREAD=#canvas,
MIN_WEBGL_VERSION=2 and MAX_WEBGL_VERSION=2. Context proxying is disallowed;
explicit swap control and worker-side commit_frame are used. The default fixture
adds ASYNCIFY=1; blocking-worker instead uses synchronous C++ sleeps without it.

### Results

- Initial run webgl-worker-48xj2a8n: worker context, drawing and resize passed;
  the SDK context-loss callback did not arrive. Installed libhtml5_webgl.js
  registers that callback on a main-thread DOM event target, not the transferred
  OffscreenCanvas.
- Worker-local OffscreenCanvas listener, yielding fixture
  webgl-worker-l1uyrgac: Debug and Release passed worker creation, pixel readback
  (blue channel 217), resize from 320x180 to 640x360, actual induced context-loss
  event, listener removal, context destruction and exit 0. Page heartbeat counts
  were 82 and 79, respectively, with no page errors and retained DOM canvas.
- Current lifecycle-style blocking worker, webgl-worker-807gmlzw: both fixture
  configurations compiled; Debug browser execution failed loss notification after
  successful drawing and resize. Page stayed responsive (133 heartbeats), but
  the worker event listener did not execute before its timeout. Release browser
  execution was not reached.

### Initial design issue and authorized resolution

The current browser_runtime.cpp remains in a C++ loop and waits with futexes;
it does not yield to the worker's JavaScript event loop. A transferred canvas
listener therefore cannot be assumed to run there. The passing Asyncify fixture
is not evidence that the current Nau lifecycle satisfies task 1.1.

Proposed next investigation: test owner-side context-loss polling with the pinned
SDK against the same blocking-loop fixture, including real loss and no new draws
after detection. If sufficient, explicitly document polling in the renderer
design. Otherwise, propose a worker event-loop yielding lifecycle integration
with the existing cadence, stop, executor and cleanup contracts preserved.
Neither production polling nor Asyncify/lifecycle changes have been applied.

The user authorized proceeding with the polling investigation. Run:

```powershell
python NauEngineLite/cmake/probes/emscripten/test_webgl_worker.py --blocking-worker --poll-loss
```

Evidence webgl-worker-br9u89e6: Debug and Release pass worker context creation,
pixel readback, resize, owner-side detection of induced real context loss,
rejection of a subsequent draw, destruction and successful exit. No Asyncify
setting is used. This completes task 1.1 only. The design now explicitly selects
polling for production integration rather than requiring event delivery.

## Task 1.2 dependency boundary

Delivered engine doc/naudemo_web_dependencies.md and cmake/naudemo_sources.json.
The manifest names all 9 CoreAssets and 27 CoreScene implementation sources,
the two existing CPU glTF parser/accessor sources, kernel helper additions,
required new adapters and excluded targets. File existence was checked. The
current glTF parser uses Nau JSON/runtime values; no new third-party parser is
needed. The full glTF container and CoreAssetFormats target remain excluded due
to animation/texture-tool coupling. CPU accessor validation and a package VFS
adapter remain actual work in 2.3, not satisfied by the inventory.

## Task 2.1 profile checks

Added opt-in NAU_RUNTIME_PROFILE=demo and NauDemoRuntime.cmake, consuming the
explicit manifest with missing-source checks. It selects PlatformApp, CoreAssets,
CoreScene and NauFrameworkDemo. At this stage the framework retains minimal
scene-disabled behavior until task 2.4, and no demo executable is claimed until
task 4.1. No existing preset definitions were changed.

```powershell
python NauEngineLite/cmake/probes/emscripten/test_demo_profile.py
```

All four configurations pass: web/native Debug/Release, exact implementation
source matching, declared third-party allowlist, excluded-target audit and native
browser-flag isolation. A disposable fixture verifies missing-source diagnostics
without removing any repository source. Presets match their HEAD contents.
Evidence: engine build/demo-profile-evidence (JSON target lists and configure logs).
Web caches are build/web-demo-cpu-debug and web-demo-cpu-release; native caches
are build/native-demo-cpu-debug and native-demo-cpu-release.

Existing web-minimal-debug was reconfigured and rebuilt successfully after the
profile changes. Its actual Chrome success lifecycle acceptance also passed via
cmake/probes/minimal_app_web/run.py --build build/web-minimal-debug --scenario
success. Logs: build/demo-minimal-configure.log, demo-minimal-build.log and
demo-minimal-acceptance.json. Broader native/minimal suites remain task 5.4.

## Task 2.2 initial compile findings

Compiled the selected browser CPU graph. Two MSVC-specific ui64 integer suffixes
in asset_manager_impl.h/.cpp were converted to standard ULL without changing the
values. The next build reaches kernel/include/nau/math/transform.h and fails on
SIMD-only get128, FloatInVec, vector comparison/select operations and Point3
conversion unavailable in the selected scalar math backend. Logs are retained
under build/web-demo-cpu-debug/build.log and build-next.log. This task remains
incomplete; neither archive compilation nor a working scene is claimed.

The scalar-port review also identifies an existing shared behavior issue:
isRotationNormalized returns abs(dot(q,q)-1) > 0, so an identity quaternion is
reported not normalized and Transform::isValid returns false. Correcting this
predicate changes native observable behavior and should be explicitly decided
before implementing a common native/scalar normalization check. Transform
source has not been modified. Recommended correction: accept finite unit
quaternions within a documented tolerance, with native and Wasm regression tests
for identity, normalized rotation, non-unit and non-finite inputs.

## Approved Transform correction and scalar port

The user approved the shared normalization correction. Transform now accepts
finite squared quaternion length within 0.001 of one and rejects non-unit and
non-finite rotations. The initial 0.0001 tolerance was tightened beyond the
existing native normalize() precision: its SSE implementation uses unrefined
_mm_rsqrt_ps. The final tolerance explicitly covers that output, with tests.
Native composition/inverse/normalizer algorithms have not been changed.

Added scalar implementations for Transform finite checks, scale masking,
point conversion, comparisons and diagnostic formatting. Replaced compatible
SIMD multiply expressions with mulPerElem. Changed dag_color.h's MSVC-only
__forceinline to the existing NAU_FORCE_INLINE macro.

Release tests exposed a separate bundled scalar bug: Vector3/Quat indexed
accessors performed pointer arithmetic from mX across separate member objects.
Optimized indexed writes and named-component reads became inconsistent. The
eight affected scalar accessor overloads now select actual members explicitly,
including the Vector3 W storage lane. No SSE/NEON library code was changed.

Eight new TransformPortability tests cover normalization, non-finite components,
indexed writes/readback, matrix versus point/vector transformation, composition,
inverse, negative/zero scale, interpolation and formatting. Composition checks
allow 0.005 positional error for the existing native approximate normalizer;
direct matrix/point checks retain 0.0001 tolerance.

Final validation passed:

- Native Debug and Release: CorePortability CTest, 34 Google Tests each.
- Wasm Debug and Release: CorePortability CTest, 35 Google Tests each, plus the
  separate expected-fatal diagnostic CTest. Wasm tests run under SDK Node, not
  Chrome; these results do not claim browser scene lifecycle acceptance.
- Wasm CPU graph Debug and Release: CoreScene, CoreAssets and NauFrameworkDemo
  archives compile. This does not establish an executable link or scene startup.
- Strict OpenSpec validation and git diff whitespace checks pass.

Reproduce after explicit SDK activation, from the repository root:

```powershell
cmake --build NauEngineLite/build/wasm-core-debug --target NauCorePortabilityTests -j 8
ctest --test-dir NauEngineLite/build/wasm-core-debug --output-on-failure
cmake --build NauEngineLite/build/wasm-core-release --target NauCorePortabilityTests -j 8
ctest --test-dir NauEngineLite/build/wasm-core-release --output-on-failure
cmake --build NauEngineLite/build/core-native-debug --config Debug --target NauCorePortabilityTests
ctest --test-dir NauEngineLite/build/core-native-debug -C Debug --output-on-failure
cmake --build NauEngineLite/build/core-native-release --config Release --target NauCorePortabilityTests
ctest --test-dir NauEngineLite/build/core-native-release -C Release --output-on-failure
```

These existing core-validation caches use cmake/probes/wasm_core as their source.
Logs: engine build/transform-wasm-{debug,release}.log,
transform-native-{Debug,Release}.log and each cache's Testing/Temporary/LastTest.log;
CPU graph logs: build/web-demo-cpu-{debug,release}/build-transform-final.log.
At that checkpoint, task 2.2 remained unchecked pending focused scene/asset
ownership and error-path runtime tests. The following run closes that gap.

## Task 2.2 scene/assets runtime verification (2026-09-20)

`cmake/probes/demo_scene` now links a real CoreScene/CoreAssets executable. Its
five Google Tests exercise scene ownership and weak-reference invalidation,
parent/child world transforms and CameraComponent settings, asset subresource
paths and missing-manager errors, registered container ownership/release, and
unregistered asset-scheme errors. Fixtures install the actual service provider,
scene factory/manager, broadcaster and logger used by these operations.

Direct includes for WorkQueue and EASTL variant remove two private headers'
reliance on their module precompiled headers. The standalone validation target
explicitly selects C++20 for native builds.

Reproduce from the repository root:

```powershell
$env:EMSDK_QUIET = '1'
. C:/Users/Yakov/emsdk/emsdk_env.ps1
C:/Python314/python.exe NauEngineLite/cmake/probes/demo_scene/run.py
```

SDK 6.0.9; Chrome 153.0.8010.52. All five tests pass in native Windows Debug and
Release, SDK Node Debug and Release, and actual Chrome Debug and Release. Both
browser runs are cross-origin isolated, exit zero, report five passing tests,
and have no page errors or aborts. Structured results and exact configure/build/
CTest commands and logs are in `NauEngineLite/build/demo-scene-evidence/`.

Task 2.2 is complete; progress is 4/24. These checks cover CPU foundations, not
mesh decoding, activated scene lifecycle, rendering, or packaged NauDemo acceptance.

## Task 2.3 decoder compilation checkpoint (2026-09-20)

The focused project additionally compiles the two recorded glTF CPU sources into
`NauDemoMeshDecoder`, without Animation, GraphicsAssets or the desktop asset-format
module. Initial SDK compilation failed because `MapLikeNativeDictionary::getKey`
passed an EASTL iterator to `std::advance`; libc++ rejects EASTL's distinct iterator
category tags. A simple increment loop preserves map enumeration on both libraries.
A sixth test checks the first and second keys of both std and EASTL maps.

The latest `demo_scene/run.py` run passes all six tests in Windows, SDK Node and
Chrome, Debug and Release, and compiles the decoder archives in all four build
configurations. Results replace the earlier five-test checkpoint in
`build/demo-scene-evidence/`. Strict OpenSpec validation and diff whitespace checks
also pass. This is compilation and dictionary evidence only: task 2.3 remains
unchecked until the real asset adapter, cube decoding and corrupt-input diagnostics
are implemented and verified. Existing mesh-accessor reads ignore copy errors and
assume validated layouts; the new loader must validate and own input data before
using that accessor, or harden the accessor's checked error handling.

## Task 2.3 asset integration and failure blocker (2026-09-20)

Added the demo-only CoreAssetsCpu module to the explicit source manifest. It
contains a checked mesh container loader, CPU view factory, immutable buffer
ownership and read-only package-file source for Nau VFS. The recorded glTF parser
and mesh accessor remain the decoder boundary. The loader rejects unsupported
layouts before constructing that accessor. The abstract loader's previously
undefined getSupportedAssetKind declaration is now pure virtual; all existing
loaders provide overrides, removing the missing Wasm vtable definition.

The expanded focused executable builds in Wasm Debug. Its original six tests and
the actual cube geometry/view-cache test pass. Missing/truncated buffers,
malformed JSON, invalid accessor references and unsupported stride also pass.
InvalidIndexFails exposes a shared AssetViewEntry failure-settlement bug and
aborts during teardown. Subsequent tests did not execute in that run. Full new
native/Chrome/Release validation is pending; previous six-test results remain
historical foundation evidence only.

See asset-view-failure-followup.md for the exact cause, reproduction and proposed
shared initial-view correction. Logs: build/cpu-assets-build.log and
build/cpu-assets-test.log. Task 2.3 remains unchecked; progress stays 4/24.

## Shared initial-view failure correction verified (2026-09-20)

The user approved the proposed shared fix. AssetViewEntry::getAssetView now
captures fabrication errors, rejects its pending creation state with the same
error, and returns that error to the initiating caller. The successful cache path
and existing explicit-request retry policy are preserved.

FactoryFailureSettlesAllWaitersAndAllowsExplicitRetry verifies two overlapping
requests use one factory invocation, both receive the identical failure object,
and two subsequent requests share one successful retry. Descriptor removal and
fixture teardown complete. The earlier corrupt-index teardown abort is resolved;
the non-finite-position and read-only-file tests also execute successfully.

`cmake/probes/demo_scene/run.py` passes all 16 tests in native Windows, SDK Node
and Chrome 153.0.8010.52, Debug and Release. Browser runs are isolated, exit zero
and have no page errors or abort. Current results and full commands/logs are in
`build/demo-scene-evidence/`. `test_demo_profile.py` passes all four source and
dependency graph audits, missing-source diagnostics and unchanged preset checks.
Strict OpenSpec validation passes.

This resolves the shared initial-view blocker. Task 2.3 remains open for its final
input-validation/diagnostic coverage review; overall progress remains 4/24. This
does not claim renderer, hot-reload, application lifecycle or delivery acceptance.

## Task 2.3 diagnostic review completed (2026-09-20)

The CPU loader now logs its original failure with the glTF path before CoreAssets
converts a failed container load into an empty view. Tests subscribe to the real
logger and check the named binary input for missing/truncated buffers, glTF path
for malformed JSON, and specific causes for invalid accessor/stride data. View
factory errors retain their specific invalid-index/non-finite diagnostic through
the shared failure fix.

All 16 tests pass again in Windows, SDK Node and Chrome Debug/Release, with no
browser page errors or aborts. Evidence remains in build/demo-scene-evidence.
The recorded cube yields 24 owned positions/normals and 36 valid indices, unit
face normals and +/-1 corners; repeated requests share the cached view and a
held view survives descriptor removal. The immutable VFS source rejects writes.

Task 2.3 is complete; progress is 5/24. Supported input is the recorded glTF 2.0
single-mesh, single-primitive, single external-buffer layout, packed float
POSITION/NORMAL with optional recorded TEXCOORD_0/TANGENT and uint16 triangle
indices. Other required layouts/features diagnose failure. This is CPU asset
acceptance, not browser rendering or staged demo package acceptance.

## Task 2.4 shared scene integration checkpoint (2026-09-20)

NauFrameworkDemo now links CoreScene and enables its existing initialization,
update, shutdown and shutdown-polling calls through NAU_SCENE_RUNTIME. Graphics,
UI and VFX guards remain separate. The minimal profile does not enable scenes.

The linked fixture exposed EASTL's required unsupported-architecture debug-break
hook; cmake/platformSpec/emscripten_eastl_debug_break.cpp supplies a diagnostic
followed by abort, linked only for Emscripten. No bundled EASTL source was edited.
The fixture now explicitly allocates 64 MiB initial memory with 12 workers after
the full scene/application initialization exceeded the former 16 MiB default.

The 18-test checkpoint passed native Windows, SDK Node and Chrome Debug/Release:
checked application creation/startup, scene activation, scene updates, normal
Stop and pending async component work at repeated Stop. Cleanup polling settles
that work without new game updates; deactivation and destruction each occur once.
Existing CPU scene/asset/diagnostic checks also pass. Results and commands are in
build/demo-scene-evidence.

A subsequent 19th test, StopDuringSceneActivationCleansUpBeforeStopped, fails in
SDK Node Debug: early Stop bypasses orderly scene deactivation because the
application's main-loop pointer is assigned only by finishStartup. Component
destruction occurs, but its deactivation callback is skipped. The complete run
has 18 passes and one failure; native/Chrome execution of this new case remains
pending. See startup-scene-cleanup-followup.md for the proposed shared correction
and build/demo-startup-stop-test.log for evidence. Task 2.4 remains open; progress
is 5/24.

## Task 2.4 completion ? scene lifecycle

The demo framework now initializes, updates and asynchronously shuts down real
CoreScene without full graphics/UI/VFX. All 19 scene/asset/lifecycle tests passed
in native Windows, SDK Node and Chrome Debug/Release. Cases cover normal Stop,
pending asynchronous component update, repeated Stop, and Stop during pending
scene activation. The last case exposed skipped deactivation before Running;
the applied registered-service lookup correction and regression evidence are
recorded in startup-scene-cleanup-followup.md. Native minimal lifecycle and
browser minimal startup/failure/pending-work/cleanup regressions passed.

## Task 2.5 completion ? shared demo

NauDemo/src/demo_scene.h owns common cube/camera construction and the 45-degree
per simulation-second rotation. The native adapter retains its material, light
and HDR environment. The 20-test suite passes Windows, SDK Node and Chrome in
Debug/Release, including 20 x 100 ms producing 90 degrees and the real object's
quaternion orientation. Orientation uses atan2, independent of native approximate
normalization length; the angular tolerance remains 1e-5 radians.

Native Debug compiled through build.py (existing libraries). A fresh desktop
Release engine and NauDemo build completed at build/naudemo-desktop. This exposed
an invalid deferred add_subdirectory in the existing demo hook; the hook now sets
NAU_DEMO_SOURCE_DIR, consumed normally after engine sample targets. The desktop
configure explicitly selected Python 3.10 with cymbal/clang on PATH. Logs:
build/demo-desktop-configure.log and build/demo-desktop-release-build.log;
NauDemo/build/shared-scene-debug.log. Full fresh native Debug and visual checks
remain task 5.4.

## Actual package integration checkpoint

Debug and Release actual NauDemo packages rendered a visible blue cube, changed
orientation, and completed repeated Stop in Chrome 153.0.8010.52. Initial buffer
success with blank screenshots was rejected; see the integrated presentation
correction in design.md. The runner now requires a blue-pixel area and changed
RGB screenshot content, in addition to real submitted Nau model/view/projection
matrices and 36 indices. Artifacts: build/demo-browser-{debug,release}/results.json
and cube-first.png/cube-rotated.png. These are initial integration checks, not
completion evidence for the remaining full acceptance scenarios.

## Renderer/build/delivery checks

Tasks 3.1, 3.4 and 4.1?4.3 are verified in both configurations. Actual staged
packages use NauDemo.js/.wasm/.data, the real static scene/assets modules and
worker WebGL 2. Startup reports readiness only after scene activation, asset view
loading, shader linking/upload and the first draw. Missing canvas, unavailable
context, missing buffer, bad shader and bad material configuration all diagnose
failure. Size tests cover 420x260 CSS pixels, DPR 2 (840x520), zero-height
suspension/recovery and proportional clamping of 100000x1000 to GL limits.
Results: build/demo-acceptance-{debug,release}/{scenario}/results.json.

Package manifests have exact SHA-256 inventories. test_staging.py checks both
configurations, stale-file removal and missing-input failure preserving the
previous package. Results: build/demo-staging-results.json. Required inputs are
copied into the preload archive and also shipped loose for inspection; modifying
loose copies requires rebuilding the archive, as documented in package README.

Task 5.3 passed: both packages copied to a temporary directory outside the
checkout and served at /relocated/demo/ using their own serve.py classes. Chrome
verified rendering/rotation/resize/Stop and asserted every network request stayed
under that URL base (or a local blob worker). Exact locations and codes:
build/demo-relocation-results.json; detailed evidence build/demo-relocated-*.

Interrupted startup is exercised at explicit owner-loop asset/graphics stages.
Stop at either stage reaches Stopped with zero updates and no rendered frame,
and does not allocate later graphics resources. Normal scene startup remains
asynchronous and service polling resolves accepted stage work before cleanup.

## Final browser acceptance and regression audit

The real-package runner uses installed Chrome 153.0.8010.52 in new headless mode
with a disposable profile and CDP `no_defaults=True`. This preserves real tab
visibility; Playwright's default controlled-page setup reported both pages visible
and was rejected for that scenario. Early headed integration screenshots were
also inspected. The PNG/provenance assertion now captures directly through CDP
and only accepts a capture during which the C++ frame number stayed unchanged.
This avoids pairing a delayed screenshot with earlier scene matrices. Failed
capture attempts remain failures rather than being counted as rendering proof.

Both configurations pass these actual-package scenarios:

| Requirement/scenario | Evidence under `NauEngineLite/build/` |
| --- | --- |
| Independent builds and required dependency/SDK diagnostics | `demo-profile-evidence/`, `demo-profile-final.log`, `demo-unsupported-sdk.log`, default configure/build logs |
| Real scene cube, shared rotation and camera | `demo-scene-evidence/results.json`; `demo-acceptance-{debug,release}/success` and `/camera` |
| Opaque blue perspective cube, nearest-face depth and directional shading | Success PNGs plus CPU reference triangle test using packaged geometry and C++ matrices |
| Context creation, shader compile and link errors | `/no-context`, `/bad-shader`, `/bad-link` |
| Resize, DPR 1/2, graphics limits, zero area/recovery | `/success` resized/limited snapshots and projection assertions |
| Foreground, responsive controls and actual hide/show | `/success` rate, heartbeat, simulation and visibility assertions; nominal 100 ms cadence retained |
| Stop at asset/graphics initialization and pending scene work | `/stop-assets`, `/stop-graphics`, `/pending-scene` |
| Repeated running Stop, no later submissions, reload | `/success` terminal/reload snapshots and frozen frame counts |
| Terminal context/host loss, no automatic restart | `/context-loss`, `/host-loss` |
| Missing buffer, invalid material/configuration | `/missing-buffer`, `/bad-config`; additional corrupt mesh/normal/index and ownership tests in `demo-scene-evidence` |
| Missing loader/wasm/data and hosting/graphics preflight | `/missing-loader`, `/missing-wasm`, `/missing-data`, `/missing-headers`, `/file-url`, `/missing-canvas`, `/no-offscreen` |
| Package inventory, hashes, stale/missing inputs | `demo-staging-results.json` |
| Both packages outside checkout, nested URL, no source/SDK requests | `demo-relocation-results.json`, `demo-relocated-{debug,release}` |
| Blank-image and broken-assertion runner rejection | `/blank-frame`, `/runner-failure`: expected unsuccessful structured results and process exit 1 |
| Native/Node/Chrome scene, assets, shutdown and shared rotation | All 20 focused tests pass in Debug/Release: `demo-scene-final.log`, `demo-scene-evidence` |
| Existing native minimal behavior | `demo-native-minimal-{Debug,Release}-final-ctest.log` |
| Existing browser minimal behavior | `demo-minimal-{debug,release}-final.json`, both success/visibility/repeated Stop |
| Existing browser lifecycle failure/Stop coverage | `demo-runtime-{debug,release}-final-ctest.log`: all 13 CTests pass per configuration |
| Native NauDemo coexistence build | `demo-native-{Debug,Release}-final-build.log`, both succeed |

Camera and pending-scene are explicitly compiled acceptance fixtures using
NAU_DEMO_TEST_HOOKS=ON. Their results record package manifests and runner identity.
Default delivery was restored with that option OFF in both build caches. Pending
work proves deactivation before settlement, no premature destruction/completion,
and exactly one destruction after release. Renderer shutdown is checked and runs
before platform disposal; scene shutdown precedes service shutdown. A post-step
renderer failure is latched and consumed by the bounded runtime-service poll.

### Native visual check (task 5.4): user-confirmed pass

Native Debug and Release build and launch. Normal window-close shutdown was also
exercised. The computer-use provider identified the correct NauDemo window but
captured pixels from an occluding unrelated window, even with restore requested;
keyboard focus verification likewise failed. Those images were rejected as
appearance evidence and are not retained in the validation artifacts. Native
appearance was subsequently checked directly by the user. On 2026-09-20, after
receiving the Debug/Release launch commands and visual checklist, the user
reported: "All visual checks passed using user eye". This confirms retained
appearance, rotation, camera/framing, resize/minimize/restore and window-close
behavior for both configurations. This is user-observed acceptance, not an
automated screenshot result; no new screenshots were supplied. Together with
the recorded passing builds and regression suites, this completes task 5.4.

### Scope and limitations

Browser material is intentionally simplified; desktop HDR/shadows/material parity
and 60 FPS are not claimed. Required CPU scene/asset sources are explicit, and
native/minimal graphs exclude the browser renderer. No new desktop Render, UI,
VFX, physics, Qt, USD or shader-tool dependencies enter the web graph. Existing
preset objects remain unchanged; new demo presets are additive. Bundled edits
remain the earlier verified scalar Vector3/Quat accessors; renderer matrix
serialization uses explicit columns/components without further vendor edits.
The approved shared normalization and asset-view settlement fixes and startup
scene cleanup correction retain their separate regression evidence.

No commits, submodule revision updates, publishing or archive action were made
for this implementation. The source is an explicitly recorded working patch
bundle over the repository bases, not a claim that those bases alone contain the
feature. Fresh-checkout results are recorded separately below.

## Task 6.2: executed independent fresh-checkout walkthrough

Checkout: `C:\Users\Yakov\AppData\Local\Temp\nau-demo-repro-verified-20260920`. The helper used fresh local `git clone --no-hardlinks --no-checkout` checkouts, checked out the recorded base revisions, then applied explicit binary patches and hashed untracked source files. No build tree or generated input was copied. SDK setup was explicitly sourced before invoking `NauDemo/web/reproduce.py`.

| Repository | Base revision | Patch SHA-256 |
| --- | --- | --- |
| root | `634a25360c911b532c64420cc0f60c06fd5d58dd` | `eb5ed7a77698956a23f0ce02e57f442d5875668a22c768fc19065703582b253c` |
| NauEngineLite | `37e1f4ea00c826882567ba928f1f3d36c3128c01` | `852a218bc1eabbbd5866300f528eecfa897f7c9f09b49274411489a4fc012c5e` |
| NauDemo | `4129dc65a3b01e6691e0c3de73ba89439ad0e401` | `2c79b3df1d9ee2ae9a0d201e51a237d95abc0e34d5a4ecb55157e7b0a64f397e` |

Complete file hashes and commands: `NauEngineLite/build/demo-fresh-evidence/results.json`; exact patches are adjacent. `tool-*.log` records Git, CMake, Ninja and Emscripten. The test results record Chrome/Python and package identity. Both Debug and Release configured, built from source, rendered and stopped successfully at `/fresh/demo/`, including resize, DPR, real visibility and reload. The helper verified no build edits to tracked source.

Environment: Windows-11-10.0.26200-SP0; Python 3.14.2; Playwright 1.63.0; Pillow 12.1.1. SDK 6.0.9 was reused from the explicit external installation. Required web dependencies are recorded bundled engine sources; editor/docs and desktop-only nested dependencies were not required for this procedure.

The initial shared-object clone attempt was replaced by independent clones. A later attempt exposed screenshot/matrix timing in the acceptance driver; the current driver uses a bounded CDP capture with matching frame numbers. The final complete helper invocation passed both configurations. Earlier failed-attempt records are retained separately; they are not completion evidence.

This is a fresh checkout plus an identified development patch bundle, not an assertion that the base commits alone reproduce the feature. Final documentation, inventory annotations and OpenSpec evidence/task edits follow the source snapshot; compiled implementation is unchanged. Task 6.2 is complete.
