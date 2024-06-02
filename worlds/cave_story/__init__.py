from typing import Any, Mapping
from BaseClasses import Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Options import CaveStoryOptions
from .Items import CaveStoryItem, ALL_ITEMS, FILLER_ITEMS
from .Locations import CaveStoryLocation, ALL_LOCATIONS
from .RegionsRules import REGIONS

base_id = 0xD00_000

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="CaveStoryClient")

components.append(Component("Cave Story Client", "CaveStoryClient", func=launch_client, component_type=Type.CLIENT))



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

    game = "Cave Story"
    options_dataclass = CaveStoryOptions
    options: CaveStoryOptions
    topology_present = True
    item_name_to_id = {
        name : data.item_id for name, data in ALL_ITEMS.items()}
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
        for region_data in REGIONS:
            region = Region(region_data.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
        for region_data in REGIONS:
            region = self.multiworld.get_region(region_data.name, self.player)
            for exit_data in region_data.exits:
                exit_ = region.create_exit(f"{region.name} -> {exit_data.name}")
                exit_.access_rule = lambda state, player=self.player, fn=exit_data.rule: fn(state,player)
                exit_.connect(self.multiworld.get_region(exit_data.name, self.player))
            for loc_data in region_data.locations:
                loc_ = CaveStoryLocation(self.player, loc_data.name, ALL_LOCATIONS[loc_data.name], region)
                loc_.access_rule = lambda state, player=self.player, fn=loc_data.rule: fn(state, player)
                region.locations.append(loc_)

    def create_items(self) -> None:
        # Exclude preselected items if it becomes a feature. Must be replaced with junk items
        for (item_name, item_data) in ALL_ITEMS.items():
            for _i in range(item_data.cnt):
                self.multiworld.itempool.append(CaveStoryItem(
                    item_name, item_data.classification, item_data.item_id, self.player))

    def set_rules(self) -> None:        
        goals = [
            "Bad Ending",
            "Normal Ending",
            "Best Ending",
        ]
        self.multiworld.completion_condition[self.player] = lambda state, player=self.player, goal=self.options.goal: state.has(
            goals[goal], player)

    def generate_basic(self) -> None:
        pass

    # Unorder methods:

    def fill_slot_data(self) -> Mapping[str, Any]:
        return {'goal':int(self.options.goal)}

    def create_item(self, item: str):
        if item in FILLER_ITEMS.keys():
            item_data = FILLER_ITEMS[item]
        else:
            item_data = ALL_ITEMS[item]
        return CaveStoryItem(item, item_data.classification, item_data.item_id, self.player)
    
    def get_filler_item_name(self) -> str:
        return FILLER_ITEMS.keys()[0]
