# Spec Delta

## Purpose

Provide a buildable minimal Nau sample that executes the real application lifecycle
in Chrome on Windows, exposes progress and orderly Stop, and coexists with native builds.

## ADDED Requirements

### Requirement: Actual minimal sample browser builds

The existing `web-minimal-debug` and `web-minimal-release` presets SHALL configure
and build the actual minimal sample with the pinned SDK and documented source
dependencies. The browser target SHALL select `app_sample_main_min.cpp` as its
single entry-point source, use the shared non-rendering runtime and statically
registered required platform module, and execute the application on a worker.
The presets SHALL retain separate build outputs and consistent threaded options.

#### Scenario: Both browser presets build the sample
- **WHEN** a developer activates the supported SDK and builds each browser preset
- **THEN** both configurations produce their own actual sample JavaScript/Wasm
  outputs, without the obsolete missing-lifecycle prerequisite rejection
- **AND** generated source/link inputs identify one selected sample main, the real
  minimal runtime and static platform registration with worker execution

#### Scenario: Desktop-only dependencies are unavailable
- **WHEN** the browser prerequisites are present but desktop dependency paths are unavailable
- **THEN** sample configuration and compilation do not require renderer, UI, VFX,
  DirectX, Qt, USD, shader tools, desktop generator packages or native libraries

### Requirement: Checked sample startup

The sample SHALL check required module and platform-service setup results and
use the existing checked lifecycle. A successful browser startup SHALL report
Running only after required services initialize. An unsuccessful startup SHALL
report Failed with a diagnostic and phase, perform safe partial cleanup and
return failure without entering game updates.

#### Scenario: Sample starts with a valid host
- **WHEN** the actual sample loads with a valid DOM host and required browser capabilities
- **THEN** it reaches Running on the application worker and begins real updates

#### Scenario: Required platform host is missing
- **WHEN** the actual sample starts without its required DOM host
- **THEN** it reports Failed with a startup diagnostic, never reports Running,
  performs no game updates and reports cleanup completion after safe teardown
- **AND** its application exit result indicates failure

### Requirement: Observable sample execution

The sample SHALL expose the existing ordered lifecycle status and completed-game-step
count to its host. A small acceptance page SHALL display status and count and
provide an enabled Stop control once the lifecycle bridge is available. The page
SHALL remain responsive while the real sample runs and during cleanup. Its count
SHALL reflect actual completed application updates, not a page-side simulation.

#### Scenario: Foreground execution is observed
- **WHEN** the unloaded sample runs in a visible Chrome tab for five seconds
- **THEN** the completed-update rate averages 8–12 per second, the displayed count
  advances, lifecycle snapshots remain ordered and page heartbeat/control processing continues

#### Scenario: Sample returns from the background
- **WHEN** Chrome hides and restores the sample tab
- **THEN** execution resumes using the existing visibility-aware lifecycle without
  replaying missed updates or passing oversized suspension elapsed time to updates

### Requirement: Sample Stop uses orderly cleanup

The sample host SHALL forward Stop through the existing asynchronous lifecycle
control. Stop SHALL not block the browser UI. No new game updates SHALL begin after
Stop is observed; repeated requests SHALL be safe. Stopped SHALL be displayed only
after successful cleanup completes, with the final count and cleanup result retained.

#### Scenario: User stops the running sample
- **WHEN** the user activates Stop while the sample is Running
- **THEN** it stops scheduling updates, completes real runtime/platform cleanup,
  reports Stopped with cleanup complete and returns a successful application exit result

#### Scenario: Stop is repeated during and after cleanup
- **WHEN** Stop is requested repeatedly while cleanup is active and after it finishes
- **THEN** cleanup is not duplicated, the final count/result remains stable and
  page interaction does not require waiting synchronously for the worker

### Requirement: Sample retains terminal failure policy

The sample SHALL preserve the existing lifecycle's failure and reload policy.
Runtime host loss SHALL stop new updates and report Failed with a diagnostic;
safe cleanup SHALL complete before its completion is claimed. A new start on the
same page after failure or normal stop SHALL be rejected with reload guidance.

#### Scenario: The running sample loses its host
- **WHEN** the actual DOM host disconnects during sample execution
- **THEN** the sample reports Failed, stops advancing completed updates after failure
  is observed and completes safe cleanup without changing the terminal result to Stopped

#### Scenario: Retry is requested on a completed page
- **WHEN** the host requests another start after Failed or Stopped
- **THEN** no new application instance is created and the host receives reload-to-retry guidance

### Requirement: Native sample coexistence

The native minimal sample SHALL remain buildable using its Windows platform path
and existing running-loop timing. Browser control code, SDK discovery and browser
link options SHALL not leak into native builds. Existing desktop sample entry-point
selection and preset behavior SHALL remain supported.

#### Scenario: Native minimal builds follow browser builds
- **WHEN** the native minimal sample is built in Debug and Release alongside the browser builds
- **THEN** it uses the Windows toolchain without browser options, and the shared
  native lifecycle regression suite continues to pass

### Requirement: Acceptance identifies the actual sample and its boundary

Acceptance SHALL run the executable produced by the actual sample presets in
Chrome on Windows in Debug and Release with the pinned SDK. Structured results
SHALL distinguish successful application completion, expected sample failure and
test/infrastructure failure. The results SHALL identify the sample source/link
inputs and document reproducible build/test commands. Independent lifecycle
fixtures SHALL not substitute for sample acceptance, and build-directory tests
SHALL not be reported as staged-package, relocation or clean-checkout delivery acceptance.

#### Scenario: Sample integration is declared complete
- **WHEN** validation for this change is recorded
- **THEN** both actual sample configurations cover startup, observable execution,
  visibility, Stop, startup/runtime failure and native coexistence
- **AND** the evidence explicitly identifies package staging, delivery hosting and
  relocation work still pending in their owning changes

#### Scenario: The acceptance check fails
- **WHEN** an expected sample result or runner assertion is deliberately violated
- **THEN** the acceptance runner exits unsuccessfully with a diagnostic rather
  than treating the unexpected result as an expected application failure
