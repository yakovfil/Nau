# Validation: portable camera input

Validated on Windows on 2026-10-10 with MSVC 19.51.36260 (v145), Windows SDK
10.0.26100.0, CMake 4.2.1, Emscripten 6.0.9 and Chrome 155.0.8059.39.

## Delivery acceptance

| Platform | Configuration | Build, input acceptance and root launcher |
| --- | --- | --- |
| Windows | Debug | Passed |
| Windows | Release | Passed |
| Web | Debug | Passed |
| Web | Release | Passed |

All four final deliveries use prepared archive SHA-256
`a5dca98d85d59a851fdc7d0b7734e0a11e3621505e46e4f68aae05fa6177012e`.
The root launchers also freshly prepared and ran/served the authored project in
both configurations. Web launcher checks used a test-owned Chrome instance.

`NauDemo/tests/verify_input.py` exercises the production CoreInput service and
shared game controller through an independent rendered-frame observer. It checks
the authored camera UID, owner thread, live pose and submitted view-projection
matrix, all six movement directions, held/released state, drag sensitivity,
release outside the host, focus reset, resize and shutdown with active input.
Web checks cover DPR 1 and 2, unrelated page input, visibility reset, host loss,
partial callback installation failure and callback removal after Stop. Both
primary and middle buttons release correctly outside the host. Screenshots
confirm visible camera movement and rotation.

Native fixtures deliver messages to their own real Windows windows. Browser
keyboard/mouse events come from Playwright; visibility and initialization faults
are injected into the real DOM bindings. Deliveries are relocated outside the
checkout; browser acceptance uses a nested URL.

## Regression results

- Native input and camera unit tests: 9 passed per configuration. These include
  gainput action/signal processing, one automatic advancement per frame in
  milliseconds, manual sampling before a managed frame, invalid codes, focus
  reset, motion consumption, camera directions, diagonal speed and pitch/time bounds.
- Web input and camera unit tests: 6 passed per configuration under Node; real
  browser service acceptance is covered separately above.
- Existing rendering and billboard acceptance suites: passed on Windows and web
  in Debug and Release, including resource failures and orderly cleanup.
- Existing non-rendering startup acceptance: passed on both platforms in both
  configurations; all four non-rendering deliveries rebuilt successfully.
- Common-host native and browser Debug CTest suites: 18/18 passed each.
- Common-host scene CTest suite: passed.
- Eight rendering/non-rendering target graph audits: passed. Additional native
  and browser minimal graph checks found no CoreInput or gainput targets.
- Rebuilt desktop CoreInput, NauFramework and SceneBaseSample: visible startup
  and clean exit passed. Desktop queries retain gainput behavior and normalized
  mouse units; the packaged Windows/browser subset uses client/CSS pixels.
- Python/CMake declaration agreement tests, strict OpenSpec validation and
  component `git diff --check`: passed.

## Commands and evidence

From NauDemo, exercised `run_windows.bat Debug`, `run_windows.bat Release`,
`run_web.bat Debug` and `run_web.bat Release`. Configured the existing rendering
trees with `NAU_BROWSER_PROJECT_ACCEPTANCE=ON` and `NAU_PORTABLE_INPUT_TESTS=ON`
to build the probes and unit executables. From the checkout root, ran:

```powershell
python NauDemo/tests/verify_input.py Windows Debug
python NauDemo/tests/verify_input.py Windows Release
python NauDemo/tests/verify_input.py Web Debug
python NauDemo/tests/verify_input.py Web Release
python NauDemo/tests/audit_rendering_graphs.py
python NauEngineModules/tools/asset_tools/test_packaged_declaration.py
openspec validate add-portable-camera-input --strict
```

Also ran `verify_native_rendering.py`, `verify_web_rendering.py`,
`verify_billboards.py`, `verify_native_startup.py` and `verify_web_startup.py` for
their supported configurations. CTest used the common-host-native,
common-host-web-debug and common-host-scene trees under NauEngineModules/build.
Detailed command logs are under `NauDemo/build/input-*.log`; observer records,
archive identities and screenshots are under
`NauDemo/build/basic-rendering-scene/input-{windows,web}-{debug,release}/`.
Generated evidence is kept out of commits.

## Source revisions

Validation includes the uncommitted changes based on:

| Component | HEAD |
| --- | --- |
| Root | `f1936aa547ec06f8977299ea09389552b0fe9272` |
| NauEngineLite | `c2cddda56a8b910b3cee4ff991e5f628b5658c73` |
| NauEngineModules | `5d8b6028874b9473d65e2e7cccd2078c0e287cf0` |
| NauDemo | `7baefcb63c068d5ca2df7af7cf7240bf6719b93c` |
