# Spec Delta

## ADDED Requirements

### Requirement: Shared demo application host and update behavior

Native and browser NauDemo SHALL use one shared entry-point source and the engine's common owning application host. Cube rotation and screen-text submission SHALL use shared application pre-update behavior. Browser drawing SHALL run in application post-update after the scene manager update call. Platform-specific demo configuration, assets and renderer adapters SHALL remain supported without separate application entry points or duplicate updates. The migration SHALL preserve the full-viewport browser canvas, native and browser appearance, and existing shutdown behavior without reintroducing demo test hooks.

#### Scenario: Both demo targets are built
- **WHEN** native and browser NauDemo are built
- **THEN** each compiles the shared entry point and shared rotation/text behavior with its selected configuration and presentation adapter

#### Scenario: A demo game step runs
- **WHEN** NauDemo completes an eligible game step on either platform
- **THEN** its cube advances once and its text is submitted in pre-update before scene processing
- **AND** browser drawing uses that scene state from post-update without a second simulation update

## MODIFIED Requirements

### Requirement: Lifecycle-integrated rendering

The demo SHALL use the common application host over the shared checked lifecycle, with presentation-driven cooperative scheduling on the browser and existing native scheduling. It SHALL report Running only after required scene, asset and graphics initialization and application startup succeed. Rendering SHALL follow actual scene updates without independent page-side game simulation. Hidden-tab resumption SHALL preserve bounded elapsed time and skip missed updates. The page SHALL remain responsive and expose ordered status and asynchronous Stop through the runtime API, without requiring external HTML controls. Default minimal browser runtime cadence SHALL remain unchanged.

#### Scenario: Foreground execution and visibility
- **WHEN** the initialized demo runs, becomes hidden and returns to the foreground
- **THEN** real scene updates and rendering resume on presentation callbacks without catch-up rotation or suspension-sized elapsed time, and runtime controls remain responsive

#### Scenario: Application startup has not completed
- **WHEN** required demo scene, asset, graphics or application startup work is pending or fails
- **THEN** the host does not report Running or dispatch demo update callbacks, while required initialization and cleanup progress remains possible
