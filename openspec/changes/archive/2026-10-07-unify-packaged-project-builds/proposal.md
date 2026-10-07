# Proposal

## Why

EditorProject already runs packaged scenes in a browser, but its Windows build uses a separate launcher, dependency graph and asset-loading path. A shared non-rendering project build will make platform differences explicit and allow the same game code and cooked content to be validated on Windows and web before expanding rendering support.

## What Changes

- Provide Windows and web Debug/Release builds of the same packaged, non-rendering scene application using one entry source and startup implementation.
- Separate runtime feature selection from target platform; declare the portable modules and supported project components once for build, cooking and runtime validation.
- Share native asset preparation and allow the exact same prepared archive to be delivered to either platform.
- Provide a common build interface with platform/configuration selection, isolated outputs, actionable prerequisite failures and thin platform run wrappers.
- Preserve existing browser commands and the current rendered Windows SDK build as a separate selectable route.
- Validate native/browser scene state, failure handling, logging and orderly shutdown from relocated deliveries.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `editor-project-web-startup`: Extend the existing packaged project capability with shared Windows/web builds, a common project declaration and archive, and cross-platform acceptance. Existing browser requirements remain applicable.

## Impact

- NauEngineModules: generalize browser project CMake integration, native preparation tooling and packaged-scene delivery; retain module ownership here.
- NauDemo/EditorProject: shared portable entry, project declaration, build/run helpers, documentation and acceptance tests; retain the rendered Windows launcher and SDK route.
- NauEngineLite: reuse the common host, native/browser platform services and archive filesystem; only narrowly required platform-independent integration fixes are in scope.
- Native cooking still requires provisioned asset tools, a matching SDK/registration DLL and OpenUSD/Python. Web compilation still uses the recorded Emscripten SDK. No new third-party dependency is planned.

## Non-goals

Rendering unification, browser graphics/physics/audio/input/animation enablement, editor export UI, broad template migration, arbitrary project compatibility, automatic SDK installation, and replacing the existing rendered Windows build.
