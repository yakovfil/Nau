# Spec Delta

## ADDED Requirements

### Requirement: Standard UTF-8 string interfaces

Engine interfaces and maintained consumers SHALL use `std::string` for owned general-purpose text and `std::string_view` for borrowed text in place of the deprecated Nau string classes. Text SHALL use UTF-8, with standard string sizes, indexes and iteration measured in bytes. Supported builds and installed SDK consumers SHALL require neither the retired classes nor tiny_utf8. Migration documentation SHALL identify the source and ABI break and require matching rebuilt consumers.

#### Scenario: Standard string consumer
- **WHEN** a rebuilt application supplies standard UTF-8 strings to migrated engine interfaces
- **THEN** it compiles without custom string adapters or tiny_utf8 and retains the supplied text, including embedded nulls in length-delimited values.

#### Scenario: Multibyte text units
- **WHEN** a caller stores two three-byte Unicode characters in a standard engine text value
- **THEN** its standard size and length are six bytes and Unicode operations explicitly select code-point semantics.

### Requirement: Explicit Unicode operations after string migration

Unicode validation, encoding conversion and code-point operations required by migrated callers SHALL remain available explicitly. Callers previously relying on code-point indexing, slicing or iteration SHALL preserve their intended text results without splitting UTF-8 sequences. Checked malformed conversion SHALL report a diagnostic and return an empty result without partial output or requiring exceptions on Web. Standard byte storage itself SHALL NOT imply validation or automatic transcoding. Nullable external text inputs previously treated as empty SHALL be handled explicitly before constructing standard strings or views.

#### Scenario: Unicode round trip
- **WHEN** supported UTF-8 text containing supplementary characters and embedded nulls is explicitly converted through UTF-16 or UTF-32
- **THEN** the round trip preserves its complete value and length.

#### Scenario: Code-point slice
- **WHEN** a migrated caller requests a code-point slice across multibyte characters
- **THEN** explicit Unicode operations return the same complete characters as before migration.

#### Scenario: Malformed conversion on Web
- **WHEN** a checked conversion receives malformed UTF-8 or an invalid Unicode scalar sequence in an exception-disabled browser build
- **THEN** it emits a diagnostic and returns an empty result with no partial converted content.

#### Scenario: Nullable external input
- **WHEN** an external API supplies a null text pointer at a migrated boundary whose established behavior is empty text
- **THEN** the boundary produces empty text without passing the null pointer to a standard string constructor.

### Requirement: String migration value compatibility

Migrating string storage SHALL preserve formatting output, serialized text, asset and module lookup behavior, and existing explicit identifier-hash algorithms and equality behavior on each supported target. Transient standard container hashes SHALL NOT be used as replacements for persistent identifiers. Retained encoding, formatting and hashing utilities SHALL operate with standard string storage.

#### Scenario: Persisted values and identifier hashes
- **WHEN** representative ASCII, non-ASCII and supported embedded-null values are formatted, serialized and passed through retained identifier hashing
- **THEN** their outputs match recorded pre-migration values for the same target, without requiring transient container hashes to remain numerically identical.

#### Scenario: Unicode project runtime
- **WHEN** rebuilt native and browser applications load their packaged scenes and assets and a native editor opens a project under a Unicode path
- **THEN** lookup, text output, startup and normal shutdown retain their established behavior.
