from typing import Optional, Dict

from BaseClasses import ItemClassification, Location, Region
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

    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: Region):
        super().__init__(player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(CaveStoryItem(
                name, ItemClassification.progression, None, parent.player))


ALL_LOCATIONS: Dict[str, Optional[int]] = {
    "Egg Corridor - Basil Spot": base_id+0,
    "Egg Corridor - Cthulhu's Abode": base_id+1,
    "Egg No. 06 - Chest": base_id+2,
    "Egg Observation Room - Chest": base_id+3,
    "Grasstown - West Floor": base_id+4,
    "Grasstown - West Ceiling": base_id+5,
    "Grasstown - East Chest": base_id+6,
    "Grasstown - Kazuma Crack": base_id+7,
    "Grasstown - Kazuma Chest": base_id+8,
    "Grasstown - Kulala": base_id+9,
    "Santa's House - Santa": base_id+10,
    "Santa's House - Santa's Fireplace": base_id+11,
    "Chaco's House - Chaco's Bed": base_id+12,
    "Power Room - MALCO": base_id+13,
    "Grasstown Hut - Chest": base_id+14,
    "Execution Chamber - Treasure": base_id+15,
    "Gum - Chest": base_id+16,
    "Labyrinth B - Booster Chest": base_id+17,
    "Boulder Chamber - Chest": base_id+18,
    "Core - Robot's Arm": base_id+19,
    "Core - Drowned Curly": base_id+20,
    "Main Artery - Ironhead Boss": base_id+21,
    "Labyrinth I - Behind Critter": base_id+22,
    "Labyrinth Shop - Chaba Chest (Machine Gun)": base_id+23,
    "Labyrinth Shop - Chaba Chest (Fireball)": base_id+24,
    "Labyrinth Shop - Chaba Chest (Spur)": base_id+25,
    "Camp - Dr. Gero": base_id+26,
    "Camp - Chest": base_id+27,
    "Clinic Ruins - Puu Black Boss": base_id+28,
    "Last Cave (Hidden) - Red Demon Boss": base_id+29,
    "Sacred Grounds - B1 - Ledge": base_id+30,
    "Sacred Grounds - B3 - Chest": base_id+31,
    "First Cave - West Ledge": base_id+32,
    "Hermit Gunsmith - Chest": base_id+33,
    "Hermit Gunsmith - Tetsuzou": base_id+34,
    "Mimiga Village - Chest": base_id+35,
    "Yamashita Farm - Pool": base_id+36,
    "Reservoir - Underwater": base_id+37,
    "Assembly Hall - Fireplace": base_id+38,
    "Graveyard - Arthur's Grave": base_id+39,
    "Graveyard - Mr. Little": base_id+40,
    "Storage - Chest": base_id+41,
    "Storage - Ma Pignon Boss": base_id+42,
    "Arthur's House - Professor Booster": base_id+43,
    "Plantation - Kanpachi's Bucket": base_id+44,
    "Plantation - Curly's Gift": base_id+45,
    "Plantation - Broken Sprinker": base_id+46,
    "Plantation - Platforming Spot": base_id+47,
    "Plantation - Puppy": base_id+48,
    "Storehouse - Itoh": base_id+49,
    "Rest Area - Megane": base_id+50,
    "Jail No. 1 - Gift": base_id+51,
    "Hideout - Momorin": base_id+52,
    "Egg Corridor? - Dragon Chest": base_id+53,
    "Egg Observation Room? - Sisters Boss": base_id+54,
    "Little House - Mr. Little": base_id+55,
    "Clock Room - Chest": base_id+56,
    "Sand Zone - Upper Spot": base_id+57,
    "Sand Zone - Pawprint Spot": base_id+58,
    "Sand Zone - Pawprint Chest": base_id+59,
    "Sand Zone - Lower Spot": base_id+60,
    "Sand Zone - Outside Warehouse": base_id+61,
    "Sand Zone Residence - Curly Boss": base_id+62,
    "Small Room - Beside Bed": base_id+63,
    "Small Room - Curly's Closet": base_id+64,
    "Jenka's House - Jenka": base_id+65,
    "Deserted House - Attic": base_id+66,
    "Sand Zone Storehouse - King": base_id+67,
}

ALL_EVENTS = {
    "Balrog 1": None,
    "Igor": None,
    "Balrog 2": None,
    "Balfrog": None,
    "Curly": None,
    "Omega": None,
    "Toroko+": None,
    "Puu Black": None,
    "Monster X": None,
    "Balrog 3": None,
    "Core": None,
    "Ironhead": None,
    "Sisters": None,
    "Ma Pignon": None,
    "Red Demon": None,
    "Misery": None,
    "Doctor": None,
    "Undead Core": None,
    "Heavy Press": None,

    "Toroko Kidnapped": None,
    "Lowered Egg Corridor Barrier": None,
    "Saved Sue": None,
    "Return Santa's Key": None,
    "Summon Jellies": None,
    "Activated Fans": None,
    "Saved Kazuma": None,  # Two
    "Returned Puppies": None,
    "Labyrinth I Access": None,  # Two, perhaps add MazeI door
    "Apply Cure-All": None,
    "Egg Corridor? Access": None,  # Two
    "Drained Curly": None,
    "Droll Attack": None,
    "Built Rocket": None,
    "Throne Access": None,

    # "Bad Ending" : None,
    # "Normal Ending" : None,
    # "Best Ending" : None,
    "Victory": None
}
