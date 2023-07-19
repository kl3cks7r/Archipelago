from typing import Dict, List

from BaseClasses import Region

REGIONS: Dict[str, List[str]] = {
    "Menu": [],
    "Start Point": [],
    "First Cave": ["First Cave Pickup"],
    "Hermit Gunsmith": ["Hermit Gunsmith Chest"],
    "Mimiga Village": ["Mimiga Village Chest"],
    "Mimiga Save Point": [],
    "Mimiga Reservior": ["Reservior Pickup"],
    "Yamanshita Farm": ["Yamanshita Farm Pickup"],
    "Mimiga Old Shack": ["Toroko Kidnapped"],
    "Mimiga Graveyard": ["Arthur's Grave Pickup"],
    "Mimiga Assembly Hall": [],
    "Arthur's House": []
}

REGION_CONNECTIONS: Dict[str, List[str]] = {
    "Menu": ["Start Point"],
    "Start Point": ["First Cave"],
    "First Cave": ["Hermit Gunsmith", "Mimiga Village"],
    "Hermit Gunsmith": [],
    "Mimiga Village": ["Mimiga Save Point", "Mimiga Reservior", "Yamanshita Farm", "Mimiga Assembly Hall", "Mimiga Old Shack", "Mimiga Graveyard", "Arthur's House"],
    "Mimiga Save Point": [],
    "Mimiga Reservior": [],
    "Yamanshita Farm": [],
    "Mimiga Shack": [],
    "Mimiga Graveyard": [],
    "Mimiga Assembly Hall": [],
    "Arthur's House": []
}

class CaveStoryRegion(Region):
    def __init__(self, name: str, world) -> None:
        super().__init__(name, world.player, world.multiworld)
        world.multiworld.regions.append(self)