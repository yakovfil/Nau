# Spec Delta

## MODIFIED Requirements

### Requirement: Exact minimal entry-point selection

The browser target SHALL use `minimalApp/app_sample_main_min.cpp` from the selected external NauSamples checkout as its entry-point source and SHALL link exactly one application entry point. It SHALL consume the dedicated minimal framework shared with native validation rather than a mock runtime.

#### Scenario: Both existing sample sources are present
- **WHEN** the sample directory contains both existing source files defining an entry point
- **THEN** the browser target selects the requested minimal source without linking the other entry point.
