=zim2ip=
''zim2ip'' is a python package that contains three executable python scripts
''zim2ip_srv'' is the server that reads the /usr/share/zim2ip.txt file and opens
an unix socket (and therefore must be run as root).
''zim2ip_cli'' is the command line interface for the client, connects to
the given unix cluster and gives instructions on cli for usage.
''zim2ip_gui'' is the GUI with the same functionality as zim2ip_cli.

===installation===
1. copy the zim2ip.txt file to /usr/share/zim2ip.txt
2. clone this repository: `git clone https://gitlab.stusta.de/stustanet/zim2ip.git`
3. ./setup.py build
4. sudo ./setup.py install

===running the program===
1. start the server with `sudo zim2ip_srv`
2. run either the cli (`zim2ip_cli`) or the gui (`zim2ip_gui`)
3. ???
4. PROFIT!

===the zim2ip.txt file===
the zim2ip.txt contains lines for each room with the following format:
'''
741-09 13-18-0:741-09-13-18-0 d-z-01:10.150.xxx.yyy 10.150.xxx.yyy+1 10.150.xxx.yyy+2 ...
'''

* The first three letters are the Wohnheimsanlage, e.g. 740 is StuSta - Altstadt, 741 is StuSta - Neustadt and 787 is Max-Bill Wohnheim.
* the next two letters are the number of the house
* following after a space character is the floor number (2 digits)
* and after that (separated by the dash) is the room number (2 digits)
* and after that a "-0"
e.g.: StuSta Neustadt HSH (Haus 9) room 1318 is "741-09 13-18-0"