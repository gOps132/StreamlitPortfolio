"""Personal portfolio for Epilan, Gian Cedrick — built with Streamlit."""

import json
import re
from pathlib import Path

import requests
import streamlit as st

USERNAME = "gops132"

# Anchor the image paths to this file so the app works no matter which
# directory it was started from.
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"

# Every image the app serves is pre-rendered by tools/build_assets.py, so
# nothing is decoded, rotated or resized while the page is loading.
GALLERY_DIR = IMAGE_DIR / "gallery"    # full photo, shown in the lightbox
THUMB_DIR = IMAGE_DIR / "thumbs"       # square thumbnail, shown in the grid
PROJECT_DIR = IMAGE_DIR / "projects"   # 16:9 frame, shown in the carousel

PHOTO_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
GALLERY_COLUMNS = 4

st.set_page_config(
    page_title="Epilan, Gian Cedrick | Portfolio",
    page_icon="👋",
    layout="wide"
)


def load_manifest() -> dict:
    """The size of every pre-rendered image, written by build_assets.py."""
    manifest = IMAGE_DIR / "manifest.json"
    if not manifest.exists():
        return {}
    try:
        return json.loads(manifest.read_text())
    except json.JSONDecodeError:
        return {}


MANIFEST = load_manifest()


def gallery_files() -> list[Path]:
    """Every photo in the gallery folder, in filename order."""
    if not GALLERY_DIR.is_dir():
        return []
    return sorted(
        p for p in GALLERY_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in PHOTO_EXTS
    )


# --------------------------------------------------------------------------
# Carousel
# --------------------------------------------------------------------------

def _shift_carousel(state_key: str, delta: int, count: int) -> None:
    """Callback for the carousel arrows — moves the index and wraps around."""
    st.session_state[state_key] = (st.session_state[state_key] + delta) % count


def render_carousel(paths: list[Path], key: str) -> None:
    """A prev/next carousel over a list of images, driven by session state."""
    state_key = f"carousel_{key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    index = int(st.session_state[state_key]) % len(paths)

    prev_col, frame_col, next_col = st.columns(
        [1, 5, 1], vertical_alignment="center", gap="small"
    )

    with frame_col:
        st.image(str(paths[index]), width="stretch")
        if len(paths) > 1:
            st.caption(f"Shot {index + 1} of {len(paths)}")

    if len(paths) == 1:
        return

    with prev_col:
        st.button(
            "◀",
            key=f"{key}_prev",
            on_click=_shift_carousel,
            args=(state_key, -1, len(paths)),
            disabled=index == 0,
            width="stretch",
            help="Previous shot",
        )

    with next_col:
        st.button(
            "▶",
            key=f"{key}_next",
            on_click=_shift_carousel,
            args=(state_key, 1, len(paths)),
            disabled=index == len(paths) - 1,
            width="stretch",
            help="Next shot",
        )


# --------------------------------------------------------------------------
# Project data
# --------------------------------------------------------------------------

PROJECTS = [
    {
        "name": "Zyklon",
        "emoji": "🖥️",
        "tagline": "A software renderer, written from scratch in C++.",
        "description": (
            "A renderer I've been working on in order to teach myself C++, "
            "systems programming and graphics programming."
        ),
        "links": [("Source code", "https://github.com/gOps132/Zyklon")],
        "images": [PROJECT_DIR / "zyklon.jpg"],
    },
    {
        "name": "Pixtasm",
        "emoji": "🧩",
        "tagline": "Pixel art to Turbo Assembly, for my computer architecture class.",
        "description": (
            "A solution to manually making pixel art to Turbo Assembly for my "
            "computer architecture class! This helped a lot of peeps in my batch."
        ),
        "links": [("Try it out", "https://pix-tasm.vercel.app/")],
        "images": [PROJECT_DIR / "pixtasm0.jpg", PROJECT_DIR / "pixtasm1.jpg"],
    },
    {
        "name": "Parallel Apart",
        "emoji": "🏆",
        "tagline": "Our group project for the UPCSG game jam.",
        "description": "Our UPCSG submission which won us the game jam!",
        "links": [("Play it", "https://glensh.itch.io/in-parallel-apart")],
        "images": [PROJECT_DIR / "parallel_apart0.jpg", PROJECT_DIR / "parallel_apart1.jpg"],
    },
]


# --------------------------------------------------------------------------
# Photo lightbox
# --------------------------------------------------------------------------

def _close_dialog() -> None:
    """Called when a dialog is dismissed so it does not pop open again."""
    if "active_dialog" in st.session_state:
        del st.session_state["active_dialog"]


def _shift_gallery(delta: int, count: int) -> None:
    st.session_state["gallery_idx"] = (st.session_state["gallery_idx"] + delta) % count


def _open_gallery(index: int) -> None:
    """Callback for the gallery thumbnails — opens the lightbox."""
    st.session_state["gallery_idx"] = index
    st.session_state["active_dialog"] = "gallery"


@st.dialog("Photo", width="large", on_dismiss=_close_dialog)
def photo_dialog() -> None:
    """Full size photo with prev/next navigation."""
    files = gallery_files()
    index = st.session_state.get("gallery_idx", 0)
    if not files or not 0 <= index < len(files):
        st.info("This photo is no longer available.")
        return
    path = files[index]

    # The dialog is not laid out yet when the image is rendered, so an
    # explicit pixel width is used instead of stretching to the container.
    size = MANIFEST.get("gallery", {}).get(path.stem)
    with st.container(horizontal_alignment="center"):
        if size:
            st.image(str(path), width=size[0])
        else:
            st.image(str(path))
    st.caption(f"{index + 1} / {len(files)} — {path.stem}")

    prev_col, spacer, next_col = st.columns([1, 6, 1])
    with prev_col:
        st.button(
            "◀",
            key="gallery_prev",
            on_click=_shift_gallery,
            args=(-1, len(files)),
            disabled=index == 0,
            width="stretch",
            help="Previous photo",
        )
    with next_col:
        st.button(
            "▶",
            key="gallery_next",
            on_click=_shift_gallery,
            args=(1, len(files)),
            disabled=index == len(files) - 1,
            width="stretch",
            help="Next photo",
        )


# --------------------------------------------------------------------------
# Contact form
# --------------------------------------------------------------------------

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@st.dialog("Get in touch", width="medium", on_dismiss=_close_dialog)
def contact_dialog() -> None:
    """A small form that says thank you once it is sent."""
    if st.session_state.get("contact_sent"):
        name = st.session_state.get("contact_name", "")
        st.success(f"Thanks, {name}! 🎉 I've got your message.")
        st.markdown("I'll get back to you as soon as I can — talk soon!")
        st.caption("This form is a placeholder for now, so nothing was actually sent.")
        if st.button("Close", key="contact_close", type="primary", width="stretch"):
            del st.session_state["contact_sent"]
            del st.session_state["contact_name"]
            st.session_state["active_dialog"] = None
            st.rerun()
        return

    with st.form("contact_form"):
        name = st.text_input("Your name", placeholder="Ada Lovelace")
        email = st.text_input("Your email", placeholder="ada@example.com")
        message = st.text_area("Message", placeholder="Tell me about your project…", height=140)
        submitted = st.form_submit_button("Send message", type="primary")

    if submitted:
        if not name.strip():
            st.error("Please tell me your name.")
        elif not EMAIL_RE.match(email.strip()):
            st.error("That email address doesn't look right.")
        elif not message.strip():
            st.error("Don't forget to write a message.")
        else:
            st.session_state["contact_name"] = name.strip().split()[0]
            st.session_state["contact_sent"] = True
            st.rerun()


# --------------------------------------------------------------------------
# Autobiography
# --------------------------------------------------------------------------

st.title("Hi, I am Epilan, Gian Cedrick! 👋")

profile_col1, profile_col2 = st.columns(2)

# photo of meee

profile_col1.image(str(IMAGE_DIR / "pfp2.jpg"), width="stretch")
with profile_col2:
    st.markdown("#### I'm a **passionate dev 💻** and **photographer 📸** who loves building applications")
    st.markdown("#### Proud CIT-U BSCS-3 F1 student 🎒")
    st.markdown("")
    cta_col1, cta_col2 = st.columns([1, 1])
    with cta_col1:
        if st.button("Get in touch", type="primary", width="stretch"):
            st.session_state["active_dialog"] = "contact"
    with cta_col2:
        st.link_button("GitHub", f"https://github.com/{USERNAME}", width="stretch")


## github history

st.image(f"https://ghchart.rshah.org/{USERNAME}", width="stretch")

## CUSTOM save for later

# url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last"
# data = requests.get(url).json()

# # Level 0 (empty) -> Level 4 (max commits): Black-green to neon green
# palette = {
#     0: "#0f1411",  # Near-black empty square
#     1: "#0e4429",  # Deep forest green
#     2: "#006d32",  # Rich mid green
#     3: "#26a641",  # Vibrant green
#     4: "#39d353",  # Bright neon green accent
# }

# cells_html = "".join(
#     f'<div title="{day["date"]}: {day["count"]} contributions" '
#     f'style="width:12px; height:12px; border-radius:3px; '
#     f'background:{palette[day["level"]]}; '
#     f'border:1px solid rgba(57,211,83,0.08);"></div>'
#     for day in data["contributions"]
# )

# st.markdown(
#     f"""
#     <div style="background:#070a08; border:1px solid #192b20; border-radius:12px; padding:18px; overflow-x:auto;">
#         <div style="color:#7ee787; font-family:monospace; font-size:14px; margin-bottom:10px;">
#             {data["total"]["lastYear"]} contributions in the last year
#         </div>
#         <div style="display:grid; grid-template-rows:repeat(7, 12px); grid-auto-flow:column; gap:3px; width:max-content;">
#             {cells_html}
#         </div>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# Project section

st.header("Projects 🚀")

for project in PROJECTS:
    with st.container(border=True):
        text_col, media_col = st.columns([1, 1], gap="large")
        with text_col:
            st.subheader(f"{project['emoji']} {project['name']}")
            st.markdown(f"*{project['tagline']}*")
            st.markdown(project["description"])
            st.markdown("")
            for label, url in project["links"]:
                st.link_button(label, url, icon="↗")
        with media_col:
            render_carousel(project["images"], project["name"])


# Photosss
## display each photo in a grid, each with a fixed size cell, each can be
# clicked to open a modal of the full photo.


st.header("Some of my photos!")

photos = gallery_files()
if photos:
    st.caption("Click a photo to see it full size.")

    # The thumbnail *is* the button: the real button is stretched over the
    # photo and made invisible, so clicking the photo opens the lightbox.
    st.markdown(
        """
        <style>
        [class*="st-key-gallery_cell_"] { position: relative; }
        [class*="st-key-gallery_cell_"] [class*="st-key-gallery_view_"] {
            position: absolute;
            inset: 0;
        }
        [class*="st-key-gallery_cell_"] [class*="st-key-gallery_view_"] button {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            opacity: 0;
            border: none;
            cursor: zoom-in;
        }
        [class*="st-key-gallery_cell_"] [data-testid="stElementToolbar"] { display: none; }
        [class*="st-key-gallery_cell_"] img {
            border-radius: 12px;
            transition: box-shadow 120ms ease;
        }
        [class*="st-key-gallery_cell_"]:hover img {
            box-shadow: 0 0 0 3px rgba(255, 77, 109, 0.45);
        }
        [class*="st-key-gallery_cell_"]:has(button:focus-visible) img {
            box-shadow: 0 0 0 3px rgba(255, 77, 109, 0.9);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Matched by filename stem so a photo still finds its thumbnail even if
    # the file extensions differ in case.
    thumbs = {p.stem: p for p in THUMB_DIR.iterdir() if p.is_file()}

    gallery_cols = st.columns(GALLERY_COLUMNS)
    for i, path in enumerate(photos):
        with gallery_cols[i % GALLERY_COLUMNS]:
            with st.container(key=f"gallery_cell_{i}"):
                # No width="stretch" here: a positioned ancestor makes
                # Streamlit collapse stretched images to 16px.
                st.image(str(thumbs.get(path.stem, path)))
                st.button(
                    f"View photo {i + 1}",
                    key=f"gallery_view_{i}",
                    on_click=_open_gallery,
                    args=(i,),
                    width="stretch",
                )

    if st.session_state.get("active_dialog") == "gallery":
        photo_dialog()
else:
    st.info("No photos found in `images/gallery/`.")


# contact feed back form

# want to get in touch with me? Reach through here OPEN MODAL
# name, email, message

st.header("Let's work together 👋")
st.markdown("Want to get in touch with me? Reach through here.")
if st.button("Get in touch", type="primary"):
    st.session_state["active_dialog"] = "contact"

if st.session_state.get("active_dialog") == "contact":
    contact_dialog()

st.divider()
st.caption(f"Made with Streamlit · © 2026 Epilan, Gian Cedrick · [github.com/{USERNAME}](https://github.com/{USERNAME})")
