# cocos-ui-retirement Specification

## Purpose

Define the supported runtime, tooling, and distribution behavior after retiring the Cocos2d-backed UI implementation and its consumers.

## Requirements

### Requirement: Runtime and SDK independence from retired UI

Supported engine, module, application, and installed SDK builds SHALL configure, compile, and run without the retired UI module, Cocos2d sources, headers, libraries, or exclusive prebuilt dependencies. They SHALL NOT fetch or substitute Cocos2d implicitly. Installed public interfaces and templates SHALL NOT expose the retired UI API.

#### Scenario: Clean desktop build
- **WHEN** the supported desktop configuration is built from a clean output directory after retirement
- **THEN** its target and link graphs contain no retired UI or Cocos2d targets and ordinary scene rendering, update, and shutdown work without UI service registration

#### Scenario: Installed SDK consumer
- **WHEN** a fresh SDK installation is relocated and the empty project template is built against it
- **THEN** compilation and startup succeed without retired UI exports, headers, libraries, shaders, or source checkout paths

### Requirement: Explicit retirement of UI consumers

The distribution SHALL remove the Cocos-backed widget API, its dedicated sample and tests, GUI authoring and synchronization integrations, and UI translation paths. Retained tools SHALL NOT advertise creation or editing of the retired UI assets. When retained editor or conversion workflows encounter identifiable legacy UI content, they SHALL report it as unsupported without crashing or silently claiming a successful UI conversion. Existing asset files SHALL NOT be rewritten or deleted merely by encountering unsupported content.

#### Scenario: Editor starts without GUI authoring
- **WHEN** the editor starts and opens a supported non-UI project
- **THEN** the editor shell, scene viewport, and non-UI asset workflows remain usable, with no registered retired GUI editor or synchronization plugin

#### Scenario: Legacy UI content is encountered
- **WHEN** a retained editor or conversion entry point encounters an asset identified as belonging to the retired UI implementation
- **THEN** it reports the unsupported feature, preserves the input file, and does not load a missing UI module or report successful UI translation

### Requirement: Independent graphics features remain functional

Retirement SHALL preserve scene rendering, ImGui diagnostics, and the existing asset-backed screen-text API. Native and browser NauDemo SHALL retain their rotating scene and font-backed label. Minimal and scene profiles SHALL retain lifecycle behavior and freedom from desktop UI dependencies.

#### Scenario: Native rendering and text
- **WHEN** native NauDemo is built and run in Debug and Release
- **THEN** its scene and label render correctly, existing text acceptance checks pass, and normal close completes

#### Scenario: Browser and minimal runtime
- **WHEN** browser NauDemo and minimal runtime fixtures are built and exercised in Debug and Release
- **THEN** applicable existing rendering, text, startup, stop, and failure acceptance checks pass without Cocos2d dependencies

#### Scenario: Debug interface remains available
- **WHEN** an existing ImGui diagnostic interface is opened in a supported native application
- **THEN** it remains usable independently of the retired UI system

### Requirement: Retirement is reflected in current distribution and evidence

Current build instructions, module lists, SDK packaging, templates, and feature documentation SHALL reflect the retirement. Historical archives SHALL remain historical. Completion evidence SHALL identify affected repository revisions or working-tree identities, validation commands, results, and any unavailable checks; unavailable checks SHALL NOT be recorded as passes.

#### Scenario: Distribution is inspected
- **WHEN** a fresh package and its current documentation are inspected
- **THEN** retired UI artifacts are absent and removed features are documented without advertising their continued availability
