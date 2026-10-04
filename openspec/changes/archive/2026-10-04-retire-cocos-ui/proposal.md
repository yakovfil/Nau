# Proposal

## Why

Desktop graphics and the application framework currently pull in the Cocos2d-backed UI implementation, including platform-specific prebuilt dependencies, even for applications that do not use UI. Retiring this implementation removes that coupling and its obsolete consumers while preserving rendering and the independent screen-text capability.

## What Changes

- **BREAKING**: Remove the current `ui` module, its public API, bundled Cocos2d tree, exclusive dependencies/assets, and UI implementation tests. No replacement widget backend is provided.
- Remove concrete UI includes, links, service lookups, update calls, and render calls from Graphics and the full application framework.
- **BREAKING**: Retire UiSampleApp and the editor GUI-authoring, synchronization, and USD UI translation paths that require this API. Keep the editor shell and non-UI scene/content workflows usable; existing UI content is unsupported and must be reported explicitly when encountered through retained workflows.
- Clean build/module registrations, installed SDK exports, project templates, packaging, current documentation, and affected tests across the component repositories.
- Preserve ImGui diagnostics, NauScreenText, native/browser NauDemo, remaining samples, and minimal/scene runtime behavior.

## Capabilities

### New Capabilities

- `cocos-ui-retirement`: Defines a Cocos-free runtime/SDK graph, explicit retirement of UI consumers, and preservation of unrelated workflows.

### Modified Capabilities

- `external-samples`: Exempts the deliberately retired UiSampleApp from sample target and behavior preservation.
- `minimal-runtime-profile`: Updates desktop compatibility to explicitly exclude the retired Cocos-backed UI features.

## Impact

NauEngineModules owns the deleted UI implementation and affected Graphics, USD tools, SDK integration, and templates. NauEngineLite owns framework integration. NauSamples owns UiSampleApp and sample discovery/distribution. NauEditorPublic owns GUI editing and synchronization consumers. NauDemo supplies native/browser rendering and text regression coverage. Current documentation in affected repositories, including NauDocsPublic where applicable, must describe the retirement. Existing archived evidence remains historical.

This builds on the completed but unarchived `add-cross-platform-screen-text` change; its implementation and artifacts are preserved. No commit, push, or implementation is part of this proposal workflow.
