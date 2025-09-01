import std/[json, strutils, os, uri, osproc, parseopt]
import sear/[searchBang, readBang, openInBrowser]
import cliche

const filePath = "bangs.json"

func help(): string =
  result =
    """
Interact with Kagi Bangs in the CLI

Usage:
  searc COMMAND|BANG QUERY FLAG <FLAG_INPUT>

Commands:
  list      Lists all bangs
  inspect   Output json file

Flags:
  -b, --browser    Open search in the browser
"""

proc inspect(bangs: JsonNode) =
  for bang in bangs:
    if bang.kind == JObject:
      for key, value in bang.pairs:
        printJsonField(key, value)
      echo ""

proc list(bangs: JsonNode) =
  for bang in bangs:
    if bang.kind == JObject:
      if bang.hasKey("s") and bang.hasKey("t"):
        let name = bang["s"].getStr()
        let alias = bang["t"].getStr()
        echo name, ":", alias

proc main() =
  # Hardcoded: bangs.json
  let bangs: JsonNode = readBang(filePath)

  let cmdParams = commandLineParams()
  cmdParams.getOpt((browser: false), declareFlag = [("b", "browser")])

  # Quit if empty
  if cmdParams.len == 0:
    quit(help(), 1)

  var bang: string
  var queryParts: seq[string] = @[]

  # Parse arguments
  var p = initOptParser(cmdParams)
  while true:
    p.next()
    case p.kind
    of cmdEnd, cmdLongOption, cmdShortOption:
      break
    of cmdArgument:
      case p.key
      of "list":
        list(bangs)
        return
      of "inspect":
        inspect(bangs)
        return
      else:
        if bang.len == 0:
          bang = p.key
          continue
        queryParts.add(p.key)

  # Empty query
  if queryParts.len == 0:
    quit("Error: No search query provided.", 1)

  let query = queryParts.join(" ")
  echo searchBang(bangs, bang, query, browser)

when isMainModule:
  main()
