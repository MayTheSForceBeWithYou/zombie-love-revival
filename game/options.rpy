##############################################################################
# game/options.rpy
# -----------------------------------------------------------------------------
# Game configuration and global settings for Zombie Love Revival.
#
# This file controls:
#   - Basic game metadata (title, version, build)
#   - Window size and display settings
#   - Text speed, auto-forward, and accessibility options
#   - Save slot configuration
#   - Developer flags
#
# Ren'Py options reference:
#   https://www.renpy.org/doc/html/config.html
##############################################################################


##############################################################################
# GAME METADATA
##############################################################################

define config.name = "Zombie Love Revival"

# Short version shown in the title bar
define config.version = "0.1.0-dev"

# Developer info (used in error reports)
define build.name = "zombie_love_revival"


##############################################################################
# DISPLAY SETTINGS
##############################################################################

# Default window size — 1280x720 is standard for visual novels
define config.screen_width = 1280
define config.screen_height = 720

# Allow the player to toggle fullscreen
define config.window_title = "Zombie Love Revival"

# Default to windowed mode
default preferences.fullscreen = False


##############################################################################
# TEXT AND TIMING
##############################################################################

# Characters per second for text rollout
# 0 = instant; increase for typewriter effect
define config.default_text_cps = 0

# Auto-forward delay (seconds per character)
define config.afm_time = 15

# Rollback: allow players to rewind dialogue
define config.rollback_enabled = True


##############################################################################
# SAVE SYSTEM
##############################################################################

# Number of save slots (excluding autosave and quicksave)
define config.savedir = "zombie_love_revival"

# Number of autosave slots
define config.autosave_slots = 5


##############################################################################
# AUDIO
##############################################################################

# Default volume levels (0.0 to 1.0)
default preferences.music_volume = 0.7
default preferences.sfx_volume = 0.8
default preferences.voice_volume = 1.0

# Audio channel configuration
define config.has_music = True
define config.has_sound = True
define config.has_voice = False   # Enable when voice acting is added


##############################################################################
# TRANSITIONS
##############################################################################

# Default scene transition (used by "with" statements)
define config.with_statement_should_wait = True

# Transition presets — reference these by name in scripts
define dissolve_slow  = Dissolve(1.5)
define dissolve_fast  = Dissolve(0.3)
define fade_to_black  = Fade(0.5, 0.5, 0.5)


##############################################################################
# DEVELOPER FLAGS
# Set developer = True to enable Ren'Py developer tools (shift+D, etc.)
# Always False in production builds.
##############################################################################

define config.developer = True   # Set to False before shipping


##############################################################################
# SKIP AND ACCESSIBILITY
##############################################################################

# Allow skipping unread text (set False for story-first experience)
define config.allow_skipping = True

# Skip mode speed
define config.skip_delay = 75  # milliseconds between skipped lines


##############################################################################
# BUILD CONFIGURATION
# Controls what goes into the distribution package.
##############################################################################

init python:
    # Files to exclude from the build
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.*", None)     # hidden files
    build.classify("**.py", "all")    # include Python files in all builds

    # Source-only files (not shipped to players)
    build.documentation("*.md")
