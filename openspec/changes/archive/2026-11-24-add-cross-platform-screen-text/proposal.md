# Proposal

## Why

NauDemo needs to demonstrate engine-rendered text from a specified TTF asset on native Windows and in the browser. The existing Cocos2d-based UI module cannot be used by the minimal browser renderer, and platform window labels or HTML overlays do not demonstrate this engine capability.

## What Changes

- Add a small portable screen-text library in NauEngineModules: load project-controlled TTF assets through Nau VFS, prepare a single UTF-8 line at a specified size, and retain its coverage bitmap and metrics.
- Reuse the engine's bundled stb_truetype implementation and rasterize the complete string when font, text, or raster size changes.
- Expose one platform-neutral submission API for prepared text, upper-left position, logical pixel size, and color. Implement textured-rectangle rendering inside native Graphics and NauBrowserRenderer.
- Display "Nau Demo" through this API on both targets using the same bundled, redistributable TTF asset. Package the font and its license for browser delivery.
- Verify rendered pixels, font provenance, resize/DPI behavior, resource lifetime, and existing cube rendering in Debug and Release.
- Keep the feature limited to single-line text; full UI integration, editable text, shaping, wrapping, glyph atlases, and arbitrary external font ingestion are outside this change.

## Capabilities

### New Capabilities

- `screen-text`: Portable loading, preparation, submission, rendering, and lifetime of a single TTF text line with native and browser renderer implementations.

### Modified Capabilities

- `naudemo-web`: Add acceptance requirements for an engine-rendered font label in native and browser NauDemo, including relocatable font assets and visible-output verification.

## Impact

- NauEngineModules: new `modules/screen_text` library and tests; native Graphics overlay integration; browser_renderer overlay and cleanup.
- NauDemo: shared label setup, native and browser adapters, TTF/license assets, CMake and explicit runtime/source manifest, preload and staging inventory, fast native build integration, package tests, and documentation.
- NauEngineLite: consume the existing bundled `stb` dependency through shared build facilities; keep feature code and concrete module references outside the standalone kernel.
- OpenSpec: new screen-text capability and an additive NauDemo requirement. Existing specs contain a historical 100 ms demo cadence while the current code follows presentation frames; this change preserves the current code and does not revise that unrelated requirement.
- The API is additive. Backend graphics operations remain engine-owned; no new OS text or DOM text path is introduced into demo rendering.
