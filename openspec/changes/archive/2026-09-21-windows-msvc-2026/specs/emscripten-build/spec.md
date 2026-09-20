# Spec Delta

## MODIFIED Requirements

### Requirement: Native minimal build coexistence

The build integration SHALL support a separate native Windows build of the shared minimal framework using the supported VS 2026/v145 MSVC baseline and preserve desktop configuration and dependency behavior under the replacement VS 2026 presets. Native minimal preset names SHALL remain available; retired VS 2022 desktop presets SHALL NOT be required for coexistence. Browser-only flags and dependency substitutions SHALL NOT leak into native targets. Browser configuration SHALL remain independent of the native VS installation and toolchain baseline checks.

#### Scenario: Native validation configuration
- **WHEN** the shared minimal framework is built in its native Windows configuration
- **THEN** it links with the VS 2026/v145 Windows toolchain without Emscripten flags and is available for the native lifecycle validation suite.

#### Scenario: Existing desktop build
- **WHEN** a supported replacement VS 2026 desktop preset is selected without the minimal browser profile
- **THEN** it retains its desktop configuration and dependency behavior, with no requirement for emsdk.

#### Scenario: Browser build has no native toolchain
- **WHEN** the documented browser prerequisites are present but VS 2026 is unavailable
- **THEN** browser configuration and build do not require native VS discovery or apply MSVC compiler-version checks to Emscripten.
