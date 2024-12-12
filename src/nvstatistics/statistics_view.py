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

        self.view = ttk.Notebook(self)
        self.view.enable_traversal()
        self.view.pack(fill='both', expand=True)

        self.partFrame = ttk.Frame(self.view)
        self.chapterFrame = ttk.Frame(self.view)
        self.sectionFrame = ttk.Frame(self.view)
        self.povFrame = ttk.Frame(self.view)
        self.plotstructureFrame = ttk.Frame(self.view)
        self.plotlineFrame = ttk.Frame(self.view)

        self.view.add(self.sectionFrame, text=_('Sections'))
        self.view.add(self.chapterFrame, text=_('Chapters'))
        self.view.add(self.partFrame, text=_('Parts'))
        self.view.add(self.povFrame, text=_('Viewpoints'))
        self.view.add(self.plotstructureFrame, text=_('Plot structure'))
        self.view.add(self.plotlineFrame, text=_('Plot lines'))

        kw = dict(
            borderwidth=0,
            highlightthickness=0
            )

        self.partCanvas = tk.Canvas(self.partFrame, cnf={}, **kw)
        self.partCanvas.pack(side='left', fill='both', expand=True)
        self.partCanvas['background'] = self.prefs['color_background']

        self.chapterCanvas = tk.Canvas(self.chapterFrame, cnf={}, **kw)
        self.chapterCanvas.pack(side='left', fill='both', expand=True)
        self.chapterCanvas['background'] = self.prefs['color_background']

        self.sectionCanvas = tk.Canvas(self.sectionFrame, cnf={}, **kw)
        self.sectionCanvas.pack(side='left', fill='both', expand=True)
        self.sectionCanvas['background'] = self.prefs['color_background']

        self.povCanvas = tk.Canvas(self.povFrame, cnf={}, **kw)
        self.povCanvas.pack(side='left', fill='both', expand=True)
        self.povCanvas['background'] = self.prefs['color_background']

        self.plotstructureCanvas = tk.Canvas(self.plotstructureFrame, cnf={}, **kw)
        self.plotstructureCanvas.pack(side='left', fill='both', expand=True)
        self.plotstructureCanvas['background'] = self.prefs['color_background']

        self.plotlineCanvas = tk.Canvas(self.plotlineFrame, cnf={}, **kw)
        self.plotlineCanvas.pack(side='left', fill='both', expand=True)
        self.plotlineCanvas['background'] = self.prefs['color_background']

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(anchor='e', padx=5, pady=5)

        # Respond to windows resizing.
        self.bind('<Configure>', self.refresh)

        self.initialize_controller(model, view, controller)
        self._mdl.add_observer(self)

    def clear_frames(self):
        for frame in self.view.winfo_children():
            for child in frame.winfo_children():
                child.destroy()

    def on_quit(self, event=None):
        self._mdl.delete_observer(self)
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def refresh(self, event=None):
        self.calculate_statistics()

