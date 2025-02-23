"""Provide a class for project statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import textwrap

from nvlib.novx_globals import CH_ROOT
from nvstatistics.statistics_frame import StatisticsFrame


class PovFrame(StatisticsFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewpointSections = {}

    def calculate(self):
        self.wordsTotal = 0
        for crId in self._mdl.novel.characters:
            self.viewpointSections[crId] = []
        for chId in self._mdl.tree.get_children(CH_ROOT):
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self._mdl.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        if self._mdl.novel.sections[scId].characters:
                            crId = self._mdl.novel.sections[scId].characters[0]
                            self.viewpointSections[crId].append((self.wordsTotal, self._mdl.novel.sections[scId].wordCount))
                        self.wordsTotal += self._mdl.novel.sections[scId].wordCount

    def draw(self):
        try:
            wcNorm, x0, x3 = self._get_win_scaling()
        except:
            # handling delayed refresh while the view is already closed
            return

        barColor = self.prefs['color_viewpoint']
        y = self._LBL_HEIGHT
        self.canvas.delete("all")
        for crId in self.viewpointSections:
            if self.viewpointSections[crId]:
                y += self._LBL_HEIGHT
                y1 = y
                y2 = y1 + self._BAR_HEIGHT
                self.canvas.create_rectangle(x0, y1, x3, y2, fill=self._BG_COLOR)
                for position, wordCount in self.viewpointSections[crId]:
                    if wordCount > 0:
                        x1 = x0 + position * wcNorm
                        x2 = x1 + wordCount * wcNorm
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
                title = textwrap.shorten(self._mdl.novel.characters[crId].title, width=self._TEXT_MAX)
                titleLabel = self.canvas.create_text((self._LBL_WIDTH, y + self._HALF_BAR), text=title, fill=self._TEXT_COLOR, anchor='e', tags=crId)
                self.canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        self._adjust_scrollbar()

