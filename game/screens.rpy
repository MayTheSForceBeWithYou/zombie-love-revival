##############################################################################
# game/screens.rpy
# -----------------------------------------------------------------------------
# UI screens for Zombie Love Revival.
#
# This file defines:
#   - The main menu screen
#   - The in-game HUD (relationship indicators, day counter)
#   - The inventory overlay
#   - The mission log overlay
#   - A generic notification screen
#
# Architecture note:
#   Screens are kept thin — they display data from the systems in game/systems/.
#   Business logic lives in those system files, not here.
#
# Ren'Py screen language reference:
#   https://www.renpy.org/doc/html/screens.html
##############################################################################


##############################################################################
# MAIN MENU SCREEN
# Shown when the player starts the application or returns to menu.
##############################################################################

screen main_menu():
    tag menu

    # Background image — replace with actual art when available
    add "gui/main_menu_bg.png"

    # Game title
    vbox:
        xalign 0.5
        ypos 0.3

        text "Zombie Love Revival":
            size 48
            color "#e8d5b7"
            xalign 0.5

        text "Some things survive the apocalypse.":
            size 18
            color "#c0a080"
            xalign 0.5

    # Navigation buttons
    vbox:
        xalign 0.5
        yalign 0.7
        spacing 12

        textbutton "New Game":
            action Start()
            style "main_menu_button"

        textbutton "Continue":
            action ShowMenu("load")
            style "main_menu_button"
            sensitive persistent._seen_ever  # only if game was played before

        textbutton "Settings":
            action ShowMenu("preferences")
            style "main_menu_button"

        textbutton "Quit":
            action Quit(confirm=True)
            style "main_menu_button"


##############################################################################
# IN-GAME HUD
# Displayed during gameplay to show key status indicators.
# Call: show screen hud() / hide screen hud
##############################################################################

screen hud():
    # Non-interactive overlay — appears on top of scenes
    zorder 5

    # Day counter — top left
    frame:
        xpos 10
        ypos 10
        padding (8, 4)
        background "#00000088"

        hbox:
            spacing 8
            text "Day":
                color "#aaaaaa"
                size 14
            text "[day_count]":
                color "#ffffff"
                size 14

    # Relationship quick-view — top right
    # Shows affection/trust for the last-interacted character
    frame:
        xalign 1.0
        xoffset -10
        ypos 10
        padding (8, 4)
        background "#00000088"

        vbox:
            spacing 2
            for char_id, char_data in relationships.items():
                hbox:
                    spacing 6
                    text "[char_data['name']]":
                        color "#cccccc"
                        size 12
                    text "♥ [char_data['affection']]":
                        color "#ff9999"
                        size 12


##############################################################################
# INVENTORY SCREEN
# Shown when player opens their inventory.
# Call: show screen inventory_screen()
##############################################################################

screen inventory_screen():
    tag overlay
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 400
        padding (20, 20)
        background "#1a1a1a"

        vbox:
            spacing 10

            # Header
            hbox:
                xfill True
                text "Inventory":
                    size 24
                    color "#e8d5b7"
                textbutton "✕":
                    action Hide("inventory_screen")
                    xalign 1.0

            # Item list
            if inventory:
                vpgrid:
                    cols 1
                    ymaximum 300
                    scrollbars "vertical"

                    for item_id, quantity in inventory.items():
                        hbox:
                            spacing 10
                            text "[item_id]":
                                color "#cccccc"
                                size 16
                                xminimum 200
                            text "x[quantity]":
                                color "#aaaaaa"
                                size 16
            else:
                text "Nothing here yet.":
                    color "#777777"
                    size 16
                    xalign 0.5
                    yalign 0.5


##############################################################################
# MISSION LOG SCREEN
# Shown when player opens their mission log.
##############################################################################

screen mission_log_screen():
    tag overlay
    modal True

    frame:
        xalign 0.5
        yalign 0.5
        xsize 650
        ysize 450
        padding (20, 20)
        background "#1a1a1a"

        vbox:
            spacing 10

            # Header
            hbox:
                xfill True
                text "Mission Log":
                    size 24
                    color "#e8d5b7"
                textbutton "✕":
                    action Hide("mission_log_screen")
                    xalign 1.0

            # Active missions
            text "Active":
                size 14
                color "#aaaaaa"

            for mission in get_active_missions():
                frame:
                    padding (8, 6)
                    background "#2a2a2a"
                    vbox:
                        text "[mission['title']]":
                            color "#ffffff"
                            size 16
                        text "[mission['description']]":
                            color "#999999"
                            size 13

            # Completed missions
            if get_completed_missions():
                text "Completed":
                    size 14
                    color "#aaaaaa"

                for mission in get_completed_missions():
                    text "✓ [mission['title']]":
                        color "#558855"
                        size 14


##############################################################################
# NOTIFICATION SCREEN
# Lightweight popup for item gains, relationship changes, etc.
# Call: show screen notification("Message here")
# Auto-hides after a short delay.
##############################################################################

screen notification(message):
    timer 2.5 action Hide("notification")

    frame:
        xalign 0.5
        yalign 0.05
        padding (12, 8)
        background "#000000bb"

        text "[message]":
            color "#e8d5b7"
            size 16
            xalign 0.5
