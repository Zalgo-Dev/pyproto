# protocol/base.py


class BasePacket:
    PACKET_ID = None
    STATE = None       # ex: State.HANDSHAKING
    DIRECTION = None   # ex: Direction.SERVERBOUND

    def serialize(self) -> bytes:
        raise NotImplementedError
