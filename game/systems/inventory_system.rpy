##############################################################################
# game/systems/inventory_system.rpy
# -----------------------------------------------------------------------------
# Item tracking and inventory management for Zombie Love Revival.
#
# This system manages:
#   - Adding and removing items
#   - Checking item quantities
#   - A simple inventory UI (via screens.rpy)
#   - Item metadata (description, type, rarity)
#
# Architecture:
#   - `inventory` is a dict mapping item_id -> quantity
#   - `item_registry` is a dict mapping item_id -> metadata
#   - Item definitions come from game/data/items.yaml (loaded at init)
#   - Functions are defined in an init python block
#
# Design intent:
#   Items should feel like real survivor possessions — not magical game tokens.
#   Scarcity matters. Finding a working flashlight should feel like something.
##############################################################################


##############################################################################
# DATA STRUCTURES
##############################################################################

default inventory = {}
    # { "item_id": quantity (int), ... }

default item_registry = {}
    # { "item_id": { "name": str, "description": str, "type": str, "weight": int }, ... }


##############################################################################
# INITIALIZATION
# Called once at game start via `$ init_inventory()` in script.rpy
##############################################################################

init python:

    def init_inventory():
        """
        Set up the inventory system.
        Loads item definitions from the registry and starts with starter items.
        """
        # Start with an empty inventory
        store.inventory = {}

        # Starter items — give the player a minimal survival kit
        _add_item("water_bottle", 2)
        _add_item("energy_bar", 1)
        _add_item("bandage", 3)

        # Item registry — populated here as a fallback.
        # In a full build, this is loaded from game/data/items.yaml via tools/
        store.item_registry = {
            "water_bottle": {
                "name": "Water Bottle",
                "description": "Clean water. Getting harder to find.",
                "type": "consumable",
                "weight": 1,
            },
            "energy_bar": {
                "name": "Energy Bar",
                "description": "Stale. Still better than nothing.",
                "type": "consumable",
                "weight": 1,
            },
            "bandage": {
                "name": "Bandage",
                "description": "Clean bandage. Keep wounds from getting worse.",
                "type": "medical",
                "weight": 1,
            },
            "crowbar": {
                "name": "Crowbar",
                "description": "Crow calls his 'Old Reliable'. You have your own.",
                "type": "tool",
                "weight": 3,
            },
            "notebook": {
                "name": "Notebook",
                "description": "Half-filled. Someone's thoughts. You try not to read it.",
                "type": "key_item",
                "weight": 1,
            },
            "medication": {
                "name": "Medication",
                "description": "Prescription. The name on the bottle isn't yours.",
                "type": "medical",
                "weight": 1,
            },
        }


##############################################################################
# CORE FUNCTIONS
##############################################################################

    def _add_item(item_id, quantity=1):
        """
        Internal: add an item without notification.
        Use add_item() for gameplay calls.
        """
        if item_id in store.inventory:
            store.inventory[item_id] += quantity
        else:
            store.inventory[item_id] = quantity


    def add_item(item_id, quantity=1):
        """
        Add one or more of an item to the player's inventory.

        Args:
            item_id (str): Item identifier from item_registry
            quantity (int): Number of items to add (default: 1)

        Shows a notification to the player.

        Example usage in a .rpy script:
            $ add_item("bandage", 2)
            $ add_item("crowbar")
        """
        _add_item(item_id, quantity)

        item_name = get_item_name(item_id)
        if quantity == 1:
            renpy.show_screen("notification", message=f"+ {item_name}")
        else:
            renpy.show_screen("notification", message=f"+ {item_name} ×{quantity}")


    def remove_item(item_id, quantity=1):
        """
        Remove one or more of an item from the player's inventory.

        Args:
            item_id (str): Item identifier
            quantity (int): Number to remove (default: 1)

        Returns:
            bool: True if removal succeeded, False if insufficient quantity

        Example usage:
            $ remove_item("bandage")
            if remove_item("water_bottle", 2):
                riley "Here, take these."
        """
        current = store.inventory.get(item_id, 0)
        if current < quantity:
            return False

        store.inventory[item_id] = current - quantity
        if store.inventory[item_id] <= 0:
            del store.inventory[item_id]

        return True


    def has_item(item_id, quantity=1):
        """
        Check whether the player has at least `quantity` of an item.

        Args:
            item_id (str): Item identifier
            quantity (int): Minimum required quantity (default: 1)

        Returns:
            bool

        Example usage in a .rpy menu:
            menu:
                "Give Crow a bandage" if has_item("bandage"):
                    $ remove_item("bandage")
                    $ relationship_change("crow", affection_delta=1)
        """
        return store.inventory.get(item_id, 0) >= quantity


    def get_item_count(item_id):
        """
        Return how many of an item the player currently has.

        Args:
            item_id (str): Item identifier

        Returns:
            int: Quantity (0 if not in inventory)
        """
        return store.inventory.get(item_id, 0)


    def get_item_name(item_id):
        """
        Return the display name for an item.

        Args:
            item_id (str): Item identifier

        Returns:
            str: Display name, or the item_id itself as a fallback
        """
        return store.item_registry.get(item_id, {}).get("name", item_id)


    def get_item_description(item_id):
        """
        Return the description for an item.

        Args:
            item_id (str): Item identifier

        Returns:
            str: Description string, or empty string if not found
        """
        return store.item_registry.get(item_id, {}).get("description", "")


##############################################################################
# EXAMPLE USAGE IN SCRIPTS
# The label below is a reference example, not part of the real game.
##############################################################################

label example_inventory_usage:

    # Give the player a key item during a scene
    "[Riley finds an old notebook tucked under the counter.]"

    menu:
        "Take it.":
            $ add_item("notebook")
            riley "Someone left this here. Or forgot it. Or couldn't carry it anymore."
            riley "I'm not sure which is worse."

        "Leave it.":
            riley "Not everything left behind needs to be carried."
            # Note: this choice can matter later if a character asks about the notebook

    # Example: gate a dialogue option on having an item
    if has_item("bandage"):
        menu:
            "Offer Crow a bandage" if has_item("bandage"):
                $ remove_item("bandage")
                $ relationship_change("crow", affection_delta=1)
                crow "Oh thank god. Okay. Okay, this is going to be fine."

    return
