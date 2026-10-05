## Purpose

Provide compatible asset archive construction and checked read-only filesystem access on native and browser runtimes without concrete feature-module dependencies.

## ADDED Requirements

### Requirement: Portable package access

The engine SHALL expose read-only filesystem access to uncompressed `nau-vfs-pack` archives on Windows and Emscripten. It SHALL preserve file bytes and paths, support file lookup, directory enumeration, independent seek/read positions and zero-length files, and retain backing storage while open files or streams need it. Write requests SHALL fail without modifying package data.

#### Scenario: One archive is read on both platforms
- **WHEN** a valid archive containing nested files is mounted on Windows and Emscripten
- **THEN** both expose the same paths, sizes and bytes and permit independent interleaved reads

#### Scenario: Mounted storage outlives its original owner
- **WHEN** the caller releases the input stream or unmounts the filesystem while a file stream remains open
- **THEN** the open stream remains readable until released and storage is reclaimed afterward

### Requirement: Checked package validation

Package opening SHALL return a diagnostic error for malformed or truncated headers/indexes, wrong container kind, unsupported version/compression, invalid numeric ranges, out-of-bounds entries, path traversal, duplicate normalized paths and file/directory conflicts. Validation SHALL be bounded by explicit limits and SHALL NOT depend on assertions or unchecked integer narrowing. A failed open SHALL NOT publish a partial filesystem.

#### Scenario: Invalid archive is supplied
- **WHEN** an archive has an overflowing offset, truncated payload, duplicate path or malformed index
- **THEN** opening fails in Debug and Release without an assertion, crash, unbounded allocation or partial mount

### Requirement: Compatible package construction

The host packaging tool SHALL accept an explicit manifest mapping source files to package paths and produce a deterministic uncompressed archive compatible with the existing Windows reader. Identical inputs and options SHALL produce identical bytes. The existing Windows package API and valid existing uncompressed archives SHALL remain usable.

#### Scenario: Writer and readers interoperate
- **WHEN** the tool builds an archive from an unchanged manifest twice
- **THEN** both outputs are byte-identical and both the portable reader and existing Windows reader retrieve the original input bytes
- **AND** a valid pre-change archive remains readable

### Requirement: Package construction failure is observable

Missing inputs, invalid manifest entries, read/write failures and unsuccessful final publication SHALL cause a nonzero tool exit with an identifying diagnostic. The tool SHALL clean up owned temporary files and SHALL NOT publish a partial archive or report an older archive as the result of a failed build.

#### Scenario: An input disappears after an earlier successful build
- **WHEN** a required source file is removed and packaging runs again
- **THEN** packaging fails and dependent delivery targets fail even if the previous archive still exists

### Requirement: Runtime and host tool dependency isolation

Portable runtime package access SHALL remain in the standalone engine without concrete modules. Building the host packer SHALL NOT require editor, OpenUSD, graphics, asset-import modules or the full application framework. Cross builds SHALL execute a host-native packer from a separate build, never a target WebAssembly executable.

#### Scenario: Browser assets are packaged
- **WHEN** the Emscripten demo is built with the documented host toolchain
- **THEN** asset packaging runs natively and the browser runtime links only its selected runtime dependencies
