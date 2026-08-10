---
name: photo-motion-prompt
description: create copy-ready english prompts for grok image-to-video generation from an uploaded or referenced image. use when the user asks to turn a photo, portrait, street shot, lifestyle image, scenery image, or product/scene image into a natural video prompt, especially when they want motion that fits the people, pose, implied action, and environment without ai-like random movement. output only the final prompt unless the user explicitly asks for analysis or variants.
---

# Photo Motion Prompt

## Core Goal

Given an uploaded or referenced image, write one copy-ready English prompt for Grok image-to-video generation. The prompt must infer the natural motion implied by the photo and extend the moment realistically. Do not generate or edit images. Do not call image or video generation tools.

Treat the image as a frozen frame from a real video, not as a still photo that needs decorative animation.

## Default Output Contract

- Output only the final English prompt, with no heading, explanation, markdown fence, or separate negative prompt.
- Keep it copy-ready for Grok.
- Default to about 6 seconds unless the user specifies another duration.
- Use realistic, natural, restrained motion unless the user requests a stronger style.
- Include avoidance constraints inside the same prompt instead of as a separate negative prompt.
- If no image is available, ask the user to upload the image.
- If multiple images are present and the target image is unclear, use the most recent image unless the user explicitly identifies another.

## Image Analysis Workflow

Before writing the prompt, silently inspect the image and decide:

1. What kind of frame is it?
   - static portrait
   - candid street/lifestyle moment
   - walking, turning, mid-step, or other action continuation
   - interaction with an object
   - environmental/landscape scene
   - product, architecture, or still-life scene

2. What motion is already implied by the image?
   - body direction, foot placement, shoulder angle, head turn, gaze direction
   - hair or clothing displacement
   - hand/object relationship
   - environmental cues such as wind, leaves, sunlight, water, traffic, steam, curtains, reflections

3. What should stay stable?
   - identity, face, body proportions, expression baseline
   - hands, fingers, object shapes, cups, bags, phones, logos, signs
   - camera perspective, composition, lighting, background layout

4. What would look fake in this image?
   - random gestures, sudden emotional changes, invented interactions, object morphing, background chaos, unnecessary camera moves

## Motion Selection Rules

Choose one primary motion idea and at most one or two secondary ambient motions. Avoid listing every possible micro-motion.

### Static Portrait

Use minimal micro-motion only: natural breathing, a soft blink, tiny hair or fabric movement if the scene supports it. Do not add turning, walking, hand gestures, or expression changes.

### Candid Street or Lifestyle Moment

Do not freeze the subject unnaturally if the body posture implies movement. Continue the captured moment gently. Use motion such as a slight head/shoulder settling, gaze stabilizing toward or away from the camera, small weight shift, restrained hand/object movement, and hair/clothing follow-through.

The subject should feel candid, not like they are performing for the camera.

### Walking / Turning / Looking Back

If the person appears mid-step, mid-turn, or looking back, extend that exact momentum. Allow subtle continuation of the turn or walk, then natural settling. Keep the motion small and physically plausible. Do not create a full new action sequence unless requested.

Good motion language:
- "continue the natural momentum already implied by the frame"
- "her head and shoulders settle from the turn"
- "her gaze briefly stabilizes on the camera"
- "hair follows the motion and outdoor breeze"
- "the object remains stable with minor realistic movement"

Avoid:
- waving, posing, speaking, drinking, dancing, sudden smiles, large turns, exaggerated walking, model-like performance

### Object Interaction

If the subject holds an object, keep the object stable and preserve hand shape. Use only minor physically realistic motion unless the photo clearly implies an action. Never make cups, phones, bags, tools, or food morph or change position abruptly.

### Environmental Scene

Animate physical elements only: leaves, clouds, water, steam, sunlight, shadows, curtains, dust, reflections, or distant traffic/pedestrians when already plausible. Do not introduce unrelated events.

### Product / Architecture / Still Life

Prioritize stability. Use subtle light changes, reflections, environmental particles, or a tiny camera drift. Do not animate the product or architecture unless physically justified.

## Prompt Composition Template

Write a single paragraph or two short paragraphs using this structure:

1. Start with reference-frame instruction:
   "Use the uploaded image as the exact reference frame. Treat it as a frozen frame from a real video, not as a still photo that needs artificial animation."

2. State duration and realism:
   "Create a realistic 6-second video continuation..."

3. Preserve identity and scene details:
   Mention the visible subject type, face/identity, pose, clothing, important held objects, lighting, lens perspective, composition, and environment.

4. Describe scene-specific primary motion:
   Base this on the image's implied action, not a generic animation recipe.

5. Describe restrained ambient motion:
   Use only environment elements that fit the image.

6. State camera behavior:
   Usually "observational," "locked-off," "slight handheld drift," or "barely perceptible push-in." Avoid dramatic camera movement.

7. End with embedded negative constraints:
   "No exaggerated gestures, no acting, no new people or objects, no face morphing..."

## Style Rules for Grok Prompts

- Write in direct English.
- Avoid parameter syntax unless the user asks for it.
- Avoid overusing "cinematic" because it often encourages artificial camera moves and drama.
- Prefer: realistic, candid, observational, natural, physically plausible, restrained, documentary-like.
- For street photos, prefer "real candid street video" over "live photo" when the body implies motion.
- Avoid generic filler motion. Every described movement must have a cause from the photo.
- Use "continue" and "settle" language for action photos; use "subtle ambient motion" language for quiet scenes.

## Quality Bar

A good prompt makes the generated video feel like the camera recorded a few seconds around the original frame. It should not feel like the AI invented a new scene.

Prefer a slightly understated video over one with meaningless motion. But for photos that clearly capture a moving moment, do not make the subject completely frozen; continue the visible motion in a restrained way.
