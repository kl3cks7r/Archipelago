from Options import AssembleOptions, Toggle, Range, Choice, Option, PerGameCommonOptions
from dataclasses import dataclass
import typing

class Goal(Choice):
    """Sets which ending completes your goal."""
    display_name = "Goal"
    option_bad = 0
    option_normal = 1
    alias_neutral = 1
    option_best = 2
    default = 2  # default to best

class NoFallingBlocks(Toggle):
    """Disables falling blocks in Sacred Grounds: B2"""
    display_name = "No Falling Blocks"
    default = False

class EarlyWeapon(Toggle):
    """Ensures a weapon is placed early in your world"""
    display_name = "Early Weapon"
    default = True

class StartingLocation(Choice):
    display_name = "Starting Location"
    option_start_point = 0
    option_arthurs_house = 1
    option_camp = 2
    default = 1

class ExcludeHellLocations(Toggle):
    """Prevents any progression items from appearing in Sacred Grounds"""
    display_name = "Exclude Hell Locations"
    default = True

class Deathlink(Toggle):
    """When you die, everyone dies. Of course the reverse is true too."""
    display_name = "Deathlink"
    default = False

@dataclass
class CaveStoryOptions(PerGameCommonOptions):
    goal: Goal
    starting_location: StartingLocation
    early_weapon: EarlyWeapon
    deathlink: Deathlink
    exclude_hell: ExcludeHellLocations
    no_blocks: NoFallingBlocks