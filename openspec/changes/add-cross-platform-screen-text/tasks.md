# Tasks

## 1. Portable text API and assets

- [x] 1.1 Add `NauEngineModules/modules/screen_text` with the public font/prepared-line handles, metrics, frame submission contract, and `NauScreenText` CMake target using NauKernel and bundled stb; verify a small consumer compiles on Windows and Emscripten without renderer/UI headers.
- [x] 1.2 Add a redistributable TTF and license in NauDemo assets, record source/license/hash and supported input limits, and supply the same font to test fixtures; verify the files and attribution are present and tests identify the font bytes explicitly.
- [x] 1.3 Implement VFS font loading with owned bytes, bounded reads, detectable font-envelope validation, and asset-specific errors; verify native/Wasm tests cover a valid mounted asset, missing/empty/unsupported input, oversized input, and font-handle lifetime.

## 2. Line preparation and resource ownership

- [x] 2.1 Implement single-line UTF-8 decoding, font metrics, advances/kerning, bounds, missing-glyph policy, and coverage compositing in one private stb implementation translation unit; verify CPU tests cover kerning, spaces, negative bearings/descenders, empty text, missing codepoints, malformed UTF-8, line breaks, invalid sizes, and checked bounds on native/Wasm.
- [x] 2.2 Implement bounded preparation reuse keyed by font/text/raster size and owning prepared handles; verify unchanged preparation is reused, position/color do not rerasterize, changed inputs do refresh coverage, and released handles allow cache reclamation.
- [x] 2.3 Implement the shared submission service with immutable per-frame snapshots, explicit owner-thread handoff, retained handles for accepted work, and shutdown rejection; verify focused tests cover nonaccumulating frames, release after submission, and repeated shutdown.

## 3. Renderer integration

- [x] 3.1 Add native Graphics coverage-texture upload and screen-space rectangle shader/pass after scene rendering through Render; verify an integrated native build and rendered-surface capture show correct color/alpha, upper-left placement, clipping, and unchanged scene pixels outside glyphs.
- [x] 3.2 Add the same submission consumer and coverage draw pass to NauBrowserRenderer before its final commit; verify a Debug browser render shows text in the canvas itself, and the existing cube geometry/pixel assertions still pass.
- [x] 3.3 Implement native cache eviction/in-flight lifetime and browser text cleanup for normal Stop, partial initialization, and context loss; verify repeated Stop, released labels, controlled upload failure, and browser context-loss checks account for resources without duplicate teardown.
- [x] 3.4 Implement browser logical-to-drawable conversion and raster refresh at changed device pixel ratio, retaining native engine client-pixel coordinates; verify resize, DPR changes, clipping, and zero-area/resume preserve placement and logical text size.

## 4. NauDemo and build/package integration

- [x] 4.1 Add shared demo label setup for `Nau Demo`, the selected font, size 24, position (24, 24), and white color; connect native/web adapters to the same engine API and gate ready state on font/preparation/upload success; verify both targets display the label and a missing font produces an asset-specific startup failure.
- [x] 4.2 Update NauDemo CMake links, `cmake/NauDemoRuntime.cmake`, `cmake/naudemo_sources.json`, and profile audit expectations for `NauScreenText` and stb; verify configure/build and dependency audits exclude desktop UI/Render from the browser graph and preserve standalone kernel/minimal graph independence.
- [x] 4.3 Update web preload assets, `/demo` filesystem population, `web/stage.cmake` inventory/hashes, and packaging documentation for the TTF/license; verify staging tests cover exact inventory, missing font/license rejection, and preservation of the last valid package after staging failure.
- [x] 4.4 Update the native `build.py` route to include new dependencies from generated engine configuration, or clearly diagnose an incompatible old cache and direct the user to the integrated NauDemo target; verify the route cannot silently produce a binary without text, and native build/evidence output remains under NauDemo.

## 5. Cross-target acceptance and documentation

- [x] 5.1 Extend browser package acceptance to compare actual canvas glyph pixels with the specified font, exercise changed font/text/size/color, relocation under a nested URL, resize/DPR, missing font, and Stop; run Debug and Release and retain structured results/screenshots under NauDemo/build, with failures producing nonzero status.
- [x] 5.2 Build and run native Debug and Release NauDemo, capture the actual rendering for font-derived glyph checks and changed-font provenance, verify resize/clipping/scene preservation, and close normally; retain commands, revisions, screenshots, and shutdown/log results under NauDemo/build.
- [x] 5.3 Run focused native/Wasm text tests, affected existing demo scene/lifecycle/browser checks, and standalone kernel/minimal configuration regressions; verify recorded results distinguish successful checks from unavailable toolchains or unexecuted checks.
- [x] 5.4 Document the common API, asset path and license, logical coordinate/size semantics, cache/lifetime behavior, supported font trust model, single-line/shaping limits, and native/web build commands; verify examples match the implemented API and all generated outputs remain excluded from commits.
