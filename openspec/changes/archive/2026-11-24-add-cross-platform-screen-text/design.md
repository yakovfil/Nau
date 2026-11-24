# Design

## Context

See proposal.md for motivation. The current code supplies two independent rendering paths: native Graphics renders through Render and a frame graph; NauBrowserRenderer owns an application-worker WebGL 2 context and commits a frame directly after drawing the cube. Its commit must move after the new text pass.

The native frame graph in `modules/graphics/src/render_window/render_graph.cpp` already has an overlay stage after scene/debug rendering. Cocos2d-based UiManager is optional there. The existing UI FreeType target imports platform binaries, while `NauEngineLite/engine/3rdparty_libs/stb` exposes a header-only target containing stb_truetype.

NauDemo supplies an explicit browser dependency/source manifest and read-only packaged filesystem mounted at `/demo`. The new font must enter that mount. Web preload inputs, staging inputs, package hashes, and relocation checks must agree. The fast native `build.py` currently borrows SceneBaseSample's link settings, which will not automatically include a new text dependency.

## Goals / Non-Goals

**Goals:** share font parsing, basic line layout, coverage generation, and the public submission contract; keep backend uploads and draw calls inside engine modules; cache stable text rather than rasterizing each frame.

**Non-Goals:** port Cocos2d, change the standalone kernel's module independence, add a scene text component, build a general widget system, implement complex script shaping/bidi, accept arbitrary downloaded fonts, or claim runtime support beyond the current Windows and Emscripten targets.

## Decisions

### Portable text library in NauEngineModules

Create `modules/screen_text` with a small `NauScreenText` library. Its public header defines owning font/prepared-text handles, layout metrics, draw commands, and a common submission service contract. CPU implementation depends on NauKernel/VFS and the existing `stb` target; it has no Graphics, Render, WebGL, Cocos2d, or window dependencies. Renderer integration selects the implementation without exposing backend handles to the demo.

A proposed usage is `loadFont(vfsPath)`, `createText(font, utf8, logicalSize)`, and `draw(preparedText, position, rgba)`. Loads and preparation return Nau errors/results. Final declarations follow nearby Nau service/async conventions. Font loading uses a mounted VFS path and owns the bytes for the font handle's lifetime; it does not require a new asset importer or an offline font conversion pipeline. A persistent prepared handle can be submitted repeatedly; a submission becomes an immutable snapshot for a frame, rather than accumulating across frames.

Alternative: extend NauLabel. That couples this narrow feature to the desktop UI stack and does not solve the browser integration. Alternative: add a kernel feature. Feature modules already belong in NauEngineModules.

### Whole-string coverage bitmap from bundled stb_truetype

Compile stb_truetype's implementation in one private translation unit. Decode UTF-8 to codepoints, apply glyph advances and pair kerning, calculate bounds including negative bearings/descenders, and composite antialiased glyph coverage into one byte-per-pixel bitmap for the complete line. Preserve whitespace advances and baseline metrics. Empty text produces an empty drawable. Missing codepoints use the selected font's missing-glyph glyph without searching system fonts. Invalid UTF-8, line breaks, nonpositive/nonfinite sizes, unsupported font headers, and requests beyond documented allocation limits return errors.

Treat the requested size as font ascent-minus-descent height. Cache preparation by font identity, UTF-8 content, and raster size. Position/color changes reuse coverage; font/text/size changes produce new preparation. Use conservative limits on font bytes, codepoints, bitmap dimensions, and checked allocation arithmetic. Preflight the font envelope and table ranges before calling stb. This detects ordinary missing/unsupported inputs; it does not turn stb into a hardened parser for hostile fonts. Supported assets are project-controlled TTF files.

Alternative: source-built FreeType. It is viable for broader font handling but adds a dependency/build task here. Alternative: a glyph atlas. It improves frequently changing text but adds packing, eviction, batching, and lifetime machinery unnecessarily for a label.

### Engine-owned screen-space drawing in both renderers

Each backend uploads the coverage bitmap once per prepared image/raster scale and draws one textured rectangle with color multiplied by coverage. Use consistently defined alpha blending, no depth test/write, and viewport clipping; restore graphics state needed by subsequent rendering. Render after the scene and before final presentation. Transparent pixels leave the cube/background unchanged.

Native: add a small Graphics overlay pass and shader through existing Render/shader facilities. Publish immutable commands from the application thread; consume them on the graphics owner thread. Do not reuse UiManager or ImGui to draw the label.

Browser: add coverage texture/shader/rectangle resources to NauBrowserRenderer, consume the same command contract on the application worker, and commit only after both cube and text drawing. Add resources to partial-initialization, context-loss, and Stop cleanup. No DOM text elements or browser font API participates in drawing.

Coordinates use the upper-left of the drawable in logical units: native engine client pixels (scale 1 under the existing window API), browser CSS pixels. Browser devicePixelRatio converts these units to drawable pixels and selects raster resolution. A changed ratio refreshes only the affected raster/upload; positive resize preserves logical position and size, zero drawable area skips drawing. This deliberately avoids expanding native window DPI APIs in this change.

Alternative: rasterize using browser Canvas or Windows font APIs. Those would duplicate font behavior and put platform-specific text logic into the demonstration rather than the engine.

### Explicit lifetime and bounded caching

Font and prepared-text handles own CPU data. Queued commands retain their handles until consumed. GPU texture caches hold weak prepared-image identities and release unused resources at an owner-thread-safe point; native in-flight draws follow existing Render lifetime rules. Shutdown closes submission before draining/dropping commands and destroying backend textures/programs/buffers. Repeated Stop remains idempotent, and context loss does not trigger unsafe WebGL resource calls.

### Demo integration and assets

Bundle one redistributable font and its license in NauDemo and record its source/license in documentation. Use the same font path, string `Nau Demo`, size 24, position `(24, 24)`, and white color through shared demo setup on both targets. Native/browser adapter code only chooses the engine renderer service. Prepare the initial label before declaring startup ready; missing required font or upload failure is a startup error.

Update `NauDemoRuntime.cmake`, `naudemo_sources.json`, target links, package preload/staging inventory, and dependency audits for the text library and `stb`. Extend the native fast-build route to resolve the text dependency/registration from engine-generated settings, or emit a precise instruction to build the updated integrated NauDemo target if the old engine cache cannot supply them. It must not report success with the text feature omitted. Build outputs/evidence remain in NauDemo-owned directories.

### Acceptance based on rendered pixels

CPU tests use a known project font to verify bounds, kerning, whitespace, empty text, missing glyph behavior, invalid inputs, cache reuse/invalidation, and handle lifetimes on native and Wasm. Screen tests use the same font bytes and compare coverage-derived masks against the actual native render surface/browser canvas with tolerances for backend blending. Font substitution and DOM/window overlays must fail this check. Preserve the existing cube geometry/pixel assertions outside the text region.

Browser acceptance extends `web/test_package.py` for the label, changed text/size/color, resize/DPR, missing font, relocation, and cleanup. Native Debug/Release acceptance captures the actual demo rendering, changes the specified font to verify provenance, and closes the window normally. Graph checks retain the browser's excluded desktop targets and standalone kernel/minimal configurations.

## Risks / Trade-offs

- Whole-string bitmaps consume more memory for many labels or frequent edits -> bound dimensions/cache lifetime; this feature targets a small number of stable lines.
- stb does not guarantee safe parsing of hostile fonts -> use project-controlled packaged fonts, preflight detectable envelope errors, document that unsupported trust model.
- Basic codepoint layout cannot shape all languages -> document supported basic layout and add shaping only in a separate change.
- Native render thread and browser worker have different ownership rules -> keep CPU handles immutable and GPU resources strictly backend-owned; verify Stop and partial failures.
- Native logical units follow existing client pixels -> browser DPI scaling is covered; native DPI abstraction work is outside this change.
- Historical OpenSpec demo cadence differs from current code -> preserve the current presentation-driven behavior; this addition does not silently edit that unrelated requirement.

## Migration Plan

Add the CPU library and focused tests first, then native/browser rendering and the common API, then demo assets/build integration and acceptance. Rebuild matching engine modules and demo binaries in Debug/Release. The API is additive; rollback removes the demo integration and text target/backend hooks without changing existing scene assets or kernel APIs.
