# Proposal

## Why

The deprecated `nau::string` and `nau::string_view` maintain a second string model backed by tiny_utf8, requiring conversions around APIs that already use standard strings. Completing this migration simplifies engine interfaces and dependencies while making Unicode operations explicit.

## What Changes

- **BREAKING** Replace the custom string and view classes with direct `std::string` and `std::string_view` use in engine APIs and maintained consumers; require coordinated rebuilds.
- Define engine text as UTF-8 bytes. Standard indexing, sizes, iteration and substrings use byte units; migrate callers requiring code-point operations to explicit Unicode helpers.
- Retain encoding conversion, validation, formatting and identifier-hash utilities, preserving supported values and exception-free Web conversion failures.
- Migrate modules, tools, editor, samples, NauDemo and generated templates, including formatting and encoding boundaries.
- Remove tiny_utf8 from supported build and SDK dependencies after its consumers are gone; retain UTF conversion and fmt support.
- Adapt regression tests and document the source/ABI migration.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `toolchain-standard-library`: require standard UTF-8 string storage and views, explicit Unicode operations, retirement of the custom classes and tiny_utf8 dependency, and coordinated consumer migration.

## Impact

Primary code is `NauEngineLite/engine/core/kernel/include/nau/string/`, its implementations, module and diagnostic interfaces, and native/Web string tests. Consumer changes span NauEngineModules, NauEditorPublic, NauSamples and NauDemo, including project templates and SDK exports. The string utilities directory remains useful; this does not replace fmt, redesign identifiers, introduce Unicode normalization or grapheme editing, or change authored asset formats.
