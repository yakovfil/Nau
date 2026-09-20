# Spec Delta

## Purpose

Run the real non-rendering Nau application lifecycle on a browser worker with
observable startup, timed steps, cooperative stop and terminal failure reporting.

## ADDED Requirements

### Requirement: Real worker-owned application lifecycle

The browser runtime SHALL execute shared application creation, initialization,
updates and cleanup on an application worker, retaining required platform and
background services. Page controls and status delivery SHALL NOT synchronously
wait for worker completion. Successful native lifecycle callers SHALL remain
supported without changing existing public application method signatures.

#### Scenario: Application starts successfully
- **WHEN** required production modules and services initialize successfully
- **THEN** the browser reports Running, real application updates execute on a
  worker, and the browser page remains responsive

#### Scenario: Native lifecycle is exercised
- **WHEN** existing native callers create, start, step and stop the minimal runtime
- **THEN** their successful lifecycle and update ordering remain supported

### Requirement: Startup results preserve all service failures

Checked startup SHALL preserve immediate and deferred creation, pre-initialization
and initialization failures, including failures from independent services.
Started independent tasks SHALL be accounted for before their objects are freed.
Failed prerequisites SHALL prevent dependent initialization and game updates.
Partial startup SHALL use cleanup appropriate to the phases actually completed.

#### Scenario: Independent initialization fails immediately
- **WHEN** an independent service returns an already-completed error
- **THEN** startup reports the phase/error, does not report Running and does not
  invoke game updates or dependent initialization

#### Scenario: Initialization fails asynchronously
- **WHEN** one started service fails while other initialization tasks are pending
- **THEN** the failure is retained, started tasks are accounted for, and partial
  resources are cleaned up without entering normal updates

#### Scenario: Application creation fails after allocating resources
- **WHEN** configuration or application setup fails after partial resource creation
- **THEN** the checked result reports failure and existing resources are safely
  unwound without requiring an initialized game loop

### Requirement: Observable lifecycle status

The runtime SHALL expose Starting, Running, Stopping, Stopped and Failed status,
a monotonically increasing completed game-step count and ordered status updates.
Failures SHALL identify their phase and diagnostic. Status SHALL distinguish
incomplete cleanup from completed cleanup. Startup and cleanup queue processing
SHALL NOT increment the game-step count. Delayed status delivery SHALL NOT access
destroyed runtime state or overwrite a newer snapshot.

#### Scenario: Status is observed across startup and stop
- **WHEN** a page observes a successful run followed by Stop
- **THEN** it receives ordered lifecycle status and an advancing count only for
  completed game updates, ending with Stopped and completed cleanup

#### Scenario: A callback arrives after teardown
- **WHEN** a previously scheduled status callback arrives late
- **THEN** it cannot access destroyed application state or replace a newer result

### Requirement: Nominal 100 millisecond cadence

Foreground game updates SHALL use a nominal 100 ms interval, independently of
executor work and control requests. Missed deadlines SHALL be skipped rather than
replayed. In the unloaded acceptance fixture, a five-second foreground interval
SHALL average between 8 and 12 completed updates per second. Long-running callbacks
SHALL NOT cause concurrent game updates to compensate for a missed deadline.

#### Scenario: Foreground application runs normally
- **WHEN** the unloaded application runs in a visible tab for five seconds
- **THEN** its completed update rate is within the acceptance range and page
  heartbeat/control processing continues

#### Scenario: Executor work arrives between deadlines
- **WHEN** queued work wakes the worker before the next game-step deadline
- **THEN** the work progresses without generating an extra game update

### Requirement: Best-effort background execution without catch-up

Hidden-tab execution SHALL be best-effort without a guaranteed update frequency.
On resumption or a detected long scheduling gap, the runtime SHALL discard missed
deadlines and reset its timing baseline. Browser game-update elapsed time SHALL
be nonnegative and at most the nominal 100 ms interval, so suspension is not
converted into an oversized update. Native timing policy SHALL remain unchanged.

#### Scenario: A backgrounded page resumes
- **WHEN** Chrome hides and later restores the runtime tab
- **THEN** execution resumes without replaying missed updates or passing a
  suspension-sized elapsed time to the next update

### Requirement: Cooperative idempotent Stop

Stop SHALL be asynchronous, idempotent and able to wake an idle application worker.
Stop during startup SHALL latch intent, prevent new initialization phases and
prevent transition to Running. Already-started work SHALL settle or use supported
cooperative cancellation before its resources are released. After Stop is observed,
no new game update SHALL begin; an update already executing can finish.

#### Scenario: Stop arrives during an idle interval
- **WHEN** the page requests Stop between game-step deadlines
- **THEN** the worker wakes for cleanup without waiting for the next game deadline,
  while the request returns without blocking the UI

#### Scenario: Stop arrives during startup
- **WHEN** Stop arrives while a controlled initialization task is pending
- **THEN** the runtime does not enter Running or start later initialization phases,
  and completes cleanup once already-started work settles

#### Scenario: Stop is requested repeatedly
- **WHEN** Stop is requested during cleanup or after completion
- **THEN** cleanup is not duplicated and completed state remains stable

### Requirement: Cleanup accounts for work and errors

Cleanup SHALL stop new game updates, continue required executor progress and
account for outstanding service tasks, platform operations and worker ownership.
Shutdown hooks SHALL apply to successfully initialized services, while disposal
SHALL cover all instantiated resources. Cleanup errors SHALL be reported without
skipping other eligible cleanup. Stopped SHALL be published only after successful
cleanup completes; a timeout SHALL NOT be treated as proof of completion.

#### Scenario: Stop encounters pending work
- **WHEN** accepted asynchronous work remains during Stop
- **THEN** cleanup progresses without the normal game cadence delay, does not
  strand awaiting tasks, and completes before Stopped is reported

#### Scenario: A shutdown hook fails
- **WHEN** a shutdown or asynchronous disposal operation reports an error
- **THEN** the error is retained, other eligible cleanup is attempted, and the
  terminal result is Failed with an accurate cleanup-completion indicator

#### Scenario: Native scene update is pending at Stop
- **WHEN** a native asynchronous scene component update starts before Stop and
  its pending work is released after Stop
- **THEN** cleanup pumps the required scene update and post-update continuation
  queues with the appropriate executor context, allows the started work to
  settle and completes without beginning new game or component updates
- **AND** scene/component ownership is retained until the pending work settles,
  with the behavior verified using the real scene lifecycle in Debug and Release

### Requirement: Terminal failure requires reload

A reported startup or runtime failure SHALL produce Failed and attempt safe
cleanup. Platform host loss SHALL be treated as runtime failure. Failed SHALL
remain terminal for the page instance even if cleanup later completes; another
start SHALL be rejected and retry SHALL require page reload. An observed fatal
runtime abort SHALL report failure without claiming cleanup that could not run.

#### Scenario: Running application loses its host
- **WHEN** the platform reports host disconnection during execution
- **THEN** the runtime stops scheduling updates, reports Failed with a diagnostic
  and performs safe cleanup

#### Scenario: Start is requested after failure
- **WHEN** the page requests another start after Failed
- **THEN** the request is rejected with reload-to-retry guidance and no new runtime
  instance is created

#### Scenario: Runtime abort is observed
- **WHEN** the host observes a fatal runtime abort
- **THEN** it reports Failed with incomplete cleanup rather than falsely reporting
  an orderly stop or attempting unsafe recovery inside the aborted runtime

### Requirement: Lack of progress is visible

The lifecycle SHALL report an identified phase and incomplete cleanup when its
configurable foreground lack-of-progress deadline expires. The default deadline
SHALL be 10 seconds. Hidden time SHALL NOT by itself trigger that deadline.
Reporting failure SHALL NOT free resources still used by unfinished work. If
cooperative work later settles, cleanup SHALL proceed while Failed remains terminal.

#### Scenario: Cleanup stalls then becomes able to finish
- **WHEN** controlled pending work exceeds the configured foreground deadline and
  is subsequently released
- **THEN** status first reports Failed with incomplete cleanup and later reports
  cleanup completion without changing the terminal failure into success

### Requirement: Application acceptance uses production services

Acceptance SHALL run the real shared application and statically registered browser
platform services in Chrome on Windows in Debug and Release with the pinned SDK.
It SHALL include lifecycle success/failure, UI responsiveness, real background
visibility transitions, Stop during startup and pending-work cleanup, plus native
regressions for shared behavior. Node-only or platform-service-only tests SHALL
NOT substitute for application lifecycle acceptance.

#### Scenario: Lifecycle implementation is declared complete
- **WHEN** lifecycle validation is recorded
- **THEN** reproducible commands and results cover the browser scenarios in both
  configurations and native regressions, without claiming sample/package delivery
