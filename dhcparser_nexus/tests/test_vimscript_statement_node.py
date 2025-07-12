import unittest

import dhcparser_nexus.vimscript_stmt_node
from vimscript_stmt_node import VimscriptStmtNode, vimscript_reset
import vimscript_stmt_node


class TestVimLStmtNode(unittest.TestCase):
    def test_create_node(self):
        dhcparser_nexus.vimscript_stmt_node.vimscript_delete()
        vsn = VimscriptStmtNode()

        correct = isinstance(vsn, VimscriptStmtNode)

        self.assertEqual(True, correct)  # add assertion here

        vimscript_reset()
        del vsn

    def test_validate_node(self):
        dhcparser_nexus.vimscript_stmt_node.vimscript_delete()
        vsn2 = VimscriptStmtNode()

        correct = vsn2.validate()

        self.assertEqual(True, correct)  # add assertion here

        vimscript_reset()
        del vsn2

    def test_add_to_stmt_list_via_str(self):
        dhcparser_nexus.vimscript_stmt_node.vimscript_delete()
        vsn3 = VimscriptStmtNode('TOKEN_NAME')
        vsn3.set_cluster_flag()
        vsn3.set_groupname('THIS_TOKEN_NAME')
        count = vsn3.add_to_stmt_list()

        vsn3.validate()

        self.assertEqual(1, count)  # add assertion here

        vimscript_reset()
        del vsn3

    def test_add_to_stmt_list(self):
        dhcparser_nexus.vimscript_stmt_node.vimscript_delete()
        vsn4 = VimscriptStmtNode('TOKEN_NAME')
        vsn4.clear_cluster_flag()
        vsn4.set_groupname('THIS_TOKEN_NAME')
        count = vsn4.add_to_stmt_list()
        vsn4.validate()
        self.assertEqual(1, count)  # add assertion here

        vsn5 = VimscriptStmtNode()
        vsn5.clear_cluster_flag()
        vsn5.set_groupname('THAT_TOKEN_NAME')

        vsn5.validate()

        count = vsn5.add_to_stmt_list()
        self.assertEqual(2, count)  # add assertion here

        vimscript_reset()
        del vsn4
        del vsn5

    def test_validate_first(self):
        vsn6 = VimscriptStmtNode()

        result = vsn6.validate()

        self.assertEqual(True, result)

        vimscript_reset()
        del vsn6

    def test_validate_bad_first(self):
        vsn7: VimscriptStmtNode = VimscriptStmtNode()
        vsn7._flag_contained = True
        vsn7.add_to_stmt_list()

        result7 = vsn7.validate()

        self.assertEqual(False, result7)

        vimscript_reset()
        del vsn7

    def test_validate_skippies_1(self):
        vsn8: VimscriptStmtNode = VimscriptStmtNode()
        vsn8._flag_cluster = True
        vsn8._flag_skipempty = True
        vsn8._flag_skipnl = True
        vsn8._flag_skipwhite = True
        vsn8._item = 'an item'
        vsn8.add_to_stmt_list()

        result = vsn8.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn8

    def test_validate_matches(self):
        vsn9: VimscriptStmtNode = VimscriptStmtNode()
        vsn9._flag_match = True
        vsn9._flag_oneline = True
        vsn9._region_skip = 'inadvertently'
        vsn9._match_group = True
        vsn9.add_to_stmt_list()

        result = vsn9.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn9

    def test_validate_keywords(self):
        vsn10: VimscriptStmtNode = VimscriptStmtNode()
        vsn10._flag_keyword = True
        vsn10._contains = True
        vsn10.add_to_stmt_list()

        result = vsn10.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn10

    def test_validate_cluster(self):
        vsn11: VimscriptStmtNode = VimscriptStmtNode()
        vsn11._flag_cluster = True
        vsn11._flag_excludenl = True
        vsn11._flag_fold = True
        vsn11._flag_display = True
        vsn11._flag_extend = True
        vsn11._flag_concealends = True
        vsn11.add_to_stmt_list()

        result = vsn11.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn11

    def test_validate_cluster2(self):
        vsn12: VimscriptStmtNode = VimscriptStmtNode()
        vsn12._flag_cluster = True
        vsn12._flag_containedin = True
        vsn12._flag_transparent = True
        vsn12._flag_skipempty = True
        vsn12._flag_skipnl = True
        vsn12._flag_skipwhite = True
        vsn12._flag_contained = True
        vsn12._flag_conceal = True
        vsn12._flag_cchar = True
        vsn12.add_to_stmt_list()

        result = vsn12.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn12

    def test_validate_noncluster(self):
        vsn12: VimscriptStmtNode = VimscriptStmtNode()
        vsn12._flag_region = True
        vsn12._flag_cchar = True
        vsn12.add_to_stmt_list()

        result = vsn12.validate()

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn12

    def test_is_group1(self):
        vsn13: VimscriptStmtNode = VimscriptStmtNode()
        vsn13._flag_cluster = True

        result = vsn13.is_group

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn13

    def test_is_group2(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_cluster = False

        result = vsn14.is_group

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn14

    def test_is_group3(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = False
        vsn15._flag_region = True

        result = vsn15.is_group

        self.assertEqual(True, result)

        vimscript_reset()
        del vsn15

    def test_is_group4(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_cluster = False
        vsn14._flag_match = True

        result = vsn14.is_group

        self.assertEqual(True, result)

        vimscript_reset()
        del vsn14

    def test_is_group5(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = False
        vsn15._flag_keyword = True

        result = vsn15.is_group

        self.assertEqual(True, result)

        vimscript_reset()
        del vsn15

    def test_is_cluster1(self):
        vsn13: VimscriptStmtNode = VimscriptStmtNode()
        vsn13._flag_cluster = False
        vsn13._flag_region = True

        result = vsn13.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn13

    def test_is_cluster2(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_cluster = False
        vsn14._flag_match = True

        result = vsn14.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn14

    def test_is_cluster3(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = False
        vsn15._flag_keyword = True

        result = vsn15.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_cluster4(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._flag_cluster = False
        vsn16._flag_region = False

        result = vsn16.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn16

    def test_is_cluster5(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = False
        vsn15._flag_match = True

        result = vsn15.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_cluster6(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = False
        vsn15._flag_keyword = True

        result = vsn15.is_cluster

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_match1(self):
        vsn13: VimscriptStmtNode = VimscriptStmtNode()
        vsn13._flag_match = False
        vsn13._flag_region = True

        result = vsn13.is_match
        self.assertEqual(False, result)

        vimscript_reset()
        del vsn13

    def test_is_match2(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_match = False
        vsn14._flag_cluster = True

        result = vsn14.is_match

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn14

    def test_is_match3(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_match = False
        vsn15._flag_keyword = True

        result = vsn15.is_match

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_match4(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._flag_match = False
        vsn16._flag_region = False

        result = vsn16.is_match

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn16

    def test_is_match5(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_match = False
        vsn15._flag_cluster = True

        result = vsn15.is_match

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_match6(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_match = False
        vsn15._flag_keyword = True

        result = vsn15.is_match
        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_region1(self):
        vsn13: VimscriptStmtNode = VimscriptStmtNode()
        vsn13._flag_region = False
        vsn13._flag_match = True

        result = vsn13.is_region
        self.assertEqual(False, result)

        vimscript_reset()
        del vsn13

    def test_is_region2(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_region = False
        vsn14._flag_cluster = True

        result = vsn14.is_region

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn14

    def test_is_region3(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_region = False
        vsn15._flag_keyword = True

        result = vsn15.is_region

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_region4(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._flag_region = False
        vsn16._flag_match = False

        result = vsn16.is_region

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn16

    def test_is_region5(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_region = False
        vsn15._flag_cluster = True

        result = vsn15.is_region

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_region6(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_region = False
        vsn15._flag_keyword = True

        result = vsn15.is_region

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_keyword1(self):
        vsn13: VimscriptStmtNode = VimscriptStmtNode()
        vsn13._flag_keyword = False
        vsn13._flag_match = True

        result = vsn13.is_keyword
        self.assertEqual(False, result)

        vimscript_reset()
        del vsn13

    def test_is_keyword2(self):
        vsn14: VimscriptStmtNode = VimscriptStmtNode()
        vsn14._flag_keyword = False
        vsn14._flag_cluster = True

        result = vsn14.is_keyword

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn14

    def test_is_keyword3(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_keyword = False
        vsn15._flag_region = True

        result = vsn15.is_keyword

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_keyword4(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._flag_keyword = False
        vsn16._flag_match = False

        result = vsn16.is_keyword

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn16

    def test_is_keyword5(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_keyword = False
        vsn15._flag_cluster = True

        result = vsn15.is_keyword

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_is_keyword6(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_keyword = False
        vsn15._flag_region = True

        result = vsn15.is_keyword

        self.assertEqual(False, result)

        vimscript_reset()
        del vsn15

    def test_set_cluster_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_region = True
        vsn15._flag_match = True

        vsn15.set_cluster_flag()

        self.assertEqual(True, vsn15._flag_cluster)
        self.assertEqual(False, vsn15._flag_region)
        self.assertEqual(False, vsn15._flag_match)

        vimscript_reset()
        del vsn15

    def test_clear_cluster_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = True

        vsn15.clear_cluster_flag()

        self.assertEqual(False, vsn15._flag_cluster)

        vimscript_reset()
        del vsn15

    def test_set_region_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_cluster = True
        vsn15._flag_match = True

        vsn15.set_region_flag()

        self.assertEqual(True, vsn15._flag_region)
        self.assertEqual(False, vsn15._flag_cluster)
        self.assertEqual(False, vsn15._flag_match)

        vimscript_reset()
        del vsn15

    def test_clear_region_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_region = True

        vsn15.clear_region_flag()

        self.assertEqual(False, vsn15._flag_region)

        vimscript_reset()
        del vsn15

    def test_set_match_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_match = True
        vsn15._flag_cluster = True
        vsn15._flag_region = True

        vsn15.set_match_flag()

        self.assertEqual(True, vsn15._flag_match)
        self.assertEqual(False, vsn15._flag_cluster)
        self.assertEqual(False, vsn15._flag_region)

        vimscript_reset()
        del vsn15

    def test_clear_match_flag(self):
        vsn15: VimscriptStmtNode = VimscriptStmtNode()
        vsn15._flag_match = True

        vsn15.clear_match_flag()

        self.assertEqual(False, vsn15._flag_match)

        vimscript_reset()
        del vsn15

    def test_get_groupname(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._groupname = None

        result15 = vsn16.get_groupname()

        self.assertEqual(None, result15)

        vimscript_reset()
        del vsn16

    def test_set_groupname(self):
        vsn16: VimscriptStmtNode = VimscriptStmtNode()
        vsn16._groupname = None

        token_name = 'SOME String'
        vsn16.set_groupname(token_name)

        self.assertEqual(token_name, vsn16._groupname)

        vimscript_reset()
        del vsn16
