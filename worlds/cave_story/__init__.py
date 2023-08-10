from functools import partial

from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from .Options import cave_story_options
from .Items import CaveStoryItem, ALL_ITEMS
from .Locations import CaveStoryLocation, ALL_LOCATIONS
from .RegionsRules import REGIONS

base_id = 0xD00_000


class CaveStoryWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Tutorial",
            "A guide to setting up the Cave Story randomizer on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["kl3cks7r"],
        )
    ]
    theme = "stone"
    bug_report_page = "https://github.com/kl3cks7r/Cave-Story-Archipelago/issues"


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
    item_name_to_id = {
        item_data.name: item_data.item_id for item_data in ALL_ITEMS.values()}
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
        menu = Region("Menu", self.player, self.multiworld)
        menu.connect("Start Point")
        self.multiworld.regions.append(menu)
        for region_data in REGIONS:
            region = Region(region_data.name, self.player, self.multiworld)
            for exits in region_data.exits:
                region.add_exits(exits.keys(),exits)
            for locations in region_data.locations:
                # for loc in region.locations:
                #     if loc.name in LOCATION_RULES:
                #         loc.access_rule = partial(LOCATION_RULES[loc.name], player=self.player)
                region.add_locations({locations[0]:ALL_LOCATIONS[locations[0]]},CaveStoryLocation)
            self.multiworld.regions.append(region)

    def create_items(self) -> None:
        # Exclude preselected items if it becomes a feature. Must be replaced with junk items
        for (item_name, item_data) in ALL_ITEMS.items():
            for _i in range(item_data.cnt):
                self.multiworld.itempool.append(CaveStoryItem(
                    item_name, item_data.classification, item_data.item_id, self.player))

    def set_rules(self) -> None:        
        self.multiworld.completion_condition[self.player] = lambda state: state.has(
            "Victory", self.player)

    def generate_basic(self) -> None:
        pass

    # Unorder methods:

    def create_item(self, item: str):
        return CaveStoryItem(*vars(ALL_ITEMS[item]).values(), self.player)
