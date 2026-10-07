# Validation

Validated on Windows on 2026-10-07. This change provides shared packaged,
non-rendering EditorProject execution; it does not add portable rendering or
arbitrary editor-project compatibility.

## Source baseline and tools

Implementation changes are uncommitted. Baseline revisions:

| Repository | Revision |
| --- | --- |
| Root | cd12399 |
| NauEngineLite | 284d4811 |
| NauEngineModules | d1a9f7c |
| NauDemo | 0fd5612 |

VS 2026/v145 (MSVC 19.51), CMake 4.2.1, Ninja 1.13.2, Emscripten 6.0.9,
OpenUSD 24.08 with matching Python 3.10.11, and Chrome 154.0.8037.98 were used.
Browser automation used Playwright. Native cooking used the existing provisioned
Release SDK and tools; portable targets used engine/modules sources and static
project registration. No SDK was installed by these commands.

## Build and acceptance matrix

One fresh native preparation included the authored acceptance fixture. The
archive was then explicitly selected for all four target configurations.

| Platform | Configuration | Acceptance |
| --- | --- | --- |
| Windows | Debug | 18/18 cases passed |
| Windows | Release | 18/18 cases passed |
| Web | Debug | 23/23 cases passed |
| Web | Release | 23/23 cases passed |

The production application is run separately from the independent observer.
Native deliveries are copied outside the checkout and launched with an unrelated
working directory and PATH restricted to Windows system directories. The actual
application reaches checked scene startup and exits zero after repeated native
window-close requests. The observer validates loaded scene data and ten actual
updates, including mover translation and rotator rotation invariants.

Web deliveries are relocated outside the checkout and served under a nested URL
with COOP/COEP headers. Real Chrome executes the production runtime and observer,
including responsive pending startup, terminal status and cleanup.

The archive selected during paired acceptance had SHA-256:

`686eb1e567e14964cbe4c5de71a2edcb75fa93dec3e7e49ac7b3e1afd30ed91b`

The selected-input snapshots, native package/probe-package archives and web
package/probe-package preload data were byte-identical. Per-file hashes were
recorded in `EditorProject/build/unified-archive-hashes.json`. A retained snapshot
is under `build/unified-acceptance/content.nau_pack`. Subsequent ordinary wrapper
runs freshly prepare their main-scene delivery; explicit snapshot reuse is the
reproducible paired-archive mode, not an automatic freshness claim.

### Reproduce

From NauDemo/EditorProject, with provisioned prerequisites:

```powershell
./build.ps1 -Platform Windows -Configuration Debug -Acceptance
$archive = (Resolve-Path ./build/prepared-debug/content.nau_pack).Path
./build.ps1 -Platform Windows -Configuration Release -Acceptance -PreparedArchive $archive
. 'C:/path/to/emsdk/emsdk_env.ps1'
./build.ps1 -Platform Web -Configuration Debug -Acceptance -PreparedArchive $archive
./build.ps1 -Platform Web -Configuration Release -Acceptance -PreparedArchive $archive
python ./tests/verify_native_startup.py --configuration Debug
python ./tests/verify_native_startup.py --configuration Release
python ./tests/verify_web_startup.py --configuration Debug
python ./tests/verify_web_startup.py --configuration Release
```

The reusable driver supports explicit project/engine/modules paths. Host SDK,
tools, USD and Python paths are configurable; local sibling discovery was tested.
Native fresh preparation/build ran with EMSDK removed. Prepared-archive native
Release also built successfully with deliberately nonexistent HostSdk, HostTools
and UsdSdk overrides, proving that target delivery does not discover cooking
prerequisites in this mode.

## Requirement scenario evidence

| Added scenario | Evidence |
| --- | --- |
| All portable configurations execute | Four configurations above compile the same portable_main.cpp and declaration policy; production and fixture execution passed. |
| Native compilation has no browser SDK | Fresh Windows Debug build/preparation with EMSDK unset succeeded. |
| Supported component declaration changes | Preparation test removes MyMover from the declaration and rejects the fixture without changing the prior archive; CMake-generated runtime policy consumes the same declaration, and both target observers use it. |
| Excluded module is declared | Python and CMake validation reject Physics on native/web declaration paths; link audits exclude all prohibited feature targets. |
| One archive is delivered twice | Selected archive, all native archives and both web preload deliveries have the identical hash above. |
| Inputs change or preparation fails | Eight fresh-preparation tests cover clean input, declaration change, authored values, metadata, rebuilt component definitions, missing references, conversion failure and publication failure. Prior archive bytes remain intact after failures. |
| Platforms are built consecutively | Common interface builds all four independent target/configuration caches; native/web link inspections show appropriate platform sources, static modules and no host SDK DLL inputs. |
| Deliveries are relocated | Native production/observer launch outside checkout from unrelated working directory and system-only PATH; web uses relocated nested HTTP URLs. |
| Rendered and portable Windows builds coexist | Existing rendered Release SDK route rebuilt and ran independently; desktop inspection showed the skybox and mesh, physics/scene startup logs were present, and window close returned zero. |
| Successful execution is compared | Both observers verify authored hierarchy, component identities, transforms, properties, required references, actual motion and cleanup; production paths exercise ordinary startup/Stop. |
| Failure and Stop are compared | Both configurations/platforms cover missing/corrupt config, database, scene and archive, unknown/excluded components, immediate/deferred activation failure and repeated Stop. Native returns nonzero for failure; browser retains Failed diagnostics and completes eligible cleanup. |

Native pending-startup tests request Stop before mount and during an awaited
activation, then assert no initial/update snapshots or component updates and
completed cleanup; the activation test confirms accepted work settled. Browser
tests additionally cover actual pending asset loading and repeated Stop through
the production bridge. Update comparisons use authored initial expectations and
motion invariants, not equal native/browser frame timing.

## Preparation, declaration and compatibility checks

The preparation runner uses a disposable clone and the declaration:

```powershell
python ./tests/verify_preparation.py --python C:/path/to/Python310/python.exe `
  --tools C:/path/to/native-tools/bin/Release `
  --module ./build/portable-host-components/bin/Release/MainGameModule.dll `
  --sdk C:/path/to/native-sdk --usd-sdk C:/path/to/openusd/install
```

All eight cases passed. The component-definition case rebuilds a registration
DLL with a new reflected field and verifies it in freshly cooked output.
Authored project files are not imported in place.

Declaration validation exercised valid input, malformed JSON, unsupported version,
excluded/missing modules, duplicate component identities and an invalid startup
configuration path through Python and CMake with native/web selection. All
expected accept/reject outcomes matched. A conflicting legacy/generic source
option fails before graph creation. Both old/new preparation command interfaces
retain --declaration support. An explicit corrupt archive is rejected by the
common driver before configuring a target.

Holding the common build lock while starting another driver invocation produced
the intended retry diagnostic before selected inputs were changed. The normal
driver also rebuilds host registration before fresh preparation; failed cooking
returns before target publication/Run. Staging is confined to ignored build
directories and native publication checks prior failure remnants.

`run_windows.bat Debug` was exercised through fresh build, native launch and
window close; it returned zero. `run_web.bat Debug` was exercised through fresh
build, browser launch and package serving. HTTP returned 200 with the required
isolation headers and the production loader reference; the test-owned server
process tree was stopped afterward. Existing web/build.ps1 configuration and
override arguments were also exercised.

## Consumer regressions and evidence files

- Native common-host Debug: 13/13 CTest entries passed after rebuilding.
- Web common-host Debug: 13/13 CTest scenarios passed after rebuilding.
- Portable asset-package native Release: 4/4 CTest entries passed after rebuilding.
- Existing rendered Windows EditorProject Release: rebuilt, rendered skybox/mesh
  observed through the computer-use skill, and clean window-close exit verified.
- Browser logging severity/duplicate assertions remain part of the 23-case suite.
- Formatting and git diff --check passed; no bundled third-party or editor changes.
- OpenSpec strict validation passed.

Generated evidence is under EditorProject/build: `unified-*.log`,
`native-acceptance-debug.json`, `native-acceptance-release.json`,
`acceptance-debug.json`, `acceptance-release.json`, `preparation-checks.json`,
`unified-archive-hashes.json`, and the rendered window screenshot/state.
These files are ignored and are not committed build artifacts.

## Boundaries

The portable Windows window intentionally has no rendered scene. The rendered
Windows SDK route retains its original content-loading path. The portable
profile accepts only the declared supported service-independent components.
The native machine needs its corresponding MSVC runtime, while web needs the
recorded threaded browser prerequisites and isolation headers. Explicit archive
reuse validates the supplied snapshot/profile but does not prove source freshness.
Fresh cooking remains required to incorporate authored changes.
