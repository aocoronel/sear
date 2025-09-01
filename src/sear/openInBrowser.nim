import std/osproc

proc openInBrowser*(url: string) =
  when defined(windows):
    discard execCmd("start " & url)
  elif defined(macosx):
    discard execCmd("open " & url)
  else:
    discard execCmd("xdg-open " & url)
