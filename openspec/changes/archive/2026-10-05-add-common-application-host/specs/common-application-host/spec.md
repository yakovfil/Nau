# Spec Delta

## Purpose

Provide a reusable application host that runs the same application delegate on native and browser platforms with explicit update phases, owned lifetime and checked lifecycle completion.

## ADDED Requirements

### Requirement: Shared application entry contract

The engine SHALL provide one owning application runner and delegate contract available to native and browser consumers. The same application entry source SHALL build for both platforms without platform-specific runner calls. The common contract SHALL not require concrete scene or renderer types, and a non-rendering consumer SHALL run without enabling those feature modules. Platform scheduling SHALL reuse the existing application lifecycle and production platform services.

#### Scenario: A shared non-rendering consumer runs on both platforms
- **WHEN** the same consumer entry and delegate sources are built for native and browser targets
- **THEN** both execute configuration, service setup, application startup, updates and cleanup through the common host without scene or renderer dependencies

#### Scenario: Feature services are supplied by an application
- **WHEN** a consumer registers optional scene or rendering services
- **THEN** those services participate in the existing lifecycle without requiring the common host to reference consumer content or concrete feature implementations

### Requirement: Explicit application update phases

The host SHALL expose separate pre-update and post-update application callbacks on the application owner thread. For an eligible game step, pre-update SHALL execute before the scene manager update call and post-update SHALL execute after that call, with the same elapsed-time value and at most one dispatch of each callback. Without a scene manager the callbacks SHALL retain this relative order. Post-update SHALL not imply completion of asynchronous scene work or GPU presentation. Application callbacks SHALL not execute before successful application startup or after Stop has been observed.

#### Scenario: Application modifies scene state before scene processing
- **WHEN** a running application changes an object in its pre-update callback
- **THEN** scene processing for that step observes the change and application post-update follows the scene manager call

#### Scenario: A non-rendering application updates
- **WHEN** a running application without a scene manager completes a game step
- **THEN** its pre-update and post-update callbacks each execute once in that order with equal elapsed-time values

#### Scenario: Pre-update requests Stop
- **WHEN** the pre-update callback requests Stop and returns
- **THEN** the host does not start the application's post-update callback or any subsequent application update callback, and cleanup proceeds

### Requirement: Legacy delegate source compatibility

Existing delegates implementing only the legacy application-step callback SHALL remain source-compatible and receive that callback once in post-update on each eligible step. The default explicit pre-update callback SHALL perform no application work. Overriding the explicit post-update callback SHALL replace default legacy forwarding; the host SHALL not independently invoke the legacy callback a second time. Existing low-level application lifecycle and borrowed browser runner callers SHALL remain supported.

#### Scenario: An existing delegate is rebuilt
- **WHEN** an existing delegate overrides only the legacy step callback and runs through the common host
- **THEN** that callback executes once after the scene manager update call without requiring source changes

#### Scenario: A delegate overrides both post-update forms
- **WHEN** a delegate overrides explicit post-update and the legacy step callback
- **THEN** only explicit post-update is dispatched by the host, and the legacy callback executes only if explicitly forwarded by the delegate

### Requirement: Checked asynchronous application startup

The host SHALL invoke application initialization notification and asynchronous application startup once after successful required service initialization, unless Stop has already been observed. Running status and application update callbacks SHALL require successful completion of application startup. Immediate or deferred startup errors SHALL retain diagnostics and initiate safe cleanup. While startup is pending, required executor, lifecycle and presentation progress SHALL continue without dispatching application update callbacks or counting application game steps.

#### Scenario: Startup waits for external work
- **WHEN** application startup remains pending on accepted asynchronous work
- **THEN** the browser remains responsive, required work can progress, and the host does not report Running or invoke application updates until startup succeeds

#### Scenario: Startup fails immediately or later
- **WHEN** application startup returns an error immediately or completes asynchronously with an error
- **THEN** the host reports the startup failure, never enters normal application updates and cleans up resources from completed and partial initialization

#### Scenario: Startup waits for initial presentation
- **WHEN** startup awaits a renderer's initial presentation without using application update callbacks
- **THEN** the required presentation and executor work can complete and startup can succeed

### Requirement: Host-owned delegate lifetime and cleanup

The owning runner SHALL retain the delegate through all startup, update and teardown operations that can reference it. Browser scheduling handoff SHALL not require caller-owned static storage. Delegate destruction SHALL occur exactly once after safe application and service teardown. Stop SHALL be idempotent, prevent later application work and allow already-started tasks to settle or cancel through supported mechanisms. A progress timeout SHALL not free state still used by unfinished work. Failure SHALL remain observable even if cleanup subsequently succeeds.

#### Scenario: Browser execution leaves the initial call stack
- **WHEN** the browser host yields to its event loop after accepting an owned delegate
- **THEN** later callbacks continue to access a live delegate until teardown completes, after which it is destroyed exactly once before final runtime exit

#### Scenario: Stop arrives during pending startup
- **WHEN** Stop is requested repeatedly while startup work remains pending
- **THEN** no later application phase or update begins, required cleanup progress continues, and the delegate remains alive until accepted work and teardown finish

#### Scenario: Cleanup reports an error
- **WHEN** an eligible shutdown operation fails
- **THEN** remaining eligible cleanup is attempted, the failure diagnostic is retained, and terminal success is not reported

#### Scenario: Native execution terminates
- **WHEN** the native host finishes an orderly stop or encounters a checked lifecycle failure
- **THEN** the runner returns zero for the orderly stop and nonzero for the failure after safe teardown

### Requirement: Platform scheduling and completion remain explicit

The common host SHALL support the existing default scheduling policy and an explicit presentation-driven policy. Native callers using existing defaults SHALL retain native timing behavior. Browser default scheduling SHALL retain the existing nominal fixed cadence, while presentation-driven browser execution SHALL use cooperative presentation callbacks and bounded elapsed time without suspension catch-up. Browser status and asynchronous Stop SHALL remain accessible through the existing runtime bridge. A cooperative browser invocation SHALL report eventual completion through terminal status and runtime exit rather than promise a synchronous C++ return with the eventual result.

#### Scenario: Existing browser defaults are used
- **WHEN** a consumer runs with the default browser scheduling policy
- **THEN** the existing fixed-cadence lifecycle, responsive control and cleanup contracts remain supported

#### Scenario: A presentation-driven consumer resumes
- **WHEN** a browser consumer selects presentation-driven execution and resumes after being hidden
- **THEN** updates follow presentation opportunities with bounded elapsed time and no catch-up burst, while asynchronous Stop remains responsive

### Requirement: Common host acceptance uses independent consumers

Acceptance SHALL exercise a shared-source consumer other than NauDemo on native and real-browser production services in Debug and Release. Coverage SHALL include both update phases, legacy forwarding, immediate and deferred startup failures, Stop during pending startup, cleanup failure and delegate lifetime across browser handoff. Scene-dependent tests SHALL verify phase ordering with the real scene manager. Minimal build checks SHALL demonstrate that the common host does not add scene or renderer dependencies.

#### Scenario: The common host is declared validated
- **WHEN** implementation acceptance is recorded
- **THEN** reproducible commands and results cover the independent consumer, real scene ordering, lifecycle failures, ownership and minimal dependency checks in addition to NauDemo smoke tests
