.libPaths(c("work/authors-library", .libPaths()))
options(warn = 1)

output_dir <- "results/inference"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)
elite <- read.csv("original/data/analysis/elite_survey.csv")
citizen <- read.csv("original/data/analysis/citizen_survey.csv")
admin <- read.csv("original/data/analysis/resignation_admin.csv")
stopifnot(nrow(elite) == 604L, !anyDuplicated(elite$r_villageid))
elite$cohort <- sprintf(
  "%04d-%02d", elite$sarpanch_election_year, elite$sarpanch_election_month
)
elite$month_index <- (elite$sarpanch_election_year - 2015) * 12 +
  elite$sarpanch_election_month - 1
matched <- match(citizen$r_villageid, elite$r_villageid)
stopifnot(!anyNA(matched), all(citizen$direct == elite$direct[matched]))
for (field in c("cohort", "month_index", "sarpanch_election_year")) {
  citizen[[field]] <- elite[[field]][matched]
}
stopifnot(!anyNA(elite$month_index))

elite_outcomes <- c(
  "most_influential_gd", "prop_speakingtime_sarpanch", "i_decide_masik_sabha",
  "sarpanch_maratha", "avg_prop_land_held_sarpanch_caste", "sarpanch_male",
  "sarpanch_land_own_name", "three_four_wheeler", "pacca_house",
  "sarpanch_uncontested", "resignation", "rich_landowner_influences_gp"
)
citizen_outcomes <- c(
  "sarpanch_nominate_BDO", "sarpanch_inauguralevents", "other_nominate_BDO",
  "formersarpanch_otherperson_inauguralevents", "resignation_reported"
)
outcomes <- c(elite_outcomes, citizen_outcomes, "resigned")

extract_estimate <- function(fit, outcome, specification, dataset) {
  index <- match("direct", names(fit$coefficients))
  data.frame(
    outcome = outcome, dataset = dataset, specification = specification,
    n = fit$nobs, estimate = fit$coefficients[index],
    se = fit$std.error[index], df = fit$df[index],
    p = fit$p.value[index], lower = fit$conf.low[index],
    upper = fit$conf.high[index], row.names = NULL
  )
}

estimates <- list()
bootstraps <- list()
leaveouts <- list()
ranks <- list()
nested <- list()
cluster_counts <- list()
for (outcome in outcomes) {
  dataset <- if (outcome %in% citizen_outcomes) "citizen" else "elite"
  if (outcome == "resigned") dataset <- "admin"
  d <- switch(dataset, elite = elite, citizen = citizen, admin = admin)
  d <- d[complete.cases(d[c(outcome, "direct")]), ]
  d$y <- d[[outcome]]
  clustered <- dataset == "citizen"
  baseline <- if (clustered) {
    estimatr::lm_robust(
      y ~ direct, data = d, clusters = r_villageid, se_type = "CR2"
    )
  } else {
    estimatr::lm_robust(y ~ direct, data = d, se_type = "HC2")
  }
  estimates[[length(estimates) + 1L]] <- extract_estimate(
    baseline, outcome,
    if (clustered) "baseline_GP_CR2" else "baseline_HC2", dataset
  )
  raw_difference <- mean(d$y[d$direct == 1]) - mean(d$y[d$direct == 0])
  stopifnot(abs(coef(baseline)["direct"] - raw_difference) < 1e-10)
  if (dataset == "admin") next

  cohort_fit <- estimatr::lm_robust(
    y ~ direct, data = d, clusters = cohort, se_type = "CR2"
  )
  estimates[[length(estimates) + 1L]] <- extract_estimate(
    cohort_fit, outcome, "election_month_CR2", dataset
  )
  for (specification in c("year_FE", "linear_month")) {
    formula <- if (specification == "year_FE") {
      y ~ direct + factor(sarpanch_election_year)
    } else {
      y ~ direct + month_index
    }
    fit <- if (clustered) {
      estimatr::lm_robust(
        formula, data = d, clusters = r_villageid, se_type = "CR2"
      )
    } else {
      estimatr::lm_robust(formula, data = d, se_type = "HC2")
    }
    estimates[[length(estimates) + 1L]] <- extract_estimate(
      fit, outcome, paste0(specification, "_baseline_SE"), dataset
    )
    fit <- estimatr::lm_robust(
      formula, data = d, clusters = cohort, se_type = "CR2"
    )
    estimates[[length(estimates) + 1L]] <- extract_estimate(
      fit, outcome, paste0(specification, "_month_CR2"), dataset
    )
  }

  model <- lm(y ~ direct, data = d)
  independent_cr2 <- clubSandwich::coef_test(
    model, vcov = "CR2", cluster = d$cohort, test = "Satterthwaite",
    coefs = "direct"
  )
  stopifnot(
    abs(independent_cr2$SE - cohort_fit$std.error["direct"]) < 1e-9,
    abs(independent_cr2$p_Satt - cohort_fit$p.value["direct"]) < 1e-9
  )
  set.seed(20261002)
  dqrng::dqset.seed(20261002)
  boot <- fwildclusterboot::boottest(
    model, param = "direct", clustid = "cohort", B = 9999,
    conf_int = TRUE, type = "rademacher", impose_null = TRUE,
    bootstrap_type = "fnw11", engine = "R", nthreads = 1
  )
  stopifnot(boot$N == nrow(d), boot$boot_iter == 9999)
  bootstraps[[outcome]] <- data.frame(
    outcome = outcome, n = boot$N, clusters = length(unique(d$cohort)),
    estimate = boot$point_estimate, p = boot$p_val,
    monte_carlo_se = sqrt(boot$p_val * (1 - boot$p_val) / boot$boot_iter),
    lower = boot$conf_int[1], upper = boot$conf_int[2],
    draws = boot$boot_iter, seed = 20261002,
    weights = "Rademacher", null_imposed = TRUE, algorithm = "fnw11"
  )

  cohort_matrix <- model.matrix(~ factor(cohort), data = d)
  full_matrix <- cbind(cohort_matrix, direct = d$direct)
  cohort_rank <- qr(cohort_matrix)$rank
  full_rank <- qr(full_matrix)$rank
  ranks[[outcome]] <- data.frame(
    outcome = outcome, n = nrow(d), cohorts = ncol(cohort_matrix),
    cohort_rank = cohort_rank, full_columns = ncol(full_matrix),
    full_rank = full_rank,
    treatment_identified = full_rank > cohort_rank
  )
  stopifnot(full_rank == cohort_rank)

  cohort_sizes <- as.data.frame(table(d$cohort, d$direct))
  names(cohort_sizes) <- c("cohort", "direct", "n")
  cohort_sizes$outcome <- outcome
  cluster_counts[[outcome]] <- cohort_sizes[cohort_sizes$n > 0, ]
  if (clustered) {
    by_gp <- split(d$cohort, d$r_villageid)
    cohort_per_gp <- vapply(by_gp, function(x) length(unique(x)), integer(1))
    stopifnot(all(cohort_per_gp == 1L))
    one_way <- sandwich::vcovCL(
      model, cluster = d$cohort, type = "HC1", cadjust = TRUE
    )
    two_way <- sandwich::vcovCL(
      model, cluster = d[c("cohort", "r_villageid")],
      type = "HC1", cadjust = TRUE
    )
    discrepancy <- max(abs(one_way - two_way))
    stopifnot(discrepancy < 1e-10)
    nested[[outcome]] <- data.frame(
      outcome = outcome, max_covariance_discrepancy = discrepancy,
      gp_clusters = length(unique(d$r_villageid)),
      month_clusters = length(unique(d$cohort))
    )
  }
  for (excluded in sort(unique(d$cohort))) {
    reduced <- d[d$cohort != excluded, ]
    fit <- if (clustered) {
      estimatr::lm_robust(
        y ~ direct, data = reduced, clusters = r_villageid, se_type = "CR2"
      )
    } else {
      estimatr::lm_robust(y ~ direct, data = reduced, se_type = "HC2")
    }
    row <- extract_estimate(
      fit, outcome, "leave_one_month_out_baseline_SE", dataset
    )
    row$excluded_cohort <- excluded
    row$excluded_n <- nrow(d) - nrow(reduced)
    leaveouts[[length(leaveouts) + 1L]] <- row
  }
  message("Completed: ", outcome)
}

write_result <- function(rows, name) {
  result <- do.call(rbind, rows)
  write.csv(
    result, file.path(output_dir, paste0(name, ".csv")), row.names = FALSE
  )
  invisible(result)
}
all_estimates <- write_result(estimates, "estimates")
all_bootstraps <- write_result(bootstraps, "wild_bootstrap")
all_leaveouts <- write_result(leaveouts, "leave_one_month_out")
write_result(ranks, "cohort_rank")
write_result(nested, "nested_clusters")
write_result(cluster_counts, "cluster_sizes")
year_support <- as.data.frame(table(elite$sarpanch_election_year, elite$direct))
names(year_support) <- c("election_year", "direct", "n_gp")
write.csv(
  year_support, file.path(output_dir, "year_support.csv"), row.names = FALSE
)
summarize_leaveouts <- function(d) {
  data.frame(
    outcome = d$outcome[1], minimum = min(d$estimate),
    maximum = max(d$estimate),
    cohort_at_minimum = d$excluded_cohort[which.min(d$estimate)],
    cohort_at_maximum = d$excluded_cohort[which.max(d$estimate)],
    minimum_p = min(d$p), maximum_p = max(d$p)
  )
}
leaveout_summary <- lapply(
  split(all_leaveouts, all_leaveouts$outcome), summarize_leaveouts
)
write_result(leaveout_summary, "leaveout_ranges")

stopifnot(
  nrow(all_estimates) == 103L,
  nrow(all_bootstraps) == 17L,
  all(is.finite(all_estimates$estimate)),
  all(all_estimates$lower <= all_estimates$estimate),
  all(all_estimates$upper >= all_estimates$estimate),
  all(all_bootstraps$p >= 0 & all_bootstraps$p <= 1)
)
capture.output(sessionInfo(), file = file.path(output_dir, "session-info.txt"))
writeLines(
  paste(
    "PASS: row conservation, treatment join, raw mean identity,",
    "bootstrap sample/draws, independent CR2, cohort rank,",
    "nested covariance identity,",
    "result completeness."
  ),
  file.path(output_dir, "validation.txt")
)
