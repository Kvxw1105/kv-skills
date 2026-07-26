# HTML Presentation Template Reference

Use this file as the structural contract for every generated Frontend Slides deck.

## Base requirements

- Generate a single self-contained `.html` file.
- Author every slide at a fixed 1920 x 1080 stage size.
- Scale the whole `.deck-stage` uniformly to the viewport; never reflow slide internals by device width.
- Put all CSS and JavaScript inline unless the user explicitly requests separate files.
- Include the full contents of `viewport-base.css` inside the final `<style>` block.
- Provide keyboard navigation, touch/swipe navigation, progress state, and reduced-motion support.
- Include inline editing by default after a draft is generated unless the user asks for a locked/export-only deck.

## Minimal structure

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Presentation Title</title>
  <style>
    /* paste viewport-base.css first */
    /* then deck-specific style system */
  </style>
</head>
<body>
  <main class="deck-viewport" aria-label="Presentation">
    <section class="deck-stage" id="deckStage">
      <article class="slide active" data-slide="1" aria-label="Slide 1">
        <div class="slide-content">
          <h1>Presentation Title</h1>
          <p>Subtitle or author</p>
        </div>
      </article>
      <article class="slide" data-slide="2" aria-label="Slide 2">
        <div class="slide-content">
          <h2>Slide Title</h2>
          <p>Content...</p>
        </div>
      </article>
    </section>
  </main>
  <nav class="deck-controls" aria-label="Slide navigation">
    <button id="prevSlide" type="button">Previous</button>
    <span id="slideCounter">1 / 2</span>
    <button id="nextSlide" type="button">Next</button>
  </nav>
  <div class="edit-hotzone" aria-hidden="true"></div>
  <button id="editToggle" class="edit-toggle" type="button">Edit</button>
  <script>
    // slide controller, scaling, navigation, and optional inline editor
  </script>
</body>
</html>
```

## JavaScript contract

Implement a `SlidePresentation` controller with:

- `currentIndex`, `slides`, `goTo(index)`, `next()`, `previous()`, and `updateScale()`.
- Keyboard navigation: ArrowLeft, ArrowRight, PageUp, PageDown, Space.
- Touch navigation with horizontal swipe threshold.
- Wheel navigation with debounce.
- Window resize handling for stage scale.
- Class-based visibility: only the current slide receives `.active` or `.visible`.

## Inline editing

Include editing by default for draft HTML decks:

- Use `contenteditable` only after edit mode is enabled.
- Save edits to `localStorage` using a deck-specific key.
- Provide an export/download button when possible.
- Do not use a CSS sibling-hover chain for the edit toggle. Use JavaScript hover handling with a short delay so the button does not disappear while the user moves toward it.

## Verification checklist

Before returning a generated deck:

1. Confirm every slide remains inside 1920 x 1080 coordinates.
2. Confirm no slide depends on vertical page scrolling.
3. Confirm slide switching cannot reveal all slides at once.
4. Confirm text does not overflow its card or collide with decorative elements.
5. Confirm the design has a clear typographic and color system, not a generic AI dashboard/card grid.
