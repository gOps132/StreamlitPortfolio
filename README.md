<!-- Improved compatibility of back to top link -->
<a id="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Portfolio</h1>

<!-- PROJECT SHIELDS -->
<div style="display:flex;justify-content:center;">

[![Python][python-shield]][python-url]
[![Streamlit][streamlit-shield]][streamlit-url]
[![Render][render-shield]][render-url]

</div>

  <p align="center">
    Personal portfolio of <strong>Epilan, Gian Cedrick</strong> — a passionate dev and photographer.<br />
    Built with Streamlit, deployed on Render.
    <br />
    <a href="https://github.com/gOps132/StreamlitPortfolio"><strong>Source Code »</strong></a>
    <br />
    <br />
    <a href="#project-structure">Project Files</a>
    &middot;
    <a href="#contact-form">Contact Form</a>
    &middot;
    <a href="https://github.com/gOps132/StreamlitPortfolio">GitHub</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li>
      <a href="#contact-form">Contact Form</a>
      <ul>
        <li><a href="#configuration">Configuration</a></li>
        <li><a href="#on-render">On Render</a></li>
        <li><a href="#a-note-on-the-free-tier">A Note on the Free Tier</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

A one-page personal portfolio built with [Streamlit](https://streamlit.io). It shows a
profile, a GitHub contribution chart, project showcases with screenshots, a photo
gallery with a lightbox, and a contact form that delivers messages straight to a
real inbox through [Resend](https://resend.com).

Highlights:

- **Project carousel** — screenshots per project, navigable with prev/next arrows
- **Photo gallery** — pre-rendered thumbnails in a grid, click any photo to open a full-size lightbox
- **Contact form** — sends to a real inbox via the Resend API, with a hidden field that quietly drops bots
- **Pre-rendered assets** — images are resized ahead of time, so the app never decodes or resizes at runtime

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Streamlit][streamlit-shield]][streamlit-url] — the whole UI, served by one Python file
- [![Python][python-shield]][python-url] — the language the app runs on
- [![Requests][requests-shield]][requests-url] — calls the Resend HTTP API
- [![Pillow][pillow-shield]][pillow-url] — pre-renders the gallery, thumbnail and project images
- [![Resend][resend-shield]][resend-url] — delivers the contact form submissions
- [![Render][render-shield]][render-url] — hosts the app

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PROJECT STRUCTURE -->
## Project Structure

```text
.
├── app.py                    # the whole app
├── images/                   # photos, thumbnails and project shots
│   ├── gallery/              # full photos, shown in the lightbox
│   ├── thumbs/               # square thumbnails, shown in the grid
│   ├── projects/             # 16:9 frames, shown in the carousel
│   └── manifest.json         # the size of every pre-rendered image
├── tools/
│   └── build_assets.py       # pre-renders every image the app serves
├── .streamlit/
│   ├── config.toml           # headless server settings
│   └── secrets.toml.example  # copy to secrets.toml for local development
├── .python-version           # the Python version Render and pyenv use
├── requirements.txt
└── render.yaml               # service definition for Render
```

<!-- CONTACT -->
## Contact

**Epilan, Gian Cedrick** — [@gOps132](https://github.com/gOps132)

Project Link: [https://github.com/gOps132/StreamlitPortfolio](https://github.com/gOps132/StreamlitPortfolio)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[stars-shield]: https://img.shields.io/github/stars/gOps132/StreamlitPortfolio?style=for-the-badge
[stars-url]: https://github.com/gOps132/StreamlitPortfolio/stargazers
[forks-shield]: https://img.shields.io/github/forks/gOps132/StreamlitPortfolio?style=for-the-badge
[forks-url]: https://github.com/gOps132/StreamlitPortfolio/network/members
[issues-shield]: https://img.shields.io/github/issues/gOps132/StreamlitPortfolio?style=for-the-badge
[issues-url]: https://github.com/gOps132/StreamlitPortfolio/issues
[python-shield]: https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[streamlit-shield]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[streamlit-url]: https://streamlit.io/
[requests-shield]: https://img.shields.io/badge/Requests-2FA5D3?style=for-the-badge&logo=python&logoColor=white
[requests-url]: https://requests.readthedocs.io/
[pillow-shield]: https://img.shields.io/badge/Pillow-FFD43B?style=for-the-badge&logo=python&logoColor=white
[pillow-url]: https://pillow.readthedocs.io/
[resend-shield]: https://img.shields.io/badge/Resend-000000?style=for-the-badge&logo=resend&logoColor=white
[resend-url]: https://resend.com/
[render-shield]: https://img.shields.io/badge/Render-46E3BA?style=for-the-badge&logo=render&logoColor=white
[render-url]: https://render.com/
