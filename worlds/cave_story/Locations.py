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
            if name[:-8] == "Level MG":
                self.place_locked_item(CaveStoryItem(
                    "Level MG", ItemClassification.progression, None, parent.player))
            self.place_locked_item(CaveStoryItem(
                name, ItemClassification.progression, None, parent.player))


ALL_LOCATIONS: Dict[str, Optional[int]] = {
    "Egg Corridor - Basil Spot" : base_id+0,
    "Egg Corridor - Outside Cthulhu's Abode" : base_id+1,
    "Egg No. 06 - Chest" : base_id+2,
    "Egg Observation Room - Chest" : base_id+3,
    "Grasstown - West Floor" : base_id+4,
    "Grasstown - West Ceiling" : base_id+5,
    "Grasstown - East Chest" : base_id+6,
    "Grasstown - Kazuma Crack" : base_id+7,
    "Grasstown - Kazuma Chest" : base_id+8,
    "Grasstown - Kulala" : base_id+9,
    "Santa's House - Santa" : base_id+10,
    "Santa's House - Fireplace" : base_id+11,
    "Chaco's House - Chaco's Bed" : base_id+12,
    "Power Room - MALCO" : base_id+13,
    "Grasstown Hut - Chest" : base_id+14,
    "Execution Chamber - Above" : base_id+15,
    "Gum - Chest" : base_id+16,
    "Labyrinth B - Booster Chest" : base_id+17,
    "Boulder Chamber - Chest" : base_id+18,
    "Core - Robot's Arm" : base_id+19,
    "Core - Drowned Curly" : base_id+20,
    "Main Artery - Ironhead Boss" : base_id+21,
    "Labyrinth I - Critter Spot" : base_id+22,
    "Labyrinth Shop - Chaba Chest (Machine Gun)" : base_id+23,
    "Labyrinth Shop - Chaba Chest (Fireball)" : base_id+24,
    "Labyrinth Shop - Chaba Chest (Spur)" : base_id+25,
    "Camp - Dr. Gero" : base_id+26,
    "Camp - Chest" : base_id+27,
    "Clinic Ruins - Puu Black Boss" : base_id+28,
    "Last Cave (Hidden) - Red Demon Boss" : base_id+29,
    "Sacred Grounds - B1 - Ledge" : base_id+30,
    "Sacred Grounds - B3 - Hidden Chest" : base_id+31,
    "First Cave - West Ledge" : base_id+32,
    "Hermit Gunsmith - Chest" : base_id+33,
    "Hermit Gunsmith - Tetsuzou" : base_id+34,
    "Mimiga Village - Chest" : base_id+35,
    "Yamashita Farm - Pool" : base_id+36,
    "Reservoir - Fishing Spot" : base_id+37,
    "Assembly Hall - Fireplace" : base_id+38,
    "Graveyard - Arthur's Grave" : base_id+39,
    "Graveyard - Mr. Little" : base_id+40,
    "Storage? - Chest" : base_id+41,
    "Storage? - Ma Pignon Boss" : base_id+42,
    "Arthur's House - Professor Booster" : base_id+43,
    "Plantation - Kanpachi's Bucket" : base_id+44,
    "Plantation - Curly" : base_id+45,
    "Plantation - Broken Sprinker" : base_id+46,
    "Plantation - Platforming Spot" : base_id+47,
    "Plantation - Puppy" : base_id+48,
    "Storehouse - Itoh" : base_id+49,
    "Rest Area - Megane" : base_id+50,
    "Jail No. 1 - Sue's Gift" : base_id+51,
    "Hideout - Momorin" : base_id+52,
    "Egg Corridor? - Dragon Chest" : base_id+53,
    "Egg Observation Room? - Sisters Boss" : base_id+54,
    "Little House - Mr. Little" : base_id+55,
    "Clock Room - Chest" : base_id+56,
    "Sand Zone - Polish Spot" : base_id+57,
    "Sand Zone - Pawprint Spot" : base_id+58,
    "Sand Zone - Pawprint Chest" : base_id+59,
    "Sand Zone - Running Puppy" : base_id+60,
    "Sand Zone - Outside Warehouse" : base_id+61,
    "Sand Zone Residence - Curly Boss" : base_id+62,
    "Small Room - Beside Bed" : base_id+63,
    "Small Room - Curly's Closet" : base_id+64,
    "Jenka's House - Jenka" : base_id+65,
    "Deserted House - Attic" : base_id+66,
    "Sand Zone Storehouse - King" : base_id+67,
    # Events:
    "Defeated Igor" : None,
    "Lowered Egg Corridor Barrier" : None,
    "Saved Sue" : None,
    "Returned Santa's Key" : None,
    "Entered Grasstown from Fireplace" : None,
    "Summoned Jellies" : None,
    "Activated Fans" : None,
    "Defeated Balrog 2" : None,
    "Defeated Balfrog" : None,
    "Saved Kazuma" : None,
    "Entered Labyrinth B from Above" : None,
    "Defeated Balrog 3" : None,
    "Defeated Core" : None,
    "Saved Curly" : None,
    "Defeated Ironhead" : None,
    "Opened Labyrinth I Door" : None,
    "Used Labyrinth I Teleporter" : None,
    "Defeated Monster X" : None,
    "Delivered Cure-All" : None,
    "Start in Camp" : None,
    "Defeated Puu Black" : None,
    "Defeated Red Demon" : None,
    "Lowered Barrier" : None,
    "Defeated Misery" : None,
    "Defeated Doctor" : None,
    "Defeated Undead Core" : None,
    "Normal Ending" : None,
    "Picked up Curly (Hell)" : None,
    "Picked up Curly (Core)" : None,
    "Defeated Heavy Press" : None,
    "Best Ending" : None,
    "Start in Start Point" : None,
    "Defeated Ma Pignon" : None,
    "Used Ma Pignon" : None,
    "Toroko Kidnapped" : None,
    "Defeated Balrog 1" : None,
    "Start in Arthur's House" : None,
    "Entered Passage? from above" : None,
    "Droll Attack" : None,
    "Built Rocket" : None,
    "Used Egg Corridor? Teleporter" : None,
    "Defeated Sisters" : None,
    "Bad Ending" : None,
    "Entered Outer Wall from Storehouse" : None,
    "Entered Outer Wall from Clock Room" : None,
    "Defeated Omega" : None,
    "Defeated Curly" : None,
    "Returned Puppies" : None,
    "Defeated Toroko+" : None,
    "Egg Corridor - Level MG" : None,
    "Grasstown (West) - Level MG" : None,
    "Grasstown (East) - Level MG" : None,
    "Labyrinth M - Level MG" : None,
    "Labyrinth W - Level MG" : None,
    "Shack - Level MG" : None,
    "Plantation - Level MG" : None,
    "Egg Corridor? (West) - Level MG" : None,
    "Egg Corridor? (Centre) - Level MG" : None,
    "Egg Corridor? (East) - Level MG" : None,
    "Outer Wall - Level MG" : None,
    "Sand Zone (Lower) - Level MG" : None,
    "Sand Zone (Upper) - Level MG" : None
}
