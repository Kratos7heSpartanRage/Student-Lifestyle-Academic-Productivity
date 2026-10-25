import os
from PIL import Image

def generate_pdf():
    candidates = ['figures/figures_eda', '../figures/figures_eda', 'figures_eda', '/home/mayank_kumar_388/Courses/Sem 5/Data Handling & Visualization/Course Project/figures/figures_eda']
    fig_dir = next((p for p in candidates if os.path.exists(p)), None)
    if not fig_dir:
        raise FileNotFoundError('figures_eda directory not found.')
    
    out_pdf = 'reports/analysis_figures.pdf'
    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    
    files = [
        'eda_fig01_frequency_polygon_ogive.png',
        'eda_fig02_normalization_comparison.png',
        'eda_fig03_outliers_leverage_cooks.png',
        'eda_fig04_descriptive_distributions.png',
        'eda_fig05_categorical_crosstabs.png',
        'eda_fig06_correlation_heatmap_annotated.png',
        'eda_fig07_anova_group_comparisons.png',
        'eda_fig08_regression_diagnostics.png',
        'eda_fig09_multivariate_interactions.png',
        'eda_fig10_executive_storytelling_dashboard.png'
    ]
    
    imgs = [Image.open(os.path.join(fig_dir, f)).convert('RGB') for f in files]
    imgs[0].save(out_pdf, save_all=True, append_images=imgs[1:], resolution=150.0)
    print(f'Successfully compiled {out_pdf} with all 10 figures ({round(os.path.getsize(out_pdf)/(1024*1024), 2)} MB)!')

if __name__ == '__main__':
    generate_pdf()
