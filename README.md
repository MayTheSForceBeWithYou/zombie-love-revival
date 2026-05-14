# 🧟 Zombie Love Revival

> *"Some things survive the apocalypse. Love is one of them."*

---

## Overview

**Zombie Love Revival** is an indie narrative game blending visual novel storytelling, light RPG mechanics, and a relationship simulator — all set against a zombie apocalypse backdrop. Players navigate a world where survival isn't just about bullets and barricades, but about the bonds you form with the dead, the living, and everyone in between.

This is a game about **connection under impossible circumstances**.

---

## Genre

- Visual Novel
- Light RPG / Relationship Simulator
- Narrative Survival
- Dark Comedy / Romance

---

## Inspiration

- *Disco Elysium* — dialogue depth, moral ambiguity, internal monologue
- *Oxenfree* — atmospheric tone, teen drama, supernatural tension
- *Night in the Woods* — emotional honesty, slice-of-life absurdism
- *The Walking Dead (Telltale)* — choice-driven narrative, loss and loyalty
- *Stardew Valley* — relationship-building loops, warmth inside bleakness

---

## Tech Stack

| Layer | Technology |
|---|---|
| Game Engine | [Ren'Py 8](https://www.renpy.org/) |
| Scripting | Python 3 |
| Game Data | YAML / JSON |
| CI/CD | GitHub Actions |
| Documentation | Markdown |
| Workflow | CLI-first, AI-agent-friendly |

---

## Setup Instructions

### Prerequisites

1. Install [Ren'Py 8](https://www.renpy.org/latest.html)
2. Install Python 3.10+
3. Install required Python packages:

```bash
pip install pyyaml
```

### Running the Game

1. Open the Ren'Py launcher
2. Click **Add Existing Project** and select this directory
3. Click **Launch Project**

### Running Dev Tools

```bash
# Validate YAML data files and preview generated content
python tools/generate_rpy_from_yaml.py
```

---

## Development Philosophy

This project is designed to be:

- **Modular** — each system lives in its own file and can be developed independently
- **Readable** — code is written for humans (and AI agents) first
- **Data-driven** — content lives in YAML files, not hardcoded scripts
- **AI-agent-friendly** — clear naming, consistent structure, rich comments
- **Rapidly iterable** — small files, small functions, fast feedback loops

We avoid:
- Premature optimization
- Complex inheritance chains
- Giant monolithic scripts
- Unnecessary abstractions

---

## Project Structure

```
zombie-love-revival/
├── .github/
│   └── workflows/
│       └── ci.yml              # CI: lint, validate, syntax check
├── docs/
│   ├── story_bible.md          # World, tone, themes, lore
│   └── character_bible.md      # Character profiles and dynamics
├── prompts/
│   ├── scene_writer.md         # AI prompt: write scenes
│   ├── dialogue_generator.md   # AI prompt: write dialogue
│   ├── mission_generator.md    # AI prompt: generate missions
│   └── character_generator.md  # AI prompt: create characters
├── tools/
│   └── generate_rpy_from_yaml.py  # YAML → Ren'Py content generator
├── game/
│   ├── script.rpy              # Main entry point and chapter routing
│   ├── screens.rpy             # UI screens (HUD, menus, overlays)
│   ├── options.rpy             # Game configuration and settings
│   ├── gui.rpy                 # GUI theme and visual styling
│   ├── audio/                  # Music and SFX assets
│   ├── images/                 # Sprites, backgrounds, CGs
│   ├── gui/                    # GUI image assets
│   ├── chapters/               # Per-chapter story scripts
│   ├── characters/             # Per-character define files
│   ├── systems/
│   │   ├── relationship_system.rpy
│   │   ├── inventory_system.rpy
│   │   └── mission_system.rpy
│   ├── data/
│   │   ├── characters.yaml
│   │   ├── missions.yaml
│   │   └── items.yaml
│   └── screens/                # Modular screen components
└── README.md
```

---

## AI-Assisted Workflow

This project is built with AI collaboration in mind. The `prompts/` directory contains structured prompts for use with AI coding assistants and language models.

### Workflow Pattern

1. **Data first** — Define characters, missions, and items in YAML (`game/data/`)
2. **Generate stubs** — Use `tools/generate_rpy_from_yaml.py` to scaffold `.rpy` files
3. **Write content** — Use prompts from `prompts/` to fill in scenes and dialogue
4. **Integrate** — Wire content into `game/chapters/` and `game/script.rpy`
5. **Validate** — CI checks syntax and formatting on every push

### For AI Agents

- Read `docs/story_bible.md` and `docs/character_bible.md` before generating any content
- Use prompts in `prompts/` as system instructions for content generation
- Keep each scene under 200 lines; split large chapters into multiple files
- Follow Ren'Py naming conventions: `snake_case` for labels, `CamelCase` for characters

---

## Contributing

This is an AI-assisted solo/small-team project. All contributions should:

- Match the tone described in `docs/story_bible.md`
- Follow character voices from `docs/character_bible.md`
- Pass CI checks before merging
- Keep files small and focused

---

## License

MIT License — see `LICENSE` for details (coming soon).
