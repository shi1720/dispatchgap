# DispatchGap

An exact, source-linked audit of document-date routes in Revolutionary Networks,
1771–1783. Author: **Shivam Gupta**, Independent Researcher, India.

The research manuscript is *From Dated Ties to Defensible Routes: A Handoff-Feasibility
Audit of Revolutionary Correspondence, 1771–1783*. This repository provides the
completed computational study. Conference acceptance is not claimed.

## What the software establishes

Each contact carries a calendar date and documentary identifier. A modeled route
requires its next author to equal its previous recipient, with a declared minimum
gap between document dates. The software computes exact admissible-pair sets and
provides document sequences for individual queries. It does not establish receipt,
reading, forwarding, or transmission of shared content. Missing archival routes
cannot establish that people were historically disconnected.

The terminal leg is counted when its document is dated inside the window. It is
not required to become available for another hop before the window closes.
Direct contacts therefore remain feasible for every gap. Gap 0 computes a
same-day fixed point; results do not depend on CSV row ordering.

## Reproduce

Python 3.10 or later is required. The analysis and verification have **no external
Python dependencies**. Run from the repository root:

```sh
python3 -m unittest discover -s tests -v
python3 src/analyze.py
python3 src/verify_real.py
python3 src/controls.py
python3 src/build_tables.py
python3 src/query.py --year 1771 --source 250648 --target 128909 --gap 27
python3 src/query.py --year 1771 --source 250648 --target 128909 --gap 28
```

The two queries report feasibility and infeasibility, respectively, with the same
critical threshold of 27 days. Source URLs accompany positive route witnesses.

Optional figure generation:

```sh
python3 -m venv .venv
. .venv/bin/activate
python3 -m pip install -r requirements-plot.txt
python3 src/figures.py
```

The archived analysis was executed with Python 3.12. The figure versions are
specified in `requirements-plot.txt`; statistical tests, trained models, or LLM
calls are not needed to regenerate the numerical results.

## Data and provenance

The included CSV is the unchanged Rotunda release at commit
`dacbbff257a769740c5bf8e25c6fb0a5212bf671`.

SHA-256:
`07efdd2764c1820b652afcac2591429ca1582fbf391ebb6439a8ebceba2e82f0`

Cite the original compilation:

> Rotunda, University of Virginia Press. *Revolutionary Networks: Correspondence
> Metadata, 1771–1783* [dataset]. 2026.
> https://github.com/rotunda-uvap/revolutionary-networks

Its metadata and compilation are CC BY 4.0; see `data/DATA_LICENSE.md` and the
original `data/SOURCE_README.md`. The metadata does not include letter transcripts.
This study supplies analysis of the metadata, not a new edition of the letters.

Normalization excludes 31 rows without both endpoint identifier sets, deduplicates
six repeated identifier tokens within fields, and removes 153 projected
self-contacts. Names are display labels; joins use identifiers. Group documents
are expanded into author-to-recipient pairs sharing one document identifier and
date. These are declared projection choices, not inferred physical deliveries.

## Results

The usable compilation contains 40,659 documents and 5,009 identifiers. Thirteen
annual aggregate graphs admit 3,578,961 non-self source-year pairs. Date-ordered
routes retain 59.78%; seven-day gaps retain 55.45%; thirty-day gaps retain 43.38%.

`results/annual.csv` contains all primary counts. `profiles.csv` reports controlled
document exclusions under a common full-corpus denominator. `date_controls.csv`
contains 20 within-year document-date permutations, seeds 0–19. These controls
are exploratory diagnostics, not historical reconstructions or uncertainty
intervals for lost correspondence. `witnesses.json` records one rule-selected
threshold illustration per year. `real_oracle_checks.json` records nine independent
checks on complete annual graphs; the exhaustive suite checks 55,575 toy
origin-stream-gap cases and validates witnesses.

## Scope and relation to prior work

Temporal reachability and minimum waiting constraints are established methods.
The contribution is this frozen-corpus benchmark, source-linked query workflow,
explicit terminal-leg convention, and controlled reconstruction of how selected
representations change the opportunity graph. Algorithmic priority, actual
information diffusion, postal-time estimation, and patentability are not claimed.
The accompanying literature ledger records primary sources and the limited
novelty search. A literature search cannot prove the universal absence of prior work.

## Licensing and disclosure

Software: MIT, copyright Shivam Gupta, 2026. Data retain their separate original
license. Generative AI assisted literature discovery, software development,
analysis, visualization, and drafting.
