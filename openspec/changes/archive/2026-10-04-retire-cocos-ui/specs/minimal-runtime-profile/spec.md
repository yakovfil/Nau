# Spec Delta

## MODIFIED Requirements

### Requirement: Native and desktop coexistence
The minimal framework SHALL support isolated native Windows validation builds.
The full desktop framework and existing preset behavior SHALL remain compatible except for the explicitly retired Cocos-backed UI implementation and its dedicated consumers.

#### Scenario: Native validation
- **WHEN** the focused native minimal lifecycle suite is built in Debug or Release
- **THEN** it links the shared minimal framework with native compiler options and passes bounded lifecycle checks.

#### Scenario: Existing desktop selection
- **WHEN** an existing desktop preset is configured without minimal selection
- **THEN** it retains its remaining full-framework features without the retired UI dependency, dependency/toolchain settings and a valid sample entry point.
