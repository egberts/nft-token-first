# Title: VimL Syntax statements
""" Supports for VimL Syntax statements """

# Futures
from __future__ import unicode_literals
from __future__ import print_function

# Generic/Built-in
# import re

# Other Libs
# import youtube_dl
# import pandas as pd

# Owned
# from nostalgia_util import log_utils
# from nostalgia_util import settings_util
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

    @staticmethod
    def next_group(next_group_name: str) -> None:
        """ used by cluster/region/match/keyword """
        print(f'\\ nextgroup={next_group_name}', end='\n')

    @staticmethod
    def contains(contain_name: str) -> None:
        """ used by cluster/region/match/keyword """
        print(f'\\ contains={contain_name}', end='\n')

    @staticmethod
    def cluster(cluster_name: str):
        """
        If in-sequence AND operator, then collect
        """
        # No highlighter for syntax cluster statements
        print(f"syntax cluster {cluster_name}", end='\n')

    @staticmethod
    def start_region(pattern: str):
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        print(f' start=\'{pattern}\'', end='')

    @staticmethod
    def end_region(pattern: str):
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        print(f' start=\'{pattern}\'', end='\n')

    @staticmethod
    def region(region_name: str):
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        print(f'hi link {region_name} Delimiter', end='\n')
        print(f'syntax region {region_name}', end='')

    def region_start_end(
            self,
            region_name: str,
            start_pattern: str,
            end_pattern: str
            ):
        """
        If in-sequence (element (group (:Text, then syntax region
        """
        self.region(region_name)
        self.start_region(start_pattern)
        self.end_region(end_pattern)

    @staticmethod
    def match(match_name: str, pattern: str):
        """
        If SYM_REGEX literal have been encountered
        """
        print(f'hi link {match_name} String', end='\n')
        print(f'syntax match {match_name} "{pattern}"', end='')

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
