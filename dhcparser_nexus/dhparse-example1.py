# Title: VimL Syntax statements
""" Supports for VimL Syntax statements """

# Futures
from __future__ import print_function
from __future__ import unicode_literals

# Generic/Built-in
import copy
import sys
from typing import List, Any, Tuple

# Other Libs
import DHParser
from DHParser.dsl import create_parser

# Owned
import symbol_table
import viml_syntax_output
from symbol_table import SymbolTable
from csg_token_node import CSGTokenNode
from vimscript_stmt_node import VimscriptStmtNode

# from vim_node import VimscriptStmtNode

__author__ = 'egberts@github.com'
__copyright__ = 'Copyright 2024'
__credits__ = ['egberts@github.com']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'egberts@github.com'
__email__ = 'egberts@github.com'
__status__ = 'Dev'

global my_definition_table, empty_definition_table

vim_out = viml_syntax_output.Output('nft_')
symbol_table: None | SymbolTable = None

#  Read in DHParser multi-variant EBNF specification file
fd = open('ebnf-flexible.dhparse')
ebnf_grammar = fd.read()

# grammatically parse the EBNF for sub-sequential EBNF compiling
ebnf_parser: DHParser.Grammar = create_parser(ebnf_grammar, 'nft')

g_first_vimscript_statement: bool = True


def process_literal(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'literal' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'literal' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'literal':
        if len(pn.children) == 0:
            new_value = copy.copy(pn.result)
            # Remove DHParser's single-quote pair
            if new_value[0:1] == '\'':
                new_value = new_value[1:]
            if new_value[-1:] == '\'':
                new_value = new_value[0:-1]
            csg_token_node: CSGTokenNode = CSGTokenNode()
            csg_token_node.set_literal()
            csg_token_node.set_token(new_value)
        else:
            print(f'proces_literal: {pn.result} unexpectedly has more than 0 children')
    else:
        print(f'process_literal: Unexpectedly called using {pn.name}.')
    return csg_token_node


def process_text(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'text' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'text' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == ':Text':
        if len(pn.children) == 0:
            new_value = copy.copy(pn.result)
            if pn.result[0:1] == '\'':
                new_value = pn.result[1:]
            if new_value[-1:] == '\'':
                new_value = pn.result[0:-1]
            csg_token_node = CSGTokenNode()
            csg_token_node.set_token(new_value)
            if new_value == 'AND':
                csg_token_node.set_operator_and()
            elif new_value == 'OR':
                csg_token_node.set_operator_or()
            csg_token_node.insert_at_end({'text_op': new_value})
        else:
            print(f'process_text: {pn.result} unexpectedly has more than 0 children')
    else:
        print(f'process_text: Unexpectedly called using {pn.name}.')
    return csg_token_node


def process_repetition(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'repetition' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'repetition' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'repetition':
        if len(pn.children) > 0:
            for n_idx in range(0, len(pn.children)):
                nc: DHParser.Node = pn.children[n_idx]
                if nc.name == 'literal':
                    if len(pn.children) == 1:
                        csg_token_node = process_literal(nc)
                    else:
                        print(f'process_repetition: {nc.name} unexpectedly has more than 1 children')
                elif nc.name == 'element':
                    if len(pn.children) > 1:
                        csg_token_node = process_element(nc)
                    else:
                        print(f'process_repetition: {nc.name} unexpectedly has less than 2 children')
                elif nc.name == ':Text':
                    csg_token_node = process_text(nc)
                else:
                    print(f'process_repetition: Unknown \'{nc.name}\' node type.')

        else:
            print('process_repetition unexpectedly missing a child')
    else:
        print(f'process_repetition: unexpectedly called with {pn.name}')
    return csg_token_node


def process_element(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'element' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'element' node
    :return: A VimscriptStmtNode to the Vim linked-list
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'element':
        if len(pn.children) > 0:
            nc: DHParser.Node = pn.children[0]
            if nc.name == 'literal':
                if len(pn.children) == 1:
                    csg_token_node = process_literal(nc)
                else:
                    print(f'process_element: {nc.name} unexpectedly has more than 1 children')
            elif nc.name == 'symbol':
                if len(pn.children) == 1:
                    csg_token_node: CSGTokenNode = process_symbol(nc)
                    csg_token_node.set_token('')
                    # TODO where do I set 'symbol' flag ???
                else:
                    print(f'process_element: {nc.name} unexpectedly has more than 1 children')
            else:
                print(f'process_element: Unexpectedly called using {nc.name}.')
        else:
            print('process_element unexpectedly missing a child')
    else:
        print(f'process_element: unexpectedly called with {pn.name}')
    return csg_token_node


def process_term(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'term' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'term' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'term':
        if len(pn.children) > 0:
            for n_idx in range(0, len(pn.children)):
                this_parse_node: DHParser.Node = pn.children[n_idx]
                if this_parse_node.name == 'element':
                    csg_token_node = CSGTokenNode(None)
                    if len(pn.children) == 1:
                        csg_token_node = process_element(this_parse_node)
                    else:
                        print(f'process_term: {this_parse_node.name} unexpectedly has not exactly 1 children')
                elif this_parse_node.name == 'repetition':
                    if len(pn.children) == 1:
                        csg_token_node = process_repetition(this_parse_node)
                    else:
                        print(f'process_term: {this_parse_node.name} unexpectedly does not have exactly 1 child.')
                else:
                    print(f'process_term: Unexpectedly called using {pn.name}.')
        else:
            print('process_term: unexpectedly has no child')
    else:
        print(f'process_term: unexpectedly called with {pn.name}')
    return csg_token_node


def process_difference(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'difference' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'difference' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'difference':
        if len(pn.children) > 0:
            this_parse_node: DHParser.Node = pn.children[0]
            if len(pn.children) == 1:
                csg_token_node = process_term(this_parse_node)
            else:
                print(f'process_difference: {this_parse_node.name} unexpectedly has not exactly 1 children')
        else:
            print('process_difference: unexpectedly has no child')
    else:
        print(f'process_difference: unexpectedly called with {pn.name}')
    return csg_token_node


def process_interleave(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'interleave' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'interleave' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'interleave':
        if len(pn.children) == 1:
            this_parse_node: DHParser.Node = pn.children[0]
            csg_token_node = process_difference(this_parse_node)
        else:
            print('process_interleave: unexpectedly has more than 1 children')
    else:
        print(f'process_interleave: unexpectedly called with {pn.name}')
    return csg_token_node


def process_sequence(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    All about the AND-logic:
    Process the 'sequence' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'sequence' node
    :return: a dict of numerically-index elements containing AND'd elements
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'sequence':
        if len(pn.children) > 0:
            if len(pn.children) == 1:
                this_parse_node: DHParser.Node = pn.children[0]
                csg_token_node = process_interleave(this_parse_node)
            elif len(pn.children) > 1:
                csg_token_node = VimscriptStmtNode('AND')
                csg_token_node.set_operator_and()
                for n_idx in range(0, len(pn.children)):
                    this_parse_node: DHParser.Node = pn.children[n_idx]
                    if this_parse_node.name == 'interleave':
                        pi = process_interleave(this_parse_node)
                        if pi.is_symbol:
                            csg_token_node.add_to_stmt_list(pi)
                    elif this_parse_node.name == 'AND':
                        pass
            else:
                print('process_sequence: unexpectedly has more than 1 children')
        else:
            print('process_sequence: unexpectedly has no child.')
    else:
        print(f'process_sequence: Unexpectedly called using {pn.name}.')
    return csg_token_node


def process_expression(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'expression' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'expression' node
    :return:
    """
    vsn: (None, VimscriptStmtNode) = None
    if pn.name == "expression":
        if len(pn.children) > 0:
            this_parse_node: DHParser.Node = pn.children[0]
            for n_idx in range(0, len(pn.children)):
                if this_parse_node.name == 'sequence':
                    csg_token_node = process_sequence(this_parse_node)
                    if len(pn.children) == 1:
                        vsn = csg_token_node
                    elif len(pn.children) >= 3:
                        vsn.add_to_stmt_list(csg_token_node)
                    else:
                        print(f'process_expression: {this_parse_node.name} unexpectedly has more than 1 child.')
                elif this_parse_node.name == 'OR':
                    vsn.set_operator_or()
                else:
                    print(f'process_expression: unexpectedly have '
                          'a \'{this_parse_node.name}\' child.')
        else:
            print(f'process_expression: unexpectedly have no child.')
    else:
        print(f'process_expression: unexpectedly called with {pn.name}.')
    return vsn


def process_def(pn: DHParser.Node) -> None | VimscriptStmtNode:
    """
    Process the 'DEF' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'DEF' node
    :return:
    """
    symtbl_entry = None
    if pn.name == 'DEF':
        if len(pn.children) == 0:
            pass
        else:
            print('process_DEF: DEF unexpectedly has at least 1 child')
    else:
        print(f'process_DEF: unexpectedly called with {pn.name}')
    return symtbl_entry


def process_sym_regex(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'SYM_REGEX' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'SYM_REGEX' node
    :return:
    """
    csg_token_node: None | CSGTokenNode = None
    if pn.name == 'SYM_REGEX':
        if len(pn.children) == 0:
            new_name = copy.copy(pn.result)
            csg_token_node = CSGTokenNode(new_name)
        else:
            print('process_SYM_REGEX: SYM_REGEX unexpectedly has more than 0 children')
    else:
        print(f'process_SYM_REGEX: unexpectedly called with {pn.name}')
    return csg_token_node


def process_symbol(pn: DHParser.Node) -> None | CSGTokenNode:
    """
    Process the 'symbol' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'symbol' node
    :return:
    """
    csg_token_node: (None, CSGTokenNode) = None
    if pn.name == 'symbol':
        if len(pn.children):
            for cn in range(0, len(pn.children)):
                nc: DHParser.Node = pn.children[cn]
                if nc.name == 'SYM_REGEX':
                    csg_token_node: (None, CSGTokenNode) = process_sym_regex(nc)
                else:
                    print(f'process_symbol: Unexpectedly called using {pn.name}.')
        else:
            print('process_symbol: has no children')
    else:
        print(f'process_symbol: unexpectedly called with {pn.name}')
    return csg_token_node


def process_definition(pn: DHParser.Node) -> dict:
    """
    Process the 'definition' node of an EBNF syntax tree

    :param pn: A node to the syntax tree, specifically the EBNF 'definition' node
    :return:
    """
    vn: None | VimscriptStmtNode = None
    symtbl_entry = {}
    symbol_name_str = ''
    csg_token_node: None | CSGTokenNode = None
    if type(pn.children) is tuple:
        for cn in range(0, len(pn.children) - 1):
            nc: DHParser.Node = pn.children[cn]
            vn: VimscriptStmtNode = VimscriptStmtNode()
            if type(nc) is DHParser.Node:
                if nc.name == 'symbol':
                    lh_syn_token_node: None | CSGTokenNode = process_symbol(nc)
                    symbol_name_str = lh_syn_token_node.get_token
                elif nc.name == 'DEF':
                    vn: VimscriptStmtNode = process_def(nc)
                    # symtbl_entry['lhs_name'] = symbol_name_str
                elif nc.name == 'expression':
                    csg_token_node: CSGTokenNode = process_expression(nc)
                    vn: VimscriptStmtNode = VimscriptStmtNode(symbol_name_str)
                    vn.set_groupname(symbol_name_str)
                    if csg_token_node.is_literal:
                        # got enough for a symbol table entry
                        sym_tbl_entry = SymbolTable()
                        sym_tbl_entry.set_label(symbol_name_str)
                        sym_tbl_entry.add_to_symbol_table(
                            symbol_name_str,
                            csg_token_node.get_token
                        )
                        vn.set_match_flag()
                        vn._item = csg_token_node.get_token
                    else:
                        vn.set_cluster_flag()
                elif nc.name == 'ENDL':
                    pass
                else:
                    print(f'process_definition: Unexpectedly called using {pn.name}.')
                    pass
            else:
                print("'process_definition' children unexpectedly encountered a non Node.")
        if csg_token_node.is_operator_and:
            this_str: str = vn.get_groupname()
            next_vn: CSGTokenNode = csg_token_node.get_next
            if next_vn.is_cluster:
                vim_out.cluster(symbol_name_str + this_str)
                while next_vn:
                    vim_out.contains(next_vn._groupname)
                    next_vn = next_vn.next
            elif next_vn.is_group:
                vim_out.match(symbol_name_str + this_str, pattern=next_vn._groupname)
                while next_vn:
                    vim_out.next_group(next_vn._groupname)
                    next_vn = next_vn.next
        elif vn.is_literal:
            literal_value = vn.get_groupname()
            tmp_symtbl_items = {'lhs_name': symbol_name_str, '_item': literal_value}
            symtbl_entry.update(tmp_symtbl_items.copy())
            symbol_table.add_literal(symbol_name_str, literal_value)
            if vn.is_group:
                vim_out.match(symbol_name_str, literal_value)
                vim_out.skipwhite()
                vim_out.contained()
            # no `nextgroup=` here.
    else:
        print("process_definition: Unexpectedly with non-tuple")
    return symtbl_entry.copy()


def collect_one_definition(node: any) -> list:
    """

    :param node:
    :return:
    """
    this_list = []
    symbol_name = None
    node_value = None
    if isinstance(node, DHParser.Node):
        if node.name == 'definition':
            node_symbol = node.children[0]
            if node_symbol.name == 'symbol':
                node_sym_regex = node_symbol.children[0]
                if node_sym_regex.name == 'SYM_REGEX':
                    symbol_name = node_sym_regex.content
                    if symbol_name == 'ZONE':
                        print('ZONE got here')
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
                                        node_value = '\'fancy-regex\''

    if node_value is not None:
        this_list = [symbol_name, node_value]
    else:
        this_list = None
    return this_list


def collect_definitions(rn: DHParser.RootNode) -> tuple[None | list[list], None | list[list]]:
    """
    Collect only definitions
    :param rn: Root Node from DHParser
    :return: A list of definitions
    :rtype: list
    """
    if rn.name != 'syntax':
        print('collect_symbols: parse tree is not root-labeled as \'syntax\'.')
        return None, None
    list_definitions = []

    if type(rn) is not DHParser.RootNode and rn.name != 'syntax':
        print("Not a RootNode")
        sys.exit(-9)
    print("Node count: ", len(rn.children))
    if len(rn.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    this_def_pairs = []
    empty_def_pairs = []
    for n in range(0, len(rn.children)):  # how many 'syntax' (usually 1)
        if n == 2:
            print('Debug me')
        node = rn.children[n]
        this_def = collect_one_definition(node)
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
    return this_def_pairs, empty_def_pairs


def is_symbol(this_string):
    """
    is this string a symbol that contains a raw lexical token value?
    :param this_string:
    :return:
    """
    if 'A' <= this_string[0] <= 'Z':
        return True
    if '_' == this_string[0] and ('A' <= this_string[1] <= 'Z'):
        return True
    return False


def is_expression(this_string: str) -> bool:
    """
    is this string an expression?  A symbol name denoted by all lowercase
    :param this_string:
    :return:
    """
    if 'a' <= this_string[0] <= 'z':
        return True
    return False


def get_expression_node(this_string: str, this_expression_table=None) -> None | DHParser.Node:
    """
    get a node based on expression name
    :param this_string:
    :param this_expression_table:
    :return:
    """
    for this_expression in this_expression_table:
        if this_string == this_expression[0]:
            return this_expression
    return None


def get_definition_value(this_string: str, this_definition_table=None):
    """
    get a value based on symbol name
    :param this_string:
    :param this_definition_table:
    :return:
    """
    for this_sym in this_definition_table:
        if this_string == this_sym[0]:
            return this_sym[1]
    return None


def is_in_my_parse_table(this_string: str, symtable=None):
    """
    Is it in my symbol table?
    :param this_string:
    :return:
    """
    for this_sym in symtable:
        if this_string == this_sym[0]:
            return True
    return False


def is_literal(this_string: str, symtable: list) -> bool:
    """
    is this string a Literal
    :param this_string:
    :param symtable:
    :return:
    """
    if is_symbol(this_string):
        for this_sym in symtable:
            if this_string == this_sym[0]:
                return True
    return False


def node_sequence_print_first_lexical(node_sequence):
    """
    Node sequence, print out first lexicals
    :param node_sequence:
    :return:
    """
    if node_sequence.name == 'sequence':
        for this_subsequence in node_sequence.children:
            if this_subsequence.name == 'AND':
                break  # get out of loop
            elif this_subsequence.name == 'interleave':
                for this_difference in this_subsequence.children:
                    node_term = this_difference.children[0]
                    if node_term.name == 'term':
                        node_element = node_term.children[0]
                        if node_element.name == 'element':
                            node_subelement = node_element.children[0]
                            if node_subelement.name == 'literal':
                                print('literal: ', node_subelement.content)
                            elif node_subelement.name == 'group':
                                for node_subgroup in node_subelement:
                                    if node_subgroup.name == 'expression':
                                        for node_subexpression in node_subgroup.children:
                                            if node_subexpression.name == 'OR':
                                                continue
                                            elif node_subexpression.name == 'sequence':
                                                node_sequence_print_first_lexical(node_subexpression)
                                        if is_in_my_parse_table(node_subgroup.content, my_definition_table):
                                            print('xlate: ', get_definition_value(node_subgroup.content, my_definition_table))

                            elif node_subelement.name == 'symbol':
                                node_sym_regex = node_subelement.children[0]
                                if node_sym_regex.name == 'SYM_REGEX':
                                    content = node_sym_regex.content
                                    if is_expression(node_sym_regex.name):
                                        print('label: ', content)
                                    if is_symbol(node_sym_regex.name):
                                        print('symbol: ', content)
                                    if is_literal(node_sym_regex.name, my_definition_table):
                                        print('literal: ', content)
                                    if is_in_my_parse_table(content, my_definition_table):
                                        print('xlate: ', get_definition_value(content, my_definition_table))
    return


def find_this_label(label: str, symtbl: list):
    """
    find this label and start resolving from there
    :param symtbl:
    :param label:
    :return:
    """
    if 'a' <= label[0] <= 'z':
        for this_symbol in symtbl:
            if this_symbol[0] == label:
                return this_symbol
    return None


def goto_next_lexical(node: any, this_parse_tree: list):
    """
    goto_next_lexical

    :param this_parse_tree:
    :param node: a pointer to a node of a syntax tree
    :type node: any
    :return:
    """
    symbol_name = None
    node_value = None
    if isinstance(node, DHParser.Node):
        if node.name == 'definition':
            node_symbol = node.children[0]
            if node_symbol.name == 'symbol':
                node_sym_regex = node_symbol.children[0]
                if node_sym_regex.name == 'SYM_REGEX':
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
                                node_subterm = node_term.children[0]
                                if node_subterm.name == 'repetition':
                                    node_value = node_subterm.content
                                if node_subterm.name == 'element':
                                    node_subelement = node_subterm.children[0]
                                    if node_subelement.name == 'group':
                                        for this_subgroup in node_subelement.children:
                                            if this_subgroup.name == ':Text':
                                                print(this_subgroup.result)
                                            elif this_subgroup.name == 'expression':
                                                for this_subexpress in this_subgroup.children:
                                                    if this_subexpress.name == 'sequence':
                                                        node_sequence_print_first_lexical(node_sequence)
                                                    elif this_subexpress.name == 'OR':
                                                        continue
                                    node_symbol = node_subelement.children[0]
                                    if node_symbol.name == 'symbol':
                                        node_value = node_symbol.content
                                        if is_expression(node_value):
                                            find_this_label(node_value, this_parse_tree)

    if node_value is not None:
        this_list = [symbol_name, node_value]
    else:
        this_list = None
    return this_list


def walk_lexical_tree(rn: DHParser.RootNode, this_parse_tree: list) -> None | List:
    """

    :param this_parse_tree:
    :param rn:
    :return:
    """
    if len(rn.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    this_def_pairs = [['input', 'line']]
    empty_def_pairs = []
    for n in range(0, len(rn.children)):  # how many 'syntax' (usually 1)
        if n == 2:
            print('Debug me')
        node = rn.children[n]
        this_def = goto_next_lexical(node, this_parse_tree)
        if this_def is not None:
            this_def_pairs.append(this_def)
    return this_def_pairs


def collect_symbols(rn: DHParser.RootNode) -> list:
    """
    Process the EBNF syntax tree

    :param rn: A node to the syntax tree, specifically the EBNF 'syntax' root node
    :return:
    """
    if rn.name != 'syntax':
        print('collect_symbols: parse tree is not root-labeled as \'syntax\'.')
        return []

    symtbl_entries = []

    if type(rn) is not DHParser.RootNode and rn.name != 'syntax':
        print("Not a RootNode")
        sys.exit(-9)
    if len(rn.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    print("Node count: ", len(rn.children))
    for n in range(0, len(rn.children)):  # how many 'syntax' (usually 1)
        if n == 2:
            print('Debug me')
        node = rn.children[n]
        this_syntax_items = process_definition(node)
        symtbl_entries.append(this_syntax_items)
    return symtbl_entries.copy()


def print_symbols(symtbl_entries: list) -> None:
    """ print symbol tables """
    print("print symbols: begin")
    for n in range(0, len(symtbl_entries)):
        se: dict = symtbl_entries[n]
        name = '(undefined)'
        if 'name' in se:
            name = se['name']
        value = '(undefined)'
        if '_item' in se:
            value = se['_item']
        print(f'    {name}  {value}')
    print("print symbols: end")


def walk_nested_symbols(my_parse_tree, given_definition_table: list, start_expression: str = 'input'):
    """
    walk the
    :param my_parse_tree:
    :param given_definition_table:
    :param start_expression:
    :return:
    """
    # skip the syntax overhead of the syntax tree, if any
    this_node = None
    if type(my_parse_tree) is DHParser.RootNode:
        if my_parse_tree.name == 'syntax':
            # find the 'input' symbol
            for this_subsyntax in my_parse_tree:
                if this_subsyntax.name == 'definition':
                    this_symbol = this_subsyntax.children[0]
                    if this_symbol.name == 'symbol':
                        this_sym_regex = this_symbol.children[0]
                        if this_sym_regex.content == start_expression:
                            print("Found %s in syntax file." % start_expression)
                            this_node = my_parse_tree
                            break
        else:
            this_node = my_parse_tree
    else:
        this_node = my_parse_tree

    if this_node is None:
        print("Symbol '%s' symbol is not found")
        sys.exit(-9)
    if len(this_node.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    print("Node count: ", len(this_node.children))

    for node in this_node:
        goto_next_lexical(node, given_definition_table)

    return


def collect_one_expression(node: any, this_definition_table) -> None | list:
    """
    Extract the children of an expression
    :param this_definition_table:
    :param node:
    :return:
    """
    this_list = []
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

                                    if node_subelement.name == 'symbol':
                                        node_subsymbol = node_subelement.children[0]
                                        if node_subsymbol.name == 'SYM_REGEX':
                                            value_name = node_subsymbol.content
                                            if is_symbol(value_name):
                                                node_value = get_definition_value(value_name, this_definition_table)

    if node_value is not None:
        this_list = [symbol_name, node_value]
    else:
        this_list = None
    return this_list


def collect_expressions(rn: DHParser.RootNode, this_definition_table) -> None | DHParser.Node:
    """
    Collect only definitions
    :param rn: Root Node from DHParser
    :param this_definition_table:
    :return: A pull-up condensed flattened parse tree
    :rtype: DHParser.Node | None
    """
    if rn.name != 'syntax':
        print('collect_symbols: parse tree is not root-labeled as \'syntax\'.')
        return None
    list_definitions = []

    if type(rn) is not DHParser.RootNode and rn.name != 'syntax':
        print("Not a RootNode")
        sys.exit(-9)
    print("Node count: ", len(rn.children))
    if len(rn.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    this_def_pairs = []
    empty_def_pairs = []
    for n in range(0, len(rn.children)):  # how many 'syntax' (usually 1)
        if n == 2:
            print('Debug me')
        node = rn.children[n]
        this_def = collect_one_expression(node, this_definition_table)
        if this_def is not None:
            if is_expression(this_def[0]):
                this_def_pairs.append(this_def)
    return this_def_pairs


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            ebnf_text = f.read()
        f.close()
    else:
        print("usage:", sys.argv[0], " <EBNF filename>")
        sys.exit(1)

    parse_tree: DHParser.RootNode = ebnf_parser(ebnf_text)

    # how: 'S-expression', 'XML', 'JSON', 'indented' accordingly, or
    #         'AST', 'CST', 'default'
    how = 'CST'
    print(parse_tree.serialize(how=how))

    # collect all the literal definitions (beyond EBNF)
    my_definition_table, empty_definition_table = collect_definitions(parse_tree)

    # collect all the EBNF expressions
    my_expression_tbl = collect_expressions(parse_tree, my_definition_table)

    #
    walk_nested_symbols(parse_tree, my_definition_table, 'line')

    # lexical = walk_lexical_tree(target_parse_tree)

    fd = open(f'nftables.serialize.{how}', "+w")
    fd.write(parse_tree.serialize(how=how))
    fd.close()

    if False:
        symbol_table: list = collect_symbols(parse_tree)
        print_symbols(symbol_table)

#    a = target_parse_tree.walk_tree()
#    if type(a) is str:
#        fd = open('nftables.walk_tree', "+w")
#       fd.write(a)
#       fd.close()
#    else:
#        print("target_parse_tree.as_: is not a str type.")
