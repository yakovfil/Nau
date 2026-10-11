# Battlezone scene validation

Validated on 2026-10-11. Implementation is in the working trees; the following
are committed baselines, not commits containing this change:

- Root: `3e9a7abe7c983e0f419185802cd69782bd2594c4`
- NauEngineModules: `763581ded0e884cfe6f754a7b9b0fe9256ec7475`
- NauDemo: `96acf97c49928e38d5d0af3299da69a180aeb214`
- NauEngineLite, unchanged: `3f1bae6a6942a0693dd9095fa32e53a5a658983a`

Tools: Windows build 26200, MSVC 19.51.36260.0/v145, Windows SDK 10.0.26100.0,
CMake 4.2.1, Emscripten 6.0.9, its Node 24.19.0, Chrome 155.0.8059.39,
Python 3.10.11 for OpenUSD 24.08/native cooking, Python 3.14.2 for acceptance,
Playwright, Pillow, soundcard and NumPy. Native captures use Orca 1.4.224.

## Production game matrix

All four configurations pass `verify_battlezone.py` using the same archive:

`e9f6503ef980237af378fce517130064aec85f3224e0000dadd677c9e4a7be6e`

| Target | Configuration | Result | Measured audio peak |
| --- | --- | --- | --- |
| Windows | Debug | PASS | 0.13927 |
| Windows | Release | PASS | 0.12252 |
| Chrome/WebAssembly | Debug | PASS | 0.11948 |
| Chrome/WebAssembly | Release | PASS | 0.11948 |

Typical commands from the checkout root (activate EMSDK before web commands):

```powershell
./NauDemo/build.ps1 -Platform Windows -Configuration Debug -Declaration D:/Programming/github/Nau/NauDemo/portable_rendering_project.json
cmake -S NauEngineLite -B NauDemo/build/basic-rendering-scene/windows-debug -DNAU_BROWSER_PROJECT_ACCEPTANCE=ON -DNAU_BILLBOARD_TESTS=ON
cmake --build NauDemo/build/basic-rendering-scene/windows-debug --config Debug --target NauDemoMainPackage NauBattlezoneProbePackage NauBattlezoneTests NauVectorContractTests test_input test_portable_audio --parallel 8
python NauDemo/tests/verify_battlezone.py --platform Windows --configuration Debug
```

Web uses `-Platform Web`, `NauDemoMainWebPackage` and
`NauBattlezoneProbeWebPackage`; use the respective web build directory. Release
uses the corresponding release directory/configuration. Cross-platform and
Release selections reused the exact accepted archive with `-PreparedArchive`.
The final four package directories select Battlezone.

Acceptance copies native deliveries outside the checkout and serves browser
deliveries under `/relocated/nested/application/`. Production screenshots are
captured from NauDemoMain without observer services. The separate probe observes
actual scene simulation, frame contributions and production mixer statistics;
its deterministic last-life setup still uses real enemy firing and collisions
to reach game over. No page-side game simulation or HTML HUD is used.

Checks establish a scored kill (1000 points exactly once), visible enemy
destruction, movement/turning, focus pause/recovery, game over and R restart,
resize/zero-size recovery, scene-source removal and repeated Stop. Firing and
explosion output is measured at miniaudio's actual Web Audio node; fresh-page
Space activation works without autoplay overrides. Delayed activation followed
by focus loss does not replay a shot; a later trusted gesture retries correctly.
Native WASAPI loopback captures and nonzero production mixer frames establish
audible output alongside corresponding game events.

Fault cases include missing/corrupt game JSON and firing WAV, non-finite live
vector coordinates, capacity overflow, shader creation/upload failure,
backend initialization/submission failure, Stop during graphics startup and
after Running, and browser context loss. Native cases return appropriate
nonzero status after eligible cleanup; browser cases report Failed with cleanup
complete. Successful Stop cases return/report Stopped. Shader/upload/backend
failure returns are explicitly injected acceptance hooks in real backend
resource paths. Browser context loss uses the actual WEBGL_lose_context
extension. Hardware removal or spontaneous physical GPU failures were not
induced.

Evidence: ignored `NauDemo/build/basic-rendering-scene/battlezone-*/results.json`,
production/probe/game-over PNGs, runtime/probe/failure logs and native
`output.wav`; build and acceptance command logs are under `NauDemo/build/`.

## Visual review

The reviewed opening, turned/destruction and game-over views contain outlined
tanks with barrel/turret/tracks, boxes and pyramids, green lines on black,
mountains, volcano, moon, center sight, radar, score/lives and stroke-text
controls. HUD glyphs were corrected after screenshot review. Obstacle geometry
fits its collision bounds and the tank's collision circle encloses its outline.
Parent world transforms are applied to game geometry and camera together.

Reference: https://6502disassembly.com/va-battlezone/ and its objects.html page.
The review targets composition and silhouettes rather than exact original
pixels, CRT persistence or arcade behavior. Automated screenshot gates require
more than 500 green pixels, at least 80% near-black pixels, and more than 50 green
pixels separately in HUD, battlefield and controls bands. These gates supplement
manual composition review and scene observations, not replace them. Native
client crops and browser canvas captures have different drawable dimensions;
exact pixel equality is not required.

## Focused tests and preparation

- Battlezone simulation: five tests pass in Windows and Node/WebAssembly,
  Debug and Release. They cover fixed-step/frame-rate equivalence, swept nearest
  hits/obstacle blocking, cooldown, exactly-once score, replacement, protection,
  lives/restart, cancellation and bounded elapsed time.
- Vector contract executable passes in all four configurations: near/frustum
  clipping, finite/range checks, capacity, degenerate segments, aspect/width,
  zero drawable, removal and checked overflow for extreme finite coordinates.
- Existing portable input/audio tests pass: Windows **14/14** in each
  configuration; web **11/11** in each configuration (seven input, four audio).
- Python/CMake declaration agreement tests pass for legacy click mapping,
  named effects, bad paths/names, capacity and module/profile exclusions.
- Game data validation tests pass, including invalid version, edges, vertices,
  missing required shape and occupied opening spawn.
- `verify_battlezone_freshness.py`: **12 real cooking cases pass** for repeat
  identity, geometry edit/invalid/missing/restore, sound edit/missing/corrupt/
  restore, and original/game declaration switching. Failed preparation retains
  the previously accepted archive and does not change authored inputs.
- Existing original-scene freshness: **10 cooking cases pass** with its original
  declaration and unchanged assertions.

Freshness commands:

```powershell
python NauDemo/tests/verify_battlezone_freshness.py --python C:/Users/Yakov/AppData/Local/Programs/Python/Python310/python.exe --tools D:/Programming/github/Nau/NauEditorPublic/build/latest-release/bin/Release --usd D:/Programming/github/Nau/NauEngineLite/engine/3rdparty_libs/build/openusd/install --module D:/Programming/github/Nau/NauDemo/build/portable-host-components/bin/Release/MainGameModule.dll
```

Repeat with `verify_rendering_freshness.py` for the original scene. Evidence is
under `build/basic-rendering-scene/battlezone-freshness/` and `freshness/`.

## Launchers and compatibility

- Literal `NauDemo/run_windows.bat Debug` freshly builds and presents Battlezone,
  then exits zero after closing its window. Evidence: `battlezone-launch-windows.log`
  and `battlezone-launcher.png`.
- Literal `NauDemo/run_web.bat Debug` freshly builds and serves Battlezone on
  port 8000, opens its browser tab, and provides a playable production page.
  A real-browser check on that served page reaches Running, fires and Stops.
  Its test server was stopped afterwards. Evidence: `battlezone-launch-web.log`,
  `battlezone-web-launcher.png` and `battlezone-web-launcher-runtime.log`.
- The retained original declaration preserves its prior archive hash exactly:
  `0ebf18e1db9497ea16e1aac854fa3a41133b1b5d7abc797615f0c9c6d5d582e1`.
  Its production rendering, scene rendering/failure, billboard (22 cases per
  combination), camera/input and click-audio suites pass on Windows/web in Debug
  and Release. The default game's controllers do not affect that selection.
- Eight existing target graph audits pass, including desktop dependencies and
  non-rendering/audio exclusions. Explicit additional rendering declarations
  omitting Audio configure/build/run on Windows and web in Debug, visibly
  present the original scene and stop without an audio backend. The web page
  has no miniaudio global. Evidence: `build/no-audio-evidence/` and no-audio
  configure/build logs.
- Non-rendering native/browser Debug deliveries rebuild and pass their startup,
  failure and pending-work Stop suites. Existing independent legacy startup
  defaults were not changed.
- Rebuilt common-host native and real-browser Debug suites pass **18/18 each**.
- Full desktop SceneBaseSample, CoreInput and Audio rebuild; SceneBaseSample
  presents its native UI and exits zero with `Graphics shutdown completed`.
  Evidence: `build/battlezone-legacy-run/` and legacy build logs.
- Strict OpenSpec validation and whitespace checks pass.

## Limits

This validates the existing Windows and Chrome/WebAssembly platforms. There is
no claim of arcade timing/AI accuracy, ROM emulation, original sound recordings,
missile/saucer gameplay, continuous engine audio or CRT effects. Geometry and
effects are newly authored. Native loopback includes system output; application
mixer statistics and event observations provide corresponding game evidence.
Concurrent-build capture discontinuity warnings did not change non-silent
results. Browser measurements establish output at the real audio node, without
physical-speaker calibration.
