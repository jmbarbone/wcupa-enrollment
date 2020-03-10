#' Download data from WCUPA
#'
#' @param url The URL associated with the file
#' @return data set with academic headcount information

download_wcupa <- function(url)
{
  attributes(url) <- list(class = str_replace(url, regex("^.*\\.edu.*\\.([:alpha:]{3})[:alpha:]?$"), "\\1"))
  UseMethod("download_wcupa", url)
}

download_wcupa.xls <- function(url) {
  temp <- paste0(tempfile(), ".xlsx")
  temp <- tempfile()
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  readxl::read_excel(temp) %>%
    mutate_at(vars(TOTAL), as.numeric)
}

download_wcupa.pdf <- function(url) {
  temp <- paste0(tempfile(), ".pdf")
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  pdf_lines <- pdftools::pdf_text(temp)

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
    filter(str_detect(value, "ACAD|CAREER|Headcount|Total", negate = T),
           not(equals(value, ""))) %>%
    separate(value, into = col_names_new, regex("\\s{2,}")) %>%
    drop_na(`ACAD CAREER`) %>%
    select(-name, -id) %>%
    # mutate(`Effective date` = NA) %>%
    # mutate_at(vars(`Effective date`), lubridate::as_datetime) %>%
    mutate_at(vars(TOTAL), as.numeric)
}
