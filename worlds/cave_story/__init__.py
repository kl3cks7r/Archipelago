from functools import partial

from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld, World
from .Options import cave_story_options
from .Items import CaveStoryItem, ALL_ITEMS, DUPES
from .Locations import CaveStoryLocation, ALL_LOCATIONS
from .Regions import CaveStoryRegion, REGION_LOCATIONS, REGION_CONNECTIONS
from .Rules import REGION_RULES, LOCATION_RULES

base_id = 0xD00_000

class CaveStoryWeb(WebWorld):
    theme = "stone"

    bug_report_page = "https://github.com/kl3cks7r/Cave-Story-Archipelago/issues"

    tut_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Cave Story randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["kl3cks7r"],
    )

    tutorials = [tut_en]


class CaveStoryWorld(World):
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
    item_name_to_id = {item_data.name: item_data.item_id for item_data in ALL_ITEMS.values()}
    location_name_to_id = ALL_LOCATIONS
    data_version = 0
    # required_client_version = (0, 4, 1)
    # required_server_version = (0, 4, 1)
    web = CaveStoryWeb()


    def generate_early(self) -> None:
        # read player settings to world instance
        pass
        # self.dificulty = self.multiworld.dificulty[self.player].value

    def create_regions(self) -> None:
        for region in [CaveStoryRegion(reg_name, self) for reg_name in REGION_LOCATIONS]:
            if region.name in REGION_LOCATIONS:
                region.add_locations({k: ALL_LOCATIONS[k] for k in REGION_LOCATIONS[region.name] if ALL_LOCATIONS[k] in ALL_LOCATIONS.values()}, CaveStoryLocation)
            if region.name in REGION_CONNECTIONS:
                region.add_exits(REGION_CONNECTIONS[region.name])

    def create_items(self) -> None:
        # Exclude preselected items if it becomes a feature. Must be replaced with junk items
        for item_data in ALL_ITEMS.values():
            self.multiworld.itempool.append(CaveStoryItem(*vars(item_data).values(), self.player))
        for item, count in DUPES.items():
            for _i in range(count):
                self.multiworld.itempool.append(CaveStoryItem(*vars(ALL_ITEMS[item]).values(), self.player))
    
    def set_rules(self) -> None:
        for region in self.multiworld.get_regions(self.player):
            if region.name in REGION_RULES:
                for entrance in region.entrances:
                    entrance.access_rule = partial(REGION_RULES[region.name], player=self.player)
            for loc in region.locations:
                if loc.name in LOCATION_RULES:
                    loc.access_rule = partial(LOCATION_RULES[loc.name], player=self.player)

    def generate_basic(self) -> None:
        pass

    # Unorder methods:

    def create_item(self, item: str):
        return CaveStoryItem(*vars(ALL_ITEMS[item]).values(), self.player)
