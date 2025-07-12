"""
Track EBNF syntax for 'AND' and 'OR' operators for grouping together
TOKENs for later statement partial ordering reconstruction via
multimethod dispatch.
"""

# Futures
from __future__ import print_function
from __future__ import unicode_literals

# Generic/Built-in
import sys

# Other Libs
# import pandas as pd

# Owned
# from vim_node import VimscriptStmtNode

__author__ = 'egberts@github.com'
__copyright__ = 'Copyright 2024'
__credits__ = ['egberts@github.com']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'egberts@github.com'
__email__ = 'egberts@github.com'
__status__ = 'Dev'

from inspect import isclass


class CSGTokenNode:
    """
    At EBNF CSG/CST tree, we deal with EBNF-side of Vimscript Syntax
    """

    # hint types
    _token: str
    _syntax_literal: bool
    _syntax_operator_and: bool
    _syntax_operator_or: bool

    def __init__(self, token: (None | str) = None):
        """ Create an instance of VimscriptStmtNode with optional token """
        if (
                token is not None and
                not isinstance(token, str) and
                not isclass(token)
        ):
            raise ValueError

        self._token: (None | str | CSGTokenNode) = token
        # Notice, no _item here, just _token/TOKEN (which includes AST literal as TOKEN)
        self._head = None
        self._next = None
        # CSG-related (DHParser Syntax Tree)
        self._syntax_operator_and = False
        self._syntax_operator_or = False

        # CSG-related (DHParser Syntax Tree)
        # self._syntax_terminal = False
        self._syntax_literal = False
        # self._syntax_symbol_name = False
        # note: there is no keyword support (use `syntax match` instead)

    @property
    def is_literal(self) -> bool:
        """ Is this Vim node contains a syntax literal? """
        return self._syntax_literal

    @property
    def is_operator_and(self) -> bool:
        """ Is this Vim node to the AND operator """
        return self._syntax_operator_and

    @property
    def is_operator_or(self) -> bool:
        """ Is this Vim node to the OR operator """
        return self._syntax_operator_or

    def set_literal(self) -> None:
        """ Set this Vim node to literal type """
        self._syntax_literal = True

    def set_operator_and(self) -> None:
        """ Set this Vim node to the AND operator """
        self._syntax_operator_and = True

    def set_operator_or(self) -> None:
        """ Set this Vim node to the OR operator """
        self._syntax_operator_or = True

    @property
    def get_token(self):
        """ return a _item """
        return self._token

    def set_token(self, arg_value: str) -> None:
        """ set a _item """
        self._token = arg_value

    @property
    def get_head(self):
        """ Get _head of linked-list """
        return self._head

    def set_head(self, head) -> None:
        """ Set the _head of linked-list """
        self._head = head

    @property
    def get_next(self):
        """ Get _next of linked-list """
        return self._next

    def set_next(
            self,
            new_next
    ) -> None:
        """ Set the _next of linked-list """
        self._next = new_next

    def insert_at_end(self, data) -> None:
        """ Insert node at end of linked-list """
        if self != self.get_head:
            print('not a head link')
            raise LookupError
        if isinstance(data, str):
            new_node = CSGTokenNode(data)
            new_node.set_head(self)
            new_node.set_next(None)
            this_node: CSGTokenNode = self
            while this_node:
                new_next = this_node.get_next
                if new_next:
                    this_node = new_next
                else:
                    break
            this_node.set_next(new_node)
        elif isinstance(data, CSGTokenNode):
            ctn: CSGTokenNode = data
            if self._head is None:
                self._head = data

            current_node = self
            while current_node._next:
                current_node = current_node._next

            current_node._next = data
        else:
            print('insert_at_end: token is not str type nor VimscriptStmtNode type')
            sys.exit(-9)
