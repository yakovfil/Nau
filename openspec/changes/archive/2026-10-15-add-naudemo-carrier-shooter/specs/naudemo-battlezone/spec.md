# Spec Delta

## MODIFIED Requirements

### Requirement: Default packaged game scene

The root Windows and web launchers SHALL open the carrier-shooter scene by default in Debug and Release through the shared packaged application. Battlezone SHALL remain explicitly selectable with `battlezone`, and the original mesh/billboard scene with `original`, retaining their existing gameplay, camera and sound behavior. Both targets SHALL consume byte-identical prepared content for each selected scene. Selecting one scene SHALL NOT activate another scene's controllers. Existing non-rendering and legacy desktop entry paths SHALL retain their supported behavior.

#### Scenario: Normal launch
- **WHEN** either root launcher is run without a scene override
- **THEN** the production application displays the carrier-shooter scene

#### Scenario: Battlezone selected
- **WHEN** the user selects `battlezone`
- **THEN** the playable retro battlefield appears with its tank controls, score, lives and sound

#### Scenario: Original scene selected
- **WHEN** the user selects the documented original-demo option
- **THEN** the original animated meshes, billboard, free-camera controls, and click feedback operate without tank or shooter gameplay

### Requirement: Reproducible game acceptance

Acceptance SHALL cover Windows and a real browser in Debug and Release using the same prepared content. It SHALL include production screenshots establishing the reference-inspired composition and wireframe silhouettes, deterministic behavior checks for combat/score/lives/restart, actual non-silent sound output, focus/visibility recovery, resize and zero-drawable recovery, missing/corrupt content, and repeated Stop during play and pending startup. Native delivery SHALL run outside the checkout and web delivery under a nested URL without autoplay overrides. The default shooter and explicitly selected Battlezone and original scenes SHALL be exercised, and affected no-audio/non-rendering/legacy paths SHALL retain coverage. Evidence SHALL record commands, revisions, tool versions, archive hashes, visual tolerances and any unexecuted checks; observer counts alone SHALL NOT establish visible or audible success.

#### Scenario: Completion claimed
- **WHEN** this change is reported validated
- **THEN** all four target/configuration combinations have production Battlezone visual and gameplay evidence, audible output evidence, lifecycle results and default-shooter/original-demo regression results
