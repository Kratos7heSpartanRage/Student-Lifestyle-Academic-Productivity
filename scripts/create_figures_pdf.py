import os
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

fig_base = next(p for p in ['figures/figures_eda', '../figures/figures_eda', 'figures_eda'] if os.path.exists(p))
out_pdf = 'reports/Mayank_Analysis_Figures.pdf' if os.path.exists('reports') else ('../reports/Mayank_Analysis_Figures.pdf' if os.path.exists('../reports') else 'Mayank_Analysis_Figures.pdf')
os.makedirs(os.path.dirname(out_pdf), exist_ok=True)

fig_files = [
    ('eda_fig01_frequency_polygon_ogive.png', 'Figure 1: Tabular Representation, Frequency Polygon and Ogives (Unit 4)'),
    ('eda_fig02_normalization_comparison.png', 'Figure 2: Normalization Techniques — Raw vs Min-Max vs Z-Score Standardization (Unit 3)'),
    ('eda_fig03_outliers_leverage_cooks.png', 'Figure 3: Outliers, Leverage (Hat Values), and Influential Points (Cooks Distance) (Unit 3)'),
    ('eda_fig04_descriptive_distributions.png', 'Figure 4: Outcome Distributions across Lifestyle Habits — Violin, Box, and Strip Plots (Unit 5)'),
    ('eda_fig05_categorical_crosstabs.png', 'Figure 5: Categorical Data Analysis — Contingency Tables and Stacked Bar Charts (Unit 2 & 5)'),
    ('eda_fig06_correlation_heatmap_annotated.png', 'Figure 6: Spearman Rank Correlation Matrix with Significance Annotations (Unit 2)'),
    ('eda_fig07_anova_group_comparisons.png', 'Figure 7: One-Way ANOVA and Group Differences across Lifestyle Categories (Unit 2)'),
    ('eda_fig08_regression_diagnostics.png', 'Figure 8: Multiple Linear Regression 4-Panel Diagnostic Suite (Unit 2 & 3)'),
    ('eda_fig09_multivariate_interactions.png', 'Figure 9: Multivariate Faceted Visualization — Study Hours vs CGPA by Consistency (Unit 5)'),
    ('eda_fig10_executive_storytelling_dashboard.png', 'Figure 10: Executive Visual Storytelling Dashboard (Unit 6)')
]

with PdfPages(out_pdf) as pdf:
    for fname, title in fig_files:
        img_path = os.path.join(fig_base, fname)
        if os.path.exists(img_path):
            img = mpimg.imread(img_path)
            h, w = img.shape[0], img.shape[1]
            aspect = w / h
            fig, ax = plt.subplots(figsize=(11, 11 / aspect if aspect > 1 else 8.5))
            ax.imshow(img)
            ax.axis('off')
            ax.set_title(title, fontsize=12, fontweight='bold', pad=12)
            plt.tight_layout()
            pdf.savefig(fig, bbox_inches='tight', dpi=150)
            plt.close(fig)
            print(f'Added {img_path} to PDF')

print(f'Successfully compiled {out_pdf}!')
