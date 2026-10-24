import os, shutil, glob

# 1. Remove garbage folders and files
garbage_dirs = [d for d in os.listdir('.') if 'Users' in d or 'makku' in d]
for gd in garbage_dirs:
    if os.path.isdir(gd):
        shutil.rmtree(gd, ignore_errors=True)
        print("Removed stray dir:", gd)

# Remove Zone.Identifier files
for f in glob.glob('*Zone.Identifier*') + glob.glob('*/*Zone.Identifier*'):
    try:
        os.remove(f)
        print("Removed:", f)
    except:
        pass

# 2. Create organized directories
dirs = ['notebooks', 'reports', 'figures', 'data/raw', 'data/processed', 'data/tables', 'scripts_archive']
for d in dirs:
    os.makedirs(d, exist_ok=True)

# 3. Copy / Move Notebooks
for nb in ['Mayank.ipynb', 'Pranav.ipynb', 'Krish.ipynb']:
    if os.path.exists(nb):
        shutil.copy2(nb, os.path.join('notebooks', nb))
        print("Copied to notebooks/:", nb)

# 4. Copy / Move Reports
for r in ['IDHV_Project_Complete.docx', 'IDHV Project.docx', 'Project_Report.pdf']:
    if os.path.exists(r):
        shutil.copy2(r, os.path.join('reports', r))
        print("Copied to reports/:", r)

# 5. Copy / Move Figures
for fig_pdf in ['Mayank_Analysis_Figures.pdf', 'figures.pdf']:
    if os.path.exists(fig_pdf):
        shutil.copy2(fig_pdf, os.path.join('figures', fig_pdf))
        print("Copied to figures/:", fig_pdf)

if os.path.exists('figures_eda') and not os.path.exists('figures/figures_eda'):
    shutil.copytree('figures_eda', 'figures/figures_eda')
    print("Copied figures_eda/ to figures/figures_eda/")

# 6. Copy / Move Data
raw_files = ['raw_data.csv', 'Data - Form responses 1.csv']
for rf in raw_files:
    if os.path.exists(rf):
        shutil.copy2(rf, os.path.join('data/raw', rf))
        print("Copied to data/raw/:", rf)

proc_files = ['cleaned_data.csv', 'cleaned_imputed.csv', 'student_survey_processed (1).csv']
for pf in proc_files:
    if os.path.exists(pf):
        shutil.copy2(pf, os.path.join('data/processed', pf))
        print("Copied to data/processed/:", pf)

tbl_files = ['descriptive_statistics.csv', 'freq_table_study_hours.csv', 'freq_table_sleep_hours.csv']
for tf in tbl_files:
    if os.path.exists(tf):
        shutil.copy2(tf, os.path.join('data/tables', tf))
        print("Copied to data/tables/:", tf)

# 7. Move temporary scratch scripts into scripts_archive/
scratch_patterns = ['*.py', '*.txt', '*.ipynb']
keep_root = {'Mayank.ipynb', 'raw_data.csv', 'cleaned_data.csv', 'IDHV_Project_Complete.docx', 'Mayank_Analysis_Figures.pdf'}

for f in os.listdir('.'):
    if f in keep_root or f in dirs or f in ['figures_eda', '__pycache__', 'data']:
        continue
    if os.path.isfile(f):
        shutil.move(f, os.path.join('scripts_archive', f))
        print("Moved to scripts_archive/:", f)

if os.path.exists('__pycache__'):
    shutil.rmtree('__pycache__', ignore_errors=True)

print("\nDIRECTORY REORGANIZATION COMPLETE!")
