<div align="right"><i>Last edit: 2026-07-07 04:45</i></div>

# `fill_collection_names.py` — how it works (short version)

*A condensed overview of how it works. For a detailed look at the Python code see
[`fill_collection_names.md`](fill_collection_names.md).*

## What it does

Given an Excel workbook with two tabs, this script fills in missing
collection names on one tab by looking them up on the other, then saves the
result as a **new** file (the original is never touched).

| Sheet | Column A | Column B |
|---|---|---|
| `Collections` | Collection ID (`HST-PCBP`) | Collection Name (`Brown, Peter C. Papers`) |
| `Assets by Row Numbers` | Collection # | *(filled in by this script)* |

`Collections` is the "answer key" — a complete ID → Name table.
`Assets by Row Numbers` has the ID but is missing the name; this script closes
that gap. *(Details: [Purpose](fill_collection_names.md#purpose),
[Expected layout](fill_collection_names.md#expected-workbook-layout))*

## Running it

```
python fill_collection_names.py [input.xlsx] [output.xlsx]
```

- No arguments → uses the built-in defaults (a specific dated export as input,
  `Assets by Row Numbers-filled.xlsx` as output).
- One argument → that file becomes the input; output still defaults.
- Two arguments → both are overridden.

*(Details: [Inputs & outputs](fill_collection_names.md#inputs--outputs-in-detail))*

## How it works, in three parts

1. **`build_lookup(ws)`** reads the `Collections` sheet once and turns it
   into a Python dict: `{"HST-PCBP": "Brown, Peter C. Papers", ...}`. IDs and
   names are trimmed of whitespace. An ID with a blank name is still added to
   the dict — just mapped to `""`. *(Details:
   [build_lookup walkthrough](fill_collection_names.md#3-build_lookupws-function-in-detail-lines-2941))*

2. **`fill_names(input_path, output_path)`** opens the workbook, calls
   `build_lookup`, then walks every row of `Assets by Row Numbers`:
   - Blank Collection # → row is skipped entirely.
   - ID found with a real name → name is written into column B.
   - ID not found, *or* found with a blank name → `"#N/A"` is written into
     column B, and the row is logged for the summary.

   It then saves to the output file and prints how many rows were filled,
   plus up to the first 20 unmatched IDs (with row numbers). *(Details:
   [fill_names walkthrough](fill_collection_names.md#4-fill_namesinput_path-output_path-function-in-detail-lines-4491))*

3. **The entry point** (`if __name__ == "__main__":`) only runs when the
   script is executed directly. It resolves the input/output paths from
   command-line arguments (falling back to defaults), exits with an error if
   the input file doesn't exist, and then calls `fill_names(...)`. *(Details:
   [Entry point walkthrough](fill_collection_names.md#5-script-entry-point-in-detail-lines-94103))*

## Behavior worth knowing

- **Non-destructive** — always writes a separate output file; the input is
  only ever opened for reading.
- **Traceable failures** — unmatched rows get `"#N/A"` in the spreadsheet
  (never a silent blank) and are listed in the console output.
- **A blank name counts as "no match"** — same as an ID that isn't in
  `Collections` at all. Both end up flagged `#N/A`.
- **Matching is exact-text only** (after trimming whitespace) — no fuzzy
  matching, so case or punctuation differences won't match.
- **No structural validation** — a wrong sheet name crashes loudly
  (`KeyError`); a wrong column number or header-row count fails silently,
  quietly producing bad data instead of an error.

*(Details: [Summary of behavior](fill_collection_names.md#summary-of-behavior-in-detail))*
