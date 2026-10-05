## MODIFIED Requirements

### Requirement: Independent demo browser builds

The project SHALL provide separate Debug and Release NauDemo browser builds using the recorded SDK and required source dependencies. They SHALL statically link the selected real runtime, scene, asset and renderer services with consistent threading support, isolated from native and minimal build caches. They SHALL NOT require desktop rendering binaries, Qt, USD, UI, VFX, physics or desktop shader tools. Asset archive creation SHALL use a separately built host-native packaging executable and documented host compiler prerequisites; that executable SHALL NOT be linked into the browser runtime.

#### Scenario: Both demo configurations build
- **WHEN** a developer builds both demo browser configurations with documented prerequisites
- **THEN** each produces an independent runnable demo package without desktop runtime binary inputs or modifying existing minimal outputs
- **AND** its asset archive is produced by the isolated host packaging build

#### Scenario: Required dependency is missing
- **WHEN** a required source dependency, host packaging toolchain or supported SDK is unavailable
- **THEN** configuration or build fails with an actionable diagnostic rather than substituting a host library into the browser runtime or installing dependencies implicitly

### Requirement: Complete relocatable assets and runtime

Each demo delivery SHALL contain its runtime artifacts, an engine asset archive containing cube mesh data, font, browser material/shaders and asset configuration, plus serving instructions and required license notices. Required resources SHALL resolve under the package serving base without original checkout or SDK access. The engine SHALL consume the archive through its portable package filesystem; Emscripten preload transport remains supported. Missing or corrupt required assets SHALL be diagnosed, and stale outputs SHALL NOT conceal missing inputs.

#### Scenario: Package is moved
- **WHEN** either package is copied outside the checkout and served under a nested URL with required hosting headers
- **THEN** the actual demo renders and stops successfully without source-tree or SDK-path requests

#### Scenario: Required asset is absent or corrupt
- **WHEN** the archive or a required mesh, buffer, font or material input is missing or malformed
- **THEN** packaging, staging or runtime initialization reports the identified input failure rather than using stale data or entering Running with substitute geometry
