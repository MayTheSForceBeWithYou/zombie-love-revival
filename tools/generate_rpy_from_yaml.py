#!/usr/bin/env python3
"""
tools/generate_rpy_from_yaml.py
-------------------------------------------------------------------------------
YAML → Ren'Py content generator for Zombie Love Revival.

This script:
  1. Loads YAML data files from game/data/
  2. Validates their structure against expected schemas
  3. Generates or previews .rpy stub content for items, characters, and missions
  4. Can be run in "validate only" mode for CI

Usage:
    # Validate YAML and preview generated stubs (no files written)
    python tools/generate_rpy_from_yaml.py

    # Validate only (for CI)
    python tools/generate_rpy_from_yaml.py --validate-only

    # Write stub files to game/characters/ and game/systems/
    python tools/generate_rpy_from_yaml.py --write

Architecture:
    - Each load_* function handles one data type
    - Each validate_* function checks structure and reports errors
    - Each generate_* function produces Ren'Py stub text
    - main() orchestrates everything

Dependencies:
    pip install pyyaml
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install it with: pip install pyyaml")
    sys.exit(1)


# ---------------------------------------------------------------------------
# PATHS
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
DATA_DIR = REPO_ROOT / "game" / "data"
CHARACTERS_YAML = DATA_DIR / "characters.yaml"
MISSIONS_YAML = DATA_DIR / "missions.yaml"
ITEMS_YAML = DATA_DIR / "items.yaml"

OUTPUT_CHARS_DIR = REPO_ROOT / "game" / "characters"
OUTPUT_SYSTEMS_DIR = REPO_ROOT / "game" / "systems"


# ---------------------------------------------------------------------------
# LOADERS
# ---------------------------------------------------------------------------

def load_yaml(filepath: Path) -> dict:
    """
    Load and parse a YAML file.

    Args:
        filepath: Path to the YAML file

    Returns:
        Parsed YAML content as a dict

    Raises:
        SystemExit: If the file doesn't exist or cannot be parsed
    """
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    with filepath.open("r", encoding="utf-8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"ERROR: Failed to parse {filepath.name}:\n  {e}")
            sys.exit(1)


def load_characters() -> list:
    """Load and return the list of character definitions."""
    data = load_yaml(CHARACTERS_YAML)
    return data.get("characters", [])


def load_missions() -> list:
    """Load and return the list of mission definitions."""
    data = load_yaml(MISSIONS_YAML)
    return data.get("missions", [])


def load_items() -> list:
    """Load and return the list of item definitions."""
    data = load_yaml(ITEMS_YAML)
    return data.get("items", [])


# ---------------------------------------------------------------------------
# VALIDATORS
# ---------------------------------------------------------------------------

def validate_character(character: dict, index: int) -> list[str]:
    """
    Validate a single character entry against the expected schema.

    Args:
        character: Character dict from YAML
        index: Position in the characters list (for error messages)

    Returns:
        List of error strings (empty if valid)
    """
    errors = []
    required_fields = ["id", "name", "pronouns", "faction", "role", "motivations"]

    for field in required_fields:
        if field not in character:
            errors.append(f"Character[{index}]: missing required field '{field}'")

    char_id = character.get("id", f"<unknown[{index}]>")

    if "motivations" in character:
        if "primary" not in character["motivations"]:
            errors.append(f"Character '{char_id}': motivations.primary is required")

    return errors


def validate_mission(mission: dict, index: int) -> list[str]:
    """
    Validate a single mission entry against the expected schema.

    Args:
        mission: Mission dict from YAML
        index: Position in the missions list

    Returns:
        List of error strings (empty if valid)
    """
    errors = []
    required_fields = ["id", "title", "type", "chapter", "location", "description"]
    valid_types = {"scavenge", "escort", "negotiate", "investigate", "relationship", "crisis"}

    for field in required_fields:
        if field not in mission:
            errors.append(f"Mission[{index}]: missing required field '{field}'")

    mission_id = mission.get("id", f"<unknown[{index}]>")
    mission_type = mission.get("type", "")

    if mission_type and mission_type not in valid_types:
        errors.append(
            f"Mission '{mission_id}': invalid type '{mission_type}'. "
            f"Valid types: {', '.join(sorted(valid_types))}"
        )

    if "outcomes" in mission:
        outcomes = mission["outcomes"]
        if "success" not in outcomes:
            errors.append(f"Mission '{mission_id}': outcomes.success is required")
        if "failure" not in outcomes:
            errors.append(f"Mission '{mission_id}': outcomes.failure is required")

    return errors


def validate_item(item: dict, index: int) -> list[str]:
    """
    Validate a single item entry against the expected schema.

    Args:
        item: Item dict from YAML
        index: Position in the items list

    Returns:
        List of error strings (empty if valid)
    """
    errors = []
    required_fields = ["id", "name", "description", "type"]
    valid_types = {"consumable", "medical", "tool", "key_item", "trade", "misc"}

    for field in required_fields:
        if field not in item:
            errors.append(f"Item[{index}]: missing required field '{field}'")

    item_id = item.get("id", f"<unknown[{index}]>")
    item_type = item.get("type", "")

    if item_type and item_type not in valid_types:
        errors.append(
            f"Item '{item_id}': invalid type '{item_type}'. "
            f"Valid types: {', '.join(sorted(valid_types))}"
        )

    return errors


def validate_all(characters: list, missions: list, items: list) -> int:
    """
    Validate all data lists and report errors.

    Args:
        characters: List of character dicts
        missions: List of mission dicts
        items: List of item dicts

    Returns:
        Number of validation errors found
    """
    all_errors = []

    for i, char in enumerate(characters):
        all_errors.extend(validate_character(char, i))

    for i, mission in enumerate(missions):
        all_errors.extend(validate_mission(mission, i))

    for i, item in enumerate(items):
        all_errors.extend(validate_item(item, i))

    if all_errors:
        print(f"\n{'='*60}")
        print(f"VALIDATION ERRORS ({len(all_errors)} found):")
        print('='*60)
        for error in all_errors:
            print(f"  ✗ {error}")
        print()
    else:
        print("✓ All YAML data is valid.")

    return len(all_errors)


# ---------------------------------------------------------------------------
# GENERATORS
# ---------------------------------------------------------------------------

def generate_character_stub(character: dict) -> str:
    """
    Generate a Ren'Py character define stub from a character dict.

    Args:
        character: Character dict from YAML

    Returns:
        Ren'Py script text as a string
    """
    char_id = character["id"]
    name = character["name"]
    pronouns = character.get("pronouns", "they/them")
    role = character.get("role", "unknown")
    faction = character.get("faction", "none")
    primary_motivation = character.get("motivations", {}).get("primary", "unknown")

    lines = [
        f"# {'='*70}",
        f"# Character: {name}",
        f"# ID: {char_id}",
        f"# Pronouns: {pronouns}",
        f"# Faction: {faction}",
        f"# Role: {role}",
        f"# Primary motivation: {primary_motivation}",
        f"# {'='*70}",
        "",
        f"# TODO: Replace color placeholder with final palette value",
        f"define {char_id} = Character(\"{name}\", color=\"#ffffff\")",
        "",
    ]

    return "\n".join(lines)


def generate_item_registry_entry(item: dict) -> str:
    """
    Generate a Python dict entry for the item registry from an item dict.

    Args:
        item: Item dict from YAML

    Returns:
        Python dict entry as a formatted string
    """
    item_id = item["id"]
    name = item["name"]
    description = item["description"]
    item_type = item["type"]
    weight = item.get("weight", 1)
    value = item.get("value", 0)

    lines = [
        f'    "{item_id}": {{',
        f'        "name": "{name}",',
        f'        "description": "{description}",',
        f'        "type": "{item_type}",',
        f'        "weight": {weight},',
        f'        "value": {value},',
        f'    }},',
    ]
    return "\n".join(lines)


def generate_mission_label_stub(mission: dict) -> str:
    """
    Generate a Ren'Py label stub for a mission from a mission dict.

    Args:
        mission: Mission dict from YAML

    Returns:
        Ren'Py script text as a string
    """
    mission_id = mission["id"]
    title = mission["title"]
    description = mission.get("description", "").strip().replace("\n", " ")
    mission_type = mission.get("type", "unknown")
    chapter = mission.get("chapter", "?")
    primary_objective = mission.get("objectives", {}).get("primary", "")

    success_scene = mission.get("outcomes", {}).get("success", {}).get("next_scene", "placeholder")
    failure_scene = mission.get("outcomes", {}).get("failure", {}).get("next_scene", "placeholder")

    lines = [
        f"# Mission: {title} (Chapter {chapter})",
        f"# Type: {mission_type}",
        f"# Objective: {primary_objective}",
        "",
        f"label mission_{mission_id}_briefing:",
        f'    # TODO: Write briefing dialogue for "{title}"',
        f'    $ activate_mission("{mission_id}")',
        f"    return",
        "",
        f"label mission_{mission_id}_complete:",
        f'    # TODO: Write completion scene for "{title}"',
        f'    $ complete_mission("{mission_id}", outcome="success")',
        f"    jump {success_scene}",
        "",
        f"label mission_{mission_id}_failed:",
        f'    # TODO: Write failure scene for "{title}"',
        f'    $ complete_mission("{mission_id}", outcome="failure")',
        f"    jump {failure_scene}",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# PREVIEW / WRITE
# ---------------------------------------------------------------------------

def preview_all(characters: list, missions: list, items: list) -> None:
    """
    Print generated stubs to stdout for review.

    Args:
        characters: Validated character list
        missions: Validated mission list
        items: Validated item list
    """
    print("\n" + "="*60)
    print("GENERATED CHARACTER STUBS")
    print("="*60)
    for char in characters:
        print(generate_character_stub(char))

    print("\n" + "="*60)
    print("GENERATED ITEM REGISTRY ENTRIES")
    print("="*60)
    print("item_registry = {")
    for item in items:
        print(generate_item_registry_entry(item))
    print("}")

    print("\n" + "="*60)
    print("GENERATED MISSION LABEL STUBS")
    print("="*60)
    for mission in missions:
        print(generate_mission_label_stub(mission))


def write_character_stubs(characters: list) -> None:
    """
    Write character stub .rpy files to game/characters/.

    Args:
        characters: Validated character list
    """
    OUTPUT_CHARS_DIR.mkdir(parents=True, exist_ok=True)
    for char in characters:
        char_id = char["id"]
        output_path = OUTPUT_CHARS_DIR / f"{char_id}.rpy"
        stub_text = generate_character_stub(char)

        with output_path.open("w", encoding="utf-8") as f:
            f.write(stub_text)

        print(f"  Wrote: {output_path.relative_to(REPO_ROOT)}")


def write_mission_stubs(missions: list) -> None:
    """
    Write mission stub .rpy content to a single missions_generated.rpy file.

    Args:
        missions: Validated mission list
    """
    OUTPUT_SYSTEMS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_SYSTEMS_DIR / "missions_generated.rpy"

    header = (
        "# missions_generated.rpy\n"
        "# AUTO-GENERATED by tools/generate_rpy_from_yaml.py\n"
        "# Do not edit manually — edit game/data/missions.yaml and regenerate.\n\n"
    )

    content = header + "\n".join(generate_mission_label_stub(m) for m in missions)

    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)

    print(f"  Wrote: {output_path.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate YAML data and generate Ren'Py stubs for Zombie Love Revival."
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate YAML files; do not generate or preview output.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write generated stubs to game/ directories (default: preview only).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    print("Zombie Love Revival — YAML Validator & Generator")
    print("-" * 48)

    # Load data
    print("\nLoading YAML data files...")
    characters = load_characters()
    missions = load_missions()
    items = load_items()

    print(f"  Loaded {len(characters)} characters")
    print(f"  Loaded {len(missions)} missions")
    print(f"  Loaded {len(items)} items")

    # Validate
    print("\nValidating data...")
    error_count = validate_all(characters, missions, items)

    if error_count > 0:
        print(f"Validation failed with {error_count} error(s). Fix them before generating.")
        sys.exit(1)

    if args.validate_only:
        print("\nValidation complete. Exiting (--validate-only mode).")
        return

    # Generate
    if args.write:
        print("\nWriting generated stubs...")
        write_character_stubs(characters)
        write_mission_stubs(missions)
        print("\nDone. Review generated files before committing.")
    else:
        print("\nPreviewing generated output (use --write to save files):")
        preview_all(characters, missions, items)


if __name__ == "__main__":
    main()
