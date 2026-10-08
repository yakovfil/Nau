# portable-project-generation Specification

## Purpose

Make newly generated code projects build and run consistently on Windows and web through shared project configuration, while preserving native editor integration and the legacy desktop route.

## Requirements

### Requirement: Generated portable application

The standard code-project template SHALL generate a shared portable application entry, project component sources, project declaration and documented build/run commands for Windows and web Debug and Release. Its portable default SHALL select `basic-rendering-scene` and include supported authored startup content with a camera, visible geometry and explicit materials. Creation through the editor and command-line tool SHALL produce equivalent portable integration without requiring users to copy files from a demo project.

#### Scenario: A new project is created
- **WHEN** the standard code template is instantiated through the editor or command-line tool
- **THEN** the project contains a complete portable declaration and build integration, with all project-name substitutions resolved
- **AND** its default portable delivery displays the provided supported scene on both platforms

### Requirement: Consistent declaration selection

Generated scripts and portable presets SHALL use the same authoritative default declaration. Platform and build configuration SHALL be independent of the declared feature profile. An explicit alternate declaration SHALL be validated and honored consistently, without merging independently maintained platform policies. Invalid or conflicting selection SHALL fail with an identifying diagnostic rather than silently choosing another profile. Build output SHALL identify the selected declaration, runtime profile and delivery directory.

#### Scenario: Entry commands use their defaults
- **WHEN** the same generated project is built using a script or its matching portable preset without a declaration override
- **THEN** both use the same declaration, startup scene, component policy and target delivery location

#### Scenario: An alternate declaration is selected
- **WHEN** a valid non-rendering declaration is explicitly selected through a script or portable preset
- **THEN** each builds the non-rendering profile with its existing exclusions and separate outputs
- **AND** a malformed declaration or incompatible prepared archive fails without fallback or launch

### Requirement: Equivalent preparation and build behavior

Normal generated script and preset builds SHALL prepare current project assets and native component registration before delivering the selected runtime. Preparation failure SHALL prevent successful delivery or launch of stale content. Explicit prepared-archive mode SHALL validate and deliver the selected bytes without requiring cooking tools. Native-only builds SHALL NOT require Emscripten. Command failures SHALL propagate as nonzero completion.

#### Scenario: A preset is used for the first build
- **WHEN** a freshly generated project with no prepared assets is configured and built through a portable preset with provisioned prerequisites
- **THEN** the build prepares and packages its required content and produces a runnable delivery without an undocumented preparation command

#### Scenario: Preparation fails after an earlier success
- **WHEN** a required authored input is removed or invalidated and a normal script or preset build runs
- **THEN** the build fails identifying the input and does not launch or report the prior package as newly successful

#### Scenario: Prepared content is reused
- **WHEN** one valid prepared archive is selected for Windows and web through either supported build entry
- **THEN** both deliveries contain those identical archive bytes without invoking host cooking tools

### Requirement: Isolated generation and rebuild operations

Generated build artifacts SHALL stay under ignored project build directories with distinct portable platform/configuration/profile, host-registration and legacy outputs. Project generation SHALL NOT require unrelated desktop shader compilation for portable scaffolding. Configure and rebuild commands SHALL respect the selected route's toolchain and output location. Cleaning or rebuilding one target SHALL NOT delete another target, shared host/preparation outputs or authored project files. Unsafe output paths SHALL be rejected before deletion.

#### Scenario: One target is rebuilt
- **WHEN** Windows and web outputs exist and the user requests a clean rebuild of one selected target
- **THEN** only that target's owned outputs are cleaned and the other target, host tools, prepared content and authored inputs remain intact

#### Scenario: Browser configuration is generated
- **WHEN** a portable browser preset is selected during project configuration
- **THEN** native-only architecture arguments and desktop shader-generation steps are not imposed on the browser route

### Requirement: External project locations and provisioning

Generated projects SHALL support explicitly configured engine, modules, SDK and host-tool locations independent of repository layout. Committed generated files SHALL NOT contain machine-specific dependency paths. Local machine settings and generated outputs SHALL be ignored by version control. Missing required dependencies SHALL cause actionable diagnostics without implicit installation or substitution of a different runtime route.

#### Scenario: A project lives outside the checkout
- **WHEN** a generated project with a non-demo name is built from an external directory containing spaces using configured dependency locations
- **THEN** scripts and portable presets resolve the project and dependencies correctly without sibling-checkout assumptions

### Requirement: Legacy desktop and native editor compatibility

The generated project SHALL retain an explicitly selectable legacy desktop SDK application route and native shared game-module builds required by editing and asset cooking. The host module and portable application SHALL share project component sources and identities, while browser application targets SHALL NOT link native host binaries. Existing editor Build/Run controls SHALL retain their current native behavior without a new platform selector. Updating the generator SHALL NOT rewrite existing project defaults or authored content.

#### Scenario: The editor loads a new project
- **WHEN** a project generated from the updated template is opened and its native game module is compiled through existing editor integration
- **THEN** the module remains loadable and its components available without requiring Emscripten or selecting a portable application target

#### Scenario: Legacy and portable deliveries coexist
- **WHEN** the explicit legacy desktop route and portable Windows/web routes are built for a generated project
- **THEN** legacy startup remains available with its desktop services and independent outputs while portable deliveries retain their declared feature set

#### Scenario: An existing project is used
- **WHEN** updated tools build an existing project with its current declaration and legacy presets
- **THEN** its default profile and authored configuration remain unchanged and no automatic template migration occurs

### Requirement: Generated-project acceptance

Acceptance SHALL create fresh projects through deployed CLI templates and editor creation, including an external directory and non-demo identity. It SHALL run generated Windows/web Debug/Release deliveries with visible scene output and orderly cleanup, compare script/preset selection and archive provenance, and verify relocation, alternate profile selection, preparation failure and targeted cleanup. Native editor module loading and the retained legacy desktop Release route SHALL be exercised. Commands, tool/template revisions, results and limitations SHALL be recorded; copying a pre-integrated demo SHALL NOT substitute for generation acceptance.

#### Scenario: The workflow is declared complete
- **WHEN** generated-project integration is reported as validated
- **THEN** evidence covers all four portable configurations, both creation entry points, script/preset parity, native editor compatibility and legacy startup
- **AND** relocated native and browser deliveries run without source-tree or host SDK access
