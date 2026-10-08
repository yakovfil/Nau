# Proposal

## Why

Project creation and builds already have reusable tooling, but the editor requires interactive project selection and offers no coherent command interface. Independent editor commands will make project setup, opening and Windows/web builds reproducible from terminals and automation.

## What Changes

- Add `NauEditor.exe project create`, `open`, `compile`, `build` and `inspect` commands with help, version output, console diagnostics and dependable exit status.
- Run create, compile, build and inspect without editor windows or graphics initialization; allow explicit `create --open` and direct project opening.
- Reuse project templates, native module compilation and shared portable build presets; preserve explicit legacy desktop builds.
- Validate paths and selections before executing, report occupied editor instances, and retain interactive startup with no command.
- Document and test the deployed command interface, including external project paths, redirected output and failures.

## Capabilities

### New Capabilities

- `editor-project-cli`: Independent editor commands for project creation, opening, native module compilation, preset builds and inspection.

### Modified Capabilities

None. Existing portable-project-generation and packaged-project contracts remain authoritative; this adds an editor command entry to those workflows without changing their selection rules or GUI controls.

## Impact

- NauEditorPublic executable startup, argument parsing, project loading, process execution, console handling, tests and documentation.
- Existing NauEngineModules ProjectTool/BuildTool and shared packaged-project integration are reused; narrowly scoped adapters may be needed for command selection and deployment.
- Approved Unicode validation repairs cover tool arguments/PCH/shaders, editor and asset filesystem boundaries, native Windows file streams, and generated legacy configuration loading; the retired ui startup request is removed.
- The editor distribution remains a Windows host with its existing runtime dependencies. Web refers to generated application delivery, not a browser-hosted editor.
- No live-editor remote control, scene/asset manipulation commands, automatic project migration, dependency installation or new editor Build/Run selectors.
