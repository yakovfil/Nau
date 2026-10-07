# Tasks

## 1. Portable browser project build

- [x] 1.1 Add reusable non-rendering browser project integration in NauEngineModules with explicit portable module/source selection and the recorded Emscripten version; verify configuration rejects unsupported modules and the generated link graph excludes native SDK, USD, Qt and excluded service implementations.
- [x] 1.2 Separate EditorProject's portable game component sources from desktop module dependencies and statically register its game module for web; verify Debug and Release target builds resolve the project factories without DLL loading.
- [x] 1.3 Add project browser build/delivery helpers and isolated native-tool, target and delivery output paths under ignored project build directories; verify configuration separation, actionable missing-prerequisite failures and absence of generated engine-tree outputs.

## 2. Portable scene loading and strict validation

- [x] 2.1 Extract/share the existing compiled-scene reader and registration without desktop format dependencies, add portable component type names with legacy native fallback, and verify a native-cooked scene loads through the portable target while desktop registration and old scene reading remain functional.
- [x] 2.2 Add packaged VFS configuration and asset-database initialization for the profile; verify valid entries resolve through the mounted archive and malformed configuration, missing entries and unresolved identities return checked errors.
- [x] 2.3 Implement the profile's supported component policy, including passive camera/static-mesh data and registered service-independent project components; verify hierarchy/properties survive and unknown or excluded-service components fail with object/type diagnostics before activation, while legacy missing-component behavior remains available outside this profile.
- [x] 2.4 Implement required asset-reference presence/readability validation without requesting GPU views; verify a valid reference resolves and a missing or unreadable dependency blocks startup.

## 3. Native preparation and package delivery

- [x] 3.1 Provide host-native project component registration for asset cooking using the same definitions as the browser game module; verify cooking retains non-default MyMover/MyRotator identities and properties.
- [x] 3.2 Add targeted preparation of configuration, compiled startup scene, asset mappings and the required non-rendering data dependency closure using existing native asset tools; verify a clean preparation succeeds without an old asset database/cache or authored-content changes.
- [x] 3.3 Propagate scene compiler/output failures and connect source, metadata, configuration and component-definition dependencies to preparation; verify changed inputs rebuild affected outputs and missing inputs or failed writes cannot report stale delivery as success.
- [x] 3.4 Package prepared content with the existing archive tool and stage relocatable browser delivery; verify the archive contents resolve required identities and delivery runs from a nested URL outside the checkout without loose-source or SDK access.

## 4. Common-host startup and shutdown

- [x] 4.1 Connect EditorProject to the common host with portable services and ordered registration, mount, configuration, checked scene loading and awaited activation; verify Running and ordinary component updates remain gated until activation completes.
- [x] 4.2 Add a checked required-scene startup path while retaining existing optional-scene behavior; verify missing, corrupt and unactivatable scenes propagate failure rather than completing startup after a log message.
- [x] 4.3 Integrate idempotent Stop and failure cleanup with pending scene work, scene deactivation and asset/package owner lifetimes; verify repeated Stop during startup and execution settles safely and reports actual teardown completion or failure through the production lifecycle bridge.

## 5. End-to-end acceptance and compatibility

- [x] 5.1 Add a separate editor-authored acceptance fixture containing hierarchy, non-default transforms and the project's mover/rotator properties; verify expected identities/properties in the cooked and activated scene without modifying the user's main scene.
- [x] 5.2 Run the actual EditorProject main scene and component fixture in real-browser Debug and Release deliveries; verify actual hierarchy, transforms, properties, required asset resolution, component updates and successful terminal cleanup using runtime observations rather than page-side substitutes.
- [x] 5.3 Run browser failure cases in both configurations for missing/corrupt package/configuration/scene data, unresolved required references, unknown and excluded-service components; verify identifying diagnostics, no Running transition and completed eligible cleanup.
- [x] 5.4 Exercise relocated delivery and Stop during pending mount/load/activation and execution in both configurations; verify browser responsiveness, no early/post-Stop updates and safe completion of accepted asynchronous work.
- [x] 5.5 Rebuild native EditorProject Release and run affected common-host, portable-package and minimal-runtime checks plus existing rendered NauDemo native/web smoke checks; record results demonstrating their prior behavior remains supported.

## 6. Documentation and evidence

- [x] 6.1 Document reusable integration, EditorProject build/serve commands, configurable native prerequisites, generated output locations and the supported component/data boundary; verify instructions cover a clean build without machine-specific Qt/USD paths or implicit tool installation.
- [x] 6.2 Record commands, component revisions, SDK/tool versions, Debug/Release acceptance results and any remaining limitations in the change validation evidence; verify every specification scenario is mapped to observed evidence and the milestone is described as non-rendering startup support.
