from typing import List, Dict, Tuple, Callable, Optional

from BaseClasses import CollectionState


class RegionData:
    name: str
    exits: List[Dict[str, Optional[Callable[[CollectionState, int], bool]]]]
    locations: List[Tuple[str,
                          Optional[Callable[[CollectionState, int], bool]]]]

    def __init__(
        self,
        name: str, exits: List[Tuple[str, Optional[Callable[[CollectionState, int], bool]]]],
        locations: List[Tuple[str,
                              Optional[Callable[[CollectionState, int], bool]]]]
    ):
        self.name = name
        self.exits = exits
        self.locations = locations


def has_flight(state: CollectionState, player: int):
    return state.has("Progressive Booster", player) or state.has_all({"Machine Gun", "Level MG"})


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
    return False


REGIONS: List[RegionData] = [
    RegionData(
        "Egg Corridor - Door to Cthulhu's Abode (Lower)",
        [
            # Regions
            ("Cthulhu's Abode - Door to Egg Corridor (Lower)", lambda state, player: True),
            ("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: True)
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
            ("Cthulhu's Abode - Door to Egg Corridor (Upper)", lambda state, player: True),
            ("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: True)
        ],
        [
            # Locations
            ("Egg Corridor - Cthulhu's Abode", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Corridor - Teleporter to Arthur's House",
        [
            # Regions
            ("Arthur's House - Teleporter to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1")))
        ],
        [
            # Locations
            ("Egg Corridor - Basil Spot", lambda state, player: True),
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg Corridor - Outside Cthulhu's Abode",
        [
            # Regions
            ("Egg Corridor - Door to Cthulhu's Abode (Lower)", lambda state, player: True),
            ("Egg Corridor - Door to Cthulhu's Abode (Upper)", lambda state, player: has_flight(state, player) or (state.has("tricks;Dboost;1") and state.has("damage;Damage;2"))),
            ("Egg Corridor - Teleporter to Arthur's House", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1"))),
            ("Egg Corridor - Outside Egg Observation Room", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1")))
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
            ("Egg Corridor - Outside Cthulhu's Abode", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1"))),
            ("Egg Corridor - H/V Trigger to Egg No. 06", lambda state, player: True),
            ("Egg Corridor - Door to Egg Observation Room", lambda state, player: True),
            ("Egg Corridor - H/V Trigger to Egg No. 01", lambda state, player: True),
            ("Egg Corridor - Outside Egg No. 00", lambda state, player: True)
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
            ("Egg No. 06 - Door to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
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
            ("Egg Observation Room - Door to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
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
            ("Egg No. 01 - Door to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Outside Egg Observation Room", lambda state, player: True)
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
            ("Egg Corridor - Outside Egg Observation Room", lambda state, player: True),
            ("Egg Corridor - Door to Egg No. 00", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Igor", lambda state, player: can_kill_bosses(state, player) or (state.has("items;supers;1") and state.has("tricks;BossMissiles;1") and state.has("items;missile;8")) or (state.has("items;missiles;1") and state.has("items;missile;18") and state.has("tricks;BossMissiles;2")))
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Egg No. 00",
        [
            # Regions
            ("Egg No. 00 - Door to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Outside Egg No. 00", lambda state, player: True),
            ("Egg Corridor - Door to Side Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Igor", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg Corridor - Door to Side Room",
        [
            # Regions
            ("Side Room - Door to Egg Corridor", lambda state, player: True),
            ("Egg Corridor - Door to Egg No. 00", lambda state, player: True)
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
            ("Egg Corridor - Door to Cthulhu's Abode (Lower)", lambda state, player: True),
            ("Cthulhu's Abode - Door to Egg Corridor (Upper)", lambda state, player: True),
            ("Cthulhu's Abode - Save Point", lambda state, player: True)
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
            ("Egg Corridor - Door to Cthulhu's Abode (Upper)", lambda state, player: True),
            ("Cthulhu's Abode - Door to Egg Corridor (Lower)", lambda state, player: True)
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
            ("Cthulhu's Abode - Door to Egg Corridor (Lower)", lambda state, player: True)
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
            ("Egg Corridor - H/V Trigger to Egg No. 06", lambda state, player: True)
        ],
        [
            # Locations
            ("Egg No. 06 - Egg Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room - Door to Egg Corridor",
        [
            # Regions
            ("Egg Corridor - Door to Egg Observation Room", lambda state, player: True)
        ],
        [
            # Locations
            ("Egg Observation Room - Egg Observation Room Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg No. 01 - Door to Egg Corridor",
        [
            # Regions
            ("Egg Corridor - H/V Trigger to Egg No. 01", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Lowered Egg Corridor Barrier", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg No. 00 - Door to Egg Corridor",
        [
            # Regions
            ("Egg Corridor - Door to Egg No. 00", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Saved Sue", lambda state, player: True)
        ]
    ),
    RegionData(
        "Side Room - Door to Egg Corridor",
        [
            # Regions
            ("Egg Corridor - Door to Side Room", lambda state, player: True),
            ("Side Room - Save Point", lambda state, player: True)
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
            ("Side Room - Door to Egg Corridor", lambda state, player: True),
            ("Side Room - Refill", lambda state, player: True)
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
            ("Side Room - Save Point", lambda state, player: True)
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
            ("Santa's House - Door to Grasstown", lambda state, player: True),
            ("Grasstown - West Side", lambda state, player: True)
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
            ("Chaco's House - Door to Grasstown", lambda state, player: True),
            ("Grasstown - West Side", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1") and has_flight(state, player)) or state.has("tricks;pacifist;2"))
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
            ("Chaco's House - Exit to Grasstown", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Entered Grasstown from Chaco Fireplace", lambda state, player: True)
        ]
    ),
    RegionData(
        "Grasstown - Door to Power Room",
        [
            # Regions
            ("Power Room - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Save Point - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Grasstown Hut - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Shelter - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Execution Chamber - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Gum - Door to Grasstown", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: True)
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
            ("Grasstown - Door to Santa's House", lambda state, player: True),
            ("Grasstown - Door to Chaco's House", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1") and has_flight(state, player)) or state.has("tricks;pacifist;2")),
            ("Grasstown - Area Centre", lambda state, player: has_flight(state, player) or state.has("events;eventFans;1") or (state.has("tricks;IframeReset;1") and ((state.has("tricks;Dboost;1") and state.has("damage;Damage;6")) or (state.has("tricks;Dboost;2") and state.has("damage;Damage;4")) or (state.has("tricks;Dboost;3") and state.has("damage;Damage;2") and has_weapon(state, player))) and reset_iframes(state, player) and (has_weapon(state, player) or (state.has("tricks;pacifist;1") and state.has("damage;Damage;5")) or state.has("tricks;pacifist;2")))),
            ("Grasstown - Teleporter to Arthur's House", lambda state, player: True)
        ],
        [
            # Locations
            ("Grasstown - West Grasstown Floor", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1"))),
            ("Grasstown - West Grasstown Ceiling", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1"))),
            ("Grasstown - Kulala", lambda state, player: has_weapon(state, player) and state.has("events;eventJellies;1")),
            # Events
            ("Return Santa's Key", lambda state, player: True),
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Grasstown - East Side",
        [
            # Regions
            ("Grasstown - Door to Power Room", lambda state, player: True),
            ("Grasstown - Door to Save Point", lambda state, player: True),
            ("Grasstown - Door to Grasstown Hut", lambda state, player: has_flight(state, player) or state.has("events;eventFans;1") or (state.has("tricks;Dboost;2") and state.has("tricks;IframeReset;1") and state.has("damage;Damage;4") and reset_iframes(state, player))),
            ("Grasstown - Door to Shelter", lambda state, player: True),
            ("Grasstown - Door to Execution Chamber", lambda state, player: True),
            ("Grasstown - Door to Gum", lambda state, player: state.has("items;gumKey;1") and (has_flight(state, player) or state.has("events;eventFans;1"))),
            ("Grasstown - Area Centre", lambda state, player: (state.has("events;eventFans;1") or has_flight(state, player) or (remove_points_of_no_return(state, player) and state.has("events;eventFireplace;1")) or ((state.has("tricks;GravHop;5")) or (state.has("tricks;Dboost;3") and state.has("damage;Damage;2")) or (state.has("tricks;Dboost;2") and state.has("damage;Damage;3")))) and (has_weapon(state, player) or (state.has("tricks;pacifist;2") and ((state.has("tricks;Dboost;1") and state.has("damage;Damage;3")) or has_flight(state, player))) or (state.has("tricks;pacifist;3") and state.has("tricks;GravHop;3"))))
        ],
        [
            # Locations
            ("Grasstown - Grasstown East Chest", lambda state, player: True),
            ("Grasstown - Kazuma Crack", lambda state, player: True),
            ("Grasstown - Kazuma Chest", lambda state, player: True),
            # Events
            ("Saved Kazuma", lambda state, player: True),
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Grasstown - Area Centre",
        [
            # Regions
            ("Grasstown - West Side", lambda state, player: True),
            ("Grasstown - East Side", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;2") and (has_flight(state, player) or (state.has("damage;Damage;3") and state.has("tricks;Dboost;1")))) or (state.has("tricks;pacifist;3") and state.has("tricks;GravHop;3")))
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
            ("Arthur's House - Teleporter to Grasstown", lambda state, player: True),
            ("Grasstown - West Side", lambda state, player: True)
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
            ("Grasstown - Door to Santa's House", lambda state, player: True),
            ("Santa's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Santa's House - Santa", lambda state, player: True),
            ("Santa's House - Santa's Fireplace", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Santa's House - Save Point",
        [
            # Regions
            ("Santa's House - Door to Grasstown", lambda state, player: True),
            ("Santa's House - Refill", lambda state, player: True)
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
            ("Santa's House - Save Point", lambda state, player: True)
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
            ("Grasstown - Door to Chaco's House", lambda state, player: True),
            ("Chaco's House - Exit to Grasstown", lambda state, player: True),
            ("Chaco's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Chaco's House - Chaco's Bed, where you two Had A Nap", lambda state, player: True),
            # Events
            ("Summon Jellies", lambda state, player: True)
        ]
    ),
    RegionData(
        "Chaco's House - Exit to Grasstown",
        [
            # Regions
            ("Grasstown - Entrance from Chaco's House", lambda state, player: True)
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
            ("Chaco's House - Door to Grasstown", lambda state, player: True),
            ("Chaco's House - Bed", lambda state, player: True)
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
            ("Chaco's House - Save Point", lambda state, player: True)
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
            ("Grasstown - Door to Power Room", lambda state, player: True)
        ],
        [
            # Locations
            ("Power Room - MALCO", lambda state, player: state.has("events;eventFans;1") and state.has("items;charcoal;1") and state.has("items;Juice;1") and state.has("items;gumBase;1") and state.has("events;eventBalrog2;1")),
            # Events
            ("Activated Fans", lambda state, player: True)
        ]
    ),
    RegionData(
        "Save Point - Door to Grasstown",
        [
            # Regions
            ("Grasstown - Door to Save Point", lambda state, player: True),
            ("Save Point - Save Point", lambda state, player: True),
            ("Save Point - Refill", lambda state, player: True)
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
            ("Save Point - Door to Grasstown", lambda state, player: True)
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
            ("Save Point - Door to Grasstown", lambda state, player: True)
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
            ("Grasstown - Door to Grasstown Hut", lambda state, player: True)
        ],
        [
            # Locations
            ("Grasstown Hut - Grasstown Hut", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Execution Chamber - Door to Grasstown",
        [
            # Regions
            ("Grasstown - Door to Execution Chamber", lambda state, player: True)
        ],
        [
            # Locations
            ("Execution Chamber - Execution Chamber", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;1") and state.has("items;missile;2"))),
            # Events
        ]
    ),
    RegionData(
        "Gum - Door to Grasstown",
        [
            # Regions
            ("Grasstown - Door to Gum", lambda state, player: True)
        ],
        [
            # Locations
            ("Gum - Gum Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Shelter - Door to Grasstown",
        [
            # Regions
            ("Grasstown - Door to Shelter", lambda state, player: True),
            ("Shelter - Save Point", lambda state, player: True),
            ("Shelter - Teleporter to Jail No. 2", lambda state, player: True)
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
            ("Shelter - Door to Grasstown", lambda state, player: True),
            ("Shelter - Refill", lambda state, player: True)
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
            ("Jail No. 2 - Teleporter to Shelter", lambda state, player: True),
            ("Shelter - Door to Grasstown", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Saved Kazuma", lambda state, player: True)
        ]
    ),
    RegionData(
        "Shelter - Refill",
        [
            # Regions
            ("Shelter - Save Point", lambda state, player: True)
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
            ("Boulder Chamber - Door to Labyrinth B", lambda state, player: True),
            ("Labyrinth B - Door to Labyrinth W", lambda state, player: True)
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
            ("Labyrinth W - Door to Labyrinth B", lambda state, player: True),
            ("Labyrinth B - Door to Boulder Chamber", lambda state, player: True),
            ("Labyrinth B - Teleporter to Arthur's House", lambda state, player: True),
            ("Labyrinth B - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Enter Labyrinth B from Above", lambda state, player: True)
        ]
    ),
    RegionData(
        "Labyrinth B - Teleporter to Arthur's House",
        [
            # Regions
            ("Arthur's House - Teleporter to Labyrinth B", lambda state, player: True),
            ("Labyrinth B - Door to Labyrinth W", lambda state, player: has_flight(state, player) or (state.has("events;eventMazeB;1") and remove_points_of_no_return(state, player)))
        ],
        [
            # Locations
            ("Labyrinth B - Booster Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth B - Save Point",
        [
            # Regions
            ("Labyrinth B - Door to Labyrinth W", lambda state, player: True),
            ("Labyrinth B - Refill", lambda state, player: True)
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
            ("Labyrinth B - Save Point", lambda state, player: True)
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
            ("Labyrinth B - Door to Boulder Chamber", lambda state, player: True),
            ("Boulder Chamber - Door to Labyrinth M", lambda state, player: True),
            ("Boulder Chamber - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Boulder Chamber - Boulder Chest", lambda state, player: True),
            # Events
            ("Balrog 3", lambda state, player: state.has("events;eventCureAll;1") and (can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;2") and (state.has("items;missiles;24") or (state.has("items;missiles;15") and state.has("items;supers;1"))))))
        ]
    ),
    RegionData(
        "Boulder Chamber - Door to Labyrinth M",
        [
            # Regions
            ("Labyrinth M - Door to Boulder Chamber", lambda state, player: True),
            ("Boulder Chamber - Door to Labyrinth B", lambda state, player: True)
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
            ("Boulder Chamber - Door to Labyrinth B", lambda state, player: True)
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
            ("Boulder Chamber - Door to Labyrinth M", lambda state, player: True),
            ("Labyrinth M - Door to Dark Place", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;3") and has_flight(state, player)) or state.has("tricks;pacifist;4"))
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
            ("Dark Place - Door to Labyrinth M", lambda state, player: True),
            ("Labyrinth M - Door to Boulder Chamber", lambda state, player: state.has("events;eventBalrog3;1") and (has_weapon(state, player) or (state.has("tricks;pacifist;3") and has_flight(state, player)) or state.has("tricks;SNBubbler;4"))),
            ("Labyrinth M - Teleporter to Labyrinth Shop", lambda state, player: has_weapon(state, player) or state.has("tricks;pacifist;1"))
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
            ("Labyrinth Shop - Teleporter to Labyrinth M", lambda state, player: True),
            ("Labyrinth M - Door to Dark Place", lambda state, player: has_weapon(state, player) or state.has("tricks;pacifist;1"))
        ],
        [
            # Locations
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Dark Place - Door to Labyrinth M",
        [
            # Regions
            ("Labyrinth M - Door to Dark Place", lambda state, player: True),
            ("Dark Place - Door to Core", lambda state, player: True),
            ("Dark Place - Exit to Waterway", lambda state, player: True),
            ("Dark Place - Save Point", lambda state, player: True)
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
            ("Core - Door to Dark Place", lambda state, player: True),
            ("Dark Place - Door to Labyrinth M", lambda state, player: True)
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
            ("Waterway - Entrance from Dark Place", lambda state, player: True),
            ("Dark Place - Door to Labyrinth M", lambda state, player: True)
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
            ("Reservoir - Debug Cat to Dark Place", lambda state, player: True),
            ("Dark Place - Door to Labyrinth M", lambda state, player: True)
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
            ("Dark Place - Door to Labyrinth M", lambda state, player: True)
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
            ("Dark Place - Door to Core", lambda state, player: True),
            ("Core - Inner Room", lambda state, player: state.has("events;eventBalrog3;1") and (can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;1") and (state.has("items;missiles;1") or state.has("items;supers;1")) and state.has("items;missile;2"))))
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
            ("Core - Door to Dark Place", lambda state, player: True)
        ],
        [
            # Locations
            ("Core - Robot's Arm", lambda state, player: True),
            # Events
            ("Core", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;4") and state.has("items;missiles;1") and state.has("items;missile;38")) or (state.has("tricks;BossMissiles;3") and state.has("items;supers;1") and state.has("items;missile;16")) or (state.has("tricks;pacifist;2")))
        ]
    ),
    RegionData(
        "Waterway - Entrance from Dark Place",
        [
            # Regions
            ("Dark Place - Exit to Waterway", lambda state, player: True),
            ("Waterway - Door to Waterway Cabin", lambda state, player: state.has("items;airTank;1") and (has_weapon(state, player) or state.has("tricks;pacifist;2")))
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
            ("Main Artery - Entrance from Waterway", lambda state, player: True)
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
            ("Waterway Cabin - Door to Waterway", lambda state, player: True),
            ("Waterway - Exit to Main Artery", lambda state, player: True)
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
            ("Waterway - Door to Waterway Cabin", lambda state, player: True),
            ("Waterway Cabin - Bed", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Drained Curly", lambda state, player: True)
        ]
    ),
    RegionData(
        "Waterway Cabin - Save Point",
        [
            # Regions
            ("Waterway Cabin - Door to Waterway", lambda state, player: True),
            ("Waterway Cabin - Bed", lambda state, player: True)
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
            ("Waterway Cabin - Save Point", lambda state, player: True)
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
            ("Waterway - Exit to Main Artery", lambda state, player: True),
            ("Main Artery - Exit to Reservoir", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Ironhead", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;2") and state.has("items;supers;1") and state.has("items;missile;10")) or (state.has("tricks;BossMissiles;3") and state.has("items;missiles;1") and state.has("items;missile;24")))
        ]
    ),
    RegionData(
        "Main Artery - Exit to Reservoir",
        [
            # Regions
            ("Reservoir - Entrance from Main Artery", lambda state, player: True)
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
            ("Labyrinth H - Door to Labyrinth I", lambda state, player: True),
            ("Labyrinth I - Room Bottom", lambda state, player: True)
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
            ("Labyrinth I - Door to Labyrinth H", lambda state, player: True),
            ("Labyrinth I - Save Point", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;1") and state.has("items;supers;1") and state.has("items;missile;1")) or state.has("tricks;GravHop;3"))
        ],
        [
            # Locations
            ("Labyrinth I - Labyrinth Life Capsule", lambda state, player: has_weapon(state, player) or state.has("tricks;pacifist;3") or (state.has("tricks;pacifist;2") and has_flight(state, player))),
            # Events
            ("Opened Labyrinth I Door", lambda state, player: has_weapon(state, player) or ((state.has("tricks;pacifist;1") and has_flight(state, player))) or state.has("tricks;pacifist;3")),
            ("Use Labyrinth I Teleporter", lambda state, player: True)
        ]
    ),
    RegionData(
        "Labyrinth I - Entrance from Sand Zone Storehouse",
        [
            # Regions
            ("Sand Zone Storehouse - Exit to Labyrinth I", lambda state, player: True),
            ("Labyrinth I - Room Bottom", lambda state, player: True)
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
            ("Sand Zone - Teleporter to Labyrinth I", lambda state, player: True),
            ("Labyrinth I - Room Bottom", lambda state, player: True)
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
            ("Labyrinth I - Room Bottom", lambda state, player: True)
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
            ("Labyrinth I - Door to Labyrinth H", lambda state, player: True),
            ("Labyrinth H - Door to Labyrinth W", lambda state, player: True)
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
            ("Labyrinth W - Door to Labyrinth H", lambda state, player: True),
            ("Labyrinth H - Door to Labyrinth I", lambda state, player: True)
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
            ("Labyrinth H - Door to Labyrinth W", lambda state, player: True),
            ("Labyrinth W - Outside Camp", lambda state, player: True)
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
            ("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True),
            ("Labyrinth W - Outside Camp", lambda state, player: True)
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
            ("Labyrinth W - Door to Labyrinth H", lambda state, player: True),
            ("Labyrinth W - Door to Labyrinth Shop", lambda state, player: True),
            ("Labyrinth W - Door to Camp (Lower)", lambda state, player: True),
            ("Labyrinth W - Door to Camp (Upper)", lambda state, player: can_break_blocks(state, player) and ((state.has("tricks;Dboost;1") and state.has("damage;Damage;8")) or has_flight(state, player) or (state.has("tricks;Dboost;2") and state.has("damage;Damage;3"))) and traverse_labyrinth_w(state, player)),
            ("Labyrinth W - Door to Clinic Ruins", lambda state, player: state.has("items;clinicKey;1") and traverse_labyrinth_w(state, player)),
            ("Labyrinth W - Before Monster X", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Labyrinth W - Door to Camp (Lower)",
        [
            # Regions
            ("Camp - Door to Labyrinth W (Lower)", lambda state, player: True),
            ("Labyrinth W - Outside Camp", lambda state, player: True)
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
            ("Camp - Door to Labyrinth W (Upper)", lambda state, player: True),
            ("Labyrinth W - Outside Camp", lambda state, player: can_break_blocks(state, player) and traverse_labyrinth_w(state, player))
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
            ("Clinic Ruins - Door to Labyrinth W", lambda state, player: True),
            ("Labyrinth W - Outside Camp", lambda state, player: True)
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
            ("Labyrinth B - Door to Labyrinth W", lambda state, player: True),
            ("Labyrinth W - Before Monster X", lambda state, player: True)
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
            ("Labyrinth W - Outside Camp", lambda state, player: True),
            ("Labyrinth W - Door to Labyrinth B", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Monster X", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;3") and state.has("items;supers;1") and state.has("items;missile;30")) or (state.has("tricks;BossMissiles;4") and state.has("items;missiles;1") and state.has("items;missile;60")))
        ]
    ),
    RegionData(
        "Labyrinth Shop - Door to Labyrinth W",
        [
            # Regions
            ("Labyrinth W - Door to Labyrinth Shop", lambda state, player: True),
            ("Labyrinth Shop - Teleporter to Labyrinth M", lambda state, player: True),
            ("Labyrinth Shop - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Labyrinth Shop - Chaba Chest (Machine Gun)", lambda state, player: True),
            ("Labyrinth Shop - Chaba Chest (Fireball)", lambda state, player: True),
            ("Labyrinth Shop - Chaba Chest (Spur)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Labyrinth Shop - Teleporter to Labyrinth M",
        [
            # Regions
            ("Labyrinth M - Teleporter to Labyrinth Shop", lambda state, player: True),
            ("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True)
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
            ("Labyrinth Shop - Door to Labyrinth W", lambda state, player: True)
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
            ("Labyrinth W - Door to Camp (Lower)", lambda state, player: True),
            ("Camp - Door to Labyrinth W (Upper)", lambda state, player: True),
            ("Camp - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Camp - Dr. Gero", lambda state, player: True),
            # Events
            ("Cure-All", lambda state, player: True)
        ]
    ),
    RegionData(
        "Camp - Door to Labyrinth W (Upper)",
        [
            # Regions
            ("Labyrinth W - Door to Camp (Upper)", lambda state, player: True),
            ("Camp - Door to Labyrinth W (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            ("Camp - Camp Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Camp - Room Spawn",
        [
            # Regions
            ("Camp - Door to Labyrinth W (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Camp", lambda state, player: True)
        ]
    ),
    RegionData(
        "Camp - Save Point",
        [
            # Regions
            ("Camp - Door to Labyrinth W (Lower)", lambda state, player: True)
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
            ("Labyrinth W - Door to Clinic Ruins", lambda state, player: True)
        ],
        [
            # Locations
            ("Clinic Ruins - Puu Black Boss", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Final Cave - Door to Plantation",
        [
            # Regions
            ("Plantation - Door to Final Cave", lambda state, player: True),
            ("Final Cave - Door to Balcony (Pre-Bosses)", lambda state, player: True)
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
            ("Balcony (Pre-Bosses) - Door to Final Cave", lambda state, player: True),
            ("Final Cave - Door to Plantation", lambda state, player: True)
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
            ("Plantation - Door to Last Cave (Hidden)", lambda state, player: True),
            ("Last Cave (Hidden) - Before Red Demon", lambda state, player: state.has("items;booster2;1") and has_weapon(state, player))
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
            ("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)", lambda state, player: True),
            ("Last Cave (Hidden) - Before Red Demon", lambda state, player: state.has("items;booster2;1") and has_weapon(state, player))
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
            ("Last Cave (Hidden) - Door to Plantation", lambda state, player: True),
            ("Last Cave (Hidden) - Door to Balcony (Pre-Bosses)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Red Demon", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;2") and state.has("items;supers;1") and state.has("items;missile;8")) or (state.has("tricks;BossMissiles;3") and state.has("items;missiles;1") and state.has("items;missile;18")))
        ]
    ),
    RegionData(
        "Balcony (Pre-Bosses) - Exit to Throne Room",
        [
            # Regions
            ("Throne Room - Entrance from Balcony (Pre-Bosses)", lambda state, player: True)
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
            ("Final Cave - Door to Balcony (Pre-Bosses)", lambda state, player: True),
            ("Balcony (Pre-Bosses) - Door to Prefab Building", lambda state, player: True)
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
            ("Last Cave (Hidden) - Door to Balcony (Pre-Bosses)", lambda state, player: True),
            ("Balcony (Pre-Bosses) - Door to Prefab Building", lambda state, player: True)
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
            ("Prefab Building - Door to Balcony (Pre-Bosses)", lambda state, player: True),
            ("Balcony (Pre-Bosses) - Exit to Throne Room", lambda state, player: True),
            ("Balcony (Pre-Bosses) - Door to Final Cave", lambda state, player: True),
            ("Balcony (Pre-Bosses) - Door to Last Cave (Hidden)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Lowered Barrier", lambda state, player: (state.has("events;eventSue;1") and (state.has("misc;normalEnd;1") or (state.has("items;ironBond;1") and state.has("items;booster2;1") and (state.has("misc;bestEnd;1") or (state.has("events;eventBalfrog;1") and state.has("events;eventBalrog;1") and state.has("events;eventBalrog2;1") and state.has("events;eventBalrog3;1") and state.has("events;eventFightCurly;1") and state.has("events;eventIgor;1") and state.has("events;eventIronhead;1") and state.has("events;eventMaPignon;1") and state.has("events;eventMonsterX;1") and state.has("events;eventOmega;1") and state.has("events;eventPuu;1") and state.has("events;eventSisters;1") and state.has("events;eventToroko;1") and state.has("events;eventCore;1") and (state.has("misc;allBosses;1") or (state.has("misc;hundo;1") and ()))))))))
        ]
    ),
    RegionData(
        "Prefab Building - Door to Balcony (Pre-Bosses)",
        [
            # Regions
            ("Balcony (Pre-Bosses) - Door to Prefab Building", lambda state, player: True),
            ("Prefab Building - Save Point/Bed", lambda state, player: True)
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
            ("Prefab Building - Door to Balcony (Pre-Bosses)", lambda state, player: True)
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
            ("Balcony (Pre-Bosses) - Exit to Throne Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Misery", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;3") and state.has("items;supers;1") and state.has("items;missile;13")) or (state.has("tricks;BossMissiles;4") and state.has("items;missiles;1") and state.has("items;missile;31")))
        ]
    ),
    RegionData(
        "Throne Room - Exit to Balcony (Post-Bosses)",
        [
            # Regions
            ("Balcony (Post-Bosses) - Entrance from Throne Room", lambda state, player: True)
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
            ("The King's Table - H/V Trigger to Throne Room", lambda state, player: True),
            ("Throne Room - Exit to Balcony (Post-Bosses)", lambda state, player: True)
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
            ("Throne Room - H/V Trigger to The King's Table", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Doctor", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;2") and state.has("items;missiles;1") and state.has("items;missile;36")) or (state.has("tricks;BossMissiles;3") and state.has("items;supers;1") and state.has("items;missile;16")))
        ]
    ),
    RegionData(
        "The King's Table - H/V Trigger to Black Space",
        [
            # Regions
            ("Black Space - H/V Trigger to The King's Table", lambda state, player: True),
            ("The King's Table - H/V Trigger to Throne Room", lambda state, player: True)
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
            ("The King's Table - H/V Trigger to Black Space", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Undead Core", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;3") and state.has("items;supers;1") and state.has("items;missile;18")) or (state.has("tricks;BossMissiles;4") and state.has("items;missiles;1") and state.has("items;missile;42")))
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Entrance from Throne Room",
        [
            # Regions
            ("Throne Room - Exit to Balcony (Post-Bosses)", lambda state, player: True),
            ("Balcony (Post-Bosses) - Exit to Prefab House", lambda state, player: state.has("items;ironBond;1") and (state.has("misc;bestEnd;1") or state.has("misc;allBosses;1") or state.has("misc;hundo;1") or state.has("misc;entranceRando;1")))
        ],
        [
            # Locations
            # Events
            ("Normal Ending", lambda state, player: state.has("misc;normalEnd;1") and state.has("events;eventCore2;1"))
        ]
    ),
    RegionData(
        "Balcony (Post-Bosses) - Exit to Prefab House",
        [
            # Regions
            ("Prefab House - Entrance from Balcony (Post-Bosses)", lambda state, player: True)
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
            ("Prefab House - Exit to Balcony (Post-Bosses)", lambda state, player: True),
            ("Balcony (Post-Bosses) - Entrance from Throne Room", lambda state, player: True)
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
            ("Balcony (Post-Bosses) - Exit to Prefab House", lambda state, player: True),
            ("Prefab House - Exit to Balcony (Post-Bosses)", lambda state, player: True),
            ("Prefab House - Exit to Sacred Grounds - B1", lambda state, player: True),
            ("Prefab House - Save Point", lambda state, player: True)
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
            ("Balcony (Post-Bosses) - Entrance from Prefab House", lambda state, player: True)
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
            ("Sacred Grounds - B1 - Entrance from Prefab House", lambda state, player: True)
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
            ("Prefab House - Entrance from Balcony (Post-Bosses)", lambda state, player: True)
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
            ("Prefab House - Exit to Sacred Grounds - B1", lambda state, player: True)
        ],
        [
            # Locations
            ("Sacred Grounds - B1 - Hell B1 Spot", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sacred Grounds - B1 - Door to Sacred Grounds - B2",
        [
            # Regions
            ("Sacred Grounds - B2 - Door to Sacred Grounds - B1", lambda state, player: True)
        ],
        [
            # Locations
            ("Sacred Grounds - B1 - Hell B1 Spot", lambda state, player: True),
            # Events
            ("Curly", lambda state, player: True)
        ]
    ),
    RegionData(
        "Sacred Grounds - B2 - Door to Sacred Grounds - B1",
        [
            # Regions
            ("Sacred Grounds - B1 - Door to Sacred Grounds - B2", lambda state, player: True),
            ("Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3", lambda state, player: True)
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
            ("Sacred Grounds - B3 - H/V Trigger to Sacred Grounds - B2", lambda state, player: True),
            ("Sacred Grounds - B2 - Door to Sacred Grounds - B1", lambda state, player: True)
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
            ("Sacred Grounds - B2 - H/V Trigger to Sacred Grounds - B3", lambda state, player: True)
        ],
        [
            # Locations
            ("Sacred Grounds - B3 - Hell B3 Chest", lambda state, player: (has_flight(state, player) or (state.has("tricks;Dboost;1") and state.has("damage;Damage;10"))) and has_weapon(state, player)),
            # Events
            ("Heavy Press", lambda state, player: can_kill_bosses(state, player) and (has_flight(state, player) or (state.has("tricks;Dboost;1") and state.has("damage;Damage;10"))))
        ]
    ),
    RegionData(
        "Sacred Grounds - B3 - Exit to Passage?",
        [
            # Regions
            ("Passage? - Entrance from Sacred Grounds - B3", lambda state, player: True)
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
            ("Passage? - Door to Corridor", lambda state, player: True),
            ("Corridor - Exit to Seal Chamber", lambda state, player: True)
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
            ("Seal Chamber - Entrance from Corridor", lambda state, player: True),
            ("Corridor - Door to Passage?", lambda state, player: True)
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
            ("Corridor - Exit to Seal Chamber", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Best Ending", lambda state, player: (can_kill_bosses(state, player) or (state.has("tricks;pacifist;1") and state.has("events;eventCurly3;1"))) and has_flight(state, player) and (state.has("misc;bestEnd;1") or state.has("misc;allBosses;1") or state.has("misc;hundo;1")))
        ]
    ),
    RegionData(
        "Start Point - Door to First Cave",
        [
            # Regions
            ("First Cave - Door to Start Point", lambda state, player: True),
            ("Start Point - Save Point", lambda state, player: True)
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
            ("Start Point - Door to First Cave", lambda state, player: True),
            ("Start Point - Refill", lambda state, player: True)
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
            ("Start Point", lambda state, player: True)
        ]
    ),
    RegionData(
        "Start Point - Refill",
        [
            # Regions
            ("Start Point - Save Point", lambda state, player: True)
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
            ("Start Point - Door to First Cave", lambda state, player: True),
            ("First Cave - Door to Hermit Gunsmith", lambda state, player: True),
            ("First Cave - Door to Mimiga Village", lambda state, player: can_break_blocks(state, player) and (has_weapon(state, player) or state.has("events;startPoint;1")))
        ],
        [
            # Locations
            ("First Cave - First Cave Life Capsule", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "First Cave - Door to Hermit Gunsmith",
        [
            # Regions
            ("Hermit Gunsmith - Door to First Cave", lambda state, player: True),
            ("First Cave - Door to Start Point", lambda state, player: True)
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
            ("Mimiga Village - Door to First Cave", lambda state, player: True),
            ("First Cave - Door to Start Point", lambda state, player: True)
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
            ("First Cave - Door to Hermit Gunsmith", lambda state, player: True)
        ],
        [
            # Locations
            ("Hermit Gunsmith - Hermit Gunsmith Chest", lambda state, player: True),
            ("Hermit Gunsmith - Tetsuzou", lambda state, player: (state.has("items;polarStar;1") or state.has("items;spur;1")) and state.has("events;eventCore;1")),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to First Cave",
        [
            # Regions
            ("First Cave - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Mimiga Village - Door to First Cave", lambda state, player: True),
            ("Mimiga Village - Door to Save Point", lambda state, player: True),
            ("Mimiga Village - Door to Reservoir", lambda state, player: True),
            ("Mimiga Village - Door to Yamashita Farm", lambda state, player: True),
            ("Mimiga Village - Door to Assembly Hall", lambda state, player: True),
            ("Mimiga Village - Door to Graveyard", lambda state, player: True),
            ("Mimiga Village - Door to Shack", lambda state, player: True),
            ("Mimiga Village - Door to Arthur's House", lambda state, player: True)
        ],
        [
            # Locations
            ("Mimiga Village - Mimiga Village Chest", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Mimiga Village - Door to Save Point",
        [
            # Regions
            ("Save Point - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Reservoir - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Yamashita Farm - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Assembly Hall - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Graveyard - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Shack - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Arthur's House - Door to Mimiga Village", lambda state, player: True),
            ("Mimiga Village - Room Centre", lambda state, player: True)
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
            ("Mimiga Village - Door to Save Point", lambda state, player: True),
            ("Save Point - Save Point", lambda state, player: True),
            ("Save Point - Refill", lambda state, player: True)
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
            ("Save Point - Door to Mimiga Village", lambda state, player: True)
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
            ("Save Point - Door to Mimiga Village", lambda state, player: True)
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
            ("Mimiga Village - Door to Yamashita Farm", lambda state, player: True)
        ],
        [
            # Locations
            ("Yamashita Farm - Yamashita Farm", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Door to Mimiga Village",
        [
            # Regions
            ("Mimiga Village - Door to Reservoir", lambda state, player: True),
            ("Reservoir - Debug Cat to Dark Place", lambda state, player: state.has("misc;entranceRando;1") and state.has("events;eventIronhead;1"))
        ],
        [
            # Locations
            ("Reservoir - Reservoir", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Reservoir - Debug Cat to Dark Place",
        [
            # Regions
            ("Dark Place - Entrance from Reservoir", lambda state, player: True),
            ("Reservoir - Door to Mimiga Village", lambda state, player: True)
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
            ("Main Artery - Exit to Reservoir", lambda state, player: True),
            ("Reservoir - Door to Mimiga Village", lambda state, player: True)
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
            ("Mimiga Village - Door to Assembly Hall", lambda state, player: True)
        ],
        [
            # Locations
            ("Assembly Hall - Assembly Hall Fireplace", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Mimiga Village",
        [
            # Regions
            ("Mimiga Village - Door to Graveyard", lambda state, player: True),
            ("Graveyard - Door to Storage", lambda state, player: True)
        ],
        [
            # Locations
            ("Graveyard - Arthur's Grave", lambda state, player: True),
            ("Graveyard - Mr. Little (Graveyard)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Graveyard - Door to Storage",
        [
            # Regions
            ("Storage - Door to Graveyard", lambda state, player: True),
            ("Graveyard - Door to Mimiga Village", lambda state, player: True)
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
            ("Graveyard - Door to Storage", lambda state, player: True)
        ],
        [
            # Locations
            ("Storage - Storage? Chest", lambda state, player: True),
            # Events
            ("Ma Pignon", lambda state, player: state.has("items;mushBadge;1") and (state.has("items;polarStar;1") or state.has("items;machineGun;1") or state.has("items;bubbler;1") or state.has("items;fireball;1") or state.has("items;spur;1") or state.has("items;snake;1") or state.has("items;nemesis;1")))
        ]
    ),
    RegionData(
        "Shack - Door to Mimiga Village",
        [
            # Regions
            ("Mimiga Village - Door to Shack", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Toroko Kidnapped", lambda state, player: state.has("items;locket;1") and has_weapon(state, player)),
            ("Balrog 1", lambda state, player: state.has("events;eventToroko2;1") and (can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;1") and ((state.has("items;missiles;1") and state.has("items;missile;4")) or (state.has("items;supers;2") and state.has("items;missile;2")))))),
            ("Level MG", lambda state, player: state.has("items;machineGun;1") and state.has("events;eventBalrog;1"))
        ]
    ),
    RegionData(
        "Arthur's House - Door to Mimiga Village",
        [
            # Regions
            ("Mimiga Village - Door to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Arthur's House - Door to Mimiga Village", lambda state, player: True),
            ("Arthur's House - Save Point", lambda state, player: True),
            ("Arthur's House - Teleporter to Egg Corridor", lambda state, player: True),
            ("Arthur's House - Teleporter to Grasstown", lambda state, player: True),
            ("Arthur's House - Teleporter to Sand Zone", lambda state, player: True),
            ("Arthur's House - Teleporter to Labyrinth B", lambda state, player: True),
            ("Arthur's House - Teleporter to Teleporter", lambda state, player: True),
            ("Arthur's House - Teleporter to Egg Corridor?", lambda state, player: state.has("events;eventCore;1") or state.has("events;eventEgg2Teleport;1")),
            ("Arthur's House - Room Spawn", lambda state, player: True)
        ],
        [
            # Locations
            ("Arthur's House - Professor Booster", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Arthur's House - Save Point",
        [
            # Regions
            ("Arthur's House - Main Teleporter", lambda state, player: True),
            ("Arthur's House - Refill", lambda state, player: True)
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
            ("Egg Corridor - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Grasstown - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Sand Zone - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Labyrinth B - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Teleporter - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Egg Corridor? - Teleporter to Arthur's House", lambda state, player: True),
            ("Arthur's House - Main Teleporter", lambda state, player: True)
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
            ("Arthur's House", lambda state, player: True)
        ]
    ),
    RegionData(
        "Arthur's House - Refill",
        [
            # Regions
            ("Arthur's House - Save Point", lambda state, player: True)
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
            ("Rest Area - Door to Plantation", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True)
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
            ("Teleporter - Door to Plantation", lambda state, player: True),
            ("Plantation - Lower Level", lambda state, player: True)
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
            ("Storehouse - Door to Plantation", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True)
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
            ("Jail No. 1 - Door to Plantation (Lower)", lambda state, player: True),
            ("Plantation - Upper Level", lambda state, player: True)
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
            ("Jail No. 1 - Door to Plantation (Upper)", lambda state, player: True),
            ("Plantation - Upper Level", lambda state, player: True)
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
            ("Jail No. 2 - Door to Plantation", lambda state, player: True),
            ("Plantation - Upper Level", lambda state, player: True)
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
            ("Last Cave (Hidden) - Door to Plantation", lambda state, player: True),
            ("Plantation - Top Level", lambda state, player: True)
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
            ("Passage? - Door to Plantation", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True)
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
            ("Hideout - Door to Plantation", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True)
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
            ("Plantation - Door to Teleporter", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True)
        ],
        [
            # Locations
            ("Plantation - Kanpachi's Bucket", lambda state, player: True),
            ("Plantation - Jammed it into Curly's mouth", lambda state, player: state.has("events;eventCurly;1") and state.has("items;maPignon;1")),
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Plantation - Middle Level",
        [
            # Regions
            ("Plantation - Door to Rest Area", lambda state, player: True),
            ("Plantation - Door to Storehouse", lambda state, player: True),
            ("Plantation - Door to Passage?", lambda state, player: True),
            ("Plantation - Door to Hideout", lambda state, player: True),
            ("Plantation - Lower Level", lambda state, player: True),
            ("Plantation - Upper Level", lambda state, player: True),
            ("Plantation - Top Level", lambda state, player: True)
        ],
        [
            # Locations
            ("Plantation - Broken Sprinker", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Plantation - Upper Level",
        [
            # Regions
            ("Plantation - Door to Jail No. 1 (Lower)", lambda state, player: True),
            ("Plantation - Door to Jail No. 1 (Upper)", lambda state, player: True),
            ("Plantation - Door to Jail No. 2", lambda state, player: True),
            ("Plantation - Middle Level", lambda state, player: True),
            ("Plantation - Top Level", lambda state, player: (state.has("items;booster2;1") and state.has("items;machineGun;1") and state.has("tricks;Dboost;4") and state.has("damage;Damage;2")) or (state.has("items;booster2;1") and state.has("tricks;Dboost;5")))
        ],
        [
            # Locations
            ("Plantation - Plantation Platforming Spot", lambda state, player: has_flight(state, player) or (state.has("tricks;Dboost;3") and state.has("tricks;IframeReset;1") and state.has("damage;Damage;10") and reset_iframes(state, player))),
            ("Plantation - Plantation Puppy", lambda state, player: state.has("events;eventRocket;1")),
            # Events
        ]
    ),
    RegionData(
        "Plantation - Door to Final Cave",
        [
            # Regions
            ("Final Cave - Door to Plantation", lambda state, player: True),
            ("Plantation - Top Level", lambda state, player: True)
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
            ("Plantation - Door to Last Cave (Hidden)", lambda state, player: state.has("items;booster2;1") and (state.has("events;eventRocket;1"))),
            ("Plantation - Upper Level", lambda state, player: True),
            ("Plantation - Door to Final Cave", lambda state, player: state.has("items;booster2;1") and (state.has("events;eventRocket;1")))
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
            ("Plantation - Door to Storehouse", lambda state, player: True),
            ("Storehouse - Door to Outer Wall", lambda state, player: True)
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
            ("Outer Wall - Door to Storehouse", lambda state, player: True),
            ("Storehouse - Door to Plantation", lambda state, player: True),
            ("Storehouse - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Storehouse - Itoh", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Storehouse - Save Point",
        [
            # Regions
            ("Storehouse - Door to Outer Wall", lambda state, player: True)
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
            ("Plantation - Door to Passage?", lambda state, player: True),
            ("Passage? - Door to Statue Chamber", lambda state, player: True)
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
            ("Statue Chamber - Door to Passage?", lambda state, player: True),
            ("Passage? - Door to Plantation", lambda state, player: True),
            ("Passage? - Door to Corridor", lambda state, player: True)
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
            ("Corridor - Door to Passage?", lambda state, player: True),
            ("Passage? - Door to Statue Chamber", lambda state, player: has_flight(state, player) and state.has("events;eventHell4;1"))
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
            ("Sacred Grounds - B3 - Exit to Passage?", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Entered Passage from Above", lambda state, player: True)
        ]
    ),
    RegionData(
        "Statue Chamber - Door to Passage?",
        [
            # Regions
            ("Passage? - Door to Statue Chamber", lambda state, player: True)
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
            ("Plantation - Door to Rest Area", lambda state, player: True),
            ("Rest Area - Bed", lambda state, player: True)
        ],
        [
            # Locations
            ("Rest Area - Megane", lambda state, player: state.has("items;mask;1") and state.has("items;brokenSprinkler;1")),
            # Events
        ]
    ),
    RegionData(
        "Rest Area - Bed",
        [
            # Regions
            ("Rest Area - Door to Plantation", lambda state, player: True)
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
            ("Plantation - Door to Teleporter", lambda state, player: True),
            ("Teleporter - Room Hub", lambda state, player: True)
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
            ("Teleporter - Door to Plantation", lambda state, player: True),
            ("Teleporter - Teleporter to Arthur's House", lambda state, player: state.has("items;teleportKey;1") or state.has("events;eventDroll;1")),
            ("Teleporter - Exit to Jail No. 1", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Droll Attack", lambda state, player: True)
        ]
    ),
    RegionData(
        "Teleporter - Teleporter to Arthur's House",
        [
            # Regions
            ("Arthur's House - Teleporter to Teleporter", lambda state, player: True),
            ("Teleporter - Room Hub", lambda state, player: True)
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
            ("Jail No. 1 - Entrance from Teleporter", lambda state, player: True)
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
            ("Plantation - Door to Jail No. 1 (Upper)", lambda state, player: True)
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
            ("Teleporter - Exit to Jail No. 1", lambda state, player: True),
            ("Jail No. 1 - Door to Plantation (Upper)", lambda state, player: True),
            ("Jail No. 1 - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Jail No. 1 - Jail No. 1", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Jail No. 1 - Door to Plantation (Lower)",
        [
            # Regions
            ("Plantation - Door to Jail No. 1 (Lower)", lambda state, player: True)
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
            ("Jail No. 1 - Entrance from Teleporter", lambda state, player: True)
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
            ("Plantation - Door to Jail No. 2", lambda state, player: True),
            ("Jail No. 2 - Teleporter to Shelter", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;1")))
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
            ("Shelter - Teleporter to Jail No. 2", lambda state, player: True),
            ("Jail No. 2 - Door to Plantation", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;1")))
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
            ("Plantation - Door to Hideout", lambda state, player: True),
            ("Hideout - Bed", lambda state, player: True)
        ],
        [
            # Locations
            ("Hideout - Chivalry Sakamoto's Wife", lambda state, player: True),
            # Events
            ("Built Rocket", lambda state, player: (state.has("items;booster1;1") or state.has("items;booster2;1")) and state.has("items;newSprinkler;1") and state.has("items;controller;1"))
        ]
    ),
    RegionData(
        "Hideout - Bed",
        [
            # Regions
            ("Hideout - Door to Plantation", lambda state, player: True),
            ("Hideout - Save Point", lambda state, player: True)
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
            ("Hideout - Bed", lambda state, player: True)
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
            ("Cthulhu's Abode? - Door to Egg Corridor? (Upper)", lambda state, player: True),
            ("Egg Corridor? - Area Centre", lambda state, player: True)
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
            ("Cthulhu's Abode? - Door to Egg Corridor? (Lower)", lambda state, player: True),
            ("Egg Corridor? - West Side", lambda state, player: True)
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
            ("Egg Corridor? - Door to Cthulhu's Abode? (Lower)", lambda state, player: True)
        ],
        [
            # Locations
            ("Egg Corridor? - Dragon Chest", lambda state, player: has_weapon(state, player) or state.has("tricks;pacifist;3") or (state.has("tricks;pacifist;2") and state.has("damage;Damage;10") and state.has("tricks;Dboost;1"))),
            # Events
            ("Used Egg Corridor? Teleporter", lambda state, player: True),
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg Corridor? - Area Centre",
        [
            # Regions
            ("Egg Corridor? - Door to Cthulhu's Abode? (Upper)", lambda state, player: True),
            ("Egg Corridor? - Door to Egg Observation Room? (West)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg Corridor? - East Side",
        [
            # Regions
            ("Egg Corridor? - Door to Egg Observation Room? (East)", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1") and has_flight(state, player)) or (state.has("tricks;Dboost;1") and state.has("damage;Damage;10") and state.has("tricks;pacifist;3"))),
            ("Egg Corridor? - Door to Egg No. 00", lambda state, player: True),
            ("Egg Corridor? - Door to Side Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Egg Corridor? - Door to Egg Observation Room? (West)",
        [
            # Regions
            ("Egg Observation Room? - Door to Egg Corridor? (Western)", lambda state, player: True),
            ("Egg Corridor? - Area Centre", lambda state, player: True)
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
            ("Egg Observation Room? - Door to Egg Corridor? (Eastern)", lambda state, player: True),
            ("Egg Corridor? - East Side", lambda state, player: True)
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
            ("Egg No. 00 - Door to Egg Corridor?", lambda state, player: True),
            ("Egg Corridor? - East Side", lambda state, player: True)
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
            ("Side Room - Door to Egg Corridor?", lambda state, player: True),
            ("Egg Corridor? - East Side", lambda state, player: True)
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
            ("Arthur's House - Teleporter to Egg Corridor?", lambda state, player: True),
            ("Egg Corridor? - West Side", lambda state, player: True)
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
            ("Egg Corridor? - Door to Cthulhu's Abode? (Upper)", lambda state, player: True),
            ("Cthulhu's Abode? - Door to Egg Corridor? (Lower)", lambda state, player: has_weapon(state, player) and (can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;3"))))
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
            ("Egg Corridor? - Door to Cthulhu's Abode? (Lower)", lambda state, player: True),
            ("Cthulhu's Abode? - Door to Egg Corridor? (Upper)", lambda state, player: has_weapon(state, player) and (can_break_blocks(state, player) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;3")) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1"))))
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
            ("Egg Corridor? - Door to Egg Observation Room? (West)", lambda state, player: True),
            ("Egg Observation Room? - Door to Egg Corridor? (Eastern)", lambda state, player: True)
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
            ("Egg Corridor? - Door to Egg Observation Room? (East)", lambda state, player: True),
            ("Egg Observation Room? - Door to Egg Corridor? (Western)", lambda state, player: state.has("events;eventSisters;1") or has_flight(state, player)),
            ("Egg Observation Room? - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Egg Observation Room? - Sisters Boss", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Egg Observation Room? - Save Point",
        [
            # Regions
            ("Egg Observation Room? - Door to Egg Corridor? (Eastern)", lambda state, player: True)
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
            ("Egg Corridor? - Door to Side Room", lambda state, player: True),
            ("Side Room - Save Point", lambda state, player: True)
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
            ("Side Room - Door to Egg Corridor?", lambda state, player: True),
            ("Side Room - Refill", lambda state, player: True)
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
            ("Side Room - Save Point", lambda state, player: True)
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
            ("Egg Corridor? - Door to Egg No. 00", lambda state, player: True),
            ("Egg No. 00 - Door to Outer Wall", lambda state, player: True)
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
            ("Outer Wall - Door to Egg No. 00", lambda state, player: True),
            ("Egg No. 00 - Door to Egg Corridor?", lambda state, player: True)
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
            ("Egg No. 00 - Door to Outer Wall", lambda state, player: True),
            ("Outer Wall - Room Bottom", lambda state, player: True)
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
            ("Little House - Door to Outer Wall", lambda state, player: True),
            ("Outer Wall - Room Bottom", lambda state, player: True)
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
            ("Outer Wall - Room Bottom", lambda state, player: True),
            ("Outer Wall - Room Top", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;2") and has_flight(state, player)) or (state.has("tricks;pacifist;3") and state.has("damage;Damage;5")) or (state.has("tricks;pacifist;4"))),
            ("Outer Wall - Door to Clock Room", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Outer Wall - Door to Storehouse",
        [
            # Regions
            ("Storehouse - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Entered Outer Wall from Storehouse", lambda state, player: True)
        ]
    ),
    RegionData(
        "Outer Wall - Room Bottom",
        [
            # Regions
            ("Outer Wall - Door to Egg No. 00", lambda state, player: True),
            ("Outer Wall - Door to Little House", lambda state, player: True),
            ("Outer Wall - Outside Clock Room", lambda state, player: has_flight(state, player) or (remove_points_of_no_return(state, player) and state.has("events;eventOside;1")))
        ],
        [
            # Locations
            # Events
            ("Bad Ending", lambda state, player: state.has("misc;badEnd;1") and state.has("events;eventKazuma;1") and state.has("events;eventCore;1"))
        ]
    ),
    RegionData(
        "Outer Wall - Room Top",
        [
            # Regions
            ("Outer Wall - Outside Clock Room", lambda state, player: True),
            ("Outer Wall - Door to Storehouse", lambda state, player: True)
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
            ("Clock Room - Door to Outer Wall", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Entered Outer Wall from Clock Room", lambda state, player: True)
        ]
    ),
    RegionData(
        "Little House - Door to Outer Wall",
        [
            # Regions
            ("Outer Wall - Door to Little House", lambda state, player: True)
        ],
        [
            # Locations
            ("Little House - Little House", lambda state, player: state.has("items;blade;1") and state.has("items;mrLittle;1")),
            # Events
        ]
    ),
    RegionData(
        "Clock Room - Door to Outer Wall",
        [
            # Regions
            ("Outer Wall - Door to Clock Room", lambda state, player: True)
        ],
        [
            # Locations
            ("Clock Room - Clock Room", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Door to Jenka's House",
        [
            # Regions
            ("Jenka's House - Door to Sand Zone", lambda state, player: True),
            ("Sand Zone - Outside Jenka's House", lambda state, player: True)
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
            ("Arthur's House - Teleporter to Sand Zone", lambda state, player: True),
            ("Sand Zone - Outside Sand Zone Residence", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and state.has("items;missiles;1")))
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
            ("Sand Zone - Teleporter to Arthur's House", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;1") and (state.has("items;missiles;1") or state.has("items;supers;1")) and state.has("items;missile;1"))),
            ("Sand Zone - Door to Sand Zone Residence", lambda state, player: True),
            ("Sand Zone - Above Sunstones", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNMissiles;2") and state.has("items;missiles;1") and state.has("items;missile;3")) or (state.has("tricks;SNMissiles;3") and (state.has("items;missile;3") or (state.has("items;missile;1") and state.has("items;supers;1")))) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")))
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
            ("Sand Zone Residence - Door to Sand Zone", lambda state, player: True),
            ("Sand Zone - Outside Sand Zone Residence", lambda state, player: True)
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
            ("Sand Zone - Door to Deserted House", lambda state, player: True),
            ("Sand Zone - Outside Jenka's House", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;3")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;2")))),
            ("Sand Zone - Outside Sand Zone Storehouse", lambda state, player: has_flight(state, player) or (has_flight(state, player) and state.has("tricks;pacifist;1")) or state.has("tricks;pacifist;2"))
        ],
        [
            # Locations
            ("Sand Zone - Puppy (Run)", lambda state, player: True),
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Sand Zone - Door to Deserted House",
        [
            # Regions
            ("Deserted House - Door to Sand Zone", lambda state, player: True),
            ("Sand Zone - Lower Side", lambda state, player: True)
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
            ("Sand Zone Storehouse - Entrance from Sand Zone", lambda state, player: True)
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
            ("Sand Zone - Outside Sand Zone Residence", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;3")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;2")))),
            ("Sand Zone - Before Omega", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;27")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;13")) or (state.has("tricks;SNMissiles;4") and state.has("items;missile;1")))),
            ("Sand Zone - Outside Jenka's House", lambda state, player: state.has("events;eventOmega;1") and (can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;2") and state.has("items;missile;4")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;2")) or (state.has("tricks;SNMissiles;4") and state.has("items;missile;1")))),
            ("Sand Zone - Pawprint Spot", lambda state, player: state.has("events;eventOmega;1") and (can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;2") and state.has("items;missiles;3"))))
        ],
        [
            # Locations
            ("Sand Zone - Polish Spot", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("items;missile;10") and state.has("tricks;SNMissiles;2")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;5")))),
            # Events
            ("Level MG", lambda state, player: True)
        ]
    ),
    RegionData(
        "Sand Zone - Before Omega",
        [
            # Regions
            ("Sand Zone - Above Sunstones", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;22")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;11")) or (state.has("tricks;SNMissiles;4") and state.has("items;missile;1")))),
            ("Sand Zone - Refill (Upper)", lambda state, player: True)
        ],
        [
            # Locations
            # Events
            ("Omega", lambda state, player: (can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;6")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;2")) or (state.has("tricks;SNMissiles;4") and state.has("items;missile;1")))) and (can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;1") and state.has("items;supers;1") and state.has("items;missile;11")) or (state.has("tricks;BossMissiles;2") and state.has("items;supers;1") and state.has("items;missile;10")) or (state.has("tricks;BossMissiles;3") and state.has("items;missiles;1") and state.has("items;missile;50")) or (state.has("tricks;BossMissiles;5") and state.has("items;missiles;1") and state.has("items;missile;25"))))
        ]
    ),
    RegionData(
        "Sand Zone - Outside Jenka's House",
        [
            # Regions
            ("Sand Zone - Door to Jenka's House", lambda state, player: True),
            ("Sand Zone - Lower Side", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or ((state.has("tricks;SNMissiles;2") and state.has("items;missile;3")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;1")))),
            ("Sand Zone - Above Sunstones", lambda state, player: ((state.has("tricks;SNMissiles;2") and state.has("items;missile;4")) or (state.has("tricks;SNMissiles;3") and state.has("items;missile;2")) or (state.has("tricks;SNMissiles;4") and state.has("items;missile;1")) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or can_break_blocks(state, player)) and state.has("events;eventOmega;1")),
            ("Sand Zone - Pawprint Spot", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;2") and state.has("items;missiles;3")))
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
            ("Sand Zone - Above Sunstones", lambda state, player: state.has("events;eventOmega;1") and (can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;2") and state.has("items;missiles;3")))),
            ("Sand Zone - Outside Jenka's House", lambda state, player: can_break_blocks(state, player) or (state.has("tricks;SNBubbler;1") and state.has("items;bubbler;1")) or (state.has("tricks;SNMissiles;2") and state.has("items;missiles;3")))
        ],
        [
            # Locations
            ("Sand Zone - Pawprint Spot", lambda state, player: True),
            ("Sand Zone - Puppy (Chest)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Refill (Upper)",
        [
            # Regions
            ("Sand Zone - Before Omega", lambda state, player: True),
            ("Sand Zone - Save Point (Upper)", lambda state, player: True)
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
            ("Sand Zone - Outside Sand Zone Storehouse", lambda state, player: True),
            ("Sand Zone - Save Point (Lower)", lambda state, player: True)
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
            ("Labyrinth I - Teleporter to Sand Zone", lambda state, player: True),
            ("Sand Zone - Outside Sand Zone Storehouse", lambda state, player: True)
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
            ("Sand Zone - Lower Side", lambda state, player: has_weapon(state, player) or (state.has("tricks;pacifist;1") and has_flight(state, player)) or state.has("tricks;pacifist;2")),
            ("Sand Zone - Exit to Sand Zone Storehouse", lambda state, player: True),
            ("Sand Zone - Refill (Lower)", lambda state, player: True),
            ("Sand Zone - Teleporter to Labyrinth I", lambda state, player: state.has("events;eventSandMazeTeleport;1") and remove_points_of_no_return(state, player))
        ],
        [
            # Locations
            ("Sand Zone - Puppy (Sleep)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone - Save Point (Lower)",
        [
            # Regions
            ("Sand Zone - Refill (Lower)", lambda state, player: True)
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
            ("Sand Zone - Refill (Upper)", lambda state, player: True)
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
            ("Sand Zone - Door to Sand Zone Residence", lambda state, player: True),
            ("Sand Zone Residence - Door to Small Room", lambda state, player: True),
            ("Sand Zone Residence - Before Curly", lambda state, player: True)
        ],
        [
            # Locations
            ("Sand Zone Residence - Curly Boss", lambda state, player: state.has("events;eventFightCurly;1") and (state.has("items;polarStar;1") or state.has("items;spur;1"))),
            # Events
        ]
    ),
    RegionData(
        "Sand Zone Residence - Door to Small Room",
        [
            # Regions
            ("Small Room - Door to Sand Zone Residence", lambda state, player: True),
            ("Sand Zone Residence - Door to Sand Zone", lambda state, player: True),
            ("Sand Zone Residence - Before Curly", lambda state, player: True)
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
            ("Curly", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;1") and state.has("items;supers;1") and state.has("items;missile;9")))
        ]
    ),
    RegionData(
        "Small Room - Door to Sand Zone Residence",
        [
            # Regions
            ("Sand Zone Residence - Door to Small Room", lambda state, player: True),
            ("Small Room - Refill", lambda state, player: True)
        ],
        [
            # Locations
            ("Small Room - Puppy (Curly)", lambda state, player: True),
            ("Small Room - Curly's Closet", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Small Room - Refill",
        [
            # Regions
            ("Small Room - Door to Sand Zone Residence", lambda state, player: True),
            ("Small Room - Save Point", lambda state, player: True)
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
            ("Small Room - Refill", lambda state, player: True)
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
            ("Sand Zone - Door to Jenka's House", lambda state, player: True),
            ("Jenka's House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Jenka's House - Jenka", lambda state, player: True),
            # Events
            ("Returned Puppies", lambda state, player: True)
        ]
    ),
    RegionData(
        "Jenka's House - Save Point",
        [
            # Regions
            ("Jenka's House - Door to Sand Zone", lambda state, player: True)
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
            ("Sand Zone - Door to Deserted House", lambda state, player: True),
            ("Deserted House - Save Point", lambda state, player: True)
        ],
        [
            # Locations
            ("Deserted House - Puppy (Dark)", lambda state, player: True),
            # Events
        ]
    ),
    RegionData(
        "Deserted House - Save Point",
        [
            # Regions
            ("Deserted House - Door to Sand Zone", lambda state, player: True)
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
            ("Sand Zone - Exit to Sand Zone Storehouse", lambda state, player: True),
            ("Sand Zone Storehouse - Before Toroko+", lambda state, player: True),
            ("Sand Zone Storehouse - Exit to Labyrinth I", lambda state, player: True)
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
            ("Toroko+", lambda state, player: can_kill_bosses(state, player) or (state.has("tricks;BossMissiles;2") and state.has("items;supers;1") and state.has("items;missile;13")) or (state.has("tricks;BossMissiles;4") and state.has("items;missiles;1") and state.has("items;missile;30")))
        ]
    ),
    RegionData(
        "Sand Zone Storehouse - Exit to Labyrinth I",
        [
            # Regions
            ("Labyrinth I - Entrance from Sand Zone Storehouse", lambda state, player: True)
        ],
        [
            # Locations
            # Events
        ]
    ),
]

