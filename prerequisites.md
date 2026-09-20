# Build prerequisites

Installation record: 2026-09-19; sample verification updated 2026-09-20. These requirements cover the
`emscripten-build` change and its native Windows validation. Editor and packaging
requirements are listed separately. See [build.md](build.md) for commands.

## Browser toolchain

| Dependency | Version / setup | Verified status |
| --- | --- | --- |
| Windows and PowerShell | Native Windows host; Windows PowerShell 5.1 supported by the scripts | Used for all checks below |
| Git | Installed 2.55.0.windows.5 | Available; engine submodules are initialized |
| CMake | 3.24+ for preset schema 5 and the SDK probe; tested 4.2.1 | Existing installation retained |
| Ninja | Tested 1.13.2 | Installed using `Ninja-build.Ninja` through WinGet |
| External emsdk / Emscripten | Exact supported SDK **6.0.9**, pinned in `NauEngineLite/cmake/emscripten-sdk-version.txt` | Installed at `$HOME/emsdk`, activated; Debug and Release coroutine/pthread compile-link probes pass |
| SDK LLVM, sysroot and binary tools | Supplied by emsdk 6.0.9; release hash `f04ea239d533260dd1db760dd2d668d5f9a88d6b` | Installed by emsdk |
| SDK Node.js | 24.19.0 | Installed by emsdk; used by compiler tools |
| SDK Python | 3.13.3 | Installed by emsdk; separate from desktop generator Python |
| Chrome on Windows | Tested 153.0.8010.52 | Production browser platform tests pass in Debug/Release using a temporary headless profile |
| Browser-test Python | Tested system Python 3.14.2 | Runs the local isolated server and Chrome acceptance runner; distinct from SDK Python |
| Browser automation | `playwright==1.63.0`, `pyee==13.0.1`, `greenlet==3.5.6`, `typing-extensions==4.15.0` | Installed for Python 3.14; uses existing Chrome, no Playwright browser download required |

The SDK pin passes both its standalone capability probe and the real selected
Nau core and actual minimal sample tests in Debug/Release. Browser sample execution
is verified; runtime package staging and relocation remain pending.
CMake 4.2.1 triggers an SDK warning about shared libraries; the probe and
browser runtime use static linking. No change to existing CMake was necessary.

Use explicit SDK installation and activation commands from the
[official emsdk instructions](https://emscripten.org/docs/getting_started/downloads.html).
The checked-in preflight and CMake checks never install, activate, or upgrade an SDK.
Open a new PowerShell after WinGet changes PATH, then load `emsdk_env.ps1` for each
browser session. SDK activation was not added to the global PATH.

## Native validation and desktop engine tools

| Dependency | Version / setup | Verified status |
| --- | --- | --- |
| Visual Studio 2026 C++ tools | VS 18 with Desktop development with C++, x64 tools and Windows SDK; native CMake 4.2+ | Clean minimal Debug/Release builds and lifecycle tests pass; full desktop/editor validation in progress |
| MSVC v145 | Tested compiler 19.51.36257.0; tool directory 14.51.36231 | Selected explicitly, including when older MSVC tools are installed in VS 2026 |
| Windows SDK | Test selected 10.0.26100.0 | Available |
| Desktop generator Python | 3.10.11 with pip | Installed; select with `py -3.10` |
| Python packages | `cymbal==1.0.0`, `clang==21.1.7` | Installed under Python 3.10; available for desktop generation and the validated scene dependency build |
| vcpkg | Existing bootstrapped checkout; executable reports 2025-12-16 | Reused `D:/Programming/vcpkg`; user `VCPKG_ROOT` configured, no baseline or installed package revisions changed |
| Native manifest libraries | protobuf 3.21.12#2 and DirectX DXC 2024-03-29 at the engine's recorded vcpkg baseline | Installed by the successful desktop configuration checks; not used by the browser probe |

The native minimal profile now builds and passes its focused lifecycle suite in
Debug and Release. It needs VS C++ tools, a Windows SDK, CMake and recorded bundled
sources. vcpkg and the Python generator packages are desktop-only requirements.
The browser build must bypass desktop vcpkg, Qt, USD and DirectX dependencies.

## Repository source dependencies

Keep dependencies at recorded revisions; do not update them to latest releases.
`git submodule status --recursive -- NauEngineLite` showed these engine dependencies
initialized at their recorded commits:

| Source | Revision |
| --- | --- |
| NauEngineLite | `52197201e525a584fb9490be22b1d064b0c666e1` before this change |
| engine/3rdparty_libs/DirectX-Headers | `de28d93dfa9ebf3e473127c1c657e1920a5345ee` |
| engine/3rdparty_libs/googletest | `f8d7d77c06936315286eb55f8de22cd23c188571` |
| engine/3rdparty_libs/tracy | `37aff70dfa50cf6307b3fee6074d627dc2929143` |
| tools/3rd_party/argparse | `a2b4d27989177466d4ceceba05e8278f9da498f2` |
| tools/3rd_party/json | `960b763ecd144f156d05ec61f577b04107290137` |

Other bundled sources are recorded directly in the engine checkout. This inventory
is broader than the implemented minimal profile; its exact selection is in
`NauEngineLite/cmake/NauMinimalRuntime.cmake`. Existing editor dependency revision differences and
uninitialized optional OpenSSL submodules were left untouched.

The minimal runtime uses EABase, EASTL, tiny-utf8, fmt, utfcpp, ModifiedSonyMath,
jsoncpp, wyhash and fast_float. The explicit minimal kernel manifest excludes the
unused compression/asset IO groups. Focused tests additionally require bundled
googletest; the core serialization suite also uses its googlemock component. These are source
libraries, not additional system installations.

## Source prerequisites still required

These are planned project implementations, not packages that an installer can provide:

The `minimal-runtime-profile` prerequisite is implemented and validated natively;
see [its guide](NauEngineLite/doc/minimal_runtime_profile.md). Current source status:
- `wasm-core-portability` is implemented and validated: see the
  [core build/test guide](NauEngineLite/doc/wasm_core_portability.md). Its independent
  validation uses activated SDK Node 24.19.0 and Python 3 standard-library helpers;
  no additional packages or SDK upgrades are required.
- `browser-platform-services` is implemented and validated against real DOM state
  in Chrome, including platform readiness and disposal. See the
  [platform guide](NauEngineLite/doc/browser_platform_services.md).
- `browser-runtime-lifecycle` is implemented using the real shared application
  worker and production static PlatformApp. Its Debug/Release Chrome acceptance
  uses the same SDK, Python/Playwright and Chrome dependencies as the platform
  suite; no additional installation or SDK change is required. See the
  [lifecycle guide](NauEngineLite/doc/browser_runtime_lifecycle.md).
- `minimal-app-web` is implemented: the selected sample builds through both browser
  presets and passes actual-sample Chrome acceptance. See the
  [sample guide](NauEngineLite/doc/minimal_app_web.md). The existing SDK and
  Python/Playwright/Chrome installations were reused; no additional dependencies
  were installed. Runner Python is required only for acceptance, not sample builds.
- `minimal-web-delivery-validation`: browser page/server with isolation headers
  and relocation checks; focused native lifecycle checks are already supplied.

`NauFrameworkMinimal` shares the lifecycle without rendering integration. Native
Debug/Release lifecycle checks pass; full browser packages remain pending.

Browser presets and shared platform options build the real sample. Both
configurations audit 97 compile commands with consistent threaded/no-exception
options and no native Windows libraries. Minimal graph configuration skips
vcpkg, desktop generator packages and unrelated feature modules. Unsupported
browser desktop-profile and shared-library settings report explicit errors.
The existing desktop preset configured successfully without emsdk before and
after these changes, retaining its compiler/cache settings.

## Additional editor/documentation/packaging requirements

For the delivered minimal web folder, install Python 3.9+ and current Chrome.
Run its `serve.py --port 8000` and open the printed URL. No SDK, CMake, Ninja,
vcpkg or Playwright is needed to serve a copied package. The bundled server sends
the required isolation headers; file URLs and ordinary servers without COOP/COEP
cannot launch the threaded application. See the
[delivery guide](NauEngineLite/doc/minimal_web_delivery.md) for nested URLs,
another port, Stop/cleanup, reload and missing-file diagnostics. Acceptance uses
the separately listed Python/Playwright installation. Clean build-directory and
copied-package checks do not replace fresh-checkout/environment reproduction.

These are outside the Emscripten dependency installation performed here:

- Editor: project Qt 6.4.1 MSVC x64 distribution, Debug libraries, Linguist and Svg;
  prepare its headers with `NauEditorPublic/scripts/prepare_qt_for_msvc.py` for MSVC 14.51.
  OpenUSD 24.08 is fetched by the desktop DLL configuration. See [build.md](build.md).
- Installer packaging: NSIS and the plugins/redistributables used by the editor
  installer scripts.
- Documentation: Sphinx and the dependencies in `NauDocsPublic/README.md`.

No editor, renderer, NauDemo, or unrelated submodule implementation was modified.


## NauDemo web additions

The demo uses the same explicitly activated **Emscripten SDK 6.0.9**, CMake
**3.25+** (tested 4.2.1), Ninja 1.13.2, Git and Chrome as the browser runtime.
Keep the `NauDemo` and `NauEngineLite` submodules adjacent. Its CPU asset profile
also needs the recorded bundled `tinyimageformat` headers; no new external
rendering SDK, Qt, USD, desktop shader tool or native DLL is required.

Chrome must support WebGL 2, transferable OffscreenCanvas, workers and
SharedArrayBuffer on a secure cross-origin isolated page. The packaged Python
3.9+ server supplies the required headers. Serving does not need the SDK.

Acceptance uses Python 3.14.2 with `playwright==1.63.0` and **Pillow==12.1.1**
for PNG/pixel validation, using installed Chrome 153.0.8010.52. These packages
were already available; no additional installation was required. The focused
native/Node/Chrome scene suite additionally needs the engine googletest submodule
and VS 2026 C++ tools (v145), with CMake 4.2 or newer. Desktop generation uses Python 3.10 with its `Scripts`
directory on PATH, `cymbal==1.0.0` and `clang==21.1.7`.

Native MSVC validation uses VS Community 2026 18.10.1, MSVC tools 14.51.36231
(compiler 19.51.36257.0), Windows SDK 10.0.26100.0 and CMake 4.2.1. The separate
clang-cl compiler supplied by VS 2026 is LLVM 22.1.3; the Python `clang` package
is a generator dependency, not that compiler. Prepare the recorded USD/TBB and
Google Test headers using the [clang-cl setup helper](NauEngineLite/cmake/probes/windows_toolchain/README.md).
Static and DLL builds pass after preparation. Runtime validation passes 409
static tests with one exclusion and 406 DLL tests with four exclusions; the
deferred async/allocator failures remain in [failed-tests.md](failed-tests.md).
See the [validation record](openspec/changes/archive/2026-09-21-windows-msvc-2026/validation.md) for scope and evidence.

See [NauDemo web](NauEngineLite/doc/naudemo_web.md) for build, serving, fixture,
relocation and recorded fresh-checkout commands.

## NauSamples dependency

The root `NauSamples` submodule (`https://github.com/yakovfil/NauSamples.git`) supplies native samples and the minimal browser application. Initialize it from Nau with `git submodule update --init NauSamples`. Native NauDemo requires its shared support and sceneBase resources. The browser demo-only build uses NauDemo's own assets.

Select another checkout through CMake's `NAU_SAMPLES_SOURCE_DIR` cache path. Configuration reports missing required sample files and never clones repositories automatically. Existing SDK/compiler prerequisites are unchanged. Keep generated caches out of source migration and reconfigure old build trees. Compatible samples, engine and demo revisions are recorded by the parent repository; publish their commits before a parent revision that references them.
