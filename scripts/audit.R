.libPaths(c("work/authors-library", .libPaths()))
suppressPackageStartupMessages({
  library(dplyr)
  library(estimatr)
  library(ggplot2)
})

dir.create("results/audit", recursive = TRUE, showWarnings = FALSE)
write_result <- function(x, name) {
  write.csv(x, file.path("results/audit", paste0(name, ".csv")),
    row.names = FALSE, na = ""
  )
}

elite <- read.csv("original/data/analysis/elite_survey.csv")
citizen <- read.csv("original/data/analysis/citizen_survey.csv")
admin <- read.csv("original/data/analysis/resignation_admin.csv")
stopifnot(
  nrow(elite) == 604, !anyDuplicated(elite$r_villageid),
  nrow(citizen) == 3658, nrow(admin) == 1425,
  sum(elite$direct == 1) == 234, sum(elite$direct == 0) == 370
)
elite <- elite |>
  mutate(
    period = case_when(
      direct == 0 & sarpanch_election_year <= 2017 ~ "early_indirect",
      direct == 1 ~ "direct",
      direct == 0 & sarpanch_election_year >= 2020 ~ "late_indirect"
    ),
    election_date = as.Date(sprintf(
      "%04d-%02d-01", sarpanch_election_year, sarpanch_election_month
    ))
  )
stopifnot(!anyNA(elite$period), !anyNA(elite$election_date))
citizen <- citizen |>
  left_join(
    elite |>
      select(
        r_villageid, direct, period, election_date, sarpanch_election_year,
        sarpanch_election_month, reserved_women, reserved_sc, reserved_obc,
        sarpanch_maratha
      ),
    by = "r_villageid", relationship = "many-to-one", suffix = c("", "_elite")
  )
stopifnot(
  nrow(citizen) == 3658, !anyNA(citizen$direct_elite),
  all(citizen$direct == citizen$direct_elite)
)

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
datasets <- list(elite = elite, citizen = citizen, admin = admin)
outcomes <- list(elite = elite_outcomes, citizen = citizen_outcomes, admin = "resigned")

moments <- function(x) {
  observed <- x[!is.na(x)]
  n <- length(observed)
  c(
    total = length(x), n = n, missing = sum(is.na(x)),
    missing_rate = mean(is.na(x)), mean = mean(observed),
    sum = sum(observed), se = sd(observed) / sqrt(n)
  )
}

fit_difference <- function(data, variable, clustered = FALSE) {
  f <- reformulate("direct", variable)
  model <- if (clustered) {
    lm_robust(f, data = data, clusters = data$r_villageid, se_type = "CR2")
  } else {
    lm_robust(f, data = data, se_type = "HC2")
  }
  data.frame(
    difference = unname(coef(model)["direct"]),
    se = unname(model$std.error["direct"]),
    ci_low = unname(model$conf.low["direct"]),
    ci_high = unname(model$conf.high["direct"]),
    p = unname(model$p.value["direct"]), n_model = model$nobs,
    method = if (clustered) "GP CR2" else "HC2"
  )
}

mean_rows <- list()
cohort_rows <- list()
for (source in names(datasets)) {
  data <- datasets[[source]]
  for (variable in outcomes[[source]]) {
    observed <- data[[variable]][!is.na(data[[variable]])]
    stopifnot(all(observed >= 0 & observed <= 1))
    row <- data.frame(source = source, variable = variable)
    for (arm in 0:1) {
      summary <- moments(data[[variable]][which(data$direct == arm)])
      for (name in names(summary)) {
        row[[paste0(if (arm == 1) "direct_" else "indirect_", name)]] <- summary[name]
      }
    }
    row$missing_treatment <- sum(is.na(data$direct))
    row <- cbind(row, fit_difference(data, variable, source == "citizen"))
    stopifnot(abs(row$difference - (row$direct_mean - row$indirect_mean)) < 1e-12)
    for (period in c("early_indirect", "direct", "late_indirect")) {
      if (source == "admin") next
      summary <- moments(data[[variable]][which(data$period == period)])
      for (name in c("n", "mean", "missing", "total")) {
        row[[paste0(period, "_", name)]] <- summary[name]
      }
      cohort_rows[[length(cohort_rows) + 1]] <- cbind(
        data.frame(source = source, variable = variable, period = period),
        as.data.frame(as.list(summary))
      )
    }
    mean_rows[[length(mean_rows) + 1]] <- row
  }
}
raw_means <- bind_rows(mean_rows)
cohort_means <- bind_rows(cohort_rows)
write_result(raw_means, "raw-means")
write_result(cohort_means, "cohort-means")

transition_rows <- list()
for (source in c("elite", "citizen")) {
  for (variable in outcomes[[source]]) {
    for (comparison in c("early_vs_direct", "late_vs_direct", "early_vs_late")) {
      periods <- switch(comparison,
        early_vs_direct = c("early_indirect", "direct"),
        late_vs_direct = c("late_indirect", "direct"),
        early_vs_late = c("early_indirect", "late_indirect")
      )
      data <- datasets[[source]] |>
        filter(period %in% periods)
      if (comparison == "early_vs_late") {
        data$direct <- as.integer(data$period == "late_indirect")
      }
      transition_rows[[length(transition_rows) + 1]] <- cbind(
        data.frame(source = source, variable = variable, comparison = comparison),
        fit_difference(data, variable, source == "citizen")
      )
    }
  }
}
write_result(bind_rows(transition_rows), "transition-contrasts")

authority_rows <- list()
for (variable in c("most_influential_gd", "prop_speakingtime_sarpanch")) {
  for (quota in c("all", "women_reserved", "other")) {
    data <- elite
    if (quota != "all") {
      data <- filter(data, reserved_women == as.integer(quota == "women_reserved"))
    }
    direct_values <- data[[variable]][data$direct == 1]
    direct_values <- direct_values[!is.na(direct_values)]
    illustrative <- t.test(direct_values, mu = 1 / 3)
    authority_rows[[length(authority_rows) + 1]] <- cbind(
      data.frame(
        variable = variable, quota = quota, n_direct = length(direct_values),
        mean_direct = mean(direct_values),
        mean_indirect = mean(data[[variable]][data$direct == 0], na.rm = TRUE),
        distance_from_third = mean(direct_values) - 1 / 3,
        direct_mean_low = illustrative$conf.int[1],
        direct_mean_high = illustrative$conf.int[2],
        illustrative_p_third = illustrative$p.value
      ),
      fit_difference(data, variable)
    )
  }
}
write_result(bind_rows(authority_rows), "authority-benchmark")
interactions <- lapply(
  c("most_influential_gd", "prop_speakingtime_sarpanch"),
  function(variable) {
    model <- lm_robust(
      reformulate("direct * reserved_women", variable), data = elite,
      se_type = "HC2"
    )
    term <- "direct:reserved_women"
    data.frame(
      variable = variable, interaction = unname(coef(model)[term]),
      se = unname(model$std.error[term]), p = unname(model$p.value[term]),
      ci_low = unname(model$conf.low[term]),
      ci_high = unname(model$conf.high[term])
    )
  }
)
write_result(bind_rows(interactions), "authority-quota-interaction")
write_result(
  elite |> count(direct, prop_speakingtime_sarpanch, .drop = FALSE),
  "speaking-share-distribution"
)

missing_rows <- list()
land <- "avg_prop_land_held_sarpanch_caste"
for (group in c(
  "direct", "period", "sarpanch_election_year", "reserved_women",
  "reserved_sc", "reserved_obc", "sarpanch_maratha"
)) {
  grouped <- elite |>
    group_by(.data[[group]]) |>
    summarise(
      total = n(), observed = sum(!is.na(.data[[land]])),
      missing = sum(is.na(.data[[land]])),
      missing_rate = mean(is.na(.data[[land]])),
      observed_mean = mean(.data[[land]], na.rm = TRUE), .groups = "drop"
    )
  names(grouped)[1] <- "level"
  grouped$level <- as.character(grouped$level)
  grouped$group <- group
  test <- suppressWarnings(chisq.test(table(elite[[group]], is.na(elite[[land]]))))
  grouped$pearson_p <- test$p.value
  grouped$min_expected <- min(test$expected)
  missing_rows[[length(missing_rows) + 1]] <- grouped
}
write_result(bind_rows(missing_rows), "land-missingness")
write_result(
  elite |>
    group_by(period, reserved_women, reserved_sc, reserved_obc, sarpanch_maratha) |>
    summarise(
      total = n(), observed = sum(!is.na(.data[[land]])),
      mean = mean(.data[[land]], na.rm = TRUE), .groups = "drop"
    ),
  "land-missingness-crosscells"
)
bound_rows <- elite |>
  group_by(direct) |>
  summarise(
    n = n(), observed = sum(!is.na(.data[[land]])),
    lower = sum(.data[[land]], na.rm = TRUE) / n(),
    upper = (sum(.data[[land]], na.rm = TRUE) + sum(is.na(.data[[land]]))) / n(),
    .groups = "drop"
  )
write_result(bound_rows, "land-bounds")

category_rows <- list()
weight_rows <- list()
pairs <- list(
  bdo = c("sarpanch_nominate_BDO", "other_nominate_BDO"),
  events = c("sarpanch_inauguralevents", "formersarpanch_otherperson_inauguralevents")
)
for (question in names(pairs)) {
  a <- citizen[[pairs[[question]][1]]]
  b <- citizen[[pairs[[question]][2]]]
  stopifnot(identical(is.na(a), is.na(b)), all(a + b <= 1, na.rm = TRUE))
  data <- citizen |>
    mutate(category = case_when(
      is.na(a) ~ "missing", a == 1 ~ "current_president",
      b == 1 ~ "former_president_or_other", TRUE ~ "other_released_categories"
    ))
  counts <- data |>
    count(direct, category) |>
    group_by(direct) |>
    mutate(
      total_records = sum(n),
      answered = sum(n[category != "missing"]),
      proportion_all = n / total_records,
      proportion_answered = if_else(category == "missing", NA_real_, n / answered),
      question = question
    ) |>
    ungroup()
  category_rows[[question]] <- counts
}
write_result(bind_rows(category_rows), "citizen-categories")
write_result(citizen |> count(r_villageid, direct), "citizens-per-gp")
for (variable in citizen_outcomes) {
  gp <- citizen |>
    group_by(r_villageid, direct) |>
    summarise(value = mean(.data[[variable]], na.rm = TRUE), .groups = "drop")
  gp$value[is.nan(gp$value)] <- NA_real_
  weight_rows[[variable]] <- cbind(
    data.frame(
      variable = variable,
      indirect_mean_equal_gp = mean(gp$value[gp$direct == 0], na.rm = TRUE),
      direct_mean_equal_gp = mean(gp$value[gp$direct == 1], na.rm = TRUE)
    ),
    fit_difference(gp, "value")
  )
}
write_result(bind_rows(weight_rows), "citizen-equal-gp-weight")

timing_rows <- list()
for (source in c("elite", "citizen")) {
  variable <- if (source == "elite") "resignation" else "resignation_reported"
  for (unit in c("election_date", "sarpanch_election_year")) {
    summary <- datasets[[source]] |>
      group_by(.data[[unit]], direct) |>
      summarise(
        total = n(), n = sum(!is.na(.data[[variable]])),
        positive = sum(.data[[variable]], na.rm = TRUE),
        mean = mean(.data[[variable]], na.rm = TRUE), .groups = "drop"
      )
    names(summary)[1] <- "election_time"
    summary$election_time <- as.character(summary$election_time)
    summary$unit <- unit
    summary$variable <- variable
    timing_rows[[length(timing_rows) + 1]] <- summary
  }
}
timing <- bind_rows(timing_rows)
write_result(timing, "shared-tenure-by-election-time")
plot_data <- timing |>
  filter(unit == "election_date") |>
  mutate(
    election_date = as.Date(election_time),
    respondent = if_else(variable == "resignation", "President", "Citizen informant"),
    regime = if_else(direct == 1, "Direct", "Indirect")
  )
theme_set(theme_classic(base_size = 11))
plot <- ggplot(plot_data, aes(election_date, 100 * mean, size = n, color = regime)) +
  geom_point(alpha = 0.85) +
  facet_wrap(~respondent, ncol = 1) +
  scale_color_manual(values = c(Direct = "#146b79", Indirect = "#333333")) +
  scale_y_continuous(limits = c(0, 100)) +
  scale_x_date(date_breaks = "1 year", date_labels = "%Y") +
  labs(
    x = "Reported presidential election month", y = "Shared tenure reported (%)",
    size = "Observed N", color = "Election regime",
    title = "Shared tenure varies sharply across election cohorts",
    caption = paste(
      "Released survey records; raw means among nonmissing answers.",
      "Points show election months, not survey dates or elapsed exposure.",
      "Question wording includes anticipated rotation; small cells are descriptive.",
      sep = "\n"
    )
  ) +
  theme(legend.position = "top", plot.caption = element_text(hjust = 0))
ggsave("results/audit/shared-tenure-by-election-month.png", plot,
  width = 8, height = 7, dpi = 180
)

missing_plot <- ggplot(
  filter(cohort_means, variable == land),
  aes(
    factor(period, levels = c("early_indirect", "direct", "late_indirect")),
    100 * n / total
  )
) +
  geom_col(width = 0.55, fill = "#146b79") +
  geom_text(aes(label = paste0(n, "/", total)), vjust = -0.6) +
  scale_x_discrete(labels = c("Early indirect", "Direct", "Late indirect")) +
  scale_y_continuous(limits = c(0, 110), breaks = seq(0, 100, 25)) +
  labs(
    x = NULL, y = "Councils with observed caste land share (%)",
    title = "Land-share coverage is concentrated in later cohorts",
    caption = "Gram sevak's approximate assessment; denominator is all councils in each cohort."
  ) +
  theme(plot.caption = element_text(hjust = 0))
ggsave("results/audit/land-observation-by-cohort.png", missing_plot,
  width = 8, height = 4.5, dpi = 180
)

capture.output(sessionInfo(), file = "results/audit/session-info.txt")
cat("Audit complete: means, denominators, cohorts, bounds, categories and figures.\n")
