# protocol/base.py


class BasePacket:
    PACKET_ID = None

    def serialize(self) -> bytes:
        raise NotImplementedError
