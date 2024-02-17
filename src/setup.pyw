#!/usr/bin/python3
"""Install the nv_aeon2 plugin. 

Version @release

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_collection
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from shutil import copytree
from shutil import copyfile
from shutil import copy2
from pathlib import Path
try:
    from tkinter import *
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)
from tkinter import messagebox

PLUGIN = 'nv_aeon2.py'
VERSION = ' @release'
CONFIGURATION = 'nv_aeon2.ini'

root = Tk()
processInfo = Label(root, text='')
message = []


def install_template():
    """Install the Aeon2 sample template, if needed."""
    try:
        appDataLocal = os.getenv('LOCALAPPDATA').replace('\\', '/')
        aeon2dir = f'{appDataLocal}/Scribble Code/Aeon Timeline 2/CustomTemplates/'
        sampleTemplate = 'noveltree.xml'
        if not os.path.isfile(aeon2dir + sampleTemplate):
            copy2(f'sample/{sampleTemplate}', f'{aeon2dir}{sampleTemplate}')
            output(f'Copying "{sampleTemplate}"')
        else:
            if messagebox.askyesno('Aeon Timeline 2 "yWriter" template', f'Update "{aeon2dir}{sampleTemplate}"?'):
                copy2(f'sample/{sampleTemplate}', f'{aeon2dir}{sampleTemplate}')
                output(f'Updating "{sampleTemplate}"')
                root.tplButton['state'] = DISABLED
    except:
        pass


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


if __name__ == '__main__':
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("600x250")
    root.title(f'Install {PLUGIN}{VERSION}')
    header = Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Install the plugin.
    homePath = str(Path.home()).replace('\\', '/')
    noveltreeDir = f'{homePath}/.noveltree'
    if os.path.isdir(noveltreeDir):
        if os.path.isfile(f'./{PLUGIN}'):
            pluginDir = f'{noveltreeDir}/plugin'
            os.makedirs(pluginDir, exist_ok=True)
            copyfile(PLUGIN, f'{pluginDir}/{PLUGIN}')
            output(f'Sucessfully installed "{PLUGIN}" at "{os.path.normpath(pluginDir)}"')
        else:
            output(f'ERROR: file "{PLUGIN}" not found.')

        # Install the localization files.
        copytree('locale', f'{noveltreeDir}/locale', dirs_exist_ok=True)
        output(f'Copying "locale"')

        # Install the configuration file.
        configDir = f'{noveltreeDir}/config'
        if os.path.isfile(f'{configDir}/{CONFIGURATION}'):
            output(f'Keeping configuration file')
        else:
            os.makedirs(configDir, exist_ok=True)
            copy2(f'sample/{CONFIGURATION}', configDir)
            output(f'Copying configuration file')

    else:
        output(f'ERROR: Cannot find a noveltree installation at "{noveltreeDir}"')

    root.tplButton = Button(text="Install the Aeon2 sample template", command=lambda: install_template())
    root.tplButton.config(height=1, width=30)
    root.tplButton.pack(padx=5, pady=5)
    root.quitButton = Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
