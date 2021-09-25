
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import tabula
import httpimport
import pyjordan

# Some of the files are PDFs

urls = {
  # These are good
  "fall_2020": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2020HeadcountbyAcademicPlanandDemographics.xls",
  "fall_2019": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Fall2019HeadcountbyAcademicPlanandDemographics.xls",
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
  "spring_2021": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2021HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2020": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2020HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2019": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2019HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2018": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2018HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2017": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2017HeadcountbyAcademicPlanandDemographics.xls",
  "spring_2016": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2016HeadcountbyAcademicPlanandDemographics.xls",

  # These are bad
  "spring_2015": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2015HeadcountbyAcademicPlanandDemographics.pdf",
  "spring_2014": "https://www.wcupa.edu/viceProvost/institutionalResearch/documents/Spring2014HeadcountbyAcadPlanandDemographics.pdf",
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

# Hey, a different order
DEMOS2 = ["FEMALE", "MALE", "AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "UNKNOWN", "MULTI_RACIAL", "IN_STATE", "OUT_OF_STATE"]
DEMOS2 = [x for x in [[x + "_N", x + "_P"] for x in DEMOS2]]
DEMOS2 = pyjordan.unnest(DEMOS2)
COLNAMES2 = ACADS + ["DEGREE", "DESCRIPTION", "TOTAL"] + DEMOS2


def wcu_column_names(i):
    switch={
      1: COLNAMES,
      2: COLNAMES2,
      }
    # Should this be an error?
    return switch.get(i, "Invalid Column version")


def rename_columns(x):
  x = [i.upper() for i in x]
  d = {"-": "_", " ": "_", "%": "P"}
  res = [pyjordan.str_replace_all(i, d) for i in x]
  return res
  
  
def unnest_columns(dataframe):
  return [x[0] if "Unnamed" in x[1] else f"{x[0]}_{x[1]}" for x in dataframe]
  
BAD_ROWS = [x + " Total" for x in ["Undergraduate", "Graduate", "University"]]
BAD_ROWS.append("Acad Group")
BAD_ROWS.append("College")

def wcu_read_excel(x, engine=None, nrows=None):
  df = pd.read_excel(urls.get(x), header=[0, 1], engine=engine, nrows=nrows)
  df.columns = rename_columns(unnest_columns(df.columns))
  df = df[~df.ACAD_GROUP.isin(BAD_ROWS)]
  return df

# Excel files are a bit more clean

wcu_read_excel("fall_2020", nrows=289)
wcu_read_excel("fall_2019", nrows=286)
wcu_read_excel("fall_2018", nrows=275)
wcu_read_excel("fall_2017", nrows=270)
wcu_read_excel("fall_2016", nrows=258)
wcu_read_excel("fall_2015", nrows=242)
wcu_read_excel("fall_2014", nrows=235)
# fall 2013 is for some reason a pdf...
wcu_read_excel("fall_2012", engine="openpyxl", nrows=235)

wcu_read_excel("spring_2021", nrows=291)
wcu_read_excel("spring_2020", nrows=283)
wcu_read_excel("spring_2019", nrows=278)
wcu_read_excel("spring_2018", nrows=264)
wcu_read_excel("spring_2017", nrows=263)
wcu_read_excel("spring_2016", nrows=242)


# Fall 2013 ----------------------------------------------------------
# PDF

def wcu_read_pdf(x,
                 skiprows=0,
                 fill=False, 
                 ant=False,
                 cols=1
                 ):
  po = {"skiprows": [skiprows]}
  df = tabula.read_pdf(urls.get(x),
                       pages="all",
                       pandas_options=po,
                       multiple_tables=False)
  df = df[0]
  df = df.replace("-", "0")
  
  # Set the new column names
  df.columns = wcu_column_names(cols)
  df[~df.ACAD_GROUP.isin(BAD_ROWS)]
  df = df[~df.ACAD_GROUP.str.endswith("Total", na=False)]
  df = df[~df.ACAD_GROUP.str.endswith("Totals", na=False)]
  df = df[~df.ACAD_PLAN.str.endswith("Total", na=False)]
  df = df[~df.ACAD_PLAN.str.endswith("Totals", na=False)]
  df = df[~df.ACAD_PLAN.isna()]
  
  if ant:
    df.ACAD_ORG[0] = "ANT"
  
  
  if fill:
    df = df.fillna(method="ffill")
    
  
  return df


# the ones that fail too hard may have to be manually done...

wcu_read_pdf("fall_2013", skiprows=1)
wcu_read_pdf("fall_2011", fill=True, ant=True) # CAREER needs recoding
wcu_read_pdf("fall_2010", fill=True, ant=True, cols=2) # bad alignment
wcu_read_pdf("fall_2009") # 29 cols
wcu_read_pdf("fall_2008") # 31 cols
wcu_read_pdf("fall_2007") # 34 cols
wcu_read_pdf("fall_2006") # 26 cols
wcu_read_pdf("fall_2005") # 39 cols
wcu_read_pdf("fall_2004") # fails
wcu_read_pdf("fall_2003") # 26 cols

wcu_read_pdf("spring_2015") # 35 columns
wcu_read_pdf("spring_2014") # fail
wcu_read_pdf("spring_2013")
wcu_read_pdf("spring_2012") # 25 cols
wcu_read_pdf("spring_2011") # some misalignment
wcu_read_pdf("spring_2010") # fail
wcu_read_pdf("spring_2009") # fail


# Oh gosh darnit, fall_2011 is whack
# po = {"skiprows": [0]}
# df = tabula.read_pdf(urls.get("fall_2011"), pages="all", pandas_options=po, multiple_tables=False)[0]
# df.columns = COLNAMES
# df = df[~df.ACAD_GROUP.str.endswith("Totals", na=False)]
# df = df[~df["ACAD_PLAN"].str.endswith("Total", na=False)]
# df = df[~df.ACAD_PLAN.isna()]
# df = df[df.ACAD_GROUP != "Acad Group"]
# df.ACAD_ORG[0] = "ANT"
# df.fillna(method="ffill")
# df
# # df.fill # fill the empty rows
# df
# View(df)


def doDownloadData():
    print("Working on it")


if __name__ == "__main__":
    doDownloadData()
