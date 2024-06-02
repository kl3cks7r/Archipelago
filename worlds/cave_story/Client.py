import asyncio
import json
from typing import Tuple
from enum import Enum
from pathlib import Path
import subprocess
import sys
import os
import uuid
from .Patcher import *
from . import CaveStoryWorld

import Utils
from settings import FolderPath

from CommonClient import CommonContext, server_loop, gui_enabled, ClientCommandProcessor, logger, \
    get_base_parser

AP_OFFSET = 0xD00_000
CS_LOCATION_OFFSET = 7300
CS_COUNT_OFFSET = 7500
CS_DEATH_OFFSET = 7777
LOCATIONS_NUM = 69
BASE_UUID = uuid.UUID('00000000-0000-1111-0000-000000000000')

class CSPacket(Enum):
    READINFO = 0
    RUNTSC = 1
    READFLAGS = 2
    RUNEVENTS = 3
    READMEM = 4
    WRITEMEM = 5
    READSTATE = 6
    ERROR = 255
    DISCONNECT = 255

class CaveStoryClientCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_tsc(self, script: str) -> bool:
        """Execute the following TSC Comand"""
        if self.ctx.cs_streams:
            Utils.async_start(send_packet(self.ctx, encode_packet(CSPacket.RUNTSC, script)))
            return True
        return False
    
    def _cmd_cs_sync(self, script: str):
        """Force a sync to occur"""
        self.ctx.syncing = True

class CaveStoryContext(CommonContext):
    command_processor: int = CaveStoryClientCommandProcessor
    game = "Cave Story"
    items_handling = 0b001

    def __init__(self, args):
        super().__init__(args.connect, args.password)
        self.cs_streams: Tuple = None
        self.client_connected = False
        self.patched = asyncio.Event()
        self.game_watcher_task = None
        self.locations_vec = [False] * LOCATIONS_NUM
        self.offsets = None
        self.game_dir = CaveStoryWorld.settings.game_path
        if args.rcon_port:
            self.rcon_port = args.rcon_port
        else:
            self.rcon_port = 5451
        self.seed_name = None
        self.slot_num = None
        self.syncing = False
        self.slot_data = None
        self.victory = False
        self.finished_game = False

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(CaveStoryContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    
    def on_package(self, cmd: str, args: dict):
        if cmd == 'RoomInfo':
            self.seed_name = args['seed_name']
        elif cmd == 'Connected':
            # uuid_path = self.game_dir.joinpath('data\\uuid.txt')
            # with open(uuid_path) as f:
            #     uuid = f.read()
            # if uuid == '{00000000-0000-1111-0000-000000000000}':
            if not self.patched.is_set():
                self.slot_num = args['slot']
                Utils.async_start(self.send_msgs([
                    {"cmd": "LocationScouts",
                    "locations": self.server_locations,
                    "create_as_hint": 0}
                ]))
                self.slot_data = args['slot_data']
            else:
                launch_game(self)
        elif cmd == 'LocationInfo':
            if not self.patched.is_set():
                patch_game(self)
                launch_game(self)
        elif cmd == 'ReceivedItems':
            if self.patched.is_set():
                self.syncing = True

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class CaveStoryManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Cave Story Client"

        self.ui = CaveStoryManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

def encode_packet(pkt_type: CSPacket, data = None, addr: int = None):
    if not data:
        return pkt_type.value.to_bytes(1, 'little') + (b'\x00'*4)
    if pkt_type in (CSPacket.RUNTSC,):
        data_bytes = data.encode()
    elif pkt_type in (CSPacket.READFLAGS,CSPacket.RUNEVENTS,):
        data_bytes = b''
        for n in data:
            data_bytes = data_bytes + n.to_bytes(4, 'little')
    elif pkt_type in (CSPacket.READMEM,):
        data_bytes = addr.to_bytes(4, 'little') + data.to_bytes(2, 'little')
    elif pkt_type in (CSPacket.WRITEMEM,):
        data_bytes = addr.to_bytes(4, 'little')
        for b in data:
            data_bytes = data_bytes + b
    elif pkt_type in (CSPacket.READSTATE,):
        if data:
            data_bytes = data.to_bytes(1, 'little')
    return pkt_type.value.to_bytes(1, 'little') + len(data_bytes).to_bytes(4, 'little') + data_bytes

def decode_packet(ctx: CaveStoryContext, pkt_type: int, data_bytes: bytes, sync: bool=False):
    if pkt_type in (CSPacket.READINFO,):
        data = json.loads(data_bytes.decode())
        ctx.offsets = data['offsets']
        logger.info(f"Connected to \'{data['platform']}\' client using API v{data['api_version']} with UUID {data['uuid']}")
    elif pkt_type in (CSPacket.READFLAGS,):
        if sync:
            try:
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
                        new_bit_count = (~((count+1) << 8) & 0xFF00) + (count+1)
                        update_script = ''
                        for i, j in enumerate(range(15,-1,-1)):
                            if ((new_bit_count >> j) & 1) == 1:
                                update_script += f'<FL+{CS_COUNT_OFFSET+i:04}'
                            else:
                                update_script += f'<FL-{CS_COUNT_OFFSET+i:04}'
                        script = verify_script + update_script + f'<EVE{ctx.items_received[count].item-AP_OFFSET:04}'
                        return send_packet(ctx, encode_packet(CSPacket.RUNTSC, script))
                    else:
                        logger.debug('Sync completed!')
                        ctx.syncing = False
                        return send_packet(ctx, encode_packet(CSPacket.RUNTSC, '<FL-7777'))
                else:
                    logger.debug('Resetting Count')
                    update_script = ''
                    for i in range(15,-1,-1):
                        op = '+' if i < 8 else '-'
                        update_script += f'<FL{op}{CS_COUNT_OFFSET+i:04}'
                    script = update_script + '<END'
                    return send_packet(ctx, encode_packet(CSPacket.RUNTSC, script))
            except Exception as e:
                logger.debug(f'Syncing exception at line {e.__traceback__.tb_lineno}: {e}')
        else:
            locations_checked = []
            for i, b in enumerate(data_bytes):
                if i == LOCATIONS_NUM:
                    if b == 1:
                        ctx.syncing == True
                elif b == 1 and not ctx.locations_vec[i]:
                    ctx.locations_vec[i] = True
                    if i == LOCATIONS_NUM - 1:
                        ctx.victory = True
                    else:
                        locations_checked.append(AP_OFFSET+i)
            if len(locations_checked) > 0:
                return ctx.send_msgs([
                    {"cmd": "LocationChecks",
                    "locations": locations_checked}
                ])
    elif pkt_type in (CSPacket.READMEM,):
        # I don't think i'll use this??
        pass
    elif pkt_type in (CSPacket.READSTATE,):
        return data_bytes[0] == 2
    elif pkt_type in (CSPacket.ERROR,):
        data = data_bytes.decode()
        logger.info(f"Cave Story Error: {data}")
    return None

async def send_packet(ctx: CaveStoryContext, pkt: bytes, sync: bool=False):
    reader, writer = ctx.cs_streams
    writer.write(pkt)
    await asyncio.wait_for(writer.drain(), timeout=1.5)
    header = await asyncio.wait_for(reader.read(5), timeout=5)
    if header:
        pkt_type = CSPacket(header[0])
        length = int.from_bytes(header[1:4], 'little')
        if length > 0:
            data_bytes = await asyncio.wait_for(reader.read(length), timeout=5)
            return decode_packet(ctx, pkt_type, data_bytes, sync)
        else:
            data_bytes = None

def teardown(ctx, msg):
    logger.debug(msg)
    ctx.cs_streams = None
    ctx.client_connected = False

def patch_game(ctx):
    locations = []
    for loc, item in ctx.locations_info.items():
        if item.player == ctx.slot:
            player_name = None
            item_name = item.item-AP_OFFSET
        else:
            player_name = ctx.player_names[item.player]
            item_name = ctx.item_names[item.item]
        locations.append([loc-AP_OFFSET,player_name,item_name])
    if ctx.slot_num and ctx.seed_name:
        cs_uuid = uuid.uuid3(BASE_UUID,ctx.seed_name+str(ctx.slot_num))
    else:
        cs_uuid = None
    logger.info(f"Game Dir: {ctx.game_dir}")
    patch_files(locations, cs_uuid, Path(ctx.game_dir).expanduser(), ctx.slot_data, logger)
    ctx.patched.set()

def launch_game(ctx):
    logger.info("Starting Cave Story")
    exec_dir = Path(ctx.game_dir).expanduser().joinpath('freeware')
    exec_path = Path(exec_dir).joinpath('Doukutsu.exe')
    subprocess.Popen([exec_path], cwd=exec_dir)
    ctx.syncing = True

async def cave_story_connector(ctx: CaveStoryContext):
    await ctx.patched.wait()
    logger.info("Starting Cave Story connector")
    while not ctx.exit_event.is_set():
        try:
            if not ctx.client_connected:
                ctx.cs_streams = await asyncio.wait_for(asyncio.open_connection("localhost", ctx.rcon_port), timeout=4)
                if ctx.cs_streams:
                    await send_packet(ctx, encode_packet(CSPacket.READINFO))
                # TODO Check if running program's UUID, if mismatch tell user to restart CS and retry connection
                pass
                ctx.client_connected = True
                logger.info("Successfully connected to Cave Story")
            elif ctx.cs_streams:
                # Poll Cave Story for location flags
                task = await send_packet(ctx, encode_packet(
                    CSPacket.READFLAGS,
                    range(CS_LOCATION_OFFSET,CS_LOCATION_OFFSET+LOCATIONS_NUM+1)
                ))
                if task: await task
                if ctx.syncing and await send_packet(ctx, encode_packet(CSPacket.READSTATE)):
                    logger.debug("Attempting to sync")
                    task = await send_packet(ctx, encode_packet(
                        CSPacket.READFLAGS,
                        range(CS_COUNT_OFFSET,CS_COUNT_OFFSET+16)
                    ), True)
                    if task:
                        await task
                if ctx.victory and not ctx.finished_game:
                    ctx.finished_game = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
                # Pause between requests (and allow quiting!)
                try:
                    await asyncio.wait_for(ctx.exit_event.wait(), 1)
                except asyncio.TimeoutError:
                    continue
            else:
                teardown(ctx, "Woah, something weird happened!")
                continue
        except TimeoutError:
            teardown(ctx, "Connection Timed Out, Trying Again")
            continue
        except ConnectionRefusedError:
            teardown(ctx, "Connection Refused, Trying Again")
            continue
        except (ConnectionResetError, ConnectionAbortedError):
            teardown(ctx, "Connection Lost, Trying Again")
            continue

async def main(args):
    ctx = CaveStoryContext(args)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()
    ctx.game_watcher_task = asyncio.create_task(cave_story_connector(ctx), name="game connector")

    await ctx.exit_event.wait()
    ctx.server_address = None

    await ctx.shutdown()

    if ctx.game_watcher_task:
        await ctx.game_watcher_task

def launch():
    parser = get_base_parser(description="Cave Story Client, for text interfacing.")
    parser.add_argument('--rcon-port', default='5451', type=int, help='Port to use to communicate with CaveStory')
    args, rest = parser.parse_known_args()

    import colorama
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
