# install-packages.R
#
# Installs everything needed to render this site. Run once on a new machine:
#
#   source("install-packages.R")
#
# Deliberately NOT version-pinned (no renv). The published site's
# reproducibility comes from the committed _freeze/ directory, which holds the
# frozen results of every code chunk -- so package updates cannot change the
# live site until a page is deliberately re-rendered. See
# MODERNIZATION-PLAN.md section 1 for the reasoning.

# install.packages() needs an explicit mirror when R runs non-interactively:
# the default "repos" option is the unresolved placeholder "@CRAN@", which
# prompts for a mirror in RStudio but errors under Rscript.
repos <- getOption("repos")
if (is.null(repos[["CRAN"]]) || repos[["CRAN"]] == "@CRAN@") {
  options(repos = c(CRAN = "https://cloud.r-project.org"))
}

cran_packages <- c(
  # Core -- these two account for the large majority of usage
  "tidyverse",      # includes dplyr, ggplot2, lubridate, stringr, forcats, ...
  "easystats",      # includes see, correlation, parameters, performance, ...

  # Plotting
  "patchwork",
  "ggdist",
  "ggbeeswarm",
  "ggbrace",

  # Stats / teaching helpers
  "afex",
  # Suggests-only dep of modelbased, so easystats does not pull it in. Needed by
  # estimate_means()/estimate_slopes()/estimate_contrasts(), but NOT by
  # estimate_relation(), which goes through insight::get_predicted() instead.
  "marginaleffects",
  "emmeans",
  "distributional",
  "faux",
  "irr",
  "psych",
  "WebPower",

  # Tables / rendering
  #
  # kableExtra was removed. It was doing two things: one `kable_styling(font_size)`
  # call, and two `scroll_box()` tables that were hiding most of their rows inside a
  # child scroller (4 of 61 rows on one slide, 5 of 46 on the other) where no overflow
  # sweep could see them and no audience could scroll them. Its `kePrint.js` also
  # threw "$ is not defined" on every deck that loaded it, since revealjs has no
  # jQuery. Tibble printing covers the data slides and a plain markdown table covers
  # the other. Do not add it back without checking whether the same is true again.
  "knitr",

  # Misc
  "praise"
)

# Not installed yet -- these are needed only once the planned chapters are
# written, and there is no reason to make everyone install them before then.
#
#   mice    -- Chapter 12b, multiple imputation
#   lavaan  -- Chapter 12b, FIML
#   splines -- Chapter 09b (ships with R, nothing to install)

missing <- setdiff(cran_packages, rownames(installed.packages()))
if (length(missing) > 0) {
  install.packages(missing)
} else {
  message("All CRAN packages already installed.")
}

# standist is not on CRAN -- it's your own package, installed from GitHub.
# Used once, in archive/Unit_B/05b_Slides.qmd, to visualize t distributions.
if (!requireNamespace("standist", quietly = TRUE)) {
  if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
  remotes::install_github("jmgirard/standist")
}
