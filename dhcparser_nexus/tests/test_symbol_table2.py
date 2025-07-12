import unittest
from dhcparser_nexus.symbol_table import SymbolTable

TEST_PATTERN_1 = 'TESTING123'
TEST_LITERAL_VALUE_1 = 'testing123'
TEST_PATTERN_2 = 'OOPSIEDAISY'
TEST_LITERAL_VALUE_2 = 'oopsie daisy'
TEST_PATTERN_3 = 'KENELA'
TEST_LITERAL_VALUE_3 = 'What is that'
TEST_PATTERN_4 = 'Impala'
TEST_LITERAL_VALUE_4 = 'A gazelle?'


class TestSymbolTable(unittest.TestCase):
    def test_insert_1_symbol(self):
        vst2 = SymbolTable()
        vst2.add_to_symbol_table(literal_name=TEST_PATTERN_1, value=TEST_LITERAL_VALUE_1)
        self.assertEqual(vst2._array_symtbl[0]['name'], TEST_PATTERN_1)
        del vst2

    def test_insert_3_symbol(self):
        vst3 = SymbolTable()
        vst3.add_to_symbol_table(literal_name=TEST_PATTERN_2, value=TEST_LITERAL_VALUE_2)
        vst3.add_to_symbol_table(literal_name=TEST_PATTERN_3, value=TEST_LITERAL_VALUE_3)
        vst3.add_to_symbol_table(literal_name=TEST_PATTERN_4, value=TEST_LITERAL_VALUE_4)
        self.assertEqual(vst3._array_symtbl[2]['name'], TEST_PATTERN_4)
        self.assertEqual(vst3._array_symtbl[1]['name'], TEST_PATTERN_3)
        self.assertEqual(vst3._array_symtbl[0]['name'], TEST_PATTERN_2)
        del vst3

    def test_find_symbol(self):
        vst = SymbolTable()
        vst.add_to_symbol_table(TEST_PATTERN_2, TEST_LITERAL_VALUE_2)
        self.assertEqual(vst.find_symbol(TEST_PATTERN_2), True)
        del vst
