#!/usr/bin/env python3

#######################################################################
#
# SYMBOLS SECTION - Can be edited. Changes will be preserved.
#
#######################################################################


import collections
from functools import partial
import os
import sys
from typing import Tuple, List, Union, Any, Optional, Callable, cast

try:
    import regex as re
except ImportError:
    import re

try:
    scriptdir = os.path.dirname(os.path.realpath(__file__))
except NameError:
    scriptdir = ''
if scriptdir and scriptdir not in sys.path: sys.path.append(scriptdir)

try:
    from DHParser import versionnumber
except (ImportError, ModuleNotFoundError):
    i = scriptdir.rfind("/DHParser/")
    if i >= 0:
        dhparserdir = scriptdir[:i + 10]  # 10 = len("/DHParser/")
        if dhparserdir not in sys.path:  sys.path.insert(0, dhparserdir)

from DHParser.compile import Compiler, compile_source, Junction, full_compile
from DHParser.configuration import set_config_value, add_config_values, get_config_value, \
    access_thread_locals, access_presets, finalize_presets, set_preset_value, \
    get_preset_value, NEVER_MATCH_PATTERN
from DHParser import dsl
from DHParser.dsl import recompile_grammar, never_cancel
from DHParser.ebnf import grammar_changed
from DHParser.error import ErrorCode, Error, canonical_error_strings, has_errors, NOTICE, \
    WARNING, ERROR, FATAL
from DHParser.log import start_logging, suspend_logging, resume_logging
from DHParser.nodetree import Node, WHITESPACE_PTYPE, TOKEN_PTYPE, RootNode, Path, ZOMBIE_TAG
from DHParser.parse import Grammar, PreprocessorToken, Whitespace, Drop, DropFrom, AnyChar, Parser, \
    Lookbehind, Lookahead, Alternative, Pop, Text, Synonym, Counted, Interleave, INFINITE, ERR, \
    Option, NegativeLookbehind, OneOrMore, RegExp, SmartRE, Retrieve, Series, Capture, TreeReduction, \
    ZeroOrMore, Forward, NegativeLookahead, Required, CombinedParser, Custom, IgnoreCase, \
    LateBindingUnary, mixin_comment, last_value, matching_bracket, optional_last_value, \
    PARSER_PLACEHOLDER, UninitializedError
from DHParser.pipeline import end_points, full_pipeline, create_parser_junction, \
    create_preprocess_junction, create_junction, PseudoJunction 
from DHParser.preprocess import nil_preprocessor, PreprocessorFunc, PreprocessorResult, \
    gen_find_include_func, preprocess_includes, make_preprocessor, chain_preprocessors
from DHParser.stringview import StringView
from DHParser.toolkit import is_filename, load_if_file, cpu_count, RX_NEVER_MATCH, \
    ThreadLocalSingletonFactory, expand_table
from DHParser.trace import set_tracer, resume_notices_on, trace_history
from DHParser.transform import is_empty, remove_if, TransformationDict, TransformerFunc, \
    transformation_factory, remove_children_if, move_fringes, normalize_whitespace, \
    is_anonymous, name_matches, reduce_single_child, replace_by_single_child, replace_or_reduce, \
    remove_whitespace, replace_by_children, remove_empty, remove_tokens, flatten, all_of, \
    any_of, transformer, merge_adjacent, collapse, collapse_children_if, transform_result, \
    remove_children, remove_content, remove_brackets, change_name, remove_anonymous_tokens, \
    keep_children, is_one_of, not_one_of, content_matches, apply_if, peek, \
    remove_anonymous_empty, keep_nodes, traverse_locally, strip, lstrip, rstrip, \
    replace_content_with, forbid, assert_content, remove_infix_operator, add_error, error_on, \
    left_associative, lean_left, node_maker, has_descendant, neg, has_ancestor, insert, \
    positions_of, replace_child_names, add_attributes, delimit_children, merge_connected, \
    has_attr, has_parent, has_children, has_child, apply_unless, apply_ifelse, traverse
from DHParser import parse as parse_namespace__

import DHParser.versionnumber
if DHParser.versionnumber.__version_info__ < (1, 8, 0):
    print(f'DHParser version {DHParser.versionnumber.__version__} is lower than the DHParser '
          f'version 1.8.0, {os.path.basename(__file__)} has first been generated with. '
          f'Please install a more recent version of DHParser to avoid unexpected errors!')


#######################################################################
#
# PREPROCESSOR SECTION - Can be edited. Changes will be preserved.
#
#######################################################################



# To capture includes, replace the NEVER_MATCH_PATTERN 
# by a pattern with group "name" here, e.g. r'\input{(?P<name>.*)}'
RE_INCLUDE = NEVER_MATCH_PATTERN
RE_COMMENT = '#.*'  # THIS MUST ALWAYS BE THE SAME AS dhparser_projectGrammar.COMMENT__ !!!


def dhparser_projectTokenizer(original_text) -> Tuple[str, List[Error]]:
    # Here, a function body can be filled in that adds preprocessor tokens
    # to the source code and returns the modified source.
    return original_text, []

preprocessing: PseudoJunction = create_preprocess_junction(
    dhparser_projectTokenizer, RE_INCLUDE, RE_COMMENT)


#######################################################################
#
# PARSER SECTION - Don't edit! CHANGES WILL BE OVERWRITTEN!
#
#######################################################################

class dhparser_projectGrammar(Grammar):
    r"""Parser for a dhparser_project source file.
    """
    countable = Forward()
    element = Forward()
    expression = Forward()
    source_hash__ = "3b64cd7446fce4fb2f5a0d65c8017e7b"
    disposable__ = re.compile('(?:FOLLOW_UP$|ANY_SUFFIX$|is_mdef$|countable$|EOF$|component$|no_range$|MOD_SEP$|MOD_SYM$|pure_elem$)')
    static_analysis_pending__ = []  # type: List[bool]
    parser_initialization__ = ["upon instantiation"]
    error_messages__ = {'definition': [(re.compile(r','), 'Delimiter "," not expected in definition!\\nEither this was meant to be a directive and the directive symbol @ is missing\\nor the error is due to inconsistent use of the comma as a delimiter\\nfor the elements of a sequence.')]}
    COMMENT__ = r'(?!#x[A-Fa-f0-9])#.*(?:\n|$)|/\*(?:.|\n)*?\*/|\(\*(?:.|\n)*?\*\)'
    comment_rx__ = re.compile(COMMENT__)
    WHITESPACE__ = r'\s*'
    WSP_RE__ = mixin_comment(whitespace=WHITESPACE__, comment=COMMENT__)
    wsp__ = Whitespace(WSP_RE__)
    dwsp__ = Drop(Whitespace(WSP_RE__))
    RAISE_EXPR_WO_BRACKETS = Text("")
    HEXCODE = RegExp('(?:[A-Fa-f1-9]|0(?!x)){1,8}')
    SYM_REGEX = RegExp('(?!\\d)\\w(?:-?\\w)*')
    RE_CORE = RegExp('(?:(?<!\\\\)\\\\(?:/)|[^/])*')
    regex_heuristics = SmartRE(f'(?! +`[^`]*` +/| +´[^´]*´ +/| +\'[^\']*\' +/| +"[^"]*" +/| +\\w+ +/)([^/\\n*?+\\\\]*[*?+\\\\][^/\\n]*/|[^\\w]+/|[^ ])', '!/ +`[^`]*` +\\//|/ +´[^´]*´ +\\//|/ +\'[^\']*\' +\\//|/ +"[^"]*" +\\//|/ +\\w+ +\\// /[^\\/\\n*?+\\\\]*[*?+\\\\][^\\/\\n]*\\//|/[^\\w]+\\//|/[^ ]/')
    literal_heuristics = SmartRE(f'((?:~?\\s*"(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^"]*)*")|(?:~?\\s*\'(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^\']*)*\')|(?:~?\\s*`(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^`]*)*`)|(?:~?\\s*´(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^´]*)*´)|(?:~?\\s*/(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^/]*)*/))', '/~?\\s*"(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^"]*)*"/|/~?\\s*\'(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^\']*)*\'/|/~?\\s*`(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^`]*)*`/|/~?\\s*´(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^´]*)*´/|/~?\\s*\\/(?:[\\\\]\\]|[^\\]]|[^\\\\]\\[[^\\/]*)*\\//')
    more_than_one_blank = RegExp('[^ \\]]*[ ][^ \\]]*[ ]')
    STRICT_SYM_REGEX = RegExp('(?!\\d)\\w+')
    CH_LEADIN = Capture(SmartRE(f'(?P<:Text>0x|%x|U\\+|u\\+|\\#x|\\\\x|\\\\u|\\\\U)', '`0x`|`%x`|`U+`|`u+`|`#x`|`\\x`|`\\u`|`\\U`'), zero_length_warning=False)
    MOD_SYM = Drop(Text("->"))
    character = Series(Retrieve(CH_LEADIN), HEXCODE)
    RE_LEADOUT = Capture(Text("/"), zero_length_warning=True)
    RE_LEADIN = Capture(Alternative(Series(Text("/"), Lookahead(regex_heuristics)), Text("^/")), zero_length_warning=True)
    TIMES = Capture(Text("*"), zero_length_warning=False)
    RNG_DELIM = Capture(Text(","), zero_length_warning=False)
    BRACE_SIGN = Capture(SmartRE(f'(?P<:Text>\\{{|\\()', '`{`|`(`'), zero_length_warning=False)
    RNG_BRACE = Capture(Retrieve(BRACE_SIGN), zero_length_warning=True)
    ENDL = Capture(SmartRE(f'(?P<:Text>;|)', '`;`|``'), zero_length_warning=False)
    AND = Capture(SmartRE(f'(?P<:Text>,|)', '`,`|``'), zero_length_warning=False)
    OR = Capture(Alternative(Text("|"), Series(Text("/"), NegativeLookahead(regex_heuristics))), zero_length_warning=True)
    _DEF = SmartRE(f'(?P<:Text>=|:=|::=|<\\-)|(:\\n)|(?P<:Text>:\\ )', '`=`|`:=`|`::=`|`<-`|/:\\n/|`: `')
    DEF = Capture(Synonym(_DEF), zero_length_warning=False)
    EOF = Drop(Series(SmartRE(f'(?!.)', '!/./'), Option(Pop(ENDL, match_func=optional_last_value)), Option(Pop(DEF, match_func=optional_last_value)), Option(Pop(OR, match_func=optional_last_value)), Option(Pop(AND, match_func=optional_last_value)), Option(Pop(RNG_DELIM, match_func=optional_last_value)), Option(Pop(BRACE_SIGN, match_func=optional_last_value)), Option(Pop(CH_LEADIN, match_func=optional_last_value)), Option(Pop(TIMES, match_func=optional_last_value)), Option(Pop(RE_LEADIN, match_func=optional_last_value)), Option(Pop(RE_LEADOUT, match_func=optional_last_value))))
    name = Synonym(SYM_REGEX)
    placeholder = Series(Series(Text("$"), dwsp__), name, NegativeLookahead(Text("(")), dwsp__)
    multiplier = SmartRE(f'([1-9]\\d*)(?:{WSP_RE__})', '/[1-9]\\d*/ ~')
    whitespace = SmartRE(f'(~)(?:{WSP_RE__})', '/~/ ~')
    any_char = Series(Text("."), dwsp__)
    free_char = SmartRE(f'([^\\n\\[\\]\\\\]|\\\\[nrtfv`´\'"(){{}}\\[\\]/\\\\])', '/[^\\n\\[\\]\\\\]/|/\\\\[nrtfv`´\'"(){}\\[\\]\\/\\\\]/')
    range_desc = Series(Alternative(character, free_char), Option(Series(Option(Text("-")), Alternative(character, free_char))))
    char_range_heuristics = Series(NegativeLookahead(Alternative(RegExp('[\\n]'), more_than_one_blank, Series(dwsp__, literal_heuristics), Series(dwsp__, Option(SmartRE(f'(?P<:Text>::|:\\?|:)', '`::`|`:?`|`:`')), STRICT_SYM_REGEX, RegExp('\\s*\\]')))), Lookahead(Series(OneOrMore(range_desc), Text("]"))))
    range_chain = Series(Text("["), Option(Text("^")), OneOrMore(range_desc), Text("]"))
    char_ranges = Series(RE_LEADIN, range_chain, ZeroOrMore(Series(Text("|"), range_chain)), RE_LEADOUT, dwsp__)
    char_range = Series(Text("["), Lookahead(char_range_heuristics), Option(Text("^")), OneOrMore(range_desc), Series(Text("]"), dwsp__))
    regexp = Series(Retrieve(RE_LEADIN), RE_CORE, Retrieve(RE_LEADOUT), dwsp__)
    plaintext = SmartRE(f'(?:(`(?:(?<!\\\\)(?:\\\\\\\\)*\\\\`|[^`])*?`)(?:{WSP_RE__}))|(?:(´(?:(?<!\\\\)(?:\\\\\\\\)*\\\\´|[^´])*?´)(?:{WSP_RE__}))', '/`(?:(?<!\\\\)(?:\\\\\\\\)*\\\\`|[^`])*?`/ ~|/´(?:(?<!\\\\)(?:\\\\\\\\)*\\\\´|[^´])*?´/ ~')
    literal = SmartRE(f'(?:("(?:(?<!\\\\)(?:\\\\\\\\)*\\\\"|[^"])*?")(?:{WSP_RE__}))|(?:(\'(?:(?<!\\\\)(?:\\\\\\\\)*\\\\\'|[^\'])*?\')(?:{WSP_RE__}))|(?:(’(?:(?<!\\\\)(?:\\\\\\\\)*\\\\’|[^’])*?’)(?:{WSP_RE__}))', '/"(?:(?<!\\\\)(?:\\\\\\\\)*\\\\"|[^"])*?"/ ~|/\'(?:(?<!\\\\)(?:\\\\\\\\)*\\\\\'|[^\'])*?\'/ ~|/’(?:(?<!\\\\)(?:\\\\\\\\)*\\\\’|[^’])*?’/ ~')
    symbol = Series(SYM_REGEX, dwsp__)
    argument = Alternative(literal, Series(name, dwsp__))
    parser = Series(Series(Text("@"), dwsp__), name, Series(Text("("), dwsp__), Option(argument), Series(Text(")"), dwsp__))
    no_range = Drop(Alternative(NegativeLookahead(multiplier), Series(Lookahead(multiplier), Retrieve(TIMES))))
    macro = Series(Series(Text("$"), dwsp__), name, Series(Text("("), dwsp__), no_range, expression, ZeroOrMore(Series(Series(Text(","), dwsp__), no_range, expression)), Series(Text(")"), dwsp__))
    range = Series(RNG_BRACE, dwsp__, multiplier, Option(Series(Retrieve(RNG_DELIM), dwsp__, multiplier)), Pop(RNG_BRACE, match_func=matching_bracket), dwsp__)
    counted = Alternative(Series(countable, range), Series(countable, Retrieve(TIMES), dwsp__, multiplier), Series(multiplier, Retrieve(TIMES), dwsp__, countable, mandatory=3))
    option = Alternative(Series(NegativeLookahead(char_range), Series(Text("["), dwsp__), expression, Series(Text("]"), dwsp__), mandatory=2), Series(element, Series(Text("?"), dwsp__)))
    repetition = Alternative(Series(Series(Text("{"), dwsp__), no_range, expression, Series(Text("}"), dwsp__), mandatory=2), Series(element, Series(Text("*"), dwsp__), no_range))
    oneormore = Alternative(Series(Series(Text("{"), dwsp__), no_range, expression, Series(Text("}+"), dwsp__)), Series(element, Series(Text("+"), dwsp__)))
    group = Series(Series(Text("("), dwsp__), no_range, expression, Series(Text(")"), dwsp__), mandatory=2)
    retrieveop = SmartRE(f'(?P<:Text>::)(?:{WSP_RE__})|(?P<:Text>:\\?)(?:{WSP_RE__})|(?P<:Text>:)(?:{WSP_RE__})', '"::"|":?"|":"')
    flowmarker = SmartRE(f'(?P<:Text>!)(?:{WSP_RE__})|(?P<:Text>\\&)(?:{WSP_RE__})|(?P<:Text><\\-!)(?:{WSP_RE__})|(?P<:Text><\\-\\&)(?:{WSP_RE__})', '"!"|"&"|"<-!"|"<-&"')
    ANY_SUFFIX = RegExp('[?*+]')
    is_mdef = Series(Series(Text("$"), dwsp__), name, Option(Series(Series(Text("("), dwsp__), placeholder, ZeroOrMore(Series(Series(Text(","), dwsp__), placeholder)), Series(Text(")"), dwsp__))), dwsp__, Retrieve(DEF))
    pure_elem = Series(element, NegativeLookahead(ANY_SUFFIX), mandatory=1)
    MOD_SEP = RegExp(' *: *')
    hide = SmartRE(f'(?P<:Text>HIDE)(?:{WSP_RE__})|(?P<:Text>Hide)(?:{WSP_RE__})|(?P<:Text>hide)(?:{WSP_RE__})|(?P<:Text>DISPOSE)(?:{WSP_RE__})|(?P<:Text>Dispose)(?:{WSP_RE__})|(?P<:Text>dispose)(?:{WSP_RE__})', '"HIDE"|"Hide"|"hide"|"DISPOSE"|"Dispose"|"dispose"')
    drop = SmartRE(f'(?P<:Text>DROP)(?:{WSP_RE__})|(?P<:Text>Drop)(?:{WSP_RE__})|(?P<:Text>drop)(?:{WSP_RE__})|(?P<:Text>SKIP)(?:{WSP_RE__})|(?P<:Text>Skip)(?:{WSP_RE__})|(?P<:Text>skip)(?:{WSP_RE__})', '"DROP"|"Drop"|"drop"|"SKIP"|"Skip"|"skip"')
    part = Series(Alternative(oneormore, pure_elem), Option(Series(MOD_SYM, dwsp__, drop)))
    term = Series(Alternative(oneormore, counted, repetition, option, pure_elem), Option(Series(MOD_SYM, dwsp__, drop)))
    difference = Series(term, Option(Series(NegativeLookahead(Text("->")), Series(Text("-"), dwsp__), part, mandatory=2)))
    lookaround = Series(flowmarker, part, mandatory=1)
    interleave = Series(difference, ZeroOrMore(Series(Series(Text("°"), dwsp__), Option(Series(Text("§"), dwsp__)), difference)))
    sequence = Series(Option(Series(Text("§"), dwsp__)), Alternative(interleave, lookaround), ZeroOrMore(Series(NegativeLookahead(Text("@")), NegativeLookahead(Series(symbol, Retrieve(DEF))), Retrieve(AND), dwsp__, Option(Series(Text("§"), dwsp__)), Alternative(interleave, lookaround))))
    modifier = Series(Alternative(drop, Option(hide)), MOD_SEP)
    FOLLOW_UP = Alternative(Text("@"), Text("$"), modifier, symbol, EOF)
    is_def = Alternative(Series(Option(Series(MOD_SEP, symbol)), Retrieve(DEF)), Series(MOD_SEP, is_mdef))
    macrobody = Synonym(expression)
    definition = Series(Option(modifier), symbol, Retrieve(DEF), dwsp__, Option(Series(Retrieve(OR), dwsp__)), expression, Option(Series(MOD_SYM, dwsp__, hide)), Retrieve(ENDL), dwsp__, Lookahead(FOLLOW_UP), mandatory=2)
    procedure = Series(SYM_REGEX, Series(Text("()"), dwsp__))
    literals = OneOrMore(literal)
    macrodef = Series(Option(modifier), Series(Text("$"), dwsp__), name, dwsp__, Option(Series(Series(Text("("), dwsp__), placeholder, ZeroOrMore(Series(Series(Text(","), dwsp__), placeholder)), Series(Text(")"), dwsp__), mandatory=1)), Retrieve(DEF), dwsp__, Option(Series(OR, dwsp__)), macrobody, Option(Series(MOD_SYM, dwsp__, hide)), Retrieve(ENDL), dwsp__, Lookahead(FOLLOW_UP))
    _is_def = Alternative(Series(Option(Series(MOD_SEP, symbol)), _DEF), Series(MOD_SEP, is_mdef))
    component = Alternative(regexp, literals, procedure, Series(symbol, NegativeLookahead(_DEF), NegativeLookahead(_is_def)), Series(Lookahead(Text("$")), NegativeLookahead(is_mdef), placeholder, NegativeLookahead(is_def), mandatory=2), Series(Series(Text("("), dwsp__), expression, Series(Text(")"), dwsp__)), Series(RAISE_EXPR_WO_BRACKETS, expression))
    directive = Series(Series(Text("@"), dwsp__), symbol, Series(Text("="), dwsp__), component, ZeroOrMore(Series(Series(Text(","), dwsp__), component)), Lookahead(FOLLOW_UP), mandatory=1)
    element.set(Alternative(Series(Option(retrieveop), symbol, NegativeLookahead(is_def)), literal, plaintext, char_ranges, regexp, char_range, Series(character, dwsp__), any_char, whitespace, group, Series(macro, NegativeLookahead(is_def)), Series(placeholder, NegativeLookahead(is_def)), parser))
    countable.set(Alternative(option, oneormore, element))
    expression.set(Series(sequence, ZeroOrMore(Series(Retrieve(OR), dwsp__, sequence))))
    syntax = Series(dwsp__, ZeroOrMore(Alternative(definition, directive, macrodef)), EOF)
    resume_rules__ = {'definition': [re.compile(r'\n\s*(?=@|\w+\w*\s*=)')],
                      'directive': [re.compile(r'\n\s*(?=@|\w+\w*\s*=)')]}
    root__ = syntax
        
parsing: PseudoJunction = create_parser_junction(dhparser_projectGrammar)
get_grammar = parsing.factory # for backwards compatibility, only


#######################################################################
#
# AST SECTION - Can be edited. Changes will be preserved.
#
#######################################################################

dhparser_project_AST_transformation_table = {
    # AST Transformations for the dhparser_project-grammar
    # "<": [],  # called for each node before calling its specific rules
    # "*": [],  # fallback for nodes that do not appear in this table
    # ">": [],   # called for each node after calling its specific rules
    "document": [],
    "WORD": [],
    "EOF": [],
}


# DEPRECATED, because it requires pickling the transformation-table, which rules out lambdas!
# ASTTransformation: Junction = create_junction(
#     dhparser_project_AST_transformation_table, "CST", "AST", "transtable")

def dhparser_projectTransformer() -> TransformerFunc:
    return partial(transformer, transformation_table=dhparser_project_AST_transformation_table.copy(),
                   src_stage='CST', dst_stage='AST')

ASTTransformation: Junction = Junction(
    'CST', ThreadLocalSingletonFactory(dhparser_projectTransformer), 'AST')


#######################################################################
#
# COMPILER SECTION - Can be edited. Changes will be preserved.
#
#######################################################################

class dhparser_projectCompiler(Compiler):
    """Compiler for the abstract-syntax-tree of a 
        dhparser_project source file.
    """

    def __init__(self):
        super(dhparser_projectCompiler, self).__init__()
        self.forbid_returning_None = True  # set to False if any compilation-method is allowed to return None

    def reset(self):
        super().reset()
        # initialize your variables here, not in the constructor!

    def prepare(self, root: RootNode) -> None:
        assert root.stage == "AST", f"Source stage `AST` expected, `but `{root.stage}` found."
        root.stage = "dhparser_project"
    def finalize(self, result: Any) -> Any:
        return result

    def on_document(self, node):
        return self.fallback_compiler(node)

    # def on_WORD(self, node):
    #     return node

    # def on_EOF(self, node):
    #     return node



compiling: Junction = create_junction(
    dhparser_projectCompiler, "AST", "dhparser_project")


#######################################################################
#
# END OF DHPARSER-SECTIONS
#
#######################################################################

#######################################################################
#
# Post-Processing-Stages [add one or more postprocessing stages, here]
#
#######################################################################

# class PostProcessing(Compiler):
#     ...

# # change the names of the source and destination stages. Source
# # ("dhparser_project") in this example must be the name of some earlier stage, though.
# postprocessing: Junction = create_junction(PostProcessing, "dhparser_project", "refined")
#
# DON'T FORGET TO ADD ALL POSTPROCESSING-JUNCTIONS TO THE GLOBAL
# "junctions"-set IN SECTION "Processing-Pipeline" BELOW!

#######################################################################
#
# Processing-Pipeline
#
#######################################################################

# Add your own stages to the junctions and target-lists, below
# (See DHParser.compile for a description of junctions)

# ADD YOUR OWN POST-PROCESSING-JUNCTIONS HERE:
junctions = set([ASTTransformation, compiling])

# put your targets of interest, here. A target is the name of result (or stage)
# of any transformation, compilation or postprocessing step after parsing.
# Serializations of the stages listed here will be written to disk when
# calling process_file() or batch_process() and also appear in test-reports.
targets = end_points(junctions)
# alternative: targets = set([compiling.dst])

# provide a set of those stages for which you would like to see the output
# in the test-report files, here. (AST is always included)
test_targets = set(j.dst for j in junctions)
# alternative: test_targets = targets

# add one or more serializations for those targets that are node-trees
serializations = expand_table(dict([('*', [get_config_value('default_serialization')])]))


#######################################################################
#
# Main program
#
#######################################################################

def compile_src(source: str, target: str = "dhparser_project") -> Tuple[Any, List[Error]]:
    """Compiles the source to a single target and returns the result of the compilation
    as well as a (possibly empty) list or errors or warnings that have occurred in the
    process.
    """
    full_compilation_result = full_pipeline(
        source, preprocessing.factory, parsing.factory, junctions, set([target]))
    return full_compilation_result[target]


def process_file(source: str, out_dir: str = '') -> str:
    """Compiles the source and writes the serialized results back to disk,
    unless any fatal errors have occurred. Error and Warning messages are
    written to a file with the same name as `result_filename` with an
    appended "_ERRORS.txt" or "_WARNINGS.txt" in place of the name's
    extension. Returns the name of the error-messages file or an empty
    string, if no errors or warnings occurred.
    """
    global serializations
    serializations = get_config_value('dhparser_project_serializations', serializations)
    return dsl.process_file(source, out_dir, preprocessing.factory, parsing.factory,
                            junctions, targets, serializations)


def _process_file(args: Tuple[str, str]) -> str:
    return process_file(*args)


def batch_process(file_names: List[str], out_dir: str,
                  *, submit_func: Callable = None,
                  log_func: Callable = None,
                  cancel_func: Callable = never_cancel) -> List[str]:
    """Compiles all files listed in file_names and writes the results and/or
    error messages to the directory `our_dir`. Returns a list of error
    messages files.
    """
    return dsl.batch_process(file_names, out_dir, _process_file,
        submit_func=submit_func, log_func=log_func, cancel_func=cancel_func)


def main(called_from_app=False) -> bool:
    # recompile grammar if needed
    scriptpath = os.path.abspath(__file__)
    if scriptpath.endswith('Parser.py'):
        grammar_path = scriptpath.replace('Parser.py', '.ebnf')
    else:
        grammar_path = os.path.splitext(scriptpath)[0] + '.ebnf'
    parser_update = False

    def notify():
        nonlocal parser_update
        parser_update = True
        print('recompiling ' + grammar_path)

    if os.path.exists(grammar_path) and os.path.isfile(grammar_path):
        if not recompile_grammar(grammar_path, scriptpath, force=False, notify=notify):
            error_file = os.path.basename(__file__)\
                .replace('Parser.py', '_ebnf_MESSAGES.txt')
            with open(error_file, 'r', encoding="utf-8") as f:
                print(f.read())
            sys.exit(1)
        elif parser_update:
            if '--dontrerun' in sys.argv:
                print(os.path.basename(__file__) + ' has changed. '
                      'Please run again in order to apply updated compiler')
                sys.exit(0)
            else:
                import platform, subprocess
                call = ['python', __file__, '--dontrerun'] + sys.argv[1:]
                result = subprocess.run(call, capture_output=True)
                print(result.stdout.decode('utf-8'))
                sys.exit(result.returncode)
    else:
        print('Could not check whether grammar requires recompiling, '
              'because grammar was not found at: ' + grammar_path)

    from argparse import ArgumentParser
    parser = ArgumentParser(description="Parses a dhparser_project-file and shows its syntax-tree.")
    parser.add_argument('files', nargs='*' if called_from_app else '+')
    parser.add_argument('-d', '--debug', action='store_const', const='debug',
                        help='Store debug information in LOGS subdirectory')
    parser.add_argument('-o', '--out', nargs=1, default=['out'],
                        help='Output directory for batch processing')
    parser.add_argument('-v', '--verbose', action='store_const', const='verbose',
                        help='Verbose output')
    parser.add_argument('-f', '--force', action='store_const', const='force',
                        help='Write output file even if errors have occurred')
    parser.add_argument('--singlethread', action='store_const', const='singlethread',
                        help='Run batch jobs in a single thread (recommended only for debugging)')
    parser.add_argument('--dontrerun', action='store_const', const='dontrerun',
                        help='Do not automatically run again if the grammar has been recompiled.')
    parser.add_argument('-s', '--serialize', nargs='+', default=[])

    args = parser.parse_args()
    file_names, out, log_dir = args.files, args.out[0], ''

    if args.serialize:
        serializations['*'] = args.serialize
        access_presets()
        set_preset_value('dhparser_project_serializations', serializations, allow_new_key=True)
        finalize_presets()

    if args.debug is not None:
        log_dir = 'LOGS'
        access_presets()
        set_preset_value('history_tracking', True)
        set_preset_value('resume_notices', True)
        set_preset_value('log_syntax_trees', frozenset(['CST', 'AST']))  # don't use a set literal, here!
        finalize_presets()
    start_logging(log_dir)

    if args.singlethread:
        set_config_value('batch_processing_parallelization', False)

    def echo(message: str):
        if args.verbose:
            print(message)

    if called_from_app and not file_names:  return False

    batch_processing = True
    if len(file_names) == 1:
        if os.path.isdir(file_names[0]):
            dir_name = file_names[0]
            echo('Processing all files in directory: ' + dir_name)
            file_names = [os.path.join(dir_name, fn) for fn in os.listdir(dir_name)
                          if os.path.isfile(os.path.join(dir_name, fn))]
        elif not ('-o' in sys.argv or '--out' in sys.argv):
            batch_processing = False

    if batch_processing:
        if not os.path.exists(out):
            os.mkdir(out)
        elif not os.path.isdir(out):
            print('Output directory "%s" exists and is not a directory!' % out)
            sys.exit(1)
        error_files = batch_process(file_names, out, log_func=print if args.verbose else None)
        if error_files:
            category = "ERRORS" if any(f.endswith('_ERRORS.txt') for f in error_files) \
                else "warnings"
            print("There have been %s! Please check files:" % category)
            print('\n'.join(error_files))
            if category == "ERRORS":
                sys.exit(1)
    else:
        result, errors = compile_src(file_names[0])

        if not errors or (not has_errors(errors, ERROR)) \
                or (not has_errors(errors, FATAL) and args.force):
            print(result.serialize(serializations['*'][0])
                  if isinstance(result, Node) else result)
            if errors:  print('\n---')

        for err_str in canonical_error_strings(errors):
            print(err_str)
        if has_errors(errors, ERROR):  sys.exit(1)

    return True


if __name__ == "__main__":
    main()
