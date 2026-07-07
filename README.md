# HSTL-Analysis

A collection of ad-hoc data analysis tasks supporting Harry S. Truman
Presidential Library (HSTL) metadata projects. Each task lives in its own
subdirectory, self-contained with its own code, documentation, and data.

## Tasks

- [`collection-names/`](collection-names/) — looks up each Collection # in the
  Assets sheet against the Collections sheet and fills in the matching
  Collection Name. See
  [`fill_collection_names_summary.md`](collection-names/fill_collection_names_summary.md)
  for a quick overview, or
  [`fill_collection_names.md`](collection-names/fill_collection_names.md) for
  a full line-by-line walkthrough.

- [`audio-metadata-analysis/`](audio-metadata-analysis/) — analysis and
  reporting scripts for the HSTL Audio Metadata catalog export (moved from
  the `HST-Metadata-Audio` project's `analysis/` folder). See
  [`PROCESS_NOTES.md`](audio-metadata-analysis/PROCESS_NOTES.md) for details.
