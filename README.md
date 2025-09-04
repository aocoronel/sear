# Interact with Kagi Bangs in the CLI

`sear` allows you to use the powerful [Kagi Bangs](https://github.com/kagisearch/bangs) from the CLI. Check the official bang repository to know more about it.

Essentially, it allows you configure a `json` file to predefine a search query, and quickly replace the query template and open in a browser.

```bash
python sear pm Leishmaniosis
# Output
# https://pubmed.ncbi.nlm.nih.gov/?term=Leishmaniosis&filter=simsearch2.ffrft
```

## Features

- Open links in a browser
- Find bangs by any JSON key

## Usage

```
usage:
  sear.py COMMAND|BANG QUERY [FLAGS]

commands:
  list             Lists all bangs
  inspect          Output json file
  find [BANG_NAME] Find a bang with a specified name

positional arguments:
  args                  Command or bang search

options:
  -h, --help            show this help message and exit
  -c, --config CONFIG   Path to bangs JSON file
  -b, --browser         Open URL in browser
  -f, --findkey FINDKEY
                        Key to search for in 'find' (e.g., s, t, u)
  -l, --inline          Find results are inline
```

## Scripting

Combine this script with the power of `fzf` to interactively select a bang:

```bash
read -rp "Enter your query: " QUERY
python sear.py -l find "" -c bangs.json | fzf | awk -F "|" '{print $6}' | sed 's|{{{s}}}|$QUERY|' | xargs -I {} xdg-open {}
```

## License

This repository is licensed under the MIT License, a very permissive license that allows you to use, modify, copy, distribute and more.
