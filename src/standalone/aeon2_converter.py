"""Provide a converter class for test_aeon2yw. 

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os

from nvaeon2.json_timeline2 import JsonTimeline2
from nvaeon2.nvaeon2_locale import _
from nvlib.controller.services.nv_service import NvService
from nvlib.model.converter.converter import Converter
from nvlib.novx_globals import Error
from nvlib.novx_globals import norm_path


class Aeon2Converter(Converter):
    """A converter class for novelibre and Aeon Timeline 2."""

    def run(self, sourcePath, **kwargs):
        """Create source and target objects and run conversion.

        Positional arguments: 
            sourcePath: str -- the source file path.
        
        The direction of the conversion is determined by the source file type.
        Only novelibre project files and Aeon Timeline 2 files are accepted.
        """
        nvService = NvService()
        kwargs['nv_service'] = nvService
        if not os.path.isfile(sourcePath):
            self.ui.set_status(f'!{_("File not found")}: "{norm_path(sourcePath)}".')
            return

        fileName, fileExtension = os.path.splitext(sourcePath)
        if fileExtension == JsonTimeline2.EXTENSION:
            # Source is a timeline
            sourceFile = JsonTimeline2(sourcePath, **kwargs)
            if os.path.isfile(f'{fileName}{nvService.get_novx_file_extension()}'):
                # Update existing novelibre project from timeline
                targetFile = nvService.new_novx_file(f'{fileName}{nvService.get_novx_file_extension()}', **kwargs)
                self._import_to_novx(sourceFile, targetFile)
            else:
                # Create new novelibre project from timeline
                targetFile = nvService.new_novx_file(f'{fileName}{nvService.get_novx_file_extension()}', **kwargs)
                self._create_novx(sourceFile, targetFile)
        elif fileExtension == nvService.get_novx_file_extension():
            # Update existing timeline from novelibre project
            sourceFile = nvService.new_novx_file(sourcePath, **kwargs)
            targetFile = JsonTimeline2(f'{fileName}{JsonTimeline2.EXTENSION}', **kwargs)
            self._export_from_novx(sourceFile, targetFile)
        else:
            # Source file format is not supported
            self.ui.set_status(f'!{_("File type is not supported")}: "{norm_path(sourcePath)}".')

    def _export_from_novx(self, source, target):
        """Convert from novelibre project to other file format.

        Positional arguments:
            source -- NovxFile instance.
            target -- JsonTimeline2 instance.

        Operation:
        1. Send specific information about the conversion to the UI.
        2. Convert source into target.
        3. Pass the message to the UI.
        4. Save the new file pathname.

        Error handling:
        - If the conversion fails, newFile is set to None.
        
        Overrides the superclass method.
        """
        nvService = NvService()
        self.ui.set_info(
            _('Input: {0} "{1}"\nOutput: {2} "{3}"').format(source.DESCRIPTION, norm_path(source.filePath), target.DESCRIPTION, norm_path(target.filePath)))
        message = ''
        try:
            self._check(source, target)
            source.novel = nvService.new_novel()
            target.novel = nvService.new_novel()
            source.read()
            target.read()
            target.write(source.novel)
        except Error as ex:
            message = f'!{str(ex)}'
            self.newFile = None
        else:
            message = f'{_("File written")}: "{norm_path(target.filePath)}".'
            self.newFile = target.filePath
        finally:
            self.ui.set_status(message)
