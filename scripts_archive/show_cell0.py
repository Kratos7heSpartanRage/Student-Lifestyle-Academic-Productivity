import json

with open('Krish.ipynb', 'r', encoding='utf-8') as f:
    krish = json.load(f)

print(''.join(krish['cells'][0]['source']))
