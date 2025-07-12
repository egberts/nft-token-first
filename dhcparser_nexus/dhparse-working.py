"""
Two-stage parse trees
1. EBNF parse tree
2. Target parse tree (e.g., nftables)
"""

# Futures
from __future__ import print_function
from __future__ import unicode_literals

# Generic/Built-in
import pathlib
import sys
# from typing import List, Any, Tuple

# Other Libs
import DHParser
from DHParser.dsl import create_parser

# Owned

__author__ = 'egberts@github.com'
__copyright__ = 'Copyright 2024'
__credits__ = ['egberts@github.com']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'egberts@github.com'
__email__ = 'egberts@github.com'
__status__ = 'Dev'


def is_symbol(this_string: str) -> bool:
    """
    is this string a symbol that contains a raw lexical token value?
    :param this_string:
    :type this_string: str
    :return:
    :rtype: bool
    """
    if str.__len__ == 0:
        print('is_symbol() was given zero-length string')
        return False
    if 'A' <= this_string[0] <= 'Z':
        return True
    if '_' == this_string[0] and ('A' <= this_string[1] <= 'Z'):
        return True
    return False


def is_expression(this_string: str) -> bool:
    """
    is this string an expression?  A symbol name denoted by all lowercase
    :param this_string:
    :type this_string: str
    :return:
    :rtype: bool
    """
    if 'a' <= this_string[0] <= 'z':
        return True
    return False


class LexicalNode:
    """
    Lexical Node for the upcoming Lexical Tree
    """
    lexical_string: str

    def __init__(self, my_string: str) -> None:
        self.lexical_string = my_string


class LexicalTree:
    """
    A simple first-encounter literal tree
    """
    root: LexicalNode = None
    head: LexicalNode = None

    def __init__(self):
        self.root: LexicalNode = LexicalNode('')
        self.head = self.root


class TwoStageParser:
    """
    The two-stage parser
    """
    # first-stage parser for multivariant EBNF
    ebnf_grammar: str
    ebnf_parser: DHParser.Grammar

    # second-stage parser for target's BNF
    target_text_bnf: str  # useful for locating line error(s)
    target_parse_tree: DHParser.RootNode

    # lookup tables (for speed)
    terminal_ebnf_definition_table: None | list  # both 'literal' and 'regexp'
    nonterminal_target_definition_hash: None | list  # 'SYM_REGEX' 'symbol' uppercase (semi-terminal)
    nonterminal_target_jump_hash: None | list  # 'SYM_REGEX' 'symbol' lowercase (jump)
    nonterminal_target_lexical_tree: None | LexicalTree  # 'SYM_REGEX' 'symbol' lowercase (jump)

    my_definition_table: list  # old
    empty_definition_table: list  # old

    def __init__(self):
        # lookup tables (for speed)
        self.terminal_ebnf_definition_table = None  # both 'literal' and 'regexp'
        self.nonterminal_target_definition_hash = None  # 'SYM_REGEX' 'symbol' uppercase (semi-terminal)
        self.nonterminal_target_jump_hash = None  # 'SYM_REGEX' 'symbol' lowercase (jump)
        self.nonterminal_target_lexical_tree = None  # 'SYM_REGEX' 'symbol' lowercase (jump)

        #  Read in DHParser the EBNF specification file of EBNF and its multi-variants thereof
        print('Loading ebnf-flexible.dhparse for multi-variant EBNF support ...', end='')
        fd = open('ebnf-flexible.dhparse')
        print(': loaded.')
        self.ebnf_grammar: str = fd.read()

        # grammatically parse the EBNF for sub-sequential EBNF compiling
        print('Parsing EBNF syntax ...', end='')
        self.ebnf_parser: DHParser.Grammar = create_parser(self.ebnf_grammar, 'nft')
        print(': parsed.')
        target_text_bnf: str  # useful for locating line error(s)
        target_parse_tree: DHParser.RootNode

    def get_definition_value(self, this_string: str) -> None | str:
        """
        get a value based on symbol name
        :param this_string:
        :type this_string: str
        :return: A value string value to the symbol name or a None type
        :rtype: str | None
        """
        for this_sym in self.terminal_ebnf_definition_table:
            if this_string == this_sym[0]:
                return this_sym[1]
        return None

    def collect_expressions(self) -> None | list[list]:
        """
        Collect only definitions
        :return: A pull-up condensed flattened parse tree
        :rtype: DHParser.Node | None
        """
        if self.target_parse_tree.name != 'syntax':
            print('collect_symbols: parse tree is not root-labeled as \'syntax\'.')
            return None

        if (type(self.target_parse_tree) is not DHParser.RootNode and
                self.target_parse_tree.name != 'syntax'):
            print("Not a RootNode")
            sys.exit(-9)
        print("Node count: ", len(self.target_parse_tree.children))
        if len(self.target_parse_tree.children) < 3:
            print("Not a enough nodes for a tree")
            sys.exit(-9)
        this_def_pairs = []
        for n in range(0, len(self.target_parse_tree.children)):  # how many 'syntax' (usually 1)
            node: DHParser.Node = self.target_parse_tree.children[n]
            this_def = self.collect_one_expression(node)
            if this_def is not None:
                if is_expression(this_def[0]):
                    this_def_pairs.append(this_def)
        return this_def_pairs

    def construct_grammar_target_parse_tree(self) -> None:
        """

        :rtype: None
        """
        print('Constructing target parse tree ...', end='')
        self.target_parse_tree: DHParser.RootNode = self.ebnf_parser(self.target_text_bnf)
        for my_error in self.target_parse_tree.errors_sorted:
            print(my_error)
        print(': finished.')

    def load_target_grammar_text(self, filespec: pathlib.Path) -> None:
        """

        :param filespec:
        :type filespec: pathlib.Path
        :rtype: None
        """
        print('Loading %s BNF file ...' % filespec, end='')
        with open(filespec, 'r', encoding='utf-8') as f:
            self.target_text_bnf = f.read()
        f.close()
        print(': loaded.')

    @staticmethod
    def collect_one_definition(node: DHParser.Node | DHParser.RootNode) -> list:
        """

        :param node:
        :type node: DHParser.Node | DHParser.RootNode
        :return: A list of nodes containing Bison symbol definitions
        :rtype: list
        """

        symbol_name = None
        node_value = None
        if isinstance(node, DHParser.Node):
            if node.name == 'definition':
                node_symbol = node.children[0]
                if node_symbol.name == 'symbol':
                    node_sym_regex = node_symbol.children[0]
                    if node_sym_regex.name == 'SYM_REGEX':
                        if type(node_sym_regex.result) is str:
                            symbol_name = node_sym_regex.result
                        elif type(node_sym_regex.content) is str:
                            symbol_name = node_sym_regex.content
                        else:
                            print('SYM_REGEX(\"%s\") is not a str.')
                            sys.exit(-3)
                node_expression = node.children[2]
                if node.children[2].name == 'expression':
                    node_sequence = node_expression.children[0]
                    if node_sequence.name == 'sequence':
                        node_interleave = node_sequence[0]
                        if node_interleave.name == 'interleave':
                            node_difference = node_interleave[0]
                            if node_difference.name == 'difference':
                                node_term = node_difference[0]
                                if node_term.name == 'term':
                                    node_element = node_term[0]
                                    if node_element.name == 'element':
                                        node_subelement = node_element.children[0]
                                        if node_subelement.name == 'literal':
                                            node_value = node_subelement.content
                                        if node_subelement.name == 'regexp':
                                            node_value = '<regexp>' + node_subelement.content

        if node_value is not None:
            this_list = [symbol_name, node_value]
        else:
            this_list = None
        return this_list

    def collect_target_terminal_definitions(self) -> None:
        """
        Collect only definitions
        """
        if self.target_parse_tree.name != 'syntax':
            print('collect_symbols: parse tree is not root-labeled as \'syntax\'.')
            return

        if type(self.target_parse_tree) is not DHParser.RootNode and self.target_parse_tree.name != 'syntax':
            print("Not a RootNode")
            sys.exit(-9)
        if len(self.target_parse_tree.children) < 3:
            print("Not a enough nodes for a tree")
            sys.exit(-9)
        this_def_pairs = []
        empty_def_pairs = []
        for n in range(0, len(self.target_parse_tree.children)):  # how many 'syntax' (usually 1)
            node = self.target_parse_tree.children[n]
            this_def = self.collect_one_definition(node)
            if this_def is not None:
                this_char = this_def[0][0]
                if 'A' <= this_char <= 'Z':
                    this_def_pairs.append(this_def)
                elif '_' == this_char:
                    second_char = this_def[0][1]
                    if 'A' <= second_char <= 'Z':
                        this_def_pairs.append(this_def)
                    else:
                        empty_def_pairs.append(this_def)
                else:
                    empty_def_pairs.append(this_def)
        self.terminal_ebnf_definition_table = this_def_pairs
        self.empty_definition_table = empty_def_pairs

    def collect_one_expression(self, node: None | DHParser.Node):
        """
        Extract the children of an expression
        :param node:
        :type node: None | DHParser.Node
        :return:
        :rtype: None | list
        """
        symbol_name = None
        node_value = None
        if isinstance(node, DHParser.Node):
            if node.name == 'definition':
                node_symbol = node.children[0]
                if node_symbol.name == 'symbol':
                    node_sym_regex = node_symbol.children[0]
                    if node_sym_regex.name == 'SYM_REGEX':
                        # pay attention to only the lowercase labels (expression)
                        if not is_expression(node_sym_regex.content):
                            return None
                        symbol_name = node_sym_regex.content
                node_expression = node.children[2]
                if node.children[2].name == 'expression':
                    node_sequence = node_expression.children[0]
                    if node_sequence.name == 'sequence':
                        node_interleave = node_sequence[0]
                        if node_interleave.name == 'interleave':
                            node_difference = node_interleave[0]
                            if node_difference.name == 'difference':
                                node_term = node_difference[0]
                                if node_term.name == 'term':
                                    node_element = node_term[0]
                                    if node_element.name == 'element':
                                        node_subelement = node_element.children[0]
                                        if node_subelement.name == 'literal':
                                            node_value = node_subelement.content
                                        elif node_subelement.name == 'symbol':
                                            node_subsymbol = node_subelement.children[0]
                                            if node_subsymbol.name == 'SYM_REGEX':
                                                value_str: str = node_subsymbol.content
                                                if is_symbol(value_str):
                                                    node_value = self.get_definition_value(value_str)

        if node_value is not None:
            this_list = [symbol_name, node_value]
        else:
            this_list = None
        self.nonterminal_target_definition_hash = this_list
        return this_list

    @staticmethod
    def only_one_sym_regexp(this_node: DHParser.Node) -> bool:
        """

        :param this_node:
        :type this_node: DHParser.Node
        :return: Returns a True if there is only one SYM_REGEX in the group
        :rtype: bool
        """
        if this_node.name == 'symbol':
            node_symbol = this_node.children[0]
            if node_symbol.name == 'SYM_REGEX':
                return True
        return False

    @staticmethod
    def is_declaration_node(this_node: DHParser.Node) -> bool:
        """

        :param this_node:
        :type this_node: DHParser.Node
        :return: Returns a True if node is a declaration
        :rtype: bool
        """
        if this_node.name == 'DEF':
            if this_node.content == '=':
                return True
        return False

    @staticmethod
    def get_expression_node(this_node: DHParser.Node) -> tuple | None:
        """

        :param this_node:
        :type this_node: DHParser.Node
        :return:
        :rtype: tuple | None
        """
        if this_node.name == 'expression':
            return this_node.result
        return None

    def extract_expression_from_sym_regex(self, this_node: DHParser.Node) -> str | None:
        """

        :param this_node:
        :type this_node: DHParser.Node
        :return:
        :rtype: tuple | None
        """
        if len(this_node.children) == 0:
            if this_node.name == 'SYM_REGEX':
                return this_node.content
        return None


    def extract_expression_from_definition(self, this_node: DHParser.Node) -> tuple | None:
        """

        :param this_node:
        :type this_node: DHParser.Node
        :return:
        :rtype: tuple | None
        """
        if len(this_node.children) == 4:
            if this_node.name == 'definition':
                if self.only_one_sym_regexp(this_node.children[0]):
                    if self.is_declaration_node(this_node.children[1]):
                        return self.get_expression_node(this_node.children[2])
        return None

    def find_parse_expression(self, label: str) -> tuple | None:
        """

        :param label:
        :type label: str
        :return:
        :rtype: DHParser.Node | None
        """
        this_target_parse_children = self.target_parse_tree.children
        for this_node in this_target_parse_children:
            if isinstance(this_node, DHParser.Node):
                if this_node.name == 'definition':
                    node_symbol = this_node.children[0]
                    if node_symbol.name == 'symbol':
                        node_sym_regex = node_symbol.children[0]
                        if node_sym_regex.name == 'SYM_REGEX':
                            # pay attention to only the lowercase labels (expression)
                            if is_expression(node_sym_regex.content):
                                if node_sym_regex.content == label:
                                    return self.extract_expression_from_definition(this_node)
        return None

    def build_expression_tree(self, label: str) -> tuple | None:
        """
        build out the literals in expression_tree
        :param label:
        :type label: str
        :return: the node pointer to the given label
        :rtype: DHParser.Node | None
        """
        # Find node matching this label
        this_expression = self.find_parse_expression(label)
        return this_expression

    def get_first_lexicals_start_at_expression_node(
            self,
            node_expression: DHParser.Node
    ):
        """

        :param node_expression:
        :type node_expression: DHParser.Node
        :return:
        """
        value_str: str = ''
        skip_subsequence_any_and: bool = False
        skip_subsequence_and: bool = False
        force_subsequence_question_operator: bool = False
        lexical_set = []
        if node_expression.name == 'expression':
            for node_subexpression in node_expression.children:
                lexical = None
                if node_subexpression.name == 'OR':
                    pass
                elif node_subexpression.name == 'sequence':
                    node_subsequence = node_subexpression[0]
                    if node_subsequence.name == 'AND':
                        if force_subsequence_question_operator:
                            force_subsequence_question_operator = False
                            continue
                        elif skip_subsequence_any_and:
                            skip_subsequence_any_and = False  # markup_format
                            continue
                        break
                    elif node_subsequence.name == 'interleave':
                        node_subinterleave = node_subsequence[0]
                        if node_subinterleave.name == 'difference':
                            node_subdifference = node_subinterleave[0]
                            if node_subdifference.name == 'term':
                                node_subterm = node_subdifference[0]
                                if node_subterm.name == 'element':
                                    node_subelement = node_subterm.children[0]
                                    if node_subelement.name == 'literal':
                                        node_value = node_subelement.content
                                        print('DEBUG: node_value not used: %s' % node_value)
                                    elif node_subelement.name == 'symbol':
                                        node_subsymbol = node_subelement.children[0]
                                        if node_subsymbol.name == 'SYM_REGEX':
                                            value_str: str = node_subsymbol.content
                                            if value_str == 'RULE':
                                                print('SET arrived!')
                                            if is_symbol(value_str):
                                                lexical = self.get_definition_value(value_str)
                                                if lexical is None:
                                                    print('lexical \"%s\" symbol is not found in \'%s\' file.' % (value_str, nftables_ebnf_filepath))
                                                    sys.exit(-9)
                                                lexical_set.append([lexical, value_str])
                                            elif is_expression(value_str):
                                                # Find node matching this label
                                                # lexical = self.find_parse_expression(value_str)
                                                lexical = self.get_definition_value(value_str)
                                                if node_subsymbol.content == value_str:
                                                    lexical = self.extract_expression_from_sym_regex(node_subsymbol)
                                                    print('lexical ', lexical)
                                                if lexical is None:
                                                    print('lexical \'%s\' expression \"%s\" is not found.' % (value_str, lexical))
                                                    sys.exit(-9)
                                                lexical_set.append([lexical, value_str])
        if lexical_set is None:
            print('OUCH!~')
        return lexical_set

    @staticmethod
    def get_first_lexicals_starting_at_interleave_node(this_parser_subtree: DHParser.Node):
        """
        get the first lexicals (might be OR'd together so get those as well)
        :param this_parser_subtree:
        :return:
        """
        force_subsequence_question_operator: bool = False
        skip_subsequence_any_and: bool = False
        skip_subsequence_and: bool = False
        lexical = None
        lexical_set = []
        for node_subsequence in this_parser_subtree:
            if node_subsequence.name == 'OR':
                if skip_subsequence_and:
                    skip_subsequence_and = False  # markup_format
                    continue
                break
            elif node_subsequence.name == 'AND':
                if force_subsequence_question_operator:
                    force_subsequence_question_operator = False
                    continue
                elif skip_subsequence_any_and:
                    skip_subsequence_any_and = False  # markup_format
                    continue
                break
            elif node_subsequence.name == 'interleave':
                node_subinterleave = node_subsequence.children[0]
                if node_subinterleave.name == 'difference':
                    node_subdifference = node_subinterleave.children[0]
                    if node_subdifference.name == 'term':
                        node_subterm = node_subdifference.children[0]
                        if node_subterm.name == 'option':
                            for node_suboption in node_subterm.children:
                                if node_suboption.name == 'element':
                                    node_subelement = node_suboption.children[0]
                                    group_state = False
                                    if node_subelement.name == 'symbol':
                                        node_subsymbol = node_subelement.children[0]
                                        if node_subsymbol.name == 'SYM_REGEX':
                                            value_str: str = node_subsymbol.content
                                            lexical = tpt.get_definition_value(node_subsymbol.content)
                                            if lexical is not None:
                                                lexical_set.append([lexical, value_str])
                                                continue
                                    elif node_subelement.name == 'group':  # monitor_object
                                        # node_subgroup = node_subelement.children[0]
                                        for this_subgroup in node_subelement.children:
                                            if this_subgroup.name == ':Text':
                                                if this_subgroup.content == '(':
                                                    group_state = True
                                                    print('1sub-GROUP! Do something')
                                                elif this_subgroup.content == ')':
                                                    group_state = False
                                            elif this_subgroup.name == 'expression' and group_state is True:
                                                lexical = tpt.get_first_lexicals_start_at_expression_node(
                                                    this_subgroup)
                                                if lexical is not None:
                                                    lexical_set.append(lexical)
                                elif node_suboption.name == ':Text':
                                    if node_suboption.content == '?':
                                        skip_subsequence_and = True  # markup_format
                        if node_subterm.name == 'element':
                            node_subelement = node_subterm.children[0]
                            group_state = False
                            if node_subelement.name == 'group':
                                # node_subgroup = node_subelement.children[0]
                                for this_subgroup in node_subelement.children:
                                    if this_subgroup.name == ':Text':
                                        if this_subgroup.content == '(':
                                            group_state = True
                                            print('2sub-GROUP! Do something')
                                        elif this_subgroup.content == ')':
                                            group_state = False
                                    elif this_subgroup.name == 'expression' and group_state is True:
                                        lexical = tpt.get_first_lexicals_start_at_expression_node(this_subgroup)
                                        if lexical is not None:
                                            lexical_set.append(lexical)

                            elif node_subelement.name == 'symbol':
                                symbol_lexical = None
                                node_subsymbol = node_subelement.children[0]
                                if node_subsymbol.name == 'SYM_REGEX':
                                    if is_expression(node_subsymbol.content):
                                        subexpression = node_subsymbol.content
                                        print('%s is an sub-expression' % subexpression)
                                        subexpression_tuple: tuple = tpt.build_expression_tree(subexpression)
                                        print('subtree of ', subexpression, 'subexpression: ', subexpression_tuple)
                                        for this_subsequence in subexpression_tuple:
                                            symbol_lexical = tpt.get_first_lexicals_starting_at_sequence_node(
                                                this_subsequence)
                                            if symbol_lexical is not None:
                                                lexical_set.append([symbol_lexical, subexpression])
                                                continue
                                    if is_symbol(node_subsymbol.content):
                                        print('%s is a symbol' % node_subsymbol.content)
                                        lexical = tpt.get_definition_value(node_subsymbol.content)
                                    if lexical is not None:
                                        lexical_set.append(symbol_lexical)
                                        continue
                                    else:
                                        print("4: %s is referenced but not defined." % node_subsymbol.content)
                                        sys.exit(-9)
        return lexical_set

    @staticmethod
    def get_first_lexicals_starting_at_sequence_node(
            this_parser_subtree: DHParser.Node
    ) -> (tuple, bool):
        """
        get the first lexicals (might be OR'd together so get those as well)
        :param this_parser_subtree:
        :type this_parser_subtree: DHParser.Node
        :return:
        :rtype: (tuple, bool)
        """
        force_subsequence_question_operator: bool = False
        skip_subsequence_any_and: bool = False
#        lexical = None
        lexical_set = []
        for node_subsequence in this_parser_subtree:
            if node_subsequence.name == 'AND':
                if force_subsequence_question_operator:
                    force_subsequence_question_operator = False
                    continue
                elif skip_subsequence_any_and:
                    skip_subsequence_any_and = False  # markup_format
                    continue
                break
            elif node_subsequence.name == 'interleave':
                node_subinterleave = node_subsequence.children[0]
                if node_subinterleave.name == 'difference':
                    node_subdifference = node_subinterleave.children[0]
                    if node_subdifference.name == 'term':
                        # may have 2 or more nodes due to '?' suffix operator
                        node_subterm = node_subdifference.children[0]
                        if node_subterm.name == 'option':
                            # Pretty much always 2 or more children with 'option'
                            for node_suboption in node_subterm.children:
                                # First children is typically a SYM_REGEX
                                # Second children is typically a '?', which means we continue on to next 'difference' or above 'element'->'option'->'term'->'difference'
                                if node_suboption.name == 'element':
                                    node_subelement = node_suboption.children[0]
                                    group_state = False
                                    if node_subelement.name == 'symbol':
                                        node_subsymbol = node_subelement.children[0]
                                        if node_subsymbol.name == 'SYM_REGEX':
                                            if is_symbol(node_subsymbol.content):
                                                lexical = tpt.get_definition_value(node_subsymbol.content)
                                                if lexical is not None:
                                                    lexical_set.append([lexical, node_subsymbol.content])
                                                    continue
                                                else:
                                                    print("%s is referenced but not defined\n\n\n\n\n\n" % node_subsymbol.content)
                                                    sys.exit(-9)
                                            elif is_expression(node_subsymbol.content):
                                                subexpression = node_subsymbol.content
                                                print('%s is an sub-expression' % subexpression)
                                                subexpression_tuple: tuple = tpt.build_expression_tree(
                                                    subexpression)
                                                if subexpression_tuple is None:
                                                    print('subexpression \"%s\" is not found in \'%s\' file.' % (subexpression, nftables_ebnf_filepath))
                                                    sys.exit(-9)  # File Not Found
                                                print('subtree of ', subexpression, 'subexpression: ',
                                                      subexpression_tuple)
                                                for this_subsequence in subexpression_tuple:
                                                    if this_subsequence.name == 'sequence':
                                                        lexical, force_subsequence_question_operator = tpt.get_first_lexicals_starting_at_sequence_node(
                                                            this_subsequence)
                                                        if lexical is not None:
                                                            lexical_set.append(lexical)
                                                            continue
                                                        else:
                                                            print("2: %s is referenced but not a lexical", lexical)
                                                    elif this_subsequence.content == 'OR':
                                                        continue
                                                continue
                                    elif node_subelement.name == 'group':  # monitor_object
                                        # node_subgroup = node_subelement.children[0]
                                        for this_subgroup in node_subelement.children:
                                            if this_subgroup.name == ':Text':
                                                if this_subgroup.content == '(':
                                                    group_state = True
                                                    print('3sub-GROUP! Do something')
                                                elif this_subgroup.content == ')':
                                                    group_state = False
                                            elif this_subgroup.name == 'expression' and group_state is True:
                                                lexical = tpt.get_first_lexicals_start_at_expression_node(
                                                    this_subgroup)
                                                if lexical is not None:
                                                    lexical_set.append(lexical)
                                                    continue
                                elif node_suboption.name == ':Text':
                                    if node_suboption.content == '?':
                                        skip_subsequence_any_and = True  # markup_format
                                        force_subsequence_question_operator = True
                                        continue
                        elif node_subterm.name == 'element':
                            node_subelement = node_subterm.children[0]
                            group_state = False
                            if node_subelement.name == 'literal':
                                node_value = node_subelement.content
                                if node_value is not None:
                                    lexical = [ node_value ]
                                    if lexical is None:
                                        print('lexical is None')
                                        sys.exit(-1)
                                    lexical_set.append(lexical)
                            elif node_subelement.name == 'group':
                                # node_subgroup = node_subelement.children[0]
                                for this_subgroup in node_subelement.children:
                                    if this_subgroup.name == ':Text':
                                        if this_subgroup.content == '(':
                                            group_state = True
                                            print('4sub-GROUP! Do something')
                                        elif this_subgroup.content == ')':
                                            group_state = False
                                    elif this_subgroup.name == 'expression' and group_state is True:
                                        lexical = tpt.get_first_lexicals_start_at_expression_node(this_subgroup)
                                        if lexical is not None:
                                            lexical_set.append(lexical)

                            elif node_subelement.name == 'symbol':
                                node_subsymbol = node_subelement.children[0]
                                if node_subsymbol.name == 'SYM_REGEX':
                                    if is_expression(node_subsymbol.content):
                                        subexpression = node_subsymbol.content
                                        print('Expanding \"%s\" sub-expression ...' % subexpression)
                                        subexpression_tuple: tuple = tpt.build_expression_tree(subexpression)
                                        if subexpression_tuple is None:
                                            print('sub-expression \"%s\" is not found in \'%s\' file.' % (subexpression, nftables_ebnf_filepath))
                                            sys.exit(-9)  # File Not Found
                                        print('subexpression \'', subexpression, '\' tuple: ', subexpression_tuple)
                                        # EBNF '|' operator used here
                                        for this_subsequence in subexpression_tuple:
                                            if this_subsequence.name == 'sequence':
                                                lexical, force_subsequence_question_operator = tpt.get_first_lexicals_starting_at_sequence_node(
                                                    this_subsequence)
                                                if lexical is not None:
                                                    lexical_set.append([lexical, this_subsequence.content])
                                            elif this_subsequence.content == '|':
                                                # Because this design is about all 'possible' first-level words/symbol, we continue beyond 'OR' (but not 'AND')
                                                continue
                                    elif is_symbol(node_subsymbol.content):
                                        print('is_symbol(%s)' % node_subsymbol.content)
                                        # print('%s is a symbol' % node_subsymbol.content)
                                        lexical = tpt.get_definition_value(node_subsymbol.content)
                                        if lexical is not None:
                                            lexical_set.append([lexical, node_subsymbol.content])
                                        else:
                                            print("Symbol \"%s\" is referenced but not defined in \'%s\' file." % (node_subsymbol.content, nftables_ebnf_filepath))
                                            sys.exit(-9)
                        # '?' operator encountered here
                        elif node_subterm.name == 'option':
                            for this_subterm in node_subterm.children:
                                node_subelement = this_subterm
                                group_state = False
                                if node_subelement.name == 'group':
                                    # node_subgroup = node_subelement.children[0]
                                    for this_subgroup in node_subelement.children:
                                        if this_subgroup.name == ':Text':
                                            if this_subgroup.content == '(':
                                                group_state = True
                                                print('5sub-GROUP! Do something')
                                            elif this_subgroup.content == ')':
                                                group_state = False
                                        elif this_subgroup.name == 'expression' and group_state is True:
                                            lexical = tpt.get_first_lexicals_start_at_expression_node(this_subgroup)
                                            if lexical is not None:
                                                lexical_set.append(lexical)

                                elif node_subelement.name == 'symbol':
                                    node_subsymbol = node_subelement.children[0]
                                    if node_subsymbol.name == 'SYM_REGEX':
                                        if is_expression(node_subsymbol.content):
                                            subexpression = node_subsymbol.content
                                            print('%s is an sub-expression' % subexpression)
                                            subexpression_tuple: tuple = tpt.build_expression_tree(subexpression)
                                            print('subtree of ', subexpression, 'subexpression: ', subexpression_tuple)
                                            # EBNF '|' operator used here
                                            for this_subsequence in subexpression_tuple:
                                                if this_subsequence.name == 'sequence':
                                                    lexical,force_subsequence_question_operator = tpt.get_first_lexicals_starting_at_sequence_node(this_subsequence)
                                                    if lexical is not None:
                                                        lexical_set.append(lexical)
                                                elif this_subsequence.content == 'OR':
                                                    continue
                                        if is_symbol(node_subsymbol.content):
                                            print('%s is a symbol' % node_subsymbol.content)
                                            lexical = tpt.get_definition_value(node_subsymbol.content)
                                            if lexical is not None:
                                                lexical_set.append(lexical)
                                            else:
                                                print("3: %s is referenced but not defined.\n\n\n\n\n" % node_subsymbol.content)
                                                sys.exit(-9)
                                elif node_subelement.name == ':Text':
                                    if node_subelement.content == '?':
                                        force_subsequence_question_operator = True
        return lexical_set, force_subsequence_question_operator


    def print_all_first_level_lexicals_of_this_node(self, label: str, this_parser_tuple: tuple):
        """
        Print out the first-encounter literals in a given expression tree
        :param label:
        :param this_parser_tuple:
        :type this_parser_tuple: tuple
        :return:
        """
        seq_seen: bool = False
        seq_next: bool = True
        or_next: bool = False
        lexicals = []
        for this_node in this_parser_tuple:
            if this_node.name == 'sequence':
                if not seq_next:
                    print('In %s, sequence did not appear firstly' % label)
                    break
                seq_seen = True
                or_next = True
                seq_next = False
                this_lex, tmp_bool = self.get_first_lexicals_starting_at_sequence_node(this_node)
                if len(this_lex) == 0:
                    this_sym_name = this_node.children[0].children[0].children[0].children[0].children[0].content
                    print('WARNING: In %s, `%s` is not explicitly declared nor defined.' % (label, this_sym_name))
                lexicals.append([this_lex, this_node.content])
            elif this_node.name == 'OR':
                if not seq_seen:
                    print('In %s, OR unexpectedly came first; Out of order sequence' % label)
                    break
                if not or_next:
                    print('In %s, OR unexpectedly out-of-order' % label)
                    break
                if or_next:
                    or_next = False
                    seq_next = True
                    continue
        print('%s = %s.' % (label, lexicals))

        return


if __name__ == "__main__":
    # vim_syntax_group_name_target = 'verdict_expr'
    # weird, 'set_elem_stmt' was expanded in nftables.ebnf
    # vim_syntax_group_name_target = 'input'
    # vim_syntax_group_name_target = 'base_cmd'
    vim_syntax_group_name_target = 'add_cmd'

    nftables_ebnf_filepath = 'nftables.ebnf'
    # nftables_ebnf_filepath = 'test-nftables-tmp.ebnf'
    # nftables_ebnf_filepath = 'test-nftables-tmp-rule_alloc.ebnf'
    # nftables_ebnf_filepath = 'test-nftables-question-mark.ebnf'
    # nftables_ebnf_filepath = 'test-nftables-AND-two.ebnf'

    nftables_ebnf_path = pathlib.Path(nftables_ebnf_filepath)

    print('Executing...')

    # Prepare the EBNF parser-parser
    tpt = TwoStageParser()

    # Load target-specific parser based on EBNF parse syntax
    tpt.load_target_grammar_text(nftables_ebnf_path)

    # Construct CFG/SREC parse tree of target-specific parse syntax
    tpt.construct_grammar_target_parse_tree()

    # collect all the literal definitions (beyond EBNF)
    tpt.collect_target_terminal_definitions()

    print('Building %s parse tree...' % vim_syntax_group_name_target, end='')
    vim_syntax_group_node: tuple = tpt.build_expression_tree(vim_syntax_group_name_target)
    print('.')

    if vim_syntax_group_node is None:
        print('subexpression \"%s\" is not a valid node name.' % vim_syntax_group_name_target)
        if is_expression(vim_syntax_group_name_target):
            print('This \"%s\" is not an expression (all lower-case)' % vim_syntax_group_name_target)
        if is_symbol(vim_syntax_group_name_target):
            print('This \"%s\" is a symbol, you probably want an expression (all lower-case)' % vim_syntax_group_name_target)
        sys.exit(-9)  # File Not Found

    print('%s: ' % vim_syntax_group_name_target, end='')
    print('Printing lexical strings for %s ...' % vim_syntax_group_name_target)
    tpt.print_all_first_level_lexicals_of_this_node(vim_syntax_group_name_target, vim_syntax_group_node)

#     tpt.collect_expressions()
