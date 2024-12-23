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
        plotlineSections = {}
        for plId in self._mdl.novel.plotLines:
            plotlineSections[plId] = []
        viewpointSections = {}
        for crId in self._mdl.novel.characters:
            viewpointSections[crId] = []
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
                        if partId is not None:
                            partWords[partId] += self._mdl.novel.sections[scId].wordCount
                        if stage1Id is not None:
                            stage1Words[stage1Id] += self._mdl.novel.sections[scId].wordCount
                        if stage2Id is not None:
                            stage2Words[stage2Id] += self._mdl.novel.sections[scId].wordCount
                        for plId in self._mdl.novel.sections[scId].scPlotLines:
                            plotlineSections[plId].append((wordsTotal, self._mdl.novel.sections[scId].wordCount))
                        if self._mdl.novel.sections[scId].characters:
                            crId = self._mdl.novel.sections[scId].characters[0]
                            viewpointSections[crId].append((wordsTotal, self._mdl.novel.sections[scId].wordCount))
                        wordsTotal += self._mdl.novel.sections[scId].wordCount
                    elif self._mdl.novel.sections[scId].scType == 2:
                        stage1Id = scId
                        stage1Words[stage1Id] = 0
                    elif self._mdl.novel.sections[scId].scType == 3:
                        stage2Id = scId
                        stage2Words[stage2Id] = 0

        LBL_WIDTH = 200
        LBL_DIST = 10
        RIGHT_MARGIN = 40
        LBL_HEIGHT = 20
        BAR_HEIGHT = 10
        HALF_BAR = BAR_HEIGHT / 2
        TEXT_COLOR = self.prefs['color_text']
        BG_COLOR = self.prefs['color_filler']
        TEXT_MAX = LBL_WIDTH / 5

        self.update()
        try:
            xMax = self.view.winfo_width()
        except:
            # handling delayed refresh while the view is already closed
            return

        x0 = LBL_WIDTH + LBL_DIST
        x3 = xMax - RIGHT_MARGIN
        xSpan = x3 - x0
        wcNorm = xSpan / wordsTotal

        #--- Parts.
        canvas = self.partCanvas
        barColor = self.prefs['color_part']
        y = LBL_HEIGHT
        canvas.delete("all")
        x2 = LBL_WIDTH + LBL_DIST
        for chId in partWords:
            title = textwrap.shorten(self._mdl.novel.chapters[chId].title, width=x2 / 5)
            y += LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + partWords[chId] * wcNorm
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = canvas.create_text((x1 - LBL_DIST, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=chId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        #--- Chapters.
        canvas = self.chapterCanvas
        barColor = self.prefs['color_chapter']
        y = LBL_HEIGHT
        canvas.delete("all")
        x2 = LBL_WIDTH + LBL_DIST
        for chId in chapterWords:
            title = textwrap.shorten(self._mdl.novel.chapters[chId].title, width=x2 / 5)
            y += LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + chapterWords[chId] * wcNorm
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = canvas.create_text((x1 - LBL_DIST, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=chId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        #--- Sections.
        canvas = self.sectionCanvas
        barColor = self.prefs['color_section']
        y = LBL_HEIGHT
        canvas.delete("all")
        x2 = LBL_WIDTH + LBL_DIST
        for scId in sectionWords:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=x2 / 5)
            y += LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + sectionWords[scId] * wcNorm
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = canvas.create_text((x1 - LBL_DIST, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        #--- Viewpoints.
        canvas = self.povCanvas
        barColor = self.prefs['color_viewpoint']
        y = LBL_HEIGHT
        canvas.delete("all")
        for crId in viewpointSections:
            if not viewpointSections[crId]:
                continue

            y += LBL_HEIGHT
            y1 = y
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x0, y1, x3, y2, fill=BG_COLOR)
            for position, wordCount in viewpointSections[crId]:
                if wordCount > 0:
                    x1 = x0 + position * wcNorm
                    x2 = x1 + wordCount * wcNorm
                    canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            title = textwrap.shorten(self._mdl.novel.characters[crId].title, width=TEXT_MAX)
            titleLabel = canvas.create_text((LBL_WIDTH, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=crId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        #--- Plot structure.
        canvas = self.plotstructureCanvas
        barColor = self.prefs['color_stage1']
        y = LBL_HEIGHT

        canvas.delete("all")
        heading = _('Stages (first level)')
        canvas.create_text(LBL_DIST, y, text=heading, fill=TEXT_COLOR, anchor='w')
        x2 = LBL_WIDTH + LBL_DIST
        for scId in stage1Words:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=x2 / 5)
            y += LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + stage1Words[scId] * wcNorm
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = canvas.create_text((x1 - LBL_DIST, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)

        y += LBL_HEIGHT
        heading = _('Stages (second level)')
        canvas.create_text(LBL_DIST, y, text=heading, fill=TEXT_COLOR, anchor='w')
        barColor = self.prefs['color_stage2']
        x2 = LBL_WIDTH + LBL_DIST
        for scId in stage2Words:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=x2 / 5)
            y += LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + stage2Words[scId] * wcNorm
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = canvas.create_text((x1 - LBL_DIST, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=scId)
            canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        totalBounds = canvas.bbox('all')
        if totalBounds is not None:
            canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

        #--- Plot lines.
        canvas = self.plotlineCanvas
        barColor = self.prefs['color_plotline']
        y = LBL_HEIGHT
        canvas.delete("all")
        for plId in plotlineSections:
            y += LBL_HEIGHT
            y1 = y
            y2 = y1 + BAR_HEIGHT
            canvas.create_rectangle(x0, y1, x3, y2, fill=BG_COLOR)
            for position, wordCount in plotlineSections[plId]:
                if wordCount > 0:
                    x1 = x0 + position * wcNorm
                    x2 = x1 + wordCount * wcNorm
                    canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            title = f'{self._mdl.novel.plotLines[plId].shortName} - {self._mdl.novel.plotLines[plId].title}'
            title = textwrap.shorten(title, width=TEXT_MAX)
            titleLabel = canvas.create_text((LBL_WIDTH, y + HALF_BAR), text=title, fill=TEXT_COLOR, anchor='e', tags=plId)
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

