"""Provide a service class for the statistics viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvlib.gui.set_icon_tk import set_icon
from nvstatistics.statistics_view import StatisticsView


class StatisticsService(SubController):
    INI_FILENAME = 'statistics.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='510x440',
        color_plotline='deepSkyBlue',
        color_viewpoint='goldenrod1',
        color_section='greenyellow',
        color_part='aquamarine1',
        color_chapter='green',
        color_stage1='red',
        color_stage2='orange',
        color_background='black',
        color_text='white',
        color_filler='gray15',
    )
    OPTIONS = {}

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self.statisticsView = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
        )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self.statisticsView is not None:
            if self.statisticsView.isOpen:
                self.statisticsView.on_quit()

        #--- Save configuration
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)

    def start_viewer(self, windowTitle):
        if self.statisticsView is not None:
            if self.statisticsView.isOpen:
                if self.statisticsView.state() == 'iconic':
                    self.statisticsView.state('normal')
                self.statisticsView.lift()
                self.statisticsView.focus()
                return

        self.statisticsView = StatisticsView(
            self._mdl,
            self._ui,
            self._ctrl,
            self.prefs,
        )
        self.statisticsView.title(f'{self._mdl.novel.title} - {windowTitle}')
        set_icon(self.statisticsView, icon='sLogo32', default=False)
