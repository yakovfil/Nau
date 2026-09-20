# Design

## Context

See proposal.md for motivation and scope. The existing sample CMake already
selects `app_sample_main_min.cpp` for the minimal profile and registers
`NAU_MINIMAL_MODULES`. The selected main ignores `loadModulesList()` errors and
uses a native startup/step/sleep loop. The browser presets select the minimal
profile, Ninja and isolated outputs, but top-level CMake unconditionally rejects
browser configuration before building that graph.

`NauMinimalRuntime.cmake` already names the minimal modules/dependencies and gates
desktop tools/tests. `engine/core/CMakeLists.txt` selects the minimal module set.
The top-level minimal path already skips desktop Python checks, tools, final
desktop install blocks and source-tree test-wrapper generation. These are existing
mechanisms to verify and connect, not a reason to build a second graph.

The completed browser-runtime-lifecycle change exposes
`runBrowserApplication(delegate)` and `Module.nauRuntime.status/stop()`. Its
independent fixture links real production services but has its own main and
injected services; it does not establish sample integration. Source changes are
currently uncommitted, so implementation evidence must identify HEAD plus dirty
prerequisite state honestly rather than inventing completed-change revisions.

## Goals / Non-Goals

**Goals:** one production sample entry point, one existing lifecycle owner, browser
preset builds through the normal engine graph, observable real sample acceptance,
and native coexistence. Prefer existing graph gates and runner infrastructure.

**Non-Goals:** new runtime APIs, a duplicate loop, fault-injection services in the
production sample, automatic shutdown of normal runs, renderer/asset integration,
in-page restart, staged packages or a finished delivery page/server. The acceptance
server is temporary test infrastructure with required isolation headers.

## Decisions

### Reuse the driver from the selected sample main

Define sample setup through `ApplicationInitDelegate`, with explicit successful
basic configuration and checked module loading followed by platform-window service
registration. Do not call desktop default-application initialization that pulls in
features excluded by the minimal profile. For Emscripten, main returns the result
of `runBrowserApplication(delegate)`. Keep a native branch using checked creation
and the existing startup/step/sleep behavior; handle failure without dereferencing
an empty application and preserve the successful native timing path.

Do not port the lifecycle fixture's injected services or replace sample main with
the fixture. A separate browser main would duplicate the entry-point selection
contract; a second loop would duplicate validated timing/cleanup ownership.

### Enable only the supported browser profile

Replace the obsolete unconditional rejection with actionable checks for the
supported Emscripten/minimal/static configuration. Preserve exact SDK validation;
reject browser intent with a non-Emscripten compiler and unsupported browser
desktop-profile combinations rather than silently selecting Windows behavior.
Reuse existing profile gates throughout top-level, dependencies, modules and
samples. Make browser sample selection explicit and keep native tests and runner
Python discovery out of ordinary browser configure/build prerequisites.

Use the shared browser option helper for consistent pthread/no-exception/static
settings. Carry the proven application-specific link settings from the lifecycle
fixture to the real sample: runtime exit enabled, prewarmed pthread pool of 12 and
main-browser-thread blocking disallowed. Keep these sample settings scoped to
Emscripten. The pool size is a tested initial configuration, not a new public API
or a general engine concurrency guarantee.

Preserve target name `MinimalAppSample` and the current per-preset `bin`/`lib`
outputs. Verify actual generated outputs before documenting loader paths. Do not
add staging or assume a separate worker filename: SDK 6.0.9 can embed worker
support in the loader. An independent probe or guard-bypass switch would leave
the real preset contract untested and is not the chosen route.

### Test the production output using a small host harness

Add sample acceptance helpers beside the existing browser probes, for example
`cmake/probes/minimal_app_web`, consuming the preset's existing build directory.
They must not configure a replacement C++ application or change production sample
behavior. Reuse isolated Chrome/CDP and loopback COOP/COEP handling from existing
browser runners where practical. Python/Playwright are explicit test dependencies,
not needed to compile the sample; invoke the runner directly against both builds.

The harness supplies the DOM host, configures Module before loader execution,
displays the current state/count, and forwards a button click to the existing Stop
bridge. Disable Stop until the bridge exists; retain final status after application
exit and show reload guidance. Observe the existing immutable snapshots without
maintaining a second synthetic game counter. Reuse the existing host onExit/onAbort
hooks and ensure no callbacks synchronously wait for worker completion.

Run these actual-sample cases in each configuration:

- Success: wait for Running and advancing completed steps, measure 8–12 Hz over
  five foreground seconds, check UI heartbeat and displayed count, then Stop via
  the page control and verify successful exit and completed cleanup.
- Real hide/show during success: use a second Chrome tab with Playwright focus
  emulation disabled, check resumed progress and absence of catch-up bursts.
  Retain the existing driver deterministic elapsed-time tests as complementary
  evidence; do not add instrumentation services solely to measure sample dt.
- Missing host: omit the element before loading the unmodified sample; verify
  Failed/startup diagnostic, zero updates, completed safe cleanup and nonzero exit.
- Host loss: remove the real host after updates begin; verify Failed, frozen count
  after observed failure, safe cleanup and nonzero exit.
- Across applicable cases, check sequence ordering, repeated Stop, stable final
  state and rejection of another start. Exercise Stop during cleanup by observing
  Stopping and issuing additional requests while that state is available; the
  lifecycle fixture separately retains controlled pending-work coverage.
- Deliberately violate a runner expectation against real sample output, requiring
  a nonzero runner result. Expected application failures pass only when their
  exact status, exit and cleanup assertions match. Timeouts, crashes and unrelated
  infrastructure errors must remain failures.

The existing 13-case lifecycle fixture remains responsible for controlled pending
startup/cleanup, aggregation, stalls and fatal abort injection. Rerun it as an
affected regression; it does not replace actual-sample acceptance.

### Coordinate build evidence without changing ownership

This change implements the build integration needed for the confirmed sample
scope. Record evidence cross-references for `emscripten-build` tasks 2.3, 3.2–3.5
and 5.1 when every criterion of those tasks is actually established. Refresh their
tracking only after verification; current planning does not mark them done.
Task 5.2 includes independent packages, so a successful sample build alone cannot
complete it. Leave staging tasks 4.1–4.3, relocation 5.4 and reproduction 6.2
pending. Task 6.1 also retains any unmet package/documentation criteria.

An isolated empty browser build directory is a clean sample-build check, not
proof of a fresh-checkout/environment walkthrough or relocation. Distinguish these
claims in validation.md and in the updated build/prerequisite guides.

## Risks / Trade-offs

- Enabling the root graph may expose configuration paths absent from standalone
  probes -> audit generated targets and compile/link commands, configure with
  desktop dependency paths unavailable, and fix only minimal-profile integration
  gaps within this scope. A newly required subsystem port needs a scope decision.
- Sample configuration could accidentally add desktop services -> use the minimal
  delegate, retain the explicit module/dependency lists and verify no renderer graph.
- Small sample changes could diverge native behavior -> keep successful native
  timing, build the actual native sample in Debug/Release and run focused lifecycle tests.
- Browser timing is sensitive to load -> use the existing unloaded five-second
  acceptance window and record measurements, alongside deterministic driver tests.
- The acceptance page could be mistaken for delivery -> label its test role and
  document that staged/copyable packages, missing-isolation delivery UX and hosting
  instructions remain owned by subsequent delivery work.
- Thread-pool/exit defaults differ from the tested fixture -> explicitly transfer
  the proven link settings and verify process exit, final snapshots and cleanup.

## Migration Plan

Implement checked sample setup and the Emscripten branch, connect the existing
browser presets to the minimal graph, then run actual-sample acceptance and native
regressions. Update commands, artifact inventories and ownership evidence only
after those runs. No data migration or deployment is involved. If integration
must be reverted, restore the guarded browser preset path and sample changes
without removing the separately validated lifecycle/platform implementations.
