import pandas as pd

p1 = pd.read_csv('student_survey_processed (1).csv')
ci = pd.read_csv('cleaned_imputed.csv')

print('student_survey_processed (1).csv shape:', p1.shape)
print('cleaned_imputed.csv shape:', ci.shape)
print('\nstudent_survey_processed columns:', list(p1.columns))
print('\ncleaned_imputed columns:', list(ci.columns))
