# Validation

Validated on Windows 11 with MSVC 19.51.36260.0 / v145, CMake 4.2.1,
Emscripten 6.0.9, its Node 24.19.0 and Chrome 155.0.8059.39.
Host asset preparation used the existing OpenUSD SDK and Python 3.10;
acceptance tooling used Python 3.14, Playwright, Pillow, soundcard and NumPy.

## Source baseline

These are the committed baselines beneath the working changes, not commits
containing the new implementation:

- Root: `ab7f14b58b530d0605996537d8e5f45848376258`
- NauEngineLite: `3f1bae6a6942a0693dd9095fa32e53a5a658983a` (unchanged)
- NauEngineModules: `e9f04f8c1d442a099d2f90c28a77805dd897be9f`
- NauDemo: `8360b5d09572ad60fe2621c02e1846fb0a1a460f`

## Builds and unit tests

Windows/web Debug and Release production and acceptance packages build from
the rendering declaration through the root build helpers. The first Windows
Debug invocation cooked the assets; subsequent builds selected that archive.
Representative commands, from the checkout root:

```powershell
./NauDemo/build.ps1 -Platform Windows -Configuration Debug -Declaration portable_rendering_project.json -Acceptance
$env:EMSDK = 'C:/Users/Yakov/emsdk'
./NauDemo/build.ps1 -Platform Web -Configuration Debug -Declaration portable_rendering_project.json -PreparedArchive NauDemo/build/basic-rendering-scene/prepared-debug/content.nau_pack -Acceptance
```

The same prepared archive was selected for Release on both targets. Focused
tests were enabled with `NAU_PORTABLE_INPUT_TESTS=ON` and
`NAU_PORTABLE_AUDIO_TESTS=ON`, then built alongside the packages:

```powershell
cmake --build NauDemo/build/basic-rendering-scene/windows-debug --config Debug --target test_portable_audio test_input NauDemoMainPackage NauDemoMainAcceptancePackage --parallel 8
ctest --test-dir NauDemo/build/basic-rendering-scene/windows-debug -C Debug -R 'PortableAudio|PortableInput' --output-on-failure
```

Repeat with windows-release/Release. Native results: **14/14 per configuration**
(four audio and ten input cases). Web test executables run with the SDK's Node:
**11/11 per configuration** (four audio and seven portable input cases).
Coverage includes WAV format/range failures, real mixer output, shared PCM
lifetime, voice reclamation/stealing, bounded/cancelled pending playback,
partial cleanup, short taps, repeat suppression, stable frame epochs,
first-eligible input after startup, invalid controls and legacy gainput behavior.

## Audio acceptance

```powershell
python NauDemo/tests/verify_audio.py Windows Debug
python NauDemo/tests/verify_audio.py Windows Release
python NauDemo/tests/verify_audio.py Web Debug
python NauDemo/tests/verify_audio.py Web Release
```

All four pass with archive SHA-256:

`0ebf18e1db9497ea16e1aac854fa3a41133b1b5d7abc797615f0c9c6d5d582e1`

Native deliveries are copied outside the checkout; browser deliveries are
served under `/relocated/nested/application/`. Tests exercise all nine controls,
holds/repeats, short mouse/key taps, simultaneous controls, mouse-button chords,
bounded rapid input, unrelated keys/wheel, focus cancellation and Stop while a
voice is active. Windows also checks repeat events after focus reset.

Windows captures non-silent output from the default Realtek speaker's WASAPI
loopback into `output.wav`, together with production mixer statistics. Browser
acceptance attaches an analyser to miniaudio's actual output node and records
nonzero output, using trusted first-keyboard and first-mouse interactions in
fresh contexts. No autoplay-policy override is used.

Browser fault checks cover rejected and delayed activation, retry without a
backlog, focus loss while activation is pending, Stop with a late promise,
closed output context, unavailable context construction and partial binding
failure. Both platforms reject missing/corrupt required audio. Browser failure
checks wait for listener cleanup as well as the failure diagnostic.

Evidence: ignored `NauDemo/build/basic-rendering-scene/audio-*/results.json`,
`runtime.log`, native `output.wav`, and `NauDemo/build/audio-*.log`.

## Preparation and regressions

- `test_packaged_declaration.py`: two suites pass, including matching Python/
  CMake audio selection, invalid paths, audio without its module and audio
  settings on the non-rendering profile.
- `verify_rendering_freshness.py`: ten real cooking cases pass. Audio bytes
  match the source; repeated unchanged cooking is identical; changed audio
  changes the package; corrupt/missing audio fails without publishing a new
  archive; restoration reproduces the original archive.
- `verify_input.py`: native/browser Debug and Release pass camera movement,
  dragging, outside release, focus/visibility behavior, host loss and cleanup.
- Native/browser rendering acceptance suites pass in Debug and Release,
  including rendering/content failures and pending-work shutdown.
- `verify_production_rendering.py`: all four relocated/nested production
  deliveries show the animated scene/billboard and stop cleanly. These are the
  production deliveries selected by the existing root batch launchers; the
  underlying root build helpers were executed for this change.
- Eight CMake target graph audits pass. Audio and miniaudio stay excluded from
  no-audio profiles; browser gainput, desktop rendering, USD and Qt exclusions
  remain enforced.
- Non-rendering Windows/web Debug and Release packages rebuild and their
  startup suites pass, including failure and Stop scenarios.
- Common-host native Debug and browser Debug suites pass **18/18 each** after
  rebuilding, including lifecycle and cleanup failures.
- Full desktop `Audio`, `CoreInput` and `SceneBaseSample` rebuild. The legacy
  sample displays its live native window/UI and exits zero with
  `Graphics shutdown completed`; evidence is in `build/audio-legacy-run/`.
- Strict OpenSpec validation and whitespace checks pass.

## Limits

Audio acceptance covers the existing Windows and Chrome/WebAssembly targets.
Spatial audio, legacy emitter/container behavior, streaming and additional
operating systems are outside this change. Legacy Audio received a build
regression check; its existing spatial/container defects were not repaired or
claimed as playback validation. Native loopback records system output; request
counts and nonzero production mixer samples provide corresponding application
evidence. A capture discontinuity warning occurred under concurrent builds,
without changing the non-silent output result. Browser measurements establish
output at the production Web Audio node, not physical speaker calibration.
