# Tasks

## 1. Portable project declaration and build graph

- [x] 1.1 Add and validate the versioned portable project declaration and its generated runtime policy in NauEngineModules; verify malformed declarations, unsupported versions and excluded modules fail with identifying diagnostics for both targets.
- [x] 1.2 Generalize the existing browser project CMake hook/profile for Windows and web, retaining compatibility mapping; verify both configure successfully, conflicting legacy/new options fail, and native configuration works with EMSDK absent.
- [x] 1.3 Wire EditorProject's portable targets and game module to the shared declaration and explicit source graph; inspect native/web links to verify static project registration, no host cooking DLL inputs and no excluded runtime services.

## 2. Shared application startup and native delivery

- [x] 2.1 Replace the browser-only portable entry with one shared entry using the packaged-scene delegate and generated declaration policy; compile it for Windows/web and verify the rendered Windows entry remains independently selectable.
- [x] 2.2 Add reusable delivery-path resolution for the native archive and browser preload path without project platform branches; verify configuration and scene loading from an unrelated native working directory and nested browser serving URL.
- [x] 2.3 Add native portable delivery staging with required runtime dependencies and checked publication; run the actual application after relocation without source/SDK paths in its environment and verify normal Stop/exit plus nonzero failure on a missing archive.

## 3. Shared preparation and build interface

- [x] 3.1 Generalize native preparation to consume the project declaration and rebuilt registration module, retaining the previous tool entry where needed; verify component policy changes reach cooking and both runtime policies without editing duplicate lists.
- [x] 3.2 Add common orchestration for host preparation and Windows/web Debug/Release target builds with explicit locations and isolated outputs; run consecutive builds and verify native-only operations never discover browser tools or overwrite rendered outputs.
- [x] 3.3 Add explicit prepared-archive delivery mode and safe shared-input staging; verify both deliveries contain the selected archive bytes, invalid/missing inputs fail, and the mode works without USD/host cooking tool discovery.
- [x] 3.4 Preserve fresh normal preparation and safe publication under overlapping invocations; verify source/component/declaration changes are consumed, failed preparation does not launch stale output, and concurrent work cannot mix or replace another invocation's selected inputs.
- [x] 3.5 Convert existing web build/run commands into compatible thin wrappers and add the Windows portable run route; exercise configuration selection, prerequisite overrides, browser launch and native launch through the documented wrappers.

## 4. Cross-platform acceptance

- [x] 4.1 Generalize the independent observer and fixture runners for paired native/browser execution; verify initial hierarchy, identities, transforms and properties against authored expectations and compare real updates using controlled time or behavior invariants.
- [x] 4.2 Build and run the production portable project and observer in Windows/web Debug/Release using one selected archive; record delivery/archive hashes and confirm relocated startup, visible logging, component execution and orderly cleanup in all four configurations.
- [x] 4.3 Exercise missing/corrupt package/configuration/scene data, unsupported components and immediate/deferred activation failure on both platforms/configurations; verify startup gates, identifying diagnostics, native exit codes and browser terminal status.
- [x] 4.4 Exercise repeated Stop during pending startup and execution on both platforms/configurations; verify no premature/post-Stop application updates, retained owners and completed eligible cleanup.
- [x] 4.5 Rebuild and smoke-run the existing rendered Windows EditorProject Release route and run affected common-host/package regressions; verify rendering and the original startup behavior remain available and no authored content or unrelated consumer build contract changed.

## 5. Documentation and evidence

- [x] 5.1 Document the common build interface, project declaration, prepared-archive mode, platform run wrappers, prerequisite discovery/overrides and output locations; verify examples distinguish portable non-rendering execution from the preserved rendered Windows route.
- [x] 5.2 Record commands, revisions, tool versions, archive hashes, the four-configuration acceptance matrix and regression results in validation.md; verify every added scenario has evidence and any remaining limitation is explicit.
