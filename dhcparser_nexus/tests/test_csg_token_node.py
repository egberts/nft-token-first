""" Testing CSG Token Node """
import unittest
from csg_token_node import CSGTokenNode


class TestCsgTokenNode(unittest.TestCase):
    """ Context Syntax Graph (CSG/CST) """
    def test_get_node(self):
        ctn = CSGTokenNode()

        self.assertEqual(isinstance(ctn, CSGTokenNode), True)

        del ctn

    def test_get_node_with_token_name(self):

        ctn2 = CSGTokenNode('TOKEN_NAME')

        self.assertEqual(isinstance(ctn2, CSGTokenNode), True)
        self.assertEqual(ctn2.get_token, 'TOKEN_NAME')

        del ctn2

    def test_csg_node_literal(self):
        ctn3 = CSGTokenNode('NEXT_TOKEN')

        ctn3.set_literal()

        self.assertEqual(ctn3.is_literal, True)
        self.assertEqual(ctn3.is_operator_and, False)
        self.assertEqual(ctn3.is_operator_or, False)

        del ctn3

    def test_set_token_name(self):
        ctn5 = CSGTokenNode()

        ctn5.set_token('SET_TOKEN_NAME')

        self.assertEqual(ctn5.get_token, 'SET_TOKEN_NAME')

        del ctn5

    def test_get_token_name(self):
        ctn4 = CSGTokenNode('NAME_OF_TOKEN')

        self.assertEqual(ctn4.get_token, 'NAME_OF_TOKEN')

        del ctn4

    def test_set_head(self):
        ctn6 = CSGTokenNode('SIXTH_TOKEN')
        ctn7 = CSGTokenNode('SEVENTH_TOKEN')

        ctn6.set_head(ctn7)

        self.assertEqual(ctn6.get_head, ctn7)

        del ctn6
        del ctn7

    def test_set_next(self):
        ctn8 = CSGTokenNode('EIGHTH_TOKEN')
        ctn9 = CSGTokenNode('NINTH_TOKEN')

        ctn8.set_next(ctn9)

        self.assertEqual(ctn8.get_next, ctn9)

        del ctn8
        del ctn9

    def test_set_operator_and(self):
        ctn10 = CSGTokenNode('TENTH_TOKEN')

        ctn10.set_operator_and()

        self.assertEqual(True, ctn10.is_operator_and)

        del ctn10

    def test_set_operator_or(self):
        ctn11 = CSGTokenNode('ELEVENTH_TOKEN')

        ctn11.set_operator_or()

        self.assertEqual(True, ctn11.is_operator_or)

        del ctn11

    def test_insert_at_end(self):
        ctn12 = CSGTokenNode('TWELVETH_TOKEN')
        ctn12.set_head(ctn12)
        ctn13 = CSGTokenNode('THIRTEENTH_TOKEN')

        ctn12.insert_at_end(ctn13)

        self.assertEqual(ctn12.get_next, ctn13)

        del ctn12
        del ctn13

    def test_insert_at_end_invalid_data(self):

        with self.assertRaises(ValueError):
            CSGTokenNode(['INVALID_TOKEN'])

    def test_insert_at_end_invalid_head(self):
        ctn14 = CSGTokenNode('FORTEENTH_TOKEN')
        ctn15 = CSGTokenNode('FIFTHEENTH_TOKEN')
        ctn16 = CSGTokenNode('SIXTHEENTH_TOKEN')

        ctn14.set_head(ctn14)

        with self.assertRaises(LookupError):
            ctn15.insert_at_end(ctn16)

    def test_insert_at_end_3rd_valid_link(self):
        ctn17 = CSGTokenNode('SEVENTHEENTH_TOKEN')
        ctn17.set_head(ctn17)
        ctn18 = CSGTokenNode('EIGHTHEENTH_TOKEN')
        ctn17.insert_at_end(ctn18)

        ctn19 = CSGTokenNode('NINETHEENTH_TOKEN')
        ctn17.insert_at_end(ctn19)

        self.assertEqual(ctn17.get_next, ctn18)
        self.assertEqual(ctn18.get_next, ctn19)
        self.assertEqual(ctn19.get_next, None)

    def test_insert_at_end_no_head_3rd_link(self):
        ctn17 = CSGTokenNode('SEVENTHEENTH_TOKEN')
        ctn17.set_head(ctn17)
        ctn18 = CSGTokenNode('EIGHTHEENTH_TOKEN')
        ctn17.insert_at_end(ctn18)

        ctn17.insert_at_end('NINETEENTH_TOKEN')

        self.assertEqual(ctn17.get_next, ctn18)
        ctn19: CSGTokenNode = ctn18.get_next
        self.assertEqual(ctn19.get_next, None)
        self.assertEqual(ctn19.get_token, 'NINETEENTH_TOKEN')

    def test_insert_at_end_3rd_link_invalid_data(self):
        ctn17 = CSGTokenNode('SEVENTHEENTH_TOKEN')
        ctn17.set_head(ctn17)
        ctn18 = CSGTokenNode('EIGHTHEENTH_TOKEN')
        ctn17.insert_at_end(ctn18)

        with self.assertRaises(SystemExit):
            ctn17.insert_at_end(['NINETEENTH_TOKEN'])


class TestCsgLinkedList:
    """ exercise the linked list of CSG Token Nodes """
    def test_append(self):
        ctn10 = CSGTokenNode('TENTH_TOKEN')
        ctn10.set_head(ctn10)  # designated head link

        ctn10.insert_at_end('ELEVENTH_TOKEN')

        print("Hey")


class TestCsgLinkedList:
    """ exercise the linked list of CSG Token Nodes """
    def test_append(self):
        ctn10 = CSGTokenNode('TENTH_TOKEN')
        ctn10.set_head(ctn10)  # designated head link

        ctn10.insert_at_end('ELEVENTH_TOKEN')

        print("Hey")
