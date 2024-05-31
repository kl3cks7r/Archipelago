from __future__ import annotations

import ModuleUpdate
ModuleUpdate.update()

from worlds.cave_story.Client import launch
import Utils

if __name__ == "__main__":
    Utils.init_logging("CaveStoryClient", exception_logger="Client")
    launch()
