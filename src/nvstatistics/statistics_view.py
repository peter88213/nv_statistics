"""Provide a popup window for project statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.gui.observer import Observer
from nvstatistics.chapter_frame import ChapterFrame
from nvstatistics.nvstatistics_locale import _
from nvstatistics.part_frame import PartFrame
from nvstatistics.platform.platform_settings import KEYS
from nvstatistics.platform.platform_settings import PLATFORM
from nvstatistics.plotline_frame import PlotlineFrame
from nvstatistics.plotstruct_frame import PlotstructFrame
from nvstatistics.pov_frame import PovFrame
from nvstatistics.section_frame import SectionFrame
from nvlib.controller.sub_controller import SubController
import tkinter as tk


class StatisticsView(tk.Toplevel, Observer, SubController):

    def __init__(self, model, view, controller, prefs):
        tk.Toplevel.__init__(self)
        self.minsize(400, 400)
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

        self.partFrame = PartFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )
        self.chapterFrame = ChapterFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )
        self.sectionFrame = SectionFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )
        self.povFrame = PovFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )
        self.plotstructureFrame = PlotstructFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )
        self.plotlineFrame = PlotlineFrame(
            model,
            view,
            controller,
            prefs,
            self.view,
        )

        self._frames = [
            (self.sectionFrame, _('Sections')),
            (self.chapterFrame, _('Chapters')),
            (self.partFrame, _('Parts')),
            (self.povFrame, _('Viewpoints')),
            (self.plotstructureFrame, _('Plot structure')),
            (self.plotlineFrame, _('Plot lines')),
        ]
        for frame, text in self._frames:
            self.view.add(frame, text=text)
        self.view.bind('<<NotebookTabChanged>>', self._onTabChange)
        self.activeFrame = self._frames[0][0]

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.on_quit,
        ).pack(anchor='e', padx=5, pady=5)

        # Respond to windows resizing.
        self.redrawing = False
        # semaphore to prevent overflow
        self.bind('<Configure>', self.redraw)

        self._mdl = model
        self.isOpen = True
        self._mdl.add_observer(self)

    def clear_frames(self):
        for frame in self.view.winfo_children():
            for child in frame.winfo_children():
                child.destroy()

    def on_quit(self, event=None):
        self.isOpen = False
        self._mdl.delete_observer(self)
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.destroy()

    def redraw(self, event=None):
        if self.redrawing:
            return

        self.redrawing = True
        self.activeFrame.draw()
        self.redrawing = False

    def refresh(self, event=None):
        self.activeFrame.calculate()
        self.activeFrame.draw()

    def _onTabChange(self, event=None):
        self.activeFrame = self._frames[self.view.index('current')][0]
        self.activeFrame.calculate()
        self.activeFrame.draw()
