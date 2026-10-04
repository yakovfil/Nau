# Retirement validation

Validated on Windows x64, 2026-10-04. Changes are uncommitted across the six component repositories and the parent checkout. Component base revisions and SHA-256 identities of their tracked diffs and new files are recorded in `working-tree-identities.json`. The existing dirty engine googletest submodule was not edited by this change.

## Accepted validation exception

The user explicitly answered **“skip that validation”** when informed that Qt 6.4.1 and OpenUSD 24.08 were unavailable locally and the project's OpenUSD download failed TLS verification (`SEC_E_WRONG_PRINCIPAL`). Editor/USD compilation, launch, scene open/edit/save, conversion, and their regression tests are **SKIPPED**, not passed. Their source changes and test coverage are implemented and reviewed, but runtime behavior in those configurations remains unverified. No certificate verification was disabled.

The user confirmed **“I checked: scene and ImGui work”** for the relocated Release SceneBaseSample and inputDemo. Automated native text checks covered both configurations. The attempted Orca desktop capture was occluded and keyboard input returned `window_not_focused`; that capture is not visual acceptance evidence. The owned inspection process was closed through its primary window.

## Results

| Check | Result | Local evidence under `NauDemo/build/` |
| --- | --- | --- |
| Fresh native desktop/module/sample/NauDemo build, static, Debug and Release | PASS | `retire-ui-native/`, `retire-ui-debug.log`, `retire-ui-release.log` |
| Debug module/framework/kernel CTest | PASS: 586/586 | `retire-ui-ctest-debug.log` |
| Release CTest with 30-second per-test limit | 574 passed, 6 skipped, 6 existing failures; no new failure names | `retire-ui-ctest-release.log` |
| Native screen-text framebuffer/resize/failure acceptance, Debug and Release | PASS: 14 scenarios | `native-text-acceptance/results.json`, `retire-ui-native-text.log` |
| Browser scene/text/failure/lifecycle acceptance, Debug and Release | PASS: 22 scenarios | `text-browser-acceptance/results.json`, `retire-ui-text-browser.log` |
| Scene-profile CPU/source/dependency audits, native/browser, Debug/Release | PASS: four graphs plus missing-source/preset diagnostics | `demo-profile-evidence/`, `retire-ui-profile.log` |
| Native minimal lifecycle, Debug and Release | PASS: 1/1 each | `retire-ui-minimal-native-test.log`, `retire-ui-minimal-native-release-test.log` |
| Browser minimal sample success, missing-host, host-loss, Debug and Release | PASS: all six fixtures; failure scenarios correctly fail runtime while passing acceptance | `retire-ui-minimal-web-test.log`, `retire-ui-minimal-web-{missing-host,host-loss}.log`, `retire-ui-minimal-web-release-{success,missing-host,host-loss}.log` |
| External sample discovery/profile/missing-input regression | PASS | `python NauSamples/tests/test_external_samples.py` |
| Fresh SDK install and relocation, Debug and Release | PASS: 2,986 files; no retired artifacts | `retire-ui-sdk-clean/`, `retire-ui-sdk-relocated/`, `retire-ui-audit.json` |
| Installed SceneBaseSample/inputDemo rebuild, Debug/Release | PASS | `retire-ui-sdk-sample-{Debug,Release}-build.log` |
| Generated empty template build/startup, Debug/Release | PASS | `retire-ui-template-{config,build,debug-build}.log`, `retire-ui-consumer/StdSdkConsumer/` |
| Relocated samples/template resize, inputDemo secondary-first close, normal shutdown | PASS: six final launches, all exit zero | `retire-ui-sdk-final-check/results.json`, `retire-ui-sdk-final-check.log` |
| Remaining native scene/ImGui visual output | User-confirmed, Release | Confirmation quoted above |
| Editor/USD build/runtime/regression tests | SKIPPED by user request | Exception above |
| Working-tree whitespace and Python syntax | PASS | `git diff --check` in changed components; `python -m py_compile` on changed runners |
| Strict OpenSpec validation | PASS | `openspec validate retire-cocos-ui --strict` |

The six Release failure names exactly match `NauEngineLite/cmake/probes/windows_toolchain/failed-tests-release.txt`: `TestSpinLock.MultipleSubsequentLockMustFail` (timeout), `TestSpinLock.DestructWhileLockedMustFail`, `TestRecursiveSpinLock.DestructWhileLockedMustFail`, `TestAssetPath.ConstructFromInvalidString`, `TestAssetPath.SetScheme`, and `TestAssetPath.SetContainerPath`. These checks remain failed; they were neither fixed nor counted as passes. Native framebuffer logs also retain the previously recorded DX12 pipeline/resource validation diagnostics; successful pixel and shutdown checks do not imply diagnostic-free rendering.

## Source, graph, and install audit

Tracked inventories contain no `modules/ui`, bundled Cocos, USD `ui_translator`/`gui_schema`, GUI editor/synchronizer, UiSampleApp, template UI shaders, or widget `gui_content`. Application framework state/update/link integration and Graphics UI rendering/link integration are removed. The renamed ScreenTextStage retains text rendering before ImGui. PNG/compression/hashing and other shared dependencies with remaining consumers are retained.

Native CMake File API inventories contain 100 targets and 3,297 source/header entries per configuration, including NauFramework, Graphics, NauScreenText, SceneBaseSample, and inputDemo, and no retired targets or inputs. Installed sample and template graphs contain 13 and 4 targets respectively, with no NauEngineLite/NauEngineModules/NauSamples checkout paths in their configured target data. The active scene-profile source manifest also no longer lists the deleted UI accessor.

The shared editor `NauUsdSceneUITranslator` forwards ordinary USD scene notices to Qt inspectors/outliners and remains necessary for scene editing; it is not the deleted Cocos widget translator. Legacy UI metadata/type recognition remains solely for unsupported diagnostics. Three AssetTools regression cases and one editor integration case cover rejection, authored-type recognition without the GUI plugin, unchanged source bytes/no output, and continued ordinary access. Their execution is skipped under the explicit exception above.

An install iteration exposed ignored generated resources remaining under the deleted source sample directory. Sample installation now explicitly excludes `uiSampleApp`, preventing those stale local files from being packaged. Final evidence uses a new clean install and rebuilt relocated consumers, not the earlier contaminated SDK. SDK/template imports now include NauScreenText and omit Cocos-exclusive imported targets. Template SDK variable handling and the installed check-script path were corrected to make the relocated template build succeed.

## Reproduction

Run from the parent Nau checkout. Native requirements: VS 18/2026 x64 v145, CMake 4.2, and the bootstrapped vcpkg toolchain. Browser requirements: the installed Emscripten environment, Chrome, Playwright, and Pillow.

```powershell
cmake -S NauEngineLite -B NauDemo/build/retire-ui-native -G "Visual Studio 18 2026" -A x64 -T v145,host=x64 -DBUILD_SHARED_LIBS=OFF -DNAU_CORE_TESTS=ON -DNAU_DEMO_TEST_HOOKS=ON -DNAU_BUILD_SDK=ON -DCMAKE_TOOLCHAIN_FILE=D:/Programming/vcpkg/scripts/buildsystems/vcpkg.cmake -DCMAKE_PROJECT_NauEngine_INCLUDE=D:/Programming/github/Nau/NauDemo/cmake/attach_demo.cmake -DCMAKE_INSTALL_PREFIX=D:/Programming/github/Nau/NauDemo/build/retire-ui-sdk-clean
cmake --build NauDemo/build/retire-ui-native --config Debug --parallel 8
cmake --build NauDemo/build/retire-ui-native --config Release --parallel 8
ctest --test-dir NauDemo/build/retire-ui-native -C Debug --timeout 30 --output-on-failure
ctest --test-dir NauDemo/build/retire-ui-native -C Release --timeout 30 --output-on-failure
python NauDemo/tests/test_native_text.py

. "$env:USERPROFILE/emsdk/emsdk_env.ps1"
NauDemo/web/build.ps1 -Configuration Debug -TestHooks
NauDemo/web/build.ps1 -Configuration Release -TestHooks
python NauDemo/web/test_text_acceptance.py
python NauDemo/web/test_demo_profile.py
python NauSamples/tests/test_external_samples.py

cmake --install NauDemo/build/retire-ui-native --config Debug
cmake --install NauDemo/build/retire-ui-native --config Release
python NauSamples/tests/sdk_shutdown/run.py --sdk NauDemo/build/retire-ui-sdk-relocated --consumer NauDemo/build/retire-ui-consumer/StdSdkConsumer --repetitions 1 --resize-primary --close-secondary-first --output NauDemo/build/retire-ui-sdk-final-check
openspec validate retire-cocos-ui --strict
```

Browser packages must be built with `-TestHooks` for framebuffer readback and pending-scene acceptance. An initial readback timeout came from testing packages without those hooks; rebuilding the correct acceptance packages resolved it. The runner now records state on failure and bounds owned-Chrome cleanup without masking the original exception. The obsolete packages/setup failures are not counted as successful checks. Minimal build roots, generated template sources, and additional configure/install/audit logs are retained in ignored `NauDemo/build/` outputs.
