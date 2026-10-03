# Nau Web Port: Minimal Application Specification List

Status: exploration record, not implemented capabilities or completed OpenSpec specifications.

## Confirmed Direction and Scope

Start the Emscripten/WebAssembly port from:

`NauEngineLite/samples/minimalApp/app_sample_main_min.cpp`

NauDemo is removed from the port scope. Its files and submodule are not to be deleted or modified as part of this planning change.

The selected entry point creates a Nau application, registers the platform window service, starts the runtime, and repeatedly calls `app->step()` with a 100 ms sleep. It does not explicitly show a window or render a scene.

The first milestone is therefore a **non-rendering browser runtime**:

- Execute the actual Nau application, service, and module lifecycle in WebAssembly.
- Register a browser-compatible platform window service without requiring a GPU context.
- Advance application steps on an Emscripten pthread worker while keeping the browser UI thread responsive.
- Demonstrate startup, repeated steps, errors, and an explicit orderly stop through a small browser test page and diagnostics.
- Build without the desktop graphics, UI, VFX, or content-tool dependency chains.

WebGPU remains a later direction, not a dependency or acceptance requirement for this milestone. Scene rendering, shaders, materials, cube rotation, lighting, asset pipelines, physics, animation, audio, networking, and editor support are deferred. The previous simplified-lighting agreement only applies if a later rendering milestone returns to that scope.

The initial browser target is **desktop Chrome on Windows only**. Edge, other browsers, and mobile are outside this milestone's validation scope.

## Confirmed Design Decisions

- **Threaded runtime:** run Nau's application entry point on an Emscripten pthread worker. Retain background execution where needed and adapt Windows-specific services. The browser UI thread handles page controls and browser-facing operations; it must not block on runtime work.
- **Hosting:** require cross-origin isolation through COOP/COEP response headers. Report missing isolation clearly before attempting threaded runtime startup. There is no single-threaded fallback in this milestone.
- **Step timing:** preserve approximately 10 application steps per second, with a nominal 100 ms interval on the application worker. Background-tab timing is best-effort; do not execute a burst of catch-up steps on return.
- **Minimal window behavior:** register Nau's platform window service and maintain the required window state without creating a GPU context. The test page displays runtime status, an advancing step counter, and a Stop button that requests orderly Nau shutdown.
- **Framework separation:** introduce a dedicated minimal framework target sharing the existing lifecycle code while excluding graphics, UI, and VFX dependencies. Both the browser sample and a native Windows validation build use this target; avoid maintaining a separate copy of the runtime.

These decisions constrain the future OpenSpec design. Exact target names, header values, worker counts, and scheduling mechanisms remain implementation details to resolve during design and validation.

## Proposed Capabilities

Each capability below is a candidate for `specs/<name>/spec.md` in a future OpenSpec change. Specs should define observable behavior and acceptance scenarios. Implementation choices belong in the change's design.

| Spec | Scope and key acceptance scenarios |
| --- | --- |
| `emscripten-build` | Build on native Windows/PowerShell using an external, exactly pinned emsdk and CMake/Ninja Debug and Release presets. Compile required bundled dependencies from recorded revisions without vcpkg, use static linking and consistent pthread support, and select exactly one entry point. Produce a complete runtime package per configuration, independent of source-tree and SDK paths at runtime. |
| `minimal-runtime-profile` | Define a dedicated non-rendering framework target and static module registration. Share existing lifecycle code between browser and native Windows validation builds. Retain the kernel services and platform-window API needed by the selected entry point. Exclude graphics, UI, VFX, scene rendering, and content tools; report unsupported required modules explicitly. |
| `wasm-core-portability` | Port the core facilities required to compile and execute this profile: allocation, platform types, identifiers, diagnostics, synchronization, and any unavoidable math or serialization dependencies. Verify pointer-size/alignment assumptions and focused native/Wasm behavior. Do not require a port of unused kernel features. |
| `browser-platform-services` | Register a browser-compatible platform window service and maintain its required state without creating a WebGPU/WebGL device. Define window identity, size, visibility, timing, and console-diagnostic behavior. Route browser-facing operations to the browser UI thread as needed. Handle unavailable desktop operations explicitly; full input integration and rendered canvas behavior are deferred. |
| `browser-runtime-lifecycle` | Run the Nau application entry point on an Emscripten pthread worker, retaining background execution where needed. Support startup, approximately 10 steps per second, and explicit orderly shutdown while keeping the browser UI thread responsive. Cover pending tasks, cancellation, failure reporting, best-effort background timing, and resumption without catch-up bursts. |
| `minimal-app-web` | Adapt `app_sample_main_min.cpp` to exercise real Nau application/module/service APIs in the browser. Expose observable startup success and an advancing step counter, plus a stop control that executes Nau shutdown. A standalone JavaScript loop or a mocked application is insufficient. No scene, mesh, asset pack, or GPU is required. |
| `minimal-web-delivery-validation` | Produce a static browser test page and documented local serving procedure with required COOP/COEP headers. Validate desktop Chrome on Windows, clear failure when cross-origin isolation is missing, successful startup, repeated steps, page responsiveness, and orderly stop. Build the shared minimal framework target on Windows and run equivalent native lifecycle checks. |

## Emscripten Build: Confirmed Decisions

- **Build host:** support native Windows/PowerShell initially. WSL and Linux build-host support are deferred. This is separate from the Chrome-on-Windows browser target.
- **Toolchain management:** use an external emsdk installation. Select one exact supported SDK version after compatibility validation and record it in the repository. Check the active version and provide actionable setup instructions when it is missing or incompatible. SDK installation and upgrades are explicit operations, not automatic configure/build side effects.
- **Dependencies:** compile the minimal runtime's required bundled libraries from source with Emscripten, using the revisions recorded by the repository. Bypass the desktop vcpkg manifest and toolchain for this milestone. Do not reuse native Windows libraries in the Wasm link.
- **Configurations:** use CMake with Ninja and separate Debug and Release browser presets, each with its own build directory. Debug enables diagnostics; Release enables optimization. Both configurations use static linking and consistent pthread support across runtime libraries and the application.
- **Output package:** produce a self-contained runtime output directory for each configuration, containing the Wasm binary, JavaScript loader, and any worker-support files required by the pinned toolchain. Runtime loading must not depend on source-tree or SDK paths; build-time access to those locations is expected.
- **Ownership boundary:** `emscripten-build` owns producing the complete runtime package. `minimal-web-delivery-validation` owns the browser test page and server/hosting configuration. A successful compile alone does not demonstrate the startup, stepping, or shutdown requirements owned by the lifecycle and sample specs.

The exact SDK version remains to be selected and validated. Preset names, output-directory names, and detailed diagnostic/optimization flags remain design details within these decisions.

### Build Acceptance Criteria

- [ ] A clean checkout with documented prerequisites can configure and build from Windows/PowerShell without editing generated files or adding machine-specific paths to tracked files.
- [ ] The supported SDK version is recorded exactly, and a missing or incompatible active SDK produces an actionable diagnostic.
- [ ] Configure and build do not install or upgrade the SDK implicitly.
- [ ] Separate Debug and Release presets use Ninja and isolated build/output directories, without reusing native CMake caches.
- [ ] Required bundled dependencies build from their recorded source revisions with Emscripten; the browser build does not require vcpkg or link native Windows libraries.
- [ ] Configuration excludes desktop graphics, Qt, USD, and shader-tool dependency chains, rather than merely omitting them from the final executable.
- [ ] The application and its linked runtime libraries use compatible pthread settings and static linking.
- [ ] The selected entry point is `app_sample_main_min.cpp`, and exactly one `main()` is linked.
- [ ] Each configuration produces the complete Wasm/JavaScript/worker runtime package. The delivery test page can load a copied package without access to the original source tree or SDK location.
- [ ] The shared minimal framework remains buildable in a separate native Windows validation configuration.

These criteria describe future verification; none are marked complete by this exploration record.

## Codebase Boundaries

- `samples/minimalApp/CMakeLists.txt` links `NauFramework` and `PlatformAppApi` and registers `PlatformApp`.
- That CMake file collects all `.cpp` files in the sample directory. Both `app_sample_main.cpp` and `app_sample_main_min.cpp` currently define `main()`. The port must select the requested entry point explicitly and preserve a valid native target.
- `engine/core/app_framework/src/CMakeLists.txt` publicly links `NauKernel`, `PlatformAppApi`, `CoreScene`, `Graphics`, `ui`, and `VFX`. The small entry point therefore does not currently imply a small build. Isolate the required framework functionality rather than attempting a renderer port as a prerequisite.
- The selected entry point calls `createApplication()` directly, not `runApplication()`. Changing only `src/app/run_application.cpp` would not adapt this sample.
- `src/app/application_impl.cpp` polls pending service initialization tasks. Startup, execution queues, and shutdown must be examined in addition to replacing the sample's outer loop and `sleep_for(100ms)`.
- Application setup registers a threaded background-work service, and the current platform window service starts a message-pump thread. The browser port retains the threaded execution model while adapting platform-specific behavior and avoiding waits on the browser UI thread.
- The selected entry point calls `loadModulesList(NAU_MODULES_LIST)`. Static module registration and service availability must be verified for the browser build rather than assuming desktop DLL loading is available.
- The platform setup rejects non-Windows targets. Windows-specific services and compile definitions remain relevant even when graphics is excluded.

## Suggested Delivery Order

```text
Entry-point selection + minimal dependency profile
                    |
        Emscripten build + core portability
                    |
          Platform service + lifecycle
                    |
           Minimal application in browser
                    |
           Delivery + lifecycle validation
```

Validation accompanies every stage. This is a suggested dependency order, not a commitment to implementing each capability in isolation.

## Milestone Acceptance Checklist

- [ ] The minimal application builds and starts in desktop Chrome on Windows.
- [ ] Nau's application entry point runs on a worker at approximately 10 steps per second in the foreground.
- [ ] Runtime status and an advancing step counter are visible while the test page remains responsive.
- [ ] Background-tab timing is best-effort, with no catch-up burst on return.
- [ ] The minimal platform window service operates without a GPU context.
- [ ] Stop requests execute Nau's shutdown lifecycle and report completion rather than merely terminating the worker.
- [ ] Missing cross-origin isolation produces a clear startup error, and the serving instructions document the required headers.
- [ ] The dedicated minimal framework target excludes graphics, UI, and VFX dependencies and shares existing lifecycle code.
- [ ] The same minimal framework target builds and passes equivalent lifecycle checks on native Windows.

These are planned acceptance criteria, not claims of completed verification. The main scope decisions are settled; implementation details will be resolved in the formal design.

This file supersedes the previous 14-spec cube/rendering milestone with seven proposed capabilities for the minimal application port. Formal proposal, design, requirements/scenarios, and implementation tasks remain to be authored through OpenSpec. No engine or sample implementation changes are made by this document.

## Implementation handoff — 2026-09-19

The preceding sections preserve the original exploration checklist. Subsequent
OpenSpec changes have implemented the native minimal runtime, pinned SDK 6.0.9,
Wasm core portability, browser platform services and browser runtime lifecycle.
The lifecycle's independent real-application target passes 13/13 Chrome cases in
Debug and Release, including approximately 10 Hz updates, Stop, cleanup,
visibility and failure reporting. See the
[lifecycle evidence](openspec/changes/browser-runtime-lifecycle/validation.md).

`minimal-app-web` should call `nau::runBrowserApplication(delegate)` from the
selected `app_sample_main_min.cpp` entry point, link `NauFrameworkMinimal` and
production static PlatformApp, and expose `Module.nauRuntime.status` and `.stop()`
through its page. The [integration guide](NauEngineLite/doc/browser_runtime_lifecycle.md)
documents delegate setup, host requirements, timing and reload behavior.

The selected sample/preset integration, package staging, delivery page/server,
missing-isolation diagnostics, clean-checkout reproduction and relocated Chrome
acceptance remain pending. The independent lifecycle fixture does not complete
those delivery criteria; `emscripten-build` stays at 11/24 tasks.

## Actual sample handoff — 2026-09-20

`minimal-app-web` now builds the selected `app_sample_main_min.cpp` entry through
both real browser presets and runs it with the existing worker lifecycle. Actual
sample Chrome acceptance passes in Debug and Release, including displayed status
and count, approximately 10 Hz updates, real hide/show, Stop and startup/runtime
failure. Native sample builds and lifecycle regressions pass.

Build-graph evidence advances `emscripten-build` to **17/24**. The concrete runtime
inputs for delivery are `build/web-minimal-{debug,release}/bin/MinimalAppSample.js`
and `.wasm`; see the [sample guide](NauSamples/doc/minimal_app_web.md) and
[validation record](openspec/changes/minimal-app-web/validation.md).

The remaining work is complete package staging and stale-output handling,
finished delivery page/server and missing-isolation UX, fresh-checkout reproduction,
and relocated Chrome package acceptance. The sample acceptance harness is temporary
test infrastructure and does not complete those delivery criteria.
