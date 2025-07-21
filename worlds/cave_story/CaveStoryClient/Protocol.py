import asyncio
import uuid

from CommonClient import logger

from .Enums import *
from .Constants import *

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

async def send_packet(ctx, pkt: bytes):
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