#!/usr/bin/env python3

import gui
import os
import sys

if os.getuid() != 0:
    print('PLEASE USE ROOT')
    sys.exit(0)

if __name__ == '__main__':
    app = gui.GUI()
    