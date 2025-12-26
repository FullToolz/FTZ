import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from pathlib import Path

import builtins


import Jpat


def test_jcc_plus_xor_short(tmp_path, capsys):

    # make a file with a prior XOR (0x32) within 20 bytes, then a short JCC (0x71)

    data = bytearray(b"\x00" * 10)

    data[0] = 0x32         # XOR‐family opcode early

    data += bytes([0x71])  # JCC at offset 10

    data += b"\x00" * 10

    f = tmp_path / "jcc_xor.bin"

    f.write_bytes(bytes(data))


    # call main(); it will print a rich table

    Jpat.main(str(f))

    captured = capsys.readouterr().out

    assert "JCC + XOR" in captured


def test_near_jcc(tmp_path, capsys):

    # near JCC is 0F 8x, put 0x0F 0x82 at offset 5

    data = bytearray(b"\x00" * 5)

    data += bytes([0x0F, 0x82])

    data += b"\x00" * 20

    f = tmp_path / "near.bin"

    f.write_bytes(bytes(data))


    Jpat.main(str(f))

    captured = capsys.readouterr().out

    # without an XOR in the prior 20 bytes, it should fall back to plain "JCC(near)"

    assert "JCC(near)" in captured
