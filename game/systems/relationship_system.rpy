##############################################################################
# game/systems/relationship_system.rpy
# -----------------------------------------------------------------------------
# Relationship tracking for Zombie Love Revival.
#
# This system manages:
#   - Affection values  (emotional warmth / romantic connection)
#   - Trust values      (reliability / willingness to share information)
#   - Helper functions  (change values, check thresholds, get labels)
#   - Dialogue branching based on relationship state
#
# Architecture:
#   - All relationship data lives in the `relationships` dict (Python, not store)
#   - Helper functions are defined as Python functions in an init block
#   - Scripts call these functions with `$ function_name(args)`
#   - Screens read `relationships` directly
#
# Scale: -10 (hostile) to +10 (deep bond). Default: 0 (neutral).
##############################################################################


##############################################################################
# DATA STRUCTURE
# relationships = {
#     "character_id": {
#         "name":      str,      # display name
#         "affection": int,      # -10 to +10
#         "trust":     int,      # -10 to +10
#     },
#     ...
# }
##############################################################################

default relationships = {}


##############################################################################
# INITIALIZATION
# Called once at game start via `$ init_relationships()` in script.rpy
##############################################################################

init python:

    def init_relationships():
        """Set all relationship values to their starting defaults.

        These values represent Riley's initial feelings toward each character,
        not the inverse. Relationships are intentionally asymmetric — Crow
        is immediately enthusiastic about Riley (his YAML default toward Riley
        is 2), but Riley starts only mildly warm toward Crow (+1). The gap
        closes naturally through story interactions.
        """
        store.relationships = {
            "zed": {
                "name": "Zed",
                "affection": 0,   # Riley: neutral / cautious at first meeting
                "trust": 0,
            },
            "sable": {
                "name": "Sable",
                "affection": 0,   # Riley: neutral / professional distance
                "trust": 0,
            },
            "crow": {
                "name": "Crow",
                "affection": 1,   # Riley: finds Crow pleasant but hasn't committed yet
                "trust": 0,       # Note: Crow's own default toward Riley is 2 (more enthusiastic)
            },
        }


##############################################################################
# HELPER FUNCTIONS
##############################################################################

    def relationship_change(character_id, affection_delta=0, trust_delta=0):
        """
        Adjust affection and/or trust for a character.

        Args:
            character_id (str): Key in the relationships dict (e.g., "sable")
            affection_delta (int): Amount to add to affection (-10 to +10 range)
            trust_delta (int): Amount to add to trust

        Clamps values to the [-10, +10] range automatically.

        Example usage in a .rpy script:
            $ relationship_change("crow", affection_delta=1)
            $ relationship_change("sable", trust_delta=-1)
            $ relationship_change("zed", affection_delta=2, trust_delta=1)
        """
        if character_id not in store.relationships:
            return  # Silently skip unknown characters

        rel = store.relationships[character_id]

        if affection_delta:
            rel["affection"] = max(-10, min(10, rel["affection"] + affection_delta))

        if trust_delta:
            rel["trust"] = max(-10, min(10, rel["trust"] + trust_delta))

        # Show a brief HUD notification on significant changes
        if abs(affection_delta) >= 2 or abs(trust_delta) >= 2:
            name = rel["name"]
            if affection_delta > 0:
                renpy.show_screen("notification", message=f"{name}: ♥ +{affection_delta}")
            elif affection_delta < 0:
                renpy.show_screen("notification", message=f"{name}: ♥ {affection_delta}")


    def get_affection(character_id):
        """
        Return the current affection value for a character.

        Args:
            character_id (str): Key in relationships dict

        Returns:
            int: Affection value, or 0 if character not found
        """
        return store.relationships.get(character_id, {}).get("affection", 0)


    def get_trust(character_id):
        """
        Return the current trust value for a character.

        Args:
            character_id (str): Key in relationships dict

        Returns:
            int: Trust value, or 0 if character not found
        """
        return store.relationships.get(character_id, {}).get("trust", 0)


    def relationship_label(character_id):
        """
        Return a human-readable label for the current relationship state.

        Args:
            character_id (str): Key in relationships dict

        Returns:
            str: Label like "Stranger", "Friend", "Bonded", etc.
        """
        affection = get_affection(character_id)

        if affection <= -5:
            return "Hostile"
        elif affection <= -1:
            return "Wary"
        elif affection <= 2:
            return "Acquaintance"
        elif affection <= 5:
            return "Friendly"
        elif affection <= 8:
            return "Close"
        else:
            return "Bonded"


    def check_relationship(character_id, min_affection=None, min_trust=None):
        """
        Check whether a relationship meets minimum thresholds.
        Use this to gate dialogue options or scenes.

        Args:
            character_id (str): Key in relationships dict
            min_affection (int, optional): Required minimum affection
            min_trust (int, optional): Required minimum trust

        Returns:
            bool: True if all specified thresholds are met

        Example usage in a .rpy menu:
            menu:
                "Open up to Sable" if check_relationship("sable", min_trust=3):
                    ...
        """
        if min_affection is not None:
            if get_affection(character_id) < min_affection:
                return False
        if min_trust is not None:
            if get_trust(character_id) < min_trust:
                return False
        return True


##############################################################################
# EXAMPLE DIALOGUE BRANCHING
# This label demonstrates how relationship values gate dialogue options.
# It is NOT part of the actual game — it's a reference example.
#
# To see this in action, jump to: label example_relationship_branch
##############################################################################

label example_relationship_branch:

    # Example: Sable offers different responses based on trust level

    if check_relationship("sable", min_trust=4):
        # High trust — Sable is candid
        sable "We lost two people on the north run. I didn't want to tell the council yet."
        sable "You're the only one who'd understand why."

    elif check_relationship("sable", min_trust=1):
        # Moderate trust — Sable is guarded but not hostile
        sable "The run had complications. I'm handling it."
        sable "Don't ask me for details right now."

    else:
        # Low trust — Sable deflects entirely
        sable "Run was fine. We're good."
        # Note: this is a lie, and the player probably knows it

    menu:
        "I won't push." if check_relationship("sable", min_trust=0):
            $ relationship_change("sable", trust_delta=1)
            riley "Understood. Let me know if you need anything."

        "I need to know what's going on." if check_relationship("sable", min_trust=2):
            $ relationship_change("sable", trust_delta=-1)
            riley "Sable, I'm not going to pretend I didn't notice."
            sable "..."
            sable "Two days. Give me two days."

    return
