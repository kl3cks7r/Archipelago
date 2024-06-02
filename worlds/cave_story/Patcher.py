# This adapts some code from patcher.py from the project cave-story-randomizer, licensed under zlib
# Please see: https://github.com/cave-story-randomizer/cave-story-randomizer/blob/master/LICENSE

from pathlib import Path
from typing import Callable, Optional
import shutil
import struct
import random
from collections import defaultdict

LOC_TSC_EVENTS = ( # Index is location ID, tuple is TSC Event 
    ('Eggs','0403'), ('Eggs','0404'), ('Egg6','0201'), ('EggR','0301'),
    ('Weed','0700'), ('Weed','0701'), ('Weed','0303'), ('Weed','0800'),
    ('Weed','0801'), ('Weed','0702'), ('Santa','0501'), ('Santa','0302'),
    ('Chako','0212'), ('Malco','0350'), ('WeedB','0301'), ('WeedD','0305'),
    ('Frog','0300'), ('MazeB','0502'), ('MazeS','0202'), ('Almond','0243'),
    ('Almond','1111'), ('Pool','0412'), ('MazeI','0301'), ('MazeA','0502'),
    ('MazeA','0512'), ('MazeA','0522'), ('MazeO','0305'), ('MazeO','0401'),
    ('MazeD','0201'), ('Priso2','0300'), ('Hell1','0401'), ('Hell3','0400'),
    ('Cave','0401'), ('Pole','0202'), ('Pole','0303'), ('Mimi','0202'),
    ('Plant','0401'), ('Pool','0301'), ('Comu','0303'), ('Cemet','0301'),
    ('Cemet','0202'), ('Mapi','0202'), ('Mapi','0501'), ('Pens1','0652'),
    ('Cent','0268'), ('Cent','0324'), ('Cent','0417'), ('Cent','0501'),
    ('Cent','0452'), ('Itoh','0405'), ('Lounge','0204'), ('Jail1','0301'),
    ('Momo','0201'), ('Eggs2','0321'), ('EggR2','0303'), ('Little','0204'),
    ('Clock','0300'), ('Sand','0502'), ('Sand','0503'), ('Sand','0423'),
    ('Sand','0422'), ('Sand','0421'), ('Curly','0518'), ('CurlyS','0401'),
    ('CurlyS','0421'), ('Jenka2','0221'), ('Dark','0401'), ('Gard','0602'),
)

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

def patch_files(locations, uuid, game_dir: Path, slot_data, logger):    
    logger.info("Copying base files...")
    base_dir = game_dir.joinpath("data")
    dest_dir = game_dir.joinpath("freeware","data")
    try:
        shutil.copytree(base_dir, dest_dir, dirs_exist_ok=True, ignore=(lambda _dir, files: [file for file in files if file[-3:] in ('pxm','pxa','tbl','txt')]))
    except shutil.Error:
        raise Exception("Error copying base files. Ensure the directory is not read-only, and that Doukutsu.exe is closed")

    scripts = defaultdict(list)
    for loc, player, item in locations:
        if player:
            tsc_script = "\r\n<PRI<MSG<TUR<GIT1038\r\n"+f"Got {player}'s ={item}=!"+"<WAI0025<NOD<END\r\n"
        else:
            tsc_script = f"\r\n<EVE{item:04d}\r\n"
        map_name, event_num = LOC_TSC_EVENTS[loc]
        scripts[map_name].append((event_num,tsc_script))
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
    scripts['Start'].append(('0201',f'\r\n{goal_flags}\r\n<FL+6200<EVE0091\r\n'))
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
    for map_name, events in scripts.items():
        tsc_path = dest_dir.joinpath("Stage", f"{map_name}.tsc")
        tsc = Tsc(decode_tsc(tsc_path))
        for event, script in events:
            try:
                tsc.set_event(event,script)
            except KeyError:
                logger.debug(f"Error finding Event #{event} in {map_name}.tsc")
        encode_tsc(tsc_path,tsc.get_string())
    tsc_path = dest_dir.joinpath("Head.tsc")
    tsc = Tsc(decode_tsc(tsc_path))
    tsc.set_event('0048','<SMC<LDP<FL+7777')
    encode_tsc(tsc_path,tsc.get_string())

    logger.info("Copying hash and uuid...")
    random.seed(uuid.int)
    hash = ",".join([f"{num:04d}" for num in [random.randint(1, 38) for _ in range(5)]])
    dest_dir.joinpath("hash.txt").write_text(hash)
    dest_dir.joinpath("uuid.txt").write_text(str({str(uuid)}))

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