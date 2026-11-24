# Design

## Context

See proposal.md for motivation. The current kernel string header wraps `tiny_utf8::basic_string<char32_t, char8_t, std::allocator<char>>`. Its size is bytes, length is code points, iterators and substrings operate on code points, and constructors accept multiple encodings. The custom view refers to a Nau string and maintains code-point offsets. This differs from a standard contiguous byte view and requires a lifetime audit during migration.

`nau::utils::format` already returns `std::string`; `string_conv.h` provides standard string/view conversion helpers. `string_utils.h` contains both standard and Nau overloads. `hash_string` caches an explicit size-dependent FNV-style hash and compares hashes; `StringHash` is for transient lookup. These utilities have distinct purposes and must not all be deleted with string.h.

The kernel links tinyutf8 and the standalone minimal dependency list includes it. Existing runtime string tests cover code-point mutation and slicing; Web migration tests cover embedded nulls, conversion, formatting, hashing and nullable inputs. Module manager interfaces, version formatting, diagnostics, module implementations and project templates still use Nau strings. The earlier toolchain-standard-library spec already requires preserved values and exception-free Web conversion failures; this delta adds the standard byte-string interface without weakening those guarantees.

## Goals / Non-Goals

**Goals:** Expose one standard byte-string model, preserve application text behavior through explicit Unicode operations, and remove the custom classes and their build dependency across maintained consumers.

**Non-Goals:** Unicode normalization, locale-aware collation, grapheme editing, changing identifier algorithms, changing asset formats, replacing fmt, replacing unrelated legacy third-party string types, or providing compatibility with old SDK binaries.

## Decisions

1. **Use std::string/std::string_view directly.** UTF-8 is the engine text convention. No permanent `nau::string` aliases or wrapper replacement: aliases would hide byte/code-point behavior changes and collide with existing standard overloads and specializations. `std::u8string` remains usable at explicitly typed encoding boundaries but is not the general public text type because current standard APIs and formatting primarily accept char bytes.

2. **Make Unicode intent explicit.** Retain and extend `nau::strings` conversion/validation utilities using the existing UTF conversion support. Provide named code-point count, iteration and slicing operations needed by migrated callers; express mutation through explicit decode/edit/encode when required. Specify offsets and bounds in each helper. Convert only at boundaries rather than transcoding every stored string. Checked conversion validates the complete input before publishing output; preserve the Web diagnostic-plus-empty failure contract. Ordinary standard string construction remains byte storage. Preserve null-to-empty behavior at actual nullable boundaries explicitly.

3. **Audit semantics along with types.** Migrate qualified and unqualified uses, includes, exported methods, overrides, traits, formatters, overloads and tests. For every affected length/index/find/substr/iterator operation, determine whether it represents bytes, ASCII syntax or Unicode code points. Map former .tostring() to the value or a view, and former encoding conversions to explicit helpers. Replace char8_t casts and u8 literal assumptions with deliberate byte bridges. Check borrowed view lifetimes and temporary formatting results; views must not survive their backing storage.

4. **Keep utilities with standard storage.** Route string formatting through existing `nau::utils::format`/fmt. Collapse duplicate split/comparison overloads and remove obsolete custom format/hash specializations. Back `hash_string` with std::string while preserving its existing unsigned UTF-8 byte hashing, size_t width, null termination behavior and equality contract. Preserve known answers separately for 32-bit Web and 64-bit native targets; do not unify their existing hash widths in this change. Ordinary unordered containers use standard transient hashes.

5. **Remove dependency integration after consumer migration.** Remove tinyutf8 linkage, discovery, minimal-profile and SDK export requirements, then remove the unused bundled dependency through the repository's actual dependency ownership mechanism. Verify no remaining maintained consumers before deletion; do not modify unrelated bundled libraries. Retain utf8cpp/no-exception conversion support and fmt. Remove string.h when its declarations and includes have migrated; retain the useful directory and headers.

## Risks / Trade-offs

- Silent character truncation from byte offsets -> audit semantic operations and add mixed ASCII/Cyrillic/CJK/supplementary-character regression cases.
- Changed borrowed view lifetime -> remove views into temporaries and test boundary ownership where relevant.
- Unicode filesystem regression -> preserve explicit native wide-path conversions and rerun Unicode editor/project checks.
- Changed hash values or embedded-null behavior -> record current known answers before replacing storage and test each supported word width.
- ABI changes across DLLs -> rebuild engine, modules, tools, editor and SDK consumers with compatible configurations; do not mix binaries.
- Reduced automatic validation -> document byte storage and validate at checked conversion or ingestion boundaries that previously relied on it.

## Migration Plan

Implement helpers and behavior regressions first, migrate kernel interfaces and utilities, then all maintained consumers and templates. Remove retired classes/dependency integration only after the complete graph is migrated. Update coding/migration documentation with replacements and rebuild instructions.

Validate focused native and exception-disabled Web tests, clean Windows Debug/Release and Web Debug/Release demo builds with runtime checks, affected module/sample/tool builds, editor Release Unicode project open/compile, and a generated consumer against a relocated SDK. Record exact commands, configurations, revisions, results and any explicitly authorized exclusions; do not count unexecuted checks as passes.

Rollback requires restoring the coordinated component revisions and rebuilding their SDK and consumers together. Authored project assets require no migration.
