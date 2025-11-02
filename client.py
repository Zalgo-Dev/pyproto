import socket
from protocol.handshake import Handshake
from protocol.status import StatusRequest
from network.utils import read_varint, read_string

def main():
    host = 'localhost'
    port = 25565

    handshake_packet = Handshake(
        protocol_version=754,
        server_address=host,
        server_port=port,
        next_state=1
    ).serialize()

    status_request_packet = StatusRequest().serialize()

    with socket.create_connection((host, port)) as sock:
        print(f"[+] Connecting to {host}:{port}")
        sock.sendall(handshake_packet)
        print("[>] Handshake sent.")

        sock.sendall(status_request_packet)
        print("[>] Status request sent.")

        packet_length = read_varint_from_socket(sock)
        response_data = sock.recv(packet_length)
        _, offset = read_varint(response_data)
        json_response, _ = read_string(response_data, offset)
        print(f"[✓] Server Response:\n{json_response}")

def read_varint_from_socket(sock):
    result = 0
    shift = 0
    while True:
        byte = sock.recv(1)
        if not byte:
            raise IOError("Socket closed before full VarInt read.")
        val = byte[0]
        result |= (val & 0x7F) << shift
        if not (val & 0x80):
            break
        shift += 7
    return result

if __name__ == "__main__":
    main()
