# Validation

## Result

Implementation supports non-rendering browser startup of the actual EditorProject
scene and a separately authored project-component fixture. Both Debug and Release
passed 23 real-browser checks: 46 checks total. Required failures never reached
Running and eligible teardown completed. Scene observations come from a separate
C++ consumer of the production delegate and engine APIs, not page-side substitutes.

## Environment and source revisions

- Windows host; Visual Studio 2026 v145 / MSVC 19.51; CMake 4.2.1; Ninja.
- Emscripten 6.0.9, the recorded external SDK.
- Host OpenUSD 24.08, its matching Python 3.10 and recorded Nau/Adobe plugins.
- Chrome 154.0.8037.98; browser automation used the installed Playwright package.
- Baseline root `66b2fc1`; NauEngineLite `84962eaa`; NauEngineModules `b1b6386`;
  NauDemo `c191822`; NauEditorPublic `8f90bd5`. Implementation is uncommitted.
- Native tools and SDK were rebuilt from this working tree. No SDK installation
  or dependency download was performed by the browser build helpers.

## Build and preparation

From the repository root, both commands passed with provisioned machine-local
paths supplied through the documented parameters:

```powershell
./NauDemo/EditorProject/web/build.ps1 -Configuration Debug -HostSdk <native-sdk> -HostTools <native-tools/bin/Release> -UsdSdk <usd-sdk> -Acceptance
./NauDemo/EditorProject/web/build.ps1 -Configuration Release -HostSdk <native-sdk> -HostTools <native-tools/bin/Release> -UsdSdk <usd-sdk> -Acceptance
```

The native game module builds under `EditorProject/build/web-host-components`.
Separate fresh native preparation directories and browser target/delivery trees
are under the same ignored project build root. The existing editor asset database
and shader cache are not preparation inputs; authored main-scene content is unchanged.

Inspected both browser link graphs and generated static registration files:
PlatformApp, CoreAssets, CoreScene, CoreSceneFormats and MainGameModule are static.
No native SDK binaries, USD, Qt, Graphics, Render, GraphicsAssets, Animation,
Physics, PhysicsJolt, CoreInput, Audio or full CoreAssetFormats are linked.
A configure requesting Physics failed with the identifying unsupported-module
error. Missing helper prerequisites fail before configuration/build work.

`tests/verify_preparation.py`, with explicit native Python/tool/module/SDK paths,
checks clean cooking, changed authored values, changed metadata, rebuilt component
definitions, missing references, failed conversion and failed publication. It runs
in a scratch project beneath `build/`; failed invocations return nonzero and do
not publish stale outputs as a successful result. Logs and structured evidence
are `build/preparation-*.log` and `build/preparation-checks.json`.

## Browser acceptance

```powershell
python NauDemo/EditorProject/tests/verify_web_startup.py --configuration Debug
python NauDemo/EditorProject/tests/verify_web_startup.py --configuration Release
```

Each configuration passed these cases in an independent temporary directory
outside the checkout, served under `/relocated/nested/` with COOP/COEP headers:

- Actual project delivery startup, updates, repeated Stop and terminal cleanup.
- Main-scene state: all compiled identities and hierarchy retained, Xform local
  translation `(0, 0, -15)` and the mesh UID/reference preserved.
- Authored component fixture: parent translation `(1, 2, 3)` and scale `(2, 3, 4)`,
  child translation `(4, -2, 5)`, fixed component UIDs, mover axis/amplitude/frequency/
  phase, rotator axis/speed and camera data/translation verified before updates.
  Real component updates change the child's translation and rotation afterward.
- Missing configuration, scene, mesh and mesh-buffer entries.
- Corrupt configuration, database, scene and archive; missing archive.
- Unknown component and known component requiring an excluded service.
- Unresolved required asset identity.
- A scene block offset overflowing wasm32, a cyclic hierarchy and invalid numeric
  component properties.
- Stop before mounting, during genuine pending scene loading and during asynchronous
  component activation. Zero game updates, responsive page and completed cleanup
  are asserted. VFS mounting itself is synchronous; the before-mount case covers
  Stop while startup is pending before that atomic operation.
- Immediate and deferred component activation errors propagate to failed startup
  after accepted work settles, without reaching Running.

Results/history are `build/acceptance-debug.json` and `build/acceptance-release.json`;
console/test logs are the corresponding `.log` files. Test observation code and
its activation gate exist only in the separate `probe-package` consumer. Ordinary
project builds omit that executable and extra fixture packaging.

## Native and affected-consumer regressions

- Native scene probe loaded the same cooked fixture and updated actual components.
- A fixture with component type-name fields removed loaded through the shared
  reader using native legacy hashes. Opaque MissingComponent data, type name,
  numeric identity and UID remain preserved outside checked startup.
- Native EditorProject Release rebuilt against the refreshed SDK:
  `cmake --build NauDemo/EditorProject/build/release --config Release --target NauDemoMain --parallel 8`.
- Native common-host/minimal tests: all 13 CTest entries passed, including
  `MinimalRuntime.Lifecycle` and file-logging teardown.
- Browser common-host Debug: all 13 CTest scenarios passed, including pending
  startup, cleanup errors, visibility and progress deadlines.
- Native portable archive graph: all 4 CTest entries passed, including the existing
  Windows legacy reader, portable reader, builder and CLI.
- WebAssembly core Debug: all 157 underlying tests passed, including the new
  embedded in-place storage alignment regression, reflection/JSON and transforms.
- Existing demo CPU/scene/font suite: all 29 underlying Release tests passed.
- Rendered native NauDemo Release rebuilt and passed real cube rendering/rotation,
  TTF label, resize, close and missing-font cleanup checks using its existing runner
  and Orca computer inspection.
- Existing rendered NauDemo web Debug rebuilt; `web/test_package.py --scenario success`
  passed actual canvas, cube/text and terminal cleanup checks using the native font
  references generated by the CPU suite.
- Editor Release also rebuilt after the shared scene record changes. Generated
  translation edits from that build were removed; no editor source changes remain.

Regression logs and screenshots are under `EditorProject/build/regressions` and
`build/regression-*.log`. Existing common-host and archive build trees were reused
for their focused suites. Browser project binaries and preparation outputs remain
inside the consumer project; no new engine-source build directory was created.

## Compatibility decisions and limits

The approved additive `componentTypeName` field resolves the native/wasm32 hash
mismatch. Numeric component IDs use 64-bit storage, with native legacy fallback;
new browser scenes require type names. Existing container representation/version
is reused. Scene block offsets retain their full width until bounds validation.

The profile explicitly supports transform, passive camera/static-mesh data and
registered service-independent project components. It does not render, request
GPU asset views, simulate physics, play animation/audio, process input, import USD
in the browser or claim arbitrary editor-project compatibility. Passive material
and texture dependencies are retained as data. No editor export UI was added.

Memory starts at 128 MiB and grows to a bounded 512 MiB by default. Very large
projects beyond configured memory/data limits and components outside the declared
supported set are outside this milestone. Existing rendered-demo Release was not
revalidated separately; the affected rendered browser smoke used Debug, while
this project's startup acceptance covered both configurations.
