import json

with open('Pranav.ipynb', 'r', encoding='utf-8') as f:
    pranav = json.load(f)

with open('pranav_dump.txt', 'w', encoding='utf-8') as out:
    for i, cell in enumerate(pranav['cells']):
        ctype = cell['cell_type']
        out.write(f'*** CELL {i} ({ctype}) ***\n')
        out.write(''.join(cell['source']))
        out.write('\n\n' + '='*40 + '\n\n')

print('Dumped', len(pranav['cells']), 'cells to pranav_dump.txt')
