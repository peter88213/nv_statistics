"""Provide a class for project statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import textwrap

from nvlib.novx_globals import CH_ROOT
from nvstatistics.statistics_frame import StatisticsFrame


class PartFrame(StatisticsFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.partWords = {}

    def calculate(self):
        self.wordsTotal = 0
        partId = None
        for chId in self._mdl.tree.get_children(CH_ROOT):
            if self._mdl.novel.chapters[chId].chType == 0:
                if self._mdl.novel.chapters[chId].chLevel == 1:
                    partId = chId
                    self.partWords[partId] = 0
                for scId in self._mdl.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        if partId is not None:
                            self.partWords[partId] += self._mdl.novel.sections[scId].wordCount
                        self.wordsTotal += self._mdl.novel.sections[scId].wordCount

    def draw(self):
        try:
            wcNorm, x0, x3 = self._get_win_scaling()
        except:
            # handling delayed refresh while the view is already closed
            return

        barColor = self.prefs['color_part']
        y = self._LBL_HEIGHT
        self.canvas.delete("all")
        x2 = self._LBL_WIDTH + self._LBL_DIST
        for chId in self.partWords:
            title = textwrap.shorten(
                self._mdl.novel.chapters[chId].title,
                width=x2 / 5
            )
            y += self._LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + self.partWords[chId] * wcNorm
            y2 = y1 + self._BAR_HEIGHT
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = self.canvas.create_text(
                (x1 - self._LBL_DIST, y + self._HALF_BAR),
                text=title,
                fill=self._TEXT_COLOR,
                anchor='e',
                tags=chId,
            )
            self.canvas.tag_bind(
                titleLabel, '<Double-Button-1>', self._on_double_click
            )
        self._adjust_scrollbar()

