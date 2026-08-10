---
name: single-photo-sequence-prompt-maker
description: generate two image-generation prompts from one uploaded single-person photo. use when the user wants to keep the uploaded photo as the middle image of a three-image set, and generate one visually consistent image before it and one visually consistent image after it. the skill analyzes the visible person, pose, action, environment, composition, lighting, color style, and typography, then outputs two prompts for creating the missing first and third images.
---

# Single Photo Sequence Prompt Maker

## Goal

Turn one uploaded single-person photo into two copy-ready image generation prompts.

Treat the uploaded photo as the middle image in a three-image sequence. The final intended sequence is:

1. generated previous image
2. uploaded original image
3. generated next image

Do not generate images directly unless the user explicitly asks for image generation. The default output is two text prompts.

## Input

Expect one uploaded image containing one main person.

If the image contains multiple people, focus on the most prominent person unless the user specifies otherwise.

If the image contains visible text, typography, captions, posters, product labels, signs, UI, or graphic design elements, analyze and preserve the typography style in both prompts.

## Visual Analysis Rules

Before writing the two prompts, inspect the uploaded photo and extract only visible information:

- Person: face structure, hairstyle, clothing, accessories, body orientation, expression, visible posture
- Action: gesture, movement direction, gaze, hand position, interaction with objects
- Environment: indoor or outdoor setting, background objects, props, location cues
- Visual style: lighting, color palette, contrast, camera angle, lens feel, depth of field
- Composition: framing, crop, subject placement, aspect ratio, image distance
- Typography: font category, weight, spacing, color, placement, alignment, decoration, hierarchy

Do not infer private identity, name, ethnicity, nationality, health, relationship status, occupation, or other sensitive attributes.

## Sequence Construction Logic

Always treat the uploaded photo as the exact middle frame of a three-image group. Create exactly two prompts.

### Prompt 1: Previous Frame

Generate the natural moment before the uploaded photo.

This image should feel like it happened immediately before the uploaded photo.

Use one of these approaches:

- If the uploaded photo shows an action, create the preparation or beginning of that action.
- If the uploaded photo shows a pose, create the person moving into that pose.
- If the uploaded photo shows an emotional moment, create the emotional setup.
- If the uploaded photo is editorial or poster-like, create a complementary opening composition.

### Prompt 2: Next Frame

Generate the natural moment after the uploaded photo.

This image should feel like it happened immediately after the uploaded photo.

Use one of these approaches:

- If the uploaded photo shows an action, create the completion or follow-through of that action.
- If the uploaded photo shows a pose, create the person relaxing or transitioning out of that pose.
- If the uploaded photo shows an emotional moment, create the emotional continuation.
- If the uploaded photo is editorial or poster-like, create a complementary closing composition.

## Output Format

Always output exactly two sections:

```markdown
Prompt 1｜前一张图生成提示词
...

Prompt 2｜后一张图生成提示词
...
```

Do not include analysis notes unless the user asks.

## Prompt 1 Requirements

Prompt 1 must describe the image that comes before the uploaded photo.

Include:

- Use the uploaded photo as the middle reference image.
- Generate the previous image in the same three-image sequence.
- Preserve the same person, face, hairstyle, clothing, accessories, body proportions, and overall visual identity.
- Preserve the same environment, lighting direction, color grading, camera angle, lens style, depth of field, and aspect ratio.
- Show the natural moment before the original pose or action.
- Make the image visually compatible when placed to the left of the uploaded photo.
- Preserve typography style if visible in the uploaded photo.
- Avoid making the image look like a duplicate of the uploaded photo.

Write Prompt 1 in Chinese unless the user requests another language.

## Prompt 2 Requirements

Prompt 2 must describe the image that comes after the uploaded photo.

Include:

- Use the uploaded photo as the middle reference image.
- Generate the next image in the same three-image sequence.
- Preserve the same person, face, hairstyle, clothing, accessories, body proportions, and overall visual identity.
- Preserve the same environment, lighting direction, color grading, camera angle, lens style, depth of field, and aspect ratio.
- Show the natural moment after the original pose or action.
- Make the image visually compatible when placed to the right of the uploaded photo.
- Preserve typography style if visible in the uploaded photo.
- Avoid making the image look like a duplicate of the uploaded photo.

Write Prompt 2 in Chinese unless the user requests another language.

## Typography Handling

If the uploaded photo contains visible text or strong font styling, preserve the typography system across both generated images.

Describe:

- font category: serif, sans-serif, handwritten, bold display, condensed, retro, neon, luxury, minimal, etc.
- font weight and letter spacing
- color, shadow, outline, glow, texture, or decorative treatment
- text placement and alignment
- relationship between text and person
- overall graphic hierarchy

Do not invent exact font names unless they are clearly visible or requested.

If the text is unreadable, describe it as stylized text blocks instead of guessing the content.

## Consistency Rules

Both prompts must strongly preserve continuity with the uploaded photo.

Avoid:

- changing the person, face, hairstyle, clothing, accessories, or body proportions
- changing the background, lighting, color style, camera language, or image ratio
- adding unrelated people or unrelated objects
- creating unreadable, random, misspelled, or inconsistent text
- turning the image into a different photoshoot, illustration style, cartoon style, anime style, oil painting, or unrelated visual genre unless explicitly requested
- over-beautifying the person or changing the original realism level
- duplicating the uploaded photo with only tiny variations

## Prompt Quality Bar

The two prompts should be directly usable in image generation tools.

Each prompt should be specific, visual, and operational. Avoid vague wording such as "make it beautiful" unless paired with concrete visual details.

The final three-image set should feel intentional and coherent:

1. generated previous image
2. uploaded original image
3. generated next image

The generated images should not be copies. They should be natural sequence extensions of the original photo.
