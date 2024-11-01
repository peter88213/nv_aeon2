"""Aeon Timeline 2 sync plugin for novelibre.

Version @release
Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
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
from datetime import datetime
import os
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import webbrowser

from nvaeon2lib.nvaeon2_globals import _
from novxlib.file.doc_open import open_document
from novxlib.novx_globals import Error
from novxlib.novx_globals import norm_path
from nvaeon2lib.json_timeline2 import JsonTimeline2
from nvlib.plugin.plugin_base import PluginBase
import tkinter as tk


class Plugin(PluginBase):
    """Plugin class for synchronization with Aeon Timeline 2."""
    VERSION = '@release'
    API_VERSION = '4.11'
    DESCRIPTION = 'Synchronize with Aeon Timeline 2'
    URL = 'https://github.com/peter88213/nv_aeon2'
    _HELP_URL = f'https://peter88213.github.io/{_("nvhelp-en")}/nv_aeon2/'

    FEATURE = 'Aeon Timeline 2'
    INI_FILENAME = 'nv_aeon2.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        narrative_arc='Narrative',
        property_description='Description',
        property_notes='Notes',
        property_moonphase='Moon phase',
        type_arc='Arc',
        type_character='Character',
        type_location='Location',
        type_item='Item',
        role_arc='Arc',
        role_plotline='Storyline',
        role_character='Participant',
        role_item='Item',
        role_location='Location',
        color_section='Red',
        color_event='Yellow',

    )
    OPTIONS = dict(
        add_moonphase=False,
        lock_on_export=False,
    )

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._timelineButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
                
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._timelineButton.config(state='normal')

    def install(self, model, view, controller, prefs=None):
        """Add a submenu to the main menu.
        
        Positional arguments:
            model -- reference to the main model instance of the application.
            view -- reference to the main view instance of the application.
            controller -- reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Overrides the superclass method.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller

        # Create a submenu in the Tools menu.
        self._pluginMenu = tk.Menu(self._ui.toolsMenu, tearoff=0)
        self._ui.toolsMenu.add_cascade(label=self.FEATURE, menu=self._pluginMenu)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._pluginMenu.add_command(label=_('Information'), command=self._info)
        self._pluginMenu.add_separator()
        # self._pluginMenu.add_command(label=_('Settings'), command=self._edit_settings)
        # self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Update the timeline'), command=self._export_from_novx)
        self._pluginMenu.add_command(label=_('Update the project'), command=self._import_to_novx)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Add or update moon phase data'), command=self._add_moonphase)
        self._pluginMenu.add_separator()
        self._pluginMenu.add_command(label=_('Open Aeon Timeline 2'), command=self._launch_application)

        # Add an entry to the "File > New" menu.
        self._ui.newMenu.add_command(label=_('Create from Aeon Timeline 2...'), command=self._create_novx)

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Aeon 2 plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        #--- Configure the toolbar.
        self._configure_toolbar()

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        self._pluginMenu.entryconfig(_('Update the project'), state='disabled')

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        self._pluginMenu.entryconfig(_('Update the project'), state='normal')

    def _add_moonphase(self):
        """Add/update moon phase data.
        
        Add the moon phase to the event properties.
        If the moon phase event property already exists, just update.
        """
        #--- Try to get persistent configuration data
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if not os.path.isfile(timelinePath):
            return

        sourceDir = os.path.dirname(timelinePath)
        if not sourceDir:
            sourceDir = '.'
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            pluginCnfDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/{self.INI_FILENAME}', f'{sourceDir}/{self.INI_FILENAME}']
        configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        kwargs = {}
        kwargs.update(configuration.settings)
        kwargs.update(configuration.options)
        kwargs['add_moonphase'] = True
        kwargs['nv_service'] = self._mdl.nvService
        timeline = JsonTimeline2(timelinePath, **kwargs)
        timeline.novel = self._mdl.nvService.make_novel()
        try:
            timeline.read()
            timeline.write(timeline.novel)
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(timeline.filePath)}".'
        self._ui.set_status(message)

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
            aeon2Icon = tk.PhotoImage(file=f'{iconPath}/aeon2.png')
        except:
            aeon2Icon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Put a button on the toolbar.
        self._timelineButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Open Aeon Timeline 2'),
            image=aeon2Icon,
            command=self._launch_application
            )
        self._timelineButton.pack(side='left')
        self._timelineButton.image = aeon2Icon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._timelineButton, self._timelineButton['text'])

    def _create_novx(self):
        """Create a novelibre project from a timeline."""
        timelinePath = filedialog.askopenfilename(
            filetypes=[(JsonTimeline2.DESCRIPTION, JsonTimeline2.EXTENSION)],
            defaultextension=JsonTimeline2.EXTENSION,
            )
        if not timelinePath:
            return

        self._ctrl.close_project()
        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{self._mdl.nvService.get_novx_file_extension()}'
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = JsonTimeline2(timelinePath, **kwargs)
        target = self._mdl.nvService.make_novx_file(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        message = ''
        try:
            source.novel = self._mdl.nvService.make_novel()
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
        """Update the timeline file from the novx file.
        
        Note:
        The model's novel is not used as the conversion source here.
        It is considered safer to use a copy of the novel read from the file.
        """
        if not self._mdl.prjFile:
            return

        self._ui.propertiesView.apply_changes()
        self._ui.restore_status()
        if not self._mdl.prjFile.filePath:
            if not self._ctrl.save_project():
                return
                # cannot create a timeline if no novx project exists

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(self.FEATURE))
            return

        if self._mdl.isModified:
            if not self._ui.ask_yes_no(_('Save the project and update the timeline?')):
                return

            self._ctrl.save_project()
        elif not self._ui.ask_yes_no(_('Update the timeline?')):
            return

        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = self._mdl.nvService.make_novx_file(self._mdl.prjFile.filePath, **kwargs)
        source.novel = self._mdl.nvService.make_novel()
        target = JsonTimeline2(timelinePath, **kwargs)
        target.novel = self._mdl.nvService.make_novel()
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
            pluginCnfDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            pluginCnfDir = '.'
        iniFiles = [f'{pluginCnfDir}/{self.INI_FILENAME}', f'{sourceDir}/{self.INI_FILENAME}']
        configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        kwargs = {}
        kwargs.update(configuration.settings)
        kwargs.update(configuration.options)
        return kwargs

    def _import_to_novx(self):
        """Update the current project file from the timeline file.
        
        Note:
        The NvWorkFile object of the open project cannot be used as target object.
        This is because the JsonTimeline2 source object's IDs do not match, so 
        the sections and other elements are identified by their titles when merging.
        If anything goes wrong during the conversion, the model remains untouched.
        """
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(self.FEATURE))
            return

        if not self._ui.ask_yes_no(_('Save the project and update it?')):
            return

        self._ctrl.save_project()
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = JsonTimeline2(timelinePath, **kwargs)
        target = self._mdl.nvService.make_novx_file(self._mdl.prjFile.filePath, **kwargs)
        try:
            target.novel = self._mdl.nvService.make_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(f'{message}')

    def _info(self):
        """Show information about the Aeon Timeline 2 file."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if os.path.isfile(timelinePath):
            try:
                timestamp = os.path.getmtime(timelinePath)
                if timestamp > self._mdl.prjFile.timestamp:
                    cmp = _('newer')
                else:
                    cmp = _('older')
                fileDate = datetime.fromtimestamp(timestamp).strftime('%c')
                message = _('{0} file is {1} than the novelibre project.\n (last saved on {2})').format(self.FEATURE, cmp, fileDate)
            except:
                message = _('Cannot determine file date.')
        else:
            message = _('No {} file available for this project.').format(self.FEATURE)
        messagebox.showinfo(f'{self.FEATURE}', message)

    def _launch_application(self):
        """Launch Aeon Timeline 2 with the current project."""
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if os.path.isfile(timelinePath):
            if self.OPTIONS['lock_on_export']:
                self._ctrl.lock()
            open_document(timelinePath)
        else:
            self._ui.set_status(_('!No {} file available for this project.').format(self.FEATURE))

