# portable-input Specification

## Purpose

Provide consistent keyboard and pointer input to engine applications on Windows and web, with defined frame state, focus behavior and safe platform lifetime.

## Requirements

### Requirement: Portable input service availability

An application that explicitly selects CoreInput SHALL receive one usable keyboard and pointer input service on Windows and web. Supported portable queries SHALL include held key and pointer-button state, pointer position and per-frame pointer movement. Unsupported browser input features SHALL report unsupported behavior explicitly rather than appearing to work with permanently empty state. Applications that do not select CoreInput SHALL retain their current module graph.

#### Scenario: Input is requested on either platform

- **WHEN** a Windows or web application starts with CoreInput selected
- **THEN** the service initializes with supported keyboard and pointer queries before ordinary application updates

#### Scenario: Input is not requested

- **WHEN** a minimal or non-rendering application omits CoreInput
- **THEN** its existing platform services and dependency graph remain usable without the input module

### Requirement: Consistent frame input state

The input service SHALL deliver platform events to a stable frame state on the application owner thread before the application's input-consuming update. A held key or pointer button SHALL remain held across eligible updates until release. Pointer movement SHALL be reported once for the eligible frame and SHALL not repeat in later frames without new movement. Invalid or unknown keys and buttons SHALL not alter supported states.

#### Scenario: Key remains held

- **WHEN** a key is pressed, several game updates occur and the key is released
- **THEN** the application sees it held during each intervening update and released on the next eligible update

#### Scenario: Pointer moves once

- **WHEN** the pointer moves between two eligible updates and then remains still
- **THEN** the first update receives that movement and later updates receive zero movement

### Requirement: Window-scoped focus and pointer capture

Windows input SHALL be associated with the active application window and browser input with the page-owned demo host. Browser keyboard controls SHALL activate only while the host owns focus; primary-button drag SHALL retain pointer movement until release or loss of capture. Focus loss, document hiding, host disconnection or loss of pointer capture SHALL clear held keys, buttons and pending movement before further application updates. Input event handling SHALL not suppress unrelated page interaction.

#### Scenario: Browser host gains and loses focus

- **WHEN** the user focuses the browser demo host, holds a movement key and then changes focus
- **THEN** the key moves the camera only while the host is focused and is no longer held after focus loss

#### Scenario: Drag ends outside the host

- **WHEN** the user starts a primary-button drag on the host and releases outside its bounds
- **THEN** the drag ends and later pointer motion does not rotate the camera

### Requirement: Input lifetime and failure handling

Platform input callbacks SHALL remain valid only while their service and host are live. Shutdown SHALL detach browser listeners, release pointer capture if owned, and prevent later callbacks from accessing disposed service state. Input initialization failure SHALL be observable and SHALL prevent successful application startup when CoreInput is required.

#### Scenario: Stop during active input

- **WHEN** Stop occurs while a key is held or pointer drag is active
- **THEN** input handlers detach safely and no subsequent event reaches released application state

#### Scenario: Required input cannot initialize

- **WHEN** the selected input service cannot bind to its active platform window
- **THEN** startup reports the input failure and follows checked cleanup instead of entering Running

### Requirement: Preserved portable press transitions

Portable input SHALL expose new key and pointer-button presses independently of the final held state of a frame. A press followed by release between updates SHALL remain observable once, and multiple new presses within documented finite capacity SHALL retain their count. Repeated down events while a control is held SHALL NOT count as new presses. Transition state SHALL be published on the application owner thread before input consumers, remain stable for that frame and not replay in later frames. Focus loss, document hiding, host loss and shutdown SHALL clear pending presses. Invalid controls SHALL not create transitions. Existing held-state and movement semantics SHALL remain unchanged.

#### Scenario: Press and release between frames
- **WHEN** a supported key or button goes down and up between consecutive publications
- **THEN** the next frame exposes one press while reporting the control released, and the following frame exposes no additional press

#### Scenario: Repeat and multiple presses
- **WHEN** a held key receives auto-repeat events followed by release and a second press before publication
- **THEN** exactly two new presses are exposed within capacity, regardless of repeat count

#### Scenario: Pending presses are cancelled
- **WHEN** focus is lost or Stop occurs before pending presses reach a consumer
- **THEN** those presses are discarded and cannot trigger feedback after refocus or shutdown
