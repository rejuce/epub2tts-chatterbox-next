# Styling Concepts — epub2tts-chatterbox (eBook / Audiobook conversion theme)

> **Concepts only — no code changes.** These are 10 visual-direction options for
> re-skinning the FastAPI + HTMX + Jinja2 web UI. Each is described so it could
> be handed to implement later. The current UI lives in
> `epub2tts_chatterbox/web/templates/base.html` (CSS variables) plus
> `home.html`, `jobs.html`, `job.html`, `progress.html`.

**Current state (for reference):** a functional dark theme, flat panels
(`#15171c` bg, `#1e2128` panels, `#2c313a` lines, `#4da3ff` blue accent),
system-ui sans-serif, 8 px radius, flat badges and a single-color progress bar.
Solid and readable — but visually plain.

The app's identity is **eBook → audiobook conversion** (EPUB → text → TTS → M4B).
So the strongest concepts pull from two worlds: **books/reading** and
**audio/recording studios**. Each concept below notes which UI elements it would
most touch (header, book picker, job cards, state badges, live progress bar,
audio player).

---

## 1. Warm Paper (the "open book" reader)
Warm, cream/parchment background with a soft paper texture, deep ink text, and a
single warm accent (oxblood or olive). Serif headings (e.g. a slab or humanist
serif), clean sans for UI chrome. Evokes reading a well-loved physical book.
- **Palette:** parchment `#f4ecd8`, ink `#2b2317`, accent oxblood `#7a1f25`, soft shadow.
- **Type:** serif display (Merriweather/EB Garamond) + neutral sans (Inter) for labels.
- **Signature:** header styled like a book's title page (spine on the left, title + nav on the "pages").
- **Touches:** cards as "pages" with a subtle left spine; badges as wax-seal dots.
- **Vibe:** calm, literary, editorial.

## 2. Studio Dark (pro audio / DAW)
Lean fully into the *audiobook* half: a dark, neutral studio palette with
waveform motifs, audio-meter accents, and fine monospace readouts. Reminds of
Reaper / Adobe Audition / Pro Tools.
- **Palette:** near-black `#0d0f12`, panel `#161a1f`, neon-green/amber meter accents, cool gray text.
- **Type:** grotesque sans (Inter/Space Grotesk) + monospace for numbers/ETA.
- **Signature:** the live progress bar becomes a **waveform/transport bar** with a playhead; chapter list looks like tracks on a mixing board.
- **Touches:** badges as small LED indicators; the audio player gets a real waveform scrubber.
- **Vibe:** professional, technical, "in the booth".

## 3. Modern Reader (Kindle/Kobo clean)
A bright, airy, minimal reader-app look: generous whitespace, soft rounded
cards, light shadows, and a **light/dark toggle** like an eReader. Focus on
legibility and calm.
- **Palette:** off-white `#fafaf7`, soft gray, one muted accent (indigo or teal). Ships in both light and dark.
- **Type:** high-legibility serif body option + humanist sans UI.
- **Signature:** a one-click "reading mode" that maximizes text area on the chapter review page.
- **Touches:** cards as soft tiles; a top toggle flips the whole theme.
- **Vibe:** friendly, clean, approachable.

## 4. Vintage Library (leather, brass & bookshelf)
Deep oxblood/burgundy panels with **brass/gold** accents and serif headings —
the feeling of a classic leather-bound library. Great thematic fit for
long-form fiction books.
- **Palette:** oxblood `#4a1218`, brass `#c8a25a`, cream text `#efe3c8`, dark walnut background.
- **Type:** serif display (Cormorant/Playfair) + a clean serif body.
- **Signature:** header as a bookshelf; job cards as leather-bound spines when listed.
- **Touches:** badges as brass plaques; borders as thin gold rules.
- **Vibe:** warm, prestigious, "grand library".

## 5. Terminal / Console (homage to the CLI roots)
The tool started as a CLI, so lean into that: monospace throughout, phosphor
green (or amber) on black, faint scanline glow, a blinking cursor on the
"live" progress area. Nods to old terminals and hacker culture.
- **Palette:** black `#0b0d0f`, phosphor green `#37d66a` **or** amber `#ffb000`, dim green text.
- **Type:** monospace only (JetBrains Mono / IBM Plex Mono).
- **Signature:** the live progress pane renders like a shell (`$ transcribing…` + scrolling stdout).
- **Touches:** badges as `[TRANSCRIBING]` tags; buttons as `[ENTER]` keycaps.
- **Vibe:** retro-tech, dev-first, playful.

## 6. Neon Night (cyber / modern edgy)
Deep purple-to-black gradient background with **neon cyan and magenta** accents
and soft glow on interactive elements. Modern, eye-catching, "late-night
rendering" feel.
- **Palette:** `#0a0618` → `#1a0b2e` gradient, neon cyan `#22d3ee`, magenta `#e879f9`.
- **Type:** geometric sans (Orbitron for display, Inter for body) — use glow sparingly.
- **Signature:** glowing outline on hover; the progress bar glows like a neon tube.
- **Touches:** badges glow by state; the audio player gets a neon ring.
- **Vibe:** bold, modern, "gamer/creator studio".

## 7. Minimalist Monochrome (editorial, typographic)
Pure black/white/gray with **exactly one** accent color used only for action
states. Everything else is gray-scale and relies on type, spacing, and hairline
borders. Timeless and unobtrusive.
- **Palette:** `#000`/`#fff`/grays, single accent (e.g. a single red for "danger", one blue for "primary").
- **Type:** strong grotesque (Inter/Helvetica) with careful weight hierarchy.
- **Signature:** no color except state — the eye is led purely by the one accent.
- **Touches:** badges are outlined/ghost except the active one; hairline dividers everywhere.
- **Vibe:** sophisticated, quiet, "designer tool".

## 8. Cassette / Analog Nostalgia (audiobook retro)
Audiobooks predate streaming — lean into **cassette tapes / VHS / analog**
nostalgia: warm muted colors, tape-reel motifs, VHS scanlines, chunky 80s cards.
- **Palette:** mustard `#e3b23e`, teal `#2b7a7b`, cream `#f2e9d8`, warm brown.
- **Type:** rounded retro display (e.g. a 70s/80s style) + clean sans body.
- **Signature:** the live progress area shows **tapes winding** (two spinning reels); job cards look like cassette labels.
- **Touches:** badges as sticker labels; the audio player has a cassette-transport look.
- **Vibe:** warm, nostalgic, characterful.

## 9. Forest Reading Nook (calm, organic)
A soft, nature-inspired palette: deep forest green + cream + warm wood tones.
Calm and focused — good for long reading/TTS sessions without eye strain.
- **Palette:** forest `#1f3d2b`, moss `#5c7a55`, cream `#f3efe0`, warm-brown accents.
- **Type:** humanist serif (Lora/EB Garamond) + warm sans for UI.
- **Signature:** a subtle leaf/spine motif; very low-contrast, easy-on-the-eyes.
- **Touches:** soft rounded cards, matte (no gloss) surfaces.
- **Vibe:** serene, natural, cozy.

## 10. Frosted Glass (glassmorphism / depth)
A modern, premium look: a soft gradient backdrop with **frosted-glass panels**
(blur + subtle transparency), layered depth, and soft shadows. Feels current
and polished.
- **Palette:** muted gradient backdrop (indigo→rose) with translucent white panels `rgba(255,255,255,0.08)` + blur.
- **Type:** geometric sans (Inter/SF Pro) with generous spacing.
- **Signature:** every card is a frosted pane that blurs the gradient behind it.
- **Touches:** header is a translucent floating bar; badges are soft frosted chips.
- **Vibe:** premium, modern, "2024 SaaS".

---

## Cross-cutting ideas (apply to whichever concept is chosen)
- **Book/audiobook motif:** chapter list as tracks/spines; progress as a
  book being read aloud (page-turn or waveform).
- **State badges → LED/ink seals:** keep the 6 states (TRANSCRIBING, DONE,
  FAILED, CANCELLED, AWAITING_REVIEW, ENCODING) but restyle as a consistent
  glyph system (color + icon).
- **Audio player upgrade:** the `audio` element is the one interactive piece
  that screams "audiobook" — a waveform + chapter scrubber is a big thematic win.
- **Light/dark toggle:** ship the chosen palette in both light and dark.
- **Keep it accessible:** ensure ≥ 4.5:1 contrast for text; don't rely on color
  alone for state (add text/icons).

## Suggested next step
Pick a concept (or a blend, e.g. "Studio Dark + a Warm Paper light mode"). Then
I can prototype one page (e.g. the job detail page) as a standalone HTML file
to see it before touching the repo templates.