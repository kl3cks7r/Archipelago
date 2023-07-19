from typing import Set, Optional, Dict

from BaseClasses import ItemClassification, Location
from .Regions import CaveStoryRegion
from .Items import CaveStoryItem

LOCATIONS = [
    "First Cave Pickup",
    "Hermit Gunsmith Chest",
    "Mimiga Village Chest",
    "Reservior Pickup",
    "Yamanshita Farm Pickup",
    "Arthur's Grave Pickup"
]

EVENTS = [
    "Toroko Kidnapped"
]

class CaveStoryLocation(Location):
    game = "Cave Story"
    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: CaveStoryRegion):
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(CaveStoryItem(name, ItemClassification.progression, None, parent.player))