# Layered Collage vs Articulated Code Cut-Paper

## Layered collage

A complete illustration may be separated into registered depth layers. Motion is mainly camera, parallax, rigid-family movement, and limited local transforms. This can be excellent collage animation, but it is not automatically articulated cut-paper.

## Articulated code cut-paper

A principal character must be built from independently movable parts with explicit pivots and z-order, such as head, torso, upper/lower arms, legs, cape, prop, animal body, neck, tail, and limbs. Every visible action must name the moving part, pivot, trigger, and occlusion consequence.

## Failure test

Reject the “cut-paper” label when:

- the character is one PNG;
- only the camera or whole image moves;
- the background and subject share the same painterly AI texture;
- joints are metadata only and do not drive local motion;
- no paper edge, layer shadow, or occlusion change is visible.

Complete AI illustrations may guide composition and palette, but must not be presented as code-generated articulated animation.
