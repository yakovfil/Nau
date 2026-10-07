# Design

## Context

`NauDemo/EditorProject` is an editor-created desktop project. Its generated CMake consumes an installed native SDK and its game module declares graphics, animation, input and physics dependencies. The application already uses the common application host, but its delegate initializes desktop services and finds configuration through native filesystem paths.

The separate rendered NauDemo browser application demonstrates Emscripten 6.0.9, static module registration, portable asset archives and the browser host lifecycle. Its dependency inventory and cube configuration are specific to that application. They are evidence for the reusable path, not a generic editor-project implementation.

The existing host scene compiler translates USD and writes the engine's compiled scene container. The scene reader under `modules/asset_formats/src/scene` uses container streams and serialized scene data, but its module currently registers it alongside desktop format loaders. CoreScene provides deserialization, activation and component updates. Its missing-component fallback is useful for other consumers but cannot establish successful startup for this profile.

The project's current main scene contains a transformed root, a mesh reference and a camera. It does not instantiate its registered MyMover/MyRotator types, so startup of that scene alone cannot validate project component properties or updates.

## Goals / Non-Goals

**Goals:**
- Build the actual editor project as Debug and Release WebAssembly using reusable module-owned integration.
- Cook editor-authored content on the host and load its compiled scene through the production package, VFS and asset paths in the browser.
- Preserve scene hierarchy, identity, transforms, reflected properties and project component behavior.
- Gate Running on successful scene activation, and complete asynchronous cleanup on failure or Stop.
- Keep native project builds and existing rendered demo behavior compatible.

**Non-Goals:**
- Rendering, GPU resource views, physics simulation, animation playback, audio or input handling.
- USD conversion in WebAssembly, editor export UI, or porting every native SDK module.
- Replacing the compiled scene format, changing widget behavior, or changing the authored main scene to simplify acceptance.

## Decisions

### 1. Add an opt-in browser startup profile in NauEngineModules

Provide reusable CMake integration in the modules repository, with explicit portable source/module selection. The graph includes the common application framework, platform lifecycle, asset/package services, CoreScene and compiled-scene reading, plus statically registered project code. Extract or share existing portable integration where appropriate; do not make the generic profile depend on NauDemo-owned configuration or its source inventory.

Select the profile in EditorProject without importing the native SDK into the Emscripten link. Separate the project's portable component sources from desktop-only link declarations. Unsupported module requests fail configuration with the relevant dependency named. Keep concrete feature selection out of NauEngineLite.

Use the existing pinned Emscripten version initially. Place target builds, native preparation outputs and browser delivery in distinct ignored directories under the project build directory, separated by configuration. Host tools are native processes with their own toolchain, never cross-compiled executables invoked during cooking.

Alternative: reuse the rendered demo graph unchanged. Rejected because it adds rendering dependencies and embeds application-specific assets and configuration. Linking installed desktop SDK binaries is not an option for WebAssembly.

### 2. Cook the startup asset closure using native tools

Keep USD translation on the host. Build/load a matching native registration of the project's game components before scene compilation so reflected custom types and properties survive cooking. Reuse the existing asset compiler, UID mappings, compiled scene format and portable archive writer. Add the required project-module registration and targeted preparation plumbing to the host tools without changing their existing desktop defaults.

Start preparation from project configuration and the startup scene; include the asset database mappings and data dependencies required by this non-rendering profile. Retain referenced mesh/material identities and include required payloads as data, without requiring GPU views or shader compilation. The existing restricted CPU glTF loader is not a promise that all editor mesh formats can be decoded: this milestone validates reference resolution and payload availability, not rendering-ready asset views.

Build dependencies cover authored files, metadata, configuration and component definitions. A failed conversion or archive write fails the build and cannot select an old successful package. Propagate compiler write errors and verify produced outputs where the current compiler relies on assertions or unchecked results. Do not depend on an existing ignored asset database/cache, or alter authored content during preparation.

Alternative: load USD directly or hand-author a web JSON scene. Both bypass the editor-to-runtime path being validated; USD also brings an unsuitable browser dependency graph.

### 3. Expose the existing portable compiled-scene reader

Factor the scene container reader and its registration into a portable target usable by this profile and the desktop format module. Share the format definitions and implementation rather than maintaining a web copy. Register each loader once in a consumer. Keep host scene building and unrelated desktop loaders outside the browser graph.

Compiled component records gain an additive `componentTypeName` field. Native and WebAssembly use different width-dependent hashes, so records with a name resolve their type using the consuming runtime's hash. Keep the numeric field as a 64-bit legacy value and preserve native reading of older records without names. Newly cooked browser scenes require names; unknown names still fail the strict component policy. Missing-component preservation retains both fields. This format adjustment was approved during implementation.

Mount the delivered archive with the engine's existing package reader and VFS. Resolve packaged configuration, asset database entries and startup scene through those services. Provide a VFS-based configuration path instead of walking native directories. Delivery URLs are relative to the served package, so moving it to a nested URL does not require rebuilding or a host filesystem fallback.

Missing or corrupt required configuration, mappings, scene containers or dependency payloads produce a checked startup error. Merely opening an archive or finding scene bytes does not complete startup.

### 4. Use an explicit non-rendering component policy

Register project component factories before deserializing the scene. Support scene transforms, passive camera and static-mesh reference data, and registered project components that operate on the available services, including this project's mover/rotator. Camera/mesh presence does not enable rendering.

Apply strict component validation to this profile before activation. Unknown types and known components requiring excluded services fail with object and component identity. Use an explicit supported type/service policy; factory registration alone does not demonstrate that a component is safe to activate. Do not silently instantiate MissingComponent placeholders or remove unsupported components. Preserve the existing fallback for other profiles.

Validate required asset references through the package mappings before Running. Preserve references and properties even when their rendering use is outside this milestone. Add a separate editor-authored acceptance fixture with hierarchy, non-default transforms and MyMover/MyRotator properties; keep the user's main scene intact.

### 5. Compose the common host with checked scene startup

The project uses the common host and a portable delegate/service setup. Startup proceeds through registration, package mount, packaged configuration/database initialization, checked scene deserialization, policy validation and awaited activation. The host remains Starting until every required stage succeeds. Updates reach active project components only after this gate.

Provide a checked startup-scene path or explicit strict policy: the current helper can log a missing scene and return normally, which is insufficient here. Preserve optional-scene behavior for consumers that rely on it. Keep generic lifecycle changes in the framework and scene-specific implementation in the modules/project integration.

The checked profile registers an activation diagnostics collector. SceneManager reports synchronous and asynchronous activation errors after accepted operations settle, including already-rejected tasks; the checked delegate rejects startup on those errors. Consumers without this collector retain their existing best-effort activation behavior.

Stop or startup failure cancels further startup work and waits for pending operations to settle before releasing their owners. Deactivate scenes before destroying asset services and unmounting content; reuse the common host's asynchronous teardown and idempotent Stop behavior. Surface real host status and errors to the existing browser lifecycle bridge, without introducing demo-only production test hooks or simulated success in HTML.

### 6. Validate actual runtime state and compatibility

Acceptance uses clean host preparation and real browser Debug/Release builds. Load both the project's main scene and the separate authored component fixture. Observe actual activated scene identities, hierarchy, local transforms, reflected properties and component updates through a test consumer/observer of production runtime APIs. Compare with explicit authored expectations, not merely serializer round trips or log strings. Where useful, read the same compiled package in a native test consumer to separate format failures from browser lifecycle failures.

Exercise relocated delivery, missing/corrupt configuration or package entries, invalid compiled scene data, unresolved required asset references, unknown and service-dependent components, and Stop while startup/updates are pending. Running must remain unreachable on required failures; cleanup must finish without callbacks accessing released owners.

Rebuild the desktop EditorProject Release target and run focused common-host, portable-package and minimal-runtime regressions plus existing rendered NauDemo native/web smoke checks. Record commands, SDK/tool revisions and the deliberate non-rendering boundary in project and reusable integration documentation.

## Risks / Trade-offs

- **Host/runtime component registration can diverge.** Build both from the same project definitions and test non-default custom properties after cooking and activation.
- **Native imports may assume the full SDK or global asset imports.** Introduce targeted startup preparation and profile-specific services while retaining existing desktop defaults; validate from a clean generated-output directory.
- **Passive data can be mistaken for enabled services.** Document the supported component policy and reject service-dependent types before activation; do not report mesh rendering or physics success.
- **Shared scene-reader extraction may change desktop registration.** Use one implementation with explicit registration ownership and regression coverage of existing native consumers.
- **Pending asynchronous operations can outlive startup failure.** Test Stop at each observable lifecycle boundary and verify teardown completion, not just a status transition.
- **The initial supported set is deliberately limited.** Additional modules require later profile extensions and their own service/asset acceptance criteria.

## Migration Plan

Add the profile and delivery helper as opt-in paths, then enable them in EditorProject. Document native host prerequisites using configurable locations rather than machine-specific paths. Generated artifacts remain disposable. Rollback removes the web selection/integration without rewriting project content or invalidating the existing native build and compiled asset formats.
