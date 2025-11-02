# protocol/status.py

from protocol.base import BasePacket
from protocol import PacketRegistry, State, Direction
from network.utils import write_varint, read_string, write_string


@PacketRegistry.register
class StatusRequest(BasePacket):
    PACKET_ID = 0x00
    STATE = State.STATUS
    DIRECTION = Direction.SERVERBOUND

    def serialize(self) -> bytes:
        body = write_varint(self.PACKET_ID)
        return write_varint(len(body)) + body

    @classmethod
    def deserialize(cls, data: bytes, offset: int = 0):
        return cls(), offset


@PacketRegistry.register
class StatusResponse(BasePacket):
    PACKET_ID = 0x00
    STATE = State.STATUS
    DIRECTION = Direction.CLIENTBOUND

    def __init__(self, json_response: str):
        self.json_response = json_response

    def serialize(self) -> bytes:
        body = write_varint(self.PACKET_ID) + write_string(self.json_response)
        return write_varint(len(body)) + body

    @classmethod
    def deserialize(cls, data: bytes, offset: int = 0):
        json_response, offset = read_string(data, offset)
        return cls(json_response), offset
