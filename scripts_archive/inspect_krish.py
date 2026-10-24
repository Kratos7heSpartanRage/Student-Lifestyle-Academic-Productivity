import json, sys

with open('Krish.ipynb', 'r', encoding='utf-8') as f:
    krish = json.load(f)

print('KRISH CELLS:', len(krish['cells']))
for i, cell in enumerate(krish['cells']):
    print(f'=== CELL {i} ({cell["cell_type"]}) ===')
    print(''.join(cell['source']))
