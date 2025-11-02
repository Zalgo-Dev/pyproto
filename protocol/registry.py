# protocol/registry.py

class PacketRegistry:
    _registry = {}

    @classmethod
    def register(cls, packet_cls):
        pid = packet_cls.PACKET_ID
        if pid is None:
            raise ValueError(f"Packet {packet_cls.__name__} has no PACKET_ID")
        cls._registry[pid] = packet_cls
        return packet_cls

    @classmethod
    def get(cls, packet_id):
        return cls._registry.get(packet_id)

    @classmethod
    def all(cls):
        return cls._registry.copy()
