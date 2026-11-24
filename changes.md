# Major changes from upstream Nau Engine

This fork grew from three upstream checkouts into a six-component workspace. Its largest changes are the separation of the engine kernel from feature modules, a C++ standard-library migration that affects binary compatibility, and a shared Windows and WebAssembly runtime that can launch an editor-authored game project. This record covers the component revisions pinned by root commit `17eee38` on 2026-11-24. For build instructions, see the [workspace README](readme.md).

## Upstream baseline

The root repository has its own history. Its first commit, `dcc4beb`, pinned the three components below. Git identifies those same pins as the last common ancestors between the fork and the upstream default branches checked for this record. The changes described here follow the fork forward from those ancestors. Upstream engine and editor development continued independently. [Upstream Nau Engine organization](https://github.com/NauEngine)

| Upstream component | Common ancestor | Fork component at this snapshot | Upstream HEAD checked |
| --- | --- | --- | --- |
| [NauEnginePublic](https://github.com/NauEngine/NauEnginePublic) | `52197201` | `NauEngineLite` at `157706cb` | `8840fb3c` |
| [NauEditorPublic](https://github.com/NauEngine/NauEditorPublic) | `5b6880a` | `NauEditorPublic` at `d812c10` | `27d71f58` |
| [NauDocsPublic](https://github.com/NauEngine/NauDocsPublic) | `f252ec3` | `NauDocsPublic` at `a21e959` | `f252ec3` |

The root also pins `NauEngineModules` at `60639f2`, `NauSamples` at `50c860e`, and `NauDemo` at `530e4b7`. A diff of the engine directory alone therefore misses both relocated code and subsequent development.

## Engine structure and build compatibility

- **Kernel, modules, and samples have separate build boundaries.** The kernel can build independently. Feature modules, module-dependent tools, and templates moved into `NauEngineModules`. The application framework sources and kernel tests live with the engine, while the module hook enables the framework for consumers. The former engine samples tree moved into `NauSamples` with its history and assets. Its own CMake hook attaches modules before adding the examples. Root milestones include `c6ab80a` (samples), `4eac124` (modules), and `ce02d0b` (framework and tests). [Samples extraction record](NauSamples/README.md) · [Module integration](NauEngineModules/README.md)
- **The Windows toolchain moved to Visual Studio 2026 and MSVC v145.** Engine and editor presets, SDK builds, and consumer configuration were updated together. Native desktop builds use CMake 4.2+ and vcpkg. The editor can build against the sibling engine and modules with a locally built OpenUSD SDK. The web target has its own Emscripten toolchain, while desktop tools still prepare its content. [Build guide](build.md) · [Prerequisites](prerequisites.md)
- **C++20 standard types replaced EASTL and custom strings.** The fork removed EASTL and EABase from the active build and SDK interfaces, retaining Nau adapters where allocation, ownership, or container semantics require them. A separate migration changed public string interfaces to standard UTF-8 strings and made Unicode conversion and code-point operations explicit. Engine, editor, modules, and SDK consumers must be rebuilt together across this ABI change. Engine commits `af98cc36` and `c2cddda5` distinguish the two migrations. [Standard-library specification](openspec/specs/toolchain-standard-library/spec.md) · [String migration validation](openspec/changes/archive/2026-11-24-replace-nau-string-with-std/validation.md)

## Browser runtime and portable game projects

- **The real application lifecycle runs in WebAssembly.** A minimal profile brought engine startup, service registration, repeated updates, and orderly shutdown to an Emscripten pthread worker while leaving the browser thread responsive. The browser host reports lifecycle state and forwards engine logs to the console. Windows and web applications now share host and update behavior, and the minimal sample uses one application entry point on both targets. Engine milestones include `37e1f4ea` (web build) and `37b9a839` (common host). [Browser lifecycle](openspec/specs/browser-runtime-lifecycle/spec.md) · [Common application host](openspec/specs/common-application-host/spec.md)
- **An editor-created project can produce both native and browser packages.** A portable project declaration selects modules, startup configuration, and supported components. Native tools cook authored content into an asset archive. Both targets load the packaged scene through the shared startup path. The web delivery includes an HTML entry point, a JavaScript loader, WebAssembly, and packaged data. Templates and build helpers apply the same workflow to generated projects outside the workspace. Root commits `6aa62de` and `1e15a6e` record build and generation unification. [Portable project generation](openspec/specs/portable-project-generation/spec.md) · [Packaged project startup](openspec/specs/editor-project-web-startup/spec.md)
- **A portable rendering profile draws authored scenes on Windows and WebGL 2.** Supported content includes meshes, cameras, textured billboards, and vector geometry. Screen-relative billboards support HUD placement and aspect-preserving images. Optional modules provide keyboard and pointer input, focus handling, and one-shot audio from packaged assets. The profile defines which components it accepts, so browser support can be assessed per project. [Rendering contract](openspec/specs/portable-scene-rendering/spec.md) · [Input](openspec/specs/portable-input/spec.md) · [Audio](openspec/specs/portable-audio/spec.md)

## UI and editor workflows

The fork retired the Cocos2d-backed UI module, GUI authoring and synchronization tools, USD UI translation, and the old UI sample. The editor reports legacy UI assets as unsupported. Its desktop interface still uses Qt. New engine facilities provide scene-backed widgets with hierarchy, transforms, size, pivot, and prefab persistence, plus a separate optional renderer for single-line text from packaged fonts. The docs fork records the Cocos retirement in `a21e959`. [UI retirement](openspec/specs/cocos-ui-retirement/spec.md) · [Widget model](openspec/specs/widget-foundation/spec.md) · [Screen text](openspec/specs/screen-text/spec.md)

The deployed editor gained independent commands to create, inspect, open, compile, and build projects. Scripts can resolve a project explicitly, select a build preset, and observe completion without driving the editor UI. Editor commit `b21cabb` introduced these commands. [Editor CLI contract](openspec/specs/editor-project-cli/spec.md)

## Demo and validation

`NauDemo` exercises the portable project workflow with one package and a responsive scene selector. The **Original** scene demonstrates animated geometry, billboards, camera input, and click audio. **Battlezone** exercises vector rendering and tank controls. **Shooter** adds a carrier sortie with extracted aircraft artwork and six enemy waves. **Benchmark** renders 1,024 cubes and reports frame-submission cadence. Players can switch scenes and return to the menu without rebuilding or reloading. Root commits `507f2fd`, `d2d914e`, `338c876`, and `e0aede9` track their integration. [Demo guide](NauDemo/README.md)

The fork includes checks for browser lifecycle transitions, asset relocation and failure handling, scene switching, resize and input behavior, and orderly shutdown. The browser acceptance workflow uses desktop Chrome on Windows. Archived changes preserve the reasoning and validation records alongside the current behavior specifications. [Menu verifier](NauDemo/tests/verify_menu.py) · [Web build and validation](NauDemo/web/README.md) · [Archived changes](openspec/changes/archive/)

## Updating this record

Use the root history to find when a component revision entered the workspace, then inspect the history inside that component for the implementation. For example, run these commands from the root:

```powershell
git log --oneline -- NauEngineLite NauEngineModules NauEditorPublic NauSamples NauDemo NauDocsPublic
git log --submodule=log -p -1 e0aede9
git -C NauEngineLite log --oneline 52197201..157706cb
```

For a new milestone, record the affected component, its pinned revision, the observable behavior or compatibility change, and a link to the specification or validation record. Refresh the upstream comparison revisions when updating the baseline.
