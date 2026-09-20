# Spec Delta

## Purpose

Provide production browser platform services for the non-rendering Nau runtime,
with one real DOM-backed window, observable readiness and safe threaded disposal.

## ADDED Requirements

### Requirement: Production browser platform discovery

The Emscripten minimal runtime SHALL discover its browser window manager through
the production PlatformApp module and service registration. The native Windows
backend and existing public window signatures SHALL remain compatible.

#### Scenario: Browser module supplies the real service
- **WHEN** the focused browser runtime loads its production static modules
- **THEN** platform service discovery finds the browser manager and can initialize
  its DOM-backed window without a substitute test implementation

#### Scenario: Native lifecycle remains supported
- **WHEN** the native minimal runtime loads PlatformApp and executes its lifecycle
- **THEN** it uses the Windows backend and passes its existing lifecycle assertions

### Requirement: One page-owned host window

The browser service SHALL bind exactly one connected HTMLElement selected by
configuration supplied before initialization, defaulting to `#nau-window`. It
SHALL preserve that window's identity and SHALL NOT create or delete the host.
Additional window requests SHALL return an empty result and an unsupported-operation
diagnostic without changing the active window.

#### Scenario: Existing element becomes the active window
- **WHEN** initialization resolves exactly one valid host
- **THEN** the ready service exposes a stable active window backed by that element
  and leaves its initial layout and visibility under page control

#### Scenario: Additional window is requested
- **WHEN** a caller requests another window after initialization
- **THEN** the request returns empty, emits a diagnostic and preserves the host

### Requirement: Observable platform readiness and failure

Platform initialization SHALL report success only after the host, browser event
callbacks and executor are usable. Missing or ambiguous hosts, an unavailable
browser manager and backend initialization errors SHALL produce a failed platform
service initialization result and a diagnostic. Partial initialization SHALL
release its resources and SHALL NOT leave a service worker waiting indefinitely.
This contract concerns the platform service result, not application startup policy.

#### Scenario: Host selection fails
- **WHEN** the selector matches zero elements, multiple elements or a non-HTMLElement
- **THEN** platform initialization fails with a diagnostic identifying host selection
  and no ready window is published

#### Scenario: Backend is missing
- **WHEN** browser platform initialization cannot discover its manager
- **THEN** it reports failure instead of silently treating initialization as successful

#### Scenario: Initialization fails after allocating resources
- **WHEN** backend initialization fails after its worker or callbacks are created
- **THEN** the failure result settles and partial resources are cleaned up safely

### Requirement: Actual CSS-pixel geometry

Window geometry SHALL use integer CSS pixels independent of device pixel ratio.
Window size SHALL report the layout border box and client size SHALL report the
client area. Size changes SHALL request the outer layout size and subsequent reads
SHALL report actual measured results, including constraints imposed by page CSS.

#### Scenario: Host is resized through the service
- **WHEN** a worker changes the size of an unconstrained host with padding and borders
- **THEN** a subsequent read reports the requested outer size and corresponding client
  area in CSS pixels

#### Scenario: Page changes or constrains layout
- **WHEN** page CSS changes the host size or clamps a requested size
- **THEN** subsequent geometry reads reflect the resulting browser layout

### Requirement: Element and document visibility are separate

The service SHALL report element display eligibility separately from document
visibility. Element visibility SHALL account for connection and ancestor
display/visibility state, without promising occlusion or intersection detection.
setVisible SHALL control host visibility while preserving layout; it SHALL NOT
override an ancestor's display policy. Document visibility SHALL be available to
subsequent runtime lifecycle integration without adding scheduling behavior.

#### Scenario: Host visibility is changed
- **WHEN** a visible host is hidden and shown through the window interface
- **THEN** element visibility follows those changes and its layout space is preserved

#### Scenario: An ancestor prevents display
- **WHEN** the host is set visible beneath a display:none ancestor
- **THEN** the service continues to report the element as not visible

#### Scenario: Document becomes hidden
- **WHEN** the browser changes document visibility while host styles stay unchanged
- **THEN** document visibility reflects that transition independently of host visibility

### Requirement: Defined browser window operations

Naming the window SHALL set the host accessible label without changing the document
title. Desktop position changes SHALL emit an unsupported-operation diagnostic and
leave host layout unchanged; position reads SHALL return the documented unavailable
value {0, 0}. The service SHALL NOT create a graphics context.

#### Scenario: Host is named or positioned
- **WHEN** a caller changes the window name and requests a desktop position
- **THEN** the accessible label changes, the document title and layout stay unchanged,
  and positioning reports its unsupported status

### Requirement: Wakeable worker execution and UI dispatch

The service SHALL retain a dedicated platform worker and execute DOM operations on
the browser UI thread. A completed synchronous window operation SHALL be reflected
by subsequent reads. Enqueued work SHALL wake an idle message pump; a nonblocking
pump SHALL return promptly and a supplied processing limit SHALL bound work batches.
UI dispatch SHALL NOT require the UI thread to wait synchronously on the worker.

#### Scenario: Work arrives at an idle worker
- **WHEN** another worker enqueues an invocation while the platform pump is waiting
- **THEN** the pump wakes and executes the invocation exactly once without an
  application stepping timer

#### Scenario: A worker accesses the DOM-backed window
- **WHEN** a worker performs a window mutation followed by a state read
- **THEN** DOM access runs on the UI thread and the read reflects the completed mutation

#### Scenario: Queue remains busy
- **WHEN** producers keep enqueueing while a pump has a processing-time limit
- **THEN** the pump returns after a bounded batch instead of waiting for queue exhaustion

### Requirement: Safe host loss and service disposal

Host removal after readiness SHALL report a failed browser status and a diagnostic
without silently rebinding. Disposal SHALL wake idle pumping, detach browser event
callbacks and account for accepted executor work and in-flight UI operations before
releasing their context. Accepted work SHALL complete or settle through supported
cancellation; it SHALL NOT strand awaiting tasks. New window operations after
closing begins SHALL be rejected with a diagnostic. Repeated disposal and releasing
retained executor references after disposal SHALL be safe. The page host SHALL
remain page-owned, and worker joining SHALL NOT block the browser UI thread.

#### Scenario: Page removes the host
- **WHEN** the page disconnects the ready service's host
- **THEN** browser status becomes failed, a diagnostic is emitted, and disposal remains safe

#### Scenario: Disposal races with outstanding work
- **WHEN** disposal starts with queued executor work and in-flight DOM operations
- **THEN** their completion or cancellation is accounted for before context release,
  callbacks are detached, and the worker terminates without a UI-thread join

#### Scenario: Idle or repeated disposal
- **WHEN** an idle service is disposed and disposal is requested again
- **THEN** the idle pump wakes, cleanup completes safely, retained references remain
  safe to release, and the host element is not deleted

### Requirement: Real-browser acceptance evidence

Acceptance SHALL exercise the production browser module and shared platform service
in Chrome on Windows using the pinned Emscripten SDK in Debug and Release. Evidence
SHALL include DOM behavior, readiness errors, worker dispatch, wake-up and disposal,
plus native minimal lifecycle regression results. The fixture SHALL provide pthread
isolation and a bounded timeout with structured failure output. Node-only tests or
framework compilation alone SHALL NOT satisfy browser platform acceptance.

#### Scenario: Platform acceptance is recorded
- **WHEN** validation is reported complete
- **THEN** recorded commands, tool versions and results demonstrate the browser
  scenarios in both configurations and the native lifecycle regression checks
