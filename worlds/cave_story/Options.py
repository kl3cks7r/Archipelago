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

# class Deathlink(Toggle):
#     """When you die, everyone dies. Of course the reverse is true too."""
#     display_name = "Deathlink"

@dataclass
class CaveStoryOptions(PerGameCommonOptions):
    goal: Goal