from typing import Set, Optional, Dict

from BaseClasses import ItemClassification, Location
from .Regions import CaveStoryRegion
from .Items import CaveStoryItem

base_id = 0xD00_000

class CaveStoryLocation(Location):
    game = "Cave Story"
    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: CaveStoryRegion):
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(CaveStoryItem(name, ItemClassification.progression, None, parent.player))

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

ALL_LOCATIONS = {
    **{name: id for id, name in enumerate(LOCATIONS, base_id)},
    **{name: None for name in EVENTS}
}
