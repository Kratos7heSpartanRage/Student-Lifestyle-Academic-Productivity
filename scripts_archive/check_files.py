import shutil, os, pandas as pd

# Check raw file
if not os.path.exists('raw_data.csv'):
    shutil.copy('Data - Form responses 1.csv', 'raw_data.csv')
    print('Created raw_data.csv from Data - Form responses 1.csv')
else:
    print('raw_data.csv already exists')

# Check cleaned files
print('Checking cleaned files...')
if os.path.exists('cleaned_data.csv'):
    print('cleaned_data.csv exists, shape:', pd.read_csv('cleaned_data.csv').shape)
else:
    print('cleaned_data.csv does NOT exist yet')

if os.path.exists('cleaned_imputed.csv'):
    print('cleaned_imputed.csv exists, shape:', pd.read_csv('cleaned_imputed.csv').shape)
