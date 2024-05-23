from Options import AssembleOptions, Toggle, Range, Choice, Option
import typing

class Difficulty(Choice):
    """Sets overall game difficulty."""
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1  # default to normal

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

# By convention we call the options dict variable `<world>_options`.
cave_story_options: typing.Dict[str, AssembleOptions] = {
    "goal": Goal,
    "difficulty": Difficulty,
    #"deathlink": Deathlink,
}