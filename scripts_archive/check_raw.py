import pandas as pd
import numpy as np

raw = pd.read_csv('Data - Form responses 1.csv')
print('Raw shape:', raw.shape)

# Let's inspect the columns and missing values in raw
print('Missing per column in raw:')
print(raw.isnull().sum())
print('\nMissing per row:')
print(raw.isnull().sum(axis=1).value_counts().sort_index())
