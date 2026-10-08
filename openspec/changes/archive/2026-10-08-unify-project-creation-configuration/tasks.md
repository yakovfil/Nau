# Tasks

## 1. Shared configuration and build integration

- [x] 1.1 Add reusable portable executable/module integration to module-owned CMake helpers, using project-supplied identity and shared entry configuration; verify a non-demo target configures without copied acceptance code or hard-coded demo paths.
- [x] 1.2 Make generated-project wrappers resolve engine/modules and host dependency locations from explicit overrides or documented environment settings; verify external paths containing spaces, actionable missing-prerequisite failures and native selection without EMSDK.
- [x] 1.3 Add the preset orchestration branch delegating package builds to the existing shared driver with separate outer/inner caches; verify a first preset build performs preparation, propagates failures and avoids recursive configuration or nested build-lock acquisition.
- [x] 1.4 Unify declaration resolution/reporting across wrapper and preset invocation while retaining existing driver defaults; verify default rendering, explicit non-rendering, invalid declaration and incompatible prepared-archive cases select identically or fail without fallback.

## 2. Generated project template

- [x] 2.1 Add the portable application entry, thin build/run scripts, portable configure/build presets and default rendering declaration to the standard code template; update substitution metadata and verify generated names and paths contain no unresolved placeholders or machine-specific values.
- [x] 2.2 Add authored starter camera, visible geometry, simple material mappings and a portable updating component with startup configuration; verify preparation accepts the complete closure without modifying source assets and runtime identities match authored content.
- [x] 2.3 Separate portable component dependencies from native editor/cooking and legacy dependencies, retaining legacy entry and preset names; verify native host DLL compilation independently of EMSDK and browser graph exclusion of native binaries/full desktop services.
- [x] 2.4 Include a usable generated ignore file and document dependency settings, script/preset commands, alternate declarations, prepared archives and explicit legacy selection; verify generated outputs and local settings are ignored and documented commands match emitted files.

## 3. Project tools and template distribution

- [x] 3.1 Make template generation avoid unrelated desktop/UI shader compilation for portable scaffolding while retaining required shader preparation for legacy builds; verify CLI creation and editor API creation produce equivalent portable integration and legacy preparation remains available.
- [x] 3.2 Update configure/IDE handling to honor selected presets and actual binary directories without forced native architecture on portable routes; verify Windows and web preset generation plus an actionable unsupported-IDE diagnostic where no solution exists.
- [x] 3.3 Limit clean/rebuild to the selected owned target directory with resolved-path containment checks; verify sentinels/hashes in sibling configurations, profiles, host/preparation directories and authored content survive, and unsafe paths are rejected before deletion.
- [x] 3.4 Update project-tool tests and deployed template/helper distribution; create an external project using installed tools/templates and verify its required files, substitutions and referenced helpers are complete.

## 4. End-to-end acceptance

- [x] 4.1 Generate a fresh non-demo project outside the checkout in a path containing spaces and run Windows/web Debug/Release through generated scripts and matching presets; verify visible starter geometry/component motion, declaration/output parity, shared archive provenance and orderly cleanup.
- [x] 4.2 Exercise first-time preset preparation, changed/missing assets, alternate non-rendering declarations, prepared-archive mode without cooking tools and target-specific clean/rebuild; verify fresh output or identifying failure, no stale launch, correct profile exclusions and preservation of unrelated outputs.
- [x] 4.3 Create/open a project through the actual editor using deployed templates, compile/load its native game module through existing controls, and run its explicit legacy desktop Release route; verify component availability and existing editor behavior without adding platform selection UI.
- [x] 4.4 Run relocated generated native deliveries and nested-URL browser deliveries, plus existing EditorProject portable rendering/non-rendering and legacy Release regressions; verify no runtime source/SDK fallback and no existing-project default/content changes.
- [x] 4.5 Record reproducible commands, tool/template revisions, all acceptance results and limitations in validation.md, mapping each requirement to evidence; run strict OpenSpec validation before reporting implementation complete.
