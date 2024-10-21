"""Provide a tkinter widget for project statistics display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvstatisticslib.nvstatistics_globals import _
from nvstatisticslib.platform.platform_settings import PLATFORM
from nvstatisticslib.platform.platform_settings import KEYS
import tkinter as tk


class StatisticsViewer(tk.Toplevel):

    def __init__(self, plugin, model):
        self._plugin = plugin
        self._mdl = model
        super().__init__()

        self.geometry(self._plugin.kwargs['window_geometry'])
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def on_quit(self, event=None):
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

