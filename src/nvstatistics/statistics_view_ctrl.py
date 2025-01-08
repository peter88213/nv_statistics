"""Provide a mixin class controlling the the statistics display.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController


class StatisticsViewCtrl(SubController):

    def initialize_controller(self, model, view, controller):
        super().initialize_controller(model, view, controller)
        self.isOpen = True
        # self.activeFrame.draw()

    def draw(self, event=None):
        if self.calculating:
            return

        self.calculating = True
        self.activeFrame.draw()
        self.calculating = False
