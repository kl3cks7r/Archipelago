from typing import Dict, List

from BaseClasses import Region

REGION_LOCATIONS: Dict[str, List[str]] = {
    "Menu": [],
    "First Cave": ["First Cave - Ledge", "First Cave - Hermit Gunsmith"],
    "Mimiga Village": ["Mimiga Village - Above Old Shack", "Mimiga Village - Reservior", "Mimiga Village - Yamanshita Farm"],
    "Mimiga Shack": [],
    "Mimiga Graveyard": ["Mimiga Village - Graveyard"],
    "Arthur's House": [],
    "Egg Corridor": ["Egg Corridor - Basil", "Egg Corridor - Outside Abode", "Egg Corridor - Egg 06", "Egg Corridor - Observation Room"],
    "Grasstown": ["Grasstown - Fan Ledge", "Grasstown - Ceiling", "Grasstown - Execution Room"],
    "Sand Zone": ["Sand Zone - Upper Passage", "Sand Zone - Sun Stone Paw Block Dupe 1"],
    "Labyrinth": ["Labyrinth - Labyrinth I Critter", "Labyrinth - Camp Upper Room"],
    "Core": ["Core - Robot Arm"],
    "Ruined Egg Corridor": ["Ruined Egg Corridor - Behind Dragon", "Ruined Egg Corridor - Observation Room"],
    "Outer Wall": ["Outer Wall - Clock Room"],
    "Plantation": ["Plantation - Stumpy Horde"],
    "Sacred Grounds": ["Sacred Ground - B1 Ledge"],
}

REGION_CONNECTIONS: Dict[str, List[str]] = {
    "Menu": ["First Cave"],
    "First Cave": ["Mimiga Village"],
    "Mimiga Village": ["Mimiga Shack", "Arthur's House"],
    "Mimiga Shack": ["Mimiga Graveyard"],
    "Arthur's House": ["Egg Corridor"],
    "Egg Corridor": ["Grasstown"],
    "Grasstown": ["Sand Zone"],
    "Sand Zone": ["Labyrinth"],
    "Labyrinth": ["Core"],
    "Core": ["Ruined Egg Corridor"],
    "Ruined Egg Corridor": ["Outer Wall"],
    "Outer Wall": ["Plantation"],
    "Plantation": ["Sacred Grounds"],
}

class CaveStoryRegion(Region):
    def __init__(self, name: str, world) -> None:
        super().__init__(name, world.player, world.multiworld)
        world.multiworld.regions.append(self)