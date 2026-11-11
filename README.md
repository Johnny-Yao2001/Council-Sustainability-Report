# Council Sustainability Report

## Master workbook

Use **Labels.xlsx** for all Excel changes. Original course inputs are `row labels`, `IntermediateDemand`, `Output`, and the first row of `Satellite`. Satellite row 6 contains the user's added emissions sum. Do not overwrite the user's matrix formulas.

Resident: one hypothetical adult in a two-adult shared apartment in Redfern, City of Sydney; no private car; mainly public transport. Period: November 2025–October 2026. Annual personal expenditure: **AUD 29,760**. The 40 split allocations are explicit illustrative assumptions.

- `Annual expenditure`, `Expenditure assumptions`: expenditure, annualisation and personal allocation.
- `Expenditure split`: allocations to original sector IDs; shares per source must total one.
- `IO_345 demand`: all 345 sectors, annual AUD and provisional AUD-million demand.
- `IO_345 table`: labelled view of the supplied 345 × 345 intermediate-demand matrix.
- `Validation`: expenditure, share and sector-count reconciliation.

## Excel matrix workflow (updated to the user's formulas)

1. `𝐗 ̂`: diagonal output matrix, `MUNIT(345) * Output!A1:A345` (array formula).
2. `𝐗 ̂ inverse`: `MINVERSE(Xhat)` (array formula).
3. `A coefficients`: `A_ij = T_ij / x_j`, algebraically equivalent to `MMULT(T, Xhat inverse)`. This sheet retains the user's column-normalisation formulas.
4. `L matrix`: `MINVERSE(MUNIT(345) - A)` (array formula).
5. `q matrix`: `MMULT(Q, Xhat inverse)` (array formula).
6. `m matrix`: `MMULT(q, L)` (array formula).
7. `Footprint sectors`: links to the q and m matrices. Consumption contributions are `m_j * y_j * 1000` in tonnes; induced output uses `MMULT(L_row, y)` and emitting-sector contributions are `q_i * (Ly)_i * 1000`.
8. `Footprint summary`: total and top-10 baseline ranking/chart; re-sort the ranking if spending changes. `Footprint checks`: algebraic checks.

All matrix links are internal to Labels.xlsx. No external workbook is required. Use Excel recalculation; L is **no longer a Python-generated numeric snapshot**. Preserve array ranges (345 × 345 or 1 × 345); do not edit individual spill/output cells. The old `scripts/update_footprint.py` generator has been removed because it would overwrite this workflow.

Run `python scripts/validate_workbook.py` for a **read-only** independent audit (NumPy/openpyxl). It validates saved/cached results after Excel recalculation and never changes formulas. It does not resolve accounting assumptions.

Baseline provisional supply-chain estimate: **9.543 t CO2-e/person/year**. Nominal 2025–26 purchaser spending is applied to 2018 sector intensities. Price conversion, taxes/margins, insurance service valuation and household direct combustion remain unresolved. Do not describe this as a complete inventory or directly compare it with territorial CO2 statistics.

## Calculation evidence

`Evidence S1`–`Evidence S7` in Labels.xlsx are linked, printable evidence views. Their source ranges and actual matrix formulas are identified. They show expenditure, all split allocations, active demand sectors (the full workbook retains 345), matrix construction, q/m/footprint results, validation, and sector hotspots.

The `evidence/` directory contains PNG snapshots exported from those actual spreadsheet views, a PDF of the same views, a read-only audit report, and source/caption notes. These are LibreOffice Calc renderings of the Excel workbook, not Microsoft Excel application-window screenshots. Representative matrix excerpts are explicitly labelled; a whole 345 × 345 matrix is intentionally not shrunk into one image. The Word supplementary section includes these images.

A contextual Australian/international comparison is now provided in Figure 2 (see the 8 November update below). The stricter harmonised all-GHG comparison remains unresolved; the original calculation-evidence images describe the earlier capture stage.

## Australian and international context (8 November 2026)

The latest user Word version (`be4b567`) is the editing baseline; its 14 existing images are retained. Figures 1 and 2 are now real result images. Main-text duplicate tables/template notes and unused optional material have been removed; detailed supporting material remains in Labels.xlsx and the supplementary section. Both report filenames are synchronised with v2.

`Comparison data`, `Comparison history` and `Sources` in **Labels.xlsx** record OWID/Global Carbon Budget national consumption-based CO2 references (2018 primary comparison; 1990–2023 trends; 2023 latest available values retained). All pre-existing worksheet XML/formulas and caches are unchanged. Figure 2 separates the personal CO2-e estimate from the CO2-only national references. This is **contextual comparison**, not a harmonised GHG ranking or a percentage reduction relative to the Australian average. The stricter same-gas/same-boundary comparison remains a limitation.

Figures are in `figures/`. Exact source extract, definitions, URLs, verified source version/SHA256, access date and reference entries are in `sources/`. `writing_plan.md` and `sources/word_count.json` record approximate word count and unfinished sections; the 3,000-word limit remains the target. The older evidence captures retain their original capture date and supplementary provenance; the new comparison is Figure 2 in the main report.


## Completed report (11 November 2026)

The Word report is complete, with APA author–year references and approximately **2,629 words**, including visible main-figure text. Necessary assumptions and limitations are consolidated in Methodology rather than repeated throughout Results and Recommendations. Existing user supplementary images are retained. Cover name, student ID and actual submission date remain to be entered.

A budget-neutral food substitution is documented in the new `Reduction scenario` worksheet of Labels.xlsx and `sources/reduction_scenario.json`: 20% less expenditure on fresh meat, poultry, milk and cheese releases AUD 384, split equally between legumes and vegetables. The modelled footprint changes from 9.543 to 9.018 t CO2e/year, a saving of 0.525 t (5.50%), with annual expenditure unchanged at AUD 29,760. This is a scenario within the same model, not a measured outcome. Original worksheet XML and user matrix formulas are preserved.

See `sources/references_apa7.md` for the bibliography, citation/claim mapping and source-access record, `sources/final_report_checks.md` for rubric coverage, and `writing_plan.md` for final section counts.
