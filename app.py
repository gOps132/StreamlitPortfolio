import requests
import streamlit as st

USERNAME = "gops132"

st.set_page_config(
    page_title="Epilan, Gian Cedrick | Portfolio",
    page_icon="👋",
    layout="wide"
)

# Autobiography 
st.title("Hi, I am Epilan, Gian Cedrick! 👋")

# st.container()

profile_col1, profile_col2 = st.columns(2)


if "img_idx" not in st.session_state:
    st.session_state.img_idx = 0

# photo of meee

profile_col1.image("./images/pfp2.jpg")
with profile_col2: 
    st.markdown("#### I'm a **passionate dev 💻** and **photographer 📸** who loves building applications")
    st.markdown("#### Proud CIT-U BSCS-3 F1 student 🎒")


## github history 

st.image(f"https://ghchart.rshah.org/{USERNAME}", use_container_width=True)

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


## Zyklon
# github: https://github.com/gOps132/Zyklon
# Zyklon.png

# A renderer i've been working on in order to teach myself
# c++, systems programming and graphics programming.

## Pixtasm

### A solution to manually making pixel art to turbo-assembly for my computer
### architecture class! This helped a lot of peeps in my batch!


### you can try it on https://pix-tasm.vercel.app/ !!

### photos carousel
# pixtasm0.png, pixtasm1.png

## project 3 (group project) Parallel Apart

### Our UPCSG submission which won us the game jam!


### you can try it on https://glensh.itch.io/in-parallel-apart

### photos carousel

# Photosss
## display each photo in a grid, each with a fixed size cell, each can be 
# clicked to open a modal of the full photo.


st.header("Some of my photos!")

# gallery section
## images are in images/gallery/*

# contact feed back form

# want to get in touch with me? Reach through here OPEN MODAL
# name, email, message