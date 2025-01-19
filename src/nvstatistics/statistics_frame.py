"""Provide a class for project statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC, abstractmethod

from mvclib.controller.sub_controller import SubController
from nvstatistics.scroll_frame import ScrollFrame


class StatisticsFrame(ABC, ScrollFrame, SubController):
    _LBL_WIDTH = 200
    _LBL_DIST = 10
    _RIGHT_MARGIN = 40
    _LBL_HEIGHT = 20
    _BAR_HEIGHT = 10

    def __init__(self, model, view, controller, prefs, parent, *args, **kw):
        ScrollFrame.__init__(self, parent, *args, **kw)
        super().initialize_controller(model, view, controller)
        self.prefs = prefs
        self._HALF_BAR = self._BAR_HEIGHT / 2
        self._TEXT_COLOR = self.prefs['color_text']
        self._BG_COLOR = self.prefs['color_filler']
        self._TEXT_MAX = self._LBL_WIDTH / 5
        self.canvas['background'] = self.prefs['color_background']
        self.wordsTotal = 0

    @abstractmethod
    def draw(self):
        pass

    def _adjust_scrollbar(self):
        totalBounds = self.canvas.bbox('all')
        if totalBounds is not None:
            self.canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

    def _get_element_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _get_win_scaling(self):
        self.update_idletasks()
        x0 = self._LBL_WIDTH + self._LBL_DIST
        x3 = self.winfo_width() - self._RIGHT_MARGIN
        try:
            wcNorm = (x3 - x0) / self.wordsTotal
        except ZeroDivisionError:
            wcNorm = 0
        return wcNorm, x0, x3

    def _on_double_click(self, event):
        """Select the double-clicked section in the project tree."""
        elementId = self._get_element_id(event)
        self._ui.tv.go_to_node(elementId)

