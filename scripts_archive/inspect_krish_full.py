import json

with open('Krish.ipynb', 'r', encoding='utf-8') as f:
    krish = json.load(f)

for i in [0, 1, 2, 3]:
    print(f'*** CELL {i} ***')
    print(''.join(krish['cells'][i]['source'])[:1500])
    print('\n' + '='*50 + '\n')
