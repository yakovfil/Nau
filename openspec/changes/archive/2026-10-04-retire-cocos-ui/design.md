# Design

## Context

See proposal.md for motivation and the confirmed retirement scope. This is a coordinated change across independently versioned components.

The observed coupling is concrete: Graphics links `ui` and calls `UiManager::render` in `render_window/render_graph.cpp`; `graphics_impl.cpp` also includes the UI header. NauEngineLite's full application framework links `ui`, caches a manager pointer, and calls `update(dt)` before the main game step. Minimal and scene variants already exclude this integration. The UI public Node inherits from `cocos2d::Node`, so deleting only Cocos cannot preserve the UI API.

UsdTranslator compiles a `ui_translator` adapter family and links ui. Editor consumers include `editor-core`, `editor-engine`, `nau-gui-editor`, `usd-ui-editor-synchronizer`, and UI translator/inspector paths in `usd-asset-editor-common`. UiSampleApp uses Cocos directly. Sample discovery scans subdirectories and installation copies the sample tree. SDK and empty-template files explicitly import UI/Cocos targets.

The completed `add-cross-platform-screen-text` implementation is the baseline. Its overlay pass shares the desktop render graph with the UI call but has separate rendering and shutdown resources.

## Goals / Non-Goals

**Goals:** Make the supported build and distribution graph independent of Cocos and remove concrete UI integration from shared runtime code. Keep non-UI consumers buildable and preserve their behavior. Make retired asset handling explicit.

**Non-Goals:** Replacing widgets, preserving UI ABI/source compatibility, converting old UI assets, adding a generic overlay plugin architecture, removing ImGui, or removing unrelated platform dependencies. No broad third-party cleanup based solely on names or proximity.

## Decisions

1. **Delete the retired implementation and API.** Remove `modules/ui`, including Cocos, its exclusive shaders/assets and test_ui, rather than retain a default-off option or no-op compatibility library. A disabled tree would retain the binary maintenance burden and a stub would imply unsupported compatibility. Preserve shared libraries still used by other modules, such as PNG, compression, and hashing.

2. **Remove concrete integration at its source.** Delete framework UI state, forward declarations, includes, update calls, and links. Delete Graphics' UI render invocation and unused include/link. Preserve adjacent screen-text, ImGui, VFX, render-target state, and presentation ordering. No generic hooks are needed for a feature being retired.

3. **Remove feature consumers while keeping their hosts.** Remove the USD UI adapter family and registrations, editor GUI editor and synchronizer, and their menu/asset-creation registrations. Prune UI-specific branches of shared viewport, inspector, application startup, and translator code; do not remove the entire editor, shared inspector, or UsdTranslator. Remove exclusive GUI schema/plugin targets once no retained runtime path needs them. For retained entry points, recognize legacy UI assets using existing metadata/type identification and issue an unsupported-content diagnostic before translation or mutation. Recognition may retain minimal type identifiers; it must not retain the old widget implementation. Pure schema/data definitions with independent non-UI consumers are kept only with documented evidence of those consumers. The editor common `NauUsdSceneUITranslator` is such an independent consumer: it forwards USD notices to Qt scene inspectors/outliners, contains no Cocos references, and remains in place.

4. **Treat installed and source builds equally.** Remove stale imports from `cmake/for_build`, empty templates, module registration lists, and editor/sample resource copy commands. Delete UiSampleApp and exclusive resources so directory discovery and installation cannot resurrect it. Validate using fresh output/install directories; stale local UI DLLs must not make a test pass. Document clean rebuild requirements for existing SDK users rather than deleting user-managed installations automatically.

5. **Retain meaningful tests.** Remove tests solely for retired widgets or GUI authoring. Keep animation, scene, input, platform, render, and framework tests even when their old dependency on Cocos was transitive. Add focused regression coverage for unsupported legacy assets and retained editor registration behavior. Audit the configured target/link graph and installed inventory as acceptance checks; source-search results alone do not prove independence.

6. **Reconcile compatibility contracts narrowly.** Existing external-samples and minimal-runtime-profile preservation requirements gain explicit retirement exceptions. Historical migration requirements and archived evidence remain historical. Screen-text contracts need no changes; both its native and browser acceptance suites remain regression gates.

## Risks / Trade-offs

- Public UI API removal breaks downstream UI applications -> document the breaking removal and identify the last compatible repository combination; provide no misleading stubs.
- Shared editor/translator files mix GUI-specific and general behavior -> remove feature branches and registrations, then exercise ordinary scene editing and non-UI conversion.
- Old UI assets can otherwise appear to import successfully -> test explicit unsupported diagnostics and unchanged input bytes at retained entry points.
- UI and screen text share final rendering code -> exercise label framebuffer checks, scene output, resize, and shutdown in native Debug/Release.
- Stale SDK exports or copied libraries can hide missed references -> fresh configure/install and relocated-template builds are required.
- Existing local toolchain or runtime failures can complicate validation -> record baseline versus new failures and keep unavailable validation tasks incomplete.

## Migration Plan

Apply component changes together locally, removing runtime coupling, exclusive consumers, and distribution references before clean builds. Record all affected repository identities and working-tree deltas used for verification. Build native Debug/Release, run focused module/framework tests and remaining sample smoke checks, validate editor and USD workflows, then run browser/text regressions and a relocated SDK template test. Update current guides and release notes; preserve historical docs as historical where clearly labeled.

When commits are requested, commit within components before updating parent submodule revisions. Rollback restores the coordinated prior component revision set, including the old UI API and consumers; do not mix old UI-dependent editor binaries with the new SDK. No user asset conversion or deletion is part of migration.

## Accepted validation exception

On 2026-10-04 the user explicitly requested skipping Editor/USD validation because Qt/OpenUSD were unavailable and the project download failed TLS verification. Their build/runtime/test checks are recorded as SKIPPED rather than passes in validation.md; the implementation and regression sources remain part of this change. This explicit exception supersedes the requirement to execute those validation tasks in this local run. The user separately confirmed the remaining Release scene and ImGui visual output.
