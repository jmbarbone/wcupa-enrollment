
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import tabula
import httpimport
import pyjordan
import os
import glob

pd.set_option('display.max_rows', 20)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 800)

# Some of the files are PDFs
# TODO changes these to the file paths
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

BAD_ROWS = [x + " Total" for x in ["Undergraduate", "Graduate", "University"]]
BAD_ROWS.append("Acad Group")
BAD_ROWS.append("College")


def wcu_column_names(i=1):
    d = {
        1: wcu_cn_demos(1),
        2: wcu_cn_demos(2),
        3: wcu_cn_demos(3),
        4: wcu_cn_demos(4),
        5: wcu_cn_old(1)
    }

    return d.get(i)


def wcu_cn_demos(i=1):
    d = {
        1: ["FEMALE", "MALE", "AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "PACIFIC_ISLANDER", "MULTI_RACIAL", "UNKNOWN", "IN_STATE", "OUT_OF_STATE"],
        2: ["FEMALE", "MALE", "AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "UNKNOWN", "MULTI_RACIAL", "IN_STATE", "OUT_OF_STATE"],
        3: ["AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "MULTI_RACIAL", "FEMALE", "MALE", "IN_STATE", "OUT_OF_STATE"],
        4: ["AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "MULTI_RACIAL", "UNKNOWN", "MALE", "FEMALE", "IN_STATE", "OUT_OF_STATE"]
    }
    
    demos = [x for x in [[x + "_N", x + "_P"] for x in d.get(i)]]
    demos = pyjordan.unnest(demos)
    acads = ["ACAD_" + x for x in ["GROUP", "ORG", "CAREER", "PLAN"]]
    res = acads + ["DEGREE", "DESCRIPTION", "TOTAL"] + demos
    return res
  
  
def wcu_cn_old(i=1):
    d = {
        1: ["AFRICAN_AMERICAN", "NATIVE_AMERICAN", "ASIAN", "LATINO", "WHITE", "NON_RESIDENT_ALIEN", "MULTI_RACIAL", "UNKNOWN", "MALE", "FEMALE"]
    }
  
    demos = [x for x in [[x + "_N", x + "_P"] for x in d.get(i)]]
    demos = pyjordan.unnest(demos)
    # Plan here is CIP...
    acads= ["ACAD_CAREER", "ACAD_GROUP", "ACAD_ORG", "ACAD_PLAN", "DESCRIPTION", "TOTAL_N"]
    res = acads + demos
    return(res)


def rename_columns(x):
    x = [i.upper() for i in x]
    d = {"-": "_", " ": "_", "%": "P"}
    res = [pyjordan.str_replace_all(i, d) for i in x]
    return res
  
  
def unnest_columns(dataframe):
    return [x[0] if "Unnamed" in x[1] else f"{x[0]}_{x[1]}" for x in dataframe]


def wcu_read_excel(x, engine=None, nrows=None, skipfooter=0):
    df = pd.read_excel(urls.get(x),
                       header=[0, 1],
                       engine=engine, 
                       nrows=nrows,
                       skipfooter=skipfooter)
    df.columns = rename_columns(unnest_columns(df.columns))
    df = df[~df.ACAD_GROUP.isin(BAD_ROWS)]
    return df


# Excel files --------------------------------------------------------
# Excel files are a bit more clean
# May be able to safely bind these together

# could have used skipfooter=3 but I know how many rows they have

# PDFs ---------------------------------------------------------------

def wcu_read_pdf(x,
                 skiprows=0,
                 fill=False, 
                 ant=False,
                 cols=1,
                 lattice=False,
                 lineterminator=None
                 ):
    # x = "fall_2009"
    # skiprows = 0
    # fill = False
    # ant = False
    # cols = 3
    
    po = {
        "skiprows": [skiprows],
        "na_values": "-", 
        "lineterminator": lineterminator
    }

    df = tabula.read_pdf(urls.get(x),
                         pages="all",
                         pandas_options=po,
                         multiple_tables=False,
                         lattice=lattice)
    df = df[0]
    # Does this do anything?
    df = df.replace("-", "0")

    # Set the new column names
    df.columns = wcu_column_names(cols)
    
    df = df[~df.ACAD_GROUP.isin(BAD_ROWS)]
    df = df[~df.ACAD_CAREER.str.contains("total", na=False, case=False)]
    df = df[~df.ACAD_GROUP.str.contains("total", na=False, case=False)]
    df = df[~df.ACAD_PLAN.str.contains("total", na=False, case=False)]
    df = df[~df.ACAD_PLAN.isna()]

    if ant:
      df.ACAD_ORG[0] = "ANT"
    

    if fill:
      df = df.fillna(method="ffill")

    return df


# the ones that fail too hard may have to be manually done...

# wcu_read_pdf("fall_2013", skiprows=1)
# wcu_read_pdf("fall_2011", fill=True, ant=True) # CAREER needs recoding
# wcu_read_pdf("fall_2010", fill=True, ant=True, cols=2) # bad alignment
# wcu_read_pdf("fall_2009", cols=3)
# wcu_read_pdf("fall_2008", cols=4, lattice=True) # This looks pretty bad -- simething wrong with the line returns in OOS?
# wcu_read_pdf("fall_2007") # 34 cols -- something is wrong
# wcu_read_pdf("fall_2006", cols=5) # 26 cols -- something is wrong
# wcu_read_pdf("fall_2005") # 39 cols
# wcu_read_pdf("fall_2004") # fails
# wcu_read_pdf("fall_2003", cols=5)
# 
# wcu_read_pdf("spring_2015") # 35 columns
# wcu_read_pdf("spring_2014") # fail
# wcu_read_pdf("spring_2013")
# wcu_read_pdf("spring_2012") # 25 cols
# wcu_read_pdf("spring_2011") # some misalignment
# wcu_read_pdf("spring_2010") # fail
# wcu_read_pdf("spring_2009") # fail



def wcu_pdf_to_csv(x):
    df = tabula.read_pdf(x, pages="all", multiple_tables=False)
    df = pd.concat(df)
    filename = os.path.splitext(os.path.basename(x))[0]
    filename = "data-raw/pdf2csv/" + filename + ".csv"
    df.to_csv(filename, index=False)
    return filename
  

def try_wcu_pdf_to_csv(x):
  try:
    res = wcu_pdf_to_csv(x)
  except Exception:
    res = None
  
  return res


def doDownloadData():
    print("Working on it")
    wcu_excel_dict = {
        "fall_2020"   : wcu_read_excel("fall_2020", nrows=289),
        "fall_2019"   : wcu_read_excel("fall_2019", nrows=286),
        "fall_2018"   : wcu_read_excel("fall_2018", nrows=275),
        "fall_2017"   : wcu_read_excel("fall_2017", nrows=270),
        "fall_2016"   : wcu_read_excel("fall_2016", nrows=258),
        "fall_2015"   : wcu_read_excel("fall_2015", nrows=242),
        "fall_2014"   : wcu_read_excel("fall_2014", nrows=235),
        "fall_2012"   : wcu_read_excel("fall_2012", engine="openpyxl", nrows=235),
        "spring_2021" : wcu_read_excel("spring_2021", nrows=291),
        "spring_2020" : wcu_read_excel("spring_2020", nrows=283),
        "spring_2019" : wcu_read_excel("spring_2019", nrows=278),
        "spring_2018" : wcu_read_excel("spring_2018", nrows=264),
        "spring_2017" : wcu_read_excel("spring_2017", nrows=263),
        "spring_2016" : wcu_read_excel("spring_2016", nrows=242)
    }

    wcu_excel_df = pd.concat(wcu_excel_dict)
    wcu_excel_df.to_csv("data-raw/excel2csv/wcu_headcounts.csv", index=False)
    
    pdfs = glob.glob("data-raw/*.pdf")
    [try_wcu_pdf_to_csv(i) for i in pdfs]


if __name__ == "__main__":
    doDownloadData()
