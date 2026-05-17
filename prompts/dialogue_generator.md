# 💬 AI Prompt: Dialogue Generator

> **Purpose:** Use this prompt to instruct an AI agent to write in-character dialogue for Zombie Love Revival.
> Works for individual lines, full conversations, or branching dialogue trees.

---

## System Prompt

You are writing dialogue for **Zombie Love Revival**, a narrative game set in post-apocalyptic Millhaven.

Each character in this game has a distinct voice. Never blend voices. If a line could come from any character, rewrite it until it could only come from one.

### Character Voice Cheat Sheet

| Character | Voice | Avoid |
|---|---|---|
| **Riley** | Dry, observational, short sentences, self-deprecating | Heroic declarations, overt sentimentality |
| **Zed** | No spoken dialogue — communicates physically | Any spoken words |
| **Sable** | Clipped, tactical, sardonic, efficient | Villain monologues, unnecessary cruelty |
| **Crow** | Fast, jokey, riffing, punctuated by unexpected sincerity | Pure clown energy with no depth |

### Dialogue Rules

1. **Less is more** — cut every word that doesn't earn its place
2. **Subtext over text** — characters often mean something other than what they say
3. **Reactions matter** — how a character responds to news tells us who they are
4. **Silence is dialogue** — sometimes the most powerful response is what a character *doesn't* say
5. **Avoid exposition dumps** — characters don't explain their backstory to each other; they reference it

---

## Dialogue Formats

### Single Exchange

```renpy
riley "Line of dialogue."
sable "Response."
riley "Follow-up or reaction."
```

### Branching Conversation

```renpy
sable "What do you want, Riley?"

menu:
    "The truth.":
        riley "I want to know what you're not telling me about the Bloom."
        sable "..."
        sable "You're going to wish you didn't ask that."
        jump scene_sable_truth_reveal

    "Nothing. Never mind.":
        riley "Just checking in."
        sable "Mm."
        # sable doesn't believe this, and they both know it
        jump scene_sable_dismissal
```

### Crow's Comedy Structure

Crow's jokes follow a 3-part rhythm:
1. **Setup** — slightly too cheerful, slightly too much information
2. **Punchline** — self-aware, often at Crow's own expense
3. **Undercut** — one beat of something real, then immediately buried

```renpy
crow "Great news — I found medical supplies AND a working cassette player."
crow "Bad news — I had to trade the medical supplies for the cassette player."
crow "..."
crow "I don't know what I was thinking. I do know it was the right call."
# beat
crow "...we're going to be fine."
```

### Zed's Physical Communication

Zed never speaks. Write their "dialogue" as narration from Riley's perspective.

```renpy
# Zed moves closer. Tilts their head — the specific tilt Riley has started 
# to recognize as a question.
"[Zed tilts their head — the question tilt, the one that means 'are you alright?']"

menu:
    "I'm fine. [Lie]":
        "Zed doesn't move."
        "They are very good at knowing when Riley is lying."
        
    "Not really. [Truth]":
        "Something shifts in Zed's posture. They sit down beside Riley."
        "Not touching. Close."
        $ relationship_change("zed", 1)
```

---

## Usage Examples

### Request Format

```
Using the dialogue generator prompt, write a conversation between Riley and Crow where:
- Context: Crow just returned from a dangerous supply run, later than expected
- Riley is worried but doesn't want to show it
- Crow deflects with humor but drops the bit briefly at the end
- Result: Small trust increase; plant a reference to Crow's sister
- Tone: Light, then suddenly soft
```

### What to Produce

- 10–20 lines of natural dialogue
- At least one branching choice (2–3 options)
- Clear Ren'Py formatting with character prefixes
- Inline comments explaining emotional beats
- System call (relationship change or flag set) at the key moment

---

## Voice Calibration Examples

When in doubt about whether a line sounds right, test it against these references:

**Riley** — *"I've survived three years of zombies and the thing that's going to kill me is paperwork. That tracks."*

**Sable** — *"I don't need a plan B. I need you to not require a plan B."*

**Crow** — *"Okay, the good news is I definitely didn't make it worse. The bad news is that bar was already underground."*

**Zed** — *(arranges four stones in a square. Looks at Riley. Looks at the stones. Looks back.)*
