# protocol/handshake.py

import struct

from network.utils import write_varint, write_string
from protocol import PacketRegistry
from protocol.base import BasePacket


@PacketRegistry.register
class Handshake(BasePacket):
    PACKET_ID = 0x00

    def __init__(self, protocol_version: int, server_address: str, server_port: int, next_state: int):
        self.protocol_version = protocol_version
        self.server_address = server_address
        self.server_port = server_port
        self.next_state = next_state

    def serialize(self) -> bytes:
        data = bytearray()
        data.extend(write_varint(self.PACKET_ID))
        data.extend(write_varint(self.protocol_version))
        data.extend(write_string(self.server_address))
        data.extend(struct.pack('>H', self.server_port))
        data.extend(write_varint(self.next_state))
        full_payload = bytes(data)
        return write_varint(len(full_payload)) + full_payload
