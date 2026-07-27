# Animation Patterns

Use animation to create deliberate presentation energy. Prefer a few well-orchestrated effects over many scattered micro-interactions.

## General rules

- Use CSS-only animation when possible.
- Respect `prefers-reduced-motion: reduce`.
- Animate opacity, transform, filter, and clip-path more often than layout-affecting properties.
- Stagger entrances with `animation-delay` for hierarchy.
- Keep slide transitions short enough to preserve presenter control.

## Patterns

### Staggered reveal

Use for title slides, agenda grids, and multi-card layouts.

```css
.reveal { opacity: 0; transform: translateY(28px); animation: revealUp 700ms cubic-bezier(.2,.8,.2,1) forwards; }
.reveal:nth-child(2) { animation-delay: 120ms; }
.reveal:nth-child(3) { animation-delay: 240ms; }
@keyframes revealUp { to { opacity: 1; transform: translateY(0); } }
```

### Scale-in emphasis

Use for central numbers, product screenshots, or decisive claims.

```css
.hero-mark { opacity: 0; transform: scale(.92); animation: scaleIn 650ms cubic-bezier(.16,1,.3,1) forwards; }
@keyframes scaleIn { to { opacity: 1; transform: scale(1); } }
```

### Ambient background drift

Use for atmospheric gradients and abstract shapes.

```css
.orb { animation: drift 12s ease-in-out infinite alternate; }
@keyframes drift { from { transform: translate3d(0,0,0) scale(1); } to { transform: translate3d(32px,-24px,0) scale(1.08); } }
```

### Progress draw

Use for timelines, process slides, and section dividers.

```css
.rule { transform-origin: left center; transform: scaleX(0); animation: drawRule 900ms ease forwards; }
@keyframes drawRule { to { transform: scaleX(1); } }
```

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
}
```
