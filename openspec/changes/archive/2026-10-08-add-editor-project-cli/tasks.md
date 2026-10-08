# Tasks

## 1. Command startup and execution foundation

- [x] 1.1 Add typed parsing for the five project commands, global/command help and version before GUI startup; verify valid combinations, unknown commands, missing arguments, conflicting options and existing no-command ignore-project-modules behavior with focused tests.
- [x] 1.2 Separate batch dispatch from GUI application creation and move GUI guard acquisition to opening/interactive paths; verify batch commands show no windows while the guard is held and direct open reports the documented conflict result.
- [x] 1.3 Add command console handling and a child-process runner with incremental stdout/stderr forwarding, argument-list execution and documented result categories; verify redirected output, launch failure, child nonzero exit/crash and Unicode arguments using subprocess tests.

## 2. Project validation, creation and inspection

- [x] 2.1 Implement shared project path/metadata validation without mutable project loading; verify explicit files, unique directory selection, ambiguity, malformed JSON, relative paths, spaces and Unicode from an unrelated working directory.
- [x] 2.2 Implement template creation with existing ProjectTool generation and required editor metadata finalization; verify a fresh project matches deployed template integration, existing destinations remain untouched, invalid templates fail and failure never opens an editor.
- [x] 2.3 Implement read-only inspection and supported preset/declaration resolution; verify legacy absence, malformed present files, includes/inheritance/user presets, distinct configure/build preset names and unchanged project contents without SDK/Emscripten provisioning.

## 3. Opening and builds

- [x] 3.1 Add validated explicit project startup and create --open through normal editor initialization; verify chooser bypass, native module loading, ignore-project-modules, migration-required rejection, initialization failure and instance-conflict reporting without remote forwarding.
- [x] 3.2 Implement native compile dispatch with selected/default configuration and deployed BuildToolCmd; verify successful module creation, unavailable tools and an actual compilation error return accurate results without requiring Emscripten or loading the module in the command process.
- [x] 3.3 Implement portable build preset dispatch to the existing configure/build workflow; verify selected configure/build mapping, declaration/configuration/output parity and rejection of missing presets or conflicting overrides without route fallback.
- [x] 3.4 Implement explicit legacy build dispatch with configuration and destination through the full existing build route; verify sources/assets are built, unsafe destinations fail and portable defaults remain unchanged.

- [x] 3.5 Repair Unicode support through the full existing native compilation route, including Windows tool arguments, native path conversions, MSVC PCH source encoding and shader input/cache/output paths; verify the externally generated Unicode project produces its module, legacy executable and nonempty shader cache while preserving caller compiler flags, and add a shader path regression check.

- [x] 3.6 Repair the approved editor engine/asset importer UTF-8 path boundaries, including Windows native filesystem resolution, file streams and generated legacy configuration loading and remove the stale retired ui request; verify Unicode project opening loads its native module, imports assets into the intended directory and closes successfully, with ASCII import/build regressions checked.

## 4. Deployment and documentation

- [x] 4.1 Integrate command sources/tests and required deployed tools/templates into editor build packaging; build the editor and affected tests, then verify commands execute from the deployed editor directory with documented dependency locations.
- [x] 4.2 Document every command, defaults, portable versus native/legacy selection, exit categories, prerequisites, independent-session behavior and PowerShell/cmd waiting/redirection; verify examples use generic paths and match deployed help.

## 5. End-to-end acceptance

- [x] 5.1 Run deployed create/inspect/compile/open against a fresh externally located project, including paths with spaces and Unicode; verify native module loading, direct opening, create --open, orderly close and unchanged interactive chooser startup, recording results.
- [x] 5.2 Build and start generated portable Windows/web Debug/Release deliveries through the CLI; verify supported visible startup and shutdown plus parity with direct preset selection, and record selected profiles, configurations and output directories.
- [x] 5.3 Build and launch explicit legacy desktop Release through the CLI; verify its existing scene behavior and closure while preserving the portable outputs and authored configuration.
- [x] 5.4 Exercise missing/malformed/ambiguous inputs, invalid presets, missing dependencies, stale-delivery preparation failure, child failure, occupied GUI guard and batch commands alongside a running editor; verify nonzero results, useful redirected diagnostics and preservation of unrelated files/processes.
- [x] 5.5 Record reproducible commands, revisions, results and limitations in validation.md; run affected focused tests, strict OpenSpec validation and whitespace checks, and confirm every acceptance claim is supported by recorded evidence.
