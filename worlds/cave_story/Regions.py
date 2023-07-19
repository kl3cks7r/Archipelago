from typing import Dict, List

from BaseClasses import Entrance, Region
from . import CaveStoryWorld
from .Locations import CaveStoryLocation

REGIONS: Dict[str, List[str]] = {
    "Menu": [],
    "Start Point": [],
    "First Cave": ["First Cave Pickup"],
    "Hermit Gunsmith": ["Hermit Gunsmith Chest"],
    "Mimiga Village": ["Mimiga Village Chest"],
    "Mimiga Save Point": [],
    "Mimiga Reservior": ["Reservior Pickup"],
    "Yamanshita Farm": ["Yamanshita Farm Pickup"],
    "Mimiga Shack": ["Toroko Kidnapped"],
    "Mimiga Graveyard": ["Arthur's Grave Pickup"],
    "Mimiga Assembly Hall": [],
    "Arthur's House": []
}

REGION_CONNECTIONS: Dict[str, List[str]] = {
    "Menu": ["Start Point"],
    "Start Point": ["First Cave"],
    "First Cave": ["Hermit Gunsmith", "Mimiga Village"],
    "Hermit Gunsmith": [],
    "Mimiga Village": ["Mimiga Save Point", "Mimiga Reservior", "Yamanshita Farm", "Mimiga Assembly Hall", "Mimiga Old Shack", "Arthur's House"],
    "Mimiga Save Point": [],
    "Mimiga Reservior": [],
    "Yamanshita Farm": [],
    "Mimiga Shack": [],
    "Mimiga Graveyard": [],
    "Mimiga Assembly Hall": [],
    "Arthur's House": []
}

class CaveStoryRegion(Region):
    def __init__(self, name: str, world: CaveStoryWorld) -> None:
        super().__init__(name, world.player, world.multiworld)
        self.add_locations(self.multiworld.worlds[self.player].location_name_to_id)
        world.multiworld.regions.append(self)

    def add_locations(self, name_to_id: Dict[str, int]) -> None:
        for loc in REGIONS[self.name]:
            self.locations.append(CaveStoryLocation(loc, self, name_to_id.get(loc, None)))

    def add_exits(self, exits: List[str]) -> None:
        for exit in exits:
            ret = Entrance(self.player, f"{self.name} -> {exit}", self)
            self.exits.append(ret)
            ret.connect(self.multiworld.get_region(exit, self.player))