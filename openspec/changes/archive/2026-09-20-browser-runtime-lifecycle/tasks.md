# Tasks

## 1. Shared service results and cleanup

- [x] 1.1 Preserve immediate and deferred independent service initialization results in ServiceProviderImpl; add native tests verifying errors propagate, started tasks settle and dependent initialization does not run after failure.
- [x] 1.2 Track instantiated services and completed initialization phases for partial cleanup; verify tests dispose partially initialized objects, invoke shutdown only for initialized services and preserve dependency order.
- [x] 1.3 Aggregate shutdown/disposal errors while continuing eligible cleanup and accounting for started tasks; verify immediate/deferred failure tests do not skip other disposal or release live task contexts.

## 2. Checked application lifecycle

- [x] 2.1 Add compatible checked application creation and unwind partial setup failures; verify configuration/module-setup failure tests return diagnostics and release created global resources without entering the game loop.
- [x] 2.2 Add pumpable checked startup and explicit lifecycle phases to the shared application; verify immediate/deferred startup errors never enter updates and legacy startup/step callers retain their signatures and safe failure behavior.
- [x] 2.3 Add latched Stop during startup using existing cooperative task contracts; verify a delayed initialization test prevents later phases/Running and cleans up once already-started work settles.
- [x] 2.4 Provide cleanup progress independently of game updates and reconcile service/runtime-registry disposal ownership. Extend the internal scene/main-loop lifecycle with a native scene cleanup-only pump for update and post-update continuation queues, preserving executor context without starting new game/component updates. Verify pending-work tests finish without duplicate disposal or stranded continuations; add and run a native Debug/Release regression that starts an asynchronous scene component update before Stop, releases it afterward and proves cleanup completes without additional game/component updates.

## 3. Browser driver and control bridge

- [x] 3.1 Add a reusable worker-owned lifecycle driver and independent browser lifecycle build target consuming the real shared application and production static PlatformApp; verify compilation/link inputs and successful real startup on an application worker.
- [x] 3.2 Implement ordered lifecycle snapshots, completed game-step counts and asynchronous idempotent Stop; verify browser tests observe state/count ordering, UI responsiveness and repeated Stop without duplicate cleanup.
- [x] 3.3 Protect bridge callback lifetime and final status delivery with explicit ownership; verify delayed-callback tests cannot access a destroyed application or overwrite a newer snapshot.
- [x] 3.4 Implement terminal failure/reload policy and platform host-loss handling; verify failure stops updates, cleanup status remains accurate and another start is rejected without creating a runtime instance.
- [x] 3.5 Report observed fatal aborts through the host bridge without invoking unsafe Wasm cleanup; verify an isolated intentional-abort fixture reports Failed with incomplete cleanup and a failing process/test result.

## 4. Timing, wake-up and stalled progress

- [x] 4.1 Implement monotonic 100 ms deadlines and wake integration for Stop/executor work; verify deterministic scheduling tests skip missed deadlines, queue wakes do not create extra steps and Stop interrupts idle waiting.
- [x] 4.2 Implement visibility-aware timing baseline resets and the browser-only elapsed-time cap; verify deterministic long-gap tests and real Chrome hide/show tests produce no catch-up burst or oversized update while native timing stays unchanged.
- [x] 4.3 Add configurable foreground lack-of-progress reporting with a 10-second default; verify a short-threshold pending-work fixture reports Failed/incomplete cleanup, excludes hidden time, then completes cleanup safely after work is released.

## 5. Integrated validation and documentation

- [x] 5.1 Extend the isolated Chrome runner with lifecycle success, immediate/deferred startup failure, creation failure, Stop-during-startup, pending-work and shutdown-error cases; verify structured results and a deliberate fixture failure are correctly distinguished.
- [x] 5.2 Run full real-application Chrome acceptance in Debug and Release with SDK 6.0.9; record every specification scenario, foreground 8–12 Hz measurements over five seconds, UI heartbeat results and real visibility transitions in validation.md.
- [x] 5.3 Run native service/application failure tests and existing native minimal lifecycle tests in Debug and Release; record results and resolve regressions introduced by shared lifecycle changes.
- [x] 5.4 Run affected browser platform and Wasm core regression suites in both configurations and compile affected desktop framework/platform targets within the recorded validation boundary; record results and distinguish existing unrelated desktop dependency failures.
- [x] 5.5 Update prerequisites.md, build.md and engine lifecycle documentation with tested commands, checked APIs, status/Stop integration, timing defaults and failure/reload behavior; verify commands match recorded builds and tests.
- [x] 5.6 Update the emscripten-build/minimal-app-web handoff with concrete lifecycle integration points and remaining sample/package work; verify no untested application delivery task is marked complete and run strict OpenSpec validation for affected artifacts.
