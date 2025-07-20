import asyncio
import subprocess
import traceback

from Utils import is_windows

from CommonClient import logger

from .Constants import *
from .Patcher import *
from .Connector import *

def game_running(ctx):
    if ctx.game_process and ctx.game_process.poll() is None:
        return True
    elif ctx.ignore_process:
        return True
    else:
        return False 

def launch_game(ctx):
    if not game_running(ctx):
        if ctx.needs_patch():
            logger.info(f"UUID mismatch, patching files")
            patch_game(ctx)
        logger.info("Launching Cave Story")
        exe_dir = ctx.game_dir.joinpath('pre_edited_cs', ctx.game_platform)
        if ctx.game_platform == "freeware":
            exe_path = exe_dir.joinpath('Doukutsu.exe')
        elif ctx.game_platform == "tweaked":
            if is_windows:
                exe_path = exe_dir.joinpath('CSTweaked.exe')
            else:
                exe_path = exe_dir.joinpath('CSTweaked')
        else:
            raise Exception("Unknown Platform!")
        try:
            ctx.game_process = subprocess.Popen([exe_path], cwd=exe_dir)
            return True
        except Exception as e:
            logger.info(f"Launching Failed: {e}")
            return False
    else:
        logger.info(f"Game is already Running!")
        return True
    
def patch_game(ctx):
    try:
        locations = []
        for loc, item in ctx.locations_info.items():
            if item.player == ctx.slot:
                player_name = None
                item_name = item.item-AP_OFFSET
            else:
                player_name = ctx.player_names[item.player]
                item_name = ctx.item_names.lookup_in_slot(item.item, item.player) # per-game ids should work here?
            locations.append([loc-AP_OFFSET,player_name,item_name])
        cs_uuid = '{'+str(uuid.uuid3(BASE_UUID,ctx.seed_name+str(ctx.slot_num)))+'}'
        patch_files(locations, cs_uuid, ctx.game_dir, ctx.game_platform, ctx.slot_data, logger)
        return True
    except Exception as e:
        logger.info(f"Patching Failed! {e}, please reconnect to retry!")
        logger.info(f"{traceback.print_exc()}")
        return False