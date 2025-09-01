import std/[uri, json, strutils]
import openInBrowser

proc searchBang*(
    bangs: JsonNode, target: string, query: string, browser = false
): string =
  for bang in bangs:
    if bang.kind == JObject:
      if bang.hasKey("t") and bang["t"].getStr() == target:
        if bang.hasKey("u"):
          var url = bang["u"].getStr()
          let encodedQuery = encodeUrl(query.replace(" ", "+"))
          url = url.replace("{{{s}}}", encodedQuery)
          if browser:
            openInBrowser(url)
            return url
          else:
            return url
  echo "No bang found with t = \"", target, "\""
  return ""

proc printJsonField*(key: string, value: JsonNode, indent = 2) =
  let pad = repeat(' ', indent)
  case value.kind
  of JObject:
    echo pad, key, ":"
    for k, v in value.pairs:
      printJsonField(k, v, indent + 2)
  of JArray:
    echo pad, key, ": ["
    for item in value.items:
      if item.kind in {JObject, JArray}:
        printJsonField("", item, indent + 2)
      else:
        echo repeat(' ', indent + 2), "- ", item
    echo pad, "]"
  else:
    echo pad, key, ": ", value
