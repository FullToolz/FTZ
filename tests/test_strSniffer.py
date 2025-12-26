import pytest
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strSniffer import *

def test_extract_strings_ascii(tmp_path):
    # create a file with an ASCII string of length ≥ 4
    content = b"ZZ" + b"teststr" + b"\x00" + b"YY"
    f = tmp_path / "ascii.bin"
    f.write_bytes(content)

    strs = extract_strings(str(f), min_len=4)
    # we should see "teststr" in the extracted strings
    assert any(s == "teststr" for _, s in strs)

def test_extract_strings_utf16le(tmp_path):
    # UTF-16LE encode "HELLO" gives b'H\x00E\x00L\x00L\x00O\x00'
    s = "HELLO"
    content = s.encode("utf-16le")
    f = tmp_path / "utf16.bin"
    f.write_bytes(content)

    strs = extract_strings(str(f), min_len=4)
    assert any(s == "HELLO" for _, s in strs)

def test_find_keywords_and_sort_hits():
    # simulate two extracted strings, one with "error", one with "password"
    strings = [
        (0x10, "An error occurred"),
        (0x20, "Enter password please")
    ]
    hits = find_keywords(strings)
    # we expect one Errors and one Auth
    cats = {h[0] for h in hits}
    assert cats == {"Errors", "Auth"}

    sorted_hits = sort_hits(hits)
    # CATEGORY_ORDER has Auth (1) before Errors (4)
    assert sorted_hits[0][0] == "Auth"
    assert sorted_hits[1][0] == "Errors"
