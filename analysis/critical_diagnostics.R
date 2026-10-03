.libPaths(c("work/authors-library", .libPaths()))
suppressPackageStartupMessages({
  library(dplyr)
  library(estimatr)
  library(sensemakr)
})

dir.create("results/critical", recursive = TRUE, showWarnings = FALSE)
write_result <- function(data, name) {
  write.csv(data, file.path("results/critical", paste0(name, ".csv")),
    row.names = FALSE, na = ""
  )
}

elite <- read.csv("original/data/analysis/elite_survey.csv")
citizen <- read.csv("original/data/analysis/citizen_survey.csv")
controls <- c(
  "number_villages_GP", "total_population_gp", "overall_percent_SC_gp",
  "km_from_block_office", "total_time_from_block_office", "speed_to_block_office",
  "pilgrimage_sites", "historic_sites", "economic_opportunities",
  "all_villages_electricity_grid", "reserved_women", "reserved_obc", "reserved_sc"
)
citizen <- left_join(citizen, select(elite, r_villageid, all_of(controls)),
  by = "r_villageid", relationship = "many-to-one"
)
stopifnot(nrow(citizen) == 3658)
outcomes <- read.csv("results/audit/raw-means.csv") |>
  filter(source != "admin")
datasets <- list(elite = elite, citizen = citizen)

partial_r_squared <- function(full, reduced) {
  (sum(resid(reduced)^2) - sum(resid(full)^2)) / sum(resid(reduced)^2)
}

benchmark_rows <- list()
bound_rows <- list()
for (i in seq_len(nrow(outcomes))) {
  variable <- outcomes$variable[i]
  data <- datasets[[outcomes$source[i]]]
  formula <- reformulate(c("direct", controls), variable)
  model <- lm(formula, data = data)
  observed <- model.frame(model)
  reduced_controls <- setdiff(controls, "reserved_women")
  treatment_model <- lm(reformulate(controls, "direct"), data = observed)
  treatment_reduced <- lm(reformulate(reduced_controls, "direct"), data = observed)
  outcome_reduced <- lm(reformulate(c("direct", reduced_controls), variable), data = observed)
  treatment_r2 <- partial_r_squared(treatment_model, treatment_reduced)
  outcome_r2 <- partial_r_squared(model, outcome_reduced)
  treatment_t <- coef(summary(treatment_model))["reserved_women", "t value"]
  outcome_t <- coef(summary(model))["reserved_women", "t value"]
  stopifnot(
    abs(treatment_r2 - treatment_t^2 / (treatment_t^2 + df.residual(treatment_model))) < 1e-12,
    abs(outcome_r2 - outcome_t^2 / (outcome_t^2 + df.residual(model))) < 1e-12
  )
  sensitivity <- sensemakr(model,
    treatment = "direct", benchmark_covariates = "reserved_women",
    kd = 1:3, ky = 1:3, q = 1, alpha = 0.05, reduce = TRUE
  )
  benchmark_rows[[i]] <- cbind(
    data.frame(
      variable = variable, source = outcomes$source[i], n = nobs(model),
      quota_treatment_partial_r2 = treatment_r2,
      quota_outcome_partial_r2 = outcome_r2
    ),
    sensitivity$sensitivity_stats
  )
  bound_rows[[i]] <- cbind(
    data.frame(variable = variable), sensitivity$bounds,
    outcome_bound_at_limit = sensitivity$bounds$r2yz.dx == 1
  )
}
benchmarks <- bind_rows(benchmark_rows)
bounds <- bind_rows(bound_rows)
write_result(benchmarks, "sensitivity-benchmarks")
write_result(bounds, "sensitivity-bounds")

author_lines <- readLines("original/code/appendix.R")
author_environment <- new.env()
author_environment$elite_df <- elite
author_environment$merged_citizen_df <- citizen
checked <- 0L
for (figure in c("D.1", "D.2", "D.3")) {
  start <- grep(paste0("# Figure ", figure, ": Sensitivity"), author_lines, fixed = TRUE)
  following <- which(seq_along(author_lines) > start & grepl("# Arrange the plots", author_lines, fixed = TRUE))
  end <- min(following) - 1L
  eval(parse(text = author_lines[start:end]), envir = author_environment)
  for (j in seq_len(if (figure == "D.1") 5 else 6)) {
    original_model <- get(paste0("model", j), envir = author_environment)
    variable <- all.vars(formula(original_model))[1]
    original_result <- get(paste0("sensitivity_", j), envir = author_environment)
    expected <- benchmarks[benchmarks$variable == variable, ]
    expected_bounds <- bounds[bounds$variable == variable, names(original_result$bounds)]
    stopifnot(
      abs(expected$estimate - coef(original_model)["direct"]) < 1e-12,
      isTRUE(all.equal(original_result$bounds, expected_bounds, check.attributes = FALSE))
    )
    checked <- checked + 1L
  }
}
stopifnot(checked == 17L)
writeLines(
  "All 17 models and 51 bounds equal execution of the original author model blocks.",
  "results/critical/author-sensitivity-validation.txt"
)

authority <- outcomes |>
  filter(variable %in% c(
    "most_influential_gd", "prop_speakingtime_sarpanch", "i_decide_masik_sabha",
    "sarpanch_nominate_BDO", "sarpanch_inauguralevents"
  ))
quota_rows <- list()
for (i in seq_len(nrow(authority))) {
  variable <- authority$variable[i]
  data <- datasets[[authority$source[i]]]
  data <- data[complete.cases(data[c(variable, "direct", "reserved_sc")]), ]
  for (quota in 0:1) {
    group <- data[data$reserved_sc == quota, ]
    formula <- reformulate("direct", variable)
    model <- if (authority$source[i] == "citizen") {
      lm_robust(formula, data = group, clusters = r_villageid, se_type = "CR2")
    } else {
      lm_robust(formula, data = group, se_type = "HC2")
    }
    quota_rows[[length(quota_rows) + 1]] <- data.frame(
      variable = variable, comparison = paste0("sc_", quota),
      n_indirect = sum(group$direct == 0), n_direct = sum(group$direct == 1),
      councils_indirect = length(unique(group$r_villageid[group$direct == 0])),
      councils_direct = length(unique(group$r_villageid[group$direct == 1])),
      indirect_mean = mean(group[[variable]][group$direct == 0]),
      direct_mean = mean(group[[variable]][group$direct == 1]),
      estimate = unname(coef(model)["direct"]), se = model$std.error["direct"],
      low = model$conf.low["direct"], high = model$conf.high["direct"],
      p = model$p.value["direct"]
    )
  }
  formula <- reformulate("direct * reserved_sc", variable)
  interaction <- if (authority$source[i] == "citizen") {
    lm_robust(formula, data = data, clusters = r_villageid, se_type = "CR2")
  } else {
    lm_robust(formula, data = data, se_type = "HC2")
  }
  term <- "direct:reserved_sc"
  quota_rows[[length(quota_rows) + 1]] <- data.frame(
    variable = variable, comparison = "interaction",
    estimate = unname(coef(interaction)[term]), se = interaction$std.error[term],
    low = interaction$conf.low[term], high = interaction$conf.high[term],
    p = interaction$p.value[term]
  )
}
write_result(bind_rows(quota_rows), "sc-authority")

raw <- read.csv("original/data/raw/survey_experiment.csv")
experiment <- read.csv("original/data/analysis/survey_experiment_clean.csv")
experiment_controls <- c(
  "rural", "age", "gender", "religion", "caste", "education", "prior_vote",
  "knowledge_local_politics", "gender_norms"
)
flow <- data.frame(
  stage = c("raw", "blank_assignment", "assigned", "covariates_complete"),
  n = c(
    nrow(raw), sum(raw$sarpanchgendercaste_combination == "NA NA", na.rm = TRUE),
    nrow(experiment), sum(complete.cases(experiment[experiment_controls]))
  )
)
stopifnot(flow$n[1] - flow$n[2] == flow$n[3])
experiment_rows <- list()
missing_rows <- list()
for (variable in c("authority", "pliability", "backlash")) {
  for (male in 0:1) {
    for (maratha in 0:1) {
      group <- experiment[experiment$Male == male & experiment$Maratha == maratha, ]
      missing_rows[[length(missing_rows) + 1]] <- data.frame(
        variable = variable, male = male, maratha = maratha, assigned = nrow(group),
        observed = sum(!is.na(group[[variable]])), missing = sum(is.na(group[[variable]]))
      )
    }
  }
  for (treatment in c("Male", "Maratha")) {
    for (adjusted in c(FALSE, TRUE)) {
      rhs <- c(treatment, if (adjusted) experiment_controls)
      formula <- reformulate(rhs, variable)
      model <- lm_robust(formula, data = experiment, se_type = "HC2")
      experiment_rows[[length(experiment_rows) + 1]] <- data.frame(
        variable = variable, treatment = treatment, adjusted = adjusted, n = model$nobs,
        estimate = unname(coef(model)[treatment]), se = model$std.error[treatment],
        low = model$conf.low[treatment], high = model$conf.high[treatment],
        p = model$p.value[treatment]
      )
    }
  }
}
write_result(flow, "experiment-flow")
write_result(bind_rows(experiment_rows), "experiment-estimates")
write_result(bind_rows(missing_rows), "experiment-missingness")

balance_data <- experiment[complete.cases(experiment[experiment_controls]), ]
balance_rows <- list()
for (condition in sort(unique(balance_data$sarpanchgendercaste_combination))) {
  balance_data$assigned <- as.numeric(balance_data$sarpanchgendercaste_combination == condition)
  for (specification in c("original_HC2", "ordinary_F", "exclude_sparse_HC2")) {
    data <- if (specification == "exclude_sparse_HC2") {
      balance_data[!balance_data$religion %in% c("Christian", "Jain"), ]
    } else {
      balance_data
    }
    formula <- reformulate(experiment_controls, "assigned")
    if (specification == "ordinary_F") {
      model <- lm(formula, data = data)
      statistics <- summary(model)$fstatistic
      n <- nobs(model)
    } else {
      model <- lm_robust(formula, data = data, se_type = "HC2")
      statistics <- model$fstatistic
      n <- model$nobs
    }
    balance_rows[[length(balance_rows) + 1]] <- data.frame(
      condition = condition, specification = specification, n = n,
      f = unname(statistics[1]), numerator_df = unname(statistics[2]),
      denominator_df = unname(statistics[3]),
      p = unname(pf(statistics[1], statistics[2], statistics[3], lower.tail = FALSE))
    )
  }
}
write_result(bind_rows(balance_rows), "experiment-balance")
write_result(as.data.frame(table(
  religion = balance_data$religion,
  condition = balance_data$sarpanchgendercaste_combination
)), "experiment-religion-cells")
gender_table <- table(
  gender = balance_data$gender,
  condition = balance_data$sarpanchgendercaste_combination
)
gender_test <- chisq.test(gender_table)
write_result(as.data.frame(gender_table), "experiment-gender-cells")
write_result(data.frame(
  n = sum(gender_table), statistic = unname(gender_test$statistic),
  df = unname(gender_test$parameter), p = gender_test$p.value
), "experiment-gender-balance")
capture.output(sessionInfo(), file = "results/critical/session-info.txt")
