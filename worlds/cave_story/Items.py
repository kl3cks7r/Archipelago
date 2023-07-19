from typing import Dict, Optional, NamedTuple

from BaseClasses import Item, ItemClassification
from . import base_id

class CaveStoryData(NamedTuple):
    name: str
    classification: ItemClassification
    item_id: Optional[int]
    def __init__(self, name: str, classification: ItemClassification,
                 item_id: Optional[int]):
        self = {name, classification, item_id}

class CaveStoryItem(Item):
    game = "Cave Story"
    def __init__(self, name: str, classification: ItemClassification,
                 item_id: Optional[int], player: int):
        super().__init__(name, classification, item_id, player)

WEAPONS_PROGRESSION = [
    "Polar Star"
    # "Fireball",
]

WEAPONS_USEFUL = [
    # "Machine Gun",
    # "Snake",
    # "Spur",
    # "Progressive Missile Launcher",
    # "Bubbler",
    # "Blade",
    # "Nemesis"
]

WEAPONS_FILLER = []

INV_PROGRESSION = [
    "Silver Locket",
    "Arthur's Key",
    # "ID Card",
    # "Santa's Key",
    # "Rusty Key",
    # "Gum Key",
    # "Jellyfish Juice",
    # "Charcoal",
    # "Gum Base",
    # "Explosive",
    # "Cure-All",
    # "Clinic Key",
    # "Tow Rope",
    # "Air Tank",
    # "Nikumaru Counter",
    # "Teleporter Room Key",
    # "Sue's Letter",
    # "Progressive Booster",
    # "Little Man",
    # "Ma Pignon",
    # "Iron Bond",
    # "Mimiga Mask",
    # "Broken Sprinkler",
    # "Working Sprinkler",
    # "Controller"
]

INV_USEFUL = [
    "Map System",
    # "Life Pot",
    # "Arms Barrier",
    # "Turbocharge",
]

INV_FILLER = [
    # "Chaco's Lipstick",
    # "Curly's Underwear",
    # "Whimsical Star",
    # "Alien Metal",
    # "Mushroom Badge",
    # "Clay Figure Metal"
]

PICKUPS_PROGRESSION = []

PICKUPS_USEFUL = [
    "+3 HP Life Capsule", #3
    # "+4 HP Life Capsule", #2
    # "+5 HP Life Capsule", #7
    # "+5 Max Missile Ammo" #4
    # "+24 Max Missile Ammo"
]

PICKUPS_FILLER = [
    # "Heart Bundle", #+6 HP
    # "Missle Bundle", #+3 Missiles
    # "Energy Refill", #+1 +5 +20
]

PROGRESSION_ITEMS = [(name, ItemClassification.progression) for name in [
    *WEAPONS_PROGRESSION,
    *INV_PROGRESSION,
    *PICKUPS_PROGRESSION
]]

USEFUL_ITEMS = [(name, ItemClassification.useful) for name in [
    *WEAPONS_USEFUL,
    *INV_USEFUL,
    *PICKUPS_USEFUL
]]

FILLER_ITEMS = [(name, ItemClassification.filler) for name in [
    *WEAPONS_FILLER,
    *INV_FILLER,
    *PICKUPS_FILLER
]]

ALL_ITEMS: Dict[str, CaveStoryData] = {name: CaveStoryData(name, classification, id) for
                       id, (name, classification) in enumerate([
                           *PROGRESSION_ITEMS,
                           *USEFUL_ITEMS,
                           *FILLER_ITEMS
                           ], base_id)}
