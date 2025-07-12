""" Exercise the matching against a list of _flag_groupname reserved words """
'NONE',
'ALL',
'ALLBUT',
'TOP',
'CONTAINS',
'CONTAINED',

import unittest
from dhcparser_nexus.reserved_words import is_viml_groupname_reserved_word

TEST_RESERVED_WORD1 = 'None'
TEST_RESERVED_WORD2 = 'ALL'
TEST_RESERVED_WORD3 = 'AllBut'
TEST_RESERVED_WORD4 = 'contains'
TEST_RESERVED_WORD5 = 'CONTAINED'
TEST_NONRESERVED_WORD1 = 'syntax'
TEST_NONRESERVED_WORD2 = 'cluster'
TEST_NONRESERVED_WORD3 = 'region'
TEST_NONRESERVED_WORD4 = 'match'
TEST_NONRESERVED_WORD5 = 'keepall'


class TestGroupnameReservedWords(unittest.TestCase):
    def test_matches_groupname_reserve_word1(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_RESERVED_WORD1),
            True
        )

    def test_matches_groupname_reserve_word2(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_RESERVED_WORD2),
            True
        )

    def test_matches_groupname_reserve_word3(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_RESERVED_WORD3),
            True
        )

    def test_matches_groupname_reserve_word4(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_RESERVED_WORD4),
            True
        )

    def test_matches_groupname_reserve_word5(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_RESERVED_WORD5),
            True
        )

    def test_mismatches_groupname_reserve_word1(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_NONRESERVED_WORD1),
            False
        )

    def test_mismatches_groupname_reserve_word2(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_NONRESERVED_WORD2),
            False
        )

    def test_mismatches_groupname_reserve_word3(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_NONRESERVED_WORD3),
            False
        )

    def test_mismatches_groupname_reserve_word4(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_NONRESERVED_WORD4),
            False
        )

    def test_mismatches_groupname_reserve_word5(self):
        self.assertEqual(
            is_viml_groupname_reserved_word(TEST_NONRESERVED_WORD5),
            False
        )
