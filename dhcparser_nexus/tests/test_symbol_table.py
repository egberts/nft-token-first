
import unittest
import symbol_table


class TestSymbolTable2(unittest.TestCase):

    def test_get_a_node(self):
        node = symbol_table.SymbolTable()
        result = isinstance(node, symbol_table.SymbolTable)
        self.assertEqual(result, True)  # add assertion here

    def test_get_empty_search(self):
        node2 = symbol_table.SymbolTable()
        with self.assertRaises(ValueError):
            node2.find_symbol('does not exist')

    def test_get_empty_extract(self):
        node2 = symbol_table.SymbolTable()
        with self.assertRaises(ValueError):
            result = node2.extract_symbol('does not exist')

    def test_add_preexisting_symbol(self):
        node3 = symbol_table.SymbolTable()
        node3.add_to_symbol_table('EXIST', 'true')
        node4 = symbol_table.SymbolTable()
        try:
            node4.add_to_symbol_table('EXIST', 'false')
        except OverflowError:
            self.assertEqual(True, True)

    def test_find_successfully(self):
        node5 = symbol_table.SymbolTable()
        node5.add_to_symbol_table('FOUND', 'yep')
        result = node5.find_symbol('FOUND')

        self.assertEqual(result, True)

    def test_extract_symbol(self):
        node6 = symbol_table.SymbolTable()
        node6.add_to_symbol_table('TOKEN6', 'value6')

        result6 = node6.extract_symbol('TOKEN6')

        self.assertEqual(result6, True)

    def test_get_label(self):
        node7 = symbol_table.SymbolTable()
        node7.add_to_symbol_table('TOKEN7', 'value7')

        result7 = node7.get_label

        self.assertEqual(result7, 'TOKEN7')

    def test_set_avlue_undefined(self):
        node8 = symbol_table.SymbolTable()

        with self.assertRaises(ValueError) as context:
            node8.add_to_symbol_table()

        self.assertTrue(type(context.exception) in [ValueError])

    def test_set_label_undefined(self):
        node8 = symbol_table.SymbolTable()
        node8.set_label('LABEL8')

        with self.assertRaises(ValueError) as context:
            node8.add_to_symbol_table()

        self.assertTrue(type(context.exception) in [ValueError])

    def test_set_label_value(self):
        node8 = symbol_table.SymbolTable()

        node8.set_label('TOKEN8')
        node8.set_value('value8')

        node8.add_to_symbol_table()

        result_label8 = node8.get_label
        result_value8 = node8.get_value

        self.assertEqual('TOKEN8', result_label8)
        self.assertEqual('value8', result_value8)
