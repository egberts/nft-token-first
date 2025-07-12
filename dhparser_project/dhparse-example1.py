# Title: VimL Syntax statements
""" Supports for VimL Syntax statements """

# Futures
from __future__ import unicode_literals
from __future__ import print_function

# Generic/Built-in
import sys

# Other Libs
import DHParser
from DHParser.dsl import create_parser

# Owned
import vim_syntax

#  Read in DHParser multi-variant EBNF specification file
fd = open('ebnf-flexible.dhparse')
ebnf_grammar = fd.read()

# grammatically parse the EBNF for sub-sequential EBNF compiling
ebnf_parser: DHParser.Grammar = create_parser(ebnf_grammar, 'nft')


def process_tuple(t):
    """

    :param t:
    :return:
    """
    if type(t) is tuple:
        for ct in range(0, len(t)):
            ctn = t[ct]
            if type(ctn) is DHParser.Node:
                process_node(ctn)
            else:
                print(f"ctn is not a 'DHParser.Node' type")
    else:
        print(f"t[{t}] is not a 'tuple' type")
    return


def process_node(n: DHParser.Node):
    """

    :param n:
    :return:
    """
    symtbl_entry = {}
    if n.name == 'definition':
        if type(n.children) is tuple:
            for cn in range(0, len(n.children)-1):
                nc = n.children[cn]
                if type(nc) is DHParser.Node:
                    tmp_entry = process_node(nc)
                    symtbl_entry.update(tmp_entry)
                else:
                    print("'definition' n.")
        else:
            print("'definition' n.children is not a tuple")
    if n.name == 'symbol':
        print('symbol.children len: ', len(n.children))
        for cn in range(0, len(n.children)):
            nc: DHParser.Node = n.children[cn]
            tmp_entry = process_node(nc)
            symtbl_entry.update(tmp_entry)
    elif n.name == 'SYM_REGEX':
        tmp_entry = n.result
        print('tmp_symtbl_entry:', tmp_entry)
        symtbl_entry = {'name': tmp_entry}
    else:
        return {}
    return symtbl_entry


def collect_symbols(p: DHParser.RootNode):
    """

    :param p:
    :return:
    """
    sym_tbl = {}
    if type(p) is not DHParser.RootNode and p.name != 'syntax':
        print("Not a RootNode")
        sys.exit(-9)
    if len(p.children) < 3:
        print("Not a enough nodes for a tree")
        sys.exit(-9)
    print("Node count: ", len(p.children))
#    node = p[-1]
    for n in range(0, len(p.children)-1):
        node = p.children[n]
        print("child idx:", len(node.children))
        process_node(node)
    return sym_tbl


if __name__ == '__main__':
    if len(sys.argv) > 0:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            ebnf_text = f.read()
        f.close()
    else:
        print("usage:", sys.argv[0], " <EBNF filename>")
        sys.exit(1)
    syntax_tree: DHParser.RootNode = ebnf_parser(ebnf_text)

    symbol_table = collect_symbols(syntax_tree)
    # how: 'S-expression', 'XML', 'JSON', 'indented' accordingly, or
    #         'AST', 'CST', 'default'
    how = 'default'
    print(syntax_tree.serialize(how=how))
    fd = open(f'nftables.serialize.{how}', "+w")
    fd.write(syntax_tree.serialize(how=how))
    fd.close()

#    a = syntax_tree.walk_tree()
#    if type(a) is str:
#        fd = open('nftables.walk_tree', "+w")
#       fd.write(a)
#       fd.close()
#    else:
#        print("syntax_tree.as_: is not a str type.")
