# Implementation progress

Task 1.1 completed: self-contained selected OBJ/MTL inputs, hash provenance and four-view previews are in NauDemo/content/reference/warbirds. The medium external aircraft variants preserve original face colors from decoded source data. Retractable wheel groups are excluded from P38 (91/93/95 hex), ZERO21 (92/94) and G4M2 (91); D3A2 retains fixed undercarriage. CBSINK uses the user-specified source unchanged. Aircraft and carrier previews were inspected.

Task 1.2 is complete. The converter writes checked triangulated USD color batches for the existing host-to-glTF pipeline. The user approved documented carrier repairs on 2026-10-15. The unchanged curated CBSINK.obj contains these four repaired records:

- Line 2201: `f 990 991 991`, only two distinct vertices.
- Line 2207: another face with only two distinct vertices.
- Lines 2657 and 2921: nine-vertex polygons which the projected ear-clipping triangulator cannot resolve.

The source OBJ remains unchanged. The converter omits the two zero-area records and reorders the two self-crossing island polygons along their visible perimeter, recording exact tokens and output counts. Four asset regression tests pass.

The shooter is implemented as the default scene with P38, three enemy types, six waves and automatic CBSINK launch/recovery. Battlezone and original remain explicitly selectable. All four production platform/configuration combinations, content faults, lifecycle checks and existing-scene regressions have passed. See `NauDemo/content/reference/warbirds/VALIDATION.md` for evidence, commands and the explicitly unexecuted full legacy desktop run. No engine or modules source changes were required.
