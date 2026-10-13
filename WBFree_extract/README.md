# WarBirds P-51D extraction

One aircraft extracted from the local `C:\WBFree` installation. The source files
are read only. This directory is independent of NauDemo.

## Result

- `extracted/P51D/P51D.obj`: highest-detail object `P51Dy`, 1,059 vertices and
  450 original polygons, grouped by 29 original part/condition IDs.
- `extracted/P51D/P51D.mtl`: original polygon colors and one texture material.
- `extracted/P51D/p51d.png`: decoded 128 x 256 texture; 12 polygons have texture
  bindings, with 49 UV coordinates.
- `extracted/P51D/preview.png`: four orthographic views with polygon colors.
  This preview does not render texture mapping.
- `extracted/P51D/manifest.json`: source hashes, bounds, counts and limitations.

Import the OBJ into a 3D editor with the MTL and PNG beside it. Coordinates retain
the game's native units; no meter scale has been inferred. No normals are supplied;
the importer can calculate flat normals from the polygons.

This is a static extraction, not a reconstruction of runtime visibility or
animation. All polygons in this detail object are retained, so conditional parts
can appear simultaneously. In particular, the propeller effect and a green
triangle below the aircraft are present. The triangle belongs to `part_9d`; its
runtime purpose is not established. Part IDs are preserved without assigning
speculative names. The other detail objects, rigging, flight parameters, collision
data, runtime lighting, back-face colors and material behavior are not exported.
Original n-gons are retained; triangulation depends on the importing application.

## Reproduce

Requires Python 3 and Pillow:

```powershell
python -m pip install Pillow
python WBFree_extract/extract_model.py --source C:\WBFree
```

The script selects `FreeHost Launcher 1.700/DEF3D.FH` and `DEF3DT.FH` when present,
otherwise `DEF3D.TRN` and `DEF3D.TEX`. Use `--output <directory>` to change the
destination. The selected P51D model bytes are identical between the original
and FreeHost geometry archives in this installation.

## Format notes

The decoder was derived by inspecting this installation's `WBD3D.EXE`.

- Encoded archives have an eight-byte interleaved key/seed header, followed by
  substitution-encoded data with a position-dependent key. Decoder routines are
  around virtual addresses `0x4b4950` and `0x4b5110` in that executable.
- Decoded archive headers and directories are big-endian: version 3, entry count,
  and 600 reserved 32-byte directory slots. Each entry has a 16-byte name and
  four 32-bit fields (offset, length, flags, unused). Offsets refer to the decoded
  stream. The archive payload starts at byte 19,208.
- Models have the `GSC1` signature and big-endian integers. The object graph root
  is at header offset 32. Object links are at offsets 42 and 54, the polygon root
  at 30, and the vertex-array pointer at 38. Object loader: `0x455940`.
- Vertex arrays have an eight-byte header with a 16-bit count at offset 2,
  followed by signed 32-bit XYZ triples. Polygon nodes contain three tree links,
  color bytes, a texture-binding offset, and 16-bit vertex indices starting at
  offset 40. Polygon loader: `0x455c10`.
- TXF contains a fixed texture directory and per-polygon binding records with
  texture index, vertex count and float UV pairs. OBJ V coordinates are flipped
  for its texture-coordinate convention.
- HTX is little-endian. Width, row stride, height and depth are at offsets 12,
  16, 20 and 24. The palette starts at 36 as 256 BGR0 entries. The pixel-data
  pointer is at 1060. This texture is uncompressed, eight bits per pixel.
  Texture loading routines include `0x455050` and `0x46e650`.

The script implements the layouts needed for this model, not every possible
WarBirds object or texture variant. A zero archive seed assumes the executable's
initial random-generator state; this model's archive uses a nonzero seed.

## Validation performed

Both geometry archive directories decoded and passed entry-bounds checks
(100 original entries, 166 FreeHost entries). P51D payload equality was checked.
The exported OBJ was reread and its 1,059 positions, 49 UVs, 450 faces, all vertex
and UV indices, and all material references were checked. The referenced PNG was
reopened and its dimensions verified. The four-view color preview was visually
inspected. Texture placement has not been independently checked in the game or a
third-party OBJ viewer.
