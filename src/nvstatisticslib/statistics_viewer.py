"""Provide a tkinter widget for project statistics display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from novxlib.novx_globals import CH_ROOT
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

        self._mdl.register_client(self)
        self.refresh()

    def on_quit(self, event=None):
        self._plugin.kwargs['window_geometry'] = self.winfo_geometry()
        self.destroy()
        self.isOpen = False

    def refresh(self):
        """Update the statistics."""
        partWords = {}
        chapterWords = {}
        sectionWords = {}
        stage1Words = {}
        stage2Words = {}
        partId = None
        stage1Id = None
        stage2Id = None
        for chId in self._mdl.tree.get_children(CH_ROOT):
            if self._mdl.novel.chapters[chId].chLevel == 1:
                partId = chId
                partWords[partId] = 0
            else:
                chapterWords[chId] = 0
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self._mdl.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        sectionWords[scId] = self._mdl.novel.sections[scId].wordCount
                        chapterWords[chId] += self._mdl.novel.sections[scId].wordCount
                        if partId is not None:
                            partWords[partId] += self._mdl.novel.sections[scId].wordCount
                        if stage1Id is not None:
                            stage1Words[stage1Id] += self._mdl.novel.sections[scId].wordCount
                        if stage2Id is not None:
                            stage2Words[stage2Id] += self._mdl.novel.sections[scId].wordCount
                    elif self._mdl.novel.sections[scId].scType == 2:
                        stage1Id = scId
                        stage1Words[stage1Id] = 0
                    elif self._mdl.novel.sections[scId].scType == 3:
                        stage2Id = scId
                        stage2Words[stage2Id] = 0

        print('Parts')
        for partId in partWords:
            print(partId, partWords[partId])
        print('Chapters')
        for chId in chapterWords:
            print(chId, chapterWords[chId])
        print('Sections')
        for scId in sectionWords:
            print(scId, sectionWords[scId])
        print('Stage 1st level')
        for scId in stage1Words:
            print(scId, stage1Words[scId])
        print('Stage 2nd level')
        for scId in stage2Words:
            print(scId, stage2Words[scId])
