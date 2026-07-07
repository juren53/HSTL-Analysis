<div align="right"><i>Last edit: 2026-07-07 08:46</i></div>

# Walkthrough: `zy-search.py`

## Purpose

Searches a folder of ZyIMAGE photo-database export text files (one record
per file, each containing an `<accession_number>` tag, a date, a caption,
and an `<xref image="...">` pointer to the source TIFF — see
`67-1890.txt` for a sample record) for a specific phrase, and prints the
filenames of every record whose text contains it.

## How it works

```python
directory = '/home/juren/Projects/HST-ZyImage-Project/'
search_query = '"Senator Tom Connally meets"'

def search_files(directory, search_query):
    results = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r') as file:
                file_contents = file.read()
                if re.search(search_query, file_contents):
                    results.append(filename)
    return results

matching_files = search_files(directory, search_query)
```

1. `directory` and `search_query` are hard-coded at the top of the file —
   there's no command-line input.
2. `search_files()` lists every entry in `directory`, skips anything that
   isn't a `.txt` file, reads each remaining file's full contents, and runs
   `re.search(search_query, file_contents)` against it.
3. Any file where the search matches gets its filename appended to
   `results`, which is returned once every file has been checked.
4. Back in the main script, the matching filenames are printed one per
   line, or `'No matching files found.'` if the list is empty.

## Things worth knowing

- **The query is a regex, not a literal string** — `re.search` treats
  `search_query` as a regular expression. Since the query here is wrapped
  in literal double quotes (`'"Senator Tom Connally meets"'`), the match
  only succeeds if the target text is *also* wrapped in double quotes
  (which the sample record isn't) — this looks like a leftover from the
  original ChatGPT example (see `Notes/Conversation-w-ChatGPT-on-ZyDB-search.txt`)
  rather than intentional regex syntax. In practice this means the script
  as written won't match plain-text records like `67-1890.txt` unless the
  quotes are removed from `search_query`.
- **Not recursive** — only searches files directly inside `directory`, not
  subfolders.
- **Case-sensitive, single-phrase** — no `re.IGNORECASE`, and only one
  phrase can be searched per run; both `directory` and `search_query` must
  be edited in the source to change what's searched.
- **Whole-file read** — each file is read entirely into memory before
  searching, which is fine at ZyIMAGE-record sizes (a few hundred bytes to
  a few KB each) but wouldn't scale to large files.
