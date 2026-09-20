# Browser platform acceptance

Validated 2026-09-19 against engine base
`52197201e525a584fb9490be22b1d064b0c666e1` plus the current uncommitted changes.
No component revision was committed or archived.

## Results

| Check | Result |
| --- | --- |
| Browser platform Debug | 8/8 CTest cases pass; final run 10.90 seconds |
| Browser platform Release | 8/8 CTest cases pass; final run 10.91 seconds |
| Deliberate fixture failure | Exit 1 with GoogleTest failure, isolated page and zero remaining host registrations |
| Native minimal Debug lifecycle | 1/1 passes, 3.43 seconds |
| Native minimal Release lifecycle | 1/1 passes, 1.00 second |
| Wasm core Debug | CorePortability and CoreFatalDiagnostic pass, 0.70 seconds |
| Wasm core Release | CorePortability and CoreFatalDiagnostic pass, 0.60 seconds |
| Affected desktop targets | NauFramework and PlatformApp Debug compile with dependency project builds skipped |

Toolchain: emsdk 6.0.9, SDK Node 24.19.0, CMake 4.2.1, Ninja 1.13.2;
Chrome 153.0.8010.52, system Python 3.14.2 and Playwright 1.63.0. The installed
automation dependencies are pyee 13.0.1, greenlet 3.5.6 and typing-extensions 4.15.0.
Native validation uses VS 2022 Build Tools/MSVC 19.44.35229.0.

## Scenario evidence

All browser scenarios use the production PlatformApp module, generated static
registration, real kernel and shared PlatformWindowService. They do not use a
mock window manager or the core probe's header-only PlatformAppApi.

| Specification scenario | Evidence |
| --- | --- |
| Browser module supplies the real service | ProductionService discovers exactly one ICoreWindowManager; generated registration contains one PlatformApp entry; browser source graph excludes Windows platform files |
| Native lifecycle remains supported | Existing native lifecycle test passes in both configurations |
| Existing element becomes the active window | Valid case verifies stable identity, page initial visibility and actual host geometry |
| Additional window is requested | Empty createWindow result and captured unsupported diagnostic |
| Host selection fails | Missing, ambiguous and non-HTMLElement CTest cases return failed preInit with no published manager |
| Backend is missing | Backend case skips module initialization and observes explicit failed service preInit |
| Initialization fails after allocating resources | Callbacks case throws after installing a visibility listener; cleanup removes it and settles failed preInit without a live host registration |
| Host is resized through the service | Worker sets 320x240 border box, observes 316x236 client size with real padding/borders; repeated at DPR 2 |
| Page changes or constrains layout | CSS max-width clamps a request; subsequent page width changes are measured correctly |
| Host visibility is changed | Hide/show changes visibility while preserving measured layout width |
| An ancestor prevents display | display:none parent keeps host invisible |
| Document becomes hidden | Chrome backgrounds/restores a real tab with focus emulation disabled; status changes independently of element visibility |
| Host is named or positioned | Accessible label changes, document title stays unchanged, unsupported positioning returns documented fallback |
| Work arrives at an idle worker | Cross-worker callback wakes idle pump and executes once |
| A worker accesses the DOM-backed window | Worker-origin setters/readers observe confirmed DOM state; executor callback verifies platform-thread separation |
| Queue remains busy | Timed pump returns before a prefilled 64-callback batch drains while a producer continues; nonblocking pump returns promptly |
| Page removes the host | Hostloss case observes Failed status/diagnostic and safe disposal without rebinding |
| Disposal races with outstanding work | Queued callbacks and task complete while another worker mutates the window; cleanup accounts for in-flight operations |
| Idle or repeated disposal | Disposal completes with callbacks drained, repeated disposal passes, retained executor release is safe, and valid case preserves the page element |
| Platform acceptance is recorded | This record, per-build CTest logs and reproducible engine guide |

The runner additionally checks crossOriginIsolated, zero remaining host registrations
and zero graphics-context requests. CTest enforces a 100-second case timeout; its
normal cases complete in about 1–2 seconds. The intentional failing fixture verifies
failure propagation instead of relying only on green test runs.

## Reproduction and logs

Use `NauEngineLite/doc/browser_platform_services.md` for the full browser build loop
and the standalone negative fixture command. Browser logs are in each ignored
`build/browser-platform-{debug,release}/ctest.log` and
`Testing/Temporary/LastTest.log`; build diagnostics are in `build.log`.
The negative result is `build/browser-platform-debug/browser-fixture-failure.json`.

Native and core regression commands, from NauEngineLite:

```powershell
cmake --build build/native-minimal-debug --config Debug --parallel 8
ctest --test-dir build/native-minimal-debug -C Debug --output-on-failure
cmake --build build/native-minimal-release --config Release --parallel 8
ctest --test-dir build/native-minimal-release -C Release --output-on-failure
cmake --build build/wasm-core-debug --parallel 8
ctest --test-dir build/wasm-core-debug --output-on-failure
cmake --build build/wasm-core-release --parallel 8
ctest --test-dir build/wasm-core-release --output-on-failure
cmake --build build/desktop-platform-after --config Debug --target NauFramework PlatformApp --parallel 8 -- /p:BuildProjectReferences=false
```

Native/core logs use `browser-platform-build.log` and `browser-platform-ctest.log`
inside their existing build directories. The desktop target log is
`build/desktop-platform-after/browser-platform-target-build.log`.

## Implementation decisions and limits

The existing executor callback API cannot reject/cancel an arbitrary Invocation.
Accepted work is drained. Closing/closed executor submissions are diagnosed and
completed on the submitting thread, avoiding lost coroutine continuations without
adding a kernel API. Late work has no platform-thread affinity; new DOM operations
remain rejected. This behavior is documented and exercised with a late task.

The broader desktop dependency build fails on existing native kernel source
selection: core_platform.cpp from the Emscripten directory is compiled natively,
and `nau_utf8` collides during that build. The affected desktop targets above pass
with dependency builds skipped; no full desktop application success is claimed.

Application startup still ignores service startup errors in ApplicationImpl.
Application scheduling, stop controls, minimal sample browser entry integration,
staging and relocation remain subsequent capabilities. The browser application
presets keep their existing guard. This change does not complete those
emscripten-build tasks and does not alter renderer, editor, NauDemo or bundled code.
