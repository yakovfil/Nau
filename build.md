# Building the Engine and Editor

These instructions cover Windows x64 builds of `NauEngineLite` and `NauEditorPublic` using Visual Studio 2026 and PowerShell, plus the Emscripten toolchain checks below. Run commands one at a time and continue only after each succeeds. The repository root has no CMake project; configure each component separately. See [prerequisites.md](prerequisites.md) for required tools, exact SDK versions, installation status and remaining source prerequisites.

## Standard-library migration

The engine, editor, samples and demo use the selected C++20 toolchain standard library. EASTL is not an active source, SDK, or build dependency; old EASTL-based binaries are not ABI-compatible with the migrated interfaces. EABase was also removed after the independent consumer audit found no remaining active use. Nau adapters retain the required frame, stack, pool, aligned, inline, sorted, bit, intrusive and bounded-callback contracts where the standard library alone is insufficient.

After changing the migration, configure each affected component into a fresh build directory and rebuild all engine, editor, sample, and demo consumers with the same toolchain and configuration. Do not mix pre-migration libraries with migrated headers or Debug/Release artifacts. The standard migration matrix uses these roots:

```powershell
# From NauEngineLite
cmake --preset win_vs2026_x64 -B build/replace-eastl-msvc-static
cmake --build build/replace-eastl-msvc-static --config Debug
cmake --build build/replace-eastl-msvc-static --config Release

cmake --preset win_vs2026_x64_dll -B build/replace-eastl-msvc-dll
cmake --build build/replace-eastl-msvc-dll --config Debug
cmake --build build/replace-eastl-msvc-dll --config Release
```

If a DLL configure cannot download the recorded USD archive because of a transient network or certificate failure, pass `-DFETCHCONTENT_SOURCE_DIR_USD=<path-to-usd24.08-root>` to use an already provisioned local package. The path must contain `pxrConfig.cmake`; do not disable certificate verification or reuse an incomplete download directory. The same source/ABI rule applies to the editor, generated projects, and installed SDK samples. Use the component-specific commands below, and do not copy build outputs or CMake caches from a pre-migration tree. Exact results, exclusions, compiler identities, and remaining acceptance boundaries are recorded in [the migration validation record](openspec/changes/archive/2026-10-03-replace-eastl-with-std/validation.md).

## 1. Install prerequisites

Install the following before configuring either project:

| Dependency | Required setup |
| --- | --- |
| Visual Studio 2026 | Desktop development with C++, MSVC v145, and Windows 10 SDK. |
| CMake | CMake 4.2 or newer for the Visual Studio 18 2026 generator. Browser requirements remain separate. |
| Git | Available on `PATH`, with recursive submodule support. |
| Python | Python 3.10 with pip on `PATH`, matching the version documented by this project. The downloaded USD package also contains its own Python 3.10 runtime. |
| vcpkg | A bootstrapped checkout outside this repository; setup below. |
| Qt (editor only) | The project's documented Qt 6.4.1 MSVC x64 distribution, including Debug libraries, Linguist tools, and SVG support. |

Use **Developer PowerShell for VS 2026** with the x64 toolchain. Prefer a short local checkout path without Cyrillic characters or cloud synchronization.

Verify the command-line tools and install the Python packages checked by CMake:

```powershell
git --version
cmake --version
py -3.10 --version
py -3.10 -m pip install cymbal==1.0.0 clang==21.1.7
$nauPython = py -3.10 -c 'import sys; print(sys.prefix)'
$env:PATH = "$nauPython;$nauPython/Scripts;$env:PATH"
python --version
pip show cymbal clang
```

The build explicitly invokes `pip`, so it must refer to the Python installation where those packages were installed. Use `Get-Command python,pip` to inspect their locations.

### Set up vcpkg

For a new vcpkg installation:

```powershell
New-Item -ItemType Directory -Force C:/Tools
git clone https://github.com/microsoft/vcpkg C:/Tools/vcpkg
& C:/Tools/vcpkg/bootstrap-vcpkg.bat
$env:VCPKG_ROOT = 'C:/Tools/vcpkg'
Test-Path "$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"
```

If vcpkg already exists, reuse its checkout and set `VCPKG_ROOT` accordingly. This variable points to the **vcpkg directory**, not its parent. The assignment applies to the current shell; optionally persist it for future shells:

```powershell
[Environment]::SetEnvironmentVariable('VCPKG_ROOT', $env:VCPKG_ROOT, 'User')
```

Both projects have `vcpkg.json` manifests with a pinned baseline and dependencies on protobuf and DirectX DXC. Configuration uses the vcpkg toolchain to resolve them; the initial run needs network access and may take substantially longer than subsequent runs.

## 2. Initialize the source checkout

Start in the directory containing this file. Keep this PowerShell session open; later examples reuse `$nauRepo`.

```powershell
$nauRepo = (Get-Location).Path.Replace('\', '/')
git submodule update --init --recursive
git submodule status --recursive
$env:NAU_ENGINE_SOURCE_DIR = Join-Path $nauRepo 'NauEngineLite'
```

The expected layout is:

```text
Nau/
  build.md
  NauEngineLite/
  NauEngineModules/
  NauSamples/
  NauEditorPublic/
  NauDocsPublic/
```

Use the submodule revisions recorded by the parent repository for a consistent checkout. Preserve any local component changes before changing revisions.

## 3. Build the standalone engine

### Configure and compile

The standard engine preset builds a static/monolithic runtime, with tools, samples, and core tests enabled by default.

```powershell
Set-Location (Join-Path $nauRepo 'NauEngineLite')
cmake --list-presets
cmake --preset win_vs2026_x64
cmake --build build/win_vs2026_x64 --config Debug
```

The equivalent build-preset command is `cmake --build --preset "VS Debug"`. For an optimized build, use:

```powershell
cmake --build build/win_vs2026_x64 --config Release
```

Visual Studio presets support multiple configurations in one build directory. Supply `--config` when building and `-C` when testing. Most engine executables are placed in `build/win_vs2026_x64/bin/Debug/`, with libraries under `lib/`.

For IDE development, open `build/win_vs2026_x64/NauEngine.sln`, select Debug or Release and x64, and build `ALL_BUILD`. To run an example, select an executable sample such as `MinimalAppSample` as the startup project.

### Run engine tests

```powershell
ctest --test-dir build/win_vs2026_x64 -C Debug -N
ctest --test-dir build/win_vs2026_x64 -C Debug --output-on-failure
```

The first command lists registered tests; the second executes them. Add `-R '<regex>'` to select test names. Tests require `NAU_CORE_TESTS=ON` and must be compiled first. Use these portable commands instead of the absolute paths in the checked-in `run_tests.bat`.

### Install the engine SDK

After a successful build:

```powershell
cmake --install build/win_vs2026_x64 --config Debug
```

The engine's `CMakeLists.txt` forces the install prefix to `NauEngineLite/output/`, overriding the preset's `dist/` default. The installed tree includes a separate CMake project; the engine README describes configuring and building that tree when preparing the SDK. Installation is not required to configure the editor against engine sources.

### Optional engine configurations

For a DLL engine, including USD-dependent tools:

```powershell
cmake --preset win_vs2026_x64_dll -A x64
cmake --build build/win_vs2026_x64_dll --config Debug
ctest --test-dir build/win_vs2026_x64_dll -C Debug --output-on-failure
```

The DLL configuration downloads the project's OpenUSD 24.08 archive automatically through `cmake/defaults/UsdPackages.cmake`.

To omit standalone engine tests or samples, reconfigure with `-DNAU_CORE_TESTS=OFF` or `-DNAU_CORE_SAMPLES=OFF`. Keep the defaults for the initial build. These options do not provide an equivalent way to disable editor requirements: the editor explicitly enables engine tools and samples and disables engine core tests in its own build.

## 4. Build the editor

### Prepare Qt

The checked-in [installation documentation](NauDocsPublic/source/beta/user-doc/introduction_to_nau/install_nau/install_nau_doc.rst) identifies Qt 6.4.1 and provides the project's distribution location. Extract that package and locate its `msvc2019_64` directory. This is the Qt prefix, containing `bin/` and `lib/cmake/Qt6/`.

Set the actual path for your machine:

```powershell
$nauQt = 'C:/path/to/Qt/6.4.1/msvc2019_64' # Replace with your Qt SDK location.
Test-Path "$nauQt/lib/cmake/Qt6/Qt6Config.cmake"
Test-Path "$nauQt/bin/windeployqt.exe"
```

Both checks should return `True`. The editor requires Qt Core, Widgets, Network, Test, OpenGL, LinguistTools, and Svg. Its vcpkg manifest does not install Qt. The documentation also lists Qt Visual Studio Tools for IDE integration; the commands below use CMake directly.

Prepare the Qt 6.4.1 headers for MSVC 14.51 before configuring:

```powershell
py -3.10 "$nauRepo/NauEditorPublic/scripts/prepare_qt_for_msvc.py" "$nauQt"
```

This reproducible upstream backport removes references to retired STL iterator helpers. It preserves the Qt binaries and backs up the original header; see the [preparation instructions](NauEditorPublic/scripts/README.md).

### Build the local OpenUSD SDK

The validated Release route builds OpenUSD 24.08 and Adobe's required
`usdGltf_plugin` from the pinned engine submodules. With the prerequisites and
submodules above initialized:

```powershell
py -3.10 -m pip install Jinja2==3.1.6
& "$nauRepo/NauEngineLite/cmake/build_openusd.ps1" -Jobs 8
$nauUsdSdk = "$nauRepo/NauEngineLite/engine/3rdparty_libs/build/openusd/install"
```

The helper also builds the glTF plugin's dependencies as static libraries with
the dynamic CRT, avoiding conflicts with the engine's `fmt.dll`. If the core
SDK is already built, add the plugin with
`& "$nauRepo/NauEngineLite/cmake/build_usd_gltf.ps1" -Jobs 8`.
Source URLs, pinned revisions and output paths are in the
[local SDK guide](NauEngineLite/doc/openusd.md).

### Configure against the engine and modules sources

```powershell
Set-Location (Join-Path $nauRepo 'NauEditorPublic')
cmake --preset win_vs2026_x64_dll -B build/latest-release `
  "-DNAU_ROOT_DIR=$nauRepo/NauEngineLite" `
  "-DNAU_MODULES_SOURCE_DIR=$nauRepo/NauEngineModules" `
  "-DNAU_SAMPLES_SOURCE_DIR=$nauRepo/NauSamples" `
  "-DCMAKE_PROJECT_NauEngine_INCLUDE=$nauRepo/NauEngineModules/cmake/attach_modules.cmake" `
  "-DNAU_EXTERNAL_PROJECT_DIRS=$nauRepo/NauEngineModules;$nauRepo/NauSamples" `
  "-DNAU_USD_SDK_DIR=$nauUsdSdk" `
  "-DCMAKE_PREFIX_PATH=$nauQt"
```

Use the DLL preset: the editor's USD plugin targets require `BUILD_SHARED_LIBS`.
`NAU_ROOT_DIR` points to the engine sources, not its build or installed SDK.
The editor compiles the engine, modules and required sample resources within its
own build tree; a standalone engine build is not required.

`NAU_USD_SDK_DIR` selects the locally built SDK layout. Omitting it retains the
legacy downloaded archive route. `pxr_DIR` alone does not select the local SDK.
The helper produces a Release SDK; Debug requires a matching SDK and separate
validation. Do not build Debug against these Release-only dependencies.

### Compile, verify and launch

Close running instances from the output directory before building, since they
lock runtime DLLs during deployment.

```powershell
cmake --build build/latest-release --config Release --target NauEditor --parallel 8
$nauEditorDir = (Resolve-Path build/latest-release/Release/NauEditor).Path
py -3.10 "$nauRepo/NauEngineLite/cmake/usd_gltf/check_plugin.py" $nauUsdSdk --deployment $nauEditorDir
Start-Process -FilePath "$nauEditorDir/NauEditor.exe" -WorkingDirectory $nauEditorDir
```

The plugin check must report successful `.gltf` and `.glb` triangle imports.
The build deploys Qt, engine/USD libraries, plugins and project templates beside
the executable. Keep that complete folder together. `--target NauEditor` avoids
requesting installer packaging.

The Release build, both deployed import checks, loading all nine required USD
plugins and startup to the responsive project browser passed on 2026-10-06.
Full project editing, editor test suites and installer packaging were not part
of that validation. See the [editor README](NauEditorPublic/README.md#release-with-the-locally-built-openusd-sdk)
for the complete standalone command sequence and missing-plugin/DLL troubleshooting.

### Build and run editor tests

```powershell
$nauEditorBuild = (Resolve-Path build/latest-release).Path
$env:PATH = "$nauQt/bin;$nauEditorBuild/bin/Release;$env:PATH"
cmake --build build/latest-release --config Release --target NauEditorUnitTests NauEditorUiTests
& ./build/latest-release/Release/NauEditorUnitTests/NauEditorUnitTests.exe
& ./build/latest-release/Release/NauEditorUiTests/NauEditorUiTests.exe
```

Unit tests use Google Test discovery. The Qt UI test executable is not registered with CTest in its current CMake file, so run it separately in an interactive desktop session. Run standalone engine tests from the engine build tree, since the editor disables those suites.

The commands run the configuration's unit binary directly and should report 64 tests. An exit code of zero with zero tests is not acceptance. The four deferred Release death tests are listed in `scripts/failed-tests-release.txt` and the root `failed-tests.md`; to apply only those exclusions, pass `"--gtest_filter=-$((Get-Content scripts/failed-tests-release.txt) -join ':')"` to the Release unit binary.

Set PATH before building because discovery runs the test executable during the build. For a separately provisioned Debug build, change the build directory, configuration and runtime PATH together.

### Optional installer packaging

A default editor build, including `ALL_BUILD`, also runs the `Installer` target. This packaging route was not validated with the local Release SDK. To request packaging explicitly:

```powershell
cmake --build build/latest-release --config Release --target Installer
```

The scripts additionally build/install an engine SDK, copy it into the editor distribution, download redistributables, and use NSIS. They may install NSIS and its plugin with an elevation prompt. Expected output is `build/latest-release/Release/Installer.exe`. Inspect the packaging output as well as the exit status: the SDK helper currently resets one returned build status before proceeding. Use `--target NauEditor` when only developing the application.

## 5. Troubleshooting and rebuilding

| Symptom | Action |
| --- | --- |
| Cannot read presets | Run from the component directory and use CMake with schema version 5 support. |
| Missing compiler or Windows SDK | Install the listed VS components and reopen the x64 Developer PowerShell. |
| vcpkg toolchain missing | Verify `VCPKG_ROOT` and the toolchain `Test-Path` check before configuring. |
| Missing `cymbal` or `clang` | Check `pip show` and `Get-Command python,pip`; CMake invokes bare `pip`. |
| Qt6 package or component missing | Check the Qt prefix and installed modules; select the MSVC x64 package with the requested configuration's libraries. |
| USD download/schema generation fails | Inspect configure output, network access, and the downloaded package's bundled Python/files. Use the FetchContent override above for a complete local archive. |
| Editor cannot find engine sources | Pass an absolute `NAU_ROOT_DIR` explicitly. A variable persisted by the engine's setup script may not be visible in the current shell. |
| DLL or Qt plugin missing at launch | Finish the editor post-build deployment, retain its output directory, and try launching through the generated VS solution. |
| Installer failure during a default build | Build `NauEditor` explicitly for development, or resolve the SDK/NSIS error for packaging. |
| Generator, architecture, or dependency cache mismatch | Configure into a new build directory using `-B build/<new-name>` and use that directory for subsequent build/test commands. |

After ordinary source edits, rerun the relevant build command. After manifest or toolchain changes, prefer a fresh build directory. Avoid broad `git clean -d -x -f` cleanup: it removes untracked and ignored work as well as build artifacts.

Configuration and builds can update source-tree files, including `run_tests.bat`, translations, and shader caches. Inspect `git status` within both components before committing.

## 6. Emscripten setup and capability checks

On 2026-09-19, external emsdk **6.0.9** and Ninja **1.13.2** were installed. CMake
**4.2.1** was retained. The SDK includes Node **24.19.0** and Python **3.13.3**.
The exact pin is stored in `NauEngineLite/cmake/emscripten-sdk-version.txt`.
It passes toolchain probes, production Wasm core tests and focused production
browser platform and actual minimal sample tests. Runtime packaging and delivery remain pending.

For this machine, emsdk is installed at `$HOME/emsdk`. Reopen PowerShell to pick
up Ninja's PATH entry. Starting at the repository root:

```powershell
. "$HOME/emsdk/emsdk_env.ps1"
Set-Location NauEngineLite
./cmake/check_emscripten.ps1
./cmake/check_emscripten.ps1 -Probe -Configuration Debug
./cmake/check_emscripten.ps1 -Probe -Configuration Release
python cmake/probes/emscripten/test_preflight.py
python cmake/probes/emscripten/test_platform_options.py
```

The probes use separate `build/emscripten-probe-debug` and
`build/emscripten-probe-release` directories. Both compile and link C++20
coroutines and pthreads, producing `.js` and `.wasm` files. They do not build or
run Nau. Seven preflight checks passed, including missing/mismatched SDK,
missing SDK files, direct CMake rejection and native compiler-cache rejection.
SDK activation metadata remained unchanged during those checks.

See the sample [Emscripten guide](NauSamples/doc/emscripten_build.md) for
fresh installation commands, exact tool versions and the delivery boundary.
The shared minimal framework now passes native Debug/Release lifecycle tests.
Browser platform services and the actual sample pass Chrome tests. Use the browser
sample build commands below; staged packages and relocation are covered there.

Browser presets `web-minimal-debug` and `web-minimal-release` now exist with
matching build presets, isolated Ninja caches, and separate `bin`/`lib` paths.
Both presets configure and build the actual `MinimalAppSample`. Its production
minimal graph excludes desktop dependencies. The platform checks also retain
standalone option checks using bundled `xxHash`; sample graph and Chrome checks
are documented in the [sample guide](NauSamples/doc/minimal_app_web.md).

The existing desktop `win_vs2022_x64` preset also configured successfully before
and after the platform changes, without an active emsdk. Its preset definitions
and 36 selected compiler/cache settings matched; the browser checks left its
original native cache unchanged. Full engine/editor compilation remains unverified.

The approved one-line bundled `fmt` fix resolves its C++20 consteval failure with
SDK 6.0.9. Run `python cmake/probes/emscripten/test_fmt_compatibility.py` from the
engine directory to reproduce Debug/Release builds, Node runtime formatting and
invalid-format compile rejection. Native `fmt` library builds also pass in both
configurations; see the [compatibility record](NauEngineLite/doc/fmt_emscripten_compatibility.md).

VS 2022 C++ Build Tools **17.14.41**, Python **3.10.11**, `cymbal==1.0.0` and
`clang==21.1.7` were also installed for native validation. A separate native C++20
smoke test configured, built and ran with MSVC **19.44.35229.0** and Windows SDK
**10.0.26100.0**, without an active emsdk. This does not establish full desktop
engine/editor build success. Existing vcpkg was reused and user `VCPKG_ROOT` set
to `D:/Programming/vcpkg`; new shells inherit it. No dependency revisions were
updated.

## 7. Native minimal runtime

The non-rendering profile is implemented. From `NauEngineLite`:

```powershell
cmake --preset native-minimal-debug
cmake --build --preset native-minimal-debug
ctest --test-dir build/native-minimal-debug -C Debug --output-on-failure
cmake --preset native-minimal-release
cmake --build --preset native-minimal-release
ctest --test-dir build/native-minimal-release -C Release --output-on-failure
```

Both configurations build the real kernel, `NauFrameworkMinimal`, `PlatformApp`,
sample and focused lifecycle suite. Both configurations pass 19 Google Tests,
including real platform startup, five pre/post updates, orderly shutdown,
service initialization failures, partial cleanup, shutdown/disposal errors,
dependency order, initialization proxies, checked application creation/startup,
Stop during startup and pending cleanup without duplicate disposal. The native
kernel source-selection error is fixed, and the scene cleanup regression plus
11 existing scene update/deactivation tests pass in Debug and Release.
The independent browser application lifecycle is also implemented; see the
[validation record](openspec/changes/browser-runtime-lifecycle/validation.md).
This profile uses bundled
sources without vcpkg, Qt, USD or Python generator packages. See the
[profile guide](NauSamples/doc/minimal_runtime_profile.md) for dependency lists,
graph checks and validation limits. Affected desktop `NauFramework` and
`PlatformApp` Debug libraries also compile with dependency project builds skipped;
a full desktop application build remains unverified.

## Reference and validation scope

The `wasm-core-portability` milestone now passes focused tests with the production
kernel in isolated native and Wasm Debug/Release directories. It also compiles
all eight shared minimal-framework sources. Use the
[core build guide](NauEngineLite/doc/wasm_core_portability.md) for the exact CMake
commands and graph/failure audits; these remain independent of the browser
application presets. Required dependencies are listed in
[prerequisites.md](prerequisites.md).

Validation includes 27 Wasm tests under activated SDK Node 24.19.0, fatal diagnostic
exit checks, 26 native core tests, and the real native minimal lifecycle in both
configurations. The approved malformed-UTF behavior is diagnostic plus empty
result on Wasm, with no partial conversion. Native checked conversion behavior
is retained. Browser platform services and the real application lifecycle pass
the focused Chrome suites described below. The actual sample/preset integration
also passes; packages and Chrome relocation tests remain pending.

## Browser platform build and validation

From `NauEngineLite`, install the test runner with
`python -m pip install playwright==1.63.0` and load the activated SDK environment.
The [platform guide](NauEngineLite/doc/browser_platform_services.md) contains the
complete Debug/Release configure, build and CTest commands, host contract and
shutdown behavior. Required tools and exact tested versions are listed in
[prerequisites.md](prerequisites.md).

The independent build entry point is `cmake/probes/browser_platform`, with outputs
in `build/browser-platform-debug` and `build/browser-platform-release`. Both pass
8/8 Chrome cases using real production static module registration and the shared
platform service. Coverage includes DOM geometry/visibility, initialization errors,
worker dispatch, bounded pumping, host removal and disposal. The test server uses
isolation headers and a temporary Chrome profile; it is not a relocatable app package.

For desktop CMake regeneration, put the installed Python 3.10 directory and its
`Scripts` directory first on PATH: the existing package checks invoke `pip`
directly. With that environment, the affected desktop framework/platform Debug
libraries compile. The approved kernel source-selection fix also allows the full
`test_scene` dependency build in Debug and Release; 12 affected scene tests pass
in each. A complete desktop application build remains unverified.

## Browser application lifecycle build and validation

Use the [lifecycle guide](NauEngineLite/doc/browser_runtime_lifecycle.md) for the
complete PowerShell configure/build/test commands. Its independent entry point
is `NauEngineLite/cmake/probes/browser_runtime`, with Debug/Release outputs under
`build/browser-runtime-debug` and `build/browser-runtime-release`. Configure with
the activated SDK 6.0.9 toolchain and explicitly select the Python interpreter
containing Playwright using `-DPython3_EXECUTABLE=<absolute-python-path>`.

The real application worker and production static PlatformApp supply ordered
status, completed-step counts, asynchronous Stop, checked startup failures,
cleanup and reload-to-retry behavior. Thirteen Chrome cases per configuration
include five-second 8–12 Hz acceptance, UI heartbeat, real tab hide/show, pending
work, host loss and isolated negative fixtures. Deterministic timing tests run
in the 19-test native lifecycle suite. See the [scenario evidence](openspec/changes/browser-runtime-lifecycle/validation.md).

The sample project consumes this lifecycle through `web-minimal-*`. From
the repository root with the SDK active:

```powershell
./NauSamples/build_minimal.ps1 -Platform Web -Configuration Debug
./NauSamples/build_minimal.ps1 -Platform Web -Configuration Release
python NauSamples/tests/minimal_app_web/run.py --build NauEngineLite/build/web-minimal-debug --scenario success
python NauSamples/tests/minimal_app_web/run.py --build NauEngineLite/build/web-minimal-release --scenario success
```

Use Python with Playwright installed for the runner. Both sample configurations
pass success, missing-host, host-loss and intentional runner-failure checks.
Foreground rates measured 9.7830 Hz Debug / 9.7711 Hz Release. The
[sample guide](NauSamples/doc/minimal_app_web.md) covers all scenarios and
[validation evidence](openspec/changes/minimal-app-web/validation.md) records graph
and regression results. Outputs are `bin/MinimalAppSample.js` and `.wasm` in each
preset build directory; no separate worker script was emitted by SDK 6.0.9.
Default browser builds now stage `package/` in each preset directory. Run
`python build/web-minimal-debug/package/serve.py --port 8000` from the engine
directory (or use the Release path), then open the printed URL. Copy the entire
folder to serve elsewhere; `--base-path /relocated/nau/` supports nested URLs.
The [delivery guide](NauSamples/doc/minimal_web_delivery.md) covers controls,
failure diagnostics and acceptance. Serving needs Python 3.9+ and Chrome only;
Playwright and the SDK are not serving dependencies. The page checks isolation
before loading runtime files, exposes real status/Stop/cleanup, and requires
reload to retry. The sample extraction walkthrough validates fresh local
checkouts of the engine, samples and demo with the recorded SDK setup.

These instructions were checked against the component `CMakePresets.json` files,
engine and editor CMake targets, installer scripts, and local installation
documentation. Both configure-preset lists were successfully read with CMake.
Validation performed for the Emscripten update is listed above. Full engine/editor
compilation, test execution, and installer generation remain
unverified.


## NauDemo Windows and browser builds

NauDemo is the editor-created project at the root of its submodule. From
`NauDemo/`, use `run_windows.bat [Debug|Release]` or
`run_web.bat [Debug|Release]` to build and launch the shared rendering scene.
Web activates Emscripten SDK 6.0.9 through `EMSDK` or the default user installation.

For build-only runs, activate Emscripten first for Web:

```powershell
./NauDemo/build.ps1 -Platform Windows -Configuration Debug -Declaration ./portable_rendering_project.json
./NauDemo/web/build.ps1 -Configuration Debug -Declaration ./portable_rendering_project.json
```

Both use the shared packaged-project workflow and native asset preparation.
The `NauDemoMain` deliveries are under
`NauDemo/build/basic-rendering-scene/{windows,web}-{debug,release}/package`.
Copy the entire package for relocation; source assets and the host SDK/USD are
not needed at runtime. See [NauDemo build instructions](NauDemo/web/README.md)
for overrides, serving, prerequisite discovery and visual acceptance checks.

## External samples checkout

All engine samples now live in the sibling `NauSamples` submodule. From this repository root run `git submodule update --init NauSamples` before configuring native samples or the minimal browser app. Sample target names remain unchanged; Windows presets now use `win_vs2026_x64*`. The engine presets configure the engine alone. Use `NauSamples/cmake/attach_samples.cmake` through `CMAKE_PROJECT_NauEngine_INCLUDE` to add samples; `NauSamples/build_minimal.ps1` does this for the minimal profiles. Pass `"-DNAU_SAMPLES_SOURCE_DIR=<absolute path>"` for another location.

Use a clean configuration after moving from engine-local samples. NauDemo uses its own project content and shared module build integration; it does not require the sample checkout. Engine-only configurations without sample consumers do not require it either. Installed SDKs continue to contain a `samples/` directory. See [external sample integration](NauSamples/doc/external_samples.md) for paths, SDK behavior and component publication order.

## VS 2026 migration

Native MSVC builds now require VS 2026 C++ tools, v145 and CMake 4.2+. Replace `win_vs2022_x64`, `_dll` and `_dll_asan` with their `win_vs2026_x64` counterparts. Configure fresh build directories; do not retarget an old CMake cache. For the unchanged `native-minimal-debug` and `native-minimal-release` names, use `-B build/native-minimal-vs2026-debug` or `-B build/native-minimal-vs2026-release`, and pass those paths to build/CTest. VS 2022 can remain installed, but is no longer a supported compiler selection.

Existing Qt/USD package names may describe older producer compilers; do not rename their paths to match the new preset. Qt 6.4.1 requires the preparation step above for MSVC 14.51. Native minimal Debug/Release lifecycle tests, full static Debug/Release builds, and all six source-build scene/input/demo visual checks pass with MSVC 19.51.36257.0 and Windows SDK 10.0.26100.0. Release test exclusions and relocated SDK shutdown findings are recorded in [failed-tests.md](failed-tests.md). Editor and other compiler acceptance remain tracked in the [current validation record](openspec/changes/archive/2026-09-21-windows-msvc-2026/validation.md). Earlier validation records above refer to the tools originally tested.

The retained Ninja/clang-cl route uses VS 2026's LLVM 22.1.3. This compiler version is separate from the Python `clang==21.1.7` bindings used by generators. Its recorded USD/TBB and Google Test headers require the [clang-cl dependency preparation](NauEngineLite/cmake/probes/windows_toolchain/README.md). From a VS 2026 x64 developer prompt with LLVM, Python 3.10 and its Scripts directory on PATH:

```powershell
# From NauEngineLite; choose your existing USD 24.08 package root.
$nauUsd = 'C:/Tools/usd24.08'
cmake --preset win_ninja_clangcl-debug -B build/clang-vs2026-static
cmake --preset win_ninja_clangcl-debug_dll -B build/clang-vs2026-dll "-DFETCHCONTENT_SOURCE_DIR_USD=$nauUsd"
python cmake/probes/windows_toolchain/prepare_clang_dependencies.py --usd-root "$nauUsd" --googletest-root engine/3rdparty_libs/googletest
cmake --build build/clang-vs2026-static --target NauKernel SceneBaseSample test_runtime -j 4
cmake --build build/clang-vs2026-dll --target NauKernel test_runtime -j 4
ctest --test-dir build/clang-vs2026-static/engine/core/kernel/tests/test_runtime --timeout 15 --output-on-failure --exclude-from-file "$PWD/cmake/probes/windows_toolchain/failed-tests-clang-debug.txt"
ctest --test-dir build/clang-vs2026-dll/engine/core/kernel/tests/test_runtime --timeout 15 --output-on-failure --exclude-from-file "$PWD/cmake/probes/windows_toolchain/failed-tests-clang-dll-debug.txt"
```

The exclusions record the observed `WhenAll_NoTimeout` illegal-instruction failure and, only on the DLL route, three legacy allocator failures whose test names remain in the historical failure ledger. These are deferred tests, not compiler or runtime fixes; see [failed-tests.md](failed-tests.md). Dependency preparation preserves backups and rejects unrecognized headers. It does not change the USD/Qt/TBB binaries or disable compiler diagnostics. For clang-cl, the platform flags retain `/clang:-Wno-option-ignored` for the bundled Google Test headers and omit `/JMC`, which clang-cl reports as an ignored option when no debug information is requested; this does not weaken MSVC warning settings.

## Retired Cocos UI

The Cocos2d-backed `ui` module and its widget API, UiSampleApp, GUI editor, UI synchronization, and USD UI translation have been retired. Existing UI assets are unsupported; retained tools report this without converting or deleting them. Rebuild engine, modules, editor, samples, and installed SDK consumers together in fresh output directories. Old UI DLLs, headers, and SDK exports are incompatible.

Asset-backed single-line text remains available through `NauScreenText`; see [the screen-text API](NauEngineModules/modules/screen_text/include/nau/text/screen_text.h). ImGui diagnostic interfaces and the editor's Qt interface remain available.
