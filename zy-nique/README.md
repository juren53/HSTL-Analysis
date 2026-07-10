<div align="right"><i>Last edit: 2026-07-09 19:54</i></div>

# zy-nique

An HSTL Photo data task built around the legacy **ZyIMAGE** photo database.
The original goal (under the direction of Laurie Austin, Audiovisual
Archives) was to determine whether ZyIMAGE contains records that are
*unique* — i.e. not represented in the HST Photo Database — by comparing
accession numbers (ANs) between the two systems. `zy-search.py` handles a
related, narrower need: searching accession-number-tagged ZyIMAGE text
records for matching text (e.g. by caption or accession number). See
[`WALK-THRU_zy-search-py.md`](WALK-THRU_zy-search-py.md) for a full
line-by-line walkthrough of that script.

This folder also holds the full **ZyImage Database Project** archive,
merged in from the standalone `HST-Zyimage-Project` repo — background docs,
code, documentation, notes, sample reports, and raw data exports.

## The ZyIMAGE database, briefly

The ZyIMAGE database itself is organized into three top-level directories —
`NEWCARDS`, `TEXT`, and `TRUMAN` — each holding one text record per photo,
tagged with an accession number. As of the last count: `NEWCARDS` had 6,833
files (6,810 ANs); `TEXT` had 10,983 files across 77 subdirectories (25,018
ANs, 2,026 compound ANs); `TRUMAN` had 14,468 files across 98 subdirectories
(25,855 ANs, 1,980 compound ANs). See
[`Documentation/`](Documentation/) for diagrams and the full project
summary.

## Contents

- **`zy-search.py`** — searches a folder of ZyIMAGE text records for a
  phrase and prints the matching filenames. See
  [`WALK-THRU_zy-search-py.md`](WALK-THRU_zy-search-py.md) for details, and
  `67-1890.txt` for a sample record.
- **`Code/`** — helper scripts developed for the AN-uniqueness comparison
  (e.g. `unique-ans.py`, `find-missing-ans.py`, `find-TEXT-ANs.py`,
  `an-fill-in-6.py`, `pygrep.py`) plus an `Archive/` of earlier iterations.
- **`Data/`** — raw and derived data: database exports (`PhotoExport.csv`,
  `ZyFiles.zip`, `Converted NEWCARD files.tar.gz`) and comparison output
  (`UNIQUE.TXT`, `zy-ans-all-3.txt`).
- **`Documentation/`** — the project's high-level summary (PDF/DOCX) and
  diagrams of the ZyIMAGE directory structure.
- **`Background/`** — reference material consulted while building the
  comparison tooling (Python/data-import references, command-line text
  utilities, licensing).
- **`Notes/`** — working notes, including ChatGPT conversations that shaped
  the AN-matching and text-search approach.
- **`Reports/`** — sample generated reports for individual accession
  numbers.

## Where to look next

- Script walkthrough → [`WALK-THRU_zy-search-py.md`](WALK-THRU_zy-search-py.md)
- Project background/diagrams → [`Documentation/`](Documentation/)
