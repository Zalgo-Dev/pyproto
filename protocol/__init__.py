# procotol/__init__.py
from enum import IntEnum

class State(IntEnum):
    """Protocol states."""
    HANDSHAKING = 0 # handshake
    STATUS = 1      # status ping
    LOGIN = 2       # login/authentication
    PLAY = 3        # in-game

class Direction(IntEnum):
    """Packet directions."""
    SERVERBOUND = 0 # client -> server
    CLIENTBOUND = 1 # server -> client

class PacketRegistry:
    """Registry for protocol packets."""
    _registry = {}  # keys: (State, Direction, PACKET_ID) or ("__id_only__", id)

    @classmethod
    def register(cls, packet_cls=None, *, state=None, direction=None):
        # Autoriser l'utilisation du décorateur avec ou sans arguments
        if packet_cls is None:
            return lambda pc: cls.register(pc, state=state, direction=direction)

        pid = getattr(packet_cls, "PACKET_ID", None)
        st = getattr(packet_cls, "STATE", None) if state is None else state
        dr = getattr(packet_cls, "DIRECTION", None) if direction is None else direction

        if pid is None:
            raise ValueError(f"Packet {packet_cls.__name__} has no PACKET_ID")

        if st is None or dr is None:
            key = ("__id_only__", pid)
        else:
            key = (State(st), Direction(dr), pid)

        cls._registry[key] = packet_cls
        return packet_cls

    @classmethod
    def get(cls, *, state=None, direction=None, packet_id=None):
        if packet_id is None:
            return None
        if state is None or direction is None:
            return cls._registry.get(("__id_only__", packet_id))
        return cls._registry.get((State(state), Direction(direction), packet_id))

    @classmethod
    def all(cls):
        return cls._registry.copy()

# Importer les sous-modules pour déclencher les décorateurs @PacketRegistry.register
from . import base as base   # noqa: F401
from . import handshake as handshake  # noqa: F401
from . import status as status  # noqa: F401

__all__ = ["PacketRegistry", "State", "Direction", "base", "handshake", "status"]