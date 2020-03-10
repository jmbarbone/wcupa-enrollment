#' Download data from WCUPA
#'
#' @param url The URL associated with the file
#' @return data set with academic headcount information
#'
#' @importFrom dplyr filter
#' @importFrom dplyr mutate_at
#' @importFrom dplyr select
#' @importFrom dplyr vars
#' @importFrom magrittr equals
#' @importFrom magrittr not
#' @importFrom pdftools pdf_text
#' @importFrom purrr map
#' @importFrom purrr map_dfr
#' @importFrom readxl read_excel
#' @importFrom stringr regex
#' @importFrom stringr str_detect
#' @importFrom stringr str_replace
#' @importFrom stringr str_split
#' @importFrom tibble enframe
#' @importFrom tidyr drop_na
#' @importFrom tidyr separate
#'
#' @export

download_wcupa <- function(url) {
  attributes(url) <- list(class = str_replace(url, regex("^.*\\.edu.*\\.([:alpha:]{3})[:alpha:]?$"), "\\1"))
  UseMethod("download_wcupa", url)
}

#' @export
download_wcupa.xls <- function(url) {
  temp <- paste0(tempfile(), ".xlsx")
  temp <- tempfile()
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  read_excel(temp) %>%
    mutate_at(vars(TOTAL), as.numeric)
}

#' @export
download_wcupa.pdf <- function(url) {
  temp <- paste0(tempfile(), ".pdf")
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  pdf_lines <- pdf_text(temp)

  col_names_new <- c(
    "id",
    "ACAD GROUP", "ACAD ORG", "ACAD CAREER", "ACAD PLAN", "DEGREE",
    # "EFFECTIVE DATE", "PLAN STATUS",
    "DESCRIPTION", "TOTAL",
    "Female", "...11",
    "Male", "...13",
    "African-American", "...15",
    "Asian", "...17",
    "Latino", "...19",
    "Multi-Racial", "...21",
    "Native American", "...23",
    "Pacific Islander", "...25",
    "Unknown", "...27",
    "White", "...29",
    "Non-Resident Alien", "...31",
    "In-State", "...33",
    "Out-of-State", "...35"
  )

  pdf_lines %>%
    map(~ str_split(.x, "\\r\\n", simplify = F)) %>%
    unlist %>%
    str_split("\n") %>%
    # extract(-c(1:4)) %>%
    map_dfr(enframe) %>%
    filter(str_detect(value, "ACAD|CAREER|Headcount|Total", negate = TRUE),
           not(equals(value, ""))) %>%
    separate(value, into = col_names_new, regex("\\s{2,}")) %>%
    drop_na(`ACAD CAREER`) %>%
    select(-name, -id) %>%
    # mutate(`Effective date` = NA) %>%
    # mutate_at(vars(`Effective date`), lubridate::as_datetime) %>%
    mutate_at(vars(TOTAL), as.numeric)
}
