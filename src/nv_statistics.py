"""Project statistics view plugin for novelibre.

Requires Python 3.6+
Copyright (c) 2025 Peter Triesberger
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
from tkinter import ttk
import webbrowser

from nvstatistics.nvstatistics_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvstatistics.statistics_service import StatisticsService
import tkinter as tk


class Plugin(PluginBase):
    """Statistics view plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A project statistics view'
    URL = 'https://github.com/peter88213/nv_statistics'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_statistics'

    FEATURE = _('Project statistics view')

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._stButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._stButton.config(state='normal')

    def install(self, model, view, controller):
        """Install the plugin.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.statisticsService = StatisticsService(model, view, controller)

        # Create an entry in the Tools menu.
        self._ui.toolsMenu.add_command(
            label=self.FEATURE,
            command=self.start_viewer,
        )
        self._ui.toolsMenu.entryconfig(
            self.FEATURE,
            state='disabled',
        )

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(
            label=_('Project statistics Online help'),
            command=self.open_help,
        )

        #--- Configure the toolbar.
        self._configure_toolbar()

    def on_close(self):
        self.statisticsService.on_close()

    def on_quit(self):
        self.statisticsService.on_quit()

    def open_help(self, event=None):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        self.statisticsService.start_viewer(self.FEATURE)

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None
        try:
            tlIcon = tk.PhotoImage(file=f'{iconPath}/statistics.png')
        except:
            tlIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(
            self._ui.toolbar.buttonBar,
            bg='light gray',
            width=1,
        ).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._stButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=self.FEATURE,
            image=tlIcon,
            command=self.start_viewer,
        )
        self._stButton.pack(side='left')
        self._stButton.image = tlIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._stButton, self._stButton['text'])

