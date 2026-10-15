# Tasks

## 1. Deterministic benchmark content

- [x] 1.1 Add benchmark scene generation, shared cube mesh/material, configuration and project declaration; verify exactly 1,024 unique cube component identities, 32 by 32 positions, shared geometry/material and identical repeated generated output.
- [x] 1.2 Integrate benchmark preparation with native/web build scripts and packaged glyph inputs; verify unchanged preparation hashes agree and missing/corrupt required geometry or glyph data fails with an identifying path.

## 2. Frame measurement and presentation

- [x] 2.1 Implement the timestamp-driven one-second cadence accumulator; test steady and irregular intervals, reciprocal frame time, initial pending state, invalid timestamps, reset and genuine long stalls without averaging reciprocal samples.
- [x] 2.2 Register benchmark-only observer/shared lifetime state and the forwarding backend decorator; verify samples count only successful submissions, reset on focus/visibility/zero-drawable/resize recovery, and preserve backend errors and failure injection.
- [x] 2.3 Add the benchmark scene component with fixed angled framing and cached vector statistics overlay; verify all cubes fit wide/tall viewports, text updates after full sample windows and cube/camera transforms stay stable between resizes.
- [x] 2.4 Isolate generic camera and click behavior from benchmark and clear state on scene removal/Stop; verify movement/drag cannot change the view and removed components are never accessed by observers.

## 3. Launch and build compatibility

- [x] 3.1 Add benchmark routing and usage text to both root launchers; extend launcher tests to cover benchmark, unchanged default and existing selections, plus invalid arguments.
- [x] 3.2 Add focused unit/probe targets following packaged_project.cmake conventions; verify Windows and web compile, accumulator tests run natively and under Node, and affected non-rendering/legacy component compilation remains supported.

## 4. Production verification and documentation

- [x] 4.1 Run Windows and real-browser Debug/Release benchmark packages; record shared prepared-content hashes, visible grid/HUD captures, 1,024 submitted identities, shared geometry and unchanged transforms across frames.
- [x] 4.2 Exercise wide/tall resize, focus/visibility and zero-drawable recovery, scene removal, repeated Stop during startup/play and missing/corrupt content; verify pending-to-fresh statistics, checked diagnostics and clean shutdown.
- [x] 4.3 Run affected shooter/Battlezone/original launcher and presentation regressions, including any shared HUD helper; document passed checks and explicitly identify unexecuted variants.
- [x] 4.4 Document Release benchmark commands, static workload, averaging formula, drawable dimensions/DPR and pacing limitations; deliver an evidence summary with revisions, tool/device/browser details and measured rates without a universal FPS pass threshold.
