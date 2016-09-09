#!/usr/bin/env python3
"""
Ask user for a room number and fetch IPs for the room from zim2ip_srv
"""
import argparse
import re
import socket
import sys


VALIDROOMS = re.compile("[0-9]{3}-[0-9]{2} [0-9]{2}-[0-9]{2}-[0-9]")

def zim2ip_lookup(roomnr, location):
    if VALIDROOMS.match(roomnr):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

        try:
            sock.connect(location)
        except:
            raise
        # except socket.error, msg:
        #     print >>sys.stderr, msg
        #     sys.exit(1)

        sock.sendall(roomnr.encode())
        buf = bytearray()
        result = None
        while True:
            data = sock.recv(1024)
            if len(data) + len(buf) > 8196:
                break
            if not data:
                break
            buf += data
            npos = buf.find(b"\n")
            if npos == -1:
                continue
            result = buf[:npos]
            if result == 'invalid room':
                result = None
                break
            result = result.decode().split()
        sock.close()
        return result


def main():
    cmd = argparse.ArgumentParser()
    cmd.add_argument('--socket', '-s', default='/run/zim2ip.sock',
                     help='Path to the UNIX-Socket, default=%(default)s')

    args = cmd.parse_args()


    roomnr = input('Bitte die "Wohnungsnummer", wie auf dem Mietvertrag '
                   'angegeben, eingeben (sowas wie "741-12 00-28-0"): ')
    print('')
    result = zim2ip_lookup(roomnr, args.socket)
    if result:
        print('Die gültigen IPs für Zimmer ' + roomnr + ' sind:')
        print("\n".join(result))
    else:
        print('Kein gültiges Zimmer angegeben, falls tatsächlich so angegeben, '
              'bitte mit allen vorhandenen Informationen an den Vorstand '
              'melden.', file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()
