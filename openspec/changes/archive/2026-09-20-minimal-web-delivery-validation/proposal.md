# Proposal

## Why

The actual minimal sample runs in Chrome, but current acceptance serves its build
directory and cannot establish that another developer can run a copied package.
The remaining delivery gap is a complete staged folder, clear hosting failures
and real browser evidence independent of checkout and SDK locations.

## What Changes

- Stage separate Debug/Release delivery folders from the actual sample outputs,
  with current runtime inventory and removal of obsolete staged files.
- Provide a static launch page showing real lifecycle status, completed updates,
  Stop, cleanup and reload guidance; check browser prerequisites before loading
  the runtime and report missing isolation or runtime files clearly.
- Include a Python standard-library local server and concise package instructions
  so a copied folder can run without the engine checkout, SDK or build tools.
- Validate copied packages outside the checkout under a nested URL in Chrome on
  Windows, including runtime resource requests, lifecycle behavior and hosting/load
  failures, in both configurations.
- Coordinate staging and relocation evidence with `emscripten-build`, preserving
  its separate fresh-checkout/environment reproduction requirement.

## Capabilities

### New Capabilities

- `minimal-web-delivery-validation`: Portable minimal-sample delivery folders,
  prerequisite-aware launch UI, local serving and relocated browser acceptance.

### Modified Capabilities

None. The durable capability inventory is empty. Existing build, sample and
lifecycle change deltas retain their contracts; this change supplies the agreed
delivery integration and evidence, without changing runtime behavior.

## Impact

Affected areas are browser-only sample/package CMake, new delivery page/server
assets, staging and browser acceptance helpers, and build/prerequisite/package
documentation. Reuse the actual `MinimalAppSample`, pinned SDK 6.0.9, existing
lifecycle bridge and Chrome/Playwright test infrastructure. Serving requires
Python and Chrome, not emsdk, CMake, Ninja, vcpkg or Playwright.

Package staging is explicitly included by user agreement and remains coordinated
with `emscripten-build`. Fresh-checkout reproduction remains separate; uncommitted
source snapshots must not be presented as a clean committed checkout. No runtime
redesign, renderer, editor, hosted deployment, TLS provisioning, installer, CDN,
service worker, single-thread fallback or in-page runtime restart is included.
