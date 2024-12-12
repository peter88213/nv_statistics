"""Provide a tkinter widget for project statistics display.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import textwrap

from mvclib.controller.sub_controller import SubController
from nvlib.novx_globals import CH_ROOT
from nvstatistics.nvstatistics_locale import _


class StatisticsViewCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self.isOpen = True
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
            if self._mdl.novel.chapters[chId].chType == 0:
                if self._mdl.novel.chapters[chId].chLevel == 1:
                    partId = chId
                    partWords[partId] = 0
                else:
                    chapterWords[chId] = 0
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

        LBL_WIDTH = 200
        LBL_DIST = 20
        RIGHT_MARGIN = 40
        LBL_HEIGHT = 20
        BAR_HEIGHT = 10
        TEXT_COLOR = self.prefs['color_text']
        BG_COLOR = self.prefs['color_filler']
        TEXT_MAX = 35

        self.update()
        xMax = self.view.winfo_width()
        xSpan = xMax - LBL_WIDTH - RIGHT_MARGIN
        x3 = xMax - RIGHT_MARGIN

        canvas = self.partCanvas
        barColor = self.prefs['color_part']
        y = LBL_HEIGHT
        canvas.delete("all")
        for chId in partWords:
            title = textwrap.shorten(self._mdl.novel.chapters[chId].title, width=TEXT_MAX)
            percentage = partWords[chId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=chId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        canvas = self.chapterCanvas
        barColor = self.prefs['color_chapter']
        y = LBL_HEIGHT
        canvas.delete("all")
        for chId in chapterWords:
            title = textwrap.shorten(self._mdl.novel.chapters[chId].title, width=TEXT_MAX)
            percentage = chapterWords[chId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=chId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        canvas = self.sectionCanvas
        barColor = self.prefs['color_section']
        y = LBL_HEIGHT
        canvas.delete("all")
        for scId in sectionWords:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=TEXT_MAX)
            percentage = sectionWords[scId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        canvas = self.povCanvas
        barColor = self.prefs['color_viewpoint']
        y = LBL_HEIGHT
        canvas.delete("all")
        for crId in viewpointWords:
            if viewpointWords[crId] == 0:
                continue

            title = textwrap.shorten(self._mdl.novel.characters[crId].title, width=TEXT_MAX)
            percentage = viewpointWords[crId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=crId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        canvas = self.plotstructureCanvas
        barColor = self.prefs['color_stage1']
        y = LBL_HEIGHT

        canvas.delete("all")
        heading = _('Stages (first level)')
        canvas.create_text(LBL_DIST, y, text=heading, fill=TEXT_COLOR, anchor='w')
        for scId in stage1Words:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=TEXT_MAX)
            percentage = stage1Words[scId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)

        y += LBL_HEIGHT
        heading = _('Stages (second level)')
        canvas.create_text(LBL_DIST, y, text=heading, fill=TEXT_COLOR, anchor='w')
        barColor = self.prefs['color_stage2']
        for scId in stage2Words:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=TEXT_MAX)
            percentage = stage2Words[scId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        canvas = self.plotlineCanvas
        barColor = self.prefs['color_plotline']
        y = LBL_HEIGHT
        canvas.delete("all")
        for plId in plotlineWords:
            title = textwrap.shorten(self._mdl.novel.plotLines[plId].title, width=TEXT_MAX)
            percentage = plotlineWords[plId] / wordsTotal * xSpan
            y += LBL_HEIGHT
            x1 = LBL_WIDTH + LBL_DIST
            y1 = y
            x2 = x1 + int(percentage)
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            canvas.create_rectangle(x2, y1, x3, y2, fill=BG_COLOR)
            titleLabel = canvas.create_text((LBL_WIDTH, y), text=title, fill=TEXT_COLOR, anchor='e', tags=plId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

    def _get_element_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _on_double_click(self, event):
        """Select the double-clicked section in the project tree."""
        elementId = self._get_element_id(event)
        self._ui.tv.go_to_node(elementId)

