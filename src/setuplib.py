"""nv_aeon2 installer library module. 

Version @release

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from pathlib import Path
from shutil import copy2
from shutil import copytree
from shutil import rmtree
import sys
import zipfile

PLUGIN = 'nv_aeon2.py'
VERSION = ' @release'
PRJ = 'nv_aeon2'

pyz = os.path.dirname(__file__)


def extract_file(sourceFile, targetDir):
    with zipfile.ZipFile(pyz) as z:
        z.extract(sourceFile, targetDir)


def extract_tree(sourceDir, targetDir):
    with zipfile.ZipFile(pyz) as z:
        for file in z.namelist():
            if file.startswith(f'{sourceDir}/'):
                z.extract(file, targetDir)


def cp_tree(sourceDir, targetDir):
    copytree(sourceDir, f'{targetDir}/{sourceDir}', dirs_exist_ok=True)


def main(zipped=True):
    if zipped:
        copy_file = extract_file
        copy_tree = extract_tree
    else:
        copy_file = copy2
        copy_tree = cp_tree

    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    print(f'*** Installing {PLUGIN} {VERSION} ***')
    homePath = str(Path.home()).replace('\\', '/')
    applicationDir = f'{homePath}/.novx'
    if os.path.isdir(applicationDir):
        pluginDir = f'{applicationDir}/plugin'
        os.makedirs(pluginDir, exist_ok=True)

        # Install the plugin.
        print(f'Copying "{PLUGIN}" ...')
        copy_file(PLUGIN, pluginDir)

        # Install the localization files.
        print('Copying locale ...')
        copy_tree('locale', applicationDir)

        # Install the icons.
        print('Copying icons ...')
        copy_tree('icons', applicationDir)

        # Provide the sample files.
        print('Copying/replacing sample files ...')
        rmtree(f'{applicationDir}/{PRJ}_sample', ignore_errors=True)
        copy_tree(f'{PRJ}_sample', applicationDir)

        # Show a success message.
        print(
            f'Sucessfully installed "{PLUGIN}" '
            f'at "{os.path.normpath(pluginDir)}".'
        )
    else:
        print(
            'ERROR: Cannot find a novelibre installation '
            f'at "{os.path.normpath(applicationDir)}".'
        )

    input('Press any key to quit.')
