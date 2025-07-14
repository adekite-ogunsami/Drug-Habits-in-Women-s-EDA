import streamlit as st
import pandas as pd

AGE_MAP = {
    1: "12-17",
    2: "18-25",
    3: "26-34",
    4: "35-49",
    5: "50-65",
    6: "65+"
}

EDU_MAP = {
    1: "< High School",
    2: "High School Grad",
    3: "Some College",
    4: "College Grad",
    5: "Post Grad"
}

WORK_MAP = {
    1: "Employed",
    2: "Unemployed",
    3: "Not in labor force",
    4: "Other(Misc.)",
    99: "Declined to Answer"
}

MARITAL_MAP = {
    1: "Married",
    2: "Widowed",
    3: "Divorced",
    4: "Never married",
    99: "Declined to Answer"
}

YES_NO_MAP = {
    1: "Yes",
    2: "No"
}

INCOME_MAP = {
    1: "<$20k",
    2: "$20k-$49k",
    3: "$50k-$74k",
    4: "$75k+"
}

POVERTY_MAP = {
    1: "Below Poverty",
    2: "Near Poverty",
    3: "Above Poverty"
}

ALCPDANG_MAP = {
    1: "Very dangerous",
    2: "Dangerous",
    3: "Slightly dangerous",
    4: "Not dangerous"
}

def apply_display_mappings(df):
    df_display = df.copy()
    if 'age2' in df_display.columns:
        df_display['age2_label'] = df_display['age2'].map(AGE_MAP).fillna(df_display['age2']).astype(str)
    if 'eduhighcat' in df_display.columns:
        df_display['eduhighcat_label'] = df_display['eduhighcat'].map(EDU_MAP).fillna(df_display['eduhighcat']).astype(str)
    if 'irwrkstat' in df_display.columns:
        df_display['irwrkstat_label'] = df_display['irwrkstat'].map(WORK_MAP).fillna(df_display['irwrkstat']).astype(str)
    if 'irmaritstat' in df_display.columns:
        df_display['irmaritstat_label'] = df_display['irmaritstat'].map(MARITAL_MAP).fillna(df_display['irmaritstat']).astype(str)
    if 'income' in df_display.columns:
        df_display['income_label'] = df_display['income'].map(INCOME_MAP).fillna(df_display['income']).astype(str)
    if 'poverty3' in df_display.columns:
        df_display['poverty3_label'] = df_display['poverty3'].map(POVERTY_MAP).fillna(df_display['poverty3']).astype(str)
    if 'imother' in df_display.columns:
        df_display['imother_label'] = df_display['imother'].map(YES_NO_MAP).fillna(df_display['imother']).astype(str)
    if 'ifather' in df_display.columns:
        df_display['ifather_label'] = df_display['ifather'].map(YES_NO_MAP).fillna(df_display['ifather']).astype(str)
    if 'mjever' in df_display.columns:
        df_display['mjever_label'] = df_display['mjever'].map(YES_NO_MAP).fillna(df_display['mjever']).astype(str)
    if 'alcever' in df_display.columns:
        df_display['alcever_label'] = df_display['alcever'].map(YES_NO_MAP).fillna(df_display['alcever']).astype(str)
    if 'alcbng30d' in df_display.columns:
        df_display['alcbng30d_label'] = df_display['alcbng30d'].map(YES_NO_MAP).fillna(df_display['alcbng30d']).astype(str)
    if 'alclimit' in df_display.columns:
        df_display['alclimit_label'] = df_display['alclimit'].map(YES_NO_MAP).fillna(df_display['alclimit']).astype(str)
    if 'drvinalco' in df_display.columns:
        df_display['drvinalco_label'] = df_display['drvinalco'].map(YES_NO_MAP).fillna(df_display['drvinalco']).astype(str)
    if 'txyralc' in df_display.columns:
        df_display['txyralc_label'] = df_display['txyralc'].map(YES_NO_MAP).fillna(df_display['txyralc']).astype(str)
    if 'txalconly' in df_display.columns:
        df_display['txalconly_label'] = df_display['txalconly'].map(YES_NO_MAP).fillna(df_display['txalconly']).astype(str)
    if 'alcpdang' in df_display.columns:
        df_display['alcpdang_label'] = df_display['alcpdang'].map(ALCPDANG_MAP).fillna(df_display['alcpdang']).astype(str)

    return df_display

# Load dataset
@st.cache_data
def load_data():
    """
    Loads the main dataset from a CSV file.
    Displays an error and stops the app if the file is not found.
    """
    try:
        df = pd.read_csv(r"C:\Users\zanny\Desktop\School\NCAIR Cohort\Data Science Beginners\Project\National Survey of Drug Use and Health\Dataset and Splits\Cleaned Womens Dataset.csv")
        return df
    except FileNotFoundError:
        st.error("Dataset 'Cleaned Womens Dataset.csv' not found. Please ensure it's in the correct directory.")
        st.stop()

