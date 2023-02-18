import socket
import json

from yeelight import discover_bulbs

MCAST_GRP = '239.255.255.250'
MCAST_PORT = 1982

SSDP_REQUEST = f"""M-SEARCH * HTTP/1.1
HOST: {MCAST_GRP}:{MCAST_PORT}
MAN: "ssdp:discover"
ST: wifi_bulb

"""


def try_discover():
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Enable multicast TTL
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    
    # Send data to the multicast group
    sock.sendto(SSDP_REQUEST.encode(), (MCAST_GRP, MCAST_PORT))

    # Look for responses from all recipients
    while True:
        try:
            data, addr = sock.recvfrom(1024)
        except socket.timeout:
            break
        else:
            print('Received from {}: \n{}'.format(addr, data.decode()))


def try_command():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.bind(('', 0))
    print(sock.getsockname())

    message = {'id': 1, 'method': 'set_power', 'params': ['on', 'smooth', 500]}
    sock.sendto(json.dumps(message).encode(), ("192.168.1.15", 80))
    sock.settimeout(1)


def main():
    print(discover_bulbs())


if __name__ == "__main__":
    import logging
    from ipdb import launch_ipdb_on_exception
    logging.basicConfig(level=logging.INFO)

    with launch_ipdb_on_exception():
        main()
