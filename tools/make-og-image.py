#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph image for MagicaVoxel (ephtracy.github.io).

Pillow-only and portable: run from anywhere on a checkout; override FONT_DIR
if the system font directories differ. Draws a dark voxel-themed card using
the site's own colors (#222/#232 UI, purple accent from the mascot favicon)
and the site's real meta tagline. No invented logo -- the cube motif is a
generic voxel-art reference, not a redraw of the MagicaVoxel mascot.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FONT_DIR = os.environ.get("FONT_DIR", "/usr/share/fonts/truetype/dejavu")

def font(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for base in (FONT_DIR, "/usr/share/fonts/truetype/liberation"):
        p = os.path.join(base, name)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_voxel(d, x, y, s, colors):
    """Draw a simple isometric-looking voxel cube made of three quads."""
    # top face
    d.polygon([(x, y - s*0.5), (x + s*0.5, y - s), (x + s, y - s*0.5), (x + s*0.5, y)], fill=colors[0])
    # right face
    d.polygon([(x + s*0.5, y), (x + s, y - s*0.5), (x + s, y + s*0.5), (x + s*0.5, y + s)], fill=colors[1])
    # left face
    d.polygon([(x, y - s*0.5), (x + s*0.5, y), (x + s*0.5, y + s), (x, y + s*0.5)], fill=colors[2])

def main():
    img = Image.new("RGB", (W, H), "#101014")
    d = ImageDraw.Draw(img)

    # subtle dark footer strip like the site's #222/#232 UI
    d.rectangle([0, 500, W, H], fill="#1c1c1f")
    d.rectangle([0, 498, W, 500], fill="#2a2a2e")

    # voxel cube motif (top-right corner): a stack of 3 cubes
    palettes = [
        ("#e8734a", "#c2542f", "#f08a62"),  # warm orange
        ("#8a5cf6", "#6a3fe0", "#a47df8"),  # purple (mascot accent)
        ("#4a9cf6", "#2f7ad0", "#63b0f8"),  # blue
    ]
    # back cube
    draw_voxel(d, 950, 220, 130, palettes[1])
    # mid cube
    draw_voxel(d, 1000, 250, 110, palettes[2])
    # front cube
    draw_voxel(d, 1050, 290, 90, palettes[0])

    # wordmark
    d.text((70, 150), "MagicaVoxel", font=font(88), fill="#f5f5f5")
    # tagline (real meta description copy)
    d.text((70, 270), "A free lightweight GPU-based voxel art editor", font=font(38), fill="#d0d0d4")
    d.text((70, 322), "and interactive path tracing renderer.", font=font(38), fill="#d0d0d4")

    # URL pill
    d.rounded_rectangle([70, 420, 70 + 460, 420 + 58], radius=29, fill="#2a2a2e", outline="#3a3a40")
    d.text((108, 434), "ephtracy.github.io", font=font(32), fill="#a47df8")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "og-image.png")
    img.save(out, "PNG")
    print(f"wrote {out} {img.size}")

if __name__ == "__main__":
    main()