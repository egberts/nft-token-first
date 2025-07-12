"""
Each node contains a VimL/vimscript syntax statement.

Options and patterns are given to each node.

Also tracks symbol names for cluster-notation ('@').
"""
# Futures
from __future__ import print_function
from __future__ import unicode_literals

# Generic/Built-in
from typing import List, Any  # , Dict, Set, Any

# Other Libs
import regex
# import pandas as pd

# Owned
# import vim_syntax_token_node

__author__ = 'egberts@github.com'
__copyright__ = 'Copyright 2024'
__credits__ = ['egberts@github.com']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'egberts@github.com'
__email__ = 'egberts@github.com'
__status__ = 'Dev'

vimscript_file = []
total_viml_statements = 0


def vimscript_reset() -> None:
    """ Reset vimscript; used by test utilities """
    global vimscript_file
    global total_viml_statements
    vimscript_file = []
    total_viml_statements = 0
    return


class VimscriptStmtNode:
    """
    a
    """

    # hint types
    _groupname: (None | str)
    _nextgroup: (None | list[str])
    _contains: (None | list[str])
    _region_skip: None | str
    _match_group: None | str
    _flag_cluster: bool
    _flag_region: bool
    _flag_match: bool
    _flag_keyword: bool
    _item: None | str  # only region/match/keyword
    _flag_conceal: bool
    # `cchar` only used with `conceal`
    _flag_cchar: bool
    _flag_contained: bool   # not recognized at top-level
    _flag_containedin: bool
    _flag_transparent: bool
    _flag_oneline: bool
    # skip[white|nl|empty] only used with _flag_groupname
    _flag_skipwhite: bool   # skip over space and tab characters
    _flag_skipnl: bool   # skip over the end of a line
    _flag_skipempty: bool   # skip over empty lines (implies a "skipnl")
    _flag_display: bool
    _flag_extend: bool
    _flag_fold: bool
    _flag_concealends: bool
    _flag_excludenl: bool   # match/region

    def __del__(self):
        del self._nextgroup

    def __init__(self, groupname=None):
        """ Create an instance of VimscriptStmtNode with optional token """
        self._groupname: (None | str) = groupname  # common
        self._nextgroup: (None | list[str]) = None  # common
        self._contains: (None | list[str]) = None  # match, region, cluster
        self._region_skip: (None | str) = None
        self._match_group: (None | str) = None

        self._flag_cluster = False
        self._flag_region = False
        self._flag_match = False
        self._flag_keyword = False

        # _item is for region/match/keyword, not cluster
        self._item: (str | regex.Regex | None) = None  # only region/match/keyword

        self._flag_conceal: bool = False
        # `cchar` only used with `conceal`
        self._flag_cchar: bool = False
        self._flag_contained: bool = False  # not recognized at top-level
        self._flag_containedin: bool = False
        self._flag_transparent: bool = False
        self._flag_oneline: bool = False

        # skip[white|nl|empty] only used with _flag_groupname
        self._flag_skipwhite: bool = False  # skip over space and tab characters
        self._flag_skipnl: bool = False  # skip over the end of a line
        self._flag_skipempty: bool = False  # skip over empty lines (implies a "skipnl")

        self._flag_display: bool = False
        self._flag_extend: bool = False
        self._flag_fold: bool = False
        self._flag_concealends: bool = False
        self._flag_excludenl: bool = False  # match/region

    def validate(self) -> bool:
        """ Validate the VimscriptStmtNode """
        valid = True
        if vimscript_file is not None:
            if isinstance(vimscript_file, List):
                if len(vimscript_file):
                    if vimscript_file[0] == {self}:
                        if self._flag_contained:
                            print('W: ._contained cannot be set in first Vimscript statement.')
                            valid = False

        if not (self._flag_region | self._flag_match | self._flag_keyword):
            if self._flag_skipempty:
                print('W: ._flag_skipempty cannot be used with cluster')
                valid = False
            if self._flag_skipnl:
                print('W: ._flag_skipnl cannot be used with cluster')
                valid = False
            if self._flag_skipwhite:
                print('W: ._flag_skipwhite cannot be used with cluster')
                valid = False
            if self._item is not None:
                print('W: ._item is supposed to be `None`.')
                valid = False

        if not self._flag_region:
            if self._flag_oneline:
                print('W: ._flag_oneline inadvertently set to True')
                valid = False
            if isinstance(self._region_skip, str):
                print('W: ._flag_region_skip inadvertently not None.')
                valid = False
            if self._match_group is not None:
                print('W: ._match_group inadvertently not set to None.')
                valid = False

        if not (self._flag_cluster | self._flag_region | self._flag_match):
            if self._contains is not None:
                print('W: ._contains inadverentaly set to not None')
                valid = False

        if self._flag_match | self._flag_region:
            pass
        else:
            if self._flag_excludenl is True:
                print('W: ._flag_excludenl inadvertently set to True')
                valid = False
            if self._flag_fold is True:
                print('W: ._flag_fold inadvertently to False')
                valid = False
            if self._flag_display is True:
                print('W: ._flag_display inadvertently to False')
                valid = False
            if self._flag_extend is True:
                print('W: ._flag_extend inadvertently to False')
                valid = False
            if self._flag_concealends is True:
                print('W: ._flag_concealends inadvertently to False')
                valid = False

        if self._flag_cluster:
            if self._flag_containedin:
                print('W: ._flag_containedin cannot be used with cluster')
                valid = False
            if self._flag_transparent:
                print('W: ._flag_transparent cannot be used with cluster')
                valid = False
            if self._flag_skipempty:
                print('W: ._flag_skipempty cannot be used with cluster')
                valid = False
            if self._flag_skipnl:
                print('W: ._flag_skipnl cannot be used with cluster')
                valid = False
            if self._flag_skipwhite:
                print('W: ._flag_skipwhite cannot be used with cluster')
                valid = False
            if self._flag_contained:
                print('W: ._flag_contained inadvertently True')
                valid = False
            if self._flag_conceal:
                print('W: ._flag_conceal inadvertently set to True')
                valid = False
            if self._flag_cchar:
                print('W: ._flag_cchar inadvertently True')
                valid = False
        else:
            if not self._flag_conceal:
                if self._flag_cchar:
                    print('W: ._flag_cchar inadvertently True')
                    valid = False
        return valid

    @property
    def is_group(self) -> bool:
        """ is this Vim node a Vim _flag_groupname? """
        if self._flag_cluster:
            print('is_cluster: errant ._flag_cluster bit set')
        return self._flag_region | self._flag_match | self._flag_keyword

    @property
    def is_cluster(self) -> bool:
        """ is this Vim node a Vim Cluster? """
        if self._flag_region | self._flag_match | self._flag_keyword:
            print('is_cluster: errant bit(s) set')
        return self._flag_cluster

    @property
    def is_match(self) -> bool:
        """ is this Vim node a Vimscript 'syntax match'? """
        if self._flag_region | self._flag_cluster | self._flag_keyword:
            print('is_cluster: errant bit(s) set')
        return self._flag_match

    @property
    def is_region(self) -> bool:
        """ is this Vim node a Vimscript 'syntax region'? """
        if self._flag_match | self._flag_cluster | self._flag_keyword:
            print('is_cluster: errant bit(s) set')
        return self._flag_region

    @property
    def is_keyword(self) -> bool:
        """ is this Vim node a Vimscript 'syntax keyword'? """
        if self._flag_match | self._flag_cluster | self._flag_region:
            print('is_cluster: errant bit(s) set')
        return self._flag_keyword

    def set_cluster_flag(self) -> None:
        """ Set this Vim node to clustername (and not _flag_groupname) """
        if self._flag_region:
            print(f'set_cluster_flag: {self._groupname} was '
                  'previously set to _flag_region attribute')
        if self._flag_match:
            print(f'set_cluster_flag: {self._groupname} was '
                  'previously set to _flag_match attribute')
        self._flag_cluster = True
        self._flag_region = False
        self._flag_match = False

    def clear_cluster_flag(self) -> None:
        """ Clear this Vim node of any cluster (it is a plain groupname) """
        if self._flag_cluster:
            print(f'clear_cluster_flag: {self._groupname} was '
                  'previously set to _flag_cluster attribute')
        self._flag_cluster = False

    def set_region_flag(self) -> None:
        """ Set this Vim node to clustername (and not _flag_groupname) """
        if self._flag_cluster:
            print(f'set_region_flag: {self._groupname} was '
                  'previously set to _flag_cluster attribute')
        if self._flag_match:
            print(f'set_region_flag: {self._groupname} was '
                  'previously set to _flag_match attribute')
        self._flag_region = True
        self._flag_cluster = False
        self._flag_match = False

    def clear_region_flag(self) -> None:
        """ Clear this Vim node of any region (it is something else) """
        if self._flag_region:
            print(f'clear_region_flag: {self._groupname} was '
                  'previously set to _flag_region attribute')
        self._flag_region = False

    def set_match_flag(self) -> None:
        """ Set this Vim node to clustername (and not _flag_groupname) """
        if self._flag_cluster:
            print(f'set_match_flag: {self._groupname} was '
                  'previously set to _flag_cluster attribute')
        if self._flag_region:
            print(f'set_match_flag: {self._groupname} was '
                  'previously set to _flag_region attribute')
        self._flag_match = True
        self._flag_cluster = False
        self._flag_region = False

    def clear_match_flag(self) -> None:
        """ Clear this Vim node of any match (it is something else) """
        if self._flag_match:
            print(f'clear_match_flag: {self._groupname} was '
                  'previously set to _flag_match attribute')
        self._flag_match = False

    def get_groupname(self) -> str:
        """ return a _item """
        return self._groupname

    def set_groupname(self, arg_value: str) -> None:
        """ set a _item """
        self._groupname = arg_value

    def add_to_stmt_list(self) -> int:
        """ Insert node at end of list array """
        global total_viml_statements
        vimscript_file.append({self})
        total_viml_statements = total_viml_statements + 1
        return total_viml_statements


def vimscript_delete() -> None:
    """ delete the list of VimL statements """
    global total_viml_statements
    global vimscript_file
    total_viml_statements = 0
    vimscript_file = []
