# Repository Guidelines

## Project Structure & Module Organization

This repository groups three Git submodules; there is no root-level build target.

- `NauEngineLite/`: C++ engine code in `engine/core/`, developer tools in `tools/`, examples and assets in `samples/`, and reusable projects in `project_templates/`. Tests live beside their modules under `tests/`.
- `NauEditorPublic/`: Qt 6/C++20 editor code in `editor/source/`, tests in `editor/tests/`, and localization in `translations/`.
- `NauDocsPublic/`: Sphinx documentation in `source/beta/`, with build helpers in `scripts/` and root batch files.

Read any component-local `AGENTS.md` before editing that component. Avoid unrelated changes to bundled third-party code.

## Build, Test, and Development Commands

From the repository root, initialize dependencies with `git submodule update --init --recursive`.

Engine development requires Visual Studio 2022 C++ tools, CMake, and bootstrapped vcpkg with `VCPKG_ROOT` configured. Run these commands from `NauEngineLite/`:

```powershell
cmake --preset win_vs2022_x64
cmake --build build/win_vs2022_x64 --config Debug
ctest --test-dir build/win_vs2022_x64 -C Debug --output-on-failure
```

These configure, compile, and test the engine. Use the editor's own presets when building `NauEditorPublic/`; set `NAU_ENGINE_SOURCE_DIR` to the absolute path of `NauEngineLite/`.

For documentation, install the Sphinx dependencies listed in `NauDocsPublic/README.md`, then run `sphinx-build -M html source/beta/user-doc build/beta/user-doc` from `NauDocsPublic/`.

## Coding Style & Naming Conventions

Follow neighboring code and component conventions. The engine's `.clang-format` specifies four spaces, no tabs, and Allman braces; format engine changes with that configuration. Preserve established snake_case filenames and editor `nau_` prefixes. Keep generated builds and documentation output out of commits.

## Testing Guidelines

C++ unit tests use Google Test; editor UI tests use Qt Test. Follow existing patterns such as engine `test_*.cpp` and editor `nau_*_tests.cpp`. Add regression tests for behavior changes and run affected suites. Engine tests require `NAU_CORE_TESTS=ON`. No root-level coverage threshold is defined. Prefer portable CTest commands over the machine-specific paths in `run_tests.bat`.

## Commit & Pull Request Guidelines

The root history contains one commit, `Add Nau documentation, editor, and engine submodules`; follow its concise, imperative style. Commit component changes within the appropriate submodule, then update its recorded revision here. PRs should explain behavior changes, identify affected components and revisions, link relevant issues, and report validation. Include screenshots for visible editor changes.
