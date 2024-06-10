from typing import List, NamedTuple, Callable, Optional

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

def trivial(state: CollectionState, player: int):
    """Inspired by Messenger"""
    return True


def has_flight(state: CollectionState, player: int):
    return state.has("Progressive Booster", player) or state.has_all({"Machine Gun", "Level MG"}, player)


def can_break_blocks(state: CollectionState, player: int):
    return state.has_any({"Blade", "Machine Gun", "Nemesis", "Progressive Polar Star"}, player)


def can_kill_bosses(state: CollectionState, player: int):
    return state.has_any({"Blade", "Bubbler", "Fireball", "Machine Gun", "Nemesis", "Progressive Polar Star", "Snake"}, player)


def has_weapon(state: CollectionState, player: int):
    return state.has_any({"Blade", "Bubbler", "Fireball", "Machine Gun", "Nemesis", "Progressive Polar Star", "Snake"}, player)
    # No missile logic yet "Progressive Missile Launcher"


def remove_points_of_no_return(state: CollectionState, player: int):
    return True


def traverse_labyrinth_w(state: CollectionState, player: int):
    return has_weapon(state, player)

REGIONS: List[RegionData] = [
    RegionData(
        "Egg Corridor - Door to Cthulhu's Abode (Lower)",
        [
            # Regions
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)", trivial),
            RuleData("Egg Corridor - Outside Cthulhu's Abode", trivial)
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
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Upper)", trivial),
            RuleData("Egg Corridor - Outside Cthulhu's Abode", trivial)
        ],
        [
            # Locations
            RuleData("Egg Corridor - Outside Cthulhu's Abode", trivial),
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Egg Corridor", trivial),
            RuleData("Egg Corridor - Outside Cthulhu's Abode", has_weapon)
        ],
        [
            # Locations
            RuleData("Egg Corridor - Basil Spot", trivial),
            # Events
            RuleData("Egg Corridor - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor - Outside Cthulhu's Abode",
        [
            # Regions
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Lower)", trivial),
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Upper)", has_flight),
            RuleData("Egg Corridor - Teleporter to Arthur's House", has_weapon),
            RuleData("Egg Corridor - Outside Egg Observation Room", has_weapon)
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
            RuleData("Egg Corridor - Outside Cthulhu's Abode", has_weapon),
            RuleData("Egg Corridor - H/V Trigger to Egg No. 06", trivial),
            RuleData("Egg Corridor - Door to Egg Observation Room", trivial),
            RuleData("Egg Corridor - H/V Trigger to Egg No. 01", trivial),
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
            RuleData("Egg No. 06 - Door to Egg Corridor", trivial),
            RuleData("Egg Corridor - Outside Egg Observation Room", trivial)
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
            RuleData("Egg Observation Room - Door to Egg Corridor", trivial),
            RuleData("Egg Corridor - Outside Egg Observation Room", trivial)
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
            RuleData("Egg No. 01 - Door to Egg Corridor", trivial),
            RuleData("Egg Corridor - Outside Egg Observation Room", trivial)
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
            RuleData("Defeated Igor", can_kill_bosses)
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Egg No. 00",
        [
            # Regions
            RuleData("Egg No. 00 - Door to Egg Corridor", trivial),
            RuleData("Egg Corridor - Outside Egg No. 00", lambda state,
                     player: state.has("Defeated Igor", player, 1)),
            RuleData("Egg Corridor - Door to Side Room", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Side Room",
        [
            # Regions
            RuleData("Side Room - Door to Egg Corridor", trivial),
            RuleData("Egg Corridor - Door to Egg No. 00", trivial)
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
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Lower)", trivial),
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Upper)",
                     can_break_blocks),
            RuleData("Cthulhu's Abode - Save Point", trivial)
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
            RuleData("Egg Corridor - Door to Cthulhu's Abode (Upper)", trivial),
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)",
                     can_break_blocks)
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
            RuleData("Cthulhu's Abode - Door to Egg Corridor (Lower)", trivial)
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
            RuleData("Egg Corridor - H/V Trigger to Egg No. 06", trivial)
        ],
        [
            # Locations
            RuleData("Egg No. 06 - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Door to Egg Observation Room", trivial)
        ],
        [
            # Locations
            RuleData("Egg Observation Room - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Egg No. 01 - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - H/V Trigger to Egg No. 01", trivial)
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
            RuleData("Egg Corridor - Door to Egg No. 00", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Saved Sue", trivial)
        ]
    ),
    RegionData(
        "Side Room - Door to Egg Corridor",
        [
            # Regions
            RuleData("Egg Corridor - Door to Side Room", trivial),
            RuleData("Side Room - Save Point", trivial)
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
            RuleData("Side Room - Door to Egg Corridor", trivial),
            RuleData("Side Room - Refill", trivial)
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
            RuleData("Side Room - Save Point", trivial)
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
            RuleData("Santa's House - Door to Grasstown", trivial),
            RuleData("Grasstown - West Side", trivial)
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
            RuleData("Chaco's House - Door to Grasstown", trivial),
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
            RuleData("Chaco's House - Exit to Grasstown", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Grasstown from Fireplace", trivial)
        ]
    ),
    RegionData(
        "Grasstown - Door to Power Room",
        [
            # Regions
            RuleData("Power Room - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Grasstown Save Point - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Grasstown Hut - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Shelter - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Execution Chamber - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Gum - Door to Grasstown", trivial),
            RuleData("Grasstown - East Side", trivial)
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
            RuleData("Grasstown - Door to Chaco's House", has_weapon),
            RuleData("Grasstown - Area Centre", lambda state, player: has_flight(state,
                                                                                 player) or state.has("Activated Fans", player, 1)),
            RuleData("Grasstown - Teleporter to Arthur's House", trivial)
        ],
        [
            # Locations
            RuleData("Grasstown - West Floor", has_weapon),
            RuleData("Grasstown - West Ceiling", has_weapon),
            RuleData("Grasstown - Kulala", lambda state, player: has_weapon(state,
                                                                            player) and state.has("Summoned Jellies", player, 1)),
            # Events
            RuleData("Returned Santa's Key", lambda state,
                     player: state.has("Santa's Key", player, 1)),
            RuleData("Grasstown (West) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Grasstown - East Side",
        [
            # Regions
            RuleData("Grasstown - Door to Power Room", lambda state,
                     player: state.has("Rusty Key", player, 1)),
            RuleData("Grasstown - Door to Save Point", trivial),
            RuleData("Grasstown - Door to Grasstown Hut", lambda state,
                     player: has_flight(state, player) or state.has("Activated Fans", player, 1)),
            RuleData("Grasstown - Door to Shelter", lambda state,
                     player: state.has("Explosive", player, 1)),
            RuleData("Grasstown - Door to Execution Chamber", trivial),
            RuleData("Grasstown - Door to Gum", lambda state, player: state.has("Gum Key", player, 1)
                     and (has_flight(state, player) or state.has("Activated Fans", player, 1))),
            RuleData("Grasstown - Area Centre", lambda state, player: (state.has("Activated Fans", player, 1) or has_flight(state, player)
                                                                       or (remove_points_of_no_return(state, player) and state.has("Entered Grasstown from Fireplace", player, 1))))
        ],
        [
            # Locations
            RuleData("Grasstown - East Chest", trivial),
            RuleData("Grasstown - Kazuma Crack", trivial),
            RuleData("Grasstown - Kazuma Chest", lambda state,
                     player: state.has("Rusty Key", player, 1)),
            # Events
            RuleData("Grasstown (East) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Grasstown - Area Centre",
        [
            # Regions
            RuleData("Grasstown - West Side", trivial),
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
            RuleData("Arthur's House - Teleporter to Grasstown", trivial),
            RuleData("Grasstown - West Side", trivial)
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
            RuleData("Grasstown - Door to Santa's House", trivial),
            RuleData("Santa's House - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Santa's House - Santa", lambda state,
                     player: state.has("Returned Santa's Key", player, 1)),
            RuleData("Santa's House - Fireplace", lambda state,
                     player: state.has("Jellyfish Juice", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Santa's House - Save Point",
        [
            # Regions
            RuleData("Santa's House - Door to Grasstown", trivial),
            RuleData("Santa's House - Refill", trivial)
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
            RuleData("Santa's House - Save Point", trivial)
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
            RuleData("Grasstown - Door to Chaco's House", trivial),
            RuleData("Chaco's House - Exit to Grasstown", lambda state,
                     player: state.has("Jellyfish Juice", player, 1)),
            RuleData("Chaco's House - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Chaco's House - Chaco's Bed",
                     lambda state, player: state.has("Returned Santa's Key", player, 1)),
            # Events
            RuleData("Summoned Jellies", lambda state, player: state.has(
                "Returned Santa's Key", player, 1))
        ]
    ),
    RegionData(
        "Chaco's House - Exit to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Entrance from Chaco's House", trivial)
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
            RuleData("Chaco's House - Door to Grasstown", trivial),
            RuleData("Chaco's House - Bed", trivial)
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
            RuleData("Chaco's House - Save Point", trivial)
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
            RuleData("Grasstown - Door to Power Room", trivial)
        ],
        [
            # Locations
            RuleData("Power Room - MALCO", lambda state, player: state.has("Activated Fans", player, 1) and state.has("Charcoal", player, 1)
                     and state.has("Jellyfish Juice", player, 1) and state.has("Gum Base", player, 1) and state.has("Defeated Balrog 2", player, 1)),
            # Events
            RuleData("Activated Fans", trivial),
            RuleData("Defeated Balrog 2", can_kill_bosses)
        ]
    ),
    RegionData(
        "Grasstown Save Point - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Save Point", trivial),
            RuleData("Grasstown Save Point - Save Point", trivial),
            RuleData("Grasstown Save Point - Refill", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown Save Point - Save Point",
        [
            # Regions
            RuleData("Grasstown Save Point - Door to Grasstown", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Grasstown Save Point - Refill",
        [
            # Regions
            RuleData("Grasstown Save Point - Door to Grasstown", trivial)
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
            RuleData("Grasstown - Door to Grasstown Hut", trivial)
        ],
        [
            # Locations
            RuleData("Grasstown Hut - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Execution Chamber - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Execution Chamber", trivial)
        ],
        [
            # Locations
            RuleData("Execution Chamber - Above", can_break_blocks),
            # Events
        ]
    ),
    RegionData(
        "Gum - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Gum", trivial)
        ],
        [
            # Locations
            RuleData("Gum - Chest", trivial),
            # Events
            RuleData("Defeated Balfrog", can_kill_bosses),
        ]
    ),
    RegionData(
        "Shelter - Door to Grasstown",
        [
            # Regions
            RuleData("Grasstown - Door to Shelter", trivial),
            RuleData("Shelter - Save Point", lambda state,
                     player: state.has("Saved Kazuma", player, 1)),
            RuleData("Shelter - Teleporter to Jail No. 2", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Saved Kazuma", trivial)
        ]
    ),
    RegionData(
        "Shelter - Save Point",
        [
            # Regions
            RuleData("Shelter - Door to Grasstown", trivial),
            RuleData("Shelter - Refill", trivial)
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
            RuleData("Jail No. 2 - Teleporter to Shelter", trivial),
            RuleData("Shelter - Door to Grasstown", lambda state,
                     player: state.has("Explosive", player, 1))
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Shelter - Refill",
        [
            # Regions
            RuleData("Shelter - Save Point", trivial)
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
            RuleData("Boulder Chamber - Door to Labyrinth B", trivial),
            RuleData("Labyrinth B - Door to Labyrinth W", trivial)
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
            RuleData("Labyrinth W - Door to Labyrinth B", trivial),
            RuleData("Labyrinth B - Door to Boulder Chamber", trivial),
            RuleData("Labyrinth B - Teleporter to Arthur's House", trivial),
            RuleData("Labyrinth B - Save Point", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Labyrinth B from Above", trivial)
        ]
    ),
    RegionData(
        "Labyrinth B - Teleporter to Arthur's House",
        [
            # Regions
            RuleData("Arthur's House - Teleporter to Labyrinth B", trivial),
            RuleData("Labyrinth B - Door to Labyrinth W", lambda state, player: has_flight(state, player)
                     or (state.has("Entered Labyrinth B from Above", player, 1) and remove_points_of_no_return(state, player)))
        ],
        [
            # Locations
            RuleData("Labyrinth B - Booster Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Save Point",
        [
            # Regions
            RuleData("Labyrinth B - Door to Labyrinth W", trivial),
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
            RuleData("Labyrinth B - Save Point", trivial)
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
            RuleData("Labyrinth B - Door to Boulder Chamber", trivial),
            RuleData("Boulder Chamber - Door to Labyrinth M", lambda state,
                     player: state.has("Defeated Balrog 3", player, 1)),
            RuleData("Boulder Chamber - Save Point", lambda state,
                     player: state.has("Defeated Balrog 3", player, 1))
        ],
        [
            # Locations
            RuleData("Boulder Chamber - Chest", lambda state,
                     player: state.has("Defeated Balrog 3", player, 1)),
            # Events
            RuleData("Defeated Balrog 3", lambda state, player: state.has(
                "Delivered Cure-All", player, 1) and can_kill_bosses(state, player))
        ]
    ),
    RegionData(
        "Boulder Chamber - Door to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Door to Boulder Chamber", trivial),
            RuleData("Boulder Chamber - Door to Labyrinth B", trivial)
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
            RuleData("Boulder Chamber - Door to Labyrinth B", trivial)
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
            RuleData("Boulder Chamber - Door to Labyrinth M", trivial),
            RuleData("Labyrinth M - Door to Dark Place", has_weapon)
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
            RuleData("Dark Place - Door to Labyrinth M", trivial),
            RuleData("Labyrinth M - Door to Boulder Chamber", lambda state,
                     player: state.has("Defeated Balrog 3", player, 1) and (has_weapon(state, player))),
            RuleData("Labyrinth M - Teleporter to Labyrinth Shop", has_weapon)
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
            RuleData("Labyrinth Shop - Teleporter to Labyrinth M", trivial),
            RuleData("Labyrinth M - Door to Dark Place", has_weapon)
        ],
        [
            # Locations
            # Events
            RuleData("Labyrinth M - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Dark Place - Door to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Door to Dark Place", trivial),
            RuleData("Dark Place - Door to Core", lambda state,
                     player: state.has("Defeated Balrog 3", player, 1)),
            RuleData("Dark Place - Exit to Waterway", lambda state,
                     player: state.has("Curly's Air Tank", player, 1)),
            RuleData("Dark Place - Save Point", trivial)
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
            RuleData("Core - Door to Dark Place", trivial),
            RuleData("Dark Place - Door to Labyrinth M", trivial)
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
            RuleData("Waterway - Entrance from Dark Place", trivial),
            RuleData("Dark Place - Door to Labyrinth M", trivial)
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
            RuleData("Reservoir - Debug Cat to Dark Place", trivial),
            RuleData("Dark Place - Door to Labyrinth M", trivial)
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
            RuleData("Dark Place - Door to Labyrinth M", trivial)
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
            RuleData("Dark Place - Door to Core", trivial),
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
            RuleData("Core - Robot's Arm", trivial),
            RuleData("Core - Drowned Curly", lambda state, player: state.has("Defeated Core", player, 1)),
            # Events
            RuleData("Defeated Core", can_kill_bosses),
            RuleData("Picked up Curly (Core)", lambda state,
                     player: state.has("Defeated Core", player, 1) and state.has("Tow Rope", player, 1))
        ]
    ),
    RegionData(
        "Waterway - Entrance from Dark Place",
        [
            # Regions
            RuleData("Dark Place - Exit to Waterway", trivial),
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
            RuleData("Main Artery - Entrance from Waterway", trivial)
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
            RuleData("Waterway Cabin - Door to Waterway", trivial),
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
            RuleData("Waterway - Door to Waterway Cabin", trivial),
            RuleData("Waterway Cabin - Bed", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Saved Curly", lambda state, player: state.has(
                "Picked up Curly (Core)", player, 1))
        ]
    ),
    RegionData(
        "Waterway Cabin - Save Point",
        [
            # Regions
            RuleData("Waterway Cabin - Door to Waterway", trivial),
            RuleData("Waterway Cabin - Bed", trivial)
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
            RuleData("Waterway Cabin - Save Point", trivial)
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
            RuleData("Waterway - Exit to Main Artery", trivial),
            RuleData("Main Artery - Exit to Reservoir", lambda state,
                     player: state.has("Defeated Ironhead", player, 1))
        ],
        [
            # Locations
            RuleData("Main Artery - Ironhead Boss", lambda state,
                     player: state.has("Defeated Ironhead", player, 1)),
            # Events
            RuleData("Defeated Ironhead", can_kill_bosses)
        ]
    ),
    RegionData(
        "Main Artery - Exit to Reservoir",
        [
            # Regions
            RuleData("Reservoir - Entrance from Main Artery", trivial)
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
            RuleData("Labyrinth H - Door to Labyrinth I", trivial),
            RuleData("Labyrinth I - Room Bottom", trivial)
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
            RuleData("Labyrinth I - Save Point", can_break_blocks)
        ],
        [
            # Locations
            RuleData("Labyrinth I - Critter Spot", has_weapon),
            # Events
            RuleData("Opened Labyrinth I Door", lambda state,
                     player: has_weapon(state, player)),
            RuleData("Used Labyrinth I Teleporter", trivial)
        ]
    ),
    RegionData(
        "Labyrinth I - Entrance from Sand Zone Storehouse",
        [
            # Regions
            RuleData("Sand Zone Storehouse - Exit to Labyrinth I", trivial),
            RuleData("Labyrinth I - Room Bottom", trivial)
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
            RuleData("Sand Zone - Teleporter to Labyrinth I", trivial),
            RuleData("Labyrinth I - Room Bottom", trivial)
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
            RuleData("Labyrinth I - Room Bottom", trivial)
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
            RuleData("Labyrinth I - Door to Labyrinth H", trivial),
            RuleData("Labyrinth H - Door to Labyrinth W", trivial)
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
            RuleData("Labyrinth W - Door to Labyrinth H", trivial),
            RuleData("Labyrinth H - Door to Labyrinth I", trivial)
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
            RuleData("Labyrinth H - Door to Labyrinth W", trivial),
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
            RuleData("Labyrinth Shop - Door to Labyrinth W", trivial),
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
            RuleData("Labyrinth W - Before Monster X", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Labyrinth W - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Camp (Lower)",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Lower)", trivial),
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
            RuleData("Camp - Door to Labyrinth W (Upper)", trivial),
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
            RuleData("Clinic Ruins - Door to Labyrinth W", trivial),
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
            RuleData("Labyrinth B - Door to Labyrinth W", trivial),
            RuleData("Labyrinth W - Before Monster X", trivial)
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
            RuleData("Defeated Monster X", can_kill_bosses)
        ]
    ),
    RegionData(
        "Labyrinth Shop - Door to Labyrinth W",
        [
            # Regions
            RuleData("Labyrinth W - Door to Labyrinth Shop", trivial),
            RuleData("Labyrinth Shop - Teleporter to Labyrinth M",
                     has_flight),
            RuleData("Labyrinth Shop - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Labyrinth Shop - Chaba Chest (Machine Gun)",
                     lambda state, player: state.has("Machine Gun", player, 1)),
            RuleData("Labyrinth Shop - Chaba Chest (Fireball)",
                     lambda state, player: state.has("Fireball", player, 1)),
            RuleData("Labyrinth Shop - Chaba Chest (Spur)",
                     lambda state, player: state.has("Progressive Polar Star", player, 2)),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth Shop - Teleporter to Labyrinth M",
        [
            # Regions
            RuleData("Labyrinth M - Teleporter to Labyrinth Shop", trivial),
            RuleData("Labyrinth Shop - Door to Labyrinth W", trivial)
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
            RuleData("Labyrinth Shop - Door to Labyrinth W", trivial)
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
            RuleData("Labyrinth W - Door to Camp (Lower)", trivial),
            RuleData("Camp - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Camp - Dr. Gero", trivial),
            # Events
            RuleData("Delivered Cure-All", lambda state,
                     player: state.has("Cure-All", player, 1))
        ]
    ),
    RegionData(
        "Camp - Door to Labyrinth W (Upper)",
        [
            # Regions
            RuleData("Labyrinth W - Door to Camp (Upper)", trivial)
        ],
        [
            # Locations
            RuleData("Camp - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Camp - Save Point",
        [
            # Regions
            RuleData("Camp - Door to Labyrinth W (Lower)", trivial)
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
            RuleData("Labyrinth W - Door to Clinic Ruins", trivial)
        ],
        [
            # Locations
            RuleData("Clinic Ruins - Puu Black Boss", trivial),
            # Events
            RuleData("Defeated Puu Black", can_kill_bosses),
        ]
    ),
    RegionData(
        "Final Cave - Door to Plantation",
        [
            # Regions
            RuleData("Plantation - Door to Final Cave", trivial),
            RuleData("Final Cave - Door to Balcony (Pre-Bosses)", has_weapon)
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
            RuleData("Balcony (Pre-Bosses) - Door to Final Cave", trivial),
            RuleData("Final Cave - Door to Plantation", has_weapon)
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
            RuleData("Plantation - Door to Last Cave (Hidden)", trivial),
            RuleData("Last Cave (Hidden) - Before Red Demon", lambda state,
                     player: state.has("Progressive Booster", player, 2) and has_weapon(state, player))
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
            RuleData("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)", trivial),
            RuleData("Last Cave (Hidden) - Before Red Demon", lambda state,
                     player: state.has("Progressive Booster", player, 2) and has_weapon(state, player))
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
            RuleData("Last Cave (Hidden) - Red Demon Boss", lambda state,
                     player: state.has("Defeated Red Demon", player, 1)),
            # Events
            RuleData("Defeated Red Demon", can_kill_bosses)
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Exit to Throne Room",
        [
            # Regions
            RuleData("Throne Room - Entrance from Balcony (Pre-Bosses)", trivial)
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
            RuleData("Final Cave - Door to Balcony (Pre-Bosses)", trivial),
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building", trivial)
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
            RuleData("Last Cave (Hidden) - Door to Balcony (Pre-Bosses)", trivial),
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building", trivial)
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
            RuleData("Prefab Building - Door to Balcony (Pre-Bosses)", trivial),
            RuleData("Balcony (Pre-Bosses) - Exit to Throne Room", lambda state,
                     player: state.has("Lowered Barrier", player, 1)),
            RuleData("Balcony (Pre-Bosses) - Door to Final Cave", lambda state,
                     player: state.has("Progressive Booster", player, 2)),
            RuleData("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)",
                     lambda state, player: state.has("Progressive Booster", player, 2))
        ],
        [
            # Locations
            # Events
            RuleData("Lowered Barrier", lambda state, player: (
                state.has("Saved Sue", player, 1) and (
                    False or (  # Normal Ending
                        state.has("Iron Bond", player, 1) and
                        state.has("Progressive Booster", player, 2) and (
                            True or (  # Best Ending
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
            RuleData("Balcony (Pre-Bosses) - Door to Prefab Building", trivial),
            RuleData("Prefab Building - Save Point/Bed", trivial)
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
            RuleData("Prefab Building - Door to Balcony (Pre-Bosses)", trivial)
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
            RuleData("Throne Room - H/V Trigger to The King's Table", lambda state,
                     player: state.has("Defeated Misery", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Misery", can_kill_bosses)
        ]
    ),
    RegionData(
        "Throne Room - Exit to Balcony (Post-Bosses)",
        [
            # Regions
            RuleData("Balcony (Post-Bosses) - Entrance from Throne Room", trivial)
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
            RuleData("The King's Table - H/V Trigger to Throne Room", trivial),
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
            RuleData("Throne Room - H/V Trigger to The King's Table", trivial),
            RuleData("The King's Table - H/V Trigger to Black Space", lambda state,
                     player: state.has("Defeated Doctor", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Doctor", can_kill_bosses)
        ]
    ),
    RegionData(
        "The King's Table - H/V Trigger to Black Space",
        [
            # Regions
            RuleData("Black Space - H/V Trigger to The King's Table", trivial),
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
            RuleData("The King's Table - H/V Trigger to Black Space", lambda state,
                     player: state.has("Defeated Undead Core", player, 1))
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Undead Core", can_kill_bosses)
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Entrance from Throne Room",
        [
            # Regions
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
            RuleData("Prefab House - Entrance from Balcony (Post-Bosses)", trivial)
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
            RuleData("Prefab House - Exit to Balcony (Post-Bosses)", trivial),
            RuleData("Balcony (Post-Bosses) - Entrance from Throne Room", trivial)
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
            RuleData("Balcony (Post-Bosses) - Exit to Prefab House", trivial),
            RuleData("Prefab House - Exit to Balcony (Post-Bosses)", trivial),
            RuleData("Prefab House - Exit to Sacred Grounds - B1",
                     lambda state, player: state.has("Used Ma Pignon", player, 1)),
            RuleData("Prefab House - Save Point", trivial)
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
            RuleData("Balcony (Post-Bosses) - Entrance from Prefab House", trivial)
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
            RuleData("Sacred Grounds - B1 - Entrance from Prefab House", trivial)
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
            RuleData("Prefab House - Entrance from Balcony (Post-Bosses)", trivial)
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
            RuleData("Prefab House - Exit to Sacred Grounds - B1", trivial),
            RuleData("Sacred Grounds - B1 - Door to Sacred Grounds - B2", lambda state, player: state.has(
                "Progressive Booster", player, 2) and state.has("Picked up Curly (Hell)", player, 1)),
        ],
        [
            # Locations
            RuleData("Sacred Grounds - B1 - Ledge", lambda state,
                     player: state.has("Progressive Booster", player, 2)),
            # Events
            RuleData("Picked up Curly (Hell)", lambda state,
                     player: state.has("Used Ma Pignon", player, 1))
        ]
    ),
    RegionData(
        "Sacred Grounds - B1 - Door to Sacred Grounds - B2",
        [
            # Regions
            RuleData("Sacred Grounds - B2 - Door to Sacred Grounds - B1", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B2 - Door to Sacred Grounds - B1",
        [
            # Regions
            RuleData("Sacred Grounds - B1 - Door to Sacred Grounds - B2", trivial),
            RuleData(
                "Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3", has_weapon)
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
            RuleData(
                "Sacred Grounds - B3 - H/V Trigger to Sacred Grounds - B2", trivial),
            RuleData(
                "Sacred Grounds - B2 - Door to Sacred Grounds - B1", has_weapon)
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
            RuleData("Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3", trivial),
            RuleData("Sacred Grounds - B3 - Exit to Passage?", lambda state, player: state.has("Defeated Heavy Press", player, 1))
        ],
        [
            # Locations
            RuleData("Sacred Grounds - B3 - Hidden Chest", lambda state,
                     player: has_flight(state, player) and can_break_blocks(state, player)),
            # Events
            RuleData("Defeated Heavy Press", lambda state, player: can_kill_bosses(
                state, player) and has_flight(state, player))
        ]
    ),
    RegionData(
        "Sacred Grounds - B3 - Exit to Passage?",
        [
            # Regions
            RuleData("Passage? - Entrance from Sacred Grounds - B3", trivial)
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
            RuleData("Passage? - Door to Corridor", trivial),
            RuleData("Corridor - Exit to Seal Chamber", trivial)
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
            RuleData("Seal Chamber - Entrance from Corridor", trivial),
            RuleData("Corridor - Door to Passage?", trivial)
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
            RuleData("Corridor - Exit to Seal Chamber", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Best Ending", can_kill_bosses)
        ]
    ),
    RegionData(
        "Start Point - Door to First Cave",
        [
            # Regions
            RuleData("First Cave - Door to Start Point", trivial),
            RuleData("Start Point - Save Point", trivial)
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
            RuleData("Start Point - Door to First Cave", trivial),
            RuleData("Start Point - Refill", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Start Point - Refill",
        [
            # Regions
            RuleData("Start Point - Save Point", trivial)
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
            RuleData("Start Point - Door to First Cave", trivial),
            RuleData("First Cave - Door to Hermit Gunsmith", trivial),
            RuleData("First Cave - Door to Mimiga Village", lambda state, player: can_break_blocks(state, player))
        ],
        [
            # Locations
            RuleData("First Cave - West Ledge", trivial),
            # Events
        ]
    ),
    RegionData(
        "First Cave - Door to Hermit Gunsmith",
        [
            # Regions
            RuleData("Hermit Gunsmith - Door to First Cave", trivial),
            RuleData("First Cave - Door to Start Point", trivial)
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
            RuleData("Mimiga Village - Door to First Cave", trivial),
            RuleData("First Cave - Door to Start Point", can_break_blocks)
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
            RuleData("First Cave - Door to Hermit Gunsmith", trivial)
        ],
        [
            # Locations
            RuleData("Hermit Gunsmith - Chest", trivial),
            RuleData("Hermit Gunsmith - Tetsuzou", lambda state, player: state.has(
                "Progressive Polar Star", player, 1) and state.has("Defeated Core", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to First Cave",
        [
            # Regions
            RuleData("First Cave - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
                     has_flight),
            RuleData("Mimiga Village - Door to Save Point", trivial),
            RuleData("Mimiga Village - Door to Reservoir", trivial),
            RuleData("Mimiga Village - Door to Yamashita Farm", trivial),
            RuleData("Mimiga Village - Door to Assembly Hall", trivial),
            RuleData("Mimiga Village - Door to Graveyard", lambda state,
                     player: state.has("Toroko Kidnapped", player, 1)),
            RuleData("Mimiga Village - Door to Shack", trivial),
            RuleData("Mimiga Village - Door to Arthur's House", lambda state,
                     player: state.has("Arthur's Key", player, 1))
        ],
        [
            # Locations
            RuleData("Mimiga Village - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Save Point",
        [
            # Regions
            RuleData("Mimiga Village Save Point - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Reservoir - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Yamashita Farm - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Assembly Hall - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Graveyard - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Shack - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
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
            RuleData("Arthur's House - Door to Mimiga Village", trivial),
            RuleData("Mimiga Village - Room Centre", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village Save Point - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Save Point", trivial),
            RuleData("Mimiga Village Save Point - Save Point", trivial),
            RuleData("Mimiga Village Save Point - Refill", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village Save Point - Save Point",
        [
            # Regions
            RuleData("Mimiga Village Save Point - Door to Mimiga Village", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village Save Point - Refill",
        [
            # Regions
            RuleData("Mimiga Village Save Point - Door to Mimiga Village", trivial)
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
            RuleData("Mimiga Village - Door to Yamashita Farm", trivial)
        ],
        [
            # Locations
            RuleData("Yamashita Farm - Pool", trivial),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Reservoir", trivial),
            RuleData("Reservoir - Debug Cat to Dark Place", lambda state,
                     player: state.has("Defeated Ironhead", player, 1))
        ],
        [
            # Locations
            RuleData("Reservoir - Fishing Spot", trivial),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Debug Cat to Dark Place",
        [
            # Regions
            RuleData("Dark Place - Entrance from Reservoir", trivial),
            RuleData("Reservoir - Door to Mimiga Village", trivial)
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
            RuleData("Main Artery - Exit to Reservoir", trivial),
            RuleData("Reservoir - Door to Mimiga Village", trivial)
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
            RuleData("Mimiga Village - Door to Assembly Hall", trivial)
        ],
        [
            # Locations
            RuleData("Assembly Hall - Fireplace", lambda state,
                     player: state.has("Jellyfish Juice", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Graveyard", trivial),
            RuleData("Graveyard - Door to Storage?", lambda state,
                     player: has_flight(state, player))
        ],
        [
            # Locations
            RuleData("Graveyard - Arthur's Grave", trivial),
            RuleData("Graveyard - Mr. Little", trivial),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Storage?",
        [
            # Regions
            RuleData("Storage? - Door to Graveyard", trivial),
            RuleData("Graveyard - Door to Mimiga Village", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Storage? - Door to Graveyard",
        [
            # Regions
            RuleData("Graveyard - Door to Storage?", trivial)
        ],
        [
            # Locations
            RuleData("Storage? - Chest", lambda state,
                     player: state.has("Saved Curly", player, 1)),
            RuleData("Storage? - Ma Pignon Boss", lambda state,
                     player: state.has("Defeated Ma Pignon", player, 1)),
            # Events
            RuleData("Defeated Ma Pignon", lambda state, player: state.has("Mushroom Badge", player, 1) and (
                state.has("Polar Star", player, 1) or
                state.has("Machine Gun", player, 1) or
                state.has("Bubbler", player, 1) or
                state.has("Fireball", player, 1) or
                state.has("Snake", player, 1) or
                state.has("Nemesis", player, 1)
            ))
        ]
    ),
    RegionData(
        "Shack - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Shack", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Toroko Kidnapped", lambda state, player: state.has(
                "Silver Locket", player, 1) and has_weapon(state, player)),
            RuleData("Defeated Balrog 1", lambda state, player: state.has(
                "Toroko Kidnapped", player, 1) and can_kill_bosses(state, player)),
            RuleData("Shack - Level MG", lambda state, player: state.has("Machine Gun",
                                                                             player, 1) and state.has("Defeated Balrog 1", player, 1))
        ]
    ),
    RegionData(
        "Arthur's House - Door to Mimiga Village",
        [
            # Regions
            RuleData("Mimiga Village - Door to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Arthur's House - Save Point", trivial),
            RuleData("Arthur's House - Teleporter to Egg Corridor", trivial),
            RuleData("Arthur's House - Teleporter to Grasstown", trivial),
            RuleData("Arthur's House - Teleporter to Sand Zone", trivial),
            RuleData("Arthur's House - Teleporter to Labyrinth B", trivial),
            RuleData("Arthur's House - Teleporter to Teleporter", trivial),
            RuleData("Arthur's House - Teleporter to Egg Corridor?", lambda state, player: state.has(
                "Defeated Core", player, 1) or state.has("Used Egg Corridor? Teleporter", player, 1))
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
            RuleData("Arthur's House - Main Teleporter", trivial),
            RuleData("Arthur's House - Refill", trivial)
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
            RuleData("Egg Corridor - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Grasstown - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Sand Zone - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Labyrinth B - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Teleporter - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
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
            RuleData("Egg Corridor? - Teleporter to Arthur's House", trivial),
            RuleData("Arthur's House - Main Teleporter", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Refill",
        [
            # Regions
            RuleData("Arthur's House - Save Point", trivial)
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
            RuleData("Rest Area - Door to Plantation", trivial),
            RuleData("Plantation - Middle Level", trivial)
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
            RuleData("Teleporter - Door to Plantation", trivial),
            RuleData("Plantation - Lower Level", trivial)
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
            RuleData("Storehouse - Door to Plantation", trivial),
            RuleData("Plantation - Middle Level", trivial)
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
            RuleData("Jail No. 1 - Door to Plantation (Lower)", trivial),
            RuleData("Plantation - Upper Level", trivial)
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
            RuleData("Jail No. 1 - Door to Plantation (Upper)", trivial),
            RuleData("Plantation - Upper Level", trivial)
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
            RuleData("Jail No. 2 - Door to Plantation", trivial),
            RuleData("Plantation - Upper Level", trivial)
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
            RuleData("Last Cave (Hidden) - Door to Plantation", trivial),
            RuleData("Plantation - Top Level", trivial)
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
            RuleData("Passage? - Door to Plantation", trivial),
            RuleData("Plantation - Middle Level", trivial)
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
            RuleData("Hideout - Door to Plantation", trivial),
            RuleData("Plantation - Middle Level", trivial)
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
            RuleData("Plantation - Middle Level", trivial)
        ],
        [
            # Locations
            RuleData("Plantation - Kanpachi's Bucket", trivial),
            RuleData("Plantation - Curly", lambda state,
                     player: state.has("Used Ma Pignon", player, 1)),
            # Events
            RuleData("Plantation - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1)),
            RuleData("Used Ma Pignon", lambda state,
                     player: state.has("Saved Curly", player, 1) and state.has("Ma Pignon", player, 1))
        ]
    ),
    RegionData(
        "Plantation - Middle Level",
        [
            # Regions
            RuleData("Plantation - Door to Rest Area", trivial),
            RuleData("Plantation - Door to Storehouse", trivial),
            RuleData("Plantation - Door to Passage?", trivial),
            RuleData("Plantation - Door to Hideout", lambda state,
                     player: state.has("Sue's Letter", player, 1)),
            RuleData("Plantation - Lower Level", trivial),
            RuleData("Plantation - Upper Level", trivial),
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
            RuleData("Plantation - Door to Jail No. 1 (Lower)", trivial),
            RuleData("Plantation - Door to Jail No. 1 (Upper)",
                     has_flight),
            RuleData("Plantation - Door to Jail No. 2", trivial),
            RuleData("Plantation - Middle Level", trivial),
        ],
        [
            # Locations
            RuleData("Plantation - Platforming Spot",
                     has_flight),
            RuleData("Plantation - Puppy", lambda state,
                     player: state.has("Built Rocket", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Final Cave",
        [
            # Regions
            RuleData("Final Cave - Door to Plantation", trivial),
            RuleData("Plantation - Top Level", trivial)
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
                "Progressive Booster", player, 2) and (state.has("Built Rocket", player, 1))),
            RuleData("Plantation - Upper Level", trivial),
            RuleData("Plantation - Door to Final Cave", lambda state, player: state.has(
                "Progressive Booster", player, 1) and (state.has("Built Rocket", player, 1)))
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
            RuleData("Plantation - Door to Storehouse", trivial),
            RuleData("Storehouse - Door to Outer Wall", trivial)
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
            RuleData("Outer Wall - Door to Storehouse", trivial),
            RuleData("Storehouse - Door to Plantation", trivial),
            RuleData("Storehouse - Save Point", trivial)
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
            RuleData("Storehouse - Door to Outer Wall", trivial)
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
            RuleData("Plantation - Door to Passage?", trivial),
            RuleData("Passage? - Door to Statue Chamber", trivial)
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
            RuleData("Statue Chamber - Door to Passage?", trivial),
            RuleData("Passage? - Door to Plantation", trivial),
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
            RuleData("Corridor - Door to Passage?", trivial),
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
            RuleData("Passage? - Door to Corridor", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Passage? from above", trivial)
        ]
    ),
    RegionData(
        "Statue Chamber - Door to Passage?",
        [
            # Regions
            RuleData("Passage? - Door to Statue Chamber", trivial)
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
            RuleData("Plantation - Door to Rest Area", trivial),
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
            RuleData("Rest Area - Door to Plantation", trivial)
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
            RuleData("Plantation - Door to Teleporter", trivial),
            RuleData("Teleporter - Room Hub", trivial)
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
            RuleData("Arthur's House - Teleporter to Teleporter", trivial),
            RuleData("Teleporter - Room Hub", trivial)
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
            RuleData("Jail No. 1 - Entrance from Teleporter", trivial)
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
            RuleData("Plantation - Door to Jail No. 1 (Upper)", trivial)
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
            RuleData("Teleporter - Exit to Jail No. 1", trivial),
            RuleData("Jail No. 1 - Door to Plantation (Upper)", trivial),
            RuleData("Jail No. 1 - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Jail No. 1 - Sue's Gift", trivial),
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Door to Plantation (Lower)",
        [
            # Regions
            RuleData("Plantation - Door to Jail No. 1 (Lower)", trivial)
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
            RuleData("Jail No. 1 - Entrance from Teleporter", trivial)
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
            RuleData("Plantation - Door to Jail No. 2", trivial),
            RuleData("Jail No. 2 - Teleporter to Shelter", can_break_blocks)
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
            RuleData("Shelter - Teleporter to Jail No. 2", trivial),
            RuleData("Jail No. 2 - Door to Plantation", can_break_blocks)
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
            RuleData("Plantation - Door to Hideout", trivial),
            RuleData("Hideout - Bed", trivial)
        ],
        [
            # Locations
            RuleData("Hideout - Momorin", lambda state,
                     player: state.has("Progressive Booster", player, 1)),
            # Events
            RuleData("Built Rocket", lambda state, player: (state.has("Progressive Booster", player, 1) or state.has(
                "Progressive Booster", player, 2)) and state.has("Sprinkler", player, 1) and state.has("Controller", player, 1))
        ]
    ),
    RegionData(
        "Hideout - Bed",
        [
            # Regions
            RuleData("Hideout - Door to Plantation", trivial),
            RuleData("Hideout - Save Point", trivial)
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
            RuleData("Hideout - Bed", trivial)
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
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Upper)", trivial),
            RuleData("Egg Corridor? - Area Centre", trivial)
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
            RuleData("Cthulhu's Abode? - Door to Egg Corridor? (Lower)", trivial),
            RuleData("Egg Corridor? - West Side", trivial)
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
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Lower)", trivial)
        ],
        [
            # Locations
            RuleData("Egg Corridor? - Dragon Chest", lambda state,
                     player: has_weapon(state, player)),
            # Events
            RuleData("Used Egg Corridor? Teleporter", trivial),
            RuleData("Egg Corridor? (West) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - Area Centre",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Upper)", trivial),
            RuleData(
                "Egg Corridor? - Door to Egg Observation Room? (West)", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Egg Corridor? (Centre) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - East Side",
        [
            # Regions
            RuleData(
                "Egg Corridor? - Door to Egg Observation Room? (East)", has_weapon),
            RuleData("Egg Corridor? - Door to Egg No. 00", trivial),
            RuleData("Egg Corridor? - Door to Side Room?", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Egg Corridor? (East) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Egg Observation Room? (West)",
        [
            # Regions
            RuleData(
                "Egg Observation Room? - Door to Egg Corridor? (Western)", trivial),
            RuleData("Egg Corridor? - Area Centre", trivial)
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
            RuleData(
                "Egg Observation Room? - Door to Egg Corridor? (Eastern)", trivial),
            RuleData("Egg Corridor? - East Side", trivial)
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
            RuleData("Egg No. 00 - Door to Egg Corridor?", trivial),
            RuleData("Egg Corridor? - East Side", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Side Room?",
        [
            # Regions
            RuleData("Side Room? - Door to Egg Corridor?", trivial),
            RuleData("Egg Corridor? - East Side", trivial)
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
            RuleData("Arthur's House - Teleporter to Egg Corridor?", trivial),
            RuleData("Egg Corridor? - West Side", trivial)
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
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Upper)", trivial),
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
            RuleData("Egg Corridor? - Door to Cthulhu's Abode? (Lower)", trivial),
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
            RuleData(
                "Egg Corridor? - Door to Egg Observation Room? (West)", trivial),
            RuleData(
                "Egg Observation Room? - Door to Egg Corridor? (Eastern)", trivial)
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
            RuleData(
                "Egg Corridor? - Door to Egg Observation Room? (East)", trivial),
            RuleData("Egg Observation Room? - Door to Egg Corridor? (Western)", lambda state,
                     player: state.has("Defeated Sisters", player, 1) or has_flight(state, player)),
            RuleData("Egg Observation Room? - Save Point", lambda state,
                     player: state.has("Defeated Sisters", player, 1))
        ],
        [
            # Locations
            RuleData("Egg Observation Room? - Sisters Boss", lambda state,
                     player: state.has("Defeated Sisters", player, 1)),
            # Events
            RuleData("Defeated Sisters", can_kill_bosses)
        ]
    ),
    RegionData(
        "Egg Observation Room? - Save Point",
        [
            # Regions
            RuleData(
                "Egg Observation Room? - Door to Egg Corridor? (Eastern)", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room? - Door to Egg Corridor?",
        [
            # Regions
            RuleData("Egg Corridor? - Door to Side Room?", trivial),
            RuleData("Side Room? - Save Point", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room? - Save Point",
        [
            # Regions
            RuleData("Side Room? - Door to Egg Corridor?", trivial),
            RuleData("Side Room? - Refill", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
    RegionData(
        "Side Room? - Refill",
        [
            # Regions
            RuleData("Side Room? - Save Point", trivial)
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
            RuleData("Egg Corridor? - Door to Egg No. 00", trivial),
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
            RuleData("Outer Wall - Door to Egg No. 00", trivial),
            RuleData("Egg No. 00 - Door to Egg Corridor?", trivial)
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
            RuleData("Egg No. 00 - Door to Outer Wall", trivial),
            RuleData("Outer Wall - Room Bottom", trivial)
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
            RuleData("Little House - Door to Outer Wall", trivial),
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
            RuleData("Outer Wall - Room Bottom", trivial),
            RuleData("Outer Wall - Room Top", lambda state,
                     player: has_weapon(state, player)),
            RuleData("Outer Wall - Door to Clock Room", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Outer Wall - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Outer Wall - Door to Storehouse",
        [
            # Regions
            RuleData("Storehouse - Door to Outer Wall", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Outer Wall from Storehouse", trivial)
        ]
    ),
    RegionData(
        "Outer Wall - Room Bottom",
        [
            # Regions
            RuleData("Outer Wall - Door to Egg No. 00", lambda state,
                     player: state.has("Saved Kazuma", player, 1) or state.has("Entered Outer Wall from Clock Room", player, 1) or state.has("Entered Outer Wall from Storehouse", player, 1)),
            RuleData("Outer Wall - Door to Little House",
                     has_flight),
            RuleData("Outer Wall - Outside Clock Room", lambda state, player: has_flight(state, player)
                     or (remove_points_of_no_return(state, player) and state.has("Entered Outer Wall from Clock Room", player, 1)))
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
            RuleData("Outer Wall - Outside Clock Room", trivial),
            RuleData("Outer Wall - Door to Storehouse", trivial)
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
            RuleData("Clock Room - Door to Outer Wall", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Entered Outer Wall from Clock Room", trivial)
        ]
    ),
    RegionData(
        "Little House - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Little House", trivial)
        ],
        [
            # Locations
            RuleData("Little House - Mr. Little", lambda state,
                     player: state.has("Blade", player, 1) and state.has("Little Man", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Clock Room - Door to Outer Wall",
        [
            # Regions
            RuleData("Outer Wall - Door to Clock Room", trivial)
        ],
        [
            # Locations
            RuleData("Clock Room - Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Door to Jenka's House",
        [
            # Regions
            RuleData("Jenka's House - Door to Sand Zone", trivial),
            RuleData("Sand Zone - Outside Jenka's House", trivial)
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
            RuleData("Arthur's House - Teleporter to Sand Zone", trivial),
            RuleData("Sand Zone - Outside Sand Zone Residence", can_break_blocks)
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
                     can_break_blocks),
            RuleData("Sand Zone - Door to Sand Zone Residence", trivial),
            RuleData("Sand Zone - Above Sunstones", can_break_blocks)
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
            RuleData("Sand Zone Residence - Door to Sand Zone", trivial),
            RuleData("Sand Zone - Outside Sand Zone Residence", trivial)
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
            RuleData("Sand Zone - Door to Deserted House", trivial),
            RuleData("Sand Zone - Outside Jenka's House", can_break_blocks),
            RuleData("Sand Zone - Outside Sand Zone Storehouse",
                     has_flight)
        ],
        [
            # Locations
            RuleData("Sand Zone - Running Puppy", trivial),
            # Events
            RuleData("Sand Zone (Lower) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Sand Zone - Door to Deserted House",
        [
            # Regions
            RuleData("Deserted House - Door to Sand Zone", trivial),
            RuleData("Sand Zone - Lower Side", trivial)
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
            RuleData("Sand Zone Storehouse - Entrance from Sand Zone", trivial)
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
                     can_break_blocks),
            RuleData("Sand Zone - Before Omega", can_break_blocks),
            RuleData("Sand Zone - Outside Jenka's House", lambda state, player: state.has(
                "Defeated Omega", player, 1) and can_break_blocks(state, player)),
            RuleData("Sand Zone - Pawprint Spot", lambda state, player: state.has("Defeated Omega",
                                                                                  player, 1) and can_break_blocks(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Polish Spot", can_break_blocks),
            # Events
            RuleData("Sand Zone (Upper) - Level MG", lambda state,
                     player: state.has("Machine Gun", player, 1))
        ]
    ),
    RegionData(
        "Sand Zone - Before Omega",
        [
            # Regions
            RuleData("Sand Zone - Above Sunstones", can_break_blocks),
            RuleData("Sand Zone - Refill (Upper)", trivial)
        ],
        [
            # Locations
            # Events
            RuleData("Defeated Omega", can_break_blocks)
        ]
    ),
    RegionData(
        "Sand Zone - Outside Jenka's House",
        [
            # Regions
            RuleData("Sand Zone - Door to Jenka's House", trivial),
            RuleData("Sand Zone - Lower Side", can_break_blocks),
            RuleData("Sand Zone - Above Sunstones", lambda state, player: can_break_blocks(state,
                                                                                           player) and state.has("Defeated Omega", player, 1)),
            RuleData("Sand Zone - Pawprint Spot", can_break_blocks)
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
            RuleData("Sand Zone - Outside Jenka's House", can_break_blocks)
        ],
        [
            # Locations
            RuleData("Sand Zone - Pawprint Spot", trivial),
            RuleData("Sand Zone - Pawprint Chest", trivial),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Refill (Upper)",
        [
            # Regions
            RuleData("Sand Zone - Before Omega", trivial),
            RuleData("Sand Zone - Save Point (Upper)", trivial)
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
            RuleData("Sand Zone - Outside Sand Zone Storehouse", trivial),
            RuleData("Sand Zone - Save Point (Lower)", trivial)
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
            RuleData("Labyrinth I - Teleporter to Sand Zone", trivial),
            RuleData("Sand Zone - Outside Sand Zone Storehouse", trivial)
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
            RuleData("Sand Zone - Refill (Lower)", can_break_blocks),
            RuleData("Sand Zone - Teleporter to Labyrinth I", lambda state, player: state.has(
                "Used Labyrinth I Teleporter", player, 1) and remove_points_of_no_return(state, player))
        ],
        [
            # Locations
            RuleData("Sand Zone - Outside Warehouse", trivial),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Save Point (Lower)",
        [
            # Regions
            RuleData("Sand Zone - Refill (Lower)", trivial)
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
            RuleData("Sand Zone - Refill (Upper)", trivial)
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
            RuleData("Sand Zone - Door to Sand Zone Residence", trivial),
            RuleData("Sand Zone Residence - Door to Small Room", lambda state,
                     player: state.has("Defeated Curly", player, 1)),
            RuleData("Sand Zone Residence - Before Curly", trivial)
        ],
        [
            # Locations
            RuleData("Sand Zone Residence - Curly Boss", lambda state, player: state.has("Defeated Curly",
                                                                                         player, 1) and state.has("Progressive Polar Star", player, 1)),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Residence - Door to Small Room",
        [
            # Regions
            RuleData("Small Room - Door to Sand Zone Residence", trivial),
            RuleData("Sand Zone Residence - Door to Sand Zone", lambda state,
                     player: state.has("Defeated Curly", player, 1)),
            RuleData("Sand Zone Residence - Before Curly", trivial)
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
            RuleData("Defeated Curly", can_kill_bosses)
        ]
    ),
    RegionData(
        "Small Room - Door to Sand Zone Residence",
        [
            # Regions
            RuleData("Sand Zone Residence - Door to Small Room", trivial),
            RuleData("Small Room - Refill", trivial)
        ],
        [
            # Locations
            RuleData("Small Room - Beside Bed", trivial),
            RuleData("Small Room - Curly's Closet", trivial),
            # Events
        ]
    ),
    RegionData(
        "Small Room - Refill",
        [
            # Regions
            RuleData("Small Room - Door to Sand Zone Residence", trivial),
            RuleData("Small Room - Save Point", trivial)
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
            RuleData("Small Room - Refill", trivial)
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
            RuleData("Sand Zone - Door to Jenka's House", trivial),
            RuleData("Jenka's House - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Jenka's House - Jenka", lambda state,
                     player: state.has("Returned Puppies", player, 1)),
            # Events
            RuleData("Returned Puppies", lambda state,
                     player: state.has("Puppy", player, 5))
        ]
    ),
    RegionData(
        "Jenka's House - Save Point",
        [
            # Regions
            RuleData("Jenka's House - Door to Sand Zone", trivial)
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
            RuleData("Sand Zone - Door to Deserted House", trivial),
            RuleData("Deserted House - Save Point", trivial)
        ],
        [
            # Locations
            RuleData("Deserted House - Attic", trivial),
            # Events
        ]
    ),
    RegionData(
        "Deserted House - Save Point",
        [
            # Regions
            RuleData("Deserted House - Door to Sand Zone", trivial)
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
            RuleData("Sand Zone - Exit to Sand Zone Storehouse", trivial),
            RuleData("Sand Zone Storehouse - Before Toroko+", trivial),
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
            RuleData("Sand Zone Storehouse - King", lambda state,
                     player: state.has("Defeated Toroko+", player, 1)),
            # Events
            RuleData("Defeated Toroko+", can_kill_bosses)
        ]
    ),
    RegionData(
        "Sand Zone Storehouse - Exit to Labyrinth I",
        [
            # Regions
            RuleData("Labyrinth I - Entrance from Sand Zone Storehouse", trivial)
        ],
        [
            # Locations
            # Events
        ]
    ),
]
