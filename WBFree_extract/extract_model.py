"""WarBirds 2.77 asset decoding, reverse engineered from the supplied WBD3D.EXE."""

import struct
import argparse
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


def decode_archive(data):
    if data[:4] == b"\x00\x00\x00\x03":
        return data
    if len(data) < 8:
        raise ValueError("Truncated encoded archive")
    key = int.from_bytes(data[:8:2], "little")
    seed = int.from_bytes(data[1:8:2], "little")
    if seed == 0:
        seed = (((0x4233423F + 0x2D62F) ^ 0xC5C4B) * 0x1460F) & 0xFFFFFFFF
    table = list(range(256))
    for _ in range(10):
        for i in range(256):
            seed = (((seed + 0x2D62F) ^ 0xC5C4B) * 0x1460F) & 0xFFFFFFFF
            j = seed & 255
            table[i], table[j] = table[j], table[i]
    inverse = [0] * 256
    for i, value in enumerate(table):
        inverse[value] = i
    key = (key + 0xA9CFD9EF) & 0xFFFFFFFF
    result = bytes(inverse[((value - position) & 255) ^ ((key >> (position & 7)) & 255)]
                   for position, value in enumerate(data[8:], 8))
    if result[:4] != b"\x00\x00\x00\x03":
        raise ValueError("Decoded archive has an unexpected signature")
    return result


def extract_geometry(data, object_name):
    if data[:4] != b"GSC1" or struct.unpack_from(">I", data, 4)[0] != len(data):
        raise ValueError("Invalid GSC1 model")
    integer = lambda offset: struct.unpack_from(">i", data, offset)[0]
    pending, seen, selected = [integer(32)], set(), None
    while pending:
        offset = pending.pop()
        if offset == -1 or offset in seen:
            continue
        if not 0 <= offset <= len(data) - 76:
            raise ValueError("Object outside model")
        seen.add(offset)
        name = data[offset + 6:offset + 14].split(b"\0")[0].decode("ascii")
        if name == object_name:
            selected = offset
        pending.extend([integer(offset + 42), integer(offset + 54)])
    if selected is None:
        raise ValueError(f"Object not found: {object_name}")
    base = integer(selected + 38)
    count = struct.unpack_from(">H", data, base + 2)[0]
    vertices = [struct.unpack_from(">3i", data, base + 8 + 12 * i) for i in range(count)]
    pending, seen, faces = [integer(selected + 30)], set(), []
    while pending:
        offset = pending.pop()
        if offset == -1 or offset in seen:
            continue
        if not 0 <= offset <= len(data) - 40:
            raise ValueError("Polygon outside model")
        seen.add(offset)
        count = struct.unpack_from(">H", data, offset + 2)[0]
        indices = struct.unpack_from(f">{count}H", data, offset + 40)
        if count < 3 or any(i >= len(vertices) for i in indices):
            raise ValueError("Invalid polygon indices")
        faces.append(dict(offset=offset, flags=data[offset], part=data[offset + 1],
                          color=list(data[offset + 26:offset + 29]), indices=indices,
                          texture_offset=integer(offset + 36)))
        pending.extend(struct.unpack_from(">3i", data, offset + 4))
    return vertices, sorted(faces, key=lambda face: face["offset"])


def extract_texture(data, destination):
    size, pixel_bytes, flags, width, stride, height, bpp = struct.unpack_from("<7I", data)
    pixel_offset = struct.unpack_from("<I", data, 1060)[0]
    if size != len(data) or bpp != 8 or stride < width or pixel_bytes != stride * height:
        raise ValueError("Unsupported HTX layout")
    pixels = data[pixel_offset:pixel_offset + pixel_bytes]
    if len(pixels) != pixel_bytes:
        raise ValueError("Truncated HTX pixels")
    palette = [tuple(data[36 + i * 4:39 + i * 4][::-1]) for i in range(256)]
    image = Image.new("RGB", (width, height))
    image.putdata([palette[pixels[y * stride + x]] for y in range(height) for x in range(width)])
    image.save(destination)
    return [width, height]


def preview(vertices, faces, destination):
    """Orthographic color preview; OBJ/MTL carries the separate texture mapping."""
    image = Image.new("RGB", (1200, 900), "#17212c")
    draw = ImageDraw.Draw(image)
    views = [(35, 25, "Perspective direction"), (0, 90, "Above"),
             (90, 0, "Side"), (180, 0, "Front / rear axis")]
    for panel, (azimuth, elevation, label) in enumerate(views):
        a, e = math.radians(azimuth), math.radians(elevation)
        right = (math.cos(a), 0, -math.sin(a))
        up = (math.sin(a) * math.sin(e), math.cos(e), math.cos(a) * math.sin(e))
        depth = (-math.sin(a) * math.cos(e), math.sin(e), -math.cos(a) * math.cos(e))
        points = [tuple(sum(v[i] * axis[i] for i in range(3)) for axis in (right, up, depth))
                  for v in vertices]
        limits = [(min(p[i] for p in points), max(p[i] for p in points)) for i in range(2)]
        scale = min(540 / max(1, limits[0][1] - limits[0][0]),
                    350 / max(1, limits[1][1] - limits[1][0]))
        cx, cy = panel % 2 * 600 + 300, panel // 2 * 450 + 235
        center = [(lo + hi) / 2 for lo, hi in limits]
        for face in sorted(faces, key=lambda f: sum(points[i][2] for i in f["indices"]) / len(f["indices"])):
            polygon = [(cx + (points[i][0] - center[0]) * scale,
                        cy - (points[i][1] - center[1]) * scale) for i in face["indices"]]
            draw.polygon(polygon, fill=tuple(face["color"]), outline="#424b53")
        draw.text((panel % 2 * 600 + 20, panel // 2 * 450 + 20), label, fill="white")
    draw.text((20, 875), "P51D: original polygon colors; all conditional parts; texture shown separately in p51d.png", fill="white")
    image.save(destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("C:/WBFree"))
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "extracted/P51D")
    args = parser.parse_args()
    model_path = args.source / "FreeHost Launcher 1.700/DEF3D.FH"
    texture_path = args.source / "FreeHost Launcher 1.700/DEF3DT.FH"
    if not model_path.exists():
        model_path, texture_path = args.source / "DEF3D.TRN", args.source / "DEF3D.TEX"
    model_archive, texture_archive = model_path.read_bytes(), texture_path.read_bytes()
    model = archive_entries(decode_archive(model_archive))["P51D"]
    textures = archive_entries(decode_archive(texture_archive))
    txf = textures["P51D.txf"]
    vertices, faces = extract_geometry(model, "P51Dy")
    material_base, binding_base = struct.unpack_from(">2I", txf, 8)
    texture_count = struct.unpack_from(">H", txf, material_base)[0]
    texture_names = [txf[material_base + 2 + i * 24 + 8:material_base + 2 + (i + 1) * 24]
                     .split(b"\0")[0].decode("ascii") for i in range(texture_count)]
    args.output.mkdir(parents=True, exist_ok=True)
    dimensions = {}
    for name in texture_names:
        dimensions[name] = extract_texture(textures[name], args.output / (Path(name).stem + ".png"))
    obj = ["# WarBirds P51D / P51Dy; native coordinates, static conditional geometry", "mtllib P51D.mtl", "o P51D"]
    obj.extend("v %d %d %d" % v for v in vertices)
    materials, uv_count, textured_faces = {}, 0, 0
    for face in faces:
        material = "rgb_" + "".join(f"{c:02x}" for c in face["color"])
        materials[material] = "Kd " + " ".join(f"{c / 255:.6f}" for c in face["color"])
        refs = [str(i + 1) for i in face["indices"]]
        if face["texture_offset"] >= 0:
            binding = binding_base + face["texture_offset"]
            flags, texture_id, count = struct.unpack_from(">hhI", txf, binding)
            if texture_id >= 0:
                if texture_id >= texture_count or count != len(refs):
                    raise ValueError("Invalid texture binding")
                name = Path(texture_names[texture_id]).stem
                material = "texture_" + name
                materials[material] = f"Kd 1 1 1\nmap_Kd {name}.png"
                for index in range(count):
                    u, v = struct.unpack_from(">2f", txf, binding + 8 + index * 8)
                    if not math.isfinite(u) or not math.isfinite(v):
                        raise ValueError("Invalid UV")
                    obj.append(f"vt {u:.9g} {1 - v:.9g}")
                    uv_count += 1
                    refs[index] += f"/{uv_count}"
                textured_faces += 1
        obj.extend([f"g part_{face['part']:02x}", f"usemtl {material}", "f " + " ".join(refs)])
    (args.output / "P51D.obj").write_text("\n".join(obj) + "\n", encoding="ascii")
    (args.output / "P51D.mtl").write_text("\n\n".join(
        f"newmtl {name}\nKa 0 0 0\n{body}\nKs 0 0 0\nd 1\nillum 1"
        for name, body in sorted(materials.items())) + "\n", encoding="ascii")
    preview(vertices, faces, args.output / "preview.png")
    manifest = dict(model="P51D", object="P51Dy", vertices=len(vertices), polygons=len(faces),
                    textured_polygons=textured_faces, uv_coordinates=uv_count,
                    bounds=[[min(v[i] for v in vertices), max(v[i] for v in vertices)] for i in range(3)],
                    part_ids=sorted(set(f["part"] for f in faces)), texture_dimensions=dimensions,
                    sources={str(path): hashlib.sha256(data).hexdigest() for path, data in
                             [(model_path, model_archive), (texture_path, texture_archive)]},
                    model_sha256=hashlib.sha256(model).hexdigest(),
                    limitations=["Native coordinate units; no physical scale inferred.",
                                 "All conditional polygons in the selected detail object are included.",
                                 "Part IDs retained without inferred animation or visibility semantics.",
                                 "No rig, animation, collision or flight parameters exported.",
                                 "Original n-gons retained; importer triangulation may vary.",
                                 "Texture materials are unmodulated; runtime lighting is not reproduced.",
                                 "Preview uses polygon colors, without texture mapping."])
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


def archive_entries(data):
    version, count = struct.unpack_from(">II", data)
    if version != 3 or count > 600 or len(data) < 19208:
        raise ValueError("Invalid WarBirds archive directory")
    result = {}
    for i in range(count):
        start = 8 + i * 32
        name = data[start:start + 16].split(b"\0")[0].decode("ascii")
        offset, size, flags, unused = struct.unpack_from(">4I", data, start + 16)
        if offset < 19208 or offset + size > len(data):
            raise ValueError(f"Entry out of bounds: {name}")
        result[name] = data[offset:offset + size]
    return result


if __name__ == "__main__":
    main()
