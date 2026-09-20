# Tasks

## 1. Preserve source ownership and history

- [x] 1.1 Record engine, samples, demo and parent revisions, tracked sample inventory and native sample target baseline; verify destination remote/initial commit and distinguish existing failures before moving sources.
- [x] 1.2 Extract samples-only history in a disposable clone and merge it into the existing NauSamples history; verify the extracted tree matches the recorded source tree and both imported history and destination initial commit remain reachable.
- [x] 1.3 Retain original license notices, add repository usage/ignore guidance and account for every tracked sample file; verify no ignored generated build inputs were imported and record any integration edits separately from extraction.

## 2. Integrate external sample sources

- [x] 2.1 Add NAU_SAMPLES_SOURCE_DIR resolution and external add_subdirectory integration with stable binary directories; verify default/custom paths, a path containing spaces, missing/invalid source diagnostics and engine-only/browser-demo configurations without samples.
- [x] 2.2 Update sample shader/UI include roots and shared runtime asset discovery for source and installed layouts; verify representative resource lookups use the selected root and required shaders regenerate without old caches.
- [x] 2.3 Update native NauDemo CMake, asset configuration and build.py for the separate samples root; verify SampleCommonLib/SceneBaseSample integration and unchanged Debug/Release target/output locations.
- [x] 2.4 Update SDK sample installation and installed target discovery, including sample_common ordering; verify installed inventory retains every intended sample and excludes Git metadata and generated build directories.
- [x] 2.5 Remove engine-owned tracked sample sources only after extraction verification, register the existing NauSamples clone as a root submodule and coordinate local component revisions; verify .gitmodules URL, gitlink identity, complete file accounting and unchanged unrelated submodule revisions.

## 3. Adapt tests and reproduction tooling

- [x] 3.1 Update minimal runtime/profile/package audits to resolve external source paths while retaining entry-point, module and dependency assertions; run the affected graph and negative-source checks.
- [x] 3.2 Extend fresh-checkout helpers to include NauSamples and record all repository/patch identities; verify fresh checkout materialization uses no original build tree and detects missing required sample sources.

## 4. Verify compatibility across consumers

- [x] 4.0 Repair the approved engine EASTL allocator alignment defect; add allocation/offset/reallocation/container regressions, rerun native inputDemo Debug/Release with logs, and verify shared allocator compatibility in Wasm builds.

- [x] 4.1 Build all previously buildable native sample targets and NauDemo in Debug/Release from clean configurations; run affected native regressions and record target-by-target results against the pre-move baseline.
- [x] 4.2 Launch native SceneBaseSample, a sample using shared sample-root discovery and NauDemo from documented working directories; verify assets, retained appearance/behavior and normal close in Debug/Release, recording visual evidence or explicit user confirmation.

  Evidence: inputDemo startup and normal close verified in Debug/Release; user accepted inputDemo visual input behavior, then explicitly accepted both SceneBaseSample and NauDemo on 2026-09-20.

- [x] 4.3 Build and run existing minimal and demo browser Debug/Release acceptance, including source provenance, startup/Stop/failure cases and relocated packages; verify unchanged non-rendering graphs, timing and demo rendering.
- [x] 4.4 Install and relocate the native SDK, configure its installed sample workflow and compile representative minimal and asset-using samples; verify runtime resource lookup and absence of original source-tree dependencies.
- [x] 4.5 Execute documented fresh-checkout builds with recorded submodule revisions and external SDK setup; verify minimal/demo Debug/Release rendering or update progress and Stop, and distinguish local repository availability from remote publication.

## 5. Document and finalize the migration

- [x] 5.1 Update current root/component build guides, prerequisites and repository layout instructions, including custom sample roots, clean reconfiguration, SDK paths and publication order; verify commands against implemented entry points and leave archived historical evidence intact.
- [x] 5.2 Record extraction provenance, coordinated repository identities, scenario results and remaining limitations; verify every spec scenario has evidence, required checks are complete and strict OpenSpec validation passes before marking the change complete.
