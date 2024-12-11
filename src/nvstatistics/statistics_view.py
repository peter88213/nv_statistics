"""Provide a tkinter widget for project statistics display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.view.observer import Observer
from nvstatistics.nvstatistics_locale import _
from nvstatistics.platform.platform_settings import KEYS
from nvstatistics.platform.platform_settings import PLATFORM
from nvstatistics.statistics_view_ctrl import StatisticsViewCtrl
import tkinter as tk


class StatisticsView(tk.Toplevel, Observer, StatisticsViewCtrl):

    def __init__(self, model, view, controller, prefs):
        tk.Toplevel.__init__(self)
        self.prefs = prefs

        self.geometry(self.prefs['window_geometry'])
        self.lift()
        self.focus()
        self.protocol("WM_DELETE_WINDOW", self.on_quit)
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)

        self._view = ttk.Notebook(self)
        self._view.enable_traversal()
        self._view.pack(fill='both', expand=True)

        self._partFrame = ttk.Frame(self._view)
        self._chapterFrame = ttk.Frame(self._view)
        self._sectionFrame = ttk.Frame(self._view)
        self._povFrame = ttk.Frame(self._view)
        self._plotstructureFrame = ttk.Frame(self._view)
        self._plotlineFrame = ttk.Frame(self._view)

        VIEW_PADDING = 15
        self._view.add(self._sectionFrame, text=_('Sections'), padding=VIEW_PADDING)
        self._view.add(self._chapterFrame, text=_('Chapters'), padding=VIEW_PADDING)
        self._view.add(self._partFrame, text=_('Parts'), padding=VIEW_PADDING)
        self._view.add(self._povFrame, text=_('Viewpoints'), padding=VIEW_PADDING)
        self._view.add(self._plotstructureFrame, text=_('Plot structure'), padding=VIEW_PADDING)
        self._view.add(self._plotlineFrame, text=_('Plot lines'), padding=VIEW_PADDING)

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(anchor='e', padx=5, pady=5)

        self.initialize_controller(model, view, controller)
        self._mdl.add_observer(self)

    def clear_frames(self):
        for frame in self._view.winfo_children():
            for child in frame.winfo_children():
                child.destroy()

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def refresh(self):
        self.calculate_statistics()

