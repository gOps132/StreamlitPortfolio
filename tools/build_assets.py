"""Build the web-ready image assets from the originals.

Run this after adding or changing a photo in `images/_originals/`:

    pip install pillow
    python tools/build_assets.py

It writes three sets of files that the app serves directly, so the app
itself never has to decode, rotate or resize anything at runtime:

    images/gallery/<name>.jpg    full photo for the lightbox (<= 1200x640)
    images/thumbs/<name>.jpg     square grid thumbnail (600x600)
    images/projects/<name>.jpg   16:9 frame for the project carousels
    images/manifest.json         the size of every generated file

The originals in `images/_originals/` are never modified.
"""

import json
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parent.parent
ORIGINALS = BASE_DIR / "images" / "_originals"
IMAGES = BASE_DIR / "images"

GALLERY_OUT = IMAGES / "gallery"
THUMBS_OUT = IMAGES / "thumbs"
PROJECTS_OUT = IMAGES / "projects"
MANIFEST = IMAGES / "manifest.json"

# Background the project shots are padded onto, so a carousel never jumps.
CANVAS_BG = (13, 17, 23)

THUMB_SIZE = 600
FULL_MAX = (1200, 640)
FRAME_SIZE = (1280, 720)
PROFILE_MAX = 1200

# Project shot -> file in images/_originals/projects/
PROJECTS = {
    "zyklon": "Zyklon.png",
    "pixtasm0": "pixtasm0.png",
    "pixtasm1": "pixtasm1.png",
    "parallel_apart0": "parallel_apart0.jpg",
    "parallel_apart1": "parallel_apart1.png",
}


def open_rgb(path: Path) -> Image.Image:
    """Open a photo, apply its EXIF rotation and normalise it to RGB."""
    img = ImageOps.exif_transpose(Image.open(path))
    return img if img.mode == "RGB" else img.convert("RGB")


def save_jpeg(img: Image.Image, path: Path, quality: int = 88) -> tuple[int, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, format="JPEG", quality=quality, optimize=True)
    print(f"  {path.relative_to(BASE_DIR)}  {img.width}x{img.height}  {path.stat().st_size // 1024} KB")
    return img.width, img.height


def clean_outdir(path: Path) -> None:
    """Remove previously generated files so a rebuild never leaves duplicates.

    The originals can be named `DSC03643.JPG` while the generated file is
    `DSC03643.jpg`; on a case sensitive filesystem both would otherwise end
    up in the gallery.
    """
    if not path.is_dir():
        return
    for old in path.iterdir():
        if old.is_file() and old.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            old.unlink()


def square_thumb(img: Image.Image) -> Image.Image:
    """Centre-crop to a square so every gallery cell is the same size."""
    w, h = img.size
    side = min(w, h)
    left, top = (w - side) // 2, (h - side) // 2
    return img.crop((left, top, left + side, top + side)).resize(
        (THUMB_SIZE, THUMB_SIZE), Image.LANCZOS
    )


def frame(img: Image.Image) -> Image.Image:
    """Fit a shot inside a fixed 16:9 canvas, padded with the page colour."""
    width, height = FRAME_SIZE
    scale = min(width / img.width, height / img.height)
    resized = img.resize(
        (max(1, int(img.width * scale)), max(1, int(img.height * scale))), Image.LANCZOS
    )
    canvas = Image.new("RGB", FRAME_SIZE, CANVAS_BG)
    canvas.paste(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return canvas


def build_gallery() -> dict[str, list[int]]:
    print("gallery:")
    sizes: dict[str, list[int]] = {}
    source_dir = ORIGINALS / "gallery"
    for src in sorted(source_dir.iterdir()):
        if not src.is_file() or src.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        img = open_rgb(src)
        name = src.stem + ".jpg"

        thumb = square_thumb(img)
        save_jpeg(thumb, THUMBS_OUT / name, quality=85)

        full = img.copy()
        full.thumbnail(FULL_MAX, Image.LANCZOS)
        sizes[src.stem] = save_jpeg(full, GALLERY_OUT / name, quality=90)
    return sizes


def build_projects() -> dict[str, list[int]]:
    print("projects:")
    sizes: dict[str, list[int]] = {}
    for name, source in PROJECTS.items():
        img = open_rgb(ORIGINALS / "projects" / source)
        sizes[name] = save_jpeg(frame(img), PROJECTS_OUT / f"{name}.jpg", quality=88)
    return sizes


def build_profile() -> Optional[list[int]]:
    print("profile:")
    src = ORIGINALS / "pfp2.jpg"
    if not src.exists():
        return None
    img = open_rgb(src)
    img.thumbnail((PROFILE_MAX, PROFILE_MAX), Image.LANCZOS)
    return save_jpeg(img, IMAGES / "pfp2.jpg", quality=88)


if __name__ == "__main__":
    for outdir in (GALLERY_OUT, THUMBS_OUT, PROJECTS_OUT):
        clean_outdir(outdir)

    gallery = build_gallery()
    projects = build_projects()
    profile = build_profile()

    manifest = {"gallery": gallery, "projects": projects, "profile": profile}
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"\n  {MANIFEST.relative_to(BASE_DIR)}")
    print("done")
