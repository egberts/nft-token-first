# Title: VimL Syntax statements
""" Supports for VimL Syntax statements """

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


class Output:
    """ outputs various vim syntax commands """

    # hint types
    prefix_info: str

    def __init__(self, prefix_label):
        self.prefix_info = prefix_label

    @staticmethod
    def contained() -> None:
        """
        If a close-loop (not top-level), then it's contained
        :rtype: None
        """
        print(f'\\ contained', end='\n')

    @staticmethod
    def skipwhite() -> None:
        """
        If loosely a keyword boundary stepper, then 'skipwhite'
        If matching literally on a per-character basis, then do not use this
        :rtype: None
        """
        print(f'\\ skipwhite', end='\n')

    @staticmethod
    def skipnl() -> None:
        """
        If performing multi-line, then skipnl
        If restraining matching to within a single line, do not use skipnl
        :rtype: None
        """
        print(f'\\ skipnl', end='\n')

    def next_group(self, next_group_name: str) -> None:
        """ used by cluster/region/match/keyword """
        groupname = self.prefix_info + next_group_name
        print(f'\\ nextgroup={groupname}', end='\n')

    def contains(self, contain_name: str) -> None:
        """ used by cluster/region/match/keyword """
        contain_info = self.prefix_info + contain_name
        print(f'\\ contains={contain_info}', end='\n')

    def cluster(self, cluster_name: str) -> None:
        """
        If in-sequence AND operator, then collect
        """
        cluster_info = self.prefix_info + cluster_name
        # No highlighter for syntax cluster statements
        print(f"syntax cluster {cluster_info}", end='\n')

    @staticmethod
    def start_region(pattern: str) -> None:
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        if not isinstance(pattern, str):
            print('vim_syntax.start_region: pattern argument is not a str type')
            sys.exit(-9)
        print(f' start=\'{pattern}\'', end='')

    @staticmethod
    def end_region(pattern: str) -> None:
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        if not isinstance(pattern, str):
            print('vim_syntax.end_region: pattern argument is not a str type')
            sys.exit(-9)
        print(f' start=\'{pattern}\'', end='\n')

    def region(self, region_name: str) -> None:
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        if not isinstance(region_name, str):
            print('vim_syntax.region: region_name argument is not a str type')
            sys.exit(-9)
        region_info = self.prefix_info + region_name
        print(f'hi link {region_info} Delimiter', end='\n')
        print(f'syntax region {region_info}', end='')

    def region_start_end(
            self,
            region_name: str,
            start_pattern: str,
            end_pattern: str
    ) -> None:
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        if not isinstance(region_name, str):
            print('vim_syntax.region_start_end: region_name argument is not a str type')
            sys.exit(-9)
        if not isinstance(start_pattern, str):
            print('vim_syntax.region_start_end: start_pattern argument is not a str type')
            sys.exit(-9)
        if not isinstance(end_pattern, str):
            print('vim_syntax.region_start_end: end_pattern argument is not a str type')
            sys.exit(-9)
        self.region(region_name)
        self.start_region(start_pattern)
        self.end_region(end_pattern)

    def match(self, match_name: str, pattern: str) -> None:
        """
        If SYM_REGEX literal have been encountered
        """
        if not isinstance(match_name, str):
            print('vim_syntax.match: match_name is not a str type')
            sys.exit(-9)
        if not isinstance(pattern, str):
            print('vim_syntax.match: match_name is not a str type')
            sys.exit(-9)

        match_label = self.prefix_info + match_name
        print(f'hi link {match_label} String', end='\n')
        print(f'syntax match {match_label} "{pattern}"', end='\n')

    @staticmethod
    def end_match() -> None:
        """
        After all `syntax match` options have been specified, call this
        """
        print(end='\n')


class Group:
    """ combination of output generators """

    def g1(self):
        """ template """
        return
