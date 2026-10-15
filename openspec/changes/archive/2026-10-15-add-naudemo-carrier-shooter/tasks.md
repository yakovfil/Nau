# Tasks

## 1. Curated extracted art

- [x] 1.1 Select coherent flight variants and conditional parts for P38, ZERO21, D3A2 and G4M2 plus the specified CBSINK; store curated inputs and a provenance/selection manifest in NauDemo, verifying hashes and top/oblique previews for all five assets.
- [x] 1.2 Implement deterministic conversion into portable single-primitive meshes and original-color materials, including axis/scale normalization and concave triangulation; verify valid indices/normals, malformed-input failures and identical repeated output hashes.
- [x] 1.3 Integrate generated asset metadata and preparation dependencies; verify preparation succeeds without C:\WBFree or the sibling extraction tree and changed/missing inputs regenerate or fail without stale output.

## 2. Deterministic sortie simulation

- [x] 2.1 Add phase progression and six authored finite wave schedules with validated population limits; test takeoff, all waves, escaped-enemy progression, safe recovery and mission complete.
- [x] 2.2 Add normalized bounded movement, shared held-fire cadence and swept projectile collision; test diagonal speed, simultaneous fire bindings, cadence across frame rates and fast projectile impacts.
- [x] 2.3 Implement fighter curves, diver sweeps/spreads and bomber aimed bursts with distinct health/score values; test each behavior, enemy expiry and maximum concurrent populations.
- [x] 2.4 Add damage protection, three lives, score-once events and terminal restart; test simultaneous hits, enemy collisions, game over and complete resets from both outcomes.

## 3. Shared scene presentation

- [x] 3.1 Register the shooter component and author the ocean scene, camera and bounded reusable model instances; verify scene activation/deactivation and visible coherent models through the existing renderer.
- [x] 3.2 Connect simulation transforms to player/enemy art, scrolling ocean and carrier takeoff/recovery; verify recognizable launch and landing, flight direction, wide/tall framing and maximum-load draw counts on Windows and web.
- [x] 3.3 Add projectiles, explosions and scene-owned score/lives/wave/control/terminal HUD; verify visible feedback and readable layout throughout the sortie and on resize.
- [x] 3.4 Connect portable input, pause/focus clearing and packaged fire/explosion events; verify held-fire behavior, browser gesture activation, non-silent output and no stale events after focus recovery or Stop.

## 4. Default routing and compatibility

- [x] 4.1 Set shooter startup as the default and retain dedicated Battlezone/original declarations; update both root launchers for shooter|battlezone|original and verify default, all explicit selections and invalid-argument diagnostics.
- [x] 4.2 Update tests that assumed default Battlezone to select it explicitly; run affected gameplay, input, audio and preparation regressions and verify controllers never cross-activate.
- [x] 4.3 Document controls, scene selection, asset provenance, flat-color rendering and reproduction commands; verify documented launcher/build commands match actual routing and content paths.

## 5. Production acceptance

- [x] 5.1 Add production shooter probes and acceptance checks following existing NauDemo patterns; verify real presented frames and gameplay outcomes cover takeoff, each enemy, damage, both terminal states, recovery and restart.
- [x] 5.2 Run Windows and real-browser Debug/Release acceptance with matching prepared-content hashes, including actual firing/explosion audio; record commands, revisions, tools, screenshots and results for all four combinations.
- [x] 5.3 Verify focus/visibility pause, resize/zero-drawable recovery, repeated Stop during startup/play, missing/corrupt inputs and deterministic preparation; record failures with identifying diagnostics and cleanup results.
- [x] 5.4 Verify relocated native and nested-URL browser delivery and all three scene selections, plus affected non-rendering/no-audio/legacy paths; deliver an evidence summary explicitly listing any unexecuted checks.
