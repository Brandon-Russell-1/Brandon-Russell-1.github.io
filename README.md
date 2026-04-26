# Brandon Russell - personal site

A Quarto-based static site for a professional / academic web presence.

## What's here

```
website/
├── _quarto.yml          # site config: nav, footer, theme
├── styles.css           # typography and small style tweaks
├── index.qmd            # landing page (hero + currently)
├── about.qmd            # bio, education, certs, philosophy
├── teaching.qmd         # courses, manuals, instructional role
├── writing.qmd          # Medium link, working papers, post listing
├── speaking.qmd         # YouTube, talks, booking
├── projects.qmd         # GitHub work
├── cv.qmd               # CV summary + PDF download
├── contact.qmd          # email, LinkedIn, what you're open to
├── images/              # profile photo etc. (create this)
├── files/               # CV PDF and other downloads (create this)
└── posts/               # optional: short posts surfaced on writing.qmd
```

## One-time setup

1. Install Quarto: <https://quarto.org/docs/get-started/>
2. Create the asset folders:
   ```bash
   cd website
   mkdir -p images files posts
   ```
3. Drop a profile photo at `images/profile.jpg` and a CV at `files/brandon-russell-cv.pdf`.
4. Find-and-replace `YOUR_HANDLE` and `you@yourdomain.com` across the `.qmd` files and `_quarto.yml`.

## Preview locally

```bash
quarto preview
```

Hot-reloads in your browser as you edit.

## Build the static site

```bash
quarto render
```

Output lands in `_site/`.

## Deploy to GitHub Pages

The simplest path:

1. Create a new GitHub repo (public).
2. Push this `website/` folder to it.
3. In repo settings, enable GitHub Pages and point it at the `gh-pages` branch.
4. Use Quarto's built-in publish command:
   ```bash
   quarto publish gh-pages
   ```
5. Add a custom domain (e.g. `brandonrussell.com`) in repo Settings -> Pages, then set up the DNS records your registrar tells you to.

## Notes on style

The copy throughout uses hyphens rather than em dashes, plain language, Arial typeface. The cosmo theme is a clean default; if you want a more academic look, swap `theme: cosmo` in `_quarto.yml` for `litera`, `flatly`, or `journal`.

## Add a post

Create `posts/YYYY-MM-DD-slug.qmd`:

```markdown
---
title: "Post title"
date: 2026-04-25
description: "One-sentence summary."
categories: [cybersecurity, teaching]
---

Post body here.
```

It will automatically appear in the listing on `writing.qmd`.
