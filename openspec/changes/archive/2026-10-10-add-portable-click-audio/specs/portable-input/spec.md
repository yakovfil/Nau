## ADDED Requirements

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
