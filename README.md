# FTZ — FullToolz

FullToolz (FTZ) is a small Python utility collection that helps speed up static reverse-engineering tasks by scanning binaries for interesting strings, suspicious control-flow patterns, and likely string-decode loops. Use it as a quick triage tool when you need to find likely areas of interest inside PE/ELF binaries.



> NOTE: This repository is intended for legitimate security research, malware analysis, debugging, and reverse-engineering tasks. Ensure you have authorization before analyzing or running untrusted binaries. See the "Legal & Security" section below.

Table of contents
- About
- Features
- Requirements
- Installation
- Usage
  - Interactive (main.py)
  - Executable (recommended)
  - Module examples
- Outputs
- Development
- Contributing
- License
- Legal & Security

About
-----
FTZ is a set of focused scanners:
- strSniffer: extracts ASCII/UTF-16LE strings and highlights categories of interest (license, auth, anti-debug, crypto, network, etc.) in a nice table using rich.
- Jpat: lightweight binary-scan for suspicious control-flow patterns (Jcc + nearby XOR/CMP/TEST).
- DSWL: heuristic scanner for LEA-based string builders/decoders (marked as incomplete).
- HexoRat: sliding-window heuristic that scores blocks for CMP/JCC/XOR/backward-jump patterns; writes hints to output.txt and prints a table.

Features
--------
- Fast binary string extraction (ASCII + UTF-16LE) and keyword categorization.
- Heuristic detection of suspicious control-flow constructs commonly used by obfuscators/malware.
- Simple, dependency-light code (single Python dependency: rich) that is easy to extend.
- Outputs human-readable tables and a plain-text hints file.

Requirements
------------
- Python: 3.8+ (3.10/3.11 recommended)
- pip

Runtime dependencies
- rich — used for colorful console tables and output
- strings



Installation
------------
Clone the repository and install dependencies:

```bash
git clone https://github.com/FullToolz/FTZ.git
cd FTZ

# create venv (recommended)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows PowerShell

# install runtime deps
pip install rich
```



Usage
-----
Interactive mode 


```bash
python main.py
```

Executable (recommended):

> NOTE: For Windows, The executable needs to be added inside PATH, and for linux, it's needed to add it as an alias in shell's config file. (e.g. .bashrc)

Windows :
```pwsh
ftz
```

Linux:
```bash
ftz
```


The script will prompt for the binary path, then present a menu:
- 1 — strSniff
- 2 — JPat
- 3 — DSWL (incomplete)
- 4 — HexoRat

Example run:
1. Enter path to your EXE/DLL/ELF when prompted (absolute or relative).
2. Choose the scanner number to run.
3. View results printed as a table in your terminal (and output.txt for HexoRat).

Module usage examples
- Run strSniffer directly from Python (non-interactive):

```python
# from a Python shell or script
import strSniffer
strSniffer.main("binaries/sample.exe")
```

- Run Jpat directly:

```python
import Jpat
Jpat.main("binaries/sample.exe")
```

- Run HexoRat directly (it will ask whether to include LOW/MED hints and writes output.txt):

```python
import HexoRat
HexoRat.main("binaries/sample.exe")
# or run via `python main.py` and choose option 4
```

- DSWL is experimental/incomplete: it detects LEA followed by arithmetic/XOR hints but currently does not render results; included for future expansion.

Outputs
-------
- Most tools render results to the terminal using rich tables.
- HexoRat writes a plain text file `output.txt` containing hint lines like:
  [HIGH] 0x1234 — XOR loop (possible string decoder)

Development
-----------
- The code is intentionally small and dependency-light. If you add features:
  - Add unit tests and place them under tests/
  - Follow formatting with black and lint with flake8
  - Pin new dependencies in requirements.txt

Suggested dev commands:
```bash
# formatting / linting
black .
flake8 .

# tests (after you add them)
pytest -q
```

Contributing
------------
Contributions are welcome. Please:
1. Fork the repository
2. Create a branch with a descriptive name
3. Add tests for new functionality
4. Open a pull request describing your changes

When contributing features that change scanners' heuristics, include short notes describing the motivation and expected false-positive characteristics.

License
-------
This repository includes a LICENSE file in the project root. Please consult that file for license details.

Legal & Security
----------------
- Reverse engineering and analyzing binaries may be restricted by law and/or license agreements. Only analyze binaries you own or have explicit authorization to analyze.
- This project can be used for both defensive and offensive research; the author and maintainers are not responsible for misuse.
- Be careful when running untrusted binaries — analyze them in isolated environments (VMs, sandboxes).

Notes & Known Limitations
-------------------------
- DSWL is currently incomplete and is noted as such in the menu. It performs detection of LEA+XOR/ADD patterns but does not currently render results.
- Heuristics are simple — they can produce false positives and are not a replacement for manual analysis in a disassembler/debugger.
- This repository assumes reasonably-sized binaries; extreme large files may require streaming-based processing.

If you'd like, I can:
- Generate a pinned requirements.txt for you and open a PR with the README added.
- Add simple CLI wrappers so each tool can be run as a standalone script with arguments (e.g., `python -m ftz.strsniffer path`).
- Add unit tests for core functions (string extraction, pattern detection).

Contact
-------
Created by Samyar-Sharafi. Open issues or PRs on the repository for questions, bugs, and feature requests.
