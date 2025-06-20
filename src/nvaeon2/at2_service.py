"""Provide an Aeon Timeline 2 service class for novelibre.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from datetime import datetime
import os
from pathlib import Path
from tkinter import filedialog

from nvaeon2.json_timeline2 import JsonTimeline2
from nvaeon2.nvaeon2_locale import _
from nvlib.controller.services.service_base import ServiceBase
from nvlib.model.file.doc_open import open_document
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path


class At2Service(ServiceBase):
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

    def __init__(self, model, view, controller, windowTitle):
        super().__init__(model, view, controller)
        self.windowTitle = windowTitle

    def add_moonphase(self):
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
        configuration = self._mdl.nvService.new_configuration(
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
        timeline.novel = self._mdl.nvService.new_novel()
        try:
            timeline.read()
            timeline.write(timeline.novel)
        except Error as ex:
            message = f'!{str(ex)}'
        else:
            message = f'{_("File written")}: "{norm_path(timeline.filePath)}".'
        self._ui.set_status(message)

    def create_novx(self):
        """Create a novelibre project from a timeline."""
        self._ui.restore_status()
        timelinePath = filedialog.askopenfilename(
            filetypes=[(JsonTimeline2.DESCRIPTION, JsonTimeline2.EXTENSION)],
            defaultextension=JsonTimeline2.EXTENSION,
            )
        if not timelinePath:
            return

        if not self._ctrl.close_project():
            return

        root, __ = os.path.splitext(timelinePath)
        novxPath = f'{root}{self._mdl.nvService.get_novx_file_extension()}'
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = JsonTimeline2(timelinePath, **kwargs)
        target = self._mdl.nvService.new_novx_file(novxPath)

        if os.path.isfile(target.filePath):
            self._ui.set_status(f'!{_("File already exists")}: "{norm_path(target.filePath)}".')
            return

        statusMsg = ''
        try:
            source.novel = self._mdl.nvService.new_novel()
            source.read()
            target.novel = source.novel
            target.write()
        except Error as ex:
            statusMsg = f'!{str(ex)}'
        else:
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            statusMsg = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=target.filePath, doNotSave=True)
        finally:
            self._ui.set_status(statusMsg)

    def export_from_novx(self):
        """Update the timeline file from the novx file.
        
        Note:
        The model's novel is not used as the conversion source here.
        It is considered safer to use a copy of the novel read from the file.
        """
        self._ui.restore_status()
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
            self._ui.set_status(_('!No {} file available for this project.').format(self.windowTitle))
            return

        if self._mdl.isModified:
            if not self._ui.ask_yes_no(
                message=_('Save the project and update the timeline?'),
                detail=f"{_('There are unsaved changes')}.",
                title=self.windowTitle
                ):
                return

            self._ctrl.save_project()
        elif not self._ui.ask_yes_no(
            message=_('Update the timeline?'),
            title=self.windowTitle
            ):
            return

        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = self._mdl.nvService.new_novx_file(self._mdl.prjFile.filePath, **kwargs)
        source.novel = self._mdl.nvService.new_novel()
        target = JsonTimeline2(timelinePath, **kwargs)
        target.novel = self._mdl.nvService.new_novel()
        try:
            source.read()
            target.read()
            target.write(source.novel)
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(message)

    def import_to_novx(self):
        """Update the current project file from the timeline file.
        
        Note:
        The NvWorkFile object of the open project cannot be used as target object.
        This is because the JsonTimeline2 source object's IDs do not match, so 
        the sections and other elements are identified by their titles when merging.
        If anything goes wrong during the conversion, the model remains untouched.
        """
        self._ui.restore_status()
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        if not os.path.isfile(timelinePath):
            self._ui.set_status(_('!No {} file available for this project.').format(self.windowTitle))
            return

        if not self._ui.ask_yes_no(
            _('Save the project and update it?'),
            title=self.windowTitle
            ):
            return

        self._ctrl.save_project()
        kwargs = self._get_configuration(timelinePath)
        kwargs['nv_service'] = self._mdl.nvService
        source = JsonTimeline2(timelinePath, **kwargs)
        target = self._mdl.nvService.new_novx_file(self._mdl.prjFile.filePath, **kwargs)
        message = ''
        try:
            target.novel = self._mdl.nvService.new_novel()
            target.read()
            source.novel = target.novel
            source.read()
            target.novel = source.novel
            target.write()
            self._ctrl.fileManager.copy_to_backup(target.filePath)
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self._ctrl.open_project(filePath=self._mdl.prjFile.filePath, doNotSave=True)
        except Error as ex:
            message = f'!{str(ex)}'
        self._ui.set_status(f'{message}')

    def info(self):
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
                tlInfo = _('{0} file is {1} than the novelibre project.\n (last saved on {2})').format(self.windowTitle, cmp, fileDate)
            except:
                tlInfo = _('Cannot determine file date.')
        else:
            tlInfo = _('No {} file available for this project.').format(self.windowTitle)
        self._ui.show_info(
            message=self.windowTitle,
            detail=tlInfo,
            title=_('Information')
            )

    def launch_application(self):
        """Launch Aeon Timeline 2 with the current project."""
        self._ui.restore_status()
        if not self._mdl.prjFile:
            return

        timelinePath = f'{os.path.splitext(self._mdl.prjFile.filePath)[0]}{JsonTimeline2.EXTENSION}'
        prefs = self._get_configuration(timelinePath)
        if os.path.isfile(timelinePath):
            if prefs['lock_on_export']:
                self._ctrl.lock()
            try:
                open_document(timelinePath)
            except Exception as ex:
                self._ui.set_status(f'!{str(ex)}')
        else:
            self._ui.set_status(_('!No {} file available for this project.').format(self.windowTitle))

    def _get_configuration(self, sourcePath):
        """ Read persistent configuration data for Aeon 2 conversion.
        
        First, look for a global configuration file in the novelibre installation directory,
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
        configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        for iniFile in iniFiles:
            configuration.read(iniFile)
        kwargs = {}
        kwargs.update(configuration.settings)
        kwargs.update(configuration.options)
        return kwargs

