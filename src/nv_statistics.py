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

from mvclib.view.set_icon_tk import set_icon
from nvlib.plugin.plugin_base import PluginBase
from nvstatisticslib.linked_percentage_bar import LinkedPercentageBar
from nvstatisticslib.nvstatistics_globals import _
from nvstatisticslib.nvstatistics_globals import open_help
from nvstatisticslib.statistics_viewer import StatisticsViewer


class Plugin(PluginBase):
    """Statistics view plugin class."""
    VERSION = '@release'
    API_VERSION = '4.11'
    DESCRIPTION = 'Plugin template'
    URL = 'https://github.com/peter88213/nv_statistics'

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
        self._statistics_viewer = None

        # Initialize the class (this hack makes the interface smaller):
        LinkedPercentageBar.treeView = self._ui.tv

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Project statistics Online help'), command=open_help)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

        # Register as a client.
        self._mdl.add_observer(self)

    def on_close(self):
        """Close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Write back the configuration file.
        
        Overrides the superclass method.
        """
        if self._statistics_viewer is not None:
            if self._statistics_viewer.isOpen:
                self._statistics_viewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def refresh(self):
        if self._statistics_viewer is not None:
            if self._statistics_viewer.isOpen:
                self._statistics_viewer.calculate_statistics()

    def _start_viewer(self):
        if self._statistics_viewer is not None:
            if self._statistics_viewer.isOpen:
                if self._statistics_viewer.state() == 'iconic':
                    self._statistics_viewer.state('normal')
                self._statistics_viewer.lift()
                self._statistics_viewer.focus()
                self._statistics_viewer.build_tree()
                return

        self._statistics_viewer = StatisticsViewer(self, self._mdl, self._ui)
        self._statistics_viewer.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        set_icon(self._statistics_viewer, icon='sLogo32', default=False)
