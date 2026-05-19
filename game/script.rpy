##############################################################################
# game/script.rpy
# -----------------------------------------------------------------------------
# Main entry point for Zombie Love Revival.
#
# Architecture:
#   - Character definitions live here (or in game/characters/)
#   - The "start" label launches the prologue
#   - Chapter labels route to game/chapters/chapter_XX.rpy files
#   - Systems are initialized in the "start" label before any story content
#
# Naming conventions:
#   - Labels:      snake_case         (e.g., scene_riley_meets_sable)
#   - Characters:  CamelCase variable (e.g., riley, sable, crow)
#   - Flags:       snake_case string  (e.g., "noticed_gifts")
#   - Images:      snake_case path    (e.g., bg_green_zone_gate)
##############################################################################


##############################################################################
# CHARACTER DEFINITIONS
# Each character has a display name and a color for their dialogue label.
# Sprites are defined separately in game/characters/ when assets exist.
##############################################################################

define riley = Character("Riley", color="#a8d8a8")
    # Protagonist. Soft green — alive, growing, slightly uncertain.

define sable = Character("Sable", color="#c0a0a0")
    # Survivor leader. Muted rose — warmth buried under pragmatism.

define crow = Character("Crow", color="#f0d080")
    # Comic relief / hidden depth. Warm gold — energy, wit, and heat.

define narrator = Character(None, kind=nvl)
    # Full-screen narration. Used for chapter transitions and internal monologue.

# Zed has no spoken dialogue. Their "lines" are narrated by Riley.
# We define them here for reference only — do not use as a speaking character.
# define zed = Character("Zed")  # <-- intentionally commented out


# Placeholder backgrounds until art assets exist.
image bg green_zone_gate = Solid(
    "#2a3a2a",
    xsize=config.screen_width,
    ysize=config.screen_height,
)


##############################################################################
# GAME START
# This label is called automatically when a new game begins.
# Initialize all systems here before any story content.
##############################################################################

label start:

    # --- Initialize relationship system ---
    # Sets all affection/trust values to their defaults.
    $ init_relationships()

    # --- Initialize inventory system ---
    $ init_inventory()

    # --- Initialize mission system ---
    $ init_missions()

    # --- Set persistent game flags ---
    $ flags = {}

    # --- Begin the prologue ---
    jump chapter_01_prologue


##############################################################################
# CHAPTER ROUTING
# Each chapter is defined in its own file in game/chapters/.
# This section provides a central map of chapter entry points.
#
# To add a new chapter:
#   1. Create game/chapters/chapter_XX.rpy
#   2. Define the entry label: label chapter_XX_prologue:
#   3. Add a jump below for reference
##############################################################################

# Chapter 1: Arrival
# label chapter_01_prologue: (defined in game/chapters/chapter_01.rpy)

# Chapter 2: The Bloom
# label chapter_02_prologue: (defined in game/chapters/chapter_02.rpy)

# Add future chapters here as the project grows.


##############################################################################
# PLACEHOLDER CHAPTER — Remove when real chapters are written
# This is a minimal starter scene so the game launches without errors.
##############################################################################

label chapter_01_prologue:

    scene black with dissolve_fast
    play music "audio/ambient_gray.ogg" fadein 2.0
    # ^ Placeholder path — this audio file does not exist yet.
    #   Create game/audio/ambient_gray.ogg when audio assets are available.
    #   Ren'Py will silently skip missing audio files during development.

    narrator """
    Millhaven, Year 3.

    The city breathed differently now.
    """

    narrator """
    You've been here eighteen months.
    Long enough that you've stopped counting the days.

    Long enough that you've started calling it home.
    """

    scene bg green_zone_gate with dissolve_fast
    # ^ Placeholder: bg_green_zone_gate.png should be in game/images/

    riley "Right. Day three hundred and something."

    riley "Let's see what the apocalypse has planned."

    # --- Transition to main hub (placeholder) ---
    jump placeholder_main_hub


label placeholder_main_hub:

    # This label will be replaced by the real hub scene in Chapter 1.
    # For now it just ends the demo gracefully.

    narrator "[[ Chapter 1 content goes here. See game/chapters/chapter_01.rpy ]]"

    return
