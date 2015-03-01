#!/usr/bin/python

import sys
import os
import subprocess
import importlib
from machinekit import launcher
from time import *


launcher.register_exit_handler()
launcher.set_debug_level(5)
os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    launcher.check_installation()                                     # make sure the Machinekit installation is sane
    launcher.cleanup_session()                                        # cleanup a previous session
    #launcher.load_bbio_file('myoverlay.bbio')                         # load a BBB universal overlay
    #launcher.install_comp('fake_ext.comp')                              # install a comp HAL component of not already installed
    launcher.start_process("configserver -n Testmachine")   # start the configserver
    launcher.start_process('linuxcnc axis.ini')                        # start linuxcnc
except subprocess.CalledProcessError:
    launcher.end_session()
    sys.exit(1)

while True:
    sleep(1)
    launcher.check_processes()
