# Tasks

## 1. Portable package reading

- [x] 1.1 Add a pre-change archive fixture and format tests in kernel IO tests; verify exact header/index/blob offsets and byte recovery using the existing Windows reader before modifying format handling.
- [x] 1.2 Implement checked package parsing with documented bounds, version/compression handling, canonical paths and wide numeric validation; verify malformed headers, truncated data, overflows, duplicate paths, traversal and file/directory conflicts return errors in Debug and Release.
- [x] 1.3 Add the portable stream-backed read-only filesystem and integrate its sources into native and browser kernel builds; verify lookup, enumeration, zero-length files, independent/interleaved reads, seeks, EOF and rejected writes on both platforms.
- [x] 1.4 Verify backing ownership and synchronization with tests covering concurrent streams, input-owner release and unmount while files remain open; confirm the existing Windows factory remains source-compatible and valid old archives are readable.

## 2. Reliable host packaging

- [x] 2.1 Repair AssetPackTool writer/index-reading error propagation, uncompressed metadata initialization and temporary-file cleanup; verify missing streams, short writes and injected IO failures produce errors without successful partial output.
- [x] 2.2 Add AssetPackToolCmd manifest processing, canonical sorting, diagnostics and atomic publication; verify duplicate/invalid entries fail, failed publication preserves prior output without reporting success, and identical inputs produce identical bytes.
- [x] 2.3 Add a focused Modules host-tool build entry point and tool documentation; build it without application framework, USD, graphics or editor targets and cross-read its output with portable and Windows readers.

## 3. Native demo integration

- [x] 3.1 Define explicit native archive entries for mesh/font/material/environment and renderer resource dependencies; move demo shader-cache generation to NauDemo/build using existing sources/helpers and verify packaging no longer depends on running the SceneBaseSample build as a side effect.
- [x] 3.2 Add native package generation/deployment dependencies; verify a changed asset rebuilds the archive, a removed input fails despite an old archive, and all new generated outputs stay in demo-owned build/deployment paths.
- [x] 3.3 Replace native source-directory mounts with the portable archive mount and executable-relative bootstrap configuration before asset-consuming services initialize; verify existing asset URIs load and no runtime source-directory fallback remains.
- [x] 3.4 Repair native graphics teardown exposed by the visible resize/close check, releasing render-window GPU resources and settling pending work before driver destruction; verify Debug and Release visible close and startup-failure checks complete without resource-lifetime assertions or null-executor loops.
- [x] 3.5 Adapt native acceptance to packaged delivery; run Debug and Release outside the checkout from an unrelated working directory with source assets inaccessible, checking cube/environment/text, rotation, resize, close and missing/corrupt archive or required-entry failures.

## 4. Browser demo integration

- [x] 4.1 Update web build scripts to build or accept the separate host packer under NauDemo/build and generate the explicit web archive before preload/link; verify missing host prerequisites fail clearly and no native runtime binary enters the wasm link graph.
- [x] 4.2 Preload the archive, mount the portable filesystem and read mesh/font/JSON/shaders through it; remove the loose-entry CPU filesystem copy and verify actual Debug and Release browser rendering reaches Running only after successful asset startup.
- [x] 4.3 Update staging manifests, licenses and serving documentation for archive transport; verify source changes update the shipped bytes, missing inputs cannot use stale output, and relocated nested-base delivery works without loose asset sidecars.
- [x] 4.4 Adapt browser failure fixtures to modify the real archive/preload payload; verify missing archive, malformed/truncated archive, missing font/buffer and bad shader fail with identifying diagnostics and applicable cleanup without adding production demo hooks.

## 5. Integration acceptance and documentation

- [x] 5.1 Run package reader/writer and CLI suites in native Debug/Release and portable reader tests in real Chrome Debug/Release; record byte compatibility, numeric-boundary and failure-case results.
- [x] 5.2 Run complete native and real Chrome demo Debug/Release acceptance, including text/cube pixels, rotation, resize, visibility, ordinary/repeated Stop, context/host loss and relocation; record commands, tools, source revisions and structured results.
- [x] 5.3 Run affected standalone kernel and native/browser minimal lifecycle regressions and audit dependency graphs; verify package support introduces no concrete modules into Lite and no graphics/editor/USD into the host packer or minimal runtime.
- [x] 5.4 Execute and record a fresh-checkout build/delivery walkthrough separately from clean build-directory tests; verify documented host tool prerequisites, archive generation and relocated execution reproduce successfully.
- [x] 5.5 Update demo and package API/tool documentation with manifests, build locations, platform-specific contents, lifetime/limits and error behavior; format changed C++, run diff checks and strict OpenSpec validation, and attach final acceptance evidence.
