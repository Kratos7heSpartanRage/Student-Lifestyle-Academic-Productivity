# Fix \n in python files
for fname in ['cells_part1.py', 'cells_part2.py', 'cells_part3.py']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    # Replace nbf.v4.new_code_cell(""" with nbf.v4.new_code_cell(r"""
    content = content.replace('nbf.v4.new_code_cell("""', 'nbf.v4.new_code_cell(r"""')
    content = content.replace('nbf.v4.new_markdown_cell("""', 'nbf.v4.new_markdown_cell(r"""')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {fname} with raw strings.")
