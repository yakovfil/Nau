# Tasks

## 1. Selected sample lifecycle integration

- [x] 1.1 Add minimal sample delegate setup that checks module loading and registers the production platform-window service; use checked creation on the native path and verify setup errors cannot be ignored or dereference an empty application, while native Debug/Release sample compilation succeeds.
- [x] 1.2 Route the Emscripten branch of app_sample_main_min.cpp through runBrowserApplication and preserve the native successful startup/step/sleep path; verify the actual sample source uses the existing driver without another browser loop, main or injected fixture services.

## 2. Production browser preset and graph integration

- [x] 2.1 Replace the obsolete top-level browser prerequisite rejection with supported Emscripten/minimal-profile checks and update preset selection/descriptions; verify both browser presets configure through the real engine graph and unsupported browser/compiler/profile combinations report actionable errors.
- [x] 2.2 Apply the existing static threaded options and proven runtime-exit/pthread-pool/main-thread-blocking settings to MinimalAppSample only on Emscripten; verify generated Debug/Release compile/link commands contain the selected sample main, production static registration and compatible Wasm runtime/dependency inputs with no native libraries.
- [x] 2.3 Complete any required minimal-profile graph gating using existing dependency/module selectors; verify generated targets exclude desktop feature chains and unrelated samples/tests, configure with desktop dependencies unavailable, and confirm desktop generator checks and source-tree run_tests.bat generation are skipped.
- [x] 2.4 Update build-contract checks that assumed the obsolete prerequisite rejection; run applicable SDK, missing-source, platform-option and native-cache isolation checks and verify exact SDK errors still work without implicit installation or activation.

## 3. Actual sample acceptance harness

- [x] 3.1 Add a small host page and runner consuming the existing preset-built MinimalAppSample outputs, reusing isolated Chrome and COOP/COEP infrastructure; verify no replacement C++ target is built, status/count are visibly derived from the existing bridge, Stop becomes usable when the bridge exists, and runner dependencies are unnecessary for ordinary sample compilation.
- [x] 3.2 Add success, real hide/show and repeated Stop acceptance with ordered snapshot/count checks; verify a five-second foreground measurement, responsive page heartbeat, no catch-up burst, stable final status, completed platform/runtime cleanup, successful application exit and reload-only restart behavior on the actual sample.
- [x] 3.3 Add missing-host and host-loss cases plus a deliberate runner-expectation failure; verify startup failure has no Running/updates, runtime failure freezes subsequent counts, both report diagnostics and safe cleanup with nonzero application exit, and unexpected assertions/infrastructure failures produce nonzero runner results.

## 4. Integrated build and regression evidence

- [x] 4.1 Build the actual sample from isolated empty Debug/Release browser build directories using SDK 6.0.9 and the existing presets; record configure/build commands, source/link graph audit and actual JS/Wasm/worker-support output inventory without claiming staged-package or fresh-checkout delivery acceptance.
- [x] 4.2 Run every actual-sample acceptance case in Chrome on Windows for Debug and Release; record browser/tool versions, five-second rates, heartbeat and real visibility results, status/Stop/failure assertions and the deliberate failing-runner result against every spec scenario in validation.md.
- [x] 4.3 Build the actual native minimal sample in Debug/Release and run its shared lifecycle/timing regression suite; verify Windows-only platform selection, no Emscripten options or SDK requirement, native cache independence and preservation of the desktop sample source selection.
- [x] 4.4 Rerun browser lifecycle, browser platform and Wasm core regressions in both configurations after shared build integration; record results and resolve regressions introduced by this change, broadening native desktop compilation only if affected shared paths require it.

## 5. Documentation and coordinated handoff

- [x] 5.1 Update prerequisites.md, build.md and engine-local sample/build guides with tested preset/runner commands, output paths, status/Stop usage, existing timing/failure defaults and the test-harness boundary; verify every documented command matches an implemented entry point and remove superseded prerequisite diagnostics from relevant guidance.
- [x] 5.2 Cross-reference verified build-graph/prerequisite evidence in emscripten-build tracking and update the minimal-web-delivery-validation handoff; complete overlapping tasks only when all their criteria pass, leaving package staging, relocation, fresh-checkout reproduction and other unmet delivery criteria unchecked.
- [x] 5.3 Review all minimal-app-web scenarios against validation.md and run strict OpenSpec validation for this change and affected handoff artifacts; verify the final scope audit includes no renderer/editor implementation or unrelated submodule edits and that implementation tasks are marked complete only with recorded evidence.
