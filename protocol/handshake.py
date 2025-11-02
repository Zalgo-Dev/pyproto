# protocol/handshake.py

from network.utils import write_varint, write_string, read_varint, read_string
import struct

class Handshake:
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

    def deserialize(self, data: bytes):
        offset = 0
        packet_id, offset = read_varint(data, offset)
        if packet_id != self.PACKET_ID:
            raise ValueError(f"Invalid Packet ID: expected {self.PACKET_ID}, got {packet_id}")
        self.protocol_version, offset = read_varint(data, offset)
        self.server_address, offset = read_string(data, offset)
        self.server_port = struct.unpack_from('>H', data, offset)[0]
        offset += 2
        self.next_state, offset = read_varint(data, offset)    