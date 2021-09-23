
import pandas as pd
import tabula
import httpimport
import pyjordan

# Some of the files are PDFs

urls = {
  # These are good
  "fall_2018": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2018HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2017": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2017HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2016": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2016HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2015": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2015HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2014": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/FALL2014HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2013": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/RevisedFall2013HeadcountEnrollmentbyProgrambyGenderbyRace.pdf",
  "fall_2012": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2012HeadcountbyAcademicPlanandDemographics_000.xlsx",
  "fall_2011": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadcountsbyAcadPlanDemoF11.pdf",

  # These are bad
  "fall_2010": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadcountsbyAcadPlanDemoF10.pdf",
  "fall_2009": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/EnrollmentbyGenderEthnResF09.pdf",
  "fall_2008": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/FallHeadCountbyAcadPlanDemographics_08_000.pdf",
  "fall_2007": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountAcadPlanDemographics2075_000.pdf",
  "fall_2006": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_065.pdf",
  "fall_2005": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_055.pdf",
  "fall_2004": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptDemoUGG_045.pdf",
  "fall_2003": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/HeadCountEnrlByDeptMinorityUGG_065.pdf",

  # these are good
  "spring_2019": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2019HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2018": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2018HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2017": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2017HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2016": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2016HeadcountbyAcademicPlanandDemographics.xls",

  # These are bad
  "spring_2015": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2015HeadcountbyAcademicPlanandDemographics.pdf",
  "spring_2014": "https://www.wc upa.edu/viceProvost/institutionalResearch/documents/Spring2014HeadcountbyAcadPlanandDemographics.pdf",
  "spring_2013": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2013HeadcountbyAcademicPlanandDemographics.pdf",
  "spring_2012": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spr12HeadcountsbyAcadPlan.pdf",
  "spring_2011": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/SpringHeadcountsbyAcadplan_000.pdf",
  "spring_2010": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2010HeadcountbyAcademicPlanandDemographics.pdf",
  "spring_2009": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2009HeadcountbyAcademicPlanandDemographics.pdf"
}

# List of default column names?
DEMOS = ["FEMALE", "MALE", "AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "PACIFIC_ISLANDER", "MULTI_RACIAL", "UNKNOWN", "IN_STATE", "OUT_OF_STATE"]
DEMOS = [x for x in [[x + "_N", x + "_P"] for x in DEMOS]]
DEMOS = pyjordan.unnest(DEMOS)
ACADS = ["ACAD_" + x for x in ["GROUP", "ORG", "CAREER", "PLAN"]]
COLNAMES = ACADS + ["DEGREE", "DESCRIPTION", "TOTAL"] + DEMOS


def rename_columns(x):
  x = [i.upper() for i in x]
  d = {"-": "_", " ": "_", "%": "P"}
  res = [pyjordan.str_replace_all(i, d) for i in x]
  return res
  
  
def unnest_columns(dataframe):
  return [x[0] if "Unnamed" in x[1] else f"{x[0]}_{x[1]}" for x in dataframe]
  

# Read each file
# Not the cleanest but many of these have differences

df = pd.read_excel(urls.get("fall_2018"), header=[0, 1], nrows=275)
# Clean up the multiple headers
df.columns = rename_columns(unnest_columns(df.columns))
# maybe just add it to the dictionary?
fall_2018 = df

df = pd.read_excel(urls.get("fall_2017"), header=[0, 1], nrows=270)
df.columns = rename_columns(unnest_columns(df.columns))
fall_2017 = df

po = {"skiprows": [1]}
df = tabula.read_pdf(urls.get("fall_2013"), pages=1, pandas_options=po, multiple_tables=False)[0]
df.columns = COLNAMES
View(df)

View(df)

def doDownloadData():
    print("Working on it")


if __name__ == "__main__":
    doDownloadData()
