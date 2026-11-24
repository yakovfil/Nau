# Tasks

## 1. Unicode contracts and helpers

- [x] 1.1 Capture pre-migration formatting, serialization and identifier-hash known answers for ASCII, non-ASCII and embedded-null inputs; verify the fixtures document native 64-bit and Web 32-bit expectations.
- [x] 1.2 Extend standard-string conversion and validation helpers for required UTF-8/16/32 and native-wide boundaries; verify round trips, invalid sequences, supplementary characters, empty input and embedded nulls in focused tests.
- [x] 1.3 Add explicit code-point operations required by current callers and move character-semantic tests to them; verify indexing/slicing/iteration and mutation results on mixed-width UTF-8, with documented bounds and failure behavior.

## 2. Kernel migration

- [x] 2.1 Migrate kernel public string/view interfaces, module loading and version/diagnostic consumers to standard types; verify kernel compilation and module/version/diagnostic tests, including explicit handling of nullable boundaries.
- [x] 2.2 Migrate formatting, split/comparison utilities, hash_string storage and associated traits/overloads; verify formatting and serialized known answers and unchanged explicit identifier hashes/equality.
- [x] 2.3 Audit migrated length/index/find/substr/iteration operations and borrowed view lifetimes; record the byte/code-point decisions and verify targeted regressions for any changed call-site logic.
- [x] 2.4 Adapt native runtime and exception-disabled Web string suites to the new APIs, retaining meaningful conversion and embedded-null coverage; verify focused tests pass on both targets.

## 3. Consumers and dependency retirement

- [x] 3.1 Migrate NauEngineModules module interfaces, implementations, tools and tests; verify affected module/tool builds and their relevant tests.
- [x] 3.2 Migrate editor, samples, NauDemo and generated project templates; verify their compile checks and search maintained sources for remaining qualified and unqualified custom string uses.
- [x] 3.3 Remove retired custom string declarations/implementations and includes, tinyutf8 build/export/discovery integration and unused bundled dependency; verify clean configuration and SDK inspection show no required tinyutf8 or retired string APIs.
- [x] 3.4 Update coding and migration documentation with byte semantics, Unicode/formatting replacements, nullable boundaries and coordinated rebuild instructions; verify documented examples use the migrated public interfaces.

## 4. Integrated acceptance

- [x] 4.1 Build clean Windows Debug and Release demo/runtime graphs and run packaged scene, logging, resize and shutdown checks; record commands and actual results.
- [x] 4.2 Build clean Web Debug and Release demo packages and run browser scene, logging and stop/cleanup checks with exceptions disabled; record commands and actual results.
- [x] 4.3 Rebuild editor Release and required tools, then create/open/compile a project under a Unicode path; verify assets load and module compilation and editor shutdown succeed.
- [x] 4.4 Build a freshly generated consumer against a relocated rebuilt SDK and exercise module loading; verify no source-tree or tinyutf8 fallback and compatible DLL interfaces.
- [x] 4.5 Record repository/toolchain inputs, test counts, results and any explicitly authorized exclusions in validation.md; verify the evidence covers all delta scenarios and distinguishes failures or unexecuted checks from passes.
