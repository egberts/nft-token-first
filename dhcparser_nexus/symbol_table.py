""" Title: Symbol Table for EBNF """

# Futures
from __future__ import unicode_literals
from __future__ import print_function

# Generic/Built-in
import re

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


class SymbolTable:
    """ Maintain a symbol table """

    # hint types
    _total_count: int = 0
    _array_symtbl: dict[0] = {}
    label: str
    value: str

    def __init__(self) -> None:
        """
        :rtype: None

        """
        # self._array_symtbl = {}
        self.label: str = ''
        self.value: str = ''
        # self.symbol: bool = False
        # self.literal: bool = False
        # self.groupname_symbol: bool = False
        # self.clustername = False
        pass

    def set_label(self, label: str) -> None:
        """

        :param label:
        """
        self.label: str = label

    @property
    def get_label(self) -> str:
        """

        :return:
        """
        return self.label

    def set_value(self, value: str) -> None:
        """

        :param value:
        :return:
        """
        self.value: str = value

    @property
    def get_value(self) -> str:
        """

        :return:
        """
        return self.value

    def find_symbol(self, literal_name: str) -> bool:
        """ find symbol in symbol table """
        if not bool(re.match('^[a-zA-Z0-9_]+$', literal_name)):
            print(f'Token {literal_name} is not a valid token identifier')
            raise ValueError
        for x in self._array_symtbl:
            if self._array_symtbl[x]['name'] == literal_name:
                return True
        return False

    def extract_symbol(self, literal_name) -> bool:
        """ extract symbol _item from symbol table """
        result_str = self.find_symbol(literal_name)
        return result_str

    def add_to_symbol_table(
            self,
            literal_name: str = '',
            value: str = ''
            ) -> None:
        """
        Add a literal string name

        :param literal_name:
        :param value:
        :return:
        """
        if literal_name == '':
            if self.label == '':
                raise ValueError
        else:
            self.label = literal_name
        if value == '':
            if self.value == '':
                raise ValueError
        else:
            self.value = value
        if self.find_symbol(self.label):
            print(f'add_literal: symbol {literal_name} already exist in symbol table.')
            raise OverflowError
        one_symbol_entry = {'name': literal_name, '_item': value}
        self._array_symtbl[self._total_count] = one_symbol_entry
        self._total_count += 1
