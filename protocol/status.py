# protocol/status.py

from network.utils import write_varint

class StatusRequest:
    PACKET_ID = 0x00

    def serialize(self) -> bytes:
        data = write_varint(self.PACKET_ID)
        return write_varint(len(data)) + data
