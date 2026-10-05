# Gemini Omni Flash — Prompt Structure Quick Reference

## The Formula (copy-paste template)

```
[Reference declarations — one line per <IMAGE_REF_N> with role]

[SUBJECT: who/what — key visual details, linked to references],
[ACTION: what they do — time-segmented for >5s],
in [ENVIRONMENT: where — indoor/outdoor, lighting, depth cues],
camera [MOVEMENT: one type only — direction, speed],
style [STYLE: aesthetic — lighting, color, texture, mood],
audio [AUDIO: music, SFX, dialogue, or "no audio"],
[CONSTRAINTS: what to exclude — embedded inline, no separate parameter]
```

## Reference Assignment Template

```
<IMAGE_REF_0> as [role: character face | character appearance | first frame | style]
<IMAGE_REF_1> as [role: outfit | environment | storyboard | product]
<IMAGE_REF_2> as [role]
...up to <IMAGE_REF_6>
```

For image-to-video:
```
<FIRST_FRAME> as the opening frame
```

## Time-Segment Template

```
[00:00-00:XX] Shot description (camera type).
Visual description. Action description. Audio cue.

[00:XX-00:YY] Shot description (camera type).
...
```

## Camera Movement Cheat Sheet

| Movement | Prompt phrasing |
|---|---|
| Static | `fixed camera, no movement` |
| Push-in | `camera slowly pushes in` |
| Pull-out | `camera pulls out to reveal` |
| Pan L/R | `camera pans [left/right] across` |
| Tilt U/D | `camera tilts [up/down] from` |
| Tracking | `camera tracks alongside` |
| Orbit | `camera orbits around` |
| Crane | `crane shot rising above` |
| Handheld | `subtle handheld camera with natural shake` |
| Steadicam | `continuous steadicam, unbroken shot` |
| POV | `first-person POV` |
| Aerial | `aerial camera descends toward` |
| Whip pan | `whip pan to the [direction]` |
| Hitchcock zoom | `dolly out while zooming in` |

**Rule:** Max 2 simultaneous movements. 1 per clip is safest.

## Lighting Keywords (highest impact on output)

`golden hour` · `rim light` · `natural light` · `neon` · `backlit` · `overcast` ·
`studio lighting` · `candlelight` · `moonlight` · `soft window light` · `volumetric light` ·
`dappled sunlight` · `silhouette` · `high key` · `low key`

## Style Anchors

`cinematic` · `film grain` · `4K` · `shallow depth of field` · `anamorphic` ·
`documentary` · `warm tone` · `cool tone` · `moody` · `soft focus` · `lens flare` ·
`desaturated` · `high contrast` · `vintage` · `noir`

## Identity Lock Phrases (use in every segment)

```
Face is <IMAGE_REF_0> throughout — same eyes, same nose, same lips, same skin tone.
Face remains <IMAGE_REF_0> — identical, no drift.
Identity locked from <IMAGE_REF_0> — no variation, no substitution.
Reproduce this exact face in every frame.
```

## Audio Direction Templates

### Music
```
A soft warm lo-fi pop instrumental plays continuously at steady volume. No vocals.
```

### Sound effects
```
A loud crisp SNAP sound effect — sharp, foregrounded above the music, landing exactly
on the gesture.
```

### No audio
```
No speech, no voice, no vocals of any kind.
```

## Constraint Template (embed inline — no separate parameter)

```
Do not [action]. Do not [action]. Never [action].
```

Common constraints:
- `Do not let her speak, mouth words, or open lips to talk.`
- `Do not change the face, hair, or makeup between segments.`
- `Do not move the camera or alter the framing.`
- `Do not morph or dissolve between outfit changes — hard cuts only.`
- `Do not add captions, text, or on-screen graphics.`
- `Do not add a second person.`

## Hard Limits

| Limit | Value |
|---|---|
| Max images | 7 |
| Max audio | 1 (voice ref only at launch) |
| Max video input | 1 (edit endpoint only) |
| Max duration | 10 seconds |
| Min duration | 3 seconds |
| Resolution | 720p @ 24fps |
| Aspect ratios | 16:9, 9:16 |
| Optimal word count | 100–300 words |
| Negative prompt | None — embed inline |
| Camera movements per segment | 1 (max 2) |
| Audio output | Native (auto-generated with video) |

## Endpoint Decision Tree

```
User provides NO media files?
  -> Text to Video endpoint

User provides 1 image as starting frame?
  -> Image to Video endpoint

User provides multiple images (character, outfits, style, environment)?
  -> Reference to Video endpoint (default for multi-image)

User wants to modify a previously generated video?
  -> Edit endpoint (multi-turn, stateful)
```

## Reference to Video — fal.ai API Schema

```json
{
  "prompt": "string (required) — use <IMAGE_REF_N> tags inline",
  "image_urls": ["url1", "url2", ...],
  "aspect_ratio": "16:9 | 9:16",
  "duration": 8
}
```

## Key Differences from Other Models

| Feature | Gemini Omni Flash | MiniMax H3 | Seedance 2.0 |
|---|---|---|---|
| Reference syntax | `<IMAGE_REF_N>` (0-indexed) | `#ImageN` (1-indexed) | `@ImageN` (1-indexed) |
| Max image refs | 7 | 9 | 9 |
| Max video refs | 0 (edit only) | 3 | 3 |
| Max audio refs | 1 (voice only) | 3 | 3 |
| Prompt structure | Inline natural language | 7-section schema | 6-part formula |
| Negative prompts | Inline (no parameter) | In Exclusions section | In avoid section |
| Identity lock | Via reference + repetition | Via subject_definitions | Not supported for faces |
| Native audio | Yes (auto-generated) | Via soundscape sections | Via audio direction |
| Max duration | 10s | Model-dependent | 15s |
| Resolution | 720p | Model-dependent | 720p |
| Multi-turn editing | Yes (stateful) | No | No |
| Face generation | Supported (not real people) | Supported | Not supported |
