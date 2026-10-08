# Proposal

## Why

EditorProject demonstrates a shared Windows/web packaged application, but newly generated projects still receive desktop-only startup, module dependencies and presets. Users must manually reproduce the integration, and different entry commands can select different runtime profiles.

## What Changes

- Generate a shared portable application entry, declaration, thin build/run wrappers and Windows/web Debug/Release presets from the standard code-project template.
- Default new portable builds to `basic-rendering-scene`, with a camera, supported visible geometry and explicit simple materials.
- Resolve the project default declaration consistently across scripts and presets, while supporting explicit alternate declarations and keeping existing project defaults unchanged.
- Make generation and selected-target rebuild aware of portable workflows; avoid unconditional desktop shader compilation, forced native architecture arguments and deletion of unrelated build outputs.
- Keep native editor/cooking module builds and the explicit legacy desktop application route available and isolated.
- Validate freshly generated projects outside the checkout through both CLI creation and editor creation, including build/run parity and failure handling.

## Capabilities

### New Capabilities

- `portable-project-generation`: Generate, configure and build portable code projects consistently through scripts and presets, with visible starter content, isolated outputs and legacy/editor compatibility.

### Modified Capabilities

None. Existing packaged runtime, rendering and non-rendering contracts remain intact; this capability makes their integration available to newly created projects.

## Impact

- `NauEngineModules/project_templates/empty`, project-tool generation/rebuild logic and tests, shared packaged-project CMake/PowerShell integration, and template installation into editor/tool distributions.
- Editor project creation is an acceptance consumer. Its native game-module compilation and existing Build/Run controls remain compatible; no platform selector is added to the editor UI.
- Generated projects require explicit engine/modules locations and provisioned host tools; machine-specific settings stay outside committed project configuration.
- Existing NauDemo/EditorProject builds provide regression coverage; no automatic migration or rewriting of existing projects is included.

## Non-goals

Renderer feature expansion, input/physics/audio portability, replacement of the full desktop renderer, non-Windows host cooking, automatic SDK installation, editor Build/Run UI changes, and automatic existing-project migration.
