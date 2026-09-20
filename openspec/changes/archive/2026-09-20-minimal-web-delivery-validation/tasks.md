# Tasks

## 1. Delivered launch page

- [x] 1.1 Add the authored delivery page with secure-context/isolation/threaded-browser checks before loader insertion; verify absent headers and file URLs show serving guidance, leave Stop unavailable and make no runtime resource requests.
- [x] 1.2 Connect visible state/count/diagnostics, asynchronous Stop and retained final cleanup/reload reporting to the existing lifecycle bridge; verify page controls against the actual sample without synthetic updates, test query switches or runtime recreation.
- [x] 1.3 Handle loader errors and pre-bridge Wasm aborts without false startup/cleanup claims; verify missing-loader/missing-Wasm failures and a labeled page-level abort-hook check retain diagnostics despite later UI callbacks.

## 2. Standalone package server and instructions

- [x] 2.1 Add the Python standard-library loopback server with package-relative root, configurable port/base path, launch URL, COOP/COEP, no-cache and Wasm MIME handling; verify root and nested-path responses, out-of-root/traversal rejection and occupied-port diagnostics using copied assets.
- [x] 2.2 Add package-local instructions distinguishing serving requirements from build/test dependencies, including normal launch, another port, file-URL/isolation errors and reload behavior; verify documented commands work from outside the checkout without repository imports or SDK/build-tool environment variables.

## 3. Browser package staging

- [x] 3.1 Define the pinned SDK runtime inventory from actual sample link outputs and add the browser-only default-build MinimalAppWebPackage target with per-configuration package paths; verify both preset builds stage the real loader/Wasm and delivery files without assuming a separate worker filename or adding a system Python build dependency.
- [x] 3.2 Implement validated temporary staging, owned destination replacement and configuration/SDK/file-hash manifest generation; verify missing inputs and unsafe destinations fail, obsolete staged files disappear, unrelated paths are preserved and clean/repeated staging inventories match.
- [x] 3.3 Build Debug and Release packages from clean build/staging directories and audit their manifests, file hashes and source/link identities; verify configuration independence, current runtime completeness and absence of required external debug-symbol/source resources without claiming fresh-checkout reproduction.

## 4. Relocated Chrome acceptance and regressions

- [x] 4.1 Add a runner that copies each package outside the entire workspace and launches the copied server under a nested URL with a neutral environment; verify request/response capture includes worker resource loading and rejects requests outside the copied package or to original checkout/SDK paths.
- [x] 4.2 Verify relocated actual-sample startup, visible progress, five-second 8–12 Hz cadence, UI heartbeat, real hide/show, Stop/repeated Stop and stable final cleanup/reload behavior in Chrome Debug/Release; retain structured results, network evidence and rendered page screenshots.
- [x] 4.3 Add missing-header, file-URL, missing-loader, missing-Wasm, host-loss and server-startup failure acceptance, plus an intentional runner-expectation failure; verify each produces its specific diagnostic/outcome and unrelated infrastructure errors cannot count as expected failures in either configuration.
- [x] 4.4 Build native minimal targets and run their shared lifecycle tests in Debug/Release after browser CMake integration; verify no package target/browser options leak into native builds, rerun actual-sample acceptance and the existing lifecycle suite as affected regressions, and record real-abort evidence separately from page-hook simulation.
- [x] 4.5 Record every delivery specification scenario in validation.md with source state, tool versions, exact build/serve/test commands, external copy locations, nested URLs, runtime inventories and measured results; verify all required Debug/Release outcomes have evidence and full-checkout reproduction is explicitly distinguished.

## 5. Documentation and coordinated completion

- [x] 5.1 Update prerequisites.md, build.md and engine sample/delivery guides with tested package paths, serving commands, browser limitations, status/Stop behavior and negative-case guidance; verify the distributed instructions remain self-contained and ordinary serving requires neither SDK nor automation dependencies.
- [x] 5.2 Cross-reference verified staging/package/relocation evidence in emscripten-build tasks 4.1–4.3, 5.2, 5.4 and 6.1 and refresh its scenario review; verify only fully satisfied criteria are checked and task 6.2 remains pending for separate fresh-checkout/environment reproduction.
- [x] 5.3 Run strict OpenSpec validation for this change and affected build artifacts, review scope/whitespace changes and reconcile task evidence; verify no runtime redesign, renderer/editor work, deployment, commit or archive is introduced by applying this delivery change.
