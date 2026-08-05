"""Project statistics view plugin for novelibre.

Requires Python 3.7+
Copyright (c) Peter Triesberger
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
from nvlib.controller.plugin.plugin_base import PluginBase
from nvstatistics.nvstatistics_locale import _
from nvstatistics.statistics_service import StatisticsService


class Plugin(PluginBase):
    """Statistics view plugin class."""
    VERSION = '@release'
    API_VERSION = '5.63'
    DESCRIPTION = 'A project statistics view'
    URL = 'https://github.com/peter88213/nv_statistics'
    HELP_PAGE = 'nv_statistics'

    FEATURE = _('Project statistics view')

    def install(self, model, view, controller):
        """Install the plugin at runtime.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """

        super().install(model, view, controller)
        self.statisticsService = StatisticsService(model, view, controller)
        self._icon = self._get_icon('statistics.png')

        #--- Configure the user interface.

        def start_viewer():
            self.statisticsService.start_viewer(self.FEATURE)

        # Add an entry to the Tools menu.
        label = self.FEATURE
        self._ui.toolsMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=start_viewer,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        self._add_help_menu_entry(_('Project statistics plugin help'))

        # Put a button on the toolbar.
        self._ui.toolbar.add_separator(),
        self._ui.toolbar.new_button(
            text=self.FEATURE,
            image=self._icon,
            command=start_viewer,
            disableOnLock=False,
        ).pack(side='left')

    def on_close(self):
        self.statisticsService.on_close()

    def on_quit(self):
        self.statisticsService.on_quit()

