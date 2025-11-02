# protocol/status.py

from protocol.base import BasePacket
from protocol import PacketRegistry, State, Direction
from network.utils import write_varint


@PacketRegistry.register
class StatusRequest(BasePacket):
    PACKET_ID = 0x00
    STATE = State.STATUS
    DIRECTION = Direction.SERVERBOUND

    def serialize(self) -> bytes:
        data = write_varint(self.PACKET_ID)
        return write_varint(len(data)) + data
