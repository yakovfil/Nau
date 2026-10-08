# Design

## Context

See proposal.md for motivation. `editor/source/editor/nau_main.cpp` currently acquires `NauRunGuard` before parsing arguments and returns `false` (success) on conflict. `NauApp` parses only `--ignore-project-modules`; `NauEditorApplication::loadProject()` always opens a modal chooser. Initialization subsequently loads USD plugins, compiles the project module and starts graphics/editor services.

`NauProject::create()` calls the shared ProjectTool API, then finalizes editor metadata and scene state. `NauProject::load()` can return a non-null object even when loading fails, so pointer existence is insufficient validation. `NauWinDllCompilerCpp` invokes BuildToolCmd with the native DLL preset, chooses configuration from the editor build, and collects output only after completion. The editor GUI's build action can copy already-built binaries; it is not suitable as the new CLI build implementation.

Generated projects already have portable configure/build presets that invoke the shared PowerShell build driver. Native editor modules and legacy SDK applications remain separate routes. The portable-project-generation specification remains unchanged.

The executable is declared `WIN32` in CMake and dynamically links editor/Qt/USD libraries. Avoiding graphics initialization does not make it a standalone tool without those installed DLLs.

## Goals / Non-Goals

**Goals:** Separate command dispatch from interactive startup; reuse existing project and build ownership; make failures observable from an automation process; retain native editor compatibility and project-controlled portable selection.

**Non-Goals:** IPC, remote control, simultaneous editing sessions, scene operations, generic command plugins, automatic migration, dependency installation, minimal-dependency CLI packaging, changes to GUI Build/Run selection or a new persistent project configuration format.

## Decisions

### 1. One executable, early command dispatch

Introduce a typed command parser/dispatcher before the GUI instance guard and editor initialization. Parse Unicode arguments from the Windows command line correctly. Help/version and invalid commands return immediately. Batch commands use core application/process facilities without constructing editor windows or initializing USD/graphics services. Only interactive startup and explicit opening acquire the GUI guard and create the GUI application. Avoid creating a QCoreApplication and then a second QApplication in the same process; choose the application kind once from the parsed operation, including `create --open`.

Keep command parsing separate from `NauApp`'s current parser so arguments are parsed once and explicit project selection is passed as structured startup options. Preserve the old no-command option path. A separate CLI executable would simplify dependencies but would change the agreed interface and add distribution work.

### 2. Command grammar and defaults

```
NauEditor.exe --help
NauEditor.exe --version
NauEditor.exe project create --directory <parent> --name <name> [--template empty] [--open]
NauEditor.exe project open --project <file-or-directory> [--ignore-project-modules]
NauEditor.exe project compile --project <file-or-directory> [--config Debug|Release]
NauEditor.exe project build --project <file-or-directory> --preset <portable-build-preset>
NauEditor.exe project build --project <file-or-directory> --preset <legacy-configure-preset> --config <Debug|Release> --output <directory>
NauEditor.exe project inspect --project <file-or-directory>
```

All command levels support help. Require preset selection for build; do not infer a route from the editor build type. Portable presets own configuration and declaration, so reject portable `--config`/`--output` overrides rather than silently ignoring them. Compile defaults to the editor distribution configuration and the existing native DLL route. No JSON output contract in this first version.

Resolve project paths once against the invocation directory, accept exactly one project file for directory inputs, and validate JSON and required project identity before constructing mutable editor state. Reuse existing version compatibility rules, but report an upgrade requirement without a modal prompt or automatic modification. Inspection can report an incompatible version without upgrading; opening must reject it.

### 3. Reuse generation and distinguish compile from build

Creation uses the deployed `empty` template by default and the ProjectTool generation API with solution generation disabled. Extract/reuse necessary editor metadata finalization so command-created projects open normally, without duplicating template substitutions or depending on widgets and global editor services. Preflight destination existence and template validity; never delete an existing destination for retry. On a partial generation failure, report the path and failure rather than claiming a usable project.

Native compile delegates to BuildToolCmd's existing `compile` route with explicit configuration and native DLL preset. Preserve native compiler inputs and avoid loading the built DLL in the batch process. Do not call the editor startup sequence or remove existing DLLs before validating inputs.

Portable build invokes CMake configure and build presets from the project working directory. Resolve a selected build preset to its configure preset rather than assuming their names match; use supported CMake preset discovery/evaluation and reuse existing resolution where possible. This enters `NauPackagedProjectPresets.cmake` and the shared build driver, preserving declaration validation, cooking, locking, output isolation and prepared-archive settings already present in project presets. Do not duplicate module/profile lists in editor code or dispatch by preset name prefix alone.

Legacy build uses the existing full BuildToolCmd build route with explicit configuration and destination, compiling sources and assets. It must not use the GUI copy-only flags. Reject ambiguous/unsupported routes and unsafe source-overlapping destinations before invocation. No clean operation is introduced.

### 4. Direct opening remains an editor session

Pass a validated project to the existing initialization path, bypassing only the chooser. Preserve recent-project handling after successful load and the existing module compilation/loading behavior, including the explicit ignore option. Report initialization failure accurately; a failed initialization must not be converted to success merely because the process started. Existing tolerance for module compilation errors in interactive startup is retained and diagnosed rather than silently tightened for all users.

`open` runs the editor in the invoked process and returns its eventual exit status. `create --open` transitions into the same route after successful creation. If the guard is occupied, report nonzero and the created path if creation already completed; do not roll back a successfully created project or contact the running editor. No-argument startup still presents the chooser.

### 5. Console output and process lifetime

Keep the GUI subsystem. For command mode, preserve inherited redirected standard handles; attach to the parent console only where needed and do not allocate a visible console window for ordinary GUI startup. Route command diagnostics to stdout/stderr and forward child output incrementally. Use executable plus argument-list process APIs, never shell-concatenated user input. Wait for each child to finish, distinguish start failure/crash/nonzero exit, and prevent later stages after a failure.

Define documented result categories: 0 success; 2 invalid command/project/selection; 3 missing prerequisite; 4 execution or initialization failure; 5 editor instance conflict. Include downstream exit status in diagnostics rather than assuming it fits these categories. Synchronous GUI commands return only when the editor exits. Document Windows GUI-subsystem shell waiting, including `Start-Process -Wait -PassThru` and `start /wait` where appropriate, and verify with actual subprocess capture rather than relying on an interactive shell prompt.

Independent commands may run alongside the editor, but this does not authorize bypassing loaded-DLL file locks or concurrent writes to the same project. Preserve shared portable build locking and report native file-lock/build failures. No broad editor-session locking redesign is included.

### 6. Inspection and dependency discovery

Inspection reads project metadata and preset/declaration files without calling mutable `NauProject` save/settings paths. Include visible configure/build preset names and distinguish them, resolve supported includes/inheritance/user presets consistently with build dispatch, and report default declaration/profile or explicit absence. Malformed present files fail. Inspection needs no SDK, compiler or Emscripten activation; a CMake executable may be used for preset interpretation and must be documented if required.

Resolve deployed project/build tools and templates relative to the editor installation; preserve documented environment overrides for engine/modules/SDK/USD/tool locations in underlying workflows. Missing installations fail with actionable paths. Do not embed this workstation's Qt or SDK locations. Verify all necessary template/tool payloads are deployed by the editor target.

### 7. Approved Unicode asset-loading repair

Opening the Unicode acceptance project exposed ANSI filesystem conversions in the editor engine and asset importer. The user approved repairing these boundaries and removing the retired `ui` startup request. Shared tool filesystem strings carry UTF-8; convert explicitly to native filesystem paths at API boundaries and back to UTF-8 for metadata, USD identifiers and subprocess arguments. Preserve native path objects for filesystem operations. The Windows native filesystem resolves UTF-8 root/file paths explicitly, and file streams recover handle filenames through the wide API before converting back to UTF-8. Regression coverage reads a payload from a Unicode root and filename. Template subdirectories use filesystem-relative paths, avoiding separator-dependent string replacement. Mount staged legacy editor resources when present, with the existing resources directory retained as the fallback. Generated legacy applications and their shared configuration loader preserve UTF-8 project roots; material writers and legacy delivery metadata/shortcut paths also retain native Unicode paths.

CMake's Visual Studio PCH wrappers can contain ANSI-encoded header paths even with MSVC `/utf-8`. Query the CMake file API for original precompile-header declarations and repair only generated wrappers contained in the selected Unicode build cache. Retain their guards, include ordering and PCH compilation, preserve existing CMake flags, and do not modify authored headers.

## Risks / Trade-offs

The user selected repair of Unicode support through the full legacy compilation route after validation exposed narrow path conversions, MSVC PCH source encoding and shader tool failures. Retain the existing native target graph, including its application and shader work; do not add module-only target selection. Convert native tool arguments and filesystem boundaries explicitly between UTF-8 and wide Windows paths, preserve caller compiler flags while enabling MSVC UTF-8 source interpretation, and validate shader output plus module creation in an external Unicode directory. Inspection uses the deployed shared Python declaration validator and CMake preset discovery rather than duplicating profile policy.

- [GUI executable console/wait behavior varies by shell] -> Test redirected subprocesses and documented PowerShell/cmd waiting, preserving inherited handles.
- [Existing project APIs assume qApp, logging and mutable settings] -> Separate pure validation/inspection and reuse only required generation finalization; check authored files for changes.
- [Preset handling drifts from CMake] -> Prefer CMake discovery and existing preset resolution, cover includes, inheritance and different configure/build names, reject unsupported cases explicitly.
- [Native dependencies are loaded before command dispatch] -> Validate against the deployed editor distribution; do not promise dependency-free help or inspection.
- [Legacy and portable build routes differ] -> Require explicit route-compatible selections and run actual acceptance for both.
- [External paths expose narrow-string assumptions in tools] -> Exercise Unicode and spaces, repair only affected argument/path boundaries without changing unrelated tools.

## Migration Plan

Deploy the updated editor and any required adapter/tool changes together. Existing project files require no migration; generated scripts/presets remain authoritative. Add command documentation and automated acceptance alongside existing editor tests. Rollback restores prior editor/tool binaries; projects created by this command remain ordinary template-generated projects. Do not rewrite existing projects or templates solely to mark CLI support.
