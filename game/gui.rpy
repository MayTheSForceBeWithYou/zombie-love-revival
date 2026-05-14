##############################################################################
# game/gui.rpy
# -----------------------------------------------------------------------------
# GUI theme and visual styling for Zombie Love Revival.
#
# This file controls:
#   - Color palette
#   - Font selections
#   - Dialogue box styling
#   - Button styling
#   - Layout constants
#
# Design intent:
#   The visual style should feel like a survivor's journal — worn, organic,
#   but legible. Earthy tones, faded greens, warm ambers. Not grimdark.
#   Not cute. Grounded.
#
# Ren'Py GUI reference:
#   https://www.renpy.org/doc/html/gui.html
##############################################################################


##############################################################################
# COLOR PALETTE
# Named variables for the game's core colors.
# Always reference these by name — never use raw hex codes in screens.
##############################################################################

define gui.COLOR_TEXT_PRIMARY     = "#e8d5b7"   # warm parchment — main text
define gui.COLOR_TEXT_SECONDARY   = "#c0a080"   # faded tan — secondary / captions
define gui.COLOR_TEXT_MUTED       = "#888877"   # dim — timestamps, labels
define gui.COLOR_ACCENT_GREEN     = "#7fb98f"   # survivor green — Riley, nature
define gui.COLOR_ACCENT_ROSE      = "#c09090"   # muted rose — Sable, warmth/grit
define gui.COLOR_ACCENT_GOLD      = "#d4a84b"   # warm gold — Crow, energy
define gui.COLOR_ACCENT_BLOOM     = "#9b7fc0"   # dusty violet — Bloom / Zed
define gui.COLOR_BG_DARK          = "#111111"   # near-black background
define gui.COLOR_BG_PANEL         = "#1e1c18"   # dark panel background
define gui.COLOR_BG_OVERLAY       = "#000000bb" # semi-transparent overlay


##############################################################################
# FONTS
# Place font files in game/gui/ if using custom fonts.
# Fallback to system fonts for now.
##############################################################################

define gui.default_font = "DejaVuSans.ttf"
    # ^ Ren'Py includes DejaVuSans by default. Replace when custom fonts arrive.

define gui.text_font      = gui.default_font
define gui.name_text_font = gui.default_font
define gui.interface_text_font = gui.default_font


##############################################################################
# TEXT SIZES
##############################################################################

define gui.text_size       = 22     # main dialogue text
define gui.name_text_size  = 24     # character name in dialogue box
define gui.interface_text_size = 18 # menus, buttons, UI labels
define gui.label_text_size = 14     # small captions, hints


##############################################################################
# DIALOGUE BOX
# The box that appears at the bottom of the screen during dialogue.
##############################################################################

define gui.textbox_height  = 185
define gui.textbox_yalign  = 1.0   # pin to bottom of screen

# Name tag above dialogue
define gui.namebox_width   = 300
define gui.namebox_height  = None  # auto-size to content

# Text padding inside the dialogue box
define gui.text_xpos   = 40
define gui.text_ypos   = 40
define gui.text_width  = 1180
define gui.text_color  = gui.COLOR_TEXT_PRIMARY

# Name text styling
define gui.name_xpos = 40
define gui.name_ypos = 0
define gui.name_text_color = gui.COLOR_TEXT_PRIMARY


##############################################################################
# CHOICE MENU (in-game branching dialogue options)
##############################################################################

define gui.choice_button_width    = 760
define gui.choice_button_text_size = 20

define gui.choice_button_text_color          = gui.COLOR_TEXT_PRIMARY
define gui.choice_button_hover_background    = "#3a3228"
define gui.choice_button_selected_background = "#2a2018"


##############################################################################
# MAIN MENU BUTTON STYLE
# Used by the main_menu_button style referenced in screens.rpy
##############################################################################

style main_menu_button:
    xsize 240
    ysize 48
    xalign 0.5
    background "#3a3228"
    hover_background "#5a4f3a"
    padding (12, 8)

style main_menu_button_text:
    size 20
    color gui.COLOR_TEXT_PRIMARY
    hover_color gui.COLOR_ACCENT_GOLD
    xalign 0.5


##############################################################################
# FRAME / PANEL STYLING
# Default style for UI panels and overlays.
##############################################################################

style game_frame:
    background gui.COLOR_BG_PANEL
    padding (16, 16)

style overlay_frame:
    background gui.COLOR_BG_OVERLAY
    padding (20, 20)


##############################################################################
# SCROLLBAR STYLING
##############################################################################

define gui.scrollbar_size = 8
define gui.scrollbar_tile = False


##############################################################################
# NVL MODE (full-screen narration)
# Used for chapter intros and internal monologue passages.
##############################################################################

define gui.nvl_width      = 960
define gui.nvl_xpos       = 160
define gui.nvl_text_color = gui.COLOR_TEXT_SECONDARY
define gui.nvl_text_size  = 22
