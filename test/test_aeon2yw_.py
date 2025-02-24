""" Python unit tests for the aeon2yw project.

Test suite for aeon2yw.pyw.

For further information see https://github.com/peter88213/aeon2yw
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import codecs
from io import StringIO
from json import JSONDecodeError
import json
import os
from shutil import copyfile
import sys
import unittest
import zipfile

from standalone.aeon2_converter import Aeon2Converter
from nvlib.configuration.configuration import Configuration
from nvlib.user_interface.ui import Ui

UPDATE = False

# Test environment
# The paths are relative to the "test" directory,
# where this script is placed and executed
TEST_PATH = os.getcwd() + '/../test'
TEST_DATA_PATH = TEST_PATH + '/data/'
TEST_EXEC_PATH = TEST_PATH + '/temp/'
APPNAME = 'nv_aeon2'
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

# Test data
INI_FILE = TEST_EXEC_PATH + 'nv_aeon2.ini'
TEST_NOVX = TEST_EXEC_PATH + 'yw7 Sample Project.novx'
TEST_NOVX_BAK = TEST_EXEC_PATH + 'yw7 Sample Project.novx.bak'
TEST_AEON = TEST_EXEC_PATH + 'yw7 Sample Project.aeonzip'
TEST_AEON_BAK = TEST_EXEC_PATH + 'yw7 Sample Project.aeonzip.bak'


def convert(sourcePath, installDir='.'):

    # Try to get persistent configuration data
    sourceDir = os.path.dirname(sourcePath)
    iniFileName = f'{APPNAME}.ini'
    iniFiles = [f'{installDir}/{iniFileName}', f'{sourceDir}/{iniFileName}']
    configuration = Configuration(SETTINGS, OPTIONS)
    for iniFile in iniFiles:
        configuration.read(iniFile)
    kwargs = {'suffix': ''}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    # Convert the file specified by sourcePath.
    converter = Aeon2Converter()
    converter.ui = Ui('')
    converter.run(sourcePath, **kwargs)

    # Write error message, if any.
    sys.stderr.write(converter.ui.infoHowText)


def open_timeline(filePath):
    """Unzip the project file and read 'timeline.json'.
    Return the JSON timeline structure.
    """
    with zipfile.ZipFile(filePath, 'r') as myzip:
        jsonBytes = myzip.read('timeline.json')
        jsonStr = codecs.decode(jsonBytes, encoding='utf-8')
    return json.loads(jsonStr)


def read_file(inputFile):
    try:
        with open(inputFile, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        # HTML files exported by a word processor may be ANSI encoded.
        with open(inputFile, 'r') as f:
            return f.read()


def remove_all_testfiles():
    try:
        os.remove(TEST_NOVX)
    except:
        pass
    try:
        os.remove(TEST_NOVX_BAK)
    except:
        pass
    try:
        os.remove(TEST_AEON_BAK)
    except:
        pass
    try:
        os.remove(TEST_AEON)
    except:
        pass
    try:
        os.remove(INI_FILE)
    except:
        pass


class NormalOperation(unittest.TestCase):
    """Test case: Normal operation."""

    def setUp(self):
        self.test_out = StringIO()
        self.test_err = StringIO()
        self.original_output = sys.stdout
        self.original_err = sys.stderr
        sys.stdout = self.test_out
        sys.stderr = self.test_err
        try:
            os.mkdir(TEST_EXEC_PATH)
        except:
            pass
        remove_all_testfiles()

    # @unittest.skip('')
    def test_ambiguous_aeon_event(self):
        copyfile(TEST_DATA_PATH + 'normal.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_AEON)
        self.assertStderrEquals('Error: Ambiguous Aeon event title "Mrs Hubbard sleeps".')

    # @unittest.skip('')
    def test_create_novx(self):
        copyfile(TEST_DATA_PATH + 'nv_aeon2.ini', INI_FILE)
        copyfile(TEST_DATA_PATH + 'date_limits.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_AEON)
        if UPDATE:
            copyfile(TEST_NOVX, TEST_DATA_PATH + 'date_limits.novx')
        self.assertEqual(read_file(TEST_NOVX), read_file(TEST_DATA_PATH + 'date_limits.novx'))

    # @unittest.skip('')
    def test_update_novx(self):
        copyfile(TEST_DATA_PATH + 'nv_aeon2.ini', INI_FILE)
        copyfile(TEST_DATA_PATH + 'date_limits.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'updated.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_AEON)
        if UPDATE:
            copyfile(TEST_NOVX, TEST_DATA_PATH + 'updated_from_aeon.novx')
        self.assertEqual(read_file(TEST_NOVX), read_file(TEST_DATA_PATH + 'updated_from_aeon.novx'))
        self.assertEqual(read_file(TEST_NOVX_BAK), read_file(TEST_DATA_PATH + 'date_limits.novx'))

    # @unittest.skip('')
    def test_create_date_limits_aeon(self):
        copyfile(TEST_DATA_PATH + 'date_limits.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'minimal.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_NOVX)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'created.aeonzip')
        self.assertEqual(open_timeline(TEST_AEON), open_timeline(TEST_DATA_PATH + 'created.aeonzip'))

    # @unittest.skip('')
    def test_create_arc_aeon(self):
        copyfile(TEST_DATA_PATH + 'arc.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'minimal.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_NOVX)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'created_arc.aeonzip')
        self.assertEqual(open_timeline(TEST_AEON), open_timeline(TEST_DATA_PATH + 'created_arc.aeonzip'))

    # @unittest.skip('')
    def test_update_aeon(self):
        copyfile(TEST_DATA_PATH + 'updated.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'created.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_NOVX)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'updated_from_yw.aeonzip')
        self.assertEqual(open_timeline(TEST_AEON), open_timeline(TEST_DATA_PATH + 'updated_from_yw.aeonzip'))

    # @unittest.skip('')
    def test_update1_aeon(self):
        copyfile(TEST_DATA_PATH + 'updated1.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'updated_from_yw.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_NOVX)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'updated1_from_yw.aeonzip')
        self.assertEqual(open_timeline(TEST_AEON), open_timeline(TEST_DATA_PATH + 'updated1_from_yw.aeonzip'))

    # @unittest.skip('')
    def test_create_novx_birthday(self):
        copyfile(TEST_DATA_PATH + 'nv_aeon2.ini', INI_FILE)
        copyfile(TEST_DATA_PATH + 'birthday.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_AEON)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'birthday.aeonzip')
        self.assertEqual(read_file(TEST_NOVX), read_file(TEST_DATA_PATH + 'birthday.novx'))

    # @unittest.skip('')
    def test_update_aeon_birthday(self):
        copyfile(TEST_DATA_PATH + 'birthday.novx', TEST_NOVX)
        copyfile(TEST_DATA_PATH + 'created.aeonzip', TEST_AEON)
        os.chdir(TEST_EXEC_PATH)
        convert(TEST_NOVX)
        if UPDATE:
            copyfile(TEST_AEON, TEST_DATA_PATH + 'birthday_updated.aeonzip')
        self.assertEqual(open_timeline(TEST_AEON), open_timeline(TEST_DATA_PATH + 'birthday_updated.aeonzip'))

    def tearDown(self):
        sys.stdout = self.original_output
        sys.stderr = self.original_err
        remove_all_testfiles()

    # assert that sys.stdout would be equal to expected value
    def assertStdoutEquals(self, value):
        self.assertEqual(self.test_out.getvalue().strip(), value)

    # assert that sys.stdout would not be equal to expected value
    def assertStdoutNotEquals(self, value):
        self.assertNotEqual(self.test_out.getvalue().strip(), value)

    # assert that sys.stderr would be equal to expected value
    def assertStderrEquals(self, value):
        self.assertEqual(self.test_err.getvalue().strip(), value)

    # assert that sys.stderr would not be equal to expected value
    def assertStderrNotEquals(self, value):
        self.assertNotEqual(self.test_err.getvalue().strip(), value)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
