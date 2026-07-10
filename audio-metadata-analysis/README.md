<div align="right"><i>Last edit: 2026-07-09 19:51</i></div>

# audio-metadata-analysis

An HSTL Audio data task that compares sound recording metadata from two
sources — the NARA catalog export and the Truman Library's Drupal
website export — to identify discrepancies, prepare catalog updates, and
adapt unpublished-in-catalog records for bulk cataloging submission.

Moved from the `HST-Metadata-Audio` project's `analysis/` folder.

## What it produces

Running `build_tabs.py` reads both source exports and writes a single
timestamped workbook (`HST_Audio_Analysis_YYYY-MM-DD-HHMM.xlsx`) with eight
tabs, split across two goals:

- **Comparison and cleanup** — side-by-side analysis of records present in
  both sources (title/accession-number/description mismatches), plus
  catalog records missing from Drupal.
- **Catalog submissions and updates** — Drupal-published records not yet in
  the NARA catalog, and existing matched records, both mapped to the bulk
  cataloging template format.

See [`PROCESS_NOTES.md`](PROCESS_NOTES.md) for the full tab-by-tab
breakdown (row counts, column mappings, lookup tables, date-parsing rules,
and known limitations requiring manual review).

## Contents

- **`build_tabs.py`** — the main script; reads the two CSV exports below and
  writes the multi-tab output workbook.
- **`add_footer.py`** — a small utility that adds a page-number footer
  (`filename` / `Page X of Y`) to a `.docx` file; used on
  `PROCESS_NOTES.docx`.
- **`PROCESS_NOTES.md`** / **`PROCESS_NOTES.docx`** — the detailed
  process/reference documentation (same content, two formats).
- **`HST-SRC_ALL_DrupalExport_2026-05-07_edited.csv`** — Drupal export input
  (all sound recordings, published and unpublished).
- **`HST-SRC_ALL_catalog-export-20260507.csv`** — NARA catalog export input
  (published sound recordings only).
- **`LAA_2ndDraft_SoundRec_Template-BulkVer10-19-23.xlsx`** — bulk
  cataloging template (work in progress) used as the target format for the
  template-mapped tabs.
- **`HST_Audio_Analysis_2026-06-08-2027.xlsx`** — a prior output run of the
  script.
- **`MSG_LAA-Drupal-Catalog.txt`** — background correspondence for this
  task.

## Running it

```
python build_tabs.py
```

Input filenames are hard-coded relative to the script's own folder (no
command-line arguments); the output filename is auto-timestamped, so
re-running never overwrites a previous run's output.

## Where to look next

- Full process notes → [`PROCESS_NOTES.md`](PROCESS_NOTES.md)
