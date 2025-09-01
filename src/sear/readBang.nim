import std/[json, os]

proc readBang*(filePath: string): JsonNode =
  if not fileExists(filePath):
    echo "Error: File not found: ", filePath
    quit(1)

  let jsonString = readFile(filePath)
  var bangs: JsonNode

  try:
    bangs = parseJson(jsonString)
  except JsonParsingError:
    echo "Failed to parse JSON: ", getCurrentExceptionMsg()
    quit(1)
  if bangs.kind != JArray:
    echo "Expected a JSON array of bangs."
    quit(1)

  return bangs
