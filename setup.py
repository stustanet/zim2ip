#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="zim2ip",
    version="0.1",
    description="Lookup StuStaNet IPs by Room",
    maintainer="StuStaNet e. V.",
    maintainer_email="vorstand@stusta.net",
    url="https://gitlab.stusta.de/stustanet/zim2ip",
    license='GPL3+',
    packages=[
        "zim2ip",
    ],
    scripts=[
        "scripts/zim2ip_gui",
        "scripts/zim2ip_cli",
        "scripts/zim2ip_srv",
    ],
    data_files=[
        ("/usr/lib/systemd/system/", [
            "zim2ip_srv.service",
        ]),
        ("/usr/share/applications/", [
            "zim2ip_gui.desktop",
        ]),
        ("/usr/share/zim2ip/", [
            "layout.glade",
            "StuStaNet_Logo.svg",
        ]),
    ],
    platforms=[
        'Linux',
    ],
)
