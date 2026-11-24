# Nau Engine workspace

This repository pins the versions of the Nau C++20 engine, its feature modules, the Qt editor, documentation, samples, and a playable demo. The components are sibling Git submodules. Each build starts in the component that owns it. To try the engine on Windows or in a browser, start with **NauDemo**. To develop against individual engine APIs, start with **NauSamples**.

For the fork’s upstream baseline, major changes, and compatibility notes, see [Changes from upstream Nau Engine](changes.md).

## Repository layout

| Directory | What it contains |
| --- | --- |
| [NauEngineLite](NauEngineLite/) | Standalone engine kernel, application framework sources, bundled libraries, CMake presets, and tests. |
| [NauEngineModules](NauEngineModules/) | Engine features including assets, scenes, rendering, input, and audio, alongside module tests, asset tools, and packaging support. Its CMake hook attaches modules to an engine build. |
| [NauSamples](NauSamples/) | Focused examples for application startup, scene setup, physics, input, networking, scripting, and asset handling. Samples share support code and build through the engine. |
| [NauDemo](NauDemo/) | Editor-authored project with native and browser launchers. Open `NauDemo.nauproject` in the editor to work on the project. Authored assets live in `content/`, game components in `source/`, and the portable project declarations in the component root. |
| [NauEditorPublic](NauEditorPublic/) | Qt 6 desktop editor. Editor code lives in `editor/source/`, tests in `editor/tests/`, and translations in `translations/`. |
| [NauDocsPublic](NauDocsPublic/) | Sphinx documentation sources, assets, and build helpers. The beta user guide lives in `source/beta/user-doc/`. |
| [openspec](openspec/) | Current behavior specifications in `specs/`, active changes in `changes/`, and completed changes in `changes/archive/`. |

## Build and run the demo

Use **x64 Developer PowerShell for Visual Studio 2026**. The launchers require the v145 C++ toolset, Windows SDK, CMake 4.2+, Python 3.10 with the project's generator dependencies, and a bootstrapped vcpkg checkout with `VCPKG_ROOT` set. The browser target also requires Ninja and Emscripten **6.0.9**. The web launcher locates the SDK through `EMSDK` or `%USERPROFILE%\emsdk`. For installation commands and OpenUSD prerequisites, see the [build guide](build.md) and [toolchain inventory](prerequisites.md).

From the root of a fresh checkout, initialize the pinned sources and launch the Windows Release demo:

```powershell
git submodule update --init --recursive
Set-Location NauDemo
.\run_windows.bat Release
```

For the browser version, run the following from `NauDemo/`:

```powershell
.\run_web.bat Release
```

Both launchers prepare the native asset tools, cook the scene content, and build the selected application. The first run also builds the host SDK by default. Subsequent runs reuse outputs under `NauDemo/build/`. Omitting `Release` selects Debug. The web launcher starts a local server and opens the demo in a browser. Press Ctrl+C in that terminal to stop serving it.

### Scenes in the demo

The default `menu` package includes all four scenes. Click a scene or use Up/Down and Enter to select it. Escape returns to the menu. To launch a scene directly, pass its name after the configuration, for example `.\run_web.bat Release benchmark`.

| Scene | What to try |
| --- | --- |
| `shooter` | Fly a P-38 through six enemy waves and return to the carrier. Move with WASD or the arrow keys and fire with Space or the primary mouse button. |
| `battlezone` | Drive a tank with W/S, turn with A/D, and press Space or click to fire a shot. |
| `original` | Explore the animated mesh and billboard scene. Move with WASD, change height with Q/E, and drag with the left mouse button to look around. |
| `benchmark` | View a fixed grid of 1,024 cubes. The overlay reports frame submission rate and milliseconds per frame. Use the same viewport size when comparing runs. |

The browser release uses Emscripten to compile the engine and game to WebAssembly. The Release menu package is staged in `NauDemo/build/basic-rendering-scene/web-release/package/`. Its `index.html` loads the JavaScript, WebAssembly, and data files from the same directory. For deployment, serve the package over HTTPS with cross-origin isolation for its worker threads. The included local server supplies the headers for development. See the [demo guide](NauDemo/README.md) and [web packaging guide](NauDemo/web/README.md).

To check scene selection, switching, and shutdown after building the corresponding Release menu package, run its verifier from `NauDemo/`. The web check requires Playwright and Chrome.

```powershell
python tests/verify_menu.py --platform Windows
python tests/verify_menu.py --platform Web
```

## Build the engine, modules, and samples

Run the following examples from `NauEngineLite/`. Each configuration has its own build directory so the standalone kernel, module tests, and samples can coexist.

**Standalone Windows kernel**

```powershell
cmake --preset win_vs2026_x64
cmake --build build/win_vs2026_x64 --config Debug
```

**Engine with feature modules and tests**

```powershell
$moduleHook = (Resolve-Path ../NauEngineModules/cmake/attach_modules.cmake).Path
cmake --preset win_vs2026_x64 -B build/modules "-DCMAKE_PROJECT_NauEngine_INCLUDE=$moduleHook" -DNAU_CORE_TESTS=ON
cmake --build build/modules --config Debug
ctest --test-dir build/modules -C Debug --output-on-failure
```

**Scene sample** (the sample hook also attaches the modules)

```powershell
$sampleHook = (Resolve-Path ../NauSamples/cmake/attach_samples.cmake).Path
cmake --preset win_vs2026_x64 -B build/samples "-DCMAKE_PROJECT_NauEngine_INCLUDE=$sampleHook"
cmake --build build/samples --config Debug --target SceneBaseSample
```

For additional native and browser sample targets, see the [samples guide](NauSamples/README.md).

## Build the editor and documentation

The editor uses its own CMake presets and requires the project's Qt 6.4.1 MSVC x64 distribution. Configure from `NauEditorPublic/` with `NAU_ENGINE_SOURCE_DIR` pointing to `NauEngineLite/` and `NAU_MODULES_SOURCE_DIR` pointing to `NauEngineModules/`. The [engine and editor build guide](build.md) gives the complete Release configuration, Qt paths, and build commands.

To build the beta user guide, install the Python dependencies in the [documentation README](NauDocsPublic/README.md), then run this from `NauDocsPublic/`:

```powershell
sphinx-build -M html source/beta/user-doc build/beta/user-doc
```

Open `build/beta/user-doc/html/index.html` to read the generated guide.
