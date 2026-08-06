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

cran_packages <- c(
  # Core -- these two account for the large majority of usage
  "tidyverse",      # includes dplyr, ggplot2, lubridate, stringr, forcats, ...
  "easystats",      # includes see, correlation, parameters, performance, ...

  # Plotting
  "patchwork",
  "ggdist",
  "ggeffects",
  "ggbeeswarm",
  "ggbrace",

  # Stats / teaching helpers
  "afex",
  "distributional",
  "faux",
  "irr",
  "lsr",
  "psych",
  "WebPower",

  # Tables / rendering
  "knitr",
  "kableExtra",

  # Misc
  "praise"
)

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
