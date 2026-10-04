# Author-code execution and numerical reproduction

The unedited author pipeline runs to completion with the installed R 4.6.0 after installing missing dependencies into a repository-local library. All 28 deposited LaTeX tables match at their printed numerical precision (2,925 numerical cells), and all 161 checked labels in main Figures 3–6 match. This is reproduction of the deposited estimates, not validation of their measurement or causal interpretation.

## Attempts and environment

1. `work/authors-unchanged/code/`: ran `Rscript master.R` without edits or library overrides. It stopped in `helpers.R` because `modelsummary` was absent and the default system library was not writable. The preserved log is `results/authors/unchanged.log`.
2. Installed missing `modelsummary` and `skimr` plus dependencies into `work/authors-library` using `install.packages(..., repos="https://cloud.r-project.org")`. The first network-restricted attempt could not contact CRAN; the network-enabled retry succeeded. Both install logs are retained. The author's `devtools::install_local("pwtest-package")` then installed the deposited `pwtest` package into that local library without an author-code edit.
3. Ran unchanged `master.R` with `R_LIBS_USER` set to the local library; `clean.R`, `main.R`, and all of `appendix.R` completed. See `results/authors/local-library.log`.
4. Ran `Rscript scripts/run_authors.R`, which copies original inputs and code to `work/authors-reproducible`, removes copied result artifacts, creates empty result directories, and sources unchanged `master.R`. This prevents deposited files being mistaken for regenerated results. It then sources `main.R` once more to capture its data frames before appendix objects overwrite their names. It exports comparisons and asserts equality of transcribed main-figure labels. A subsequent main-only execution tested the added complete Figure 3 label comparisons; see `figure-check.log`. The final formatted runner was then executed end to end; see `final-run.log`.

The author README specifies R 4.4.3 on macOS Sonoma 14.3.1. This machine has only R 4.6.0 installed. No R 4.4.3 container was used. The Python verification tier was separately run in the standard Python 3.14 Docker image. Thus this is **not** an exact reproduction of the author's software environment. The recorded environment is R 4.6.0, macOS 27.0.1, estimatr 1.0.6, modelsummary 2.6.0, ggplot2 4.0.3, and the deposited pwtest 0.0.0.9000. Complete versions are in `session-info.txt` and `package-versions.csv`.

No author-code changes were required. Byte comparisons confirmed that every file under the working copy's `code/` still matches `original/code/`. The regenerated `survey_experiment_clean.csv` also matches the deposited file byte for byte.

## Coverage and limits

| Artifact | Check | Result |
|---|---|---|
| Main Figure 2 | Regenerated election-frequency graph; exported every nonzero month/year/regime count | Completed; raster bars were not independently converted back into numerical counts |
| Main Figure 3 | 112 labels: two means, two mean SEs, difference, difference SE, N, p-value for 14 covariates | All match printed precision |
| Main Figure 4 | Five outcomes × two means and difference | All 15 labels match |
| Main Figure 5 | Thirteen outcomes × indirect mean and difference | All 26 labels match |
| Main Figure 6 | Two adjusted effects, two control means, four group means | All 8 labels match |
| Appendix tables B1–B2, C1–C5, D1–D16, D18–D19, F2–F4 | Every numerical cell in deposited TeX table bodies, including coefficients, SEs, N, fit statistics and displayed tests | 28/28 tables and 2,925/2,925 numerical cells match |
| Appendix figures C1, D1–D3, G1, H1–H2 | Regeneration from empty result directories | 7/7 generated; no comprehensive independent numerical verification of raster labels or plotted coordinates |

The package deposits 12 PNG figures total. Main Figure 1 and appendix items without generating code or a deposited generated artifact are outside the automated comparison. Printed precision is the strongest numerical claim available for deposited tables and raster labels; it does not establish identity of unrounded original estimates. Significance stars, model labels, and all graphical styling were not included in the numerical-cell comparison. Main-figure label values were transcribed from the deposited figures; OCR transcripts are retained for traceability. These transcriptions are not independent raw-data estimates.

`artifact-comparison.csv` enumerates every deposited generated artifact. `main-figure-label-comparison.csv` records the published label, the reproduced unrounded value, its precision, and the match result. Individual `*.tex-numeric-cells.csv` files retain ordered original and reproduced values. Table parsing ignores TeX layout commands after row terminators: otherwise old `cmidrule` indices would misleadingly appear as changed numbers under the newer renderer.

## Confirmed arithmetic issue

`helpers.R:51–52` computes balance-table group mean SEs using the entire treatment-group denominator even when the outcome is missing. Seven group-variable combinations are affected. In main Figure 3, the indirect population mean SE is reproduced as **223.518**, using SD/√370; the outcome is observed for **369** indirect councils, giving the corrected SE **223.821**. The other six corrections do not change the printed three-decimal values. This changes a descriptive mean SE, not the difference estimate, its regression SE, its p-value, or the substantive balance conclusion. The headline function `run_regressions` uses the nonmissing denominator correctly. Table C4 uses regressions and is not produced by this helper.

Full old/new SEs and denominators are in `balance-mean-se-denominator-audit.csv`. The original published pipeline remains unchanged; corrections are separate audit calculations.

## Warnings and verification

Execution generated package deprecation warnings, ggplot scale replacement warnings, a manual-fill-scale mismatch, missing observations in the establishment-date histogram, and gridGraphics contour-label warnings. Appendix sensitivity plots may differ visually because the renderer reports that it cannot emulate contour labels. Modern modelsummary/tinytable changes table layout code and warns about noncontiguous grouping columns. None of these warnings prevented execution or changed the verified printed numerical table cells. The full warnings are retained in `warnings.txt`; figures have not been claimed pixel-identical.

Local verification completed: repeated full unedited master pipelines in isolated working copies, including the final formatted runner; styler formatting and zero lintr findings under the repository 120-column configuration; source-file byte comparisons; SHA-256 verification of all 113 original files against the preserved manifest; regenerated clean experiment-data byte comparison; all 28 numeric table comparisons; all 161 main-figure label assertions; and the balance SE denominator inequality check. Formatting and lint results are in `style-lint.log`; file hashes are in `original-immutability-check.csv`. Run `Rscript scripts/run_authors.R` from the repository root to regenerate these outputs with the installed packages. On another machine, the author's helper attempts to install any missing packages, so a writable R library and CRAN access are required.
