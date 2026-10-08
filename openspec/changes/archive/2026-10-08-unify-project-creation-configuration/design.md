# Design

## Context

See proposal.md for motivation. The reusable packaged-project driver already prepares assets and selects Windows or Emscripten targets, while EditorProject supplies a portable entry and project-specific CMake glue. Its wrappers currently require explicit engine/module locations derived from the sibling checkout. Newly generated projects instead receive the desktop-only `project_templates/empty` integration.

ProjectTool copies template files and substitutes selected filenames through `template.json`. It excludes the template's `.gitignore`, runs desktop and former UI shader compilation unconditionally, forces `-A x64` during solution generation, and deletes the whole `build` tree during clean rebuild. Existing tests cover template discovery/substitution but not portable project execution. Editor creation calls the same ProjectTool API without solution generation and preserves a template-provided main scene. Editor compilation and Build controls still use native SDK presets.

This crosses template generation, build orchestration and compatibility boundaries, so a design is required. Existing `editor-project-web-startup` contracts describe the non-rendering profile; `portable-scene-rendering` adds an explicit rendering profile. This change supplements both without weakening their dependency or runtime validation rules.

## Goals / Non-Goals

**Goals:** Make a generated code project runnable on either target through a small shared integration, including first-build asset preparation. Keep native host registration independent of runtime selection. Make scripts and presets converge on the same declaration, preparation policy and target directories.

**Non-Goals:** Changing the editor's Build/Run UI or routing its existing controls to web; converting existing projects automatically; adding rendering features; supporting non-Windows cooking hosts. The code-project template is the acceptance target; unrelated content-only templates are not redesigned.

## Decisions

### 1. Upgrade the standard code template, preserve explicit legacy selection

Extend `empty` so editor and CLI creation produce the same portable files automatically. Keep its existing native SDK CMake path and presets available for editor compilation and legacy desktop builds. Add clearly named portable presets instead of repurposing the native preset names the editor already invokes. New portable-template CLI creation with `--generate` and no explicit preset selects portable Windows Debug; legacy templates retain the native DLL default. Keep legacy startup source separate from the shared portable entry until feature parity permits retirement.

Alternative: a separate opt-in portable template would preserve all old behavior but leave the requested normal new-project workflow desktop-only. Automatically converting existing projects risks changing user scenes and dependencies, so only newly generated files get the new defaults.

### 2. Use the existing declaration as the single portable default

Generate `portable_project.json` with `basic-rendering-scene`. All new wrappers and portable presets omit any competing default filename and resolve this same project-relative file. An explicit `-Declaration` or equivalent preset cache override selects an alternate valid declaration; it does not merge policies or infer a profile from platform names. Preserve existing declarations and the shared driver's fallback filename, so old non-rendering projects keep their defaults. Fail on malformed/conflicting selection rather than falling back to a different profile.

Platform and Debug/Release remain orthogonal selections. Legacy desktop is a separate build route, not a third portable runtime profile. The direct legacy CMake route remains compatible with current editor callers.

Alternative: storing duplicate module/profile lists in `.nauproject`, scripts and presets would recreate drift. No second project settings schema is needed for the portable default.

### 3. Centralize orchestration, including preset preparation

Generated PowerShell/batch wrappers pass project identity, platform, configuration and overrides to the shared packaged-project driver. Extract reusable executable/module integration from the demonstrated EditorProject pattern into module-owned CMake helpers; project code should not copy acceptance probes or the complete driver.

Portable configure/build presets use a thin orchestration CMake branch in the generated project. Its build target invokes the same driver used by scripts. The orchestration build directory is separate from the driver's inner engine target directories, preventing recursive configuration. Configure records validated selection and dependency locations; building the default package target performs host registration, fresh preparation (or explicit prepared-archive validation), target build and staging. Preset configuration alone does not claim to have cooked assets. Use a generator independent of target architecture for this orchestration layer; only the inner target build receives the native or Emscripten toolchain.

This avoids a second asset pipeline and the current mismatch between configuring the project root versus the engine root. Presets and scripts report the resolved declaration/profile, target and delivery location. A changed declaration is read again by the driver, rather than silently retained in a preset cache. Normal builds may not silently reuse a prepared archive after failed preparation.

Alternative: native target presets that assume an already cooked archive make first-time builds fragile and provide different freshness semantics from the scripts.

### 4. Separate portable application, host module and legacy outputs

Use the existing per-profile/platform/configuration runtime locations and a distinct preset-orchestration directory. Retain a separate native shared game-module build for editor loading and cooking. Generated component CMake selects portable dependencies for packaged targets and native SDK dependencies for host/legacy targets; browser targets never link the host DLL. Use the same component sources and registration identities.

Selected-target clean/rebuild resolves and validates its own owned output directory. It must not recursively delete project `build`, shared preparation, host registration, another target or authored content. ProjectTool must honor preset binary directories and apply architecture/IDE behavior appropriate to the selected route instead of forcing `-A x64` or assuming a solution under `build`. Keep portable IDE opening unsupported with a clear diagnostic where no solution exists.

Alternative: one cache for editor DLL and application targets mixes incompatible linkage/toolchains and allows clean operations to destroy unrelated builds.

### 5. Template content and generator behavior are profile aware

Ship a small authored portable starter scene with a main camera, visible static geometry, simple material mappings and one existing portable project component producing observable motion. Use a dedicated portable startup configuration if required to preserve the legacy scene/material contract; no appearance parity with full desktop Graphics is promised. Preserve the legacy resource set required by the editor route. Do not copy NauDemo names or paths into generic templates.

Generation copies/substitutes files and supplies a usable ignore file. Portable shader generation belongs to target builds. Skip desktop/UI shader work for portable scaffolding; retain required desktop shader preparation when the legacy route is explicitly built. Stage the complete legacy resource tree and compiled shader cache under ignored `build/legacy-resources`, and mount that resource copy through the generated legacy VFS configuration. Reload `config/scene.json` explicitly after legacy configuration discovery so the portable startup configuration cannot override its scene. Update template metadata to substitute portable filenames/target identity correctly. A generated project's native editor DLL must still build and load without requiring Emscripten or portable asset cooking.

### 6. Explicit dependencies and installed-template coverage

Resolve engine and modules locations from documented environment variables (`NAU_ENGINE_SOURCE_DIR`, `NAU_MODULES_SOURCE_DIR`) or explicit overrides; allow ignored local preset/settings overrides. Reuse existing HostSdk/HostTools/UsdSdk parameters and environment variables for cooking. Do not assume the generated project is a sibling of NauEngineLite, or embed this machine's paths. Report missing prerequisites without installing them. Native-only builds must not discover Emscripten.

Ensure installed/staged ProjectTool and editor template distributions include the new files and shared helper references. Test that path, not only generation from the source template. Source-tree engine/modules integration remains the portable target model; creating a standalone prebuilt web SDK is outside scope.

## Risks / Trade-offs

- [Editor expects native preset names and DLL locations] -> Retain those routes; test actual editor creation, module compilation/loading and legacy Release startup.
- [Portable starter material is not a desktop PBR material] -> Keep portable configuration/mappings explicit and preserve legacy content behavior; do not promise full renderer parity.
- [Nested orchestration obscures errors or deadlocks] -> One driver owns the build lock; wrapper targets forward exit codes and do not acquire it twice. Record distinct outer/inner directories and test failed preparation.
- [Template metadata matches by basename] -> Add focused substitution tests and ensure legacy/portable entry filenames cannot receive unintended replacement rules.
- [Clean rebuild removes another configuration] -> Validate absolute owned paths and use sentinel/hash regression checks for sibling outputs and authored inputs.
- [Source-only testing misses distribution omissions] -> Create projects using deployed templates/tools, including an external path containing spaces and a non-demo project name.
- [Old browser cache masks a new profile] -> Reuse the corrected no-store development server and verify switching deliveries at the same URL.

## Migration Plan

Add shared helper/orchestration support, then update the code template and generator route handling. Deploy updated tools/templates together and create fresh projects for acceptance. Existing project files are never rewritten automatically; document opt-in manual adoption separately. Regress existing EditorProject rendering/non-rendering scripts and legacy native Release. Rollback is selecting the retained legacy presets or restoring the prior template/tool distribution; generated user projects are not deleted.
