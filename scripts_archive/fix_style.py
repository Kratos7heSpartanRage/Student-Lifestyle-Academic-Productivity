with open('build_complete_docx.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace("table.style = 'Light Shading' if 'Light Shading' in [s.name for s in doc.styles] else 'Table Grid'", "table.style = 'TableNormal'")
with open('build_complete_docx.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated table style to TableNormal in build_complete_docx.py")
