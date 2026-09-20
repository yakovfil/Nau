# Spec Delta

## Purpose

Deliver the real minimal Nau browser sample as a portable folder with clear launch
requirements, local serving instructions and verified execution after relocation.

## ADDED Requirements

### Requirement: Complete configuration-specific delivery folders

Each browser configuration SHALL produce a separate delivery folder containing
the actual sample's required runtime files, launch page, local server and usage
instructions. Staging SHALL use the current supported SDK output contract, fail
when required inputs are absent, and exclude obsolete files from previous staging.
The folder SHALL run without checkout, SDK or build-tool access. Runtime loading
SHALL not require external debug-symbol or source files.

#### Scenario: Debug and Release packages coexist
- **WHEN** both supported browser presets are built
- **THEN** each produces its own complete delivery folder without overwriting the
  other configuration or relying on stale outputs

#### Scenario: Staging replaces an older inventory
- **WHEN** staging runs with obsolete artifacts in its owned destination
- **THEN** the resulting inventory contains only the current runtime and delivery
  files and matches the required file set produced by clean staging

#### Scenario: A required staging input is missing
- **WHEN** a runtime file required by the selected SDK is absent
- **THEN** staging fails with an identified missing-input diagnostic and does not
  report the incomplete package as successfully produced

### Requirement: Prerequisites are checked before runtime loading

The launch page SHALL verify secure-context availability, cross-origin isolation
and required threaded-WebAssembly browser facilities before loading the runtime.
Unsupported hosting SHALL produce a visible diagnostic and concrete serving
guidance, keep Stop unavailable and avoid starting the application. No implicit
single-threaded fallback SHALL be provided.

#### Scenario: Isolation headers are absent
- **WHEN** the page is served without the required isolation configuration
- **THEN** it displays an isolation/serving diagnostic before requesting the
  application loader, Wasm or worker resources

#### Scenario: The page is opened as a local file
- **WHEN** the user opens the launch page through a file URL
- **THEN** it directs the user to the packaged local-server command instead of
  attempting an unsupported runtime launch

### Requirement: Runtime loading failures remain visible

The launch page SHALL report loader or Wasm loading/initialization failures visibly
and preserve the diagnostic until reload. A failure before the lifecycle bridge
exists SHALL not leave the page displaying indefinite normal startup or claim an
orderly application cleanup. The page SHALL retain the runtime's fatal-abort and
reload policy once runtime initialization begins.

#### Scenario: The application loader is missing
- **WHEN** the page passes its prerequisite checks but the loader request fails
- **THEN** it reports a load failure, keeps Stop unavailable and provides reload
  or package-repair guidance without reporting Running or Stopped

#### Scenario: The Wasm file is missing
- **WHEN** the loader starts but its required Wasm resource cannot be loaded
- **THEN** the page reports failure without claiming successful startup or cleanup

### Requirement: Delivered controls expose the real lifecycle

The delivered page SHALL show actual ordered runtime status, completed updates,
diagnostics and cleanup state, and SHALL forward Stop asynchronously to the existing
application lifecycle. Final state SHALL remain visible after exit. Failure SHALL
remain terminal, and another run after failure or normal stop SHALL require reload.

#### Scenario: A copied application is run and stopped
- **WHEN** a supported browser loads the copied package and the user activates Stop
- **THEN** the real application reaches Running, its visible count advances while
  the page stays responsive, and Stop leads to completed cleanup before Stopped
- **AND** repeated Stop does not change the final count or duplicate cleanup

#### Scenario: The runtime reports failure
- **WHEN** the running application loses its platform host or reports fatal abort
- **THEN** the page retains Failed and its diagnostic, accurately reflects whether
  cleanup completed and presents reload guidance without attempting runtime recreation

### Requirement: Packaged local serving

The delivery folder SHALL include a local server executable with documented Python
standard-library requirements and no dependency on repository modules or automation
packages. It SHALL serve only its selected package directory on loopback by default,
support a configurable port and URL base, send the required isolation headers and
correct runtime MIME types, and report its launch URL and startup errors clearly.

#### Scenario: Serving a copied directory
- **WHEN** the documented server command runs from a copied package with Python
  available and no SDK or engine checkout in its environment
- **THEN** the launch URL serves the package with COOP same-origin, COEP require-corp
  and Wasm content type application/wasm

#### Scenario: A port is unavailable
- **WHEN** the requested local server port is already occupied
- **THEN** startup fails with an actionable port diagnostic and unsuccessful exit

### Requirement: Relocated resource loading is self-contained

The complete delivered application SHALL run from a nested URL base after copying
outside the checkout. Required page, loader, Wasm and worker requests SHALL resolve
within the copied package; the application SHALL not fetch resources from original
checkout/SDK paths or external runtime hosts. Embedded worker support SHALL remain
supported without imposing a fixed separate worker filename.

#### Scenario: Both configurations run under a different URL base
- **WHEN** each copied package is served under a nested URL using the packaged server
- **THEN** its real worker application starts, updates and stops successfully and
  its recorded resource requests require no original source, SDK or debug-symbol files

### Requirement: Delivery acceptance records real browser behavior

Acceptance SHALL run the delivered files and server in Chrome on Windows for Debug
and Release. It SHALL verify five-second foreground cadence of 8–12 completed
updates/second, UI responsiveness, real hide/show without catch-up bursts, orderly
Stop, terminal failure and negative hosting/loading cases. Unexpected application,
server or runner failures SHALL fail acceptance. Native shared lifecycle regressions
SHALL remain passing. Copied-package evidence SHALL not be labeled fresh-checkout
or fresh-environment build reproduction.

#### Scenario: Delivery is declared validated
- **WHEN** completion evidence is recorded
- **THEN** it identifies source state, tool versions, package inventories, exact
  commands, relocated URLs, resource requests and scenario outcomes in both configurations
- **AND** it records native regressions and separately identifies any unmet
  fresh-checkout/environment reproduction requirement

#### Scenario: The runner encounters an unexpected result
- **WHEN** an assertion is deliberately violated or an unexpected resource/server failure occurs
- **THEN** the acceptance runner returns a nonzero result and a diagnostic rather
  than accepting the event as an expected negative-case outcome
