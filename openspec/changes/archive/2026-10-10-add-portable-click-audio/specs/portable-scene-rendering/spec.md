## MODIFIED Requirements

### Requirement: Explicit portable rendering profile

The packaged project workflow SHALL offer an opt-in `basic-rendering-scene` profile for Windows and web in Debug and Release using the same application entry and project component sources. One project declaration SHALL define the profile, logical modules, supported components, startup configuration and rendering content policy for both targets. The rendering profile SHALL permit explicitly declared optional CoreInput and Audio modules on both targets. Audio selection SHALL enable portable one-shot playback without requiring legacy spatial audio components or enabling the full desktop graph. The existing non-rendering profile, minimal applications, native full-rendered project and native/browser NauDemo SHALL retain their supported behavior. Applications omitting Audio SHALL acquire no audio backend dependency. Browser runtime targets SHALL NOT link desktop rendering binaries, USD or Qt. Unsupported declarations SHALL fail with identifying diagnostics.

#### Scenario: Rendering and non-rendering builds coexist

- **WHEN** the project builds both profiles for Windows and web
- **THEN** rendering deliveries display supported scene content, non-rendering deliveries retain their rendering-free graph, and their target and delivery outputs remain isolated

#### Scenario: Supported input module is requested

- **WHEN** a rendering declaration includes CoreInput on Windows or web
- **THEN** its packaged application starts with the input service available and uses the same authored archive as a rendering delivery without CoreInput

#### Scenario: Supported audio module is requested

- **WHEN** a rendering declaration includes Audio on Windows or web
- **THEN** its packaged application exposes portable one-shot audio with checked lifetime and browser activation where required

#### Scenario: Audio is omitted

- **WHEN** a rendering, minimal or non-rendering application does not select Audio
- **THEN** it retains its supported behavior without acquiring audio services or backend dependencies

#### Scenario: Unsupported module is requested

- **WHEN** the rendering declaration requests a module outside its supported set
- **THEN** both target builds reject it without silently omitting the module or enabling the full desktop graph
