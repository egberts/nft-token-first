""" Maintain a list of reserved words used within VimL/vimscript """

viml_groupname_reserved_words = [
 'NONE',
 'ALL',
 'ALLBUT',
 'TOP',
 'CONTAINS',
 'CONTAINED',
]


def is_viml_groupname_reserved_word(given_word: str) -> bool:
    """ not a reserved word for a _flag_groupname """
    for this_reserved_word in viml_groupname_reserved_words:
        if this_reserved_word.lower() == given_word.lower():
            return True
    return False
