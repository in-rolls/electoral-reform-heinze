# Run from the repository root with Rscript scripts/run_authors.R.
args <- commandArgs(trailingOnly = FALSE)
script_arg <- sub("^--file=", "", args[grepl("^--file=", args)])
root <- normalizePath(file.path(dirname(script_arg), ".."))
local_library <- file.path(root, "work", "authors-library")
dir.create(local_library, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(local_library, .libPaths()))
options(repos = c(CRAN = "https://cloud.r-project.org"))
output <- file.path(root, "results", "authors")
dir.create(output, recursive = TRUE, showWarnings = FALSE)
run_directory <- file.path(root, "work", "authors-reproducible")
dir.create(run_directory, recursive = TRUE, showWarnings = FALSE)
stopifnot(file.copy(list.files(file.path(root, "original"), full.names = TRUE),
  run_directory,
  recursive = TRUE, overwrite = TRUE
))
# Remove copied artifacts so that coverage cannot count stale deposited outputs.
unlink(list.files(file.path(run_directory, "results"), full.names = TRUE), recursive = TRUE)
dir.create(file.path(run_directory, "results", "tables"), recursive = TRUE)
dir.create(file.path(run_directory, "results", "figures"), recursive = TRUE)
setwd(file.path(run_directory, "code"))
start_time <- Sys.time()
source("master.R")
writeLines(capture.output(sessionInfo()), file.path(output, "session-info.txt"))
writeLines(capture.output(warnings()), file.path(output, "warnings.txt"))
package_versions <- as.data.frame(installed.packages()[, c("Package", "Version", "LibPath", "Built")])
write.csv(package_versions, file.path(output, "package-versions.csv"), row.names = FALSE)
writeLines(
  c(
    paste("Started:", start_time), paste("Finished:", Sys.time()),
    "Original code edits: none", paste("R:", R.version.string)
  ),
  file.path(output, "execution-status.txt")
)

# Capture main-figure source numbers before appendix objects replace their names.
source("main.R")
exports <- list(
  figure3_balance = balancetable, figure4_authority = results,
  figure5_formal_capture = results1, figure5_informal_capture = results2,
  figure6_experiment = results_df, figure6_group_means = mean_values
)
exports$figure2_election_counts <- as.data.frame(with(
  elite_df,
  table(sarpanch_election_year, sarpanch_election_month, direct)
))
exports$figure2_election_counts <- subset(exports$figure2_election_counts, Freq > 0)
for (name in names(exports)) {
  write.csv(exports[[name]], file.path(output, paste0(name, ".csv")), row.names = FALSE)
}

numeric_cells <- function(path) {
  lines <- readLines(path, warn = FALSE)
  lines <- lines[grepl("&", lines, fixed = TRUE) & grepl("\\\\", lines, fixed = TRUE)]
  rows <- lapply(lines, function(line) {
    line <- strsplit(line, "\\\\", fixed = TRUE)[[1]][1]
    cells <- strsplit(line, "&", fixed = TRUE)[[1]][-1]
    lapply(cells, function(cell) {
      matches <- regmatches(cell, gregexpr("[-+]?[0-9]+(?:\\.[0-9]+)?(?:[eE][-+]?[0-9]+)?", cell, perl = TRUE))[[1]]
      as.numeric(matches)
    })
  })
  unlist(rows, use.names = FALSE)
}
original_results <- file.path(root, "original", "results")
regenerated_results <- file.path(run_directory, "results")
files <- list.files(original_results, recursive = TRUE)
comparison <- lapply(files, function(file) {
  original_path <- file.path(original_results, file)
  regenerated_path <- file.path(regenerated_results, file)
  exists <- file.exists(regenerated_path)
  is_table <- grepl("\\.tex$", file)
  old <- if (is_table) numeric_cells(original_path) else numeric()
  new <- if (is_table && exists) numeric_cells(regenerated_path) else numeric()
  equal_length <- length(old) == length(new)
  difference <- if (is_table && exists && equal_length) abs(old - new) else NA_real_
  data.frame(
    artifact = file, regenerated = exists, numeric_values_original = length(old),
    numeric_values_reproduced = length(new),
    numeric_values_different = if (is_table && equal_length) sum(difference > 1e-12) else NA_integer_,
    max_numeric_difference = if (is_table && equal_length && length(difference)) max(difference) else NA_real_,
    status = if (!exists) {
      "not_generated"
    } else if (!is_table) {
      "regenerated_raster_numeric_check_separate"
    } else if (!equal_length) {
      "cell_count_differs"
    } else if (any(difference > 1e-12)) {
      "numeric_difference"
    } else {
      "all_printed_numeric_cells_match"
    }
  )
})
write.csv(do.call(rbind, comparison), file.path(output, "artifact-comparison.csv"), row.names = FALSE)
for (file in files[grepl("\\.tex$", files)]) {
  old <- numeric_cells(file.path(original_results, file))
  new <- numeric_cells(file.path(regenerated_results, file))
  if (length(old) == length(new)) {
    cells <- data.frame(cell = seq_along(old), deposited = old, reproduced = new, difference = new - old)
    write.csv(cells, file.path(output, paste0(basename(file), "-numeric-cells.csv")), row.names = FALSE)
  }
}
file.copy(file.path(run_directory, "results"), output, recursive = TRUE, overwrite = TRUE)

# Values transcribed from deposited main-figure labels; OCR transcripts are retained.
figure_checks <- list()
check_values <- function(figure, variable, statistic, published, reproduced, digits = 3L) {
  data.frame(
    figure = figure, variable = variable, statistic = statistic,
    published = published, reproduced = reproduced, digits = digits,
    matches_printed_precision = round(reproduced, digits) == published
  )
}
figure_checks[[1]] <- check_values(
  "4", results$dependent_var, "indirect_mean",
  c(.178, .259, .211, .583, .617), results$indirect_mean
)
figure_checks[[2]] <- check_values(
  "4", results$dependent_var, "direct_mean",
  c(.329, .311, .325, .665, .748), results$direct_mean
)
figure_checks[[3]] <- check_values(
  "4", results$dependent_var, "ATE",
  c(.151, .052, .114, .082, .132), results$ATE
)
figure_checks[[4]] <- check_values(
  "5_formal", results1$dependent_var, "indirect_mean",
  c(.232, .289, .357, .334, .168, .511), results1$indirect_mean
)
figure_checks[[5]] <- check_values(
  "5_formal", results1$dependent_var, "ATE",
  c(.098, .154, .160, .155, .119, .105), results1$ATE
)
figure_checks[[6]] <- check_values(
  "5_informal", results2$dependent_var, "indirect_mean",
  c(.409, .233, .131, .168, .205, .210, .193), results2$indirect_mean
)
figure_checks[[7]] <- check_values(
  "5_informal", results2$dependent_var, "ATE",
  c(-.281, -.207, -.083, -.052, -.057, -.180, -.138), results2$ATE
)
figure_checks[[8]] <- check_values(
  "6", results_df$Independent_Var, "ATE",
  c(.049, .139), results_df$ATE
)
figure_checks[[9]] <- check_values(
  "6", results_df$Independent_Var, "control_mean",
  c(.658, .605), results_df$Mean_Indep_0
)
figure_checks[[10]] <- check_values(
  "6", as.character(mean_values$sarpanchgendercaste_combination), "group_mean",
  c(.58, .74, .63, .77), mean_values$mean_value, 2L
)
figure_check <- do.call(rbind, figure_checks)
write.csv(figure_check, file.path(output, "main-figure-label-comparison.csv"), row.names = FALSE)
stopifnot(all(figure_check$matches_printed_precision))

balance_se <- do.call(rbind, lapply(covariates_for_balance, function(variable) {
  do.call(rbind, lapply(0:1, function(group) {
    outcome <- elite_df[elite_df$direct == group, variable]
    published_se <- sd(outcome, na.rm = TRUE) / sqrt(length(outcome))
    valid_n <- sum(!is.na(outcome))
    corrected_se <- sd(outcome, na.rm = TRUE) / sqrt(valid_n)
    data.frame(
      variable = variable, direct = group, all_group_n = length(outcome),
      nonmissing_n = valid_n, published_se = published_se,
      corrected_se = corrected_se,
      published_printed = sprintf("%.3f", published_se),
      corrected_printed = sprintf("%.3f", corrected_se),
      changes_printed_value = round(published_se, 3) != round(corrected_se, 3)
    )
  }))
}))
write.csv(balance_se, file.path(output, "balance-mean-se-denominator-audit.csv"), row.names = FALSE)
stopifnot(all(balance_se$corrected_se >= balance_se$published_se))

figure3_published <- read.csv(text = "direct_mean,direct_se,indirect_mean,indirect_se,difference,difference_se,n,p
1.308,.049,1.238,.033,.070,.059,604,.239
3262.064,727.367,3024.707,223.518,237.357,761.025,603,.755
.166,.008,.166,.006,0,.010,599,.999
20.831,.820,20.622,.617,.209,1.026,604,.838
.826,.133,.758,.085,.069,.157,604,.664
40.894,7.643,38.092,5.621,2.802,9.487,604,.768
.300,.030,.314,.024,-.013,.039,603,.735
.111,.021,.124,.017,-.013,.027,604,.622
.244,.028,.266,.023,-.022,.036,603,.545
.970,.011,.965,.010,.005,.015,601,.721
.453,.033,.503,.026,-.050,.042,604,.234
.350,.031,.381,.025,-.031,.040,604,.446
.338,.031,.292,.024,.046,.039,604,.241
.312,.030,.327,.024,-.015,.039,604,.699")
figure3_raw <- run_ate_for_multiple_outcomes(elite_df, covariates_for_balance, "direct")
figure3_actual <- figure3_raw[, c(
  "mean_treated", "se_treated", "mean_control", "se_control",
  "coef_treatment.treatment", "se_treatment.treatment", "total_n", "p_value.treatment"
)]
figure3_checks <- do.call(rbind, lapply(seq_len(ncol(figure3_published)), function(index) {
  check_values(
    "3", covariates_for_balance, names(figure3_published)[index],
    figure3_published[[index]], figure3_actual[[index]]
  )
}))
figure_check <- rbind(figure_check, figure3_checks)
write.csv(figure_check, file.path(output, "main-figure-label-comparison.csv"), row.names = FALSE)
stopifnot(all(figure_check$matches_printed_precision))
