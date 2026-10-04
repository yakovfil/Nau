# Spec Delta

## ADDED Requirements

### Requirement: Engine-rendered packaged font label

Native and browser NauDemo SHALL display the single line "Nau Demo" in white at logical position (24, 24) using size 24 and the same redistributable TTF asset through the shared engine text contract. The label SHALL be part of the rendered scene surface and SHALL NOT be produced by an OS child label, page text element, or system-font substitution. Required font initialization SHALL complete before startup reports ready. Browser packages SHALL preload the font into the demo asset mount, contain its license and inspection copy, record its hash, and remain relocatable. Staging SHALL reject missing required font/license inputs; runtime loading/upload failure SHALL report a diagnostic rather than a successful demo with an omitted label.

#### Scenario: Native and browser display the label
- **WHEN** native and browser Debug/Release NauDemo start with their required assets
- **THEN** the actual rendered surface contains the selected font's "Nau Demo" glyphs at the required logical position/size alongside the rotating cube

#### Scenario: Package is moved or font is missing
- **WHEN** a browser package is relocated and served under a nested base, or a required font input is absent
- **THEN** the relocated intact package resolves its own font and renders the label, while missing font input fails staging or startup diagnostically without system-font fallback

#### Scenario: Font provenance and lifecycle are accepted
- **WHEN** acceptance runs both configurations on native Windows and in Chrome
- **THEN** evidence checks actual render-surface pixels against the packaged font's glyph coverage, verifies a changed specified font changes output, covers resize/browser pixel ratio and orderly Stop, and retains existing cube rendering and lifecycle checks
