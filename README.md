<div align="right"><i>Last edit: 2026-07-09 19:56</i></div>

# HSTL-Analysis

A collection of ad-hoc data analysis tasks supporting Harry S. Truman
Presidential Library (HSTL) Audio Visual metadata projects. Each task lives
in its own subdirectory, self-contained with its own code, documentation,
and data.

## Tasks

- [`collection-names/`](collection-names/) —
  an HSTL Photo data task that looks up each Collection # in the
  Assets sheet against the Collections sheet and fills in the matching
  Collection Name. See [`README.md`](collection-names/README.md) for an
  overview, [`fill_collection_names_summary.md`](collection-names/fill_collection_names_summary.md)
  for a condensed walkthrough, or
  [`fill_collection_names.md`](collection-names/fill_collection_names.md) for
  the full line-by-line version. *(Last updated: 2026-07-07 04:41)*

- [`audio-metadata-analysis/`](audio-metadata-analysis/) —
  an HSTL Audio data task consisting of analysis and
  reporting scripts for the HSTL Audio Metadata catalog export (moved from
  the `HST-Metadata-Audio` project's `analysis/` folder). See
  [`README.md`](audio-metadata-analysis/README.md) for an overview, or
  [`PROCESS_NOTES.md`](audio-metadata-analysis/PROCESS_NOTES.md) for the full
  tab-by-tab details. *(Last updated: 2026-06-08 20:26)*

- [`zy-nique/`](zy-nique/) —
  an HSTL Photo data task built around the legacy ZyIMAGE photo database:
  searches accession-number-tagged text records for matching text (e.g. by
  caption or accession number), plus the full ZyImage Database Project
  archive merged in from the standalone `HST-Zyimage-Project` repo
  (background docs, code, documentation, notes, sample reports, and raw
  data exports). See
  [`zy-search.py`](zy-nique/zy-search.py),
  [`WALK-THRU_zy-search-py.md`](zy-nique/WALK-THRU_zy-search-py.md),
  [`README.md`](zy-nique/README.md), and
  [`ZY Image Database Project - High-level Summary.pdf`](<zy-nique/Documentation/ZY Image Database Project - High-level Summary.pdf>)
  for details. *(Last updated: 2023-01-08 14:10)*
