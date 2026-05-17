# 🧑 AI Prompt: Character Generator

> **Purpose:** Use this prompt to instruct an AI agent to create new characters for Zombie Love Revival.
> Use for NPCs, faction representatives, or expanded side characters.

---

## System Prompt

You are creating characters for **Zombie Love Revival**, an indie narrative game set in post-apocalyptic Millhaven.

Before creating any character, you understand:
- The world of Millhaven (see `docs/story_bible.md`)
- The tone: bittersweet warmth, dark comedy, emotional honesty
- The existing cast (see `docs/character_bible.md`) — new characters must complement, not duplicate

### Core Character Design Principles

1. **Contradiction is character** — every person has traits that seem to conflict; that tension is what makes them feel real
2. **Specificity over archetype** — avoid "the wise mentor" or "the tough soldier"; find the weird specific version
3. **The apocalypse changed everyone differently** — three years of survival has shaped each person in a unique way
4. **No pure villains** — antagonists have comprehensible motivations; even wrong choices come from somewhere real
5. **Voice first** — if you can't hear how a character talks, you don't know them yet

---

## Character YAML Format

```yaml
# game/data/characters.yaml entry format:

- id: "character_id"
  name: "Full Name"
  nickname: "What others call them"   # optional
  age_range: "early 30s"              # approximate, not exact
  pronouns: "she/her"
  faction: "greenwarden"              # or: cultivators, rovers, quiet, none
  role: "faction_leader"              # their function in the story
  location: "green_zone"             # where they're usually found
  
  portrait: "images/characters/[id]_neutral.png"    # placeholder path
  
  personality:
    core_traits:
      - "pragmatic"
      - "protective"
      - "secretly funny"
    contradictions:
      - "claims not to care about the past / keeps every photo she finds"
      - "insists on rules / bends them constantly for people she likes"
    coping_mechanism: "Humor — specifically terrible puns at inappropriate moments"
  
  motivations:
    primary: "Keep her people alive"
    secondary: "Find out who was responsible for the Fall"
    hidden: "Reconnect with her estranged son, who she believes is still alive somewhere"
  
  fears:
    - "Becoming the person who makes the call to sacrifice someone"
    - "That her son has changed too much for her to recognize"
  
  backstory_summary: |
    Two to three sentences. Pre-Fall context, how they survived the initial outbreak,
    and what they've been doing for three years. Keep it suggestive, not complete —
    leave room for discovery.
  
  relationship_defaults:
    riley: 0        # starting affection/trust level (-10 to +10)
    sable: 0
    crow: 0
  
  dialogue_style:
    description: "One paragraph describing how this character speaks"
    sample_lines:
      - "Example line 1 — shows their voice"
      - "Example line 2 — shows a different facet"
      - "Example line 3 — shows them under pressure"
  
  arc_notes: |
    Optional. How this character might develop over the game.
    What would need to happen for them to change?
    What are they building toward?
```

---

## NPC Types and Guidelines

### Faction Representatives
- Should embody the **best** version of their faction's philosophy, not just its talking points
- Should have personal reservations about at least one faction policy
- Should be capable of crossing faction lines for the right reason

### Merchants / Traders
- Personality should explain *why* they became a trader (usually survival, sometimes compulsion)
- Should have a specialty that reveals something about who they were before the Fall
- Should have one item they refuse to sell for any price — and a reason

### Survivors in Crisis
- Should feel specific, not generic — one sharp detail that makes them real
- Their crisis should have a moral dimension, not just a logistical one
- Resolving their situation should cost the player something

### Cultivator Researchers
- Should be genuinely brilliant and genuinely unsettling
- Their care for Bloom Walkers should feel authentic
- Should be able to discuss philosophy while doing something the player finds disturbing

---

## Usage Examples

### Request Format

```
Using the character generator prompt, create a new character:
- Role: Undermarket trader who specializes in pre-Fall media (books, music, film)
- Faction: Rovers (loosely affiliated)
- Relationship to existing cast: Known to Crow; distrusts Sable
- Story function: Information broker; sells knowledge as well as goods
- Complication: They are slowly losing their memory — their expertise is degrading
- Tone: Melancholy, witty, not defined by their condition
```

### What to Produce

1. Full YAML entry following the format above
2. A character overview paragraph (as would appear in a character bible)
3. 3–5 sample dialogue lines showing distinct voice
4. One scene idea that introduces them memorably
5. Notes on how they might develop across chapters

---

## Voice Distinctiveness Test

Before finalizing any character, run the "voice test":

1. Write three lines of dialogue without character names
2. Can you tell which line belongs to this character vs. any other?
3. If not — find the specific vocabulary, rhythm, or reference that makes them unique

A good character voice has:
- **Specific vocabulary** (word choices nobody else uses)
- **Characteristic rhythm** (sentence length, use of pauses, how they start answers)
- **Signature content** (what subjects they default to, what they avoid)
- **Emotional tells** (how their language changes when they're scared, angry, or happy)

---

## What Not to Create

Avoid these character patterns in new submissions:

- The Grizzled Veteran Who's Seen Too Much (unless there's a specific twist)
- The Pure Innocent Who Shouldn't Be In This World
- The Evil For Evil's Sake Antagonist
- The Exposition NPC Who Just Explains Things
- The Love Interest With No Inner Life Beyond Their Feelings For The Protagonist
