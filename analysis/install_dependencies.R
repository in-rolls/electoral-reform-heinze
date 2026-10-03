local_library <- file.path("work", "authors-library")
dir.create(local_library, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(local_library, .libPaths()))
packages <- c(
  "devtools", "dplyr", "estimatr", "readxl", "ggplot2", "gridExtra",
  "modelsummary", "lubridate", "stringr", "readr", "sensemakr", "tidyr",
  "patchwork", "ggplotify", "rdrobust", "xtable", "skimr", "knitr",
  "sandwich", "clubSandwich", "dqrng", "lintr", "styler", "remotes"
)
missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing)) {
  install.packages(missing, lib = local_library, repos = "https://cloud.r-project.org")
}
stopifnot(all(vapply(packages, requireNamespace, logical(1), quietly = TRUE)))
if (!requireNamespace("fwildclusterboot", quietly = TRUE)) {
  remotes::install_github(
    "s3alfisc/fwildclusterboot",
    ref = "336bb574eba169ac0183317f01d0564791d8122f",
    lib = local_library, upgrade = "never", dependencies = NA
  )
}
stopifnot(requireNamespace("fwildclusterboot", quietly = TRUE))
