# network/utils.py

import struct

def write_varint(value: int) -> bytes:
    """Encode un entier en VarInt (format variable Minecraft)."""
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value:
            byte |= 0x80
        result.append(byte)
        if not value:
            break
    return bytes(result)

def read_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Decode un VarInt depuis des bytes, retourne la valeur et le nouvel offset."""
    value = 0
    shift = 0
    while True:
        byte = data[offset]
        offset += 1
        value |= (byte & 0x7F) << shift
        shift += 7
        if not (byte & 0x80):
            break
    return value, offset

def write_string(s: str) -> bytes:
    """Encode une string Minecraft (VarInt longueur + UTF-8)."""
    data = s.encode('utf-8')
    return write_varint(len(data)) + data

def read_string(data: bytes, offset: int = 0) -> tuple[str, int]:
    """Decode une string Minecraft."""
    length, offset = read_varint(data, offset)
    s = data[offset:offset + length].decode('utf-8')
    return s, offset + length

def write_unsigned_short(value: int) -> bytes:
    """Encode un unsigned short (2 octets, big-endian)."""
    return struct.pack('>H', value)

def read_long(data: bytes, offset: int = 0) -> tuple[int, int]:
    """Decode un long (8 octets, big-endian)."""
    value = struct.unpack_from('>Q', data, offset)[0]
    return value, offset + 8

def write_long(value: int) -> bytes:
    """Encode un long (8 octets, big-endian)."""
    return struct.pack('>Q', value)