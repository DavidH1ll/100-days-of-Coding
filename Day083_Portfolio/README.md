# Day 83 - Portfolio Website

## Overview
A personal developer portfolio website built with Flask, showcasing skills and projects from the 100 Days of Code challenge. Features a modern dark theme with teal accents, smooth-scroll navigation, scroll-triggered animations, and fully responsive design.

## Design System

| Element | Value |
|---------|-------|
| **Background** | Dark navy (`#0a192f`) |
| **Surface** | Light navy (`#112240`) |
| **Accent** | Teal (`#64ffda`) |
| **Text** | Slate (`#8892b0` / `#a8b2d1`) |
| **Headings** | Playfair Display (serif) |
| **Body** | Inter (sans-serif) |
| **Mono** | SF Mono / Fira Code |

## Sections

1. **Hero** — Animated intro with name, tagline, and CTAs
2. **About** — Background story and tech stack list
3. **Skills** — Grid of 12 technology badges with icons
4. **Projects** — 8 project cards from the 100 Days challenge
5. **Contact** — Email CTA and social links

## Features

- Fixed navbar with blur backdrop and scroll-aware background
- Smooth scroll navigation with active section highlighting
- Scroll-triggered fade-in animations via Intersection Observer
- Bouncing scroll indicator
- Hover effects on cards, buttons, and social links
- Fully responsive: 768px and 480px breakpoints
- `prefers-reduced-motion` accessibility support
- Custom scrollbar styling
- CSS variables for consistent design tokens

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

Visit `http://localhost:5000` in your browser.

## Reflection

### How I Approached the Project

Before writing a single line of code, I did a full audit of every web project in the repository (Days 54-69). I mapped out which patterns evolved over time — inline HTML strings gave way to Jinja templates, internal `<style>` blocks graduated to external CSS files, and manual forms were replaced by Flask-WTF. This gave me a clear picture of what "good" looks like in this codebase and helped me avoid repeating mistakes from earlier days.

I decided on a single-page portfolio because it's the most common pattern for developer portfolios and it plays to Flask's strengths without over-engineering. The data (projects, skills) lives in Python dictionaries in `main.py`, which keeps the HTML template clean and declarative. If I ever wanted to add a CMS or database later, the separation is already there.

For the design, I studied a handful of real developer portfolios and noticed a pattern: dark backgrounds with a single vibrant accent color, generous whitespace, and clear typographic hierarchy. I settled on navy (`#0a192f`) and teal (`#64ffda`) because the combination feels technical but warm — not as cold as pure black-and-green terminal aesthetics.

### What Was Hard

**Animation sequencing.** I wanted the hero section to "reveal" line by line — greeting, then name, then tagline, then description, then buttons. The obvious approach is CSS `@keyframes` with staggered `animation-delay` values, but the elements are invisible (`opacity: 0`) until their animation fires, which means the page loads blank for a full second. I solved this by keeping the `animation-fill-mode: forwards` so elements remain visible after their animation completes, but it still felt clunky on slow connections. Next time I'd use JavaScript to trigger the animation only after fonts have loaded.

**The `about-image-wrapper::after` border trick.** I wanted a framed photo effect — a teal border offset behind the image. I used a pseudo-element positioned absolutely, but getting the hover transition to shrink the offset smoothly (`top: 14px → 8px`) while keeping the image still took trial and error with z-index stacking.

**Scroll-spy accuracy.** Highlighting the active nav link based on scroll position sounds simple but has edge cases. If the last section is shorter than the viewport, the IntersectionObserver fires late or not at all. I ended up using the traditional `scroll` event for nav highlighting and reserved IntersectionObserver only for the reveal animations — a pragmatic split.

### What Was Easy

**Flask wiring.** One route, one template, two data lists. After the multi-model, multi-form complexity of Day 69, this felt like a warm-up.

**CSS variables.** Defining `--navy`, `--teal`, `--slate`, etc. at the top of the stylesheet and referencing them everywhere made the entire design feel cohesive immediately. I changed the accent color three times during development (from green to purple to teal) and each change took exactly one line edit.

**Font pairing.** Playfair Display (serif, elegant) for headings and Inter (sans-serif, clean) for body text. They have enough contrast to create hierarchy but share similar x-heights so they sit well together on the same page. Google Fonts made this trivial with a single `<link>` tag.

### Biggest Learning

**`clamp()` is a game-changer for responsive typography.** Instead of writing separate font-size declarations for mobile, tablet, and desktop, `clamp(2rem, 8vw, 5rem)` handles it continuously. The hero name scales smoothly from 2rem on a phone to 5rem on a wide monitor without a single media query. I'll use this everywhere going forward.

**The scroll performance tradeoff.** IntersectionObserver fires asynchronously and doesn't block the main thread, making it ideal for reveal animations. But for continuous updates like nav highlighting, the `scroll` event (throttled implicitly by `requestAnimationFrame` in modern browsers) gives more precise positional data. Understanding *which* tool to reach for based on the task was the real learning — not just knowing both APIs exist.

### What I'd Do Differently

1. **Start with mobile-first CSS.** I wrote the desktop styles first and then overrode them in `@media` queries. Writing mobile-first (`min-width` breakpoints instead of `max-width`) would have reduced the total CSS and avoided specificity conflicts.
2. **Add a build step.** Even for a small project, something like Flask-Assets to minify CSS/JS would be good practice for production deployment.
3. **Use actual screenshot images** for project cards instead of folder icons. Visual previews would make the project section much more compelling.
4. **Add a contact form endpoint** with Flask-WTF + SMTP (like Day 60/61) instead of a plain `mailto:` link. It's a portfolio — the contact section should work end-to-end.
5. **Write the README first**, or at least sketch the sections I wanted, before writing HTML. I wrote the code first and documented second, which made the README feel like an afterthought rather than a spec.
6. **Deploy immediately.** The project is container-ready (single Python file, few dependencies) but sitting on localhost doesn't help anyone see it. Render's free tier or GitHub Pages (with Flask-Freeze) would take 10 minutes.

---

**Day 83: Complete!** ✅
