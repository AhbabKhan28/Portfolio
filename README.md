# Animated Portfolio

A modern, dark/light themed portfolio built with plain **HTML, CSS, and JavaScript** — no build step, no dependencies. Designed to showcase visual work like banners and thumbnails.

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
index.html   # Markup: hero, about, projects, contact
style.css    # Design tokens, layout, animations, responsive rules
script.js    # Scroll reveal, counters, nav, theme toggle
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
- **Projects**: duplicate a `.project-card` block and set its `--accent` color.
