import nbformat as nbf

nb = nbf.v4.new_notebook()

def add_md(text):
    nb.cells.append(nbf.v4.new_markdown_cell(text.strip()))

def add_code(code):
    nb.cells.append(nbf.v4.new_code_cell(code.strip()))

# --- Title & Metadata ---
add_md("""
# Course Project: Exploratory Data Analysis & Statistical Modeling
## Course: Data Handling and Visualization (Sem 5)
**Student Name:** Mayank Kumar  
**Group Role:** Lead Data Analyst & Visualization Designer (Descriptive Statistics, Frequency Distributions, Normalization, Outlier & Influence Diagnostics, Categorical Analysis, ANOVA, Regression Modeling, Multivariate EDA, and Visual Storytelling)  
**Collaborators:** Pranav (Data Organization & Preprocessing), Krish (Reporting & Synthesis)  
**Research Study Topic:** *Investigating the Impact of Sleep Patterns, Digital Screen Time, Physical Activity, and Study Habits on Academic Performance and Student Well-Being*

---

### Abstract & Alignment with Course Curriculum
This notebook presents an end-to-end exploratory and inferential data analysis of primary survey data collected from university students ($N=55$ valid responses). The investigation applies core theoretical concepts and computational workflows across all units of the **Data Handling & Visualization** course:
- **Unit 1:** Data Classification (Cross-sectional, Qualitative vs Quantitative, Univariate vs Multivariate) & Survey Sampling Evaluation.
- **Unit 2:** Organization of Data, Basic Descriptive Statistics (Central Tendency & Dispersion), Categorical Data Analysis ($\chi^2$, Cramér's V), ANOVA ($F$-statistic, $\eta^2$), Correlation Analysis (Pearson $r$ vs Spearman $\rho$), and Linear Regression.
- **Unit 3:** Normalization Techniques (Min-Max Scaling vs Z-Score Standardization) & Diagnostic Evaluation of Outliers, Leverage ($h_{ii}$), and Influential Points (Cook's Distance $D_i$).
- **Unit 4:** Principles of Data Visualization, Tabular Representation (Frequency Tables with Class Intervals & Cumulative Frequencies), and Graphical Representations (Histograms, Frequency Polygons, and Less-than/More-than Ogives for graphical median determination).
- **Unit 5:** Categorical & Continuous Visualizations (Violin, Box, and Strip plots), Exploratory Graphical Analysis, and Multivariate Faceted Visualizations (FacetGrids, Joint Interactions).
- **Unit 6:** Tool Integration (Python: Matplotlib, Seaborn, Scipy, Statsmodels), Publication-Quality Visual Design, and Executive Visual Storytelling Dashboard.
""")

# --- Unit 1: Environment & Ingestion ---
add_md("""
## 1. Environment Setup & Data Ingestion (Unit 1 & 2)

### 1.1 Data Taxonomy & Research Context (Unit 1)
- **Study Design:** Cross-Sectional Sample Survey collected via an online structured questionnaire.
- **Sampling Methodology:** Non-probability convenience and volunteer response sampling across engineering undergraduates.
- **Data Classification:**
  - **Quantitative Continuous:** `sleep_hours`, `recreational_screen_hours`, `social_media_hours`, `gaming_ott_hours`, `study_hours`, `cgpa`.
  - **Quantitative Discrete:** `workout_days_num` (days per week), `sports_hours_per_week`.
  - **Qualitative Ordinal (Likert Scales 1–5):** `sleep_quality`, `phone_distraction`, `study_consistency`, `stress_level`, `concentration`, `academic_productivity`, `mental_fatigue`.
  - **Qualitative Nominal:** `gender`, `year_of_study`, `bedtime`, `phone_before_sleep`, `activity_helps`.
  - **Derived Composite Indices:** `academic_score` (mean of productivity and concentration scaled to $0-100$), `wellbeing_score` (mean of reversed stress, reversed fatigue, and sleep quality scaled to $0-100$), `focus_score` (mean of concentration and reversed distraction scaled to $0-100$).
""")

add_code("""
# 1.1 Library Imports
import os, sys, re
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.multitest import multipletests
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 1.2 Publication-Grade Visualization Styling (Unit 4 & 6)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette('deep')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 14,
    'figure.titleweight': 'bold',
    'figure.dpi': 120
})

print("Environment configured successfully. Ready for analysis.")
""")

add_code("""
# 1.3 Dataset Ingestion (Connecting with Pranav's Preprocessing Pipeline)
df = pd.read_csv('cleaned_data.csv')

print(f"Dataset successfully loaded: {df.shape[0]} respondents, {df.shape[1]} variables.")
print("\nVariable Data Types Summary:")
print(df.dtypes.value_counts())
display(df[['year_of_study', 'gender', 'sleep_hours', 'study_hours', 'recreational_screen_hours', 'cgpa', 'academic_score']].head())
""")

with open('nb_step1.py', 'w', encoding='utf-8') as f:
    f.write("# Step 1 done\n")
print("Step 1 prepared.")
