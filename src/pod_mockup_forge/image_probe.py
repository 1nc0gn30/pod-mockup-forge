"""Read pixel dimensions from PNG / JPEG / GIF / WebP headers (stdlib only)."""
import os
import struct
from typing import Tuple


def probe_image(path: str) -> Tuple[int, int, float]:
    """Return (width_px, height_px, size_mb) without decoding the image."""
    size_mb = os.path.getsize(path) / (1024 * 1024)
    with open(path, "rb") as f:
        head = f.read(32)  # enough for PNG/GIF/WebP headers
        if head.startswith(b"\x89PNG\r\n\x1a\n"):
            w, h = struct.unpack(">II", head[16:24])
            return w, h, size_mb
        if head[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", head[6:10])
            return w, h, size_mb
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            chunk = head[12:16]
            if chunk == b"VP8X":
                w = int.from_bytes(head[24:27], "little") + 1
                h = int.from_bytes(head[27:30], "little") + 1
                return w, h, size_mb
            f.seek(12)
            data = f.read(30)
            if chunk == b"VP8 ":
                w, h = struct.unpack("<HH", data[14:18])
                return w & 0x3FFF, h & 0x3FFF, size_mb
            if chunk == b"VP8L":
                b = data[9:13]
                w = 1 + (((b[1] & 0x3F) << 8) | b[0])
                h = 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
                return w, h, size_mb
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    break
                code = marker[1]
                if code in (0xD8, 0x01) or 0xD0 <= code <= 0xD7:
                    continue
                (seg_len,) = struct.unpack(">H", f.read(2))
                if code in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    f.read(1)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h, size_mb
                f.seek(seg_len - 2, 1)
    raise ValueError(f"{path}: unsupported or corrupt image (PNG, JPEG, GIF, WebP supported)")
