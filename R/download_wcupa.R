#' Download data from WCUPA
#'
#' @param url The URL associated with the file
#' @return data set with academic headcount information
#' @export

download_wcupa <- function(url) {
  attributes(url) <- list(class = stringr::str_replace(url, stringr::regex("^.*\\.edu.*\\.([:alpha:]{3})[:alpha:]?$"), "\\1"))
  UseMethod("download_wcupa", url)
}

#' @export
#' @rdname download_wcupa
download_wcupa.xls <- function(url) {
  temp <- paste0(tempfile(), ".xlsx")
  temp <- tempfile()
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  readxl::read_excel(temp) %>%
    dplyr::mutate(dplyr::across(TOTAL), as.numeric)
}

#' @export
#' @rdname download_wcupa
download_wcupa.pdf <- function(url) {
  temp <- paste0(tempfile(), ".pdf")
  download.file(url, destfile = temp, method = "libcurl", mode = "wb")
  pdf_lines <- pdftool::pdf_text(temp)

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
    purrr::map(~stringr::str_split(.x, "\\r\\n", simplify = FALSE)) %>%
    unlist() %>%
    stringr::str_split("\n") %>%
    # extract(-c(1:4)) %>%
    purrr::map_dfr(enframe) %>%
    dplyr::filter(stringr::str_detect(value, "ACAD|CAREER|Headcount|Total", negate = TRUE),
           magrittr::not(magrittr::equals(value, ""))) %>%
    tidyr::separate(value, into = col_names_new, stringr::regex("\\s{2,}")) %>%
    tidyr::drop_na(`ACAD CAREER`) %>%
    dplyr::select(-name, -id) %>%
    # mutate(`Effective date` = NA) %>%
    # mutate_at(vars(`Effective date`), lubridate::as_datetime) %>%
    dplyr::mutate(dplyr::across(TOTAL), as.numeric)
}
