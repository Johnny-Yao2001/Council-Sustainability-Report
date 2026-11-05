# Council-Sustainability-Report

## Report workbook

Use **Labels.xlsx** as the single master Excel workbook for all future expenditure, IO mapping and footprint work. The standalone Resident_Annual_Expenditure.xlsx has been consolidated into this workbook.

- Original inputs: `row labels`, `IntermediateDemand`, `Output`, `Satellite` (preserved).
- `Annual expenditure`: monthly personal amounts and annualisation formulas.
- `Expenditure assumptions`: resident profile, boundaries and unresolved valuation assumptions.
- `Expenditure split`: mixed categories split into explicit allocations to the original sector IDs.
- `IO_345 demand`: all 345 sectors in original order, aggregated personal AUD, provisional AUD-million demand, and linked x/Q.
- `IO_345 table`: labelled 345-by-345 view linked to the supplied intermediate-demand matrix.
- `Validation`: raw, split and mapped totals, sector count and allocation-share checks.

Baseline: AUD 29,760 per person per year; 40 allocation rows. All expenditure and allocation shares are illustrative assumptions. Monthly amounts already represent the individual's share. Source allocation shares must sum to one; validation differences must be zero. Recalculate in Excel after edits. Adding source/split rows requires updating the relevant formula ranges.

The demand vector remains provisional: purchaser/basic-price differences, margins/taxes, insurance service valuation and adjustment to 2018 prices are unresolved. No footprint has been calculated. Do not add retail margins on top of the same product spending or interpret this mapping as a verified basic-price demand vector.

## Provisional footprint calculation

`Labels.xlsx` now includes `A coefficients`, `L inverse`, `Footprint sectors`, `Footprint summary` (top-10 chart) and `Footprint checks`. Baseline provisional IO supply-chain estimate: **9.543 t CO2-e/person/year**. This is not a final, valuation-adjusted inventory. No country comparison or separate household direct-gas combustion estimate has been added.

To refresh the numerical Leontief inverse and chart ranking after changing inputs, run `python scripts/update_footprint.py` from this repository with NumPy and openpyxl installed. Source T/x/Q worksheets are preserved exactly. Excel formulas link the expenditure vector to contributions; **L is a numeric snapshot and must be regenerated after T/x changes**. Reopen/recalculate Excel after edits. Formula errors, allocation-share checks and boundary limitations must be reviewed before final use. Changes to sector labels/IDs require a mapping review. The script checks algebraic consistency; it does not resolve pricing or accounting-boundary assumptions.
