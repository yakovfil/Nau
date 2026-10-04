# Tasks

Accepted validation exception (2026-10-04): the user explicitly requested skipping Editor/USD validation after the missing Qt/OpenUSD packages and TLS download failure were reported. Those builds, runtime workflows, and new regression tests are recorded as **SKIPPED**, not passes, in validation.md. Implementation tasks retain their source changes and test coverage; task 5.3 records this authorized waiver. Six existing Release CTest failures remain failed in the evidence.

## 1. Detach runtime integration

- [x] 1.1 Remove concrete UI state, includes, update calls, and link dependencies from NauEngineLite's full application framework; verify source references are gone and full/minimal/scene framework targets configure.
- [x] 1.2 Remove UI invocation and dependencies from Graphics while preserving screen-text and ImGui render ordering and state; verify Graphics compiles and its configured link graph has no ui dependency.

## 2. Retire UI implementation and tools

- [x] 2.1 Remove NauEngineModules/modules/ui, bundled Cocos2d, exclusive resources, and test_ui; verify tracked-file and target inventories contain no implementation remnants and preserve shared third-party dependencies with remaining consumers.
- [x] 2.2 Remove USD UI adapters, registrations, and exclusive GUI schema/plugin integration; verify UsdTranslator and retained USD tools compile and their remaining tests pass.
- [x] 2.3 Add explicit unsupported legacy UI diagnostics at retained conversion entry points using existing asset/type identification; verify regression fixtures produce a failure/unsupported result and preserve source asset bytes.

## 3. Retire editor and sample consumers

- [x] 3.1 Remove nau-gui-editor and usd-ui-editor-synchronizer implementation/build/registration paths; verify editor module inventories and menus no longer advertise the retired feature.
- [x] 3.2 Remove UI-specific branches and links from editor-core, editor-engine, shared USD inspector/translator code, viewport handling, and resource copying; verify the editor builds with its Qt shell and non-UI scene workflows intact.
- [x] 3.3 Add editor handling and regression coverage for identifiable unsupported legacy UI assets; verify a clear diagnostic, unchanged asset bytes, and continued editor operation.
- [x] 3.4 Remove UiSampleApp and its exclusive assets, distribution entries, and launch instructions; verify source and installed sample discovery retains the other targets without scanning a retired UI directory.

## 4. Clean distribution and documentation

- [x] 4.1 Remove retired UI/Cocos imports, exports, headers, module lists, shader/resource staging, and target assumptions from SDK integration and empty-project templates; verify a fresh installation inventory has no retired artifacts.
- [x] 4.2 Update affected active build/profile checks and retain non-UI tests that previously inherited Cocos transitively; verify no retained test is removed merely because it linked the full framework.
- [x] 4.3 Update current component guides and applicable NauDocsPublic pages with the breaking retirement, unsupported old assets, clean rebuild guidance, and independent screen-text alternative; verify current instructions do not advertise GUI authoring and historical archives are unchanged.

## 5. Validate the coordinated change

- [x] 5.1 Configure and build supported native module/sample and NauDemo graphs in fresh Debug and Release outputs; inspect configured target/link graphs and run affected framework/module CTest suites, recording absence of Cocos/UI inputs and all results.
- [x] 5.2 Run native NauDemo text framebuffer acceptance in Debug and Release and smoke-test remaining graphics samples including inputDemo resize/additional-window behavior; verify scene output, text, ImGui diagnostics, and normal shutdown.
- [x] 5.3 Record the explicit user waiver of Editor/USD Debug/Release build, launch, scene open/edit/save, non-UI conversion, and regression execution; identify the unavailable prerequisites and preserve these results as skipped rather than passed.
- [x] 5.4 Build browser NauDemo Debug and Release and run existing browser/text acceptance checks plus applicable native/browser minimal lifecycle fixtures; verify preserved behavior with no retired UI dependency.
- [x] 5.5 Install a fresh SDK with remaining samples, relocate it, and build/run the empty template and a representative installed sample; verify no source-checkout dependency or retired UI export/resource is required.
- [x] 5.6 Record repository identities, source/graph/install audits, commands, results, and baseline versus new failures in retirement evidence; run strict OpenSpec validation and leave unavailable or failing checks explicitly incomplete.
