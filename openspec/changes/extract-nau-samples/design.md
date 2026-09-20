# Design

## Context

See proposal.md for motivation. At exploration, engine revision 02574c71 owns 414 tracked sample files across 12 directories. NauSamples is a separate local clone on main with initial commit bcf3bf4 and a LICENSE; Nau has not registered it as a submodule. The destination remote is https://github.com/yakovfil/NauSamples.git.

Engine CMake unconditionally enters samples, whose dispatcher selects minimalApp for the minimal profile, skips samples for the demo profile, and otherwise adds SampleCommonLib plus discovered samples. Native NauDemo links SampleCommonLib and depends on SceneBaseSample to generate shared shader caches. Its configuration names the engine-local sceneBase assets. SampleAppDelegate searches parent directories for samples/<name>. Shader and UI CMake files use relative paths back into engine sources. SDK installation copies the samples directory, while cmake/for_build uses a separate list of installed sample paths. Minimal acceptance audits and NauDemo's reproduction helper also encode the old layout.

## Goals / Non-Goals

**Goals:** Establish external source ownership without changing preset names, target identities, output paths or runtime contracts. Preserve both destination and extracted history. Make dependency selection observable and testable. Keep native SDK consumption working.

**Non-Goals:** A standalone sample build system independent of engine CMake, moving NauDemo, changing sample rendering/features, upgrading tools, rewriting engine history, publishing repositories without a separate request, or repairing unrelated pre-existing sample defects silently.

## Decisions

### 1. Extract history in a disposable clone and merge into the existing destination

Use a bounded samples-only history extraction (for example git subtree split --prefix=samples) in a disposable clone at a recorded engine revision. Import the resulting history into NauSamples and merge with its existing initial commit using an explicit unrelated-history merge. Keep the destination LICENSE and retain the original engine BSD notice in an accompanying license file referenced by the repository documentation; preserve per-file notices. Record source-to-extracted commit provenance and compare the extracted tree with the original samples tree before integration edits.

A snapshot-only copy loses sample history. Replacing destination history loses its existing initial commit and would invite a force push; neither is selected. Only tracked sample content is extracted: existing tracked asset databases remain included, while ignored generated caches/builds are regenerated. Do not reset or overwrite later user changes if source identities have advanced.

### 2. Keep engine CMake as the integration entry point

Introduce cache PATH NAU_SAMPLES_SOURCE_DIR defaulting to the sibling NauSamples directory. Resolve it before adding sample-dependent targets and validate required CMake files. Add the external directory with an explicit binary directory ${CMAKE_BINARY_DIR}/samples to preserve generated target paths used by existing tooling. The samples dispatcher remains in NauSamples at its root.

Require samples when NAU_CORE_SAMPLES is enabled for a profile that consumes them, or a selected native application needs SampleCommonLib/SceneBaseSample. Do not require samples for engine-only configurations or the existing browser demo profile, which uses its own assets. The minimal package does require NauSamples. Preserve existing dependency exclusions and preset options; add only source-path configuration where needed. Missing paths produce initialization/override guidance, never an implicit fetch.

Keeping an engine-local duplicate or junction would mask incomplete migration and retain ambiguous ownership. Making NauSamples independently configure the entire engine is unnecessary for this extraction.

### 3. Separate source roots, binary roots and installed paths

Pass an explicit engine source root to sample shader/UI CMake code rather than deriving it from directory depth. Use the configured sample root for source-build runtime lookup and retain an installed-layout lookup for SDK consumers. Configured source paths must not be required by relocated installed samples. Keep shader generation behavior scoped to its selected source/build inputs and preserve ignore rules for generated caches.

Update native NauDemo's compile-time samples root, sceneBase property and build.py integration; its engine root remains separate. Preserve the build/samples/sceneBase target location where possible. Update minimal graph audits to distinguish external source directory identities from stable binary locations. Source identity assertions must not be removed merely because paths moved.

Install the CONTENTS of NauSamples into <prefix>/samples, excluding repository metadata and generated build directories. Ensure installed sample discovery includes sample_common before consumers and does not silently omit migrated targets. Audit cmake/for_build against the source target inventory rather than assuming its existing list is complete.

### 4. Register one additional root submodule and validate coordinated inputs

Reuse the existing NauSamples clone and its configured remote. Register its path and revision in Nau; do not nest another engine checkout inside it. Keep the engine's bundled dependencies and all other submodule references unchanged. Component commits and gitlink updates needed to represent the extraction are part of local implementation; remote pushes remain separate. Any future publication must make component revisions available before publishing the parent reference.

Extend fresh-checkout tooling to clone/check out NauSamples and record its identity, including explicit patch identity when validating uncommitted development state. Verify a fresh parent/submodule checkout locally without relying on original worktrees or their caches. Local-only revisions are not evidence of remote clone availability.

## Risks / Trade-offs

The user approved repairing the existing EASTL allocator alignment defect after both migrated and pre-migration inputDemo Debug binaries failed during additional-swapchain creation. The engine-owned allocator will retain allocation metadata using a portable malloc-backed header, honor the bundled EASTL `pointer - offset` alignment contract, and preserve that contract and existing bytes across reallocations. All allocation overloads must share the matching deallocator; allocation overflow or failure must leave an existing reallocation input intact. Tests cover ordinary and over-aligned allocations, offsets, container nodes, resizing and failure handling. Rebuild and rerun native inputDemo in both configurations and validate the shared allocator in browser builds. This is a focused, approved extension to migration validation, not a third-party library edit.

The user approved improving the existing demo image acceptance during application: sample multiple geometrically selected interior pixels, retain nearest-triangle depth and shading assertions, and retain deliberate blank-image/runner failure rejection. The original center-pixel failure remains in evidence. This changes acceptance tooling, not rendering behavior.

- Hidden sample-relative paths can survive successful compilation -> audit source/configuration/docs, launch asset-using native samples and NauDemo, and test a custom samples path containing spaces.
- Native shader caches in the original checkout can hide missing generation dependencies -> use clean build/resource outputs and record regeneration; do not migrate ignored caches as inputs.
- Installed SDK discovery already differs from source discovery -> validate relocated installation and representative native samples, not just source CMake.
- History extraction may encounter large asset history or tool limitations -> record the extraction command and commit mapping, verify trees before removal, and retain disposable extraction data until the migration is verified.
- Existing sample targets may have unrelated failures -> record the pre-move target baseline and distinguish migration regressions; unresolved required acceptance stays pending rather than silently reducing scope.
- Old build caches retain absolute paths -> document clean reconfiguration for the migration while preserving preset names and binary layout.

## Migration Plan

1. Record current component revisions, clean/dirty status, tracked sample inventory and existing native target baseline. Preserve user changes and verify destination initial history.
2. Extract/import sample history and license provenance; verify destination file accounting before removing engine-owned tracked sources.
3. Adapt external CMake/runtime/SDK paths and NauDemo, then register the new submodule and coordinate local revisions. Regenerate rather than transfer ignored outputs.
4. Run graph/path tests, native target builds and runtime checks, minimal/demo browser acceptance, SDK relocation and fresh-checkout validation.
5. Update current guides and evidence, validate OpenSpec and prepare the coordinated component/parent commits. Do not rewrite archived historical paths as though old evidence used the new layout.

Rollback uses the recorded parent and component revisions in a separate clean checkout or explicit revert commits. Preserve the imported NauSamples history; do not delete its clone or force-reset shared branches. If remotely published later, use forward/revert commits rather than rewriting published history.
