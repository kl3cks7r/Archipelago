import asyncio
import subprocess
import traceback

from Utils import is_windows

from CommonClient import logger

from .Constants import *
from .Patcher import *
from .Connector import *

from .. import CaveStoryWorld

def game_running(ctx):
    if ctx.game_process and ctx.game_process.poll() is None:
        return True
    elif CaveStoryWorld.settings['ignore_process']:
        return True
    else:
        return False 

def launch_game(ctx, tweaked):
    game_dir = Path(CaveStoryWorld.settings['game_dir']).expanduser()
    if not game_running(ctx):
        if needs_patch(ctx, tweaked):
            logger.info(f"UUID mismatch, patching files")
            patch_game(ctx, tweaked)    
        logger.info("Launching Cave Story")
        
        if tweaked:
            exe_dir = game_dir.joinpath('pre_edited_cs', 'tweaked')
            if is_windows:
                exe_path = exe_dir.joinpath('CSTweaked.exe')
            else:
                exe_path = exe_dir.joinpath('CSTweaked')
        else:
            exe_dir = game_dir.joinpath('pre_edited_cs', 'freeware')
            if is_windows:
                exe_path = exe_dir.joinpath('Doukutsu.exe')
            else:
                logger.error("Please use Tweaked for Non-Windows platforms!")
        try:
            ctx.game_process = subprocess.Popen([exe_path], cwd=exe_dir)
            return True
        except Exception as e:
            logger.info(f"Launching Failed: {e}")
            return False
    else:
        logger.info(f"Game is already Running!")
        return True

def needs_patch(ctx, tweaked) -> bool:
    game_dir = Path(CaveStoryWorld.settings['game_dir']).expanduser()
    if ctx.slot_num and ctx.seed_name:
        server_uuid = '{'+str(uuid.uuid3(BASE_UUID,ctx.seed_name+str(ctx.slot_num)))+'}'
        try:
            with open(game_dir.joinpath('pre_edited_cs', 'tweaked' if tweaked else 'freeware', 'data', 'uuid.txt')) as f:
                client_uuid = f.read()
        except:
            client_uuid = BASE_UUID
        return client_uuid != server_uuid
    return False

def patch_game(ctx, tweaked):
    game_dir = Path(CaveStoryWorld.settings['game_dir']).expanduser()
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
        patch_files(locations, cs_uuid, game_dir, tweaked, ctx.slot_data, logger)
        return True
    except Exception as e:
        logger.info(f"Patching Failed! {e}, please reconnect to retry!")
        logger.info(f"{traceback.print_exc()}")
        return False