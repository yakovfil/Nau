# Delivery acceptance — 2026-09-20

## Source and tools

Applied to the dirty engine working tree based on
`52197201e525a584fb9490be22b1d064b0c666e1`, parent repository
`b7647ed488572f889d8c125ea75d3ef5a683bc98`. Prerequisite runtime/sample changes
remain uncommitted. This is clean build-directory and copied-package evidence,
**not fresh-checkout/environment reproduction**. No commit or archive was made.

`NauEngineLite/build/delivery-source-state.json` records both Git statuses,
recursive dependency revisions, tracked-diff hash and individual modified/untracked
implementation-file hashes. Its SHA-256 is
`fa67ad42f877654931b9e0af9526bc8c1071ebc8f05524c497b0a82acd5632c7`.
`build/delivery-summary.json` reconciles all 18 delivery and eight raw-sample
outcomes, inventories and manifest hashes. These are local generated evidence.

Tools: external emsdk **6.0.9** at `C:/Users/Yakov/emsdk`, SDK Node 24.19.0 and
Python 3.13.3; CMake 4.2.1, Ninja 1.13.2; test Python
`C:/Python314/python.exe` 3.14.2 with Playwright 1.63.0; Chrome
`C:/Program Files/Google/Chrome/Application/chrome.exe` 153.0.8010.52.
Native: VS 2022 Build Tools 17.14.41, MSVC 19.44.35229.0, SDK 10.0.26100.0.
Python 3.9+ is the server's language/API requirement; the executed server tests
used 3.14.2. CMake's Emscripten shared-library warning does not affect this static
application. No SDK, dependency or runtime C++ changes were needed for delivery.

## Clean builds and package inventory

From `NauEngineLite`, existing browser directories were first moved to
`build/web-minimal-{debug,release}-before-delivery`, after resolving and checking
both source paths under the engine build root. The original preset destinations
were absent before these commands:

```powershell
$env:PATH += ';' + [Environment]::GetEnvironmentVariable('Path','User')
$env:EMSDK_QUIET='1'
. C:/Users/Yakov/emsdk/emsdk_env.ps1
cmake --preset web-minimal-debug
cmake --build --preset web-minimal-debug
cmake --preset web-minimal-release
cmake --build --preset web-minimal-release
C:/Python314/python.exe cmake/probes/minimal_app_web/audit.py
C:/Python314/python.exe cmake/probes/minimal_web_delivery/test_package.py -v
```

Both builds completed **105 steps**, including the actual application link and
default-build package target. Graph audits report **38 targets / 97 compile
commands** each, exactly one minimal entry point, correct module/static and
pthread inputs, no desktop feature targets/libraries, and unchanged native
caches/desktop wrapper. Unsupported browser desktop/shared settings still fail.
Logs: `build/delivery-{debug,release}-{configure,build,restage}.log`,
`build/delivery-graph-audit.log`, and each browser directory's
`sample-graph-audit.json`. Later authored server fixes were restaged by ordinary
default builds; all final browser evidence uses those final asset hashes.

Each `build/web-minimal-{debug,release}/package` has exactly:

```text
index.html
MinimalAppSample.js
MinimalAppSample.wasm
serve.py
README.md
manifest.json
```

The manifest records configuration, SDK 6.0.9 and the SHA-256 of the other five
files. Raw link-output hashes match staged runtime hashes. Configurations remain
independent, with different JS and Wasm content. The SDK embeds worker support
in the loader; neither a separate worker script nor external symbols are needed.

| Runtime | Debug SHA-256 | Release SHA-256 |
| --- | --- | --- |
| JS | `ffa15865c1f9fe92cee030abc92e9795d34a6ee49250383d53109365d96063e6` | `df494c82a99231b5a1c1c7b4f8e1db2b6712525e23b5f70b1055874d38906bb2` |
| Wasm | `cb0bc13cb7ce78c1db81fd8f96151415c011adfb566938b84bff2abd1a145f40` | `ab2a0d47c638c23f79c7909170e243703699f9bfd80cb39645dc1613d7163269` |

Shared asset hashes: index.html
`183e670380192e2c22d4fc0435bae1ab119e2b86f6aedbac6ded08ce7467acd6`, serve.py
`936a7a2e11b62d917e9630f435d2d0c75a3c379bf04d7cf00aa8f8cba9fbfdc7`, README.md
`02366d57ee0f5a38f06087eac9030beaa7c8f5caab19ea8226f4e3535367b2e5`.

The two standard-library contract tests pass. Disposable staging validates hashes,
clean/repeated inventory equality, obsolete worker-file removal, preservation of
unrelated files, missing-Wasm diagnostics and unchanged old manifest, rejection
of build-root/source/outside destinations, and blocked replacement diagnostics.
Copied-server checks cover root/nested URLs, headers, no-cache, Wasm MIME,
encoded traversal/backslash rejection, a Windows junction escape rejection,
outside-base 404 and occupied-port failure.
Windows socket exclusivity prevents a second server from silently sharing a port.
Evidence: `build/delivery-package-tests.log`.

## Relocated Chrome acceptance

Exact runner invocations, from the engine directory:

```powershell
foreach ($configuration in @('debug', 'release')) {
    foreach ($scenario in @('success', 'host-loss', 'missing-headers', 'file-url',
                            'missing-loader', 'missing-wasm', 'abort-hook',
                            'server-startup', 'runner-failure')) {
        C:/Python314/python.exe cmake/probes/minimal_web_delivery/run.py --build "build/web-minimal-$configuration" --scenario $scenario
    }
}
```

Each run verifies the manifest and copies the folder outside the **entire Nau
workspace**. Positive/file-loss runs invoke absolute Python and copied serve.py
with `--port 0 --base-path /relocated/nau/`, from the neutral temporary parent.
Only COMSPEC, SYSTEMROOT, TEMP, TMP, USERPROFILE and WINDIR are retained in the
server environment: no PATH, SDK, build-tool or repository variables/imports.
Missing-header acceptance uses a separate test-only server; delivered serve.py
has no header-disabling option. File-URL acceptance opens the copied index.html.

Primary successful copies and URLs (copies removed after acceptance):

| Configuration | External package | URL |
| --- | --- | --- |
| Debug | `C:/Users/Yakov/AppData/Local/Temp/nau-delivery-42_i8u69/package` | `http://127.0.0.1:54854/relocated/nau/` |
| Release | `C:/Users/Yakov/AppData/Local/Temp/nau-delivery-kkc9sgiy/package` | `http://127.0.0.1:50299/relocated/nau/` |

Each successful trace contains one page request, **13 loader requests/responses**
(page plus 12 worker loads), and one successful Wasm fetch. All return 200 inside
the copied URL base. Worker events identify all 12 script URLs; the runner asserts
worker loader requests are present in network capture. No original source, SDK,
external host, symbol or debug-source request occurs. Wasm uses application/wasm.
The actual worker reaches Running, advances steps and reports completed cleanup.
This establishes runtime independence without removing the installed checkout/SDK.

| Scenario | Debug | Release | Checked outcome |
| --- | --- | --- | --- |
| success | Pass, 9.7626 Hz / 502 heartbeats | Pass, 9.7673 Hz / 502 heartbeats | Five-second 8–12 Hz cadence, real hide/show, no catch-up, visible count, UI Stop, two Stop requests during cleanup, stable final count 59, Stopped/cleanup complete, reload-only retry |
| host-loss | Pass | Pass | Real DOM host removal after Running; terminal Failed/Running-phase diagnostic, cleanup complete, zero retained platform hosts |
| missing-headers | Pass | Pass | Visible cross-origin-isolation/server guidance, Stop disabled; zero loader/Wasm/worker requests |
| file-url | Pass | Pass | Visible local-file/server guidance, Stop disabled; zero loader/Wasm/worker requests |
| missing-loader | Pass | Pass | Explicit MinimalAppSample.js loading failure, no Running/Stopped or cleanup claim |
| missing-wasm | Pass | Pass | Retained Wasm-fetch abort diagnostic, no Running/Stopped or cleanup claim |
| abort-hook | Pass | Pass | **Controlled page-hook simulation**, not real Wasm abort; Failed and original message survive later callbacks, cleanup not confirmed |
| server-startup | Pass | Pass | Second copied server returns 1 with choose-another-port diagnostic; first server still runs the real application successfully |
| runner-failure | Expected runner 1 | Expected runner 1 | Exact `Deliberately violated acceptance expectation`, after application code 0 and all success checks; unrelated infrastructure errors rejected |

JSON, full request/response logs, worker URLs, snapshots, diagnostics and PNGs
are in `build/web-minimal-{debug,release}/delivery-evidence/`. Running/stopped
screenshots are also retained there. Stopped and missing-Wasm screenshots were
visually inspected: readable status/count, accurate cleanup, disabled Stop and
reload/serving guidance. Raw console summaries are `build/delivery-<config>-<scenario>.log`.

## Regressions

Native shell (without SDK activation):

```powershell
foreach ($configuration in @('Debug', 'Release')) {
    $directory = "build/native-minimal-$($configuration.ToLower())"
    cmake --build $directory --config $configuration --target MinimalAppSample NauMinimalLifecycleTests --parallel 8
    ctest --test-dir $directory -C $configuration --output-on-failure
}
C:/Python314/python.exe cmake/probes/test_minimal_runtime.py --minimal build/native-minimal-debug --minimal build/native-minimal-release --desktop build/desktop-platform-after
```

Both native samples build; **19/19 Google Tests** pass in each configuration
(one CTest executable). Native graphs retain 18 targets, no package target or
browser options; existing desktop graph selection passes. Logs are native
`delivery-{build,tests}.log`, `Testing/Temporary/LastTest.log`, and
`build/delivery-native-graph.log`.

With SDK activated:

```powershell
foreach ($configuration in @('debug', 'release')) {
    cmake --build "build/browser-runtime-$configuration"
    ctest --test-dir "build/browser-runtime-$configuration" --output-on-failure
    foreach ($scenario in @('success', 'missing-host', 'host-loss', 'runner-failure')) {
        C:/Python314/python.exe cmake/probes/minimal_app_web/run.py --build "build/web-minimal-$configuration" --scenario $scenario
    }
}
```

Browser lifecycle passes **13/13 CTest** in both configurations, including
`BrowserRuntime-abort`, which is the real fatal-abort regression distinct from
the delivered page-hook simulation. Actual raw-sample success/missing-host/host-loss
pass and deliberate runner failure has the exact expected code/diagnostic.
Logs are lifecycle `delivery-{build,tests}.log` and browser sample
`delivery-raw-<scenario>.json` (PowerShell UTF-16; parse bytes or specify encoding).

## Specification and completion review

All delivery scenarios are covered above: configuration coexistence, stale/missing
staging inputs, absent isolation/local file, missing JS/Wasm, real controls and
terminal failures, copied serving/port failure, nested resource independence,
declared validation and intentional runner failure. Build commands, serving
requirements, package paths and limitations are documented in root build.md and
prerequisites.md, engine delivery/sample/build guides and distributed README.md.

This evidence completes emscripten-build tasks 4.1–4.3, 5.2, 5.4 and 6.1. Its 6.2
remains pending for genuine fresh-checkout/environment reproduction. Earlier
sample/fixture records retain their historical scope; they are not relabeled as
delivery or reproducible-source evidence.

Scope is browser-only sample packaging CMake, authored page/server/README,
delivery probes, documentation and OpenSpec tracking. Existing dirty prerequisite
and editor changes are preserved. No runtime redesign, rendering, editor work,
dependency update, deployment, commit or archive is introduced. Strict OpenSpec validation passes for this change and emscripten-build; root
and engine git diff --check and new-file whitespace/Python syntax checks pass.
All 16 implementation tasks are complete.
