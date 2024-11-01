"""Build the nv_aeon2 novelibre plugin package.
        
Note: VERSION must be updated manually before starting this script.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '4.8.1'


class PluginBuilder(PackageBuilder):

    PRJ_NAME = 'nv_aeon2'
    LOCAL_LIB = 'nvaeon2lib'
    GERMAN_TRANSLATION = True

    def __init__(self, version):
        super().__init__(version)
        self.sampleTarget = f'{self.buildDir}/{self.PRJ_NAME}_sample'

    def add_extras(self):
        self.add_sample()
        self.add_icons()


def main():
    pb = PluginBuilder(VERSION)
    pb.run()


if __name__ == '__main__':
    main()
