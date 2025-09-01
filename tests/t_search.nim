import sear/[searchBang, readBang]
import unittest

suite "Search tests":
  test "returns correct URL when valid bang is given":
    let bangs = readBang("tests/bangs.json")
    let bang = "pm"
    let query = "test"
    let browser = false
    let result: string = searchBang(bangs, bang, query, browser)
    assert result == "https://pubmed.ncbi.nlm.nih.gov/?term=test&filter=simsearch2.ffrft"
