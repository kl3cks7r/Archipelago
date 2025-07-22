# This adapts some code from patcher.py from the project cave-story-randomizer, licensed under zlib
# Please see: https://github.com/cave-story-randomizer/cave-story-randomizer/blob/master/LICENSE

from pathlib import Path
from typing import Callable, Optional
import shutil
import struct
import random
from collections import defaultdict

from .. import CaveStoryWorld

from .Constants import LOC_TSC_EVENTS, AP_SPRITE

class Tsc:
    def __init__(self, raw_tsc):
        tsc_vec = raw_tsc.split('#')
        tsc_map = dict()
        for i in range(len(tsc_vec)):
            event = tsc_vec[i][:4]
            if i != 0:
                tsc_vec[i] = [event,tsc_vec[i][4:]]
                tsc_map.update({event:i})
        self.vec = tsc_vec
        self.map = tsc_map

    def set_event(self, event, script):
        self.vec[self.map[event]][1] = script

    def get_string(self):
        result = ''
        for s in self.vec:
            if isinstance(s, list):
                result += '#' + s[0] + s[1]
            else:
                result += s
        return result
    
class Npc:
    def __init__(self, x, y, flag_number, event_number, npc_type, attributes):
        self.x = x
        self.y = y
        self.flag_number = flag_number
        self.event_number = event_number
        self.type = npc_type
        self.attributes = attributes
    def __repr__(self):
        return (f"Npc(({self.x}, {self.y}), F={self.flag_number}, E={self.event_number}, T={self.type}, A={self.attributes:04x})")

def patch_files(locations, uuid, game_dir: Path, tweaked: bool, slot_data, logger):    
    logger.info("Copying base files...")
    base_dir = game_dir.joinpath('pre_edited_cs', "data")
    dest_dir = game_dir.joinpath('pre_edited_cs', 'tweaked' if tweaked else 'freeware', "data")
    try:
        shutil.copytree(base_dir, dest_dir, dirs_exist_ok=True, ignore=(lambda _dir, files: [file for file in files if file[-3:] in ('txt')]))
    except shutil.Error:
        raise Exception("Error copying base files. Ensure the directory is not read-only, and that Doukutsu.exe is closed")

    scripts = defaultdict(list)
    booster_placed = False
    for loc, player, item in locations:
        if player:
            for c in ('#','<','='):
                player = player.replace(c, '?')
                item = item.replace(c, '?')
            if not tweaked:
                gfx = '<GIT1045'
            else:
                gfx = ''
            tsc_script = "\r\n<PRI<MSG<TUR" + gfx + "\r\n"+f"Got {player}'s ={item}=!"+"<WAI0025<NOD<END<EVE0015\r\n"
        else:
            if item < 100:
                # Regular Items
                tsc_script = f"\r\n<EVE{item:04d}\r\n"
            elif item == 110:
                # Black Wind Trap
                tsc_script = f"\r\n<PRI<MSG<TURYou feel a black wind...<WAI0025<NOD<END<ZAM<EVE0015\r\n"
        map_name, tsc_event_num, npc_event_num = LOC_TSC_EVENTS[loc]
        # Health Canister
        if item in (12,13,14,):
            new_npc = 32
        # Puppy
        elif item == 20:
            new_npc = 130
        # Dead Booster
        elif not booster_placed and item == 68:
            new_npc = 167
            booster_placed = True
        # Health Refill
        elif item == 17:
            new_npc = 17
        else:
            npc_event_num = ''
            new_npc = 0
        if npc_event_num != '':
            logger.debug(f"Attempting to set NPC {npc_event_num} in {map_name} to {new_npc}")
        scripts[map_name].append((tsc_event_num,tsc_script,npc_event_num,new_npc))
    # Victory stuff is super hacky atm
    # 6003: Bad | 6000: Normal | 6001: Best | 6002: All Bosses | 6004: 100%
    # Goal flags
    goal = slot_data['goal']
    goal_flags = ''
    if goal == 0:
        goal_flags = '<FL+6003'
    elif goal == 1:
        goal_flags = '<FL+6000'
    elif goal == 2:
        goal_flags = '<FL+6001'
    # Starting locations
    if slot_data['start'] == 0:
        # First Cave
        start_room = '<FL+6200<EVE0091'
    elif slot_data['start'] == 1:
        # Arthur's House
        start_room = '<FL+0301<FL+0302<FL+1641<FL+1642<FL+0320<FL+0321<TRA0001:0094:0017:0008'
    else:
        # Camp
        start_room = '<FL+0301<FL+0302<FL+1641<FL+1642<FL+0320<FL+0321<FL+6201<FL+6202<TRA0040:0092:0004:0005'
    if slot_data['no_blocks']:
        no_blocks = '<FL+1351'
    else:
        no_blocks = ''
    # Flags for the starting point
    softlock_flags = '<MP+0040<MP+0043<MP+0057<MP+0006<MP+0053<MP+0032<MP+0033<MP+0036'
    tp_flags = '<PS+0001:6001<PS+0002:6002<PS+0003:6003<PS+0004:6004<PS+0005:6005'
    hp_counter_flags = '<FL+4011<FL+4012<FL-4013<FL-4014<FL-4015<FL-4016' # 6-bit binary number for 3
    # Rocket Skip
    extra = '<FL+6400'
    scripts['Start'].append(('0201',f'\r\n{goal_flags}\r\n{tp_flags}{hp_counter_flags}{no_blocks}{softlock_flags}{extra}\r\n{start_room}\r\n','',0))
    # Victory flags
    if goal == 0:
        tsc_path = dest_dir.joinpath("Stage", "Oside.tsc")
        tsc = Tsc(decode_tsc(tsc_path))
        tsc.vec[tsc.map['0402']][1] = '\r\n<FL+7368' + tsc.vec[tsc.map['0402']][1]
        encode_tsc(tsc_path,tsc.get_string())
    else:
        tsc_path = dest_dir.joinpath("Stage", "Island.tsc")
        tsc = Tsc(decode_tsc(tsc_path))
        if goal == 1:
            tsc.vec[tsc.map['0100']][1] = '\r\n<FL+7368' + tsc.vec[tsc.map['0100']][1]
        elif goal == 2:
            tsc.vec[tsc.map['0110']][1] = '\r\n<FL+7368' + tsc.vec[tsc.map['0110']][1]
        encode_tsc(tsc_path,tsc.get_string())
    # Patch all maps in scripts
    for map_name, events in scripts.items():
        tsc_path = dest_dir.joinpath("Stage", f"{map_name}.tsc")
        tsc = Tsc(decode_tsc(tsc_path))
        pxe_path = dest_dir.joinpath("Stage", f"{map_name}.pxe")
        npcs = decode_pxe(pxe_path)
        for tsc_event, script, npc_event, npc_num in events:
            try:
                tsc.set_event(tsc_event,script)
                if npc_event != '':
                    for npc in npcs:
                        if npc_event == f"{npc.event_number:04}":
                            # If NPC is a Refill Station or the replaced NPC is Sparkle
                            if npc_num in (17,) or npc.type in (70,):
                                logger.debug(f"Set NPC {npc.event_number:04}({npc.type}) in {map_name} to {npc_num}")
                                npc.type = npc_num
            except KeyError:
                logger.debug(f"Error finding Event #{tsc_event} in {map_name}.tsc")
        encode_tsc(tsc_path,tsc.get_string())
        encode_pxe(pxe_path,npcs)
    # Death detection
    tsc_path = dest_dir.joinpath("Head.tsc")
    tsc = Tsc(decode_tsc(tsc_path))
    # tsc.vec[tsc.map['0016']][1] = '\r\n<FL+7777' + tsc.vec[tsc.map['0016']][1]
    tsc.vec[tsc.map['0040']][1] = '\r\n<FL+7777' + tsc.vec[tsc.map['0040']][1]
    tsc.vec[tsc.map['0041']][1] = '\r\n<FL+7777' + tsc.vec[tsc.map['0041']][1]
    tsc.vec[tsc.map['0042']][1] = '\r\n<FL+7777' + tsc.vec[tsc.map['0042']][1]
    encode_tsc(tsc_path,tsc.get_string())
    # AP sprite
    if not tweaked:
        patch_ap_sprite(dest_dir)
    # Hash and UUID
    logger.info("Copying hash and uuid...")
    random.seed(uuid)
    hash = ",".join([f"{num:04d}" for num in [random.randint(1, 38) for _ in range(5)]])
    dest_dir.joinpath("hash.txt").write_text(hash)
    dest_dir.joinpath("uuid.txt").write_text(uuid)
    logger.info(f"Done! Patching took {0} seconds")

def patch_ap_sprite(path):
    with open(path.joinpath('ItemImage.bmp'), "rb") as f:
        file_data = bytearray(f.read())

    for j in range(16):
        for i in range(15):
            file_data[0x8A+256*(16*2+j)+(32*5)+9+i] = AP_SPRITE[i+15*(15-j)]

    with open(path.joinpath('ItemImage.bmp'), "wb") as f:
        f.write(file_data)

def patch_mychar(game_dir: Path, char: str):
    import pkgutil
    char_data = pkgutil.get_data(CaveStoryWorld.__module__, f"assets/mychar/{char}.bmp")
    char2x_data = pkgutil.get_data(CaveStoryWorld.__module__, f"assets/mychar/2x/{char}.bmp")
    game_dir.joinpath('pre_edited_cs', 'freeware', 'data', 'MyChar.bmp').write_bytes(char_data)
    game_dir.joinpath('pre_edited_cs', 'tweaked', 'data', 'MyChar.bmp').write_bytes(char_data)
    game_dir.joinpath('pre_edited_cs', 'tweaked', 'data', 'sprites_up', 'MyChar.bmp').write_bytes(char2x_data)

def decode_tsc(path):
    with open(path,'rb') as f:
        tsc = f.read()
        f.close()
        key = len(tsc)//2
        shift = tsc[key]
        res = ''
        for x in tsc[:key]:
            res += chr((x - shift) % 256)
        res += chr(shift)
        for x in tsc[key+1:]:
            res += chr((x - shift) % 256)
    return res

def encode_tsc(path, tsc):
    with open(path,'wb') as f:
        key = len(tsc)//2
        shift = ord(tsc[key])
        res = b''
        for x in tsc[:key]:
            res += bytes([(ord(x) + shift) % 256])
        res += bytes([shift])
        for x in tsc[key+1:]:
            res += bytes([(ord(x) + shift) % 256])
        f.write(res)
        f.close()

def decode_pxe(path):
    with open(path, 'rb') as f:
        header = f.read(4)
        if header != b'PXE\0':
            raise ValueError("Invalid PXE: Header does not match 'PXE\\0'")

        count_bytes = f.read(4)
        count = struct.unpack('<I', count_bytes)[0]

        npcs = []
        for _ in range(count):
            # Each object consists of 6 tuples of 2-byte numbers (little-endian)
            object_bytes = f.read(12)
            if len(object_bytes) < 12:
                raise ValueError("File ends unexpectedly, data structure incomplete.")
            data = struct.unpack('<6H', object_bytes)  # 6 unsigned shorts (2 bytes each)
            game_event = Npc(*data)
            npcs.append(game_event)
        f.close()
    return npcs
    

def encode_pxe(path, npcs):
    with open(path, 'wb') as f:
        f.write(b'PXE\0')
        count = len(npcs)
        f.write(struct.pack('<I', count))
        for npc in npcs:
            packed_data = struct.pack('<6H', npc.x, npc.y, npc.flag_number, 
                                      npc.event_number, npc.type, npc.attributes)
            f.write(packed_data)