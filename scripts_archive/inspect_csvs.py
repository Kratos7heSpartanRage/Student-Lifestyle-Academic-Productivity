import pandas as pd
for fname in ['Data - Form responses 1.csv', 'cleaned_imputed.csv', 'student_survey_processed (1).csv']:
    try:
        df = pd.read_csv(fname)
        print(f'*** {fname} ***')
        print('Shape:', df.shape)
        print('Columns:', list(df.columns))
        print('Sample head:\n', df.head(2))
        print('\n' + '-'*50 + '\n')
    except Exception as e:
        print(f'Error reading {fname}: {e}')
