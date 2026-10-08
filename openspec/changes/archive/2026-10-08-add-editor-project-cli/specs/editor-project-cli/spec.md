# Spec Delta

## Purpose

Provide independent editor commands for reproducible project creation, direct opening, native module compilation, application builds and project inspection from terminals and automation.

## ADDED Requirements

### Requirement: Independent command dispatch

The editor SHALL expose `project create`, `project open`, `project compile`, `project build` and `project inspect`, plus global and command help and version output. Create without `--open`, compile, build and inspect SHALL execute without project-selection dialogs, editor windows or graphics initialization and SHALL terminate on completion. These commands SHALL operate independently of a running editor rather than sending it commands. Starting the editor without a project command SHALL retain interactive startup and the existing ignore-project-modules option.

#### Scenario: A batch command runs while the editor is open
- **WHEN** inspection or creation of a different project is requested while an editor instance is running
- **THEN** the command executes without acquiring the editor GUI instance guard or opening a window
- **AND** it terminates with its own result

#### Scenario: Help or invalid syntax is supplied
- **WHEN** help, version, an unknown command or invalid arguments are supplied
- **THEN** the editor prints the appropriate information or identifying usage error without opening the project chooser
- **AND** help and version succeed while invalid syntax fails

### Requirement: Explicit project resolution

Existing-project commands SHALL accept a `.nauproject` file or a directory containing exactly one such file, resolve relative inputs against the caller's working directory, and support paths containing spaces and Unicode characters. Missing, ambiguous or malformed project inputs SHALL fail before invoking a build or opening editor UI. Commands SHALL NOT implicitly upgrade projects, select another project, install dependencies or clean unrelated outputs.

#### Scenario: A project directory is ambiguous
- **WHEN** a supplied directory contains multiple project files
- **THEN** the command fails and requests an explicit project file without selecting one arbitrarily

#### Scenario: A project is outside the checkout
- **WHEN** a valid external project path containing spaces or Unicode characters is supplied from an unrelated working directory
- **THEN** the selected command resolves the intended project and passes its path intact to downstream tools

### Requirement: Template-based creation

`project create --directory <parent> --name <name> --template <template>` SHALL create a project through the deployed template workflow and report the resulting project file. Omitting `--template` SHALL select `empty`. Creation SHALL NOT require configuring or compiling the generated project. It SHALL reject an existing destination or invalid template without overwriting authored files. Successful `--open` creation SHALL proceed through the explicit opening behavior; creation failure SHALL prevent opening.

#### Scenario: A portable project is created
- **WHEN** the standard template is requested with valid inputs
- **THEN** the generated project contains the same portable entry, declaration, scripts, presets and native editor integration as ordinary template generation
- **AND** the command reports the new project path and exits unless opening was requested

#### Scenario: The destination exists
- **WHEN** creation targets an existing project directory
- **THEN** it fails without replacing its files

### Requirement: Direct project opening

`project open --project <path>` SHALL validate the project and enter normal editor initialization for that project without showing the project chooser. It SHALL preserve native game-module initialization and accept `--ignore-project-modules`. An incompatible project requiring migration or an occupied editor instance guard SHALL produce a diagnostic and nonzero result without a confirmation dialog or remote forwarding. The command SHALL remain associated with the editor process until that process exits; successful process creation alone SHALL NOT be reported as successful project initialization.

#### Scenario: A valid project is opened
- **WHEN** a compatible project is supplied and the GUI instance guard is available
- **THEN** the editor initializes that project and displays its normal editor window directly
- **AND** an initialization failure returns nonzero

#### Scenario: Another editor holds the instance guard
- **WHEN** direct opening is requested while the guard is occupied
- **THEN** the command exits nonzero with a clear instance-conflict diagnostic and leaves the running editor unchanged

### Requirement: Native module compilation

`project compile --project <path> --config <Debug|Release>` SHALL compile the native shared game module through the existing editor compilation route. The default configuration SHALL match the editor distribution's configuration. Output SHALL identify the configuration and native preset. Compilation SHALL NOT require Emscripten, produce a portable application as a substitute, or claim success when compilation fails.

#### Scenario: The game module compiles
- **WHEN** native prerequisites are provisioned and compilation succeeds
- **THEN** the selected configuration's game module is produced and the command exits successfully

#### Scenario: Compilation fails
- **WHEN** a required tool is unavailable or source compilation fails
- **THEN** diagnostics identify the failure and the command exits nonzero even if an older module exists

### Requirement: Preset-selected application builds

`project build --project <path> --preset <preset>` SHALL require an explicit supported project preset. Portable selection SHALL use the project's existing configure/build preset workflow and its authoritative declaration, platform, configuration and delivery paths. Legacy desktop selection SHALL remain explicit and use the existing desktop build workflow with explicit configuration and destination. Missing, unsupported or conflicting selections SHALL fail rather than falling back to another route. Child failures SHALL prevent success reporting. Successful output SHALL identify the selected route and delivery directory; build SHALL NOT launch the application.

#### Scenario: A portable preset is built
- **WHEN** a generated Windows or web Debug or Release preset is selected with provisioned prerequisites
- **THEN** the build follows the same declaration and asset preparation as direct preset use and produces the same delivery location
- **AND** web builds do not link native host binaries and Windows builds do not require Emscripten

#### Scenario: An explicit legacy build is requested
- **WHEN** a supported legacy desktop preset, configuration and separate destination are supplied
- **THEN** the legacy delivery is built without changing the project's portable defaults or authored configuration

#### Scenario: A build fails after a previous success
- **WHEN** configuration, asset preparation or compilation fails with an older delivery present
- **THEN** the command reports failure and does not launch or present the old delivery as newly successful

### Requirement: Read-only project inspection

`project inspect --project <path>` SHALL report project identity and resolved path, available project presets, and the default portable declaration and runtime profile when available. It SHALL distinguish absent portable integration from malformed integration. Inspection SHALL NOT configure, build, cook assets, modify project settings or require native SDK or Emscripten provisioning. Referenced preset includes, inheritance and user presets SHALL be reflected consistently with the supported build selection.

#### Scenario: A legacy project is inspected
- **WHEN** a valid project has no portable declaration
- **THEN** inspection succeeds, lists available presets and explicitly reports that portable integration is absent

#### Scenario: Inspection encounters invalid configuration
- **WHEN** project or available declaration/preset data is malformed
- **THEN** inspection reports the offending input and exits nonzero without modifying it

### Requirement: Observable command completion

Commands SHALL provide readable stdout/stderr under an attached terminal and redirected execution, stream build progress, and return zero only for success and nonzero for invalid input, missing prerequisites, execution failure or instance conflict. Spawned tool crashes and launch failures SHALL count as failures. Diagnostics SHALL retain relevant downstream errors. Commands SHALL document their blocking behavior and Windows shell invocation needed to wait for a GUI-subsystem executable. Runtime dependency discovery SHALL support documented configurable locations without machine-specific committed paths.

#### Scenario: Automation captures a failed build
- **WHEN** an automation process invokes the editor with redirected output and the downstream build fails
- **THEN** it receives useful diagnostics and a failing exit status after the child process settles

### Requirement: Deployed command acceptance

Acceptance SHALL exercise the deployed editor CLI against a newly generated external project, actual native compilation and direct editor opening, all four portable Windows/web Debug/Release builds, and an explicit legacy Release build. It SHALL verify delivered startup, parity with direct preset selection, error propagation, inspection without mutation, coexistence with an editor instance, redirected output and existing interactive startup. Commands, versions, outcomes and any untested limits SHALL be recorded.

#### Scenario: The CLI is declared complete
- **WHEN** implementation validation is reported
- **THEN** evidence covers real command execution and resulting project/module/application behavior rather than only parsing tests or help output
