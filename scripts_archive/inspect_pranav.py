import json

with open('Pranav.ipynb', 'r', encoding='utf-8') as f:
    pranav = json.load(f)

print('PRANAV CELLS:', len(pranav['cells']))
for i, cell in enumerate(pranav['cells']):
    print(f'=== CELL {i} ({cell["cell_type"]}) ===')
    code = ''.join(cell['source'])
    print(code[:300] + ('...' if len(code) > 300 else ''))
