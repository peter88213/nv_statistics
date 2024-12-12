"""Provide platform specific settings for the nv_statistics plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import platform

from nvstatistics.platform.generic_keys import GenericKeys
from nvstatistics.platform.generic_mouse import GenericMouse
from nvstatistics.platform.mac_keys import MacKeys
from nvstatistics.platform.mac_mouse import MacMouse
from nvstatistics.platform.windows_keys import WindowsKeys
from nvstatistics.platform.windows_mouse import WindowsMouse
from nvstatistics.platform.linux_mouse import LinuxMouse

if platform.system() == 'Windows':
    PLATFORM = 'win'
    KEYS = WindowsKeys()
    MOUSE = WindowsMouse()
elif platform.system() in ('Linux', 'FreeBSD'):
    PLATFORM = 'ix'
    KEYS = GenericKeys()
    MOUSE = LinuxMouse()
elif platform.system() == 'Darwin':
    PLATFORM = 'mac'
    KEYS = MacKeys()
    MOUSE = MacMouse()
else:
    PLATFORM = ''
    KEYS = GenericKeys()
    MOUSE = GenericMouse()

