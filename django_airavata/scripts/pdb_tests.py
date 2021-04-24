import unittest
from .pdb_parser import validate_pdb


class TestValidator(unittest.TestCase):
    def setUp(self):
        print('Running test case on PDB Validator...')

    def tearDown(self):
        print('Test case finished on PDB Validator...')

    # No errors
    def test_ValidPDB(self):
        self.assertEqual(True, validate_pdb('tests/testPDBs/input1.pdb'))

    # Line partially Missing
    def test_NonValidPDB(self):

        self.assertEqual(False, validate_pdb('tests/testPDBs/input2.pdb'))

    # Space mid line
    def test_ParsingErrorValidPDB(self):

        self.assertEqual(False, validate_pdb('tests/testPDBs/input3.pdb'))

    # Space start of line
    def test_ParsingMidLineErrorPDB(self):
        self.assertEqual(True, validate_pdb('tests/testPDBs/input4.pdb'))
