from typing import List, NamedTuple, Tuple, Callable, Optional

from BaseClasses import CollectionState


class RuleData(NamedTuple):
    name: str
    rule: Optional[Callable[[CollectionState, int], bool]]

class RegionData:
    name: str
    exits: List[RuleData]
    locations: List[RuleData]

    def __init__(
        self,
        name: str,
        exits: List[RuleData],
        locations: List[RuleData]
    ):
        self.name = name
        self.exits = exits
        self.locations = locations


def has_flight(state: CollectionState, player: int):
    return state.has("Progressive Booster", player) or state.has_all({"Machine Gun", "Level Up Machine Gun"})


def can_break_blocks(state: CollectionState, player: int):
    return state.has_any({"Blade", "Machine Gun", "Nemesis", "Progressive Polar Star"}, player)


def can_kill_bosses(state: CollectionState, player: int):
    return state.has_any({"Blade", "Bubbler", "Fireball", "Machine Gun", "Nemesis", "Progressive Polar Star", "Snake"}, player)


def has_weapon(state: CollectionState, player: int):
    return state.has_any({"Blade", "Bubbler", "Fireball", "Machine Gun", "Nemesis", "Progressive Missile Launcher", "Progressive Polar Star", "Snake"}, player)


def remove_points_of_no_return(state: CollectionState, player: int):
    return True


def reset_iframes(state: CollectionState, player: int):
    return True  # state.has("Map System", player)


def traverse_labyrinth_w(state: CollectionState, player: int):
    return has_weapon(state, player)

# RegionData("Menu",[RuleData("Start Point - Save Point", lambda state, player: True),], []),

REGIONS: List[RegionData] = [
    RegionData("Menu",[RuleData("Start Point - Save Point", lambda state, player: True),], []),

    RegionData(
        "Egg Corridor - Door to Cthulhu's Abode (Lower)",
        [
            # Regions
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)",
             lambda state, player: True),
            RuleData("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Cthulhu's Abode (Upper)",
        [
            # Regions
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Upper)",
             lambda state, player: True),
            RuleData("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Egg Corridor - Cthulhu's Abode", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Egg Corridor",
             lambda state, player: True),
            RuleData("Egg Corridor - Outside Cthulhu's Abode",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            RuleData("Egg Corridor - Basil Spot", lambda state, player: True),
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor - Outside Cthulhu's Abode",
        [
            # Regions
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Lower)",
             lambda state, player: True),
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Upper)",
             lambda state, player: has_flight(state, player)),
            RuleData("Egg Corridor - Teleporter to Arthur's House",
             lambda state, player: has_weapon(state, player)),
            RuleData("Egg Corridor - Outside Egg Observation Room",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Outside Egg Observation Room",
        [
            # Regions
            RuleData("Egg Corridor - Outside Cthulhu's Abode",
             lambda state, player: has_weapon(state, player)),
            RuleData("Egg Corridor - H/V Trigger to Egg No. 06", lambda state, player: True),
            RuleData("Egg Corridor - Door to Egg Observation Room",
             lambda state, player: True),
            RuleData("Egg Corridor - H/V Trigger to Egg No. 01", lambda state, player: True),
            RuleData("Egg Corridor - Outside Egg No. 00", lambda state,
             player: state.has("Lowered Egg Corridor Barrier", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - H/V Trigger to Egg No. 06",
        [
            # Regions
            RuleData("Egg No. 06 - Door to Egg Corridor", lambda state, player: True),
            RuleData("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Egg Observation Room",
        [
            # Regions
            RuleData("Egg Observation Room - Door to Egg Corridor",
             lambda state, player: True),
            RuleData("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - H/V Trigger to Egg No. 01",
        [
            # Regions
            RuleData("Egg No. 01 - Door to Egg Corridor", lambda state, player: True),
            RuleData("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Outside Egg No. 00",
        [
            # Regions
            RuleData("Egg Corridor - Outside Egg Observation Room", lambda state,
             player: state.has("Lowered Egg Corridor Barrier", player, 1)),
            RuleData("Egg Corridor - Door to Egg No. 00", lambda state,
             player: state.has("Defeated Igor", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Igor", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Egg No. 00",
        [
            # Regions
            RuleData("Egg No. 00 - Door to Egg Corridor", lambda state, player: True),
            RuleData("Egg Corridor - Outside Egg No. 00", lambda state,
             player: state.has("Defeated Igor", player, 1)),
            RuleData("Egg Corridor - Door to Side Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Igor", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Side Room",
        [
            # Regions
            RuleData("Side Room - Door to Egg Corridor", lambda state, player: True),
            RuleData("Egg Corridor - Door to Egg No. 00", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Cthulhu's Abode - Door to Egg Corridor (Lower)",
        [
            # Regions
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Lower)",
             lambda state, player: True),
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Upper)",
             lambda state, player: can_break_blocks(state, player)),
            RuleData("Cthulhu's Abode - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Cthulhu's Abode - Door to Egg Corridor (Upper)",
        [
            # Regions
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Upper)",
             lambda state, player: True),
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)",
             lambda state, player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Cthulhu's Abode - Save Point",
        [
            # Regions
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg No. 06 - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - H/V Trigger to Egg No. 06", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Egg No. 06 - Egg Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Door to Egg Observation Room", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Egg Observation Room - Egg Observation Room Chest",
             lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg No. 01 - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - H/V Trigger to Egg No. 01", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Lowered Egg Corridor Barrier", lambda state,
             player: state.has("ID Card", player, 1))
        ]
    ),
    RegionData(
        "Egg No. 00 - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Door to Egg No. 00", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Saved Sue", lambda state, player: True)
        ]
    ),
    RegionData(
        "Side Room - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Door to Side Room", lambda state, player: True),
            RuleData("Side Room - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room - Save Point",
        [
            # Regions
            RuleData("Side Room - Door to Egg Corridor", lambda state, player: True),
            RuleData("Side Room - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room - Refill",
        [
            # Regions
            RuleData("Side Room - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Santa's House",
        [
            # Regions
            RuleData("Santa's House - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - West Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Chaco's House",
        [
            # Regions
            RuleData("Chaco's House - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - West Side", lambda state,
             player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Entrance from Chaco's House",
        [
            # Regions
            RuleData("Chaco's House - Exit to Grasstown", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Grasstown from Chaco Fireplace", lambda state, player: True)
        ]
    ),
    RegionData(
        "Grasstown - Door to Power Room",
        [
            # Regions
            RuleData("Power Room - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Save Point",
        [
            # Regions
            RuleData("Save Point - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Grasstown Hut",
        [
            # Regions
            RuleData("Grasstown Hut - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Shelter",
        [
            # Regions
            RuleData("Shelter - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Execution Chamber",
        [
            # Regions
            RuleData("Execution Chamber - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Door to Gum",
        [
            # Regions
            RuleData("Gum - Door to Grasstown", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - West Side",
        [
            # Regions
            RuleData("Grasstown - Door to Santa's House", lambda state,
             player: state.has("Returned Santa's Key", player, 1)),
            RuleData("Grasstown - Door to Chaco's House",
             lambda state, player: has_weapon(state, player)),
            RuleData("Grasstown - Area Centre", lambda state, player: has_flight(state,
             player) or state.has("Activated Fans", player, 1)),
            RuleData("Grasstown - Teleporter to Arthur's House", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Grasstown - West Grasstown Floor",
             lambda state, player: has_weapon(state, player)),
            RuleData("Grasstown - West Grasstown Ceiling",
             lambda state, player: has_weapon(state, player)),
            RuleData("Grasstown - Kulala", lambda state, player: has_weapon(state,
             player) and state.has("Summoned Jellies", player, 1)),
            # Events
            RuleData("Return Santa's Key", lambda state,
             player: state.has("Santa's Key", player, 1)),
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Grasstown - East Side",
        [
            # Regions
            RuleData("Grasstown - Door to Power Room", lambda state,
             player: state.has("Rusty Key", player, 1)),
            RuleData("Grasstown - Door to Save Point", lambda state, player: True),
            RuleData("Grasstown - Door to Grasstown Hut", lambda state,
             player: has_flight(state, player) or state.has("Activated Fans", player, 1)),
            RuleData("Grasstown - Door to Shelter", lambda state,
             player: state.has("Saved Kazuma", player, 1)),
            RuleData("Grasstown - Door to Execution Chamber", lambda state, player: True),
            RuleData("Grasstown - Door to Gum", lambda state, player: state.has("Gum Key", player, 1)
             and (has_flight(state, player) or state.has("Activated Fans", player, 1))),
            RuleData("Grasstown - Area Centre", lambda state, player: (state.has("Activated Fans", player, 1) or has_flight(state, player)
             or (remove_points_of_no_return(state, player) and state.has("Entered Grasstown from Fireplace", player, 1))))
        ],
        [
            # Locations
            RuleData("Grasstown - Grasstown East Chest", lambda state, player: True),
            RuleData("Grasstown - Kazuma Crack", lambda state, player: True),
            RuleData("Grasstown - Kazuma Chest", lambda state,
             player: state.has("Rusty Key", player, 1)),
            # Events
            RuleData("Saved Kazuma", lambda state, player: state.has("Explosive", player, 1)),
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Grasstown - Area Centre",
        [
            # Regions
            RuleData("Grasstown - West Side", lambda state, player: True),
            RuleData("Grasstown - East Side", lambda state,
             player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Grasstown", lambda state, player: True),
            RuleData("Grasstown - West Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Santa's House - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Santa's House", lambda state, player: True),
            RuleData("Santa's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Santa's House - Santa", lambda state,
             player: state.has("Returned Santa's Key", player, 1)),
            RuleData("Santa's House - Santa's Fireplace", lambda state,
             player: state.has("Jellyfish Juice", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Santa's House - Save Point",
        [
            # Regions
            RuleData("Santa's House - Door to Grasstown", lambda state, player: True),
            RuleData("Santa's House - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Santa's House - Refill",
        [
            # Regions
            RuleData("Santa's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Chaco's House - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Chaco's House", lambda state, player: True),
            RuleData("Chaco's House - Exit to Grasstown", lambda state,
             player: state.has("Jellyfish Juice", player, 1)),
            RuleData("Chaco's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Chaco's House - Chaco's Bed, where you two Had A Nap",
             lambda state, player: state.has("Returned Santa's Key", player, 1)),
            # Events
            RuleData("Summon Jellies", lambda state, player: state.has(
                "Returned Santa's Key", player, 1))
        ]
    ),
    RegionData(
        "Chaco's House - Exit to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Entrance from Chaco's House", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Chaco's House - Save Point",
        [
            # Regions
            RuleData("Chaco's House - Door to Grasstown", lambda state, player: True),
            RuleData("Chaco's House - Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Chaco's House - Bed",
        [
            # Regions
            RuleData("Chaco's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Power Room - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Power Room", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Power Room - MALCO", lambda state, player: state.has("Activated Fans", player, 1) and state.has("Charcoal", player, 1)
             and state.has("Jellyfish Juice", player, 1) and state.has("Gum Base", player, 1) and state.has("Defeated Balrog 2", player, 1)),
            # Events
            RuleData("Activated Fans", lambda state, player: True)
        ]
    ),
    RegionData(
        "Save Point - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Save Point", lambda state, player: True),
            RuleData("Save Point - Save Point", lambda state, player: True),
            RuleData("Save Point - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Save Point - Save Point",
        [
            # Regions
            RuleData("Save Point - Door to Grasstown", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Save Point - Refill",
        [
            # Regions
            RuleData("Save Point - Door to Grasstown", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown Hut - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Grasstown Hut", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Grasstown Hut - Grasstown Hut", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Execution Chamber - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Execution Chamber", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Execution Chamber - Execution Chamber", lambda state,
             player: can_break_blocks(state, player)),
            # Events
        ]
    ),
    RegionData(
        "Gum - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Gum", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Gum - Gum Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Shelter - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Shelter", lambda state, player: True),
            RuleData("Shelter - Save Point", lambda state,
             player: state.has("Saved Kazuma", player, 1)),
            RuleData("Shelter - Teleporter to Jail No. 2", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Shelter - Save Point",
        [
            # Regions
            RuleData("Shelter - Door to Grasstown", lambda state, player: True),
            RuleData("Shelter - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Shelter - Teleporter to Jail No. 2",
        [
            # Regions
            RuleData("Jail No. 2 - Teleporter to Shelter", lambda state, player: True),
            RuleData("Shelter - Door to Grasstown", lambda state,
             player: state.has("Saved Kazuma", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Saved Kazuma", lambda state, player: state.has("Explosive", player, 1))
        ]
    ),
    RegionData(
        "Shelter - Refill",
        [
            # Regions
            RuleData("Shelter - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Door to Boulder Chamber",
        [
            # Regions
            RuleData("Boulder Chamber - Door to Labyrinth B", lambda state, player: True),
            RuleData("Labyrinth B - Door to Labyrinth W", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Door to Labyrinth W",
        [
            # Regions
            RuleData("Labyrinth W - Door to Labyrinth B", lambda state, player: True),
            RuleData("Labyrinth B - Door to Boulder Chamber", lambda state, player: True),
            RuleData("Labyrinth B - Teleporter to Arthur's House", lambda state, player: True),
            RuleData("Labyrinth B - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Enter Labyrinth B from Above", lambda state, player: True)
        ]
    ),
    RegionData(
        "Labyrinth B - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Labyrinth B", lambda state, player: True),
            RuleData("Labyrinth B - Door to Labyrinth W", lambda state, player: has_flight(state, player)
             or (state.has("Entered Labyrinth B from Above", player, 1) and remove_points_of_no_return(state, player)))
        ],
        [
            # Locations
            RuleData("Labyrinth B - Booster Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Save Point",
        [
            # Regions
            RuleData("Labyrinth B - Door to Labyrinth W", lambda state, player: True),
            RuleData("Labyrinth B - Refill", lambda state,
             player: has_flight(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Refill",
        [
            # Regions
            RuleData("Labyrinth B - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Boulder Chamber - Door to Labyrinth B",
        [
            # Regions
            RuleData("Labyrinth B - Door to Boulder Chamber", lambda state, player: True),
            RuleData("Boulder Chamber - Door to Labyrinth M", lambda state,
             player: state.has("Defeated Balrog 3", player, 1)),
            RuleData("Boulder Chamber - Save Point", lambda state,
             player: state.has("Defeated Balrog 3", player, 1))
        ],
        [
            # Locations
            RuleData("Boulder Chamber - Boulder Chest", lambda state,
             player: state.has("Defeated Balrog 3", player, 1)),
            # Events
            RuleData("Balrog 3", lambda state, player: state.has(
                "Delivered Cure-All", player, 1) and can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Boulder Chamber - Door to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Door to Boulder Chamber", lambda state, player: True),
            RuleData("Boulder Chamber - Door to Labyrinth B", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Boulder Chamber - Save Point",
        [
            # Regions
            RuleData("Boulder Chamber - Door to Labyrinth B", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth M - Door to Boulder Chamber",
        [
            # Regions
            RuleData("Boulder Chamber - Door to Labyrinth M", lambda state, player: True),
            RuleData("Labyrinth M - Door to Dark Place",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth M - Door to Dark Place",
        [
            # Regions
            RuleData("Dark Place - Door to Labyrinth M", lambda state, player: True),
            RuleData("Labyrinth M - Door to Boulder Chamber", lambda state,
             player: state.has("Defeated Balrog 3", player, 1) and (has_weapon(state, player))),
            RuleData("Labyrinth M - Teleporter to Labyrinth Shop",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth M - Teleporter to Labyrinth Shop",
        [
            # Regions
            RuleData("Labyrinth Shop - Teleporter to Labyrinth M", lambda state, player: True),
            RuleData("Labyrinth M - Door to Dark Place",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Dark Place - Door to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Door to Dark Place", lambda state, player: True),
            RuleData("Dark Place - Door to Core", lambda state,
             player: state.has("Defeated Balrog 3", player, 1)),
            RuleData("Dark Place - Exit to Waterway", lambda state,
             player: state.has("Curly's Air Tank", player, 1)),
            RuleData("Dark Place - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Dark Place - Door to Core",
        [
            # Regions
            RuleData("Core - Door to Dark Place", lambda state, player: True),
            RuleData("Dark Place - Door to Labyrinth M", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Dark Place - Exit to Waterway",
        [
            # Regions
            RuleData("Waterway - Entrance from Dark Place", lambda state, player: True),
            RuleData("Dark Place - Door to Labyrinth M", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Dark Place - Entrance from Reservoir",
        [
            # Regions
            RuleData("Reservoir - Debug Cat to Dark Place", lambda state, player: True),
            RuleData("Dark Place - Door to Labyrinth M", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Dark Place - Save Point",
        [
            # Regions
            RuleData("Dark Place - Door to Labyrinth M", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Core - Door to Dark Place",
        [
            # Regions
            RuleData("Dark Place - Door to Core", lambda state, player: True),
            RuleData("Core - Inner Room", lambda state, player: state.has("Defeated Balrog 3",
             player, 1) and can_kill_bosses(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Core - Inner Room",
        [
            # Regions
            RuleData("Core - Door to Dark Place", lambda state,
             player: state.has("Defeated Core", player, 1))
        ],
        [
            # Locations
            RuleData("Core - Robot's Arm", lambda state, player: True),
            # Events
            RuleData("Core", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Waterway - Entrance from Dark Place",
        [
            # Regions
            RuleData("Dark Place - Exit to Waterway", lambda state, player: True),
            RuleData("Waterway - Door to Waterway Cabin", lambda state,
             player: state.has("Curly's Air Tank", player, 1) and (has_weapon(state, player)))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Waterway - Exit to Main Artery",
        [
            # Regions
            RuleData("Main Artery - Entrance from Waterway", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Waterway - Door to Waterway Cabin",
        [
            # Regions
            RuleData("Waterway Cabin - Door to Waterway", lambda state, player: True),
            RuleData("Waterway - Exit to Main Artery", lambda state,
             player: state.has("Curly's Air Tank", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Waterway Cabin - Door to Waterway",
        [
            # Regions
            RuleData("Waterway - Door to Waterway Cabin", lambda state, player: True),
            RuleData("Waterway Cabin - Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Drained Curly", lambda state, player: state.has(
                "Picked up Curly (Core)", player, 1))
        ]
    ),
    RegionData(
        "Waterway Cabin - Save Point",
        [
            # Regions
            RuleData("Waterway Cabin - Door to Waterway", lambda state, player: True),
            RuleData("Waterway Cabin - Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Waterway Cabin - Bed",
        [
            # Regions
            RuleData("Waterway Cabin - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Main Artery - Entrance from Waterway",
        [
            # Regions
            RuleData("Waterway - Exit to Main Artery", lambda state, player: True),
            RuleData("Main Artery - Exit to Reservoir", lambda state,
             player: state.has("Defeated Ironhead", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Ironhead", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Main Artery - Exit to Reservoir",
        [
            # Regions
            RuleData("Reservoir - Entrance from Main Artery", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth I - Door to Labyrinth H",
        [
            # Regions
            RuleData("Labyrinth H - Door to Labyrinth I", lambda state, player: True),
            RuleData("Labyrinth I - Room Bottom", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth I - Room Bottom",
        [
            # Regions
            RuleData("Labyrinth I - Door to Labyrinth H", lambda state,
             player: state.has("Opened Labyrinth I Door", player, 1)),
            RuleData("Labyrinth I - Save Point", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            RuleData("Labyrinth I - Labyrinth Life Capsule",
             lambda state, player: has_weapon(state, player)),
            # Events
            RuleData("Opened Labyrinth I Door", lambda state,
             player: has_weapon(state, player)),
            RuleData("Use Labyrinth I Teleporter", lambda state, player: True)
        ]
    ),
    RegionData(
        "Labyrinth I - Entrance from Sand Zone Storehouse",
        [
            # Regions
            RuleData("Sand Zone Storehouse - Exit to Labyrinth I", lambda state, player: True),
            RuleData("Labyrinth I - Room Bottom", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth I - Teleporter to Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Teleporter to Labyrinth I", lambda state, player: True),
            RuleData("Labyrinth I - Room Bottom", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth I - Save Point",
        [
            # Regions
            RuleData("Labyrinth I - Room Bottom", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth H - Door to Labyrinth I",
        [
            # Regions
            RuleData("Labyrinth I - Door to Labyrinth H", lambda state, player: True),
            RuleData("Labyrinth H - Door to Labyrinth W", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth H - Door to Labyrinth W",
        [
            # Regions
            RuleData("Labyrinth W - Door to Labyrinth H", lambda state, player: True),
            RuleData("Labyrinth H - Door to Labyrinth I", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Labyrinth H",
        [
            # Regions
            RuleData("Labyrinth H - Door to Labyrinth W", lambda state, player: True),
            RuleData("Labyrinth W - Outside Camp", lambda state,
             player: traverse_labyrinth_w(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Labyrinth Shop",
        [
            # Regions
            RuleData("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True),
            RuleData("Labyrinth W - Outside Camp", lambda state,
             player: traverse_labyrinth_w(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Outside Camp",
        [
            # Regions
            RuleData("Labyrinth W - Door to Labyrinth H", lambda state,
             player: traverse_labyrinth_w(state, player)),
            RuleData("Labyrinth W - Door to Labyrinth Shop", lambda state,
             player: traverse_labyrinth_w(state, player)),
            RuleData("Labyrinth W - Door to Camp (Lower)", lambda state,
             player: traverse_labyrinth_w(state, player)),
            RuleData("Labyrinth W - Door to Camp (Upper)", lambda state, player: can_break_blocks(state,
             player) and has_flight(state, player) and traverse_labyrinth_w(state, player)),
            RuleData("Labyrinth W - Door to Clinic Ruins", lambda state, player: state.has(
                "Clinic Key", player, 1) and traverse_labyrinth_w(state, player)),
            RuleData("Labyrinth W - Before Monster X", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Camp (Lower)",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Lower)", lambda state, player: True),
            RuleData("Labyrinth W - Outside Camp", lambda state,
             player: traverse_labyrinth_w(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Camp (Upper)",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Upper)", lambda state, player: True),
            RuleData("Labyrinth W - Outside Camp", lambda state, player: can_break_blocks(state,
             player) and traverse_labyrinth_w(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Clinic Ruins",
        [
            # Regions
            RuleData("Clinic Ruins - Door to Labyrinth W", lambda state, player: True),
            RuleData("Labyrinth W - Outside Camp", lambda state,
             player: traverse_labyrinth_w(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Labyrinth B",
        [
            # Regions
            RuleData("Labyrinth B - Door to Labyrinth W", lambda state, player: True),
            RuleData("Labyrinth W - Before Monster X", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth W - Before Monster X",
        [
            # Regions
            RuleData("Labyrinth W - Outside Camp", lambda state,
             player: state.has("Defeated Monster X", player, 1)),
            RuleData("Labyrinth W - Door to Labyrinth B", lambda state,
             player: state.has("Defeated Monster X", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Monster X", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Labyrinth Shop - Door to Labyrinth W",
        [
            # Regions
            RuleData("Labyrinth W - Door to Labyrinth Shop", lambda state, player: True),
            RuleData("Labyrinth Shop - Teleporter to Labyrinth M",
             lambda state, player: has_flight(state, player)),
            RuleData("Labyrinth Shop - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Labyrinth Shop - Chaba Chest (Machine Gun)",
             lambda state, player: state.has("Machine Gun", player, 1)),
            RuleData("Labyrinth Shop - Chaba Chest (Fireball)",
             lambda state, player: state.has("Fireball", player, 1)),
            RuleData("Labyrinth Shop - Chaba Chest (Spur)",
             lambda state, player: state.has("Spur", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth Shop - Teleporter to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Teleporter to Labyrinth Shop", lambda state, player: True),
            RuleData("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Labyrinth Shop - Save Point",
        [
            # Regions
            RuleData("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Camp - Door to Labyrinth W (Lower)",
        [
            # Regions
            RuleData("Labyrinth W - Door to Camp (Lower)", lambda state, player: True),
            RuleData("Camp - Door to Labyrinth W (Upper)", lambda state,
             player: state.has("Start in Camp", player, 1)),
            RuleData("Camp - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Camp - Dr. Gero", lambda state, player: True),
            # Events
            RuleData("Cure-All", lambda state, player: state.has("Cure-All", player, 1))
        ]
    ),
    RegionData(
        "Camp - Door to Labyrinth W (Upper)",
        [
            # Regions
            RuleData("Labyrinth W - Door to Camp (Upper)", lambda state, player: True),
            RuleData("Camp - Door to Labyrinth W (Lower)", lambda state,
             player: state.has("Start in Camp", player, 1))
        ],
        [
            # Locations
            RuleData("Camp - Camp Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Camp - Room Spawn",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Camp", lambda state, player: True)
        ]
    ),
    RegionData(
        "Camp - Save Point",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Clinic Ruins - Door to Labyrinth W",
        [
            # Regions
            RuleData("Labyrinth W - Door to Clinic Ruins", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Clinic Ruins - Puu Black Boss", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Final Cave - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Final Cave", lambda state, player: True),
            RuleData("Final Cave - Door to Balcony (Pre-Bosses)",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Final Cave - Door to Balcony (Pre-Bosses)",
        [
            # Regions
            RuleData("Balcony (Pre-Bosses) - Door to Final Cave", lambda state, player: True),
            RuleData("Final Cave - Door to Plantation",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Last Cave (Hidden) - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Last Cave (Hidden)", lambda state, player: True),
            RuleData("Last Cave (Hidden) - Before Red Demon", lambda state,
             player: state.has("Booster 2.0", player, 1) and has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Last Cave (Hidden) - Door to Balcony (Pre-Bosses)",
        [
            # Regions
            RuleData("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)",
             lambda state, player: True),
            RuleData("Last Cave (Hidden) - Before Red Demon", lambda state,
             player: state.has("Booster 2.0", player, 1) and has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Last Cave (Hidden) - Before Red Demon",
        [
            # Regions
            RuleData("Last Cave (Hidden) - Door to Plantation", lambda state,
             player: state.has("Defeated Red Demon", player, 1)),
            RuleData("Last Cave (Hidden) - Door to Balcony (Pre-Bosses)",
             lambda state, player: state.has("Defeated Red Demon", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Red Demon", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Exit to Throne Room",
        [
            # Regions
            RuleData("Throne Room - Entrance from Balcony (Pre-Bosses)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Door to Final Cave",
        [
            # Regions
            RuleData("Final Cave - Door to Balcony (Pre-Bosses)", lambda state, player: True),
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Door to Last Cave (Hidden)",
        [
            # Regions
            RuleData("Last Cave (Hidden) - Door to Balcony (Pre-Bosses)",
             lambda state, player: True),
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Door to Prefab Building",
        [
            # Regions
            RuleData("Prefab Building - Door to Balcony (Pre-Bosses)",
             lambda state, player: True),
            RuleData("Balcony (Pre-Bosses) - Exit to Throne Room", lambda state,
             player: state.has("Lowered Barrier", player, 1)),
            RuleData("Balcony (Pre-Bosses) - Door to Final Cave", lambda state,
             player: state.has("Booster 2.0", player, 1)),
            RuleData("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)",
             lambda state, player: state.has("Booster 2.0", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Lowered Barrier", lambda state, player: (
                state.has("Saved Sue", player, 1) and (
                    False or (  # Normal Ending
                        state.has("Iron Bond", player, 1) and
                        state.has("Booster 2.0", player, 1) and (
                            False or (  # Best Ending
                                state.has("Defeated Balfrog", player, 1) and
                                state.has("Defeated Balrog 1", player, 1) and
                                state.has("Defeated Balrog 2", player, 1) and
                                state.has("Defeated Balrog 3", player, 1) and
                                state.has("Defeated Curly", player, 1) and
                                state.has("Defeated Igor", player, 1) and
                                state.has("Defeated Ironhead", player, 1) and
                                state.has("Defeated Ma Pignon", player, 1) and
                                state.has("Defeated Monster X", player, 1) and
                                state.has("Defeated Omega", player, 1) and
                                state.has("Defeated Puu Black", player, 1) and
                                state.has("Defeated Sisters", player, 1) and
                                state.has("Defeated Toroko+", player, 1) and
                                state.has("Defeated Core", player, 1) and (
                                    False  # All Bosses
                                )
                            )
                        )
                    )
                )
            ))
        ]
    ),
    RegionData(
        "Prefab Building - Door to Balcony (Pre-Bosses)",
        [
            # Regions
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building",
             lambda state, player: True),
            RuleData("Prefab Building - Save Point/Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Prefab Building - Save Point/Bed",
        [
            # Regions
            RuleData("Prefab Building - Door to Balcony (Pre-Bosses)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Throne Room - Entrance from Balcony (Pre-Bosses)",
        [
            # Regions
            RuleData("Balcony (Pre-Bosses) - Exit to Throne Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Misery", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Throne Room - Exit to Balcony (Post-Bosses)",
        [
            # Regions
            RuleData("Balcony (Post-Bosses) - Entrance from Throne Room",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Throne Room - H/V Trigger to The King's Table",
        [
            # Regions
            RuleData("The King's Table - H/V Trigger to Throne Room",
             lambda state, player: True),
            RuleData("Throne Room - Exit to Balcony (Post-Bosses)", lambda state,
             player: state.has("Defeated Undead Core", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "The King's Table - H/V Trigger to Throne Room",
        [
            # Regions
            RuleData("Throne Room - H/V Trigger to The King's Table",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Doctor", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "The King's Table - H/V Trigger to Black Space",
        [
            # Regions
            RuleData("Black Space - H/V Trigger to The King's Table",
             lambda state, player: True),
            RuleData("The King's Table - H/V Trigger to Throne Room", lambda state,
             player: state.has("Defeated Undead Core", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Black Space - H/V Trigger to The King's Table",
        [
            # Regions
            RuleData("The King's Table - H/V Trigger to Black Space",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Undead Core", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Entrance from Throne Room",
        [
            # Regions
            RuleData("Throne Room - Exit to Balcony (Post-Bosses)",
             lambda state, player: True),
            RuleData("Balcony (Post-Bosses) - Exit to Prefab House",
             lambda state, player: state.has("Iron Bond", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Normal Ending", lambda state, player: state.has(
                "Defeated Undead Core", player, 1))
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Exit to Prefab House",
        [
            # Regions
            RuleData("Prefab House - Entrance from Balcony (Post-Bosses)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Entrance from Prefab House",
        [
            # Regions
            RuleData("Prefab House - Exit to Balcony (Post-Bosses)",
             lambda state, player: True),
            RuleData("Balcony (Post-Bosses) - Entrance from Throne Room",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Prefab House - Entrance from Balcony (Post-Bosses)",
        [
            # Regions
            RuleData("Balcony (Post-Bosses) - Exit to Prefab House",
             lambda state, player: True),
            RuleData("Prefab House - Exit to Balcony (Post-Bosses)",
             lambda state, player: True),
            RuleData("Prefab House - Exit to Sacred Grounds - B1", lambda state, player: True),
            RuleData("Prefab House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Prefab House - Exit to Balcony (Post-Bosses)",
        [
            # Regions
            RuleData("Balcony (Post-Bosses) - Entrance from Prefab House",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Prefab House - Exit to Sacred Grounds - B1",
        [
            # Regions
            RuleData("Sacred Grounds - B1 - Entrance from Prefab House",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Prefab House - Save Point",
        [
            # Regions
            RuleData("Prefab House - Entrance from Balcony (Post-Bosses)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B1 - Entrance from Prefab House",
        [
            # Regions
            RuleData("Prefab House - Exit to Sacred Grounds - B1", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Sacred Grounds - B1 - Hell B1 Spot", lambda state,
             player: state.has("Booster 2.0", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B1 - Door to Sacred Grounds - B2",
        [
            # Regions
            RuleData("Sacred Grounds - B2 - Door to Sacred Grounds - B1",
             lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Sacred Grounds - B1 - Hell B1 Spot", lambda state,
             player: state.has("Booster 2.0", player, 1)),
            # Events
            RuleData("Curly", lambda state, player: state.has("Used Ma Pignon", player, 1))
        ]
    ),
    RegionData(
        "Sacred Grounds - B2 - Door to Sacred Grounds - B1",
        [
            # Regions
            RuleData("Sacred Grounds - B1 - Door to Sacred Grounds - B2",
             lambda state, player: True),
            RuleData("Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3",
        [
            # Regions
            RuleData("Sacred Grounds - B3 - H/V Trigger to Sacred Grounds - B2",
             lambda state, player: True),
            RuleData("Sacred Grounds - B2 - Door to Sacred Grounds - B1",
             lambda state, player: has_weapon(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B3 - H/V Trigger to Sacred Grounds - B2",
        [
            # Regions
            RuleData("Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3",
             lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Sacred Grounds - B3 - Hell B3 Chest", lambda state,
             player: has_flight(state, player) and has_weapon(state, player)),
            # Events
            RuleData("Heavy Press", lambda state, player: can_kill_bosses(
                state, player) and has_flight(state, player))
        ]
    ),
    RegionData(
        "Sacred Grounds - B3 - Exit to Passage?",
        [
            # Regions
            RuleData("Passage? - Entrance from Sacred Grounds - B3", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Corridor - Door to Passage?",
        [
            # Regions
            RuleData("Passage? - Door to Corridor", lambda state, player: True),
            RuleData("Corridor - Exit to Seal Chamber", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Corridor - Exit to Seal Chamber",
        [
            # Regions
            RuleData("Seal Chamber - Entrance from Corridor", lambda state, player: True),
            RuleData("Corridor - Door to Passage?", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Seal Chamber - Entrance from Corridor",
        [
            # Regions
            RuleData("Corridor - Exit to Seal Chamber", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Best Ending", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Start Point - Door to First Cave",
        [
            # Regions
            RuleData("First Cave - Door to Start Point", lambda state, player: True),
            RuleData("Start Point - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Start Point - Save Point",
        [
            # Regions
            RuleData("Start Point - Door to First Cave", lambda state, player: True),
            RuleData("Start Point - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Start Point - Room Spawn",
        [
            # Regions
        ],
        [
            # Locations
            # Events
            RuleData("Start Point", lambda state, player: True)
        ]
    ),
    RegionData(
        "Start Point - Refill",
        [
            # Regions
            RuleData("Start Point - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "First Cave - Door to Start Point",
        [
            # Regions
            RuleData("Start Point - Door to First Cave", lambda state, player: True),
            RuleData("First Cave - Door to Hermit Gunsmith", lambda state, player: True),
            RuleData("First Cave - Door to Mimiga Village", lambda state, player: can_break_blocks(state,
             player) and (has_weapon(state, player) or state.has("Start in Start Point", player, 1)))
        ],
        [
            # Locations
            RuleData("First Cave - First Cave Life Capsule", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "First Cave - Door to Hermit Gunsmith",
        [
            # Regions
            RuleData("Hermit Gunsmith - Door to First Cave", lambda state, player: True),
            RuleData("First Cave - Door to Start Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "First Cave - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to First Cave", lambda state, player: True),
            RuleData("First Cave - Door to Start Point", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Hermit Gunsmith - Door to First Cave",
        [
            # Regions
            RuleData("First Cave - Door to Hermit Gunsmith", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Hermit Gunsmith - Hermit Gunsmith Chest", lambda state, player: True),
            RuleData("Hermit Gunsmith - Tetsuzou", lambda state, player: (state.has("Polar Star", player, 1)
             or state.has("Spur", player, 1)) and state.has("Defeated Core", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to First Cave",
        [
            # Regions
            RuleData("First Cave - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Room Centre",
        [
            # Regions
            RuleData("Mimiga Village - Door to First Cave",
             lambda state, player: has_flight(state, player)),
            RuleData("Mimiga Village - Door to Save Point", lambda state, player: True),
            RuleData("Mimiga Village - Door to Reservoir", lambda state, player: True),
            RuleData("Mimiga Village - Door to Yamashita Farm", lambda state, player: True),
            RuleData("Mimiga Village - Door to Assembly Hall", lambda state, player: True),
            RuleData("Mimiga Village - Door to Graveyard", lambda state,
             player: state.has("Toroko Kidnapped", player, 1)),
            RuleData("Mimiga Village - Door to Shack", lambda state, player: True),
            RuleData("Mimiga Village - Door to Arthur's House", lambda state,
             player: state.has("Arthur's Key", player, 1))
        ],
        [
            # Locations
            RuleData("Mimiga Village - Mimiga Village Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Save Point",
        [
            # Regions
            RuleData("Save Point - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Reservoir",
        [
            # Regions
            RuleData("Reservoir - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Yamashita Farm",
        [
            # Regions
            RuleData("Yamashita Farm - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Assembly Hall",
        [
            # Regions
            RuleData("Assembly Hall - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Graveyard",
        [
            # Regions
            RuleData("Graveyard - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Shack",
        [
            # Regions
            RuleData("Shack - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Door to Mimiga Village", lambda state, player: True),
            RuleData("Mimiga Village - Room Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Save Point - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Save Point", lambda state, player: True),
            RuleData("Save Point - Save Point", lambda state, player: True),
            RuleData("Save Point - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Save Point - Save Point",
        [
            # Regions
            RuleData("Save Point - Door to Mimiga Village", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Save Point - Refill",
        [
            # Regions
            RuleData("Save Point - Door to Mimiga Village", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Yamashita Farm - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Yamashita Farm", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Yamashita Farm - Yamashita Farm", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Reservoir", lambda state, player: True),
            RuleData("Reservoir - Debug Cat to Dark Place", lambda state,
             player: state.has("Defeated Ironhead", player, 1))
        ],
        [
            # Locations
            RuleData("Reservoir - Reservoir", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Debug Cat to Dark Place",
        [
            # Regions
            RuleData("Dark Place - Entrance from Reservoir", lambda state, player: True),
            RuleData("Reservoir - Door to Mimiga Village", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Entrance from Main Artery",
        [
            # Regions
            RuleData("Main Artery - Exit to Reservoir", lambda state, player: True),
            RuleData("Reservoir - Door to Mimiga Village", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Assembly Hall - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Assembly Hall", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Assembly Hall - Assembly Hall Fireplace", lambda state,
             player: state.has("Jellyfish Juice", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Graveyard", lambda state, player: True),
            RuleData("Graveyard - Door to Storage", lambda state,
             player: has_flight(state, player))
        ],
        [
            # Locations
            RuleData("Graveyard - Arthur's Grave", lambda state, player: True),
            RuleData("Graveyard - Mr. Little (Graveyard)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Storage",
        [
            # Regions
            RuleData("Storage - Door to Graveyard", lambda state, player: True),
            RuleData("Graveyard - Door to Mimiga Village", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Storage - Door to Graveyard",
        [
            # Regions
            RuleData("Graveyard - Door to Storage", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Storage - Storage? Chest", lambda state,
             player: state.has("Saved Curly", player, 1)),
            # Events
            RuleData("Ma Pignon", lambda state, player: state.has("Mushroom Badge", player, 1) and (
                state.has("Polar Star", player, 1) or
                state.has("Machine Gun", player, 1) or
                state.has("Bubbler", player, 1) or
                state.has("Fireball", player, 1) or
                state.has("Spur", player, 1) or
                state.has("Snake", player, 1) or
                state.has("Nemesis", player, 1)
            ))
        ]
    ),
    RegionData(
        "Shack - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Shack", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Toroko Kidnapped", lambda state, player: state.has(
                "Silver Locket", player, 1) and has_weapon(state, player)),
            RuleData("Balrog 1", lambda state, player: state.has(
                "Toroko Kidnapped", player, 1) and can_kill_bosses(state, player)),
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun",
             player, 1) and state.has("Defeated Balrog 1", player, 1))
        ]
    ),
    RegionData(
        "Arthur's House - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Arthur's House", lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Main Teleporter",
        [
            # Regions
            RuleData("Arthur's House - Door to Mimiga Village", lambda state,
             player: state.has("Arthur's Key", player, 1)),
            RuleData("Arthur's House - Save Point", lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Egg Corridor",
             lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Grasstown", lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Sand Zone", lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Labyrinth B", lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Teleporter", lambda state, player: True),
            RuleData("Arthur's House - Teleporter to Egg Corridor?", lambda state, player: state.has(
                "Defeated Core", player, 1) or state.has("Used Egg Corridor? Teleporter", player, 1)),
            RuleData("Arthur's House - Room Spawn", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Arthur's House - Professor Booster", lambda state,
             player: state.has("Defeated Core", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Save Point",
        [
            # Regions
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True),
            RuleData("Arthur's House - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Teleporter to Arthur's House",
             lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Teleporter to Arthur's House", lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Teleporter to Arthur's House", lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Labyrinth B",
        [
            # Regions
            RuleData("Labyrinth B - Teleporter to Arthur's House", lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Teleporter",
        [
            # Regions
            RuleData("Teleporter - Teleporter to Arthur's House", lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Teleporter to Egg Corridor?",
        [
            # Regions
            RuleData("Egg Corridor? - Teleporter to Arthur's House",
             lambda state, player: True),
            RuleData("Arthur's House - Main Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Room Spawn",
        [
            # Regions
        ],
        [
            # Locations
            # Events
            RuleData("Arthur's House", lambda state, player: True)
        ]
    ),
    RegionData(
        "Arthur's House - Refill",
        [
            # Regions
            RuleData("Arthur's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Rest Area",
        [
            # Regions
            RuleData("Rest Area - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Teleporter",
        [
            # Regions
            RuleData("Teleporter - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Lower Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Storehouse",
        [
            # Regions
            RuleData("Storehouse - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Jail No. 1 (Lower)",
        [
            # Regions
            RuleData("Jail No. 1 - Door to Plantation (Lower)", lambda state, player: True),
            RuleData("Plantation - Upper Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Jail No. 1 (Upper)",
        [
            # Regions
            RuleData("Jail No. 1 - Door to Plantation (Upper)", lambda state, player: True),
            RuleData("Plantation - Upper Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Jail No. 2",
        [
            # Regions
            RuleData("Jail No. 2 - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Upper Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Last Cave (Hidden)",
        [
            # Regions
            RuleData("Last Cave (Hidden) - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Top Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Passage?",
        [
            # Regions
            RuleData("Passage? - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Hideout",
        [
            # Regions
            RuleData("Hideout - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Lower Level",
        [
            # Regions
            RuleData("Plantation - Door to Teleporter", lambda state,
             player: state.has("Teleporter Room Key", player, 1)),
            RuleData("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Plantation - Kanpachi's Bucket", lambda state, player: True),
            RuleData("Plantation - Jammed it into Curly's mouth", lambda state,
             player: state.has("Saved Curly", player, 1) and state.has("Ma Pignon", player, 1)),
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Plantation - Middle Level",
        [
            # Regions
            RuleData("Plantation - Door to Rest Area", lambda state, player: True),
            RuleData("Plantation - Door to Storehouse", lambda state, player: True),
            RuleData("Plantation - Door to Passage?", lambda state, player: True),
            RuleData("Plantation - Door to Hideout", lambda state,
             player: state.has("Sue's Letter", player, 1)),
            RuleData("Plantation - Lower Level", lambda state, player: True),
            RuleData("Plantation - Upper Level", lambda state, player: True),
            RuleData("Plantation - Top Level", lambda state,
             player: state.has("Built Rocket", player, 1))
        ],
        [
            # Locations
            RuleData("Plantation - Broken Sprinker", lambda state,
             player: state.has("Mimiga Mask", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Plantation - Upper Level",
        [
            # Regions
            RuleData("Plantation - Door to Jail No. 1 (Lower)", lambda state, player: True),
            RuleData("Plantation - Door to Jail No. 1 (Upper)",
             lambda state, player: has_flight(state, player)),
            RuleData("Plantation - Door to Jail No. 2", lambda state, player: True),
            RuleData("Plantation - Middle Level", lambda state, player: True),
        ],
        [
            # Locations
            RuleData("Plantation - Plantation Platforming Spot",
             lambda state, player: has_flight(state, player)),
            RuleData("Plantation - Plantation Puppy", lambda state,
             player: state.has("Built Rocket", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Final Cave",
        [
            # Regions
            RuleData("Final Cave - Door to Plantation", lambda state, player: True),
            RuleData("Plantation - Top Level", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Plantation - Top Level",
        [
            # Regions
            RuleData("Plantation - Door to Last Cave (Hidden)", lambda state, player: state.has(
                "Booster 2.0", player, 1) and (state.has("Built Rocket", player, 1))),
            RuleData("Plantation - Upper Level", lambda state, player: True),
            RuleData("Plantation - Door to Final Cave", lambda state, player: state.has(
                "Booster 2.0", player, 1) and (state.has("Built Rocket", player, 1)))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Storehouse - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Storehouse", lambda state, player: True),
            RuleData("Storehouse - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Storehouse - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Storehouse", lambda state, player: True),
            RuleData("Storehouse - Door to Plantation", lambda state, player: True),
            RuleData("Storehouse - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Storehouse - Itoh", lambda state,
             player: state.has("Sue's Letter", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Storehouse - Save Point",
        [
            # Regions
            RuleData("Storehouse - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Passage? - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Passage?", lambda state, player: True),
            RuleData("Passage? - Door to Statue Chamber", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Passage? - Door to Statue Chamber",
        [
            # Regions
            RuleData("Statue Chamber - Door to Passage?", lambda state, player: True),
            RuleData("Passage? - Door to Plantation", lambda state,
             player: state.has("Defeated Undead Core", player, 1)),
            RuleData("Passage? - Door to Corridor", lambda state,
             player: state.has("Entered Passage? from above", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Passage? - Door to Corridor",
        [
            # Regions
            RuleData("Corridor - Door to Passage?", lambda state, player: True),
            RuleData("Passage? - Door to Statue Chamber", lambda state, player: has_flight(state,
             player) and state.has("Entered Passage? from above", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Passage? - Entrance from Sacred Grounds - B3",
        [
            # Regions
            RuleData("Sacred Grounds - B3 - Exit to Passage?", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Passage from Above", lambda state, player: True)
        ]
    ),
    RegionData(
        "Statue Chamber - Door to Passage?",
        [
            # Regions
            RuleData("Passage? - Door to Statue Chamber", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Rest Area - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Rest Area", lambda state, player: True),
            RuleData("Rest Area - Bed", lambda state,
             player: state.has("Built Rocket", player, 1))
        ],
        [
            # Locations
            RuleData("Rest Area - Megane", lambda state, player: state.has("Mimiga Mask",
             player, 1) and state.has("Broken Sprinkler", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Rest Area - Bed",
        [
            # Regions
            RuleData("Rest Area - Door to Plantation", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Teleporter - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Teleporter", lambda state, player: True),
            RuleData("Teleporter - Room Hub", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Teleporter - Room Hub",
        [
            # Regions
            RuleData("Teleporter - Door to Plantation", lambda state,
             player: state.has("Teleporter Room Key", player, 1)),
            RuleData("Teleporter - Teleporter to Arthur's House", lambda state, player: state.has(
                "Teleporter Room Key", player, 1) or state.has("Droll Attack", player, 1)),
            RuleData("Teleporter - Exit to Jail No. 1", lambda state,
             player: state.has("Droll Attack", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Droll Attack", lambda state, player: state.has(
                "Teleporter Room Key", player, 1))
        ]
    ),
    RegionData(
        "Teleporter - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Teleporter", lambda state, player: True),
            RuleData("Teleporter - Room Hub", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Teleporter - Exit to Jail No. 1",
        [
            # Regions
            RuleData("Jail No. 1 - Entrance from Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Door to Plantation (Upper)",
        [
            # Regions
            RuleData("Plantation - Door to Jail No. 1 (Upper)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Entrance from Teleporter",
        [
            # Regions
            RuleData("Teleporter - Exit to Jail No. 1", lambda state, player: True),
            RuleData("Jail No. 1 - Door to Plantation (Upper)", lambda state, player: True),
            RuleData("Jail No. 1 - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Jail No. 1 - Jail No. 1", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Door to Plantation (Lower)",
        [
            # Regions
            RuleData("Plantation - Door to Jail No. 1 (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Save Point",
        [
            # Regions
            RuleData("Jail No. 1 - Entrance from Teleporter", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jail No. 2 - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Jail No. 2", lambda state, player: True),
            RuleData("Jail No. 2 - Teleporter to Shelter", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jail No. 2 - Teleporter to Shelter",
        [
            # Regions
            RuleData("Shelter - Teleporter to Jail No. 2", lambda state, player: True),
            RuleData("Jail No. 2 - Door to Plantation", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Hideout - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Hideout", lambda state, player: True),
            RuleData("Hideout - Bed", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Hideout - Chivalry Sakamoto's Wife", lambda state,
             player: state.has("Booster 0.8", player, 1)),
            # Events
            RuleData("Built Rocket", lambda state, player: (state.has("Booster 0.8", player, 1) or state.has(
                "Booster 2.0", player, 1)) and state.has("Sprinkler", player, 1) and state.has("Controller", player, 1))
        ]
    ),
    RegionData(
        "Hideout - Bed",
        [
            # Regions
            RuleData("Hideout - Door to Plantation", lambda state, player: True),
            RuleData("Hideout - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Hideout - Save Point",
        [
            # Regions
            RuleData("Hideout - Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Cthulhu's Abode? (Upper)",
        [
            # Regions
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Upper)",
             lambda state, player: True),
            RuleData("Egg Corridor? - Area Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Cthulhu's Abode? (Lower)",
        [
            # Regions
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Lower)",
             lambda state, player: True),
            RuleData("Egg Corridor? - West Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - West Side",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Lower)",
             lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Egg Corridor? - Dragon Chest", lambda state,
             player: has_weapon(state, player)),
            # Events
            RuleData("Used Egg Corridor? Teleporter", lambda state, player: True),
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - Area Centre",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Upper)",
             lambda state, player: True),
            RuleData("Egg Corridor? - Door to Egg Observation Room? (West)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - East Side",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Egg Observation Room? (East)",
             lambda state, player: has_weapon(state, player)),
            RuleData("Egg Corridor? - Door to Egg No. 00", lambda state, player: True),
            RuleData("Egg Corridor? - Door to Side Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Egg Observation Room? (West)",
        [
            # Regions
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Western)",
             lambda state, player: True),
            RuleData("Egg Corridor? - Area Centre", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Egg Observation Room? (East)",
        [
            # Regions
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Eastern)",
             lambda state, player: True),
            RuleData("Egg Corridor? - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Egg No. 00",
        [
            # Regions
            RuleData("Egg No. 00 - Door to Egg Corridor?", lambda state, player: True),
            RuleData("Egg Corridor? - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Side Room",
        [
            # Regions
            RuleData("Side Room - Door to Egg Corridor?", lambda state, player: True),
            RuleData("Egg Corridor? - East Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Egg Corridor?",
             lambda state, player: True),
            RuleData("Egg Corridor? - West Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Cthulhu's Abode? - Door to Egg Corridor? (Upper)",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Upper)",
             lambda state, player: True),
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Lower)", lambda state,
             player: has_weapon(state, player) and can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Cthulhu's Abode? - Door to Egg Corridor? (Lower)",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Lower)",
             lambda state, player: True),
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Upper)", lambda state,
             player: has_weapon(state, player) and (can_break_blocks(state, player)))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room? - Door to Egg Corridor? (Western)",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Egg Observation Room? (West)",
             lambda state, player: True),
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Eastern)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room? - Door to Egg Corridor? (Eastern)",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Egg Observation Room? (East)",
             lambda state, player: True),
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Western)", lambda state,
             player: state.has("Defeated Sisters", player, 1) or has_flight(state, player)),
            RuleData("Egg Observation Room? - Save Point", lambda state,
             player: state.has("Defeated Sisters", player, 1))
        ],
        [
            # Locations
            RuleData("Egg Observation Room? - Sisters Boss", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room? - Save Point",
        [
            # Regions
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Eastern)",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room - Door to Egg Corridor?",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Side Room", lambda state, player: True),
            RuleData("Side Room - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room - Save Point",
        [
            # Regions
            RuleData("Side Room - Door to Egg Corridor?", lambda state, player: True),
            RuleData("Side Room - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room - Refill",
        [
            # Regions
            RuleData("Side Room - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg No. 00 - Door to Egg Corridor?",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Egg No. 00", lambda state, player: True),
            RuleData("Egg No. 00 - Door to Outer Wall", lambda state,
             player: state.has("Saved Kazuma", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg No. 00 - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Egg No. 00", lambda state, player: True),
            RuleData("Egg No. 00 - Door to Egg Corridor?", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Outer Wall - Door to Egg No. 00",
        [
            # Regions
            RuleData("Egg No. 00 - Door to Outer Wall", lambda state, player: True),
            RuleData("Outer Wall - Room Bottom", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Outer Wall - Door to Little House",
        [
            # Regions
            RuleData("Little House - Door to Outer Wall", lambda state, player: True),
            RuleData("Outer Wall - Room Bottom", lambda state,
             player: has_flight(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Outer Wall - Outside Clock Room",
        [
            # Regions
            RuleData("Outer Wall - Room Bottom", lambda state, player: True),
            RuleData("Outer Wall - Room Top", lambda state,
             player: has_weapon(state, player)),
            RuleData("Outer Wall - Door to Clock Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Outer Wall - Door to Storehouse",
        [
            # Regions
            RuleData("Storehouse - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Outer Wall from Storehouse", lambda state, player: True)
        ]
    ),
    RegionData(
        "Outer Wall - Room Bottom",
        [
            # Regions
            RuleData("Outer Wall - Door to Egg No. 00", lambda state,
             player: state.has("Saved Kazuma", player, 1)),
            RuleData("Outer Wall - Door to Little House",
             lambda state, player: has_flight(state, player)),
            RuleData("Outer Wall - Outside Clock Room", lambda state, player: has_flight(state, player)
             or (remove_points_of_no_return(state, player) and state.has("Entered Outer Wall from above", player, 1)))
        ],
        [
            # Locations
            # Events
            RuleData("Bad Ending", lambda state, player: state.has(
                "Saved Kazuma", player, 1) and state.has("Defeated Core", player, 1))
        ]
    ),
    RegionData(
        "Outer Wall - Room Top",
        [
            # Regions
            RuleData("Outer Wall - Outside Clock Room", lambda state, player: True),
            RuleData("Outer Wall - Door to Storehouse", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Outer Wall - Door to Clock Room",
        [
            # Regions
            RuleData("Clock Room - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Outer Wall from Clock Room", lambda state, player: True)
        ]
    ),
    RegionData(
        "Little House - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Little House", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Little House - Little House", lambda state, player: state.has("Blade",
             player, 1) and state.has("Little Man", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Clock Room - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Clock Room", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Clock Room - Clock Room", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Door to Jenka's House",
        [
            # Regions
            RuleData("Jenka's House - Door to Sand Zone", lambda state, player: True),
            RuleData("Sand Zone - Outside Jenka's House", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Sand Zone", lambda state, player: True),
            RuleData("Sand Zone - Outside Sand Zone Residence",
             lambda state, player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Outside Sand Zone Residence",
        [
            # Regions
            RuleData("Sand Zone - Teleporter to Arthur's House",
             lambda state, player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Door to Sand Zone Residence", lambda state, player: True),
            RuleData("Sand Zone - Above Sunstones", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Door to Sand Zone Residence",
        [
            # Regions
            RuleData("Sand Zone Residence - Door to Sand Zone", lambda state, player: True),
            RuleData("Sand Zone - Outside Sand Zone Residence", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Lower Side",
        [
            # Regions
            RuleData("Sand Zone - Door to Deserted House", lambda state, player: True),
            RuleData("Sand Zone - Outside Jenka's House", lambda state,
             player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Outside Sand Zone Storehouse",
             lambda state, player: has_flight(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Puppy (Run)", lambda state, player: True),
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Sand Zone - Door to Deserted House",
        [
            # Regions
            RuleData("Deserted House - Door to Sand Zone", lambda state, player: True),
            RuleData("Sand Zone - Lower Side", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Exit to Sand Zone Storehouse",
        [
            # Regions
            RuleData("Sand Zone Storehouse - Entrance from Sand Zone",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Above Sunstones",
        [
            # Regions
            RuleData("Sand Zone - Outside Sand Zone Residence",
             lambda state, player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Before Omega", lambda state,
             player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Outside Jenka's House", lambda state, player: state.has(
                "Defeated Omega", player, 1) and can_break_blocks(state, player)),
            RuleData("Sand Zone - Pawprint Spot", lambda state, player: state.has("Defeated Omega",
             player, 1) and can_break_blocks(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Polish Spot", lambda state,
             player: can_break_blocks(state, player)),
            # Events
            RuleData("Level Up Machine Gun", lambda state, player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Sand Zone - Before Omega",
        [
            # Regions
            RuleData("Sand Zone - Above Sunstones", lambda state,
             player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Refill (Upper)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Omega", lambda state, player: can_break_blocks(state, player))
        ]
    ),
    RegionData(
        "Sand Zone - Outside Jenka's House",
        [
            # Regions
            RuleData("Sand Zone - Door to Jenka's House", lambda state, player: True),
            RuleData("Sand Zone - Lower Side", lambda state,
             player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Above Sunstones", lambda state, player: can_break_blocks(state,
             player) and state.has("Defeated Omega", player, 1)),
            RuleData("Sand Zone - Pawprint Spot", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Pawprint Spot",
        [
            # Regions
            RuleData("Sand Zone - Above Sunstones", lambda state, player: state.has(
                "Defeated Omega", player, 1) and can_break_blocks(state, player)),
            RuleData("Sand Zone - Outside Jenka's House", lambda state,
             player: can_break_blocks(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Pawprint Spot", lambda state, player: True),
            RuleData("Sand Zone - Puppy (Chest)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Refill (Upper)",
        [
            # Regions
            RuleData("Sand Zone - Before Omega", lambda state, player: True),
            RuleData("Sand Zone - Save Point (Upper)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Refill (Lower)",
        [
            # Regions
            RuleData("Sand Zone - Outside Sand Zone Storehouse", lambda state, player: True),
            RuleData("Sand Zone - Save Point (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Teleporter to Labyrinth I",
        [
            # Regions
            RuleData("Labyrinth I - Teleporter to Sand Zone", lambda state, player: True),
            RuleData("Sand Zone - Outside Sand Zone Storehouse", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Outside Sand Zone Storehouse",
        [
            # Regions
            RuleData("Sand Zone - Lower Side", lambda state,
             player: has_weapon(state, player)),
            RuleData("Sand Zone - Exit to Sand Zone Storehouse", lambda state,
             player: state.has("Returned Puppies", player, 1)),
            RuleData("Sand Zone - Refill (Lower)", lambda state,
             player: can_break_blocks(state, player)),
            RuleData("Sand Zone - Teleporter to Labyrinth I", lambda state, player: state.has(
                "Used Labyrinth I Teleporter", player, 1) and remove_points_of_no_return(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Puppy (Sleep)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Save Point (Lower)",
        [
            # Regions
            RuleData("Sand Zone - Refill (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Save Point (Upper)",
        [
            # Regions
            RuleData("Sand Zone - Refill (Upper)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Residence - Door to Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Door to Sand Zone Residence", lambda state, player: True),
            RuleData("Sand Zone Residence - Door to Small Room", lambda state,
             player: state.has("Defeated Curly", player, 1)),
            RuleData("Sand Zone Residence - Before Curly", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Sand Zone Residence - Curly Boss", lambda state, player: state.has("Defeated Curly",
             player, 1) and (state.has("Polar Star", player, 1) or state.has("Spur", player, 1))),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Residence - Door to Small Room",
        [
            # Regions
            RuleData("Small Room - Door to Sand Zone Residence", lambda state, player: True),
            RuleData("Sand Zone Residence - Door to Sand Zone", lambda state,
             player: state.has("Defeated Curly", player, 1)),
            RuleData("Sand Zone Residence - Before Curly", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Residence - Before Curly",
        [
            # Regions
        ],
        [
            # Locations
            # Events
            RuleData("Curly", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Small Room - Door to Sand Zone Residence",
        [
            # Regions
            RuleData("Sand Zone Residence - Door to Small Room", lambda state, player: True),
            RuleData("Small Room - Refill", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Small Room - Puppy (Curly)", lambda state, player: True),
            RuleData("Small Room - Curly's Closet", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Small Room - Refill",
        [
            # Regions
            RuleData("Small Room - Door to Sand Zone Residence", lambda state, player: True),
            RuleData("Small Room - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Small Room - Save Point",
        [
            # Regions
            RuleData("Small Room - Refill", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Jenka's House - Door to Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Door to Jenka's House", lambda state, player: True),
            RuleData("Jenka's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Jenka's House - Jenka", lambda state,
             player: state.has("Returned Puppies", player, 1)),
            # Events
            RuleData("Returned Puppies", lambda state,
             player: state.has("Puppies", player, 5))
        ]
    ),
    RegionData(
        "Jenka's House - Save Point",
        [
            # Regions
            RuleData("Jenka's House - Door to Sand Zone", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Deserted House - Door to Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Door to Deserted House", lambda state, player: True),
            RuleData("Deserted House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            RuleData("Deserted House - Puppy (Dark)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Deserted House - Save Point",
        [
            # Regions
            RuleData("Deserted House - Door to Sand Zone", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Storehouse - Entrance from Sand Zone",
        [
            # Regions
            RuleData("Sand Zone - Exit to Sand Zone Storehouse", lambda state, player: True),
            RuleData("Sand Zone Storehouse - Before Toroko+", lambda state, player: True),
            RuleData("Sand Zone Storehouse - Exit to Labyrinth I", lambda state,
             player: state.has("Defeated Toroko+", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Storehouse - Before Toroko+",
        [
            # Regions
        ],
        [
            # Locations
            # Events
            RuleData("Toroko+", lambda state, player: can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Sand Zone Storehouse - Exit to Labyrinth I",
        [
            # Regions
            RuleData("Labyrinth I - Entrance from Sand Zone Storehouse",
             lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
]
