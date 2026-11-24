# Channel video workflow (ZEROVERSE)

Channel: ZEROVERSE (@zeroversefilms) — animated "what if" stories and short films about time, family, discipline.
Videos: 16:9, 4–7 min, no voice-over (on-screen text + music), English with Ukrainian subtitles.
Default visual style: the v2 look from `video-plan/05-days-left/render/style2.js` (layered night cities, rim light, short shots with camera moves, hard cuts).

## Production standard for every new video (user asked: better animation, editing, music, more eye candy)

- **Characters have full bodies**: use `figure()` from `video-plan/assets/rig.js` (arms with elbows, legs with knees, shoes;
  poses stand/walk/run/sit/wave/point/armsUp/hold/think/pockets/reach/hug/slump) in every shot where the body is visible.
  Bust-only `person()` is only for close-ups or characters behind a desk/table.
- **Animation**: characters blink, breathe, turn heads, walk with arm swing; secondary motion (hair, hood, steam, leaves);
  no scene is ever static — something always moves.
- **Eye candy**: particles (dust, sparks, snow, fireflies), light leaks and lens glow, volumetric beams, parallax depth layers,
  background blur for depth of field, screen shake on impacts, slow-motion beats.
- **Editing**: shots 3–8 s; transitions chosen per moment (hard cut, whip pan, match cut, zoom-through, flash on reveals);
  cuts land on music beats; a clear act structure with its own colour grade per act.
- **Text**: kinetic typography — words appear one by one, key word highlighted/glowing, gentle scale/blur-in.
- **Music by theme**: score built for the topic and the acts (e.g. mystery → ticking + pads, sad → piano + strings,
  rise → drums + build, climax → full); real silence before the key reveal. If the user provides a royalty-free track
  (YouTube Audio Library etc.), sync cuts to its beats instead of the synthesized score.
- Check stills of every shot before the full render; fix overlaps and empty frames.

## After finishing every new video — publishing package (in chat AND in `output/PUBLISH.md`)

Give it ready to paste, in English, written carefully (grammar, rhythm, no filler):

1. **Title** — up to ~60 characters; the hook and main search phrase at the start; no clickbait the video doesn't deliver;
   must not repeat the thumbnail text word for word. Plus 2 alternative titles for YouTube "Test & compare".
2. **Description**
   - Lines 1–2 (visible before "more"): the hook + main keyword, written as a sentence a person would say.
   - 2–4 lines on what the film is about, with 2–3 secondary keywords used naturally.
   - **Chapters** (timestamps from the timeline, first one `0:00`, at least 3, each ≥10 s) with short names.
   - One question for comments (drives engagement).
   - Call to action: subscribe + link placeholder to the matching playlist.
   - Exactly 3 hashtags at the end (YouTube shows the first 3 above the title).
3. **Tags** — 10–15, from specific (video topic) to broad (genre), under 500 characters.
4. **Pinned comment** — one line, invites a reply.
5. **Thumbnail text** check — 1–3 words, complements the title instead of repeating it.
6. Suggested **playlist**, **end screen** target video, and **card** (which video, at which timestamp).
