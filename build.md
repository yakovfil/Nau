# Building the Engine and Editor

These instructions cover Windows x64 builds of `NauEngineLite` and `NauEditorPublic` using Visual Studio 2022 and PowerShell, plus the Emscripten toolchain checks below. Run commands one at a time and continue only after each succeeds. The repository root has no CMake project; configure each component separately. See [prerequisites.md](prerequisites.md) for required tools, exact SDK versions, installation status and remaining source prerequisites.

## 1. Install prerequisites

Install the following before configuring either project:

| Dependency | Required setup |
| --- | --- |
| Visual Studio 2022 | Desktop development with C++, MSVC v143, and Windows 10 SDK. |
| CMake | A version supporting preset schema version 5. The top-level engine declaration of 3.20 alone is insufficient for these presets. Use `cmake --list-presets` below to verify compatibility. |
| Git | Available on `PATH`, with recursive submodule support. |
| Python | Python 3.10 with pip on `PATH`, matching the version documented by this project. The downloaded USD package also contains its own Python 3.10 runtime. |
| vcpkg | A bootstrapped checkout outside this repository; setup below. |
| Qt (editor only) | The project's documented Qt 6.4.1 MSVC x64 distribution, including Debug libraries, Linguist tools, and SVG support. |

Use **Developer PowerShell for VS 2022** with the x64 toolchain. Prefer a short local checkout path without Cyrillic characters or cloud synchronization.

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
$nauRepo = (Get-Location).Path
git submodule update --init --recursive
git submodule status --recursive
$env:NAU_ENGINE_SOURCE_DIR = Join-Path $nauRepo 'NauEngineLite'
```

The expected layout is:

```text
Nau/
  build.md
  NauEngineLite/
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
cmake --preset win_vs2022_x64
cmake --build build/win_vs2022_x64 --config Debug
```

The equivalent build-preset command is `cmake --build --preset "VS Debug"`. For an optimized build, use:

```powershell
cmake --build build/win_vs2022_x64 --config Release
```

Visual Studio presets support multiple configurations in one build directory. Supply `--config` when building and `-C` when testing. Most engine executables are placed in `build/win_vs2022_x64/bin/Debug/`, with libraries under `lib/`.

For IDE development, open `build/win_vs2022_x64/NauEngine.sln`, select Debug or Release and x64, and build `ALL_BUILD`. To run an example, select an executable sample such as `MinimalAppSample` as the startup project.

### Run engine tests

```powershell
ctest --test-dir build/win_vs2022_x64 -C Debug -N
ctest --test-dir build/win_vs2022_x64 -C Debug --output-on-failure
```

The first command lists registered tests; the second executes them. Add `-R '<regex>'` to select test names. Tests require `NAU_CORE_TESTS=ON` and must be compiled first. Use these portable commands instead of the absolute paths in the checked-in `run_tests.bat`.

### Install the engine SDK

After a successful build:

```powershell
cmake --install build/win_vs2022_x64 --config Debug
```

The engine's `CMakeLists.txt` forces the install prefix to `NauEngineLite/output/`, overriding the preset's `dist/` default. The installed tree includes a separate CMake project; the engine README describes configuring and building that tree when preparing the SDK. Installation is not required to configure the editor against engine sources.

### Optional engine configurations

For a DLL engine, including USD-dependent tools:

```powershell
cmake --preset win_vs2022_x64_dll -A x64
cmake --build build/win_vs2022_x64_dll --config Debug
ctest --test-dir build/win_vs2022_x64_dll -C Debug --output-on-failure
```

The DLL configuration downloads the project's OpenUSD 24.08 archive automatically through `cmake/defaults/UsdPackages.cmake`.

To omit standalone engine tests or samples, reconfigure with `-DNAU_CORE_TESTS=OFF` or `-DNAU_CORE_SAMPLES=OFF`. Keep the defaults for the initial build. These options do not provide an equivalent way to disable editor requirements: the editor explicitly enables engine tools and samples and disables engine core tests in its own build.

## 4. Build the editor

### Prepare Qt

The checked-in [installation documentation](NauDocsPublic/source/beta/user-doc/introduction_to_nau/install_nau/install_nau_doc.rst) identifies Qt 6.4.1 and provides the project's distribution location. Extract that package and locate its `msvc2019_64` directory. This is the Qt prefix, containing `bin/` and `lib/cmake/Qt6/`.

Set the actual path for your machine:

```powershell
$nauQt = 'C:/Tools/Qt-6.4.1_2/msvc2019_64'
Test-Path "$nauQt/lib/cmake/Qt6/Qt6Config.cmake"
Test-Path "$nauQt/bin/windeployqt.exe"
```

Both checks should return `True`. The editor requires Qt Core, Widgets, Network, Test, OpenGL, LinguistTools, and Svg. Its vcpkg manifest does not install Qt. The documentation also lists Qt Visual Studio Tools for IDE integration; the commands below use CMake directly.

### Configure against the engine sources

```powershell
Set-Location (Join-Path $nauRepo 'NauEditorPublic')
cmake --list-presets
cmake --preset win_vs2022_x64_dll -A x64 "-DNAU_ROOT_DIR=$env:NAU_ENGINE_SOURCE_DIR" "-DCMAKE_PREFIX_PATH=$nauQt"
```

Use the DLL preset for the editor: its linked USD plugin targets are enabled by `BUILD_SHARED_LIBS`. `NAU_ROOT_DIR` must point to `NauEngineLite/`, not its `build/` or `output/` directory.

The editor adds the engine with `add_subdirectory`, compiling it inside the editor's build tree. It does not reuse the standalone engine binaries. Building the standalone engine first is useful for checking the toolchain but is not a prerequisite of this configure command.

Unlike the older installation example, the current USD helper fetches OpenUSD automatically and sets `pxr_DIR` itself. Do not rely on `-Dpxr_DIR=...` alone to select another distribution. For an existing copy of the exact project archive, CMake's FetchContent override is available by adding `"-DFETCHCONTENT_SOURCE_DIR_USD=C:/Tools/openUSD_24.08_noHydra"`; point it at the extracted package root containing `pxrConfig.cmake`.

### Compile and launch

Build the editor target for local development:

```powershell
cmake --build build/win_vs2022_x64_dll --config Debug --target NauEditor
```

This includes its declared engine, plugin, sample, and translation dependencies. Post-build commands deploy Qt libraries, engine/USD DLLs, plugins, and project templates into the editor output directory.

```powershell
Push-Location build/win_vs2022_x64_dll/Debug/NauEditor
& ./NauEditor.exe
Pop-Location
```

Alternatively, open `build/win_vs2022_x64_dll/NauEditor.sln` and launch the `NauEditor` startup project. Its debugger settings configure additional USD/plugin paths. Keep the deployed files beside the executable.

For Release, repeat the build with `--config Release`; the executable will be under `build/win_vs2022_x64_dll/Release/NauEditor/`.

### Build and run editor tests

```powershell
cmake --build build/win_vs2022_x64_dll --config Debug --target NauEditorUnitTests NauEditorUiTests
$env:PATH = "$nauQt/bin;$env:PATH"
ctest --test-dir build/win_vs2022_x64_dll -C Debug -N
ctest --test-dir build/win_vs2022_x64_dll -C Debug --output-on-failure
& ./build/win_vs2022_x64_dll/Debug/NauEditorUiTests/NauEditorUiTests.exe
```

Unit tests use Google Test discovery. The Qt UI test executable is not registered with CTest in its current CMake file, so run it separately in an interactive desktop session. Run standalone engine tests from the engine build tree, since the editor disables those suites.

### Optional installer packaging

A default editor build, including `ALL_BUILD` or the `VS Debug Dll` build preset, also runs the `Installer` target. To request packaging explicitly:

```powershell
cmake --build build/win_vs2022_x64_dll --config Debug --target Installer
```

The scripts additionally build/install an engine SDK, copy it into the editor distribution, download redistributables, and use NSIS. They may install NSIS and its plugin with an elevation prompt. Expected output is `build/win_vs2022_x64_dll/Debug/Installer.exe`. Inspect the packaging output as well as the exit status: the SDK helper currently resets one returned build status before proceeding. Use `--target NauEditor` when only developing the application.

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

See the engine-local [Emscripten guide](NauEngineLite/doc/emscripten_build.md) for
fresh installation commands, exact tool versions and the delivery boundary.
The shared minimal framework now passes native Debug/Release lifecycle tests.
Browser platform services and the actual sample pass Chrome tests. Use the browser
presets below; staged packages and relocation remain pending.

Browser presets `web-minimal-debug` and `web-minimal-release` now exist with
matching build presets, isolated Ninja caches, and separate `bin`/`lib` paths.
Both presets configure and build the actual `MinimalAppSample`. Its production
minimal graph excludes desktop dependencies. The platform checks also retain
standalone option checks using bundled `xxHash`; sample graph and Chrome checks
are documented in the [sample guide](NauEngineLite/doc/minimal_app_web.md).

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
[profile guide](NauEngineLite/doc/minimal_runtime_profile.md) for dependency lists,
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

The actual sample now consumes this lifecycle through `web-minimal-*`. From
`NauEngineLite` with the SDK active:

```powershell
cmake --preset web-minimal-debug
cmake --build --preset web-minimal-debug --parallel 8
cmake --preset web-minimal-release
cmake --build --preset web-minimal-release --parallel 8
python cmake/probes/minimal_app_web/run.py --build build/web-minimal-debug --scenario success
python cmake/probes/minimal_app_web/run.py --build build/web-minimal-release --scenario success
```

Use Python with Playwright installed for the runner. Both sample configurations
pass success, missing-host, host-loss and intentional runner-failure checks.
Foreground rates measured 9.7830 Hz Debug / 9.7711 Hz Release. The
[sample guide](NauEngineLite/doc/minimal_app_web.md) covers all scenarios and
[validation evidence](openspec/changes/minimal-app-web/validation.md) records graph
and regression results. Outputs are `bin/MinimalAppSample.js` and `.wasm` in each
preset build directory; no separate worker script was emitted by SDK 6.0.9.
Default browser builds now stage `package/` in each preset directory. Run
`python build/web-minimal-debug/package/serve.py --port 8000` from the engine
directory (or use the Release path), then open the printed URL. Copy the entire
folder to serve elsewhere; `--base-path /relocated/nau/` supports nested URLs.
The [delivery guide](NauEngineLite/doc/minimal_web_delivery.md) covers controls,
failure diagnostics and acceptance. Serving needs Python 3.9+ and Chrome only;
Playwright and the SDK are not serving dependencies. The page checks isolation
before loading runtime files, exposes real status/Stop/cleanup, and requires
reload to retry. Fresh-checkout/environment reproduction remains pending.

These instructions were checked against the component `CMakePresets.json` files,
engine and editor CMake targets, installer scripts, and local installation
documentation. Both configure-preset lists were successfully read with CMake.
Validation performed for the Emscripten update is listed above. Full engine/editor
compilation, test execution, and installer generation remain
unverified.


## NauDemo browser build

From `NauEngineLite/`, with SDK 6.0.9 activated:

```powershell
. "$HOME/emsdk/emsdk_env.ps1"
cmake --preset web-demo-debug
cmake --build --preset web-demo-debug --parallel 8
cmake --preset web-demo-release
cmake --build --preset web-demo-release --parallel 8
python build/web-demo-debug/package/serve.py --port 8000
```

Open the printed Chrome URL. The `demo` profile retains real Nau scene/assets
and worker-owned WebGL 2 without desktop Graphics/UI/VFX/physics. Its browser
material is simplified blue diffuse lighting; simulation remains nominally 100 ms
per update. Stop is asynchronous; reload retries after Stop/failure.

Both package folders contain runtime, preloaded and loose asset/configuration/
shader inputs, a hashed manifest and a loopback server. Copy the entire folder;
`--base-path /games/nau/` supports nested hosting. Source paths and SDK files are
not requested at runtime. See [NauDemo browser instructions](NauEngineLite/doc/naudemo_web.md)
for exact acceptance and fresh-checkout commands. Native NauDemo now also builds
from current sources in Debug/Release using its documented CMake hook; native
appearance confirmation remains distinct from those successful builds.
