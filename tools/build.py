"""Build the nv_aeon2 novelibre plugin.
        
In order to distribute a single script without dependencies, 
this script "inlines" all modules imported from the novxlib package.

The novxlib project (see see https://github.com/peter88213/novxlib)
must be located on the same directory level as the aeon2nv project. 

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
from shutil import rmtree
import sys
sys.path.insert(0, f'{os.getcwd()}/../../novxlib/src')
import inliner
import build_tools
import translate_de

VERSION = 'x.x.x'

APP = 'nv_aeon2'
RELEASE = f'{APP}_v{VERSION}'
MO_FILE = 'nv_aeon2.mo'

LOCAL_LIB = 'nvaeon2lib'
LOCAL_LIB_PATH = '../../nv_aeon2/src/'
SOURCE_DIR = '../src/'
TEST_DIR = '../test/'
SOURCE_FILE = f'{SOURCE_DIR}nv_aeon2.py'
TEST_FILE = f'{TEST_DIR}nv_aeon2.py'
BUILD_BASE = '../build'
BUILD_DIR = f'{BUILD_BASE}/{RELEASE}'
DIST_DIR = '../dist'

distFiles = [
    (TEST_FILE, BUILD_DIR),
    (f'{SOURCE_DIR}setuplib.py', BUILD_DIR),
    ('../LICENSE', BUILD_DIR),
]


def build_package():
    print(f'\nProviding empty "{DIST_DIR}" ...')
    try:
        rmtree(DIST_DIR)
    except FileNotFoundError:
        pass
    os.makedirs(DIST_DIR)
    build_tools.make_pyz(BUILD_DIR, DIST_DIR, RELEASE)
    build_tools.make_zip(BUILD_DIR, DIST_DIR, RELEASE)


def build_plugin():
    os.makedirs(TEST_DIR, exist_ok=True)
    inliner.run(SOURCE_FILE, TEST_FILE, LOCAL_LIB, LOCAL_LIB_PATH)
    build_tools.inline_modules(TEST_FILE, TEST_FILE)
    build_tools.insert_version_number(TEST_FILE, version=VERSION)


def build_translation():
    if not MO_FILE:
        return

    if not build_tools.make_pot(TEST_FILE, app=APP, version=VERSION):
        sys.exit(1)

    translation = translate_de.main(
        MO_FILE, app=APP, version=VERSION)
    if translation is None:
        sys.exit(1)

    i18Dir, moDir = translation
    distFiles.append(
        (f'{i18Dir}/{moDir}/{MO_FILE}', f'{BUILD_DIR}/{moDir}')
        )


def clean_up():
    print(f'\nRemoving "{TEST_FILE}" ...')
    os.remove(TEST_FILE)


def prepare_package():
    print(f'\nProviding empty "{BUILD_DIR}" ...')
    try:
        rmtree(BUILD_BASE)
    except FileNotFoundError:
        pass
    build_tools.collect_dist_files(distFiles)
    build_tools.insert_version_number(
        f'{BUILD_DIR}/setuplib.py',
        version=VERSION
        )


def main():
    build_plugin()
    build_translation()
    prepare_package()
    build_package()
    clean_up()


if __name__ == '__main__':
    main()
