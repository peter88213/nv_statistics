"""Project statistics view plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_statistics
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
from pathlib import Path
import webbrowser

from mvclib.view.set_icon_tk import set_icon
from nvlib.controller.plugin.plugin_base import PluginBase
from nvstatistics.nvstatistics_locale import _
from nvstatistics.statistics_view import StatisticsView


class Plugin(PluginBase):
    """Statistics view plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'Plugin template'
    URL = 'https://github.com/peter88213/nv_statistics'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_statistics'

    FEATURE = _('Project statistics view')
    INI_FILENAME = 'statistics.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='510x440',
    )
    OPTIONS = {}

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')

    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
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

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Project statistics Online help'), command=self.open_help_page)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self.start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

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

    def open_help_page(self, event=None):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        if self.statisticsView is not None:
            if self.statisticsView.isOpen:
                if self.statisticsView.state() == 'iconic':
                    self.statisticsView.state('normal')
                self.statisticsView.lift()
                self.statisticsView.focus()
                return

        self.statisticsView = StatisticsView(self._mdl, self._ui, self._ctrl, self.prefs)
        self.statisticsView.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        set_icon(self.statisticsView, icon='sLogo32', default=False)
