# Supplementary calculation evidence

Source: `Labels.xlsx`, based on the user's GitHub upload `980c11c`, with repaired local formula links and documented error fixes. The matrix method remains Excel MUNIT/MINVERSE/MMULT. A retains its algebraically equivalent column-normalisation formulas.

These PNG files are **snapshots of actual linked worksheet print views rendered by LibreOffice Calc**, not screenshots of a Microsoft Excel application window. They show real workbook values/formulas, not re-created illustrative tables. Small matrix views are explicitly excerpts of the full 345-sector arrays.

| Figure | Worksheet | Evidence |
| --- | --- | --- |
| S1 | Evidence S1 | All personal annual expenditure items and total |
| S2 | Evidence S2 | All 40 expenditure allocation rows |
| S3 | Evidence S3 | Nonzero entries in the 345-sector final-demand vector |
| S4 | Evidence S4 | MUNIT/MINVERSE, A and L formulas and 5-by-5 excerpts |
| S5 | Evidence S5 | MMULT q/m/induced-output formulas, contributions, total |
| S6 | Evidence S6 | Expenditure/sector checks and numerical reconciliation |
| S7 | Evidence S7 | Provisional top-10 consumption-sector results |

The same views are available in `Calculation_Evidence.pdf` and inserted in the Word supplementary section. `validation.json` records an independent read-only audit of the current workbook. Baseline: AUD 29,760 and 9.543 t CO2-e/person/year (provisional).

## Repairs before capture

- Xhat and Xhat inverse array formulas referred to another workbook (`[1]`). They now refer to sheets inside Labels.xlsx.
- Footprint sectors columns I/J contained 690 cached `#VALUE!` errors. Each induced-output cell now uses the Excel array formula `MMULT(L_row, y)`; its dependent emitting-sector contribution recalculates correctly.
- q/m contributions link to the user's q matrix/m matrix, rather than maintaining parallel calculations.
- Old text about a Python-generated numeric L snapshot and the destructive generator have been removed. The new validator never writes the workbook.

All supplied input worksheet XML (including the user's Satellite sum row) is preserved. Corrections do not change the provisional total. The baseline ranking is not automatically re-sorted after future spending changes.

## Remaining assessment work

The required Australian and other-country per-capita comparison is **not yet completed**. No figure here demonstrates that comparison. Ensure compatible CO2-e/CO2, consumption/territorial, year and system boundaries before adding it. Price-year conversion, purchaser/basic-price valuation, insurance service-charge valuation and household direct combustion remain limitations.

### 8 November update

The main report now contains a contextual country comparison (Figure 2); national consumption-based CO2 data and source records are in `Comparison data`, `Comparison history`, `Sources`, and `../sources/`. This does not resolve a harmonised all-GHG comparison. Existing evidence images are historical 7 November captures; their “comparison pending” statements describe that capture stage, not the latest report. `validation.json` has been refreshed for the current workbook; its SHA256 identifies the workbook audited.
