<div align="right"><i>Last edit: 2026-07-07 04:44</i></div>

# Walkthrough: `fill_collection_names.py`

*A plain-English explanation of the Python concepts used in this code.*

## Purpose

Takes an "Assets by Row Numbers" workbook that has a **Collection #** in column A of
the Assets tab but no name in column B, looks each ID up in a **Collections** tab,
and writes the matching **Collection Name** into column B. The result is saved as a
new file — the original workbook is never modified.

### The problem

Somewhere there's a single Excel file (a **workbook**) with (at least) two
**sheets** (also called **tabs** — the labeled pages you click between at the
bottom of an Excel window):

- A `Collections` sheet that acts like a small reference table: one row per
  collection, pairing a short ID code (like `HST-PCBP`) with its full,
  human-readable name (like `Brown, Peter C. Papers`).
- An `Assets by Row Numbers` sheet listing individual assets/items, where
  each row only records *which collection* an item belongs to by its short
  ID — column B, where the full collection name would go, is empty.

The task is: for every asset row, find its ID in the `Collections` sheet and
copy the matching name over into column B of the Assets sheet — without
touching the original file.

### Why this is a job for code, not manual editing

If you're coming from Excel rather than programming, the natural comparison
is Excel's own `VLOOKUP` (or `XLOOKUP`) formula — this script does
essentially the same *kind* of thing (find a value in one table by matching
an ID, pull back a related value), just written as a Python program instead
of a spreadsheet formula. Two reasons this script exists rather than just
using a formula directly in the spreadsheet:

- It can be run repeatedly against fresh exports of the same two sheets
  without anyone re-entering a formula or re-copying it down a column each
  time.
- It doesn't just copy the found values — it also actively flags and reports
  every row where nothing matched (see the `#N/A` cells and the console
  summary — the same behavior an Excel formula could reproduce, but this
  script also tallies and lists them for you in the terminal).

### How the two functions divide the work

The whole task is split across two functions covered in depth further below,
each responsible for one half of the "lookup" idea:

- `build_lookup` (see the [dedicated section](#3-build_lookupws-function-in-detail-lines-2941))
  reads the *reference table* — the `Collections` sheet — once, up front, and
  turns it into a fast in-memory structure (a Python **dict**) that can
  answer "what's the name for this ID?" instantly, without re-scanning the
  sheet for every single asset row.
- `fill_names` (see the [dedicated section](#4-fill_namesinput_path-output_path-function-in-detail-lines-4491))
  does the actual row-by-row work over the `Assets by Row Numbers` sheet,
  using the dict `build_lookup` produced to fill in column B (or mark `#N/A`
  when nothing matches), then saves everything to a new file and prints a
  summary.

### Why the result is saved as a new file

The last sentence of the purpose statement — "the original workbook is never
modified" — is a deliberate safety choice: since this script is meant to be
run against real collection-management data, a bug or unexpected input
shouldn't be able to silently corrupt the source spreadsheet. Concretely,
this is enforced by the script always calling `wb.save(output_path)`
(covered in full in the [Summary of behavior](#non-destructive-the-original-file-is-never-touched)
section) with a filename different from wherever it read the input from —
never overwriting the file it opened.

## Inputs & outputs, in detail

- **Input** (default): `Assets by Row Numbers-2026-06-24-09-12-13.xlsx`
- **Output** (default): `Assets by Row Numbers-filled.xlsx`
- Both can be overridden by typing them after the script name when you run it from
  a terminal (these are called **command-line arguments** — extra words typed after
  the program name that the program can read and react to):
  ```
  python fill_collection_names.py <input.xlsx> <output.xlsx>
  ```

This section is really just a preview of behavior that's fully implemented in
the entry-point code (`if __name__ == "__main__":`, covered in full detail
further down) — but it's worth spelling out how these two filenames actually
get resolved, since it's easy to misuse from the command line if you don't
know the mechanics.

### Where the default filenames come from

```python
INPUT_FILE = "Assets by Row Numbers-2026-06-24-09-12-13.xlsx"
OUTPUT_FILE = "Assets by Row Numbers-filled.xlsx"
```

These are plain string constants defined near the top of the script (see the
constants section below). They're only ever *used* as fallbacks — in the
entry-point code, `Path(INPUT_FILE)` and `Path(OUTPUT_FILE)` are what get
used when no corresponding command-line argument was typed. That means the
"default" input filename is tied to a specific, one-time export of the
spreadsheet (note the timestamp baked into the name,
`2026-06-24-09-12-13`) — running the script with no arguments against a
newer export with a different timestamp in its filename simply won't find
the file, and will hit the `input_path.exists()` check and exit with an
error. In practice, the defaults are really only convenient for repeatedly
re-running the script against that one specific file while testing; any
other file has to be named explicitly.

### How arguments are supplied, and what "overriding" really means

Typing `python fill_collection_names.py <input.xlsx> <output.xlsx>` doesn't
change anything about the script itself — it's the mechanism the *operating
system* uses to hand the program a list of extra words (arguments) via
`sys.argv`, which the script then reads from (see `sys.argv` in both the
[imports](#1-imports-lines-710) and
[entry point](#5-script-entry-point-in-detail-lines-94103) sections for the
full mechanics). Two consequences follow directly from how that reading logic
works:

- **Position matters, not keywords.** There's no way to say "just override
  the output, keep the default input" by name (e.g. there's no
  `--output=result.xlsx` flag support here) — arguments are read purely by
  their position in the list. Supplying only one argument always overrides
  the *input* file (because that's `sys.argv[1]`, checked first); the *output*
  filename can only be overridden by also supplying the input filename before
  it, since `sys.argv[2]` (the output override) only gets read if there are at
  least two arguments.
- **Both, one, or neither can be given** — but never "just the second one."
  The three realistic ways to invoke the script are: with nothing (both
  defaults), with one argument (custom input, default output), or with two
  arguments (both custom).

### What counts as a valid path here

Both the default filenames and anything typed on the command line are
treated as **relative paths** unless you type an absolute one. A relative
path is interpreted relative to the **current working directory** — whatever
folder your terminal is "in" at the moment you run the `python ...` command
— not necessarily the folder the script file itself lives in. That's why
running the script from a different folder than the one containing the
`.xlsx` files would cause `input_path.exists()` to fail even if the defaults
"look right," unless you either `cd` into the right folder first or supply a
full (absolute) path as the argument instead, e.g.:

```
python fill_collection_names.py "C:\Users\you\Documents\data.xlsx" out.xlsx
```

Note the double quotes around the first path — this is ordinary
command-line-shell syntax (not something the Python script itself cares
about) needed because the folder name contains spaces; without the quotes,
the shell would treat each space-separated word as a *separate* argument,
shifting everything after it out of position.

### No file-type checking

Nothing in the script inspects the `.xlsx` extension or otherwise confirms
the input is really a valid Excel file before attempting to open it — that
job is implicitly delegated to `openpyxl.load_workbook(input_path)` inside
`fill_names`. If you pointed the script at a file that exists but isn't a
real `.xlsx` workbook (a `.csv`, a corrupted file, etc.), `input_path.exists()`
would still pass (the file *is* there), and the program would proceed past
the entry point's only check — failing later, with whatever error
`openpyxl` itself raises when it can't parse the file, rather than a
friendly message from this script.

## Expected workbook layout

| Sheet | Column A | Column B |
|---|---|---|
| `Collections` | Collection ID (e.g. `HST-PCBP`) | Collection Name (e.g. `Brown, Peter C. Papers`) |
| `Assets by Row Numbers` | Collection # | *(filled in by this script)* |

### Reading the table itself

This is a small reference table describing the two Excel sheets the script
expects to work with — it's worth reading it slowly, cell by cell, before
diving into the code that relies on it.

- The **left column, "Sheet,"** names one of the two tabs inside the Excel
  workbook. Each of the two data rows below the header describes one sheet.
- The **"Column A" and "Column B" columns** describe what's actually stored
  in the first two columns of *that* sheet — remembering that, in Excel,
  "column A" always means the leftmost column, and "column B" the one
  immediately to its right, regardless of what data lives in them.

Reading the two data rows in turn:

- **Row 1 — the `Collections` sheet.** Column A holds a short **Collection
  ID** — a code like `HST-PCBP` uniquely identifying one collection. Column B
  holds that collection's full **Collection Name** — the human-readable title,
  like `Brown, Peter C. Papers`. Together, column A and column B on this
  sheet form pairs: this sheet is the "reference table" or "answer key" the
  rest of the table plays off of. Every row here is a known, already-complete
  `ID → Name` fact.
- **Row 2 — the `Assets by Row Numbers` sheet.** Column A again holds a
  **Collection #** — the same kind of short ID code as above — but here it's
  attached to some other record (an individual asset), not a full listing of
  every collection. Column B, in this sheet, is described as *"(filled in by
  this script)"* — meaning that, before the script runs, this cell is
  expected to be **empty**, and the whole point of running the script is to
  populate it, one row at a time, by looking up column A's ID in the first
  sheet's table.

In short: the table is describing an "ID → Name" relationship split across
two places — fully known in `Collections`, but only half-known (ID present,
Name missing) in `Assets by Row Numbers` — and the rest of this document
explains how the code bridges that gap.

This table isn't just documentation the script happens to follow loosely —
every part of it corresponds to a literal value hard-coded into the
constants near the top of the file (lines 12–26), and the rest of the script
trusts those constants completely, with no checking that the real workbook
actually matches them. It's worth understanding exactly how, so you know what
to fix if the script ever errors out on a different spreadsheet.

### Sheet names must match exactly

```python
ASSETS_SHEET = "Assets by Row Numbers"
COLLECTIONS_SHEET = "Collections"
```

These two constants hold the literal, exact names of the two tabs the script
expects to find inside the `.xlsx` file. They're used later in `fill_names`
as:

```python
ws_collections = wb[COLLECTIONS_SHEET]
ws_assets      = wb[ASSETS_SHEET]
```

Recall that `wb[SHEET_NAME]` is a dict-style lookup — it looks for a sheet
whose name exactly equals the string given. "Exactly" is the key word: sheet
names in `openpyxl` are matched case-sensitively and whitespace-sensitively,
so a real workbook with a tab named `"collections"` (lowercase) or
`"Collections "` (trailing space) would **not** be found under the name
`"Collections"`. If the name genuinely doesn't exist in the workbook,
`wb[COLLECTIONS_SHEET]` raises a `KeyError` — a Python error meaning "this key
doesn't exist in this dict-like object" — and the whole script would stop
with a traceback (Python's error report) rather than silently doing the wrong
thing. There's no `try`/`except` (error-handling block) anywhere in this
script to catch that and produce a friendlier message — so a sheet-name
mismatch shows up as a raw Python crash, not a clean "Error: ..." message
like the missing-input-file case in the entry point.

### Column positions are numbers, not letters, and count from 1

```python
COL_ID   = 1   # Column A — Collection ID  (e.g. "HST-PCBP")
COL_NAME = 2   # Column B — Collection Name (e.g. "Brown, Peter C. Papers")

ASSETS_COL_ID   = 1   # Column A — Collection #
ASSETS_COL_NAME = 2   # Column B — where the name should go
```

Excel shows columns as letters (A, B, C, ...) but `openpyxl`, like the rest
of Python, works with columns as plain integers, counting from `1` for the
first column. These four constants are what the earlier walkthroughs of
`build_lookup` and `fill_names` referred to when indexing into each row's
tuple (`row[COL_ID - 1]`, `row[ASSETS_COL_NAME - 1]`, etc.) — the `- 1` in
each of those expressions converts from this "Excel-style, counting from 1"
numbering into Python's "counting from 0" indexing used for tuples and
lists.

Notice that `COL_ID`/`COL_NAME` (for the `Collections` sheet) and
`ASSETS_COL_ID`/`ASSETS_COL_NAME` (for the `Assets by Row Numbers` sheet) are
separate constants, even though they currently hold the same values (`1` and
`2`). That's deliberate future-proofing: if the two sheets' column layouts
ever diverge (say, the Assets sheet gains a new column A and the Collection #
moves to column B), only the `ASSETS_COL_*` constants would need to change,
without touching how `Collections` is read.

Because these are just plain numbers with no validation, if a real workbook
has the Collection ID in a different column than A, the script won't error
out — it will simply read the *wrong* column silently, likely producing
nonsense IDs (or blank ones) that fail every lookup. This is different from
the sheet-name case above, which fails loudly with a `KeyError` — a
mismatched column number fails quietly and shows up only as an unexpectedly
huge `missing` list.

### The header row assumption

```python
for row in ws.iter_rows(min_row=2, values_only=True):     # in build_lookup
...
for row_num, row in enumerate(
    ws_assets.iter_rows(min_row=2), start=2
):                                                          # in fill_names
```

Both loops hard-code `min_row=2`, meaning both sheets are assumed to have
exactly **one** header row (a first row of column titles, like "Collection
ID" / "Collection Name", rather than real data) before the actual data
begins. This is why row numbers throughout the script — both the `row_num`
values used in the `missing` list and the ones printed in the summary — are
1-based and start at 2, matching how a person looking at the spreadsheet in
Excel would count rows (row 1 is always the very top row, containing the
column titles).

If a real workbook had, say, two header rows, or no header row at all, the
script wouldn't detect or complain about the mismatch — it would just start
reading from the wrong row: either treating a genuine header row as if it
were data (producing a bogus entry like `lookup["Collection ID"] =
"Collection Name"`), or skipping the first row of real data by mistake. As
with the column-position assumption above, this is a silent-failure risk
rather than one that raises an error — worth double-checking by hand if the
`missing` list ever comes back suspiciously large or a `filled` count seems
too low.

### Why none of this is validated up front

It's worth noticing, as a general pattern, that this script does exactly one
existence check before running — `input_path.exists()` in the entry-point
section, confirming the *file itself* is present — and nothing beyond that.
It never confirms the two expected sheet names are actually present, that
the columns contain the kind of data implied by their names, or that there's
really just one header row. This keeps the script short and simple, but it
also means that when the workbook doesn't match the assumptions baked into
these constants, the failure mode ranges from a loud, immediate crash
(wrong sheet name → `KeyError`) to a silent, hard-to-notice one (wrong column
number or header-row count → bad data quietly flows through the whole
pipeline). Knowing which constants encode which assumption is exactly what
lets you diagnose which kind of problem you're looking at.

## Walkthrough of the code

### 1. Imports (lines 7–10)

```python
import sys
from pathlib import Path
import openpyxl
```

### Reading the code block itself

Before getting into what each library actually does, it's worth reading these
three lines slowly, since two slightly different import *forms* are used here
and the difference matters for how the rest of the script refers back to
them.

- **Line 1, `import sys`.** The plain `import <name>` form makes the entire
  `sys` module available, but only under its own name — everything inside it
  has to be reached by writing `sys.` in front (e.g. `sys.argv`, `sys.exit`,
  seen later in the script). Nothing is pulled out individually here; `sys`
  itself, as a whole package of functionality, is what becomes available.
- **Line 2, `from pathlib import Path`.** The `from <module> import <name>`
  form works differently: instead of making the whole `pathlib` module
  available, it reaches *inside* `pathlib` and pulls out just one specific
  name, `Path`, making that single thing directly available on its own —
  usable later simply as `Path(...)`, with no `pathlib.` prefix needed.
  Everything else that might exist inside `pathlib` besides `Path` is not
  imported and isn't accessible unless imported separately.
- **Line 3, `import openpyxl`.** Back to the plain form from line 1 — the
  whole `openpyxl` library becomes available under its own name, so every
  piece of it used later in the script (`openpyxl.load_workbook(...)`, etc.)
  is written with the `openpyxl.` prefix.

The practical difference to notice while reading the rest of the script: any
time you see a bare name being called directly — like `Path(...)` — that
name was almost certainly brought in with a `from ... import ...` line; any
time you see a `something.thing(...)` with a dot, the part before the dot
(`sys`, `openpyxl`) was almost certainly brought in with a plain `import
something` line. This is a useful reading habit for any Python file, not just
this one: the import lines at the top tell you exactly which "dotted" prefix
to expect for the rest of the file.

An `import` statement makes an outside chunk of code — a **module** (a single
file of Python code) or a **package** (a folder bundling multiple related
modules) — available for use inside this script, under whatever name follows
`import` (or, with `from X import Y`, just the one specific thing named `Y`
from module `X`). Python itself only understands a small set of built-in
commands; almost everything else — including all three things imported here
— comes from libraries like these. There are two kinds of libraries in play:

- **Standard library** modules (`sys`, `pathlib`) ship with every Python
  installation — nothing extra to install, they're just always there.
- **Third-party** libraries (`openpyxl`) are written and published by other
  people/projects, and must be installed separately (typically with
  `pip install openpyxl`) before a script that imports them will run.

#### `import sys`

`sys` (short for "system") is a standard library module that exposes
information and functionality tied to the Python interpreter itself and the
environment it's running in. This script uses exactly one piece of it:

- `sys.argv` — the list of command-line arguments the script was launched
  with (used in the entry-point section to accept an optional input/output
  file path).

It's also used for `sys.exit(...)`, which stops the program early with an
error message (also covered in the entry-point section). `sys` has many other
capabilities beyond these two (e.g. `sys.path` for module search locations,
`sys.stdout` for low-level output), but this script only touches `argv` and
`exit`.

#### `from pathlib import Path`

`pathlib` is a standard library module for working with filesystem paths
(locations of files/folders on disk) as objects, rather than as plain text
strings. `from pathlib import Path` pulls out just one specific name, `Path`,
from that module — as opposed to `import pathlib`, which would require typing
`pathlib.Path` every time. `Path` is a **class** (a blueprint for creating
objects) that represents a single file or directory location.

This script uses `Path` for two things:

- Wrapping a plain string like `"Assets by Row Numbers-filled.xlsx"` into a
  `Path` object — e.g. `Path(INPUT_FILE)` — so it can be handled consistently
  wherever a path is expected (both `openpyxl.load_workbook(...)` and
  `wb.save(...)` happily accept `Path` objects).
- Calling `.exists()` on a `Path` object to check whether a file is actually
  present on disk before trying to open it, avoiding a more confusing crash
  later if it isn't.

Compared to plain strings, `Path` objects understand filesystem concepts
directly (e.g. `.exists()`, `.name`, joining paths with `/`), which is why
modern Python code tends to prefer `pathlib` over building file paths by hand
with string concatenation.

#### `import openpyxl`

`openpyxl` is a **third-party** library (not part of standard Python — it has
to be installed, e.g. via `pip install openpyxl`) purpose-built for reading
and writing modern Excel `.xlsx` files. Unlike `pathlib`, this import doesn't
pull out one specific name — `import openpyxl` (without `from`) means every
piece of functionality from the library has to be accessed with the
`openpyxl.` prefix, e.g. `openpyxl.load_workbook(...)`.

This script relies on `openpyxl` for essentially all of its Excel-specific
work:

- `openpyxl.load_workbook(input_path)` — opens an existing `.xlsx` file and
  reads it into a **Workbook** object in memory.
- Looking up a sheet by name from a workbook (`wb[SHEET_NAME]`), which
  returns a **Worksheet** object.
- `worksheet.iter_rows(...)` — walking through a sheet's rows, either as raw
  values (`values_only=True`, used in `build_lookup`) or as full **Cell**
  objects that can be both read (`.value`) and written to (used in
  `fill_names`).
- `workbook.save(output_path)` — writing an in-memory workbook back out to an
  `.xlsx` file on disk.

Without `openpyxl` (or an equivalent library), Python has no built-in way to
understand the `.xlsx` file format at all — spreadsheets are really zipped
bundles of XML files under the hood, and `openpyxl` is what handles that
complexity so the rest of the script can just deal with simple rows, columns,
and cell values.

### 2. Configuration constants (lines 12–26)

```python
INPUT_FILE = "Assets by Row Numbers-2026-06-24-09-12-13.xlsx"
OUTPUT_FILE = "Assets by Row Numbers-filled.xlsx"

ASSETS_SHEET = "Assets by Row Numbers"
COLLECTIONS_SHEET = "Collections"

COL_ID   = 1   # Column A — Collection ID  (e.g. "HST-PCBP")
COL_NAME = 2   # Column B — Collection Name (e.g. "Brown, Peter C. Papers")

ASSETS_COL_ID   = 1   # Column A — Collection #
ASSETS_COL_NAME = 2   # Column B — where the name should go
```

### Reading the code block itself

This block is eight separate **assignment statements** — lines of the form
`name = value`, each creating a variable and storing a value in it — grouped
into four pairs by blank lines. Reading it top to bottom:

- **`INPUT_FILE = "..."` and `OUTPUT_FILE = "..."`** each store a piece of
  text (a **string**, written between double quotes) — the default filenames
  the script will read from and write to if nothing else is specified. These
  are the same two constants referenced by name in the
  [Inputs & outputs](#where-the-default-filenames-come-from) section above.
- **`ASSETS_SHEET = "..."` and `COLLECTIONS_SHEET = "..."`** likewise each
  store a string, but here the text is a sheet/tab name rather than a
  filename — the exact names of the two tabs the script expects to find
  inside the workbook once it's opened.
- **`COL_ID = 1` and `COL_NAME = 2`** store plain whole numbers (**integers**
  — note the lack of quotes, distinguishing them from the string constants
  above) representing column positions on the `Collections` sheet.
- **`ASSETS_COL_ID = 1` and `ASSETS_COL_NAME = 2`** store two more integers,
  this time for column positions on the `Assets by Row Numbers` sheet.

A few smaller details worth noticing while reading:

- The extra spaces before some `=` signs (e.g. `COL_ID   = 1` lining up
  under `COL_NAME = 2`) are purely cosmetic whitespace, added so the `=`
  signs visually line up in a column — Python ignores this kind of extra
  spacing around an assignment entirely; `x = 1` and `x   = 1` mean exactly
  the same thing.
- The blank lines separating the four pairs aren't required by Python
  either — they're there purely to visually group related constants for a
  human reader (filenames, then sheet names, then the two sets of column
  numbers), and could be removed without changing how the script runs.
- The text after `#` on the last four lines (e.g.
  `# Column A — Collection ID  (e.g. "HST-PCBP")`) is a **comment** — `#`
  tells Python to ignore everything from that character to the end of the
  line, so comments exist purely for human readers and have no effect on the
  program's behavior. Here they're used to remind the reader which
  spreadsheet column (by letter) each numeric constant corresponds to.

These are **constants** — plain variables written in ALL_CAPS by convention to
signal "this value shouldn't change while the program runs." Writing the sheet
names and column numbers once at the top (instead of scattering the literal
numbers `1` and `2` throughout the code) means if the spreadsheet layout ever
changes, you only need to update it in one place.

Note that spreadsheet columns are counted starting at 1 (column A = 1, column
B = 2, ...) — this is different from most things in Python, which normally
count starting at 0. That mismatch is why you'll see `- 1` in a couple of
places further down, to convert from "spreadsheet column number" to "Python
list position."

### 3. `build_lookup(ws)` function, in detail (lines 29–41)

```python
def build_lookup(ws) -> dict[str, str]:
    """Return {collection_id: collection_name} from the Collections sheet."""
    lookup = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        coll_id   = row[COL_ID - 1]
        coll_name = row[COL_NAME - 1]
        if coll_id:
            lookup[str(coll_id).strip()] = str(coll_name).strip() if coll_name else ""
    return lookup
```

### Reading the code block itself

Before diving line by line, it helps to look at the overall *shape* of this
block, since Python uses **indentation** (leading spaces) — not curly braces
or `end` keywords like some other languages — to show which lines belong
inside which other lines. Each level of indentation here nests one level
deeper than the one above it:

```
def build_lookup(ws) -> dict[str, str]:      <- level 0: the function itself
    """docstring"""                          <- level 1: inside the function
    lookup = {}                              <- level 1: inside the function
    for row in ws.iter_rows(...):            <- level 1: inside the function
        coll_id   = row[COL_ID - 1]          <- level 2: inside the for loop
        coll_name = row[COL_NAME - 1]        <- level 2: inside the for loop
        if coll_id:                          <- level 2: inside the for loop
            lookup[...] = ...                <- level 3: inside the if
    return lookup                            <- level 1: inside the function
```

A few things to notice from this shape alone, before reading any single line
in depth:

- Everything indented under the `def` line (levels 1, 2, and 3) is "inside"
  `build_lookup` — it's all part of the function's body, and none of it runs
  until the function is actually called elsewhere.
- The `for` loop's own body (everything at level 2 and 3) is indented one
  step further than `lookup = {}` and `return lookup` — which is how you can
  tell, just from indentation, that `coll_id = row[...]`, `coll_name =
  row[...]`, and the `if` block all repeat *once per row*, whereas `lookup =
  {}` runs only once (before the loop starts) and `return lookup` runs only
  once (after the loop finishes all its repetitions).
- The single line inside the `if coll_id:` block is indented one step
  further still (level 3) than the `if` line itself — showing that it's
  conditional, only running for rows where `coll_id` turns out to be truthy,
  whereas everything at level 2 runs for *every* row regardless.
- Structurally, this function has exactly one loop and one decision point
  nested inside it — read as a sentence, the whole function says: "start
  with an empty dict; for every data row in the sheet, if that row has an ID,
  record an ID→Name pair for it; once all rows are processed, hand back
  whatever was collected."

With that overall shape in mind, the rest of this section steps through each
line's details individually.

This function's job is to turn the `Collections` sheet — rows spread across
an Excel tab — into a single Python **dict** (dictionary) that the rest of the
program can search instantly. We'll walk through it statement by statement,
and follow a small worked example alongside the explanation. Imagine the
`Collections` sheet looks like this:

| | A (Collection ID) | B (Collection Name) |
|---|---|---|
| Row 1 | Collection ID | Collection Name |
| Row 2 | `HST-PCBP` | `Brown, Peter C. Papers` |
| Row 3 | `HST-XYZ ` | `""` (blank cell) |
| Row 4 | *(blank)* | `Some Orphan Name` |

#### The function definition line

```python
def build_lookup(ws) -> dict[str, str]:
```

- `def` is the keyword that starts a **function definition** — it tells
  Python "here's a reusable, named block of code," as opposed to a statement
  that just runs once immediately.
- `build_lookup` is the name we're giving this function. Elsewhere in the
  script (in `fill_names`), it gets *called* by writing
  `build_lookup(ws_collections)` — the name has to match exactly.
- `(ws)` declares that this function takes exactly one input, which will be
  referred to as `ws` (short for "worksheet") inside the function body. When
  it's called later with `build_lookup(ws_collections)`, whatever
  `ws_collections` refers to gets temporarily renamed to `ws` for the
  duration of the function.
- `-> dict[str, str]` is a **type hint** — a note for human readers (and
  optional external tools) saying "this function returns a dict whose keys
  are strings and whose values are strings." Python itself does not check or
  enforce this at runtime; it's purely documentation.
- The trailing `:` marks the end of the definition line and means "the
  indented lines below are the body of this function."

#### The docstring

```python
    """Return {collection_id: collection_name} from the Collections sheet."""
```

A triple-quoted string immediately inside a function is called a
**docstring** — a special comment describing what the function does. It
isn't executed as code; it exists so a reader (or a tool like `help()`) can
see a one-line summary without reading the implementation.

#### Creating an empty dict

```python
    lookup = {}
```

`{}` is Python's literal syntax for "an empty dict." This line creates a new,
empty dictionary and stores it in a variable named `lookup`. Right now it
holds nothing — the rest of the function's job is to fill it in, one
Collections row at a time, before handing it back at the end.

#### The for loop and `iter_rows`

```python
    for row in ws.iter_rows(min_row=2, values_only=True):
```

`ws.iter_rows(...)` is a method (a function attached to the worksheet object)
provided by `openpyxl` that goes through the sheet's rows one at a time. Two
named arguments are passed to it:

- `min_row=2` — start at row 2, skipping row 1 (the header row of column
  titles, which isn't real data to look up).
- `values_only=True` — normally `openpyxl` would hand back special "Cell"
  objects (which know their row/column position and can be written to). Since
  this function only needs to *read* values, `values_only=True` simplifies
  each row down to a plain Python **tuple** of the raw cell contents. A tuple
  is an ordered, fixed-size grouping of values — similar to a list, but
  conventionally used when you're not going to add or remove items from it.

`for row in ...:` is a **for loop**: Python takes the sequence of rows that
`iter_rows` produces and runs the indented block below once per row, each
time setting `row` to the next row's tuple of values.

Using the example table above, `iter_rows` would produce, one at a time:

- `row = ("HST-PCBP", "Brown, Peter C. Papers")` — from row 2
- `row = ("HST-XYZ ", None)` — from row 3 (blank cells come through as `None`)
- `row = (None, "Some Orphan Name")` — from row 4

#### Pulling values out of the tuple

```python
        coll_id   = row[COL_ID - 1]
        coll_name = row[COL_NAME - 1]
```

`row` is a tuple, and individual items inside a tuple (or list) are accessed
with square brackets and a numeric **index** — but Python indexes starting at
`0`, not `1`. Recall from the constants section that `COL_ID = 1` and
`COL_NAME = 2` (matching Excel's column A = 1, column B = 2 convention). So:

- `row[COL_ID - 1]` is `row[0]` — the first item in the tuple, i.e. column A's
  value.
- `row[COL_NAME - 1]` is `row[1]` — the second item, i.e. column B's value.

For our first example row, this sets `coll_id = "HST-PCBP"` and
`coll_name = "Brown, Peter C. Papers"`.

#### Skipping rows with no ID

```python
        if coll_id:
```

This is an `if` statement guarding the rest of the loop body. In Python, when
a value is used directly as a yes/no condition like this, it's checked for
being **"truthy"** or **"falsy."** Values like `None`, an empty string `""`,
the number `0`, and empty containers all count as falsy (treated as `False`);
basically anything else (a non-empty string, a non-zero number, etc.) is
truthy (treated as `True`).

So `if coll_id:` reads as "only continue if `coll_id` actually has something
in it." For our row-4 example (`coll_id = None`, since column A was blank),
this condition is `False`, so the indented line below it is skipped — no
entry gets added to `lookup` for that row.

#### Adding an entry to the dict

```python
            lookup[str(coll_id).strip()] = str(coll_name).strip() if coll_name else ""
```

This single line both builds a **key** and a **value** and stores the pair in
`lookup`. Reading it in pieces:

- `str(coll_id)` converts `coll_id` to text using the built-in `str(...)`
  function. This matters because Excel might have stored an ID as a number
  rather than text; converting guarantees we always get a string to work
  with.
- `.strip()` is a string method that removes any accidental leading/trailing
  whitespace (spaces, tabs) — so `"HST-XYZ "` becomes `"HST-XYZ"`. This
  matters because a stray trailing space would otherwise make the lookup fail
  to match later, even though the ID "looks" the same to a human.
- Together, `str(coll_id).strip()` is the **key** being added to the dict —
  the cleaned-up Collection ID.
- `str(coll_name).strip() if coll_name else ""` is the **value** being
  stored, and it's a **conditional expression** — Python's inline form of
  if/else that produces a value instead of running a block of statements. Read
  it as: *"if `coll_name` is truthy, use `str(coll_name).strip()`; otherwise
  use `""`."* This handles row 3 in our example, where the ID `HST-XYZ` exists
  but the name cell is blank (`coll_name = None`, which is falsy) — instead of
  crashing when trying to `.strip()` a `None`, it falls back to storing an
  empty string.
- `lookup[key] = value` is dict **item assignment**: it adds a new
  `key: value` pair to the dict (or overwrites the value if that key was
  already present).

Following the example through, after the loop finishes, `lookup` would be:

```python
{
    "HST-PCBP": "Brown, Peter C. Papers",
    "HST-XYZ": "",
}
```

Row 4 never made it in (no ID to key on), row 2 added a full entry, and row 3
added an entry with an empty-string name — which is deliberate, and turns out
to matter later: in `fill_names`, an ID that maps to `""` is treated the same
as an ID that isn't in the dict at all (both are "falsy," so both get flagged
`#N/A` — see the note in the next section).

#### Returning the result

```python
    return lookup
```

`return` ends the function and hands the specified value — here, the
now-fully-built `lookup` dict — back to whatever code called
`build_lookup(...)`. Once the function returns, the `lookup` variable itself
stops existing (it was local to this function); only the value it pointed to
lives on, now under whatever name the caller assigns it to (in `fill_names`,
that's a variable also named `lookup`).

### 4. `fill_names(input_path, output_path)` function, in detail (lines 44–91)

```python
def fill_names(input_path: Path, output_path: Path) -> None:
    wb = openpyxl.load_workbook(input_path)

    ws_collections = wb[COLLECTIONS_SHEET]
    ws_assets      = wb[ASSETS_SHEET]

    lookup = build_lookup(ws_collections)
    print(f"Loaded {len(lookup):,} collection entries from '{COLLECTIONS_SHEET}' tab.")

    filled = 0
    missing = []

    for row_num, row in enumerate(
        ws_assets.iter_rows(min_row=2), start=2
    ):
        coll_id_cell = row[ASSETS_COL_ID - 1]
        name_cell    = row[ASSETS_COL_NAME - 1]

        raw = coll_id_cell.value
        if raw is None:
            continue

        coll_id = str(raw).strip()
        name    = lookup.get(coll_id)

        if name:
            name_cell.value = name
            filled += 1
        else:
            name_cell.value = "#N/A"
            missing.append((row_num, coll_id))

    wb.save(output_path)

    print(f"Filled {filled:,} rows.")
    if missing:
        print(f"\nNo match found for {len(missing)} Collection ID(s):")
        for row_num, coll_id in missing[:20]:
            print(f"  Row {row_num}: '{coll_id}'")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more.")
    print(f"\nSaved to: {output_path}")
```

### Reading the code block itself

This function is considerably longer than `build_lookup`, so before reading
it line by line, it's worth looking at its overall shape — again using
Python's indentation to see which lines nest inside which other lines:

```
def fill_names(input_path, output_path) -> None:      <- level 0: the function itself
    wb = openpyxl.load_workbook(input_path)            <- level 1: runs once
    ws_collections = wb[COLLECTIONS_SHEET]             <- level 1: runs once
    ws_assets      = wb[ASSETS_SHEET]                  <- level 1: runs once
    lookup = build_lookup(ws_collections)              <- level 1: runs once
    print(...)                                         <- level 1: runs once
    filled = 0                                         <- level 1: runs once
    missing = []                                       <- level 1: runs once
    for row_num, row in enumerate(...):                <- level 1: runs once (starts the loop)
        coll_id_cell = row[...]                        <- level 2: once per asset row
        name_cell    = row[...]                        <- level 2: once per asset row
        raw = coll_id_cell.value                       <- level 2: once per asset row
        if raw is None:                                <- level 2: once per asset row
            continue                                   <- level 3: only for blank IDs
        coll_id = str(raw).strip()                     <- level 2: skipped rows never reach here
        name    = lookup.get(coll_id)                  <- level 2
        if name:                                       <- level 2
            name_cell.value = name                     <- level 3: only when matched
            filled += 1                                <- level 3: only when matched
        else:                                           <- level 2
            name_cell.value = "#N/A"                   <- level 3: only when unmatched
            missing.append((row_num, coll_id))         <- level 3: only when unmatched
    wb.save(output_path)                                <- level 1: runs once (after loop ends)
    print(...)                                          <- level 1: runs once
    if missing:                                         <- level 1: runs once
        print(...)                                      <- level 2: only if something was unmatched
        for row_num, coll_id in missing[:20]:           <- level 2: only if something was unmatched
            print(...)                                  <- level 3: once per unmatched row (up to 20)
        if len(missing) > 20:                           <- level 2: only if something was unmatched
            print(...)                                  <- level 3: only if more than 20 unmatched
    print(...)                                           <- level 1: runs once, always
```

A few observations that fall out of this shape alone, before reading any
single line closely:

- Everything at **level 1** runs exactly once per call to `fill_names` —
  opening the file, building the lookup, setting up counters, and (after the
  loop shown below finishes entirely) saving the workbook and printing the
  final lines of the summary.
- The **`for row_num, row in enumerate(...)` loop** is the one block that
  repeats — once for every row in the `Assets by Row Numbers` sheet. Its
  entire body sits at level 2 and deeper, which is how you can tell, just
  from the indentation, that `wb.save(output_path)` near the bottom runs only
  **after** every asset row has been processed, not once per row.
- Inside that loop, `if raw is None: continue` is a shortcut exit — for a
  blank Collection # cell, everything below it (levels 2 and 3 that follow)
  is simply never reached for that particular row.
- Further down, the loop contains one more decision point,
  `if name: / else:`, whose two branches (level 3) are mutually exclusive —
  exactly one of them runs per row that wasn't already skipped by
  `continue`.
- After the loop, the second `if missing:` block (also just a plain
  decision, not a loop-that-repeats-the-whole-summary) only prints its
  contents when at least one row failed to match — meaning a completely
  successful run (nothing in `missing`) skips straight from
  `print(f"Filled ...")` to the final `print(f"\nSaved to: ...")` line,
  never touching anything in that `if` block at all.

With that overall control flow in mind — one-time setup, then a loop over
every asset row, then one-time save-and-report — the rest of this section
steps through the details of each individual line.

This function is the "main" logic: it opens the file, uses `build_lookup` to
get the ID→Name dict, then goes row by row through the `Assets by Row
Numbers` sheet writing in names (or `#N/A`), and finally saves and reports
results. We'll again follow a small worked example. Assume `build_lookup` has
already produced this dict (matching the example from the previous section,
plus one ID that plainly doesn't exist in `Collections` at all):

```python
lookup = {
    "HST-PCBP": "Brown, Peter C. Papers",
    "HST-XYZ": "",
}
```

And the `Assets by Row Numbers` sheet looks like this:

| | A (Collection #) | B (name — to be filled in) |
|---|---|---|
| Row 1 | Collection # | Collection Name |
| Row 2 | `HST-PCBP` | *(blank)* |
| Row 3 | `HST-XYZ` | *(blank)* |
| Row 4 | *(blank)* | *(blank)* |
| Row 5 | `HST-NOPE` | *(blank)* |

#### The function definition line

```python
def fill_names(input_path: Path, output_path: Path) -> None:
```

Same `def` syntax as before, but this function declares **two** parameters,
`input_path` and `output_path`. Each has a type hint (`: Path`) saying they're
expected to be `Path` objects (the file-path type imported from `pathlib` at
the top of the script). The `-> None` return type hint means this function
isn't designed to hand back a value at all — its purpose is its *side
effects* (saving a file, printing to the screen), not a computed result.

#### Step 1 — loading the workbook and picking out sheets

```python
    wb = openpyxl.load_workbook(input_path)

    ws_collections = wb[COLLECTIONS_SHEET]
    ws_assets      = wb[ASSETS_SHEET]
```

- `openpyxl.load_workbook(input_path)` opens the `.xlsx` file at that path and
  reads its entire contents into memory as a **workbook** object, stored in
  the variable `wb`.
- A workbook is essentially a container of sheets/tabs. `wb[COLLECTIONS_SHEET]`
  looks up the sheet named `"Collections"` (recall `COLLECTIONS_SHEET` is a
  constant defined near the top of the file) — the square-bracket syntax here
  works the same way it does for dicts: "give me the thing filed under this
  name." The result is stored as `ws_collections` (a worksheet object).
- Likewise, `ws_assets` becomes a reference to the `"Assets by Row Numbers"`
  sheet.

At this point nothing has been changed on disk yet — `wb`, `ws_collections`,
and `ws_assets` are just in-memory Python objects representing what was read
from the file.

#### Step 2 — building and reporting the lookup

```python
    lookup = build_lookup(ws_collections)
    print(f"Loaded {len(lookup):,} collection entries from '{COLLECTIONS_SHEET}' tab.")
```

- `build_lookup(ws_collections)` **calls** the function examined in detail in
  the previous section, passing it the Collections worksheet. Whatever dict
  that function `return`s gets stored here in a new local variable, also
  named `lookup` (a coincidence of naming — it's a completely separate
  variable from the `lookup` that existed *inside* `build_lookup`).
- `len(lookup)` is the built-in `len()` function applied to a dict — it
  returns the number of key/value pairs in it (2, for our example).
- The `print(...)` call uses an **f-string** (a string literal prefixed with
  `f`, allowing `{expression}` placeholders that get evaluated and inserted
  into the text). Inside the placeholder, `{len(lookup):,}` means "compute
  `len(lookup)`, then format it with a `,` thousands-separator" — so `1234`
  would print as `1,234`. For our tiny example it would print:
  `Loaded 2 collection entries from 'Collections' tab.`

#### Step 3 — setting up counters before the main loop

```python
    filled = 0
    missing = []
```

- `filled = 0` creates a simple counter variable, starting at zero, that will
  be incremented once for every row successfully matched.
- `missing = []` creates an empty **list** using `[]`, Python's literal syntax
  for "empty list." Unlike the tuples produced by `iter_rows(...,
  values_only=True)` in `build_lookup`, a list is meant to be added to after
  creation — which is exactly what happens here: one entry gets appended for
  every Collection # that fails to find a match.

#### Step 4 — looping over Assets rows with `enumerate`

```python
    for row_num, row in enumerate(
        ws_assets.iter_rows(min_row=2), start=2
    ):
```

- `ws_assets.iter_rows(min_row=2)` behaves like it did in `build_lookup` —
  it goes through the sheet's rows starting at row 2 (skipping the header).
  Notice `values_only=True` is **not** passed this time, so each `row` here
  is a tuple of full **Cell objects**, not plain values. That distinction
  matters because this function needs to *write* new values into column B —
  something only a Cell object (not a plain value) can do.
- `enumerate(some_sequence, start=2)` is a built-in function that wraps
  around a sequence and produces `(count, item)` pairs — a running counter
  alongside each item — instead of just the item on its own. `start=2` tells
  it to begin counting at 2 rather than the default of 0, which keeps the
  counter matching Excel's actual row numbers (since data starts at row 2).
- `for row_num, row in enumerate(...):` uses **tuple unpacking**: each thing
  `enumerate` produces is a two-item pair, `(count, item)`, and writing two
  names before `in` tells Python to unpack that pair into two separate
  variables in one step — `row_num` gets the count, `row` gets the actual row
  of cells.

For our example, this loop will run four times, with:

- `row_num = 2, row = (<Cell A2>, <Cell B2>)` — the `HST-PCBP` row
- `row_num = 3, row = (<Cell A3>, <Cell B3>)` — the `HST-XYZ` row
- `row_num = 4, row = (<Cell A4>, <Cell B4>)` — the blank row
- `row_num = 5, row = (<Cell A5>, <Cell B5>)` — the `HST-NOPE` row

#### Step 5 — getting the two relevant cells, and skipping blanks

```python
        coll_id_cell = row[ASSETS_COL_ID - 1]
        name_cell    = row[ASSETS_COL_NAME - 1]

        raw = coll_id_cell.value
        if raw is None:
            continue
```

- Same indexing trick as in `build_lookup`: `row[ASSETS_COL_ID - 1]` is
  `row[0]` (column A, the Collection # cell), and
  `row[ASSETS_COL_NAME - 1]` is `row[1]` (column B, where the name will be
  written). These are stored as `coll_id_cell` and `name_cell` — full Cell
  objects, not plain values.
- `coll_id_cell.value` reads the actual contents of that cell via its
  `.value` **attribute**, and stores it in `raw`. (Contrast this with
  `build_lookup`, where `values_only=True` meant the row already gave us
  plain values directly — no `.value` needed there.)
- `if raw is None:` checks specifically for Python's `None` — the "nothing
  here" value — using `is` (identity comparison, the standard way to check
  for `None` specifically, rather than `==`). If the Collection # cell is
  genuinely blank, `continue` immediately jumps back to the top of the loop
  for the next row, skipping everything below for this one. This is what
  happens on row 4 in our example — nothing gets written to `B4` at all, and
  it's never counted as either filled or missing.

#### Step 6 — normalizing the ID and looking it up

```python
        coll_id = str(raw).strip()
        name    = lookup.get(coll_id)
```

- `str(raw).strip()` converts the raw cell value to text and trims stray
  whitespace, exactly as `build_lookup` did when building the dict's keys —
  this consistency is what makes the two sides actually match up.
- `lookup.get(coll_id)` looks up `coll_id` as a key in the `lookup` dict.
  `.get(...)` is a dict method that's a *safer* alternative to
  `lookup[coll_id]`: if the key exists, it returns the matching value; if the
  key does **not** exist, it quietly returns `None` instead of crashing the
  program with an error (which is what plain `lookup[coll_id]` would do for a
  missing key).

Walking through our example rows:

- Row 2: `coll_id = "HST-PCBP"` → `lookup.get(...)` finds it →
  `name = "Brown, Peter C. Papers"`.
- Row 3: `coll_id = "HST-XYZ"` → found in the dict, but its stored value is
  `""` → `name = ""`.
- Row 5: `coll_id = "HST-NOPE"` → not a key in the dict at all →
  `.get(...)` falls back to its default → `name = None`.

#### Step 7 — branching on whether a name was found

```python
        if name:
            name_cell.value = name
            filled += 1
        else:
            name_cell.value = "#N/A"
            missing.append((row_num, coll_id))
```

This is a full `if`/`else` statement (as opposed to the inline conditional
*expression* seen in `build_lookup`) — here we need to run more than one
statement in each branch, so the full block form is used instead.

- `if name:` again relies on truthy/falsy checking: `name` is truthy only
  when it's a non-empty string. Both `""` (row 3) and `None` (row 5) are
  falsy, so **both** end up in the `else` branch — which is exactly the
  behavior called out in the note below.
- **Truthy branch** (row 2 only, in our example): `name_cell.value = name`
  writes the found name directly into the B-column cell — this is the actual
  moment the spreadsheet gets updated in memory. `filled += 1` is shorthand
  for `filled = filled + 1`, incrementing the counter by one.
- **Falsy/`else` branch** (rows 3 and 5): `name_cell.value = "#N/A"` writes
  the literal text `#N/A` into the cell instead, so a human skimming the
  output spreadsheet can immediately spot unmatched rows. Then
  `missing.append((row_num, coll_id))` calls the list's `.append(...)`
  method to add one new item to the end of the `missing` list — that item is
  `(row_num, coll_id)`, a two-item **tuple** pairing the row number with the
  ID that failed, so the summary printed later can reference exactly where
  the problem was.

> **Note:** because `build_lookup` deliberately stores an empty string `""`
> for a Collection ID that exists but has no name (rather than skipping it),
> `lookup.get("HST-XYZ")` returns `""` — which is falsy, just like a missing
> key returning `None` would be. That means "ID found but name is blank" and
> "ID not found at all" are treated identically here: both fall into the
> `else` branch, get `#N/A` written into the cell, and get recorded in
> `missing`.

After the loop finishes for our example: `filled = 1`, and
`missing = [(3, "HST-XYZ"), (5, "HST-NOPE")]`.

#### Step 8 — saving the workbook

```python
    wb.save(output_path)
```

`wb.save(output_path)` writes the **entire** workbook — including every
change made to `name_cell.value` in memory during the loop — out to a file at
`output_path`. Because this saves to `output_path` (a different file from
`input_path`), the original input file is never opened in a writable way and
is left completely untouched.

#### Step 9 — printing the summary

```python
    print(f"Filled {filled:,} rows.")
    if missing:
        print(f"\nNo match found for {len(missing)} Collection ID(s):")
        for row_num, coll_id in missing[:20]:
            print(f"  Row {row_num}: '{coll_id}'")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more.")
    print(f"\nSaved to: {output_path}")
```

- `print(f"Filled {filled:,} rows.")` reports the count of successful
  matches. For our example: `Filled 1 rows.`
- `if missing:` — an empty list is falsy, so this whole block is skipped
  entirely if every row matched. In our example `missing` has 2 items, so
  it's truthy and the block runs.
- `f"\nNo match found for {len(missing)} Collection ID(s):"` — the `\n` inside
  the f-string is an **escape sequence** representing a blank line/line break,
  printed before the text, just to visually separate this section from the
  line above.
- `for row_num, coll_id in missing[:20]:` loops over `missing`, unpacking each
  stored tuple back into `row_num` and `coll_id` (mirroring how they were
  packed together with `.append((row_num, coll_id))` earlier). `missing[:20]`
  uses **slicing** — the `[start:stop]` syntax for taking a sub-portion of a
  list — and `[:20]` (with nothing before the colon) means "start from the
  very beginning, stop before index 20," i.e. "the first 20 items at most."
  If `missing` has fewer than 20 items (as in our example, which has 2),
  slicing simply returns all of them without error.
- Each matching row prints as e.g. `  Row 3: 'HST-XYZ'` and
  `  Row 5: 'HST-NOPE'`.
- `if len(missing) > 20:` only fires when there really were more than 20
  unmatched rows, printing a one-line count of however many extra ones were
  left out of the printed list.
- Finally, `print(f"\nSaved to: {output_path}")` confirms where the new file
  went, regardless of whether any rows were missing.

### 5. Script entry point, in detail (lines 94–103)

```python
if __name__ == "__main__":
    input_path  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(INPUT_FILE)
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(OUTPUT_FILE)

    if not input_path.exists():
        sys.exit(f"Error: '{input_path}' not found.")

    fill_names(input_path, output_path)
```

### Reading the code block itself

This block is much shorter than `fill_names`, but its indentation still
carries meaning worth noticing before reading line by line:

```
if __name__ == "__main__":                                         <- level 0: the guard condition
    input_path  = Path(sys.argv[1]) if ... else Path(INPUT_FILE)   <- level 1: inside the guard
    output_path = Path(sys.argv[2]) if ... else Path(OUTPUT_FILE)  <- level 1: inside the guard
    if not input_path.exists():                                    <- level 1: inside the guard
        sys.exit(f"Error: '{input_path}' not found.")              <- level 2: only if file missing
    fill_names(input_path, output_path)                             <- level 1: inside the guard
```

A few things to notice from this shape alone:

- **Everything in this block sits at level 1 or deeper — meaning all four
  statements only run at all if the `if __name__ == "__main__":` condition
  on line 1 is true.** If this file were imported by another script instead
  of run directly, none of these four lines would execute — not the path
  resolution, not the existence check, and not the call to `fill_names`.
  This is the entire reason the guard exists: to gate *all* of the script's
  actual behavior behind "was I run directly?"
- There is no loop in this block at all — every line here runs **at most
  once** per program run, unlike the repeating `for` loops seen inside
  `build_lookup` and `fill_names`.
- The one nested decision, `if not input_path.exists():`, has only a single
  line inside it (`sys.exit(...)`) at level 2 — and critically, there's no
  matching `else:` here. That's a meaningful absence: if the file *does*
  exist, execution doesn't jump into some other branch — it simply continues
  on to the next level-1 line, `fill_names(input_path, output_path)`, as if
  the `if` block weren't there at all. `sys.exit(...)` is what makes the
  "stop here on failure" behavior work despite there being no `else` — that
  call ends the whole program outright, so control never has the chance to
  fall through to the line below it when the file is missing.
- Reading the block's shape as a sentence: "only if this file was run
  directly: work out the input and output paths, stop with an error if the
  input file doesn't exist, and otherwise run `fill_names` with those paths."

With that control flow in mind, the rest of this section covers each part in
more depth.

Everything above this point in the file — the imports, the constants, and the
two `def` blocks — only *defines* things; none of it actually runs the
program yet. This final block is what actually kicks things off. We'll cover
what each line does, then trace through three ways someone might launch the
script from a terminal.

#### The `if __name__ == "__main__":` guard

```python
if __name__ == "__main__":
```

`__name__` is a special variable that Python automatically sets inside
*every* module (every `.py` file) as it's loaded — you never assign it
yourself. Its value depends on *how* the file was loaded:

- If the file is run directly — e.g. by typing
  `python fill_collection_names.py` at a terminal — Python sets
  `__name__` to the literal text `"__main__"` for that file.
- If the file is instead **imported** from somewhere else — e.g. another
  script does `import fill_collection_names` — Python sets `__name__` to the
  module's own name (`"fill_collection_names"`) instead.

So `if __name__ == "__main__":` is a condition that reads as "only run the
following indented block when this file was the one launched directly by the
user, not when some other file merely imported it to reuse its functions."
This is a very common, standard Python idiom — you'll see it in most
executable Python scripts. The double leading/trailing underscores (`__x__`)
are Python's naming convention for special, built-in names like this one.

Practically, this guard means someone could write `from
fill_collection_names import build_lookup` in a different script to reuse
just that one function, without triggering the whole
file-loading-and-processing routine below — because in that case `__name__`
would *not* equal `"__main__"`, so this block would simply be skipped.

#### Working out the input and output paths

```python
    input_path  = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(INPUT_FILE)
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(OUTPUT_FILE)
```

Both lines have the same shape: a **conditional expression** (the inline
if/else, `A if condition else B`, seen earlier in `build_lookup`) deciding
between a command-line argument and a hard-coded default.

`sys.argv` is a **list** of strings that Python populates automatically at
startup, one entry per word typed on the command line. Crucially,
`sys.argv[0]` is always the script's own filename — the *arguments* a user
actually supplies start at index `1`. For example, running:

```
python fill_collection_names.py myfile.xlsx result.xlsx
```

would make `sys.argv` equal to the list
`["fill_collection_names.py", "myfile.xlsx", "result.xlsx"]` — three items,
at indexes `0`, `1`, and `2`.

- `len(sys.argv) > 1` checks whether *at least one* extra argument was
  supplied beyond the script name itself (i.e. the list has more than 1
  item).
  - If **true**, `sys.argv[1]` (the first real argument, the input filename
    as typed) is wrapped in `Path(...)` and used as `input_path`.
  - If **false** (no arguments given at all), it falls back to
    `Path(INPUT_FILE)` — `INPUT_FILE` being the default filename constant
    defined near the top of the script.
- The second line works identically but one position over: `len(sys.argv) >
  2` checks whether a *second* argument was supplied, and `sys.argv[2]` would
  be it, falling back to `Path(OUTPUT_FILE)` otherwise.

Note that both branches always wrap the result in `Path(...)` — whether the
value came from `sys.argv` (a plain string typed by the user) or from the
`INPUT_FILE`/`OUTPUT_FILE` constants (also plain strings) — so that
`input_path` and `output_path` are consistently `Path` objects afterward,
matching the type hints on `fill_names(input_path: Path, output_path: Path)`.

**Three ways this could play out:**

1. `python fill_collection_names.py` (no arguments)
   → `sys.argv = ["fill_collection_names.py"]`, length 1.
   → Both conditions (`> 1`, `> 2`) are `False`, so both paths fall back to
   the defaults: `input_path = Path(INPUT_FILE)`,
   `output_path = Path(OUTPUT_FILE)`.
2. `python fill_collection_names.py data.xlsx` (one argument)
   → `sys.argv = ["fill_collection_names.py", "data.xlsx"]`, length 2.
   → `len(sys.argv) > 1` is `True`, so `input_path = Path("data.xlsx")`.
   → `len(sys.argv) > 2` is `False` (only 2 items, not more than 2), so
   `output_path` still falls back to `Path(OUTPUT_FILE)`.
3. `python fill_collection_names.py data.xlsx out.xlsx` (two arguments)
   → `sys.argv` has length 3.
   → Both conditions are `True`, so `input_path = Path("data.xlsx")` and
   `output_path = Path("out.xlsx")`.

#### Checking the input file actually exists

```python
    if not input_path.exists():
        sys.exit(f"Error: '{input_path}' not found.")
```

- `input_path.exists()` is a method on the `Path` object (imported from
  `pathlib` at the top of the file) that checks the real filesystem and
  returns `True` or `False` depending on whether something actually exists
  at that location.
- `not` is Python's logical negation operator — `not True` is `False` and
  vice versa. So `if not input_path.exists():` reads as "if the file does
  **not** exist, do the following."
- `sys.exit(...)` immediately halts the program. When given a string
  argument (as here, an f-string like
  `f"Error: '{input_path}' not found."`), Python prints that message and
  exits with a status code indicating failure — this is a deliberate,
  controlled stop, rather than letting the program crash later with a more
  confusing low-level error when `openpyxl` tries and fails to open a
  nonexistent file.

#### Running the main function

```python
    fill_names(input_path, output_path)
```

This is the single line that actually **calls** the `fill_names` function
described in the previous section, passing in the two `Path` objects worked
out above. Everything the script is meant to do — loading the workbook,
building the lookup, filling in names, saving the result, and printing the
summary — happens as a consequence of this one call. If the `if not
input_path.exists():` check above had triggered `sys.exit(...)`, the program
would have already stopped before ever reaching this line.

## Summary of behavior, in detail

This final section ties the code details covered above back into a handful of
overall guarantees the script provides — and explains, in each case, *exactly
which lines* are responsible for that guarantee, so it's not just an
assertion to take on faith.

### Non-destructive: the original file is never touched

The whole program reads from `input_path` and writes to a **different**
`output_path`:

```python
wb = openpyxl.load_workbook(input_path)   # only ever opened for reading
...
wb.save(output_path)                      # only ever written to output_path
```

`openpyxl.load_workbook(input_path)` reads the file at `input_path` into an
in-memory `Workbook` object called `wb`. Every change this script makes —
every `name_cell.value = name` or `name_cell.value = "#N/A"` — happens to
that in-memory object, not to anything on disk. Nothing in the script ever
calls `wb.save(input_path)`; the only save call is `wb.save(output_path)`, and
by default `output_path` is a different filename
(`"Assets by Row Numbers-filled.xlsx"` vs.
`"Assets by Row Numbers-2026-06-24-09-12-13.xlsx"`). So even if the script is
run repeatedly, or crashes partway through, the original input file on disk
is never opened in a mode that could modify it — at worst, you'd get a
missing or incomplete *output* file, never a corrupted *input* file.

One caveat worth knowing as a newbie: this guarantee depends on
`output_path` actually being different from `input_path`. Nothing in the code
stops someone from running
`python fill_collection_names.py data.xlsx data.xlsx` and passing the *same*
name for both — in that specific case, `wb.save(output_path)` would overwrite
the original after all. The default filenames avoid this by construction, but
it's not actively guarded against if you supply your own arguments.

### Traceable failures: unmatched rows are flagged, not hidden

This guarantee comes from two cooperating pieces of the code, both inside
`fill_names`:

```python
if name:
    name_cell.value = name
    filled += 1
else:
    name_cell.value = "#N/A"
    missing.append((row_num, coll_id))
```

and later:

```python
if missing:
    print(f"\nNo match found for {len(missing)} Collection ID(s):")
    for row_num, coll_id in missing[:20]:
        print(f"  Row {row_num}: '{coll_id}'")
```

Two things are true because of this design, and both matter for a newbie to
notice:

1. **In the spreadsheet itself**, an unmatched row's B-column cell is never
   left as an empty/blank cell — it explicitly gets the text `"#N/A"`. This
   is a deliberate choice: a blank cell could easily be mistaken for "this
   row was processed and genuinely has no name," whereas `"#N/A"` unambiguously
   signals "the script looked, and couldn't find a match."
2. **In the terminal output**, every unmatched row is recorded (as a
   `(row_num, coll_id)` tuple appended to the `missing` list) and then
   printed back out by row number and ID — so you don't have to manually
   scan the whole spreadsheet for `#N/A` cells to find out what failed and
   why; the summary tells you directly, up to the first 20 (with a count of
   any remainder).

### Two things that are *not* guaranteed (worth knowing before trusting the output)

Because the walkthrough above traced through exactly how matching works, two
consequences are worth calling out explicitly rather than assuming:

- **Blank names count as "no match," per the earlier note in `build_lookup`
  and `fill_names`.** If a Collection ID exists in the `Collections` sheet
  but its name cell is blank, that row is treated identically to an ID that
  doesn't exist in `Collections` at all — both get `"#N/A"` and both land in
  `missing`. If you ever see an unexpectedly large `missing` count, it's
  worth checking whether some of those IDs are actually present in
  `Collections` with just a blank name, rather than truly absent.
- **Matching is exact-text, not fuzzy.** Both `build_lookup` and the main
  loop in `fill_names` call `str(...).strip()` on IDs before comparing them,
  which handles stray leading/trailing whitespace and non-string cell types
  — but nothing else. Two IDs that differ in case (`"HST-PCBP"` vs.
  `"hst-pcbp"`), internal spacing, or punctuation would **not** be considered
  a match, and would end up in `missing` even though a human would recognize
  them as "the same" collection.
