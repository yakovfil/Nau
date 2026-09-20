# Acceptance evidence — 2026-09-19

Implemented in the NauEngineLite working tree based on
`52197201e525a584fb9490be22b1d064b0c666e1`; no new component commit was created.

| Scenario | Evidence | Result |
| --- | --- | --- |
| Minimal native configuration | Both native presets configure without vcpkg; file-API audit checks all 23 targets against allowed source directories | Pass |
| Unsupported required module | Real profile CMake include rejects Rendering with supported/required set | Pass |
| Missing required bundled source | Separate source fixture missing fmt produces dependency-specific failure without host fallback | Pass |
| Create and initialize | Real PlatformApp static registration; lifecycle test checks window manager, background service and virtual filesystem | Pass |
| Repeated steps and orderly stop | Five ordered pre/post callbacks, shutdown callback, service destruction, step completion and application destruction in both configurations | Pass |
| Both sample entry-point files exist | Both samples link; graph contains app_sample_main_min.cpp and generated module initialization only | Pass |
| Native validation | Debug and Release CTest pass with 30-second timeout; native graphs contain no pthread browser options | Pass |
| Existing desktop selection | win_vs2022_x64 configures, full feature graph retained, original entry point selected; affected NauFramework and PlatformApp Debug libraries compile with dependency builds skipped | Pass |

Commands and precise validation limits are recorded in
`NauEngineLite/doc/minimal_runtime_profile.md`. Logs remain in the ignored engine
build directory. These checks establish the native profile, not browser runtime
acceptance or a complete desktop application build. Renderer implementations,
editor, NauDemo and unrelated submodules were not changed by this capability.
