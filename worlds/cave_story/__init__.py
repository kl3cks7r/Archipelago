import settings
from typing import Dict, Any, Optional

from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Options import cave_story_options
from .Items import CaveStoryItem, ALL_ITEMS
from .Locations import CaveStoryLocation, LOCATIONS, EVENTS
from .Regions import REGIONS, REGION_CONNECTIONS, CaveStoryRegion

base_id = 0xD00_000

class CaveStoryWeb(WebWorld):
    theme = "stone"

    #bug_report_page

    tut_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Cave Story randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["kl3cks7r"],
    )

    tutorials = [tut_en]


class MyGameWorld(World):
    """
    You wake up in a dark cave with no memory of who you are, where you came from
    or why you're in such a place. Uncovering Mimiga Village you discover that the
    once-carefree Mimigas are in danger at the hands of a maniacal scientist. Run,
    jump, shoot, fly and explore your way through a massive action-adventure
    reminiscent of classic 8- and 16-bit games. Take control and learn the origins
    of this world's power, stop the delusional villain and save the Mimiga!
    """

    option_definitions = cave_story_options
    game = "Cave Story"
    topology_present = True
    item_name_to_id = {name: item_id for (name, _, item_id) in ALL_ITEMS.values}
    location_name_to_id = {name: id for
                           id, name in enumerate([
                               *LOCATIONS,
                               *EVENTS
                               ], base_id)}
    data_version = 0
    required_client_version = (0, 4, 1)
    required_server_version = (0, 4, 1)
    web = CaveStoryWeb()


    def generate_early(self) -> None:
        # read player settings to world instance
        self.dificulty = self.multiworld.dificulty[self.player].value

    def create_regions(self) -> None:
        for region in [CaveStoryRegion(reg_name, self) for reg_name in REGIONS]:
            if region.name in REGION_CONNECTIONS:
                region.add_exits(REGION_CONNECTIONS[region.name])

    def create_items(self) -> None:
        # Exclude preselected items if it becomes a feature. Must be replaced with junk items
        for item_data in ALL_ITEMS.values:
            self.multiworld.itempool.append(CaveStoryItem(**item_data, self.player))
    
    def set_rules(self) -> None:
        pass

    def generate_basic(self) -> None:
        pass

    # Unorder methods:

    def create_item(self, item: str):
        return CaveStoryItem(**ALL_ITEMS[str], self.player)
