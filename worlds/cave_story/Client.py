import asyncio
import traceback
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

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

import Utils
# from Utils import is_windows
is_windows = True

from CommonClient import CommonContext, ClientCommandProcessor, \
    get_base_parser, server_loop, gui_enabled, logger
    

AP_OFFSET = 0xD00_000
CS_LOCATION_OFFSET = 7300
CS_COUNT_OFFSET = 7778
CS_DEATH_OFFSET = 7777
LOCATIONS_NUM = 69
BASE_UUID = uuid.UUID('00000000-0000-1111-0000-000000000000')
VERSION = 'v0.5'

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

class CSTrackerAutoTab(Enum):
    UNDEFINED = 0
    '''Includes all other rooms not covered (no tab switch)'''
    MIMIGA_VILLAGE = 1
    '''Includes Mimiga Village, First Cave, and Graveyard rooms'''
    EGG_CORRIDOR = 2
    '''Includes Egg Corridor and Ruined Egg Corridor rooms'''
    GRASSTOWN = 3
    '''Includes Grasstown rooms'''
    SAND_ZONE = 4
    '''Includes Sand Zone rooms'''
    LABYRINTH = 5
    '''Includes Labryinth, Core, and Waterway rooms'''
    PLANTATION = 6
    '''Includes Plantation, Outer Wall, and Last Cave rooms'''
    SACRED_GROUNDS = 7
    '''Includes Balcony and Sacred Grounds rooms'''

CS_TRACKER_AUTOTAB_MAP = {
    'Eggs' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EggX' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Egg6' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EggR' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EgEnd1' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Cthu' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Egg1' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Eggs2' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Cthu2' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EggR2' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EggX2' : CSTrackerAutoTab.EGG_CORRIDOR,
    'EgEnd2' : CSTrackerAutoTab.EGG_CORRIDOR,
    'Weed' : CSTrackerAutoTab.GRASSTOWN,
    'Santa' : CSTrackerAutoTab.GRASSTOWN,
    'Chako' : CSTrackerAutoTab.GRASSTOWN,
    'Shelt' : CSTrackerAutoTab.GRASSTOWN,
    'Malco' : CSTrackerAutoTab.GRASSTOWN,
    'WeedS' : CSTrackerAutoTab.GRASSTOWN,
    'WeedD' : CSTrackerAutoTab.GRASSTOWN,
    'Frog' : CSTrackerAutoTab.GRASSTOWN,
    'WeedB' : CSTrackerAutoTab.GRASSTOWN,
    'MazeI' : CSTrackerAutoTab.LABYRINTH,
    'Stream' : CSTrackerAutoTab.LABYRINTH,
    'MazeH' : CSTrackerAutoTab.LABYRINTH,
    'MazeW' : CSTrackerAutoTab.LABYRINTH,
    'MazeO' : CSTrackerAutoTab.LABYRINTH,
    'MazeD' : CSTrackerAutoTab.LABYRINTH,
    'MazeA' : CSTrackerAutoTab.LABYRINTH,
    'MazeB' : CSTrackerAutoTab.LABYRINTH,
    'MazeS' : CSTrackerAutoTab.LABYRINTH,
    'MazeM' : CSTrackerAutoTab.LABYRINTH,
    'Drain' : CSTrackerAutoTab.LABYRINTH,
    'Almond' : CSTrackerAutoTab.LABYRINTH,
    'River' : CSTrackerAutoTab.LABYRINTH,
    'Pixel' : CSTrackerAutoTab.LABYRINTH,
    'Pens1' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Mimi' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Cave' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Start' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Barr' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Pool' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Cemet' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Plant' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Comu' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'MiBox' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Mapi' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Pole' : CSTrackerAutoTab.MIMIGA_VILLAGE,
    'Oside' : CSTrackerAutoTab.PLANTATION,
    'Itoh' : CSTrackerAutoTab.PLANTATION,
    'Cent' : CSTrackerAutoTab.PLANTATION,
    'Jail1' : CSTrackerAutoTab.PLANTATION,
    'Momo' : CSTrackerAutoTab.PLANTATION,
    'Lounge' : CSTrackerAutoTab.PLANTATION,
    'CentW' : CSTrackerAutoTab.PLANTATION,
    'Jail2' : CSTrackerAutoTab.PLANTATION,
    'Priso1' : CSTrackerAutoTab.PLANTATION,
    'Priso2' : CSTrackerAutoTab.PLANTATION,
    'Little' : CSTrackerAutoTab.PLANTATION,
    'Hell4' : CSTrackerAutoTab.PLANTATION,
    'Clock' : CSTrackerAutoTab.PLANTATION,
    'Blcny1' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Ring1' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Ring2' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Prefa1' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Ring3' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Blcny2' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Prefa2' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Hell1' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Hell2' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Hell3' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Hell42' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Statue' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Ballo1' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Ostep' : CSTrackerAutoTab.SACRED_GROUNDS,
    'Sand' : CSTrackerAutoTab.SAND_ZONE,
    'Curly' : CSTrackerAutoTab.SAND_ZONE,
    'CurlyS' : CSTrackerAutoTab.SAND_ZONE,
    'Jenka1' : CSTrackerAutoTab.SAND_ZONE,
    'Dark' : CSTrackerAutoTab.SAND_ZONE,
    'Gard' : CSTrackerAutoTab.SAND_ZONE,
    'Jenka2' : CSTrackerAutoTab.SAND_ZONE,
}

class CSTrackerEvent(Enum):
    SAVED_SUE = 0
    '''Occurs when you talk to Sue in Egg Corridor'''
    SAVED_KAZUMA = 1
    '''Occurs after destroying the shelter door in Grasstown'''
    SAVED_CURLY = 2
    '''Occurs after Curly is carried through the Main Artery'''
    USED_MA_PIGNON = 3
    '''Occurs after feeding Curly Ma Pignon'''
    DEFEATED_BALROG_1 = 3
    '''Occurs after defeating Balrog in Mimiga Village'''
    DEFEATED_IGOR = 4
    '''Occurs after defeating Igor in Egg Corridor'''
    DEFEATED_BALROG_2 = 5
    '''Occurs after defeating Balrog in Power Room'''
    DEFEATED_BALFROG = 6
    '''Occurs after defeating Balfrog in Gum'''
    DEFEATED_CURLY = 7
    '''Occurs after defeating Curly in Sand Zone Residence'''
    DEFEATED_OMEGA = 8
    '''Occurs after defeating Omega in Sand Zone'''
    DEFEATED_TOROKO = 9
    '''Occurs after defeating Frenzied Toroko in Sand Zone Warehouse'''
    DEFEATED_PUU_BLACK = 10
    '''Occurs after defeating Puu Black in Old Clinic'''
    DEFEATED_MONSTER_X = 11
    '''Occurs after defeating Monster X in Labrynith'''
    DEFEATED_BALROG_3 = 12
    '''Occurs after defeating Balrog in Boulder Chamber'''
    DEFEATED_CORE = 13
    '''Occurs after defeating the Core'''
    DEFEATED_IRONHEAD = 14
    '''Occurs after defeating Ironhead in Main Artery'''
    DEFEATED_THE_SISTERS = 15
    '''Occurs after defeating The Sisters in Ruined Egg Observation Chamber'''
    DEFEATED_MA_PIGNON = 16
    '''Occurs after defeating Ma Pignon in Store Room'''
    DEFEATED_RED_DEMON = 17
    '''Occurs after defeating Red Demon in Hidden Last Cave'''
    FINAL_BOSS = 18
    '''Occurs after defeating Undead Core or Ballos (depending on goal)'''

class CaveStoryClientCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)
    
    def _cmd_cs_launch(self) -> bool:
        """Launches the game"""
        return launch_game(self.ctx)

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
    
    def _cmd_cs_platform(self, platform) -> bool:
        """Change the platform for Cave Story"""
        if platform in ('freeware','tweaked'):
            CaveStoryWorld.settings.game_platform = platform
            self.ctx.game_platform = platform
            if self.ctx.game_platform == 'freeware':
                logger.info(f"Changed Cave Story platform to 'freeware'")
                self.ctx.cs_button.text="Launch Cave Story Freeware"
            elif self.ctx.game_platform == 'tweaked':
                logger.info(f"Changed Cave Story platform to 'tweaked'")
                self.ctx.cs_button.text="Launch Cave Story Tweaked"
        else:
            logger.info(f"Unknown platform, please input 'freeware' or 'tweaked'")
            return False
        

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
        self.game_dir = Path(CaveStoryWorld.settings.game_dir).expanduser()
        self.game_platform = CaveStoryWorld.settings.game_platform
        self.game_process = None
        self.rcon_port = args.rcon_port
        self.seed_name = None
        self.slot_num = None
        self.team_num = None
        self.slot_data = None
        self.victory = False
        self.death = False
        self.poptracker_curlevel: CSTrackerAutoTab = CSTrackerAutoTab.UNDEFINED
        self.poptracker_events = [False] * len(CSTrackerEvent)
        logger.debug(f'Running version {VERSION}')
        Clock.schedule_once(self._add_cs_gui, 0)

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
        elif cmd == 'ReceivedItems':
            if game_ready(self):
                Utils.async_start(rcon_sync(self))

    def on_deathlink(self, data):
        super().on_deathlink(data)
        Utils.async_start(send_packet(self, encode_packet(CSPacket.RUNTSC, '<HMC<SOU0017<TRA:0000:0042:0000:0000')))

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

    def _add_cs_gui(self, _dt):
        # Create Cave Story button
        extra_layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(40),
        )
        if self.game_platform == 'freeware':
            self.cs_button = Button(text="Launch Cave Story Freeware")
        elif self.game_platform == 'tweaked':
            self.cs_button = Button(text="Launch Cave Story Tweaked")
        self.cs_button.bind(on_press=lambda inst: launch_game(self))
        # Insert it in the UI
        extra_layout.add_widget(self.cs_button)
        self.ui.grid.add_widget(extra_layout, index=0)
        
    def needs_patch(self) -> bool:
        if self.slot_num and self.seed_name:
            server_uuid = '{'+str(uuid.uuid3(BASE_UUID,self.seed_name+str(self.slot_num)))+'}'
            try:
                with open(self.game_dir.joinpath('pre_edited_cs', self.game_platform, 'data', 'uuid.txt')) as f:
                    client_uuid = f.read()
            except:
                client_uuid = BASE_UUID
            return client_uuid != server_uuid
        return False

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

async def send_packet(ctx: CaveStoryContext, pkt: bytes):
    if not ctx.cs_streams:
        raise Exception("Trying to send packet when there's no connection! This is bad!")
    # Communicating with RCON must be mutex since we assume that packets sent are met with the correct response
    async with ctx.send_lock:
        pkt_type = None
        length = None
        data_bytes = None
        try:
            # Unpack streams
            reader, writer = ctx.cs_streams
            # Send packet
            writer.write(pkt)
            await asyncio.wait_for(writer.drain(), timeout=1.5)
            # Receive response
            header = await asyncio.wait_for(reader.read(5), timeout=5)
            if header:
                # Parse header
                pkt_type = CSPacket(header[0])
                length = int.from_bytes(header[1:4], 'little')
                # Verify we are receiving the right response. This should never happen due to mutex
                if pkt_type != CSPacket(pkt[0]):
                    raise Exception("Unexpected Packet Response")
                # Parse Data
                if length > 0:
                    data_bytes = await asyncio.wait_for(reader.read(length), timeout=5)
                # Log error packets
                if pkt_type in (CSPacket.ERROR,):
                    data = data_bytes.decode()
                    logger.debug(f"Cave Story RCON Error: {data}")
                # Return data bytes
                return data_bytes
            else:
                raise Exception("Bad Header Response")
        except Exception as e:
            logger.debug(f"Failed to send packet: {e}")
            if pkt_type and length and data_bytes:
                logger.debug(f"({pkt} -> {pkt_type}|{length}|{data_bytes})")
            ctx.cs_streams = None

def game_running(ctx):
    return ctx.game_process and ctx.game_process.poll() is None

async def game_ready(ctx):
    if game_running(ctx) and ctx.cs_streams and ctx.server and ctx.server.socket and not ctx.server.socket.closed:
        status = await send_packet(ctx, encode_packet(CSPacket.READSTATE))
        if status:
            return int(status[0]) in range(2,8,1)
    return False

def patch_game(ctx):
    try:
        locations = []
        for loc, item in ctx.locations_info.items():
            if item.player == ctx.slot:
                player_name = None
                item_name = item.item-AP_OFFSET
            else:
                player_name = ctx.player_names[item.player]
                item_name = ctx.item_names[item.item]
            locations.append([loc-AP_OFFSET,player_name,item_name])
        cs_uuid = '{'+str(uuid.uuid3(BASE_UUID,ctx.seed_name+str(ctx.slot_num)))+'}'
        patch_files(locations, cs_uuid, ctx.game_dir, ctx.game_platform, ctx.slot_data, logger)
        return True
    except Exception as e:
        logger.info(f"Patching Failed! {e}, please reconnect to retry!")
        logger.info(f"{traceback.print_exc()}")
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

async def rcon_sync(ctx):
    # If we are already syncing ignore additional requests
    if ctx.sync_lock.locked():
        return
    async with ctx.sync_lock:
        while not ctx.exit_event.is_set():
            if not ctx.death and await game_ready(ctx):
                logger.debug("Attempting to sync with Cave Story")
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
                            item_script = f"\r\n<PRI<MSG<TURGot Refill Station<WAIT0025<NOD<END<LI+<AE+\r\n"
                        elif item_id < 100:
                            # Normal items
                            item_script = f'<EVE{item_id:04}'
                        elif item_id == 110:
                            # Black Wind Trap
                            item_script = f"\r\n<PRI<MSG<TURYou feel a black wind...<WAIT0025<NOD<END<ZAM\r\n"
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
            else:
                await asyncio.sleep(3)

async def cr_connect(ctx):
    while not ctx.exit_event.is_set():
        if game_running(ctx):
            if ctx.cs_streams:
                # await not ctx.cs_streams
                pass
            else:
                try:
                    ctx.cs_streams = await asyncio.open_connection("localhost", ctx.rcon_port)
                    if not ctx.cs_streams:
                        raise Exception
                    data_bytes = await send_packet(ctx, encode_packet(CSPacket.READINFO))
                    if not data_bytes:
                        raise Exception
                    data = json.loads(data_bytes.decode())
                    ctx.offsets = data['offsets']
                    logger.debug(f"Connected to \'{data['platform']}\' client using API v{data['api_version']} with UUID {data['uuid']}")
                    if ctx.needs_patch():
                        ctx.cs_streams = None
                        logger.info("Current Cave Story session does not belong to the connected Archipelago server! Please restart Cave Story")
                        while game_running(ctx):
                            await asyncio.sleep(3)
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
                        if ctx.slot_data['deathlink']:
                            Utils.async_start(ctx.send_death(ctx))
                    elif b == 0 and ctx.death:
                        logger.debug('Reloaded, permitting sync')
                        # await connector_receive_items() uh why is this here?
                        ctx.death = False
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
