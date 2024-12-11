"""Provide a tkinter widget for project statistics display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import CH_ROOT
from nvstatisticslib.linked_percentage_bar import LinkedPercentageBar
from nvstatisticslib.nvstatistics_locale import _
import tkinter as tk


class StatisticsViewCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self.isOpen = True

        # Initialize the class (this hack makes the interface smaller):
        LinkedPercentageBar.treeView = self._ui.tv

        self.calculate_statistics()

    def calculate_statistics(self):
        if self._mdl.prjFile is None:
            return

        wordsTotal = 0
        partWords = {}
        chapterWords = {}
        sectionWords = {}
        stage1Words = {}
        stage2Words = {}
        plotlineWords = {}
        viewpointWords = {}
        for plId in self._mdl.novel.plotLines:
            plotlineWords[plId] = 0
        for crId in self._mdl.novel.characters:
            viewpointWords[crId] = 0
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
                        wordsTotal += self._mdl.novel.sections[scId].wordCount
                        if partId is not None:
                            partWords[partId] += self._mdl.novel.sections[scId].wordCount
                        if stage1Id is not None:
                            stage1Words[stage1Id] += self._mdl.novel.sections[scId].wordCount
                        if stage2Id is not None:
                            stage2Words[stage2Id] += self._mdl.novel.sections[scId].wordCount
                        for plId in self._mdl.novel.sections[scId].scPlotLines:
                            plotlineWords[plId] += self._mdl.novel.sections[scId].wordCount
                        if self._mdl.novel.sections[scId].characters:
                            crId = self._mdl.novel.sections[scId].characters[0]
                            viewpointWords[crId] += self._mdl.novel.sections[scId].wordCount
                    elif self._mdl.novel.sections[scId].scType == 2:
                        stage1Id = scId
                        stage1Words[stage1Id] = 0
                    elif self._mdl.novel.sections[scId].scType == 3:
                        stage2Id = scId
                        stage2Words[stage2Id] = 0

        self.clear_frames()
        LBL_WIDTH = 40
        LBL_DIST = 1

        frame = self._partFrame
        for chId in partWords:
            title = self._mdl.novel.chapters[chId].title
            percentage = partWords[chId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                chId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        frame = self._chapterFrame
        for chId in chapterWords:
            title = self._mdl.novel.chapters[chId].title
            percentage = chapterWords[chId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                chId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        frame = self._sectionFrame
        for scId in sectionWords:
            title = self._mdl.novel.sections[scId].title
            percentage = sectionWords[scId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                scId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        frame = self._povFrame
        for crId in viewpointWords:
            if viewpointWords[crId] == 0:
                continue

            title = self._mdl.novel.characters[crId].title
            percentage = viewpointWords[crId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                crId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        frame = self._plotstructureFrame

        heading1 = tk.Label(frame, text=_('Stages (first level)'), bg='white', pady=5, anchor='w')
        font: dict[str, any] = tk.font.Font(font=heading1['font']).actual()
        heading1.configure(font=(font['family'], font['size'], 'bold'))
        heading1.pack(anchor='w', fill='x')
        for scId in stage1Words:
            title = self._mdl.novel.sections[scId].title
            percentage = stage1Words[scId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                scId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        heading2 = tk.Label(frame, text=_('Stages (second level)'), bg='white', pady=5, anchor='w')
        heading2.configure(font=(font['family'], font['size'], 'bold'))
        heading2.pack(anchor='w', fill='x')
        for scId in stage2Words:
            title = self._mdl.novel.sections[scId].title
            percentage = stage2Words[scId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                scId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

        frame = self._plotlineFrame
        for plId in plotlineWords:
            title = self._mdl.novel.plotLines[plId].title
            percentage = plotlineWords[plId] / wordsTotal * 100
            LinkedPercentageBar(
                frame,
                plId,
                text=title,
                value=percentage,
                lblWidth=LBL_WIDTH,
                lblDist=LBL_DIST,
                ).pack(anchor='nw', expand=False)

