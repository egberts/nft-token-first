Conceptual Design

VimL/vimscript
====

Reserved words
-----

Reserved any-case words that cannot be used in `groupname` nor `cluster`name:
* `NONE`
* `ALL`
* `ALLBUT`
* `TOP`
* `CONTAINS`
* `CONTAINED`


vimscript output
----
```console
match
region
keyword
cluster
```

vim nodes - common
----

```python
import regex

label: str
value: (str | regex.Regex | None)
flag_conceal: bool
# `cchar` only used with `conceal`
flag_cchar: bool
flag_contained: bool  # not recognized at top-level
flag_containedin: bool
nextgroup: dict[] of str
flag_transparent: bool

# skip[white|nl|empty] only used with _flag_groupname
flag_skipwhite: bool  # skip over space and tab characters
flag_skipnl: bool  # skip over the end of a line
flag_skipempty: bool  # skip over empty lines (implies a "skipnl")
```

vim nodes - cluster
----
```
is_viml_cluster: bool
# if is_viml_[cluster|match|region] == True
contains: dict[4000] of object
```

vim nodes - groupname
----
```
# max sizeof groupname is 200
is_viml_groupname: bool
# if is_viml_groupname == True
nextgroups: dict[4000] of object
```

vim nodes - region
----
```
is_viml_region: bool
end: (str | regex.Regex)
skip: (str | regex.Regex | None)
flag_oneline: bool  # good for quoted strings
if is_viml_region == True
    start: (str | regex.Regex)
matchgroup: (str | regex.Regex)
is_viml_grouphere: bool
is_viml_groupthere: bool
flag_concealends: bool

```

`syntax keyword` has only common options
`#` max sizeof keyword is 80

vim nodes - match
----
```python
is_viml_keyword: bool
is_viml_match: bool

```

vim nodes - Both region and match
---
```python
# if is_viml_[cluster|match|region] == True
contains: dict[4000] of object
flag_fold: bool
flag_display: bool
flag_extend: bool
flag_keepend: bool  # Don't allow contained match to go past a match 
                    # with the end pattern. See syn-keepend.
```