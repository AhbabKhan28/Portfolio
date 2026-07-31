# Data Analyst Portfolio

A modern, dark/light themed portfolio built with plain **HTML, CSS, and JavaScript** — no build step, no dependencies. It showcases data-analytics work built with **Python, SQL, and Power BI**.

The analytics projects themselves live in [`projects/`](projects/) and run end-to-end on synthetic (reproducible) data — see [`projects/README.md`](projects/README.md).

## Features

- **Fade-in load animation** with staggered hero content
- **Scroll-reveal animations** powered by `IntersectionObserver`
- **Animated stat counters** that count up when scrolled into view
- **Dark / light theme toggle** (persisted via `localStorage`, respects OS preference)
- **Sticky glassmorphic navbar** with a scroll-progress indicator
- **Responsive mobile navigation** with an animated hamburger menu
- **Sleek hover effects** on project cards, buttons, and skill chips
- **Accessible**: honors `prefers-reduced-motion`

## Structure

```
index.html         # Markup: hero, about, projects, contact
style.css          # Design tokens, layout, animations, responsive rules
script.js          # Scroll reveal, counters, nav, theme toggle
assets/img/        # Project chart thumbnails shown on the site
projects/          # The data-analytics projects (Python / SQL / Power BI)
```

## Getting Started

It's a static site — just open `index.html` in a browser, or serve it locally:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Customizing

- **Content**: edit the sections in `index.html`.
- **Colors / theme**: tweak the CSS custom properties under `:root` and `[data-theme="light"]` in `style.css`.
- **Projects**: duplicate a `.project-card` block and point its `<img>` at a chart in `assets/img/`.
