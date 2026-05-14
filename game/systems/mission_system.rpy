##############################################################################
# game/systems/mission_system.rpy
# -----------------------------------------------------------------------------
# Mission tracking and management for Zombie Love Revival.
#
# This system manages:
#   - Mission definitions (loaded from data or defined inline)
#   - Mission status tracking (inactive / active / completed / failed)
#   - Activating and completing missions
#   - Reward delivery (items, relationship changes, flags)
#   - Branching outcomes based on player choices
#
# Architecture:
#   - `missions` dict maps mission_id -> mission state
#   - Mission definitions come from game/data/missions.yaml (via tools/)
#   - The system is data-driven: logic reads from mission dicts
#   - Ren'Py labels handle the narrative; this system handles the state
#
# Mission statuses:
#   "inactive"   — exists but not yet available to the player
#   "active"     — player knows about and is working on this mission
#   "completed"  — player succeeded
#   "failed"     — player failed or abandoned
##############################################################################


##############################################################################
# DATA STRUCTURE
# missions = {
#     "mission_id": {
#         "title":       str,
#         "description": str,
#         "type":        str,      # scavenge / escort / negotiate / etc.
#         "chapter":     int,
#         "status":      str,      # inactive / active / completed / failed
#         "objectives":  dict,     # primary + secondary
#         "rewards":     dict,     # items, relationship_changes, flags_set
#     },
#     ...
# }
##############################################################################

default missions = {}


##############################################################################
# STARTER MISSION DEFINITIONS
# In a full build, these come from game/data/missions.yaml.
# They're defined here so the system works before the YAML pipeline is set up.
##############################################################################

init python:

    STARTER_MISSIONS = {

        "find_the_pharmacy": {
            "title": "Old Reliable",
            "description": (
                "The shelter's medical supplies are critically low. "
                "Sable needs someone to check the old Meridian Pharmacy "
                "on the edge of the Gray."
            ),
            "type": "scavenge",
            "chapter": 1,
            "location": "meridian_pharmacy",
            "status": "inactive",
            "objectives": {
                "primary": "Find medical supplies at Meridian Pharmacy",
                "secondary": [
                    "Find the prescription log (helps identify who lived nearby)",
                    "Return before nightfall (avoids Runner activity)",
                ],
            },
            "rewards": {
                "success": {
                    "items": {"medication": 3, "bandage": 5},
                    "relationship_changes": {"sable": {"trust": 2}},
                    "flags_set": {"pharmacy_cleared": True},
                    "next_scene": "mission_pharmacy_complete",
                },
                "failure": {
                    "items": {},
                    "relationship_changes": {"sable": {"trust": -1}},
                    "flags_set": {"pharmacy_failed": True},
                    "next_scene": "mission_pharmacy_failed",
                },
            },
        },

        "meet_the_cultivators": {
            "title": "Bloom Watchers",
            "description": (
                "Crow mentioned a group called the Cultivators who study "
                "the infected in the Bloom district. They might know something "
                "about Zed."
            ),
            "type": "investigate",
            "chapter": 1,
            "location": "bloom_greenhouse",
            "status": "inactive",
            "objectives": {
                "primary": "Make contact with the Cultivators",
                "secondary": [
                    "Learn what they know about Bonded cases",
                    "Don't damage any Bloom specimens (they will notice)",
                ],
            },
            "rewards": {
                "success": {
                    "items": {},
                    "relationship_changes": {
                        "zed": {"affection": 1},
                    },
                    "flags_set": {"met_cultivators": True},
                    "next_scene": "mission_cultivators_complete",
                },
                "failure": {
                    "items": {},
                    "relationship_changes": {},
                    "flags_set": {"cultivators_hostile": True},
                    "next_scene": "mission_cultivators_failed",
                },
            },
        },

        "crows_favor": {
            "title": "A Favor for Crow",
            "description": (
                "Crow needs a package delivered to the Undermarket — "
                "and would rather not explain what's in it. He promises "
                "it's worth your time."
            ),
            "type": "escort",
            "chapter": 1,
            "location": "undermarket",
            "status": "inactive",
            "objectives": {
                "primary": "Deliver the package to Crow's contact",
                "secondary": [
                    "Don't open the package",
                    "Return with the payment",
                ],
            },
            "rewards": {
                "success": {
                    "items": {"water_bottle": 3, "energy_bar": 2},
                    "relationship_changes": {"crow": {"affection": 2, "trust": 1}},
                    "flags_set": {"crow_favor_done": True},
                    "next_scene": "mission_crow_favor_complete",
                },
                "failure": {
                    "items": {},
                    "relationship_changes": {"crow": {"affection": -1}},
                    "flags_set": {"crow_favor_failed": True},
                    "next_scene": "mission_crow_favor_failed",
                },
            },
        },
    }


##############################################################################
# INITIALIZATION
##############################################################################

    def init_missions():
        """
        Set up the mission system with starter mission definitions.
        Called once at game start.
        """
        store.missions = {}
        for mission_id, mission_def in STARTER_MISSIONS.items():
            store.missions[mission_id] = dict(mission_def)  # shallow copy


##############################################################################
# MISSION STATE FUNCTIONS
##############################################################################

    def activate_mission(mission_id):
        """
        Make a mission available and active for the player.

        Args:
            mission_id (str): Key in the missions dict

        Example usage:
            $ activate_mission("find_the_pharmacy")
        """
        if mission_id in store.missions:
            store.missions[mission_id]["status"] = "active"
            title = store.missions[mission_id]["title"]
            renpy.show_screen("notification", message=f"Mission: {title}")


    def complete_mission(mission_id, outcome="success"):
        """
        Mark a mission as completed and apply its rewards.

        Args:
            mission_id (str): Key in the missions dict
            outcome (str): "success", "failure", or a custom outcome key

        This function applies:
          - Item rewards
          - Relationship changes
          - Flag updates

        Example usage:
            $ complete_mission("find_the_pharmacy")
            $ complete_mission("find_the_pharmacy", outcome="failure")
        """
        if mission_id not in store.missions:
            return

        mission = store.missions[mission_id]

        if outcome == "success":
            status = "completed"
        else:
            status = "failed"

        mission["status"] = status

        # Retrieve the outcome data
        outcome_data = mission.get("rewards", {}).get(outcome, {})
        if not outcome_data:
            return

        # Apply item rewards
        for item_id, qty in outcome_data.get("items", {}).items():
            add_item(item_id, qty)

        # Apply relationship changes
        for char_id, changes in outcome_data.get("relationship_changes", {}).items():
            relationship_change(
                char_id,
                affection_delta=changes.get("affection", 0),
                trust_delta=changes.get("trust", 0),
            )

        # Apply flags
        for flag_name, flag_value in outcome_data.get("flags_set", {}).items():
            store.flags[flag_name] = flag_value


    def get_mission_status(mission_id):
        """
        Return the current status of a mission.

        Args:
            mission_id (str): Key in missions dict

        Returns:
            str: "inactive", "active", "completed", "failed", or "unknown"
        """
        return store.missions.get(mission_id, {}).get("status", "unknown")


    def get_active_missions():
        """
        Return a list of all currently active mission dicts.

        Returns:
            list[dict]: Active mission definitions
        """
        return [
            m for m in store.missions.values()
            if m.get("status") == "active"
        ]


    def get_completed_missions():
        """
        Return a list of all completed mission dicts.

        Returns:
            list[dict]: Completed mission definitions
        """
        return [
            m for m in store.missions.values()
            if m.get("status") == "completed"
        ]


    def is_mission_done(mission_id):
        """
        Check if a mission has been completed (not just finished — succeeded).

        Args:
            mission_id (str): Key in missions dict

        Returns:
            bool
        """
        return get_mission_status(mission_id) == "completed"


##############################################################################
# EXAMPLE USAGE
# The label below is a reference example, not part of the real game.
##############################################################################

label example_mission_usage:

    # Activate a mission through story dialogue
    sable "I need someone to check the pharmacy."
    $ activate_mission("find_the_pharmacy")

    "[A mission marker appeared in your log.]"

    # ... later, after the player completes the scavenge ...

    # Complete with success and apply rewards automatically
    $ complete_mission("find_the_pharmacy", outcome="success")

    sable "You actually got the medication."
    sable "Good."
    # Note: Sable says "good" the way some people say "thank you"

    # Gate dialogue on a completed mission
    if is_mission_done("find_the_pharmacy"):
        sable "You held up your end. I won't forget that."

    return
