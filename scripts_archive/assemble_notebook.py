import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import sys, os

from cells_part1 import cells_1
from cells_part2 import cells_2
from cells_part3 import cells_3

all_cells = cells_1 + cells_2 + cells_3

nb = nbf.v4.new_notebook()
nb.cells = all_cells

with open('Mayank.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully assembled Mayank.ipynb with {len(all_cells)} cells. Now executing all cells...")

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

with open('Mayank.ipynb', 'r', encoding='utf-8') as f:
    nb_to_run = nbf.read(f, as_version=4)

try:
    ep.preprocess(nb_to_run, {'metadata': {'path': '.'}})
    with open('Mayank.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_to_run, f)
    print("ALL CELLS IN Mayank.ipynb EXECUTED AND SAVED WITH OUTPUTS EMBEDDED!")
except Exception as e:
    print("Execution error:", e)
