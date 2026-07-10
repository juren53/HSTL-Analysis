<div align="right"><i>Last edit: 2026-07-09 19:47</i></div>

# collection-names

An HSTL Photo data task that looks up each **Collection #** in the `Assets by
Row Numbers` sheet against the `Collections` sheet and fills in the matching
**Collection Name**, saving the result as a new workbook so the original
export is never modified.

## Background

This started as a request to fix a broken Excel `VLOOKUP`: an HMS export
listed each asset's Collection # but not its full name, and a formula meant
to pull the name from a second "location guide" tab was returning `#N/A` for
IDs that were visibly present in that tab (see
[`LLC's problem statement.txt`](<LLC's problem statement.txt>)). Rather than
hand-fix a formula, the lookup was rewritten as a small Python script
(`fill_collection_names.py`) so it can be re-run against fresh exports
without re-entering or re-copying a formula each time.

## Contents

- **`fill_collection_names.py`** — the script itself.
- **`fill_collection_names_summary.md`** — a condensed, at-a-glance overview
  of how the script works.
- **`fill_collection_names.md`** — a full line-by-line walkthrough of the
  code (written for a reader learning Python), plus a closing section on
  [generalizing the lookup-and-fill pattern](fill_collection_names.md#generalizing-this-for-future-data-analysis-projects)
  for reuse in future data analysis tasks.
- **`Assets by Row Numbers-2026-06-24-09-12-13.xlsx`** — the sample input
  workbook (default `INPUT_FILE`).
- **`Assets by Row Numbers-filled.xlsx`** — the script's output from that
  sample run (default `OUTPUT_FILE`).
- **`LLC's problem statement.txt`** — the original request that prompted this
  task.

## Running it

```
python fill_collection_names.py [input.xlsx] [output.xlsx]
```

With no arguments, it runs against the sample workbook above and writes
`Assets by Row Numbers-filled.xlsx`. See
[Inputs & outputs](fill_collection_names.md#inputs--outputs) for the full
rules on how arguments override the defaults.

## Where to look next

- Quick overview → [`fill_collection_names_summary.md`](fill_collection_names_summary.md)
- Full walkthrough → [`fill_collection_names.md`](fill_collection_names.md)
