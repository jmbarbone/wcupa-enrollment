
# ------------------------------------------------------------------------#
# Create data set
# ------------------------------------------------------------------------#

# Source function ---------------------------------------------------------

source("download_wcupa.R")


# Headcount - Academic plan -----------------------------------------------

urls <- c(
  fall_2018 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2018HeadcountbyAcademicPlanandDemographics.xls",
  fall_2017 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2017HeadcountbyAcademicPlanandDemographics.xls",
  fall_2016 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2016HeadcountbyAcademicPlanandDemographics.xls",
  fall_2015 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2015HeadcountbyAcademicPlanandDemographics.xls",
  fall_2014 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/FALL2014HeadcountbyAcademicPlanandDemographics.xls",
  fall_2013 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/RevisedFall2013HeadcountEnrollmentbyProgrambyGenderbyRace.pdf",
  fall_2012 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2012HeadcountbyAcademicPlanandDemographics_000.xlsx",
  # fall_2011 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadcountsbyAcadPlanDemoF11.pdf",
  # fall_2010 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadcountsbyAcadPlanDemoF10.pdf",
  # fall_2009 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/EnrollmentbyGenderEthnResF09.pdf",
  # fall_2008 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/FallHeadCountbyAcadPlanDemographics_08_000.pdf",
  # fall_2007 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountAcadPlanDemographics2075_000.pdf",
  # fall_2006 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_065.pdf",
  # fall_2005 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_055.pdf",
  # fall_2004 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptDemoUGG_045.pdf",
  # fall_2003 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_065.pdf",

  spring_2019 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2019HeadcountbyAcademicPlanandDemographics.xls",
  spring_2018 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2018HeadcountbyAcademicPlanandDemographics.xls",
  spring_2017 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2017HeadcountbyAcademicPlanandDemographics.xls",
  spring_2016 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2016HeadcountbyAcademicPlanandDemographics.xls",
  # spring_2015 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2015HeadcountbyAcademicPlanandDemographics.pdf",
  # spring_2014 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2014HeadcountbyAcadPlanandDemographics.pdf",
  # spring_2013 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2013HeadcountbyAcademicPlanandDemographics.pdf",
  # spring_2012 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spr12HeadcountsbyAcadPlan.pdf",
  # spring_2011 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/SpringHeadcountsbyAcadplan_000.pdf",
  # spring_2010 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2010HeadcountbyAcademicPlanandDemographics.pdf",
  # spring_2009 = "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2009HeadcountbyAcademicPlanandDemographics.pdf",
  NULL
  )


# Download data -----------------------------------------------------------

headcounts <- map_dfr(urls, download_wcupa, .id = "session_year")


# Make adjustments --------------------------------------------------------

remove_acad_groups <- regex(paste(
  "Undergrad",
  "Graduate",
  "University",
  sep = "|"
))

wcupa_headcount <- headcounts %>%
  janitor::clean_names("snake") %>%
  rename(female_n             = female,
         female_p             = x11,
         male_n               = male,
         male_p               = x13,
         african_american_n   = african_american,
         african_american_p   = x15,
         asian_n              = asian,
         asian_p              = x17,
         latino_n             = latino,
         latino_p             = x19,
         multi_racial_n       = multi_racial,
         multi_racial_p       = x21,
         native_american_n    = native_american,
         native_american_p    = x23,
         pacific_islander_n   = pacific_islander,
         pacific_islander_p   = x25,
         unknown_n            = unknown,
         unknown_p            = x27,
         white_n              = white,
         white_p              = x29,
         non_resident_alien_n = non_resident_alien,
         non_resident_alien_p = x31,
         in_state_n           = in_state,
         in_state_p           = x33,
         out_of_state_n       = out_of_state,
         out_of_state_p       = x35) %>%
  filter(str_detect(acad_group, remove_acad_groups, negate = T)) %>%
  select_if(~!all(is.na(.))) %>%
  separate(session_year, c("session", "year")) %>%
  mutate_at(vars(session), factor, levels = c("spring", "fall")) %>%
  mutate_at(vars(acad_career), factor, levels = c("UGRD", "GRAD")) %>%
  mutate(year_month = lubridate::ymd(
    paste(year,
          recode(session, "fall" = "August", "spring" = "January"),
          20))) %>%
  arrange(year_month)

new_remapping <- wcupa_headcount %>%
  arrange(desc(year_month)) %>%
  distinct(acad_group, acad_org) %>%
  distinct(acad_org, .keep_all = T)

wcupa_headcount %<>%
  select(-acad_group) %>%
  left_join(new_remapping, by = "acad_org")


# Save data ---------------------------------------------------------------

save(wcupa_headcount, file = "wcupa_headcount.RData")
remove(list = ls())
