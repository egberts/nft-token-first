
This is about the Netfilter `nft` CLI terminal app.

Given a token, list all the next valid tokens at the NFT command prompt, given a certain point in the syntax tree.

For example, Bison `input` symbol would produce the following token:


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

I leveraged Bison tool into reading Netfilter nftables' and outputting a rudimentary EBNF (Extended Backus-Naur Form) syntax.

And used a two-stage parser.


## MORE DEETS ##  

I designed a two-stage parser:
   1. how to read EBNF (in DHParse-format)
   2. how to read Netfilter `nft` CLI (in EBNF-format)

For the first-stage, I leveraged [DHParser](https://dhparser.readthedocs.io/en/latest/), a [PEG parser](https://egbert.net/blog/articles/parsing-in-python-compendium.html) to read a parser file.

I used a [EBNF syntax](https://github.com/egberts/nft-token-first/blob/master/dhcparser_nexus/ebnf-flexible.dhparse) file that enables reading of any EBNF file (a file that describes EBNF, ... in EBNF): That file format is for DHParse-only.  

For the second-stage, I shoehorned Netfilter NFT CLI EBNF ... AGAIN ... thru the Python DHParser("EBNF") but this time using Netfilter NFT EBNF (supplied by Bison and [bison\_parse.y](https://git.netfilter.org/nftables/tree/src/parser_bison.y)  source file).

Then I wrote a leaf-tree navigator to look for only the first following token(s) (and not to go down any deeper).


## OTHERS ##

dhparser\_project subdirectory and its development files were made by executing:

    ~/work/github/DHParser/scripts/dhparser.py
    # and selecting option 1 to create a project and entering in `dhparser_project` 
