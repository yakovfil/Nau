# Proposal

## Why

NauDemo currently loads loose native assets from checkout directories and uses a separate Emscripten file bundle on web. Using the engine's asset package format on both platforms will demonstrate engine asset delivery and allow the demo to run independently of source asset directories.

## What Changes

- Add a portable, read-only package filesystem to NauEngineLite using the existing uncompressed `nau-vfs-pack` format, with checked parsing and stream ownership.
- Retain the existing Windows package filesystem API and compatibility with valid existing packages.
- Add a small host-native command-line pack builder using AssetPackTool, with explicit input manifests and reliable failure handling; no AssetTool/OpenUSD import step is needed.
- Build platform-specific NauDemo archives containing existing assets, mount them through engine VFS, and preserve scene, text, rendering and lifecycle behavior.
- Repair the native graphics teardown exposed by visible packaged-demo acceptance, releasing GPU resources and settling render work before driver shutdown.
- Package native dependencies currently loaded through sample content/resource directories and remove runtime reliance on those directories.
- Keep generated tools, archives and validation artifacts under NauDemo/build; cross-compiled builds use a separately built host packer.

## Capabilities

### New Capabilities

- `portable-asset-packages`: Checked package construction and portable read-only VFS access using the existing package format.
- `naudemo-asset-packages`: Native and browser archive generation, mounting, complete asset delivery and failure behavior.

### Modified Capabilities

- `naudemo-web`: Clarify the host packaging prerequisite and require the browser delivery to contain and consume an engine asset archive.

## Impact

- NauEngineLite kernel IO/container handling, package filesystem and focused tests; no references to concrete modules or demo projects.
- NauEngineModules AssetPackTool, a focused host-tool build entry point and writer/reader compatibility tests.
- NauDemo CMake, build/staging scripts, platform asset adapters, configuration, delivery documentation and acceptance tests.
- Existing archive wire format and Windows factory remain supported. Native and web archive contents may differ for renderer-specific assets. Compression, encryption, asset cooking, remote streaming and renderer parity are outside scope.
