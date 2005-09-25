#!/usr/bin/env python

# Wogix - Tabbed Window Manager for Exigo
# Copyright (C) 2005 Alex Smith <alex.extreme2 at gmail.com>

# Import our stuff

import sys
import os
import signal
import errno
import array
import traceback
import re
import string
import types
import select
import window

# Import Xlib

from Xlib import display, X, Xutil, Xatom, rdb, error
import Xlib.protocol.event

# Import our version info

import version

print "w00t0h!"
print "Exigo is born :D"
print
print "Welcome to " + version.appName + " v" + version.appVer + "!"

# Create the Display object
disp = display.Display()

# Create our Window
window = window.Window()
