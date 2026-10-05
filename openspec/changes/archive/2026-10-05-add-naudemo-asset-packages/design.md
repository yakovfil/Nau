# Design

## Context

See proposal.md for motivation. `AssetPackTool` is a library in NauEngineModules/tools/asset_pack_tool. It writes a `nau-vfs-pack` container header, JSON index and concatenated uncompressed file bytes. Its current implementation skips unavailable streams, ignores copy failures and leaves a temporary file; these behaviors cannot support dependable build outputs. The assignment to `contentCompression` also needs correction to an explicit empty string for uncompressed data.

The existing package filesystem in NauEngineLite/kernel/src/platform/windows/io uses Windows memory mapping and paging. The public path-based factory must remain supported. Shared `nau_container.cpp` currently uses assertions, unchecked Result dereferences and an implicit extra header separator byte; compatibility tests must capture the actual existing wire bytes before changing parsing.

NauDemo native configuration mounts `/demo`, `/content` and `/res` from checkout paths. Its material references `/res/shaders/cache/shader_cache.nsbc`, and its environment uses `/content/textures/environment/SunnyHills_2k.hdr`. SceneBaseSample currently generates shader caches, partly in sample source directories. Web preloads loose files into `/demo-package`, then copies mesh/font bytes into a CPU asset filesystem; shaders and JSON are read separately. Its staging script also deploys loose copies.

The existing naudemo-web independent-build scenario says there are no native binary inputs. A host executable necessarily changes that build-time constraint; the delta explicitly allows an isolated native packer while keeping desktop runtime libraries out of the browser graph.

## Goals / Non-Goals

**Goals:** Use one archive format and engine reader for demo assets across platforms; keep the runtime API module-neutral; preserve valid archive compatibility and current demo appearance; make relocated delivery and failed builds verifiable.

**Non-Goals:** AssetTool imports, USD cooking, compression, encryption, HTTP range streaming, browser/native material parity, removal of all sample build dependencies, or a general deployment system. Build-time reuse of sample source assets is allowed; runtime checkout access is not.

## Decisions

### Portable reader owns a seekable stream and explicit byte length

Add a Result-returning package filesystem factory accepting an owned `IStreamReader::Ptr`, total package length and bounded read options. Keep the current path-based Windows factory unchanged. NauDemo uses the new factory on both platforms; the legacy mapping backend remains available for existing consumers.

The common reader stores a validated index and backing stream. File streams hold shared backing ownership and independent logical cursors. A mutex protects backing seek/read pairs, giving correct concurrent and interleaved reads without requiring thread-safe input streams. Reads are bounded to each entry; directory iteration and read-only rejection follow existing IFileSystem conventions. The caller transfers exclusive use of the backing cursor. Unmount does not invalidate existing open streams.

This avoids maintaining a Windows mapping emulation in the browser and avoids eagerly copying every entry into another asset filesystem. Web preload still stores the whole archive in Emscripten memory; remote streaming is deferred. Use a narrow adapter to obtain an engine stream from the preloaded archive if the existing browser native-file abstraction is insufficient.

### Preserve the format and validate before publishing

Use the existing header/index/blob representation and version 0.1. Capture a pre-change archive fixture and byte-offset tests, including the existing header separator convention. Parse lengths and index values with checked wide arithmetic before conversion to platform size_t, important for 64-bit host to wasm32 compatibility. Validate kind, version, empty/uncompressed marker, payload limits, offset plus size, client size consistency and index structure before constructing the filesystem. The captured legacy archive confirms the old writer emitted a single NUL as its uncompressed marker; accept that established representation as well as the corrected empty string.

Canonical package paths use slash-separated relative names. Normalize legacy leading separators and backslashes consistently; reject traversal, drive-qualified paths, embedded NULs, duplicate canonical names and file/directory conflicts. New manifests emit canonical relative names. Set documented limits for header/index bytes, entry count and path length; enforce caller-provided archive length and representable offsets. Tests exercise limits without allocating huge buffers.

Prefer a checked package-specific parser or additive checked container helper over changing all unrelated container consumers. Reuse it for AssetPackTool index reading where practical. Changing the on-disk format or silently accepting malformed indexes would make compatibility harder to prove.

### Host tool stays in Modules and has a focused build

Add a small `AssetPackToolCmd` executable beside AssetPackTool. A JSON manifest contains source/path pairs and fixed package options; relative source paths resolve against the manifest directory. Sort entries by canonical archive path, reject duplicate destinations and write no timestamps or machine paths into the archive. Include a simple usage/help interface and nonzero diagnostic failures.

Repair the library writer to propagate failed opens, reads, writes and short writes and clean temporary files. The CLI writes a sibling temporary output, validates the result, then publishes by replacement; on failure the build remains failed even if an earlier good archive remains available. Keep existing library entry points source-compatible.

Provide a focused CMake entry point under Modules that builds only the kernel dependencies, AssetPackTool and CLI. Do not enable all NAU_CORE_TOOLS, which would introduce USD and unrelated tools. Demo scripts build that native executable into `NauDemo/build/asset-pack-host` using the native toolchain and pass its path to the target build. Emscripten never tries to execute a wasm packer. A prebuilt compatible executable can be supplied explicitly; missing prerequisites yield actionable errors.

### Platform manifests describe complete demo content

Use explicit native/web manifests with shared cube and font entries. Archive paths mirror VFS paths (`demo/...`, and native `content/...` and `res/...`). Mount the archive at a suitable common VFS root, or expose prefix views when the existing VFS mount policy requires separate mounts; resulting public asset URIs remain unchanged.

Native packages contain the cube mesh/buffer, font, material, environment texture, and required renderer resources and compiled shader caches. Replace the demo's dependency on SceneBaseSample as a shader-generation side effect with demo-owned cache generation under NauDemo/build, reusing shader sources/helpers. Resolve the full existing renderer resource list in the manifest and test without checkout access. Do not copy entire sample trees indiscriminately.

Bootstrap native configuration must be available before services initialize: deploy the small host configuration next to the executable or compile its stable defaults, resolve archive location relative to the executable, and mount before services consume assets. Remove source-directory VFS mounts and NAU_DEMO_DIR/NAU_SAMPLES_DIR runtime path reliance. Existing log location remains supported. Archive asset configuration is distinct from bootstrap host configuration.

Web packages contain cube/font, browser shaders, material and asset JSON. Keep Emscripten `--preload-file`, but preload the single archive instead of loose asset directories. Read JSON and shaders through the mounted engine filesystem and remove per-file copies into createCpuAssetFileSystem. Preload transport failures report delivery failure; parsed archive or asset failures enter the common host's checked startup failure path.

### Repair graphics teardown exposed by native acceptance

Visible native Debug acceptance exposed remaining textures/buffers at driver shutdown followed by null-executor loops, while the archive rendered correctly. The user authorized repairing this path within the change. Release render-window and scene GPU resources explicitly on the render worker, settle accepted work before driver destruction, and preserve checked startup failure cleanup. The traced failures were missing destructors for owned texture/mesh/environment/ImGui resources and detached scene asset-update tasks that outlived the render worker. Await scene asset updates within the owning frame before advancing or stopping. Destroy the default graphics texture before frame-graph shutdown/driver release. File logging also checks the background executor and avoids continuations onto a stopped caller; a focused regression verifies accepted writes and a late write after background disposal. Native bootstrap validates all manifest entries before graphics initialization. Add regression acceptance for visible resize/close and failed asset startup; do not mask assertions or accept a timeout as successful cleanup.

### Build graph and delivery remain explicit

Use custom commands with all manifest/source inputs and the host packer as dependencies. A missing input must fail even when an archive exists. Native shader generation precedes packaging; web archive generation precedes preload/link. Generated cache/tool/package outputs live under NauDemo/build; existing native bin deployment can receive the final archive/runtime files.

Web `.data` is a transport envelope around the engine archive, not a second asset format used by demo code. The staged delivery need not duplicate the raw archive beside `.data`; the standalone generated `.nau_pack` remains available in build output for inspection. Preserve manifest hashes, license notices, serving headers, nested-base resolution and atomic staging. Remove unnecessary loose asset sidecars and adapt corruption fixtures to mutate/rebuild the actual archive payload.

## Risks / Trade-offs

- Existing header quirks or compression-marker artifacts -> preserve known valid byte fixtures and cross-read with the Windows backend before migrating Demo.
- Native renderer implicitly opens additional resources -> enumerate configured resource references and prove relocation with source directories inaccessible; missing resources fail acceptance.
- Shared stream reads serialize -> acceptable for this small demo; preserve the Windows optimized backend for other consumers and defer performance redesign.
- Web preload consumes archive-sized memory -> avoid an additional full archive copy and per-entry extraction; no large-asset streaming claims.
- Host compiler is an additional web-build prerequisite -> isolate the build, document it, and diagnose its absence explicitly.
- Generic container changes could affect other assets -> keep changes additive or narrowly scoped and run existing container/asset reader regressions if shared code changes.

## Migration Plan

First introduce format fixtures, checked IO and the portable reader; then add the host CLI/build path. Integrate native and web manifests and mounting, remove source asset fallbacks, and update delivery tests/documentation. Keep existing Windows consumers running throughout. Rollback restores demo asset loading and build rules together; the additive reader API and compatible archives do not require an asset data migration.

Acceptance covers native and real Chrome Debug/Release, archive failures, missing font/buffer, package rebuild behavior, source-inaccessible relocation, text/cube pixels, rotation, resizing, shutdown and existing minimal lifecycle/dependency checks. Record source revisions and exact tool commands. Execute a fresh-checkout walkthrough separately before claiming reproducibility, as required by the existing web specification.
