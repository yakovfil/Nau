# Design

## Context

See proposal.md for motivation. The existing browser presets build the actual
sample with SDK 6.0.9, whose observed outputs are `MinimalAppSample.js` and `.wasm`;
the loader contains worker support and resolves files relative to its script URL.
`samples/minimalApp/CMakeLists.txt` has no package target. Its `bin` folder also
contains copied acceptance HTML, so copying that directory indiscriminately would
mix delivery and test artifacts.

The current host page unconditionally includes the loader and the test runner
provides its own temporary HTTP server. Neither tests packaged serving or early
isolation failure. The existing runtime bridge already provides ordered snapshots,
Stop, cleanup, abort observation and reload-only retry. No C++ lifecycle change
is needed. Relevant implementations are uncommitted; source evidence must retain
that distinction rather than inventing immutable prerequisite revisions.

## Goals / Non-Goals

**Goals:** a self-contained per-configuration folder, reproducible staging,
early hosting diagnostics, a usable launch page/server and acceptance against
copied delivery files. Preserve the existing sample, runtime bridge and native builds.

**Non-Goals:** arbitrary SDK output discovery, runtime recovery redesign, hosted
deployment, production web-server hardening, TLS setup, installation, compressed
distribution archives, service workers, and committing source for a fresh-checkout
walkthrough. The server is a documented loopback development utility.

## Decisions

### Stage a dedicated package during browser builds

Add an Emscripten-only `MinimalAppWebPackage` CMake target, included in the default
browser build and depending on `MinimalAppSample`. Produce
`build/web-minimal-{debug,release}/package`; keep the raw sample outputs in `bin`.
An always-run staging command is inexpensive for this milestone and ensures
editing delivery assets or injecting an obsolete staged file is handled even
when the executable does not relink. An optional packaging command alone would
leave ordinary preset builds short of the existing build contract.

Keep staging in a CMake script so sample compilation gains no system Python or
Playwright dependency. Define the pinned SDK runtime inventory from the verified
link outputs, using target-derived paths. SDK 6.0.9 currently requires the loader
and Wasm, with embedded worker support. Do not glob every file in `bin`, assume a
`.worker.js` filename, or carry arbitrary old sidecars forward. If supported link
options change the required inventory, update it with corresponding link/output
evidence; the existing SDK pin prevents silent adoption of another toolchain.

Validate all inputs before publishing. Build a fresh temporary sibling folder,
copy current required runtime files and delivery assets, and generate a manifest
with configuration, SDK version, relative filenames and hashes. Publish by replacing
only the owned package directory after validation. Reject an unsafe destination
such as the build root/source root or a path outside the intended build directory.
On failure, return nonzero and leave any earlier package explicitly identifiable
by its old manifest; do not label it as the new result. Tests use disposable
staging inputs for missing-input and replacement failures.

Expected package layout:

```text
package/
  index.html
  MinimalAppSample.js
  MinimalAppSample.wasm
  serve.py
  README.md
  manifest.json
```

Inline small page styles/bootstrap logic to keep the delivery asset set simple.
Store authored assets under `samples/minimalApp/web/`; tests live under a delivery
probe/helper directory. Neither generated files nor package output is committed.
Optional debug artifacts are not execution requirements. Debug information embedded
in Wasm or diagnostic strings naming source files is not itself a runtime fetch;
validate actual network requirements instead of banning all path strings in binaries.

### Separate page bootstrap state from runtime ownership

Preserve automatic startup on a supported page. Before inserting the loader script,
check HTTP(S)/secure context, `crossOriginIsolated`, WebAssembly, Worker and
SharedArrayBuffer availability. A file URL or missing isolation displays a clear
message with the packaged server command and required headers; it never inserts
the loader. Stop stays unavailable until the runtime bridge exists.

Create Module hooks before loading the script. Use script error handling for a
missing loader and the supported Emscripten abort hook for Wasm loading failure.
Display bootstrap failures as delivery failures with no claim that application
cleanup ran. Once available, show the existing bridge's state/count/error and
cleanup indicator; final exit must leave the final snapshot visible. Preserve
host hooks so fatal abort follows the driver's incomplete-cleanup policy.
Do not fabricate runtime snapshots, advance a JavaScript game counter, or call
back into aborted Wasm. Late page callbacks must not overwrite a recorded failure.

Keep a visible Stop button, disabled before readiness and after terminal cleanup,
plus reload guidance. Use accessible status text and keyboard-operable controls.
Production assets have no test scenario query switches or injected services;
negative tests manipulate only copied files, browser environment or DOM host.

### Include one standalone loopback server

Use Python 3 standard-library HTTP serving, with the package directory resolved
relative to `serve.py` rather than the caller's working directory. Define
`python serve.py --port 8000 --base-path /` as the default documented command;
allow `--port 0` for tests and a normalized nested path such as `/relocated/nau/`.
Print the actual URL after binding. Port conflicts return nonzero with guidance
to select another port. The server must not import repository helpers.

Serve only the package root, with COOP `same-origin`, COEP `require-corp`, explicit
`.wasm` MIME type and no-cache responses for this development workflow. Bound
path resolution to the selected root, reject traversal/out-of-base requests and
do not expose the parent checkout through directory mappings or symlink escapes.
Default to loopback; no LAN exposure or TLS provisioning is required. A generic
`python -m http.server` command is insufficient because it omits isolation headers.

Test missing isolation with an independent test-only server that deliberately
omits headers. Do not add an unsafe-header switch to the delivered server merely
for testing. Use the delivered server itself for positive and missing-file tests.

### Validate external copies rather than original build output

Copy each package into a temporary directory outside the entire Nau workspace;
assert this path boundary before use. Start the copied `serve.py` with an absolute
test Python path, a neutral working directory and an environment without SDK/build
tool variables. Serve under a nested base path. There is no runtime need to rename,
delete or disable the real checkout or SDK installations.

Use an isolated Chrome profile and the existing CDP/Playwright visibility approach.
Capture network requests/responses, including worker targets, and reject any
required HTTP(S) resource outside the copied package base or requests to original
checkout/SDK locations. Embedded blob/data worker bootstrapping is permitted;
any network resources it loads must remain package-local. Require successful
Wasm response/loading and actual worker startup, advancing steps and cleanup.
Serving only the copy and constraining requests demonstrates runtime independence
without destructive changes to the working environment.

Positive acceptance reuses the sample assertions: real Running, 8–12 Hz over five
seconds, UI heartbeat, real tab hide/show, no catch-up count bursts, Stop and repeated
Stop, completed cleanup and stable final status/reload policy. Test host loss on
the copied page and use existing lifecycle abort tests as complementary evidence
where no production fault injection is appropriate. Test delivered page handling
of abort with a controlled host-hook event, clearly labeled as a page integration
check rather than another claim of a real Wasm fatal-abort run.

Negative cases are absent isolation, file URL, missing loader, missing Wasm and
occupied server port. Missing-header tests assert zero loader/Wasm/worker requests.
Missing-file tests modify disposable copies only and assert an identified load
failure with no false Running/Stopped or cleanup claim. A deliberate runner
expectation violation must exit nonzero after reaching its intended check;
unrelated infrastructure failures do not count as successful negative tests.

### Coordinate completion evidence with emscripten-build

After verification, cross-reference the exact evidence for tasks 4.1–4.3, 5.2,
5.4 and 6.1 in `emscripten-build`. Those tasks may complete only when their full
criteria pass; refresh its scenario review as part of the handoff. Task 6.2 remains
pending until a separate genuine fresh-checkout/environment walkthrough is possible.
This change does not authorize commits, an archive or substituting an exported
dirty snapshot for that requirement. Record real source state and revisions.

## Risks / Trade-offs

- Stale build files could look like current runtime outputs -> pinned explicit
  inventory, clean owned staging and missing-input/stale-destination tests.
- Nested URLs can break worker or Wasm paths -> preserve script-relative loading
  and capture worker as well as page requests from external copies.
- The runtime may abort before the bridge exists -> install page error hooks
  before loader insertion and keep bootstrap failure reporting separate.
- Staging replacement could affect unrelated files -> fixed per-build owned paths,
  resolved containment checks and disposable boundary tests.
- Browser scheduling makes wall-clock tests noisy -> reuse unloaded five-second
  acceptance and deterministic lifecycle timing regressions without loosening criteria.
- A copied package might be mistaken for a reproducible source build -> separate
  relocation evidence from the still-pending clean-checkout requirement.

## Migration Plan

Add authored delivery assets and browser-only staging, validate the owned output
inventory, then execute external-copy acceptance and native regressions. Update
guides and package instructions from tested commands. Existing raw sample and
independent lifecycle fixtures remain usable. Rollback removes the package target
and delivery assets without reverting the already validated sample/runtime APIs.
No deployment or data migration is required.
