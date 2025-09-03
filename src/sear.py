import json
import os
import sys
import argparse
import webbrowser
from urllib.parse import quote_plus

def open_in_browser(url):
    webbrowser.open(url)

def read_bang(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            bangs = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON: {e}")
            sys.exit(1)

    if not isinstance(bangs, list):
        print("Expected a JSON array of bangs.")
        sys.exit(1)

    return bangs

def search_bang(bangs, target, query, browser=False):
    for bang in bangs:
        if isinstance(bang, dict) and bang.get('t') == target:
            if 'u' in bang:
                url_template = bang['u']
                encoded_query = quote_plus(query)
                url = url_template.replace("{{{s}}}", encoded_query)
                if browser:
                    open_in_browser(url)
                return url
    print(f'No bang found with t = "{target}"')
    return ""

def print_json_field(key, value, indent=2):
    pad = ' ' * indent
    if isinstance(value, dict):
        print(f"{pad}{key}:")
        for k, v in value.items():
            print_json_field(k, v, indent + 2)
    elif isinstance(value, list):
        print(f"{pad}{key}: [")
        for item in value:
            if isinstance(item, (dict, list)):
                print_json_field("", item, indent + 2)
            else:
                print(f"{' ' * (indent + 2)}- {item}")
        print(f"{pad}]")
    else:
        print(f"{pad}{key}: {value}")

def list_bangs(bangs):
    for bang in bangs:
        if isinstance(bang, dict) and 's' in bang and 't' in bang:
            print(f"{bang['s']}: {bang['t']}")

def inspect_bangs(bangs):
    for bang in bangs:
        if isinstance(bang, dict):
            for key, value in bang.items():
                print_json_field(key, value)
            print("")

def find_bang(bangs, request_bang, search_key="s", inline=False):
    for bang in bangs:
        if isinstance(bang, dict) and search_key in bang:
            value = str(bang[search_key])
            if request_bang.lower() in value.lower():
                if inline:
                    print(f"{bang.get('s', 'N/A')}|{bang.get('d', 'N/A')}|{bang.get('t', 'N/A')}|{bang.get('c', 'N/A')}|{bang.get('sc', 'N/A')}|{bang.get('u', 'N/A')}")
                else:
                    print(f"Title: {bang.get('s', 'N/A')}")
                    print(f"Domain: {bang.get('d', 'N/A')}")
                    print(f"Shortcode: {bang.get('t', 'N/A')}")
                    print(f"Link: {bang.get('u', 'N/A')}")
                    print(f"Category: {bang.get('c', 'N/A')}")
                    print(f"Sub-category: {bang.get('sc', 'N/A')}\n")

def main():
    parser = argparse.ArgumentParser(
        description="",
        usage="""
  sear.py COMMAND|BANG QUERY [FLAGS]

commands:
  list             Lists all bangs
  inspect          Output json file
  find [BANG_NAME] Find a bang with a specified name
"""
    )

    parser.add_argument("args", nargs="*", help="Command or bang search")
    parser.add_argument("-c", "--config", default="bangs.json", help="Path to bangs JSON file")
    parser.add_argument("-b", "--browser", action="store_true", help="Open URL in browser")
    parser.add_argument("-f", "--findkey", default="s", help="Key to search for in 'find' (e.g., s, t, u)")
    parser.add_argument("-l", "--inline", action="store_true", help="Find results are inline")

    args = parser.parse_args()
    bangs = read_bang(args.config)

    if not args.args:
        parser.print_help()
        sys.exit(1)

    command = args.args[0]

    if command == "list":
        list_bangs(bangs)
    elif command == "inspect":
        inspect_bangs(bangs)
    elif command == "find":
        if len(args.args) < 2:
            print("Error: Missing bang name for 'find'")
            sys.exit(1)
        query = " ".join(args.args[1:])
        try:
            find_bang(bangs, query, args.findkey, args.inline)
        except KeyError:
            print("[Fatal]: Your bang file has missing JSON keys.")
    else:
        bang = command
        query_parts = args.args[1:]
        if not query_parts:
            print("Error: No search query provided.")
            sys.exit(1)
        query = " ".join(query_parts)
        url = search_bang(bangs, bang, query, args.browser)
        if url and not args.browser:
            print(url)

if __name__ == "__main__":
    main()
