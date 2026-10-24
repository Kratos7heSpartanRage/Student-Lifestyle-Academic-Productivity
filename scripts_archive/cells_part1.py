import nbformat as nbf

cells_1 = []

cells_1.append(nbf.v4.new_markdown_cell(r"""# Course Project: Exploratory Data Analysis & Statistical Modeling
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
"""))

cells_1.append(nbf.v4.new_markdown_cell(r"""## 1. Environment Setup & Data Ingestion (Unit 1 & 2)

### 1.1 Data Taxonomy & Research Context (Unit 1)
- **Study Design:** Cross-Sectional Sample Survey collected via an online structured questionnaire.
- **Sampling Methodology:** Non-probability convenience and volunteer response sampling across engineering undergraduates.
- **Data Classification:**
  - **Quantitative Continuous:** `sleep_hours`, `recreational_screen_hours`, `social_media_hours`, `gaming_ott_hours`, `study_hours`, `cgpa`.
  - **Quantitative Discrete:** `workout_days_num` (days per week), `sports_hours_per_week`.
  - **Qualitative Ordinal (Likert Scales 1–5):** `sleep_quality`, `phone_distraction`, `study_consistency`, `stress_level`, `concentration`, `academic_productivity`, `mental_fatigue`.
  - **Qualitative Nominal:** `gender`, `year_of_study`, `bedtime`, `phone_before_sleep`, `activity_helps`.
  - **Derived Composite Indices:** `academic_score` (mean of productivity and concentration scaled to $0-100$), `wellbeing_score` (mean of reversed stress, reversed fatigue, and sleep quality scaled to $0-100$), `focus_score` (mean of concentration and reversed distraction scaled to $0-100$).
"""))

cells_1.append(nbf.v4.new_code_cell(r"""# 1.1 Library Imports
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
"""))

cells_1.append(nbf.v4.new_code_cell(r"""# 1.3 Dataset Ingestion (Connecting with Pranav's Preprocessing Pipeline)
# Load the cleaned dataset where impossible outliers were sanitized to NaN and features engineered
df = pd.read_csv('cleaned_data.csv')

print(f"Dataset successfully loaded: {df.shape[0]} respondents, {df.shape[1]} variables.")
print("\nVariable Data Types Summary:")
print(df.dtypes.value_counts())
display(df[['year_of_study', 'gender', 'sleep_hours', 'study_hours', 'recreational_screen_hours', 'cgpa', 'academic_score']].head())
"""))

cells_1.append(nbf.v4.new_markdown_cell(r"""## 2. Basic Descriptive Statistics: Measures of Central Tendency, Dispersion & Shape (Unit 2)

Descriptive statistics summarize the essential features of a dataset quantitatively. In accordance with Unit 2:
1. **Measures of Central Tendency:**
   - **Mean ($\bar{x}$):** Arithmetic average, sensitive to extreme outliers.
   - **Median:** 50th percentile, robust non-parametric measure of location.
   - **Mode:** Most frequently occurring value in the distribution.
2. **Measures of Dispersion:**
   - **Range:** Difference between maximum and minimum values ($x_{\max} - x_{\min}$).
   - **Variance ($s^2$) & Standard Deviation ($s$):** Average squared deviation from the mean, quantifying spread in original units.
   - **Interquartile Range ($IQR = Q_3 - Q_1$):** Spread of the central 50% of observations, resistant to extreme tails.
3. **Measures of Shape:**
   - **Fisher-Pearson Skewness ($\gamma_1$):** Quantifies asymmetry. Negative values indicate left-skew; positive indicate right-skew.
   - **Excess Kurtosis ($\gamma_2$):** Measures tail-heaviness relative to a normal distribution ($\gamma_2=0$).
"""))

cells_1.append(nbf.v4.new_code_cell(r"""# 2.1 Comprehensive Descriptive Statistics Calculation
num_vars = ['sleep_hours', 'recreational_screen_hours', 'social_media_hours',
            'gaming_ott_hours', 'study_hours', 'cgpa',
            'sleep_quality', 'phone_distraction', 'study_consistency',
            'stress_level', 'concentration', 'academic_productivity', 'mental_fatigue',
            'academic_score', 'wellbeing_score', 'focus_score']

desc_records = []
for var in num_vars:
    s = df[var].dropna()
    mode_val = s.mode()
    mode_str = f"{mode_val.iloc[0]:.2f}" if not mode_val.empty else "N/A"
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    desc_records.append({
        'Variable': var,
        'N Valid': len(s),
        'Missing': df[var].isna().sum(),
        'Mean': round(s.mean(), 2),
        'Median': round(s.median(), 2),
        'Mode': mode_str,
        'Std Dev': round(s.std(), 2),
        'Variance': round(s.var(), 2),
        'IQR': round(iqr, 2),
        'Min': round(s.min(), 2),
        'Max': round(s.max(), 2),
        'Range': round(s.max() - s.min(), 2),
        'Skewness': round(stats.skew(s, bias=False), 2),
        'Kurtosis': round(stats.kurtosis(s, bias=False), 2)
    })

desc_df = pd.DataFrame(desc_records)
desc_df.to_csv('descriptive_statistics.csv', index=False)
display(desc_df)
"""))

cells_1.append(nbf.v4.new_markdown_cell(r"""## 3. Tabular Representation & Frequency Curves (Unit 4)

A central requirement of **Unit 4 (Introduction to Data Visualization)** is the transition from raw microdata to grouped tabular and graphical frequency representations:
1. **Frequency Distribution Table:** Partitioning continuous variables into mutually exclusive, exhaustive class intervals $[a, b)$, and tabulating:
   - Class Midpoints ($x_i = \frac{a+b}{2}$)
   - Absolute Frequencies ($f_i$)
   - Relative Frequencies ($f_i / N$) and Percentages ($\frac{f_i}{N} \times 100$)
   - Cumulative Frequencies: **Less-than ($CF_<$)** and **More-than ($CF_>$)**
2. **Frequency Polygon:** A line graph formed by connecting the midpoints of the histogram bin tops, anchored to the x-axis at adjacent empty class midpoints.
3. **Cumulative Frequency Curves (Ogives):**
   - The **Less-than Ogive** ascends monotonically, plotting upper class boundaries against cumulative frequencies below that limit.
   - The **More-than Ogive** descends monotonically, plotting lower class boundaries against cumulative frequencies above or equal to that limit.
   - **Graphical Determination of Median:** The x-coordinate of the intersection point between the Less-than and More-than Ogives corresponds exactly to the 50th percentile (Median, where $CF = N/2$).
"""))

cells_1.append(nbf.v4.new_code_cell(r"""# 3.1 Frequency Distribution Tables Construction (Unit 4)
def generate_frequency_table(series, var_name, num_bins=7):
    clean_s = series.dropna()
    counts, edges = np.histogram(clean_s, bins=num_bins)
    total = len(clean_s)
    
    rows = []
    cum_less = 0
    for i in range(len(counts)):
        lo = edges[i]
        hi = edges[i+1]
        mid = (lo + hi) / 2.0
        f = counts[i]
        cum_less += f
        cum_more = total - (cum_less - f)
        rel_f = f / total
        rows.append({
            'Class Interval': f'[{lo:.2f} - {hi:.2f})',
            'Lower Bound': lo,
            'Upper Bound': hi,
            'Midpoint (xi)': round(mid, 2),
            'Frequency (fi)': f,
            'Relative Freq': round(rel_f, 3),
            'Percentage (%)': round(rel_f * 100, 1),
            'Less-Than CF': cum_less,
            'More-Than CF': cum_more
        })
    ft = pd.DataFrame(rows)
    return ft, edges, counts

ft_study, edges_study, counts_study = generate_frequency_table(df['study_hours'], 'Study Hours', num_bins=7)
ft_sleep, edges_sleep, counts_sleep = generate_frequency_table(df['sleep_hours'], 'Sleep Hours', num_bins=6)

print("=== Table 1: Frequency Distribution Table for Daily Study Hours (Unit 4) ===")
display(ft_study[['Class Interval', 'Midpoint (xi)', 'Frequency (fi)', 'Percentage (%)', 'Less-Than CF', 'More-Than CF']])

print("\n=== Table 2: Frequency Distribution Table for Weekday Sleep Hours (Unit 4) ===")
display(ft_sleep[['Class Interval', 'Midpoint (xi)', 'Frequency (fi)', 'Percentage (%)', 'Less-Than CF', 'More-Than CF']])
"""))

cells_1.append(nbf.v4.new_code_cell(r"""# 3.2 Visualizing Frequency Polygons and Ogives (Unit 4)
fig, axes = plt.subplots(2, 2, figsize=(15, 11))

# --- Panel 1: Study Hours Histogram & Frequency Polygon ---
ax = axes[0, 0]
mids_study = ft_study['Midpoint (xi)'].tolist()
bin_w = edges_study[1] - edges_study[0]
ax.bar(mids_study, counts_study, width=bin_w*0.88, color='#3B82F6', alpha=0.55, edgecolor='black', label='Grouped Frequency (Histogram)')
poly_x = [edges_study[0] - bin_w/2] + mids_study + [edges_study[-1] + bin_w/2]
poly_y = [0] + list(counts_study) + [0]
ax.plot(poly_x, poly_y, color='#DC2626', marker='o', linewidth=2.5, label='Frequency Polygon')
ax.set_title('Study Hours/Day: Histogram & Frequency Polygon', fontsize=12)
ax.set_xlabel('Daily Study Hours outside class (hrs/day)')
ax.set_ylabel('Frequency (Number of Students)')
ax.legend(frameon=True)

# --- Panel 2: Study Hours Cumulative Ogives & Graphical Median ---
ax = axes[0, 1]
lt_x = [edges_study[0]] + list(edges_study[1:])
lt_y = [0] + ft_study['Less-Than CF'].tolist()
mt_x = [edges_study[0]] + list(edges_study[1:])
mt_y = [len(df['study_hours'].dropna())] + ft_study['More-Than CF'].tolist()[1:] + [0]

ax.plot(lt_x, lt_y, color='#059669', marker='s', linewidth=2.2, label='Less-than Ogive (Cumulative < Upper Bound)')
ax.plot(mt_x, mt_y, color='#D97706', marker='^', linewidth=2.2, label='More-than Ogive (Cumulative >= Lower Bound)')

n_half_study = len(df['study_hours'].dropna()) / 2.0
med_study = df['study_hours'].median()
ax.axhline(n_half_study, color='#4F46E5', linestyle='--', alpha=0.8, label=f'N / 2 = {n_half_study:.1f}')
ax.axvline(med_study, color='#4F46E5', linestyle='--', alpha=0.8, label=f'Empirical Median = {med_study:.2f} hrs')
ax.plot(med_study, n_half_study, marker='*', markersize=15, color='#FBBF24', markeredgecolor='black', label='Intersection Point (Median)')
ax.set_title('Study Hours: Less-than & More-than Ogives', fontsize=12)
ax.set_xlabel('Daily Study Hours')
ax.set_ylabel('Cumulative Frequency (Students)')
ax.legend(fontsize=9, frameon=True)

# --- Panel 3: Sleep Hours Histogram & Frequency Polygon ---
ax = axes[1, 0]
mids_sleep = ft_sleep['Midpoint (xi)'].tolist()
bin_w_s = edges_sleep[1] - edges_sleep[0]
ax.bar(mids_sleep, counts_sleep, width=bin_w_s*0.88, color='#8B5CF6', alpha=0.55, edgecolor='black', label='Grouped Frequency (Histogram)')
poly_x_s = [edges_sleep[0] - bin_w_s/2] + mids_sleep + [edges_sleep[-1] + bin_w_s/2]
poly_y_s = [0] + list(counts_sleep) + [0]
ax.plot(poly_x_s, poly_y_s, color='#B91C1C', marker='o', linewidth=2.5, label='Frequency Polygon')
ax.set_title('Sleep Hours/Night: Histogram & Frequency Polygon', fontsize=12)
ax.set_xlabel('Weekday Sleep Duration (hrs/night)')
ax.set_ylabel('Frequency (Number of Students)')
ax.legend(frameon=True)

# --- Panel 4: Sleep Hours Cumulative Ogives & Graphical Median ---
ax = axes[1, 1]
lt_x_s = [edges_sleep[0]] + list(edges_sleep[1:])
lt_y_s = [0] + ft_sleep['Less-Than CF'].tolist()
mt_x_s = [edges_sleep[0]] + list(edges_sleep[1:])
mt_y_s = [len(df['sleep_hours'].dropna())] + ft_sleep['More-Than CF'].tolist()[1:] + [0]

ax.plot(lt_x_s, lt_y_s, color='#059669', marker='s', linewidth=2.2, label='Less-than Ogive')
ax.plot(mt_x_s, mt_y_s, color='#D97706', marker='^', linewidth=2.2, label='More-than Ogive')

n_half_sleep = len(df['sleep_hours'].dropna()) / 2.0
med_sleep = df['sleep_hours'].median()
ax.axhline(n_half_sleep, color='#4F46E5', linestyle='--', alpha=0.8)
ax.axvline(med_sleep, color='#4F46E5', linestyle='--', alpha=0.8)
ax.plot(med_sleep, n_half_sleep, marker='*', markersize=15, color='#FBBF24', markeredgecolor='black', label=f'Intersection Median = {med_sleep:.2f} hrs')
ax.set_title('Sleep Hours: Less-than & More-than Ogives', fontsize=12)
ax.set_xlabel('Weekday Sleep Duration (hrs/night)')
ax.set_ylabel('Cumulative Frequency (Students)')
ax.legend(fontsize=9, frameon=True)

plt.suptitle('Unit 4: Tabular Representation & Frequency Curves (Histograms, Polygons, and Ogives)', fontsize=14, y=1.02)
plt.tight_layout()
os.makedirs('figures_eda', exist_ok=True)
fig.savefig('figures_eda/eda_fig01_frequency_polygon_ogive.png', bbox_inches='tight')
plt.show()
print("Figure 1 generated and saved successfully.")
"""))

print("cells_part1 ready with", len(cells_1), "cells.")
