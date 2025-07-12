How to recreate the `nftables.ebnf` file:

Github checkout the nftables repository
* Change working directory to `nftables/src` repo subdirectory
* Edit `parser_bison.y` file
* Cut-and-paste entire `parser_bison.y` file from editor buffer

Visit https://www.bottlecaps.de/ebnf-convert/
* Paste into 'Input Grammar' textbox
* Press 'Convert' button (default is EBNF output)
* Go down to W3C-style Grammar text box.
* Cut-and-paste the entire textbox.

Create and edit a new `nftables.ebnf` file.
* Paste entire buffer into `nftables.ebnf` file
* Optionally insert all your 'SYM_REGEX' defines after the (first) 'input' statement.

Edit `nftables.ebnf` file to do following:

* join continuation lines together until next `::=`.