#!/usr/bin/env python3
"""
Biox Systems — QR Code Generator
--------------------------------
Generates a QR code image from a URL.

Usage (CLI):
    python qr_generator.py --url "https://example.com" --out "qr_output.png"

Requires:
    pip install qrcode[pil]
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from urllib.parse import urlparse

import qrcode  # type: ignore
from qrcode.constants import ERROR_CORRECT_M  # Balanced error correction (15%)

HEX_COLOR = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

def is_valid_url(url: str) -> bool:
    """
    Basic URL validation using urllib.parse.
    Accepts http/https schemes and requires netloc.
    """
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False

def is_hex_color(value: str) -> bool:
    return bool(HEX_COLOR.match(value))

def generate_qr(
    url: str,
    out_path: Path,
    box_size: int = 10,
    border: int = 4,
    fill_color: str = "#000000",
    back_color: str = "#FFFFFF",
) -> Path:
    """
    Create and save a QR code PNG from a URL.
    - box_size: pixel size for each QR module
    - border: width (in modules) around QR code
    - colors: hex strings like "#000000"
    """
    if not is_valid_url(url):
        raise ValueError(f"Invalid URL: {url!r}. Example: https://example.com")

    if not is_hex_color(fill_color) or not is_hex_color(back_color):
        raise ValueError("Colors must be hex like #000000 or #FFF.")

    qr = qrcode.QRCode(
        version=None,  # auto choose size
        error_correction=ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    out_path = out_path.with_suffix(".png")
    img.save(out_path)
    return out_path

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate a QR code from a URL.")
    p.add_argument("--url", required=True, help="URL to encode (e.g., https://example.com)")
    p.add_argument("--out", default="qr_output.png", help="Output PNG filename (default: qr_output.png)")
    p.add_argument("--box-size", type=int, default=10, help="Pixel size of QR modules (default: 10)")
    p.add_argument("--border", type=int, default=4, help="Border width in modules (default: 4)")
    p.add_argument("--fill", default="#000000", help="Foreground color in hex (default: #000000)")
    p.add_argument("--back", default="#FFFFFF", help="Background color in hex (default: #FFFFFF)")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    out_path = Path(args.out)
    saved = generate_qr(
        url=args.url,
        out_path=out_path,
        box_size=args.box_size,
        border=args.border,
        fill_color=args.fill,
        back_color=args.back,
    )
    print(f"✅ QR code saved to: {saved.resolve()}")

if __name__ == "__main__":
    main()
