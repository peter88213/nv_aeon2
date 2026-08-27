"""Build the aeon2_novx application package.
        
Note: VERSION must be updated manually before starting this script.

For further information see https://github.com/peter88213/nv_aeon2
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
from shutil import rmtree

sys.path.insert(0, f'{os.getcwd()}/../../novelibre/tools')
from package_builder import PackageBuilder

VERSION = '5.9.3'


def output(message):
    print(f'(package_builder) {message}')


class ApplicationBuilder(PackageBuilder):

    PRJ_NAME = 'aeon2_novx'
    LOCAL_LIB = 'nvaeon2'

    def __init__(self, version):
        """Extends the superclass constructor."""
        super().__init__(version)
        self.buildDir = '../standalone'
        self.sourceFile = f'{self.sourceDir}{self.PRJ_NAME}_.py'
        self.distFiles = [(self.testFile, self.buildDir)]

    def prepare_package(self):
        """Create the package directory and populate it with the basic files."""
        output(f'\nProviding empty "{self.buildDir}" ...')
        try:
            rmtree(self.buildBase)
        except FileNotFoundError:
            pass
        self.collect_dist_files(self.distFiles)

    def build_package(self):
        return


def main():
    ab = ApplicationBuilder(VERSION)
    ab.run()


if __name__ == '__main__':
    main()

