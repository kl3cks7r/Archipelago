import asyncio

import json
from typing import Tuple
from enum import Enum
from pathlib import Path
import uuid

from worlds.cave_story import CaveStoryWorld

from .Enums import CSPacket, CSTrackerAutoTab, CSTrackerEvent
from .ClientGui import start_gui
from .Constants import *
from .Patcher import *
from .Connector import *
from .Protocol import *

import Utils

from CommonClient import CommonContext, ClientCommandProcessor, \
    get_base_parser, server_loop, gui_enabled, logger


class CaveStoryClientCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_cs_tsc(self, script: str) -> bool:
        """Execute the following TSC Comand"""
        logger.info(f"Executing TSC command: {script}")
        if self.ctx.cs_streams:
            Utils.async_start(send_packet(self.ctx, encode_packet(CSPacket.RUNTSC, script)))
            return True
        return False
    
    def _cmd_cs_sync(self) -> bool:
        """Force a sync to occur"""
        Utils.async_start(rcon_sync(self.ctx))
        return True
        

class CaveStoryContext(CommonContext):
    command_processor: int = CaveStoryClientCommandProcessor
    game = "Cave Story"
    items_handling = 0b101

    def __init__(self, args):
        super().__init__(args.connect, args.password)
        self.cs_streams: Tuple = None
        self.send_lock: asyncio.Lock = asyncio.Lock()
        self.sync_lock: asyncio.Lock = asyncio.Lock()
        self.locations_vec = [False] * LOCATIONS_NUM
        self.offsets = None
        self.game_process = None
        self.tweaked = False
        self.rcon_port = args.rcon_port
        self.seed_name = None
        self.slot_num = None
        self.team_num = None
        self.slot_data = None
        self.victory = False
        self.death = False
        self.death_from_deathlink = False
        self.poptracker_curlevel: CSTrackerAutoTab = CSTrackerAutoTab.UNDEFINED
        self.poptracker_events = [False] * len(CSTrackerEvent)
        logger.debug(f'Running version {VERSION}')

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(CaveStoryContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    
    def on_package(self, cmd: str, args: dict):
        if cmd == 'RoomInfo':
            self.seed_name = args['seed_name']
        elif cmd == 'Connected':
            self.slot_num = args['slot']
            self.team_num = args['team']
            self.slot_data = args['slot_data']
            Utils.async_start(self.send_msgs([
                {"cmd": "LocationScouts",
                "locations": self.server_locations,
                "create_as_hint": 0}
            ]))
            if self.slot_data['deathlink']:
                Utils.async_start(self.send_msgs([
                    {"cmd": "ConnectUpdate",
                     "tags": ["DeathLink"]}]))
        elif cmd == 'ReceivedItems':
            Utils.async_start(rcon_sync(self))

    def on_deathlink(self, data):
        super().on_deathlink(data)
        self.death_from_deathlink = True
        Utils.async_start(send_packet(self, encode_packet(CSPacket.RUNTSC, '<HMC<SOU0017<WAI0020<FAO0003<TRA0000:0042:0000:0000')))
    def run_gui(self):
        start_gui(self)



def game_running(ctx):
    if ctx.game_process and ctx.game_process.poll() is None:
        return True
    elif CaveStoryWorld.settings['ignore_process']:
        return True
    else:
        return False 

async def game_ready(ctx):
    if ctx.cs_streams and ctx.server and ctx.server.socket and not ctx.server.socket.closed:
        status = await send_packet(ctx, encode_packet(CSPacket.READSTATE))
        if status:
            return int(status[0]) in range(2,8,1)
    return False

async def rcon_sync(ctx):
    # If we are already syncing ignore additional requests
    if ctx.sync_lock.locked():
        return
    async with ctx.sync_lock:
        while not ctx.exit_event.is_set():
            if not ctx.death and await game_ready(ctx):
                data_bytes = await send_packet(ctx, encode_packet(
                    CSPacket.READFLAGS,
                    range(CS_COUNT_OFFSET,CS_COUNT_OFFSET+16)
                ))
                if not data_bytes:
                    continue
                bit_count = 0
                verify_script = ''
                for i, b in enumerate(data_bytes):
                    bit_count <<= 1
                    bit_count += b
                    if b == 0x00:
                        verify_script += f'<FLJ{CS_COUNT_OFFSET+i:04}:0000'
                # logger.debug(f'Bit Count:{bit_count:016b}')
                if (~bit_count & 0xFF) == (bit_count >> 8):
                    count = bit_count & 0xFF
                    if count != len(ctx.items_received):
                        logger.debug("Items received differs, sending items")
                        new_bit_count = (~((count+1) << 8) & 0xFF00) + (count+1)
                        update_script = ''
                        for i, j in enumerate(range(15,-1,-1)):
                            if ((new_bit_count >> j) & 1) == 1:
                                update_script += f'<FL+{CS_COUNT_OFFSET+i:04}'
                            else:
                                update_script += f'<FL-{CS_COUNT_OFFSET+i:04}'
                        item_id = ctx.items_received[count].item-AP_OFFSET
                        if item_id == 17:
                            # Refill Station
                            item_script = f"\r\n<PRI<MSG<TURGot Refill Station<WAI0025<NOD<END<LI+<AE+\r\n"
                        elif item_id < 100:
                            # Normal items
                            item_script = f'<EVE{item_id:04}'
                        elif item_id == 110:
                            # Black Wind Trap
                            item_script = f"\r\n<PRI<MSG<TURYou feel a black wind...<WAI0025<NOD<END<ZAM\r\n"
                        script = verify_script + update_script + item_script
                        await send_packet(ctx, encode_packet(CSPacket.RUNTSC, script))
                    else:
                        logger.debug('Sync completed!')
                        return
                else:
                    logger.debug('Resetting Count')
                    update_script = ''
                    for i in range(15,-1,-1):
                        op = '+' if i < 8 else '-'
                        update_script += f'<FL{op}{CS_COUNT_OFFSET+i:04}'
                    script = update_script + '<END'
                    await send_packet(ctx, encode_packet(CSPacket.RUNTSC, script))
            await asyncio.sleep(1)

async def cr_connect(ctx):
    while not ctx.exit_event.is_set():
        if game_running(ctx):
            if not ctx.cs_streams:
                try:
                    ctx.cs_streams = await asyncio.open_connection("localhost", ctx.rcon_port)
                    if not ctx.cs_streams:
                        raise Exception
                    data_bytes = await send_packet(ctx, encode_packet(CSPacket.READINFO))
                    if not data_bytes:
                        raise Exception
                    data = json.loads(data_bytes.decode())
                    ctx.offsets = data['offsets']
                    logger.info(f"Connected to \'{data['platform']}\' game using API v{data['api_version']} with UUID {data['uuid']}")
                    if needs_patch(ctx, ctx.tweaked):
                        ctx.cs_streams = None
                        logger.info("Current Cave Story session does not belong to the connected Archipelago server! Please restart Cave Story")
                        while game_running(ctx):
                            if ctx.exit_event.is_set():
                                break
                            await asyncio.sleep(1)
                        continue
                    await ctx.send_msgs([{"cmd": "Sync"}])
                    Utils.async_start(rcon_sync(ctx))
                except Exception as e:
                    logger.info(f"Failed to connect to currently running game: {e}, retrying in 5 seconds")
                    await asyncio.sleep(5)
        await asyncio.sleep(1)

async def cr_sendables(ctx):
    while not ctx.exit_event.is_set():
        if await game_ready(ctx):
            data_bytes = await send_packet(ctx, encode_packet(
                CSPacket.READFLAGS,
                [*range(CS_LOCATION_OFFSET,CS_LOCATION_OFFSET+LOCATIONS_NUM),7777]
            ))
            if not data_bytes:
                continue
            locations_checked = []
            for i, b in enumerate(data_bytes):
                if i == LOCATIONS_NUM:
                    if b == 1 and not ctx.death:
                        logger.debug('Death detected from Client')
                        ctx.death = True
                        if ctx.slot_data['deathlink'] and not ctx.death_from_deathlink:
                            Utils.async_start(ctx.send_death(death_text=f"{ctx.player_names[ctx.slot_num]} fell prey to the Demon Crown!"))
                    elif b == 0 and ctx.death:
                        logger.debug('Reloaded, syncing')
                        ctx.death = False
                        ctx.death_from_deathlink = False
                        Utils.async_start(rcon_sync(ctx))
                elif b == 1 and not ctx.locations_vec[i]:
                    ctx.locations_vec[i] = True
                    if i == LOCATIONS_NUM - 1:
                        ctx.victory = True
                    else:
                        locations_checked.append(AP_OFFSET+i)
            if len(locations_checked) > 0:
                await ctx.send_msgs([
                    {"cmd": "LocationChecks",
                    "locations": locations_checked}
                ])
            if ctx.victory and not ctx.finished_game:
                ctx.finished_game = True
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
        await asyncio.sleep(1)

async def cr_autotab(ctx):
    while not ctx.exit_event.is_set():
        if await game_ready(ctx):
            data_bytes = await send_packet(ctx, encode_packet(
                CSPacket.READSTATE,
                1
            ))
            if not data_bytes:
                continue
            try:
                autotab = CS_TRACKER_AUTOTAB_MAP[data_bytes.decode()]
            except KeyError:
                autotab = CSTrackerAutoTab.UNDEFINED
            try:
                if ctx.poptracker_curlevel != autotab:
                    ctx.poptracker_curlevel = autotab
                    logger.debug(f"Switching Tab: {autotab.value}")
                    team = ctx.team_num if ctx.team_num else 0
                    slot = ctx.slot_num if ctx.slot_num else 0
                    await ctx.send_msgs([
                        {"cmd": "Set",
                        "key": f"cavestory_currentlevel_{team}_{slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "replace", "value": autotab.value}]}
                    ])
            except Exception as e:
                logger.info(f"Caught Exception: {e}")
        await asyncio.sleep(1)

async def main(args):
    ctx = CaveStoryContext(args)
    # Server task. Needs to run first in order for ctx to properly be set up
    server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    # Client tasks
    coroutines = [server_task, cr_connect(ctx), cr_sendables(ctx), cr_autotab(ctx)]
    # Run everything
    try:
        await asyncio.gather(*coroutines)
    except asyncio.CancelledError:
        pass
    finally:
        await ctx.shutdown()

def launch():
    parser = get_base_parser(description="Cave Story Client, for text interfacing.")
    parser.add_argument('--rcon-port', default='5451', type=int, help='Port to use to communicate with CaveStory')
    args, rest = parser.parse_known_args()

    Utils.init_logging("CaveStoryClient", exception_logger="Client")
    import colorama
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
