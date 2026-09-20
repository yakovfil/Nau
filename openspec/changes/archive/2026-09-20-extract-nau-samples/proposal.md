# Proposal

## Why

Samples currently share the engine repository and assume its source layout, preventing independent sample ownership. The newly created NauSamples repository provides a destination while the recently validated native and browser builds provide a compatibility baseline.

## What Changes

- Extract all tracked content under NauEngineLite/samples into the root of NauSamples, preserving sample history and original license notices alongside the destination's existing initial commit.
- Register NauSamples as a root Nau submodule using https://github.com/yakovfil/NauSamples.git and record compatible engine, samples and demo revisions.
- **BREAKING**: remove the engine-local samples source tree. Introduce an explicit external samples path with the sibling checkout as the default; document the new checkout prerequisite.
- Preserve existing engine presets, sample target names, package outputs and native/browser behavior while updating source discovery, shader/resource paths, SDK installation and NauDemo integration.
- Update build guides, acceptance tooling and fresh-checkout verification for the additional repository.
- Fix the existing engine EASTL allocator alignment defect exposed by inputDemo validation, as explicitly approved by the user; retain portable allocation/reallocation/deallocation behavior and add regression coverage.

## Capabilities

### New Capabilities

- `external-samples`: Independently versioned samples, complete extraction, explicit dependency discovery and compatible native/SDK/browser consumption.

### Modified Capabilities

- `emscripten-build`: Select the minimal entry point from the external samples checkout instead of the engine-local samples path.

## Impact

Affected repositories are Nau, NauEngineLite, NauSamples and NauDemo. Integration touches engine CMake/presets and probes, sample CMake and runtime asset lookup, installed-SDK sample discovery, native demo assets/build helpers, reproduction scripts and documentation. Existing minimal-app-web, minimal-web-delivery-validation and naudemo-web behavior contracts remain unchanged and require regression validation. No sample rendering redesign, new platform support, SDK upgrade or relocation of NauDemo is included. Remote publication is a separate action from local extraction and validation.
