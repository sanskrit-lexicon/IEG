# IEG — Indian Epigraphical Glossary

_Created: 24-06-2026 · Last updated: 11-07-2026_

Digital edition of the **Indian Epigraphical Glossary** (IEG) by **Dineschandra Sircar**
(Motilal Banarsidass, Delhi, 1966) — a glossary of the technical terms of Indian
inscriptions: the administrative, revenue, fiscal, and social vocabulary of the epigraphic
record. This repository is part of the [Cologne Digital Sanskrit Lexicon](https://www.sanskrit-lexicon.uni-koeln.de/)
(CDSL) project, which digitises, corrects, and openly publishes the foundational Sanskrit
dictionaries as citable, reproducible data.

| | |
|---|---|
| Abbreviation | IEG |
| Author | Dineschandra Sircar |
| First published | Delhi, 1966 |
| Coverage | technical terms of Indian inscriptions (epigraphic Sanskrit / Prakrit → English) |
| Digitised by | CDSL |
| Licence | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) unless noted otherwise |

## Read the dictionary

- **Browse (Cologne):** [IEG web interface](https://www.sanskrit-lexicon.uni-koeln.de/scans/IEGScan/2020/web/webtc/indexcaller.php)
- **Landing page:** [sanskrit-lexicon.github.io/IEG](https://sanskrit-lexicon.github.io/IEG/) — served from [index.html](https://github.com/sanskrit-lexicon/IEG/blob/main/index.html) via GitHub Pages
- **All dictionaries:** [sanskrit-lexicon.github.io](https://sanskrit-lexicon.github.io/)

## What is in this repository

This repo holds the corrections/change-tracking side of IEG; the searchable text is served
on the Cologne site. Contents:

- [index.html](https://github.com/sanskrit-lexicon/IEG/blob/main/index.html) — the GitHub
  Pages landing page (with Schema.org / Open Graph metadata).
- [issues/issue1/](https://github.com/sanskrit-lexicon/IEG/tree/main/issues/issue1) — a
  four-step Python pipeline used to align and merge the CDSL digitisation with the
  Andhrabharati (AB) revision into a single source file:
  [step1.py](https://github.com/sanskrit-lexicon/IEG/blob/main/issues/issue1/step1.py) (align
  CDSL and AB, wrap references in `<ls>` and Latin abbreviations in `<ab>`),
  [step2.py](https://github.com/sanskrit-lexicon/IEG/blob/main/issues/issue1/step2.py),
  [step3.py](https://github.com/sanskrit-lexicon/IEG/blob/main/issues/issue1/step3.py), and
  [step4.py](https://github.com/sanskrit-lexicon/IEG/blob/main/issues/issue1/step4.py)
  (concatenate preface, merged body, and endmatter), driven by
  [redo.sh](https://github.com/sanskrit-lexicon/IEG/blob/main/issues/issue1/redo.sh).

The source `ieg.txt` text itself lives in the shared
[csl-orig](https://github.com/sanskrit-lexicon/csl-orig) repository (`v02/ieg/ieg.txt`), not
here.

## Corrections

Corrections to the dictionary text are never made directly to the generated source: they are
prepared as change files and applied by scripts, following the canonical
[csl-orig correction workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).
Report errors or propose corrections via the
[GitHub issue tracker](https://github.com/sanskrit-lexicon/IEG/issues).

Open work is tracked under the standard CDSL milestones — Dictionary to Book, Digitization
Quality, Major Enhancements, and Structured Data.

## Reuse

Dictionary data is released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
unless otherwise noted. Please cite the Cologne Digital Sanskrit Lexicon and Sircar's original
edition.

_Dr. Mārcis Gasūns_
