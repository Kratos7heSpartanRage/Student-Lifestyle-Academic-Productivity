# 📊 Student Lifestyle & Academic Productivity Analysis

> **A Comprehensive Empirical Investigation into Digital Distraction, Sleep Quality, Study Routine Consistency, and Academic Performance**  
> *Course Project for Data Handling & Visualization (IDHV) — Semester 5*

---

## 📌 Executive Summary

Modern university students face an increasingly complex digital landscape. Algorithmic social media feeds, on-demand streaming (OTT), late-night smartphone usage, and irregular sleep schedules continuously compete with academic focus.

This project delivers an **end-to-end data science lifecycle investigation** into how daily lifestyle parameters relate to, predict, and impact academic concentration, mental fatigue, perceived productivity, and cumulative GPA (CGPA).

### Key Empirical Findings

1. **The Sleep Paradox (Quality over Quantity):**  
   Perceived sleep quality is a statistically significant, positive driver of concentration ($\rho = +0.41, p = 0.0036^{**}$) and academic productivity ($\rho = +0.38, p = 0.0048^{**}$). Conversely, total weekday sleep duration shows virtually zero direct association with CGPA ($\rho = -0.10, p = 0.535$). **Restful sleep architecture matters far more than raw hours spent in bed.**

2. **Routine Consistency Over Sheer Study Volume:**  
   In multiple linear regression modeling ($R^2 = 0.248, p = 0.0139^*$), **study routine consistency** is the single strongest positive predictor of academic performance ($\beta = +5.32, p = 0.013^*$). Raw daily study hours without consistency showed no statistically significant predictive power ($\beta = +0.48, p = 0.748$).

3. **The Digital Distraction Hazard:**  
   Recreational screen time (>6 hrs/day) and bedtime smartphone use severely exacerbate phone distraction while studying ($F = 5.70, p = 0.0059^{**}, \eta^2 = 0.186$, a large effect size) and significantly degrade nocturnal sleep quality ($\chi^2 = 12.72, p = 0.0476^*$).

4. **Consistency Moderates Study Returns (Multivariate Trellis Analysis):**  
   Among students with inconsistent routines (Consistency Levels 1–2), additional study hours do not correlate with higher CGPA. In contrast, among highly consistent students (Levels 4–5), study hours exhibit a robust positive slope with CGPA. **Habitual consistency is the prerequisite that unlocks academic returns from study time.**

---

## 👥 Group Members & Contribution Breakdown

In accordance with course guidelines, the project responsibilities were distributed as follows:

| Group Member | Primary Module & Role | Core Contributions & Deliverables |
| :--- | :--- | :--- |
| **M. Pranav** | **Data Preprocessing & Data Hygiene** *(Section 3)* | Survey data extraction, standardization of variables, missingness diagnostics (MCAR/MAR/MNAR patterns), median/mode imputation protocols, and non-imputation policy for sensitive CGPA records. Documented in `Pranav.ipynb` and Section 3 of the final report. |
| **K. Krish** | **Study Formulation, Methodology & Administration** *(Sections 1 & 2)* | Research question definition, sampling frame design (simple random sampling of college cohort), literature review, thematic questionnaire construction via Google Forms, and survey administration. Documented in `Krish.ipynb` and Sections 1 & 2 of the final report. |
| **Mayank Kumar** | **Exploratory Data Analysis, Statistical Modeling & Visualizations** *(Sections 4, 5 & Appendix)* | Comprehensive EDA covering Units 1–6: descriptive stats, frequency tables & ogives with graphical median derivation, Min-Max vs Z-score normalization, outlier/leverage diagnostics, categorical $\chi^2$ tests, One-Way ANOVA, Benjamini-Hochberg FDR-corrected correlations, multiple linear regression with 4-panel diagnostics, multivariate trellis conditioning, executive dashboard, publication-grade figures, and complete report compilation (`Mayank.ipynb`, Section 4, 5, and Appendix). |

---

## 📚 Course Syllabus Alignment (Units 1 to 6)

This project serves as a comprehensive demonstration of the entire Data Handling & Visualization syllabus:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SYLLABUS MAPPING OVERVIEW                             │
├───────────┬─────────────────────────────────────────────────────────────────┤
│ Unit 1    │ Introduction to Data, Questionnaire Design, Measurement Scales │
│ Unit 2    │ Descriptive Statistics, Hypothesis Testing, Correlation & ANOVA │
│ Unit 3    │ Data Preprocessing, Normalization, Outliers & Leverage (Cook's) │
│ Unit 4    │ Tabular Representation, Frequency Polygons & Ogive Median       │
│ Unit 5    │ Advanced Visualizations (Violin/Box/Strip, Faceted Trellis)     │
│ Unit 6    │ Visual Storytelling & Executive Decision Dashboard              │
└───────────┴─────────────────────────────────────────────────────────────────┘
```

- **Unit 1 — Data Collection & Questionnaire Design:** Structured 21-item questionnaire distributed digitally via Google Forms capturing continuous ratio (hours, CGPA), qualitative nominal (gender, bedtime window), and qualitative ordinal data (1–5 Likert scales).
- **Unit 2 — Descriptive Statistics & Inferential Tests:** Central tendency (Mean, Median, Mode), dispersion (Std Dev, Variance, Range, IQR), Fisher-Pearson skewness, Pearson's $\chi^2$ tests of independence, One-Way ANOVA with Levene homogeneity testing, Kruskal-Wallis non-parametric tests, and Benjamini-Hochberg FDR multiple-testing correction across 66 bivariate hypotheses.
- **Unit 3 — Data Preprocessing & Diagnostics:** Implementation and empirical comparison of Min-Max Scaling $[0, 1]$ versus Z-Score Standardization; univariate outlier identification via Tukey's IQR fences ($Q_3 + 1.5 \times \text{IQR}$); regression leverage diagnostics via Hat-matrix diagonals ($h_{ii}$ vs $2(p+1)/n$); and influential case evaluation via Cook's Distance ($D_i$).
- **Unit 4 — Tabular Representation & Frequency Distributions:** Continuous grouped frequency distribution tables with class intervals, midpoints, relative frequencies, percentages, less-than and more-than cumulative frequencies; frequency polygons; and **graphical derivation of empirical medians** via ogive intersection at $CF = N/2 = 24.0$.
- **Unit 5 — Advanced Visualizations & Distributions:** Multi-layered distribution displays (combining kernel probability density Violins, quartile Boxplots, and individual observation Stripplots); categorical contingency stacked charts; and 5-panel multivariate faceted regression trellis grids conditioning on routine consistency.
- **Unit 6 — Visual Storytelling & Executive Dashboard:** Designed an integrated 4-panel executive dashboard delivering actionable, evidence-based recommendations tailored for students, academic counselors, and university administrators.

---

## 🗂️ Repository Architecture

The project directory is structured cleanly into modular folders:

```text
Course Project/
│
├── README.md                           # Comprehensive project documentation
├── .gitignore                          # Standard Python, Jupyter, OS & Office ignore rules
│
├── IDHV_Project_Complete.docx          # Primary Final Report (Sections 1-6 with bordered tables & figures)
├── Mayank.ipynb                        # Primary Executed Notebook (28 cells covering Units 1-6)
├── Mayank_Analysis_Figures.pdf         # Publication-grade vector PDF of all 10 figures
├── cleaned_data.csv                    # Cleaned & range-sanitized dataset with composite scores (N=48)
├── raw_data.csv                        # Original raw survey submissions (N=60)
│
├── data/                               # Data storage
│   ├── raw/                            # Raw response CSV files
│   ├── processed/                      # Preprocessed & imputed datasets
│   └── tables/                         # Exported CSV frequency and descriptive tables
│
├── figures/                            # Visual artifacts
│   ├── figures_eda/                    # High-resolution (300 DPI) publication PNGs (Figures 1 to 10)
│   └── Mayank_Analysis_Figures.pdf     # Vector PDF compilation
│
├── notebooks/                          # Team member notebooks
│   ├── Mayank.ipynb                    # Complete EDA, modeling, and visualization suite
│   ├── Pranav.ipynb                    # Data cleaning, missing data analysis & imputation
│   └── Krish.ipynb                     # Study formulation & survey administration
│
├── reports/                            # Documentation drafts
│   ├── IDHV_Project_Complete.docx      # Complete report deliverable
│   ├── IDHV Project.docx               # Base collaborative draft
│   └── Project_Report.pdf              # Preliminary report draft
│
└── scripts_archive/                    # Automated build and styling utilities
    ├── build_final_report.py           # Production Word report generator
    ├── report_styles.py                # Table boundary, cell margin & typography engine
    └── organize_dir.py                 # Directory structuring utility
```

---

## 📋 Primary Deliverables Catalog

| File | Type | Description |
| :--- | :--- | :--- |
| [`IDHV_Project_Complete.docx`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/IDHV_Project_Complete.docx) | Word Document (~1.7 MB) | Comprehensive course report containing Sections 1–6 with embedded bordered tables, zebra striping, and 10 high-resolution figures. |
| [`Mayank.ipynb`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/Mayank.ipynb) | Jupyter Notebook (~2.5 MB) | Fully executed 28-cell notebook with all statistical tests, tabular outputs, markdown narratives, and inline visualizations covering Units 1 to 6. |
| [`Mayank_Analysis_Figures.pdf`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/Mayank_Analysis_Figures.pdf) | Vector PDF (~2.2 MB) | Standalone vector PDF compiling all 10 figures with academic title headers and italic captions. |
| [`cleaned_data.csv`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/cleaned_data.csv) | CSV Dataset (~12 KB) | Cleaned, validated, and range-sanitized dataset with composite scores and behavioral index features ($N = 48$). |
| [`raw_data.csv`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/raw_data.csv) | CSV Dataset (~10 KB) | Original raw survey responses ($N = 60$) exported directly from Google Forms. |

---

## 🖼️ Figures Suite Summary

All 10 figures are located in [`figures/figures_eda/`](file:///Ubuntu-24.04/home/mayank_kumar_388/Courses/Sem%205/Data%20Handling%20&%20Visualization/Course%20Project/figures/figures_eda/):

1. **Figure 1:** Tabular Representation, Frequency Polygons, and Cumulative Ogives with Graphical Median Derivation *(Unit 4)*
2. **Figure 2:** Normalization Techniques — Comparing Raw vs Min-Max $[0, 1]$ vs Z-Score Standardization *(Unit 3)*
3. **Figure 3:** Diagnostic Analysis of Outliers, Leverage ($h_{ii}$), and Influential Cases (Cook's Distance) *(Unit 3)*
4. **Figure 4:** Multi-Layered Outcome Distributions Across Lifestyle Categories (Violin + Box + Strip) *(Unit 5)*
5. **Figure 5:** Categorical Contingency Testing & Stacked Percentage Visualizations *(Units 2 & 5)*
6. **Figure 6:** Spearman Rank Correlation Matrix with Significance Asterisks & FDR Thresholds *(Unit 2)*
7. **Figure 7:** One-Way Analysis of Variance (ANOVA) & Group Hypotheses with $\eta^2$ Effect Sizes *(Unit 2)*
8. **Figure 8:** Multiple Linear Regression 4-Panel Diagnostic Suite (Residuals, Q-Q, Scale-Location, Leverage) *(Units 2 & 3)*
9. **Figure 9:** Multivariate Faceted Visualization — Study Hours vs CGPA across Routine Consistency Levels *(Unit 5)*
10. **Figure 10:** Executive Visual Storytelling Dashboard for Academic Stakeholders *(Unit 6)*

---

## ⚙️ Environment Setup & Reproducibility

### Prerequisites
- Python 3.10 or 3.11+
- Virtual environment tool (`venv` or `conda`)

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/student-lifestyle-academic-productivity.git
cd student-lifestyle-academic-productivity

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # On Linux/macOS/WSL
# or: .\venv\Scripts\activate  # On Windows PowerShell

# Install required dependencies
pip install pandas numpy scipy statsmodels matplotlib seaborn python-docx pypdf jupyter
```

### Running the Analysis
To view and run the complete analytical notebook:

```bash
jupyter notebook Mayank.ipynb
```

To re-generate the complete formatted Word report with table borders and embedded figures:

```bash
python scripts_archive/build_final_report.py
```

---

## 📜 Academic Integrity & Course Information

- **Institution:** University Course Project
- **Course:** Data Handling & Visualization (IDHV)
- **Academic Term:** Semester 5, Fall 2026
- **License:** Educational & Academic Use Only.
