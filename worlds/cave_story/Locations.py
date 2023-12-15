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
    "Core - Robot's Arm" : base_id+0,
    "Core - Drowned Curly" : base_id+1,
    "First Cave - West Ledge" : base_id+2,
    "Graveyard - Arthur's Grave" : base_id+3,
    "Graveyard - Mr. Little" : base_id+4,
    "Plantation - Kanpachi's Bucket" : base_id+5,
    "Plantation - Curly" : base_id+6,
    "Plantation - Broken Sprinker" : base_id+7,
    "Plantation - Platforming Spot" : base_id+8,
    "Plantation - Puppy" : base_id+9,
    "Chaco's House - Chaco's Bed" : base_id+10,
    "Clock Room - Chest" : base_id+11,
    "Assembly Hall - Fireplace" : base_id+12,
    "Sand Zone Residence - Curly Boss" : base_id+13,
    "Small Room - Beside Bed" : base_id+14,
    "Small Room - Curly's Closet" : base_id+15,
    "Deserted House - Attic" : base_id+16,
    "Egg No. 06 - Chest" : base_id+17,
    "Egg Observation Room - Chest" : base_id+18,
    "Egg Observation Room? - Sisters Boss" : base_id+19,
    "Egg Corridor - Basil Spot" : base_id+20,
    "Egg Corridor - Outside Cthulhu's Abode" : base_id+21,
    "Egg Corridor? - Dragon Chest" : base_id+22,
    "Gum - Chest" : base_id+23,
    "Sand Zone Storehouse - King" : base_id+24,
    "Sacred Grounds - B1 - Ledge" : base_id+25,
    "Sacred Grounds - B3 - Hidden Chest" : base_id+26,
    "Storehouse - Itoh" : base_id+27,
    "Jail No. 1 - Sue's Gift" : base_id+28,
    "Jenka's House - Jenka" : base_id+29,
    "Little House - Mr. Little" : base_id+30,
    "Rest Area - Megane" : base_id+31,
    "Power Room - MALCO" : base_id+32,
    "Storage? - Chest" : base_id+33,
    "Storage? - Ma Pignon Boss" : base_id+34,
    "Labyrinth Shop - Chaba Chest (Machine Gun)" : base_id+35,
    "Labyrinth Shop - Chaba Chest (Fireball)" : base_id+36,
    "Labyrinth Shop - Chaba Chest (Spur)" : base_id+37,
    "Labyrinth B - Booster Chest" : base_id+38,
    "Clinic Ruins - Puu Black Boss" : base_id+39,
    "Labyrinth I - Critter Spot" : base_id+40,
    "Camp - Dr. Gero" : base_id+41,
    "Camp - Chest" : base_id+42,
    "Boulder Chamber - Chest" : base_id+43,
    "Mimiga Village - Chest" : base_id+44,
    "Hideout - Momorin" : base_id+45,
    "Arthur's House - Professor Booster" : base_id+46,
    "Yamashita Farm - Pool" : base_id+47,
    "Hermit Gunsmith - Chest" : base_id+48,
    "Hermit Gunsmith - Tetsuzou" : base_id+49,
    "Reservoir - Fishing Spot" : base_id+50,
    "Last Cave (Hidden) - Red Demon Boss" : base_id+51,
    "Sand Zone - Polish Spot" : base_id+52,
    "Sand Zone - Pawprint Spot" : base_id+53,
    "Sand Zone - Pawprint Chest" : base_id+54,
    "Sand Zone - Running Puppy" : base_id+55,
    "Sand Zone - Outside Warehouse" : base_id+56,
    "Santa's House - Santa" : base_id+57,
    "Santa's House - Fireplace" : base_id+58,
    "Main Artery - Ironhead Boss" : base_id+59,
    "Grasstown - West Floor" : base_id+60,
    "Grasstown - West Ceiling" : base_id+61,
    "Grasstown - East Chest" : base_id+62,
    "Grasstown - Kazuma Crack" : base_id+63,
    "Grasstown - Kazuma Chest" : base_id+64,
    "Grasstown - Kulala" : base_id+65,
    "Grasstown Hut - Chest" : base_id+66,
    "Execution Chamber - Above" : base_id+67,
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
