# Reference and provenance register

Access date for external comparison sources: **8 November 2026 (Australia/Sydney)**.

## References actually used

1. **Our World in Data. (n.d.). _CO₂ and greenhouse gas emissions_ [Data set and codebook].** Retrieved November 8, 2026, from https://github.com/owid/co2-data/tree/382ee6c662b0ece26e111f263b44c029afad7787
   - Used: `consumption_co2_per_capita`, 2018 country values, 1990–2023 country histories; 2023 latest available consumption-CO₂ year in this download.
   - Unit: tonnes CO₂/person/year, not CO₂-equivalent.
   - Covers consumption-adjusted fossil/industrial CO₂; excludes land-use change and non-CO₂ gases. Population basis: OWID various sources (2024), as recorded in the codebook.
   - Report use: methodology 2.5, results 3.3, Figure 2, References; workbook `Comparison data`, `Comparison history`, `Sources`.
   - `owid_consumption_co2_selected.csv`: exactly extracted selected-country series; `owid-co2-codebook.csv`: downloaded definitions.
   - `comparison_provenance.json`: source URLs, pinned Git SHA, verified original-file SHA256 and scope limitations.

2. **Global Carbon Project. (2025). _Global Carbon Budget 2025_ [Data set].** https://globalcarbonbudget.org/
   - Underlying national consumption-CO₂ source identified in OWID’s codebook and README. Numerical data obtained through OWID; the source website was not used as a separately downloaded numerical file.
   - Citation in results and bibliography credits the original producer as requested by OWID.
   - No unverified paper DOI or individual-author list has been invented.

3. **Our World in Data. (n.d.). _Global Carbon Budget indicator metadata_.** https://github.com/owid/etl/blob/master/etl/steps/data/garden/gcp/2025-11-13/global_carbon_budget.meta.yml
   - Saved as `owid-gcb-metadata.yml`.
   - Used to check fossil/industry coverage, trade adjustment, exclusions and international aviation/shipping treatment; this is supporting metadata, not a second independent data series.

4. **The University of Sydney. (n.d.). _PHYS5033: Australian 345-sector input-output teaching dataset (2018 economy)_ [Course-supplied teaching data].** Labels.xlsx.
   - Existing user-supplied course data used for the personal result. Institutional teaching-file description is provisional bibliography attribution; confirm the exact credited author/publication date on Canvas. The year 2018 describes the economic data, not an assumed publication year.

## Comparison decision

Both national and personal measures use a consumption perspective, but their gas, demand, price and time boundaries differ. Figure 2 separates the personal CO₂-e result from national CO₂ references and explicitly labels the comparison contextual. No percentage below Australia or harmonised all-GHG ranking is claimed. 2018 matches the IO reference year, not the 2025–26 spending period. Country sparklines are individually scaled and their dots mark 2018.

## Word-count record

`word_count.json` records an approximate working count, including main headings/captions/equations and visible text from both figures. The count excludes cover, contents, References and supplementary material; this is not an authoritative statement of Canvas counting rules. `../writing_plan.md` records allocation and unfinished sections.

To rebuild the two figures from the saved source extract and current cached workbook footprint, run `python scripts/build_comparison_figures.py` (pandas, NumPy, openpyxl and Matplotlib). This does not update the Word images automatically and does not download a newer data release. Refresh source extracts and bibliography together if changing the reference year or dataset version.
