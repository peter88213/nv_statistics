"""Provide a class for project statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import textwrap

from nvlib.novx_globals import CH_ROOT
from nvstatistics.statistics_frame import StatisticsFrame


class SectionFrame(StatisticsFrame):

    def draw(self):
        wordsTotal = 0
        sectionWords = {}
        for chId in self._mdl.tree.get_children(CH_ROOT):
            if self._mdl.novel.chapters[chId].chType == 0:
                for scId in self._mdl.tree.get_children(chId):
                    if self._mdl.novel.sections[scId].scType == 0:
                        sectionWords[scId] = self._mdl.novel.sections[scId].wordCount
                        wordsTotal += self._mdl.novel.sections[scId].wordCount
        self.update()
        try:
            xMax = self.winfo_width()
        except:
            # handling delayed refresh while the view is already closed
            return

        x0 = self._LBL_WIDTH + self._LBL_DIST
        x3 = xMax - self._RIGHT_MARGIN
        xSpan = x3 - x0
        wcNorm = xSpan / wordsTotal

        barColor = self.prefs['color_section']
        y = self._LBL_HEIGHT
        self.canvas.delete("all")
        x2 = self._LBL_WIDTH + self._LBL_DIST
        for scId in sectionWords:
            title = textwrap.shorten(self._mdl.novel.sections[scId].title, width=x2 / 5)
            y += self._LBL_HEIGHT
            x1 = x2
            y1 = y
            x2 = x1 + sectionWords[scId] * wcNorm
            y2 = y1 + self._BAR_HEIGHT
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=barColor)
            titleLabel = self.canvas.create_text((x1 - self._LBL_DIST, y + self._HALF_BAR), text=title, fill=self._TEXT_COLOR, anchor='e', tags=scId)
            self.canvas.tag_bind(titleLabel, '<Double-Button-1>', self._on_double_click)
        self._adjust_scrollbar()
