#!/usr/bin/env python3
"""
Listen on Socket for Client asking for IP with Roomnumber utilizing the
zim2ip-List from the Studentenwerk
"""
import argparse
import asyncio
import grp
import os
import re
import signal


#example valid room: "741-09 13-18" oder "787-67 03-15-0"
VALIDROOMS = re.compile("[0-9]{3}-[0-9]{2} [0-9]{2}-[0-9]{2}-[0-9]")

class Zim2IPProto(asyncio.Protocol):
    """
    Data Protocol for communication with client
    """
    def __init__(self, zim_dict):
        self.zim_dict = zim_dict
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, rawdata):
        if not rawdata:
            return

        data = bytes.decode(rawdata)
        if not VALIDROOMS.match(data):
            self.transport.write(b'invalid room')
            self.transport.close()
            return

        if data in self.zim_dict:
            self.transport.write(self.zim_dict[data].encode())
        else:
            self.transport.write(b'invalid room')
        self.transport.close()


def main():
    """
    Create the socket and the dict between rooms and IPs, handle the exits
    """
    cmd = argparse.ArgumentParser()
    cmd.add_argument('--socket', '-s', default='/run/zim2ip.sock',
                     help='Path to the UNIX-Socket, default=%(default)s')
    cmd.add_argument('--list-file', '-l',
                     default='/usr/share/zim2ip.txt',
                     help=('Path to List connecting rooms and IPs, '
                           'default=%(default)s'))
    cmd.add_argument('--group', '-g', default='users',
                     help=('Group that should have access to the socket, '
                           'default=%(default)s'))

    args = cmd.parse_args()

    zim_dict = dict()
    with open(args.list_file) as zim2ip:
        for line in zim2ip:
            spline = line.split(':')
            zim_dict[spline[0]] = spline[2]

    try:
        os.unlink(args.socket)
    except OSError:
        if os.path.exists(args.socket):
            raise

    oldumask = os.umask(0o007)

    loop = asyncio.get_event_loop()
    coro = loop.create_unix_server(lambda: Zim2IPProto(zim_dict), args.socket)
    server = loop.run_until_complete(coro)
    loop.add_signal_handler(signal.SIGTERM, loop.stop)

    os.umask(oldumask)
    os.chown(args.socket, os.geteuid(), grp.getgrnam(args.group).gr_gid)

    try:
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...")

    server.close()
    loop.run_until_complete(server.wait_closed())

    loop.stop()
    loop.run_forever()
    loop.close()
    os.remove(args.socket)


if __name__ == '__main__':
    main()
