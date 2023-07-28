from typing import Optional, Dict

from BaseClasses import ItemClassification, Location
from .Regions import CaveStoryRegion
from .Items import CaveStoryItem

base_id = 0xD00_000

# class CaveStoryLocationData:
#     name: str
#     item_id: Optional[int]
#     def __init__(self, name: str, classification: ItemClassification,
#                  item_id: Optional[int]):
#         self.name = name
#         self.item_id = item_id

class CaveStoryLocation(Location):
    game = "Cave Story"
    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: CaveStoryRegion):
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(CaveStoryItem(name, ItemClassification.progression, None, parent.player))

ALL_LOCATIONS: Dict[str, Optional[int]] = {
    "Egg Corridor - Basil" : base_id+101,
    "Egg Corridor - Outside Abode" : base_id+102,
    "Egg Corridor - Egg 06" : base_id+140,
    "Egg Corridor - Observation Room" : base_id+200,
    "Grasstown - Fan Ledge" : base_id+218,
    "Grasstown - Ceiling" : base_id+220,
    "Sand Zone - Upper Passage" : base_id+270,
    "Sand Zone - Sun Stone Paw Block Dupe 1" : base_id+271,
    #"Sand Zone - Sun Stone Paw Block Dupe 2" : base_id+279,
    "First Cave - Ledge" : base_id+304,
    "Mimiga Village - Above Old Shack" : base_id+322,
    "Mimiga Village - Reservior" : base_id+370,
    "Mimiga Village - Graveyard" : base_id+390,
    "Mimiga Village - Yamanshita Farm" : base_id+412,
    #"Gum - Reward" : base_id+501,
    "Grasstown - Execution Room" : base_id+540,
    #"Grasstown - Grasstown Hut" : base_id+550,
    "Labyrinth - Labyrinth I Critter" : base_id+642,
    "Labyrinth - Camp Upper Room" : base_id+705,
    "Core - Robot Arm" : base_id+834,
    "Ruined Egg Corridor - Behind Dragon" : base_id+880,
    "Ruined Egg Corridor - Observation Room" : base_id+920,
    "Plantation - Stumpy Horde" : base_id+1043,
    "Sacred Ground - B1 Ledge" : base_id+1530,
    "First Cave - Hermit Gunsmith" : base_id+1640,
    "Outer Wall - Clock Room" : base_id+1700,
    "Victory" : None
}
