#!/usr/bin/env python3

"""
gui functionality for zim2ip
"""

import argparse
import os
import signal
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import (GObject as gobject,
                           Gtk as gtk)

from zim2ip.cli import zim2ip_lookup


class Zim2IPGui:
    """
    Class
    """
    def __init__(self, socket):
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join("/usr/share/zim2ip/",
                                                "layout.glade"))
        self.builder.connect_signals(self)

        self.buf = self.builder.get_object('output_data')
        self.socket = socket

        self.window = self.builder.get_object("window0")
        self.window.resize(300, 200)
        self.window.set_position(gtk.WindowPosition.CENTER)
        self.draw_size = (0, 0)

        self.window.show_all()

    def run(self):
        """
        run the gtk main loop
        """
        gtk.main()

    def delete_window(self, *args):
        """
        stop the application
        """
        gtk.main_quit(args)

    def start_search(self, *args):
        """
        convert the values from the gui and ask the server for IPs
        """
        house = self.builder.get_object('house').get_active_iter()
        housestwm = self.builder.get_object('houses').get_value(house, 0)
        room = self.builder.get_object('room').get_text().rjust(4, '0')
        roomstwm = "-".join((room[0:2], room[2:4])) + '-0-z-1'
        result = zim2ip_lookup(housestwm + ' ' + roomstwm, self.socket)
        if result:
            self.buf.set_text("\n".join(result))
        else:
            self.buf.set_text('Kein gültiges Zimmer angegeben, falls das '
                              'Zimmer tatsächlich so auf dem Mietvertrag '
                              'angegeben ist, bitte mit allen vorhandenen '
                              'Informationen an den Vorstand melden')


def main():
    """
    Do GUI stuff
    """
    cmd = argparse.ArgumentParser()
    cmd.add_argument('--socket', '-s', default='/run/zim2ip.sock',
                     help='Path to the UNIX-Socket, default=%(default)s')

    args = cmd.parse_args()

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    v = Zim2IPGui(args.socket)
    v.run()


if __name__ == '__main__':
    main()
