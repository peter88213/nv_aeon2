"""Aeon Timeline 2 sync plugin for novelibre.

Version @release
Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
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
import webbrowser

from nvaeon2.nvaeon2_locale import _
from nvaeon2.at2_service import At2Service
from nvlib.controller.plugin.plugin_base import PluginBase
from nvlib.gui.menus.nv_menu import NvMenu


# must be the first import here
class Plugin(PluginBase):
    """Plugin class for synchronization with Aeon Timeline 2."""
    VERSION = '@release'
    API_VERSION = '5.43'
    DESCRIPTION = 'Synchronize with Aeon Timeline 2'
    URL = 'https://github.com/peter88213/nv_aeon2'
    HELP_URL = _('https://peter88213.github.io/nv_aeon2/help/')

    FEATURE = 'Aeon Timeline 2'

    def add_moonphase(self):
        self.timelineService.add_moonphase()

    def create_novx(self):
        self.timelineService.create_novx()

    def export_from_novx(self):
        self.timelineService.export_from_novx()

    def import_to_novx(self):
        self.timelineService.import_to_novx()

    def info(self):
        self.timelineService.info()

    def install(self, model, view, controller):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the novelibre main model instance.
            view -- reference to the novelibre main view instance.
            controller -- reference to the novelibre main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.timelineService = At2Service(
            model,
            view,
            controller,
            self.FEATURE
        )
        self._icon = self._get_icon('aeon2.png')

        #--- Configure the main menu.

        # Create a submenu in the Tools menu.
        label = self.FEATURE
        self.pluginMenu = NvMenu()
        self._ui.toolsMenu.add_cascade(
            label=label,
            image=self._icon,
            compound='left',
            menu=self.pluginMenu,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        label = _('Information')
        self.pluginMenu.add_command(
            label=label,
            command=self.info,
        )

        label = _('Update the timeline')
        self.pluginMenu.add_separator()
        self.pluginMenu.add_command(
            label=label,
            command=self.export_from_novx,
        )

        label = _('Update the project')
        self.pluginMenu.add_command(
            label=label,
            command=self.import_to_novx,
        )
        self.pluginMenu.disableOnLock.append(label)

        label = _('Add or update moon phase data')
        self.pluginMenu.add_separator()
        self.pluginMenu.add_command(
            label=label,
            command=self.add_moonphase,
        )

        self.pluginMenu.add_separator()

        label = _('Open Aeon Timeline 2')
        self.pluginMenu.add_command(
            label=label,
            command=self.launch_application,
        )

        # Add an entry to the "File > New" menu.
        label = _('Create from Aeon Timeline 2...')
        self._ui.newMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.create_novx,
        )

        # Add an entry to the Help menu.
        label = _('Aeon 2 plugin Online help')
        self._ui.helpMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=self.open_help,
        )

        #--- Configure the toolbar.
        self._ui.toolbar.add_separator(),

        # Put a button on the toolbar.
        self._ui.toolbar.new_button(
            text=_('Open Aeon Timeline 2'),
            image=self._icon,
            command=self.launch_application,
            disableOnLock=False,
        ).pack(side='left')

    def launch_application(self):
        self.timelineService.launch_application()

    def lock(self):
        self.pluginMenu.lock()

    def open_help(self):
        webbrowser.open(self.HELP_URL)

    def unlock(self):
        self.pluginMenu.unlock()

