.libPaths(c("work/authors-library", .libPaths()))
options(warn = 1)
dir.create("results/recent", recursive = TRUE, showWarnings = FALSE)
write_result <- function(x, name) {
  write.csv(x, file.path("results/recent", paste0(name, ".csv")),
    row.names = FALSE, na = ""
  )
}

elite <- read.csv("original/data/analysis/elite_survey.csv")
citizen <- read.csv("original/data/analysis/citizen_survey.csv")
elite$cohort <- sprintf("%04d-%02d", elite$sarpanch_election_year, elite$sarpanch_election_month)
matched <- match(citizen$r_villageid, elite$r_villageid)
stopifnot(!anyNA(matched), all(citizen$direct == elite$direct[matched]))
for (field in c("cohort", "sarpanch_election_year")) {
  citizen[[field]] <- elite[[field]][matched]
}
outcomes <- subset(read.csv("results/audit/raw-means.csv"), source != "admin")
definitions <- c("drop_early_indirect", "since_2018", "since_2019", "since_2020", "since_2021")
retain <- function(data, specification) {
  if (specification == "drop_early_indirect") {
    data$direct == 1 | data$sarpanch_election_year >= 2020
  } else {
    data$sarpanch_election_year >= as.integer(sub("since_", "", specification))
  }
}
support <- list()
estimates <- list()
for (specification in definitions) {
  council_data <- elite[retain(elite, specification), ]
  support[[specification]] <- data.frame(
    specification = specification, direct = 0:1,
    councils = vapply(0:1, function(arm) sum(council_data$direct == arm), integer(1)),
    election_months = vapply(0:1, function(arm) {
      length(unique(council_data$cohort[council_data$direct == arm]))
    }, integer(1))
  )
  for (i in seq_len(nrow(outcomes))) {
    variable <- outcomes$variable[i]
    source <- outcomes$source[i]
    data <- if (source == "elite") elite else citizen
    data <- data[retain(data, specification), ]
    complete <- data[!is.na(data[[variable]]), ]
    row <- data.frame(specification = specification, source = source, variable = variable)
    for (arm in 0:1) {
      arm_data <- complete[complete$direct == arm, ]
      prefix <- if (arm == 0) "indirect" else "direct"
      row[[paste0(prefix, "_total")]] <- sum(data$direct == arm)
      row[[paste0(prefix, "_n")]] <- nrow(arm_data)
      row[[paste0(prefix, "_sum")]] <- sum(arm_data[[variable]])
      row[[paste0(prefix, "_mean")]] <- if (nrow(arm_data)) mean(arm_data[[variable]]) else NA_real_
      row[[paste0(prefix, "_gp")]] <- length(unique(arm_data$r_villageid))
      row[[paste0(prefix, "_months")]] <- length(unique(arm_data$cohort))
    }
    row$difference <- row$direct_mean - row$indirect_mean
    row$status <- if (min(row$indirect_gp, row$direct_gp) < 2) "insufficient_support" else "estimated"
    if (row$status == "estimated") {
      formula <- reformulate("direct", variable)
      baseline <- if (source == "citizen") {
        estimatr::lm_robust(formula, data = complete, clusters = r_villageid, se_type = "CR2")
      } else {
        estimatr::lm_robust(formula, data = complete, se_type = "HC2")
      }
      month <- estimatr::lm_robust(formula, data = complete, clusters = cohort, se_type = "CR2")
      stopifnot(abs(coef(baseline)["direct"] - row$difference) < 1e-12)
      for (method in c("baseline", "month")) {
        fit <- if (method == "baseline") baseline else month
        row[[paste0(method, "_se")]] <- unname(fit$std.error["direct"])
        row[[paste0(method, "_df")]] <- unname(fit$df["direct"])
        row[[paste0(method, "_p")]] <- unname(fit$p.value["direct"])
        row[[paste0(method, "_low")]] <- unname(fit$conf.low["direct"])
        row[[paste0(method, "_high")]] <- unname(fit$conf.high["direct"])
      }
      model <- lm(formula, data = complete)
      independent <- clubSandwich::coef_test(
        model,
        vcov = "CR2", cluster = complete$cohort, test = "Satterthwaite", coefs = "direct"
      )
      stopifnot(abs(independent$p_Satt - row$month_p) < 1e-9)
      set.seed(20261003)
      dqrng::dqset.seed(20261003)
      bootstrap <- fwildclusterboot::boottest(
        model,
        param = "direct", clustid = "cohort", B = 9999,
        conf_int = TRUE, type = "rademacher", impose_null = TRUE,
        bootstrap_type = "fnw11", engine = "R", nthreads = 1
      )
      row$wild_p <- bootstrap$p_val
      row$wild_low <- bootstrap$conf_int[1]
      row$wild_high <- bootstrap$conf_int[2]
      row$wild_draws <- bootstrap$boot_iter
      row$wild_seed <- 20261003
      row$wild_full_enumeration <- row$wild_draws == 2^(row$direct_months + row$indirect_months)
      row$wild_mc_se <- if (row$wild_full_enumeration) {
        0
      } else {
        sqrt(row$wild_p * (1 - row$wild_p) / row$wild_draws)
      }
    }
    estimates[[length(estimates) + 1L]] <- row
  }
  message("Completed ", specification)
}
write_result(dplyr::bind_rows(support), "support")
write_result(dplyr::bind_rows(estimates), "estimates")

year_rows <- list()
for (source in c("elite", "citizen")) {
  data <- if (source == "elite") elite else citizen
  variables <- if (source == "elite") c("resignation", "sarpanch_uncontested") else "resignation_reported"
  for (year in sort(unique(data$sarpanch_election_year))) {
    for (arm in 0:1) {
      group <- data[data$sarpanch_election_year == year & data$direct == arm, ]
      if (!nrow(group)) next
      for (variable in variables) {
        values <- group[[variable]]
        year_rows[[length(year_rows) + 1L]] <- data.frame(
          source = source, variable = variable, year = year, direct = arm,
          councils = length(unique(group$r_villageid)), total = nrow(group),
          n = sum(!is.na(values)), positive = sum(values, na.rm = TRUE),
          mean = mean(values, na.rm = TRUE)
        )
      }
    }
  }
}
write_result(dplyr::bind_rows(year_rows), "yearly-counts")
early <- subset(elite, direct == 0 & sarpanch_election_year <= 2017)
write_result(as.data.frame(table(
  shared_tenure = early$resignation, unopposed = early$sarpanch_uncontested, useNA = "ifany"
)), "early-cross-tab")
capture.output(sessionInfo(), file = "results/recent/session-info.txt")
