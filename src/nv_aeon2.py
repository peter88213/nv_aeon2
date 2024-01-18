"""Aeon Timeline 2 sync plugin for noveltree.

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_aeon2
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
from datetime import datetime
import gettext
import locale
import os
from pathlib import Path
import sys
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from novxlib.config.configuration import Configuration
from novxlib.file.doc_open import open_document
from novxlib.model.novel import Novel
from novxlib.model.nv_tree import NvTree
from novxlib.novx.novx_file import NovxFile
from novxlib.novx_globals import Error
from novxlib.novx_globals import _
from novxlib.novx_globals import norm_path
from nvaeon2lib.json_timeline2 import JsonTimeline2
import tkinter as tk

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
CURRENT_LANGUAGE = locale.getlocale()[0][:2]
try:
    t = gettext.translation('nv_aeon2', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = 'Aeon Timeline 2'
PLUGIN = f'{APPLICATION} plugin v@release'
INI_FILENAME = 'nv_aeon2.ini'
INI_FILEPATH = '.noveltree/config'


class Plugin():
    """Plugin class for synchronization with Aeon Timeline 2."""
    VERSION = '@release'
    NOVELTREE_API = '1.0'
    DESCRIPTION = 'Synchronize with Aeon Timeline 2'
    URL = 'https://peter88213.github.io/noveltree_aeon2'
    _HELP_URL = 'https://peter88213.github.io/noveltree_aeon2/usage'

    SETTINGS = dict(
        default_date_time='2023-01-01 00:00:00',
        narrative_arc='Narrative',
        property_yw7_sync='yw7sync',
        property_description='Description',
        property_notes='Notes',
        property_moonphase='Moon phase',
        role_location='Location',
        role_item='Item',
        role_character='Participant',
        type_character='Character',
        type_location='Location',
        type_item='Item',
        color_section='Red',
        color_event='Yellow',
        color_point='Blue',

    )
    OPTIONS = dict(
        add_moonphase=False,
    )

    def install(self, model, view, controller, prefs):
        """Add a submenu to the main menu.
        
        Positional arguments:
            view -- reference to the NoveltreeUi instance of the application.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Create a submenu in the Tools menu.
        self._pluginMenu = tk.Menu(self._ui.mainMenu, tearoff=0)
        position = self._ui.mainMenu.index('end')
        self._ui.mainMenu.insert_cascade(position, label=APPLICATION, menu=self._pluginMenu)
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        # self._pluginMenu.add_command(label=_('Settings'), command=self._edit_settings)
        # self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Add or update moon phase data'), command=self._add_moonphase)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Edit the timeline'), command=self._launch_application)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from Aeon Timeline 2...'), command=self._create_novx)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Aeon 2 plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='normal')

    def _add_moonphase(self):
        """Add/update moon phase data.
        
        Add the moon phase to the event properties.
        If the moon phase event property already exists, just update.
        """
        #--- Try to get persistent configuration data
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
            if os.path.isfile(timelinePath):
                sourceDir = os.path.dirname(timelinePath)
                if not sourceDir:
                    sourceDir = '.'
                try:
                    homeDir = str(Path.home()).replace('\\', '/')
                    pluginCnfDir = f'{homeDir}/{INI_FILEPATH}'
                except:
                    pluginCnfDir = '.'
                iniFiles = [f'{pluginCnfDir}/{INI_FILENAME}', f'{sourceDir}/{INI_FILENAME}']
                configuration = Configuration(self.SETTINGS, self.OPTIONS)
                for iniFile in iniFiles:
                    configuration.read(iniFile)
                kwargs = {}
                kwargs.update(configuration.settings)
                kwargs.update(configuration.options)
                kwargs['add_moonphase'] = True
                timeline = JsonTimeline2(timelinePath, **kwargs)
                timeline.novel = Novel(tree=NvTree())
                try:
                    timeline.read()
                    timeline.write(timeline.novel)
                except Error as ex:
                    message = f'!{str(ex)}'
                else:
                    message = f'{_("File written")}: "{norm_path(timeline.filePath)}".'
                self._ui.set_status(message)

    def _create_novx(self):
        """Create a noveltree project from a timeline."""
        timelinePath = filedialog.askopenfilename(
            filetypes=[(JsonTimeline2.DESCRIPTION, JsonTimeline2.EXTENSION)],
            defaultextension=JsonTimeline2.EXTENSION,
            )
        if not timelinePath:
            return

        self._ctrl.close_project()
        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{NovxFile.EXTENSION}'
        kwargs = self._get_configuration(timelinePath)
        source = JsonTimeline2(timelinePath, **kwargs)
        target = NovxFile(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        message = ''
        try:
            source.novel = Novel(tree=NvTree())
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(message)

    def _edit_settings(self):
        """Toplevel window"""
        return

    def _export_from_novx(self):
        """Update the timeline from noveltree."""
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
            if not os.path.isfile(timelinePath):
                self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))
                return

            self._ui.restore_status()
            if self._ui.ask_yes_no(_('Save the project and update the timeline?')):
                self._ctrl.save_project()
                kwargs = self._get_configuration(timelinePath)
                source = NovxFile(self._mdl.prjFile.filePath, **kwargs)
                source.novel = Novel(tree=NvTree())
                target = JsonTimeline2(timelinePath, **kwargs)
                target.novel = Novel(tree=NvTree())
                try:
                    source.read()
                    target.read()
                    target.write(source.novel)
                    message = f'{_("File written")}: "{norm_path(target.filePath)}".'
                except Error as ex:
                    message = f'!{str(ex)}'
                self._ui.set_status(message)

    def _get_configuration(self, sourcePath):
        """ Read persistent configuration data for Aeon 2 conversion.
        
        First, look for a global configuration file in the aeon2nv installation directory,
        then look for a local configuration file in the project directory.
        """
        sourceDir = os.path.dirname(sourcePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/{INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/{INI_FILENAME}', f'{sourceDir}/{INI_FILENAME}']
        configuration = Configuration(self.SETTINGS, self.OPTIONS)
        for iniFile in iniFiles:
            configuration.read(iniFile)
        kwargs = {}
        kwargs.update(configuration.settings)
        kwargs.update(configuration.options)
        return kwargs

    def _import_to_novx(self):
        """Update the current project from the timeline.
        
        Note:
        The NvWorkFile object of the open project cannot be used as target object.
        This is because the JsonTimeline2 source object's IDs do not match, so 
        the sections and other elements are identified by their titles when merging.
        """
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
            if not os.path.isfile(timelinePath):
                self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))
                return

            if self._ui.ask_yes_no(_('Save the project and update it?')):
                self._ctrl.save_project()
                kwargs = self._get_configuration(timelinePath)
                source = JsonTimeline2(timelinePath, **kwargs)
                target = NovxFile(self._mdl.prjFile.filePath, **kwargs)
                try:
                    target.novel = Novel(tree=NvTree())
                    target.read()
                    source.novel = target.novel
                    source.read()
                    target.novel = source.novel
                    target.write()
                    message = f'{_("File written")}: "{norm_path(target.filePath)}".'
                except Error as ex:
                    message = f'!{str(ex)}'

                # Reopen the project.
                self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
                self._ui.set_status(message)

    def _info(self):
        """Show information about the Aeon Timeline 2 file."""
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
            if os.path.isfile(timelinePath):
                try:
                    timestamp = os.path.getmtime(timelinePath)
                    if timestamp > self._mdl.prjFile.timestamp:
                        cmp = _('newer')
                    else:
                        cmp = _('older')
                    fileDate = datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat(sep=' ')
                    message = _('{0} file is {1} than the noveltree project.\n (last saved on {2})').format(APPLICATION, cmp, fileDate)
                except:
                    message = _('Cannot determine file date.')
            else:
                message = _('No {} file available for this project.').format(APPLICATION)
            messagebox.showinfo(PLUGIN, message)

    def _launch_application(self):
        """Launch Aeon Timeline 2 with the current project."""
        if self._mdl.prjFile:
            timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
            if os.path.isfile(timelinePath):
                if self._ctrl.lock():
                    open_document(timelinePath)
            else:
                self._ui.set_status(_('!No {} file available for this project.').format(APPLICATION))
