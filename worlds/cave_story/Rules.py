from typing import Dict, Callable

from BaseClasses import CollectionState

def has_mining_weapon(state: CollectionState, player: int) -> bool:
    return state.has_any({"Polar Star", "Progressive Missile Launcher"}, player)

REGION_RULES: Dict[str, Callable[[CollectionState], bool]] = {
    "Mimiga Village": lambda state, player: has_mining_weapon(state,player),
    "Mimiga Shack": lambda state, player: state.has("Silver Locket", player),
    "Arthur's House": lambda state, player: state.has("Arthur's Key", player),
    "Grasstown": lambda state, player: state.has("ID Card", player),
    #"Sand Zone": lambda state, player: state.has("Bomb", player),
    #"Labrinyth M" : lambda state, player: state.has("Cure-All", player),
}

LOCATION_RULES: Dict[str, Callable[[CollectionState], bool]] = {
    #"Malco's Gift" : lambda state, player: state.has("Gum Base", player),
}