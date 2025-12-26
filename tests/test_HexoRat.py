import pytest

from HexoRat import has_cmp, has_jcc, has_xor, has_backward_jump, score_window


def test_feature_detection_and_scoring():

    # build a 32‐byte window containing

    #  - CMP   (0x38)

    #  - JCC   (0x70)

    #  - XOR   (0x30)

    #  - backward short jump: 0x70 0x80

    w = bytes([0x38, 0x70, 0x30, 0x70, 0x80]) + b"\x00" * 27

    assert has_cmp(w)

    assert has_jcc(w)

    assert has_xor(w)

    assert has_backward_jump(w)

    # score = 3 (cmp) + 4 (jcc) + 5 (xor) + 4 (backjump) = 16

    assert score_window(w) == 16


def test_empty_window():

    w = b"\x00" * 32

    assert not has_cmp(w)

    assert not has_jcc(w)

    assert not has_xor(w)

    assert not has_backward_jump(w)

    assert score_window(w) == 0



from pathlib import Path

import builtins


from /HexoRat import main


def test_hexorat_main_high_hint(tmp_path, monkeypatch, capsys):

    # Change CWD so output.txt lands in tmp_path

    monkeypatch.chdir(tmp_path)


    # Craft a file whose first 32‐byte window has XOR (0x30), backward jump (0x70 0x80)

    content = bytes([0x30, 0x70, 0x80]) + b"\x00" * 100

    f = tmp_path / "sample.bin"

    f.write_bytes(content)


    # respond "N" to both LOW and MED prompts (HIGH hints are always included)

    answers = iter(["N", "N"])

    monkeypatch.setattr(builtins, "input", lambda _: next(answers))


    # run

    main(str(f))


    # inspect output.txt

    txt = (tmp_path / "output.txt").read_text()

    assert "[HIGH]" in txt

    assert "XOR loop (possible string decoder)" in txt


    # table should also have been printed; we can check stdout for the pattern

    out = capsys.readouterr().out

    assert "XOR loop (possible string decoder)" in out
