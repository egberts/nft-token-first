
This is about the Netfilter `nft` CLI terminal app.

Given a token, list all the next valid tokens.

For example:

    'input' would produce:
        'include'
        'undefine'
        'error'
        'define'
        'redefine'
        '\n'
        ';'
        'add'
        'table'
        'chain'
        'rule'
        <identifier>
        'last'
        'ip'
        'ip6'
        'inet'
        'netdev'
        'bridge'
        'arp'
        'accept'
        'drop'
        'continue'
        'jump'
        'goto'
        'return'
        'limit'
        'secmark'
        'synproxy'
        'replace'
        'create'
        'insert'
        'delete'
        'get'
        'list'
        'reset'
        'flush'
        'rename'
        'import'
        'export'
        'monitor'
        'describe'
        'destroy'

dhcparser\_nexus/dhparse-working.py is that starting Python point.

Changing the variable 'vim\_syntax\_group\_name\_target' gets you your different objective.

## WHY ##

I needed to study autocompletion of Netfilter 'nft' CLI tool, which is not much (at the moment).


## HOW ##

In Netfilter NFT CLI parse table, there are over 1,400 edge-state transitions.  It makes zero sense to code that up manually.

I leveraged Bison tool into outputting a rudimentary EBNF (Extended Backus-Naur Form) syntax of .

## MORE DEETS ##  

For the first-stage, I leveraged [DHParser](https://dhparser.readthedocs.io/en/latest/), a [PEG parser]({filename parsing-in-python-compendium.md}) to read a parser file.

Using DHParser, I used a EBNF syntax file that enables reading of EBNF file (a file that describes EBNF, ... in EBNF).

Then I shoehorned Netfilter NFT CLI EBNF ... AGAIN ... thru the Python DHParser("EBNF") but this time using Netfilter NFT EBNF (supplied by Bison and bison-parse.c source file).

Then I wrote a leaf-tree navigator to look for only the first following token(s) (and not to go down any deeper).


## OTHERS ##

dhparser\_project subdirectory and its development files were made by executing:

    ~/work/github/DHParser/scripts/dhparser.py
    # and selecting option 1 to create a project and entering in `dhparser_project` 
