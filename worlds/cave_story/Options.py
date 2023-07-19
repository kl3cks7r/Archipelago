from Options import AssembleOptions, Toggle, Range, Choice, Option
import typing

class Difficulty(Choice):
    """Sets overall game difficulty."""
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1  # default to normal

# By convention we call the options dict variable `<world>_options`.
cave_story_options: typing.Dict[str, AssembleOptions] = {
    "difficulty": Difficulty,
}