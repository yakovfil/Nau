# Design

## Context

See proposal.md for motivation. The common host already runs shared delegates through native and browser scheduling. EditorProject still has two launchers: the rendered SDK route in source/main.cpp and the portable browser entry in source/browser_startup.cpp. The latter uses the reusable PackagedSceneApplication in NauEngineModules, which already runs natively through cmake/probes/scene_startup. The probe is test integration, not a normal native project delivery.

NauBrowserProjectRuntime.cmake selects an explicit CPU scene graph. Browser-specific naming currently controls otherwise portable module selection. EditorProject/web/build.ps1 orchestrates native registration-DLL compilation, Python/USD cooking, browser configuration and staging, with component identities repeated in the script and entry source. The existing reader carries portable type names, so the same cooked records can resolve native64 and wasm32 component identities.

This is a cross-component build/runtime integration change and needs a design. Existing browser and common-host requirements remain in force; the delta adds a native peer rather than weakening their validation or expanding supported services.

## Goals / Non-Goals

**Goals:** Make the portable profile an ordinary application on both targets, remove duplicated project policy and build orchestration, and prove archive portability through actual execution.

**Non-Goals:** Unify renderer APIs, expand the component/service support set, replace the rendered SDK launcher, or create a general engine package manager. Native cooking remains a host operation and may require the full native SDK even though target execution does not.

## Decisions

### 1. Generalize the project profile in NauEngineModules

Introduce platform-neutral packaged-project CMake integration based on the existing explicit scene source graph. Select the portable scene profile independently from Windows/Emscripten toolchain selection. Build both portable targets from matching engine/modules sources and statically register project modules. Keep a compatibility wrapper for the existing browser hook and variables, rejecting conflicting old/new inputs.

This avoids using the desktop SDK graph as the native portable target. SDK DLLs remain host cooking inputs and dependencies of the separate rendered route. Keep NauEngineLite free of concrete project and feature-module lists.

### 2. One portable entry and one project declaration

Rename/extract browser_startup.cpp into a shared portable entry, retaining the existing source/main.cpp for rendered desktop compatibility. The entry invokes the existing common host and packaged-scene delegate. It contains no platform conditionals for startup, module policy or scene validation.

Add a small versioned project JSON declaration containing the profile, required runtime modules, project module identity, supported component names and startup configuration. CMake and native preparation tooling validate this declaration; generate the runtime policy header from it under the build directory. Pass the declaration to the preparation helper instead of repeating --supported-component lists. Component factories still come from the project module, not from arbitrary runtime loading of names in JSON. Optional acceptance additions use a separate explicit test overlay and never alter production policy.

A JSON document fits the existing Python and CMake consumers without introducing a parser dependency. Keeping independent lists in a common header and script was rejected because they can still drift.

### 3. Separate preparation, compilation and delivery

Generalize prepare_browser_project.py for the portable profile, preserving its strict checks, fresh scratch cooking and publish-on-success behavior. Keep the old entry as a forwarding compatibility interface where needed. A common PowerShell driver accepts platform/configuration and explicit engine/modules/project/prerequisite paths. The project wrapper supplies defaults and the declaration path. Host preparation always uses its matching Release SDK and registration DLL independently of target Debug/Release selection.

Normal build-and-run prepares fresh input; no new incremental cache is needed. A separate explicit prepared-archive input bypasses cooking for target compilation/delivery and must validate the selected archive/profile before publication. Missing or corrupt selected inputs fail. This mode intentionally uses the caller's supplied snapshot and does not imply that it matches current source content. Avoid making ordinary runs silently select that mode because an old archive exists.

Both platform deliveries copy/embed the same archive bytes. Acceptance prepares once and supplies that exact artifact to both builds, recording hashes before delivery and after extraction. Separate preparation invocations need not produce byte-identical output if metadata contains generated values; the portability claim is about the selected archive, not deterministic cooking.

### 4. Keep platform differences at the delivery boundary

Use platform-specific packaging adapters for native executable/runtime dependencies versus browser loader/Wasm/preload/server files. Resolve the native default archive relative to the executable through reusable platform support; browser preload uses its virtual path. Both expose the same internal VFS/configuration names. An explicit archive override may be used for acceptance. Do not depend on process working directory or embed source-machine absolute paths.

Use existing native window/Stop handling and browser asynchronous Stop through the common host. Platform helpers belong in engine infrastructure; no new platform loop goes into the project. Keep native return codes and browser terminal status contracts. PackagedSceneApplication retains its checked startup and passive reference policy on both targets.

### 5. Preserve existing entry points and isolate outputs

Keep EditorProject/run_web.bat and web/build.ps1 as thin compatibility wrappers over common orchestration, retaining supported configuration and prerequisite overrides. Add a documented Windows portable run route. Do not change the existing rendered Windows default/preset selection. Use explicit portable selection and independent targets/build directories to avoid replacing its executable or SDK cache.

All new output stays below EditorProject/build: separate host registration, preparation, platform/configuration build and delivery directories. Shared preparation publication uses an exclusive operation or isolated staging paths so concurrent runs cannot replace content another build is consuming. Paths to external SDKs remain configurable and discovered defaults remain conveniences, not prerequisites. Native-only operations do not inspect EMSDK; delivery from a prepared archive does not inspect USD or host cooking tools.

### 6. Extend existing independent acceptance

Reuse startup_probe.cpp and the authored fixture, and generalize the existing browser/preparation runners into paired native/browser checks. Build the actual portable application as well as the observer; never count the observer alone as product acceptance. Compare initial runtime snapshots to authored expectations and test component motion with controlled time or invariants, because native and browser cadences differ.

Exercise relocation from an unrelated native working directory and a nested browser URL, archive failures, declaration rejection, unknown components, activation failure and Stop during pending work. Retain the browser console severity/duplicate checks and check native output/exit status. Rebuild and smoke-run the rendered Windows Release route and affected common-host/package suites. Record commands, revisions, tool versions, hashes and limitations in validation evidence.

## Risks / Trade-offs

- Profile names currently influence several CMake branches -> audit all references and retain explicit compatibility mapping with negative configuration tests.
- Static native runtime and shared host SDK have different purposes -> separate caches and verify host libraries never enter portable target links.
- Shared declarations can drift from actual registrations -> cook with the rebuilt project DLL and retain checked runtime factory resolution.
- Fresh cooking has a runtime cost -> keep it for correctness; expose explicit prepared-archive reuse without silently accepting stale content.
- Generalizing packaging can hide missing native DLLs -> validate a relocated delivery without SDK paths in its environment.
- Legacy rendered startup is broad and fragile -> preserve its selection and code path, with a Release build/run regression before completion.

## Migration Plan

1. Add generic integration and declaration consumption behind explicit portable selection, retaining browser compatibility entry points.
2. Switch the browser portable application to the shared entry and wire the Windows portable target to it.
3. Route build wrappers through common preparation/delivery orchestration and add paired acceptance.
4. Validate all four portable configurations and rendered Windows compatibility before documenting the new normal workflow.

No authored asset migration is required. Rollback restores the previous browser integration/wrappers; the rendered SDK route remains independently usable. Generated caches are disposable and never committed. No repository-wide generated-template migration is included.
