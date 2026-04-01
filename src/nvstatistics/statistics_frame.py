"""Provide a class for project statistics display.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from abc import ABC

from nvlib.controller.sub_controller import SubController
from nvstatistics.nvstatistics_globals import prefs
from nvstatistics.scroll_frame import ScrollFrame


class StatisticsFrame(ABC, ScrollFrame, SubController):
    _LBL_WIDTH = 200
    _LBL_DIST = 10
    _RIGHT_MARGIN = 40
    _LBL_HEIGHT = 20
    _BAR_HEIGHT = 10

    def __init__(self, model, view, controller, parent, *args, **kw):
        ScrollFrame.__init__(self, parent, *args, **kw)
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._HALF_BAR = self._BAR_HEIGHT / 2
        self._TEXT_MAX = self._LBL_WIDTH / 5
        self.wordsTotal = 0

    def draw(self):
        self.canvas['background'] = prefs['color_background']

    def _adjust_scrollbar(self):
        totalBounds = self.canvas.bbox('all')
        if totalBounds is not None:
            self.canvas.configure(scrollregion=(0, 0, 0, totalBounds[3]))

    def _get_element_id(self, event):
        return event.widget.itemcget('current', 'tag').split(' ')[0]

    def _get_win_scaling(self):
        self.update()
        # update() makes resizing the window smoother than update_idletasks().
        # However, this requires the semaphore used with the
        # StatisticsView.redraw() method.

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

