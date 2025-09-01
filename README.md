# Interact with Kagi Bangs in the CLI

`sear` allows you to use the powerful [Kagi Bangs](https://github.com/kagisearch/bangs) from the CLI. Check the official bang repository to know more about it.

Essentially, it allows you configure a `json` file to predefine a search query, and quickly replace the query template and open in a browser.

```bash
sear pm Leishmaniosis
# Output
# https://pubmed.ncbi.nlm.nih.gov/?term=Leishmaniosis&filter=simsearch2.ffrft
```

Currently, `sear` only supports the `s`, `t` and `u` keys. Illustratively:

```diff
{
  "s": "Metacritic",
- "d": "www.metacritic.com",
  "t": "mc",
  "u": "https://www.metacritic.com/search/{{{s}}}/",
- "c": "Online Services",
- "sc": "Search"
}
```

## Features

- Open links in a browser

## Installation

```bash
nimble install https://github.com/aocoronel/sear
```

## Usage

```
Interact with Kagi Bangs in the CLI

Usage:
  searc COMMAND|BANG QUERY FLAG <FLAG_INPUT>

Commands:
  list      Lists all bangs
  inspect   Output json file

Flags:
  -b, --browser    Open search in the browser
```

## License

This repository is licensed under the MIT License, a very permissive license that allows you to use, modify, copy, distribute and more.
