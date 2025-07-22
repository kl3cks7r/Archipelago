from typing import Any, Mapping, ClassVar
from BaseClasses import CollectionState, Region, Tutorial, Item
from settings import Group, FolderPath
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, icon_paths, launch_subprocess
from .Options import CaveStoryOptions
from .Items import CaveStoryItem, ALL_ITEMS, FILLER_ITEMS
from .Locations import CaveStoryLocation, ALL_LOCATIONS
from .RegionsRules import REGIONS, RegionData, RuleData, trivial

base_id = 0xD00_000

def launch_client():
    from .CaveStoryClient import launch
    launch_subprocess(launch, name="CaveStoryClient")

components.append(Component(
    display_name="Cave Story Client",
    script_name="CaveStoryClient",
    func=launch_client,
    component_type=Type.CLIENT,
    description="Launches Cave Story and connects to a multiworld.",
    icon="Cave Story",
))

icon_paths["Cave Story"] = f"ap:{__name__}/assets/icon.png"

class CaveStorySettings(Group):
    class GameDir(FolderPath):
        description = "cave-story-randomizer Root Directory"

    game_dir: GameDir = GameDir("cave-story-randomizer")
    ignore_process: bool = False

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
    settings_key = "cave_story_settings"
    settings: ClassVar[CaveStorySettings]
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
        if self.options.starting_location == 0:
            starting_region = RegionData("Menu",[RuleData("Start Point - Door to First Cave", trivial)],[])
        elif self.options.starting_location == 1:
            starting_region = RegionData("Menu",[RuleData("Arthur's House - Main Teleporter", trivial)],[])
        else:
            starting_region = RegionData("Menu",[RuleData("Camp - Door to Labyrinth W (Lower)", trivial)],[])
        for region_data in [starting_region,*REGIONS]:
            region = Region(region_data.name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
        for region_data in [starting_region,*REGIONS]:
            region = self.multiworld.get_region(region_data.name, self.player)
            for exit_data in region_data.exits:
                exit_ = region.create_exit(f"{region.name} -> {exit_data.name}")
                exit_.access_rule = lambda state, player=self.player, fn=exit_data.rule: fn(state,player)
                exit_.connect(self.multiworld.get_region(exit_data.name, self.player))
            for loc_data in region_data.locations:
                loc_ = CaveStoryLocation(self.player, loc_data.name, ALL_LOCATIONS[loc_data.name], region)
                loc_.access_rule = lambda state, player=self.player, fn=loc_data.rule: fn(state, player)
                region.locations.append(loc_)
        if self.options.exclude_hell:
            self.options.exclude_locations.value.update([
                "Sacred Grounds - B1 - Ledge",
                "Sacred Grounds - B3 - Hidden Chest"
            ])

    def create_items(self) -> None:
        world_itempool: list[Item] = []
        # Exclude preselected items if it becomes a feature. Must be replaced with junk items
        # (item_name, item_data) = ("Refill Station", FILLER_ITEMS["Refill Station"])
        # for _i in range(3):
        #     world_itempool.append(CaveStoryItem(
        #         item_name, item_data.classification, item_data.item_id, self.player))
        for (item_name, item_data) in ALL_ITEMS.items():
            for _i in range(item_data.cnt):
                world_itempool.append(CaveStoryItem(
                    item_name, item_data.classification, item_data.item_id, self.player))
            # Custom handling for making only ONE missile expansion progression so we don't always start with missiles
            # if item_name == "Missile Expansion":
            #     self.multiworld.itempool[-item_data.cnt].classification = ItemClassification.progression
        # If early weapon is on place one of the weapons
        if self.options.early_weapon:
            block_breaking_weapons = [
                "Blade",
                "Machine Gun",
                "Nemesis",
                "Progressive Polar Star",
                "Bubbler"
                "Missile Expansion",
            ]
            initial_state = CollectionState(self.multiworld)
            sphere_1_locs = self.multiworld.get_reachable_locations(initial_state, self.player)
            start_loc = self.random.choice(sphere_1_locs)
            start_weapon = self.random.choice([item for item in world_itempool if item.name in block_breaking_weapons])
            world_itempool.remove(start_weapon)
            start_loc.place_locked_item(start_weapon)
        self.multiworld.itempool.extend(world_itempool)

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
        slot_data = {
            'goal' : int(self.options.goal),
            'start': int(self.options.starting_location),
            'deathlink' : bool(self.options.deathlink),
            'no_blocks': bool(self.options.no_blocks),
        }
        return slot_data

    def create_item(self, item: str):
        if item in FILLER_ITEMS.keys():
            item_data = FILLER_ITEMS[item]
        else:
            item_data = ALL_ITEMS[item]
        return CaveStoryItem(item, item_data.classification, item_data.item_id, self.player)
    
    def get_filler_item_name(self) -> str:
        return FILLER_ITEMS.keys()[0]
